"""Curated Control Systems track: Basics, Intermediate, Advanced.

Classic and modern control with a practical, intuition-first bent: a short
history of the field, feedback and the PID controller, modeling / root locus /
frequency-domain design, then state-space, LQR, observers/Kalman, Model
Predictive Control (MPC) and Active Disturbance Rejection Control (ADRC).

Dual MATLAB + Python focus: every concept shows both languages, with runnable
Python labs (numpy + matplotlib) the learner executes in the sandbox,
interactive ```plot blocks (step responses, PID/gain sliders, root locus, Bode,
pole maps), Mermaid block diagrams, LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/control_*.py) at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ── Control Systems — Basics ──────────────────────────────────────────────────

_CONTROL_BASICS = SeedCourse(
    slug="control-basics",
    title="Control Systems — Basics",
    description=(
        "What control engineering is and where it came from, open vs. closed "
        "loop and why feedback works, first- and second-order response, and the "
        "PID controller every engineer reaches for first - with side-by-side "
        "MATLAB and Python, interactive plots, and a runnable PID lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is control? A short history",
            "10 min",
            """\
# What is control? A short history

**Control engineering** is the art of making a system *behave the way you want*
by measuring what it does and adjusting what you feed it. A thermostat holds a
room at 21 degrees; cruise control holds your speed up a hill; an autopilot
holds a heading in gusty wind. In every case: **measure, compare to a goal,
correct, repeat.**

```mermaid
flowchart LR
  R[setpoint r] --> S(("sum"))
  S -- "error e" --> C[Controller]
  C -- "u" --> P[Plant / process]
  P -- "output y" --> SENS[Sensor]
  SENS -- "-" --> S
```

## A field with deep roots

- **1788 - Watt's flyball governor.** James Watt's spinning-ball governor held a
  steam engine's speed steady. Faster spin flings the balls out, which closes
  the steam valve. The first widely-used automatic feedback controller.
- **1868 - Maxwell, "On Governors".** James Clerk Maxwell wrote the equations
  explaining *why* some governors hunted (oscillated) - the birth of control
  **theory** and stability analysis.
- **1922 - Minorsky and the PID idea.** Nicolas Minorsky, analysing automatic
  ship steering for the US Navy, formalised proportional-integral-derivative
  action by watching how a helmsman steers.
- **1930s-40s - Bell Labs and the frequency domain.** Harry Nyquist (1932) and
  Hendrik Bode (1940s) developed the frequency-response tools (Nyquist, Bode
  plots, stability margins) that still dominate classic design.
- **1948 - Wiener's *Cybernetics* and Evans' root locus.** Feedback became a
  unifying idea across engineering and biology; Walter Evans gave designers the
  root-locus method.
- **1960 - Kalman and modern control.** Rudolf Kalman recast control in
  **state-space**, and his **Kalman filter** flew on Apollo. This split the
  field into *classic* (frequency-domain) and *modern* (state-space).
- **1970s-80s - MPC in industry.** Oil refineries deployed **Model Predictive
  Control** to push processes against constraints profitably.
- **1990s-2000s - ADRC.** Jingqing Han proposed **Active Disturbance Rejection
  Control**, estimating and cancelling disturbances in real time - now common in
  motion control and power electronics.

> **Practical takeaway:** the *ideas* are old and the *math* is mature. Most of
> the job is modeling honestly, choosing the simplest controller that meets the
> spec, and respecting real-world limits (noise, delay, saturation). This track
> builds from PID up to MPC and ADRC with that mindset.

**Next:** the central idea - open vs. closed loop, and why feedback works.
""",
        ),
        _t(
            "Open loop vs. closed loop",
            "10 min",
            """\
# Open loop vs. closed loop

**Open loop:** you command an input and hope. A microwave runs the magnetron for
30 seconds regardless of how hot the food actually gets - no measurement, no
correction. Cheap, simple, and helpless against surprises.

**Closed loop (feedback):** you *measure* the output, compute the **error**
$e = r - y$ (setpoint minus measurement), and let the controller drive that
error to zero.

```mermaid
flowchart LR
  R[r] --> SUM(("e = r - y"))
  SUM --> C["Controller C"]
  C --> P["Plant G"]
  D["disturbance"] -.-> P
  P --> Y[y]
  Y -- measured --> SUM
```

## Why feedback is magic

Feedback buys you three things open loop never can:

1. **Disturbance rejection** - a wind gust or a load change pushes $y$ off; the
   error grows; the controller pushes back. The loop fights what it can't predict.
2. **Robustness to a wrong model** - even if your plant model is 30% off,
   feedback still drives the error down. Open loop trusts the model completely.
3. **Setpoint tracking** - change $r$ and the output follows.

```plot
{"title": "Disturbance hits at t=4: open loop drifts, closed loop recovers", "xLabel": "time (s)", "yLabel": "output y", "xRange": [0, 10], "yRange": [0, 1.6], "grid": true, "functions": [{"expr": "1 + (x>4)*0.5", "label": "open loop (stuck off)", "color": "#dc2626"}, {"expr": "1 + (x>4)*0.5*exp(-1.5*(x-4))", "label": "closed loop (rejects it)", "color": "#16a34a"}]}
```

The cost of feedback: a sensor, the risk of **instability** (push back too hard
and the loop oscillates), and sensitivity to **measurement noise**. Managing
those trade-offs *is* control design.

