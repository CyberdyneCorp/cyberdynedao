"""Mechanical Vibrations track: Basics -> Intermediate -> Advanced.

From single-DOF free and forced vibration through damping, resonance and
isolation, to multi-DOF modal analysis and continuous systems. Lessons are
`text` with single-backslash LaTeX, interactive ```plot blocks for time
responses and frequency-response curves, ```mermaid diagrams for method
workflows and system block diagrams, and runnable ```python (NumPy/SciPy)
and ```matlab code for integrating equations of motion and eigen-analysis.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


_BASICS = SeedCourse(
    slug="mechanical-vibrations-basics",
    title="Mechanical Vibrations — Basics",
    description=(
        "Build physical intuition for oscillation: the spring-mass-damper model, "
        "natural frequency, simple harmonic motion, free response and the meaning "
        "of damping. Lots of plots and worked numbers, minimal heavy math."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What vibration is and why it matters",
            "10 min",
            r"""
# What vibration is and why it matters

**Vibration** is the oscillatory motion of a system about an equilibrium position. It appears everywhere in engineering: an engine on its mounts, a bridge under traffic, a hard-disk read head, a turbine blade. Sometimes we exploit it (ultrasonic cleaners, vibratory feeders, MEMS resonators); far more often we fight it, because oscillating stress drives **fatigue**, noise and loss of precision.

Three ingredients let a system vibrate: **inertia** (mass $m$, stores kinetic energy), **elasticity** (stiffness $k$, stores potential energy), and **energy dissipation** (damping $c$, removes energy). The canonical model that captures all three is the single-degree-of-freedom (SDOF) spring-mass-damper.

A **degree of freedom (DOF)** is an independent coordinate needed to describe the configuration. A mass sliding on a rail is 1-DOF; a rigid body in a plane is 3-DOF. Counting DOFs sets the number of natural frequencies a system has.

```mermaid
flowchart LR
  A[Energy source] --> B[Inertia: mass m]
  B --> C[Elasticity: stiffness k]
  C --> D[Damping: c]
  D -->|dissipates| E[Heat]
  C -->|stores/returns| B
```

```plot
{"title": "A lightly damped free vibration", "xLabel": "t (s)", "yLabel": "x (mm)", "xRange": [0,10], "yRange": [-1,1], "grid": true, "functions": [{"expr": "exp(-0.2*x)*cos(3*x)", "label": "x(t)", "color": "#2563eb"}]}
```

**Next:** the spring-mass-damper model in equations.
""",
        ),
        _t(
            "The spring-mass-damper model",
            "12 min",
            r"""
# The spring-mass-damper model

Apply Newton's second law to a mass $m$ on a linear spring $k$ and viscous damper $c$, with displacement $x$ measured from static equilibrium. The spring pulls back with $-kx$, the damper resists with $-c\dot x$, so
$$m\ddot x + c\dot x + k x = F(t).$$
This single equation is the workhorse of vibration theory. With $F=0$ it describes **free** vibration; with $F(t)\neq 0$, **forced** vibration.

Dividing by $m$ exposes two defining parameters:
$$\ddot x + 2\zeta\omega_n\dot x + \omega_n^2 x = F/m,$$
where the **undamped natural frequency** $\omega_n=\sqrt{k/m}$ (rad/s) and the **damping ratio** $\zeta=\dfrac{c}{2\sqrt{km}}$ (dimensionless). Natural frequency in hertz is $f_n=\omega_n/2\pi$, period $T_n=1/f_n$.

Measuring $\omega_n$ from $m$ and $k$ is the first thing any vibration analysis does: it tells you which excitation frequencies are dangerous.

```mermaid
flowchart LR
  F[Force F t] --> S[Sum: m x'' + c x' + k x = F]
  S --> P1[omega_n = sqrt k over m]
  S --> P2[zeta = c over 2 sqrt k m]
```

```python
import numpy as np
m, k, c = 2.0, 800.0, 4.0          # kg, N/m, N.s/m
wn = np.sqrt(k/m)                   # rad/s
zeta = c/(2*np.sqrt(k*m))
print(f"wn={wn:.2f} rad/s, fn={wn/(2*np.pi):.2f} Hz, zeta={zeta:.3f}")
```

