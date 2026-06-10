"""Curated Electronics & Circuits track: Basics, Intermediate, Advanced.

A complete electronics curriculum: DC circuit fundamentals (charge, Ohm,
Kirchhoff, network analysis, power), AC and reactive components (capacitors/
inductors, transients, phasors/impedance, resonance, filters), and analog
electronics (diodes, transistors, op-amps, active filters, power electronics,
practical design). Dual MATLAB + Python focus throughout, with runnable Python
labs (numpy + matplotlib), interactive ```plot blocks, Mermaid diagrams, LaTeX
formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/electronics_*.py) at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ── Electronics & Circuits — Basics ───────────────────────────────────────────

_ELECTRONICS_BASICS = SeedCourse(
    slug="electronics-basics",
    title="Electronics & Circuits — Basics",
    description=(
        "DC circuits from the ground up: charge, current, voltage and power, "
        "Ohm's law and resistor networks, Kirchhoff's laws, nodal/mesh/Thevenin "
        "analysis, and power - with side-by-side MATLAB and Python, interactive "
        "plots, and a runnable circuit-solver lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Charge, current, voltage & power",
            "10 min",
            """\
# Charge, current, voltage & power

Electronics is the controlled movement of **electric charge**. Four quantities
describe everything:

| Quantity | Symbol | Unit | Intuition |
|----------|--------|------|-----------|
| Charge | $Q$ | coulomb (C) | "amount" of electricity |
| Current | $I$ | ampere (A) | charge **flow rate**, $I = dQ/dt$ |
| Voltage | $V$ | volt (V) | energy **per charge**, the "push" |
| Power | $P$ | watt (W) | energy **per time**, $P = VI$ |

A helpful analogy: **voltage** is water pressure, **current** is flow rate, a
**resistor** is a narrow pipe, and **power** is how much work the water does.

## Ohm's law, the cornerstone

For a resistor, current is proportional to voltage:

$$V = I\\,R, \\qquad P = VI = I^2 R = \\frac{V^2}{R}.$$

Drag the resistance and watch the current-vs-voltage line tilt - a steeper line
means *less* resistance:

```plot
{"title": "Ohm's law: current vs voltage (slide R)", "xLabel": "voltage V (V)", "yLabel": "current I (A)", "xRange": [0, 10], "yRange": [0, 2.2], "grid": true, "controls": [{"name": "R", "range": [5, 100], "value": 10, "label": "resistance R (ohm)"}], "functions": [{"expr": "x/R", "label": "I = V / R"}]}
```

## A bit of history

- **1780s - Volta** builds the first battery (the "voltaic pile"), giving steady
  current for the first time.
- **1820s - Ampere and Ohm.** Ampere links current and magnetism; Georg Ohm
  publishes $V = IR$ (1827) - mocked at first, now the first thing every
  engineer learns.
- **1845 - Kirchhoff** states the two circuit laws (next lessons) while still a
  student.

## Same calculation, two languages

```matlab
V = 5; R = 220;
I = V / R;            % 0.0227 A
P = V * I;            % 0.114 W
```

```python
V, R = 5, 220
I = V / R             # 0.0227 A
P = V * I             # 0.114 W
```

**Next:** resistors in series and parallel, and the divider.
""",
        ),
        _t(
            "Ohm's law & resistor networks",
            "11 min",
            """\
# Ohm's law & resistor networks

Real circuits combine many resistors. Two rules collapse them:

- **Series** (same current): $R_{eq} = R_1 + R_2 + \\dots$
- **Parallel** (same voltage): $\\dfrac{1}{R_{eq}} = \\dfrac{1}{R_1} + \\dfrac{1}{R_2} + \\dots$ (always *smaller* than the smallest).

## The voltage divider - the most-used circuit in electronics

Two series resistors split a voltage in proportion to their resistance:

$$V_{out} = V_{in}\\,\\frac{R_2}{R_1 + R_2}.$$

```mermaid
flowchart TB
  VIN["Vin"] --> R1["R1"] --> NODE(("Vout"))
  NODE --> R2["R2"] --> GND["ground"]
```

Slide $R_1$ and see how $V_{out}$ (with $V_{in} = 10\\,$V) changes as $R_2$ grows:

```plot
{"title": "Voltage divider: Vout = Vin * R2/(R1+R2), Vin=10", "xLabel": "R2 (ohm)", "yLabel": "Vout (V)", "xRange": [0, 100], "yRange": [0, 10], "grid": true, "controls": [{"name": "R1", "range": [10, 100], "value": 50, "label": "R1 (ohm)"}], "functions": [{"expr": "10*x/(R1+x)", "label": "Vout"}]}
```

Dividers set reference voltages, scale sensor signals, and bias transistors. Its
sibling, the **current divider**, splits current between parallel branches.

```matlab
R1 = 1000; R2 = 2000; Vin = 10;
Rser = R1 + R2;                 % series
Rpar = 1/(1/R1 + 1/R2);         % parallel
Vout = Vin * R2/(R1+R2);        % divider -> 6.67 V
```

```python
R1, R2, Vin = 1000, 2000, 10
Rser = R1 + R2
Rpar = 1/(1/R1 + 1/R2)
Vout = Vin * R2/(R1+R2)         # 6.67 V
```

> **Practical insight:** a divider's output sags when you connect a **load** -
> its output impedance is $R_1 \\parallel R_2$. Use it for references and signals,
> not to power anything.

**Next:** the two laws that solve *any* circuit - Kirchhoff's.
""",
        ),
        _t(
            "Kirchhoff's laws: KCL & KVL",
            "11 min",
            """\
# Kirchhoff's laws: KCL & KVL

Ohm's law handles one resistor; **Kirchhoff's laws** handle whole networks.
They're just conservation of charge and energy:

- **KCL (Current Law)** - charge can't pile up: the currents **into** any node
  sum to zero. $\\sum I_{in} = \\sum I_{out}$.
- **KVL (Voltage Law)** - energy is conserved: voltages around any **closed
  loop** sum to zero. $\\sum V = 0$.

```mermaid
flowchart LR
  N1(("node A")) -->|I1| N2(("node B"))
  N1 -->|I2| N3(("node C"))
  N2 -->|I3| N3
```

At node A above, KCL says the current in equals $I_1 + I_2$.

## Worked idea: a single loop

A 12 V source drives $R_1 = 1\\,$k and $R_2 = 2\\,$k in series. KVL around the
loop: $12 = I R_1 + I R_2$, so $I = 12/3000 = 4\\,$mA, and the resistor voltages
are $4$ V and $8$ V - which sum back to 12 V, as KVL demands.

## Sign conventions matter

Pick a current direction and a loop direction, then be consistent: a voltage is
a *rise* or a *drop* depending on which way you traverse it. Most circuit-solving
mistakes are sign errors, not algebra.

```matlab
% Single loop: 12V, R1=1k, R2=2k in series
Vs = 12; R1 = 1e3; R2 = 2e3;
I  = Vs/(R1+R2);          % KVL -> 4 mA
V1 = I*R1;  V2 = I*R2;    % 4 V, 8 V  (sum = 12 V)
```

```python
Vs, R1, R2 = 12, 1e3, 2e3
I = Vs/(R1+R2)            # 4 mA
V1, V2 = I*R1, I*R2       # 4 V, 8 V
```

> **Practical insight:** KCL + KVL + Ohm's law are *complete* - they can solve
> any lumped circuit. The methods in the next lesson are just bookkeeping that
> applies them efficiently to big networks.