```matlab
G = tf(1, [1 1]);          % a first-order plant
T = feedback(G, 1);        % unity-feedback closed loop
step(T)
```

```python
import numpy as np
# Closed-loop step of a first-order plant with proportional gain Kp (sim below).
```

**Next:** how systems respond in time - first and second order.
""",
        ),
        _t(
            "System response: first & second order",
            "12 min",
            """\
# System response: first & second order

Most plants you meet behave like one of two canonical systems. Learn their
response and you can read a step-response plot like a doctor reads an X-ray.

## First order

$$G(s) = \\frac{K}{\\tau s + 1}.$$

One **time constant** $\\tau$: the output reaches 63% of its final value in
$\\tau$ seconds, and ~98% in $4\\tau$ (the **settling time**). No overshoot. Think
an RC circuit charging, or a tank filling.

## Second order

$$G(s) = \\frac{\\omega_n^2}{s^2 + 2\\zeta\\omega_n s + \\omega_n^2}.$$

Two knobs: the **natural frequency** $\\omega_n$ (how fast) and the **damping
ratio** $\\zeta$ (how oscillatory). Drag $\\zeta$ and watch the personality change:

```plot
{"title": "Second-order step response (natural freq = 1)", "xLabel": "time", "yLabel": "y(t)", "xRange": [0, 16], "yRange": [0, 1.8], "grid": true, "controls": [{"name": "z", "range": [0.1, 1.4], "value": 0.3, "label": "damping ratio zeta"}], "functions": [{"expr": "1 - exp(-z*x)*(cos(sqrt(abs(1-z^2))*x) + (z/sqrt(abs(1-z^2)))*sin(sqrt(abs(1-z^2))*x))", "label": "y(t)"}]}
```

Reading the dial:

| $\\zeta$ | Behaviour | Feel |
|---------|-----------|------|
| $\\zeta < 1$ | **underdamped** - overshoots, rings | fast but bouncy |
| $\\zeta = 1$ | **critically damped** - fastest with no overshoot | the sweet spot |
| $\\zeta > 1$ | **overdamped** - slow, no overshoot | sluggish |

Practical specs are usually written as **overshoot**, **rise time**, and
**settling time** - all functions of $\\zeta$ and $\\omega_n$. A common target is
$\\zeta \\approx 0.7$: ~5% overshoot, quick settling.

```matlab
wn = 1; z = 0.3;
G = tf(wn^2, [1 2*z*wn wn^2]);
step(G); stepinfo(G)        % overshoot, rise/settling time
```

```python
import numpy as np
wn, z = 1.0, 0.3
t = np.arange(0, 16, 0.01)
wd = wn*np.sqrt(1 - z**2)
y = 1 - np.exp(-z*wn*t)*(np.cos(wd*t) + (z/np.sqrt(1-z**2))*np.sin(wd*t))
```

**Next:** the controller you'll use most - PID.
""",
        ),
        _t(
            "Meet the PID controller",
            "12 min",
            """\
# Meet the PID controller

The **PID** controller is the workhorse of industry - over 90% of control loops
are PID. It sums three terms acting on the error $e(t) = r - y$:

$$u(t) = K_p\\,e(t) + K_i\\!\\int_0^t e(\\tau)\\,d\\tau + K_d\\,\\frac{de(t)}{dt}.$$

Each term has a job, and a *personality*:

- **P (proportional)** - push in proportion to the current error. More $K_p$ =
  faster and stiffer, but too much rings or destabilises, and P **alone leaves a
  steady-state error** (offset).
- **I (integral)** - accumulate past error until it's gone. I **kills the
  steady-state offset**, but adds lag and can **wind up** (overshoot badly after
  saturation).
- **D (derivative)** - react to the *rate* of change; it's anticipatory and
  **adds damping**, calming overshoot - but it **amplifies noise**, so it's
  almost always filtered.

```mermaid
flowchart LR
  E["error e"] --> P["Kp * e"]
  E --> I["Ki * integral(e)"]
  E --> D["Kd * de/dt"]
  P --> SUM(("sum"))
  I --> SUM
  D --> SUM
  SUM --> U["u to plant"]
```

## P-only control, and why you usually need I

For a simple first-order plant under proportional control, the closed-loop step
response settles at $\\frac{K_p}{1+K_p}$ - so it *never quite reaches 1*. That gap
is the **steady-state error**. Raise $K_p$ and it shrinks (and the response
speeds up), but it never vanishes:

```plot
{"title": "Proportional control of a first-order plant (tau=1)", "xLabel": "time", "yLabel": "output", "xRange": [0, 6], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "Kp", "range": [0.5, 20], "value": 2, "label": "proportional gain Kp"}], "functions": [{"expr": "(Kp/(1+Kp))*(1 - exp(-(1+Kp)*x))", "label": "y(t)"}, {"expr": "1", "label": "setpoint", "color": "#94a3b8"}]}
```

Notice the curve approaches a ceiling **below** 1 and the gap closes as $K_p$
grows - that residual offset is exactly what the **integral** term exists to
erase.

```matlab
C = pid(2, 1, 0.5);         % Kp, Ki, Kd
T = feedback(C*tf(1,[1 1]), 1);
step(T)
```

```python
# Discrete PID, one line per term (full loop in the lab):
# u = Kp*e + Ki*I + Kd*(e - e_prev)/dt
```

> **Practical order of tuning:** get a reasonable **P** for speed, add **I** to
> remove offset, add a little **D** (filtered) to tame overshoot. Then stop -
> simpler loops are more robust.

