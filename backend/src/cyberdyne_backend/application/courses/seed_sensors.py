"""Curated Sensors, Instrumentation & Data Acquisition track: Basics,
Intermediate, Advanced.

A complete measurement-chain curriculum: sensors and signal conditioning,
bridges and resistive sensors, measurement fundamentals and noise (Basics);
analog-to-digital and back, sampling theory, digital filtering and DAQ systems
(Intermediate); sensor fusion and Kalman filtering, calibration and
compensation, precision/low-noise measurement, MEMS, and instrumentation
standards (Advanced). Dual MATLAB + Python focus throughout, with runnable
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


# -- Sensors & Instrumentation -- Basics ---------------------------------------

_SENSORS_BASICS = SeedCourse(
    slug="sensors-basics",
    title="Sensors & Instrumentation -- Basics",
    description=(
        "The measurement chain from the ground up: sensors and transducers, "
        "their transfer functions and specs, signal conditioning (amplify, "
        "filter, level-shift), Wheatstone bridges and resistive sensors, "
        "measurement fundamentals (accuracy, error, calibration, SI units), "
        "and noise/grounding - with side-by-side MATLAB and Python, interactive "
        "plots, and a runnable bridge/linearization lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Sensors & transducers overview",
            "11 min",
            """\
# Sensors & transducers overview

A **sensor** turns a physical quantity (temperature, force, light, motion) into
an electrical signal you can measure. A **transducer** is the broader term for
any device that converts one form of energy to another - every sensor is a
transducer. This is the front door of every measurement system, from a kitchen
thermostat to the Mars rover.

## The transfer function

The heart of any sensor is its **transfer function**: the relationship between
the physical input $x$ and the electrical output $y$. The ideal is linear:

$$y = S\\,x + b,$$

where $S$ is the **sensitivity** (output per unit input, e.g. mV per degree C)
and $b$ is the offset. The steeper the line, the more sensitive the sensor.
Slide the sensitivity and watch the line tilt:

```plot
{"title": "Sensor transfer function: y = S x + offset (slide sensitivity)", "xLabel": "physical input x", "yLabel": "electrical output y", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "controls": [{"name": "S", "range": [0.2, 2], "value": 1, "label": "sensitivity S"}], "functions": [{"expr": "S*x + 1", "label": "y = S x + offset"}]}
```

## The key specifications

| Spec | Meaning | Why it matters |
|------|---------|----------------|
| **Sensitivity** | output per unit input ($dy/dx$) | small signals need high $S$ |
| **Range / span** | min-to-max measurable input | don't exceed it |
| **Linearity** | how straight the real curve is | nonlinearity = error |
| **Resolution** | smallest detectable change | sets the finest reading |
| **Hysteresis** | output depends on history/direction | repeatability error |

## Real nonlinearity

No real sensor is perfectly straight. A thermistor's resistance, for example, is
strongly nonlinear with temperature. Here the ideal line and a realistic curved
response diverge at the ends - the gap is the **nonlinearity error**:

```plot
{"title": "Ideal linear vs real nonlinear sensor response", "xLabel": "input", "yLabel": "output", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "ideal linear", "color": "#2563eb"}, {"expr": "x + 0.06*(x-5)^2 - 1.5", "label": "real (nonlinear)", "color": "#dc2626"}]}
```

## Common sensor types in the wild

- **Temperature** - thermocouple (industrial furnaces), RTD (precision labs),
  thermistor (cheap consumer thermostats).
- **Force/pressure** - strain-gauge load cells (bathroom scales, truck weigh
  stations), piezoresistive pressure sensors (car tire monitors).
- **Motion** - MEMS accelerometers and gyros (phones, drones, airbags).
- **Light** - photodiodes (cameras), photoresistors (night lights).

```matlab
S = 0.01;  offset = 0.5;          % 10 mV/degC, 0.5 V offset
T = 25;                           % temperature in degC
Vout = S*T + offset;              % 0.75 V
```

```python
S, offset = 0.01, 0.5             # 10 mV/degC, 0.5 V offset
T = 25                            # degC
Vout = S*T + offset               # 0.75 V
```

> **Practical insight:** always check the **range** first - a sensor measuring
> outside its span saturates or breaks, and the numbers it returns are garbage.

**Next:** the raw sensor signal is rarely usable as-is - signal conditioning.
""",
        ),
        _t(
            "Signal conditioning",
            "11 min",
            """\
# Signal conditioning

A raw sensor signal is usually too small, too noisy, or sitting at the wrong
voltage level for the **analog-to-digital converter** (ADC) that follows.
**Signal conditioning** is the analog electronics between the sensor and the ADC
that fixes all three. A thermocouple, for example, puts out only **microvolts**
per degree - useless until you amplify it.

```mermaid
flowchart LR
  S["sensor"] --> AMP["amplify"]
  AMP --> FILT["filter"]
  FILT --> LVL["level shift"]
  LVL --> ADC["ADC"]
```

## The three core jobs

1. **Amplification** - boost a small signal to use the ADC's full range. This is
   an **op-amp** job (see the Electronics track): a non-inverting amp gives gain
   $1 + R_f/R_{in}$, and an **instrumentation amplifier** amplifies the tiny
   *difference* across a bridge while rejecting shared noise.
2. **Filtering** - a low-pass filter removes high-frequency noise and (crucially)
   acts as the **anti-aliasing filter** before sampling. The RC cutoff is
   $f_c = 1/(2\\pi R C)$.
3. **Level shifting** - move and scale the signal so it lands inside the ADC's
   input window (e.g. 0 to 3.3 V). Output is $V_{adc} = G\\,V_{sensor} + V_{shift}$.

## Match the sensor to the ADC window

If your sensor swings -0.2 to +0.2 V but the ADC wants 0 to 3.3 V, you waste
almost all the ADC's resolution unless you amplify and shift. Slide the gain to
fill the window:

```plot
{"title": "Conditioning a +/-0.2 V sensor into a 0-3.3 V ADC window (slide gain)", "xLabel": "sensor voltage (V)", "yLabel": "ADC input (V)", "xRange": [-0.2, 0.2], "yRange": [0, 3.3], "grid": true, "controls": [{"name": "G", "range": [2, 8], "value": 7, "label": "gain G"}], "functions": [{"expr": "G*x + 1.65", "label": "G*Vsensor + 1.65 V shift"}]}
```

The low-pass filter's job is clearest in the frequency domain - signal passes,
high-frequency noise is attenuated (slide the cutoff):

```plot
{"title": "Anti-noise low-pass filter (slide cutoff fc)", "xLabel": "frequency f (Hz)", "yLabel": "gain |H|", "xRange": [1, 1000], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "fc", "range": [20, 400], "value": 100, "label": "cutoff fc (Hz)"}], "functions": [{"expr": "1/sqrt(1+(x/fc)^2)", "label": "low-pass |H|"}]}
```

```matlab
G = 7; Vshift = 1.65;             % gain and mid-rail shift
Vsensor = 0.1;                    % +0.1 V
Vadc = G*Vsensor + Vshift;        % 2.35 V -> inside 0-3.3 V window
```

```python
G, Vshift = 7, 1.65               # gain and mid-rail shift
Vsensor = 0.1                     # +0.1 V
Vadc = G*Vsensor + Vshift         # 2.35 V
```

> **Practical insight:** condition close to the sensor and amplify **early** -
> once noise rides on a tiny signal, no later amplifier can separate them. Gain
> first, then send the bigger signal down the wire.

**Next:** the classic way to read a resistive sensor - the bridge.
""",
        ),
        _t(
            "Bridges & resistive sensors",
            "12 min",
            """\
# Bridges & resistive sensors

Many sensors change their **resistance** with the thing they measure - a strain
gauge stretches, an RTD warms, a thermistor heats. The trouble: the *change* is
often tiny (a strain gauge might shift 0.1%). Measuring a tiny change on top of a
big baseline resistance directly is hopeless. The **Wheatstone bridge** solves
this elegantly.

## The Wheatstone bridge

Four resistors in a diamond, excited by $V_{ex}$. The output is the **difference**
between two voltage dividers:

$$V_{out} = V_{ex}\\left(\\frac{R_3}{R_3 + R_4} - \\frac{R_2}{R_1 + R_2}\\right).$$

When all four are equal the bridge is **balanced** and $V_{out} = 0$. Change one
arm by $\\Delta R$ and the output departs from zero in proportion - so the bridge
turns a tiny resistance change into a clean differential voltage **starting from
zero**, which you then amplify.

