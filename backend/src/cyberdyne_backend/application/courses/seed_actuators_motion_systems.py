"""Actuators & Motion Systems track: Basics -> Intermediate -> Advanced.

From the physics of electric actuators (DC, servo, stepper, BLDC) through power
transmission (gearboxes, lead/ball screws, belts) to motion profiling, sizing
and precision positioning. Lessons are `text` with LaTeX, interactive ```plot
blocks (torque-speed curves, trapezoidal/S-curve profiles, frequency response,
optimization convergence), ```mermaid diagrams (actuator taxonomy, control
loops, sizing workflows) and runnable ```python / ```matlab code for profiling,
sizing and trajectory optimization.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Actuators & Motion Systems — Basics ──────────────────────────────────────

_BASICS = SeedCourse(
    slug="actuators-motion-systems-basics",
    title="Actuators & Motion Systems — Basics",
    description=(
        "An intuition-first tour of electric actuators and motion systems: what an "
        "actuator is, the brushed DC motor and its torque-speed line, servo motors "
        "and closed-loop position control, stepper motors and open-loop indexing, "
        "BLDC/PMSM machines, and the load-side hardware (gears and screws) that "
        "converts a spinning shaft into useful motion. Interactive torque-speed "
        "plots and actuator taxonomy diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is an actuator?",
            "10 min",
            r"""
# What is an actuator?

An **actuator** is the component that converts a control signal and a power
source into physical motion or force. In a motion system it is the muscle: the
controller decides *what* should move, the actuator makes it happen. Electric
actuators dominate factory automation and robotics because they are clean,
precise and easy to command.

Every electric actuator obeys two coupled relations. Electrically, applied
voltage drives current through the windings; mechanically, that current produces
torque $\tau = k_t i$, and the spinning rotor generates a back-EMF
$e = k_e \omega$ that opposes the supply. These two constants ($k_t$ in
N·m/A and $k_e$ in V·s/rad) are numerically equal in SI units for an ideal
machine.

We classify electric actuators by how they are commutated and controlled:

```mermaid
flowchart TB
    A[Electric actuators] --> B[Brushed DC]
    A --> C[Brushless: BLDC / PMSM]
    A --> D[Stepper]
    A --> E[Servo motor + drive]
    C --> F[Trapezoidal BLDC]
    C --> G[Sinusoidal PMSM]
    E --> H[Closed-loop position / velocity / torque]
```

The right actuator depends on the task: smooth high-speed motion, precise
indexing, or holding a heavy load still. The rest of this course builds the
intuition to choose well.

**Next:** the brushed DC motor and its torque-speed line.
""",
        ),
        _t(
            "The brushed DC motor",
            "11 min",
            r"""
# The brushed DC motor

The **brushed DC motor** is the simplest electric actuator to understand. A
mechanical commutator (brushes on a segmented ring) automatically switches
current in the rotor windings so the produced torque always pushes the rotor
forward. Apply more voltage and it spins faster; load it harder and it draws
more current.

Its steady-state behaviour comes from the voltage equation. Ignoring inductance
at steady speed:

$$V = i R + k_e \omega$$

Combined with $\tau = k_t i$, this gives the **torque-speed line**: torque is
maximum (the *stall torque*) at zero speed, and speed is maximum (the
*no-load speed*) at zero torque. The line is straight, with slope set by winding
resistance.

```plot
{"title": "DC motor torque-speed line", "xLabel": "speed (krpm)", "yLabel": "torque (N*m)", "xRange": [0,4], "yRange": [0,1], "grid": true, "functions": [{"expr": "0.9 - 0.225*x", "label": "torque vs speed", "color": "#2563eb"}]}
```

Key facts that fall out of this line:

- **Stall torque** ($\omega=0$) is set by $V/R$ and can be huge — and the
  current $V/R$ can burn the windings, so stall is a thermal limit.
- **Maximum mechanical power** occurs at roughly *half* the no-load speed and
  *half* the stall torque.
- Speed control is easy: change the applied voltage (in practice via PWM).

Brushes wear and arc, limiting life and creating EMI, which is exactly why
brushless machines exist.

**Next:** servo motors and closed-loop control.
""",
        ),
        _t(
            "Servo motors and closed-loop control",
            "11 min",
            r"""
# Servo motors and closed-loop control

A **servo motor** is not a distinct motor technology — it is any motor (often a
PMSM or brushed DC) wrapped in a feedback loop that forces the shaft to track a
commanded position, velocity or torque. The defining ingredient is a **feedback
sensor** (encoder or resolver) and a controller that drives the error to zero.

