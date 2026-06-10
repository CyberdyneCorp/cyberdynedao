"""Curated Power Electronics track: Basics, Intermediate, Advanced.

The efficient conversion and control of electrical energy with switches:
switching devices and PWM, rectifiers, the buck/boost/buck-boost DC-DC
converters and their design and control, then isolated converters, resonant
(soft-switching) topologies, inverters and motor drives, wide-bandgap devices,
thermal/EMI, and applications. Dual MATLAB + Python, runnable Python converter
simulations, interactive ```plot blocks, Mermaid topology/control diagrams,
LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/power_electronics_*.py) at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ── Power Electronics — Basics ────────────────────────────────────────────────

_POWER_BASICS = SeedCourse(
    slug="power-electronics-basics",
    title="Power Electronics — Basics",
    description=(
        "Convert and control electrical energy efficiently with switches: why "
        "switching beats linear, the power devices (MOSFET, IGBT, thyristor), "
        "PWM, rectifiers, and the buck converter - with dual MATLAB/Python, "
        "interactive plots, and a runnable PWM lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is power electronics? A short history",
            "10 min",
            """\
# What is power electronics? A short history

**Power electronics** is the art of converting and controlling electrical energy
**efficiently** - using semiconductor **switches** rather than resistive
elements that waste energy as heat. It sits between the power source and the
load in almost everything: phone chargers, laptops, EVs, solar inverters, data
centers, and the grid itself.

## The four conversions

```mermaid
flowchart LR
  ACDC["AC -> DC (rectifier)"]
  DCDC["DC -> DC (converter)"]
  DCAC["DC -> AC (inverter)"]
  ACAC["AC -> AC (cycloconverter / matrix)"]
```

A laptop charger is **AC->DC** then **DC->DC**; a solar system is **DC->AC**; a
variable-speed motor drive is **AC->DC->AC**.

## Why switching, not linear

A linear regulator drops voltage across a transistor as **heat**: dropping 12 V
to 5 V at 2 A wastes 14 W. A switching converter instead toggles a switch fully
**on** (low voltage across it) or fully **off** (no current through it) - both
low-loss states - and uses an inductor and capacitor to deliver a smooth output.
Efficiencies of **90-98%** are routine. Compare:

```plot
{"title": "Efficiency vs output voltage (from a 12 V input)", "xLabel": "output voltage (V)", "yLabel": "efficiency", "xRange": [1, 11], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "x/12", "label": "linear regulator (Vout/Vin)", "color": "#dc2626"}, {"expr": "0.93", "label": "switching converter (~flat)", "color": "#16a34a"}]}
```

The linear regulator's efficiency *is* the voltage ratio; the switcher stays
high regardless. That gap is the whole reason power electronics exists.

## A short history

- **1900s-1940s - mercury-arc valves** rectify high power for railways and
  industry: big, fragile glass tubes.
- **1947 - the transistor**, then **1957 - the thyristor (SCR)** from GE: the
  first solid-state controllable power switch, ruling high-power AC control for
  decades.
- **1970s - the power MOSFET**: fast, voltage-controlled, easy to drive - it made
  high-frequency switching converters practical.
- **1980s - the IGBT** marries MOSFET drive with bipolar current handling for
  medium/high power (motor drives, EVs).
- **2010s - wide-bandgap (SiC, GaN)**: higher frequency, efficiency, and
  temperature - shrinking chargers and boosting EV range (Advanced course).

> **The throughline of the whole field:** switch fast between fully-on and
> fully-off, filter the result with L and C, and control the **duty cycle** to
> set the output - while managing the heat. Everything else is detail.

**Next:** the switches themselves.
""",
        ),
        _t(
            "The ideal switch & real power devices",
            "11 min",
            """\
# The ideal switch & real power devices

Power electronics begins with the **ideal switch**: zero voltage drop when on,
zero current when off, and instantaneous switching - so **zero loss**. Real
devices approximate it, and the gap is where losses (and engineering) live.

## The device family

| Device | Controlled by | Speed | Sweet spot |
|--------|---------------|-------|------------|
| **Diode** | uncontrolled (passive) | fast | rectifiers, freewheeling |
| **MOSFET** | gate **voltage** | very fast | low-medium voltage, high frequency |
| **IGBT** | gate **voltage** | medium | high voltage/current (motor drives, EV) |
| **Thyristor / SCR** | gate **pulse** (latches on) | slow | very high power AC (grid, rail) |
| **GaN / SiC** | gate voltage | fastest | high efficiency, high frequency |

```mermaid
flowchart LR
  LOWV["low V, high f"] --> GAN["GaN / Si MOSFET"]
  MIDV["high V & I"] --> IGBT["IGBT"]
  HIGHV["very high power AC"] --> SCR["thyristor / SCR"]
```

## Two kinds of loss

- **Conduction loss** - the device isn't a perfect short when on: a MOSFET has
  $R_{DS(on)}$ (loss $= I^2 R_{DS(on)}$), an IGBT/diode a forward voltage
  $V_{CE(sat)}$/$V_F$ (loss $= V \\cdot I$).
- **Switching loss** - during the brief on/off transition, voltage and current
  overlap, dissipating energy **each switching cycle**, so it grows with
  switching frequency $f_{sw}$.

Pushing $f_{sw}$ up shrinks the inductor and capacitor (good) but raises
switching loss (bad) - the central trade-off, and exactly what wide-bandgap
devices improve.

## Safe operating area & gate drive

A device must stay within its **Safe Operating Area** (voltage, current,
temperature, time) or it fails. And a switch is only as good as its **gate
driver** - the circuit that charges/discharges the gate fast enough to switch
cleanly. Slow gate drive = long transitions = switching loss and heat.