**Next:** undamped free vibration and simple harmonic motion.
""",
        ),
        _t(
            "Free vibration and simple harmonic motion",
            "12 min",
            r"""
# Free vibration and simple harmonic motion

Set $c=0$ and $F=0$: $m\ddot x + kx = 0$. The solution is pure **simple harmonic motion (SHM)**,
$$x(t) = A\cos(\omega_n t) + B\sin(\omega_n t) = X\cos(\omega_n t-\phi),$$
where $\omega_n=\sqrt{k/m}$. The constants $A,B$ (or amplitude $X$ and phase $\phi$) come from initial conditions $x(0)=x_0$, $\dot x(0)=v_0$: $A=x_0$, $B=v_0/\omega_n$, and $X=\sqrt{x_0^2+(v_0/\omega_n)^2}$.

The remarkable fact: the frequency depends only on $m$ and $k$, **not** on the amplitude. A mass pulled 1 mm or 10 mm oscillates at the same rate. Energy sloshes between kinetic ($\tfrac12 m\dot x^2$) and potential ($\tfrac12 k x^2$); the total stays constant because nothing dissipates it.

Worked number: $m=0.5\,$kg, $k=200\,$N/m gives $\omega_n=20\,$rad/s, $f_n\approx 3.18\,$Hz, $T_n\approx 0.31\,$s.

```plot
{"title": "Undamped SHM x(t) = cos(omega_n t)", "xLabel": "t (s)", "yLabel": "x", "xRange": [0,6], "yRange": [-1.2,1.2], "grid": true, "functions": [{"expr": "cos(3.14*x)", "label": "x(t)", "color": "#2563eb"}, {"expr": "0", "label": "equilibrium", "color": "#dc2626"}]}
```

```python
import numpy as np
m, k = 0.5, 200.0
wn = np.sqrt(k/m)
x0, v0 = 0.01, 0.0
t = np.linspace(0, 2, 400)
x = x0*np.cos(wn*t) + (v0/wn)*np.sin(wn*t)
print(f"fn={wn/(2*np.pi):.2f} Hz, amplitude={np.sqrt(x0**2+(v0/wn)**2)*1e3:.2f} mm")
```

**Next:** what damping does to the free response.
""",
        ),
        _t(
            "Damping and the decay of free vibration",
            "12 min",
            r"""
# Damping and the decay of free vibration

Re-introduce the damper. The character of the free response depends entirely on $\zeta$:

- **Underdamped** ($0<\zeta<1$): oscillation inside a decaying envelope, $x(t)=Xe^{-\zeta\omega_n t}\cos(\omega_d t-\phi)$, with **damped natural frequency** $\omega_d=\omega_n\sqrt{1-\zeta^2}$. Most machines live here.
- **Critically damped** ($\zeta=1$): returns to equilibrium fastest with no overshoot.
- **Overdamped** ($\zeta>1$): sluggish, non-oscillatory return.

The decaying envelope $e^{-\zeta\omega_n t}$ tells you how fast energy bleeds off. A practical measure is the **logarithmic decrement** $\delta=\ln\frac{x_i}{x_{i+1}}=\dfrac{2\pi\zeta}{\sqrt{1-\zeta^2}}$, found by reading the ratio of successive peaks — the standard way to estimate damping from a measured ring-down.

```plot
{"title": "Underdamped ring-down with envelope", "xLabel": "t (s)", "yLabel": "x", "xRange": [0,12], "yRange": [-1,1], "grid": true, "functions": [{"expr": "exp(-0.25*x)*cos(3*x)", "label": "x(t)", "color": "#2563eb"}, {"expr": "exp(-0.25*x)", "label": "envelope", "color": "#dc2626"}]}
```

```python
import numpy as np
# estimate zeta from two successive peaks
x1, x2 = 0.80, 0.52            # measured peak amplitudes
delta = np.log(x1/x2)          # log decrement
zeta = delta/np.sqrt(4*np.pi**2 + delta**2)
print(f"log decrement={delta:.3f}, zeta={zeta:.3f}")
```

