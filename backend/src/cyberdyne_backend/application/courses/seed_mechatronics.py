"""Mechatronics track: Basics -> Intermediate -> Advanced.

The synergistic integration of mechanics, electronics, control and computing:
from the system view and signal chain, through sensors, actuators, microcontrollers
and interfacing, to feedback control integration and a full mechatronic project.
Lessons are `text` with single-backslash LaTeX, interactive ```plot blocks for
response and frequency curves, ```mermaid diagrams for system architecture and
design workflows, and runnable ```python (NumPy/SciPy) and ```matlab code for
filtering, control design, kinematics and optimization.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


_BASICS = SeedCourse(
    slug="mechatronics-basics",
    title="Mechatronics — Basics",
    description=(
        "What mechatronics is and why it matters: the synergistic union of mechanical, "
        "electrical, control and computer engineering. Build intuition for the signal "
        "chain — physical quantity, sensor, signal conditioning, controller, actuator — "
        "with plenty of diagrams and worked numbers and minimal heavy math."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is mechatronics?",
            "10 min",
            r"""
# What is mechatronics?

**Mechatronics** is the synergistic integration of **mechanical** engineering, **electronics**, **control** theory and **computer** science to design smart products and systems. The word, coined at Yaskawa Electric in 1969, captures something more than the sum of its parts: a stepper-driven 3D printer, an anti-lock brake, a quadcopter and a camera autofocus are all mechatronic because intelligence is embedded where mechanics meets electronics.

The defining idea is the **closed loop**: a sensor measures the physical world, a controller (usually a microcontroller running software) decides, and an actuator acts back on the world. This feedback lets a cheap, imperfect mechanism behave precisely — the controller compensates for friction, backlash and disturbance in real time, replacing expensive precision hardware with software.

```mermaid
flowchart LR
  P[Mechanical system] --> S[Sensor]
  S --> C[Controller / MCU]
  C --> A[Actuator]
  A --> P
```

Compared with a purely mechanical design, the mechatronic approach moves complexity from hardware into software, lowering cost and raising flexibility — a firmware update can change behaviour with no new parts. The trade is that you must now reason across four disciplines at once.

```plot
{"title": "Settling of a feedback-controlled position", "xLabel": "t (s)", "yLabel": "position", "xRange": [0,8], "yRange": [0,1.3], "grid": true, "functions": [{"expr": "1 - exp(-0.7*x)*cos(2*x)", "label": "closed-loop response", "color": "#2563eb"}]}
```

**Next:** the four domains and where each contributes.
""",
        ),
        _t(
            "The four domains and the V-model",
            "11 min",
            r"""
# The four domains and the V-model

A mechatronic product lives in four overlapping domains. **Mechanical** supplies structure, kinematics and the load path. **Electrical/electronic** supplies power and the analog/digital signal hardware. **Control** supplies the algorithms that make behaviour stable and accurate. **Computing** supplies the embedded software, communication and timing. Real designs sit in the *intersection* — a motor mount is mechanical, but its stiffness sets the resonance the controller must avoid.

Development is commonly organised with the **V-model** (VDI 2206, the design methodology standard for mechatronic systems): the left arm decomposes requirements into system, then domain-specific design; the bottom is implementation; the right arm integrates and verifies upward against each left-arm level.

```mermaid
flowchart TB
  R[Requirements] --> SD[System design]
  SD --> DD[Domain design: mech / elec / SW]
  DD --> IMP[Implementation]
  IMP --> UT[Unit / module test]
  UT --> SI[System integration]
  SI --> VV[Verification vs requirements]
```

The lesson of the V-model is that **integration is designed in, not bolted on**: interfaces, signal ranges and timing budgets are agreed during system design so the domains can be built in parallel and meet cleanly. Skipping system-level design is the classic cause of a mechatronic project that "works on the bench" but fails as a whole.

**Next:** signals — the language shared across the domains.
""",
        ),
        _t(
            "Signals: analog, digital and sampling",
            "12 min",
            r"""
# Signals: analog, digital and sampling