> **Practical insight:** match the device to the job - MOSFET/GaN for
> low-voltage high-frequency (chargers, point-of-load), IGBT for
> high-power/medium-frequency (EV traction, industrial drives), thyristors for
> the very highest power AC. Always design the gate drive deliberately.

**Next:** the control knob of every converter - PWM.
""",
        ),
        _t(
            "PWM: controlling power by switching",
            "11 min",
            """\
# PWM: controlling power by switching

You can't easily make a switch "half on" without wasting power - so instead you
turn it fully on and off rapidly and vary the **fraction of time it's on**. That
fraction is the **duty cycle** $D$, and the technique is **pulse-width
modulation (PWM)**.

The **average** of a PWM signal switching between 0 and $V_{in}$ is simply

$$V_{avg} = D\\,V_{in}, \\qquad D = \\frac{t_{on}}{t_{on} + t_{off}} \\in [0, 1].$$

Slide the duty cycle and watch the pulse train and its average:

```plot
{"title": "PWM (Vin=12 V): output toggles, its average = D x Vin (slide D)", "xLabel": "time", "yLabel": "voltage (V)", "xRange": [0, 2], "yRange": [-1, 13], "grid": true, "controls": [{"name": "D", "range": [0.1, 0.9], "value": 0.35, "label": "duty cycle D"}], "functions": [{"expr": "(mod(x*5, 1) < D)*12", "label": "PWM output"}, {"expr": "D*12", "label": "average = D x 12", "color": "#dc2626"}]}
```

## Recovering the average: the LC filter

A **low-pass LC filter** after the switch passes the DC average and blocks the
switching ripple - so the load sees a smooth voltage near $D\\,V_{in}$, with
almost no loss (an inductor and capacitor store energy rather than burning it).
That switch + LC filter **is** the buck converter (two lessons from now).

The **switching frequency** $f_{sw}$ sets how small the filter can be: higher
$f_{sw}$ = smaller L and C, but more switching loss.

```matlab
Vin = 12; D = 0.35;
Vavg = D*Vin;                 % 4.2 V
fsw = 100e3; Tsw = 1/fsw;     % 10 us period
ton = D*Tsw;                  % on-time
```

```python
Vin, D = 12, 0.35
Vavg = D*Vin                  # 4.2 V
fsw = 100e3; Tsw = 1/fsw      # 10 us period
ton = D*Tsw                   # on-time
```

> **Practical insight:** PWM is everywhere - converters, motor drives, class-D
> audio, LED dimming. The same idea (vary the on-time, filter the average) scales
> from a dimmer to a megawatt inverter.

**Next:** getting DC from the AC line - rectifiers.
""",
        ),
        _t(
            "Rectifiers: AC to DC",
            "10 min",
            """\
# Rectifiers: AC to DC

The first conversion in most mains-powered systems is **AC -> DC**:
**rectification**, done with diodes (uncontrolled) or thyristors (controlled,
Intermediate course).

## Topologies

| Rectifier | Diodes | Ripple frequency | Notes |
|-----------|--------|------------------|-------|
| Half-wave | 1 | $f_{line}$ | wastes half the cycle |
| Full-wave (center-tap) | 2 | $2 f_{line}$ | needs a tapped transformer |
| **Bridge** | 4 | $2 f_{line}$ | the standard single-phase rectifier |
| **Three-phase bridge** | 6 | $6 f_{line}$ | high power, low ripple |

A reservoir capacitor smooths the rectified output; full-wave doubles the ripple
frequency, so a smaller cap suffices for the same ripple
($V_{ripple} \\approx I_{load}/(f_{ripple} C)$).

```mermaid
flowchart LR
  AC["3-phase AC"] --> BR["6-diode bridge"] --> CAP["DC bus capacitor"] --> DC["DC bus"]
```

## At power, details matter

- **Diode selection** - average/RMS current, peak reverse voltage, and surge
  (the inrush spike charging the cap at power-on) all size the diodes.
- **Power factor** - a cap-input rectifier draws current in narrow spikes at the
  voltage peaks, giving a poor **power factor** and harmonic current the grid
  dislikes. High-power supplies add **power-factor correction** (PFC, an active
  boost stage - Advanced course) to draw a clean sinusoidal current.
- **Three-phase** rectifiers dominate above a few kW: six pulses per cycle means
  inherently low ripple before any filtering.

```matlab
Vline_rms = 230; Vpk = Vline_rms*sqrt(2);   % ~325 V peak
Vdc_bridge = 2*Vpk/pi;                       % avg of full-wave (no cap)
```

```python
import numpy as np
Vline_rms = 230; Vpk = Vline_rms*np.sqrt(2)  # ~325 V peak
Vdc_bridge = 2*Vpk/np.pi                      # avg of full-wave (no cap)
```

> **Practical insight:** the humble bridge rectifier is the front end of most
> offline supplies, but its peaky current draw is why anything substantial needs
> PFC. Above a few kW, go three-phase.

**Next:** the canonical switching converter - the buck.
""",
        ),
        _t(
            "Introduction to the buck converter",
            "11 min",
            """\
# Introduction to the buck converter

The **buck converter** is the workhorse step-down DC-DC converter - the circuit
behind nearly every "12 V to 1.2 V for the CPU" rail. It's the PWM switch plus
the LC filter from two lessons ago, made concrete:

```mermaid
flowchart LR
  VIN["Vin"] --> SW["switch (PWM, duty D)"]
  SW --> NODE(("switch node"))
  NODE --> L["inductor L"]
  L --> COUT["Cout"] --> LOAD["Vout to load"]
  NODE --> D["diode (freewheel)"]
  D --> GND["gnd"]
```