**Next:** build and tune a PID loop yourself.
""",
        ),
        _code(
            "Lab: simulate a PI controller",
            "12 min",
            """\
# Simulate proportional-integral (PI) control of a first-order plant.
# tau*y' + y = u. Tune Kp and Ki and press Run.
import numpy as np
import matplotlib.pyplot as plt

dt = 0.01
t = np.arange(0, 8, dt)
tau = 1.0
r = 1.0                       # setpoint (a unit step)

Kp, Ki = 2.0, 1.5             # <-- tune these

y = np.zeros_like(t)
u = np.zeros_like(t)
integral = 0.0
yk = 0.0
for k in range(len(t)):
    e = r - yk
    integral += e*dt
    uk = Kp*e + Ki*integral           # PI control law
    yk += dt*(uk - yk)/tau            # plant: Euler step of tau*y' + y = u
    y[k], u[k] = yk, uk

fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
ax[0].plot(t, y, color="#2563eb", label="output y")
ax[0].axhline(r, ls="--", color="#94a3b8", label="setpoint")
ax[0].legend(); ax[0].set_ylabel("y"); ax[0].grid(True)
ax[1].plot(t, u, color="#dc2626"); ax[1].set_ylabel("control u")
ax[1].set_xlabel("time (s)"); ax[1].grid(True)
plt.tight_layout(); plt.show()

ss_err = r - y[-1]
print(f"Kp={Kp}, Ki={Ki}  ->  steady-state error = {ss_err:.4f}")

# Try it yourself:
#   1. Set Ki = 0 (pure P): a steady-state offset appears.
#   2. Raise Ki to 6: faster offset removal, but watch overshoot grow.
#   3. MATLAB: T = feedback(pid(2,1.5)*tf(1,[1 1]),1); step(T)
""",
        ),
    ),
)


# ── Control Systems — Intermediate ────────────────────────────────────────────

_CONTROL_INTERMEDIATE = SeedCourse(
    slug="control-intermediate",
    title="Control Systems — Intermediate: Classic Design",
    description=(
        "Classic control design: modeling with transfer functions, stability "
        "and the characteristic equation, the root locus, Bode/Nyquist and "
        "stability margins, and PID tuning that actually works in the field - "
        "with dual MATLAB/Python, interactive plots, and a PID-tuning lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Modeling & transfer functions",
            "11 min",
            """\
# Modeling & transfer functions

Design starts with a model. Take the differential equation of a plant, Laplace-
transform it (zero initial conditions), and you get a **transfer function** -
output over input as a ratio of polynomials in $s$:

$$G(s) = \\frac{Y(s)}{U(s)} = \\frac{b_m s^m + \\dots + b_0}{a_n s^n + \\dots + a_0}.$$

A mass-spring-damper $m\\ddot{x} + c\\dot{x} + kx = F$ becomes
$G(s) = \\dfrac{1}{m s^2 + c s + k}$ - a second-order system, exactly the shape
from the Basics course.

## Poles, zeros, and block algebra

**Poles** (denominator roots) set the *dynamics* - speed and damping. **Zeros**
(numerator roots) shape *how* inputs couple in. For the unity-feedback loop with
controller $C(s)$ and plant $G(s)$, the **closed-loop transfer function** is

$$T(s) = \\frac{C(s)G(s)}{1 + C(s)G(s)}.$$

The denominator $1 + C(s)G(s)$ is the star of the show - its roots are the
closed-loop poles, and they decide everything.

```plot
{"title": "Pole-zero map of G(s) = (s+1)/((s+2)(s^2+2s+5))", "xLabel": "Re(s)", "yLabel": "Im(s)", "xRange": [-3, 1], "yRange": [-3, 3], "grid": true, "points": [{"x": -2, "y": 0, "label": "pole", "color": "#dc2626", "size": 9}, {"x": -1, "y": 2, "label": "pole", "color": "#dc2626", "size": 9}, {"x": -1, "y": -2, "label": "pole", "color": "#dc2626", "size": 9}, {"x": -1, "y": 0, "label": "zero", "color": "#2563eb", "size": 9}]}
```

```matlab
G = tf([1 1], conv([1 2],[1 2 5]));
pole(G), zero(G), pzmap(G)
```

```python
import numpy as np
num = np.array([1, 1])
den = np.polymul([1, 2], [1, 2, 5])
poles = np.roots(den); zeros = np.roots(num)
```

> **Practical insight:** the **dominant poles** (closest to the imaginary axis)
> govern the response you actually see. Model just enough dynamics to capture
> them - over-modeling makes design harder, not better.

**Next:** when is a closed loop stable?
""",
        ),
        _t(
            "Stability & the characteristic equation",
            "10 min",
            """\
# Stability & the characteristic equation

A continuous LTI system is **stable** if and only if **every pole has a negative
real part** - all closed-loop poles sit in the **left half** of the $s$-plane.
One pole in the right half and the output blows up; poles on the axis mean
sustained oscillation.

```plot
{"title": "s-plane: left half is stable, right half is not", "xLabel": "Re(s)", "yLabel": "Im(s)", "xRange": [-3, 3], "yRange": [-3, 3], "grid": true, "points": [{"x": -1.5, "y": 1, "label": "stable", "color": "#16a34a", "size": 9}, {"x": -1.5, "y": -1, "label": "stable", "color": "#16a34a", "size": 9}, {"x": 1.2, "y": 0.8, "label": "UNSTABLE", "color": "#dc2626", "size": 9}]}
```