Information flows through a mechatronic system as **signals**. An **analog** signal varies continuously in time and amplitude (a thermocouple voltage); a **digital** signal takes discrete values at discrete instants (the bits an ADC produces). The bridge between them is **sampling**: reading the analog value every $T_s$ seconds at rate $f_s=1/T_s$.

The **Nyquist–Shannon theorem** sets the rule: to reconstruct a signal containing frequencies up to $f_{max}$, you must sample faster than $f_s>2f_{max}$. Sample too slowly and high frequencies masquerade as low ones — **aliasing** — which no later processing can undo. The fix is an **anti-aliasing** low-pass filter before the ADC and a comfortable margin, often $f_s\approx 5$–$10\times$ the bandwidth of interest.

```plot
{"title": "Aliasing: a fast sine read too slowly looks slow", "xLabel": "t (s)", "yLabel": "amplitude", "xRange": [0,1], "yRange": [-1.2,1.2], "grid": true, "functions": [{"expr": "sin(2*3.1416*9*x)", "label": "true 9 Hz signal", "color": "#2563eb"}, {"expr": "sin(2*3.1416*1*x)", "label": "1 Hz alias", "color": "#dc2626"}]}
```

```python
import numpy as np
fs = 10.0                  # sampling rate (Hz)
f  = 9.0                   # true signal frequency (Hz)
# A 9 Hz tone sampled at 10 Hz aliases to |f - fs| = 1 Hz
alias = abs(f - round(f/fs)*fs)
print(f"observed frequency = {alias:.1f} Hz")  # -> 1.0 Hz
```

Quantisation adds a second discretisation: an $N$-bit ADC over range $V_{FS}$ has step $q=V_{FS}/2^N$ and contributes noise of about $q/\sqrt{12}$.

**Next:** measuring the world with sensors.
""",
        ),
        _t(
            "Sensors: turning physics into voltage",
            "12 min",
            r"""
# Sensors: turning physics into voltage

A **sensor** (transducer) converts a physical quantity into an electrical signal. The key specs are **sensitivity** (output per unit input, the slope), **range**, **resolution**, **linearity**, **accuracy** vs **precision**, and **bandwidth**. Everyday mechatronic sensors:

- **Potentiometer** — absolute angle/position as a resistance divider.
- **Strain gauge** — resistance change $\Delta R/R=GF\cdot\varepsilon$ (gauge factor $GF\approx2$) in a Wheatstone bridge; the heart of load cells.
- **Thermocouple / RTD / thermistor** — temperature.
- **Encoder** — incremental or absolute digital angle.
- **Accelerometer / gyro (MEMS IMU)** — motion and orientation.

Most sensors are modelled, near an operating point, by a linear calibration $y=S\,x+b$ where $S$ is sensitivity and $b$ an offset. Calibration finds $S$ and $b$ by fitting measured points.

```plot
{"title": "Linear sensor calibration (output vs measurand)", "xLabel": "measurand x", "yLabel": "output y (V)", "xRange": [0,10], "yRange": [0,5.5], "grid": true, "functions": [{"expr": "0.5*x + 0.2", "label": "y = S x + b", "color": "#16a34a"}]}
```

```python
import numpy as np
x = np.array([0, 2, 4, 6, 8, 10])         # applied measurand
y = np.array([0.21, 1.18, 2.22, 3.19, 4.20, 5.22])  # sensor volts
S, b = np.polyfit(x, y, 1)                 # least-squares calibration
print(f"sensitivity S = {S:.3f} V/unit, offset b = {b:.3f} V")
```

**Next:** acting on the world with actuators.
""",
        ),
        _t(
            "Actuators: moving the world",
            "11 min",
            r"""
# Actuators: moving the world

An **actuator** converts a control signal (usually electrical) into physical action — force, torque or displacement. The mechatronic staples:

