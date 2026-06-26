"""Machine Design & Elements track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on designing machine components that
carry load reliably. Starts from the design process, stress and factor of safety,
builds through stress concentration, fatigue, shaft and bearing/gear design, and
reaches bolted and welded joints, springs, and probabilistic reliability with
optimization. Lessons are `text` with LaTeX, interactive ```plot blocks (S-N
curves, Goodman lines, bearing life, deflection, convergence), ```mermaid design
workflows and runnable ```python/```matlab code.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, ε, τ, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Machine Design & Elements — Basics ───────────────────────────────────────

_BASICS = SeedCourse(
    slug="machine-design-basics",
    title="Machine Design & Elements — Basics",
    description=(
        "The intuition and fundamentals of machine design: the iterative design "
        "process, loads and the static stresses they cause, the factor of safety "
        "and the design equation, why stress concentrations and fluctuating loads "
        "matter, how materials and standards are selected, and the common machine "
        "elements (shafts, bearings, gears, fasteners, springs, joints). "
        "Interactive plots and diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The machine design process",
            "10 min",
            r"""
# The machine design process

**Machine design** turns a functional need into a manufacturable set of
components that carry their loads safely, cheaply and for long enough.
It is **iterative**: you rarely get geometry, material and tolerances right on
the first pass. The classic Shigley loop is recognise the need, define the
problem, synthesise a concept, **analyse** (statics, stress, deflection),
**evaluate** against requirements, then iterate and finally document.

Two threads run through every loop: **failure prevention** (will it break, yield,
buckle, wear out or vibrate?) and **economics** (mass, material cost,
manufacturability). Good designers cycle quickly between rough hand calculations
and detailed analysis, tightening the design as confidence grows.

```mermaid
flowchart LR
  N["Recognise need"] --> P["Define problem & specs"]
  P --> C["Synthesise concept"]
  C --> A["Analyse: stress, deflection, life"]
  A --> E["Evaluate vs requirements"]
  E -->|"not OK"| C
  E -->|"OK"| D["Detail & document"]
```

A design *spec* fixes the targets: loads, environment, life (e.g. $10^7$
cycles), allowable deflection, cost and mass budgets. Everything downstream is
measured against it. Standards (ISO, ASME, AGMA, DIN) encode hard-won practice so
you do not reinvent safe proportions for every bolt, gear or shaft.

**Next:** the loads and the static stresses they create.
""",
        ),
        _t(
            "Loads and static stress",
            "11 min",
            r"""
# Loads and static stress

A machine element must first survive its **static** (steadily applied) loads.
Loads come as **axial** force, **bending** moment, **torsion** and **transverse
shear** — often several at once. Each produces a characteristic stress:

$$\sigma_{\text{axial}} = \frac{F}{A}, \quad
\sigma_{\text{bend}} = \frac{M c}{I}, \quad
\tau_{\text{tor}} = \frac{T r}{J}, \quad
\tau_{\text{shear}} = \frac{V Q}{I t}.$$

Within linear elasticity you **superpose** these at a point, then combine them
into an equivalent stress (von Mises) to compare with the material strength. The
key design insight: stress, not force, is what the material feels, so the same
load is dangerous in a thin section and harmless in a stout one.

```plot
{"title": "Bending stress vs applied moment (rect 20x40 mm)", "xLabel": "moment M (N*m)", "yLabel": "max stress sigma (MPa)", "xRange": [0, 200], "yRange": [0, 200], "grid": true, "functions": [{"expr": "0.9375*x", "label": "sigma = M c / I", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  L["Applied loads"] --> AX["Axial -> F/A"]
  L --> BD["Bending -> Mc/I"]
  L --> TO["Torsion -> Tr/J"]
  AX --> SP["Superpose at a point"]
  BD --> SP
  TO --> SP
  SP --> VM["Equivalent (von Mises) stress"]
```

Steady loads are only the start: most real machines see **fluctuating** loads,
which is why fatigue dominates later lessons.

**Next:** turning strength into a safe size — the factor of safety.
""",
        ),
        _t(
            "Factor of safety and the design equation",
            "10 min",
            r"""
# Factor of safety and the design equation

Designs never run at the failure stress. The **factor of safety** (FoS, $n$)
compares a strength measure against the actual stress:

$$n = \frac{S}{\sigma}, \qquad \sigma_{\text{allow}} = \frac{S}{n},$$