**Next:** how the world pushes systems into forced vibration.
""",
        ),
        _t(
            "Forced vibration and resonance, intuitively",
            "11 min",
            r"""
# Forced vibration and resonance, intuitively

Drive the SDOF system with a harmonic force $F(t)=F_0\cos(\omega t)$. After transients die out, the mass settles into **steady-state** motion at the *driving* frequency $\omega$, not its own $\omega_n$:
$$x_{ss}(t)=X\cos(\omega t-\phi).$$
The steady amplitude depends on the frequency ratio $r=\omega/\omega_n$. When $r\approx 1$ the force pushes in step with the motion and amplitude balloons — this is **resonance**. Only damping keeps it finite; at $r=1$ the dynamic amplification is roughly $1/(2\zeta)$.

Think of pushing a swing: shove at the swing's own rhythm and small pushes build huge arcs; shove too fast or too slow and little happens. The whole job of vibration engineering is to keep operating frequencies away from $\omega_n$, or to add damping when you cannot.

```plot
{"title": "Amplification vs frequency ratio (zeta=0.1)", "xLabel": "r = omega/omega_n", "yLabel": "X / X_static", "xRange": [0,3], "yRange": [0,6], "grid": true, "functions": [{"expr": "1/sqrt((1-x^2)^2 + (0.2*x)^2)", "label": "magnification", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  A[Harmonic force F0 cos wt] --> B[Transient: dies with damping]
  A --> C[Steady state at drive freq w]
  C --> D{r near 1?}
  D -->|yes| E[Resonance: large X]
  D -->|no| F[Modest X]
```

**Next:** check your understanding of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