- **DC motor** — torque $\tau=k_t\,i$ proportional to current; back-EMF $e=k_e\,\omega$ opposes motion. Simple, fast, needs a driver and feedback for precise position.
- **Stepper motor** — moves in fixed steps; open-loop positioning without an encoder, at the cost of possible step loss under overload.
- **Servo (RC/industrial)** — a motor plus built-in position feedback.
- **Solenoid** — on/off linear pull.
- **Pneumatic/hydraulic** — high force-to-weight, but compressible/heavy.
- **Piezo / shape-memory** — tiny, precise, niche.

Few loads can be driven directly, so an actuator is usually paired with a **driver** (H-bridge, stepper driver, ESC) that switches the power supply, and often a **transmission** (gearbox, lead screw, belt) that trades speed for torque by ratio $n$: $\tau_{out}=n\,\tau_{in}$, $\omega_{out}=\omega_{in}/n$.

```mermaid
flowchart LR
  C[Controller PWM] --> D[Driver / H-bridge]
  D --> M[Motor]
  M --> G[Gearbox ratio n]
  G --> L[Load]
```

```plot
{"title": "DC motor torque-speed curve", "xLabel": "speed (rad/s)", "yLabel": "torque (Nm)", "xRange": [0,100], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1 - 0.01*x", "label": "tau = tau_stall (1 - w/w_noload)", "color": "#dc2626"}]}
```

**Next:** check what you have learned.
""",
        ),
        _quiz(),
    ),
)


_INTERMEDIATE = SeedCourse(
    slug="mechatronics-intermediate",
    title="Mechatronics — Intermediate",
    description=(
        "The core quantitative methods that make a mechatronic system work: signal "
        "conditioning and the ADC/DAC chain, microcontroller timing with PWM and "
        "interrupts, digital communication buses, motor modelling and PWM drive, "
        "and the digital PID loop — with NumPy/SciPy and MATLAB code throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Signal conditioning and the ADC chain",
            "13 min",
            r"""
# Signal conditioning and the ADC chain

Raw sensor signals are rarely ready for a microcontroller's ADC. **Signal conditioning** amplifies, filters, levels and protects them. The canonical chain is **amplify -> filter -> level-shift -> sample**.

An **op-amp** sets gain: a non-inverting stage gives $G=1+R_f/R_g$, an inverting stage $G=-R_f/R_{in}$. An **instrumentation amplifier** rejects common-mode noise (a bridge sitting on a 2.5 V common mode) with high CMRR — essential for strain gauges and thermocouples.

The **anti-aliasing filter** is a low-pass set below $f_s/2$. A first-order RC has cutoff $f_c=1/(2\pi RC)$ and rolls off at 20 dB/decade:
$$|H(f)|=\frac{1}{\sqrt{1+(f/f_c)^2}}.$$

```plot
{"title": "First-order low-pass magnitude (fc = 1)", "xLabel": "f / fc", "yLabel": "|H|", "xRange": [0,8], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/sqrt(1 + x^2)", "label": "|H(f)|", "color": "#2563eb"}]}
```

Finally the ADC quantises: an $N$-bit converter over $V_{FS}$ has LSB $q=V_{FS}/2^N$, so code $=\mathrm{round}(V_{in}/q)$.

```python
import numpy as np
N, Vfs = 12, 3.3
q = Vfs / 2**N                         # LSB size
def adc(v): return int(round(np.clip(v,0,Vfs)/q))
print(f"LSB = {q*1e3:.2f} mV; reading 1.65 V -> code {adc(1.65)}")
```

**Next:** the microcontroller core that runs the loop.
""",
        ),
        _t(
            "Microcontrollers: timers, PWM and interrupts",
            "13 min",
            r"""
# Microcontrollers: timers, PWM and interrupts

The **microcontroller** (MCU) is the brain: a CPU, flash, RAM and a rich set of peripherals on one chip (ARM Cortex-M, AVR, ESP32). Two peripherals dominate mechatronics.

**PWM (pulse-width modulation)** emulates an analog level by switching a digital pin fast and varying its **duty cycle** $D$. The average delivered voltage is $\bar V=D\,V_{cc}$ — this is how you set motor speed or LED brightness with a binary pin. A timer counts to a period value (setting frequency) and toggles the pin at a compare value (setting duty).

