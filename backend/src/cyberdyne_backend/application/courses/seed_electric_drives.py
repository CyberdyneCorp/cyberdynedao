"""Electric Drives & Motor Control track: Basics -> Intermediate -> Advanced.

From the drive block diagram and motor types, through PWM inverters, scalar V/f
control and cascaded current/speed loops, to field-oriented (vector) control,
space-vector PWM, direct torque control, sensorless observers and a full servo
drive design case study. Lessons are `text` with LaTeX, interactive ```plot
blocks (torque-speed curves, PWM waveforms, V/f profiles, step responses) and
```mermaid block diagrams of the drive system, inverter and control loops.
"""

# Lesson prose uses typographic characters (×, →, ≈, ω, τ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Electric Drives & Motor Control — Basics ─────────────────────────────────

_ED_BASICS = SeedCourse(
    slug="electric-drives-basics",
    title="Electric Drives & Motor Control — Basics",
    description=(
        "What an electric drive is and how its blocks fit together: the motor "
        "types used in drives (DC, induction, PMSM/BLDC), torque-speed "
        "characteristics and load matching, the power-electronic converters that "
        "feed the motor, four-quadrant operation, and the basic ideas of speed "
        "and torque control. Interactive torque-speed plots and a drive block "
        "diagram."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is an electric drive?",
            "10 min",
            """\
# What is an electric drive?

An **electric drive** is the complete system that converts electrical energy
into controlled mechanical motion. It is far more than a bare motor: it is the
chain that takes a *command* (a desired speed or torque) and a *power source*
and delivers a precisely controlled shaft output to a mechanical load.

A modern drive has four functional blocks:

- **Power converter** — power electronics (rectifier + inverter) that shape
  voltage and current fed to the motor.
- **Motor** — the electromechanical energy converter (DC, induction, PMSM…).
- **Sensors / feedback** — current, position and speed measurement.
- **Controller** — the brain that compares command to feedback and drives the
  converter so the error goes to zero.

```mermaid
flowchart LR
    CMD[Speed / torque command] --> CTRL[Controller]
    CTRL --> CONV[Power converter<br/>rectifier + inverter]
    SRC[AC / DC supply] --> CONV
    CONV --> M[Motor]
    M --> LOAD[Mechanical load]
    M -- current / speed / position --> FB[Sensors]
    FB --> CTRL
```

The defining feature is the **feedback loop**: the controller continuously
measures what the motor is doing and corrects the converter output. That is what
separates a *drive* from simply switching a motor on.

Drives move roughly half of all generated electricity through pumps, fans,
conveyors, EV traction and robotics — so efficient, controllable drives are a
huge lever on energy use.

**Next:** the motor types that sit inside a drive.
""",
        ),
        _t(
            "Motor types for drives",
            "11 min",
            """\
# Motor types for drives

Different motors trade off cost, control complexity and performance.

**DC motor** — torque is set directly by armature current, $\\tau = k_t\\, i_a$,
and back-EMF $e = k_e\\,\\omega$ rises with speed. Dead simple to control (one
current loop), but the mechanical **commutator and brushes** wear out.

**Induction motor (IM)** — rugged, cheap, brushless. A rotating stator field
drags the rotor along at a **slip** below synchronous speed. The workhorse of
industry, but its rotor quantities are not directly accessible, so control is
harder.

**Permanent-magnet synchronous (PMSM) / brushless DC (BLDC)** — magnets on the
rotor give the highest torque density and efficiency; the rotor turns exactly in
step with the stator field. Needs **rotor position** feedback and electronic
commutation, but dominates servos, robotics and EV traction.

| Motor | Brushes | Control effort | Typical use |
|-------|---------|----------------|-------------|
| DC | yes | low | legacy, simple |
| Induction | no | medium | pumps, fans, conveyors |
| PMSM / BLDC | no | high | servos, EV, robotics |

The choice fixes everything downstream — the converter, the sensors and the
control algorithm.

**Next:** how a motor's torque varies with speed, and matching it to a load.
""",
        ),
        _t(
            "Torque-speed characteristics & load matching",
            "12 min",
            """\
# Torque-speed characteristics & load matching

Every motor has a **torque-speed characteristic** $\\tau_m(\\omega)$, and every
load has its own demand curve $\\tau_L(\\omega)$. The drive settles at the
**operating point** where the two cross — that is where motor torque equals load
torque and the speed stops changing.

Common load curves:

- **Constant torque** (conveyors, hoists): $\\tau_L$ flat with speed.
- **Fan / pump** (square law): $\\tau_L \\propto \\omega^2$.
- **Constant power** (winders): $\\tau_L \\propto 1/\\omega$.

Below, the blue curve is a motor whose torque falls with speed and the red curve
is a fan load rising as $\\omega^2$; they cross at the steady operating point:

```plot
{"title": "Operating point = motor curve meets load curve", "xLabel": "speed ω (per-unit)", "yLabel": "torque τ (per-unit)", "xRange": [0, 1.2], "yRange": [0, 1.4], "functions": [{"expr": "1.2 - 0.9*x", "label": "motor τ(ω)", "color": "#2563eb"}, {"expr": "0.9*x^2", "label": "fan load ∝ ω²", "color": "#dc2626"}], "points": [{"x": 0.83, "y": 0.62, "label": "operating point", "color": "#16a34a", "size": 7}]}
```

**Load matching** means picking a motor (and gearing) whose curve crosses the
load at the desired speed with torque to spare for acceleration, and whose
continuous rating is not exceeded. Too small a motor stalls or overheats; too
large wastes cost and runs inefficiently.

The **acceleration** comes from the *gap* between the curves:
$J\\,\\dfrac{d\\omega}{dt} = \\tau_m - \\tau_L$, where $J$ is the combined inertia.

**Next:** the power electronics that feed the motor.
""",
        ),
        _t(
            "Power-electronic converters for drives",
            "11 min",
            """\
# Power-electronic converters for drives

The converter is what makes a drive *controllable* — it shapes the voltage and
current delivered to the motor. A typical AC drive has two stages around a DC
link:

```mermaid
flowchart LR
    AC[3-phase AC mains] --> REC[Rectifier<br/>AC → DC]
    REC --> DCL[DC link<br/>capacitor]
    DCL --> INV[Inverter<br/>DC → variable AC]
    INV --> M[Motor]
```

- **Rectifier** — converts fixed AC mains into a roughly constant **DC-link**
  voltage. A simple diode bridge is cheap but one-directional; an active
  front-end allows power to flow back.
- **DC link** — a capacitor (and sometimes inductor) that stiffens the DC
  voltage and buffers energy between the two stages.
- **Inverter** — six switches (IGBTs or MOSFETs) chop the DC link to synthesise
  **variable-voltage, variable-frequency** AC for the motor. This is where speed
  control happens.

The switches are turned on and off thousands of times per second; by varying the
*fraction of time* each switch is on (its **duty cycle**) the inverter controls
the average voltage applied. The next courses unpack exactly how.

For a DC-motor drive the inverter is replaced by a simpler **DC chopper** that
varies the average armature voltage, but the principle — switching to control an
average — is identical.

**Next:** running the motor in all four quadrants.
""",
        ),
        _t(
            "Four-quadrant operation",
            "10 min",
            """\
# Four-quadrant operation

Plot **torque** against **speed** with both signs allowed and you get four
quadrants. A drive's capability is defined by which quadrants it can operate in.

- **Quadrant I** — speed +, torque + → **forward motoring** (power into the
  load).
- **Quadrant II** — speed +, torque − → **forward braking / regeneration**
  (load drives the motor; power flows back).
- **Quadrant III** — speed −, torque − → **reverse motoring**.
- **Quadrant IV** — speed −, torque + → **reverse braking**.

```plot
{"title": "Four quadrants: motoring (power out) vs braking (power back)", "xLabel": "speed ω", "yLabel": "torque τ", "xRange": [-1.2, 1.2], "yRange": [-1.2, 1.2], "functions": [{"expr": "0*x", "label": "τ = 0", "color": "#94a3b8"}], "points": [{"x": 0.7, "y": 0.7, "label": "I: fwd motoring", "color": "#2563eb", "size": 6}, {"x": 0.7, "y": -0.7, "label": "II: fwd braking", "color": "#16a34a", "size": 6}, {"x": -0.7, "y": -0.7, "label": "III: rev motoring", "color": "#2563eb", "size": 6}, {"x": -0.7, "y": 0.7, "label": "IV: rev braking", "color": "#16a34a", "size": 6}]}
```

**Power** is $P = \\tau\\,\\omega$: in quadrants I and III torque and speed have the
*same* sign, so power is positive (motoring). In II and IV they have *opposite*
signs, so power is negative — the machine is a **generator** and energy flows
back toward the converter.

A four-quadrant drive can accelerate, brake, reverse and hold a load in either
direction — essential for hoists, EVs and servos. A simple diode-rectifier drive
can only motor (the energy has nowhere to go on braking) unless a brake resistor
or active front-end is added.

**Next:** the basic ideas of controlling speed and torque.
""",
        ),
        _t(
            "Basic speed & torque control concepts",
            "11 min",
            """\
# Basic speed & torque control concepts

How does a controller actually make the motor follow a command? The core idea is
**closed-loop control**: measure the output, compare it to the reference, and act
on the error.

A speed loop in words:

1. **Reference** $\\omega^*$ — the desired speed.
2. **Error** $e = \\omega^* - \\omega$ — reference minus measured speed.
3. **Controller** (typically **PI**) — output $\\propto K_p e + K_i\\!\\int e\\,dt$.
4. The output becomes the **torque command**, which the converter realises by
   controlling motor current (since $\\tau \\propto i$).
5. The new torque changes the speed; loop repeats.

```mermaid
flowchart LR
    REF["ω*"] --> SUM(("Σ"))
    SUM -- error --> PI[PI controller]
    PI -- "τ* (torque cmd)" --> DRV[Converter + motor]
    DRV -- ω --> SENS[Speed sensor]
    SENS -- "−ω" --> SUM
```

Two key concepts:

- **Torque control is inner, speed control is outer.** Because torque responds
  faster than speed, drives nest a fast torque (current) loop inside a slower
  speed loop — the **cascaded** structure you will meet in detail next course.
- **Tuning** the PI gains trades off **response speed** against **overshoot and
  stability**. Too much gain rings or goes unstable; too little is sluggish.

With these basics — blocks, motors, torque-speed matching, converters, four
quadrants and the feedback loop — you have the mental model of every drive.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Electric Drives & Motor Control — Intermediate ───────────────────────────

_ED_INTERMEDIATE = SeedCourse(
    slug="electric-drives-intermediate",
    title="Electric Drives & Motor Control — Intermediate",
    description=(
        "The control machinery of real drives: closed-loop DC speed control, PWM "
        "and the voltage-source inverter, scalar V/f control of induction motors, "
        "cascaded current and speed loops, feedback devices (encoders, resolvers, "
        "Hall sensors) and regenerative braking. With PWM and V/f plots and an "
        "inverter block diagram."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "DC motor drives & closed-loop speed control",
            "11 min",
            """\
# DC motor drives & closed-loop speed control

The DC drive is the clearest place to learn closed-loop control because the
physics is linear and decoupled. The armature obeys

$$V_a = R_a i_a + L_a\\frac{di_a}{dt} + k_e\\,\\omega,
\\qquad \\tau = k_t\\, i_a,$$

so **armature voltage sets speed** and **armature current sets torque** — two
independent handles.

A DC drive nests two loops:

- **Inner current loop** — a PI controller forces $i_a$ to follow the torque
  command, by adjusting the chopper duty cycle. Fast (kHz-class).
- **Outer speed loop** — a PI controller turns speed error into the current
  reference. Slower, since speed has mechanical inertia.

```plot
{"title": "Closed-loop speed: response to a step reference", "xLabel": "time (s)", "yLabel": "speed ω (per-unit)", "xRange": [0, 1.2], "yRange": [0, 1.3], "functions": [{"expr": "1 - exp(-6*x)", "label": "well-tuned PI", "color": "#2563eb"}, {"expr": "1 - exp(-2*x)", "label": "sluggish (low gain)", "color": "#94a3b8"}], "points": [{"x": 0, "y": 1, "label": "reference ω*", "color": "#dc2626", "size": 6}]}
```

A higher-gain PI reaches the reference faster but risks overshoot; a low-gain PI
is slow but smooth. The current limit in the inner loop also gives free
**protection**: torque (and heating) can never exceed the set ceiling, which is
why the controller naturally limits acceleration.

**Next:** how the inverter actually synthesises a variable voltage — PWM.
""",
        ),
        _t(
            "PWM & the voltage-source inverter",
            "12 min",
            """\
# PWM & the voltage-source inverter

A **voltage-source inverter (VSI)** uses six switches (three legs, two switches
each) to connect each motor phase to either the top or bottom of the DC link.
Switching alone gives only full-on or full-off — so we use **pulse-width
modulation (PWM)** to control the *average*.

```mermaid
flowchart TB
    DCp["+ DC link"] --> Sa1 & Sb1 & Sc1
    Sa1 --> A((A)) --> Sa2
    Sb1 --> B((B)) --> Sb2
    Sc1 --> C((C)) --> Sc2
    Sa2 & Sb2 & Sc2 --> DCn["− DC link"]
    A & B & C --> MOT[Motor windings]
```

In **sine-triangle PWM** a low-frequency sinusoidal *reference* is compared to a
high-frequency *triangular carrier*. When the sine is above the carrier the top
switch is on; otherwise the bottom is. The **duty cycle** therefore tracks the
sine, so the *average* phase voltage is sinusoidal even though the instantaneous
voltage is a train of pulses:

```plot
{"title": "PWM: average (sine) emerges from a switched pulse train", "xLabel": "phase angle (rad)", "yLabel": "voltage (per-unit)", "xRange": [0, 6.283], "yRange": [-1.2, 1.2], "functions": [{"expr": "0.9*sin(x)", "label": "reference / average", "color": "#dc2626"}, {"expr": "0.9*sin(x) + 0.12*sin(21*x)", "label": "switched output (approx)", "color": "#2563eb"}]}
```

Key parameters:

- **Switching frequency** $f_{sw}$ — higher gives smoother current and quieter
  operation, but more switching loss.
- **Modulation index** $m$ — the reference amplitude relative to the carrier;
  it sets the output voltage magnitude (linear up to $m=1$).

A **dead-time** delay between turning one switch off and its partner on prevents
shoot-through (both switches in a leg conducting and shorting the DC link).

**Next:** the simplest way to run an induction motor at variable speed — V/f.
""",
        ),
        _t(
            "Scalar V/f control of induction motors",
            "12 min",
            """\
# Scalar V/f control of induction motors

The cheapest, most common induction-motor drive is **scalar (V/f) control**. The
synchronous speed is set by the supply frequency,
$\\omega_s = 2\\pi f / (p/2)$, so to vary speed you vary $f$.

But you cannot vary frequency alone. The stator flux is roughly
$\\lambda \\approx V/(2\\pi f)$. Drop $f$ at fixed $V$ and the flux *soars*,
saturating the iron and overheating the motor. The fix: keep the ratio
**$V/f$ constant**, so flux stays at its rated value across the speed range.

```plot
{"title": "V/f profile: linear region + constant-V field weakening", "xLabel": "frequency f (Hz)", "yLabel": "voltage V (per-unit)", "xRange": [0, 80], "yRange": [0, 1.15], "functions": [{"expr": "0.05 + 0.0158*x", "label": "V/f = const (+ boost)", "color": "#2563eb"}, {"expr": "1", "label": "voltage ceiling", "color": "#94a3b8"}], "points": [{"x": 60, "y": 1.0, "label": "base / rated point", "color": "#dc2626", "size": 7}]}
```

Two regions:

- **Below base speed** — $V$ rises linearly with $f$ to hold $V/f$ constant, so
  flux and available torque stay constant. A small **voltage boost** at low $f$
  compensates the stator resistance drop.
- **Above base speed** — $V$ is clamped at its ceiling, so $V/f$ (and flux) fall.
  This is **field weakening**: speed rises but maximum torque drops, giving a
  constant-power region.

V/f is **open-loop on torque** — simple and robust, great for fans and pumps, but
it has poor dynamic response and weak low-speed torque. For demanding loads you
need current control and, eventually, vector control.

**Next:** building proper current and speed loops.
""",
        ),
        _t(
            "Current control loops & cascaded control",
            "11 min",
            """\
# Current control loops & cascaded control

High-performance drives are built as **cascaded loops**: a fast inner loop nested
inside a slower outer loop. Because torque is set by current, the innermost loop
is almost always a **current (torque) loop**.

```mermaid
flowchart LR
    WREF["ω*"] --> S1(("Σ")) --> SPI[Speed PI]
    SPI -- "i*" --> S2(("Σ")) --> CPI[Current PI]
    CPI -- "v*" --> PWM[PWM inverter] --> M[Motor]
    M -- i --> S2
    M -- ω --> S1
```

The design rule is **bandwidth separation**: each inner loop must be several
times faster than the loop outside it, so the outer loop "sees" the inner loop as
an ideal, instantaneous block.

- **Current loop** (fastest, kHz): a PI regulator drives the voltage reference so
  measured current follows $i^*$. It also enforces the **current limit** that
  protects the switches and motor.
- **Speed loop** (medium): a PI regulator turns speed error into the current
  reference $i^*$.
- **Position loop** (slowest, servos only): turns position error into the speed
  reference.

Cascading gives clean, independent tuning (one loop at a time, inside-out) and
**limit handling for free** — saturating $i^*$ at the speed-loop output directly
bounds torque. It is the backbone structure of every modern field-oriented
drive.

**Next:** the sensors that close these loops.
""",
        ),
        _t(
            "Feedback devices: encoders, resolvers & Hall sensors",
            "10 min",
            """\
# Feedback devices: encoders, resolvers & Hall sensors

Closed-loop control needs to *measure* current, speed and position. Current is
sensed with shunts or Hall current transducers; **shaft position and speed** come
from dedicated feedback devices.

- **Incremental encoder** — an optical disk emits two square waves (A, B) in
  quadrature; counting edges gives position, the A/B phase order gives direction,
  and a Z pulse marks one reference per revolution. High resolution, low cost, but
  gives only *relative* position until it sees the index.
- **Absolute encoder** — outputs a unique digital code for every position, so the
  angle is known the instant power is applied — vital for safe servo start-up.
- **Resolver** — a rugged rotary transformer; sine and cosine windings produce
  $\\sin\\theta$ and $\\cos\\theta$, from which $\\theta$ is recovered. Survives heat,
  vibration and dirt — favoured in EV traction and aerospace.
- **Hall-effect sensors** — three digital sensors give 60°-resolution rotor
  position, just enough to commutate a BLDC motor cheaply.

The choice is set by the control method. **V/f** needs little or none; a **vector
drive** needs accurate, high-resolution position (encoder or resolver) to align
its reference frame with the rotor. Resolution and latency of the sensor directly
cap the achievable loop bandwidth and smoothness.

**Next:** recovering energy when the motor brakes.
""",
        ),
        _t(
            "Regenerative braking & energy recovery",
            "11 min",
            """\
# Regenerative braking & energy recovery

When a drive **decelerates** a load or holds an overhauling load (a descending
hoist, a braking EV), the motor runs as a **generator**: speed and torque have
opposite signs, power is negative, and energy flows *back* from the motor into the
DC link (quadrants II and IV from the Basics course).

That energy has to go somewhere. Three options:

- **Brake resistor (dynamic braking)** — when the DC-link voltage rises, a
  chopper dumps the energy into a resistor as heat. Simple and cheap, but the
  energy is wasted.
- **Regenerative front-end** — an *active* rectifier (or a back-to-back inverter)
  returns the energy to the AC mains. Efficient; standard in elevators, cranes and
  test rigs that brake often.
- **Energy storage** — a battery or supercapacitor on the DC link absorbs the
  energy and reuses it. This is exactly **EV regenerative braking**, recharging
  the pack on every slowdown.

```plot
{"title": "DC-link voltage rises during regen until the brake chopper acts", "xLabel": "time (s)", "yLabel": "DC-link voltage (per-unit)", "xRange": [0, 1.0], "yRange": [0.9, 1.25], "functions": [{"expr": "1 + 0.18*(1 - exp(-12*x))*exp(-3*x)", "label": "V_dc during braking", "color": "#2563eb"}, {"expr": "1.15", "label": "chopper threshold", "color": "#dc2626"}]}
```

A diode-rectifier drive **cannot** push energy back to the mains, so without a
brake resistor the DC link would overvoltage and trip. Recovering braking energy
can cut total system energy use substantially in cyclic applications.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Electric Drives & Motor Control — Advanced ───────────────────────────────

_ED_ADVANCED = SeedCourse(
    slug="electric-drives-advanced",
    title="Electric Drives & Motor Control — Advanced",
    description=(
        "High-performance motor control: field-oriented (vector) control in the dq "
        "frame, space-vector PWM, direct torque control, sensorless control with "
        "observers, servo drives and motion profiles, and a full drive design case "
        "study covering motor sizing and control-loop tuning. With dq-frame step "
        "responses, an SVPWM hexagon and an FOC control-loop diagram."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Field-oriented (vector) control",
            "13 min",
            """\
# Field-oriented (vector) control

**Field-oriented control (FOC)** makes an AC motor behave like the easy DC motor:
it lets you control torque and flux *independently*. The trick is a change of
reference frame.

The three stator currents are transformed into a frame **rotating with the
rotor** (the **dq frame**) via Clarke ($abc\\to\\alpha\\beta$) and Park
($\\alpha\\beta\\to dq$) transforms. In that frame the AC quantities become DC:

- **$i_d$** — the **flux-producing** current (aligned with the rotor field).
- **$i_q$** — the **torque-producing** current (90° ahead).

Torque becomes the clean, DC-like law $\\tau = \\frac{3}{2}\\,\\frac{p}{2}\\,
\\lambda_{pm}\\, i_q$. For a surface PMSM you simply set $i_d = 0$ and command
torque through $i_q$.

```mermaid
flowchart LR
    WREF["ω*"] --> SPI[Speed PI] --> IQ["i_q*"]
    ID["i_d* = 0"] --> CPI
    IQ --> CPI[dq current PI]
    CPI -- "v_d, v_q" --> IPARK[Inverse Park] --> SVPWM[SVPWM] --> INV[Inverter] --> M[Motor]
    M -- i_abc --> CLARKE[Clarke + Park] --> CPI
    M -- θ --> CLARKE & IPARK
```

Because the controlled quantities are DC, simple PI regulators give zero
steady-state error and a fast, well-damped torque response:

```plot
{"title": "FOC torque step: i_q tracks its command in milliseconds", "xLabel": "time (ms)", "yLabel": "torque-producing current i_q (per-unit)", "xRange": [0, 8], "yRange": [0, 1.2], "functions": [{"expr": "1 - exp(-1.4*x)", "label": "i_q response", "color": "#2563eb"}], "points": [{"x": 0, "y": 1, "label": "i_q* command", "color": "#dc2626", "size": 6}]}
```

FOC needs accurate **rotor angle** $\\theta$ (encoder/resolver, or estimated) and
real-time computation, but it delivers the smooth, high-bandwidth torque control
that servos, robotics and EV traction demand.

**Next:** the modulation that realises the FOC voltage command — SVPWM.
""",
        ),
        _t(
            "Space-vector PWM",
            "12 min",
            """\
# Space-vector PWM

FOC produces a desired stator voltage *vector*. **Space-vector PWM (SVPWM)** is
the modern way to synthesise it, using the inverter's switching states more
efficiently than sine-triangle PWM.

The three-leg inverter has $2^3 = 8$ switching states: **six active vectors**
($V_1\\ldots V_6$) at the corners of a hexagon, plus **two zero vectors** ($V_0,
V_7$) at the centre. Any reference vector $V^*$ inside the hexagon is produced by
**time-averaging** the two adjacent active vectors plus a zero vector over each
switching period:

$$V^* = \\frac{t_1}{T_s}V_k + \\frac{t_2}{T_s}V_{k+1}
       + \\frac{t_0}{T_s}V_0.$$

```plot
{"title": "SVPWM hexagon: reference synthesised from adjacent vectors", "xLabel": "α-axis", "yLabel": "β-axis", "xRange": [-1.2, 1.2], "yRange": [-1.2, 1.2], "points": [{"x": 1, "y": 0, "label": "V1", "color": "#2563eb", "size": 6}, {"x": 0.5, "y": 0.866, "label": "V2", "color": "#2563eb", "size": 6}, {"x": -0.5, "y": 0.866, "label": "V3", "color": "#2563eb", "size": 6}, {"x": -1, "y": 0, "label": "V4", "color": "#2563eb", "size": 6}, {"x": -0.5, "y": -0.866, "label": "V5", "color": "#2563eb", "size": 6}, {"x": 0.5, "y": -0.866, "label": "V6", "color": "#2563eb", "size": 6}, {"x": 0, "y": 0, "label": "V0/V7 (zero)", "color": "#94a3b8", "size": 5}, {"x": 0.55, "y": 0.35, "label": "V* reference", "color": "#dc2626", "size": 7}]}
```

Why SVPWM wins over sine-triangle PWM:

- **~15% more voltage** — it reaches a higher fundamental output from the same DC
  link (the largest inscribed circle in the hexagon), giving more speed before
  field weakening.
- **Lower harmonic distortion** and reduced switching loss from optimal placement
  of the zero vector.
- It maps naturally onto the $\\alpha\\beta$ voltage that FOC already produces.

The reference must stay inside the inscribed circle to remain in the **linear**
region; pushing into the hexagon corners enters **overmodulation**, trading
distortion for extra voltage.

**Next:** an alternative that skips the current loops entirely — DTC.
""",
        ),
        _t(
            "Direct torque control (DTC)",
            "12 min",
            """\
# Direct torque control (DTC)

**Direct torque control** takes a different route from FOC: instead of regulating
currents through PI loops and PWM, it controls **torque** and **stator flux**
*directly*, by choosing inverter switching states from a lookup table.

The idea:

1. **Estimate** stator flux magnitude $|\\lambda_s|$ and electromagnetic torque
   $\\tau$ from measured voltages and currents.
2. Compare each to its reference using **hysteresis comparators** (a band, not a
   PI).
3. Knowing the flux sector and the two error signs, a **switching table** picks
   the voltage vector that simultaneously nudges flux and torque back inside their
   bands.

$$\\tau \\propto |\\lambda_s|\\,|\\lambda_r|\\,\\sin\\delta,$$

so accelerating the stator flux vector ahead of the rotor flux increases the load
angle $\\delta$ and thus torque almost instantly.

DTC vs FOC:

| | FOC | DTC |
|---|-----|-----|
| Inner control | current PI + PWM | hysteresis + switching table |
| Coordinate transforms | yes (Park) | no (stays in αβ) |
| Torque response | very fast | fastest |
| Switching frequency | fixed | variable |
| Torque ripple | low | higher |

DTC gives the **fastest possible torque response** and needs no rotor-position
sensor for the basic scheme, but its variable switching frequency and higher
torque/flux ripple are the price. It is widely used in high-power traction and
industrial drives where raw torque dynamics matter most.

**Next:** running a drive with no shaft sensor at all.
""",
        ),
        _t(
            "Sensorless control & observers",
            "12 min",
            """\
# Sensorless control & observers

Encoders and resolvers add cost, wiring, failure points and length to the motor.
**Sensorless control** removes them by *estimating* rotor position and speed from
the electrical measurements the drive already has — phase currents and the known
applied voltages.

Two complementary techniques span the speed range:

- **Back-EMF / flux observers (medium-high speed).** The motor model
  $\\;\\hat\\lambda = \\int (v - R\\,i)\\,dt\\;$ reconstructs the stator flux, whose
  angle gives rotor position. A **state observer** (Luenberger or sliding-mode)
  or an **extended Kalman filter** runs the model in parallel with the real motor
  and corrects the estimate using the current error. Robust once there is enough
  back-EMF.
- **Signal injection (zero / low speed).** At standstill the back-EMF vanishes, so
  observers fail. Instead a small high-frequency voltage is **injected** and the
  rotor's magnetic **saliency** (different inductance along $d$ and $q$) modulates
  the response, revealing position even at zero speed.

An observer is itself a feedback loop: predict the state from the model, compare
predicted current to measured current, and feed the error back to drive the
estimate toward truth — the same principle as the bootstrap-free estimators used
across control theory.

Sensorless drives cut cost and improve reliability (no sensor to fail) and are now
standard in appliances, HVAC and many EV auxiliaries; the trade-off is degraded
performance and start-up difficulty at very low speed unless saliency injection is
added.

**Next:** servo drives and the motion profiles they follow.
""",
        ),
        _t(
            "Servo drives & motion profiles",
            "11 min",
            """\
# Servo drives & motion profiles

A **servo drive** is a high-performance drive built for precise **position and
motion** control — robot joints, CNC axes, pick-and-place. It adds an outermost
**position loop** on top of the cascaded speed and current loops, all running at
high bandwidth on a low-inertia PMSM with high-resolution feedback.

```mermaid
flowchart LR
    PREF["θ*"] --> P1(("Σ")) --> PPI[Position P/PI] --> WREF["ω*"]
    WREF --> S1(("Σ")) --> SPI[Speed PI] --> IREF["i_q*"]
    IREF --> C1(("Σ")) --> CPI[Current PI] --> INV[Inverter] --> M[PMSM]
    M -- i --> C1
    M -- ω --> S1
    M -- θ --> P1
```

You do not command a position *step* — that demands infinite acceleration.
Instead the controller follows a planned **motion profile** $\\theta^*(t)$ with
limited velocity and acceleration:

- **Trapezoidal velocity** — accelerate at a constant rate, cruise at max speed,
  decelerate. Simple, but the jump in acceleration jerks the mechanism.
- **S-curve** — ramps the acceleration itself (bounded **jerk**), giving smooth,
  low-vibration motion that protects gearboxes and payloads.

**Feedforward** is the servo's secret weapon: the profile's known velocity and
acceleration are injected *directly* as speed and torque references, so the
feedback loops only correct the small residual error. This slashes **following
error** and lets the axis track fast trajectories accurately — the difference
between a sloppy and a crisp servo.

**Next:** put it all together in a design case study.
""",
        ),
        _t(
            "Drive design case study: sizing & loop tuning",
            "12 min",
            """\
# Drive design case study: sizing & loop tuning

Design a drive for a horizontal **conveyor**: move a $200\\,\\text{kg}$ load,
reach $1\\,\\text{m/s}$ in $0.5\\,\\text{s}$, then run steadily against friction.

## 1. Sizing the motor

- **Steady torque** covers friction and any constant load.
- **Acceleration torque** comes from inertia: $\\tau_{acc} = J_{total}\\,
  \\dfrac{\\Delta\\omega}{\\Delta t}$, where $J_{total}$ reflects the motor plus
  load inertia through the gearbox ratio (load inertia scales as $1/N^2$).
- **Peak torque** = steady + acceleration; the motor's *peak* rating must cover
  it, and its *continuous (RMS over the cycle)* rating must cover the duty cycle
  so it does not overheat.

Pick the **gear ratio** to match load and motor speeds and to reflect a load
inertia comparable to the motor's (inertia matching ≈ best dynamics), then choose
a motor whose continuous torque ≥ RMS demand with peak headroom.

## 2. Sizing the converter

The inverter current rating follows from peak torque ($i \\propto \\tau$); the
DC-link voltage sets the top speed before field weakening; and a **brake
resistor** or regen front-end handles deceleration energy.

## 3. Tuning the loops (inside-out)

```plot
{"title": "Tuning the speed loop: gain trades speed vs overshoot", "xLabel": "time (s)", "yLabel": "speed (per-unit)", "xRange": [0, 1.0], "yRange": [0, 1.4], "functions": [{"expr": "1 - exp(-5*x)*(cos(9*x) + 0.56*sin(9*x))", "label": "too much gain (overshoot)", "color": "#dc2626"}, {"expr": "1 - exp(-7*x)*(1 + 7*x)", "label": "well damped", "color": "#2563eb"}, {"expr": "1 - exp(-2.5*x)", "label": "too low (sluggish)", "color": "#94a3b8"}]}
```

1. **Current loop first** — set its bandwidth from the switching frequency
   (typically $f_{sw}/10$ or so); the electrical time constant $L/R$ sets the PI
   gains.
2. **Speed loop next**, several times slower than the current loop, tuned for a
   well-damped response (the blue curve): fast rise, minimal overshoot.
3. **Position loop last** (if a servo), slower still, with velocity/acceleration
   **feedforward** from the motion profile.

Verify against the **thermal duty cycle** (RMS torque over the real motion
profile, not just the peak) and the four-quadrant energy flow during braking.
That closes the loop from physics to a working, well-tuned drive.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


ELECTRIC_DRIVES_COURSES: tuple[SeedCourse, ...] = (_ED_BASICS, _ED_INTERMEDIATE, _ED_ADVANCED)

__all__ = ["ELECTRIC_DRIVES_COURSES"]