## Checking without solving

The closed-loop poles are the roots of the **characteristic equation**
$1 + C(s)G(s) = 0$. You rarely need the exact roots - you need to know if any
stray into the right half-plane. The **Routh-Hurwitz** criterion answers that
from the coefficients alone (no root-finding), and it reveals the **range of
gain** for which the loop stays stable - the practical question "how hard can I
push before it oscillates?"

```matlab
T = feedback(C*G, 1);
isstable(T)                 % true if all poles in LHP
pole(T)
```

```python
import numpy as np
# Closed-loop char. poly 1 + C(s)G(s) = 0 -> check real parts:
poles = np.roots(char_den)
stable = np.all(poles.real < 0)
```

> **Practical insight:** real loops have **time delay** (sensors, computation,
> actuators). Delay eats phase and is the #1 hidden cause of instability - a
> loop that's fine in simulation can oscillate on hardware. The frequency-domain
> tools two lessons from now measure exactly that margin.

**Next:** watch the poles move as you turn up the gain - the root locus.
""",
        ),
        _t(
            "The root locus",
            "11 min",
            """\
# The root locus

As you increase a single gain $K$, the closed-loop poles **trace paths** through
the $s$-plane. The **root locus** is that map - Walter Evans' 1948 gift to
designers. It answers: *what does cranking the gain do to my dynamics, and when
do I lose stability?*

For the plant $G(s) = \\dfrac{1}{s(s+2)}$ with gain $K$, the closed-loop poles
solve $s^2 + 2s + K = 0$. They start at the open-loop poles ($s=0$ and $s=-2$),
move toward each other, meet at $s=-1$, then split vertically as a **complex
pair** - more gain means faster *and* more oscillatory. Drag $K$:

```plot
{"title": "Root locus of 1/(s(s+2)): closed-loop poles vs gain K", "xLabel": "Re(s)", "yLabel": "Im(s)", "xRange": [-3, 1], "yRange": [-3, 3], "grid": true, "controls": [{"name": "K", "range": [1, 10], "value": 2, "label": "gain K (>=1: complex poles)"}], "points": [{"x": 0, "y": 0, "label": "open-loop pole", "color": "#94a3b8", "size": 7}, {"x": -2, "y": 0, "label": "open-loop pole", "color": "#94a3b8", "size": 7}, {"xExpr": "-1", "yExpr": "sqrt(K-1)", "label": "closed-loop pole", "color": "#dc2626", "size": 9}, {"xExpr": "-1", "yExpr": "-sqrt(K-1)", "label": "closed-loop pole", "color": "#dc2626", "size": 9}]}
```

The poles ride the vertical line $\\mathrm{Re}(s) = -1$: settling time stays the
same while overshoot grows with $K$. Different plants give very different loci -
that shape *is* the design insight.

```matlab
G = tf(1, [1 2 0]);         % 1 / (s(s+2))
rlocus(G)                   % draws the locus; click to read off K
```

```python
import numpy as np
K = np.linspace(0, 10, 200)
# closed-loop poles = roots of s^2 + 2s + K for each K:
poles = np.array([np.roots([1, 2, k]) for k in K])
```

> **Practical insight:** the root locus tells you *how* to add dynamics. A
> **lead** compensator bends the locus left (more damping/speed); a **lag** lifts
> low-frequency gain (less steady-state error). PID is a lead-lag in disguise.

**Next:** the frequency-domain view - Bode, Nyquist, and margins.
""",
        ),
        _t(
            "Frequency response & stability margins",
            "12 min",
            """\
# Frequency response & stability margins

Feed a loop sinusoids and measure gain and phase vs. frequency - the **Bode
plot**. It's the most practical design view because you can *measure it on real
hardware* and because it exposes the thing that kills loops: **delay and phase
lag**.

The key idea: the loop becomes unstable if, at the frequency where the loop gain
is 1 (0 dB), the phase reaches $-180°$ (the feedback flips from negative to
positive). How far you are from that disaster is your **margin**:

- **Gain margin** - how much more gain you could add before instability.
- **Phase margin** - how much more phase lag (read: delay) you could tolerate.

```plot
{"title": "Open-loop magnitude |G(jw)| for 1/(s(s+2))", "xLabel": "frequency w (rad/s)", "yLabel": "|G(jw)|", "xRange": [0.1, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "1/(x*sqrt(x^2+4))", "label": "|G(jw)|"}, {"expr": "1", "label": "0 dB (gain = 1)", "color": "#94a3b8"}]}
```

The frequency where the curve crosses 1 is the **crossover** - the loop's
effective bandwidth and the natural place to read the phase margin.

| Margin | Rule of thumb | Meaning |
|--------|---------------|---------|
| Phase margin | aim for **45-60 degrees** | damping + delay tolerance |
| Gain margin | aim for **> 6 dB (2x)** | headroom before oscillation |

```matlab
L = C*G;                    % open-loop transfer function
margin(L)                   % Bode with gain & phase margins
nyquist(L)                  % the Nyquist view of the same thing
```

```python
import numpy as np
w = np.logspace(-1, 1, 500)
s = 1j*w
L = 1/(s*(s+2))             # open-loop frequency response
mag = np.abs(L); phase = np.angle(L, deg=True)
```