**Interrupts** give deterministic timing. Rather than polling, the MCU runs an **interrupt service routine (ISR)** on an event — a timer overflow drives the control loop at an exact rate; an encoder edge increments a counter without missing pulses. Keep ISRs short and never block in them.

```mermaid
flowchart LR
  T[Timer overflow at fs] --> ISR[Control ISR]
  ISR --> RD[Read ADC / encoder]
  RD --> CTL[Compute control u]
  CTL --> PWM[Update PWM duty]
```

```python
# Map a control output u in [0,1] to a 16-bit timer compare value
def duty_to_compare(u, period_ticks):
    u = max(0.0, min(1.0, u))
    return int(round(u * period_ticks))

period = 1000                # timer top -> sets PWM frequency
print(duty_to_compare(0.30, period))   # 30% duty -> 300 ticks
```

A real-time loop needs a fixed, jitter-free $T_s$; a timer ISR provides exactly that.

**Next:** letting devices talk over digital buses.
""",
        ),
        _t(
            "Digital communication: I2C, SPI, UART, CAN",
            "12 min",
            r"""
# Digital communication: I2C, SPI, UART, CAN

Mechatronic systems are distributed: sensors, MCUs and drivers must exchange data over standard **serial buses**. The four you meet constantly:

- **UART** — asynchronous, two wires (TX/RX), no clock; both ends agree on a **baud rate**. Simple point-to-point (GPS, debug console).
- **SPI** — synchronous, full-duplex, fast (tens of MHz); master clock plus MOSI/MISO and one chip-select per device. Great for fast ADCs and displays.
- **I2C** — synchronous, two wires (SDA/SCL) shared by many devices addressed by a 7-bit address; slower but wiring-light (IMUs, EEPROMs).
- **CAN** — robust, multi-master, differential bus with arbitration and error checking; the backbone of automotive and industrial networks.

The headline trade is **wires vs speed vs robustness**: SPI is fastest but pin-hungry, I2C is wire-thrifty, CAN is the most fault-tolerant.

```mermaid
flowchart TB
  MCU[MCU master] -->|I2C SDA/SCL| IMU[IMU]
  MCU -->|I2C| EE[EEPROM]
  MCU -->|SPI| ADC[Fast ADC]
  MCU -->|CAN| ECU[Other ECU]
```

```python
# Bytes per second a UART can carry: 8 data bits cost 10 bits on the wire
def uart_throughput(baud, frame_bits=10):
    return baud / frame_bits        # bytes/s
print(f"{uart_throughput(115200):.0f} bytes/s at 115200 baud")
```

A throughput budget (samples/s x bytes/sample x overhead) tells you early whether a bus can carry your control data.

**Next:** modelling and driving a DC motor.
""",
        ),
        _t(
            "DC motor modelling and PWM drive",
            "13 min",
            r"""
# DC motor modelling and PWM drive

The DC motor is the workhorse actuator, and it has a clean linear model. Electrically, the armature obeys
$$V = R\,i + L\frac{di}{dt} + k_e\,\omega,$$
and mechanically Newton gives
$$J\frac{d\omega}{dt} = k_t\,i - b\,\omega - \tau_L,$$
with torque constant $k_t$, back-EMF constant $k_e$ (equal in SI), inertia $J$, damping $b$. Neglecting $L$ (electrical time constant is fast), the speed response to a step voltage is first order with time constant $\tau_m=RJ/(k_t k_e + Rb)$.

```plot
{"title": "Motor speed step response (first order)", "xLabel": "t (s)", "yLabel": "omega (normalised)", "xRange": [0,5], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1 - exp(-x/0.8)", "label": "omega(t) = K(1 - e^-t/tau)", "color": "#2563eb"}]}
```

A **PWM + H-bridge** drives it: duty cycle sets average voltage $\bar V=D\,V_{cc}$ and the H-bridge gives direction (and braking). Below, SciPy integrates the full two-state model.

