"""Curated Power Systems & the Grid track: Basics, Intermediate, Advanced.

A complete power-engineering curriculum: AC power and three-phase, the per-unit
system and the grid (generation, transmission, distribution, transformers);
then power flow and faults (line modeling, Ybus and power flow, fault analysis,
protection, reactive-power control); and finally stability and the modern grid
(swing equation and equal-area, load-frequency control, renewable integration,
HVDC/FACTS, the smart grid). Dual MATLAB + Python focus throughout, with runnable
Python labs (numpy + matplotlib), interactive ```plot blocks, Mermaid diagrams,
LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Power Systems & the Grid -- Basics ----------------------------------------

_POWER_BASICS = SeedCourse(
    slug="power-systems-basics",
    title="Power Systems & the Grid -- Basics",
    description=(
        "How the electric grid works from the ground up: AC power (RMS, real, "
        "reactive and apparent power, power factor), three-phase systems, the "
        "per-unit system and phasors, the generation-transmission-distribution "
        "chain, and power transformers - with side-by-side MATLAB and Python, "
        "interactive plots, and a runnable power-triangle / three-phase lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "AC power: RMS, real, reactive & apparent power",
            "12 min",
            """\
# AC power: RMS, real, reactive & apparent power

The grid runs on **alternating current**: voltage and current are sinusoids that
swing positive and negative 50 or 60 times a second. To talk about "how much"
voltage a wiggling sinusoid has, we use the **RMS** (root-mean-square) value:

$$V_{rms} = \\frac{V_{peak}}{\\sqrt{2}}, \\qquad I_{rms} = \\frac{I_{peak}}{\\sqrt{2}}.$$

When your wall outlet reads "230 V" or "120 V", that is the RMS value - the peak
is about 1.41 times higher.

## When current lags voltage

In a resistor, current and voltage stay in step. But motors, transformers, and
fluorescent ballasts are **inductive**: their current **lags** the voltage by a
phase angle $\\phi$. Slide the angle and watch the current sinusoid slide:

```plot
{"title": "Voltage and a lagging current (slide the phase angle)", "xLabel": "angle (rad)", "yLabel": "instantaneous value", "xRange": [0, 6.2832], "yRange": [-1.6, 1.6], "grid": true, "controls": [{"name": "phi", "range": [0, 1.4], "value": 0.7, "label": "phase lag phi (rad)"}], "functions": [{"expr": "sin(x)", "label": "voltage", "color": "#2563eb"}, {"expr": "sin(x - phi)", "label": "current (lags)", "color": "#dc2626"}]}
```

## The three powers

That phase lag splits power into three quantities:

| Power | Symbol | Unit | Meaning |
|-------|--------|------|---------|
| Real (active) | $P$ | watt (W) | actually does work / heat |
| Reactive | $Q$ | volt-ampere reactive (var) | sloshes back and forth, no net work |
| Apparent | $S$ | volt-ampere (VA) | what the wires and transformer must carry |

$$P = V_{rms} I_{rms}\\cos\\phi, \\quad Q = V_{rms} I_{rms}\\sin\\phi, \\quad
S = V_{rms} I_{rms}.$$

The **power factor** is $\\text{pf} = \\cos\\phi = P/S$. A pf of 1.0 means all the
current does useful work; a pf of 0.7 means the wires carry 1.4x more current
than the real power needs.

## Why your utility cares

A factory full of motors at pf 0.8 draws far more current than its kilowatts
suggest, heating the cables and forcing bigger transformers. Utilities bill large
customers a **power-factor penalty** to push them toward pf near 1.

```matlab
Vpk = 325; Vrms = Vpk/sqrt(2);     % ~230 V
Irms = 10; phi = acos(0.8);        % pf = 0.8 lagging
P = Vrms*Irms*cos(phi);            % real power (W)
Q = Vrms*Irms*sin(phi);            % reactive power (var)
S = Vrms*Irms;                     % apparent power (VA)
```

```python
import numpy as np
Vpk = 325; Vrms = Vpk/np.sqrt(2)   # ~230 V
Irms = 10; phi = np.arccos(0.8)    # pf = 0.8 lagging
P = Vrms*Irms*np.cos(phi)          # real power (W)
Q = Vrms*Irms*np.sin(phi)          # reactive power (var)
S = Vrms*Irms                      # apparent power (VA)
```

**Next:** the power triangle and correcting a bad power factor.
""",
        ),
        _t(
            "The power triangle & power-factor correction",
            "11 min",
            """\
# The power triangle & power-factor correction

The three powers are not independent - they form a right triangle:

$$S^2 = P^2 + Q^2, \\qquad S = P + jQ \\;(\\text{complex power}).$$

Real power $P$ is the base, reactive power $Q$ is the height, apparent power $S$
is the hypotenuse, and the angle between $P$ and $S$ is the same $\\phi$ whose
cosine is the power factor.

```mermaid
flowchart LR
  P["real power P (W)"] --> S["apparent power S (VA)"]
  P --> Q["reactive power Q (var)"]
  Q --> S
```

Slide the power factor and watch the reactive height $Q$ grow as pf drops (with
$P$ fixed at 8 kW, $Q = P\\tan(\\arccos(\\text{pf}))$):

```plot
{"title": "Reactive power needed vs power factor (P fixed at 8 kW)", "xLabel": "power factor (cos phi)", "yLabel": "reactive power Q (kvar)", "xRange": [0.5, 1], "yRange": [0, 14], "grid": true, "functions": [{"expr": "8*tan(acos(x))", "label": "Q = P tan(phi)"}]}
```

## Correcting the power factor

An inductive load (a motor) absorbs reactive power. Put a **capacitor** in
parallel and it *supplies* reactive power locally, cancelling the motor's $Q$ so
the grid only has to deliver the real power. This is **power-factor correction**.

The capacitor's reactive support needed to move from $\\text{pf}_1$ to a better
$\\text{pf}_2$ is:

$$Q_C = P\\left(\\tan\\phi_1 - \\tan\\phi_2\\right).$$

Slide the target power factor and see how much capacitor support a 50 kW load
needs:

```plot
{"title": "Capacitor kvar to correct a 50 kW load from pf 0.75 (slide target pf)", "xLabel": "target power factor", "yLabel": "capacitor support Qc (kvar)", "xRange": [0.8, 1], "yRange": [0, 35], "grid": true, "controls": [{"name": "pf2", "range": [0.85, 0.99], "value": 0.95, "label": "target pf"}], "functions": [{"expr": "50*(tan(acos(0.75)) - tan(acos(pf2)))", "label": "Qc needed"}]}
```

## Real-world example

Big industrial sites install **capacitor banks** (rows of switched capacitors) on
their main bus. A factory running at pf 0.75 might add 25 kvar of capacitors to
reach pf 0.95, cutting line current ~20% and erasing the utility's pf penalty.
Utilities do the same on distribution feeders to free up cable and transformer
capacity.

```matlab
P = 50e3; pf1 = 0.75; pf2 = 0.95;
Qc = P*(tan(acos(pf1)) - tan(acos(pf2)));   % capacitor kvar
```

```python
import numpy as np
P = 50e3; pf1 = 0.75; pf2 = 0.95
Qc = P*(np.tan(np.arccos(pf1)) - np.tan(np.arccos(pf2)))  # capacitor var
```

> **Practical insight:** over-correcting (too much capacitance) pushes the pf
> *leading*, which can raise voltage and cause resonance with the system
> inductance. Aim for ~0.95-0.98, not exactly 1.0.

**Next:** why the grid uses three phases instead of one.
""",
        ),
        _t(
            "Three-phase systems: wye, delta & balanced power",
            "12 min",
            """\
# Three-phase systems: wye, delta & balanced power

The grid does not use one sinusoid - it uses **three**, each shifted 120 degrees:

$$v_a = V_m\\sin(\\omega t),\\;
v_b = V_m\\sin(\\omega t - 120^\\circ),\\;
v_c = V_m\\sin(\\omega t + 120^\\circ).$$

The three add up to **zero** at every instant, so a balanced three-phase load
needs no return (neutral) current - saving an entire conductor - and delivers
**constant** total power instead of the pulsing power a single phase gives.

```plot
{"title": "Balanced three-phase voltages (sum to zero)", "xLabel": "angle (deg)", "yLabel": "voltage", "xRange": [0, 360], "yRange": [-1.2, 1.2], "grid": true, "functions": [{"expr": "sin(rad(x))", "label": "phase a", "color": "#dc2626"}, {"expr": "sin(rad(x) - 2.0944)", "label": "phase b", "color": "#16a34a"}, {"expr": "sin(rad(x) + 2.0944)", "label": "phase c", "color": "#2563eb"}]}
```

## Wye (Y) and delta (D) connections

Three-phase sources and loads connect two ways:

| | Wye (star) | Delta |
|--|-----------|-------|
| Shape | three legs to a common neutral | three legs in a triangle |
| Line vs phase voltage | $V_{line} = \\sqrt{3}\\,V_{phase}$ | $V_{line} = V_{phase}$ |
| Line vs phase current | $I_{line} = I_{phase}$ | $I_{line} = \\sqrt{3}\\,I_{phase}$ |
| Neutral | available | none |