When the switch is **on**, the inductor connects to $V_{in}$ and its current
ramps up, delivering energy to the output. When the switch turns **off**, the
inductor's current keeps flowing through the **freewheeling diode**, releasing
its stored energy to the load. The output settles at

$$V_{out} = D\\,V_{in}.$$

Slide the duty (and the input) - output scales linearly with $D$:

```plot
{"title": "Buck converter output Vout = D x Vin (slide input voltage)", "xLabel": "duty cycle D", "yLabel": "Vout (V)", "xRange": [0, 1], "yRange": [0, 24], "grid": true, "controls": [{"name": "Vin", "range": [5, 24], "value": 12, "label": "input voltage Vin (V)"}], "functions": [{"expr": "x*Vin", "label": "Vout = D x Vin"}]}
```

## Why it's efficient

Unlike a linear regulator, the buck never *drops* the excess voltage across a
resistive element - the switch is either on (tiny $R_{DS(on)}$ loss) or off, and
the inductor/capacitor store and release energy without dissipating it. Real
bucks hit 90-95%+; the losses are switching, conduction, and the diode (which
**synchronous** bucks replace with a MOSFET - Intermediate course).

```matlab
Vin = 12; D = 0.1;            % 12 V down to ~1.2 V (a CPU rail)
Vout = D*Vin;
```

```python
Vin, D = 12, 0.1              # 12 V -> ~1.2 V
Vout = D*Vin
```

> **Practical insight:** the buck is the default for stepping voltage **down**
> efficiently. Its cousins step **up** (boost) and invert (buck-boost) - all
> three are next. First, build a PWM averager yourself.

**Next:** generate PWM and recover its average.
""",
        ),
        _code(
            "Lab: PWM and average voltage",
            "12 min",
            """\
# Generate a PWM signal and recover its average with a low-pass filter.
# This is the heart of every buck converter. Edit the duty cycle and run.
import numpy as np
import matplotlib.pyplot as plt

fs = 200000                       # simulation sample rate
t = np.arange(0, 0.005, 1/fs)     # 5 ms
Vin = 12.0
fsw = 2000.0                      # switching frequency (Hz)
D = 0.35                          # duty cycle  <-- change me

# PWM: high for the first fraction D of each switching period.
pwm = Vin * (((t*fsw) % 1.0) < D)

# Low-pass filter (the LC filter's job, modeled as a first-order RC):
tau = 1e-4
y = np.zeros_like(t)
v = 0.0
dt = 1/fs
for k in range(len(t)):
    v += dt*(pwm[k] - v)/tau      # RC averaging
    y[k] = v

plt.figure(figsize=(8, 4))
plt.plot(t*1e3, pwm, color="#94a3b8", alpha=0.7, label="PWM output")
plt.plot(t*1e3, y, color="#16a34a", lw=2, label="filtered (average)")
plt.axhline(D*Vin, ls="--", color="#dc2626", label=f"D x Vin = {D*Vin:.1f} V")
plt.xlabel("time (ms)"); plt.ylabel("voltage (V)")
plt.title(f"PWM averaging: D={D}, fsw={fsw:.0f} Hz")
plt.legend(); plt.grid(True); plt.show()

print(f"target average D*Vin = {D*Vin:.2f} V,  measured = {y[-500:].mean():.2f} V")

# Try it yourself:
#   1. Set D = 0.75 -> the average rises to 9 V.
#   2. Raise fsw to 20000 -> the filtered output is smoother (less ripple).
""",
        ),
    ),
)


# ── Power Electronics — Intermediate ──────────────────────────────────────────

_POWER_INTERMEDIATE = SeedCourse(
    slug="power-electronics-intermediate",
    title="Power Electronics — Intermediate: DC-DC Converters & Control",
    description=(
        "The DC-DC converters in depth: buck/boost/buck-boost and their "
        "volt-second derivations, inductor/capacitor (ripple) design, "
        "synchronous rectification and efficiency, controlled rectifiers and "
        "thyristors, and closed-loop control - dual MATLAB/Python, interactive "
        "plots, and a runnable buck-converter simulation."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Buck, boost & buck-boost converters",
            "12 min",
            """\
# Buck, boost & buck-boost converters

Three non-isolated converters cover most DC-DC needs. The key tool to analyse
them is **volt-second balance**: in steady state the inductor's average voltage
over a switching period is **zero** (otherwise its current would ramp forever).
Apply it and the conversion ratios fall out:

| Converter | Does | $V_{out}$ |
|-----------|------|-----------|
| **Buck** | step down | $D\\,V_{in}$ |
| **Boost** | step up | $\\dfrac{V_{in}}{1 - D}$ |
| **Buck-boost** | up or down (inverted) | $-\\dfrac{D}{1 - D}\\,V_{in}$ |

```plot
{"title": "Conversion ratio vs duty cycle (slide Vin)", "xLabel": "duty cycle D", "yLabel": "Vout (V)", "xRange": [0.05, 0.8], "yRange": [-60, 90], "grid": true, "controls": [{"name": "Vin", "range": [5, 20], "value": 12, "label": "Vin (V)"}], "functions": [{"expr": "Vin*x", "label": "buck", "color": "#2563eb"}, {"expr": "Vin/(1-x)", "label": "boost", "color": "#16a34a"}, {"expr": "-Vin*x/(1-x)", "label": "buck-boost", "color": "#dc2626"}]}
```

Notice the **boost** ratio runs away as $D \\to 1$ - you can't boost arbitrarily
high in practice (parasitic resistances cap it and efficiency collapses).

## How boost steps *up*

When the switch is on, the inductor charges from $V_{in}$ (storing energy); when
it turns off, the inductor's voltage **adds in series** with $V_{in}$, pushing a
higher voltage onto the output cap through the diode. Energy, not magic: it
trades current for voltage.

