"""Curated Analog & Mixed-Signal IC Design track: Basics, Intermediate, Advanced.

A complete analog IC curriculum: device-level analog design (the MOSFET
small-signal model, single-stage amplifiers, current mirrors, the differential
pair, frequency response), op-amps and feedback (two-stage op-amp, stability and
compensation, noise, references, switched-capacitor circuits), and mixed-signal
systems (sampling and quantization, DACs, Nyquist ADCs, delta-sigma converters,
PLLs). Dual SPICE + Python focus throughout, with runnable Python labs (numpy +
matplotlib), interactive ```plot blocks, Mermaid diagrams, LaTeX formulas, and
real-world use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time (keyed by the exact lesson titles below).
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Analog & Mixed-Signal IC Design -- Basics ---------------------------------

_ANALOG_BASICS = SeedCourse(
    slug="analog-ic-basics",
    title="Analog & Mixed-Signal IC Design -- Basics",
    description=(
        "Device-level analog design from the transistor up: the MOSFET "
        "small-signal model (gm, ro, regions), single-stage amplifiers, current "
        "mirrors and biasing, the differential pair, and amplifier frequency "
        "response - with side-by-side SPICE and Python, interactive plots, and a "
        "runnable common-source / diff-pair lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The MOSFET as an analog device",
            "12 min",
            """\
# The MOSFET as an analog device

Digital design treats a MOSFET as an on/off switch. **Analog** design lives in
the in-between, where the transistor is a **voltage-controlled current source**.
Master three quantities and you can read any analog datasheet.

## The three regions of operation

| Region | Condition | Drain current $I_D$ |
|--------|-----------|---------------------|
| Cut-off | $V_{GS} < V_{th}$ | ~0 |
| Triode (linear) | $V_{GS} > V_{th}$, $V_{DS} < V_{ov}$ | $\\mu C_{ox}\\frac{W}{L}\\left[(V_{GS}-V_{th})V_{DS} - \\frac{V_{DS}^2}{2}\\right]$ |
| Saturation (active) | $V_{GS} > V_{th}$, $V_{DS} \\ge V_{ov}$ | $\\frac{1}{2}\\mu C_{ox}\\frac{W}{L}(V_{GS}-V_{th})^2(1 + \\lambda V_{DS})$ |

The **overdrive** $V_{ov} = V_{GS} - V_{th}$ is the analog designer's main knob.
Analog amplifiers nearly always bias the device in **saturation**, where $I_D$
depends strongly on $V_{GS}$ and weakly on $V_{DS}$ - exactly a current source
you steer with the gate. The square-law curve (slide the threshold):

```plot
{"title": "NMOS saturation: Id = 0.5 k (Vgs - Vth)^2 (slide Vth)", "xLabel": "Vgs (V)", "yLabel": "Id (mA)", "xRange": [0, 3], "yRange": [0, 10], "grid": true, "controls": [{"name": "Vth", "range": [0.3, 1.2], "value": 0.6, "label": "threshold Vth (V)"}], "functions": [{"expr": "(x>Vth)*2*(x-Vth)^2", "label": "Id (saturation)"}]}
```

## Transconductance gm: the gain engine

**Transconductance** $g_m$ is how much drain current wiggles per gate-voltage
wiggle - the slope of that curve:

$$g_m = \\frac{\\partial I_D}{\\partial V_{GS}} = \\mu C_{ox}\\frac{W}{L}(V_{GS}-V_{th}) = \\frac{2 I_D}{V_{ov}} = \\sqrt{2\\mu C_{ox}\\tfrac{W}{L} I_D}.$$

Those three forms say the same thing differently: for a given current, a
**smaller overdrive gives more $g_m$** (good for gain, bad for headroom and
matching). This single tradeoff drives a huge fraction of analog design choices.

## Output resistance ro: the leak

In an ideal current source $I_D$ would not depend on $V_{DS}$ at all. The real
device has **channel-length modulation**: $I_D$ creeps up with $V_{DS}$, modeled
by a finite output resistance

$$r_o = \\frac{1}{\\lambda I_D}.$$

A higher $r_o$ is a more ideal current source - and, as the next lesson shows, a
higher amplifier gain.

## The small-signal model

For small wiggles around the bias point, replace the transistor with a linear
model: a current source $g_m v_{gs}$ in parallel with $r_o$ (and gate-source/
gate-drain capacitances for the frequency lesson). This linearization is what
makes hand analysis of amplifiers possible.

```mermaid
flowchart LR
  G["gate (vgs)"] --> GM["current source gm*vgs"]
  GM --> D["drain"]
  RO["ro in parallel"] --> D
  S["source"] --> GM
```

## Same calculation, two languages

```spice
* NMOS in saturation - DC operating point and gm
M1 d g 0 0 nmos W=10u L=0.5u
Vgs g 0 0.9
Vds d 0 1.2
.model nmos NMOS (VTO=0.6 KP=120u LAMBDA=0.1)
.op
```

```python
mu_cox_w_l = 120e-6 * (10 / 0.5)   # KP * W/L
vth, vgs, vds = 0.6, 0.9, 1.2
lam = 0.1
vov = vgs - vth                     # overdrive 0.3 V
Id = 0.5 * mu_cox_w_l * vov**2 * (1 + lam * vds)
gm = mu_cox_w_l * vov               # 2*Id/vov
ro = 1 / (lam * Id)
print(Id, gm, ro)
```

**Real-world:** every op-amp, RF low-noise amplifier, ADC comparator, and image
sensor pixel is built from MOSFETs biased exactly like this. The intrinsic gain
$g_m r_o$ of one transistor is the currency of analog IC design.

**Next:** wire one transistor into the three single-stage amplifiers.
""",
        ),
        _t(
            "Single-stage amplifiers",
            "13 min",
            """\
# Single-stage amplifiers

One transistor plus a load makes an amplifier. Which terminal you drive and which
you tap gives three canonical stages, each with a personality.

## Common-source: the voltage gain workhorse

Drive the **gate**, take the output at the **drain**. The small-signal gain is

$$A_v = -g_m (r_o \\parallel R_D) \\xrightarrow{R_D \\to \\infty} -g_m r_o.$$

That $g_m r_o$ is the **intrinsic gain** - the most voltage gain one transistor
can give. It inverts (the minus sign) and has high output resistance. Slide the
load resistance and watch the gain build toward the intrinsic limit:

```plot
{"title": "Common-source gain magnitude = gm*(ro||Rd), gm=2m ro=50k (slide Rd)", "xLabel": "drain load Rd (kohm)", "yLabel": "|Av| (V/V)", "xRange": [1, 200], "yRange": [0, 110], "grid": true, "controls": [{"name": "gm", "range": [1, 4], "value": 2, "label": "gm (mA/V)"}], "functions": [{"expr": "gm*(50*x/(50+x))", "label": "|Av|"}]}
```

## Common-gate: the current buffer

Drive the **source**, take the output at the **drain**, gate held fixed. It has
**low input resistance** ($1/g_m$) and high output resistance - a current buffer.
It is the top half of a **cascode** and the input of many RF amplifiers because
it has no Miller capacitance to limit bandwidth.

## Common-drain (source follower): the voltage buffer

Drive the **gate**, take the output at the **source**. Gain is just **below 1**:

$$A_v = \\frac{g_m R_S}{1 + g_m R_S} \\approx 1.$$

It does not amplify voltage - it amplifies **current/drive**, presenting high
input resistance and low output resistance ($\\approx 1/g_m$). Use it to drive a
heavy load or a long line without loading the previous high-impedance stage.

```mermaid
flowchart LR
  CS["Common-source: gate in, drain out -- high gain, inverting"]
  CG["Common-gate: source in, drain out -- current buffer, wideband"]
  CD["Common-drain: gate in, source out -- voltage buffer, gain ~1"]
```

## The bandwidth tradeoff

Gain is not free. The common-source stage's bandwidth falls as its gain (and
load resistance) rises - the **gain-bandwidth product** is roughly constant. The
next lessons make this precise, but the intuition is already here: a big $R_D$
means big gain and a big output time constant.

```spice
* Common-source amplifier, .ac sweep
M1 out in 0 0 nmos W=20u L=0.5u
Rd out vdd 10k
Vdd vdd 0 1.8
Vin in 0 0.9 AC 1
.model nmos NMOS (VTO=0.6 KP=120u LAMBDA=0.1)
.ac dec 20 1k 1G
```

```python
gm, ro, Rd = 2e-3, 50e3, 10e3
Av_cs = -gm * (ro * Rd) / (ro + Rd)   # common-source, inverting
Av_cd = gm * 1e3 / (1 + gm * 1e3)     # source follower, ~1
Rin_cg = 1 / gm                       # common-gate input resistance
print(Av_cs, Av_cd, Rin_cg)
```

**Real-world:** an audio preamp chains a common-source gain stage into a
source-follower output buffer; a radio front-end uses a common-gate stage for its
wide bandwidth; the source follower is the readout buffer in CMOS camera pixels.