```python
import numpy as np
from scipy.integrate import solve_ivp
R,L,ke,kt,J,b = 1.0,0.5e-3,0.01,0.01,1e-4,1e-5
V = 12.0
def motor(t, x):
    i, w = x
    di = (V - R*i - ke*w)/L
    dw = (kt*i - b*w)/J
    return [di, dw]
sol = solve_ivp(motor, [0,0.5], [0,0], max_step=1e-4)
print(f"steady-state speed ~ {sol.y[1,-1]:.0f} rad/s")
```

**Next:** closing the loop with a digital PID controller.
""",
        ),
        _t(
            "The digital PID loop",
            "14 min",
            r"""
# The digital PID loop

**PID** is the workhorse feedback law. From the error $e=r-y$ (reference minus measurement) it forms
$$u(t)=K_p\,e+K_i\!\int e\,dt+K_d\frac{de}{dt}.$$
**P** reacts to present error, **I** removes steady-state offset by accumulating past error, **D** anticipates by reacting to the trend (and adds damping).

On an MCU it runs in **discrete time** at period $T_s$. The simplest realisation integrates by sum and differentiates by backward difference:
$$u_k = K_p e_k + K_i T_s\!\sum_{j\le k} e_j + \frac{K_d}{T_s}(e_k-e_{k-1}).$$

```plot
{"title": "Closed-loop step: under-, critically and over-damped", "xLabel": "t (s)", "yLabel": "output", "xRange": [0,10], "yRange": [0,1.5], "grid": true, "functions": [{"expr": "1 - exp(-0.5*x)*cos(1.5*x)", "label": "under-damped", "color": "#dc2626"}, {"expr": "1 - exp(-1.2*x)*(1+1.2*x)", "label": "well damped", "color": "#16a34a"}]}
```

```python
class PID:
    def __init__(self, kp, ki, kd, Ts, umin=-1e9, umax=1e9):
        self.kp,self.ki,self.kd,self.Ts = kp,ki,kd,Ts
        self.umin,self.umax = umin,umax
        self.integ = 0.0; self.prev = 0.0
    def step(self, r, y):
        e = r - y
        self.integ += e*self.Ts
        d = (e - self.prev)/self.Ts
        u = self.kp*e + self.ki*self.integ + self.kd*d
        u = max(self.umin, min(self.umax, u))   # saturate
        # anti-windup: don't keep integrating once saturated
        if u in (self.umin, self.umax):
            self.integ -= e*self.Ts
        self.prev = e
        return u
```

Two practical must-haves: **integrator anti-windup** (above) and **derivative filtering** to tame measurement noise.

**Next:** check what you have learned.
""",
        ),
        _quiz(),
    ),
)


_ADVANCED = SeedCourse(
    slug="mechatronics-advanced",
    title="Mechatronics — Advanced",
    description=(
        "State-of-the-art and applied mechatronics: sensor fusion with the Kalman "
        "filter, state-space and pole-placement control, real-time systems and the "
        "digital twin, learning- and optimization-based control, and a full "
        "mechatronic design project tying every layer together — with NumPy/SciPy "
        "and MATLAB code throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Sensor fusion and the Kalman filter",
            "15 min",
            r"""
# Sensor fusion and the Kalman filter

Real sensors are noisy and incomplete: a gyro drifts, an accelerometer is noisy, an encoder is precise but only relative. **Sensor fusion** combines them into a better estimate than any one alone. The optimal linear-Gaussian fuser is the **Kalman filter**, which tracks both a state estimate $\hat x$ and its covariance $P$.

Each cycle has two stages. **Predict** rolls the model forward:
$$\hat x^- = F\hat x + Bu,\qquad P^- = FPF^\top + Q.$$
**Update** corrects with the measurement via the Kalman gain $K$:
$$K = P^-H^\top(HP^-H^\top + R)^{-1},\quad \hat x = \hat x^- + K(z - H\hat x^-),\quad P=(I-KH)P^-.$$
$Q$ is process noise (model trust), $R$ is measurement noise (sensor trust); $K$ blends them optimally. For nonlinear models the **EKF/UKF** linearise or sample around the estimate (the standard for IMU attitude and robot localisation).