Servo control is almost always organized as **cascaded loops**: an outer
position loop commands an inner velocity loop, which commands an innermost
current (torque) loop. The inner loops must be much faster than the outer ones
for the cascade to be stable.

```mermaid
flowchart LR
    P[Position cmd] --> PC[Position ctrl]
    PC --> VC[Velocity ctrl]
    VC --> CC[Current ctrl]
    CC --> AMP[Amplifier] --> M[Motor]
    M -- encoder --> PC
    M -- encoder --> VC
    M -- current sense --> CC
```

A typical position loop uses a PID controller. Its closed-loop response can be
shaped to be fast yet well-damped; an under-damped servo overshoots and rings,
while an over-damped one is sluggish:

```plot
{"title": "Servo step response (under- vs well-damped)", "xLabel": "time (s)", "yLabel": "position", "xRange": [0,6], "yRange": [0,1.6], "grid": true, "functions": [{"expr": "1 - exp(-0.7*x)*cos(2*x)", "label": "under-damped", "color": "#dc2626"}, {"expr": "1 - exp(-2*x)*(1+2*x)", "label": "critically damped", "color": "#16a34a"}]}
```

Servos shine where you need accurate, repeatable positioning under varying load
— robot joints, CNC axes, camera gimbals.

**Next:** stepper motors and open-loop indexing.
""",
        ),
        _t(
            "Stepper motors and open-loop indexing",
            "10 min",
            r"""
# Stepper motors and open-loop indexing

A **stepper motor** moves in fixed angular increments — *steps* — by energizing
its phases in sequence. A common hybrid stepper has 200 full steps per
revolution (1.8° each). Because the rotor snaps to known positions, a stepper
can be driven **open loop**: count the pulses you send and you know where the
rotor is, with no encoder. That makes steppers cheap and simple for indexing
tasks like 3D printers and small CNC machines.

```mermaid
flowchart LR
    CMD[Step + direction pulses] --> DRV[Stepper driver]
    DRV --> PH[Phase A / Phase B currents]
    PH --> ROT[Rotor advances one step per pulse]
```

The catch is the **torque-speed tradeoff**: as step rate rises, winding
inductance limits how fast current (and thus torque) builds, so available torque
falls steeply with speed. Push too hard and the motor *loses steps* silently —
the worst failure mode, since open loop has no way to detect it.

```plot
{"title": "Stepper pull-out torque vs speed", "xLabel": "step rate (kHz)", "yLabel": "torque (N*m)", "xRange": [0,4], "yRange": [0,0.6], "grid": true, "functions": [{"expr": "0.5*exp(-0.4*x)", "label": "pull-out torque", "color": "#2563eb"}]}
```

**Microstepping** subdivides each full step (e.g. 16×) by driving the two phases
with sinusoidal currents, giving smoother motion and finer resolution — but it
does *not* proportionally increase static accuracy or torque. Steppers also
dissipate heat even when holding still, since they carry rated current at zero
speed.

**Next:** brushless DC and PMSM machines.
""",
        ),
        _t(
            "BLDC and PMSM machines",
            "11 min",
            r"""
# BLDC and PMSM machines

**Brushless** machines move the windings to the stator and put permanent magnets
on the rotor, then commutate *electronically* with a power inverter instead of
brushes. This removes the wearing brushes, improves efficiency and power density,
and is why nearly all modern servos, drones and EVs use brushless motors.

Two flavours differ by how they are driven:

- **BLDC** (trapezoidal): six-step commutation, often using Hall sensors. Simple
  and cheap, but torque ripples at the commutation transitions.
- **PMSM** (sinusoidal): the windings carry sinusoidal currents controlled with
  **field-oriented control (FOC)**, giving smooth, ripple-free torque — the
  servo-grade choice.

```mermaid
flowchart LR
    POS[Rotor position<br/>Hall / encoder] --> COMM[Commutation logic]
    COMM --> INV[3-phase inverter]
    DC[DC bus] --> INV
    INV --> M[Brushless motor]
    M --> POS
```

Torque is produced when stator current leads the rotor magnets correctly;
keeping that phase relationship is the whole job of commutation. With sinusoidal
drive the three phase currents are 120° apart:

```plot
{"title": "Three-phase sinusoidal stator currents", "xLabel": "electrical angle (rad)", "yLabel": "current (A)", "xRange": [0,7], "yRange": [-1.4,1.4], "grid": true, "functions": [{"expr": "sin(x)", "label": "phase A", "color": "#2563eb"}, {"expr": "sin(x-2.094)", "label": "phase B", "color": "#dc2626"}, {"expr": "sin(x+2.094)", "label": "phase C", "color": "#16a34a"}]}
```