> **Practical insight:** more bandwidth = faster response *and* more noise and
> less delay tolerance. Pick the lowest bandwidth that meets the spec, and keep
> ~50 degrees of phase margin so hardware delays don't bite.

**Next:** turning these tools into PID tuning that works.
""",
        ),
        _t(
            "PID tuning that works",
            "12 min",
            """\
# PID tuning that works

Theory gets you close; these practices get you a loop that survives the real
world.

## A repeatable starting point: Ziegler-Nichols

1. Set $K_i = K_d = 0$. Raise $K_p$ until the output **oscillates steadily** -
   that's the **ultimate gain** $K_u$ and **period** $T_u$.
2. Back off and set, for a PID:
   $K_p = 0.6 K_u$, $K_i = 1.2 K_u / T_u$, $K_d = 0.075 K_u T_u$.

Z-N is aggressive (~25% overshoot) - a *starting point*, not a final answer.
Many shops prefer gentler rules (Tyreus-Luyben) or just manual tuning.

## Manual tuning, the way practitioners do it

| Symptom | Fix |
|---------|-----|
| Too slow | raise $K_p$ |
| Steady-state offset | add / raise $K_i$ |
| Overshoot / ringing | add (filtered) $K_d$, or lower $K_p$ |
| Noisy, jittery actuator | lower $K_d$ or filter it harder |
| Big overshoot after saturation | add **anti-windup** |

## The two fixes that separate textbook PID from working PID

- **Anti-windup.** When the actuator **saturates** (a valve is 100% open), the
  integral keeps accumulating error it can't act on, then overshoots massively
  when it recovers. Clamp or back-calculate the integral while saturated.
- **Derivative filtering & setpoint weighting.** Pure D amplifies noise and
  "kicks" on setpoint steps. Filter D with a first-order lag, and apply D to the
  *measurement* (not the error) to avoid derivative kick.

```matlab
C = pid(Kp, Ki, Kd, Tf);    % Tf = derivative filter time constant
% Simulink blocks add clamping anti-windup directly.
```

```python
# In the discrete loop: clamp u, and only integrate when not saturated.
# if u > umax: u = umax; integral -= e*dt   # simple back-off anti-windup
```

> **Practical insight:** discretize deliberately. Sample fast (10-20x your
> bandwidth), and remember every line of controller code adds delay - which
> eats the phase margin you fought for.

**Next:** tune a PID on a real second-order plant, with anti-windup.
""",
        ),
        _code(
            "Lab: tune a PID with anti-windup",
            "13 min",
            """\
# PID control of a mass-spring-damper, WITH actuator saturation + anti-windup.
# m*x'' + c*x' + k*x = u,  |u| <= umax.  Tune Kp, Ki, Kd and press Run.
import numpy as np
import matplotlib.pyplot as plt

dt = 0.005
t = np.arange(0, 12, dt)
m, c, k = 1.0, 1.0, 5.0       # plant
r = 1.0                       # setpoint
umax = 25.0                   # actuator limit

Kp, Ki, Kd = 30.0, 20.0, 10.0 # <-- tune these

x, v = 0.0, 0.0
integral, e_prev = 0.0, 0.0
X = np.zeros_like(t)
U = np.zeros_like(t)
for i in range(len(t)):
    e = r - x
    deriv = (e - e_prev)/dt
    u_unsat = Kp*e + Ki*integral + Kd*deriv
    u = max(-umax, min(umax, u_unsat))        # actuator saturation
    if u == u_unsat:                          # anti-windup: integrate only
        integral += e*dt                      # when NOT saturated
    a = (u - c*v - k*x)/m                      # plant acceleration
    v += a*dt; x += v*dt
    e_prev = e
    X[i], U[i] = x, u

fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
ax[0].plot(t, X, color="#2563eb"); ax[0].axhline(r, ls="--", color="#94a3b8")
ax[0].set_ylabel("position x"); ax[0].grid(True)
ax[1].plot(t, U, color="#dc2626"); ax[1].axhline(umax, ls=":", color="#94a3b8")
ax[1].axhline(-umax, ls=":", color="#94a3b8")
ax[1].set_ylabel("control u"); ax[1].set_xlabel("time (s)"); ax[1].grid(True)
plt.tight_layout(); plt.show()

over = (X.max() - r)/r*100
print(f"overshoot = {over:.1f}%   final error = {r - X[-1]:.4f}")

# Try it yourself:
#   1. Remove anti-windup (always integrate) and lower umax to 8 - see the
#      integral wind up and overshoot badly.
#   2. Halve Kd: more ringing. Double it: smoother but watch the control effort.
""",
        ),
    ),
)


# ── Control Systems — Advanced ────────────────────────────────────────────────

_CONTROL_ADVANCED = SeedCourse(
    slug="control-advanced",
    title="Control Systems — Advanced: Modern, MPC & ADRC",
    description=(
        "Modern and advanced control: state-space, pole placement and LQR, "
        "observers and the Kalman filter, Model Predictive Control (MPC), and "
        "Active Disturbance Rejection Control (ADRC) - with the practical "
        "deployment insights that make them work, dual MATLAB/Python, and a "
        "PID-vs-ADRC disturbance-rejection lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "State-space & modern control",
            "12 min",
            """\
# State-space & modern control

Classic control lives in one input, one output, and the frequency domain.
**Modern control** (Kalman, 1960) works directly in the time domain with the
system's internal **state** $\\mathbf{x}$ - a vector of the variables that
summarise its past (positions, velocities, currents, ...):