where $S$ is usually the yield strength $S_y$ for ductile parts (or ultimate
$S_{ut}$ for brittle ones). The **design equation** states that the equivalent
stress must stay below the allowable: $\sigma \le S/n$. Rearranged, it sizes the
part directly.

How big should $n$ be? It encodes everything you *don't* know: load
uncertainty, material scatter, analysis accuracy, consequences of failure.
Typical values run ~1.25-1.5 for well-known aerospace loads up to 3-5 for civil
or shock-loaded machinery. Larger $n$ means a bigger, heavier, costlier part —
safety trades against weight:

```plot
{"title": "Allowable stress vs factor of safety (Sy = 350 MPa)", "xLabel": "factor of safety n", "yLabel": "allowable stress (MPa)", "xRange": [1, 6], "yRange": [0, 360], "grid": true, "functions": [{"expr": "350/x", "label": "sigma_allow = Sy / n", "color": "#2563eb"}]}
```

Modern practice splits the lumped FoS into **partial factors** on loads and on
resistance (ASME, Eurocode LRFD), better matching each source of uncertainty.

```mermaid
flowchart LR
  S["Strength S (Sy or Sut)"] --> DIV["Divide by FoS n"]
  DIV --> AL["Allowable stress"]
  AL --> SZ["Size part: sigma <= S / n"]
```

**Next:** why a notch can halve the strength — stress concentration.
""",
        ),
        _t(
            "Stress concentration and notches",
            "10 min",
            r"""
# Stress concentration and notches

Real parts have holes, fillets, keyways and shoulders. At these geometric
discontinuities the stress spikes far above the nominal value. The **stress
concentration factor** captures it:

$$\sigma_{\max} = K_t\,\sigma_{\text{nom}},$$

where $K_t$ depends only on geometry (the ratio of fillet radius to width, hole
size to plate width, etc.) and is read from standard **Peterson charts**. A small
hole in a wide plate gives $K_t \approx 3$ — a tripling of stress at the hole
edge. Sharp re-entrant corners are worse; generous fillet radii are the cheapest
fix:

```plot
{"title": "Kt for a filleted shoulder vs radius ratio r/d", "xLabel": "fillet radius ratio r/d", "yLabel": "stress concentration factor Kt", "xRange": [0.02, 0.3], "yRange": [1, 3], "grid": true, "functions": [{"expr": "1 + 0.6/sqrt(x)*0.2", "label": "Kt decreases as r grows", "color": "#dc2626"}]}
```

For **ductile** materials under **static** load, local yielding redistributes the
peak, so $K_t$ is often ignored statically. But under **fatigue** (and always for
brittle materials), the notch governs life through the fatigue notch factor $K_f$.

```mermaid
flowchart LR
  G["Geometry: hole, fillet, keyway"] --> KT["Kt from Peterson chart"]
  KT --> PK["sigma_max = Kt * sigma_nom"]
  PK --> ST["Static + ductile -> often ignore"]
  PK --> FT["Fatigue / brittle -> critical (Kf)"]
```

**Next:** the loads that come and go — fluctuating loads and fatigue intuition.
""",
        ),
        _t(
            "Fluctuating loads and fatigue intuition",
            "11 min",
            r"""
# Fluctuating loads and fatigue intuition

Most machine elements fail not from one big overload but from **fatigue** —
damage accumulated under many cycles of load far below the static strength. A
rotating shaft, a vibrating bracket, a gear tooth: each sees a stress that
**fluctuates** in time. We describe it by its **mean** and **amplitude**:

$$\sigma_m = \frac{\sigma_{\max}+\sigma_{\min}}{2}, \qquad
\sigma_a = \frac{\sigma_{\max}-\sigma_{\min}}{2}.$$

Plot stress amplitude against the number of cycles to failure $N_f$ on log axes
and you get the **S-N (Wöhler) curve**. Steels show an **endurance limit**
$S_e$ (around half the ultimate strength) below which life is effectively
infinite; aluminium has no true limit and keeps declining:

```plot
{"title": "S-N curve: stress amplitude vs log cycles", "xLabel": "log10(cycles to failure)", "yLabel": "stress amplitude (MPa)", "xRange": [3, 8], "yRange": [100, 500], "grid": true, "functions": [{"expr": "650 - 70*x", "label": "finite-life region", "color": "#dc2626"}, {"expr": "200", "label": "endurance limit Se", "color": "#16a34a"}]}
```

The practical message: design against the *amplitude* of the fluctuating stress,
keep it below $S_e$ for infinite life, and treat notches, surface finish and size
as life-killers. Fatigue is the leading cause of in-service mechanical failure.