**Next:** how to make the stable bias currents these stages need - current
mirrors.
""",
        ),
        _t(
            "Current mirrors and biasing",
            "12 min",
            """\
# Current mirrors and biasing

Amplifiers need stable **bias currents**, and on a chip you cannot use precise
resistors. The trick: make **one** good reference current, then copy it
everywhere with a **current mirror**.

## The basic mirror

Two matched transistors share a gate-source voltage. If they see the same
$V_{GS}$ they carry the same $I_D$ - so the output transistor **mirrors** the
reference:

$$I_{out} = I_{ref}\\,\\frac{(W/L)_2}{(W/L)_1}.$$

Scale the width ratio and you scale the copied current (a **current scaling**
mirror). Slide the ratio:

```plot
{"title": "Current mirror: Iout = Iref * (W/L ratio), Iref=50uA (slide ratio)", "xLabel": "device count N (output width = N x reference)", "yLabel": "Iout (uA)", "xRange": [0, 8], "yRange": [0, 400], "grid": true, "controls": [{"name": "Iref", "range": [10, 80], "value": 50, "label": "reference current (uA)"}], "functions": [{"expr": "Iref*x", "label": "Iout"}]}
```

## The flaw and the cascode fix

A basic mirror is only as good as its **output resistance** $r_o$: when the
output node moves, channel-length modulation makes the copied current drift. The
**cascode mirror** stacks a second transistor on top, boosting the output
resistance to roughly $g_m r_o^2$ - a far more ideal current source - at the cost
of voltage headroom.

```mermaid
flowchart LR
  IREF["Iref into M1 (diode-connected)"] --> GATE["shared gate node"]
  GATE --> M2["M2 copies the current"]
  M2 --> CASC["cascode M3 on top -> high ro"]
  CASC --> LOAD["biased load"]
```

## Reference currents: where Iref comes from

The mirror copies a current, but something must **set** it. Options: a resistor
from the supply (simple but supply- and temperature-dependent), a **constant-gm**
bias cell (sets $g_m$, not $I$, stabilizing gain), or a **bandgap**-derived
current (Intermediate course) that is nearly supply- and temperature-independent.

```spice
* Basic NMOS current mirror
M1 ref ref 0 0 nmos W=10u L=1u
M2 out ref 0 0 nmos W=20u L=1u
Iref vdd ref 50u
Vdd vdd 0 1.8
.model nmos NMOS (VTO=0.6 KP=120u LAMBDA=0.1)
.op
```

```python
Iref = 50e-6
ratio = 20 / 10                 # (W/L)_2 / (W/L)_1
Iout = Iref * ratio             # 100 uA copied
gm, ro = 2e-3, 50e3
Rout_basic = ro                 # basic mirror
Rout_cascode = gm * ro * ro     # cascode mirror, much higher
print(Iout, Rout_basic, Rout_cascode)
```

**Real-world:** a single bandgap reference in the corner of a chip feeds a tree
of mirrors that bias hundreds of amplifiers, comparators, and oscillators. Mirror
**matching** (layout, sizing) directly sets the offset and accuracy of the whole
system.

**Next:** the most important analog circuit of all - the differential pair.
""",
        ),
        _t(
            "The differential pair",
            "13 min",
            """\
# The differential pair

The **differential pair** is the input of nearly every op-amp, comparator, and
high-speed link. Two matched transistors share a **tail current source**; you
drive their gates with a differential signal and steer the tail current between
the two branches.

## Steering the tail current

For a tail current $I_{SS}$, the two drain currents depend on the differential
input $v_{id} = v_{g1} - v_{g2}$. For small signals it is **linear**; for large
signals the pair **saturates**, dumping all the tail into one side. That smooth
tanh-like steering curve (slide the tail current):

```plot
{"title": "Diff-pair current steering: I1 - I2 vs differential input (slide Iss)", "xLabel": "differential input vid (V)", "yLabel": "output current (uA)", "xRange": [-0.4, 0.4], "yRange": [-220, 220], "grid": true, "controls": [{"name": "Iss", "range": [50, 200], "value": 100, "label": "tail current Iss (uA)"}], "functions": [{"expr": "Iss*tanh(8*x)", "label": "I1 - I2"}]}
```

## Common-mode rejection: the superpower

A differential pair amplifies the **difference** of its inputs and ignores what
they have in **common**. Shift both inputs up by the same amount and the tail
current splits the same way - the output barely moves. The **common-mode
rejection ratio** (CMRR) measures this:

$$\\text{CMRR} = \\frac{A_{dm}}{A_{cm}}, \\qquad A_{cm} \\approx \\frac{-g_m R_D}{1 + 2 g_m R_{tail}}.$$

A better (higher $r_o$) tail current source means a larger $R_{tail}$, smaller
$A_{cm}$, and higher CMRR - which is why the tail is usually a cascode mirror.
This is how an instrumentation front-end pulls a millivolt sensor signal off a
noisy common-mode background.

## The active load: free single-ended gain

Loading the pair with two resistors wastes gain and headroom. Replace them with a
**current-mirror active load** and you get two wins: it converts the differential
signal to a **single-ended** output, and it doubles the effective output current,
giving a single-stage gain of

$$A_{dm} = g_m (r_{o,n} \\parallel r_{o,p}).$$

```mermaid
flowchart TB
  IN1["v+ -> M1"] --> NODE1["drain 1"]
  IN2["v- -> M2"] --> NODE2["drain 2 (output)"]
  NODE1 --> ML["mirror load (PMOS)"]
  NODE2 --> ML
  TAIL["tail current source Iss"] --> M1M2["shared source"]
```

```spice
* NMOS differential pair with PMOS mirror load
M1 op inp tail 0 nmos W=20u L=0.5u
M2 on inn tail 0 nmos W=20u L=0.5u
M3 op op vdd vdd pmos W=40u L=0.5u
M4 on op vdd vdd pmos W=40u L=0.5u
Itail tail 0 100u
Vdd vdd 0 1.8
.model nmos NMOS (VTO=0.6 KP=120u LAMBDA=0.1)
.model pmos PMOS (VTO=-0.6 KP=40u LAMBDA=0.12)
.op
```

```python
gm, ro_n, ro_p = 1e-3, 80e3, 100e3
Adm = gm * (ro_n * ro_p) / (ro_n + ro_p)   # single-stage diff gain
Rtail = 2e6                                # cascode tail -> high CMRR
Acm = -gm * 50e3 / (1 + 2 * gm * Rtail)    # tiny common-mode gain
print(Adm, Acm)
```

**Real-world:** the diff pair is the literal front door of the LM741, every CMOS
op-amp, ECG/biopotential amplifiers, and the receivers in USB, PCIe, and Ethernet
(where CMRR rejects the noise picked up equally on both wires).

**Next:** what limits how fast all of this can go - frequency response.
""",
        ),
        _t(
            "Frequency response of amplifiers",
            "13 min",
            """\
# Frequency response of amplifiers

Every node in an amplifier has capacitance, and every capacitance with a
resistance makes a **pole** - a frequency where the gain starts to roll off. The
art of high-speed analog is knowing where the poles are.

## Poles, zeros, and the Bode plot

A single RC node gives one pole at $f_p = 1/(2\\pi R C)$: flat gain below it,
falling at **-20 dB/decade** above, with -45 degrees of phase right at the pole.
A **zero** does the opposite (gain rises, phase leads). Slide the pole frequency:

```plot
{"title": "Single-pole magnitude response, DC gain 100 (slide pole fp)", "xLabel": "frequency f (Hz, log feel)", "yLabel": "|gain| (V/V)", "xRange": [1, 1000], "yRange": [0, 110], "grid": true, "controls": [{"name": "fp", "range": [5, 200], "value": 30, "label": "pole frequency fp (Hz)"}], "functions": [{"expr": "100/sqrt(1 + (x/fp)^2)", "label": "|A(f)|"}]}
```

## The gain-bandwidth product

For the common-source stage the DC gain is $g_m R$ and the pole is $1/(2\\pi R C)$,
so their **product** does not depend on $R$:

$$\\text{GBW} = A_0 \\cdot f_p = \\frac{g_m}{2\\pi C}.$$

Push for more gain (bigger $R$) and you lose bandwidth one-for-one. This single
constant governs how you trade gain for speed across the whole chip.

## The Miller effect: the bandwidth killer

A capacitor $C_{gd}$ bridging the input and output of an **inverting** gain stage
looks **far larger** from the input than it is, multiplied by the gain:

$$C_{in,\\,Miller} = C_{gd}(1 + |A_v|).$$

A 10 fF gate-drain cap on a gain-of-100 stage acts like ~1 pF on the input -
crushing the bandwidth. This is *the* reason a plain common-source stage is slow,
and why the wideband **cascode** (common-source feeding a common-gate) exists:
the common-gate holds the drain nearly still, so there is almost no voltage swing
across $C_{gd}$ to multiply.

```mermaid
flowchart LR
  IN["input"] --> CS["common-source (gain, but Miller Cgd)"]
  CS --> CASC["cascode: common-gate kills the Miller multiplication"]
  CASC --> OUT["wideband high-gain output"]
```