The result is a motor with a flat, brush-free torque-speed characteristic and
the highest efficiency of the common electric actuators.

**Next:** gears and screws — turning rotation into useful motion.
""",
        ),
        _t(
            "Gears, lead screws and motion conversion",
            "11 min",
            r"""
# Gears, lead screws and motion conversion

Motors spin fast at low torque; loads usually want the opposite, or want linear
motion. **Transmission elements** bridge the gap.

A **gearbox** with ratio $N$ multiplies torque by $N$ and divides speed by $N$
(ignoring losses): $\tau_\text{out} = \eta N\,\tau_\text{motor}$ and
$\omega_\text{out} = \omega_\text{motor}/N$. It also reflects load inertia back
to the motor reduced by $N^2$, which is the key to **inertia matching**.

A **lead screw** or **ball screw** converts rotation to linear motion. With lead
$L$ (linear travel per revolution), the linear speed is $v = L\,\omega/2\pi$ and
the force is $F = 2\pi\,\eta\,\tau / L$. Ball screws reach 90%+ efficiency;
sliding lead screws are far lower and can be self-locking.

```mermaid
flowchart LR
    M[Motor: high speed, low torque] --> G[Gearbox ratio N]
    G --> S[Ball screw, lead L]
    S --> ST[Linear stage: force F, speed v]
```

The torque a screw demands from the motor rises with the load force; this is the
heart of actuator sizing:

```plot
{"title": "Required motor torque vs load force (ball screw, L=5mm)", "xLabel": "load force (kN)", "yLabel": "motor torque (N*m)", "xRange": [0,5], "yRange": [0,5], "grid": true, "functions": [{"expr": "0.884*x", "label": "torque = F*L/(2*pi*eta)", "color": "#2563eb"}]}
```

Choosing the ratio and lead is a tradeoff: more reduction means more torque but
lower top speed and more reflected friction. Sizing the whole chain — motor,
gearbox, screw, load — is the subject of the Intermediate course.

**Next:** check your understanding with a short quiz.
""",
        ),
        _quiz(),
    ),
)


# ── Actuators & Motion Systems — Intermediate ────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="actuators-motion-systems-intermediate",
    title="Actuators & Motion Systems — Intermediate",
    description=(
        "The core quantitative methods of motion engineering: the motor electrical "
        "and mechanical dynamic model, trapezoidal and S-curve velocity profiling, "
        "inertia matching and reflected-load calculations, the RMS-torque thermal "
        "sizing method, the cascaded PI velocity/current loops with bandwidth "
        "separation, and feedback resolution and encoders. Worked NumPy/Matplotlib "
        "code for profiling and sizing."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Modeling the actuator dynamics",
            "12 min",
            r"""
# Modeling the actuator dynamics

To control or size an actuator you need its **dynamic model**. A DC/PMSM (in the
d-q frame) reduces to two coupled equations — one electrical, one mechanical:

$$L\frac{di}{dt} = V - Ri - k_e\omega \qquad J\frac{d\omega}{dt} = k_t i - b\omega - \tau_L$$

Here $L,R$ are winding inductance and resistance, $J$ the total inertia, $b$ the
viscous friction and $\tau_L$ the load torque. The two natural time constants —
electrical $\tau_e = L/R$ (milliseconds) and mechanical
$\tau_m = JR/(k_t k_e)$ (tens of ms) — usually differ by an order of magnitude,
which is what lets us design the current loop and speed loop separately.

```python
import numpy as np
from scipy.integrate import solve_ivp

R, L, kt, ke, J, b = 1.0, 1e-3, 0.05, 0.05, 1e-4, 1e-5
V, tau_L = 24.0, 0.0  # step voltage, no load

def motor(t, x):
    i, w = x
    di = (V - R*i - ke*w) / L
    dw = (kt*i - b*w - tau_L) / J
    return [di, dw]

sol = solve_ivp(motor, [0, 0.1], [0, 0], max_step=1e-4)
print("steady speed (rad/s):", sol.y[1, -1])  # -> ~ V/ke
```

```plot
{"title": "Speed step response of the DC motor model", "xLabel": "time (ms)", "yLabel": "speed (frac of final)", "xRange": [0,60], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1 - exp(-x/12)", "label": "first-order rise, tau_m=12ms", "color": "#2563eb"}]}
```