```mermaid
flowchart TB
  EX["Vex"] --> A(("A"))
  EX --> B(("B"))
  A --> R1["R1"] --> OUTL(("out-"))
  OUTL --> R2["R2"] --> G["gnd"]
  B --> R4["R4"] --> OUTR(("out+"))
  OUTR --> R3["R3 (sensor)"] --> G
```

For one varying arm ($R_3 = R + \\Delta R$, others $= R$), the output is nearly
linear in the fractional change $x = \\Delta R / R$ but bends slightly:

```plot
{"title": "Quarter-bridge output vs fractional resistance change", "xLabel": "fractional change dR/R", "yLabel": "Vout / Vex", "xRange": [-0.1, 0.1], "yRange": [-0.03, 0.03], "grid": true, "functions": [{"expr": "x/(4 + 2*x)", "label": "exact quarter-bridge", "color": "#dc2626"}, {"expr": "x/4", "label": "linear approx (x/4)", "color": "#2563eb"}]}
```

## The resistive sensor family

| Sensor | Measures | Behaviour | Typical use |
|--------|----------|-----------|-------------|
| **Strain gauge** | strain/force | $\\Delta R/R = GF \\cdot \\varepsilon$ | load cells, scales |
| **RTD** (e.g. Pt100) | temperature | nearly linear, positive | precision industrial |
| **Thermistor** (NTC) | temperature | strongly nonlinear, negative | cheap, sensitive |

The **gauge factor** $GF$ (about 2 for metal foil) links strain to resistance
change. A thermistor follows the Steinhart-Hart / beta relation:

$$\\frac{1}{T} = \\frac{1}{T_0} + \\frac{1}{\\beta}\\ln\\!\\left(\\frac{R}{R_0}\\right).$$

The NTC thermistor's strongly curved resistance-vs-temperature is why it needs
**linearization** (you build this in the lab):

```plot
{"title": "NTC thermistor: resistance falls steeply with temperature", "xLabel": "temperature (degC)", "yLabel": "resistance / R25", "xRange": [0, 60], "yRange": [0, 3.5], "grid": true, "functions": [{"expr": "exp(3500*(1/(x+273.15) - 1/298.15))", "label": "R(T)/R25, beta=3500"}]}
```

```matlab
Vex = 5; R = 350; dR = 0.7;       % 0.2% change on a 350 ohm gauge
Vout = Vex*(dR/(2*(2*R+dR)));     % quarter-bridge output
```

```python
Vex, R, dR = 5, 350, 0.7          # 0.2% change on a 350 ohm gauge
Vout = Vex*(dR/(2*(2*R+dR)))      # quarter-bridge output
```

> **Practical insight:** use a **half** or **full** bridge (two or four active
> gauges) when you can - it doubles or quadruples sensitivity *and* cancels
> temperature drift, because all arms drift together.

**Next:** how do we even know a reading is right? Measurement fundamentals.
""",
        ),
        _t(
            "Measurement fundamentals",
            "11 min",
            """\
# Measurement fundamentals

A number from a sensor is meaningless without knowing **how good it is**. The
language of measurement quality is precise, and engineers must use it precisely.

## Accuracy vs precision (not the same thing)

- **Accuracy** - how close readings are to the **true** value (correct on
  average; no bias).
- **Precision** - how close repeated readings are to **each other** (low
  scatter), regardless of whether they're correct.

The classic dartboard: tight cluster off-center = precise but inaccurate;
scattered around the bullseye = accurate but imprecise. You want both. Here two
sensors sample the same true value - one is biased (accurate-no, precise-yes),
one is noisy (accurate-yes, precise-no):

```plot
{"title": "Accuracy vs precision: readings around a true value of 5", "xLabel": "sample number", "yLabel": "reading", "xRange": [0, 10], "yRange": [3, 8], "grid": true, "functions": [{"expr": "5", "label": "true value", "color": "#16a34a"}], "series": [{"points": [[1, 6.4], [2, 6.5], [3, 6.45], [4, 6.55], [5, 6.4], [6, 6.5], [7, 6.48], [8, 6.52], [9, 6.46], [10, 6.5]], "label": "precise but biased", "color": "#2563eb"}, {"points": [[1, 4.2], [2, 5.9], [3, 4.5], [4, 6.1], [5, 4.0], [6, 5.7], [7, 4.8], [8, 5.5], [9, 4.3], [10, 5.8]], "label": "accurate but noisy", "color": "#dc2626"}]}
```

## Error, resolution, and the budget

- **Error** = measured value - true value. Split into **systematic** (bias,
  repeatable - calibrate it out) and **random** (noise - average it down).
- **Resolution** - the smallest change the instrument can show. A 12-bit ADC over
  a 3.3 V range resolves $3.3 / 2^{12} \\approx 0.8\\,$mV.
- **Error budget** - real measurements combine many independent errors. Random
  ones add in quadrature: $\\sigma_{total} = \\sqrt{\\sigma_1^2 + \\sigma_2^2 + \\dots}$.

## Calibration

**Calibration** compares your instrument against a **known reference** (a traceable
standard) and builds a correction. A simple two-point calibration finds gain and
offset:

$$y_{true} = m\\,(y_{raw}) + c.$$

This is how a scale is "zeroed and spanned," and why lab instruments carry a
calibration sticker with an expiry date.

## SI units and traceability

Every trustworthy measurement traces back to the **SI base units** (metre,
kilogram, second, ampere, kelvin, mole, candela), now defined by fixed constants
of nature. **Traceability** - an unbroken chain of calibrations up to a national
standard - is what lets a measurement in one lab be trusted in another.

```matlab
bits = 12; Vref = 3.3;
resolution = Vref / 2^bits;       % ~0.806 mV per LSB
% two-point cal: raw 0.10 -> true 0.00, raw 0.90 -> true 1.00
m = (1.00 - 0.00)/(0.90 - 0.10);  c = -m*0.10;
```

```python
bits, Vref = 12, 3.3
resolution = Vref / 2**bits       # ~0.806 mV per LSB
m = (1.00 - 0.00)/(0.90 - 0.10);  c = -m*0.10  # two-point cal
```

> **Practical insight:** you can **average away** random error (precision
> improves as $1/\\sqrt{N}$) but you can only **calibrate away** systematic error.
> Know which one you have before you try to fix it.

**Next:** the enemy of every measurement - noise and bad grounding.
""",
        ),
        _t(
            "Noise & grounding in measurement",
            "11 min",
            """\
# Noise & grounding in measurement

The fastest way to ruin a good sensor is sloppy wiring. **Noise** and **ground
problems** can be larger than the signal you're trying to measure, and they are
the number-one cause of mysterious, irreproducible readings on the bench.

## Where noise comes from

- **Thermal (Johnson) noise** - fundamental, from any resistor; floor rises with
  resistance, bandwidth, and temperature: $v_n = \\sqrt{4 k_B T R\\,\\Delta f}$.
- **Interference** - 50/60 Hz mains hum, switching-supply spikes, radio. This is
  *coupled* in and can be fought with shielding and layout.
- **Quantization noise** - from the ADC itself (Intermediate course).

A noisy measurement is the clean signal plus an unwanted component. The more
bandwidth you let through, the more noise you collect - so a conditioning
low-pass filter both shapes the signal and **limits the noise**.

```plot
{"title": "Signal plus interference: a clean sine corrupted by 60 Hz hum", "xLabel": "time (ms)", "yLabel": "voltage", "xRange": [0, 40], "yRange": [-2.2, 2.2], "grid": true, "functions": [{"expr": "sin(2*pi*x/40)", "label": "clean signal", "color": "#16a34a"}, {"expr": "sin(2*pi*x/40) + 0.6*sin(2*pi*60*x/1000)", "label": "with 60 Hz hum", "color": "#dc2626"}]}
```

## Differential measurement and guarding

The single best defence is to measure **differentially**: read the *difference*
between two wires routed together. Interference couples almost equally into both
(it is **common-mode**), so the difference cancels it. An **instrumentation
amplifier**'s ability to do this is its **common-mode rejection ratio** (CMRR) -
the higher the better. A higher CMRR crushes the common-mode hum harder:

```plot
{"title": "Common-mode rejection: residual hum vs CMRR (slide CMRR in dB)", "xLabel": "common-mode hum amplitude (V)", "yLabel": "residual at output (mV)", "xRange": [0, 5], "yRange": [0, 60], "grid": true, "controls": [{"name": "cmrr", "range": [40, 100], "value": 60, "label": "CMRR (dB)"}], "functions": [{"expr": "1000*x/pow(10, cmrr/20)", "label": "residual hum"}]}
```

## Grounding: the silent killer

- **Ground loops** - when two points you assumed were "ground" sit at slightly
  different potentials, a current flows through the shared ground and adds a noise
  voltage to your signal. Cure: a **single-point (star) ground**.
- **Shielding** - a grounded shield around the cable intercepts capacitively
  coupled interference. Ground the shield at **one end only** to avoid a loop.
- **Guarding** - drive a guard trace at the signal's own potential to stop
  leakage currents in high-impedance measurements.

```mermaid
flowchart TB
  SIG["sensor signal"] --> SH["shielded cable"]
  SH --> INST["instrumentation amp (differential)"]
  GND["star ground (single point)"] --> INST
  SH -.shield grounded one end.-> GND
```

```matlab
kB = 1.380649e-23; T = 300; R = 1e6; BW = 1e4;
vn = sqrt(4*kB*T*R*BW);           % thermal noise voltage (Vrms)
cmrr_dB = 90;  rejection = 10^(cmrr_dB/20);  % 90 dB -> 31623x
```

```python
import numpy as np
kB, T, R, BW = 1.380649e-23, 300, 1e6, 1e4
vn = np.sqrt(4*kB*T*R*BW)         # thermal noise (Vrms)
cmrr_dB = 90; rejection = 10**(cmrr_dB/20)  # 90 dB
```

> **Practical insight:** when a reading is noisy, suspect the **wiring** before
> the sensor. Twist signal pairs, shield, measure differentially, and ground at a
> single point - most "bad sensors" are actually bad grounds.

**Next:** put it together - simulate a bridge and linearize a sensor.
""",
        ),
        _code(
            "Lab: Wheatstone bridge & sensor linearization",
            "13 min",
            """\
# Simulate a Wheatstone bridge reading a strain gauge, then linearize an NTC
# thermistor with a polynomial fit. All numpy + matplotlib, module level only.
import numpy as np
import matplotlib.pyplot as plt

# --- Part 1: quarter-bridge strain gauge ---
Vex = 5.0          # excitation voltage
R0 = 350.0         # nominal gauge resistance (ohm)
GF = 2.0           # gauge factor

strain = np.linspace(-0.004, 0.004, 200)     # +/-4000 microstrain
dR = R0 * GF * strain                          # resistance change
Vout = Vex * (dR / (2.0 * (2.0 * R0 + dR)))    # exact quarter-bridge output
Vlin = Vex * (GF * strain / 4.0)               # linear approximation

# --- Part 2: NTC thermistor linearization ---
beta = 3500.0
R25 = 10000.0
Tc = np.linspace(0, 60, 13)                    # calibration temperatures (degC)
Tk = Tc + 273.15
Rth = R25 * np.exp(beta * (1.0 / Tk - 1.0 / 298.15))   # nonlinear R(T)

# Read the thermistor as the top half of a divider with a fixed 10k resistor.
Rfixed = 10000.0
Vdiv = 3.3 * Rfixed / (Rth + Rfixed)           # divider voltage (nonlinear in T)

# Fit a cubic polynomial: temperature as a function of divider voltage.
coeffs = np.polyfit(Vdiv, Tc, 3)
Tfit = np.polyval(coeffs, Vdiv)
max_err = np.max(np.abs(Tfit - Tc))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(strain * 1e6, Vout * 1000, color="#dc2626", lw=2, label="exact bridge")
ax1.plot(strain * 1e6, Vlin * 1000, "--", color="#2563eb", label="linear approx")
ax1.set_xlabel("strain (microstrain)")
ax1.set_ylabel("bridge output (mV)")
ax1.set_title("Quarter-bridge: exact vs linear")
ax1.legend()
ax1.grid(True)

ax2.plot(Tc, Vdiv, "o-", color="#16a34a", label="divider voltage")
ax2.set_xlabel("temperature (degC)")
ax2.set_ylabel("divider voltage (V)", color="#16a34a")
ax2.set_title("NTC divider + cubic linearization")
ax2.grid(True)
ax2b = ax2.twinx()
ax2b.plot(Tc, Tfit, "s--", color="#7c3aed", label="recovered T (cubic fit)")
ax2b.set_ylabel("recovered T (degC)", color="#7c3aed")
plt.tight_layout()
plt.show()

print(f"bridge sensitivity ~ {Vout[-1] * 1000 / (strain[-1] * 1e6):.4f} mV per microstrain")
print(f"cubic-fit max temperature error = {max_err:.3f} degC")

# Try it yourself:
#   1. Use a half-bridge (two active arms) -> double the output, less curvature.
#   2. Fit a quadratic instead of a cubic and watch max_err grow.
""",
        ),
    ),
)


# -- Sensors & Instrumentation -- Intermediate ---------------------------------

_SENSORS_INTERMEDIATE = SeedCourse(
    slug="sensors-intermediate",
    title="Sensors & Instrumentation -- Intermediate: Data Acquisition",
    description=(
        "Turning analog into digital and back: the ADC (sampling, quantization, "
        "LSB, SAR vs sigma-delta vs flash, ENOB), the DAC and zero-order-hold "
        "reconstruction, anti-aliasing and Nyquist sampling theory with "
        "oversampling/decimation, digital filtering (moving average, IIR, a "
        "Kalman intro), and DAQ system design - dual MATLAB/Python, interactive "
        "plots, and a runnable quantization/oversampling lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The ADC: sampling & quantization",
            "12 min",
            """\
# The ADC: sampling & quantization

The **analog-to-digital converter** (ADC) is where the physical world becomes
numbers. It does two distinct things, and confusing them causes most beginner
errors:

1. **Sampling** - chopping the continuous signal into snapshots at a fixed rate
   $f_s$ (sampling in **time**).
2. **Quantization** - rounding each snapshot to the nearest of a finite set of
   levels (sampling in **amplitude**).

```mermaid
flowchart LR
  A["analog signal"] --> SH["sample & hold"]
  SH --> Q["quantize to levels"]
  Q --> D["digital code"]
```

## Resolution and the LSB

An $N$-bit ADC has $2^N$ levels spanning its reference voltage $V_{ref}$. The
smallest step, the **least significant bit** (LSB), is

$$\\text{LSB} = \\frac{V_{ref}}{2^N}.$$

A 12-bit ADC over 3.3 V has 4096 levels and an LSB of about 0.8 mV. More bits =
finer staircase. Watch the staircase get smoother as bits increase:

```plot
{"title": "Quantization staircase: a ramp digitized at N bits (slide N)", "xLabel": "input (fraction of full scale)", "yLabel": "quantized output", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "controls": [{"name": "N", "range": [1, 5], "value": 3, "label": "resolution bits N"}], "functions": [{"expr": "floor(x*pow(2,N))/pow(2,N)", "label": "quantized ramp"}, {"expr": "x", "label": "ideal", "color": "#94a3b8"}]}
```

## Quantization error

Rounding introduces an error of at most half an LSB. Treated as noise, it limits
the best possible **signal-to-noise ratio** of an ideal converter:

$$\\text{SNR}_{max} \\approx 6.02\\,N + 1.76 \\ \\text{dB}.$$

Every extra bit buys you about 6 dB. The sawtooth error between input and
quantized output is the quantization noise (slide bits to shrink it):

```plot
{"title": "Quantization error sawtooth (slide bits N)", "xLabel": "input (fraction of full scale)", "yLabel": "error (LSB)", "xRange": [0, 1], "yRange": [-0.1, 1.1], "grid": true, "controls": [{"name": "N", "range": [2, 6], "value": 4, "label": "bits N"}], "functions": [{"expr": "(x - floor(x*pow(2,N))/pow(2,N))*pow(2,N)", "label": "error in LSBs"}]}
```

## ADC architectures: pick your trade-off

| Type | Speed | Resolution | How it works | Use |
|------|-------|-----------|--------------|-----|
| **Flash** | fastest | low (8 bit) | $2^N - 1$ comparators at once | scopes, RF |
| **SAR** | medium | 8-18 bit | binary search, one bit/step | the workhorse MCU ADC |
| **Sigma-delta** | slow | very high (24 bit) | oversample + noise-shape + filter | audio, precision sensors |

## ENOB: the honest resolution