```spice
* Common-source .ac to see the dominant pole and rolloff
M1 out in 0 0 nmos W=20u L=0.5u
Rd out vdd 20k
Cl out 0 0.5p
Vdd vdd 0 1.8
Vin in 0 0.9 AC 1
.model nmos NMOS (VTO=0.6 KP=120u LAMBDA=0.1)
.ac dec 30 1k 10G
```

```python
import math

gm, R, C, Cgd = 2e-3, 20e3, 0.5e-12, 10e-15
A0 = gm * R
Cin_miller = Cgd * (1 + A0)        # Miller-multiplied input cap
fp = 1 / (2 * math.pi * R * C)     # output pole
gbw = gm / (2 * math.pi * C)       # gain-bandwidth product
print(A0, fp, gbw, Cin_miller)
```

**Real-world:** the GBW number on every op-amp datasheet is this constant; an op-
amp at gain 100 reaches only GBW/100 of bandwidth. Cascodes and Miller
compensation (Intermediate course) are the everyday tools for managing these
poles in real chips.

**Next:** build a common-source Bode plot and a diff-pair transfer curve in code.
""",
        ),
        _code(
            "Lab: common-source Bode and diff-pair transfer curve",
            "14 min",
            """\
# Two classic analog plots from the small-signal model, in pure numpy/matplotlib.
#   (1) Common-source amplifier Bode magnitude + phase (a single dominant pole).
#   (2) Differential-pair current-steering transfer curve (tanh-like).
import numpy as np
import matplotlib.pyplot as plt

# --- (1) Common-source amplifier ---
gm = 2e-3            # transconductance (A/V)
ro = 50e3           # device output resistance (ohm)
Rd = 20e3           # drain load (ohm)
Cl = 0.5e-12        # load capacitance (F)
R = ro * Rd / (ro + Rd)
A0 = gm * R                          # DC gain magnitude
fp = 1 / (2 * np.pi * R * Cl)        # dominant pole (Hz)

f = np.logspace(2, 10, 600)
H = A0 / (1 + 1j * f / fp)           # single-pole transfer function
mag_db = 20 * np.log10(np.abs(H))
phase = np.degrees(np.angle(H))      # inverting stage adds -180 conceptually

# --- (2) Differential-pair transfer curve ---
Iss = 100e-6        # tail current (A)
beta = 0.5e-3       # mu*Cox*W/L lumped (A/V^2)
vid = np.linspace(-0.4, 0.4, 400)
# closed-form long-tailed pair steering (saturates at +/- Iss)
radicand = np.clip(Iss / beta - vid**2 / 4, 0, None)
Iout = 2 * beta * vid * np.sqrt(radicand)
Iout = np.clip(Iout, -Iss, Iss)

fig, ax = plt.subplots(1, 3, figsize=(13, 4))
ax[0].semilogx(f, mag_db, color="#2563eb")
ax[0].axvline(fp, ls="--", color="#94a3b8")
ax[0].set_title(f"Common-source magnitude (fp ~ {fp/1e6:.1f} MHz)")
ax[0].set_xlabel("frequency (Hz)"); ax[0].set_ylabel("gain (dB)"); ax[0].grid(True)

ax[1].semilogx(f, phase, color="#dc2626")
ax[1].set_title("Common-source phase")
ax[1].set_xlabel("frequency (Hz)"); ax[1].set_ylabel("phase (deg)"); ax[1].grid(True)

ax[2].plot(vid * 1e3, Iout * 1e6, color="#16a34a")
ax[2].set_title("Diff-pair current steering")
ax[2].set_xlabel("vid (mV)"); ax[2].set_ylabel("I1 - I2 (uA)"); ax[2].grid(True)

plt.tight_layout(); plt.show()

print(f"DC gain A0 = {A0:.1f} V/V ({20*np.log10(A0):.1f} dB)")
print(f"dominant pole fp = {fp/1e6:.2f} MHz, GBW = {gm/(2*np.pi*Cl)/1e6:.1f} MHz")
print(f"diff-pair saturates near vid = {np.sqrt(Iss/beta)*1e3:.0f} mV")

# Try it yourself:
#   1. Raise Rd to 200e3: more gain, lower pole - GBW stays ~constant.
#   2. Raise Iss: the diff-pair steering curve stretches wider before saturating.
""",
        ),
    ),
)


# -- Analog & Mixed-Signal IC Design -- Intermediate ---------------------------

_ANALOG_INTERMEDIATE = SeedCourse(
    slug="analog-ic-intermediate",
    title="Analog & Mixed-Signal IC Design -- Intermediate: Op-Amps & Feedback",
    description=(
        "Building blocks into systems: the two-stage op-amp, feedback and "
        "stability (loop gain, phase margin, Miller compensation, slew rate), "
        "noise (thermal/flicker, input-referred, SNR), bandgap and voltage "
        "references, and the OTA and switched-capacitor circuits - with dual "
        "SPICE/Python, interactive plots, and a runnable loop-gain / bandgap lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The two-stage op-amp",
            "13 min",
            """\
# The two-stage op-amp

A single stage gives gain $g_m r_o$ (~30-50 dB) - not enough for a precise op-
amp. Cascade two and you multiply the gains. The **two-stage Miller op-amp** is
the textbook workhorse and still ships in countless real chips.

## The topology

```mermaid
flowchart LR
  INP["v+"] --> DIFF["stage 1: diff pair + mirror load"]
  INN["v-"] --> DIFF
  DIFF --> CC["Miller cap Cc"]
  DIFF --> GAIN["stage 2: common-source gain"]
  CC --> GAIN
  GAIN --> OUT["output"]
```

- **Stage 1** is a differential pair with an active (mirror) load: high gain,
  converts differential to single-ended, sets the input offset and most of the
  noise.
- **Stage 2** is a common-source gain stage: adds more gain and provides the
  output swing.
- **$C_c$** is the **Miller compensation capacitor** between the stages (stability
  lesson).

## The gain

The total DC gain is the product of the two stage gains:

$$A_0 = \\underbrace{g_{m1}(r_{o2}\\parallel r_{o4})}_{\\text{stage 1}} \\cdot \\underbrace{g_{m6}(r_{o6}\\parallel r_{o7})}_{\\text{stage 2}} \\approx (g_m r_o)^2.$$

Two stages of ~50 dB give ~100 dB (a gain of $10^5$) - plenty to make feedback
precise. Slide the per-stage gain and watch the total climb:

```plot
{"title": "Two-stage gain stacks: total dB = 2 x stage dB (slide stage gain)", "xLabel": "stage gain (V/V)", "yLabel": "total gain (dB)", "xRange": [10, 400], "yRange": [0, 110], "grid": true, "controls": [{"name": "k", "range": [1, 2], "value": 1, "label": "extra stage-gain multiplier"}], "functions": [{"expr": "40*log10(k*x)", "label": "20 log10(gain^2)"}]}
```

## The output stage

The common-source second stage has high output resistance - fine for driving an
on-chip capacitive load, poor for driving a resistor or pin. When an op-amp must
drive a real load, designers add a **class-AB output stage** (a push-pull source/
emitter follower) that delivers current both ways with low distortion and low
quiescent power.

```spice
* Two-stage op-amp skeleton (stage 1 diff pair, stage 2 CS, Cc compensation)
M1 o1 inp tail 0 nmos W=20u L=0.5u
M2 o2 inn tail 0 nmos W=20u L=0.5u
M6 out o2  0   0 nmos W=40u L=0.5u
Cc o2 out 1p
Itail tail 0 100u
Vdd vdd 0 1.8
.model nmos NMOS (VTO=0.6 KP=120u LAMBDA=0.1)
.op
```

```python
gm1, gm6 = 1e-3, 2e-3
ro_stage1 = 80e3 * 100e3 / (80e3 + 100e3)
ro_stage2 = 50e3 * 60e3 / (50e3 + 60e3)
A1 = gm1 * ro_stage1
A2 = gm6 * ro_stage2
A0 = A1 * A2
print(A1, A2, A0)        # ~ (g_m r_o)^2, ~100 dB
```

**Real-world:** the classic 741 and nearly every general-purpose CMOS op-amp use
this two-stage-with-output-buffer recipe. The numbers (gain, swing, drive) on an
op-amp datasheet map directly onto these three blocks.

**Next:** the feedback that turns raw gain into precision - and the price,
stability.
""",
        ),
        _t(
            "Feedback and stability",
            "14 min",
            """\
# Feedback and stability

Raw op-amp gain is huge but sloppy (varies with temperature, device, signal).
**Negative feedback** trades that excess gain for precision, bandwidth, and low
distortion - but if you are careless it turns into an **oscillator**.

## Loop gain sets everything

Wrap the op-amp (open-loop gain $A$) with a feedback factor $\\beta$. The closed-
loop gain is

$$A_{cl} = \\frac{A}{1 + A\\beta} \\xrightarrow{A\\beta \\gg 1} \\frac{1}{\\beta}.$$