_INTERMEDIATE = SeedCourse(
    slug="mechanical-vibrations-intermediate",
    title="Mechanical Vibrations — Intermediate",
    description=(
        "The quantitative core: frequency response and the magnification factor, "
        "transmissibility and vibration isolation, base excitation and rotating "
        "unbalance, the tuned mass damper, and measurement of damping. NumPy/SciPy "
        "and MATLAB code throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Frequency response and the magnification factor",
            "13 min",
            r"""
# Frequency response and the magnification factor

For $m\ddot x+c\dot x+kx=F_0\cos\omega t$, substitute the steady-state ansatz $x=X\cos(\omega t-\phi)$. With $r=\omega/\omega_n$ the **dynamic magnification factor** is
$$M(r)=\frac{X}{X_{st}}=\frac{1}{\sqrt{(1-r^2)^2+(2\zeta r)^2}}, \qquad X_{st}=F_0/k,$$
and the phase lag
$$\phi=\tan^{-1}\!\frac{2\zeta r}{1-r^2}.$$
Three regimes: at $r\ll 1$ the response is stiffness-controlled ($M\to 1$, $\phi\to 0$); near $r=1$ it is damping-controlled with the peak $M_{max}\approx 1/(2\zeta)$ at $r=\sqrt{1-2\zeta^2}$; at $r\gg 1$ it is mass-controlled ($M\to 1/r^2$, $\phi\to 180^\circ$). The 90-degree phase crossing at $r=1$ is the cleanest experimental marker of resonance.

```plot
{"title": "Magnification factor for several damping ratios", "xLabel": "r = omega/omega_n", "yLabel": "M(r)", "xRange": [0,3], "yRange": [0,6], "grid": true, "functions": [{"expr": "1/sqrt((1-x^2)^2 + (0.1*x)^2)", "label": "zeta=0.05", "color": "#dc2626"}, {"expr": "1/sqrt((1-x^2)^2 + (0.4*x)^2)", "label": "zeta=0.2", "color": "#2563eb"}, {"expr": "1/sqrt((1-x^2)^2 + (x)^2)", "label": "zeta=0.5", "color": "#16a34a"}]}
```

```python
import numpy as np
zeta = 0.05
r = np.linspace(0.01, 3, 600)
M = 1/np.sqrt((1-r**2)**2 + (2*zeta*r)**2)
r_peak = np.sqrt(1-2*zeta**2)
print(f"peak M={M.max():.2f} near r={r_peak:.3f}; 1/(2z)={1/(2*zeta):.1f}")
```

**Next:** turning amplitude into transmitted force — isolation.
""",
        ),
        _t(
            "Transmissibility and vibration isolation",
            "13 min",
            r"""
# Transmissibility and vibration isolation

Mount a vibrating machine on springs and dampers: how much force reaches the floor? The **force transmissibility** is
$$T_r=\frac{F_{transmitted}}{F_0}=\sqrt{\frac{1+(2\zeta r)^2}{(1-r^2)^2+(2\zeta r)^2}}.$$
The key result: **all curves cross $T_r=1$ at $r=\sqrt 2$**. Isolation ($T_r<1$) happens only for $r>\sqrt 2$, i.e. when the forcing frequency is well above the mount's natural frequency. So you design a *soft* mount (low $\omega_n$) so that the operating speed sits far up the $r>\sqrt2$ region.

A twist: more damping helps near resonance but *worsens* isolation for $r>\sqrt2$. Practical mounts balance the two. The same transmissibility governs **displacement** transmissibility for base-excited systems.

```plot
{"title": "Transmissibility: isolation begins past r=sqrt(2)", "xLabel": "r = omega/omega_n", "yLabel": "T_r", "xRange": [0,4], "yRange": [0,5], "grid": true, "functions": [{"expr": "sqrt((1+(0.1*x)^2)/((1-x^2)^2+(0.1*x)^2))", "label": "zeta=0.05", "color": "#dc2626"}, {"expr": "sqrt((1+(0.6*x)^2)/((1-x^2)^2+(0.6*x)^2))", "label": "zeta=0.3", "color": "#2563eb"}, {"expr": "1", "label": "T_r = 1", "color": "#16a34a"}]}
```

```python
import numpy as np
# size a mount for 80% isolation of a 50 Hz machine
f_drive, target_T = 50.0, 0.20
r = np.sqrt(1/target_T + 1)            # undamped estimate, T = 1/(r^2-1)
fn = f_drive/r
k_over_m = (2*np.pi*fn)**2
print(f"need r={r:.2f}, fn={fn:.1f} Hz, k/m={k_over_m:.0f} (rad/s)^2")
```

**Next:** vibration that enters through the base.
""",
        ),
        _t(
            "Base excitation and rotating unbalance",
            "13 min",
            r"""
# Base excitation and rotating unbalance

Two ubiquitous forcing mechanisms reuse the same math.

**Base excitation:** the support moves as $y(t)=Y\cos\omega t$ (a vehicle on a wavy road, an instrument on a shaking floor). The mass displacement transmissibility equals the force transmissibility above, so again you want $r>\sqrt2$ to protect the mass.

**Rotating unbalance:** a machine of total mass $M$ carries an eccentric mass $m$ at radius $e$ spinning at $\omega$. The rotating component injects a force $m e\omega^2$, and the steady amplitude is
$$\frac{MX}{m e}=\frac{r^2}{\sqrt{(1-r^2)^2+(2\zeta r)^2}}.$$
Because the forcing grows as $\omega^2$, the response *rises* with speed and approaches the constant $me/M$ for $r\gg 1$ — a signature shape used in field balancing of fans, pumps and rotors (ISO 1940 / ISO 21940 balance grades).

```plot
{"title": "Rotating-unbalance response MX/(me)", "xLabel": "r = omega/omega_n", "yLabel": "MX/(me)", "xRange": [0,4], "yRange": [0,6], "grid": true, "functions": [{"expr": "x^2/sqrt((1-x^2)^2+(0.2*x)^2)", "label": "zeta=0.1", "color": "#dc2626"}, {"expr": "x^2/sqrt((1-x^2)^2+(x)^2)", "label": "zeta=0.5", "color": "#2563eb"}]}
```

```matlab
M = 50; m = 0.5; e = 0.02; wn = 60; zeta = 0.1;   % SI units
w  = linspace(0, 4*wn, 800);  r = w/wn;
X  = (m*e/M) .* r.^2 ./ sqrt((1-r.^2).^2 + (2*zeta*r).^2);
plot(r, M*X/(m*e)); xlabel('r'); ylabel('MX/(me)'); grid on
```

**Next:** killing a resonance by adding a second mass.
""",
        ),
        _t(
            "The tuned mass damper",
            "12 min",
            r"""
# The tuned mass damper

When you cannot move a structure's resonance away from the excitation, **add a small auxiliary system** tuned to absorb the energy. A **tuned mass damper (TMD)** — also dynamic vibration absorber — attaches a secondary mass $m_2$, spring $k_2$ and damper $c_2$ to the primary system.

For an undamped absorber tuned exactly to the disturbance ($\omega_2=\sqrt{k_2/m_2}=\omega$), the primary mass can be driven to *zero* steady amplitude: the absorber moves out of phase and its spring force cancels the applied force. In practice some damping is added and the absorber is tuned by **Den Hartog's optimum**: for mass ratio $\mu=m_2/m_1$,
$$\frac{\omega_2}{\omega_1}=\frac{1}{1+\mu}, \qquad \zeta_{opt}=\sqrt{\frac{3\mu}{8(1+\mu)^3}}.$$
Famous installations: the 660-tonne pendulum TMD in Taipei 101, and TMDs on the Millennium Bridge after its 2000 lateral-sway problem.

```mermaid
flowchart TB
  G[Disturbance F cos wt] --> M1[Primary m1 k1]
  M1 --> M2[Absorber m2 k2 c2]
  M2 -->|out-of-phase force| M1
```

```python
import numpy as np
mu = 0.05                                  # 5% mass ratio
f_ratio = 1/(1+mu)                         # optimal tuning
zeta_opt = np.sqrt(3*mu/(8*(1+mu)**3))     # Den Hartog
print(f"tune absorber to {f_ratio:.3f} x w1, zeta_opt={zeta_opt:.3f}")
```

**Next:** measuring damping and natural frequency in the lab.
""",
        ),
        _t(
            "Measuring damping and the half-power method",
            "12 min",
            r"""
# Measuring damping and the half-power method

You rarely know $\zeta$ from first principles; you measure it. Two standard methods:

**Time domain — logarithmic decrement.** From a free ring-down, $\delta=\frac{1}{n}\ln\frac{x_0}{x_n}$ over $n$ cycles, then $\zeta=\delta/\sqrt{4\pi^2+\delta^2}$. Robust and cheap.

**Frequency domain — half-power (3 dB) bandwidth.** Sweep a harmonic force and record the FRF magnitude. At the two frequencies $\omega_1<\omega_2$ where the response falls to $1/\sqrt2$ (i.e. $-3\,$dB) of the peak, the damping is
$$\zeta\approx\frac{\omega_2-\omega_1}{2\omega_n}=\frac{\Delta\omega}{2\omega_n}.$$
A sharp, narrow peak means light damping; a broad peak means heavy damping. This underpins experimental modal analysis and the **quality factor** $Q\approx 1/(2\zeta)$.

```plot
{"title": "Half-power bandwidth on an FRF peak", "xLabel": "r = omega/omega_n", "yLabel": "|H(r)|", "xRange": [0.5,1.5], "yRange": [0,6], "grid": true, "functions": [{"expr": "1/sqrt((1-x^2)^2+(0.1*x)^2)", "label": "|H|", "color": "#2563eb"}, {"expr": "3.5", "label": "peak / sqrt 2", "color": "#dc2626"}]}
```

```python
import numpy as np
w1, w2, wn = 96.0, 104.0, 100.0    # rad/s: half-power points and resonance
zeta = (w2 - w1)/(2*wn)
Q = 1/(2*zeta)
print(f"zeta={zeta:.3f}, Q={Q:.1f}")
```

**Next:** check your understanding of the quantitative methods.
""",
        ),
        _quiz(),
    ),
)