**Next:** systematic methods - nodal, mesh, and Thevenin.
""",
        ),
        _t(
            "Circuit analysis: nodal, mesh & Thevenin",
            "12 min",
            """\
# Circuit analysis: nodal, mesh & Thevenin

For anything bigger than one loop, use a systematic method that turns the
circuit into **linear equations** $G\\mathbf{v} = \\mathbf{i}$.

## Nodal analysis (the computer's favourite)

1. Pick a **ground** (reference) node.
2. Write **KCL** at every other node, expressing branch currents via Ohm's law.
3. Solve the linear system for the node voltages.

This is exactly how **SPICE** simulators work, and what you'll code in the lab.

## Mesh analysis

The dual: assign a **loop current** to each independent loop, write **KVL**
around each, and solve. Nodal is usually easier when there are fewer nodes;
mesh when there are fewer loops.

## Thevenin & Norton: shrink any network to a two-terminal box

Any linear network, seen from two terminals, behaves like **one source plus one
resistor**:

- **Thevenin:** a voltage source $V_{th}$ in series with $R_{th}$.
- **Norton:** a current source $I_N$ in parallel with $R_N$ (with $R_N = R_{th}$).

$V_{th}$ is the open-circuit voltage; $R_{th}$ is the resistance looking in with
sources zeroed. This is how engineers reason about *output impedance* and
*loading* without re-solving the whole circuit each time.

```mermaid
flowchart LR
  BOX["any linear network"] --> EQ["Vth in series with Rth"]
  EQ --> LOAD["load"]
```

```matlab
% Nodal analysis: G * v = i  (two unknown nodes)
G = [1/R1 + 1/R2 + 1/R4, -1/R2;
     -1/R2,               1/R2 + 1/R3];
i = [Vs/R1; 0];
v = G \\ i;                 % node voltages
```

```python
import numpy as np
G = np.array([[1/R1 + 1/R2 + 1/R4, -1/R2],
              [-1/R2,               1/R2 + 1/R3]])
i = np.array([Vs/R1, 0.0])
v = np.linalg.solve(G, i)   # node voltages
```

**Next:** power and energy - and getting the most of it.
""",
        ),
        _t(
            "Power, energy & sources",
            "10 min",
            """\
# Power, energy & sources

Every component either **delivers** or **dissipates** power. For a resistor it's
always dissipated as heat:

$$P = VI = I^2 R = \\frac{V^2}{R}.$$

Energy is power over time, $E = \\int P\\,dt$ - your battery's **watt-hours**, your
electric bill's **kilowatt-hours**.

## Real sources have internal resistance

An ideal voltage source holds $V$ no matter the load; a real battery has
internal resistance $R_s$, so its terminal voltage **sags** under load:
$V_{term} = V - I R_s$. That's why a phone battery reads lower while charging a
big load.

## Maximum power transfer

A source with Thevenin resistance $R_{th}$ delivers the **most power to a load**
when $R_{load} = R_{th}$ (matched). At that point efficiency is only 50% (half
the power heats the source) - so power systems instead aim for $R_{load} \\gg
R_{th}$ (high efficiency), while RF and audio often *match* for maximum transfer.

```matlab
Vs = 10; Rs = 50;
RL = 0:1:200;
P  = (Vs.^2 .* RL) ./ (Rs + RL).^2;   % peaks at RL = Rs = 50
[Pmax, k] = max(P);
```

```python
import numpy as np
Vs, Rs = 10, 50
RL = np.arange(0, 200)
P = Vs**2 * RL / (Rs + RL)**2          # peaks at RL = Rs
```

```plot
{"title": "Maximum power transfer: load power peaks at RL = Rs = 50", "xLabel": "load resistance RL (ohm)", "yLabel": "power to load (W)", "xRange": [0, 200], "yRange": [0, 0.55], "grid": true, "functions": [{"expr": "100*x/(50+x)^2", "label": "P(RL)"}]}
```

> **Practical insight:** size resistors by **power**, not just resistance - a
> 1/4 W resistor with 1 W across it burns up. $P = V^2/R$ tells you the rating
> you need.

**Next:** put it together - solve a resistor network in code.
""",
        ),
        _code(
            "Lab: solve a resistor network",
            "12 min",
            """\
# Nodal analysis: solve a resistor network the way SPICE does.
# Build the conductance matrix G, solve G v = i for node voltages.
import numpy as np
import matplotlib.pyplot as plt

# Circuit: 10 V source through R1 to node 1; R2 from node1->node2;
#          R3 from node2->ground; R4 from node1->ground.
Vs = 10.0
R1, R2, R3, R4 = 100.0, 220.0, 330.0, 470.0

# KCL at nodes 1 and 2 (ground = 0). The source+R1 becomes a Norton current.
G = np.array([
    [1/R1 + 1/R2 + 1/R4, -1/R2],
    [-1/R2,               1/R2 + 1/R3],
])
i = np.array([Vs/R1, 0.0])

v = np.linalg.solve(G, i)          # node voltages [V1, V2]
i_R2 = (v[0] - v[1]) / R2          # current through R2
i_R3 = v[1] / R3                   # current through R3

print(f"node 1 = {v[0]:.3f} V,  node 2 = {v[1]:.3f} V")
print(f"I(R2) = {i_R2*1000:.2f} mA,  I(R3) = {i_R3*1000:.2f} mA")
print(f"KCL check at node 2: in {i_R2*1000:.2f} mA == out {i_R3*1000:.2f} mA")

plt.figure(figsize=(6, 3.5))
plt.bar(["node 1", "node 2"], v, color=["#2563eb", "#16a34a"])
plt.ylabel("voltage (V)"); plt.title("Solved node voltages")
plt.grid(True, axis="y"); plt.show()

# Try it yourself:
#   1. Change R4 to 1e9 (open it) and re-solve - node 1 rises.
#   2. The MATLAB equivalent uses the backslash solve operator: v = G \\ i;
""",
        ),
    ),
)


# ── Electronics & Circuits — Intermediate ─────────────────────────────────────

_ELECTRONICS_INTERMEDIATE = SeedCourse(
    slug="electronics-intermediate",
    title="Electronics & Circuits — Intermediate: AC & Reactive Circuits",
    description=(
        "Capacitors and inductors, first-order RC/RL transients, AC steady state "
        "with phasors and impedance, RLC resonance and the Q factor, and passive "
        "filters - with dual MATLAB/Python, interactive plots, and a runnable "
        "transient/resonance lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Capacitors & inductors",
            "11 min",
            """\
# Capacitors & inductors

Resistors dissipate energy; **capacitors** and **inductors** *store* it - and
their voltage/current relationships involve **rates of change**, which is what
makes circuits interesting.

| Component | Stores energy in | Law | Energy |
|-----------|------------------|-----|--------|
| Capacitor $C$ | electric field | $i = C\\,\\dfrac{dv}{dt}$ | $\\tfrac{1}{2}C v^2$ |
| Inductor $L$ | magnetic field | $v = L\\,\\dfrac{di}{dt}$ | $\\tfrac{1}{2}L i^2$ |

The duals of each other: a capacitor **resists voltage change** (its voltage
can't jump), an inductor **resists current change** (its current can't jump).

## Charging a capacitor through a resistor

Connect $V_s$ through $R$ to $C$ and the capacitor voltage rises exponentially
with **time constant** $\\tau = RC$:

$$v_C(t) = V_s\\left(1 - e^{-t/\\tau}\\right).$$