```matlab
Vin = 5; D = 0.6;
Vbuck = Vin*D;            % 3 V
Vboost = Vin/(1-D);       % 12.5 V
Vbb = -Vin*D/(1-D);       % -7.5 V
```

```python
Vin, D = 5, 0.6
Vbuck = Vin*D             # 3 V
Vboost = Vin/(1-D)        # 12.5 V
Vbb = -Vin*D/(1-D)        # -7.5 V
```

> **Practical insight:** pick **buck** to step down, **boost** to step up,
> **buck-boost** (or its cousin SEPIC/Cuk) when the input can be above *or* below
> the output - e.g. a battery that sags from 4.2 V to 3.0 V feeding a 3.3 V rail.

**Next:** sizing the inductor and capacitor - ripple.
""",
        ),
        _t(
            "Inductor & capacitor design (ripple)",
            "12 min",
            """\
# Inductor & capacitor design (ripple)

The inductor doesn't carry a flat current - it carries a DC average with a
**triangular ripple** as it charges and discharges each cycle. For a buck:

$$\\Delta i_L = \\frac{(V_{in} - V_{out})\\,D}{L\\,f_{sw}}.$$

Bigger $L$ or higher $f_{sw}$ = smaller ripple. Slide $L$ and watch the inductor
current ripple shrink:

```plot
{"title": "Inductor current: DC average + triangular ripple (slide L)", "xLabel": "time", "yLabel": "inductor current (A)", "xRange": [0, 2], "yRange": [0, 8], "grid": true, "controls": [{"name": "L", "range": [0.5, 4], "value": 1, "label": "inductance (relative)"}], "functions": [{"expr": "3 + (2/L)*(mod(x*3, 1) - 0.5)", "label": "iL(t)"}]}
```

## CCM vs DCM

- **Continuous conduction mode (CCM)** - inductor current never reaches zero.
  Clean behaviour, the conversion ratios from the last lesson hold.
- **Discontinuous conduction mode (DCM)** - at light load the current hits zero
  and sits there each cycle; the ratio becomes load-dependent. Converters often
  slip into DCM at light load.

The boundary is set by the load and $L$: too little inductance or too light a
load and you fall into DCM.

## Output capacitor

The output capacitor absorbs the inductor's ripple current, leaving a small
**output voltage ripple**:

$$\\Delta V_{out} \\approx \\frac{\\Delta i_L}{8\\,f_{sw}\\,C_{out}} \\;(+\\; \\Delta i_L \\cdot ESR).$$

In real caps the **equivalent series resistance (ESR)** often dominates the
ripple - which is why low-ESR ceramics and polymer caps matter.

```matlab
Vin=12; Vout=5; D=Vout/Vin; L=10e-6; fsw=500e3;
diL = (Vin-Vout)*D/(L*fsw);        % inductor ripple current
```

```python
Vin, Vout, L, fsw = 12, 5, 10e-6, 500e3
D = Vout/Vin
diL = (Vin-Vout)*D/(L*fsw)         # inductor ripple current
```

> **Practical insight:** design for ~20-40% inductor ripple (a common rule):
> too little wastes inductor size, too much hurts ripple and pushes you into
> DCM. Then size $C_{out}$ (and pick its ESR) for the output ripple you can
> tolerate.

**Next:** squeezing out the diode loss - synchronous rectification.
""",
        ),
        _t(
            "Synchronous rectification & efficiency",
            "11 min",
            """\
# Synchronous rectification & efficiency

The freewheeling **diode** in a basic buck drops ~0.5-0.7 V whenever it
conducts - at 10 A that's 5-7 W wasted, often the biggest loss in a low-voltage
converter. **Synchronous rectification** replaces it with a second MOSFET (the
"low-side" switch) driven on when the diode would conduct, dropping only
$I \\cdot R_{DS(on)}$ - a few tens of millivolts. This is standard in any
efficient modern buck.

## The loss budget

Total loss is the sum of:

- **Conduction** - $I^2 R_{DS(on)}$ in the switches, $I^2 \\cdot DCR$ in the
  inductor. Dominates at **high load**.
- **Switching** - overlap loss + gate-charge loss, $\\propto f_{sw}$. Dominates at
  **light/medium load**.
- **Quiescent** - controller bias, always present. Dominates at **very light
  load**.

So efficiency is low at light load (fixed losses dominate a tiny output), peaks
in the middle, and droops at high load ($I^2$ conduction loss):

```plot
{"title": "Converter efficiency vs load current (typical synchronous buck)", "xLabel": "load current (A)", "yLabel": "efficiency", "xRange": [0.1, 8], "yRange": [0, 1.0], "grid": true, "functions": [{"expr": "0.97*(1 - exp(-3*x)) - 0.004*x^2", "label": "efficiency"}]}
```

## Dead time and shoot-through

The high- and low-side MOSFETs must **never be on together** (that shorts the
input - "shoot-through", instant destruction). The gate driver inserts a small
**dead time** between turning one off and the other on - a tiny gap where the
body diode conducts.

```matlab
Iload=10; Rdson=5e-3;
Pdiode = 0.6*Iload;            % 6 W with a diode
Psync  = Iload^2*Rdson;        % 0.5 W with a sync MOSFET
```

```python
Iload, Rdson = 10, 5e-3
Pdiode = 0.6*Iload             # 6 W with a diode
Psync = Iload**2*Rdson         # 0.5 W with a sync MOSFET
```

> **Practical insight:** to lift light-load efficiency, controllers drop into
> **pulse-skipping / PFM** modes (lower effective $f_{sw}$); to lift heavy-load
> efficiency, parallel MOSFETs and minimise $R_{DS(on)}$ and inductor DCR. Always
> respect dead time.