```mermaid
flowchart LR
  F["Fluctuating load"] --> M["Mean stress sigma_m"]
  F --> A["Amplitude sigma_a"]
  A --> SN["Compare to S-N / endurance limit Se"]
  SN --> LIFE["Predict life Nf"]
```

**Next:** the toolbox of machine elements you will design.
""",
        ),
        _t(
            "Machine elements: shafts, bearings, gears, fasteners",
            "10 min",
            r"""
# Machine elements: shafts, bearings, gears, fasteners

Machines are assembled from a small vocabulary of standardised **elements**.
Learn the family and most designs become a matter of selecting and sizing:

- **Shafts** transmit torque and carry rotating parts; sized against combined
  bending + torsion fatigue and against deflection.
- **Bearings** support rotating shafts: **rolling-element** (selected by rated
  life $L_{10}$) or **hydrodynamic journal** (designed by film thickness).
- **Gears** transmit motion and power between shafts; designed against tooth
  **bending** (Lewis/AGMA) and surface **contact** (pitting) stress.
- **Fasteners** (bolts, screws) clamp parts; designed by **preload** so the joint
  carries load without separating or fatiguing.
- **Springs** store energy and provide controlled force/deflection.
- **Joints**: welded, riveted or bonded, designed for the stress in the joint.

```mermaid
flowchart TB
  ME["Machine elements"] --> SH["Shafts"]
  ME --> BE["Bearings"]
  ME --> GE["Gears"]
  ME --> FA["Fasteners"]
  ME --> SP["Springs"]
  ME --> JO["Joints (weld/rivet)"]
```

Each element has a governing failure mode and a standard design procedure. The
amount of material a transmitted power demands grows with torque; for a solid
shaft, diameter scales as roughly the cube root of torque:

```plot
{"title": "Required shaft diameter vs torque (tau_allow fixed)", "xLabel": "torque T (N*m)", "yLabel": "diameter d (mm)", "xRange": [0, 500], "yRange": [0, 50], "grid": true, "functions": [{"expr": "6*x^(1/3)", "label": "d ~ (16 T / pi tau)^(1/3)", "color": "#2563eb"}]}
```

**Next:** the Intermediate course — quantitative fatigue, shafts, bearings, gears.
""",
        ),
        _quiz(),
    ),
)


# ── Machine Design & Elements — Intermediate ─────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="machine-design-intermediate",
    title="Machine Design & Elements — Intermediate",
    description=(
        "The core quantitative methods of machine design: building the corrected "
        "endurance limit with Marin factors, the mean-stress fatigue criteria "
        "(Goodman, Gerber, Soderberg), shaft design under combined fluctuating "
        "loads (ASME/DE-Goodman), rolling-element bearing selection by L10 life, "
        "spur-gear bending and contact stress, and bolted-joint preload analysis. "
        "Worked equations, plots and Python computations throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Endurance limit and Marin factors",
            "12 min",
            r"""
# Endurance limit and Marin factors

The S-N curve from a polished lab specimen overstates the strength of a real
part. We start from the **uncorrected endurance limit**, estimated from the
ultimate strength:

$$S_e' \approx 0.5\,S_{ut} \quad (S_{ut} \le 1400\ \text{MPa}).$$

Then we *derate* it with the **Marin factors** to get the part's corrected
endurance limit:

$$S_e = k_a\,k_b\,k_c\,k_d\,k_e\,S_e',$$

where $k_a$ is surface finish, $k_b$ size, $k_c$ load type, $k_d$ temperature and
$k_e$ reliability. Each is below 1 — a rough, large, reliable part can lose half
its lab endurance limit.

```python
import numpy as np

Sut = 700.0                       # MPa
Se_prime = 0.5*Sut
ka = 4.51*Sut**-0.265             # machined surface (Shigley a,b)
kb = 0.85                         # size (medium shaft)
kc = 1.0                          # bending
kd = 1.0                          # room temperature
ke = 0.814                        # 99% reliability
Se = ka*kb*kc*kd*ke*Se_prime
print(f"Se' = {Se_prime:.0f} MPa, ka = {ka:.2f}, Se = {Se:.0f} MPa")
```

```plot
{"title": "Surface factor ka vs ultimate strength (machined)", "xLabel": "Sut (MPa)", "yLabel": "surface factor ka", "xRange": [300, 1400], "yRange": [0.5, 1], "grid": true, "functions": [{"expr": "4.51*x^(-0.265)", "label": "ka = a * Sut^b", "color": "#2563eb"}]}
```