```plot
{"title": "Estimate error covariance converging", "xLabel": "step", "yLabel": "trace(P)", "xRange": [0,12], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "uncertainty shrinks", "color": "#16a34a"}]}
```

```python
import numpy as np
F=np.array([[1,1.0],[0,1]]); H=np.array([[1.0,0]])
Q=np.eye(2)*1e-3; R=np.array([[0.1]])
x=np.zeros((2,1)); P=np.eye(2)
for z in [1.1, 1.9, 3.2, 3.9, 5.1]:        # noisy position reads
    x=F@x; P=F@P@F.T+Q                      # predict
    K=P@H.T@np.linalg.inv(H@P@H.T+R)        # gain
    x=x+K@(np.array([[z]])-H@x); P=(np.eye(2)-K@H)@P
print("pos,vel estimate:", x.ravel().round(2))
```

**Next:** designing controllers in state space.
""",
        ),
        _t(
            "State-space control and pole placement",
            "15 min",
            r"""
# State-space control and pole placement

PID handles single loops, but multivariable, coupled systems (a balancing robot, a quadrotor) call for **state-space** design. A linear plant is
$$\dot x = Ax + Bu,\qquad y = Cx.$$
If the pair $(A,B)$ is **controllable** (the controllability matrix $\mathcal C=[B\;AB\;\dots\;A^{n-1}B]$ has full rank), we can place the closed-loop poles anywhere with **full-state feedback** $u=-Kx$, giving $\dot x=(A-BK)x$. Choosing $K$ to set the eigenvalues of $A-BK$ is **pole placement**; choosing it to minimise $\int (x^\top Qx+u^\top Ru)\,dt$ is the **LQR**, the optimal quadratic regulator.

When the full state is not measured, an **observer (Luenberger or Kalman)** estimates it; the **separation principle** lets you design controller and observer independently.

```plot
{"title": "Pole location sets damping/speed of response", "xLabel": "t (s)", "yLabel": "state x1", "xRange": [0,6], "yRange": [-0.3,1.1], "grid": true, "functions": [{"expr": "exp(-1.0*x)*cos(2*x)", "label": "poles at -1 +- 2j", "color": "#2563eb"}, {"expr": "exp(-2.0*x)", "label": "real pole at -2", "color": "#16a34a"}]}
```

```python
import numpy as np
from scipy.signal import place_poles
A=np.array([[0,1.0],[0,0]]); B=np.array([[0],[1.0]])   # double integrator
des=np.array([-2+2j, -2-2j])                            # desired poles
K=place_poles(A,B,des).gain_matrix
print("feedback gain K =", K.round(2))
print("closed-loop poles:", np.linalg.eigvals(A-B@K).round(2))
```

**Next:** running it all in real time.
""",
        ),
        _t(
            "Real-time systems and the digital twin",
            "14 min",
            r"""
# Real-time systems and the digital twin

A control law is only correct if it runs **on time**. A **real-time system** guarantees deadlines: in a **hard** real-time loop a late control update is a failure, not just slow. The control ISR must finish well inside its period $T_s$; the spare fraction is the **timing margin**. Designers budget worst-case execution time (WCET) and bound **jitter**, the variation in actual sample instants, because jitter injects effective noise into the derivative term.

An **RTOS** (FreeRTOS, Zephyr) schedules tasks by priority — **rate-monotonic** assigns higher priority to faster tasks; the loop runs in a high-priority task triggered by a timer, while logging and comms run lower.

A **digital twin** is a live, physics-based simulation of the machine, fed by its real sensor stream. It enables hardware-in-the-loop (HIL) testing, predictive maintenance and tuning controllers in software before touching metal.

```mermaid
flowchart LR
  PH[Physical machine] -->|sensor data| DT[Digital twin model]
  DT -->|predicted state| MON[Monitoring / maintenance]
  DT -->|safe tuning| CTL[Controller]
  CTL --> PH
```