The product **$A\\beta$ is the loop gain** - the single most important quantity in
feedback design. Large loop gain means the closed-loop gain depends only on the
(precise, passive) feedback network, not the messy transistor.

## Phase margin: how close to ringing

Each pole adds phase lag. If the loop gain still exceeds 1 (0 dB) when the phase
lag reaches -180 degrees, the negative feedback has become **positive** and the
amplifier oscillates. The **phase margin** is how much phase is left at the
unity-gain frequency:

$$\\text{PM} = 180^\\circ + \\angle A\\beta\\big|_{|A\\beta|=1}.$$

A second-order loop's step response shows the cost: low phase margin rings, ~60
degrees is the sweet spot. Slide the phase margin (here mapped to damping):

```plot
{"title": "Closed-loop step response vs phase margin (slide PM)", "xLabel": "time (normalized)", "yLabel": "output", "xRange": [0, 14], "yRange": [0, 1.8], "grid": true, "controls": [{"name": "PM", "range": [15, 80], "value": 45, "label": "phase margin (deg)"}], "functions": [{"expr": "1 - exp(-PM/40*x)*cos(sqrt(max(0,1-(PM/90)^2))*3*x)", "label": "step response"}]}
```

## Miller compensation: making it stable on purpose

The two-stage op-amp has two close poles - dangerous. **Miller compensation**
puts a small capacitor $C_c$ across the second stage. Through the Miller effect it
becomes a huge effective capacitance, pushing the first pole **way down** (pole
splitting) so the amplifier rolls off to under unity gain before the second pole
adds its phase lag. The unity-gain bandwidth becomes

$$\\omega_u \\approx \\frac{g_{m1}}{C_c}.$$

```mermaid
stateDiagram-v2
  [*] --> TwoClosePoles: uncompensated (rings / oscillates)
  TwoClosePoles --> PoleSplit: add Miller Cc
  PoleSplit --> Stable: dominant pole low, PM ~60 deg
  Stable --> [*]
```

## Slew rate: the large-signal speed limit

Bandwidth is a **small-signal** limit. For big fast steps the output cannot move
faster than the tail current can charge $C_c$:

$$\\text{SR} = \\frac{I_{tail}}{C_c}.$$

Ask for a faster swing than the slew rate allows and the output ramps in a
straight line, distorting the signal. Slew rate and bandwidth are independent
specs - both matter.

```spice
* Loop-gain test: break the loop, inject, measure A*beta
M1 o1 inp tail 0 nmos W=20u L=0.5u
Cc o2 out 1p
Itail tail 0 100u
Vin inp 0 0.9 AC 1
.model nmos NMOS (VTO=0.6 KP=120u LAMBDA=0.1)
.ac dec 30 10 100Meg
```

```python
import math

gm1, Cc, Itail = 1e-3, 1e-12, 100e-6
wu = gm1 / Cc                       # unity-gain bandwidth (rad/s)
gbw_hz = wu / (2 * math.pi)
slew = Itail / Cc                   # slew rate (V/s)
beta = 0.1                          # feedback factor (gain of 10)
loop_gain_dc = 1e5 * beta
print(gbw_hz, slew, loop_gain_dc)
```

**Real-world:** every op-amp datasheet's "phase margin", "gain-bandwidth", and
"slew rate" come straight from here. Unstable feedback is the classic lab
nightmare - an amplifier that rings or sings until you fix the compensation.

**Next:** the fundamental floor under every signal - noise.
""",
        ),
        _t(
            "Noise in analog circuits",
            "13 min",
            """\
# Noise in analog circuits

Gain you can add; **noise** sets the floor you can never get below. Analog IC
design is largely a fight to keep the signal above the noise.

## The two fundamental noise sources

| Source | Origin | Spectrum | Model |
|--------|--------|----------|-------|
| **Thermal** (Johnson) | random carrier motion | flat (white) | resistor: $\\overline{v_n^2} = 4kTR\\,\\Delta f$; MOS: $\\overline{i_n^2} = 4kT\\gamma g_m\\,\\Delta f$ |
| **Flicker** (1/f) | trapped charge at the gate oxide | rises at low $f$ | $\\overline{v_n^2} = \\frac{K}{C_{ox} W L}\\frac{1}{f}\\,\\Delta f$ |

Thermal noise is white - the same at every frequency. Flicker noise dominates at
low frequencies and crosses the thermal floor at the **1/f corner**. Slide the
corner frequency:

```plot
{"title": "Input-referred noise: 1/f flicker + flat thermal (slide corner)", "xLabel": "frequency f (Hz, log feel)", "yLabel": "noise density (nV/rtHz)", "xRange": [1, 1000], "yRange": [0, 40], "grid": true, "controls": [{"name": "fc", "range": [10, 300], "value": 100, "label": "1/f corner frequency (Hz)"}], "functions": [{"expr": "10*sqrt(1 + fc/x)", "label": "total noise density"}]}
```

## Input-referred noise: the fair comparison

Every device in the chain adds noise, but a noise source after a gain stage
matters less (the signal is already big). To compare amplifiers fairly, refer all
the noise back to the **input**: divide each contribution by the gain ahead of it.
For an op-amp this makes the **input differential pair dominate** - which is why
those input transistors are large (low flicker) and biased for low thermal noise.

## SNR: the number that matters

The **signal-to-noise ratio** is the signal power over the integrated noise power:

$$\\text{SNR (dB)} = 10\\log_{10}\\frac{P_{signal}}{P_{noise}}.$$

You buy SNR with power and area: bigger devices and more current lower the noise,
but cost battery and silicon. This SNR-power-area triangle is the central tension
of low-noise design, and it sets the resolution ceiling of the data converters in
the Advanced course.

```mermaid
flowchart LR
  TH["thermal: lower by more gm / current"] --> TOT["total input-referred noise"]
  FL["flicker: lower by bigger W*L, or chopping"] --> TOT
  TOT --> SNR["SNR -> resolution / ENOB"]
```

```spice
* Noise analysis: integrated input-referred noise of stage 1
M1 out in 0 0 nmos W=50u L=2u
Rd out vdd 20k
Vin in 0 0.9 AC 1
Vdd vdd 0 1.8
.model nmos NMOS (VTO=0.6 KP=120u LAMBDA=0.1 KF=1e-25)
.noise V(out) Vin dec 20 1 10Meg
```

```python
import math

k, T = 1.380649e-23, 300.0
R = 20e3
vn_thermal = math.sqrt(4 * k * T * R)        # V/sqrt(Hz)
gm, gamma = 1e-3, 0.67
in_mos = math.sqrt(4 * k * T * gamma * gm)   # A/sqrt(Hz)
vn_in = in_mos / gm                          # input-referred (V/sqrt(Hz))
print(vn_thermal * 1e9, "nV/rtHz", vn_in * 1e9, "nV/rtHz")
```

**Real-world:** noise sets the smallest signal a hearing aid, ECG, radio
receiver, or image sensor can resolve. **Chopping** and **correlated double
sampling** (used in CMOS image sensors and precision amps) specifically cancel the
flicker noise the diff pair would otherwise contribute.

**Next:** building a stable reference voltage that ignores temperature - the
bandgap.
""",
        ),
        _t(
            "Bandgap and voltage references",
            "13 min",
            """\
# Bandgap and voltage references

Every data converter and regulator needs a **stable reference** that does not
drift with temperature or supply. The **bandgap reference** is the elegant trick
that delivers ~1.2 V almost independent of temperature.

## PTAT and CTAT: two opposite slopes

The secret is combining two quantities with opposite temperature coefficients:

- **CTAT** (Complementary To Absolute Temperature): a diode/BJT base-emitter
  voltage $V_{BE}$ **falls** with temperature (~-2 mV/C).
- **PTAT** (Proportional To Absolute Temperature): the **difference** of two
  $V_{BE}$ at different current densities **rises** with temperature,
  $\\Delta V_{BE} = \\frac{kT}{q}\\ln N$.

Add a scaled PTAT term to a CTAT term and the slopes **cancel**:

$$V_{ref} = V_{BE} + M\\,\\Delta V_{BE} \\approx 1.2\\,\\text{V (flat over temperature)}.$$

Slide the PTAT multiplier $M$ and watch the temperature curve tilt from falling
(too little PTAT) through flat to rising (too much):

```plot
{"title": "Bandgap = CTAT + M*PTAT vs temperature (slide M to flatten)", "xLabel": "temperature (deg C)", "yLabel": "Vref (V)", "xRange": [-40, 125], "yRange": [1.15, 1.30], "grid": true, "controls": [{"name": "M", "range": [5, 12], "value": 8, "label": "PTAT multiplier M"}], "functions": [{"expr": "1.25 - 0.002*x + M*0.00025*(x + 273)", "label": "Vref(T)"}]}
```

The flattest curve (the right $M$) is a gentle parabola - the residual
**curvature** is what limits a simple bandgap to tens of ppm/C; curvature-
corrected designs do better.

## PSRR: ignoring the supply