The corrected $S_e$ is the foundation for every fatigue calculation that follows.

**Next:** combining mean and alternating stress — the failure criteria.
""",
        ),
        _t(
            "Mean stress: Goodman, Gerber, Soderberg",
            "12 min",
            r"""
# Mean stress: Goodman, Gerber, Soderberg

Fatigue depends on both the alternating stress $\sigma_a$ and the mean stress
$\sigma_m$. A positive (tensile) mean stress reduces life. The **mean-stress
criteria** draw a safe envelope on the $\sigma_m$-$\sigma_a$ plane:

$$\text{Goodman:}\ \frac{\sigma_a}{S_e}+\frac{\sigma_m}{S_{ut}}=\frac{1}{n}, \quad
\text{Soderberg:}\ \frac{\sigma_a}{S_e}+\frac{\sigma_m}{S_y}=\frac{1}{n},$$

with **Gerber** using a parabola, $\frac{n\sigma_a}{S_e}+\left(\frac{n\sigma_m}{S_{ut}}\right)^2=1$.
Goodman (a straight line to $S_{ut}$) is the common, slightly conservative design
choice; Soderberg (to $S_y$) is most conservative; Gerber best fits ductile data.

```plot
{"title": "Goodman line: safe sigma_a vs sigma_m (Se=200, Sut=700)", "xLabel": "mean stress sigma_m (MPa)", "yLabel": "alternating stress sigma_a (MPa)", "xRange": [0, 700], "yRange": [0, 220], "grid": true, "functions": [{"expr": "200*(1 - x/700)", "label": "Goodman boundary (n=1)", "color": "#dc2626"}]}
```

```python
def goodman_n(sa, sm, Se, Sut):
    return 1.0/(sa/Se + sm/Sut)

Se, Sut = 200.0, 700.0
sa, sm = 90.0, 120.0              # MPa
n = goodman_n(sa, sm, Se, Sut)
print(f"factor of safety (Goodman) = {n:.2f}")
```

A point inside the line is safe; on it, $n=1$. These criteria convert a
fluctuating stress state into a single factor of safety against fatigue.

**Next:** applying it to a rotating shaft.
""",
        ),
        _t(
            "Shaft design under combined loading",
            "13 min",
            r"""
# Shaft design under combined loading

A rotating shaft carrying a steady transverse load sees **fully reversed
bending** (alternating) plus **steady torsion** (mean shear). Combining the
distortion-energy equivalent stresses with the Goodman criterion gives the
**ASME / DE-Goodman** shaft-sizing equation for diameter $d$:

$$\frac{1}{n} = \frac{16}{\pi d^3}\left(\frac{2(K_f M_a)}{S_e}
+ \frac{\sqrt{3}\,(K_{fs} T_m)}{S_{ut}}\right),$$

where $M_a$ is the alternating bending moment, $T_m$ the mean torque, and
$K_f,K_{fs}$ the fatigue stress-concentration factors at the critical section
(usually a shoulder fillet or keyway). Solve for $d$ to size the shaft.

```python
import numpy as np

Ma = 250.0        # N*m alternating bending
Tm = 340.0        # N*m mean torque
Kf, Kfs = 1.7, 1.5
Se, Sut = 210e6, 700e6     # Pa
n = 2.0
term = (16*n/np.pi)*(2*Kf*Ma/Se + np.sqrt(3)*Kfs*Tm/Sut)
d = term**(1/3)
print(f"required shaft diameter d = {d*1e3:.1f} mm")
```

```plot
{"title": "Required diameter vs target factor of safety", "xLabel": "factor of safety n", "yLabel": "diameter d (mm)", "xRange": [1, 4], "yRange": [0, 60], "grid": true, "functions": [{"expr": "30*x^(1/3)", "label": "d ~ n^(1/3)", "color": "#2563eb"}]}
```

After strength, **check deflection and critical speed**: shafts often fail
serviceability (excess slope at bearings, whirl near a natural frequency) before
they fail in fatigue. Standard diameters are then rounded up to stock sizes.

**Next:** the bearings the shaft runs in.
""",
        ),
        _t(
            "Rolling-element bearing life",
            "12 min",
            r"""
# Rolling-element bearing life

Rolling-element bearings are selected, not designed from scratch, using
catalogue ratings. The **basic dynamic load rating** $C$ is the load giving one
million revolutions of rated life for 90% of bearings. The **L10 life** (the life
90% will reach) follows a power law:

$$L_{10} = \left(\frac{C}{P}\right)^{a}\ \text{(millions of revolutions)},$$

with $a=3$ for ball bearings and $10/3$ for roller bearings, and $P$ the
**equivalent dynamic load** $P=X F_r + Y F_a$ combining radial and axial forces.
Doubling the load cuts a ball bearing's life roughly eightfold:

```plot
{"title": "Ball-bearing L10 life vs load ratio C/P", "xLabel": "load ratio C/P", "yLabel": "L10 life (million revs)", "xRange": [1, 6], "yRange": [0, 220], "grid": true, "functions": [{"expr": "x^3", "label": "L10 = (C/P)^3", "color": "#16a34a"}]}
```

```python
def l10_hours(C, P, rpm, a=3.0):
    L10_rev = (C/P)**a          # million revolutions
    return L10_rev*1e6/(rpm*60.0)

C = 30e3      # N rated dynamic capacity
P = 8e3       # N equivalent load
rpm = 1500
print(f"L10 = {l10_hours(C, P, rpm):.0f} hours")
```

For non-standard reliability use the life-adjustment factor $a_1$ (e.g. $L_5$,
$L_1$). Hydrodynamic **journal** bearings are a different discipline: designed via
the Sommerfeld number and minimum film thickness so metal never touches metal.

**Next:** the gears that connect shafts.
""",
        ),
        _t(
            "Spur gear bending and contact stress",
            "13 min",
            r"""
# Spur gear bending and contact stress

A spur gear tooth has two failure modes. **Bending fatigue** at the tooth root
is governed by the modified Lewis / AGMA equation:

$$\sigma_b = \frac{W_t\,K_v\,K_o}{F\,m\,Y},$$

where $W_t$ is the transmitted tangential load, $m$ the module, $F$ the face
width, $Y$ the Lewis form factor and $K_v,K_o$ dynamic and overload factors.
**Surface (contact) fatigue** — pitting — follows the Hertzian AGMA contact
stress:

$$\sigma_c = C_p\sqrt{\frac{W_t\,K_v}{F\,d_p\,I}},$$

with $C_p$ an elastic coefficient and $I$ a geometry factor. The tangential load
itself comes from the power and pitch-line velocity, $W_t = P/V$.

```python
import numpy as np

P = 15e3                # W transmitted power
n_rpm = 1200            # pinion speed
dp = 0.075              # m pitch diameter
V = np.pi*dp*n_rpm/60   # m/s pitch-line velocity
Wt = P/V                # N tangential load
m = 0.004               # module (m)
F = 0.040               # face width (m)
Y = 0.34                # Lewis form factor (~20 teeth)
Kv, Ko = 1.3, 1.25
sigma_b = Wt*Kv*Ko/(F*m*Y)/1e6
print(f"Wt = {Wt:.0f} N, bending stress sigma_b = {sigma_b:.1f} MPa")
```

```plot
{"title": "Tooth bending stress vs face width (fixed load)", "xLabel": "face width F (mm)", "yLabel": "bending stress sigma_b (MPa)", "xRange": [10, 60], "yRange": [0, 300], "grid": true, "functions": [{"expr": "3000/x", "label": "sigma_b ~ 1 / F", "color": "#dc2626"}]}
```

Design checks **both** modes against the gear material's allowable bending and
contact strengths; pitting often governs hardened gears.

**Next:** clamping it all together — bolted joints and preload.
""",
        ),
        _t(
            "Bolted joints and preload",
            "12 min",
            r"""
# Bolted joints and preload

A bolted joint is designed by its **preload** $F_i$, not just the external load.
Tightening stretches the bolt (stiffness $k_b$) and squeezes the members
(stiffness $k_m$). They share an external load $P$ by the **joint stiffness
constant**:

$$C = \frac{k_b}{k_b+k_m}, \qquad
F_{\text{bolt}} = C\,P + F_i, \qquad
F_{\text{member}} = (1-C)\,P - F_i.$$

Because members are much stiffer than the slender bolt ($C \approx 0.2$-$0.3$),
most external load is carried by *relieving member compression* — the bolt sees
only a fraction of $P$, which is exactly why preload makes joints fatigue-proof.
Recommended preload is $F_i = 0.75\,F_p$ (reusable) or $0.90\,F_p$ (permanent),
where $F_p = A_t S_p$ is the proof load.