```python
import numpy as np
Ts = 1e-3                                  # 1 kHz loop
exec_times = np.array([0.62, 0.71, 0.58, 0.95, 0.66])*1e-3  # measured WCET
margin = (Ts - exec_times.max())/Ts*100
print(f"worst-case CPU use {exec_times.max()/Ts*100:.0f}%, margin {margin:.0f}%")
```

**Next:** learning- and optimization-based control.
""",
        ),
        _t(
            "Learning and optimization in mechatronics",
            "15 min",
            r"""
# Learning and optimization in mechatronics

Classical control needs a model; modern mechatronics increasingly **learns** or **optimizes** behaviour. Three workhorses:

- **Model Predictive Control (MPC)** solves, every sample, a finite-horizon optimization $\min_u \sum_k \|x_k-x_{ref}\|_Q^2+\|u_k\|_R^2$ subject to the model and to hard constraints (torque limits, joint limits) — its killer feature.
- **Reinforcement learning (RL)** learns a policy by trial-and-error reward, useful when the dynamics are hard to model (contact, friction); trained in a digital twin, then transferred (sim-to-real).
- **Parameter optimization / auto-tuning** fits gains or model parameters by minimising a cost, e.g. gradient descent or evolutionary search on settling time and overshoot.

All three are **optimization at heart**, and a well-posed cost converges smoothly.

```plot
{"title": "Auto-tuning cost converging over iterations", "xLabel": "iteration", "yLabel": "cost J", "xRange": [0,12], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "J(theta) decreasing", "color": "#16a34a"}]}
```

```python
import numpy as np
# Gradient-descent auto-tune of a scalar gain minimising a convex cost
def cost(k):  return (k - 2.5)**2 + 0.1      # minimum at k=2.5
def grad(k):  return 2*(k - 2.5)
k, lr = 0.0, 0.2
for _ in range(20):
    k -= lr*grad(k)
print(f"tuned gain k = {k:.3f} (target 2.5), cost {cost(k):.3f}")
```

**Next:** integrating everything into one design project.
""",
        ),
        _t(
            "A full mechatronic design project",
            "15 min",
            r"""
# A full mechatronic design project

Tie the track together with an integrated project: a **self-balancing two-wheeled robot** (an inverted pendulum on wheels). It exercises every layer — mechanics, sensing, computing, control — and fails loudly if any layer is weak.

The **design flow** follows the V-model: requirements (stay upright, follow a speed command) -> system design (state $[\text{tilt},\dot{\text{tilt}},\text{pos},\dot{\text{pos}}]$, 200 Hz loop) -> domain design -> integration -> verification.

Each layer maps to the track: an **IMU** (sensor) feeds a **complementary/Kalman filter** (fusion) for tilt; an **MCU** runs the loop on a **timer ISR** (real-time); a **state-feedback / LQR** law (control) computes wheel torque; **PWM + H-bridge** (actuation) drives the motors; an **encoder** closes the position loop; **I2C/SPI** carry sensor data.

```mermaid
flowchart LR
  IMU[IMU + encoders] --> KF[Kalman filter]
  KF --> LQR[LQR / state feedback]
  LQR --> PWM[PWM H-bridge]
  PWM --> M[Motors + wheels]
  M --> PLANT[Robot body]
  PLANT --> IMU
```

```python
import numpy as np
# Inverted-pendulum-on-cart linearisation -> LQR balancing gain
from scipy.linalg import solve_continuous_are
A=np.array([[0,1,0,0],[16,0,0,0],[0,0,0,1],[-2,0,0,0]])
B=np.array([[0],[-1.5],[0],[0.8]])
Q=np.diag([10,1,1,1]); Rr=np.array([[0.1]])
P=solve_continuous_are(A,B,Q,Rr)
K=np.linalg.inv(Rr)@B.T@P
print("balancing gain K =", K.round(2))
```

The lesson: a mechatronic system succeeds at the **interfaces**, when each discipline's design respects the others.

**Next:** check what you have learned.
""",
        ),
        _quiz(),
    ),
)


MECHATRONICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MECHATRONICS_COURSES"]