A reference must also reject **supply** ripple - quantified by the **power-supply
rejection ratio** (PSRR). The reference is biased by current mirrors and often
cascoded specifically to keep supply wiggle out of $V_{ref}$, because that ripple
would otherwise show up directly in an ADC's output.

```mermaid
flowchart LR
  VBE["VBE (CTAT, -2mV/C)"] --> SUM["sum"]
  DVBE["delta-VBE (PTAT, +k/q ln N)"] --> GAIN["x M"]
  GAIN --> SUM
  SUM --> VREF["Vref ~ 1.2 V, flat over T"]
```

```spice
* Bandgap core: two BJTs at ratio N, op-amp forces equal node voltages
Q1 n1 b 0 npn 1
Q2 n2 b 0 npn 8
R1 vref n1 10k
R2 vref n2 10k
R3 n2 nx 1k
.model npn NPN
.op
```

```python
import math

k, q = 1.380649e-23, 1.602e-19
T = 300.0
N = 8                               # emitter-area ratio
dVbe = (k * T / q) * math.log(N)    # PTAT term (~54 mV at 300 K)
Vbe = 0.65                          # CTAT term
M = 8.0                             # PTAT multiplier to cancel slopes
Vref = Vbe + M * dVbe               # ~1.2 V
print(dVbe * 1e3, "mV", Vref, "V")
```

**Real-world:** a bandgap sits in essentially every mixed-signal chip - it sets
the full-scale of every ADC and DAC, the output of every voltage regulator, and
the trip point of every power-on reset. Its temperature drift directly limits
system accuracy.

**Next:** the analog blocks that talk to sampled-data systems - OTAs and
switched-capacitor circuits.
""",
        ),
        _t(
            "The OTA and switched-capacitor circuits",
            "13 min",
            """\
# The OTA and switched-capacitor circuits

On-chip you rarely have precise resistors - but you have excellent **capacitors**
and fast **switches**. **Switched-capacitor** (SC) circuits exploit this, and the
amplifier that drives them is the **OTA**.

## The OTA: a transconductor, not a voltage amplifier

An **Operational Transconductance Amplifier** outputs a **current** proportional
to its differential input voltage, $i_{out} = g_m\\,v_{id}$. Unlike an op-amp it is
**not** meant to drive resistive loads - it drives **capacitors**, which is
exactly what SC and continuous-time filters present. That makes it the standard
gain element inside ICs.

## A switched capacitor *is* a resistor

Toggle a capacitor between two nodes at frequency $f_s$ and it ferries a packet of
charge $C\\,\\Delta V$ each cycle. The average current makes it behave like a
resistor:

$$R_{eq} = \\frac{1}{C f_s}.$$

This is the key idea: a switch + capacitor **emulates a resistor whose value is
set by a clock**. Slide the clock frequency and watch the equivalent resistance:

```plot
{"title": "Switched-cap equivalent resistance Req = 1/(C fs), C=1pF (slide C)", "xLabel": "clock frequency fs (MHz)", "yLabel": "equivalent resistance (Mohm)", "xRange": [1, 50], "yRange": [0, 12], "grid": true, "controls": [{"name": "Cpf", "range": [1, 5], "value": 1, "label": "capacitor C (pF)"}], "functions": [{"expr": "1/(Cpf*x)*1000", "label": "Req"}]}
```

## gm/C filters and SC integrators

- A **gm/C filter** sets a pole at $g_m/C$ using only an OTA and a capacitor -
  tunable by the bias current, ideal for on-chip continuous-time filtering.
- A **SC integrator** replaces the resistor of an op-amp integrator with a
  switched cap, so its time constant becomes a **ratio of capacitors times a
  clock** - $C_1/(C_2 f_s)$. Capacitor *ratios* match to ~0.1% on silicon, while
  absolute values vary wildly, so SC circuits are remarkably **precise** and
  process-independent.

## Sampling: where it meets the digital world

A switch and a capacitor form a **sample-and-hold**: close the switch to track the
input, open it to freeze the value. This is the literal front end of the data
converters in the Advanced course - and SC integrators are the heart of the
delta-sigma modulator there.

```mermaid
flowchart LR
  VIN["Vin"] --> SW1["phase-1 switch"]
  SW1 --> CAP["sampling cap C"]
  CAP --> SW2["phase-2 switch"]
  SW2 --> OTA["OTA integrator"]
  OTA --> OUT["sampled / integrated output"]
```

```spice
* SC integrator: C1 sampled onto C2 around an OTA, two-phase clock phi1/phi2
.subckt sc_int in out
S1 in x phi1 0 sw
S2 x 0 phi2 0 sw
C1 x 0 1p
E1 out 0 0 x 1000
C2 out x 2p
.ends
```

```python
C, fs = 1e-12, 10e6
Req = 1 / (C * fs)                  # switched-cap equivalent resistor (ohm)
gm = 1e-3
f_pole = gm / (2 * 3.14159 * 2e-12) # gm/C filter pole (Hz)
C1, C2 = 1e-12, 2e-12
sc_gain = C1 / C2                   # SC gain set by a capacitor ratio
print(Req, f_pole, sc_gain)
```

**Real-world:** SC circuits build the precise filters in audio codecs, the gain
stages in pipeline and delta-sigma ADCs, and the anti-alias/decimation filters in
nearly every modern mixed-signal chip. Their accuracy rests entirely on capacitor
ratio matching - a uniquely IC-friendly property.

**Next:** put feedback theory to work - plot loop gain, phase margin, and a
bandgap curve.
""",
        ),
        _code(
            "Lab: loop gain, phase margin, and a bandgap curve",
            "14 min",
            """\
# Two pillars of intermediate analog IC design, in pure numpy/matplotlib.
#   (1) Loop gain Bode of a two-pole op-amp -> read off the phase margin.
#   (2) Bandgap reference voltage vs temperature -> find the flat point.
import numpy as np
import matplotlib.pyplot as plt

# --- (1) Loop gain and phase margin ---
A0 = 1e5            # open-loop DC gain (100 dB)
fp1 = 100.0         # dominant pole after Miller compensation (Hz)
fp2 = 5e6           # second (parasitic) pole (Hz)
beta = 1.0          # unity-gain feedback (worst case for stability)

f = np.logspace(0, 8, 800)
s = 1j * f
loop = A0 * beta / ((1 + s / fp1) * (1 + s / fp2))
mag_db = 20 * np.log10(np.abs(loop))
phase = np.degrees(np.angle(loop))

# unity-gain crossover -> phase margin
cross = np.argmin(np.abs(mag_db))
fc = f[cross]
pm = 180 + phase[cross]

# --- (2) Bandgap reference vs temperature ---
kq = 8.617e-5       # k/q (V/K)
N = 8               # BJT area ratio -> PTAT slope
M = 11.2            # PTAT multiplier chosen to flatten near room temp
Tc = np.linspace(-40, 125, 200)
Tk = Tc + 273.15
Vbe = 0.65 - 0.002 * (Tc - 27)              # CTAT term (falls with T)
dVbe = kq * Tk * np.log(N)                  # PTAT term (rises with T)
Vref = Vbe + M * dVbe                       # CTAT + scaled PTAT ~ 1.2 V
flat_T = Tc[np.argmin(np.abs(np.gradient(Vref, Tc)))]   # minimum-slope point

fig, ax = plt.subplots(1, 3, figsize=(13, 4))
ax[0].semilogx(f, mag_db, color="#2563eb")
ax[0].axhline(0, ls="--", color="#94a3b8")
ax[0].axvline(fc, ls=":", color="#dc2626")
ax[0].set_title("Loop gain magnitude")
ax[0].set_xlabel("frequency (Hz)"); ax[0].set_ylabel("|A*beta| (dB)"); ax[0].grid(True)

ax[1].semilogx(f, phase, color="#dc2626")
ax[1].axvline(fc, ls=":", color="#94a3b8")
ax[1].set_title(f"Phase (PM ~ {pm:.0f} deg)")
ax[1].set_xlabel("frequency (Hz)"); ax[1].set_ylabel("phase (deg)"); ax[1].grid(True)

ax[2].plot(Tc, Vref * 1e3, color="#16a34a")
ax[2].axvline(flat_T, ls="--", color="#94a3b8")
ax[2].set_title("Bandgap Vref vs temperature")
ax[2].set_xlabel("temperature (deg C)"); ax[2].set_ylabel("Vref (mV)"); ax[2].grid(True)

plt.tight_layout(); plt.show()

ppm = (Vref.max() - Vref.min()) / Vref.mean() / 165 * 1e6
print(f"unity-gain crossover fc = {fc/1e6:.2f} MHz, phase margin = {pm:.0f} deg")
print(f"bandgap flat near {flat_T:.0f} C, drift ~ {ppm:.0f} ppm/C, Vref ~ {Vref.mean():.3f} V")