Linearizing and taking the Laplace transform gives the speed-to-voltage transfer
function — the basis for tuning the loops you will design later.

**Next:** trapezoidal and S-curve motion profiles.
""",
        ),
        _t(
            "Trapezoidal and S-curve motion profiles",
            "12 min",
            r"""
# Trapezoidal and S-curve motion profiles

A **motion profile** is the planned velocity-versus-time the controller will
track. The simplest is the **trapezoidal** profile: accelerate at constant $a$,
cruise at constant $v$, decelerate at $-a$. It is time-optimal under a fixed
acceleration limit, but its instantaneous jump in acceleration produces infinite
**jerk** $\dot a$, which excites vibration and stresses gear teeth.

The **S-curve** profile ramps acceleration smoothly (bounded jerk), trading a
little extra move time for far less vibration and audible noise — essential for
precision and high-throughput machines.

```plot
{"title": "Trapezoidal velocity profile", "xLabel": "time (s)", "yLabel": "velocity", "xRange": [0,4], "yRange": [0,1.2], "grid": true, "functions": [{"expr": "x", "label": "accel", "color": "#16a34a"}, {"expr": "1", "label": "cruise", "color": "#2563eb"}, {"expr": "4-x", "label": "decel", "color": "#dc2626"}]}
```

```python
import numpy as np

def trapezoid(dist, vmax, amax, dt=1e-3):
    ta = vmax / amax                       # time to reach vmax
    da = 0.5 * amax * ta**2                # distance during accel
    if 2*da > dist:                        # triangular: never reach vmax
        ta = np.sqrt(dist / amax); vmax = amax*ta; da = dist/2
    tc = (dist - 2*da) / vmax              # cruise time
    T = 2*ta + tc
    t = np.arange(0, T, dt)
    v = np.clip(amax*np.minimum(t, T-t), 0, vmax)
    return t, v

t, v = trapezoid(dist=1.0, vmax=0.5, amax=1.0)
print("move time (s):", t[-1], " peak v:", v.max())
```

Bounding jerk also keeps the *required motor torque* continuous, avoiding the
current spikes a pure trapezoid demands at the corners.

**Next:** inertia matching and reflected load.
""",
        ),
        _t(
            "Inertia matching and reflected load",
            "11 min",
            r"""
# Inertia matching and reflected load

Through a reducer of ratio $N$, the load inertia *seen by the motor* is divided
by $N^2$: $J_\text{refl} = J_\text{load}/N^2$. The **inertia ratio**
$J_\text{load,refl} / J_\text{motor}$ governs how well the motor can control the
load. A common rule of thumb keeps it below 5–10:1 for responsive servos;
higher ratios make the system sluggish and prone to resonance.

For a load on a screw of lead $L$, mass $m$ reflects to the motor as a rotary
inertia $J = m\,(L/2\pi)^2$, which is why fine-lead screws make heavy loads
"feel" small to the motor.

```mermaid
flowchart LR
    JM[Motor inertia Jm] --> SUM[Total inertia at motor]
    JG[Gearbox inertia] --> SUM
    JL[Load inertia / N^2] --> SUM
    SUM --> ACC[Acceleration = torque / J_total]
```

There is an optimum: the gear ratio that **minimizes** the motor torque needed
to accelerate a given load is $N^\star = \sqrt{J_\text{load}/J_\text{motor}}$,
which exactly *matches* reflected load inertia to motor inertia. Near this point
the acceleration torque is least.

```plot
{"title": "Acceleration torque vs gear ratio (normalized)", "xLabel": "gear ratio N", "yLabel": "required torque (norm)", "xRange": [1,12], "yRange": [0,4], "grid": true, "functions": [{"expr": "x/10 + 4/x", "label": "torque(N) with optimum near matched inertia", "color": "#2563eb"}]}
```

The curve is U-shaped: too little reduction overworks the motor against the load,
too much wastes torque accelerating the reducer and motor rotor themselves.

**Next:** RMS-torque thermal sizing.
""",
        ),
        _t(
            "RMS torque and thermal sizing",
            "12 min",
            r"""
# RMS torque and thermal sizing

A servo's two torque limits are different. **Peak torque** must exceed the
worst instant of the move (usually during acceleration). But heating depends on
$i^2R$ losses averaged over the *whole cycle*, so the **continuous** limit is
governed by the **root-mean-square torque** over one duty cycle:

$$\tau_\text{rms} = \sqrt{\frac{1}{T}\int_0^T \tau(t)^2\,dt}$$