A datasheet might say 16 bits, but real noise and distortion mean fewer
*effective* bits. The **effective number of bits** comes from the measured SNR:

$$\\text{ENOB} = \\frac{\\text{SNR}_{dB} - 1.76}{6.02}.$$

```matlab
N = 12; Vref = 3.3;
lsb = Vref / 2^N;                 % ~0.806 mV
snr_max = 6.02*N + 1.76;          % ~74 dB ideal
```

```python
N, Vref = 12, 3.3
lsb = Vref / 2**N                 # ~0.806 mV
snr_max = 6.02*N + 1.76           # ~74 dB ideal
```

> **Practical insight:** don't pay for bits you can't use - if your front-end
> noise is 1 mV, a 16-bit ADC over 3.3 V (50 microvolt LSB) is wasted. Match the
> ADC's ENOB to your signal's real noise floor.

**Next:** going the other way - the DAC and reconstruction.
""",
        ),
        _t(
            "The DAC & signal reconstruction",
            "11 min",
            """\
# The DAC & signal reconstruction

The **digital-to-analog converter** (DAC) does the inverse of the ADC: it turns a
stream of numbers back into a voltage. It is how a music player makes sound, how
a microcontroller generates a control voltage, and how a function generator
builds waveforms.

## Zero-order hold: the staircase

The simplest and most common DAC behaviour is the **zero-order hold** (ZOH): each
sample's value is *held constant* until the next sample arrives, producing a
**staircase** approximation of the smooth signal.

```plot
{"title": "Zero-order hold: held samples approximate a sine (slide samples/cycle)", "xLabel": "time (samples)", "yLabel": "amplitude", "xRange": [0, 20], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "n", "range": [4, 16], "value": 8, "label": "samples per cycle"}], "functions": [{"expr": "sin(2*pi*x/20)", "label": "ideal", "color": "#94a3b8"}, {"expr": "sin(2*pi*floor(x*n/20)/n)", "label": "ZOH staircase", "color": "#2563eb"}]}
```

## Why the staircase needs filtering

The staircase contains the wanted signal **plus** high-frequency images
(harmonics of the sample rate). A **reconstruction filter** (a low-pass after the
DAC) smooths the steps and removes those images, recovering the intended smooth
waveform. The ZOH itself also imposes a gentle $\\mathrm{sinc}$-shaped droop:

$$H_{ZOH}(f) = \\mathrm{sinc}\\!\\left(\\frac{f}{f_s}\\right) = \\frac{\\sin(\\pi f / f_s)}{\\pi f / f_s}.$$

This sinc roll-off slightly attenuates the top of the band - high-end DACs
compensate for it digitally:

```plot
{"title": "Zero-order-hold sinc droop across the band", "xLabel": "frequency / fs", "yLabel": "gain", "xRange": [0, 0.5], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "abs(sin(pi*x)/(pi*x))", "label": "sinc(f/fs) ZOH response"}]}
```

```mermaid
flowchart LR
  D["digital samples"] --> DAC["DAC (zero-order hold)"]
  DAC --> LPF["reconstruction low-pass"]
  LPF --> OUT["smooth analog out"]
```

## DAC architectures (briefly)

- **R-2R ladder** - a resistor network sums binary-weighted contributions; simple
  and fast.
- **Sigma-delta** - oversamples and noise-shapes, like its ADC cousin; standard
  in audio for high resolution at low cost.
- **PWM as a poor man's DAC** - a microcontroller toggles a pin fast and an RC
  filter averages it into an analog level.

```matlab
fs = 8; t = 0:1/fs:1-1/fs;
x = sin(2*pi*t);                  % 8 samples of one cycle
held = repelem(x, 4);             % crude zero-order hold (4x upsample)
```

```python
import numpy as np
fs = 8; t = np.arange(0, 1, 1/fs)
x = np.sin(2*np.pi*t)             # 8 samples of one cycle
held = np.repeat(x, 4)            # crude zero-order hold
```

> **Practical insight:** a DAC without a reconstruction filter sounds and behaves
> "edgy" because of the image frequencies. The ZOH plus a good low-pass is what
> makes the output smooth.

**Next:** the rule you must never break - the sampling theorem.
""",
        ),
        _t(
            "Anti-aliasing & sampling theory",
            "12 min",
            """\
# Anti-aliasing & sampling theory

There is one rule in data acquisition you can never cheat: the **Nyquist-Shannon
sampling theorem**. Break it and your data lies to you in a way no amount of
processing can fix.

## The Nyquist rate

To capture a signal faithfully, you must sample at **more than twice** its
highest frequency component:

$$f_s > 2 f_{max}, \\qquad f_{Nyquist} = \\frac{f_s}{2}.$$

Anything above $f_s/2$ does not simply get lost - it **folds back** (aliases) and
masquerades as a *lower* frequency, contaminating your data. The classic example
is a wagon wheel that appears to spin backwards on film.

## Aliasing in one picture

A high-frequency sine, sampled too slowly, looks identical to a low-frequency
one. Slide the true frequency up past Nyquist and watch the apparent (aliased)
frequency fold back down:

```plot
{"title": "Aliasing: true vs apparent frequency for fs = 10 (slide true f)", "xLabel": "true frequency f (Hz)", "yLabel": "apparent frequency (Hz)", "xRange": [0, 20], "yRange": [0, 6], "grid": true, "controls": [{"name": "fs", "range": [8, 12], "value": 10, "label": "sample rate fs (Hz)"}], "functions": [{"expr": "abs(x - fs*round(x/fs))", "label": "apparent (folded) frequency"}]}
```

Notice the apparent frequency rises to $f_s/2$, then folds back down - that fold
is the alias. Below Nyquist the line is just $y = x$ (faithful); above it, lies.

## The anti-aliasing filter

Since aliasing is irreversible *after* sampling, you must remove the offending
high frequencies **before** the ADC with an analog low-pass **anti-aliasing
filter**, with its cutoff below $f_s/2$. This is a hard analog requirement - no
DSP can undo aliasing once it's happened.

```mermaid
flowchart LR
  S["sensor signal"] --> AAF["anti-alias low-pass (below fs/2)"]
  AAF --> ADC["ADC at fs"]
  ADC --> DSP["digital processing"]
```

## Oversampling and decimation

Sampling **much faster** than Nyquist (oversampling) spreads the fixed
quantization noise power over a wider band, so less of it lands in your signal
band. Then **decimating** (digitally low-pass filtering and downsampling) keeps
the signal but discards the out-of-band noise. The payoff: every **4x**
oversampling adds about **1 bit** of resolution.

$$\\Delta\\text{ENOB} = \\tfrac{1}{2}\\log_2(\\text{OSR}).$$

```plot
{"title": "Oversampling resolution gain: extra bits vs oversampling ratio", "xLabel": "oversampling ratio OSR", "yLabel": "extra effective bits", "xRange": [1, 256], "yRange": [0, 4.5], "grid": true, "functions": [{"expr": "0.5*log2(x)", "label": "+0.5 log2(OSR) bits"}]}
```

```matlab
fmax = 1000;                      % highest signal frequency
fs_min = 2*fmax;                  % Nyquist rate (use margin in practice)
OSR = 64;
extra_bits = 0.5*log2(OSR);       % +3 bits
```

```python
import numpy as np
fmax = 1000
fs_min = 2*fmax
OSR = 64
extra_bits = 0.5*np.log2(OSR)     # +3 bits
```

> **Practical insight:** in real life sample at **5-10x** the highest frequency,
> not the bare 2x - it relaxes the anti-aliasing filter and leaves margin. The
> 2x figure is a hard floor, never a target.

**Next:** cleaning up the sampled data - digital filtering.
""",
        ),
        _t(
            "Digital filtering of sensor data",
            "12 min",
            """\
# Digital filtering of sensor data

Once the signal is sampled, you can clean it with **digital filters** - pure
arithmetic on the sample stream, with no drifting components and perfectly
repeatable behaviour. This is where most real noise reduction happens today.

## The moving average (a simple FIR filter)

Average the last $M$ samples. It is the simplest **low-pass** filter: smooths
noise, but blurs sharp edges and adds delay. A longer window smooths harder.
Averaging $M$ independent samples reduces random noise by $\\sqrt{M}$:

```plot
{"title": "Noise reduction by averaging: residual noise vs window length M", "xLabel": "window length M (samples)", "yLabel": "relative noise", "xRange": [1, 64], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "noise scales as 1/sqrt(M)"}]}
```