**Next:** controlling power from the AC line - thyristors.
""",
        ),
        _t(
            "Controlled rectifiers & thyristors",
            "11 min",
            """\
# Controlled rectifiers & thyristors

A diode rectifier gives a fixed DC. Replace the diodes with **thyristors (SCRs)**
and you can **control** the DC by choosing *when* in each AC half-cycle to turn
them on - the **firing angle** $\\alpha$. This **phase control** ruled high-power
AC-DC and AC power control for decades (motor drives, electroplating, HVDC, light
dimmers).

A thyristor **latches**: a gate pulse turns it on, and it stays on until its
current drops to zero (the next zero-crossing turns it off naturally in AC).

For a single-phase controlled rectifier, the average output falls as you delay
the firing:

$$V_{avg} = \\frac{V_{m}}{\\pi}\\,(1 + \\cos\\alpha) \\quad\\Rightarrow\\quad \\text{normalised } \\tfrac{1}{2}(1 + \\cos\\alpha).$$

```plot
{"title": "Controlled rectifier: output falls as the firing angle increases", "xLabel": "firing angle alpha (rad)", "yLabel": "normalized average output", "xRange": [0, 3.1416], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "(1 + cos(x))/2", "label": "Vavg(alpha)"}]}
```

Fire early ($\\alpha \\to 0$): full output. Fire late ($\\alpha \\to \\pi$): near
zero. A triac is the AC cousin (two SCRs back-to-back) behind the classic
light-dimmer.

```mermaid
flowchart LR
  AC["AC"] --> SCR["thyristor bridge (gate at angle alpha)"]
  GATE["firing control"] --> SCR
  SCR --> DC["controlled DC"]
```

```matlab
Vm = 325; alpha = pi/3;                 % 60 degrees
Vavg = Vm/pi*(1 + cos(alpha));          % controlled average
```

```python
import numpy as np
Vm, alpha = 325, np.pi/3                # 60 degrees
Vavg = Vm/np.pi*(1 + np.cos(alpha))     # controlled average
```

> **Practical insight:** thyristors are slow but handle enormous power and are
> rugged, so they still dominate the **highest-power** AC applications (HVDC,
> large industrial drives). For everything faster/smaller, PWM with MOSFETs/IGBTs
> won.

**Next:** keeping the output steady - closed-loop control.
""",
        ),
        _t(
            "Closed-loop control of converters",
            "11 min",
            """\
# Closed-loop control of converters

Open-loop $V_{out} = D V_{in}$ assumes a fixed input and load - neither is true.
A real converter **measures** its output and adjusts the duty cycle to hold it
steady against input and load changes. That's a feedback loop, exactly like the
Control Systems track.

```mermaid
flowchart LR
  REF["Vref"] --> SUM(("error"))
  SUM --> COMP["compensator (PID-like)"]
  COMP --> PWM["PWM modulator (sets D)"]
  PWM --> CONV["power stage (buck)"]
  CONV --> VOUT["Vout"]
  VOUT --> SUM
```

## Voltage-mode vs current-mode control

- **Voltage-mode** - the compensator acts on the output-voltage error alone.
  Simple, but the LC filter's resonant double pole makes the loop harder to
  stabilise.
- **Current-mode** - an inner loop also regulates the inductor **current** each
  cycle. This tames the LC pole, gives inherent current limiting, and is the
  industry default; it needs **slope compensation** above 50% duty to avoid
  sub-harmonic oscillation.

## Stability is a Bode problem

The power stage plus its LC filter is a (usually second-order) plant; the
**compensator** shapes the loop gain for adequate **phase margin** and crossover
- the same gain/phase-margin reasoning from the Control track. Get it wrong and
the converter rings or oscillates audibly.

```matlab
% Conceptual: a type-II/III compensator shapes the loop for phase margin.
fc = 50e3;              % target crossover (~ fsw/10)
% design poles/zeros so phase margin ~ 45-60 deg (see Control track).
```

```python
fc = 50e3               # target crossover (~ fsw/10)
# place compensator zeros/poles for ~45-60 deg phase margin
```

> **Practical insight:** target a crossover near $f_{sw}/10$ and keep ~45-60
> degrees of phase margin. Current-mode control is the safe default; reach for a
> type-III compensator when a voltage-mode buck's LC resonance needs taming.

**Next:** simulate a buck converter and see it regulate.
""",
        ),
        _code(
            "Lab: simulate a buck converter",
            "13 min",
            """\
# Cycle-by-cycle simulation of a buck converter. See Vout settle near D*Vin
# and the triangular inductor-current ripple. Edit D, L, fsw and run.
import numpy as np
import matplotlib.pyplot as plt

Vin = 12.0
L = 47e-6
C = 100e-6
R = 4.0            # load resistance
fsw = 100e3        # switching frequency
D = 0.42           # duty cycle  <-- change me (Vout ~ D*Vin = 5 V)

dt = 2e-8
t = np.arange(0, 1.5e-3, dt)
iL = 0.0
vout = 0.0
IL = np.zeros_like(t)
VO = np.zeros_like(t)
for k in range(len(t)):
    switch_on = ((t[k]*fsw) % 1.0) < D
    vL = (Vin - vout) if switch_on else (-vout)   # off: current freewheels
    iL += dt*vL/L
    if iL < 0:                                     # diode blocks reverse (CCM/DCM)
        iL = 0.0
    iout = vout/R
    vout += dt*(iL - iout)/C
    IL[k], VO[k] = iL, vout

fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
ax[0].plot(t*1e3, VO, color="#16a34a"); ax[0].axhline(D*Vin, ls="--", color="#dc2626")
ax[0].set_ylabel("Vout (V)"); ax[0].grid(True)
ax[1].plot(t*1e3, IL, color="#2563eb"); ax[1].set_ylabel("iL (A)")
ax[1].set_xlabel("time (ms)"); ax[1].grid(True)
plt.suptitle(f"Buck converter: D={D}, target Vout={D*Vin:.1f} V"); plt.tight_layout(); plt.show()

print(f"settled Vout = {VO[-3000:].mean():.2f} V (expected D*Vin = {D*Vin:.1f} V)")
print(f"inductor ripple ~ {IL[-3000:].max() - IL[-3000:].min():.2f} A")

# Try it yourself:
#   1. Halve L to 22e-6 -> larger inductor-current ripple.
#   2. Set D = 0.7 -> Vout climbs toward 8.4 V.
""",
        ),
    ),
)


# ── Power Electronics — Advanced ──────────────────────────────────────────────

_POWER_ADVANCED = SeedCourse(
    slug="power-electronics-advanced",
    title="Power Electronics — Advanced: Isolation, Inverters & Applications",
    description=(
        "Isolated converters (flyback, forward, bridges), resonant soft-switching "
        "(LLC), inverters and sinusoidal PWM, motor drives and VFDs, wide-bandgap "
        "(SiC/GaN) devices, thermal and EMI, and applications - dual MATLAB/"
        "Python, interactive plots, and a runnable SPWM-inverter lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Isolated converters: flyback, forward & bridges",
            "12 min",
            """\
# Isolated converters: flyback, forward & bridges

Many supplies must **galvanically isolate** input from output - for safety
(mains to your laptop) or to make multiple/negative rails. A **transformer**
provides the isolation *and* an extra voltage-scaling knob (the turns ratio
$n$), and switching it at high frequency keeps it tiny.

| Topology | Power range | How it works |
|----------|-------------|--------------|
| **Flyback** | < ~100 W | transformer **stores** energy when on, releases when off (chargers, standby) |
| **Forward** | ~100-500 W | transformer transfers energy directly while on |
| **Half-bridge / Full-bridge** | ~500 W-kW+ | two/four switches drive the transformer both ways (server PSUs, EV chargers) |
| **Push-pull** | medium | two switches alternate halves of the primary |

```mermaid
flowchart LR
  VIN["Vin"] --> SW["switch(es) (PWM)"]
  SW --> XFMR["HF transformer (isolation + ratio n)"]
  XFMR --> RECT["secondary rectifier"]
  RECT --> COUT["Cout"] --> VOUT["isolated Vout"]
```

The **flyback** is the star of low-power isolated supplies (every phone charger):
one switch, one magnetic component acting as coupled inductors, and dirt-cheap.
Its output (in DCM) is set by duty cycle, turns ratio, and load. Bridges take
over at higher power where a flyback's peak currents become impractical.

$$V_{out} \\approx n\\,\\frac{D}{1-D}\\,V_{in} \\quad (\\text{flyback, CCM}).$$

```matlab
n = 0.25; D = 0.4; Vin = 325;     % off-line flyback (rectified mains)
Vout = n*D/(1-D)*Vin;             % isolated output
```

```python
n, D, Vin = 0.25, 0.4, 325        # off-line flyback
Vout = n*D/(1-D)*Vin              # isolated output
```

> **Practical insight:** isolation is often a safety **requirement**, not a
> choice. Flyback for cheap low power, bridges for high power; and the
> transformer's leakage inductance always bites (snubbers, clamps) - which
> motivates the next topic, resonant converters.

**Next:** switching with (almost) no loss - resonant converters.
""",
        ),
        _t(
            "Resonant converters & soft switching",
            "11 min",
            """\
# Resonant converters & soft switching

In a hard-switched converter, voltage and current overlap during each transition
- **switching loss** that grows with frequency and caps how high you can push
$f_{sw}$ (and thus how small the magnetics get). **Resonant converters** use an
LC tank to shape the waveforms so a switch turns on at **zero voltage** (ZVS) or
off at **zero current** (ZCS) - **soft switching**, with near-zero transition
loss.

That lets resonant converters run at **high frequency** (smaller, lighter) and
**high efficiency** at once - which is why the **LLC resonant converter**
dominates modern high-efficiency isolated supplies (server/telecom, LED, OLED TV,
EV on-board chargers).

The LLC is controlled by **frequency**, not duty cycle: its gain peaks near the
resonant frequency and you move around it to regulate:

```plot
{"title": "LLC resonant converter gain vs frequency (slide Q)", "xLabel": "frequency / f_resonant", "yLabel": "voltage gain", "xRange": [0.4, 2.2], "yRange": [0, 2.2], "grid": true, "controls": [{"name": "Q", "range": [2, 8], "value": 4, "label": "tank quality factor Q"}], "functions": [{"expr": "1/sqrt(1 + Q^2*(x - 1/x)^2)*2", "label": "gain |M(f)|"}]}
```

Lower $Q$ (lighter load) gives a taller, sharper gain peak; the controller picks
the switching frequency to land on the gain it needs.

## ZVS vs ZCS