Sizing rule: choose a motor whose **continuous** rating exceeds $\tau_\text{rms}$
*and* whose **peak** rating exceeds $\tau_\text{peak}$, with margin. A motor can
deliver several times its continuous torque briefly, but only the RMS value
determines steady-state winding temperature.

```python
import numpy as np

# torque trace over one cycle: accel, cruise, decel, dwell
t  = np.linspace(0, 1.0, 1000)
tau = np.piecewise(t,
        [t < 0.2, (t>=0.2)&(t<0.6), (t>=0.6)&(t<0.8), t>=0.8],
        [3.0, 0.5, -3.0, 0.0])              # N*m
tau_rms  = np.sqrt(np.trapezoid(tau**2, t) / (t[-1]-t[0]))
tau_peak = np.abs(tau).max()
print(f"RMS torque = {tau_rms:.2f} N*m, peak = {tau_peak:.2f} N*m")
# select motor: continuous > 1.3*tau_rms, peak > 1.3*tau_peak
```

```plot
{"title": "Torque trace and its RMS level over one cycle", "xLabel": "time (s)", "yLabel": "torque (N*m)", "xRange": [0,1], "yRange": [-3.5,3.5], "grid": true, "functions": [{"expr": "1.46", "label": "RMS level", "color": "#dc2626"}]}
```

Don't forget the duty cycle: a long dwell lowers $\tau_\text{rms}$, letting a
smaller motor do a job whose peak looks intimidating.

**Next:** designing the velocity and current loops.
""",
        ),
        _t(
            "Cascaded velocity and current loops",
            "12 min",
            r"""
# Cascaded velocity and current loops

Servo drives use **cascaded PI loops**: an inner **current (torque)** loop and
an outer **velocity** loop, with the position loop outermost. The cascade only
works if each loop is markedly faster than the one outside it — typically the
current-loop bandwidth is 5–10× the velocity-loop bandwidth, so the outer loop
"sees" the inner loop as an ideal, fast torque source.

```mermaid
flowchart LR
    WC[velocity cmd] --> VP[velocity PI] --> IC[current cmd]
    IC --> CP[current PI] --> PWM[PWM / inverter] --> M[motor]
    M -- i --> CP
    M -- omega --> VP
```

Tune the current loop first (it sets the achievable torque bandwidth), then the
velocity loop. A clean design has a flat closed-loop magnitude out to the
crossover, then rolls off — the frequency-response shape below shows the
resonant peak that appears if damping is too low:

```plot
{"title": "Velocity-loop closed-loop magnitude", "xLabel": "frequency ratio w/wn", "yLabel": "|H|", "xRange": [0,3], "yRange": [0,3], "grid": true, "functions": [{"expr": "1/sqrt((1-x^2)^2 + (0.2*x)^2)", "label": "low damping (peak)", "color": "#dc2626"}, {"expr": "1/sqrt((1-x^2)^2 + (1.4*x)^2)", "label": "well damped", "color": "#16a34a"}]}
```

```python
import numpy as np
# Discrete PI current controller, one step
Kp, Ki, dt = 2.0, 800.0, 5e-5
integ = 0.0
def pi_step(err):
    global integ
    integ += err * dt
    return Kp*err + Ki*integ        # voltage command, then anti-windup clamp
```

**Anti-windup** on the integrator and feedforward of the back-EMF and inertia
torques are what separate a textbook PI from a production servo.

**Next:** feedback devices and positioning resolution.
""",
        ),
        _t(
            "Feedback devices and resolution",
            "11 min",
            r"""
# Feedback devices and resolution

Closed-loop motion is only as good as its **feedback device**. The common
choices:

- **Incremental encoder** — quadrature A/B channels; counts give relative
  position. With $N$ lines, quadrature decoding yields $4N$ counts/rev.
- **Absolute encoder** — reports the true angle at power-up; no homing needed.
- **Resolver** — rugged analog device for harsh/high-temperature environments.

**Resolution** is the smallest commanded increment; **accuracy** is how close
the true position is to commanded; **repeatability** is the spread on returning
to a point. They are different — a high-resolution encoder on a backlashed gear
is precise but inaccurate.

```mermaid
flowchart LR
    ENC[Encoder lines N] --> Q[Quadrature x4]
    Q --> CPR[4N counts/rev]
    CPR --> RES[Linear resolution = lead / 4N]
```

At the load, encoder counts map to distance through the transmission. For a
$2000$-line encoder behind a $5\,$mm-lead ball screw:

$$\text{resolution} = \frac{L}{4N} = \frac{5\ \text{mm}}{8000} = 0.625\ \mu\text{m}$$