## IIR filters: more punch, less compute

An **infinite impulse response** (IIR) filter feeds its own output back, so a few
coefficients give a sharp response. The simplest is the **exponential moving
average** (a one-pole low-pass):

$$y[n] = \\alpha\\,x[n] + (1 - \\alpha)\\,y[n-1].$$

Small $\\alpha$ = heavy smoothing and slow response; large $\\alpha$ = light
smoothing and fast response. Slide $\\alpha$ to see how fast the filter chases a
step input:

```plot
{"title": "Exponential moving average step response (slide alpha)", "xLabel": "samples after step", "yLabel": "filter output", "xRange": [0, 40], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "alpha", "range": [0.05, 0.8], "value": 0.2, "label": "smoothing factor alpha"}], "functions": [{"expr": "1 - pow(1-alpha, x)", "label": "EMA chasing a step"}]}
```

| Filter | Memory | Sharpness | Cost | Phase |
|--------|--------|-----------|------|-------|
| **Moving average** (FIR) | finite | gentle | $M$ adds | linear (good) |
| **EMA / IIR** | infinite | sharp per coeff | very cheap | nonlinear |

## A first taste of the Kalman filter

The **Kalman filter** is the optimal estimator when you have a **model** of how
the signal should evolve plus noisy measurements. Each step it **predicts** from
the model, then **corrects** with the new measurement, weighting the two by their
uncertainties (the **Kalman gain**). For a constant value it reduces to a clever
adaptive average; the full version (Advanced course) tracks moving states like
position and velocity.

```mermaid
stateDiagram-v2
  [*] --> Predict
  Predict --> Update: new measurement
  Update --> Predict: next step
  Update --> [*]
```

```matlab
% Exponential moving average over a noisy vector x
alpha = 0.2; y = zeros(size(x)); y(1) = x(1);
for n = 2:numel(x)
    y(n) = alpha*x(n) + (1-alpha)*y(n-1);
end
```

```python
import numpy as np
alpha = 0.2
y = np.zeros_like(x); y[0] = x[0]
for n in range(1, len(x)):
    y[n] = alpha*x[n] + (1-alpha)*y[n-1]
```

> **Practical insight:** every filter trades **noise reduction for delay**. More
> smoothing always means more lag - choose the lightest filter that meets your
> noise spec, especially in a control loop where lag causes instability.

**Next:** the whole acquisition system - interfaces and DAQ.
""",
        ),
        _t(
            "Sensor interfaces & DAQ systems",
            "11 min",
            """\
# Sensor interfaces & DAQ systems

A **data acquisition** (DAQ) system is the full chain from physical phenomenon to
stored numbers. Real systems are built from standard building blocks, and knowing
the blocks lets you read any datasheet.

```mermaid
flowchart LR
  SENS["sensor"] --> AFE["analog front-end (amp + filter)"]
  AFE --> MUX["multiplexer"]
  MUX --> SH["sample & hold"]
  SH --> ADC["ADC"]
  ADC --> MCU["MCU / processor"]
  MCU --> LOG["storage / network"]
```

## The analog front-end (AFE)

The AFE is everything between the sensor and the ADC: amplification,
filtering/anti-aliasing, level shifting, and often a **multiplexer** so one ADC
can serve many channels in turn. Integrated AFE chips bundle all of this for a
specific sensor class (bridges, thermocouples, biopotentials).

## Digital sensor interfaces: I2C and SPI

Many modern sensors do the conversion *inside the chip* and hand you a digital
number over a serial bus:

| Bus | Wires | Speed | Devices | Best for |
|-----|-------|-------|---------|----------|
| **I2C** | 2 (SDA, SCL) | ~0.1-3.4 MHz | many (addressed) | slow sensors, many on one bus |
| **SPI** | 4 (MOSI/MISO/SCK/CS) | tens of MHz | per chip-select | fast ADCs, displays |

I2C trades speed for wiring simplicity (two shared wires, each device has an
address); SPI is faster but needs a chip-select line per device.

## Sample timing matters

The **sample rate** must clear Nyquist for your fastest signal, but timing
*quality* matters too. **Jitter** (random variation in when samples are taken)
acts like noise, worse at high frequencies. For multi-channel systems, decide
whether channels are **simultaneously sampled** (each has its own sample-and-hold
- vital for phase between channels) or **multiplexed** (read in sequence, with a
small skew between channels).

```plot
{"title": "Channel scan timing: a 4-channel multiplexed acquisition", "xLabel": "time (microseconds)", "yLabel": "channel", "xRange": [0, 40], "yRange": [0, 5], "grid": true, "series": [{"points": [[2, 1], [12, 2], [22, 3], [32, 4]], "label": "sample instants (one per channel)", "color": "#2563eb"}]}
```

```matlab
fs = 1000;                        % 1 kHz per channel
nch = 4;
mux_rate = fs*nch;                % ADC must run 4 kHz to scan 4 channels
sample_period = 1/fs;             % 1 ms between samples of a given channel
```

```python
fs, nch = 1000, 4
mux_rate = fs*nch                 # ADC scans all channels
sample_period = 1/fs              # 1 ms per channel sample
```

> **Practical insight:** if you need true phase relationships between channels
> (e.g. power measurement, vibration with multiple accelerometers), insist on
> **simultaneous sampling** - a multiplexed scan introduces a channel-to-channel
> time skew that corrupts phase.

**Next:** see quantization noise and oversampling gain for yourself.
""",
        ),
        _code(
            "Lab: ADC quantization noise & oversampling gain",
            "13 min",
            """\
# Quantize a sine with a low-resolution ADC, measure the quantization SNR,
# then show that oversampling + averaging recovers effective bits.
# numpy + matplotlib only, module level only.
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

# --- A signal sampled at a high rate ---
fsig = 50.0          # signal frequency (Hz)
fs = 20000.0         # base sample rate (Hz)
T = 0.1              # seconds
t = np.arange(0, T, 1.0 / fs)
Vfs = 1.0            # full scale (+/-Vfs)
x = 0.9 * Vfs * np.sin(2 * np.pi * fsig * t)

# --- Quantize to a low resolution (N bits) ---
N = 6
levels = 2 ** N
lsb = 2.0 * Vfs / levels
xq = np.round(x / lsb) * lsb                 # mid-tread quantizer
qnoise = xq - x
snr_meas = 10 * np.log10(np.mean(x ** 2) / np.mean(qnoise ** 2))
enob = (snr_meas - 1.76) / 6.02