After $\\tau$ it's at 63%; after $5\\tau$ it's essentially full. Slide $\\tau$:

```plot
{"title": "Capacitor charging through a resistor", "xLabel": "time (s)", "yLabel": "Vc / Vsource", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "tau", "range": [0.5, 4], "value": 1, "label": "time constant tau = RC (s)"}], "functions": [{"expr": "1 - exp(-x/tau)", "label": "Vc(t)"}]}
```

```matlab
R = 1e3; C = 1e-6; tau = R*C;     % 1 ms
t = 0:1e-5:5*tau;
vc = 5*(1 - exp(-t/tau));
```

```python
import numpy as np
R, C = 1e3, 1e-6
tau = R*C                          # 1 ms
t = np.arange(0, 5*tau, 1e-5)
vc = 5*(1 - np.exp(-t/tau))
```

**Next:** the full first-order transient story - RC and RL.
""",
        ),
        _t(
            "First-order transients: RC & RL",
            "11 min",
            """\
# First-order transients: RC & RL

Any circuit with **one** capacitor or inductor (plus resistors) is **first
order**: flip a switch and every voltage and current relaxes exponentially from
its old value to its new one, with one time constant.

- **RC:** $\\tau = RC$.
- **RL:** $\\tau = L/R$.

The universal first-order response:

$$x(t) = x_\\infty + (x_0 - x_\\infty)\\,e^{-t/\\tau}.$$

Charging rises toward the final value; discharging decays toward zero - same
$\\tau$, mirror images:

```plot
{"title": "First-order charge vs discharge (same time constant)", "xLabel": "time / tau", "yLabel": "normalized", "xRange": [0, 6], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1 - exp(-x)", "label": "charging", "color": "#2563eb"}, {"expr": "exp(-x)", "label": "discharging", "color": "#dc2626"}]}
```

## Where it bites in practice

- **RC delays** set switch debouncing, reset timing, and the speed limit of
  driving a capacitive load (a long PCB trace, a MOSFET gate).
- **Inductive kick:** open a switch on an inductor (a relay, a motor) and
  $v = L\\,di/dt$ spikes huge - which is why you put a **flyback diode** across
  coils to give the current somewhere to go.

```matlab
% RC discharge from 5 V
tau = 1e-3; t = 0:1e-5:5*tau;
vc = 5*exp(-t/tau);
```

```python
import numpy as np
tau = 1e-3
t = np.arange(0, 5*tau, 1e-5)
vc = 5*np.exp(-t/tau)
```

> **Practical insight:** "how fast is this circuit?" almost always reduces to
> "what's the time constant?" Five time constants is the rule-of-thumb for
> "settled."

**Next:** steady sinusoids - phasors and impedance.
""",
        ),
        _t(
            "AC circuits, phasors & impedance",
            "12 min",
            """\
# AC circuits, phasors & impedance

Mains, radio, audio - the world runs on **sinusoids**. In **AC steady state**
every voltage and current is a sinusoid at the same frequency, differing only in
**amplitude** and **phase**. A **phasor** captures both as a complex number, so
calculus becomes algebra.

The key generalisation of resistance is **impedance** $Z$ (complex, in ohms):

| Component | Impedance $Z$ | Behaviour |
|-----------|---------------|-----------|
| Resistor | $R$ | flat with frequency |
| Capacitor | $\\dfrac{1}{j\\omega C}$ | blocks DC, passes high $f$ |
| Inductor | $j\\omega L$ | passes DC, blocks high $f$ |

where $\\omega = 2\\pi f$. Then **Ohm's law just works** for AC: $V = I Z$, and you
combine impedances in series/parallel exactly like resistors.

A capacitor's impedance magnitude **falls** with frequency while an inductor's
**rises** - they cross over, which is the seed of resonance and filtering:

```plot
{"title": "Impedance magnitude vs frequency", "xLabel": "frequency f (Hz)", "yLabel": "|Z| (ohm)", "xRange": [1, 100], "yRange": [0, 60], "grid": true, "functions": [{"expr": "159/x", "label": "|Zc| = 1/(2 pi f C), falls with f", "color": "#2563eb"}, {"expr": "0.314*x", "label": "|Zl| = 2 pi f L, rises with f", "color": "#dc2626"}]}
```

## Reactance, magnitude & phase

The imaginary part of $Z$ is **reactance** $X$. A capacitor's current **leads**
its voltage by 90 degrees; an inductor's **lags** by 90 degrees ("ELI the ICE
man"). The magnitude $|Z| = \\sqrt{R^2 + X^2}$ sets amplitude; the angle sets
phase.

```matlab
f = 1e3; w = 2*pi*f; C = 1e-6; L = 1e-3; R = 100;
Zc = 1/(1j*w*C);  Zl = 1j*w*L;  Zr = R;
Ztot = Zr + Zc;            % a series R-C, complex ohms
```

```python
import numpy as np
f, C, L, R = 1e3, 1e-6, 1e-3, 100
w = 2*np.pi*f
Zc = 1/(1j*w*C); Zl = 1j*w*L; Zr = R
Ztot = Zr + Zc
```

**Next:** what happens when L and C meet - resonance.
""",
        ),
        _t(
            "RLC resonance & the Q factor",
            "12 min",
            """\
# RLC resonance & the Q factor

Put a capacitor and inductor together and at one special frequency their
impedances **cancel** - **resonance**:

$$\\omega_0 = \\frac{1}{\\sqrt{LC}}, \\qquad f_0 = \\frac{1}{2\\pi\\sqrt{LC}}.$$

A series RLC becomes purely resistive (minimum impedance, maximum current) at
$f_0$; a parallel RLC peaks in impedance. This is how a radio **tunes** to one
station and rejects the rest.

## The Q factor: how sharp is the peak?

The **quality factor** $Q$ measures how selective the resonance is -
$Q = \\omega_0 L / R$ for a series RLC. High $Q$ = a tall, narrow peak (sharp
tuning, low loss); low $Q$ = broad and damped. The **bandwidth** is
$\\Delta f = f_0 / Q$. Slide $Q$:

```plot
{"title": "RLC band-pass resonance (slide Q)", "xLabel": "frequency / f0", "yLabel": "|H|", "xRange": [0.2, 3], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "Q", "range": [1, 15], "value": 5, "label": "quality factor Q"}], "functions": [{"expr": "1/sqrt(1 + Q^2*(x - 1/x)^2)", "label": "|H(f)|"}]}
```

## Damping connects back to control

A series RLC is a textbook **second-order system** (from the Signals/Control
tracks): $Q$ relates to the damping ratio by $\\zeta = 1/(2Q)$. High $Q$ = lightly
damped = rings; low $Q$ = heavily damped. The same math describes a tuned radio
and a car's suspension.

```matlab
L = 1e-3; C = 1e-9;
f0 = 1/(2*pi*sqrt(L*C))            % resonant frequency
Q  = (2*pi*f0*L)/R;               % quality factor
```

```python
import numpy as np
L, C = 1e-3, 1e-9
f0 = 1/(2*np.pi*np.sqrt(L*C))      # resonant frequency
Q  = (2*np.pi*f0*L)/R              # quality factor
```

**Next:** shaping frequency on purpose - passive filters.
""",
        ),
        _t(
            "Frequency response & passive filters",
            "11 min",
            """\
# Frequency response & passive filters