```mermaid
flowchart TB
  subgraph Wye
    NA["a"] --> NN(("neutral"))
    NB["b"] --> NN
    NC["c"] --> NN
  end
  subgraph Delta
    DA["a"] --> DB["b"] --> DC["c"] --> DA
  end
```

The factor $\\sqrt{3}\\approx 1.732$ shows up everywhere because the 120-degree
phase shift makes line-to-line quantities larger than line-to-neutral ones.

Picture the three phases as a **rotating phasor set**: three vectors 120 degrees
apart spinning together at $\\omega t$. Press Play to watch phase a rotate around
the circle - the other two stay locked 120 degrees ahead and behind it:

```plot
{"title": "Rotating phasor: phase a spinning (the others trail 120 deg apart)", "xLabel": "real", "yLabel": "imaginary", "xRange": [-1.3, 1.3], "yRange": [-1.3, 1.3], "grid": true, "animate": {"param": "t", "range": [0, 6.2832], "label": "angle wt (rad)"}, "parametric": [{"x": "cos(s)", "y": "sin(s)", "range": [0, 6.2832], "label": "unit circle", "color": "#94a3b8"}], "points": [{"xExpr": "cos(t)", "yExpr": "sin(t)", "label": "phase a", "color": "#dc2626", "size": 7, "trail": true}, {"xExpr": "cos(t - 2.0944)", "yExpr": "sin(t - 2.0944)", "label": "phase b", "color": "#16a34a", "size": 7, "trail": true}, {"xExpr": "cos(t + 2.0944)", "yExpr": "sin(t + 2.0944)", "label": "phase c", "color": "#2563eb", "size": 7, "trail": true}]}
```

## Balanced three-phase power

For a balanced load the total real power is the same regardless of connection,
and is most usefully written in **line** quantities:

$$P_{3\\phi} = \\sqrt{3}\\,V_{line} I_{line}\\cos\\phi.$$

## Real-world example

A 400 V (line) three-phase motor drawing 20 A at pf 0.85 delivers
$\\sqrt{3}\\cdot 400\\cdot 20\\cdot 0.85 \\approx 11.8$ kW. Almost all industrial
power, EV fast chargers, and data-center feeds are three-phase precisely because
three wires carry constant power efficiently.

```matlab
Vline = 400; Iline = 20; pf = 0.85;
P3 = sqrt(3)*Vline*Iline*pf;       % ~11.8 kW
Vphase_wye = Vline/sqrt(3);        % ~231 V
```

```python
import numpy as np
Vline = 400; Iline = 20; pf = 0.85
P3 = np.sqrt(3)*Vline*Iline*pf     # ~11.8 kW
Vphase_wye = Vline/np.sqrt(3)      # ~231 V
```

**Next:** taming the numbers with per-unit and phasors.
""",
        ),
        _t(
            "The per-unit system & phasors",
            "11 min",
            """\
# The per-unit system & phasors

A real grid spans 765 kV transmission down to 230 V outlets, with transformers
everywhere. Tracking volts and amps across all those levels is a bookkeeping
nightmare. Power engineers normalize everything to a **per-unit** value:

$$\\text{value in per-unit} = \\frac{\\text{actual value}}{\\text{base value}}.$$

You pick a **base power** $S_{base}$ (e.g. 100 MVA) and a **base voltage** for
each zone; the base impedance and current follow:

$$Z_{base} = \\frac{V_{base}^2}{S_{base}}, \\qquad I_{base} = \\frac{S_{base}}{\\sqrt{3}\\,V_{base}}.$$

## Why per-unit is wonderful

- A transformer's per-unit impedance is the **same** on both sides, so
  transformers practically vanish from the math (no turns-ratio juggling).