# Try it yourself:
#   1. Move fp2 down to 5e5: the phase margin collapses - the op-amp rings.
#   2. Change M to 6 or 11: the bandgap tilts CTAT or PTAT (no flat point).
""",
        ),
    ),
)


# -- Analog & Mixed-Signal IC Design -- Advanced -------------------------------

_ANALOG_ADVANCED = SeedCourse(
    slug="analog-ic-advanced",
    title="Analog & Mixed-Signal IC Design -- Advanced: Data Converters & PLLs",
    description=(
        "The mixed-signal frontier: sampling and quantization, DAC architectures "
        "(binary-weighted, R-2R, current-steering, INL/DNL), Nyquist ADCs (flash, "
        "SAR, pipeline), delta-sigma converters (oversampling, noise shaping, "
        "decimation), and PLLs / frequency synthesis - with dual SPICE/Python, "
        "interactive plots, a runnable ADC/ENOB lab, and real-world use cases."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Sampling and quantization for converters",
            "13 min",
            """\
# Sampling and quantization for converters

A data converter bridges the continuous analog world and the discrete digital
one. Two operations define it: **sampling** in time and **quantization** in
amplitude. Each has a fundamental limit.

## Sampling and the Nyquist criterion

Sampling at rate $f_s$ captures a signal exactly only if its bandwidth is below
$f_s/2$ (the **Nyquist frequency**). Break this and high frequencies **alias** -
fold down and masquerade as low frequencies that you can never remove afterward.
That is why every ADC has an **anti-alias filter** in front. The aliased
frequency of a tone $f_0$ is its distance to the nearest multiple of $f_s$.

## Quantization noise and SNR

Rounding a continuous value to the nearest of $2^N$ levels introduces an error of
up to $\\pm \\tfrac{1}{2}$ LSB. Modeled as uniform white noise, it has power
$\\Delta^2/12$ (with $\\Delta$ the step size), giving the famous ideal SNR:

$$\\text{SNR} = 6.02\\,N + 1.76\\ \\text{dB}.$$

Every extra **bit buys ~6 dB**. Slide the bit count and watch the line climb:

```plot
{"title": "Ideal converter SNR = 6.02 N + 1.76 dB (slide a scale factor)", "xLabel": "resolution N (bits)", "yLabel": "SNR (dB)", "xRange": [4, 20], "yRange": [0, 130], "grid": true, "controls": [{"name": "g", "range": [0.9, 1.1], "value": 1, "label": "process scale factor"}], "functions": [{"expr": "g*(6.02*x + 1.76)", "label": "SNR"}]}
```

## ENOB: the honest resolution

Real converters fall short of the ideal because of noise and distortion. Invert
the formula on the **measured** SNDR (signal-to-noise-and-distortion ratio) to get
the **effective number of bits**:

$$\\text{ENOB} = \\frac{\\text{SNDR} - 1.76}{6.02}.$$

A "16-bit" ADC with 14.5 ENOB is honest about delivering 14.5 real bits.

## Oversampling: trading speed for resolution

Quantization noise power is fixed, but it spreads over the whole $0$ to $f_s/2$
band. **Oversample** by a factor $OSR = f_s/(2 f_B)$ and only a fraction lands in
your signal band - so digitally filtering away the rest gains

$$\\Delta\\text{SNR} = 10\\log_{10}(OSR)\\ \\text{dB} \\;=\\; 3\\,\\text{dB per doubling}.$$

This is the seed of the delta-sigma converter four lessons on.

```mermaid
flowchart LR
  IN["analog in"] --> AAF["anti-alias filter (< fs/2)"]
  AAF --> SH["sample & hold (fs)"]
  SH --> Q["quantize (N bits)"]
  Q --> OUT["digital code"]
```

```spice
* Behavioral sample-and-hold front end (ngspice/Verilog-A style)
.model sw SW(Ron=100 Roff=1G Vt=0.5)
Ssh in cap clk 0 sw
Csh cap 0 1p
.tran 1n 1u
```

```python
import math

N = 12
snr_ideal = 6.02 * N + 1.76         # dB
sndr_meas = 68.0                    # measured SNDR (dB)
enob = (sndr_meas - 1.76) / 6.02
osr = 64
osr_gain = 10 * math.log10(osr)     # dB from oversampling
print(snr_ideal, enob, osr_gain)
```

**Real-world:** sampling and quantization theory sets the resolution of audio
ADCs, camera sensors, software-defined radios, and oscilloscopes. The
6 dB-per-bit and 3 dB-per-octave rules are the back-of-envelope tools every
mixed-signal architect reaches for first.

**Next:** the converters that turn codes back into voltages - DACs.
""",
        ),
        _t(
            "DAC architectures",
            "13 min",
            """\
# DAC architectures

A **digital-to-analog converter** turns a binary code into an analog voltage or
current. Several architectures trade speed, area, and accuracy differently.

## The main families

| Architecture | How | Strength | Weakness |
|--------------|-----|----------|----------|
| **Binary-weighted** | sum currents/charges $1,2,4,\\dots$ | simple, fast | huge element spread, poor matching |
| **R-2R ladder** | only two resistor values | great matching, compact | series resistance loading |
| **Current-steering** | switch weighted current sources to the output | very fast (GHz) | needs good current-source matching |
| **Thermometer/segmented** | $2^N-1$ equal units (often for MSBs) | monotonic, low glitch | area grows as $2^N$ |

Most real high-resolution DACs are **segmented**: thermometer-coded MSBs (for
monotonicity and low glitch) plus binary LSBs (for area). The ideal transfer is a
staircase - code in, proportional output out:

```plot
{"title": "Ideal 3-bit DAC transfer staircase (code -> output)", "xLabel": "input code", "yLabel": "output (LSB)", "xRange": [0, 8], "yRange": [0, 8], "grid": true, "series": [{"points": [[0,0],[1,0],[1,1],[2,1],[2,2],[3,2],[3,3],[4,3],[4,4],[5,4],[5,5],[6,5],[6,6],[7,6],[7,7]], "label": "DAC output", "color": "#2563eb"}]}
```

## INL and DNL: the two error metrics

- **DNL** (Differential Nonlinearity): how much each code **step** deviates from
  exactly 1 LSB. DNL worse than -1 LSB means a **missing code** (and possible
  non-monotonicity) - fatal in a feedback loop.
- **INL** (Integral Nonlinearity): the **accumulated** deviation of the staircase
  from the ideal straight line - it bends the transfer curve and creates
  distortion.

A real DAC's INL bows away from the ideal line; slide the bow magnitude:

```plot
{"title": "DAC INL: real curve bows off the ideal line (slide INL)", "xLabel": "input code (fraction of full-scale)", "yLabel": "output (fraction)", "xRange": [0, 1], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "inl", "range": [0, 0.15], "value": 0.06, "label": "peak INL (fraction)"}], "functions": [{"expr": "x + inl*sin(3.14159*x)", "label": "real transfer", "color": "#dc2626"}, {"expr": "x", "label": "ideal", "color": "#94a3b8"}]}
```

```mermaid
flowchart LR
  CODE["digital code"] --> DEC["thermometer decode (MSBs)"]
  CODE --> BIN["binary weights (LSBs)"]
  DEC --> SUM["sum of weighted currents"]
  BIN --> SUM
  SUM --> OUT["analog output"]
```

```spice
* 3-bit binary-weighted current DAC into a load resistor
Ib0 0 out 1u
Ib1 0 out 2u
Ib2 0 out 4u
Rload out 0 10k
.dc Ib0 0 1u 1u
```

```python
bits = [1, 0, 1]                    # MSB..LSB, code = 5
weights = [4, 2, 1]
code = sum(b * w for b, w in zip(bits, weights))
Iunit = 1e-6
Iout = code * Iunit                 # binary-weighted current sum
peak_inl_lsb = 0.4                  # would-be spec
print(code, Iout, peak_inl_lsb)
```

**Real-world:** current-steering DACs drive cellular and Wi-Fi transmitters and
arbitrary-waveform generators at GHz rates; R-2R and segmented DACs sit in audio
codecs, instrumentation, and the feedback path of the SAR ADC in the next lesson.

**Next:** going the other way at Nyquist rates - flash, SAR, and pipeline ADCs.
""",
        ),
        _t(
            "Nyquist-rate ADCs",
            "13 min",
            """\
# Nyquist-rate ADCs

A **Nyquist-rate ADC** samples close to twice the signal bandwidth and resolves
each sample directly (no oversampling). Three architectures dominate, trading
speed against resolution and power.

## Flash: fast and hungry

A **flash** ADC compares the input against all $2^N-1$ thresholds at once with a
bank of comparators, then encodes the result in one clock - the **fastest** ADC.
The cost is brutal: comparator count (and power, area) grows as $2^N$, so flash
is practical only to ~6-8 bits. It is the engine inside oscilloscopes and the
sub-ADCs of pipelines.

## SAR: the binary-search workhorse

A **successive-approximation** ADC does a **binary search**: a DAC and one
comparator test the MSB, then each lower bit, halving the uncertainty each step.
It takes $N$ clock cycles but uses almost no static power, dominating the
medium-speed, 8-16 bit space (sensors, IoT, instrumentation). Watch the search
home in - press Play:

```plot
{"title": "SAR binary search converging on the input (press Play)", "xLabel": "approximation step", "yLabel": "DAC guess (fraction of FS)", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "animate": {"param": "t", "range": [0, 8], "label": "SAR step"}, "functions": [{"expr": "0.62", "label": "input sample", "color": "#94a3b8"}], "points": [{"xExpr": "t", "yExpr": "0.5 + 0.25*sign(0.62-0.5) - 0.125*(t>2) + 0.0625*(t>3)", "label": "DAC guess", "color": "#dc2626", "size": 7, "trail": true}]}
```

## Pipeline: speed and resolution together

A **pipeline** ADC splits the conversion into stages: each stage resolves a few
bits, amplifies the **residue** (what is left), and passes it down the line. With
stages working concurrently on different samples it sustains high throughput at
12-14 bits - the classic choice for video and communications.

## The tradeoff map

```plot
{"title": "ADC architecture map: speed vs resolution", "xLabel": "resolution (bits)", "yLabel": "sample rate (log feel, GS/s)", "xRange": [4, 20], "yRange": [0, 12], "grid": true, "points": [{"x": 6, "y": 10, "label": "flash", "color": "#dc2626", "size": 8}, {"x": 12, "y": 5, "label": "pipeline", "color": "#2563eb", "size": 8}, {"x": 14, "y": 1, "label": "SAR", "color": "#16a34a", "size": 8}, {"x": 18, "y": 0.3, "label": "delta-sigma", "color": "#9333ea", "size": 8}]}
```

```mermaid
flowchart LR
  IN["sample"] --> S1["stage 1: resolve k bits"]
  S1 --> R1["x2^k residue amplify"]
  R1 --> S2["stage 2"]
  S2 --> SN["... stage n"]
  SN --> ALIGN["digital align + correct"]
  ALIGN --> OUT["N-bit code"]
```

```spice
* SAR core: comparator + capacitive DAC array (behavioral skeleton)
Vin in 0 0.62
Acmp out in dacout comparator
.model comparator d_comparator
.tran 1n 1u
```

```python
def sar_convert():
    vin, vref, nbits = 0.62, 1.0, 8
    code, guess = 0, 0.0
    for i in range(nbits):
        step = vref / (2 ** (i + 1))
        if vin > guess + step:
            guess += step
            code |= 1 << (nbits - 1 - i)
    return code, guess


print(sar_convert())                # binary-search result for 0.62 * FS
```

**Real-world:** flash lives in oscilloscopes and 100G optical links; SAR is the
default ADC in microcontrollers, medical sensors, and battery devices; pipeline
digitizes camera, radar, and cellular base-station signals.

**Next:** trading raw speed for stunning resolution - delta-sigma converters.
""",
        ),
        _t(
            "Delta-sigma converters",
            "13 min",
            """\
# Delta-sigma converters

The **delta-sigma** ($\\Delta\\Sigma$) converter wins resolution not with precise
components but with **speed and cleverness**: oversample massively, then push the
quantization noise out of the signal band.

## Oversampling plus noise shaping

A 1-bit quantizer is crude, but wrap it in a loop with an **integrator** and
sample very fast, and two things happen:

1. **Oversampling** spreads quantization noise over a wide band, so little lands
   in your narrow signal band.
2. **Noise shaping** - the loop's feedback **high-pass-filters** the quantization
   noise, pushing it up to high frequency where a digital filter removes it. The
   signal passes unshaped.

A first-order loop shapes noise as $|1 - z^{-1}|$; a second-order loop as its
square - steeper. Slide the modulator order and watch the in-band noise plunge:

```plot
{"title": "Delta-sigma noise shaping: noise pushed to high frequency (slide order)", "xLabel": "frequency / fs", "yLabel": "noise gain", "xRange": [0, 0.5], "yRange": [0, 4], "grid": true, "controls": [{"name": "order", "range": [1, 3], "value": 2, "label": "modulator order"}], "functions": [{"expr": "pow(2*abs(sin(3.14159*x)), order)", "label": "noise transfer |NTF|"}]}
```

Near DC the noise gain is tiny; it only rises where the (out-of-band) digital
filter will kill it. Each extra order adds dramatically more in-band SNR for the
same oversampling ratio.

## Decimation: from fast bitstream to slow words

The modulator spits out a fast, coarse (often 1-bit) stream. A **decimation
filter** then low-pass-filters and **downsamples** it to a slow, high-resolution
(e.g. 24-bit) word stream at the Nyquist rate. The modulator is the analog
cleverness; the decimator is the digital heavy lifting.

```mermaid
flowchart LR
  IN["analog in"] --> SUM["subtract (delta)"]
  SUM --> INT["integrate (sigma)"]
  INT --> Q["1-bit quantizer"]
  Q --> OUT["fast bitstream"]
  Q --> DAC["1-bit DAC feedback"]
  DAC --> SUM
  OUT --> DEC["decimation filter -> N-bit words"]
```

## Why it dominates high resolution

Trading speed for accuracy, delta-sigma reaches 20-24 bits with simple, robust
analog (a 1-bit DAC is **inherently linear** - only two points). The price is
latency and a high clock, so it suits **audio, precision instrumentation, and
sensor** measurement rather than fast video.

```spice
* First-order delta-sigma modulator (behavioral, switched-cap integrator + comp)
Eint int 0 VOL='V(int) + V(in) - V(fb)'
Acmp bit int 0 comparator
Efb fb 0 VOL='(V(bit)>0) ? 1 : -1'
.model comparator d_comparator
.tran 1n 100u
```

```python
import numpy as np

fs, fin, n = 1e6, 1e3, 4096
t = np.arange(n) / fs
x = 0.5 * np.sin(2 * np.pi * fin * t)
integ, prev, bits = 0.0, 0.0, np.zeros(n)
for k in range(n):
    integ += x[k] - prev            # delta then sigma (integrate)
    prev = 1.0 if integ > 0 else -1.0
    bits[k] = prev                  # 1-bit shaped output
print("ones fraction:", (bits > 0).mean())
```

**Real-world:** delta-sigma is the architecture in audio ADCs/DACs (your phone,
studio gear), precision weigh scales and thermocouple front-ends, and the
measurement ADCs in lab instruments. The 1-bit-DAC linearity is why CD-quality
audio became cheap.

**Next:** locking frequency and phase - the PLL.
""",
        ),
        _t(
            "PLLs and frequency synthesis",
            "13 min",
            """\
# PLLs and frequency synthesis

A **phase-locked loop** is a feedback system that forces a local oscillator to
track the **phase** of a reference. From that one idea comes clock generation,
frequency synthesis, clock-and-data recovery, and demodulation.

## The loop, block by block

```mermaid
flowchart LR
  REF["reference fref"] --> PFD["phase/freq detector"]
  PFD --> CP["charge pump"]
  CP --> LF["loop filter"]
  LF --> VCO["VCO -> fout"]
  VCO --> DIV["divide by N"]
  DIV --> PFD
```

- **Phase/frequency detector (PFD)** compares the reference phase to the divided
  feedback phase and emits up/down pulses.
- **Charge pump** turns those pulses into a current that dumps charge onto the
  loop filter.
- **Loop filter** (an RC network) integrates that charge into the **control
  voltage**, setting the loop bandwidth and stability.
- **VCO** (voltage-controlled oscillator) outputs a frequency proportional to its
  control voltage, $f_{out} = f_0 + K_{VCO} V_{ctrl}$.
- **Divider (/N)** in the feedback makes the loop synthesize $f_{out} = N
  f_{ref}$ - the basis of **frequency synthesis**.

## VCO tuning and the lock condition

The VCO's frequency rises linearly with control voltage (slide the gain $K_{VCO}$):

```plot
{"title": "VCO tuning: fout = f0 + Kvco * Vctrl, f0=1000 MHz (slide Kvco)", "xLabel": "control voltage (V)", "yLabel": "output frequency (MHz)", "xRange": [0, 1.8], "yRange": [900, 1300], "grid": true, "controls": [{"name": "Kvco", "range": [50, 200], "value": 100, "label": "VCO gain (MHz/V)"}], "functions": [{"expr": "1000 + Kvco*x", "label": "fout"}]}
```

In **lock**, the divided output phase tracks the reference: the PFD nets zero
average current and the control voltage holds steady at whatever value tunes the
VCO to $N f_{ref}$.

## Loop dynamics and jitter

A PLL is a second-order feedback system: too-low loop bandwidth tracks slowly and
lets the VCO's own noise through; too-high bandwidth lets reference noise through
and can ring. The remaining timing error is **jitter** (time domain) or **phase
noise** (frequency domain) - the spec that decides whether a clock is good enough
for an ADC's sampling instant or a radio's carrier. The settling of the control
voltage when the loop acquires lock - press Play:

```plot
{"title": "PLL control voltage settling into lock (press Play)", "xLabel": "time (normalized)", "yLabel": "control voltage (V)", "xRange": [0, 12], "yRange": [0, 1.4], "grid": true, "controls": [{"name": "zeta", "range": [3, 12], "value": 6, "label": "damping (higher = calmer)"}], "animate": {"param": "t", "range": [0, 12], "label": "time"}, "functions": [{"expr": "1 - exp(-zeta/10*x)*cos(1.2*x)", "label": "Vctrl(t)"}], "points": [{"xExpr": "t", "yExpr": "1 - exp(-zeta/10*t)*cos(1.2*t)", "label": "now", "color": "#dc2626", "size": 6, "trail": true}]}
```