```python
At = 84.3e-6      # m^2 tensile stress area (M12)
Sp = 600e6        # Pa proof strength (grade 8.8)
Fp = At*Sp
Fi = 0.75*Fp
kb, km = 1.0, 4.0           # relative stiffnesses
C = kb/(kb+km)
P = 8e3                     # N external tensile load
F_bolt = C*P + Fi
print(f"proof load Fp = {Fp/1e3:.1f} kN, preload Fi = {Fi/1e3:.1f} kN")
print(f"C = {C:.2f}, bolt force = {F_bolt/1e3:.1f} kN")
```

```plot
{"title": "Bolt force vs external load (preloaded, C=0.2)", "xLabel": "external load P (kN)", "yLabel": "bolt force (kN)", "xRange": [0, 20], "yRange": [0, 45], "grid": true, "functions": [{"expr": "37.9 + 0.2*x", "label": "F_bolt = Fi + C P", "color": "#2563eb"}]}
```

Joint separation occurs when $P_0 = F_i/(1-C)$ — keep the working load well below
it.

**Next:** the Advanced course — springs, welds, reliability and optimization.
""",
        ),
        _quiz(),
    ),
)


# ── Machine Design & Elements — Advanced ─────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="machine-design-advanced",
    title="Machine Design & Elements — Advanced",
    description=(
        "State-of-the-art and applied machine design: helical compression spring "
        "design and surge, fatigue of welded joints by the structural hot-spot "
        "and notch-stress methods, fracture mechanics and damage-tolerant design, "
        "probabilistic and reliability-based design (stress-strength interference), "
        "design optimization, and a digital-twin / ML-surrogate workflow for "
        "predictive maintenance. Equations, plots and Python throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Helical compression spring design",
            "13 min",
            r"""
# Helical compression spring design

A helical compression spring trades load for deflection. Its **rate** (stiffness)
depends on wire diameter $d$, mean coil diameter $D$, active coils $N_a$ and the
shear modulus $G$:

$$k = \frac{G\,d^4}{8\,D^3\,N_a}.$$

The wire carries **torsional shear stress**, amplified at the inner coil by the
**Wahl factor** $K_W$ that corrects for curvature and direct shear:

$$\tau = K_W\,\frac{8\,F\,D}{\pi\,d^3}, \qquad
K_W = \frac{4C-1}{4C-4} + \frac{0.615}{C}, \quad C=\frac{D}{d}.$$

```python
import numpy as np

G = 79.3e9        # Pa music wire
d = 0.0030        # m wire diameter
D = 0.024         # m mean coil diameter
Na = 8.0
k = G*d**4/(8*D**3*Na)
C = D/d
Kw = (4*C-1)/(4*C-4) + 0.615/C
F = 120.0         # N
tau = Kw*8*F*D/(np.pi*d**3)/1e6
print(f"rate k = {k:.0f} N/m, C = {C:.1f}, Kw = {Kw:.2f}, tau = {tau:.0f} MPa")
```

```plot
{"title": "Spring force vs deflection (linear rate)", "xLabel": "deflection x (mm)", "yLabel": "force F (N)", "xRange": [0, 30], "yRange": [0, 300], "grid": true, "functions": [{"expr": "9.7*x", "label": "F = k x", "color": "#2563eb"}]}
```

Dynamic springs must also avoid **surge** — resonance of the coil as a wave
medium — so the natural frequency is kept well above the forcing frequency.
Buckling and solid-height stress complete the design checks.

**Next:** fatigue of welded joints.
""",
        ),
        _t(
            "Fatigue of welded joints",
            "13 min",
            r"""
# Fatigue of welded joints

Welds are the Achilles' heel of fabricated structures: the weld toe is a sharp
notch full of residual tensile stress and defects, so fatigue cracks start there
regardless of base-metal strength. Codes (IIW, Eurocode 3, AWS) classify each
detail into a **FAT class** — the stress range (MPa) giving $2\times10^6$ cycles —
and apply a common S-N slope ($m=3$):

$$N = \frac{C}{(\Delta\sigma)^m}, \qquad \Delta\sigma_{FAT}=\text{class at }2\times10^6.$$

The modern approach is the **structural hot-spot stress**: extrapolate the
geometric stress to the weld toe (ignoring the singular notch peak), then enter a
single hot-spot S-N curve. The **effective notch stress** method ($r=1$ mm
fictitious radius) goes further for local FEA.

