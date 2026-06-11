"""Curated Electric Machines & Drives track: Basics, Intermediate, Advanced.

A complete electric-machines curriculum: electromechanical energy conversion and
magnetic circuits, DC machines, transformers, three-phase fundamentals and the
rotating field (Basics); induction and synchronous/PMSM machines, space vectors
and Clarke/Park, BLDC/stepper, and losses/thermal (Intermediate); the inverter
power stage, scalar V/f control, field-oriented control, sensorless observers,
regenerative braking and real applications (Advanced). Dual MATLAB + Python focus
throughout, with runnable Python labs (numpy + matplotlib), interactive ```plot
blocks, Mermaid diagrams, LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Electric Machines & Drives -- Basics --------------------------------------

_MACHINES_BASICS = SeedCourse(
    slug="machines-basics",
    title="Electric Machines & Drives — Basics",
    description=(
        "How electricity becomes motion: electromechanical energy conversion and "
        "magnetic circuits, DC machines, transformers, three-phase power, and the "
        "rotating magnetic field that starts every AC motor - with side-by-side "
        "MATLAB and Python, interactive plots, and a runnable DC-motor lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Electromechanical energy conversion & magnetic circuits",
            "12 min",
            """\
# Electromechanical energy conversion & magnetic circuits

An electric **machine** is an energy-conversion device: it turns electrical
energy into mechanical energy (a **motor**) or the reverse (a **generator**). The
bridge between the two worlds is the **magnetic field**, so every machine is
really a cleverly arranged **magnetic circuit**.

## Flux, MMF and reluctance - the "Ohm's law" of magnetism

A coil of $N$ turns carrying current $I$ drives a **magnetomotive force**
$\\mathcal{F} = N I$ (amp-turns) around an iron core, pushing magnetic **flux**
$\\Phi$ through it against the core's **reluctance** $\\mathcal{R}$:

$$\\Phi = \\frac{\\mathcal{F}}{\\mathcal{R}} = \\frac{N I}{\\mathcal{R}}, \\qquad \\mathcal{R} = \\frac{l}{\\mu A}.$$

The analogy is exact: MMF is like voltage, flux like current, reluctance like
resistance. Iron has high permeability $\\mu$ (low reluctance), so it **guides**
flux the way a wire guides current - which is why motor cores are iron.

| Magnetic | Symbol | Electrical analogue |
|----------|--------|---------------------|
| MMF $\\mathcal{F} = NI$ | amp-turns | voltage |
| flux $\\Phi$ | weber | current |
| reluctance $\\mathcal{R}$ | A-t/Wb | resistance |
| permeability $\\mu$ | H/m | conductivity |

## Faraday & Lenz: a changing flux makes a voltage