```python
lines, lead_mm = 2000, 5.0
counts = 4 * lines
res_um = lead_mm * 1000 / counts
print(f"linear resolution = {res_um:.3f} um/count")  # 0.625 um
```

```plot
{"title": "Linear resolution vs encoder line count (5mm lead)", "xLabel": "encoder lines (k)", "yLabel": "resolution (um)", "xRange": [0.5,5], "yRange": [0,3], "grid": true, "functions": [{"expr": "1.25/x", "label": "resolution = lead/(4N)", "color": "#2563eb"}]}
```

Backlash, lost motion and encoder noise set a practical floor below the
theoretical resolution.

**Next:** check your understanding with a short quiz.
""",
        ),
        _quiz(),
    ),
)


# ── Actuators & Motion Systems — Advanced ────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="actuators-motion-systems-advanced",
    title="Actuators & Motion Systems — Advanced",
    description=(
        "State-of-the-art motion engineering: sensorless field-oriented control "
        "with observers, time-optimal and jerk-limited trajectory generation, "
        "input shaping and resonance suppression, model-based and learning "
        "iterative learning control, optimization-based actuator sizing and "
        "co-design, and a full precision nano-positioning case study. Includes "
        "Python/SciPy optimization and trajectory code."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Sensorless FOC and observers",
            "13 min",
            r"""
# Sensorless FOC and observers

**Field-oriented control (FOC)** transforms the three stator currents into a
rotating $d$-$q$ frame where torque ($i_q$) and flux ($i_d$) are controlled
independently, like a DC motor. The transform needs the rotor angle. **Sensorless**
FOC estimates that angle from currents and voltages, eliminating the encoder.

At medium/high speed a **back-EMF observer** works well: the back-EMF
$e = k_e\omega$ carries the angle. A sliding-mode or Luenberger observer
reconstructs it from the motor model:

$$\hat{\dot{x}} = A\hat{x} + Bu + Le_y, \qquad e_y = i - \hat{i}$$

At low/zero speed back-EMF vanishes, so **high-frequency injection** exploiting
magnetic saliency takes over.

```mermaid
flowchart LR
    I[i_abc] --> CLK[Clarke/Park] --> DQ[i_d, i_q]
    DQ --> PI[d-q PI ctrl] --> V[v_d, v_q]
    V --> SVPWM[SVPWM] --> INV[inverter] --> M[PMSM]
    M --> I
    V --> OBS[back-EMF observer] --> TH[theta_hat] --> CLK
```

```python
import numpy as np
# Sliding-mode back-EMF observer (alpha-beta), one step
def smo_step(i_meas, i_hat, v, e_hat, R, L, dt, k=80.0):
    err = i_hat - i_meas
    z = k * np.tanh(err / 0.5)                 # sliding control
    di = (v - R*i_hat - z) / L                 # plant copy
    i_hat = i_hat + di*dt
    e_hat = e_hat + 0.02*(z - e_hat)           # low-pass -> back-EMF est.
    theta = np.arctan2(-e_hat[0], e_hat[1])    # rotor angle from EMF
    return i_hat, e_hat, theta
```

Convergence of the angle estimate determines startup robustness and the lowest
controllable speed — the key spec of any sensorless drive.

**Next:** time-optimal, jerk-limited trajectories.
""",
        ),
        _t(
            "Time-optimal jerk-limited trajectories",
            "13 min",
            r"""
# Time-optimal jerk-limited trajectories

Beyond the textbook trapezoid lies **constrained time-optimal** planning: find
the fastest motion subject to bounds on velocity, acceleration *and* jerk, plus
the actuator's true torque-speed curve. With jerk bounded, the velocity profile
becomes a **7-segment S-curve**; with the full torque-speed envelope it becomes
a numerically optimized profile.

The general form is an optimal control problem solved by direct collocation:

$$\min_{u(\cdot),T} T \quad \text{s.t. } \dot{x}=f(x,u),\ |u|\le u_\max,\ |\dot a|\le j_\max$$

```python
import numpy as np
from scipy.optimize import minimize

# Jerk-limited point-to-point: minimize move time T with bounded a, j.
amax, jmax, dist = 5.0, 30.0, 1.0
def move_time(p):
    tj, ta = p                      # jerk-phase, accel-phase durations
    a = jmax*tj
    v = a*(tj+ta)                   # peak velocity reached
    d = v*(2*tj+ta)                 # distance over accel+decel (symmetric)
    pen = 1e3*(max(0,a-amax)**2 + (d-dist)**2)
    return 2*(2*tj+ta) + pen
r = minimize(move_time, [0.1,0.1], bounds=[(1e-3,1),(0,1)])
print("optimal jerk/accel phase times:", r.x)
```