```python
import numpy as np

# Eurocode 3 detail category C = FAT 90 (MPa) at 2e6, slope m = 3
FAT = 90.0
m = 3.0
C = FAT**m * 2e6                 # S-N constant
for dS in (60.0, 90.0, 140.0):
    N = C/dS**m
    print(f"stress range {dS:.0f} MPa -> life {N:.2e} cycles")
```

```plot
{"title": "Weld S-N curve (FAT 90, slope m=3)", "xLabel": "log10(cycles N)", "yLabel": "stress range (MPa)", "xRange": [4, 8], "yRange": [40, 300], "grid": true, "functions": [{"expr": "10^((log(2e6*90^3)/log(10) - x)/3)", "label": "log dS = (log C - log N)/3", "color": "#dc2626"}]}
```

Life is improved by **post-weld treatments** (toe grinding, TIG dressing, HFMI
peening) that blunt the notch and add compressive residual stress.

**Next:** designing with cracks present — fracture mechanics.
""",
        ),
        _t(
            "Fracture mechanics and damage tolerance",
            "13 min",
            r"""
# Fracture mechanics and damage tolerance

Real parts contain flaws. **Linear elastic fracture mechanics (LEFM)** describes
the stress field at a crack tip by the **stress intensity factor**:

$$K = Y\,\sigma\sqrt{\pi a},$$

where $a$ is crack length and $Y$ a geometry factor. The crack runs unstably when
$K$ reaches the material's **fracture toughness** $K_{Ic}$, giving the **critical
crack size** $a_c = (K_{Ic}/(Y\sigma))^2/\pi$. **Damage-tolerant design** assumes
a crack exists and ensures it grows slowly and is found before $a_c$.

Sub-critical growth follows **Paris' law**:

$$\frac{da}{dN} = C\,(\Delta K)^m,$$

integrated to predict remaining life from an inspectable flaw to $a_c$.

```python
import numpy as np

C, m = 1.0e-11, 3.0       # Paris constants (mm/cycle, MPa*sqrt(m))
Y = 1.12
dsigma = 120.0            # MPa stress range
a = 0.001                 # m initial crack
da = 1e-6
N = 0.0
Kic = 50.0                # MPa*sqrt(m)
while Y*dsigma*np.sqrt(np.pi*a) < Kic:
    dK = Y*dsigma*np.sqrt(np.pi*a)
    a += C*dK**m*1e-3      # convert mm to m per cycle batch
    N += 1
print(f"cycles to critical crack: {N:.0f}, final a = {a*1e3:.2f} mm")
```

```plot
{"title": "Crack growth da/dN vs delta-K (Paris regime)", "xLabel": "log10(delta K)", "yLabel": "log10(da/dN)", "xRange": [0.5, 2], "yRange": [-9, -4], "grid": true, "functions": [{"expr": "3*x - 11", "label": "log(da/dN) = log C + m log dK", "color": "#16a34a"}]}
```

Inspection intervals are then set so at least two inspections fall between
detectable and critical crack size.

**Next:** putting numbers on safety — reliability-based design.
""",
        ),
        _t(
            "Reliability-based design",
            "12 min",
            r"""
# Reliability-based design

A deterministic factor of safety hides scatter. In **reliability-based design**,
load **stress** $S$ and **strength** $\Sigma$ are random variables, and failure is
the event $\Sigma < S$. The overlap of their distributions is the **stress-strength
interference**. For normal variables the **reliability** comes from the safety
margin and the coupled standard deviation:

$$z = \frac{\mu_\Sigma - \mu_S}{\sqrt{\sigma_\Sigma^2 + \sigma_S^2}}, \qquad
R = \Phi(z),$$

where $\Phi$ is the standard normal CDF and $z$ is the **reliability index**
$\beta$. A small overlap (large $\beta$) gives high reliability; reducing scatter
(better material control, tighter tolerances) is often cheaper than adding mass.

```python
import numpy as np
from scipy.stats import norm

mu_str, sd_str = 400.0, 30.0     # MPa strength
mu_str_load = 250.0
mu_S, sd_S = mu_str_load, 25.0   # MPa load stress
beta = (mu_str - mu_S)/np.hypot(sd_str, sd_S)
R = norm.cdf(beta)
print(f"reliability index beta = {beta:.2f}, reliability R = {R:.5f}")
print(f"probability of failure = {1-R:.2e}")
```

```plot
{"title": "Reliability vs safety margin (reliability index beta)", "xLabel": "reliability index beta", "yLabel": "reliability R", "xRange": [0, 4], "yRange": [0.5, 1], "grid": true, "functions": [{"expr": "0.5 + 0.5*(1 - exp(-0.7*x))", "label": "R = Phi(beta) (schematic)", "color": "#2563eb"}]}
```