# --- Oversampling gain: block-average groups of OSR samples ---
osr_list = [1, 4, 16, 64]
enob_gain = []
for OSR in osr_list:
    n = (len(xq) // OSR) * OSR
    blocks = xq[:n].reshape(-1, OSR).mean(axis=1)     # decimate by averaging
    xref = x[:n].reshape(-1, OSR).mean(axis=1)
    err = blocks - xref
    snr = 10 * np.log10(np.mean(xref ** 2) / np.mean(err ** 2))
    enob_gain.append((snr - 1.76) / 6.02)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(t * 1000, x, color="#94a3b8", label="analog")
ax1.step(t * 1000, xq, where="mid", color="#dc2626", label=f"{N}-bit quantized")
ax1.set_xlim(0, 20)
ax1.set_xlabel("time (ms)")
ax1.set_ylabel("voltage (V)")
ax1.set_title(f"{N}-bit quantization (measured ENOB ~ {enob:.1f})")
ax1.legend()
ax1.grid(True)

theory = [enob_gain[0] + 0.5 * np.log2(o) for o in osr_list]
ax2.plot(osr_list, enob_gain, "o-", color="#2563eb", label="measured ENOB")
ax2.plot(osr_list, theory, "s--", color="#16a34a", label="theory: +0.5 log2(OSR)")
ax2.set_xscale("log", base=2)
ax2.set_xlabel("oversampling ratio OSR")
ax2.set_ylabel("effective bits (ENOB)")
ax2.set_title("Oversampling buys resolution")
ax2.legend()
ax2.grid(True)
plt.tight_layout()
plt.show()

print(f"ideal SNR for {N} bits = {6.02*N + 1.76:.1f} dB")
print(f"measured SNR = {snr_meas:.1f} dB  ->  ENOB = {enob:.2f} bits")
print(f"ENOB at OSR=64 = {enob_gain[-1]:.2f} bits (gained ~{enob_gain[-1]-enob_gain[0]:.1f})")

# Try it yourself:
#   1. Set N = 4 (coarser): SNR drops about 12 dB (2 bits x 6 dB).
#   2. Add a tiny dither: x += 0.5*lsb*np.random.randn(len(x)) before quantizing.
""",
        ),
    ),
)


# -- Sensors & Instrumentation -- Advanced -------------------------------------

_SENSORS_ADVANCED = SeedCourse(
    slug="sensors-advanced",
    title="Sensors & Instrumentation -- Advanced: Fusion & Precision",
    description=(
        "High-end measurement: sensor fusion and estimation (Kalman and "
        "complementary filters), calibration/linearization/compensation for "
        "drift, precision and low-noise techniques (lock-in, chopping, "
        "averaging, shielding), MEMS and modern sensors (accelerometer, gyro, "
        "IMU, pressure, optical, Hall), and instrumentation systems and standards "
        "(DAQ, SCADA, IoT) - dual MATLAB/Python, interactive plots, a runnable "
        "fusion lab, and a real-world applications tour."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Sensor fusion & estimation",
            "13 min",
            """\
# Sensor fusion & estimation

No single sensor is perfect. **Sensor fusion** combines several imperfect sensors
into one estimate that is better than any of them alone - by playing each
sensor's strengths against the others' weaknesses. Your phone's orientation, a
drone's stability, and a car's self-driving stack all live or die by fusion.

## The complementary pair

The canonical example fuses a **gyroscope** and an **accelerometer** to estimate
tilt angle:

- The **gyro** gives smooth, fast angle changes but **drifts** slowly (integrating
  a small bias).
- The **accelerometer** gives a drift-free absolute angle but is **noisy** and
  corrupted by motion.

They fail in opposite frequency bands, so combine them in a **complementary
filter**: trust the gyro at high frequency, the accelerometer at low frequency.

$$\\theta = \\alpha\\,(\\theta + \\dot{\\theta}_{gyro}\\,\\Delta t) + (1 - \\alpha)\\,\\theta_{accel}.$$

The two weighting curves cross over and always sum to one - that's why it's
called *complementary*:

```plot
{"title": "Complementary filter weighting vs frequency (slide blend alpha)", "xLabel": "frequency (relative)", "yLabel": "weight", "xRange": [0.01, 10], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "fc", "range": [0.2, 3], "value": 1, "label": "crossover frequency"}], "functions": [{"expr": "x/sqrt(x*x + fc*fc)", "label": "gyro (high-pass)", "color": "#2563eb"}, {"expr": "fc/sqrt(x*x + fc*fc)", "label": "accel (low-pass)", "color": "#dc2626"}]}
```

## The Kalman filter

The **Kalman filter** is the optimal fusion engine for linear systems with
Gaussian noise. It carries a **state estimate** and its **uncertainty** (a
covariance), and each step:

1. **Predict** - advance the state with a motion model; uncertainty grows.
2. **Update** - blend in the new measurement, weighted by the **Kalman gain** $K$,
   which leans toward whichever (prediction or measurement) is more trusted.

$$K = \\frac{P^-}{P^- + R}, \\qquad \\hat{x} = \\hat{x}^- + K\\,(z - \\hat{x}^-).$$

```mermaid
stateDiagram-v2
  [*] --> Predict
  Predict --> Update: measurement z
  Update --> Predict: next time step
```

A 1-D Kalman filter converging on a true constant from noisy measurements - the
estimate settles, and the uncertainty (shaded idea) shrinks each step:

```plot
{"title": "1-D Kalman estimate converging to a true value of 10", "xLabel": "step", "yLabel": "value", "xRange": [0, 12], "yRange": [6, 14], "grid": true, "functions": [{"expr": "10", "label": "true value", "color": "#16a34a"}], "series": [{"points": [[1, 8.2], [2, 11.8], [3, 9.1], [4, 10.9], [5, 9.4], [6, 10.6], [7, 9.7], [8, 10.3], [9, 9.9], [10, 10.1]], "label": "noisy measurements", "color": "#94a3b8"}, {"points": [[1, 8.2], [2, 9.6], [3, 9.5], [4, 9.9], [5, 9.8], [6, 10.0], [7, 9.9], [8, 10.0], [9, 10.0], [10, 10.0]], "label": "Kalman estimate", "color": "#dc2626"}]}
```

```matlab
% One complementary-filter step (dt seconds)
alpha = 0.98;
theta = alpha*(theta + gyro*dt) + (1-alpha)*accel_angle;
```

```python
alpha = 0.98
theta = alpha*(theta + gyro*dt) + (1-alpha)*accel_angle
```

> **Practical insight:** the complementary filter is a cheap, intuitive cousin of
> the Kalman filter - one tuning knob, no matrix algebra, and it runs on the
> smallest microcontroller. Reach for full Kalman only when you need optimality
> or are tracking several coupled states.

**Next:** keeping a sensor honest over its life - calibration and compensation.
""",
        ),
        _t(
            "Calibration, linearization & compensation",
            "12 min",
            """\
# Calibration, linearization & compensation

A sensor's raw output is rarely the final answer. **Calibration** corrects for
its imperfections, **linearization** straightens its curve, and **compensation**
removes the influence of unwanted variables - chiefly temperature.

## Linearization: straightening the curve

Most sensors are nonlinear (the NTC thermistor from the Basics course is a prime
example). Two practical approaches:

- **Polynomial fit** - fit $y = a_0 + a_1 x + a_2 x^2 + \\dots$ to calibration data
  and evaluate it in software.
- **Lookup table (LUT) + interpolation** - store measured points and linearly
  interpolate between them. Cheap, fast, and handles any shape.

A cubic polynomial corrects a curved sensor back onto the ideal straight line:

```plot
{"title": "Polynomial linearization corrects a curved sensor", "xLabel": "true input", "yLabel": "reading", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "10*sqrt(x/10)", "label": "raw (curved) reading", "color": "#dc2626"}, {"expr": "x", "label": "after linearization", "color": "#16a34a"}]}
```

## Compensation: temperature is everyone's enemy

Almost every sensor drifts with temperature. Two parameters drift:

- **Offset/zero drift** - the output at zero input wanders with $T$.
- **Span/sensitivity drift** - the slope changes with $T$.

You compensate by measuring the temperature too (an on-chip sensor) and applying a
correction: $y_{corr} = (y_{raw} - \\text{offset}(T)) / \\text{gain}(T)$. Without it,
a pressure sensor calibrated at 25 C reads wrong on a cold morning. Slide the
temperature and watch an uncompensated zero drift away:

```plot
{"title": "Uncompensated offset drift vs temperature (slide temp coefficient)", "xLabel": "temperature (degC)", "yLabel": "zero-offset error (mV)", "xRange": [-20, 80], "yRange": [-30, 30], "grid": true, "controls": [{"name": "tc", "range": [0.1, 0.6], "value": 0.3, "label": "drift coefficient (mV/degC)"}], "functions": [{"expr": "tc*(x - 25)", "label": "offset error vs T"}]}
```

## Multi-point calibration

A single gain/offset (two-point) calibration only fixes a straight line. For a
curved sensor, calibrate at **many** points across the range and fit, or build the
LUT. The residual after fitting is your **calibration uncertainty**.

```mermaid
flowchart LR
  RAW["raw reading"] --> LIN["linearize (poly / LUT)"]
  TEMP["temperature"] --> COMP["temperature compensation"]
  LIN --> COMP
  COMP --> OUT["calibrated value"]
```

```matlab
% Cubic linearization from calibration data (xcal, ycal)
p = polyfit(ycal, xcal, 3);       % fit input as fn of raw output
x_est = polyval(p, y_raw);        % linearized estimate
```

```python
import numpy as np
p = np.polyfit(ycal, xcal, 3)     # fit input as fn of raw output
x_est = np.polyval(p, y_raw)      # linearized estimate
```

> **Practical insight:** calibrate over the **full operating range and
> temperature**, not just at room temperature - the errors you didn't measure are
> the ones that bite in the field. Re-calibrate periodically; sensors age.

**Next:** pulling tiny signals out of the noise - precision techniques.
""",
        ),
        _t(
            "Precision & low-noise measurement",
            "12 min",
            """\
# Precision & low-noise measurement

Sometimes the signal you want is far **smaller** than the noise around it - a
nanovolt buried in microvolts of hum. Precision measurement is a toolkit of
tricks that recover such signals, used everywhere from gravitational-wave
detectors to medical instruments.

## Averaging: the free lunch (almost)

Random noise is uncorrelated between samples, so averaging $N$ samples improves
SNR by $\\sqrt{N}$. It is the simplest precision tool - but it costs **time**, and
it only helps with *random* noise, not systematic offsets.

```plot
{"title": "SNR improvement from averaging N samples", "xLabel": "samples averaged N", "yLabel": "SNR gain (dB)", "xRange": [1, 1000], "yRange": [0, 35], "grid": true, "functions": [{"expr": "10*log10(x)", "label": "10 log10(N) dB"}]}
```

## The lock-in amplifier: the king of small signals

A **lock-in amplifier** measures a signal at a known **reference frequency**,
rejecting everything else - it can pull a signal out of noise a thousand times
larger. The trick is **modulation** then **synchronous detection**:

1. **Modulate** the measurement at a reference frequency $f_{ref}$ (e.g. chop a
   light beam, or excite a bridge with an AC source).
2. **Multiply** the noisy input by a reference at $f_{ref}$ and low-pass filter.
   Only signal components *at* $f_{ref}$ survive; noise at other frequencies
   averages to zero.

This moves your measurement to a quiet part of the spectrum, away from DC drift
and low-frequency **1/f noise** - which dominates near DC:

```plot
{"title": "Noise spectrum: 1/f noise near DC, why we modulate up (slide fref)", "xLabel": "frequency (Hz)", "yLabel": "noise density", "xRange": [1, 1000], "yRange": [0, 6], "grid": true, "controls": [{"name": "fref", "range": [50, 800], "value": 400, "label": "modulation frequency fref"}], "functions": [{"expr": "5/sqrt(x) + 0.5", "label": "1/f + white noise"}, {"expr": "(abs(x-fref)<20)*5", "label": "narrow lock-in band", "color": "#16a34a"}]}
```

## Chopping and auto-zeroing

**Chopper stabilization** rapidly swaps an amplifier's inputs and corrects its
slow **offset and 1/f noise** by modulating the signal above the noisy region,
amplifying, then demodulating back. Chopper and auto-zero op-amps achieve
microvolt-level offsets - essential for thermocouples and bridges.

## And don't forget the basics

All the noise/grounding rules from the Basics course apply with a vengeance:
**shielding**, **guarding**, twisted differential pairs, single-point grounds,
bandwidth-limiting filters, and keeping sensitive nodes low-impedance. Precision
is won at the wiring as much as in the chip.

```matlab
% Synchronous (lock-in) detection: multiply by reference, then low-pass
ref = sin(2*pi*fref*t);
mixed = signal .* ref;            % shifts signal to DC
detected = movmean(mixed, 200);   % low-pass -> amplitude estimate
```

```python
import numpy as np
ref = np.sin(2*np.pi*fref*t)
mixed = signal * ref              # shifts signal to DC
detected = np.convolve(mixed, np.ones(200)/200, mode="same")  # low-pass
```

> **Practical insight:** the single most powerful precision idea is **modulate
> away from DC**: move your measurement to a frequency where the world is quiet,
> measure there, and bring it back. That's the lock-in, the chopper, and AC bridge
> excitation all in one sentence.

**Next:** the sensors inside every modern device - MEMS.
""",
        ),
        _t(
            "MEMS & modern sensors",
            "12 min",
            """\
# MEMS & modern sensors

**MEMS** (micro-electro-mechanical systems) put tiny mechanical structures -
springs, masses, beams - on a silicon chip alongside the electronics. They made
motion sensing cheap and ubiquitous: the accelerometer in your phone costs cents
and is a microscopic mass on silicon springs.

## The motion sensors

| Sensor | Measures | MEMS principle | Found in |
|--------|----------|----------------|----------|
| **Accelerometer** | linear acceleration (and gravity) | mass on springs, capacitance changes | phones, airbags, fitness |
| **Gyroscope** | angular rate | vibrating mass, Coriolis force | drones, image stabilization |
| **Magnetometer** | magnetic field/heading | Hall or magnetoresistive | compass apps |

A MEMS accelerometer is a damped spring-mass: deflection is proportional to
acceleration (and at DC it reads **gravity**, which is how phones know "down").
Its response has a resonance like any spring-mass system - slide the damping:

```plot
{"title": "MEMS accelerometer frequency response (slide damping)", "xLabel": "frequency / resonance", "yLabel": "response", "xRange": [0.1, 3], "yRange": [0, 6], "grid": true, "controls": [{"name": "zeta", "range": [0.1, 1], "value": 0.7, "label": "damping ratio zeta"}], "functions": [{"expr": "1/sqrt((1 - x*x)^2 + (2*zeta*x)^2)", "label": "|H(f)|"}]}
```

## The IMU: fusion on a chip

Combine a 3-axis accelerometer + 3-axis gyro (+ often a magnetometer) and you get
an **inertial measurement unit** (IMU). On its own a gyro **drifts** and an
accelerometer is **noisy** - so the IMU runs **sensor fusion** (the complementary
or Kalman filter from earlier) to output a clean, drift-free orientation. This is
the heart of drone flight controllers, VR headsets, and pedestrian dead-reckoning.

## Other modern sensors

- **Pressure** - MEMS piezoresistive/capacitive diaphragms: altimeters, weather,
  blood-pressure cuffs, car manifold sensors.
- **Optical** - photodiodes and image sensors (CMOS cameras), time-of-flight
  (lidar, phone face-unlock), optical encoders.
- **Hall effect** - measures magnetic field via the Hall voltage; contactless
  current sensing, position/speed (every brushless motor), and proximity.

```mermaid
flowchart LR
  ACC["3-axis accel"] --> FUSE["fusion (Kalman / complementary)"]
  GYRO["3-axis gyro"] --> FUSE
  MAG["magnetometer"] --> FUSE
  FUSE --> ORI["orientation estimate"]
```

```matlab
% Hall sensor: output voltage proportional to field B and bias current I
Vhall = Kh * I * B;               % Kh = Hall coefficient / thickness
```

```python
Vhall = Kh * I * B                # Hall voltage from current I, field B
```

> **Practical insight:** MEMS sensors are cheap and tiny but have real offsets,
> temperature drift, and noise - they only become *trustworthy* after calibration
> and fusion. The magic of a phone's rock-steady orientation is mostly software.

**Next:** how all of this scales into real systems and standards.
""",
        ),
        _t(
            "Instrumentation systems & standards",
            "11 min",
            """\
# Instrumentation systems & standards

A single sensor is a hobby project; a **system** of thousands of sensors running
a factory, a hospital, or a city is engineering. This lesson is about the
architectures and standards that scale measurement up.

## DAQ systems

A **DAQ** (data acquisition) system bundles signal conditioning, multiplexing,
ADCs, and a host interface (USB, Ethernet, PCIe). Bench and lab DAQ hardware
(National Instruments, etc.) is programmed in **LabVIEW**, MATLAB's Data
Acquisition Toolbox, or Python (`nidaqmx`, `pyvisa`). Key system choices:
channel count, per-channel rate, simultaneous vs multiplexed sampling, and
isolation.

## SCADA and industrial control

**SCADA** (Supervisory Control And Data Acquisition) is how industrial plants
monitor and control distributed processes - pipelines, power grids, water
treatment. Sensors feed **PLCs** (programmable logic controllers) and **RTUs**
(remote terminal units), which report to a central supervisory system over
industrial protocols (Modbus, PROFIBUS, OPC-UA).

```mermaid
flowchart TB
  S["field sensors"] --> PLC["PLC / RTU"]
  PLC --> SCADA["SCADA supervisory system"]
  SCADA --> HMI["operator HMI"]
  SCADA --> HIST["data historian"]
```

## IoT sensing

The **Internet of Things** pushes sensing to the network edge: low-power
microcontrollers with wireless links (Wi-Fi, BLE, LoRa, cellular NB-IoT) stream
sensor data to the cloud. The defining constraint is **energy** - a battery
sensor must sleep most of the time and wake briefly to measure and transmit.
**Duty cycling** is everything; lower duty cycle means longer battery life:

```plot
{"title": "IoT battery life vs duty cycle (slide sleep current)", "xLabel": "duty cycle (percent active)", "yLabel": "relative battery life", "xRange": [0.1, 10], "yRange": [0, 11], "grid": true, "controls": [{"name": "isleep", "range": [0.01, 0.2], "value": 0.05, "label": "sleep current (relative)"}], "functions": [{"expr": "1/(x/100 + isleep)", "label": "battery life"}]}
```

## Standards keep it trustworthy

- **SI units and traceability** (from Basics) underpin every credible reading.
- **Calibration standards** (ISO 17025 labs) certify instruments.
- **Communication standards** (IEEE 1451 smart transducers, OPC-UA, MQTT for IoT)
  let heterogeneous devices interoperate.
- **Safety/EMC standards** govern medical and industrial measurement.

```matlab
duty = 0.02; i_active = 50e-3; i_sleep = 5e-6;
i_avg = duty*i_active + (1-duty)*i_sleep;   % average current
life_h = 2000e-3 / i_avg;                   % 2000 mAh battery, hours
```

```python
duty, i_active, i_sleep = 0.02, 50e-3, 5e-6
i_avg = duty*i_active + (1-duty)*i_sleep    # average current
life_h = 2.0 / i_avg                        # 2000 mAh battery, hours
```

> **Practical insight:** at system scale the hard problems shift from the single
> measurement to **reliability, synchronization, data volume, and standards
> compliance**. A perfect sensor reading nobody can timestamp, trust, or
> interoperate with is worthless.

**Next:** estimate a state by fusing two sensors yourself.
""",
        ),
        _code(
            "Lab: Kalman & complementary sensor fusion",
            "14 min",
            """\
# Fuse a drifting gyro and a noisy accelerometer to estimate tilt angle, using
# both a complementary filter and a 1-D Kalman filter. numpy + matplotlib only,
# module level only (no user-defined function calls another).
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)