```plot
{"title": "S-curve acceleration (bounded jerk) vs trapezoid", "xLabel": "time (s)", "yLabel": "acceleration", "xRange": [0,4], "yRange": [-1.3,1.3], "grid": true, "functions": [{"expr": "sin(x)", "label": "S-curve accel (smooth)", "color": "#16a34a"}]}
```

The optimization converges quickly once warm-started near the analytic S-curve:

```plot
{"title": "Optimizer cost convergence", "xLabel": "iteration", "yLabel": "cost (norm)", "xRange": [0,12], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "cost", "color": "#2563eb"}]}
```

**Next:** input shaping and resonance suppression.
""",
        ),
        _t(
            "Input shaping and resonance suppression",
            "12 min",
            r"""
# Input shaping and resonance suppression

Flexible structures — long arms, belts, gantries — have lightly damped resonant
modes that a fast move excites, leaving residual vibration that ruins settling
time. **Input shaping** convolves the command with a short sequence of impulses
designed so the vibration from each impulse cancels the others.

A **Zero-Vibration (ZV)** shaper for natural frequency $\omega_n$ and damping
$\zeta$ uses two impulses separated by half the damped period
$T_d = 2\pi/(\omega_n\sqrt{1-\zeta^2})$:

$$A_1 = \frac{1}{1+K},\ A_2 = \frac{K}{1+K},\quad K = e^{-\zeta\pi/\sqrt{1-\zeta^2}}$$

A **ZVD** shaper (three impulses) adds robustness to errors in $\omega_n$.

```python
import numpy as np
def zv_shaper(wn, zeta):
    K  = np.exp(-zeta*np.pi/np.sqrt(1-zeta**2))
    Td = 2*np.pi/(wn*np.sqrt(1-zeta**2))
    A  = np.array([1, K]) / (1+K)        # impulse amplitudes
    t  = np.array([0, Td/2])             # impulse times
    return t, A

t, A = zv_shaper(wn=2*np.pi*8, zeta=0.05)
print("impulse times (s):", t, " amplitudes:", A)  # sums to 1
```

The frequency response of the shaper shows a deep notch exactly at the resonance,
the residual-vibration "sensitivity curve":

```plot
{"title": "Residual vibration vs frequency error (ZV shaper)", "xLabel": "w/wn", "yLabel": "residual vibration", "xRange": [0,2], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "abs(cos(3.14159*x))", "label": "ZV sensitivity (notch at wn)", "color": "#dc2626"}]}
```

Input shaping costs only a small command delay and needs no extra sensors — it
is standard on cranes, wafer stages and SCARA robots.

**Next:** iterative learning control.
""",
        ),
        _t(
            "Iterative learning control",
            "12 min",
            r"""
# Iterative learning control

When a machine repeats the *same* trajectory over and over (a pick-and-place
cycle, a laser scan), **iterative learning control (ILC)** uses the tracking
error from one run to improve the feedforward command for the next. Over a few
iterations it drives repeatable error toward zero — beating any feedback
controller on repetitive disturbances.

The canonical first-order update on the feedforward $u_k$ over the error $e_k$:

$$u_{k+1}(t) = Q\big(u_k(t) + L\,e_k(t+\delta)\big)$$

where $L$ is the learning gain, $\delta$ a phase-lead, and $Q$ a low-pass
filter that bounds learning to frequencies where the plant model is trustworthy
(the robustness/convergence tradeoff).

```mermaid
flowchart LR
    MEM[memory: u_k, e_k] --> UPD[u_{k+1} = Q(u_k + L*e_k)]
    UPD --> RUN[run trajectory k+1]
    RUN --> ERR[measure e_{k+1}]
    ERR --> MEM
```

```python
import numpy as np
def ilc_update(u_k, e_k, L=0.5):
    # zero-phase low-pass Q as a simple moving average
    Q = np.convolve(u_k + L*e_k, np.ones(5)/5, mode='same')
    return Q

# error norm shrinks geometrically across iterations when |1 - L*G| < 1
```

```plot
{"title": "ILC tracking-error norm across iterations", "xLabel": "iteration k", "yLabel": "||e_k|| (norm)", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "geometric convergence", "color": "#16a34a"}]}
```

Modern variants fold in a learned plant model or even a neural feedforward, but
the convergence condition $|1 - LG(j\omega)| < 1$ over the passband of $Q$
remains the governing stability test.