_ADVANCED = SeedCourse(
    slug="mechanical-vibrations-advanced",
    title="Mechanical Vibrations — Advanced",
    description=(
        "Multi-DOF and continuous systems: equations of motion in matrix form, the "
        "eigenvalue problem, mode shapes and modal superposition, vibration of "
        "strings and beams, plus the computational and data-driven side — FEA modal "
        "analysis, FRF identification and optimization of damping treatments."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Multi-DOF systems in matrix form",
            "14 min",
            r"""
# Multi-DOF systems in matrix form

Real structures have many coordinates. For $n$ DOFs, Newton's law (or Lagrange's equations) yields a coupled set written compactly as
$$\mathbf M\ddot{\mathbf x}+\mathbf C\dot{\mathbf x}+\mathbf K\mathbf x=\mathbf f(t),$$
with the **mass matrix** $\mathbf M$, **damping matrix** $\mathbf C$ and **stiffness matrix** $\mathbf K$ ($n\times n$, symmetric for conservative coupling). For a 2-mass chain $m_1\,$–$\,k_1\,$–$\,m_2\,$–$\,k_2$, the off-diagonal $-k_2$ terms express that the masses share a spring — they are **coupled**.

Assembling $\mathbf K$ from element stiffnesses is exactly how finite-element models are built: each spring/element contributes a small stiffness pattern that is summed into the global matrix. Coupling is what makes the free response a mixture of several frequencies rather than one clean sinusoid.

```mermaid
flowchart LR
  W1[Wall] -->|k1| M1[m1] -->|k2| M2[m2]
  M1 --> EQ[M xdd + K x = 0]
  M2 --> EQ
```

```python
import numpy as np
m1, m2, k1, k2 = 2.0, 1.0, 1000.0, 800.0
M = np.array([[m1, 0],[0, m2]])
K = np.array([[k1+k2, -k2],[-k2, k2]])
print("M=\n", M, "\nK=\n", K)
```

**Next:** solving the eigenvalue problem for natural frequencies.
""",
        ),
        _t(
            "The eigenvalue problem and mode shapes",
            "14 min",
            r"""
# The eigenvalue problem and mode shapes

Seek synchronous free motion $\mathbf x=\boldsymbol\phi\,e^{i\omega t}$ in $\mathbf M\ddot{\mathbf x}+\mathbf K\mathbf x=0$. This gives the **generalized eigenvalue problem**
$$(\mathbf K-\omega^2\mathbf M)\boldsymbol\phi=0,$$
with non-trivial solutions when $\det(\mathbf K-\omega^2\mathbf M)=0$. The $n$ roots $\omega_i^2$ are the **natural frequencies**; each eigenvector $\boldsymbol\phi_i$ is the corresponding **mode shape** — the relative deformation pattern when the structure rings at $\omega_i$. Mode 1 is usually the lowest, smoothest shape; higher modes have more nodes.

Mode shapes are **orthogonal** with respect to both $\mathbf M$ and $\mathbf K$: $\boldsymbol\phi_i^{\!\top}\mathbf M\boldsymbol\phi_j=0$ for $i\neq j$. That orthogonality is the key that decouples the system in the next lesson.

```plot
{"title": "First two mode shapes of a fixed-free beam", "xLabel": "x / L", "yLabel": "phi(x)", "xRange": [0,1], "yRange": [-1.5,1.5], "grid": true, "functions": [{"expr": "1 - cos(1.5708*x)", "label": "mode 1", "color": "#2563eb"}, {"expr": "1 - cos(4.712*x)", "label": "mode 2", "color": "#dc2626"}]}
```

```python
import numpy as np
from scipy.linalg import eigh
M = np.array([[2.,0],[0,1.]]); K = np.array([[1800.,-800],[-800,800.]])
w2, phi = eigh(K, M)                 # generalized eigenproblem
print("natural freqs (rad/s):", np.sqrt(w2))
print("mode shapes (cols):\n", phi)
```

**Next:** using modes to decouple and solve the response.
""",
        ),
        _t(
            "Modal analysis and modal superposition",
            "14 min",
            r"""
# Modal analysis and modal superposition

Collect the mode shapes as columns of a **modal matrix** $\boldsymbol\Phi$ and transform to **modal coordinates** $\mathbf x=\boldsymbol\Phi\,\mathbf q$. Pre-multiplying the equations by $\boldsymbol\Phi^{\!\top}$ and using orthogonality diagonalizes the system: each modal coordinate $q_i$ obeys an *independent* SDOF equation
$$\ddot q_i+2\zeta_i\omega_i\dot q_i+\omega_i^2 q_i=\frac{\boldsymbol\phi_i^{\!\top}\mathbf f}{\boldsymbol\phi_i^{\!\top}\mathbf M\boldsymbol\phi_i}.$$
So an $n$-DOF problem becomes $n$ uncoupled SDOF problems you already know how to solve, then you sum them: $\mathbf x(t)=\sum_i \boldsymbol\phi_i q_i(t)$. This **modal superposition** is the backbone of structural dynamics; in practice only the first handful of modes (truncation) dominate the response, making huge models tractable. Proportional (Rayleigh) damping $\mathbf C=\alpha\mathbf M+\beta\mathbf K$ keeps the modes uncoupled.

```mermaid
flowchart LR
  A[Coupled M C K] --> B[Eigen-solve -> modes]
  B --> C[x = Phi q : decouple]
  C --> D[Solve n SDOF qi]
  D --> E[Superpose x = sum phi_i q_i]
```

```python
import numpy as np
from scipy.linalg import eigh
M = np.array([[2.,0],[0,1.]]); K = np.array([[1800.,-800],[-800,800.]])
w2, Phi = eigh(K, M)
Mr = Phi.T @ M @ Phi                 # modal mass (diagonal ~ I if mass-normalized)
Kr = Phi.T @ K @ Phi                 # modal stiffness (diagonal = w^2)
print("modal mass diag:", np.diag(Mr).round(3))
print("modal stiffness diag:", np.diag(Kr).round(1))
```

**Next:** when the structure is a continuum, not lumped masses.
""",
        ),
        _t(
            "Continuous systems: strings and beams",
            "14 min",
            r"""
# Continuous systems: strings and beams

A real beam has infinitely many DOFs; its motion is a field $w(x,t)$ governed by a **partial** differential equation. For transverse string vibration (tension $T$, mass/length $\rho$): $T\,w_{xx}=\rho\,w_{tt}$, the wave equation, with mode frequencies $\omega_n=\frac{n\pi}{L}\sqrt{T/\rho}$ — a harmonic series, the physics of a guitar string.

For a slender **Euler-Bernoulli beam** (flexural rigidity $EI$):
$$EI\,\frac{\partial^4 w}{\partial x^4}+\rho A\,\frac{\partial^2 w}{\partial t^2}=0.$$
Separation of variables gives natural frequencies $\omega_n=(\beta_n L)^2\sqrt{\dfrac{EI}{\rho A L^4}}$, where $\beta_n L$ are roots of a transcendental frequency equation set by the boundary conditions (e.g. $\beta_n L=1.875,\,4.694,\,7.855,\dots$ for a cantilever). Unlike the string, beam overtones are **not** harmonic. These analytic modes are the benchmark against which FE models are validated.

```plot
{"title": "Cantilever beam: first three mode frequencies (relative)", "xLabel": "mode n", "yLabel": "(beta_n L)^2", "xRange": [1,3], "yRange": [0,65], "grid": true, "functions": [{"expr": "(1.875 + (x-1)*(4.694-1.875))^2", "label": "(beta L)^2 trend", "color": "#16a34a"}]}
```

```python
import numpy as np
E, I, rho, A, L = 200e9, 1e-8, 7800, 1e-4, 0.5   # steel cantilever, SI
betaL = np.array([1.875, 4.694, 7.855])
wn = betaL**2 * np.sqrt(E*I/(rho*A*L**4))
print("first 3 freqs (Hz):", (wn/(2*np.pi)).round(1))
```

**Next:** computing all this numerically with FEA.
""",
        ),
        _t(
            "Computational modal analysis with FEA",
            "13 min",
            r"""
# Computational modal analysis with FEA

For any real geometry, you discretize. **Finite-element analysis (FEA)** approximates the continuum with elements, assembling global $\mathbf M$ and $\mathbf K$ matrices, then solves the generalized eigenproblem $(\mathbf K-\omega^2\mathbf M)\boldsymbol\phi=0$ — exactly the multi-DOF machinery, now with thousands of DOFs. Tools: ANSYS, Abaqus, Nastran, or open stacks (FEniCS, CalculiX, scipy.sparse.linalg.eigsh for the lowest modes via shift-invert).

Two element classes for a beam: a 2-node Euler-Bernoulli element has a $4\times4$ stiffness with the famous $[12, 6L; \dots]$ pattern. The workflow: build elements, assemble, apply boundary constraints, solve a *sparse* eigenproblem for the lowest $k$ modes (the engineering-relevant ones), then validate against analytic or experimental frequencies (MAC, the modal assurance criterion).

```mermaid
flowchart LR
  G[CAD geometry] --> Me[Mesh elements]
  Me --> As[Assemble M, K]
  As --> Bc[Apply BCs]
  Bc --> Ei[Sparse eig: lowest k modes]
  Ei --> Va[Validate vs test: MAC]
```

```python
import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.sparse import csr_matrix
# K, M assembled global sparse matrices (schematic)
n = 200
K = csr_matrix(np.diag(np.full(n, 2.0)) - np.diag(np.ones(n-1), 1) - np.diag(np.ones(n-1), -1))
M = csr_matrix(np.eye(n))
w2, phi = eigsh(K, k=4, M=M, sigma=0, which='LM')   # shift-invert, lowest 4
print("lowest 4 eigenvalues:", np.sqrt(np.abs(w2)).round(4))
```

**Next:** identifying and optimizing damping from data.
""",
        ),
        _t(
            "Experimental FRF identification and damping optimization",
            "13 min",
            r"""
# Experimental FRF identification and damping optimization

Models must meet measurements. In **experimental modal analysis**, you excite a structure (impact hammer or shaker), record input force and output acceleration, and estimate the **frequency-response function** $H(\omega)=\dfrac{\text{output}}{\text{input}}$. Curve-fitting the peaks recovers natural frequencies, damping ratios and mode shapes (algorithms: peak-picking, rational-fraction polynomial, PolyMAX / LSCF). The estimate $H_1=S_{fx}/S_{ff}$ from cross/auto power spectra is robust to output noise; coherence flags bad bands.

The data-driven payoff is **optimization**: choose damping-treatment parameters (constrained-layer thickness, TMD tuning, mount stiffness) to minimize a vibration objective — peak response, RMS acceleration, or transmitted energy — subject to mass and cost constraints. Gradient or surrogate-based optimizers (and increasingly Bayesian optimization / ML surrogates over FE results) drive the iteration, converging the objective as below.

```plot
{"title": "Optimization convergence of an RMS-vibration objective", "xLabel": "iteration", "yLabel": "objective", "xRange": [0,12], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "objective", "color": "#16a34a"}]}
```

```python
import numpy as np
from scipy.optimize import minimize_scalar
# tune absorber natural-frequency ratio to minimize primary peak response
def peak_response(beta, mu=0.05, z2=0.1):
    r = np.linspace(0.5, 1.5, 800)
    num = np.sqrt((beta**2 - r**2)**2 + (2*z2*beta*r)**2)
    den = np.abs((1 - r**2)*(beta**2 - r**2) - mu*beta**2*r**2
                 + 1j*2*z2*beta*r*(1 - r**2 - mu*r**2))
    return np.max(num/den)
res = minimize_scalar(peak_response, bounds=(0.8, 1.1), method='bounded')
print(f"optimal tuning ratio beta={res.x:.3f}, peak={res.fun:.2f}")
```

**Next:** check your understanding of multi-DOF and applied methods.
""",
        ),
        _quiz(),
    ),
)


MECHANICAL_VIBRATIONS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MECHANICAL_VIBRATIONS_COURSES"]