$$\\dot{\\mathbf{x}} = A\\mathbf{x} + B\\mathbf{u}, \\qquad \\mathbf{y} = C\\mathbf{x} + D\\mathbf{u}.$$

$A$ is the system dynamics, $B$ how inputs enter, $C$ what you measure. This
scales naturally to **MIMO** (many inputs/outputs) where transfer-function
algebra gets unwieldy.

```mermaid
flowchart LR
  U["u"] --> B["B"]
  B --> SUM(("sum"))
  SUM --> INT["integrate -> x"]
  INT --> C2["C"]
  C2 --> Y["y"]
  INT --> A2["A"]
  A2 --> SUM
```

## Two questions modern control asks first

- **Controllability** - can the inputs actually steer every state? (Check the
  rank of $[B\\;AB\\;A^2B\\;\\dots]$.)
- **Observability** - can you reconstruct every state from the outputs? (Rank of
  the observability matrix.)

If a mode is uncontrollable you can't move it; if unobservable you can't see it.
Both have to hold for full state feedback and estimation to work.

```matlab
sys = ss(A, B, C, D);
rank(ctrb(sys))             % = n  -> controllable
rank(obsv(sys))             % = n  -> observable
```

```python
import numpy as np
n = A.shape[0]
Cc = np.hstack([np.linalg.matrix_power(A, i) @ B for i in range(n)])
controllable = np.linalg.matrix_rank(Cc) == n
```

> **Practical insight:** state-space shines for MIMO, time-varying, and optimal
> control, and it's the language of estimation (Kalman) and MPC. For a clean
> SISO loop, classic PID is often simpler and just as good - pick the tool, not
> the fashion.

**Next:** designing the feedback - pole placement and LQR.
""",
        ),
        _t(
            "Pole placement & LQR",
            "12 min",
            """\
# Pole placement & LQR

With the full state available, **state feedback** $\\mathbf{u} = -K\\mathbf{x}$
lets you put the closed-loop poles (eigenvalues of $A - BK$) **wherever you
want** - if the system is controllable.

## Pole placement: you pick the poles

Choose target poles (say $\\zeta = 0.7$, a chosen $\\omega_n$) and solve for $K$.
Powerful, but *where* should the poles go? Aggressive poles demand huge control
effort and amplify noise. That judgement call is exactly what LQR automates.

## LQR: let a cost function pick the poles

The **Linear-Quadratic Regulator** finds the $K$ that minimises

$$J = \\int_0^\\infty \\big(\\mathbf{x}^\\top Q\\,\\mathbf{x} + \\mathbf{u}^\\top R\\,\\mathbf{u}\\big)\\,dt.$$

$Q$ penalises state error (want tight regulation -> big $Q$); $R$ penalises
control effort (want gentle, energy-saving action -> big $R$). Turn the $Q/R$
dial and LQR returns the optimal, guaranteed-stable $K$:

```plot
{"title": "LQR Q/R trade-off: aggressive vs relaxed regulation", "xLabel": "time", "yLabel": "state x", "xRange": [0, 10], "yRange": [-0.1, 1.05], "grid": true, "controls": [{"name": "rate", "range": [0.5, 4], "value": 1, "label": "effective speed (big Q/small R -> faster)"}], "functions": [{"expr": "exp(-rate*x)", "label": "regulation of an initial error"}]}
```

Big $Q$ / small $R$ drives the error down fast (steeper curve) but spends more
control; big $R$ relaxes it. LQR is the backbone of aerospace and robotics
control.

```matlab
K = place(A, B, desired_poles);    % pole placement
K = lqr(A, B, Q, R);               % optimal LQR gain
```

```python
import numpy as np
# Pole placement via Ackermann, or LQR by solving the algebraic Riccati
# equation (scipy.linalg.solve_continuous_are in a full environment):
# K = R^-1 B^T P,  where P solves the ARE.
```