A flux that **changes** through a coil induces a voltage (Faraday's law); Lenz's
law fixes the sign so the induced effect **opposes** the change:

$$e = -N\\,\\frac{d\\Phi}{dt}.$$

This single law is behind transformers, generators, and the **back-EMF** of every
motor. Slide the frequency and watch a sinusoidal flux produce a voltage that is
bigger when the flux changes faster (and a quarter-cycle ahead):

```plot
{"title": "Faraday: induced EMF leads flux and grows with frequency (slide f)", "xLabel": "time (s)", "yLabel": "normalized", "xRange": [0, 2], "yRange": [-3.5, 3.5], "grid": true, "controls": [{"name": "f", "range": [0.5, 3], "value": 1, "label": "frequency f (Hz)"}], "functions": [{"expr": "sin(2*pi*f*x)", "label": "flux", "color": "#2563eb"}, {"expr": "f*cos(2*pi*f*x)", "label": "induced EMF ~ d(flux)/dt", "color": "#dc2626"}]}
```

## Force and torque: where the motion comes from

A current $I$ in a wire of length $l$ inside a field $B$ feels a force
$F = B I l$; arranged on a rotor at radius $r$, those forces make **torque**
$T = F r$. Equivalently, machines move toward the state of **minimum reluctance**
(maximum stored magnetic energy alignment) - the principle behind reluctance and
stepper motors.

```matlab
N = 200; I = 2; mu = 1.0e-3; A = 1e-4; len = 0.2;   % core geometry
Rel = len/(mu*A);            % reluctance
flux = N*I/Rel;              % Wb
B = flux/A; F = B*I*len;     % force on a conductor
```

```python
N, I, mu, A, length = 200, 2, 1.0e-3, 1e-4, 0.2
Rel = length/(mu*A)          # reluctance
flux = N*I/Rel               # Wb
B = flux/A; F = B*I*length   # force on a conductor
```

> **Real-world insight:** the same magnetic-circuit math sizes the iron in a phone
> charger's transformer, a hard-drive voice-coil actuator, and a 10 MW wind
> generator. Iron saturates near ~1.5-2 T, which caps how much flux (and torque)
> a given machine can produce.

**Next:** the first practical machine - the DC motor.
""",
        ),
        _t(
            "DC machines: construction, back-EMF & torque-speed",
            "12 min",
            """\
# DC machines: construction, back-EMF & torque-speed

The **DC machine** is the easiest motor to understand and still everywhere:
toys, car windows, cordless tools, and (as a model) the starting point for all
motor control. Current in the **armature** windings, sitting in the field of the
**stator** magnets, feels a force - and a **commutator** keeps that force always
pushing the rotor the same way.

## The two defining equations

A DC machine obeys two linear laws tied by the same machine constant $k$:

$$T = k\\,\\Phi\\,I_a \\quad(\\text{torque}), \\qquad E = k\\,\\Phi\\,\\omega \\quad(\\text{back-EMF}).$$

As the motor spins it generates a **back-EMF** $E$ that opposes the supply
(Lenz again). The armature circuit is just $V = E + I_a R_a$, so the current is
$I_a = (V - E)/R_a = (V - k\\Phi\\omega)/R_a$.

## The torque-speed curve

Combine the two and you get the hallmark DC-motor characteristic - a **straight
line**: highest torque at standstill (**stall**), falling linearly to zero torque
at **no-load speed** $\\omega_0 = V/(k\\Phi)$. Slide the supply voltage and watch
the whole line shift (this is exactly how you control speed):

```plot
{"title": "DC motor torque-speed line shifts with armature voltage (slide V)", "xLabel": "speed (rad/s)", "yLabel": "torque (N.m)", "xRange": [0, 320], "yRange": [0, 3.5], "grid": true, "controls": [{"name": "V", "range": [6, 24], "value": 24, "label": "armature voltage V (V)"}], "functions": [{"expr": "max(0, (V - 0.075*x)*0.075/0.6)", "label": "T = kPhi(V - kPhi*w)/Ra"}]}
```

## Construction and commutation

```mermaid
flowchart LR
  SUP["DC supply"] --> BR["brushes"]
  BR --> COM["commutator (rotating switch)"]
  COM --> ARM["armature windings (rotor)"]
  FLD["field magnets (stator)"] --> ARM
  ARM --> TRQ["torque on shaft"]
```

The **commutator + brushes** mechanically reverse the armature current twice per
revolution so torque never reverses. It is also the DC motor's weakness: brushes
**wear**, **spark**, and limit speed - which is why brushless and AC machines
took over for demanding jobs.

```matlab
V = 24; Ra = 0.6; kPhi = 0.075;   % machine constants
w = 0:1:320;
Ia = (V - kPhi.*w)/Ra;            % armature current
T  = kPhi*Ia;                     % torque-speed line
```

```python
import numpy as np
V, Ra, kPhi = 24, 0.6, 0.075
w = np.arange(0, 320)
Ia = (V - kPhi*w)/Ra              # armature current
T = kPhi*Ia                       # torque-speed line
```

> **Real-world insight:** at the instant you switch on, $\\omega = 0$ so there is
> no back-EMF and the **stall current** $V/R_a$ can be enormous - that inrush is
> why power tools dim the lights and why drives **ramp** the voltage up.

**Next:** moving energy without motion - transformers.
""",
        ),
        _t(
            "Transformers: ideal, real & the equivalent circuit",
            "12 min",
            """\
# Transformers: ideal, real & the equivalent circuit

A **transformer** has no moving parts, yet it is the workhorse that makes the
entire power grid possible: it trades **voltage for current** (and back) at
constant power, using only Faraday's law and a shared iron core.

## The ideal transformer: the turns ratio

Two coils share one magnetic core. The same changing flux links both, so the
voltages scale with the **turns ratio** $a = N_1/N_2$, and - because power in
equals power out - the currents scale inversely:

$$\\frac{V_1}{V_2} = \\frac{N_1}{N_2} = a, \\qquad \\frac{I_1}{I_2} = \\frac{N_2}{N_1} = \\frac{1}{a}.$$

A step-down transformer ($a > 1$) drops voltage and **raises** current. Slide the
turns ratio and watch secondary voltage and current trade off (primary fixed at
230 V, 2 A):

```plot
{"title": "Ideal transformer trades voltage for current (slide turns ratio a)", "xLabel": "(unused axis)", "yLabel": "secondary value", "xRange": [0, 1], "yRange": [0, 500], "grid": true, "controls": [{"name": "a", "range": [0.5, 10], "value": 2, "label": "turns ratio a = N1/N2"}], "functions": [{"expr": "230/a", "label": "V2 = V1/a (V)", "color": "#2563eb"}, {"expr": "2*a", "label": "I2 = I1*a (A)", "color": "#dc2626"}]}
```

## The real transformer and its equivalent circuit

A real transformer is not perfect. The standard **equivalent circuit** adds:

| Non-ideality | Modelled by | Cause |
|--------------|-------------|-------|
| Winding resistance | $R_1, R_2$ | copper $I^2R$ loss |
| Leakage flux | $X_1, X_2$ | flux that misses the other coil |
| Magnetizing current | $X_m$ | finite core permeability |
| Core loss | $R_c$ | hysteresis + eddy currents |

```mermaid
flowchart LR
  V1["V1"] --> R1["R1 + jX1"] --> CORE["shunt: Rc || jXm"]
  CORE --> R2["R2 + jX2 (referred)"] --> V2["V2 / load"]
```

## Losses and efficiency

Two loss families: **copper losses** $I^2R$ (grow with load) and **core losses**
(roughly constant with voltage). Efficiency peaks where they are equal, and good
power transformers hit **98-99%**. The same physics shrinks down to the little
"wall wart" charger and scales up to a 500 MVA grid transformer.

```matlab
N1 = 1000; N2 = 100; V1 = 230;
a = N1/N2;                       % 10
V2 = V1/a;                       % 23 V
I2 = 5; I1 = I2/a;               % current scales inversely
```

```python
N1, N2, V1 = 1000, 100, 230
a = N1/N2                        # 10
V2 = V1/a                        # 23 V
I2 = 5; I1 = I2/a                # current scales inversely
```

> **Real-world insight:** transmitting power at **high voltage / low current**
> slashes line losses ($P_{loss} = I^2 R$), which is the whole reason the grid is
> AC - transformers step up to hundreds of kV for transport and back down for use.

**Next:** the three-wire system the grid actually runs on.
""",
        ),
        _t(
            "Three-phase fundamentals: phasors, line vs phase & power",
            "12 min",
            """\
# Three-phase fundamentals: phasors, line vs phase & power

Almost all generation, transmission, and large motors use **three-phase** AC:
three sinusoidal voltages of equal amplitude, each shifted by **120 degrees**. It
delivers smoother power and uses copper more efficiently than single phase.

$$v_a = V_m\\cos(\\omega t), \\; v_b = V_m\\cos(\\omega t - 120^\\circ), \\; v_c = V_m\\cos(\\omega t + 120^\\circ).$$

The three add to **zero** at every instant - the deep fact that makes three-phase
work (the neutral carries no current in a balanced system). Watch all three:

```plot
{"title": "Balanced three-phase voltages sum to zero (slide frequency)", "xLabel": "time (ms)", "yLabel": "voltage (V)", "xRange": [0, 40], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "f", "range": [25, 60], "value": 50, "label": "frequency f (Hz)"}], "functions": [{"expr": "cos(2*pi*f*x/1000)", "label": "phase a", "color": "#dc2626"}, {"expr": "cos(2*pi*f*x/1000 - 2.0944)", "label": "phase b", "color": "#16a34a"}, {"expr": "cos(2*pi*f*x/1000 + 2.0944)", "label": "phase c", "color": "#2563eb"}]}
```

## Phasors: the rotating snapshot

Each phase is a **phasor** - an arrow of length $V_m$ at a fixed angle, all
spinning together at $\\omega$. The three sit 120 degrees apart on a circle. Press
Play to watch the phase-a phasor rotate around the unit circle:

```plot
{"title": "Phasor rotating at angular frequency omega", "xLabel": "real", "yLabel": "imag", "xRange": [-1.3, 1.3], "yRange": [-1.3, 1.3], "grid": true, "animate": {"param": "t", "range": [0, 6.2832], "label": "phase angle"}, "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 6.2832], "label": "unit circle", "color": "#94a3b8"}], "points": [{"xExpr": "cos(t)", "yExpr": "sin(t)", "label": "phasor tip", "color": "#dc2626", "size": 7, "trail": true}]}
```

## Line vs phase, and three-phase power

Connect the three coils in **wye (Y)** or **delta**. The relationships everyone
must memorise:

| Connection | Voltage | Current |
|------------|---------|---------|
| **Wye (Y)** | $V_{line} = \\sqrt{3}\\,V_{phase}$ | $I_{line} = I_{phase}$ |
| **Delta** | $V_{line} = V_{phase}$ | $I_{line} = \\sqrt{3}\\,I_{phase}$ |

Total three-phase real power, in line quantities, is

$$P = \\sqrt{3}\\,V_{line} I_{line} \\cos\\phi,$$

where $\\cos\\phi$ is the **power factor**. Unlike single phase, **instantaneous**
three-phase power is constant - no 100/120 Hz pulsation - which is why big motors
run so smoothly.

```matlab
Vline = 400; Iline = 10; pf = 0.85;
Vphase = Vline/sqrt(3);             % wye -> 231 V
P = sqrt(3)*Vline*Iline*pf;         % three-phase real power (W)
```

```python
import numpy as np
Vline, Iline, pf = 400, 10, 0.85
Vphase = Vline/np.sqrt(3)           # wye -> 231 V
P = np.sqrt(3)*Vline*Iline*pf       # three-phase real power
```

> **Real-world insight:** "400 V three-phase" in a factory is 230 V per phase to
> neutral (wye) - the same wiring feeds single-phase office sockets and the big
> three-phase motors on the shop floor from one supply.

**Next:** spin those three phases into a moving field.
""",
        ),
        _t(
            "AC machines & the rotating magnetic field",
            "12 min",
            """\
# AC machines & the rotating magnetic field

Here is the idea that makes every AC motor turn, and the reason three-phase is so
elegant: feed three coils placed 120 degrees apart in space with three currents
120 degrees apart in time, and their combined magnetic field becomes a **rotating
magnetic field** of constant magnitude that sweeps around the stator - a
spinning magnet with no moving parts.

## Synchronous speed

The field rotates at the **synchronous speed**, set only by the supply frequency
$f$ and the number of pole pairs $p$:

$$n_s = \\frac{120 f}{P}\\;\\text{(rpm)}, \\qquad \\omega_s = \\frac{2\\pi f}{p}.$$

A 2-pole, 50 Hz motor spins its field at 3000 rpm; a 4-pole at 1500 rpm. Slide
the pole count and watch synchronous speed step down:

```plot
{"title": "Synchronous speed ns = 120 f / P at 50 Hz (slide poles)", "xLabel": "frequency f (Hz)", "yLabel": "synchronous speed (rpm)", "xRange": [0, 60], "yRange": [0, 3800], "grid": true, "controls": [{"name": "P", "range": [2, 8], "value": 4, "label": "number of poles P"}], "functions": [{"expr": "120*x/P", "label": "ns (rpm)"}]}
```

## Watching the field rotate

The resultant field is the vector sum of three pulsating coil fields. Press Play:
the tip of the resultant field vector traces a circle at synchronous speed, even
though each coil only pushes back and forth along its own axis.

```plot
{"title": "Three pulsating fields sum to one rotating field vector", "xLabel": "field x", "yLabel": "field y", "xRange": [-1.6, 1.6], "yRange": [-1.6, 1.6], "grid": true, "animate": {"param": "t", "range": [0, 6.2832], "label": "rotation angle"}, "parametric": [{"x": "1.5*cos(t)", "y": "1.5*sin(t)", "range": [0, 6.2832], "label": "tip locus", "color": "#94a3b8"}], "points": [{"xExpr": "1.5*cos(t)", "yExpr": "1.5*sin(t)", "label": "resultant field", "color": "#dc2626", "size": 7, "trail": true}]}
```

## The two great AC families

- **Induction (asynchronous) motor** - the rotating field *induces* current in the
  rotor (no electrical connection to it). The rotor chases the field but never
  quite catches it; the lag is **slip**. Rugged, cheap, everywhere.
- **Synchronous motor** - the rotor is itself a magnet (permanent or DC-excited)
  and **locks** to the rotating field, turning at exactly $n_s$. Used in
  generators (every power plant), precise drives, and as PMSMs in EVs.

```mermaid
flowchart LR
  SUP["3-phase supply"] --> ST["stator coils (120 deg apart)"]
  ST --> RF["rotating magnetic field at ns"]
  RF --> ROT["rotor follows the field"]
  ROT --> SHAFT["shaft torque"]
```

```matlab
f = 50; P = 4;
ns = 120*f/P;                    % 1500 rpm synchronous speed
ws = 2*pi*f/(P/2);               % rad/s
```

```python
import numpy as np
f, P = 50, 4
ns = 120*f/P                     # 1500 rpm
ws = 2*np.pi*f/(P/2)             # rad/s
```

> **Real-world insight:** Nikola Tesla's rotating-field induction motor (1888)
> beat brushed DC for industry precisely because it has **no brushes or
> commutator** to wear - the rotor needs no electrical contact at all.

**Next:** put the DC-motor equations to work in code.
""",
        ),
        _code(
            "Lab: DC motor torque-speed curve",
            "12 min",
            """\
# Plot a permanent-magnet DC motor's torque-speed and power-speed curves
# from its two defining equations, and find the peak-power operating point.
import numpy as np
import matplotlib.pyplot as plt

# Motor nameplate-style constants
V = 24.0        # armature supply voltage (V)
Ra = 0.6        # armature resistance (ohm)
kPhi = 0.075    # torque/back-EMF constant (N.m/A == V.s/rad)

# No-load speed: torque = 0 when back-EMF equals supply -> w0 = V/kPhi
w0 = V/kPhi
w = np.linspace(0, w0, 400)         # speed sweep (rad/s)

Ia = (V - kPhi*w)/Ra                # armature current
T = kPhi*Ia                         # torque (N.m): a straight line
Pmech = T*w                         # mechanical output power (W)

T_stall = kPhi*V/Ra                 # torque at zero speed
k_peak = np.argmax(Pmech)           # index of peak mechanical power
w_peak = w[k_peak]

fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.plot(w, T, color="#dc2626", lw=2, label="torque")
ax1.set_xlabel("speed (rad/s)")
ax1.set_ylabel("torque (N.m)", color="#dc2626")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(w, Pmech, color="#2563eb", lw=2, label="mech power")
ax2.set_ylabel("power (W)", color="#2563eb")
ax2.axvline(w_peak, ls="--", color="#16a34a")

plt.title(f"DC motor: stall T = {T_stall:.1f} N.m, peak power at {w_peak:.0f} rad/s")
fig.tight_layout()
plt.show()

print(f"no-load speed   w0 = {w0:.1f} rad/s ({w0*60/(2*np.pi):.0f} rpm)")
print(f"stall torque       = {T_stall:.2f} N.m")
print(f"peak mech power     = {Pmech[k_peak]:.1f} W at {w_peak:.0f} rad/s")
print("note: peak power occurs at half the no-load speed (mid torque-speed line)")

# Try it yourself:
#   1. Halve V to 12: the whole torque-speed line shifts left (speed control).
#   2. The MATLAB equivalent: w0 = V/kPhi; T = kPhi*(V - kPhi*w)/Ra;
""",
        ),
    ),
)


# -- Electric Machines & Drives -- Intermediate: AC Machines -------------------

_MACHINES_INTERMEDIATE = SeedCourse(
    slug="machines-intermediate",
    title="Electric Machines & Drives — Intermediate: AC Machines",
    description=(
        "The AC machines that run industry: induction motors (slip, torque-speed, "
        "equivalent circuit, starting), synchronous machines and PMSMs, the "
        "rotating field via Clarke/Park space vectors, BLDC and stepper motors, "
        "and losses/efficiency/thermal limits - dual MATLAB/Python, interactive "
        "plots, and a runnable induction-motor lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Induction motors: slip, torque-speed & starting",
            "13 min",
            """\
# Induction motors: slip, torque-speed & starting

The **three-phase induction motor** is the most common motor on Earth - pumps,
fans, conveyors, compressors, machine tools. Its rotating stator field induces
current in a rotor that has **no electrical connection** (the rugged
"squirrel-cage"), and that induced current produces torque.

## Slip: the rotor always lags

For the field to induce rotor current, the rotor must turn **slower** than the
synchronous speed $n_s$. The fractional lag is the **slip**:

$$s = \\frac{n_s - n}{n_s}.$$

At standstill $s = 1$; near no-load $s \\approx 0$ (a few percent). The rotor
frequency is $s f$, so a barely-loaded motor induces almost nothing - exactly
enough current to make exactly the torque the load demands.

## The torque-speed curve

The famous induction torque-speed curve rises from the **locked-rotor** (starting)
torque, climbs to a **breakdown (pullout) torque**, then drops steeply to zero at
synchronous speed. The motor runs on that steep right-hand part. Slide the rotor
resistance and watch the peak slide toward standstill (the basis of wound-rotor
starting):

```plot
{"title": "Induction torque-speed (Kloss): rotor resistance shifts the peak (slide R2)", "xLabel": "slip s (1 = standstill, 0 = sync)", "yLabel": "torque (p.u.)", "xRange": [0.01, 1], "yRange": [0, 2.4], "grid": true, "controls": [{"name": "R2", "range": [0.1, 1], "value": 0.2, "label": "rotor resistance R2 (relative)"}], "functions": [{"expr": "2/((x/R2) + (R2/x))", "label": "T(s), peak at s = R2"}]}
```

The peak torque magnitude is fixed but its **location** is $s \\approx R_2/X_2$ -
more rotor resistance moves the breakdown point toward starting (high starting
torque) at the cost of efficiency when running.

## The per-phase equivalent circuit

```mermaid
flowchart LR
  V1["V1 (phase)"] --> R1["R1 + jX1 (stator)"]
  R1 --> MAG["jXm (magnetizing)"]
  R1 --> R2["R2/s + jX2 (rotor, referred)"]
  R2 --> MECH["R2(1-s)/s = mechanical power"]
```

The slip appears as the term $R_2/s$: at standstill it is small (huge current,
low power factor); near sync it is large (the rotor looks like a high resistance).

## Starting: taming the inrush

At $s = 1$ a motor drawing direct line voltage pulls **5-7x** its rated current.
Methods to limit it: **star-delta** starting, **autotransformer** start, **soft
starters** (phase-controlled SCRs), and best of all a **variable-frequency
drive** (the Advanced course) that starts at low frequency and low current.

```matlab
ns = 1500; n = 1455;
s = (ns - n)/ns;                 % 0.03 -> 3% slip
fr = s*50;                       % rotor electrical frequency = 1.5 Hz
```

```python
ns, n = 1500, 1455
s = (ns - n)/ns                  # 0.03 -> 3% slip
fr = s*50                        # rotor electrical frequency = 1.5 Hz
```

> **Real-world insight:** a fully loaded industrial induction motor runs at only
> ~2-4% slip, so its speed is nearly constant - which is why for decades "motor =
> fixed speed" and you threw away energy throttling the pump with a valve instead.

**Next:** the motor that locks to the field - synchronous & PMSM.
""",
        ),
        _t(
            "Synchronous machines & PMSM: excitation, generators & V-curves",
            "12 min",
            """\
# Synchronous machines & PMSM: excitation, generators & V-curves

A **synchronous machine** has a rotor that is itself a magnet - either an
electromagnet fed DC through slip rings (**wound-field**) or permanent magnets
(**PMSM**). It **locks** to the rotating stator field and turns at exactly the
synchronous speed, no slip.

## Generators: the backbone of the grid

Nearly all the world's electricity comes from synchronous **generators**: a
turbine (steam, gas, hydro, wind) spins the magnet rotor, and Faraday's law makes
three-phase voltage in the stator. Their **frequency is locked to shaft speed**,
which is why the grid is held at a tight 50/60 Hz.

## The torque/power angle

A synchronous machine develops torque in proportion to the **sine of the load
angle** $\\delta$ between the rotor and the stator field:

$$P = \\frac{V E}{X_s}\\sin\\delta.$$

It pulls hardest at $\\delta = 90^\\circ$; push past that and it loses
synchronism (**pole slip**). Slide the internal EMF and watch the power-angle
curve grow:

```plot
{"title": "Synchronous power-angle curve P = (V*E/Xs) sin(delta) (slide E)", "xLabel": "load angle delta (rad)", "yLabel": "power (p.u.)", "xRange": [0, 3.1416], "yRange": [0, 2.2], "grid": true, "controls": [{"name": "E", "range": [0.8, 2], "value": 1.2, "label": "internal EMF E (p.u.)"}], "functions": [{"expr": "E*sin(x)", "label": "P(delta), peak at 90 deg"}]}
```

## Excitation and the V-curves

A synchronous machine has a unique trick: by adjusting **field excitation** you
control its **power factor** independently of its mechanical load. Under-excited
it draws lagging (inductive) current; over-excited it supplies leading
(capacitive) current. Plotting stator current vs field current at fixed power
gives the famous **V-curves** - a family of V shapes, each bottoming out at unity
power factor. Slide the load:

```plot
{"title": "Synchronous V-curves: stator current vs field current (slide load)", "xLabel": "field (excitation) current (p.u.)", "yLabel": "stator current (p.u.)", "xRange": [0.2, 2], "yRange": [0, 2], "grid": true, "controls": [{"name": "Pload", "range": [0.3, 1], "value": 0.6, "label": "mechanical load (p.u.)"}], "functions": [{"expr": "sqrt(Pload*Pload + (x - 1)*(x - 1))", "label": "stator current (V-curve)"}]}
```

Over-excited synchronous machines spinning with no load are used as **synchronous
condensers** to pump reactive power into the grid for voltage support.

```mermaid
flowchart LR
  TURB["turbine / prime mover"] --> ROT["magnet rotor"]
  DC["DC field excitation"] --> ROT
  ROT --> STAT["stator: 3-phase EMF"]
  STAT --> GRID["grid (locked frequency)"]
```

```matlab
V = 1.0; E = 1.2; Xs = 0.8; delta = deg2rad(30);
P = (V*E/Xs)*sin(delta);          % power-angle relation (p.u.)
```

```python
import numpy as np
V, E, Xs, delta = 1.0, 1.2, 0.8, np.deg2rad(30)
P = (V*E/Xs)*np.sin(delta)        # power-angle relation (p.u.)
```

> **Real-world insight:** the PMSM - a synchronous machine with magnet rotor - is
> the motor in most **electric vehicles** (Tesla rear drive, Nissan Leaf) and
> high-end robots, because magnets give the best torque density and efficiency.

**Next:** the math that lets us control these fields - space vectors.
""",
        ),
        _t(
            "The rotating field & space vectors: Clarke & Park transforms",
            "13 min",
            """\
# The rotating field & space vectors: Clarke & Park transforms

Three time-varying phase currents are awkward to control. The breakthrough behind
modern drives is to repackage them as **one space vector**, then view it from a
frame that **rotates with the rotor** so the AC quantities become **DC** - much
easier to regulate. Two transforms do this.

## Clarke transform: 3 phases -> 2 axes (alpha-beta)

The Clarke transform collapses the three 120-degree phase quantities into an
equivalent two-axis (alpha, beta) **stationary** frame:

$$i_\\alpha = i_a, \\qquad i_\\beta = \\frac{1}{\\sqrt{3}}(i_b - i_c).$$

The space vector $i_\\alpha + j i_\\beta$ traces a **circle** for a balanced set -
it *is* the rotating field. Press Play to watch the tip rotate:

```plot
{"title": "Clarke: balanced currents form a rotating space vector (circle)", "xLabel": "i-alpha", "yLabel": "i-beta", "xRange": [-1.3, 1.3], "yRange": [-1.3, 1.3], "grid": true, "animate": {"param": "t", "range": [0, 6.2832], "label": "electrical angle"}, "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 6.2832], "label": "vector locus", "color": "#94a3b8"}], "points": [{"xExpr": "cos(t)", "yExpr": "sin(t)", "label": "space vector", "color": "#dc2626", "size": 7, "trail": true}]}
```

## Park transform: spin the frame (alpha-beta -> d-q)

Now rotate the axes at the rotor angle $\\theta$ so they spin **with** the field.
In this **d-q** frame the space vector stops moving - the AC becomes DC:

$$\\begin{aligned} i_d &= i_\\alpha\\cos\\theta + i_\\beta\\sin\\theta, \\\\ i_q &= -i_\\alpha\\sin\\theta + i_\\beta\\cos\\theta. \\end{aligned}$$

The two new currents have beautiful physical meaning:

- **$i_d$** (direct axis) - aligned with the rotor flux: the **magnetizing** /
  flux-producing current.
- **$i_q$** (quadrature axis) - 90 degrees ahead: the **torque-producing**
  current.

Slide the rotor angle and watch a fixed stationary vector resolve into different
$i_d$ / $i_q$ components:

```plot
{"title": "Park: same vector seen from a frame rotating by theta (slide theta)", "xLabel": "angle (rad)", "yLabel": "current component", "xRange": [0, 6.2832], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "th", "range": [0, 6.2832], "value": 0, "label": "rotor angle theta (rad)"}], "functions": [{"expr": "cos(x)*cos(th) + sin(x)*sin(th)", "label": "id(theta)", "color": "#2563eb"}, {"expr": "-cos(x)*sin(th) + sin(x)*cos(th)", "label": "iq(theta)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  ABC["ia ib ic (3-phase AC)"] --> CLK["Clarke"] --> AB["i-alpha i-beta (2-phase AC)"]
  AB --> PARK["Park (rotate by theta)"] --> DQ["id iq (DC in steady state)"]
```

```matlab
ia=1.0; ib=-0.5; ic=-0.5; theta=deg2rad(30);
ialpha = ia;
ibeta  = (ib - ic)/sqrt(3);
id =  ialpha*cos(theta) + ibeta*sin(theta);
iq = -ialpha*sin(theta) + ibeta*cos(theta);
```

```python
import numpy as np
ia, ib, ic, theta = 1.0, -0.5, -0.5, np.deg2rad(30)
ialpha = ia
ibeta = (ib - ic)/np.sqrt(3)
id =  ialpha*np.cos(theta) + ibeta*np.sin(theta)
iq = -ialpha*np.sin(theta) + ibeta*np.cos(theta)
```

> **Real-world insight:** Clarke + Park is the single most important idea in motor
> control - it lets an EV inverter regulate flux and torque as cleanly as a DC
> motor's two knobs. You will build a controller on it in the Advanced course.

**Next:** electronically commutated machines - BLDC & stepper.
""",
        ),
        _t(
            "BLDC & stepper motors: commutation & drive schemes",
            "12 min",
            """\
# BLDC & stepper motors: commutation & drive schemes

Two specialised machines dominate small precise drives: the **brushless DC
(BLDC)** motor and the **stepper**. Both are really synchronous magnet motors,
but they are driven and commutated electronically rather than with brushes.

## BLDC: a DC motor turned inside out

A BLDC has magnets on the rotor and windings on the stator, so the **inverter**
does the commutation that brushes used to do - no wearing contacts. It is
**trapezoidal**: the inverter energizes two of three phases at a time in a
**six-step** sequence, switching every 60 electrical degrees based on rotor
position (Hall sensors or back-EMF zero-crossings).

```mermaid
stateDiagram-v2
  [*] --> S1
  S1 --> S2: 60 deg
  S2 --> S3: 60 deg
  S3 --> S4: 60 deg
  S4 --> S5: 60 deg
  S5 --> S6: 60 deg
  S6 --> S1: 60 deg
```

Because two phases conduct, the back-EMF is trapezoidal and torque per step is
nearly flat. Its smoother cousin, the **PMSM**, uses sinusoidal currents and FOC
(Advanced course) for ripple-free torque - the same hardware, fancier control.

```plot
{"title": "BLDC: trapezoidal back-EMF vs PMSM sinusoidal (slide phase advance)", "xLabel": "electrical angle (deg)", "yLabel": "back-EMF (p.u.)", "xRange": [0, 360], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "adv", "range": [0, 60], "value": 0, "label": "phase advance (deg)"}], "functions": [{"expr": "clamp((x + adv - 30)/30, -1, 1) * (((x+adv)%360 < 180)*2 - 1) * 0 + clamp(sin(rad(x+adv))*3, -1, 1)", "label": "trapezoidal", "color": "#dc2626"}, {"expr": "sin(rad(x + adv))", "label": "sinusoidal (PMSM)", "color": "#2563eb"}]}
```

## Stepper: motion in discrete steps

A **stepper** moves a fixed angle per electrical step (commonly 1.8 deg = 200
steps/rev) and holds position with no feedback - **open-loop positioning**. Drive
schemes trade smoothness for simplicity:

| Scheme | Energized | Feel |
|--------|-----------|------|
| **Full step (wave)** | one phase | coarse |
| **Full step (two-phase)** | two phases | more torque |
| **Half step** | alternate 1/2 phases | 2x resolution |
| **Microstepping** | sinusoidal PWM | very smooth, fine resolution |

**Microstepping** drives the two phases with sine and cosine currents, so the
rotor settles between full-step positions - it is literally a slow, open-loop
version of the space-vector idea. The current vector walks around a circle:

```plot
{"title": "Microstepping: phase currents are sine/cosine (slide step angle)", "xLabel": "phase A current", "yLabel": "phase B current", "xRange": [-1.3, 1.3], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "ang", "range": [0, 6.2832], "value": 1.5708, "label": "commanded angle (rad)"}], "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 6.2832], "label": "current locus", "color": "#94a3b8"}], "points": [{"x": 0, "y": 0, "label": "origin", "color": "#94a3b8", "size": 4}]}
```

```matlab
steps_per_rev = 200; microsteps = 16;
deg_per_micro = 360/(steps_per_rev*microsteps);   % 0.1125 deg
```

```python
steps_per_rev, microsteps = 200, 16
deg_per_micro = 360/(steps_per_rev*microsteps)    # 0.1125 deg
```

> **Real-world insight:** steppers run your **3D printer and CNC** axes (cheap
> open-loop precision); BLDC motors spin **drones, fans, hard drives, e-bikes,
> and power tools** where efficiency and life matter more than holding torque.

**Next:** where the energy is lost - losses, efficiency & heat.
""",
        ),
        _t(
            "Machine losses, efficiency & thermal limits",
            "11 min",
            """\
# Machine losses, efficiency & thermal limits

No machine is perfect: some input power becomes heat instead of motion.
Understanding **where** the losses go tells you how to size, cool, and rate a
motor - and ultimately, **heat**, not magnetics, sets a machine's continuous
power.

## The loss budget

| Loss | Scales with | Cause |
|------|-------------|-------|
| **Copper (I^2R)** | current^2 (load^2) | winding resistance |
| **Iron / core** | frequency, flux^2 | hysteresis + eddy currents |
| **Mechanical** | speed | friction + windage |
| **Stray load** | load | leakage, harmonics |

Copper losses dominate at heavy load; iron and mechanical losses are roughly
fixed once the machine spins. Efficiency is

$$\\eta = \\frac{P_{out}}{P_{out} + P_{loss}}.$$

Because copper loss grows as load squared while fixed losses stay put, efficiency
**rises**, peaks, then falls - a motor run far below its rating is inefficient.
Slide the fixed-loss level:

```plot
{"title": "Motor efficiency vs load: peaks where fixed = copper loss (slide fixed loss)", "xLabel": "load fraction", "yLabel": "efficiency", "xRange": [0.05, 1.2], "yRange": [0, 1], "grid": true, "controls": [{"name": "Pf", "range": [0.02, 0.15], "value": 0.05, "label": "fixed loss (p.u.)"}], "functions": [{"expr": "x/(x + Pf + 0.08*x*x)", "label": "efficiency", "color": "#16a34a"}]}
```

## Thermal limits set the real rating

Every loss becomes heat in the windings. The insulation class (A, B, F, H) sets
the maximum winding temperature; exceed it and insulation life **halves for every
~10 C** over rating. The machine warms toward a steady temperature with a thermal
**time constant** of minutes - so a motor can briefly **overload** (high peak
torque) but only for short bursts before it cooks:

```plot
{"title": "Winding temperature rise under overload (slide overload)", "xLabel": "time (minutes)", "yLabel": "temperature rise (C)", "xRange": [0, 60], "yRange": [0, 180], "grid": true, "controls": [{"name": "OL", "range": [1, 2.5], "value": 1.5, "label": "overload factor"}], "functions": [{"expr": "100*OL*OL*(1 - exp(-x/12))", "label": "temp rise", "color": "#dc2626"}]}
```

The dashed mental line is the insulation limit: a 1x load settles safely; a 2x
overload blows past it within minutes.

```mermaid
flowchart LR
  PIN["electrical input"] --> CU["copper loss"]
  PIN --> FE["iron loss"]
  PIN --> POUT["mechanical output"]
  POUT --> MECH["friction + windage"]
  CU --> HEAT["heat -> winding temperature"]
  FE --> HEAT
```

```matlab
Pout = 7500; Pcu = 350; Pfe = 200; Pmech = 90;   % watts
eta = Pout/(Pout + Pcu + Pfe + Pmech);            % ~0.92
```

```python
Pout, Pcu, Pfe, Pmech = 7500, 350, 200, 90
eta = Pout/(Pout + Pcu + Pfe + Pmech)             # ~0.92
```

> **Real-world insight:** an EV motor can deliver huge **peak** torque for a few
> seconds (launch) but its **continuous** rating is far lower - limited entirely
> by how fast the cooling can pull heat out of the copper.

**Next:** simulate the induction torque-speed curve yourself.
""",
        ),
        _code(
            "Lab: induction motor torque-speed & slip",
            "13 min",
            """\
# Compute a three-phase induction motor's torque vs slip from its per-phase
# equivalent circuit, then mark the breakdown (pullout) torque and operating point.
import numpy as np
import matplotlib.pyplot as plt

# Per-phase equivalent-circuit parameters (referred to stator)
V1 = 230.0      # phase voltage (V)
R1 = 0.5        # stator resistance (ohm)
X1 = 1.2        # stator leakage reactance (ohm)
R2 = 0.4        # rotor resistance referred (ohm)
X2 = 1.2        # rotor leakage reactance referred (ohm)
f = 50.0        # supply frequency (Hz)
poles = 4

ns = 120*f/poles                 # synchronous speed (rpm)
ws = 2*np.pi*ns/60               # synchronous mech speed (rad/s)

s = np.linspace(0.001, 1.0, 500) # slip from near-sync to standstill

# Approximate torque (Thevenin-free form): per-phase, 3 phases
# T = (3/ws) * V1^2 * (R2/s) / ((R1 + R2/s)^2 + (X1 + X2)^2)
denom = (R1 + R2/s)**2 + (X1 + X2)**2
T = (3.0/ws) * V1**2 * (R2/s) / denom

k_break = np.argmax(T)           # breakdown torque index
s_break = s[k_break]
T_start = T[-1]                  # torque at s = 1 (standstill)

# Pick an operating slip (light load) and read off torque + speed
s_op = 0.03
denom_op = (R1 + R2/s_op)**2 + (X1 + X2)**2
T_op = (3.0/ws) * V1**2 * (R2/s_op) / denom_op
n_op = ns*(1 - s_op)

plt.figure(figsize=(8, 4.5))
plt.plot(s, T, color="#2563eb", lw=2, label="torque")
plt.scatter([s_break], [T[k_break]], color="#dc2626", zorder=5,
            label=f"breakdown @ s={s_break:.2f}")
plt.scatter([s_op], [T_op], color="#16a34a", zorder=5,
            label=f"operating @ s={s_op}")
plt.gca().invert_xaxis()         # standstill (s=1) on the left like a real curve
plt.xlabel("slip s  (1 = standstill, 0 = synchronous)")
plt.ylabel("torque (N.m)")
plt.title(f"Induction motor torque-speed (ns = {ns:.0f} rpm)")
plt.legend(); plt.grid(True); plt.show()

print(f"synchronous speed = {ns:.0f} rpm")
print(f"starting torque   = {T_start:.1f} N.m  (at standstill)")
print(f"breakdown torque  = {T[k_break]:.1f} N.m  at slip {s_break:.2f}")
print(f"operating point   = {T_op:.1f} N.m at {n_op:.0f} rpm (slip {s_op})")

# Try it yourself:
#   1. Raise R2 to 0.8: breakdown moves toward standstill (more starting torque).
#   2. Halve V1: torque scales with voltage squared -> ~1/4 the torque.
""",
        ),
    ),
)


# -- Electric Machines & Drives -- Advanced: Motor Drives & Control ------------

_MACHINES_ADVANCED = SeedCourse(
    slug="machines-advanced",
    title="Electric Machines & Drives — Advanced: Motor Drives & Control",
    description=(
        "Driving and controlling AC machines: the inverter power stage and PWM, "
        "scalar V/f control, field-oriented control (FOC) in depth, sensorless "
        "observers, regenerative braking and four-quadrant operation, plus a "
        "runnable d-q current-control lab and a real-applications throughline - "
        "dual MATLAB/Python with interactive plots and diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The motor-drive power stage: inverter, machine & PWM",
            "13 min",
            """\
# The motor-drive power stage: inverter, machine & PWM

A modern **drive** sits between a fixed DC bus (from the grid via a rectifier, or
a battery) and the motor, and synthesizes whatever voltages and frequency the
motor needs. The heart is the **three-phase voltage-source inverter**: six
transistors (IGBTs or SiC/GaN MOSFETs) in three half-bridge **legs**.

```mermaid
flowchart LR
  DC["DC bus (battery / rectifier)"] --> INV["3-phase inverter (6 switches)"]
  CTRL["controller (PWM)"] --> INV
  INV --> M["AC machine"]
  M --> ENC["position / current feedback"] --> CTRL
```

## Synthesizing AC from DC: PWM

Each leg can connect its phase to the **+** or **-** rail. By switching fast
(typically 4-20 kHz) and varying the **duty cycle**, the average phase voltage
follows any reference. Compare a sine reference to a triangle carrier and you get
**sinusoidal PWM** - the switch is on while reference > carrier:

```plot
{"title": "Sinusoidal PWM: reference vs triangle carrier (slide modulation depth)", "xLabel": "time (ms)", "yLabel": "normalized", "xRange": [0, 20], "yRange": [-1.2, 1.2], "grid": true, "controls": [{"name": "m", "range": [0.2, 1], "value": 0.8, "label": "modulation index m"}], "functions": [{"expr": "m*sin(2*pi*x/20)", "label": "sine reference", "color": "#dc2626"}, {"expr": "2*abs(2*(x*0.6 - floor(x*0.6 + 0.5))) - 1", "label": "triangle carrier", "color": "#94a3b8"}]}
```

## Modulation recap and the DC-bus limit

The **modulation index** $m$ sets how much of the DC bus the inverter uses. With
plain sine PWM the peak line voltage maxes at $m = 1$; **space-vector PWM (SVPWM)**
and third-harmonic injection squeeze out ~15% more, reaching a line voltage of

$$V_{line,max} = \\frac{V_{dc}}{\\sqrt{2}}.$$

Higher switching frequency means smoother current but more **switching losses** -
the central trade-off in drive design, and why SiC/GaN devices (faster, lower
loss) are taking over EVs.

```matlab
Vdc = 600; m = 0.9; fsw = 10e3;
Vphase_pk = m*Vdc/2;             % peak phase voltage (sine PWM)
Tsw = 1/fsw;                     % switching period (100 us)
```

```python
Vdc, m, fsw = 600, 0.9, 10e3
Vphase_pk = m*Vdc/2              # peak phase voltage (sine PWM)
Tsw = 1/fsw                      # switching period (100 us)
```

> **Real-world insight:** the same six-switch inverter runs in your EV traction
> drive, a factory VFD, a heat-pump compressor, and a solar string inverter -
> only the control software and switch ratings change.

**Next:** the simplest useful control law - scalar V/f.
""",
        ),
        _t(
            "Scalar V/f control",
            "11 min",
            """\
# Scalar V/f control

The simplest way to run an induction motor at variable speed is **scalar
volts-per-hertz (V/f) control**: change the supply **frequency** to set the speed,
and change the **voltage** in proportion to keep the magnetic flux constant.

## Why voltage must track frequency

Stator flux is roughly $\\Phi \\propto V/f$ (from Faraday). If you lower frequency
to slow the motor but keep voltage up, flux soars and the iron **saturates**,
drawing huge magnetizing current. So you hold $V/f$ constant - a straight line
through the origin - up to **base speed**, then keep voltage at its maximum and
raise only frequency (the **field-weakening / constant-power** region):

```plot
{"title": "V/f profile: constant V/f to base speed, then field weakening (slide boost)", "xLabel": "frequency (Hz)", "yLabel": "voltage (V)", "xRange": [0, 80], "yRange": [0, 420], "grid": true, "controls": [{"name": "boost", "range": [0, 40], "value": 15, "label": "low-speed voltage boost (V)"}], "functions": [{"expr": "min(400, boost + (400 - boost)*x/50)", "label": "stator voltage", "color": "#2563eb"}]}
```

## Low-speed boost

At very low frequency the stator resistance drop becomes significant and flux
collapses, so practical V/f adds a small **voltage boost** (the intercept above) to
keep low-speed torque.

```mermaid
flowchart LR
  REF["speed reference"] --> FREQ["set frequency f"]
  FREQ --> VF["V = (V/f) * f + boost"]
  VF --> PWM["PWM"] --> INV["inverter"] --> M["induction motor"]
```

## Where V/f wins and where it loses

| Aspect | V/f (scalar) | FOC (vector) |
|--------|--------------|--------------|
| Position sensor | not needed | needed (or estimated) |
| Dynamic response | slow | fast, precise |
| Torque at zero speed | poor | excellent |
| Compute cost | tiny | needs a DSP/MCU |
| Typical use | fans, pumps, HVAC | EV, robotics, servos |

V/f is **open-loop** on torque - perfect for **pumps and fans**, where slowing the
motor 20% cuts power ~50% (the cube law of fan/pump loads), saving enormous energy
versus throttling a valve. For dynamic, precise torque you need vector control.

```matlab
f = 30; Vrated = 400; frated = 50; boost = 15;
V = boost + (Vrated - boost)*f/frated;    % V/f with boost
V = min(V, Vrated);                       % clamp above base speed
```

```python
f, Vrated, frated, boost = 30, 400, 50, 15
V = boost + (Vrated - boost)*f/frated     # V/f with boost
V = min(V, Vrated)                        # clamp above base speed
```

> **Real-world insight:** retrofitting fixed-speed HVAC fans and pumps with V/f
> variable-frequency drives is one of the highest-return energy-efficiency moves
> in any building - often paying for itself in under two years.

**Next:** controlling torque directly - field-oriented control.
""",
        ),
        _t(
            "Field-oriented control (FOC) in depth",
            "14 min",
            """\
# Field-oriented control (FOC) in depth

**Field-oriented control** (vector control) makes an AC machine behave like the
ideal DC motor: two independent knobs - one for **flux**, one for **torque** -
regulated as smooth DC quantities. It is the control method inside virtually every
EV, robot joint, and high-performance servo.

## The core idea

Recall from the Intermediate course: transform the three phase currents into the
rotor-aligned **d-q** frame, where

- **$i_d$** controls **flux** (set to zero for a PMSM below base speed - magnets
  already supply the flux),
- **$i_q$** controls **torque**: $T \\approx k\\,i_q$.

So you regulate $i_d$ and $i_q$ to references with simple PI loops, then transform
back to three-phase voltages for the PWM. Torque is now a clean, linear command.

## The full FOC loop

```mermaid
flowchart LR
  REF["iq* (torque), id* (flux)"] --> PI["d-q PI current loops"]
  FB["measured ia,ib,ic"] --> CP["Clarke + Park (theta)"] --> PI
  PI --> IPARK["inverse Park + inverse Clarke"]
  IPARK --> SVPWM["SVPWM"] --> INV["inverter"] --> M["motor"]
  M --> ENC["encoder -> theta"] --> CP
  ENC --> IPARK
```

The sequence every PWM cycle (tens of microseconds): **measure** currents and
angle, **Clarke + Park** to $i_d, i_q$, run two **PI** controllers, **inverse
Park/Clarke** to voltages, **SVPWM** to gate signals.

## d-q decoupling

The d and q axes are not quite independent: a rotating motor cross-couples them
through the **speed EMF** terms $\\omega L i$. FOC adds **decoupling
feedforward** so the two PI loops act independently:

$$v_d = v_{d,PI} - \\omega L_q i_q, \\qquad v_q = v_{q,PI} + \\omega(L_d i_d + \\psi_{pm}).$$

A well-tuned $i_q$ loop tracks a torque step almost instantly. Slide the PI gain
and watch the closed-loop current response speed up (and risk overshoot if too
high):

```plot
{"title": "FOC iq current loop step response (slide loop bandwidth)", "xLabel": "time (ms)", "yLabel": "iq / iq*", "xRange": [0, 5], "yRange": [0, 1.4], "grid": true, "controls": [{"name": "bw", "range": [0.5, 4], "value": 1.5, "label": "loop bandwidth (relative)"}], "functions": [{"expr": "1 - exp(-bw*x)*cos(1.5*bw*x)", "label": "iq response", "color": "#dc2626"}]}
```

## Field weakening with FOC

Above base speed there is no voltage headroom left, so you drive **negative
$i_d$** to weaken the magnet flux and keep extending speed at constant power -
exactly how an EV reaches highway speed.

```matlab
% inner torque command -> q-axis current reference (PMSM, id*=0)
kt = 0.12; T_ref = 4.0;
iq_ref = T_ref/kt;               % ~33 A
id_ref = 0;                      % below base speed
```

```python
kt, T_ref = 0.12, 4.0
iq_ref = T_ref/kt                # ~33 A
id_ref = 0                       # below base speed
```

> **Real-world insight:** FOC is why a modern EV delivers instant, jerk-free
> torque from zero rpm and why robot arms can be both fast and precise - the same
> Clarke/Park/PI recipe scales from a tiny gimbal motor to a 200 kW traction drive.

**Next:** doing FOC without a position sensor - observers.
""",
        ),
        _t(
            "Sensorless control & observers",
            "13 min",
            """\
# Sensorless control & observers

FOC needs the rotor angle $\\theta$ for the Park transform. An encoder or resolver
gives it directly, but they cost money, add wiring, and can fail. **Sensorless
control** instead **estimates** rotor position and speed from the currents and
voltages the drive already measures.

## Two regimes, two methods

| Speed | Signal used | Method |
|-------|-------------|--------|
| **Medium/high** | back-EMF | model / observer estimates flux angle |
| **Low / zero** | magnetic saliency | high-frequency signal injection |

At decent speed the **back-EMF** is strong and its phase reveals the rotor angle;
near standstill the back-EMF vanishes, so you inject a small high-frequency probe
and detect the rotor's **saliency** (the d/q inductance difference).

## Observers: a model that corrects itself

An **observer** runs a real-time model of the motor and continuously corrects it
with the measurement error - a feedback loop on the *estimate*. The **Luenberger
observer** and the **sliding-mode observer** estimate the back-EMF (hence angle);
the **Kalman filter** does the same optimally under noise.

```mermaid
flowchart LR
  MEAS["measured v, i"] --> OBS["motor model + correction gain"]
  OBS --> EST["estimated back-EMF / flux"]
  EST --> ANG["theta_hat, speed_hat"]
  ANG --> FOC["FOC (Park uses theta_hat)"]
  OBS -->|error feedback| OBS
```

The estimate converges: start it wrong and the correction term drives the angle
error toward zero with a time constant set by the observer gain. Slide the gain
and watch convergence speed up (too high amplifies noise):

```plot
{"title": "Observer angle-error convergence (slide observer gain)", "xLabel": "time (ms)", "yLabel": "angle error (rad)", "xRange": [0, 20], "yRange": [-0.1, 1.1], "grid": true, "controls": [{"name": "L", "range": [0.2, 3], "value": 1, "label": "observer gain"}], "functions": [{"expr": "exp(-L*x/3)", "label": "estimation error", "color": "#dc2626"}]}
```

A phase-locked loop (PLL) typically extracts a clean angle and speed from the
estimated back-EMF.

```matlab
% sliding-mode style back-EMF estimate (sketch)
ealpha = valpha - R*ialpha - L*dialpha;   % stator-frame back-EMF
ebeta  = vbeta  - R*ibeta  - L*dibeta;
theta_hat = atan2(-ealpha, ebeta);         % rotor angle estimate
```

```python
import numpy as np
ealpha = valpha - R*ialpha - L*dialpha     # stator-frame back-EMF
ebeta  = vbeta  - R*ibeta  - L*dibeta
theta_hat = np.arctan2(-ealpha, ebeta)     # rotor angle estimate
```

> **Real-world insight:** sensorless FOC runs your **washing-machine, fridge, and
> heat-pump compressors** and many drones - removing the encoder cuts cost and a
> failure point. The hard part is always **low/zero speed**, where saliency
> injection earns its keep.

**Next:** running the machine as a generator - regenerative braking.
""",
        ),
        _t(
            "Regenerative braking & four-quadrant operation",
            "12 min",
            """\
# Regenerative braking & four-quadrant operation

A drive is not limited to motoring forward. Plot **torque vs speed** and you get
**four quadrants** - and a good drive can operate in all of them, including
**recovering** energy instead of wasting it.

## The four quadrants

| Quadrant | Speed | Torque | Power flow | Mode |
|----------|-------|--------|------------|------|
| **I** | + | + | to motor | forward motoring |
| **II** | + | - | from motor | forward braking (regen) |
| **III** | - | - | to motor | reverse motoring |
| **IV** | - | + | from motor | reverse braking (regen) |

In quadrants I and III the machine is a **motor** (power flows in); in II and IV
it is a **generator** - braking torque opposes motion and power flows **back to
the DC bus**.

```plot
{"title": "Four-quadrant torque-speed plane (Play traces a drive cycle)", "xLabel": "speed", "yLabel": "torque", "xRange": [-1.3, 1.3], "yRange": [-1.3, 1.3], "grid": true, "animate": {"param": "t", "range": [0, 6.2832], "label": "drive cycle"}, "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 6.2832], "label": "operating locus", "color": "#94a3b8"}], "points": [{"xExpr": "cos(t)", "yExpr": "sin(t)", "label": "operating point", "color": "#dc2626", "size": 7, "trail": true}]}
```

As the operating point sweeps the circle it passes through motoring (top-right),
regen braking (bottom-right), reverse motoring (bottom-left) and reverse regen
(top-left) - a complete EV acceleration-and-braking cycle.

## How regen works

To brake, the controller commands **negative $i_q$** (negative torque). The
machine now generates: current flows back through the inverter (its diodes/
synchronous switches act as a rectifier) and **charges the DC bus / battery**. The
braking energy that a friction brake would burn as heat is recovered.

```mermaid
stateDiagram-v2
  [*] --> Motoring
  Motoring --> Regen: command negative torque
  Regen --> Motoring: command positive torque
  Regen --> ChargeBus: energy to DC bus
  ChargeBus --> Battery: if SOC allows
  ChargeBus --> Chopper: else dump in brake resistor
```

## What if the bus cannot absorb it?

A battery can soak up regen (up to its charge limit); a grid-tied drive can push
it back to the grid (an **active front end**). But a simple diode-rectifier drive
**cannot** send power back - so the bus voltage would climb dangerously. The fix
is a **braking chopper + resistor** that dumps the excess as heat.

```matlab
% regen power available when braking
T = -8; w = 200;                 % negative torque, positive speed (quadrant II)
P = T*w;                         % negative -> power returned to the bus (W)
```

```python
T, w = -8, 200                   # quadrant II: braking
P = T*w                          # negative -> power back to the bus
```

> **Real-world insight:** regenerative braking extends EV range 10-25% in city
> driving and is why **trains, elevators, and cranes** feed energy back when
> descending or decelerating instead of cooking brake resistors.

**Next:** put a d-q current controller together in code.
""",
        ),
        _code(
            "Lab: d-q (FOC) current control",
            "14 min",
            """\
# Simulate the inner d-q current loop of field-oriented control on a PMSM.
# Two PI controllers regulate id and iq; we step the torque command (iq*) and
# watch the currents track. Module-level Euler simulation, numpy + matplotlib.
import numpy as np
import matplotlib.pyplot as plt

# PMSM electrical parameters
Rs = 0.5         # stator resistance (ohm)
Ld = 0.004       # d-axis inductance (H)
Lq = 0.004       # q-axis inductance (H)
psi = 0.1        # magnet flux linkage (Wb)
we = 300.0       # electrical speed (rad/s) -> couples d and q axes

# PI gains for both current loops (tuned for ~1 kHz bandwidth)
Kp = 8.0
Ki = 2000.0

dt = 2e-5        # 50 kHz control/sim step
t = np.arange(0, 0.02, dt)       # 20 ms

# References: id* = 0 (no field weakening), iq* steps from 0 to 30 A at t=2ms
id_ref = np.zeros_like(t)
iq_ref = np.where(t >= 0.002, 30.0, 0.0)

id_meas = np.zeros_like(t)
iq_meas = np.zeros_like(t)

id_i = 0.0; iq_i = 0.0           # PI integrators
id_s = 0.0; iq_s = 0.0           # state currents

for k in range(len(t)):
    # current errors
    ed = id_ref[k] - id_s
    eq = iq_ref[k] - iq_s
    # PI controllers (integrate the error)
    id_i += Ki*ed*dt
    iq_i += Ki*eq*dt
    vd_pi = Kp*ed + id_i
    vq_pi = Kp*eq + iq_i
    # decoupling feedforward: cancel the speed cross-coupling terms
    vd = vd_pi - we*Lq*iq_s
    vq = vq_pi + we*(Ld*id_s + psi)
    # PMSM electrical dynamics in the d-q frame (Euler step)
    did = (vd - Rs*id_s + we*Lq*iq_s)/Ld
    diq = (vq - Rs*iq_s - we*(Ld*id_s + psi))/Lq
    id_s += did*dt
    iq_s += diq*dt
    id_meas[k] = id_s
    iq_meas[k] = iq_s

torque = 1.5*(3/2.0)*psi*iq_meas  # T = (3/2)(P/2) psi iq, lumped constant

plt.figure(figsize=(8, 4.5))
plt.plot(t*1e3, iq_ref, "--", color="#94a3b8", label="iq* (command)")
plt.plot(t*1e3, iq_meas, color="#dc2626", lw=2, label="iq (measured)")
plt.plot(t*1e3, id_meas, color="#2563eb", lw=2, label="id (held at 0)")
plt.xlabel("time (ms)"); plt.ylabel("current (A)")
plt.title("FOC inner loop: iq tracks the torque step, id stays decoupled")
plt.legend(); plt.grid(True); plt.show()

settle = np.argmax(iq_meas > 0.95*30.0)
print(f"iq command   = 30 A")
print(f"iq reached 95% at t = {t[settle]*1e3:.2f} ms after the step")
print(f"id stayed near {np.max(np.abs(id_meas[t>0.005])):.2f} A (good decoupling)")

# Try it yourself:
#   1. Remove the decoupling terms (set them to 0): id gets disturbed by iq steps.
#   2. Raise Kp/Ki: faster tracking, but watch for overshoot/oscillation.
""",
        ),
        _t(
            "Applications & the throughline: EV, robotics, industrial & HVAC",
            "12 min",
            """\
# Applications & the throughline: EV, robotics, industrial & HVAC

Everything in this track converges in real products. The same chain -
**machine + inverter + control** - powers wildly different applications by
changing only the machine type, ratings, and control tuning.

## Electric vehicles

The flagship application. A **PMSM** (or sometimes induction motor, as in early
Teslas) driven by a **SiC inverter** under **FOC** with **field weakening**
delivers instant torque from zero rpm, high efficiency for range, and
**regenerative braking** to recover energy. The traction control loop runs the
exact Clarke/Park/PI recipe from this course at tens of kHz.

```plot
{"title": "EV traction: torque flat to base speed, then constant power (slide power)", "xLabel": "speed (krpm)", "yLabel": "torque (N.m)", "xRange": [0, 15], "yRange": [0, 350], "grid": true, "controls": [{"name": "Pk", "range": [80, 200], "value": 150, "label": "rated power (kW)"}], "functions": [{"expr": "min(300, Pk*9549/(x*1000 + 1))", "label": "torque envelope", "color": "#16a34a"}]}
```

Below base speed torque is flat (current-limited); above it, torque falls as
**1/speed** to hold constant power (voltage-limited) - the classic EV envelope.

## Robotics & servos

Robot joints use **PMSM/BLDC servos** with high-resolution encoders and FOC for
precise, fast, jerk-free torque. **Steppers** still drive cheap open-loop axes
(3D printers, small CNC). The control priority is **bandwidth and accuracy**, not
raw efficiency.

## Industrial drives

Pumps, fans, conveyors, compressors, mills - mostly **induction motors** on
**VFDs**. Simple loads run **V/f**; demanding ones (cranes, extruders, paper
mills) use **vector control**. The payoff is energy: variable-speed pumps and fans
replace wasteful valves and dampers.

## HVAC & appliances

Heat-pump and AC compressors, blowers, and circulation pumps increasingly use
**sensorless FOC PMSM** drives for quiet, efficient, variable-capacity operation -
the reason modern inverter ACs sip power compared with old on/off units.

```mermaid
flowchart LR
  SRC["DC bus / battery / grid"] --> INV["inverter (PWM)"]
  CTRL["control: V/f or FOC + observer"] --> INV
  INV --> MACH["machine: DC / induction / PMSM / BLDC / stepper"]
  MACH --> LOAD["EV wheel / robot joint / pump / compressor"]
  MACH --> FB["feedback / estimator"] --> CTRL
```

## The throughline

A magnetic circuit converts current into torque (Basics); arrange it as a rotating
field and you get rugged induction and high-density synchronous machines
(Intermediate); wrap it in an inverter and Clarke/Park/PI control and you can
command torque precisely, weaken the field for speed, run sensorless, and recover
braking energy (Advanced). **Model it** (MATLAB/Python), respect the **thermal
limits**, and the same handful of equations - Faraday, the torque law, and the d-q
transform - scale from a 5 W fan to a 10 MW ship propulsion drive.

> **Real-world insight:** electric machines and their drives consume roughly
> **45% of the world's electricity**. Even a one-point efficiency gain - better
> control, variable speed instead of throttling - is a planetary-scale energy
> saving. That is why this field is booming.

**Next:** the final check.
""",
        ),
    ),
)


MACHINES_COURSES: tuple[SeedCourse, ...] = (
    _MACHINES_BASICS,
    _MACHINES_INTERMEDIATE,
    _MACHINES_ADVANCED,
)

__all__ = ["MACHINES_COURSES"]