- **ZVS (zero-voltage switching)** - the switch turns on when the voltage across
  it is already zero. Favoured for MOSFETs (avoids dumping the output
  capacitance's energy). LLC is a ZVS topology.
- **ZCS (zero-current switching)** - the switch turns off at zero current.
  Favoured for IGBTs/thyristors with slow turn-off tails.

> **Practical insight:** resonant/soft-switching is how you get *both* high
> frequency and high efficiency - but the gain is nonlinear in frequency and the
> design is trickier than a PWM buck. It pays off in high-density, high-efficiency
> supplies; for simple rails a hard-switched buck is fine.

**Next:** going the other way - DC to AC, the inverter.
""",
        ),
        _t(
            "Inverters: DC to AC",
            "12 min",
            """\
# Inverters: DC to AC

An **inverter** synthesizes AC from DC - the conversion behind solar systems,
UPSs, EV traction, and every variable-speed motor drive. The core is a
**bridge** of switches that connects the load to +DC or -DC; the trick is
choosing the switching pattern so the *average* traces a sine.

## Sinusoidal PWM (SPWM)

Compare a low-frequency **sine reference** with a high-frequency **triangle
carrier**: switch high when the sine is above the carrier, low when below. The
result is a PWM whose duty varies sinusoidally, so its filtered average is a
clean sine:

```plot
{"title": "Sinusoidal PWM: sine reference vs triangle carrier", "xLabel": "time", "yLabel": "normalized", "xRange": [0, 3.1416], "yRange": [-1.2, 1.2], "grid": true, "functions": [{"expr": "0.8*sin(2*x)", "label": "sine reference", "color": "#dc2626"}, {"expr": "4*abs(mod(x*4, 1) - 0.5) - 1", "label": "triangle carrier", "color": "#2563eb"}]}
```

Where the red sine is above the blue triangle, the output is high; the wider
high-pulses near the sine peak give a higher local average. An LC filter (or the
motor's own inductance) recovers the sine.

The **modulation index** $m_a$ (sine amplitude / carrier amplitude) sets the
output amplitude; pushing $m_a > 1$ (**overmodulation**) gains amplitude at the
cost of low-order harmonics.

## Single- vs three-phase

```mermaid
flowchart LR
  DC["DC bus"] --> INV["3-phase bridge (6 switches)"]
  CTRL["SPWM control"] --> INV
  INV --> MOTOR["3-phase AC (motor / grid)"]
```

A **three-phase** inverter (six switches, three half-bridges) produces three
sine waves 120 degrees apart - the standard for motors and grid-tie. Higher
carrier frequency = cleaner output but more switching loss; real drives often use
**space-vector PWM** (a smarter pattern) for better DC-bus use and lower
harmonics.

```matlab
Vdc = 400; ma = 0.9;
Vphase_pk = ma*Vdc/2;          % peak phase voltage (SPWM, linear range)
```

```python
Vdc, ma = 400, 0.9
Vphase_pk = ma*Vdc/2           # peak phase voltage (SPWM, linear range)
```

> **Practical insight:** SPWM (or SVPWM) turns a DC bus into adjustable-amplitude,
> adjustable-frequency AC - which is exactly what a motor drive needs. Push the
> carrier up for audio-quiet, clean output; watch the switching loss.

**Next:** the biggest application - motor drives.
""",
        ),
        _t(
            "Motor drives & variable-frequency drives",
            "11 min",
            """\
# Motor drives & variable-frequency drives

The largest use of power electronics by far is **driving motors** - which
consume roughly **half of all the world's electricity**. A **variable-frequency
drive (VFD)** lets an AC motor run at any speed efficiently, replacing wasteful
throttling (valves, dampers) and saving enormous energy in pumps, fans, HVAC, and
industry.

```mermaid
flowchart LR
  AC["AC mains"] --> RECT["rectifier"] --> BUS["DC bus + cap"]
  BUS --> INV["inverter (SPWM/SVPWM)"]
  INV --> MOTOR["AC motor (variable speed)"]
  SENSE["speed / current feedback"] --> CTRL["control"] --> INV
```

It's the **AC -> DC -> AC** chain: rectify the mains to a DC bus, then invert it
to **adjustable frequency and voltage**.

## V/f vs field-oriented control

- **V/f (scalar) control** - keep voltage proportional to frequency to hold the
  motor's magnetic flux roughly constant. Simple, open-loop, fine for pumps/fans.
- **Field-oriented control (FOC / vector control)** - mathematically decouple the
  motor's torque-producing and flux-producing currents (via the Park/Clarke
  transforms) and control them independently, like a DC motor. Gives precise
  torque and dynamic response - the standard for EVs, robotics, and servos.

FOC closes fast **current loops** (the Control track again) inside a speed loop,
all running on the inverter's PWM.

## Regeneration

Because the bridge is bidirectional, a motor being slowed can **feed energy
back** - regenerative braking in EVs returns energy to the battery instead of
burning it in friction brakes.

```matlab
f = 30; V_rated = 400; f_rated = 50;
V = V_rated*f/f_rated;          % V/f control: scale voltage with frequency
```

```python
f, V_rated, f_rated = 30, 400, 50
V = V_rated*f/f_rated           # V/f control
```

> **Practical insight:** a VFD is often the single biggest energy saver in a
> facility - fan/pump power scales with the **cube** of speed, so a small speed
> reduction saves a lot. V/f for simple loads, FOC when you need torque control
> and dynamics.

**Next:** the devices and physics that set the limits.
""",
        ),
        _t(
            "Wide-bandgap devices, thermal & EMI",
            "11 min",
            """\
# Wide-bandgap devices, thermal & EMI

## Wide-bandgap: SiC and GaN

Silicon has ruled, but **silicon carbide (SiC)** and **gallium nitride (GaN)**
change the game. Their wider bandgap means they block more voltage in less
material and switch far faster:

- **lower losses** (conduction and switching),
- **higher switching frequency** -> much smaller magnetics and capacitors,
- **higher temperature** operation.

SiC dominates high-voltage/high-power (EV traction inverters, solar, grid); GaN
dominates lower-voltage high-frequency (fast chargers, data-center supplies).
They're why a modern laptop charger is a quarter the size of a decade ago.

## Thermal management - the real limit

Losses become **heat**, and a device dies if its **junction temperature**
exceeds its rating. Heat flows through a chain of **thermal resistances** (in
$^\\circ$C/W), exactly like Ohm's law for heat:

$$T_{junction} = T_{ambient} + P_{loss}\\,(R_{th,jc} + R_{th,cs} + R_{th,sa}).$$

Junction-to-case, case-to-sink (the thermal paste), sink-to-ambient (the
heatsink). Sizing the heatsink to keep $T_j$ safe is a core power-electronics
task - and often the thing that limits how much power a converter can deliver.

## EMI

Fast switching ($dv/dt$, $di/dt$) radiates and conducts **electromagnetic
interference**. Designs must pass EMI standards (CISPR/FCC) with **input
filters**, careful layout (minimise switching-loop area), shielding, and
sometimes slowing the edges (trading switching loss for less EMI). Wide-bandgap's
faster edges make EMI harder, not easier.

```matlab
Ploss = 25; Rth = 1.5; Tamb = 40;
Tj = Tamb + Ploss*Rth;          % junction temperature -> 77.5 C
```

```python
Ploss, Rth, Tamb = 25, 1.5, 40
Tj = Tamb + Ploss*Rth           # junction temperature
```

> **Practical insight:** in power electronics, **heat and EMI** usually decide
> what's buildable, not the schematic. Budget the thermal path early, and treat
> layout and filtering as first-class design - not an afterthought.

**Next:** build a sinusoidal-PWM inverter waveform.
""",
        ),
        _code(
            "Lab: a sinusoidal-PWM inverter",
            "13 min",
            """\
# Build a sinusoidal-PWM (SPWM) inverter: compare a sine to a triangle carrier,
# generate the PWM, and low-pass filter it back into a sine.
import numpy as np
import matplotlib.pyplot as plt

fs = 400000                        # sim sample rate
t = np.arange(0, 0.04, 1/fs)       # 40 ms = two 50 Hz cycles
f_out = 50.0                       # desired output frequency
f_carrier = 2000.0                 # triangle carrier frequency
ma = 0.8                           # modulation index (sine amp / carrier amp)
Vdc = 1.0

ref = ma*np.sin(2*np.pi*f_out*t)                       # sine reference
carrier = 4*np.abs(((t*f_carrier) % 1.0) - 0.5) - 1    # triangle in [-1, 1]
pwm = np.where(ref > carrier, Vdc, -Vdc)               # the inverter output

# Low-pass filter (the load inductance / LC filter recovering the sine):
tau = 5e-4
y = np.zeros_like(t)
v = 0.0
dt = 1/fs
for k in range(len(t)):
    v += dt*(pwm[k] - v)/tau
    y[k] = v

fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
ax[0].plot(t*1e3, pwm, color="#94a3b8", alpha=0.6, label="SPWM output")
ax[0].plot(t*1e3, ref, color="#dc2626", lw=2, label="sine reference")
ax[0].legend(loc="upper right"); ax[0].set_ylabel("switched"); ax[0].grid(True)
ax[1].plot(t*1e3, y, color="#16a34a", lw=2, label="filtered output")
ax[1].legend(loc="upper right"); ax[1].set_ylabel("recovered sine")
ax[1].set_xlabel("time (ms)"); ax[1].grid(True)
plt.suptitle(f"SPWM inverter: {f_out:.0f} Hz from DC, ma={ma}"); plt.tight_layout(); plt.show()

print(f"output frequency = {f_out:.0f} Hz, modulation index = {ma}")
print(f"filtered amplitude ~ {y[len(y)//2:].max():.2f} (expect ~ ma = {ma})")

# Try it yourself:
#   1. Raise f_carrier to 8000 -> the filtered sine gets cleaner (fewer ripples).
#   2. Set ma = 1.2 (overmodulation) -> the peak flattens, adding distortion.
""",
        ),
        _t(
            "Applications & the throughline",
            "9 min",
            """\
# Applications & the throughline

Power electronics is the quiet enabler of the electrified, efficient world:

- **Electric vehicles** - traction inverter (SiC), DC-DC for the 12 V system,
  the on-board charger, and fast DC chargers are all power electronics; they set
  range, charge time, and cost.
- **Renewables & grid** - solar/wind inverters turn DC and variable AC into
  grid-quality AC; HVDC links and grid-forming inverters increasingly run the
  grid itself.
- **Data centers** - cascaded conversions (AC->DC->DC) feed the CPUs/GPUs;
  every efficiency point saved is megawatts and millions.
- **Consumer** - phone/laptop chargers (GaN flyback/LLC), LED drivers, class-D
  audio, and every appliance with a motor.
- **Industry** - VFDs on pumps, fans, and conveyors are the biggest single
  energy-saving technology deployed.

```mermaid
flowchart LR
  SRC["source: grid / battery / PV"] --> CONV["convert: rectify / DC-DC / invert"]
  CONV --> CTRL["control duty/frequency (feedback)"]
  CTRL --> LOAD["load: CPU / motor / grid"]
  CONV --> THERM["manage heat + EMI"]
```

## The throughline

Every converter in this track is the same idea: **switch** a device fully on and
off (low loss), **store and filter** energy with inductors, capacitors, and
transformers, **control the duty cycle or frequency** with a feedback loop to set
the output, and **manage the heat and EMI** that the switching creates. Buck,
boost, flyback, LLC, inverter - they differ in topology, but that recipe, and the
relentless pursuit of efficiency, is the whole field. And whether you prototype
in MATLAB or Python, the models and the math are identical; only the syntax
changes.

**Next:** the final check.
""",
        ),
    ),
)


POWER_ELECTRONICS_COURSES: tuple[SeedCourse, ...] = (
    _POWER_BASICS,
    _POWER_INTERMEDIATE,
    _POWER_ADVANCED,
)

__all__ = ["POWER_ELECTRONICS_COURSES"]