A **filter** passes some frequencies and blocks others. The simplest is an **RC
low-pass**: a resistor feeding a capacitor. At low frequency the cap is a high
impedance (output = input); at high frequency it shorts the signal to ground
(output drops). The **cutoff frequency** where it's down to $1/\\sqrt{2}$
(-3 dB) is

$$f_c = \\frac{1}{2\\pi R C}.$$

Slide the cutoff:

```plot
{"title": "RC low-pass magnitude response (slide cutoff)", "xLabel": "frequency f (Hz)", "yLabel": "|H|", "xRange": [1, 1000], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "fc", "range": [20, 500], "value": 100, "label": "cutoff fc (Hz)"}], "functions": [{"expr": "1/sqrt(1+(x/fc)^2)", "label": "low-pass |H|"}, {"expr": "(x/fc)/sqrt(1+(x/fc)^2)", "label": "high-pass |H|", "color": "#dc2626"}]}
```

Swap R and C and you get a **high-pass**; cascade or use RLC for **band-pass**
and **band-stop**. Beyond cutoff the response rolls off at **-20 dB/decade** per
order.

```mermaid
flowchart LR
  IN["Vin"] --> R["R"] --> OUT(("Vout")) --> C["C"] --> GND["ground"]
```

```matlab
R = 1.6e3; C = 1e-6;
fc = 1/(2*pi*R*C)                 % ~100 Hz
f  = logspace(0, 4, 500);
H  = 1 ./ (1 + 1j*(f/fc));        % low-pass transfer function
semilogx(f, 20*log10(abs(H)));    % Bode magnitude
```

```python
import numpy as np
R, C = 1.6e3, 1e-6
fc = 1/(2*np.pi*R*C)              # ~100 Hz
f = np.logspace(0, 4, 500)
H = 1/(1 + 1j*(f/fc))            # low-pass
mag_db = 20*np.log10(np.abs(H))
```

> **Practical insight:** passive RC filters are gentle (first order) and load-
> sensitive. When you need a sharp cutoff or gain, you go **active** (op-amps,
> Advanced course). But an RC is often all you need to kill noise on a sensor
> line.

**Next:** simulate transients and resonance yourself.
""",
        ),
        _code(
            "Lab: RLC transient & resonance",
            "13 min",
            """\
# Simulate a series RLC circuit's step response. Watch damping vs ringing.
# State: capacitor voltage vc, inductor current iL. Euler integration.
import numpy as np
import matplotlib.pyplot as plt

L = 1e-3        # 1 mH
C = 1e-6        # 1 uF  -> f0 = 1/(2 pi sqrt(LC)) ~ 5033 Hz
Vs = 1.0        # 1 V step input

f0 = 1/(2*np.pi*np.sqrt(L*C))
dt = 1e-7
t = np.arange(0, 1.5e-3, dt)

plt.figure(figsize=(8, 4))
for R, label, color in [(10, "R=10 (under-damped, rings)", "#dc2626"),
                        (60, "R=60 (near critical)", "#16a34a"),
                        (300, "R=300 (over-damped)", "#2563eb")]:
    vc = 0.0; iL = 0.0
    VC = np.zeros_like(t)
    for k in range(len(t)):
        # series RLC: Vs = iL*R + L*diL/dt + vc ; iL = C*dvc/dt
        diL = (Vs - iL*R - vc)/L
        dvc = iL/C
        iL += diL*dt
        vc += dvc*dt
        VC[k] = vc
    Q = (2*np.pi*f0*L)/R
    plt.plot(t*1e3, VC, color=color, label=f"{label}, Q={Q:.1f}")

plt.axhline(Vs, ls="--", color="#94a3b8")
plt.xlabel("time (ms)"); plt.ylabel("capacitor voltage (V)")
plt.title(f"Series RLC step response (f0 = {f0:.0f} Hz)")
plt.legend(); plt.grid(True); plt.show()

print(f"resonant frequency f0 = {f0:.0f} Hz")

# Try it yourself:
#   1. Lower R to 2 ohm: very high Q, long ringing.
#   2. The MATLAB way: use tf([1],[L C ...]) and step(), or lsim().
""",
        ),
    ),
)


# ── Electronics & Circuits — Advanced ─────────────────────────────────────────

_ELECTRONICS_ADVANCED = SeedCourse(
    slug="electronics-advanced",
    title="Electronics & Circuits — Advanced: Semiconductors & Analog Design",
    description=(
        "Active electronics: diodes and the PN junction, BJT and MOSFET "
        "transistors, operational amplifiers and active filters, power "
        "electronics (rectifiers, regulators, switching converters), and "
        "practical design with SPICE - dual MATLAB/Python, interactive plots, "
        "and a runnable rectifier/op-amp lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Diodes & the PN junction",
            "11 min",
            """\
# Diodes & the PN junction

Everything active starts with the **semiconductor**. Dope silicon to make
**n-type** (extra electrons) and **p-type** (holes), join them, and the **PN
junction** conducts strongly one way and barely the other - a **diode**, the
electronic one-way valve.

Its current grows **exponentially** with voltage (the Shockley equation):

$$I = I_s\\left(e^{V/(n V_T)} - 1\\right), \\qquad V_T \\approx 26\\,\\text{mV at room temp}.$$

That sharp "knee" near 0.6-0.7 V (for silicon) is why we often model a conducting
diode as a fixed ~0.7 V drop:

```plot
{"title": "Diode I-V curve: the exponential knee near 0.6 V", "xLabel": "forward voltage V (V)", "yLabel": "current (mA)", "xRange": [0, 0.8], "yRange": [0, 80], "grid": true, "functions": [{"expr": "max(0, 8*exp((x-0.6)/0.05) - 0.7)", "label": "diode current"}]}
```

## The diode family and what it's for

- **Rectifier** - turns AC into DC (half-wave, full-wave bridge).
- **Zener** - conducts in *reverse* at a precise voltage -> simple voltage
  reference/regulator.
- **LED** - emits light when forward biased; **photodiode** does the reverse.
- **Schottky** - low drop, very fast -> switching supplies.

```matlab
Vt = 0.026; Is = 1e-12;
V  = linspace(0, 0.8, 200);
I  = Is*(exp(V/Vt) - 1);          % Shockley equation (amps)
```

```python
import numpy as np
Vt, Is = 0.026, 1e-12
V = np.linspace(0, 0.8, 200)
I = Is*(np.exp(V/Vt) - 1)          # Shockley equation
```

> **Practical insight:** the exponential means diode current is *exquisitely*
> sensitive to voltage and temperature ($V_T$ scales with absolute temperature).
> Never drive a diode/LED from a voltage source alone - use a **series resistor**
> to set the current.

**Next:** the amplifying switch - transistors.
""",
        ),
        _t(
            "Transistors: BJT & MOSFET",
            "12 min",
            """\
# Transistors: BJT & MOSFET

The **transistor** is the invention that built the modern world: a small signal
controls a large one. It does two jobs - **amplify** and **switch** - and comes
in two great families.

## BJT (bipolar junction transistor)

**Current-controlled**: a small base current $I_B$ controls a large collector
current $I_C = \\beta I_B$ (with $\\beta$ ~ 100). Three regions:

- **Cut-off** - off (no base current).
- **Active** - amplifier ($I_C = \\beta I_B$, roughly constant).
- **Saturation** - fully on, a closed switch.

## MOSFET (the one in every chip)

**Voltage-controlled**: the gate voltage $V_{GS}$ (no steady gate current)
controls the drain current. Above the **threshold** $V_{th}$ it turns on. Its
near-zero static gate current and easy scaling are why **CMOS** (complementary
n- and p-MOSFETs) makes up essentially all digital logic and most modern analog.