# --- Ground truth: a slow sinusoidal tilt ---
dt = 0.01
t = np.arange(0, 10, dt)
true_angle = 30.0 * np.sin(2 * np.pi * 0.2 * t)           # degrees
true_rate = np.gradient(true_angle, dt)                    # deg/s

# --- Simulated sensors ---
gyro_bias = 2.0                                            # constant drift (deg/s)
gyro = true_rate + gyro_bias + 0.5 * np.random.randn(len(t))
accel_angle = true_angle + 4.0 * np.random.randn(len(t))   # noisy absolute angle

# --- Gyro-only: integrate (drifts away) ---
gyro_only = np.cumsum(gyro) * dt

# --- Complementary filter ---
alpha = 0.98
comp = np.zeros(len(t))
comp[0] = accel_angle[0]
for k in range(1, len(t)):
    comp[k] = alpha * (comp[k - 1] + gyro[k] * dt) + (1 - alpha) * accel_angle[k]

# --- 1-D Kalman filter (state = angle, control = gyro rate) ---
Q = 0.05      # process noise (trust the model)
R = 16.0      # measurement noise (accel variance)
x_est = accel_angle[0]
P = 1.0
kalman = np.zeros(len(t))
kalman[0] = x_est
for k in range(1, len(t)):
    # predict using the gyro rate as a control input
    x_pred = x_est + gyro[k] * dt
    P = P + Q
    # update with the noisy accelerometer angle
    K = P / (P + R)
    x_est = x_pred + K * (accel_angle[k] - x_pred)
    P = (1 - K) * P
    kalman[k] = x_est