**Next:** optimization-based sizing and co-design.
""",
        ),
        _t(
            "Optimization-based actuator sizing",
            "12 min",
            r"""
# Optimization-based actuator sizing

Classical sizing checks one candidate motor/gearbox against RMS and peak torque.
**Optimization-based sizing** instead searches the catalog (and the gear ratio)
to minimize an objective — mass, cost or energy — subject to those same physical
constraints, often jointly with the trajectory (**co-design**).

A mixed continuous/discrete formulation:

$$\min_{N,\,\text{motor}} \; \text{cost} \quad \text{s.t.}\ \tau_\text{rms}(N)\le \tau_\text{cont},\ \tau_\text{peak}(N)\le \tau_\text{pk},\ J_\text{ratio}\le 10$$

```python
import numpy as np
from scipy.optimize import minimize_scalar

J_load, J_motor, tau_cont, F = 2e-3, 1e-4, 1.2, 200.0
def reflected_torque(N):
    J = J_motor + J_load/N**2          # total inertia at motor
    a = 50.0                            # demanded accel (rad/s^2 at load)
    return J*a*N + F*0.005/(2*np.pi*N)  # accel + screw load torque
res = minimize_scalar(reflected_torque, bounds=(1, 30), method='bounded')
print(f"optimal ratio N* = {res.x:.1f}, motor torque = {res.fun:.3f} N*m")
```

The cost surface over gear ratio is convex with a clear optimum — the same
U-shape from inertia matching, now scored by motor torque:

```plot
{"title": "Sizing objective vs gear ratio", "xLabel": "gear ratio N", "yLabel": "motor torque (N*m)", "xRange": [1,30], "yRange": [0,2], "grid": true, "functions": [{"expr": "0.01*x + 1.5/x", "label": "objective (accel + load)", "color": "#2563eb"}]}
```

**Co-design** goes further: by optimizing the trajectory and the actuator
*together* you can shrink the motor, because a gentler profile lowers
$\tau_\text{peak}$ — a 20–40% mass saving is common in legged robots and drones.

**Next:** a precision nano-positioning case study.
""",
        ),
        _t(
            "Case study: precision nano-positioning",
            "13 min",
            r"""
# Case study: precision nano-positioning

A semiconductor wafer stage must position to **nanometers** over millimeters of
travel at high acceleration. No single actuator does both, so a **dual-stage**
design is used: a long-travel coarse actuator (linear motor + ball screw)
carries a short-travel, high-bandwidth **piezoelectric** fine stage.

```mermaid
flowchart LR
    REF[nm reference] --> SUM[error]
    SUM --> COARSE[coarse: linear motor, mm travel]
    SUM --> FINE[fine: piezo, um travel, kHz BW]
    COARSE --> PLANT[stage position]
    FINE --> PLANT
    PLANT --> ENC[interferometer / nm encoder] --> SUM
```

Design choices that make nanometers possible:

- **Interferometric feedback** with sub-nm resolution; the encoder, not the
  motor, sets the achievable accuracy.
- **Piezo fine stage** with kHz bandwidth to reject the residual error the slow
  coarse stage cannot, plus **hysteresis compensation** (Preisach/charge drive).
- **Input shaping + feedforward** so the coarse move settles without exciting
  frame resonances.
- **Air bearings / flexures** to remove friction and stick-slip at the nm scale.

The settling error after a coarse step, with and without the fine stage and
shaping, tells the whole story:

```plot
{"title": "Settling error after a step (dual-stage)", "xLabel": "time (ms)", "yLabel": "error (nm)", "xRange": [0,8], "yRange": [-40,40], "grid": true, "functions": [{"expr": "35*exp(-0.2*x)*cos(3*x)", "label": "coarse only (ringing)", "color": "#dc2626"}, {"expr": "35*exp(-1.5*x)", "label": "with fine stage + shaping", "color": "#16a34a"}]}
```

```python
import numpy as np
# Dual-stage allocation: fine stage handles high-freq error within its stroke
def allocate(err, fine_stroke=5e-6):
    fine   = np.clip(err, -fine_stroke, fine_stroke)
    coarse = err - fine                       # remainder to the slow stage
    return coarse, fine
```

The lesson generalizes: precision comes from the *system* — metrology, mechanics,
trajectory and control co-designed — not from any one heroic component.

**Next:** check your understanding with a short quiz.
""",
        ),
        _quiz(),
    ),
)


ACTUATORS_MOTION_SYSTEMS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ACTUATORS_MOTION_SYSTEMS_COURSES"]