| | BJT | MOSFET |
|--|-----|--------|
| Controlled by | base **current** | gate **voltage** |
| On-state | $V_{CE,sat}$ ~ 0.2 V | $R_{DS(on)}$ (a small resistance) |
| Best at | analog gain, fast switching | digital, power switching, integration |

```mermaid
flowchart LR
  IN["small input (Ib or Vgs)"] --> T["transistor"]
  SUP["supply"] --> T
  T --> OUT["large controlled output (Ic or Id)"]
```

## As a switch vs. as an amplifier

Drive it hard between cut-off and saturation and it's a **switch** (logic, motor
drivers, power supplies). Bias it in the **active/saturation-region** middle and
small input wiggles become large output wiggles - an **amplifier**. Biasing
(setting that operating point with resistor networks) is the heart of analog
design.

```matlab
beta = 100; Ib = 20e-6;
Ic = beta * Ib;                   % 2 mA in the active region
```

```python
beta, Ib = 100, 20e-6
Ic = beta * Ib                    # 2 mA
```

> **Practical insight:** for switching, drive a BJT base hard (into saturation)
> or a MOSFET gate fully above threshold - a half-on transistor dissipates huge
> power. For amplifiers, a stable bias point that resists temperature drift is
> everything.

**Next:** setting the operating point - biasing in linear and switching modes.
""",
        ),
        _t(
            "Biasing transistors: linear & switching modes",
            "13 min",
            """\
# Biasing transistors: linear & switching modes

A transistor only does something useful once you set its DC **operating point**
(the **Q-point**). *Where* you place that point decides whether the device is a
**linear amplifier** or a **switch**.

## Three families, two control styles

| Family | Controlled by | Normally | Law (active / saturation) |
|--------|---------------|----------|----------------------------|
| **BJT** (bipolar) | base **current** $I_B$ | off | $I_C = \\beta I_B$ |
| **JFET** | gate **voltage** (reverse) | **on** (depletion) | $I_D = I_{DSS}\\left(1 - \\dfrac{V_{GS}}{V_P}\\right)^2$ |
| **MOSFET** | gate **voltage** | off (enhancement) | $I_D = k\\,(V_{GS} - V_{th})^2$ |

The **JFET** is the family the transistor lesson skipped: a *depletion-mode*,
normally-**on** device. Make $V_{GS}$ more negative and you pinch the channel
until, at the **pinch-off voltage** $V_P$, it shuts off. Its square-law transfer
curve (slide pinch-off):

```plot
{"title": "JFET transfer: Id = Idss(1 - Vgs/Vp)^2 (slide pinch-off Vp)", "xLabel": "Vgs (V)", "yLabel": "Id (mA)", "xRange": [-5, 0.2], "yRange": [0, 11], "grid": true, "controls": [{"name": "Vp", "range": [-5, -2], "value": -4, "label": "pinch-off Vp (V)"}], "functions": [{"expr": "(x>Vp)*10*(1 - x/Vp)^2", "label": "Id (depletion JFET)"}]}
```

MOSFETs follow the same square law but turn on **above** a positive threshold
$V_{th}$ (enhancement type, normally off) - slide the threshold:

```plot
{"title": "MOSFET transfer: Id = k(Vgs - Vth)^2 in saturation (slide Vth)", "xLabel": "Vgs (V)", "yLabel": "Id (mA)", "xRange": [0, 5], "yRange": [0, 20], "grid": true, "controls": [{"name": "Vth", "range": [0.5, 3], "value": 1.5, "label": "threshold Vth (V)"}], "functions": [{"expr": "(x>Vth)*2*(x-Vth)^2", "label": "Id (enhancement NMOS)"}]}
```

## Linear mode: the Q-point and the load line

For amplification you bias the device **mid-range** in its active (BJT) /
saturation (FET) region so the signal can swing both ways without clipping. The
**DC load line** is just KVL on the output loop - for a BJT common-emitter with
collector resistor $R_C$ and supply $V_{CC}$:

$$I_C = \\frac{V_{CC} - V_{CE}}{R_C}.$$

The Q-point sits where this line crosses the device's curve. Slide $R_C$ and
watch the load line tilt:

```plot
{"title": "BJT DC load line: Ic = (Vcc - Vce)/Rc, Vcc=12 (slide Rc)", "xLabel": "Vce (V)", "yLabel": "Ic (mA)", "xRange": [0, 12], "yRange": [0, 25], "grid": true, "controls": [{"name": "Rc", "range": [0.5, 5], "value": 1, "label": "collector resistor Rc (kohm)"}], "functions": [{"expr": "(12 - x)/Rc", "label": "load line"}]}
```

Put the Q-point in the **middle** of the load line for maximum symmetric swing.

### Biasing methods (and why one wins)

- **BJT fixed-base bias** - one base resistor. Simple, but $I_C = \\beta I_B$
  drifts with temperature and the huge part-to-part $\\beta$ spread. Avoid.
- **BJT voltage-divider bias** - a divider sets the base voltage and an emitter
  resistor $R_E$ adds **negative feedback**: if $I_C$ rises, $V_E$ rises,
  shrinking $V_{BE}$ and pushing $I_C$ back. Stable and $\\beta$-independent - the
  standard.
- **JFET self-bias** - a source resistor makes $V_{GS} = -I_D R_S$; the bias
  line crosses the transfer curve at a stable point (no divider needed, since the
  JFET is normally on).
- **MOSFET bias** - gate voltage-divider plus source resistor (analog), or a
  current mirror.

```mermaid
flowchart TB
  VCC["Vcc"] --> R1["R1"] --> B(("base"))
  B --> R2["R2"] --> GND["gnd"]
  B --> Q["transistor"]
  Q --> RE["Re (feedback)"] --> GND
```

## Switching mode: slam between off and fully-on

For logic, power supplies, and motor drivers you don't sit in the middle - you
drive the transistor hard between **cut-off** (off) and **saturation/triode**
(fully on):

- **BJT**: enough base current to saturate ($V_{CE} \\approx 0.2$ V).
- **MOSFET**: $V_{GS}$ well above $V_{th}$, so it's a small resistance $R_{DS(on)}$.

Spend as little time as possible *in between*, because the linear region is where
a power device dissipates the most heat ($P = V_{CE} I_C$). A good switch is
either fully on (low $V$) or fully off (low $I$) - low power in both.

```matlab
Vcc=12; Rc=1e3; Re=220; R1=47e3; R2=10e3; Vbe=0.7;
Vb = Vcc*R2/(R1+R2);            % divider bias
Ie = (Vb - Vbe)/Re;  Ic = Ie;  % ~equal
Vce = Vcc - Ic*(Rc+Re);        % Q-point (aim mid-range)
```

```python
Vcc, Rc, Re, R1, R2, Vbe = 12, 1e3, 220, 47e3, 10e3, 0.7
Vb = Vcc*R2/(R1+R2)            # divider bias
Ie = (Vb - Vbe)/Re; Ic = Ie
Vce = Vcc - Ic*(Rc+Re)         # Q-point
```

> **Practical insight:** for **amplifiers**, use divider bias with an emitter/
> source resistor so the Q-point resists temperature and $\\beta$ spread; for
> **switches**, overdrive the input and care about saturation voltage /
> $R_{DS(on)}$ and switching speed, not the Q-point.

**Next:** the analog designer's Swiss-army knife - the op-amp.
""",
        ),
        _t(
            "Operational amplifiers",
            "12 min",
            """\