> **Practical insight:** tune LQR by **ratios**, not absolute numbers - scale
> $Q$ entries by $1/x_{max}^2$ and $R$ by $1/u_{max}^2$ (Bryson's rule) so each
> term is in sensible units. Then nudge from there.

**Next:** you rarely measure the full state - estimate it.
""",
        ),
        _t(
            "Observers & the Kalman filter",
            "11 min",
            """\
# Observers & the Kalman filter

State feedback needs the full state $\\mathbf{x}$, but you usually measure only a
few outputs $\\mathbf{y}$. An **observer** reconstructs the rest by running a
model in parallel and correcting it with the measurement error:

$$\\dot{\\hat{\\mathbf{x}}} = A\\hat{\\mathbf{x}} + B\\mathbf{u} + L\\,(\\mathbf{y} - C\\hat{\\mathbf{x}}).$$

The gain $L$ sets how fast the estimate $\\hat{\\mathbf{x}}$ chases the truth.

```mermaid
flowchart LR
  Y["measured y"] --> OBS["Observer: model + L(y - C xhat)"]
  U["u"] --> OBS
  OBS --> XH["state estimate xhat"]
  XH --> K["-K"] --> PLANT["Plant"]
  PLANT --> Y
```

## From observer to Kalman filter

If you account for **process noise** and **measurement noise** with their
covariances, the optimal $L$ is the **Kalman gain** - the observer becomes the
**Kalman filter**. It blends prediction and measurement by their relative
trust: noisy sensor -> lean on the model; noisy model -> lean on the sensor.

Pair an LQR controller with a Kalman-filter estimator and you have **LQG**
(Linear-Quadratic-Gaussian) control. The **separation principle** says you can
design the regulator and the estimator independently - a huge practical
simplification.

```matlab
L  = lqe(A, G, C, Qn, Rn);     % Kalman estimator gain
kf = kalman(sys, Qn, Rn);      % the filter object
```

```python
# Discrete Kalman step (predict / update):
# xhat = A@xhat + B@u;  P = A@P@A.T + Qn          # predict
# Kk = P@C.T @ inv(C@P@C.T + Rn)                  # gain
# xhat += Kk@(y - C@xhat);  P = (I - Kk@C)@P      # update
```

> **Practical insight:** the Kalman filter is everywhere - GPS/IMU sensor
> fusion, drone attitude, battery state-of-charge. Its tuning knobs are the
> noise covariances $Q_n, R_n$; getting them roughly right matters more than the
> exact model.

**Next:** controlling with constraints and a model of the future - MPC.
""",
        ),
        _t(
            "Model Predictive Control (MPC)",
            "12 min",
            """\
# Model Predictive Control (MPC)

PID and LQR react to the present. **MPC** looks **ahead**: at every step it uses
a model to predict the next $N$ outputs, solves an **optimization** for the best
sequence of moves over that horizon, applies only the **first** move, then
repeats next step with fresh measurements. This is **receding-horizon** control.

```mermaid
flowchart LR
  M["measure state"] --> OPT["optimize u over horizon N (respecting constraints)"]
  OPT --> APPLY["apply only u(0)"]
  APPLY --> WAIT["wait one step"]
  WAIT --> M
```

It minimises a cost over the horizon - tracking error plus control effort -

$$\\min_{u_0,\\dots,u_{N-1}} \\sum_{i=1}^{N} \\lVert y_i - r \\rVert_Q^2 + \\sum_{i=0}^{N-1}\\lVert u_i \\rVert_R^2,$$

**subject to constraints**: $u_{min} \\le u \\le u_{max}$, slew limits, output
bounds. That constraint handling is MPC's superpower.

## Why industry loves MPC

- **Constraints, natively.** It keeps valves, currents, and temperatures inside
  hard limits while staying optimal - PID only fakes this with clamps.
- **MIMO and coupling.** One optimizer coordinates many actuators that interact.
- **Preview.** If you know the reference or a disturbance is coming (a batch
  recipe, road ahead), MPC acts *before* the error appears.

The price: you solve an optimization **every sample**, so you need a decent model
and compute budget. It started in 1970s refineries (slow processes, big payoff)
and now runs on chips fast enough for drones and engines.

```matlab
mpcobj = mpc(plant, Ts, p, m);     % prediction p, control horizon m
mpcobj.MV.Min = -25; mpcobj.MV.Max = 25;   % input constraints
```

```python
# Each step: build the prediction, solve a QP (cvxpy/OSQP in a full env),
# apply u[0], then re-measure and repeat (receding horizon).
```

> **Practical insight:** horizon length and the move-cost $R$ are your main
> dials; longer horizons are smoother but cost more compute. Always include a
> feasibility fallback - a real plant will violate a constraint eventually.

**Next:** rejecting whatever you didn't model - ADRC.
""",
        ),
        _t(
            "Active Disturbance Rejection Control (ADRC)",
            "12 min",
            """\
# Active Disturbance Rejection Control (ADRC)

Classic design leans on a good model. **ADRC** (Jingqing Han, 1990s-2000s) flips
the philosophy: lump *everything* you don't know - unmodeled dynamics, nonlinear
terms, and external disturbances - into a single **total disturbance** $f$, then
**estimate it in real time and cancel it**.

The trick is an **Extended State Observer (ESO)** that treats $f$ as an extra
state and estimates it alongside the real states:

$$\\dot{x} = \\dots + b_0 u + f, \\qquad \\text{ESO estimates } \\hat{x}\\ \\text{and}\\ \\hat{f}.$$

The control law then cancels the estimated disturbance and applies a simple
(often just PD) law on what's left:

$$u = \\frac{u_0 - \\hat{f}}{b_0}.$$

```mermaid
flowchart LR
  R["r"] --> PD["PD law -> u0"]
  PD --> COMP(("u = (u0 - fhat)/b0"))
  COMP --> PLANT["Plant (+ unknown f)"]
  PLANT --> ESO["Extended State Observer"]
  ESO -- "xhat" --> PD
  ESO -- "fhat (total disturbance)" --> COMP
```

## Why practitioners reach for ADRC

- **Nearly model-free.** You need only the system **order** and a rough input
  gain $b_0$ - not an accurate transfer function. Huge where modeling is hard.
- **Strong disturbance rejection.** Because it actively estimates and cancels
  $f$, it shrugs off load changes and parameter drift that detune a fixed PID.
- **Few, intuitive knobs.** **Linear ADRC (LADRC)** parameterises everything by
  two bandwidths - controller $\\omega_c$ and observer $\\omega_o$ (set
  $\\omega_o \\approx 3\\text{-}5\\,\\omega_c$) - so tuning is fast.

It's now common in **motion control, power electronics, and motor drives**, and
is a pragmatic middle ground between hand-tuned PID and full model-based design.

```python
# Linear ESO (first-order plant), discrete:
# z1 += dt*(z2 + b0*u + beta1*(y - z1))     # estimates output
# z2 += dt*(beta2*(y - z1))                 # estimates total disturbance f
# u = (Kp*(r - z1) - z2)/b0                 # cancel f, then simple control
```

> **Practical insight:** ADRC's robustness comes from the observer bandwidth -
> faster $\\omega_o$ rejects disturbances harder but amplifies sensor noise. It's
> the same speed-vs-noise trade-off as everywhere else in control.

**Next:** see ADRC beat a fixed PID on a disturbed plant.
""",
        ),
        _code(
            "Lab: PID vs ADRC disturbance rejection",
            "14 min",
            """\
# Compare a fixed PID with Linear ADRC when a disturbance hits the plant.
# Plant: y' = -a*y + b*u + d(t), with a,b only roughly known.
import numpy as np
import matplotlib.pyplot as plt

dt = 0.005
t = np.arange(0, 10, dt)
a, b = 1.0, 1.0                 # true plant (controller only "knows" b0)
r = 1.0
d = np.where(t >= 5.0, 1.5, 0.0)   # a step LOAD DISTURBANCE at t=5

# --- Fixed PID ---
yp = 0.0; I = 0.0; e_prev = 0.0
YP = np.zeros_like(t)
Kp, Ki, Kd = 4.0, 3.0, 0.5
for i in range(len(t)):
    e = r - yp
    I += e*dt
    u = Kp*e + Ki*I + Kd*((e - e_prev)/dt)
    yp += dt*(-a*yp + b*u + d[i])
    e_prev = e; YP[i] = yp

# --- Linear ADRC (first-order, 2-state ESO) ---
ya = 0.0; z1 = 0.0; z2 = 0.0
YA = np.zeros_like(t)
b0 = 1.0                         # rough input gain (the ONLY model info)
wo = 12.0                        # observer bandwidth
beta1, beta2 = 2*wo, wo*wo       # ESO gains
Kc = 3.0                         # simple proportional control bandwidth
for i in range(len(t)):
    u = (Kc*(r - z1) - z2)/b0    # cancel estimated disturbance z2
    ya += dt*(-a*ya + b*u + d[i])
    err = ya - z1                # observer correction
    z1 += dt*(z2 + b0*u + beta1*err)
    z2 += dt*(beta2*err)         # z2 -> estimate of total disturbance
    YA[i] = ya

plt.figure(figsize=(8, 4))
plt.plot(t, YP, label="PID", color="#dc2626")
plt.plot(t, YA, label="ADRC", color="#16a34a")
plt.axhline(r, ls="--", color="#94a3b8")
plt.axvline(5.0, ls=":", color="#94a3b8")
plt.title("Load disturbance at t=5: ADRC estimates & cancels it")
plt.xlabel("time (s)"); plt.ylabel("output y"); plt.legend(); plt.grid(True)
plt.show()

dip_pid = r - YP[t >= 5.0].min()
dip_adrc = r - YA[t >= 5.0].min()
print(f"max disturbance dip:  PID = {dip_pid:.3f}   ADRC = {dip_adrc:.3f}")

# Try it yourself:
#   1. Raise wo to 25: ADRC rejects the disturbance even harder.
#   2. Change the TRUE a,b to 2.0, 0.6 (model mismatch) - ADRC barely cares;
#      the PID detunes.
""",
        ),
        _t(
            "Deployment & use cases",
            "10 min",
            """\
# Deployment & use cases

The math is half the job; making a loop survive contact with hardware is the
other half.

## The practical checklist

- **Sample fast enough.** Discretize at 10-20x your closed-loop bandwidth; too
  slow adds delay that erodes phase margin.
- **Respect actuators.** Saturation and slew limits are always there - add
  anti-windup (PID) or constraints (MPC), and never assume infinite authority.
- **Filter measurements.** Sensor noise rides straight through derivative and
  observer gains. Filter, but watch the added phase lag.
- **Mind delay.** Computation, comms, and transport delay all eat phase margin -
  the gap between a sim that works and hardware that oscillates.
- **Schedule gains** when the plant changes with operating point (airspeed,
  load): a set of controllers blended by a measured variable.
- **Always have a fallback.** Bumpless manual override, constraint-relaxation,
  and watchdog timers turn a controller into a *system*.

## Where it all shows up

| Domain | Typical choice |
|--------|----------------|
| Drones / robotics | cascaded PID, LQR, increasingly ADRC |
| Process industry (refining, chemicals) | MPC over hundreds of loops |
| Automotive (cruise, traction, EV motors) | PID + gain scheduling, ADRC for drives |
| Aerospace (autopilot, attitude) | LQR/LQG, robust control |
| Power electronics / motor drives | PI + ADRC, fast inner loops |
| Temperature / HVAC | PID, sometimes MPC for efficiency |

## The throughline

Whatever the controller - PID, LQR, MPC, ADRC - the loop is the same idea Watt
built in 1788: **measure, compare, correct.** Choose the simplest controller
that meets the spec, model only what the dominant dynamics demand, and respect
noise, delay, and saturation. The tool changes; the discipline doesn't. And
whether you prototype in MATLAB or Python, the workflow is identical - only the
syntax differs.

**Next:** the final check.
""",
        ),
    ),
)


CONTROL_COURSES: tuple[SeedCourse, ...] = (
    _CONTROL_BASICS,
    _CONTROL_INTERMEDIATE,
    _CONTROL_ADVANCED,
)

__all__ = ["CONTROL_COURSES"]