```spice
* PLL pieces: charge pump into RC loop filter, VCO as a behavioral source
Icp ctrl 0 PULSE(0 50u 0 1n 1n 5n 100n)
R1 ctrl mid 10k
C1 mid 0 100p
C2 ctrl 0 10p
Bvco out 0 V='sin(6.283*(1e9 + 100e6*V(ctrl))*time)'
.tran 1n 5u
```

```python
import math

fref, N = 10e6, 100
fout = N * fref                     # synthesized output (1 GHz)
Kvco = 100e6                        # VCO gain (Hz/V)
Icp, R, C = 50e-6, 10e3, 100e-12
wn = math.sqrt(Icp * Kvco / (N * C))      # loop natural frequency (rad/s)
zeta = 0.5 * R * math.sqrt(Icp * Kvco * C / N)
print(fout, wn / (2 * math.pi), zeta)
```

**Real-world:** PLLs generate the multi-GHz clocks in every CPU and SoC,
synthesize the carrier in every Wi-Fi/cellular radio, recover the clock in
SerDes links (USB, PCIe, Ethernet), and demodulate FM. Jitter and phase noise are
the figures of merit that gate system performance.

**Next:** measure a converter's real resolution - simulate an ADC and a
delta-sigma spectrum.
""",
        ),
        _code(
            "Lab: ADC ENOB and delta-sigma noise shaping",
            "15 min",
            """\
# Two mixed-signal measurements from scratch, in pure numpy/matplotlib.
#   (1) Quantize a sine with an N-bit ADC -> measure SNR -> ENOB (FFT method).
#   (2) First-order delta-sigma modulator -> show noise shaped to high freq.
import numpy as np
import matplotlib.pyplot as plt

# --- (1) Nyquist ADC ENOB via a coherent FFT ---
N_bits = 10
fs = 1e6
npts = 4096
fin = (37 / npts) * fs              # coherent bin (integer cycles in window)
t = np.arange(npts) / fs
x = 0.49 * np.sin(2 * np.pi * fin * t)

lsb = 1.0 / (2 ** N_bits)
codes = np.round(x / lsb)           # quantize
xq = codes * lsb
win = np.hanning(npts)
X = np.fft.rfft(xq * win)
ps = np.abs(X) ** 2
sig_bin = np.argmax(ps[1:]) + 1
sig_pow = ps[sig_bin - 1: sig_bin + 2].sum()
noise_pow = ps[1:].sum() - sig_pow
sndr = 10 * np.log10(sig_pow / noise_pow)
enob = (sndr - 1.76) / 6.02
freq = np.fft.rfftfreq(npts, 1 / fs)

# --- (2) First-order delta-sigma modulator ---
osr_fin = 2e3
xs = 0.4 * np.sin(2 * np.pi * osr_fin * t)
integ = 0.0
prev = 0.0
bits = np.zeros(npts)
for k in range(npts):
    integ += xs[k] - prev           # delta (subtract feedback) then sigma (integrate)
    prev = 1.0 if integ > 0 else -1.0
    bits[k] = prev
B = np.abs(np.fft.rfft((bits - xs) * win)) ** 2   # quantization-error spectrum

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].plot(freq / 1e3, 10 * np.log10(ps / ps.max() + 1e-20), color="#2563eb")
ax[0].set_title(f"{N_bits}-bit ADC spectrum: SNDR {sndr:.1f} dB, ENOB {enob:.2f}")
ax[0].set_xlabel("frequency (kHz)"); ax[0].set_ylabel("power (dBFS)"); ax[0].grid(True)

ax[1].semilogx(freq[1:] / 1e3, 10 * np.log10(B[1:] / B.max() + 1e-20), color="#9333ea")
ax[1].set_title("Delta-sigma: quantization noise shaped to high freq")
ax[1].set_xlabel("frequency (kHz)"); ax[1].set_ylabel("noise (dB)"); ax[1].grid(True)

plt.tight_layout(); plt.show()

print(f"ideal SNR for {N_bits} bits = {6.02*N_bits + 1.76:.1f} dB")
print(f"measured SNDR = {sndr:.1f} dB -> ENOB = {enob:.2f} bits")
print(f"delta-sigma ones fraction = {(bits > 0).mean():.3f} (tracks the input mean)")

# Try it yourself:
#   1. Raise N_bits to 14: the noise floor drops ~24 dB, ENOB rises ~4 bits.
#   2. The delta-sigma noise rises with frequency (shaping); a real decimator
#      low-pass-filters it away to leave high in-band resolution.
""",
        ),
        _t(
            "Applications and the throughline",
            "12 min",
            """\
# Applications and the throughline

Everything in this track converges in real mixed-signal systems. This lesson maps
the blocks onto products and ties the whole story together.

## Where the blocks land

| System | Analog/mixed-signal blocks at work |
|--------|------------------------------------|
| **Smartphone radio** | LNA (common-gate), PLL synthesizer, delta-sigma/SAR ADC, current-steering DAC, bandgap |
| **Audio codec** | delta-sigma ADC + DAC, SC filters, OTAs, low-noise input amp |
| **CMOS camera** | source-follower pixel, correlated double sampling (flicker cancel), column SAR ADCs, bandgap |
| **Medical (ECG/EEG)** | high-CMRR instrumentation diff pair, chopper-stabilized amp, delta-sigma ADC |
| **Power management (PMIC)** | bandgap reference, error op-amp + feedback, PWM, current sensing |
| **Wireline link (SerDes)** | CDR PLL, pipeline/flash ADC, equalizers, current-mode drivers |

## A worked system: a sensor-to-digital chain

Consider digitizing a microvolt sensor. The path uses **every** course:

```mermaid
flowchart LR
  SENS["sensor (uV)"] --> INA["instrumentation amp: high CMRR diff pair"]
  INA --> AAF["anti-alias SC filter (OTA)"]
  AAF --> ADC["delta-sigma ADC: oversample + noise-shape"]
  ADC --> DEC["decimation filter -> 24-bit words"]
  BG["bandgap reference"] --> ADC
  PLL["PLL clock"] --> ADC
```

The diff pair (Basics) sets CMRR; feedback and noise (Intermediate) set accuracy
and floor; the bandgap sets full-scale; the PLL clocks the sampling; the ADC
(Advanced) sets resolution. The chain is only as good as its weakest block.

## The figures of merit, unified

The whole field optimizes a small set of numbers against each other:

```plot
{"title": "The eternal analog tradeoff triangle (qualitative)", "xLabel": "design effort axis", "yLabel": "relative cost", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "9 - 0.7*x", "label": "noise floor (lower = more power/area)", "color": "#dc2626"}, {"expr": "1 + 0.7*x", "label": "power & area", "color": "#2563eb"}, {"expr": "5", "label": "speed target", "color": "#16a34a"}]}
```

Push noise down (more SNR/ENOB) and you spend power and area; push speed up and
you spend power and lose resolution. The **Walden** and **Schreier** ADC
figures-of-merit (energy per conversion-step, and SNR-bandwidth per watt) make
this tradeoff a single comparable number across chips.

## The throughline

A MOSFET biased in saturation is a transconductor ($g_m$, $r_o$). Pairs of them
make differential amplifiers; mirrors bias them; two stages and feedback make a
precise op-amp; capacitors and clocks make switched-capacitor filters and sampling;
quantization plus oversampling and noise shaping make data converters; and
feedback on phase makes the clocks that run them. From one transistor's square law
to a 24-bit audio chip, it is the same handful of ideas - $g_m r_o$, feedback,
matching, noise, and sampling - composed over and over.

```spice
* The smallest complete mixed-signal cell: bandgap-biased S/H feeding a comparator
Vbg ref 0 1.2
Ssh in cap clk 0 sw
Csh cap 0 1p
Acmp out cap ref comparator
.model sw SW(Ron=200 Roff=1G Vt=0.5)
.model comparator d_comparator
.tran 1n 2u
```

```python
gm, ro = 1e-3, 80e3
intrinsic_gain = gm * ro            # the unit of analog currency
N_bits = 16
snr = 6.02 * N_bits + 1.76          # the unit of converter currency
print(intrinsic_gain, snr)
# From g_m r_o to SNR: the whole track in two numbers.
```

**Real-world:** the engineer who can reason from the transistor's $g_m r_o$ up to
a system's ENOB and jitter budget is the one who can architect the next radio,
sensor, or converter. The components and nodes shrink every generation; the
physics and the tradeoffs do not.

**Next:** the final check.
""",
        ),
    ),
)


ANALOG_IC_COURSES = (_ANALOG_BASICS, _ANALOG_INTERMEDIATE, _ANALOG_ADVANCED)

__all__ = ["ANALOG_IC_COURSES"]