# Operational amplifiers

The **operational amplifier** is a differential amplifier with enormous gain
($10^5$ or more) that you tame with **feedback** into precise, predictable
circuits. Analyse almost any op-amp circuit with two **ideal-op-amp rules**:

1. **No current flows into the inputs** (infinite input impedance).
2. With negative feedback, the op-amp drives its output so the **two inputs are
   equal** ($V_+ = V_-$) - the "virtual short".

## The two canonical amplifiers

**Non-inverting** (gain $\\ge 1$, high input impedance):

$$V_{out} = V_{in}\\left(1 + \\frac{R_f}{R_{in}}\\right).$$

```plot
{"title": "Non-inverting amplifier gain = 1 + Rf/Rin (slide Rin)", "xLabel": "Rf (kohm)", "yLabel": "gain (V/V)", "xRange": [0, 100], "yRange": [0, 110], "grid": true, "controls": [{"name": "Rin", "range": [1, 20], "value": 10, "label": "Rin (kohm)"}], "functions": [{"expr": "1 + x/Rin", "label": "gain"}]}
```

**Inverting** (gain can be < 1, sets a virtual ground at $V_-$):

$$V_{out} = -V_{in}\\,\\frac{R_f}{R_{in}}.$$

```mermaid
flowchart LR
  VIN["Vin"] --> RIN["Rin"] --> N(("V- (virtual gnd)"))
  N --> OA["op-amp"]
  OA --> VOUT["Vout"]
  VOUT --> RF["Rf"] --> N
```

## Beyond gain

Swap resistors for capacitors and the op-amp becomes an **integrator** or
**differentiator**; add an RC network in the feedback and you get **active
filters** (next lesson). Other staples: the **comparator**, **summing
amplifier**, **difference/instrumentation amplifier** (for tiny sensor signals),
and the **buffer** (gain 1, isolates a high-impedance source from a load).

```matlab
Rin = 10e3; Rf = 100e3;
gain_inv    = -Rf/Rin;            % -10
gain_noninv = 1 + Rf/Rin;         % +11
```

```python
Rin, Rf = 10e3, 100e3
gain_inv = -Rf/Rin                # -10
gain_noninv = 1 + Rf/Rin          # +11
```

> **Practical insight:** real op-amps aren't ideal - finite **gain-bandwidth
> product**, input **offset voltage**, **slew rate**, and bias currents all bite.
> The gain-bandwidth product means a 1 MHz op-amp at gain 100 only reaches
> ~10 kHz: bandwidth = GBW / gain.

**Next:** building active filters and analog blocks.
""",
        ),
        _t(
            "Active filters & analog building blocks",
            "11 min",
            """\
# Active filters & analog building blocks

Passive RC filters are gentle and sag under load. Add an op-amp and you get
**active filters**: gain, sharp roll-off, and a buffered output that doesn't
care about the next stage.

## Why active wins

- **Gain in the passband** (passive filters only attenuate).
- **No loading** - the op-amp output drives the next stage stiffly.
- **High-order responses** built from cascaded stages: **Butterworth** (maximally
  flat), **Chebyshev** (steeper, with ripple), **Bessel** (clean phase).

The workhorse is the **Sallen-Key** stage - one op-amp and two RC pairs make a
second-order (-40 dB/decade) low- or high-pass filter. Cascade two for fourth
order, and so on.

## The op-amp building-block kit

| Block | Made from | Does |
|-------|-----------|------|
| Integrator | feedback capacitor | $V_{out} = -\\tfrac{1}{RC}\\int V_{in}\\,dt$ |
| Differentiator | input capacitor | output ~ $dV_{in}/dt$ |
| Active LPF/HPF/BPF | RC + op-amp | filter **with** gain |
| Instrumentation amp | 3 op-amps | amplify tiny differential sensor signals, reject noise |
| Oscillator | filter + positive feedback | generate sine/square waves |

```matlab
% Sallen-Key low-pass cutoff (equal R, equal C):
R = 10e3; C = 1.6e-9;
fc = 1/(2*pi*R*C)                 % ~10 kHz, second order
```

```python
import numpy as np
R, C = 10e3, 1.6e-9
fc = 1/(2*np.pi*R*C)              # ~10 kHz, second order
```

> **Practical insight:** an **integrator** is also a controller's "I" term and a
> filter's building block - the same op-amp circuit recurs across the Signals,
> Control, and Electronics tracks. Analog computing was literally op-amp
> integrators wired to solve differential equations.

**Next:** when the op-amp leaves the linear region - comparators.
""",
        ),
        _t(
            "Comparators & the Schmitt trigger",
            "12 min",
            """\
# Comparators & the Schmitt trigger

So far the op-amp has lived in its **linear** region, held there by negative
feedback. Remove that feedback (or add **positive** feedback) and the op-amp
becomes **non-linear**: its huge gain slams the output to a supply rail. That's
not a bug - it's the basis of a whole family of decision-making circuits.

## The comparator: a 1-bit analog-to-digital decision

With no feedback, the op-amp compares its two inputs and saturates:

$$V_{out} = \\begin{cases} +V_{sat} & V_+ > V_- \\\\ -V_{sat} & V_+ < V_- \\end{cases}$$

It answers one question - "is this voltage above that one?" - and is the front
door of every ADC, zero-crossing detector, and threshold alarm.

## The problem: chatter

A real signal has noise. When it dawdles near the threshold, the comparator
flips back and forth many times - **chatter** - because every noise wiggle
crosses the single trip point.

## The fix: hysteresis (the Schmitt trigger)

Add a little **positive feedback** and you get **two** thresholds: an upper trip
point $V_{TH+}$ and a lower one $V_{TH-}$. Once the output flips, the input must
travel all the way to the *other* threshold to flip it back - so noise smaller
than the gap $V_{TH+}-V_{TH-}$ can't cause a false transition. This is the
**Schmitt trigger**, and its transfer characteristic is a **hysteresis loop**:

```plot
{"title": "Schmitt trigger hysteresis loop (slide the gap H)", "xLabel": "input Vin", "yLabel": "output", "xRange": [-2.2, 2.2], "yRange": [-1.4, 1.4], "grid": true, "controls": [{"name": "H", "range": [0.1, 1.5], "value": 0.6, "label": "hysteresis half-gap H"}], "parametric": [{"x": "2*sin(t)", "y": "(cos(t)>0)*sign(2*sin(t)-H) + (1-(cos(t)>0))*sign(2*sin(t)+H)", "range": [0, 6.2832], "label": "Vout vs Vin"}]}
```

The loop is the giveaway: going **right** (input rising) the output flips at
$+H$; coming **back left** it doesn't flip until $-H$. For a non-inverting Schmitt
trigger the thresholds are set by the feedback divider,
$V_{TH\\pm} \\approx \\pm V_{sat}\\,\\dfrac{R_1}{R_2}$.

```mermaid
flowchart LR
  VIN["Vin"] --> CMP["comparator"]
  CMP --> VOUT["Vout (rail to rail)"]
  VOUT --> R2["R2"] --> NPLUS(("V+"))
  NPLUS --> R1["R1"] --> GND["ref"]
  NPLUS --> CMP
```

## More patterns and a warning

- **Window comparator** - two comparators flag "inside a voltage band" (under/over
  detection).
- **Relaxation oscillator** - a Schmitt trigger plus an RC makes a square-wave
  oscillator (the link to the next lesson... and the 555).