- Values cluster near 1.0, so a "0.95 pu" voltage instantly reads as "5% low".
- Equipment ratings (a generator's 0.2 pu reactance) compare directly across
  machines of wildly different sizes.

A healthy grid keeps voltages within a tight band (about 0.95-1.05 pu). Slide a
base voltage and watch the per-unit voltage of a fixed 138 kV node move:

```plot
{"title": "Per-unit voltage of a 138 kV node vs chosen base (slide base)", "xLabel": "actual voltage (kV)", "yLabel": "voltage (per-unit)", "xRange": [120, 150], "yRange": [0.85, 1.1], "grid": true, "controls": [{"name": "Vbase", "range": [132, 145], "value": 138, "label": "base voltage (kV)"}], "functions": [{"expr": "x/Vbase", "label": "V (pu)"}]}
```

## Phasors and the single-line diagram

In steady AC, a sinusoid $V_m\\cos(\\omega t + \\theta)$ is fully captured by a
**phasor** - a complex number $V\\angle\\theta$ holding magnitude and angle. Then
$\\vec{V} = \\vec{I}\\,Z$ is just complex multiplication.

Because a balanced three-phase system is symmetric, engineers draw it as a
**single-line diagram**: one line stands for all three phases, with standard
symbols for generators, transformers, buses, and loads.

```mermaid
flowchart LR
  GEN["generator"] --> T1["step-up xfmr"] --> BUS1["HV bus"]
  BUS1 --> LINE["transmission line"] --> BUS2["load bus"]
  BUS2 --> T2["step-down xfmr"] --> LOAD["load"]
```

## Real-world example

Every utility planning study - power flow, short-circuit, stability - runs in
per-unit on a single-line model. A generator rated "0.18 pu subtransient
reactance" tells a protection engineer the fault current instantly, no matter the
machine's MVA rating.

```matlab
Sbase = 100e6; Vbase = 138e3;      % 100 MVA, 138 kV
Zbase = Vbase^2/Sbase;             % base impedance (ohm)
Z_pu = (10 + 50j)/Zbase;           % a 10+j50 ohm line in per-unit
```

```python
Sbase = 100e6; Vbase = 138e3       # 100 MVA, 138 kV
Zbase = Vbase**2/Sbase             # base impedance (ohm)
Z_pu = (10 + 50j)/Zbase            # a 10+j50 ohm line in per-unit
```

**Next:** the journey from power plant to wall socket.
""",
        ),
        _t(
            "The power grid overview: generation, transmission & distribution",
            "12 min",
            """\
# The power grid overview: generation, transmission & distribution

Electricity travels a long way from where it is made to where it is used. The
grid is organized in three stages, stitched together by transformers.

```mermaid
flowchart LR
  GEN["generation 10-25 kV"] --> SU["step-up xfmr"]
  SU --> TX["transmission 110-765 kV"]
  TX --> SUB["substation step-down"]
  SUB --> DIST["distribution 4-35 kV"]
  DIST --> SD["service xfmr"]
  SD --> LOAD["customer 120-400 V"]
```

## 1. Generation

Power plants (gas, hydro, nuclear, wind, solar) spin generators producing AC at
10-25 kV. Each plant is synchronized so its phase angle and 50/60 Hz frequency
match the rest of the grid exactly.

## 2. Transmission - go high to lose less

To send power across hundreds of kilometers, the voltage is stepped **way up** to
110-765 kV. Why? Line losses are $P_{loss} = I^2 R$. For a given power
$P = VI$, raising $V$ slashes the current $I$, and the loss falls with the
**square** of that current. Slide the transmission voltage and watch losses
collapse:

```plot
{"title": "Line loss vs transmission voltage (100 MW over a fixed line)", "xLabel": "transmission voltage (kV)", "yLabel": "I^2 R loss (relative)", "xRange": [100, 765], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "Pmw", "range": [50, 200], "value": 100, "label": "power delivered (MW)"}], "functions": [{"expr": "(Pmw/100)^2 * (138/x)^2", "label": "loss (relative to 138 kV, 100 MW)"}]}
```

This is the entire reason transmission runs at such terrifying voltages.

## 3. Distribution - bring it back down

Near towns, substations step voltage down to 4-35 kV for local **distribution
feeders**, then pole/pad transformers drop it to the 120-400 V at your outlets.

## The grid as a network

The high-voltage transmission system is a **meshed** network (many loops) so
power can reroute around an outage. Distribution is usually **radial** (tree-like)
- simpler, but a fault downstream darkens everything beyond it.

## Real-world example

A wind farm at 690 V steps up to 33 kV to collect turbines, then to 275 kV to
join the transmission grid, travels 200 km, and steps down through substations to
reach homes. The 2003 Northeast blackout showed the flip side of an
interconnected grid: a local fault cascaded across eight US states and Ontario in
minutes.

```matlab
P = 100e6; R = 5;                  % 100 MW, 5 ohm line
loss_138 = (P/138e3)^2 * R;        % loss at 138 kV
loss_765 = (P/765e3)^2 * R;        % loss at 765 kV (far smaller)
```

```python
P = 100e6; R = 5                   # 100 MW, 5 ohm line
loss_138 = (P/138e3)**2 * R        # loss at 138 kV
loss_765 = (P/765e3)**2 * R        # loss at 765 kV
```

**Next:** the device that makes all this voltage-changing possible.
""",
        ),
        _t(
            "Transformers in power systems",
            "11 min",
            """\
# Transformers in power systems

The grid only works because we can change voltage almost losslessly, and the
device that does it is the **transformer**. Two coils share a magnetic core; the
**turns ratio** sets the voltage ratio:

$$\\frac{V_1}{V_2} = \\frac{N_1}{N_2} = a, \\qquad
\\frac{I_1}{I_2} = \\frac{N_2}{N_1} = \\frac{1}{a}.$$

Volts trade for amps: step the voltage **up** by $a$ and the current steps
**down** by $a$, so the power $S = VI$ is (nearly) conserved. Slide the turns
ratio:

```plot
{"title": "Transformer: secondary voltage vs turns ratio (primary 11 kV)", "xLabel": "primary voltage (kV)", "yLabel": "secondary voltage (kV)", "xRange": [1, 25], "yRange": [0, 30], "grid": true, "controls": [{"name": "a", "range": [0.2, 5], "value": 0.5, "label": "turns ratio a = N1/N2"}], "functions": [{"expr": "x/a", "label": "V2 = V1 / a"}]}
```

## Tap changers - fine voltage control

The turns ratio is not always fixed. A transformer's winding has **taps** -
extra connection points that change the effective turns by a few percent. An
**on-load tap changer** (OLTC) adjusts taps automatically while energized to hold
the downstream voltage steady as load varies through the day. Slide the tap and
watch the regulated voltage shift:

```plot
{"title": "Tap changer trims the output voltage (nominal 11 kV)", "xLabel": "tap position", "yLabel": "output voltage (kV)", "xRange": [-8, 8], "yRange": [9.5, 12.5], "grid": true, "controls": [{"name": "step", "range": [0.5, 2.5], "value": 1.25, "label": "percent per tap step"}], "functions": [{"expr": "11*(1 + step*x/100)", "label": "regulated V"}]}
```

## Three-phase connections

Three single-phase transformers (or one three-phase unit) connect as **wye-wye,
delta-delta, wye-delta, or delta-wye**. The choice matters:

- **Delta-wye** is the workhorse step-down: the wye secondary provides a neutral
  for distribution, while the delta primary traps harmonic currents.
- A delta-wye introduces a fixed **30-degree phase shift** that protection and
  paralleling schemes must account for.

```mermaid
flowchart LR
  HV["delta primary (HV)"] --> CORE["magnetic core"]
  CORE --> LV["wye secondary (LV + neutral)"]
```

## Real-world example

A distribution substation transformer might be 138 kV delta to 13.8 kV wye, 30
MVA, with an OLTC nudging taps every few minutes so neighborhood voltage stays
near 1.0 pu from quiet 3 a.m. to the evening cooking peak. Losses are tiny: large
power transformers exceed 99% efficiency, which is why high-voltage transmission
is even worth the trouble.

```matlab
N1 = 1000; N2 = 100; a = N1/N2;    % 10:1 step-down
V1 = 11e3; V2 = V1/a;              % 1100 V
I2 = 50; I1 = I2/a;                % primary current
```

```python
N1 = 1000; N2 = 100; a = N1/N2     # 10:1 step-down
V1 = 11e3; V2 = V1/a               # 1100 V
I2 = 50; I1 = I2/a                 # primary current
```

**Next:** put AC power to work - plot the power triangle and three-phase waves.
""",
        ),
        _code(
            "Lab: power triangle, PF correction & three-phase waveforms",
            "13 min",
            """\
# Visualize AC power: the power triangle, power-factor correction with a
# capacitor, and the three balanced phase voltages summing to zero.
import numpy as np
import matplotlib.pyplot as plt

# --- A load: 230 V rms, 10 A rms, pf 0.75 lagging (inductive) ---
Vrms = 230.0
Irms = 10.0
pf1 = 0.75
phi1 = np.arccos(pf1)

S = Vrms*Irms                 # apparent power (VA)
P = S*np.cos(phi1)            # real power (W)
Q1 = S*np.sin(phi1)           # reactive power (var)

# Correct to pf 0.95 with a parallel capacitor supplying reactive power.
pf2 = 0.95
phi2 = np.arccos(pf2)
Q2 = P*np.tan(phi2)           # reactive power after correction
Qc = Q1 - Q2                  # capacitor must supply this many var
S2 = np.sqrt(P**2 + Q2**2)    # new (smaller) apparent power

print(f"before: P={P:.0f} W  Q={Q1:.0f} var  S={S:.0f} VA  pf={pf1}")
print(f"capacitor supplies Qc = {Qc:.0f} var")
print(f"after:  P={P:.0f} W  Q={Q2:.0f} var  S={S2:.0f} VA  pf={pf2}")
print(f"apparent power (line loading) dropped {100*(1-S2/S):.0f}%")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

# Power triangle: before vs after correction.
ax1.plot([0, P], [0, 0], color="#16a34a", lw=3, label="P (real)")
ax1.plot([P, P], [0, Q1], color="#dc2626", lw=3, label="Q before")
ax1.plot([0, P], [0, Q1], color="#94a3b8", lw=2, ls="--", label="S before")
ax1.plot([P, P], [0, Q2], color="#2563eb", lw=3, label="Q after")
ax1.plot([0, P], [0, Q2], color="#000000", lw=2, ls=":", label="S after")
ax1.set_xlabel("real power P (W)")
ax1.set_ylabel("reactive power Q (var)")
ax1.set_title("Power triangle: PF correction")
ax1.legend(); ax1.grid(True)

# Three-phase voltages summing to zero.
deg = np.linspace(0, 360, 500)
ang = np.deg2rad(deg)
va = np.sin(ang)
vb = np.sin(ang - 2*np.pi/3)
vc = np.sin(ang + 2*np.pi/3)
ax2.plot(deg, va, color="#dc2626", label="phase a")
ax2.plot(deg, vb, color="#16a34a", label="phase b")
ax2.plot(deg, vc, color="#2563eb", label="phase c")
ax2.plot(deg, va+vb+vc, color="#000000", lw=2, ls="--", label="a+b+c (= 0)")
ax2.set_xlabel("angle (deg)")
ax2.set_ylabel("voltage (normalized)")
ax2.set_title("Balanced three-phase sums to zero")
ax2.legend(); ax2.grid(True)

plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Change pf1 to 0.6 - the capacitor must supply much more var.
#   2. Set pf2 = 1.0 - full correction makes S equal P (smallest line current).
""",
        ),
    ),
)


# -- Power Systems & the Grid -- Intermediate ----------------------------------

_POWER_INTERMEDIATE = SeedCourse(
    slug="power-systems-intermediate",
    title="Power Systems & the Grid -- Intermediate: Power Flow & Faults",
    description=(
        "Analyzing the grid under load and fault: transmission line modeling "
        "(R, L, C and ABCD parameters), the bus admittance matrix and power-flow "
        "methods (Gauss-Seidel, Newton-Raphson), fault analysis with symmetrical "
        "components, protection systems, and reactive-power/voltage control - "
        "with dual MATLAB/Python, interactive plots, and a runnable Ybus / "
        "fault-current lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Transmission line modeling: R, L, C & ABCD parameters",
            "13 min",
            """\
# Transmission line modeling: R, L, C & ABCD parameters

A transmission line is not just a wire - it has resistance $R$, series
inductance $L$, and shunt capacitance $C$ distributed along every meter. These
**line parameters** decide how voltage and current change from the sending to the
receiving end.

| Parameter | Cause | Effect |
|-----------|-------|--------|
| Series $R$ | conductor resistance | real-power loss, heating |
| Series $L$ | magnetic field around conductors | voltage drop, limits power transfer |
| Shunt $C$ | electric field between conductors/ground | charging current, voltage rise |

## Short, medium & long line models

How much detail you need depends on length (at 50/60 Hz):

- **Short** (< 80 km): ignore $C$. Just series $Z = R + j\\omega L$.
- **Medium** (80-250 km): lump the shunt $C$ into two halves at each end - the
  **nominal pi model**.
- **Long** (> 250 km): the parameters are truly distributed; use hyperbolic
  functions of the line length.

```mermaid
flowchart LR
  VS["sending end Vs"] --> Z["series R + jwL"]
  Z --> VR["receiving end Vr"]
  VS --> C1["C/2 shunt"]
  VR --> C2["C/2 shunt"]
```

## The ABCD parameters

Any two-port line is summarized by four constants relating the two ends:

$$\\begin{bmatrix} V_s \\\\ I_s \\end{bmatrix} =
\\begin{bmatrix} A & B \\\\ C & D \\end{bmatrix}
\\begin{bmatrix} V_r \\\\ I_r \\end{bmatrix}.$$

For a lossless short line, $A = D = 1$, $B = jX$, $C = 0$. The transferred
**real power** over a line of reactance $X$ between voltages $V_s$ and $V_r$ with
angle difference $\\delta$ is the famous power-transfer equation:

$$P = \\frac{V_s V_r}{X}\\sin\\delta.$$

Power flows from the **leading** to the **lagging** angle, and peaks at
$\\delta = 90^\\circ$. Slide the line reactance:

```plot
{"title": "Power transfer P = Vs Vr sin(delta) / X (slide reactance X)", "xLabel": "angle difference delta (deg)", "yLabel": "power (pu)", "xRange": [0, 180], "yRange": [0, 2.2], "grid": true, "controls": [{"name": "X", "range": [0.5, 2], "value": 1, "label": "line reactance X (pu)"}], "functions": [{"expr": "sin(rad(x))/X", "label": "P = sin(delta)/X (Vs=Vr=1)"}]}
```

## Real-world example

A 220 km, 400 kV line is modeled as a pi-section in every planning tool. Its
**surge impedance loading** (the natural power level where reactive production
and consumption balance) is a key planning number; loaded below it the line's
capacitance dominates and the receiving voltage can rise *above* the sending
voltage - the **Ferranti effect**, real on lightly loaded long lines.

```matlab
R = 0.05; L = 1e-3; C = 12e-9; len = 200; w = 2*pi*50;
Z = (R + 1j*w*L)*len;              % series impedance
Y = 1j*w*C*len;                    % shunt admittance
A = 1 + Z*Y/2; B = Z;              % nominal-pi ABCD
Cc = Y*(1 + Z*Y/4); D = A;
```

```python
import numpy as np
R, L, C, length, w = 0.05, 1e-3, 12e-9, 200, 2*np.pi*50
Z = (R + 1j*w*L)*length            # series impedance
Y = 1j*w*C*length                  # shunt admittance
A = 1 + Z*Y/2; B = Z               # nominal-pi ABCD
Cc = Y*(1 + Z*Y/4); D = A
```

**Next:** wire the lines into a network and solve the power flow.
""",
        ),
        _t(
            "Power flow analysis: Ybus, Gauss-Seidel & Newton-Raphson",
            "13 min",
            """\
# Power flow analysis: Ybus, Gauss-Seidel & Newton-Raphson

The central question of grid operation: given the loads and generation, what is
the **voltage** at every bus and the **power** in every line? This is the
**power-flow** (load-flow) problem.

## The bus admittance matrix Ybus

First we describe the network's connectivity as a matrix. With $N$ buses, $Y_{bus}$
is $N\\times N$:

- **Diagonal** $Y_{ii}$ = sum of all admittances connected to bus $i$.
- **Off-diagonal** $Y_{ij}$ = minus the admittance directly between buses $i$ and $j$.

Then nodal analysis (KCL in complex form) gives $\\vec{I} = Y_{bus}\\,\\vec{V}$,
exactly like the resistor-network nodal analysis, but complex and per-unit.

```mermaid
flowchart LR
  B1(("bus 1")) ---|y12| B2(("bus 2"))
  B2 ---|y23| B3(("bus 3"))
  B1 ---|y13| B3
```

## Why it is nonlinear

We do not actually know the currents - we know the **power** $S = P + jQ$ at each
bus, and $S = V I^*$, so the unknown voltage appears as a product with its own
conjugate. The equations are **nonlinear**, so we iterate.

## Bus types

| Bus type | Known | Unknown |
|----------|-------|---------|
| Slack (reference) | $|V|$, angle = 0 | P, Q |
| PV (generator) | P, $|V|$ | Q, angle |
| PQ (load) | P, Q | $|V|$, angle |

## Gauss-Seidel vs Newton-Raphson

- **Gauss-Seidel**: update each bus voltage from the latest values, sweep, repeat.
  Simple, but converges **slowly** (linearly) and struggles on big systems.
- **Newton-Raphson**: linearize with the **Jacobian** and take a Newton step each
  iteration. Converges **quadratically** - typically 3-5 iterations even for
  thousands of buses. It is the industry standard.

The two converge at very different rates - error per iteration:

```plot
{"title": "Convergence: error per iteration (slide the convergence rate)", "xLabel": "iteration", "yLabel": "error (log-ish)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "rate", "range": [0.3, 0.9], "value": 0.6, "label": "Gauss-Seidel reduction per step"}], "functions": [{"expr": "pow(rate, x)", "label": "Gauss-Seidel (linear)", "color": "#dc2626"}, {"expr": "pow(0.1, pow(2, x) - 1)", "label": "Newton-Raphson (quadratic)", "color": "#16a34a"}]}
```

## Real-world example

Grid operators run power flow continuously in their **EMS** (energy management
system) to check that no line is overloaded and every voltage is in band. The
same tool runs **contingency analysis** - "what if this line trips?" - on hundreds
of cases per minute to keep the grid N-1 secure.

```matlab
% Ybus for a 3-bus network from line admittances y12, y13, y23
y12=1/(0.02+0.06j); y13=1/(0.08+0.24j); y23=1/(0.06+0.18j);
Ybus = [ y12+y13, -y12,     -y13;
        -y12,      y12+y23, -y23;
        -y13,     -y23,      y13+y23 ];
```

```python
import numpy as np
y12 = 1/(0.02+0.06j); y13 = 1/(0.08+0.24j); y23 = 1/(0.06+0.18j)
Ybus = np.array([[ y12+y13, -y12,    -y13],
                 [-y12,      y12+y23, -y23],
                 [-y13,     -y23,      y13+y23]])
```

**Next:** what happens when something goes wrong - faults.
""",
        ),
        _t(
            "Fault analysis: symmetrical faults & symmetrical components",
            "12 min",
            """\
# Fault analysis: symmetrical faults & symmetrical components

A **fault** is an abnormal connection - a line touching ground, two phases
shorting - that lets enormous currents flow. Sizing breakers and setting relays
requires knowing **how big** that current will be.

## Symmetrical (three-phase) faults

The worst-case symmetrical fault shorts all three phases together. The fault
current is set by the source voltage and the **Thevenin impedance** seen at the
fault point:

$$I_{fault} = \\frac{V_{prefault}}{Z_{th}} = \\frac{1.0\\;\\text{pu}}{Z_{th}}.$$

In per-unit this is beautifully simple. A small $Z_{th}$ (a "strong" bus close to
big generators) means a **huge** fault current. Slide the impedance and watch the
fault current blow up as the bus gets stronger:

```plot
{"title": "Fault current vs Thevenin impedance (1.0 pu prefault voltage)", "xLabel": "Thevenin impedance Zth (pu)", "yLabel": "fault current (pu)", "xRange": [0.05, 0.5], "yRange": [0, 22], "grid": true, "controls": [{"name": "V", "range": [0.9, 1.1], "value": 1, "label": "prefault voltage (pu)"}], "functions": [{"expr": "V/x", "label": "I_fault = V / Zth"}]}
```

## Unsymmetrical faults & symmetrical components

Most real faults (single line-to-ground is the commonest) are **unbalanced** - the
three phases differ. The trick that tames them is **symmetrical components**:
decompose any unbalanced set of three phasors into three **balanced** sets:

- **Positive sequence** - normal balanced rotation (a, b, c).
- **Negative sequence** - balanced but reversed rotation (a, c, b).
- **Zero sequence** - all three in phase together (flows in the neutral/ground).

$$V_a = V_0 + V_1 + V_2.$$

Each sequence has its own network ($Z_0, Z_1, Z_2$); you connect them differently
for each fault type (series for line-to-ground, parallel for line-to-line), solve
the simple balanced circuit, then transform back.

```mermaid
flowchart LR
  UNBAL["unbalanced 3-phase fault"] --> DECOMP["decompose"]
  DECOMP --> POS["positive seq Z1"]
  DECOMP --> NEG["negative seq Z2"]
  DECOMP --> ZERO["zero seq Z0"]
  POS --> SOLVE["solve as balanced"]
  NEG --> SOLVE
  ZERO --> SOLVE
```

## Real-world example

Switchgear is rated by its **interrupting capacity** (e.g. "40 kA"). The
short-circuit study computes the fault current at every bus to make sure every
breaker can interrupt its worst case - and that relays see enough current to trip.
Underrate a breaker and a fault can literally explode it.

```matlab
Zth = 0.1 + 0.0j;                  % Thevenin impedance at the bus (pu)
Ifault_pu = 1.0/abs(Zth);          % 10 pu
Ibase = 100e6/(sqrt(3)*138e3);     % base current (A)
Ifault_A = Ifault_pu*Ibase;        % actual fault current
```

```python
import numpy as np
Zth = 0.1 + 0.0j                   # Thevenin impedance at the bus (pu)
Ifault_pu = 1.0/abs(Zth)           # 10 pu
Ibase = 100e6/(np.sqrt(3)*138e3)   # base current (A)
Ifault_A = Ifault_pu*Ibase         # actual fault current
```

**Next:** the devices that detect and clear those faults.
""",
        ),
        _t(
            "Protection systems: relays, breakers & coordination",
            "12 min",
            """\
# Protection systems: relays, breakers & coordination

When a fault happens, the grid must disconnect the faulted part **fast** (tens of
milliseconds) and disturb as little else as possible. That job belongs to
**protection**: relays that sense trouble and **circuit breakers** that interrupt
the current.

## The players

- **Instrument transformers** (CTs and VTs) shrink huge currents/voltages down to
  safe levels a relay can measure.
- **Protective relay** - the brain. Decides if what it sees is a fault and issues
  a trip. Modern ones are digital microprocessors running protection algorithms.
- **Circuit breaker** - the muscle. Mechanically opens to interrupt fault current
  (using oil, SF6 gas, vacuum, or air to quench the arc).

## Common relay types

| Relay | Senses | Used for |
|-------|--------|----------|
| Overcurrent (50/51) | current above a threshold | feeders, backup |
| Distance (21) | impedance (V/I) to the fault | transmission lines |
| Differential (87) | current in vs out mismatch | transformers, busbars |
| Directional | fault direction | meshed networks |

## Inverse-time overcurrent: bigger fault, faster trip

An overcurrent relay's trip time gets **shorter** as the current gets **larger** -
an inverse-time curve. This lets a small overload ride through briefly while a
dead short trips almost instantly. Slide the time dial:

```plot
{"title": "Inverse-time overcurrent relay curve (slide the time dial)", "xLabel": "fault current (multiples of pickup)", "yLabel": "trip time (s)", "xRange": [1.2, 10], "yRange": [0, 6], "grid": true, "controls": [{"name": "TD", "range": [0.1, 1], "value": 0.5, "label": "time dial setting"}], "functions": [{"expr": "TD*13.5/(x - 1)", "label": "trip time (IEC standard inverse)"}]}
```

## Coordination and protection zones

The grid is divided into overlapping **protection zones** (around each line, bus,
transformer, generator), so every point is covered and no fault goes unseen. The
relays are **coordinated**: the device nearest the fault trips first, and the
upstream device waits a **grading margin** (~0.3 s) as backup - so a single fault
takes out the smallest possible chunk.

```mermaid
flowchart LR
  SRC["source"] --> CB1["breaker 1 (slow backup)"]
  CB1 --> CB2["breaker 2 (faster)"]
  CB2 --> CB3["breaker 3 (fastest, near load)"]
  CB3 --> LOAD["load + fault"]
```

## Real-world example

On a radial feeder, a fault at the far end should trip only the nearest
downstream **recloser**, not the substation breaker - so one customer's tree-on-a-
line does not black out the whole town. Reclosers even try re-energizing a few
times to clear temporary faults (a branch that burns away) before locking out.

```matlab
TD = 0.5; M = 5;                   % time dial, current in multiples of pickup
t_trip = TD*13.5/(M - 1);          % IEC standard-inverse trip time (s)
```

```python
TD = 0.5; M = 5                    # time dial, current in multiples of pickup
t_trip = TD*13.5/(M - 1)           # IEC standard-inverse trip time (s)
```

**Next:** keeping the voltage healthy with reactive power.
""",
        ),
        _t(
            "Voltage & reactive-power control",
            "11 min",
            """\
# Voltage & reactive-power control

Frequency is a system-wide quantity, but **voltage is local** - it sags where
load is heavy and rises where it is light. Holding every bus near 1.0 pu is a
constant balancing act, and the lever is **reactive power** $Q$.

## Why reactive power moves voltage

Transmission lines are mostly **inductive**. Pushing reactive power $Q$ through a
reactance $X$ causes a voltage drop roughly $\\Delta V \\approx \\frac{QX}{V}$. So:

- A heavily loaded line **consumes** reactive power and the receiving voltage
  **sags**.
- Injecting reactive power locally **props the voltage back up**.

Slide the line reactance and watch how reactive flow drops the voltage:

```plot
{"title": "Voltage drop vs reactive power flow (slide line reactance X)", "xLabel": "reactive power Q (pu)", "yLabel": "voltage drop (pu)", "xRange": [0, 1], "yRange": [0, 0.4], "grid": true, "controls": [{"name": "X", "range": [0.1, 0.5], "value": 0.3, "label": "line reactance X (pu)"}], "functions": [{"expr": "X*x", "label": "delta V ~ Q X / V (V~1)"}]}
```

## The reactive toolkit

| Device | Supplies / absorbs Q | Notes |
|--------|----------------------|-------|
| Shunt **capacitor** bank | supplies Q (boosts V) | cheap, switched in steps |
| Shunt **reactor** | absorbs Q (lowers V) | for lightly loaded long lines |
| **Synchronous condenser** | both, smoothly | a spinning machine, adds inertia |
| Generator excitation (AVR) | both, fast | first line of defense |
| **SVC / STATCOM** (FACTS) | both, very fast | power-electronic, Advanced course |

**Shunt compensation** - parking capacitors near the load - is the everyday fix:
it supplies $Q$ right where it is needed so it does not have to travel the line.

```mermaid
flowchart LR
  GEN["generator (AVR)"] --> LINE["line: drops V under Q load"]
  LINE --> BUS(("load bus"))
  CAP["shunt capacitor"] --> BUS
  BUS --> LOAD["heavy load"]
```

## The danger: voltage collapse

If a stressed grid runs out of reactive reserve, voltage can fall in a runaway
spiral - **voltage collapse** - because lower voltage forces more current, which
drops voltage further. This was a key factor in several major blackouts, which is
why operators watch reactive margins as closely as megawatts.

## Real-world example

Utilities switch capacitor banks on as the afternoon air-conditioning load builds
and switch them off at night. Long EHV lines get **shunt reactors** at the ends to
soak up the line's own charging reactive power and stop the Ferranti voltage rise.

```matlab
X = 0.3; Q = 0.6; V = 1.0;
dV = Q*X/V;                        % approximate voltage drop (pu)
Qc = 0.4;                          % shunt capacitor support to recover V
```

```python
X = 0.3; Q = 0.6; V = 1.0
dV = Q*X/V                         # approximate voltage drop (pu)
Qc = 0.4                           # shunt capacitor support to recover V
```

**Next:** put it together - build Ybus and compute a fault current in code.
""",
        ),
        _code(
            "Lab: build Ybus & compute a three-phase fault current",
            "14 min",
            """\
# Build the bus admittance matrix Ybus for a small network, then drive a simple
# Gauss-Seidel power-flow sweep and a symmetrical fault-current calculation.
import numpy as np
import matplotlib.pyplot as plt

# --- 3-bus network, all in per-unit on a 100 MVA base ---
# Line series impedances (R + jX) between buses.
z12 = 0.02 + 0.06j
z13 = 0.08 + 0.24j
z23 = 0.06 + 0.18j
y12, y13, y23 = 1/z12, 1/z13, 1/z23

# Ybus: diagonal = sum of incident admittances, off-diag = -branch admittance.
Ybus = np.array([
    [y12 + y13, -y12,      -y13],
    [-y12,       y12 + y23, -y23],
    [-y13,      -y23,        y13 + y23],
])
print("Ybus (per-unit):")
print(np.round(Ybus, 3))

# --- Symmetrical (3-phase) fault current at each bus ---
# Zbus = inverse of Ybus; the diagonal is the Thevenin impedance at that bus.
Zbus = np.linalg.inv(Ybus)
Vpre = 1.0                            # prefault voltage (pu)
Ifault = np.array([Vpre/abs(Zbus[i, i]) for i in range(3)])

# Convert bus 1's fault to real amps on a 138 kV system.
Sbase, Vbase = 100e6, 138e3
Ibase = Sbase/(np.sqrt(3)*Vbase)
print(f"\\nThevenin |Z| at each bus: {np.round(np.abs(np.diag(Zbus)), 3)}")
print(f"fault current (pu) at each bus: {np.round(Ifault, 2)}")
print(f"bus 1 fault current: {Ifault[0]*Ibase/1000:.1f} kA")

# --- A tiny Gauss-Seidel voltage sweep (bus 1 = slack, buses 2,3 = PQ loads) ---
S = np.array([0.0, -0.5 - 0.2j, -0.6 - 0.25j])   # injected power (loads negative)
V = np.array([1.0 + 0j, 1.0 + 0j, 1.0 + 0j])
history = []
for _ in range(20):
    for i in (1, 2):
        inj = (np.conj(S[i]/V[i]) - sum(Ybus[i, k]*V[k] for k in range(3) if k != i))
        V[i] = inj/Ybus[i, i]
    history.append(abs(V[2]))

print(f"\\nfinal bus voltages (pu mag): {np.round(np.abs(V), 4)}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.bar([1, 2, 3], Ifault, color=["#dc2626", "#16a34a", "#2563eb"])
ax1.set_xlabel("bus"); ax1.set_ylabel("fault current (pu)")
ax1.set_title("Symmetrical fault current per bus"); ax1.grid(True, axis="y")

ax2.plot(range(1, len(history)+1), history, "o-", color="#2563eb")
ax2.set_xlabel("Gauss-Seidel iteration"); ax2.set_ylabel("|V3| (pu)")
ax2.set_title("Power-flow voltage converging"); ax2.grid(True)

plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Halve z12 (a stronger tie): bus fault currents rise.
#   2. Increase the load at bus 3: its converged voltage sags further.
""",
        ),
    ),
)


# -- Power Systems & the Grid -- Advanced --------------------------------------

_POWER_ADVANCED = SeedCourse(
    slug="power-systems-advanced",
    title="Power Systems & the Grid -- Advanced: Stability, Renewables & Smart Grid",
    description=(
        "The dynamic and modern grid: rotor-angle stability (the swing equation "
        "and equal-area criterion), frequency and load-frequency control "
        "(governor droop, AGC), renewable integration (grid-tied inverters, the "
        "duck curve, grid codes), HVDC and FACTS, and the smart grid (metering, "
        "demand response, microgrids, resiliency) - with dual MATLAB/Python, "
        "interactive plots, a runnable swing-equation/droop lab, and a closing "
        "applications lesson."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Power system stability & the swing equation",
            "13 min",
            """\
# Power system stability & the swing equation

A grid generator is a spinning mass locked in step with the whole system at
50/60 Hz. **Stability** asks: after a disturbance (a fault, a sudden load change),
do the generators **stay in synchronism** or do they slip apart?

## The swing equation

A generator's rotor angle $\\delta$ (its electrical position relative to the
system reference) obeys Newton's law for rotation - the **swing equation**:

$$\\frac{2H}{\\omega_s}\\frac{d^2\\delta}{dt^2} = P_m - P_e
= P_m - \\frac{V_s V_r}{X}\\sin\\delta.$$

Here $H$ is the **inertia constant** (stored kinetic energy per MVA), $P_m$ is the
mechanical input power, and $P_e$ is the electrical output power. When $P_m \\neq
P_e$, the rotor **accelerates or decelerates** - it "swings".

The electrical power follows the same $\\sin\\delta$ curve from line modeling, and
the steady operating point is where $P_m$ crosses it:

```plot
{"title": "Power-angle curve: operating point where Pm meets Pe (slide Pm)", "xLabel": "rotor angle delta (deg)", "yLabel": "power (pu)", "xRange": [0, 180], "yRange": [0, 2.2], "grid": true, "controls": [{"name": "Pm", "range": [0.2, 1.8], "value": 0.8, "label": "mechanical power Pm (pu)"}], "functions": [{"expr": "2*sin(rad(x))", "label": "Pe = Pmax sin(delta)"}, {"expr": "Pm", "label": "Pm (input)", "color": "#dc2626"}]}
```

## Transient vs rotor-angle stability

- **Small-signal (rotor-angle) stability** - does the rotor settle (damped
  oscillation) after a tiny nudge? Poorly damped systems show growing inter-area
  oscillations.
- **Transient stability** - does the machine survive a **large** disturbance like
  a fault followed by a line trip? This is where the swing equation is integrated
  numerically.

## Real-world example

When a major line trips, generators swing against each other for a few seconds.
If protection clears the fault fast enough, they settle; if not, machines lose
synchronism and **out-of-step protection** islands them to save the rest. As the
grid adds inverter-based renewables (which have **no spinning inertia**), the
total system $H$ falls and frequency moves faster after a disturbance - a leading
concern for modern grid operators.

```matlab
H = 4; ws = 2*pi*50; Pmax = 2.0; Pm = 0.8;
delta0 = asin(Pm/Pmax);            % steady operating angle (rad)
accel = (ws/(2*H))*(Pm - Pmax*sin(delta0));   % ~0 at equilibrium
```

```python
import numpy as np
H, ws, Pmax, Pm = 4, 2*np.pi*50, 2.0, 0.8
delta0 = np.arcsin(Pm/Pmax)        # steady operating angle (rad)
accel = (ws/(2*H))*(Pm - Pmax*np.sin(delta0))  # ~0 at equilibrium
```

**Next:** the graphical stability test - the equal-area criterion.
""",
        ),
        _t(
            "The equal-area criterion",
            "12 min",
            """\
# The equal-area criterion

For a single machine against an infinite bus, you can judge transient stability
**without** solving the swing equation - just by comparing **areas** under the
power-angle curve. This is the **equal-area criterion**, one of the most elegant
results in power engineering.

## The idea

When a fault drops the electrical power $P_e$ below the mechanical input $P_m$,
the rotor **accelerates** and $\\delta$ grows - storing kinetic energy
(the **accelerating area** $A_1$). After the fault clears, $P_e$ exceeds $P_m$,
the rotor **decelerates** and gives that energy back (the **decelerating area**
$A_2$).

$$\\text{stable if } A_2 \\geq A_1
\\;\\;\\Longleftrightarrow\\;\\;
\\int_{\\delta_0}^{\\delta_c}(P_m - P_e)\\,d\\delta
= \\int_{\\delta_c}^{\\delta_{max}}(P_e - P_m)\\,d\\delta.$$

If the decelerating area can match the accelerating area before the rotor angle
runs past the point of no return, the machine stays in step.

```plot
{"title": "Equal-area: accelerating area must be repaid by decelerating area", "xLabel": "rotor angle delta (deg)", "yLabel": "power (pu)", "xRange": [0, 180], "yRange": [0, 2.2], "grid": true, "controls": [{"name": "Pm", "range": [0.4, 1.5], "value": 1, "label": "mechanical power Pm (pu)"}], "functions": [{"expr": "2*sin(rad(x))", "label": "Pe (post-fault)", "color": "#16a34a"}, {"expr": "Pm", "label": "Pm (input)", "color": "#dc2626"}]}
```

## The critical clearing angle and time

There is a maximum angle - the **critical clearing angle** $\\delta_{cr}$ - at which
the breaker must clear the fault. Clear before the rotor reaches it and $A_2$ can
still equal $A_1$; clear later and the machine accelerates past recovery and loses
synchronism. The corresponding **critical clearing time** is the hard deadline for
protection.

```mermaid
stateDiagram-v2
  [*] --> Steady
  Steady --> Accelerating: fault, Pe drops below Pm (area A1 builds)
  Accelerating --> Decelerating: breaker clears fault
  Decelerating --> Steady: A2 >= A1, machine recovers
  Decelerating --> LostSync: A2 < A1, rotor runs away
  LostSync --> [*]
```

## Real-world example

Critical clearing time is **why transmission breakers clear faults in 3-5 cycles**
(50-80 ms). It directly sets relay and breaker speed requirements and drives
investment in faster protection. Planners run thousands of equal-area / time-
domain cases to certify that the grid survives any single fault with margin.

```matlab
Pmax = 2.0; Pm = 1.0;
d0 = asin(Pm/Pmax);                % initial angle
dmax = pi - d0;                    % unstable equilibrium angle
% critical clearing angle (fault drops Pe to zero):
dcr = acos((Pm/Pmax)*(dmax - d0) + cos(dmax));
```

```python
import numpy as np
Pmax, Pm = 2.0, 1.0
d0 = np.arcsin(Pm/Pmax)            # initial angle
dmax = np.pi - d0                  # unstable equilibrium angle
dcr = np.arccos((Pm/Pmax)*(dmax - d0) + np.cos(dmax))  # critical clearing angle
```

**Next:** the system-wide quantity everyone shares - frequency.
""",
        ),
        _t(
            "Frequency & load-frequency control",
            "12 min",
            """\
# Frequency & load-frequency control

Grid **frequency** (50 or 60 Hz) is the heartbeat shared by every connected
machine. It is a direct readout of the **power balance**:

- Generation **exceeds** load -> machines speed up -> frequency **rises**.
- Load **exceeds** generation -> machines slow down -> frequency **falls**.

Because the whole synchronous grid shares one frequency, it is the perfect global
signal for balancing supply and demand second-by-second.

## Governor droop - the fast, automatic response

Each generator's **governor** adjusts mechanical power in response to frequency,
with a deliberate **droop**: a falling frequency commands more power along a
straight line. Droop $R$ is the percent frequency change for 100% power change:

$$\\Delta P = -\\frac{1}{R}\\,\\Delta f.$$

Droop lets many generators **share** a load change in proportion to their size
without fighting each other. Slide the droop and watch the line tilt:

```plot
{"title": "Governor droop: power vs frequency deviation (slide droop R)", "xLabel": "frequency deviation (percent)", "yLabel": "generator output (pu)", "xRange": [-2, 2], "yRange": [0, 2], "grid": true, "controls": [{"name": "R", "range": [2, 8], "value": 5, "label": "droop R (percent)"}], "functions": [{"expr": "1 - x/R", "label": "P = P0 - (1/R) df"}]}
```

A 5% droop means a 5% frequency drop would call for 100% more output. Smaller
droop = stiffer response.

## The two control layers

| Layer | Speed | Job |
|-------|-------|-----|
| Primary (governor droop) | seconds | arrest the frequency drop, share load |
| Secondary (**AGC**) | minutes | restore frequency to exactly 50/60 Hz, return interchange to schedule |

**AGC** (automatic generation control) sends signals to chosen generators every
few seconds to nudge the frequency back to nominal and keep each region exporting
its scheduled power (via the **area control error**).

```mermaid
flowchart LR
  LOAD["load change"] --> FREQ["frequency deviates"]
  FREQ --> GOV["governors (droop): fast, partial"]
  GOV --> AGC["AGC: slow, restores 50/60 Hz"]
  AGC --> GEN["generation setpoints"]
  GEN --> FREQ
```

## Real-world example

When a 1 GW generator trips, frequency dips within seconds; governors across the
grid pick up the slack (arresting the dip), then AGC ramps reserves to restore
nominal frequency over minutes. Operators hold **spinning reserve** for exactly
this. Grids enforce frequency tightly (e.g. 49.8-50.2 Hz); breach the limits and
**under-frequency load shedding** sheds load automatically to save the system.

```matlab
R = 0.05; df = -0.01;              % 5% droop, 1% (0.5 Hz) frequency dip
dP = -(1/R)*df;                    % each unit picks up 0.2 pu more
```

```python
R = 0.05; df = -0.01               # 5% droop, 1% frequency dip
dP = -(1/R)*df                     # each unit picks up 0.2 pu more
```

**Next:** the renewables reshaping all of this.
""",
        ),
        _t(
            "Renewable integration: inverters, the duck curve & grid codes",
            "12 min",
            """\
# Renewable integration: inverters, the duck curve & grid codes

Solar and wind are transforming the grid, but they behave very differently from a
spinning turbine - which creates new engineering challenges.

## Grid-tied inverters

Solar panels and battery storage produce **DC**; wind turbines produce variable-
frequency AC. A power-electronic **inverter** converts to grid-synchronized AC,
matching frequency and phase precisely. Unlike a generator, an inverter has
**no rotating mass**, so it provides **no natural inertia** - the grid's shock
absorber - unless programmed to mimic it (**grid-forming** / synthetic inertia).

## Intermittency

Renewable output swings with weather and time of day. A passing cloud can drop a
solar farm's output sharply in seconds; wind ramps over hours. The grid must hold
fast-responding reserves (batteries, gas peakers, hydro) to fill the gaps.

## The duck curve

As rooftop solar grows, midday **net load** (demand minus solar) plunges, then
soars at sunset as solar fades and people come home - a curve shaped like a duck.
Slide the solar penetration and watch the belly deepen and the evening ramp
steepen:

```plot
{"title": "The duck curve: net load = demand - solar (slide solar level)", "xLabel": "hour of day", "yLabel": "net load (GW)", "xRange": [0, 24], "yRange": [0, 30], "grid": true, "controls": [{"name": "solar", "range": [0, 18], "value": 10, "label": "peak solar (GW)"}], "functions": [{"expr": "18 + 7*sin(rad((x-9)*15)) - solar*max(0, sin(rad((x-6)*15)))", "label": "net load"}]}
```

The steep evening **ramp** stresses dispatchable generation, and midday surplus can
force solar **curtailment** or even negative prices.

## Grid codes

To keep the system stable as inverters multiply, **grid codes** require renewable
plants to behave like good grid citizens:

- **Fault ride-through** - stay connected through brief voltage dips (don't all
  trip at once and crash frequency).
- **Frequency/voltage support** - curtail on over-frequency, supply reactive power.
- **Ramp-rate limits** and forecasting obligations.

```mermaid
flowchart LR
  PV["solar DC"] --> INV["grid-tied inverter"]
  WIND["wind variable AC"] --> CONV["AC-DC-AC converter"]
  INV --> GRID["synchronized AC grid"]
  CONV --> GRID
  BATT["battery"] --> INV
```

## Real-world example

California's grid operator publishes the duck curve to justify massive **battery
storage** that soaks up midday solar and discharges into the evening ramp. Modern
solar/wind plants must pass grid-code fault-ride-through tests before connection,
and **grid-forming** batteries are being deployed to restore the inertia that
retiring coal and gas plants used to provide.

```matlab
hour = 0:0.5:24; demand = 18 + 7*sin((hour-9)*15*pi/180);
solar = 10*max(0, sin((hour-6)*15*pi/180));
net_load = demand - solar;         % the duck
```

```python
import numpy as np
hour = np.arange(0, 24, 0.5)
demand = 18 + 7*np.sin((hour-9)*15*np.pi/180)
solar = 10*np.maximum(0, np.sin((hour-6)*15*np.pi/180))
net_load = demand - solar          # the duck
```

**Next:** moving bulk power with electronics - HVDC and FACTS.
""",
        ),
        _t(
            "HVDC & FACTS: power-electronic grid control",
            "12 min",
            """\
# HVDC & FACTS: power-electronic grid control

High-power semiconductors let us control the grid in ways spinning machines never
could. Two families dominate: **HVDC** for moving bulk power, and **FACTS** for
controlling AC flow.

## HVDC: high-voltage DC transmission

Convert AC to DC at one end, send it as DC, convert back at the other. Why bother?

- **No charging current** over long distances - the killer for long **undersea
  cables** (AC cable capacitance would consume all the capacity).
- **Lower losses** over very long overhead lines (break-even ~600-800 km).
- **Asynchronous tie** - link two grids running at different frequencies or out of
  phase (e.g. 50 Hz to 60 Hz), which AC simply cannot do.
- **Fully controllable power** - you command the exact MW, instantly.

Below the break-even distance AC wins (converter stations are expensive); above
it, DC's lower per-km loss pays off. Slide the converter cost and watch the
break-even distance move:

```plot
{"title": "HVDC vs AC total cost vs distance (slide converter cost)", "xLabel": "line distance (km)", "yLabel": "relative total cost", "xRange": [0, 1500], "yRange": [0, 4], "grid": true, "controls": [{"name": "conv", "range": [0.5, 2], "value": 1, "label": "HVDC converter cost"}], "functions": [{"expr": "0.5 + 0.0022*x", "label": "AC cost", "color": "#dc2626"}, {"expr": "conv + 0.0009*x", "label": "HVDC cost", "color": "#16a34a"}]}
```

## FACTS: flexible AC transmission systems

FACTS devices inject controllable reactive power or voltage into an AC line to
steer flow and stabilize voltage - far faster than mechanical switches:

| Device | Acts like | Controls |
|--------|-----------|----------|
| **SVC** | switched reactor/capacitor | bus voltage (var) |
| **STATCOM** | controllable current source | voltage, very fast, works at low V |
| **TCSC** | variable series capacitor | line impedance -> power flow |
| **UPFC** | combined series+shunt | voltage, angle, and flow together |

By electronically adjusting reactance, voltage, or angle, FACTS push power onto
under-used lines and damp oscillations - getting more out of existing corridors
without building new lines.

```mermaid
flowchart LR
  GRIDA["AC grid A"] --> RECT["AC to DC converter"]
  RECT --> DC["HVDC link"]
  DC --> INV["DC to AC converter"]
  INV --> GRIDB["AC grid B (any frequency)"]
```

## Real-world example

China's longest **UHVDC** lines carry many gigawatts over 2000+ km from inland
hydro and wind to coastal cities. Europe's offshore wind comes ashore via HVDC
cables. STATCOMs stabilize voltage at weak grid points and at large wind farms to
meet grid codes. **Back-to-back HVDC** ties stitch together the otherwise
asynchronous interconnections of North America.

```matlab
ac = 0.5 + 0.0022*1200;            % AC cost at 1200 km
hvdc = 1.0 + 0.0009*1200;          % HVDC cost at 1200 km (cheaper long-haul)
```

```python
ac = 0.5 + 0.0022*1200             # AC cost at 1200 km
hvdc = 1.0 + 0.0009*1200           # HVDC cost at 1200 km
```

**Next:** the digital, distributed grid of the future.
""",
        ),
        _t(
            "The smart grid: metering, demand response & microgrids",
            "11 min",
            """\
# The smart grid: metering, demand response & microgrids

The traditional grid pushes power one way, from big plants to passive consumers.
The **smart grid** adds sensing, communication, and control everywhere - turning
the grid into a two-way, responsive, self-healing network.

## Metering and sensing

**Smart meters** (AMI - advanced metering infrastructure) report consumption in
near real time instead of once a month, enabling time-of-use pricing and instant
outage detection. On the transmission side, **PMUs** (phasor measurement units)
sample voltage/current phasors GPS-synchronized 30-60 times a second, giving
operators a live, wide-area picture (a **WAMS**) to catch instabilities early.

## Demand response

Instead of only matching generation to demand, the smart grid also flexes
**demand** to match supply. Utilities signal price or curtailment, and smart
thermostats, water heaters, EV chargers, and industrial loads shift consumption
to cheap/abundant hours. Slide the demand-response participation and watch the
evening peak shave down:

```plot
{"title": "Demand response shaves and shifts the evening peak (slide DR level)", "xLabel": "hour of day", "yLabel": "load (GW)", "xRange": [0, 24], "yRange": [0, 30], "grid": true, "controls": [{"name": "dr", "range": [0, 6], "value": 3, "label": "demand-response shift (GW)"}], "functions": [{"expr": "18 + 8*exp(-((x-19)^2)/6) - dr*exp(-((x-19)^2)/6) + dr*0.5*exp(-((x-3)^2)/8)", "label": "shaped load"}]}
```

## Microgrids and resiliency

A **microgrid** is a local cluster of generation, storage, and load that can run
connected to the main grid **or** disconnect and run as an **island** during an
outage. Hospitals, military bases, and campuses use them to stay powered through
blackouts. Combined with distributed solar, batteries, and EVs (which can feed
back via **vehicle-to-grid**), the grid becomes a resilient web of many small
sources rather than a few big ones.

```mermaid
stateDiagram-v2
  [*] --> GridConnected
  GridConnected --> Islanded: main grid fault detected
  Islanded --> GridConnected: grid restored, resynchronize
  Islanded --> [*]: orderly shutdown if reserves exhausted
```

## Cyber-resiliency

A communicating grid is a hackable grid. Smart-grid security (encryption,
segmentation, anomaly detection) is now core to reliability - the 2015 Ukraine
grid cyberattack switched off substations remotely and is the textbook warning.

## Real-world example

During wildfire shutoffs and storms, **microgrids** keep critical facilities lit
while the main grid is down. Utilities run **demand-response** programs that pay
customers to curtail during peaks, deferring billions in new plant construction.
PMU-based **WAMS** let operators see inter-area oscillations live and act before
they grow into a blackout.

```matlab
peak_no_dr = 18 + 8;               % evening peak without DR (GW)
dr = 3; peak_with_dr = peak_no_dr - dr;   % peak shaved by demand response
```

```python
peak_no_dr = 18 + 8                # evening peak without DR (GW)
dr = 3; peak_with_dr = peak_no_dr - dr    # peak shaved by demand response
```

**Next:** simulate the swing equation and droop control yourself.
""",
        ),
        _code(
            "Lab: swing equation, equal-area & governor droop",
            "14 min",
            """\
# Simulate a single machine's transient response with the swing equation and an
# equal-area view, plus the steady-state load sharing of governor droop.
import numpy as np
import matplotlib.pyplot as plt

# --- Machine and system (per-unit) ---
H = 4.0                 # inertia constant (s)
ws = 2*np.pi*60         # synchronous speed (rad/s), 60 Hz
Pmax = 2.0              # peak electrical power Pe = Pmax sin(delta)
Pm = 1.0                # mechanical input power
D = 0.0                 # (no extra damping in this simple run)

delta0 = np.arcsin(Pm/Pmax)        # steady rotor angle (rad)

# Integrate the swing equation through a fault: Pe collapses for the fault
# window, then recovers. Watch the rotor angle swing and (here) settle.
dt = 0.001
t = np.arange(0, 3.0, dt)
delta = delta0
omega = 0.0                        # speed deviation (rad/s)
fault_on, fault_off = 0.1, 0.25    # fault clears after 150 ms
DELTA = np.zeros_like(t)
for k in range(len(t)):
    Pe = 0.0 if (fault_on <= t[k] < fault_off) else Pmax*np.sin(delta)
    domega = (ws/(2*H))*(Pm - Pe - D*omega)
    omega += domega*dt
    delta += omega*dt
    DELTA[k] = delta

# Critical clearing angle from the equal-area criterion (fault Pe = 0).
dmax = np.pi - delta0
dcr = np.arccos((Pm/Pmax)*(dmax - delta0) + np.cos(dmax))
print(f"steady angle delta0 = {np.degrees(delta0):.1f} deg")
print(f"critical clearing angle = {np.degrees(dcr):.1f} deg")
print(f"max swing reached = {np.degrees(DELTA.max()):.1f} deg")

# --- Governor droop: two units sharing a load increase ---
R1, R2 = 0.05, 0.04                # 5% and 4% droop
dload = 0.3                        # 0.3 pu extra load (pu)
df = -dload/(1/R1 + 1/R2)          # common frequency deviation
dP1, dP2 = -df/R1, -df/R2          # each unit's pickup
print(f"\\nfrequency deviation = {df*100:.3f} %  ->  unit1 +{dP1:.3f} pu, unit2 +{dP2:.3f} pu")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

ax1.plot(t, np.degrees(DELTA), color="#2563eb")
ax1.axhline(np.degrees(dcr), ls="--", color="#dc2626", label="critical clearing angle")
ax1.set_xlabel("time (s)"); ax1.set_ylabel("rotor angle (deg)")
ax1.set_title("Swing equation: rotor angle after a fault")
ax1.legend(); ax1.grid(True)

d = np.linspace(0, np.pi, 300)
ax2.plot(np.degrees(d), Pmax*np.sin(d), color="#16a34a", label="Pe = Pmax sin(delta)")
ax2.axhline(Pm, color="#dc2626", label="Pm (input)")
ax2.fill_between(np.degrees(d), Pm, Pmax*np.sin(d),
                 where=(d > delta0) & (d < dcr), alpha=0.3, color="#16a34a")
ax2.set_xlabel("rotor angle (deg)"); ax2.set_ylabel("power (pu)")
ax2.set_title("Equal-area criterion"); ax2.legend(); ax2.grid(True)

plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Push fault_off to 0.4 s: the rotor swings past recovery (unstable).
#   2. Add damping D = 2: oscillations decay faster.
""",
        ),
        _t(
            "Applications, use cases & the throughline",
            "11 min",
            """\
# Applications, use cases & the throughline

Everything in this track shows up the moment you trace electricity from a power
plant to a phone charger. Here is where it all lands in the real world.

## Where each idea earns its keep

| Concept | Real-world application |
|---------|------------------------|
| Power factor & PF correction | factory capacitor banks, utility pf penalties, cutting line current |
| Three-phase | all industrial power, EV fast charging, data-center feeds |
| Per-unit & single-line | every planning, short-circuit, and stability study |
| Transmission at high voltage | 765 kV lines moving GW across continents with low loss |
| Transformers & tap changers | substations holding neighborhood voltage near 1.0 pu all day |
| Ybus & power flow | real-time EMS, contingency (N-1) analysis, market dispatch |
| Fault analysis | sizing breakers (e.g. 40 kA), setting relays, short-circuit studies |
| Protection & coordination | reclosers isolating a fault to one feeder, not a whole town |
| Reactive control | capacitor banks, SVC/STATCOM, avoiding voltage collapse |
| Swing equation & equal-area | why breakers must clear in 3-5 cycles; transient-stability studies |
| Load-frequency control | governor droop + AGC holding 50/60 Hz after a generator trips |
| Renewables & the duck curve | battery storage, curtailment, grid-code ride-through tests |
| HVDC & FACTS | undersea/long-haul links, asynchronous grid ties, flow control |
| Smart grid | smart meters, demand response, microgrids, PMU wide-area monitoring |

## A worked thread: surviving a generator trip

1. A 1 GW unit trips. **Power balance** breaks; **frequency** falls.
2. **Governor droop** on every machine picks up the deficit within seconds,
   arresting the dip; **AGC** restores exactly 60 Hz over minutes.
3. Meanwhile a line elsewhere overloads. **Power-flow / contingency** tools (run
   on **Ybus**) flag it; operators reroute, helped by **FACTS** flow control.
4. A fault on that line draws a huge current set by the bus **Thevenin
   impedance**; **protection** clears it in a few cycles - fast enough by the
   **equal-area** critical clearing time - so generators stay in **synchronism**.
5. Reactive reserves (capacitors, **STATCOMs**) hold voltage to avert **collapse**.
6. Smart **demand response** and **batteries** smooth the recovery; a **microgrid**
   campus that islanded reconnects once the grid is healthy.

```mermaid
flowchart LR
  TRIP["generator trips"] --> FREQ["frequency falls"]
  FREQ --> DROOP["droop + AGC restore Hz"]
  TRIP --> FLOW["power flow / contingency reroutes"]
  FLOW --> PROT["protection clears any fault fast"]
  PROT --> STAB["machines stay in synchronism"]
  STAB --> VOLT["reactive reserves hold voltage"]
  VOLT --> DR["DR + storage + microgrids recover"]
```

## The grand challenge: decarbonization

The grid is being rebuilt around **inverter-based** renewables. That means
falling **inertia** (faster frequency swings), the **duck curve** (steep ramps and
midday surplus), massive **storage**, **HVDC** to move remote wind/solar, and a
**smart**, communicating, resilient grid to coordinate millions of small devices.
Every classical concept here still applies - it is just being stretched and
re-engineered for a renewable, digital grid.

## The throughline

Generate AC, transform it up to move it efficiently, transform it down to use it,
keep **real and reactive power** balanced so **frequency and voltage** stay in
band, protect it from faults fast enough to stay **stable**, and now sense and
control all of it digitally. The hardware spans from a spinning turbine to a
silicon inverter; the laws - power balance, Kirchhoff, the swing equation - never
change. That is the power grid, end to end.

**Next:** the final check.
""",
        ),
    ),
)


POWER_SYSTEMS_COURSES: tuple[SeedCourse, ...] = (
    _POWER_BASICS,
    _POWER_INTERMEDIATE,
    _POWER_ADVANCED,
)

__all__ = ["POWER_SYSTEMS_COURSES"]