This underpins FORM/SORM methods and reliability-based design optimization
(RBDO), where target $\beta$ becomes a constraint.

**Next:** automating the trade-offs — design optimization.
""",
        ),
        _t(
            "Design optimization",
            "13 min",
            r"""
# Design optimization

Machine design is a constrained optimization: minimise an **objective** (mass,
cost) over **design variables** (diameters, thicknesses) subject to
**constraints** (stress, deflection, fatigue, geometry). Formally:

$$\min_{\mathbf{x}} f(\mathbf{x}) \quad \text{s.t.}\quad
g_i(\mathbf{x}) \le 0,\ \ \mathbf{x}_L \le \mathbf{x} \le \mathbf{x}_U.$$

For a minimum-mass beam or shaft, gradient-based solvers (SQP) converge quickly;
discrete or multimodal problems use genetic algorithms or particle swarm.

```python
import numpy as np
from scipy.optimize import minimize

# Minimize mass of a cantilever (proportional to b*h) s.t. bending stress <= allow
L, P = 1.0, 2000.0          # m, N
sigma_allow = 150e6
def mass(x):
    b, h = x
    return b*h                 # proportional to volume per length
def stress_con(x):            # g <= 0
    b, h = x
    sigma = 6*P*L/(b*h**2)
    return sigma_allow - sigma  # >= 0 feasible
res = minimize(mass, [0.05, 0.10],
               constraints=[{"type": "ineq", "fun": stress_con}],
               bounds=[(0.01, 0.2), (0.01, 0.3)])
print(f"optimal b={res.x[0]*1e3:.1f} mm, h={res.x[1]*1e3:.1f} mm, area={res.fun*1e4:.2f} cm^2")
```

```plot
{"title": "Optimization convergence (objective vs iteration)", "xLabel": "iteration", "yLabel": "normalized objective", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "objective ~ exp(-0.4 k)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  X["Design variables x"] --> AN["Analysis: stress, life"]
  AN --> OBJ["Objective + constraints"]
  OBJ --> OPT["Optimizer step"]
  OPT -->|"not converged"| X
  OPT --> R["Optimal lightweight design"]
```

**Topology optimization** (SIMP) extends this to grow material only where load
flows, enabling generative, additively manufactured parts.

**Next:** keeping the design alive — digital twins and ML.
""",
        ),
        _t(
            "Digital twins and ML for predictive maintenance",
            "13 min",
            r"""
# Digital twins and ML for predictive maintenance

A modern machine element is designed once but *monitored* for life. A **digital
twin** is a calibrated physics model (often a reduced-order or FEA surrogate) fed
live sensor data — vibration, temperature, strain — to estimate the part's true
state and **remaining useful life (RUL)**.

The workflow couples a fast **ML surrogate** (trained on FEA/test data) for
real-time stress prediction with a damage model (Miner's rule, Paris' law) that
accumulates fatigue from the measured load history:

$$D = \sum_i \frac{n_i}{N_i} \le 1 \quad\text{(Palmgren-Miner)}.$$

```python
import numpy as np

# Rainflow-counted load blocks -> Miner damage and remaining life
cycles = np.array([2.0e5, 5.0e4, 1.0e4])      # counted cycles n_i
Nf     = np.array([2.0e6, 6.0e5, 9.0e4])      # life at each amplitude
D = np.sum(cycles/Nf)
RUL_fraction = (1.0 - D)/ (D)                  # blocks remaining at this rate
print(f"accumulated damage D = {D:.3f}")
print(f"remaining life ~ {RUL_fraction:.1f} more equivalent blocks")
```

```plot
{"title": "Predicted remaining useful life decaying with usage", "xLabel": "operating time (kh)", "yLabel": "remaining useful life (fraction)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.25*x)", "label": "RUL ~ exp(-lambda t)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  S["Sensors: vibration, strain"] --> SUR["ML surrogate -> stress"]
  SUR --> DM["Damage model (Miner / Paris)"]
  DM --> RUL["Remaining useful life"]
  RUL --> MAINT["Schedule maintenance"]
  MAINT --> S
```

This closes the loop from design through operation: machine elements become
condition-monitored, self-reporting components in a connected, optimized system.

**Next:** you have completed the Machine Design & Elements track.
""",
        ),
        _quiz(),
    ),
)


MACHINE_DESIGN_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MACHINE_DESIGN_COURSES"]