- **Use a real comparator** (e.g. LM393) for fast, clean switching. An op-amp run
  open-loop as a comparator is slow to recover from saturation and sometimes
  unsafe for its inputs.

```matlab
Vsat = 12; R1 = 10e3; R2 = 100e3;
Vth = Vsat * R1/R2;            % +/- trip points -> +/-1.2 V (hysteresis gap 2.4 V)
```

```python
Vsat, R1, R2 = 12, 10e3, 100e3
Vth = Vsat * R1/R2             # +/- trip points
```

> **Practical insight:** any time you turn a noisy or slow analog signal into a
> clean digital edge, reach for **hysteresis**. Size the gap larger than your
> noise, smaller than your real signal swing.

**Next:** nonlinearity *inside* the loop - precision and function circuits.
""",
        ),
        _t(
            "Precision & nonlinear op-amp circuits",
            "12 min",
            """\
# Precision & nonlinear op-amp circuits

Put a **nonlinear element** (a diode or transistor) *inside* the feedback loop
and the op-amp's gain **corrects for its imperfections** - giving precise
nonlinear functions you could never get from the device alone.

## Precision (active) rectifier - the "superdiode"

An ordinary diode rectifier has a dead zone: nothing happens until the input
clears the ~0.7 V drop, useless for small signals. Wrap the diode in an op-amp's
feedback and the loop drives the op-amp output ~0.7 V *higher* to compensate -
so the **rectified output has no dead zone**:

```plot
{"title": "Precision rectifier removes the diode's 0.7 V dead zone", "xLabel": "input voltage (V)", "yLabel": "rectified output (V)", "xRange": [-2, 2], "yRange": [-0.2, 2], "grid": true, "functions": [{"expr": "max(0, x)", "label": "precision rectifier (ideal)", "color": "#16a34a"}, {"expr": "max(0, x - 0.7)", "label": "plain diode (dead zone)", "color": "#dc2626"}]}
```

It rectifies millivolt signals - essential in AC meters, peak/RMS detectors, and
sensor front-ends.

## Log & antilog amplifiers

A diode or BJT's exponential $I$-$V$ in the feedback path makes the **output
proportional to the logarithm of the input** (and antilog with it in the input
path):

$$V_{out} \\approx -V_T \\ln\\!\\left(\\frac{V_{in}}{I_s R}\\right).$$

```plot
{"title": "Log amplifier compresses a wide input range", "xLabel": "input voltage (V)", "yLabel": "output (V)", "xRange": [0.02, 5], "yRange": [-1.5, 2.2], "grid": true, "functions": [{"expr": "-0.5*ln(x/1)", "label": "Vout ~ -k ln(Vin)"}]}
```

Why care? **Logs turn multiplication into addition**: log both signals, add,
antilog - that's an **analog multiplier/divider**, and the basis of dB meters,
audio compressors (companding), and old analog computers.

## The rest of the nonlinear toolkit

| Circuit | Nonlinear element | Does |
|---------|-------------------|------|
| Precision rectifier | diode in feedback | rectify small signals |
| Log / antilog amp | diode/BJT in feedback | compress / expand, multiply |
| **Peak detector** | diode + hold capacitor | capture and hold the maximum |
| **Sample-and-hold** | switch + capacitor + buffer | freeze a value (front of every ADC) |
| **Clipper / limiter** | diodes (often Zener) | bound the output swing |

```mermaid
flowchart LR
  VIN["Vin"] --> OA["op-amp"]
  OA --> D["diode (in feedback)"]
  D --> VOUT(("Vout"))
  VOUT --> OA
```

```matlab
Vt = 0.026; Is = 1e-12; R = 10e3;
Vout = -Vt * log(Vin/(Is*R));     % log amplifier
```

```python
import numpy as np
Vt, Is, R = 0.026, 1e-12, 10e3
Vout = -Vt * np.log(Vin/(Is*R))   # log amplifier
```

> **Practical insight:** feedback "hides" a diode's 0.7 V or a BJT's spread, but
> it can't beat the op-amp's **slew rate and recovery time** - precision
> nonlinear circuits are bandwidth-limited. Many modern designs sample early and
> do the nonlinearity in DSP, but precision analog front-ends still rely on these.

**Next:** generating waveforms from scratch - oscillators.
""",
        ),
        _t(
            "Oscillators",
            "12 min",
            """\
# Oscillators

An **oscillator** turns DC power into a periodic AC waveform with **no input
signal** - the heartbeat of every radio, clock, and tone generator. The trick is
**positive feedback**: route the output back *in phase* so the circuit reinforces
its own signal.

## The Barkhausen criterion

For sustained oscillation the **loop gain** must satisfy, at the oscillation
frequency:

$$|A\\beta| = 1 \\quad\\text{and}\\quad \\angle A\\beta = 0^\\circ \\;(\\text{or } 360^\\circ).$$

In words: a signal that goes once around the loop comes back **the same size**
and **in phase**. To *start up*, you design $|A\\beta|$ slightly **> 1** so circuit
noise grows; then a **nonlinearity** (a diode, a lamp, or the amplifier gently
clipping) trims the gain back to exactly 1, settling the amplitude - the **limit
cycle**. Press Play to watch it build:

```plot
{"title": "Oscillator startup: amplitude grows, then settles (limit cycle)", "xLabel": "time", "yLabel": "output", "xRange": [0, 12], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "w", "range": [2, 8], "value": 4, "label": "oscillation frequency"}], "animate": {"param": "t", "range": [0, 12], "label": "time"}, "functions": [{"expr": "(1 - exp(-0.4*x))*sin(w*x)", "label": "v(t)"}], "points": [{"xExpr": "t", "yExpr": "(1 - exp(-0.4*t))*sin(w*t)", "label": "now", "color": "#dc2626", "size": 6, "trail": true}]}
```

## The families

| Type | Frequency-setting element | $f$ | Use |
|------|---------------------------|-----|-----|
| **RC phase-shift** | 3 RC sections (60 deg each) | audio | simple sine |
| **Wien bridge** | RC bridge | $f = \\dfrac{1}{2\\pi R C}$ | low-distortion audio sine |
| **LC (Colpitts / Hartley)** | LC tank | $f = \\dfrac{1}{2\\pi\\sqrt{LC}}$ | RF |
| **Crystal** | quartz resonator (huge Q) | very precise | clocks, MCUs, radios |
| **Relaxation (555)** | RC charge/discharge | $f \\approx \\dfrac{1.44}{(R_A + 2R_B)C}$ | square / timing |

```mermaid
flowchart LR
  AMP["amplifier (gain A)"] --> OUT["output"]
  OUT --> FB["frequency-selective feedback (beta)"]
  FB --> AMP
```

## Sine vs. square

**Harmonic** oscillators (RC, LC, crystal) make clean **sine** waves at the
frequency where the feedback phase hits 0 degrees. **Relaxation** oscillators
(the 555 timer, ring oscillators) charge and discharge a capacitor between two
thresholds, making **square/triangle** waves - cheap timing, not spectrally pure.

The **Wien bridge** has pedigree: it was the product in Hewlett-Packard's first
instrument (the HP 200A audio oscillator, 1939), whose amplitude was stabilised
by a light bulb's resistance rising as it warmed. **Crystal** oscillators, at the
other extreme, reach parts-per-million stability and clock nearly every digital
system you own.