rms_gyro = np.sqrt(np.mean((gyro_only - true_angle) ** 2))
rms_accel = np.sqrt(np.mean((accel_angle - true_angle) ** 2))
rms_comp = np.sqrt(np.mean((comp - true_angle) ** 2))
rms_kalman = np.sqrt(np.mean((kalman - true_angle) ** 2))

plt.figure(figsize=(9, 4.5))
plt.plot(t, accel_angle, color="#cbd5e1", lw=0.8, label="accel (noisy)")
plt.plot(t, gyro_only, color="#f59e0b", lw=1, label="gyro integral (drifts)")
plt.plot(t, true_angle, color="#16a34a", lw=2, label="true angle")
plt.plot(t, comp, color="#2563eb", lw=1.5, label="complementary")
plt.plot(t, kalman, color="#dc2626", lw=1.5, label="Kalman")
plt.xlabel("time (s)")
plt.ylabel("tilt angle (deg)")
plt.title("Sensor fusion: gyro + accelerometer -> clean tilt estimate")
plt.legend(loc="upper right")
plt.grid(True)
plt.show()

print(f"RMS error  gyro-only      = {rms_gyro:7.2f} deg (drifts)")
print(f"RMS error  accel-only     = {rms_accel:7.2f} deg (noisy)")
print(f"RMS error  complementary  = {rms_comp:7.2f} deg")
print(f"RMS error  Kalman         = {rms_kalman:7.2f} deg")

# Try it yourself:
#   1. Raise gyro_bias to 10: gyro-only drifts off-screen, fusion still tracks.
#   2. Lower R toward Q: the Kalman filter trusts the noisy accel more -> noisier.
""",
        ),
        _t(
            "Applications: industrial, medical, automotive & IoT",
            "11 min",
            """\
# Applications: industrial, medical, automotive & IoT

Everything in this track - sensors, conditioning, DAQ, fusion, calibration,
precision - comes together in real systems. This closing lesson walks four
domains and shows which ideas matter where.

## Industrial and process control

Factories and plants run on measurement. Temperature (RTDs, thermocouples),
pressure (MEMS, bridge transducers), flow, level, and vibration sensors feed
**PLCs and SCADA** systems. Key concerns: **4-20 mA current loops** (noise-immune
analog transmission over long cables), galvanic **isolation**, ruggedness, and
**predictive maintenance** - fusing vibration + temperature to predict a bearing
failure before it happens.

```mermaid
flowchart LR
  T["temp / pressure / vibration"] --> XMIT["4-20 mA transmitter"]
  XMIT --> PLC["PLC"]
  PLC --> SCADA["SCADA + analytics"]
  SCADA --> MAINT["predictive maintenance"]
```

## Medical instrumentation

Biopotentials are tiny and the patient is a noisy, safety-critical environment.

- **ECG/EEG** - microvolt signals: **instrumentation amplifiers** with very high
  CMRR, driven-right-leg guarding, and isolation for patient safety.
- **Pulse oximetry** - an optical sensor with **lock-in style** modulated LEDs to
  reject ambient light.
- **Infusion and ventilation** - precision flow/pressure with redundant sensors
  and rigorous **calibration/traceability**.

Every precision and noise technique in this course shows up here, because the
signal is small and the stakes are high.

## Automotive

A modern car has **hundreds of sensors**: MEMS accelerometers and gyros (airbags,
stability control, the **IMU** for navigation dead-reckoning), Hall sensors
(wheel speed, throttle position), pressure (tire, manifold, brake), oxygen
(lambda) sensors, and a sensor-fusion stack (camera + radar + lidar + IMU) for
ADAS and self-driving. The bus tying them together is **CAN**; the watchwords are
**reliability, temperature range, and functional safety** (ISO 26262).

The cost of skipping fusion is concrete - a single sensor's error vs the fused
estimate's much smaller error:

```plot
{"title": "Why fuse: single-sensor error vs fused error (slide sensor count)", "xLabel": "measurement run", "yLabel": "position error (m)", "xRange": [0, 10], "yRange": [0, 5], "grid": true, "controls": [{"name": "Nsens", "range": [1, 9], "value": 4, "label": "sensors fused"}], "functions": [{"expr": "3", "label": "single sensor error", "color": "#dc2626"}, {"expr": "3/sqrt(Nsens)", "label": "fused error ~ 1/sqrt(N)", "color": "#16a34a"}]}
```

## IoT and consumer

Smart homes, wearables, and environmental monitoring put low-cost sensors
everywhere, constrained by **energy and connectivity**. A fitness band fuses a
MEMS IMU with optical heart-rate; a smart thermostat fuses temperature, humidity,
and occupancy. The engineering is **duty-cycled low-power** acquisition, on-device
filtering to cut data volume, and cloud aggregation.

## The throughline

Sense the physical quantity, **condition** it (amplify, filter, level-shift),
**digitize** it without aliasing, **filter and fuse** it, **calibrate and
compensate** for the real world, and deliver a number you can **trust and trace**.
The sensors change across industrial, medical, automotive, and IoT domains - but
the measurement chain, and the discipline that makes its numbers trustworthy,
never does.

**Next:** the final check.
""",
        ),
    ),
)


SENSORS_COURSES: tuple[SeedCourse, ...] = (
    _SENSORS_BASICS,
    _SENSORS_INTERMEDIATE,
    _SENSORS_ADVANCED,
)

__all__ = ["SENSORS_COURSES"]