```matlab
R=10e3; C=10e-9;  f_wien = 1/(2*pi*R*C);            % Wien bridge sine
L=1e-6; Ct=100e-12; f_lc = 1/(2*pi*sqrt(L*Ct));     % LC (RF)
Ra=10e3; Rb=47e3; C2=1e-6; f_555 = 1.44/((Ra+2*Rb)*C2);  % 555 square
```

```python
import numpy as np
R, C = 10e3, 10e-9
f_wien = 1/(2*np.pi*R*C)                             # Wien bridge
L, Ct = 1e-6, 100e-12
f_lc = 1/(2*np.pi*np.sqrt(L*Ct))                     # LC
Ra, Rb, C2 = 10e3, 47e3, 1e-6
f_555 = 1.44/((Ra + 2*Rb)*C2)                        # 555 astable
```

> **Practical insight:** pick by frequency and purity - **RC/Wien** for audio
> sines, **LC** for RF, **crystal** when accuracy matters, **555/relaxation** for
> cheap square-wave timing. And respect Barkhausen: too little loop gain and it
> never starts; too much and it clips and distorts.

**Next:** moving real power - power electronics.
""",
        ),
        _t(
            "Power electronics: rectifiers, regulators & converters",
            "12 min",
            """\
# Power electronics: rectifiers, regulators & converters

Getting clean, stable DC from the wall (or a battery) is its own discipline.

## From AC to rough DC: rectifiers

A **bridge rectifier** (four diodes) flips the negative half of an AC sine up,
giving bumpy DC; a **reservoir capacitor** then smooths it, leaving some
**ripple**. Bigger cap (or higher frequency) = less ripple.

```mermaid
flowchart LR
  AC["AC mains"] --> RECT["bridge rectifier"] --> CAP["reservoir cap (smoothing)"] --> REG["regulator"] --> DC["clean DC"]
```

## From rough DC to clean DC: regulators

- **Linear regulator** (e.g. LDO): burns the excess voltage as heat. Simple,
  quiet, cheap - but inefficient when the drop is large
  ($\\eta = V_{out}/V_{in}$).
- **Switching regulator** (SMPS): rapidly switches a transistor and uses an
  inductor + capacitor to transfer energy in packets. Efficiency often **90%+**,
  at the cost of switching noise.

## Switching converter topologies

| Converter | Does | $V_{out}$ |
|-----------|------|-----------|
| **Buck** | steps voltage **down** | $V_{out} = D\\,V_{in}$ |
| **Boost** | steps voltage **up** | $V_{out} = V_{in}/(1-D)$ |
| **Buck-boost** | up or down (inverted) | $V_{out} = -V_{in}\\,D/(1-D)$ |

The control knob is the **duty cycle** $D$ of the **PWM** (pulse-width
modulation) driving the switch - and a feedback loop (often a PID-like
compensator from the Control track) adjusts $D$ to hold $V_{out}$ steady.

```matlab
Vin = 12; D = 0.4;
Vout_buck  = D*Vin;               % 4.8 V
Vout_boost = Vin/(1-D);           % 20 V
```

```python
Vin, D = 12, 0.4
Vout_buck = D*Vin                 # 4.8 V
Vout_boost = Vin/(1-D)            # 20 V
```

> **Practical insight:** efficiency matters most in battery and high-power
> systems (switchers), low noise matters most near sensitive analog/RF (linear
> LDOs). Real designs often use a switcher to get close, then an LDO to clean up.

**Next:** rectify and smooth a supply in code.
""",
        ),
        _code(
            "Lab: half-wave rectifier with smoothing",
            "12 min",
            """\
# Simulate a half-wave rectifier feeding a smoothing capacitor + load.
# Watch the ripple shrink as you change C or R.
import numpy as np
import matplotlib.pyplot as plt

fs = 20000                      # sim sample rate
t = np.arange(0, 0.06, 1/fs)    # 60 ms (a few mains cycles)
f_mains = 50                    # 50 Hz
Vpk = 10.0                      # peak input voltage
Vd = 0.7                        # diode drop
R = 1000.0                      # load resistance
C = 100e-6                      # smoothing capacitor

vin = Vpk*np.sin(2*np.pi*f_mains*t)
vout = np.zeros_like(t)
vc = 0.0
dt = 1/fs
for k in range(len(t)):
    if vin[k] - Vd > vc:        # diode conducts: cap follows the peak
        vc = vin[k] - Vd
    else:                       # diode blocks: cap discharges into R
        vc = vc - vc*dt/(R*C)
    vout[k] = vc

ripple = vout[t > 0.02].max() - vout[t > 0.02].min()

plt.figure(figsize=(8, 4))
plt.plot(t*1e3, vin, color="#94a3b8", label="Vin (AC)")
plt.plot(t*1e3, vout, color="#dc2626", lw=2, label="Vout (rectified + smoothed)")
plt.xlabel("time (ms)"); plt.ylabel("voltage (V)")
plt.title(f"Half-wave rectifier: ripple ~ {ripple:.2f} V")
plt.legend(); plt.grid(True); plt.show()

print(f"smoothed output ~ {vout[t>0.02].mean():.2f} V,  ripple ~ {ripple:.2f} V")

# Try it yourself:
#   1. Raise C to 1000e-6: ripple shrinks (bigger reservoir).
#   2. Drop R to 100: more load current drains the cap faster -> more ripple.
""",
        ),
        _t(
            "Practical design, SPICE & measurement",
            "10 min",
            """\
# Practical design, SPICE & measurement

The gap between a circuit that works on paper and one that works on a bench is
where engineering lives.

## Simulate before you solder: SPICE

**SPICE** (Simulation Program with Integrated Circuit Emphasis) does exactly
what the Basics lab did - nodal analysis - but with nonlinear device models and
across DC, AC, and transient analyses. Modern tools (LTspice, ngspice, KiCad's
simulator) let you sweep components and find problems before building anything.
Python's own ecosystem (`PySpice`, `lcapy`, `scikit-rf`) scripts and analyses
circuits programmatically.

## The non-idealities that bite

- **Noise** - thermal (Johnson) noise sets a noise floor; keep sensitive nodes
  high-impedance-aware and bandwidth-limited.
- **Parasitics** - every wire has inductance, every pair of traces a
  capacitance; at high frequency these dominate.
- **Decoupling** - put capacitors next to every chip's power pins so it can draw
  fast current locally instead of through inductive traces.
- **Grounding & layout** - a shared ground trace turns into a shared error; star
  grounds and ground planes matter as much as the schematic.
- **Thermal** - power devices need the heat to go somewhere (ratings, heatsinks).

## Measure it: the bench

An engineer's senses are the **multimeter** (DC volts/ohms/continuity), the
**oscilloscope** (voltage vs. time - your window into transients and ripple),
the **function generator** (stimulus), and the **power supply**. Probe, compare
to your model, and reconcile the difference - that loop is how real skill is
built.

## The throughline

Charge moving under voltage, shaped by R, L, and C, switched and amplified by
diodes and transistors, organised by op-amps and feedback, and powered by
converters - that's all of electronics, from a sensor front-end to a CPU's power
rail. Model it (MATLAB/Python/SPICE), respect the non-idealities, measure it, and
iterate. The components change; the laws - Ohm and Kirchhoff - never do.

**Next:** the final check.
""",
        ),
    ),
)


ELECTRONICS_COURSES: tuple[SeedCourse, ...] = (
    _ELECTRONICS_BASICS,
    _ELECTRONICS_INTERMEDIATE,
    _ELECTRONICS_ADVANCED,
)

__all__ = ["ELECTRONICS_COURSES"]
