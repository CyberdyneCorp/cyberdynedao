"""RFIC & RF Circuit Design track: Basics -> Intermediate -> Advanced.

The design of radio-frequency integrated circuits and blocks — low-noise
amplifiers, mixers, oscillators and power amplifiers — as opposed to the
*communications/system* view of the RF & Communication Systems track. Covers why
RF is different (distributed effects), decibels and link budgets, impedance
matching and the Smith chart, S-parameters, transmission lines and resonant
tanks; then noise figure and Friis, linearity (P1dB / IP3), LNA / mixer /
oscillator design and receiver architectures; and finally power amplifiers,
PA linearization, RF PLLs, on-chip passives, layout/packaging and a full
RX front-end design example. Lessons are `text` with LaTeX, interactive
```plot blocks and ```mermaid block diagrams.
"""

# Lesson prose uses typographic characters (×, →, ≈, Ω, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── RFIC & RF Circuit Design — Basics ────────────────────────────────────────

_RF_BASICS = SeedCourse(
    slug="rfic-basics",
    title="RFIC & RF Circuit Design — Basics",
    description=(
        "The foundations a radio-frequency circuit designer needs before drawing "
        "a single transistor: why RF is different (distributed effects), decibels "
        "and dBm, impedance matching and the Smith chart, S-parameters and "
        "two-port networks, transmission lines (reflection and VSWR), and "
        "resonant tanks and matching networks. Interactive plots and block "
        "diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "RF basics: why RF is different",
            "10 min",
            """\
# RF basics: why RF is different

At low frequencies a wire is just a wire — a node has one voltage. At **radio
frequencies** that breaks down. The dividing line is the **wavelength**

$$\\lambda = \\frac{c}{f}.$$

At $1\\,\\text{GHz}$, $\\lambda \\approx 30\\,\\text{cm}$ in free space (less on a PCB or
chip). Once a wire is a non-trivial fraction of $\\lambda$ long, the voltage and
current **vary along it** — the circuit is **distributed**, not lumped.

Consequences that define RF design:

- **Parasitics dominate.** A bond wire is an inductor; a pad is a capacitor; a
  trace is a transmission line. These are the circuit, not afterthoughts.
- **Power, not just voltage, matters.** We deliver power into a load, so
  **impedance matching** (usually to $50\\,\\Omega$) becomes central.
- **Reflections** appear whenever impedances are mismatched.

The plot shows a $1\\,\\text{GHz}$ wave frozen in time along a line: at the marked
quarter-wavelength point the signal is already a quarter-cycle out of phase with
the source — the line has *length*, electrically.

```plot
{"title": "A 1 GHz wave along a transmission line (λ ≈ 30 cm)", "xLabel": "position along line (cm)", "yLabel": "voltage (V)", "xRange": [0, 60], "yRange": [-1.2, 1.2], "functions": [{"expr": "cos(2*pi*x/30)", "label": "V(position)", "color": "#2563eb"}], "points": [{"x": 7.5, "y": 0, "label": "λ/4 (90° phase shift)", "color": "#dc2626", "size": 7}, {"x": 30, "y": 1, "label": "λ (one full cycle)", "color": "#16a34a", "size": 6}]}
```

Everything in this track follows from one idea: **at RF, geometry is circuitry.**

**Next:** the language of RF levels — decibels and dBm.
""",
        ),
        _t(
            "Decibels, dBm & link-budget intuition",
            "10 min",
            """\
# Decibels, dBm & link-budget intuition

RF spans enormous ranges — a transmitter at $1\\,\\text{W}$, a received signal at
$10^{-12}\\,\\text{W}$. We compress that with **decibels** (logarithmic ratios) so
gains and losses simply **add**.

- **Power ratio in dB:** $\\;G_{\\text{dB}} = 10\\log_{10}\\dfrac{P_{\\text{out}}}{P_{\\text{in}}}$.
- **dBm** is power referenced to $1\\,\\text{mW}$: $\\;P_{\\text{dBm}} = 10\\log_{10}\\dfrac{P}{1\\,\\text{mW}}$.

Handy anchors: $0\\,\\text{dBm} = 1\\,\\text{mW}$, $+30\\,\\text{dBm} = 1\\,\\text{W}$,
$-30\\,\\text{dBm} = 1\\,\\mu\\text{W}$. And $+3\\,\\text{dB} \\approx \\times 2$,
$+10\\,\\text{dB} = \\times 10$.

The magic of dB: a chain's output level is just **input plus the gains minus the
losses**, each in dB. That is a **link budget**:

$$P_{\\text{rx}} = P_{\\text{tx}} + G_{\\text{tx}} - L_{\\text{path}} + G_{\\text{rx}}.$$

The plot maps linear power ratio to dB — note how the curve flattens: huge linear
swings become small, addable dB steps.

```plot
{"title": "Power ratio → decibels: 10·log₁₀(ratio)", "xLabel": "power ratio (out/in)", "yLabel": "gain (dB)", "xRange": [0.1, 100], "yRange": [-12, 22], "functions": [{"expr": "10*log(x)/log(10)", "label": "10·log₁₀(ratio)", "color": "#2563eb"}], "points": [{"x": 2, "y": 3.01, "label": "×2 ≈ +3 dB", "color": "#dc2626", "size": 7}, {"x": 10, "y": 10, "label": "×10 = +10 dB", "color": "#16a34a", "size": 6}]}
```

A link budget tells you, before building anything, whether the receiver will even
hear the signal — the spec that drives every block's gain and noise target.

**Next:** matching impedances so that power actually transfers.
""",
        ),
        _t(
            "Impedance matching & the Smith chart",
            "11 min",
            """\
# Impedance matching & the Smith chart

Maximum power transfers from source to load when the load impedance is the
**complex conjugate** of the source. For a real $50\\,\\Omega$ system that means
presenting $50\\,\\Omega$ at every interface. A mismatch reflects power and
ripples the gain.

We quantify the mismatch with the **reflection coefficient**

$$\\Gamma = \\frac{Z_L - Z_0}{Z_L + Z_0},$$

where $Z_0$ is the reference (usually $50\\,\\Omega$). $\\Gamma = 0$ is a perfect
match; $|\\Gamma| = 1$ is total reflection (open or short).

The **Smith chart** is the RF designer's slide rule: it plots every possible
$\\Gamma$ inside the unit circle and overlays the impedance grid, so adding a
series inductor or shunt capacitor becomes a *move along an arc*. Matching = find
a path from the load to the centre ($\\Gamma = 0$).

The plot shows $|\\Gamma|$ for a purely resistive load swept around $50\\,\\Omega$:
the null at $50\\,\\Omega$ is the match; either side reflects.

```plot
{"title": "Reflection magnitude |Γ| vs load resistance (Z₀ = 50 Ω)", "xLabel": "load resistance R_L (Ω)", "yLabel": "|Γ|", "xRange": [1, 250], "yRange": [0, 1], "functions": [{"expr": "sqrt((x-50)^2)/(x+50)", "label": "|Γ| = |R_L−50|/(R_L+50)", "color": "#2563eb"}], "points": [{"x": 50, "y": 0, "label": "perfect match (Γ = 0)", "color": "#16a34a", "size": 7}, {"x": 200, "y": 0.6, "label": "4:1 mismatch", "color": "#dc2626", "size": 6}]}
```

Most RF blocks are specified by their **match** ($S_{11}$, $S_{22}$) as much as
their gain — a mismatched LNA can ring, lose gain or oscillate.

**Next:** the matrix that describes any RF two-port — S-parameters.
""",
        ),
        _t(
            "S-parameters & two-port RF networks",
            "11 min",
            """\
# S-parameters & two-port RF networks

At RF we cannot easily measure open- or short-circuit voltages (those mismatches
reflect and even oscillate), so we characterise a network with **scattering
parameters** — ratios of *incident* and *reflected* travelling waves, all in a
matched $50\\,\\Omega$ environment.

For a two-port (input = port 1, output = port 2):

$$\\begin{bmatrix} b_1 \\\\ b_2 \\end{bmatrix} =
\\begin{bmatrix} S_{11} & S_{12} \\\\ S_{21} & S_{22} \\end{bmatrix}
\\begin{bmatrix} a_1 \\\\ a_2 \\end{bmatrix}.$$

The four parameters have direct meaning:

- $S_{11}$ — **input reflection** (input match / return loss).
- $S_{21}$ — **forward gain** (the one you usually quote in dB).
- $S_{12}$ — **reverse isolation / feedback** (leakage backward; want it small).
- $S_{22}$ — **output reflection** (output match).

The signal-flow picture below shows the waves bouncing through a two-port.

```mermaid
flowchart LR
  A1["incident a₁"] -->|"S₂₁ (gain)"| B2["b₂ → load"]
  A1 -->|"S₁₁ (input reflect)"| B1["b₁ ← back to source"]
  A2["a₂ (from load)"] -->|"S₁₂ (reverse leak)"| B1
  A2 -->|"S₂₂ (output reflect)"| B2
```

The plot sketches a typical amplifier's $|S_{21}|$ (gain) and $|S_{11}|$ (match)
versus frequency: peak gain and best match coincide near the design band.

```plot
{"title": "Amplifier S-parameters vs frequency (qualitative)", "xLabel": "frequency (GHz)", "yLabel": "magnitude (dB)", "xRange": [0.5, 5], "yRange": [-30, 20], "functions": [{"expr": "15 - 6*(x-2.4)^2", "label": "|S₂₁| gain", "color": "#2563eb"}, {"expr": "-5 - 18*exp(-(x-2.4)^2)", "label": "|S₁₁| input match", "color": "#dc2626"}], "points": [{"x": 2.4, "y": 15, "label": "design band 2.4 GHz", "color": "#16a34a", "size": 6}]}
```

A network analyser measures the full S-matrix; it is the universal data sheet of
RF blocks.

**Next:** the wires themselves become circuits — transmission lines.
""",
        ),
        _t(
            "Transmission lines: reflection & VSWR",
            "11 min",
            """\
# Transmission lines: reflection & VSWR

A **transmission line** (coax, microstrip, on-chip line) carries a wave with a
**characteristic impedance** $Z_0$ set by its geometry — not its length. As long
as it is terminated in $Z_0$, the wave is fully absorbed and the line is
"invisible".

Terminate in anything else and part of the wave **reflects**, with coefficient
$\\Gamma = (Z_L - Z_0)/(Z_L + Z_0)$. Forward and reflected waves interfere to form
a **standing wave** — peaks and nulls fixed in space. We summarise its severity
with the **voltage standing-wave ratio**:

$$\\text{VSWR} = \\frac{1 + |\\Gamma|}{1 - |\\Gamma|}.$$

A perfect match is $\\text{VSWR} = 1{:}1$ ($\\Gamma = 0$); a total reflection is
$\\infty{:}1$. Practical specs are often $\\le 1.5{:}1$ or $2{:}1$.

The plot shows the standing-wave envelope $|V| = |1 + \\Gamma e^{-j2\\beta x}|$ along
a mismatched line: ripple between a max of $1+|\\Gamma|$ and a min of $1-|\\Gamma|$,
spaced every half wavelength.

```plot
{"title": "Standing wave on a mismatched line (Γ = 0.4)", "xLabel": "distance from load (λ)", "yLabel": "|V| (normalized)", "xRange": [0, 1.5], "yRange": [0, 1.6], "functions": [{"expr": "sqrt(1 + 0.4^2 + 2*0.4*cos(4*pi*x))", "label": "|V| envelope", "color": "#2563eb"}], "points": [{"x": 0, "y": 1.4, "label": "max = 1+|Γ|", "color": "#dc2626", "size": 6}, {"x": 0.25, "y": 0.6, "label": "min = 1−|Γ|", "color": "#16a34a", "size": 6}]}
```

A useful trick falls out of this: a **quarter-wave line** transforms impedance as
$Z_{\\text{in}} = Z_0^2 / Z_L$ — the basis of many matching networks.

**Next:** turning reactive components into matching with resonant tanks.
""",
        ),
        _t(
            "Resonant tanks & matching networks",
            "10 min",
            """\
# Resonant tanks & matching networks

The workhorse of narrowband RF is the **LC resonant tank**. A parallel
inductor and capacitor exchange energy and present a sharp impedance peak at the
**resonant frequency**

$$f_0 = \\frac{1}{2\\pi\\sqrt{LC}}.$$

Its sharpness is the **quality factor** $Q = f_0 / \\Delta f$ (centre over
$-3\\,\\text{dB}$ bandwidth). High $Q$ → narrow, selective, low-loss; low $Q$ →
broad. Tanks set the frequency of oscillators, the selectivity of filters and
the load of tuned amplifiers.

The plot shows two tanks at the same $f_0$ but different $Q$ — higher $Q$ gives a
taller, narrower peak.

```plot
{"title": "Resonant tank response: sharpness set by Q", "xLabel": "frequency (GHz)", "yLabel": "relative response", "xRange": [1.5, 3.5], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1 + (20*(x-2.4)/2.4)^2)", "label": "high Q (sharp)", "color": "#2563eb"}, {"expr": "1/sqrt(1 + (6*(x-2.4)/2.4)^2)", "label": "low Q (broad)", "color": "#dc2626"}], "points": [{"x": 2.4, "y": 1, "label": "f₀ = 2.4 GHz", "color": "#16a34a", "size": 6}]}
```

To match arbitrary impedances we build **L, π and T networks** from two or three
reactances. The choice trades **bandwidth** against the **transformation ratio**:

```mermaid
flowchart LR
  SRC["source Z_S"] --> L1["L-match: 1 series + 1 shunt (2 elements)"]
  L1 --> PI["π-match: shunt–series–shunt (3 elements)"]
  PI --> T1["T-match: series–shunt–series (3 elements)"]
  T1 --> LOAD["load Z_L (e.g. 50 Ω)"]
```

- **L-match** — simplest; ratio and bandwidth are coupled (no free choice).
- **π / T** — extra element lets you set the loaded $Q$ (bandwidth) independently.

These networks turn the Smith-chart "move to the centre" into real $L$ and $C$
values — the bridge from theory to a built RF circuit.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── RFIC & RF Circuit Design — Intermediate ──────────────────────────────────

_RF_INTERMEDIATE = SeedCourse(
    slug="rfic-intermediate",
    title="RFIC & RF Circuit Design — Intermediate",
    description=(
        "The active RF building blocks and how they fail: noise figure and the "
        "Friis cascade, linearity (1-dB compression and IP3), low-noise amplifier "
        "topologies, mixers (active/passive, conversion gain, image), RF "
        "oscillators and phase noise, and receiver/transmitter architectures "
        "(superheterodyne vs direct conversion). Interactive plots and block "
        "diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Noise in RF: noise figure & Friis",
            "11 min",
            """\
# Noise in RF: noise figure & Friis

Every component adds noise; in a receiver the *first* blocks set how weak a signal
you can still hear. We measure how much a block degrades the signal-to-noise
ratio with the **noise factor** $F$ (linear) and **noise figure**
$NF = 10\\log_{10}F$ (dB):

$$F = \\frac{\\text{SNR}_{\\text{in}}}{\\text{SNR}_{\\text{out}}} \\ge 1.$$

A perfect noiseless block has $F = 1$ ($NF = 0\\,\\text{dB}$). The thermal floor in a
$1\\,\\text{Hz}$ bandwidth is $-174\\,\\text{dBm/Hz}$; sensitivity is that floor plus
bandwidth plus $NF$ plus the required SNR.

For a **cascade**, the famous **Friis formula** combines stages:

$$F_{\\text{tot}} = F_1 + \\frac{F_2 - 1}{G_1} + \\frac{F_3 - 1}{G_1 G_2} + \\dots$$

The lesson: later stages' noise is **divided by the gain ahead of them**, so the
**first stage dominates**. That is why a receiver leads with a low-noise,
high-gain LNA.

```mermaid
flowchart LR
  ANT["antenna"] --> LNA["LNA: low F₁, high G₁ (sets the floor)"]
  LNA --> MIX["mixer: higher F₂, but ÷ G₁"]
  MIX --> IFAMP["IF amp: F₃ ÷ G₁G₂ (almost free)"]
```

The plot shows total $F$ as the first-stage gain $G_1$ rises: more front-end gain
suppresses everything behind it, pushing $F_{\\text{tot}}$ toward $F_1$.

```plot
{"title": "Friis cascade: high G₁ buries later-stage noise", "xLabel": "first-stage gain G₁ (linear)", "yLabel": "total noise factor F_tot", "xRange": [1, 30], "yRange": [1, 7], "functions": [{"expr": "1.6 + (4-1)/x + (10-1)/(x*8)", "label": "F_tot (F₁=1.6)", "color": "#2563eb"}], "points": [{"x": 1, "y": 1.6, "label": "F₁ floor", "color": "#16a34a", "size": 6}]}
```

**Next:** the other way a chain misbehaves — non-linearity.
""",
        ),
        _t(
            "Linearity: 1-dB compression & IP3",
            "12 min",
            """\
# Linearity: 1-dB compression & IP3

Amplifiers are linear only for small signals. Push them harder and gain
**compresses**, then they distort. Two figures of merit capture this.

**1-dB compression point** ($P_{1\\text{dB}}$): the input (or output) level at which
gain has dropped $1\\,\\text{dB}$ below its small-signal value. It marks the top of
the usable range. Below, the ideal line is straight; the real output bends away
and crosses the $1\\,\\text{dB}$-below line.

```plot
{"title": "Gain compression: the 1-dB compression point", "xLabel": "input power (dBm, qualitative)", "yLabel": "output power (dBm)", "xRange": [-30, 5], "yRange": [-20, 25], "functions": [{"expr": "x + 20", "label": "ideal (linear)", "color": "#94a3b8"}, {"expr": "x + 20 - 0.02*(x+30)^2", "label": "real output", "color": "#2563eb"}], "points": [{"x": -5, "y": 1, "label": "≈ P_1dB", "color": "#dc2626", "size": 7}]}
```

**Third-order intercept (IP3)**: with two close tones, third-order mixing creates
**intermodulation** products at $2f_1 - f_2$ and $2f_2 - f_1$ — right in the band,
impossible to filter. The fundamental rises $1\\,\\text{dB/dB}$ while the IM3
products rise $3\\,\\text{dB/dB}$; extrapolate until they meet — that (fictional)
crossing is the **IP3**. Higher IP3 = more linear.

```plot
{"title": "IP3: fundamental (slope 1) vs IM3 (slope 3) intercept", "xLabel": "input power (dBm)", "yLabel": "output power (dBm)", "xRange": [-40, 15], "yRange": [-90, 25], "functions": [{"expr": "x + 15", "label": "fundamental (slope 1)", "color": "#2563eb"}, {"expr": "3*x + 15", "label": "IM3 product (slope 3)", "color": "#dc2626"}], "points": [{"x": 0, "y": 15, "label": "IP3 (extrapolated)", "color": "#16a34a", "size": 7}]}
```

Rule of thumb: $\\text{IP3} \\approx P_{1\\text{dB}} + 10\\,\\text{dB}$. For a cascade the
*inverse* IP3 powers add (referred to input) — and unlike noise, **later high-gain
stages tend to dominate linearity**. Noise and linearity pull in opposite
directions; balancing them is the heart of RX design.

**Next:** the block that must be both quiet and matched — the LNA.
""",
        ),
        _t(
            "The low-noise amplifier (LNA)",
            "11 min",
            """\
# The low-noise amplifier (LNA)

The **LNA** is the receiver's first active stage. By Friis it sets the noise
floor, so it must add minimal noise **while** presenting a good input match
(usually $50\\,\\Omega$) and enough gain to swamp later stages. These goals fight
each other — the input that gives lowest noise is generally *not* $50\\,\\Omega$.

Common integrated topologies:

- **Common-source with inductive degeneration** — the classic. A source inductor
  creates a *real* input resistance from the transistor's $g_m$ and $C_{gs}$
  **without** adding a noisy physical resistor, letting noise-match and
  power-match coincide. The textbook RFIC LNA.
- **Common-gate** — input impedance $\\approx 1/g_m$ gives a naturally broadband
  $50\\,\\Omega$ match, but a higher noise floor.
- **Resistive / shunt-feedback** — broadband and compact, at some noise cost.

```mermaid
flowchart LR
  RFIN["RF in (50 Ω)"] --> LG["gate inductor L_g"]
  LG --> M1["CS transistor M₁ (g_m)"]
  M1 --> LD["tuned load (LC tank)"]
  LD --> RFOUT["RF out"]
  M1 --> LS["source inductor L_s (real Z_in, no noise R)"]
```

The design knob is **input match vs minimum noise**. The plot sketches noise
figure versus the source impedance seen by the device: $NF$ dips at the
*noise-optimum* source resistance, and the art is nudging that optimum toward
$50\\,\\Omega$ so one network does both jobs.

```plot
{"title": "LNA noise figure vs source resistance (the matching trade-off)", "xLabel": "source resistance R_S (Ω)", "yLabel": "noise figure NF (dB)", "xRange": [10, 120], "yRange": [0.5, 4], "functions": [{"expr": "1.2 + 0.0006*(x-55)^2", "label": "NF(R_S)", "color": "#2563eb"}], "points": [{"x": 55, "y": 1.2, "label": "noise-optimum R_S", "color": "#16a34a", "size": 7}, {"x": 50, "y": 1.22, "label": "50 Ω (power match)", "color": "#dc2626", "size": 6}]}
```

**Next:** moving signals up and down in frequency — the mixer.
""",
        ),
        _t(
            "Mixers: conversion gain & image",
            "11 min",
            """\
# Mixers: conversion gain & image

A **mixer** multiplies the RF signal by a **local oscillator (LO)** to translate
it in frequency. Multiplication of two sinusoids produces sum and difference
tones:

$$\\cos(\\omega_{\\text{RF}}t)\\cos(\\omega_{\\text{LO}}t) =
\\tfrac12\\cos(\\omega_{\\text{RF}}-\\omega_{\\text{LO}})t + \\tfrac12\\cos(\\omega_{\\text{RF}}+\\omega_{\\text{LO}})t.$$

A receiver keeps the **difference** (down-conversion to the IF); a transmitter
keeps a sum/difference to up-convert.

Key metrics:

- **Conversion gain** — IF output over RF input (active mixers can have gain;
  passive ones have loss but better linearity).
- **Linearity (IP3)** and **noise** — mixers are typically the linearity
  bottleneck and a noise contributor.
- **Port isolation** — LO leaking to RF/IF causes DC offsets and self-mixing.

The **image problem**: *two* RF frequencies, $f_{\\text{LO}} \\pm f_{\\text{IF}}$, both
land on the same IF. The wanted signal and an unwanted **image** $2 f_{\\text{IF}}$
away fold together — so you must reject the image *before* mixing (filter) or
*by* mixing (image-reject mixer / Hartley / Weaver).

```mermaid
flowchart LR
  RF["RF in"] --> MUL["× (multiplier core)"]
  LO["LO at f_LO"] --> MUL
  MUL --> IF["IF = |f_RF − f_LO|"]
  IMG["image at f_LO∓f_IF (must reject!)"] -. folds onto .-> IF
```

The plot shows wanted and image bands straddling the LO; both map to the same IF.

```plot
{"title": "Mixing: wanted and image both fold to the IF", "xLabel": "frequency (GHz)", "yLabel": "relative level", "xRange": [1.5, 3.5], "yRange": [0, 1.1], "functions": [{"expr": "exp(-40*(x-2.6)^2)", "label": "wanted (f_LO + f_IF)", "color": "#2563eb"}, {"expr": "0.7*exp(-40*(x-2.2)^2)", "label": "image (f_LO − f_IF)", "color": "#dc2626"}], "points": [{"x": 2.4, "y": 0, "label": "LO = 2.4 GHz", "color": "#16a34a", "size": 6}]}
```

**Next:** where the LO comes from — RF oscillators.
""",
        ),
        _t(
            "RF oscillators & phase noise",
            "11 min",
            """\
# RF oscillators & phase noise

An **oscillator** generates the carrier/LO with no input — a resonant tank plus
just enough active gain to cancel its losses (**Barkhausen**: loop gain $\\ge 1$,
phase $= 0^{\\circ}$ at $f_0$). The integrated favourite is the **cross-coupled LC
oscillator**: two transistors in positive feedback present a **negative
resistance** that exactly offsets the tank's loss, sustaining oscillation at

$$f_0 = \\frac{1}{2\\pi\\sqrt{LC}}.$$

```mermaid
flowchart LR
  TANK["LC tank (sets f₀, stores energy)"] --> XC["cross-coupled pair (−R: cancels loss)"]
  XC --> TANK
  TAIL["tail current (sets amplitude)"] --> XC
  TANK --> BUF["buffer → LO out"]
```

No real oscillator is a perfect tone. **Phase noise** is random jitter of the
phase, seen as skirts around the carrier and quoted in $\\text{dBc/Hz}$ at an
offset (e.g. $-110\\,\\text{dBc/Hz}$ at $1\\,\\text{MHz}$). It corrupts the LO and, via
mixing, every received channel (reciprocal mixing) — it is *the* spec that
distinguishes a good RF oscillator. **Leeson's** insight: phase noise improves
with **higher tank $Q$** and **higher signal power**, and falls as $1/(\\Delta
f)^2$ away from the carrier.

```plot
{"title": "Oscillator phase noise skirt (lower with higher Q)", "xLabel": "offset from carrier (MHz)", "yLabel": "phase noise (dBc/Hz)", "xRange": [0.05, 5], "yRange": [-130, -70], "functions": [{"expr": "-100 - 20*log(x)/log(10)", "label": "high-Q tank", "color": "#2563eb"}, {"expr": "-88 - 20*log(x)/log(10)", "label": "low-Q tank", "color": "#dc2626"}], "points": [{"x": 1, "y": -100, "label": "−100 dBc/Hz @ 1 MHz", "color": "#16a34a", "size": 6}]}
```

**Next:** assembling LNA, mixer and LO into a radio — RX/TX architectures.
""",
        ),
        _t(
            "Receiver & transmitter architectures",
            "12 min",
            """\
# Receiver & transmitter architectures

The blocks now snap together into a radio. Two classic receiver architectures:

**Superheterodyne** — down-convert to a fixed **intermediate frequency (IF)** in
one or two steps, do most of the filtering and gain there, then demodulate. Great
selectivity and dynamic range; the price is the **image** problem and bulky IF
filters.

**Direct-conversion (zero-IF / homodyne)** — mix straight to baseband
($f_{\\text{IF}} = 0$) using **I/Q** (two mixers driven by LO at $0^{\\circ}$ and
$90^{\\circ}$). No image filter, highly integrable — but suffers **DC offsets**
(LO self-mixing), **flicker noise** and **I/Q imbalance**. It dominates modern
RFICs because it integrates on a single chip.

```mermaid
flowchart LR
  ANT["antenna"] --> RFF["RF filter"]
  RFF --> LNA["LNA"]
  LNA --> MI["mixer I"]
  LNA --> MQ["mixer Q"]
  LOI["LO 0°"] --> MI
  LOQ["LO 90°"] --> MQ
  MI --> BBI["baseband I (LPF + gain + ADC)"]
  MQ --> BBQ["baseband Q (LPF + gain + ADC)"]
```

A **transmitter** runs it in reverse: baseband I/Q → up-conversion mixers →
combine → power amplifier → antenna. The same noise/linearity trade-offs apply,
but now linearity and *efficiency* of the PA dominate.

The plot contrasts the two RX plans on the frequency axis: superhet parks the
signal at a non-zero IF (image to reject), zero-IF lands it at DC (offset/flicker
near zero).

```plot
{"title": "Where the signal lands: superhet IF vs zero-IF baseband", "xLabel": "frequency (MHz, post-mix)", "yLabel": "relative level", "xRange": [-5, 80], "yRange": [0, 1.1], "functions": [{"expr": "exp(-0.02*(x-45)^2)", "label": "superhet (at IF)", "color": "#2563eb"}, {"expr": "exp(-0.05*x^2)", "label": "zero-IF (at DC)", "color": "#dc2626"}], "points": [{"x": 0, "y": 1, "label": "DC offset / flicker", "color": "#16a34a", "size": 6}]}
```

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── RFIC & RF Circuit Design — Advanced ──────────────────────────────────────

_RF_ADVANCED = SeedCourse(
    slug="rfic-advanced",
    title="RFIC & RF Circuit Design — Advanced",
    description=(
        "The hard problems of an RF chip: power-amplifier classes and the "
        "efficiency-vs-linearity trade-off, PA linearization (back-off, "
        "predistortion, Doherty), frequency synthesis with integer/fractional-N "
        "PLLs, on-chip passives and their Q, RFIC layout/packaging and EM "
        "coupling, and a worked RX front-end design example from spec to "
        "NF/IP3 budget. Interactive plots and block diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Power amplifiers: classes & efficiency",
            "12 min",
            """\
# Power amplifiers: classes & efficiency

The **power amplifier (PA)** delivers the transmit signal to the antenna and
usually burns the most power on the chip — so its **efficiency** matters as much
as its linearity. The two clash, and the **class** names the chosen point on that
trade-off, set largely by the **conduction angle** (how much of each RF cycle the
device conducts).

- **Class A** — conducts the full $360^{\\circ}$. Most linear, but theoretical max
  drain efficiency only $50\\%$ (and far less backed off).
- **Class B** — $180^{\\circ}$; max efficiency $\\approx 78.5\\%$, with crossover
  distortion.
- **Class AB** — between A and B; the practical default for *linear* PAs.
- **Class C** — $<180^{\\circ}$; higher efficiency, non-linear (constant-envelope
  signals only).
- **Switching classes D, E, F** — the transistor is a *switch*, not an amplifier;
  ideally $100\\%$ efficient (Class E shapes the voltage to avoid switching loss,
  Class F shapes harmonics into a square wave). Highest efficiency, hardest to
  keep linear.

```mermaid
flowchart LR
  LIN["linear: Class A → AB → B (efficiency ↑, linearity ↓)"]
  LIN --> NL["Class C (constant-envelope only)"]
  NL --> SW["switching: Class D / E / F (≈100% ideal, non-linear)"]
```

The plot shows the canonical curve: drain efficiency rises as conduction angle
shrinks (toward Class C/switching), trading off the linearity you keep at Class A.

```plot
{"title": "PA efficiency rises as conduction angle shrinks", "xLabel": "conduction angle (degrees)", "yLabel": "max drain efficiency (%)", "xRange": [120, 360], "yRange": [40, 100], "functions": [{"expr": "50 + 0.18*(360-x)", "label": "efficiency trend", "color": "#2563eb"}], "points": [{"x": 360, "y": 50, "label": "Class A (50%)", "color": "#dc2626", "size": 6}, {"x": 180, "y": 78, "label": "Class B (78.5%)", "color": "#16a34a", "size": 6}]}
```

**Next:** keeping a PA linear *and* efficient — linearization.
""",
        ),
        _t(
            "PA linearization: back-off, predistortion, Doherty",
            "12 min",
            """\
# PA linearization: back-off, predistortion, Doherty

Modern signals (OFDM, high-order QAM) have a high **peak-to-average power ratio
(PAPR)** — large momentary peaks. To keep peaks below $P_{1\\text{dB}}$, the simple
fix is **back-off**: run the PA well below saturation. It works but is *wasteful*,
because efficiency collapses at low output.

```plot
{"title": "Back-off kills efficiency; Doherty recovers it", "xLabel": "output power below peak (dB back-off)", "yLabel": "drain efficiency (%)", "xRange": [0, 12], "yRange": [0, 80], "functions": [{"expr": "65*exp(-0.18*x)", "label": "Class B (collapses)", "color": "#dc2626"}, {"expr": "62 - 1.5*x", "label": "Doherty (flat over back-off)", "color": "#2563eb"}], "points": [{"x": 6, "y": 50, "label": "typical 6 dB back-off", "color": "#16a34a", "size": 6}]}
```

Better approaches recover efficiency *and* linearity:

- **Digital predistortion (DPD)** — pre-warp the input with the *inverse* of the
  PA's distortion so the cascade is linear; the dominant technique in modern
  basestations and phones.
- **Doherty PA** — a **main** amplifier plus a **peaking** amplifier that turns on
  only for peaks, with an output-combining network (a quarter-wave line) that
  keeps efficiency high across a wide back-off range.
- **Envelope tracking (ET)** — modulate the supply voltage to follow the signal
  envelope so the device stays near saturation (efficient) instantly.

```mermaid
flowchart LR
  IN["RF in (high PAPR)"] --> SPLIT["splitter"]
  SPLIT --> MAIN["main PA (Class AB, always on)"]
  SPLIT --> PEAK["peaking PA (Class C, on at peaks)"]
  MAIN --> COMB["λ/4 combiner (load modulation)"]
  PEAK --> COMB
  COMB --> ANT["antenna"]
```

The choice is a system trade: DPD adds DSP, Doherty adds RF complexity, ET adds a
fast supply modulator — all to claw back the efficiency back-off throws away.

**Next:** generating clean, agile carriers — RF PLLs.
""",
        ),
        _t(
            "Frequency synthesis: integer & fractional-N PLLs",
            "12 min",
            """\
# Frequency synthesis: integer & fractional-N PLLs

Radios must hop to precise, switchable carrier frequencies locked to a crystal.
The **phase-locked loop (PLL)** does this: a **phase-frequency detector (PFD)**
compares a divided VCO output against the reference, a **charge pump + loop
filter** turns phase error into a control voltage, and the **VCO** retunes until
the loop locks. A feedback **divider $\\div N$** sets the output:

$$f_{\\text{out}} = N \\cdot f_{\\text{ref}}.$$

```mermaid
flowchart LR
  REF["reference f_ref (crystal)"] --> PFD["PFD"]
  PFD --> CP["charge pump + loop filter"]
  CP --> VCO["VCO → f_out"]
  VCO --> DIV["÷ N divider"]
  DIV --> PFD
```

- **Integer-N** — $N$ is an integer, so the **channel step equals $f_{\\text{ref}}$**.
  Fine steps force a small $f_{\\text{ref}}$, which forces a *narrow* loop bandwidth
  (slow) and a *large* $N$ (which multiplies in-band phase noise by $20\\log N$).
- **Fractional-N** — a $\\Sigma\\Delta$ modulator **dithers** $N$ between integers so
  the *average* divide ratio is fractional. This decouples step size from
  $f_{\\text{ref}}$: keep a high reference (fast loop, low $N$) yet get fine
  resolution — at the cost of **quantization (fractional) spurs** the modulator
  must noise-shape away.

The loop is a classic bandwidth trade-off: the plot shows total phase noise as the
loop bandwidth widens — wide tracks the VCO (good far out, lets reference noise
in close), narrow does the reverse; the optimum minimizes the integrated jitter.

```plot
{"title": "PLL phase noise vs loop bandwidth (find the crossover)", "xLabel": "offset frequency (relative)", "yLabel": "phase noise (dBc/Hz)", "xRange": [0.05, 5], "yRange": [-130, -80], "functions": [{"expr": "-118 + 6*x", "label": "reference + ÷N (in-band)", "color": "#2563eb"}, {"expr": "-92 - 20*log(x)/log(10)", "label": "free-running VCO", "color": "#dc2626"}], "points": [{"x": 1, "y": -92, "label": "loop bandwidth (crossover)", "color": "#16a34a", "size": 6}]}
```

**Next:** the inductors and transformers these loops and tanks rely on.
""",
        ),
        _t(
            "On-chip passives: inductors, Q & transformers",
            "11 min",
            """\
# On-chip passives: inductors, Q & transformers

Tanks, matching and PLLs all need inductors — but on silicon an inductor is a
**spiral** of metal over a lossy, conductive substrate, and it is the *worst*
component on the chip. Its **quality factor**

$$Q = \\frac{\\omega L}{R_s}$$

is limited by metal series resistance $R_s$, skin effect, and **substrate eddy
currents** that couple through the silicon. On-chip $Q$ is typically only
$5\\text{–}20$ (versus hundreds for a discrete coil), and it directly caps
oscillator phase noise (Leeson) and filter selectivity.

Design levers: thick top **metal**, wider/optimal turn width, **patterned ground
shields** to break substrate eddy currents, and not over-sizing $L$ (self-resonance
from parasitic capacitance sets a usable ceiling). The plot shows the classic
**$Q$ peak**: $Q$ rises with frequency until losses and self-resonance pull it back
down — you design the inductor so its peak sits in your band.

```plot
{"title": "On-chip spiral inductor Q peaks, then self-resonance kills it", "xLabel": "frequency (GHz)", "yLabel": "quality factor Q", "xRange": [0.5, 12], "yRange": [0, 16], "functions": [{"expr": "14*exp(-(x-4)^2/12)", "label": "Q(f)", "color": "#2563eb"}], "points": [{"x": 4, "y": 14, "label": "Q peak (design here)", "color": "#16a34a", "size": 7}, {"x": 10, "y": 4, "label": "near self-resonance", "color": "#dc2626", "size": 6}]}
```

**Transformers** (two coupled spirals) are workhorses too: they provide
**impedance transformation** (turns ratio), **single-ended ↔ differential**
conversion (**baluns**), DC isolation and bias injection. They appear in
differential LNAs, mixers and PA output combiners.

```mermaid
flowchart LR
  PRI["primary coil (single-ended in)"] -->|"magnetic coupling k"| SEC["secondary coil"]
  SEC --> DIFF["differential / matched out"]
  PRI --> BIAS["DC bias injected at center tap"]
```

**Next:** even with great devices, the *layout* can wreck the RFIC.
""",
        ),
        _t(
            "RFIC layout, packaging & EM coupling",
            "11 min",
            """\
# RFIC layout, packaging & EM coupling

At RF the **layout is the schematic**. A few microns of metal is an inductor; two
nearby traces are a coupling capacitor; the package and bond wires are part of
the matching network. Sloppy layout turns a working circuit into an oscillator,
a desensitised receiver, or a failed match.

The dominant hazards:

- **Parasitics** — every interconnect adds $L$, $C$ and $R$ that detune tanks and
  matching; extract and re-simulate (post-layout) before trusting anything.
- **EM coupling** — inductors radiate and pick up; the LO can couple into the LNA,
  or the PA into the VCO ("pulling"). Fixes: spacing, orientation, guard rings,
  **patterned ground shields**, and symmetry.
- **Substrate coupling** — digital switching noise travels through the common
  silicon into sensitive analog/RF nodes. Use **deep n-well isolation**, separate
  supplies and guard rings.
- **Grounding & supply** — a shared inductive ground/bond wire creates feedback
  and instability; use many bond wires, on-chip decoupling, and a clean RF ground.
- **Packaging** — bond-wire inductance ($\\sim 1\\,\\text{nH/mm}$) and package
  parasitics shift the match; flip-chip / wafer-level packaging reduces it.

```mermaid
flowchart LR
  PA["PA (loud aggressor)"] -. EM / substrate coupling .-> VCO["VCO (victim → pulling)"]
  DIG["digital switching"] -. substrate noise .-> LNA["LNA (victim → desense)"]
  GUARD["guard rings + deep n-well + ground shields"] --> ISO["isolation"]
```

The plot shows how unwanted coupling falls with separation — every extra few
microns or guard structure buys isolation, the currency of a clean RF layout.

```plot
{"title": "Isolation improves with separation / shielding", "xLabel": "separation (relative)", "yLabel": "coupling isolation (dB)", "xRange": [1, 20], "yRange": [10, 70], "functions": [{"expr": "20 + 30*log(x)/log(10)", "label": "isolation (more = better)", "color": "#2563eb"}], "points": [{"x": 1, "y": 20, "label": "tight (risky)", "color": "#dc2626", "size": 6}, {"x": 10, "y": 50, "label": "well-spaced + shielded", "color": "#16a34a", "size": 6}]}
```

**Next:** put it all together — a full RX front-end budget.
""",
        ),
        _t(
            "Design example: an RX front-end from spec to budget",
            "12 min",
            """\
# Design example: an RX front-end from spec to budget

Time to design top-down. Suppose a $2.4\\,\\text{GHz}$ receiver must hit:
**sensitivity $-95\\,\\text{dBm}$** in a $10\\,\\text{MHz}$ channel needing
**SNR $= 10\\,\\text{dB}$**, with a strong nearby interferer demanding
**input IP3 $\\ge -10\\,\\text{dBm}$**.

**Step 1 — noise budget.** Thermal floor is $-174\\,\\text{dBm/Hz}$; in
$10\\,\\text{MHz}$ ($+70\\,\\text{dB}$) the noise is $-104\\,\\text{dBm}$. With the SNR
requirement, the allowed **system noise figure** is

$$NF_{\\text{sys}} = \\underbrace{-95}_{\\text{sens}} - \\underbrace{(-104)}_{\\text{floor}} - \\underbrace{10}_{\\text{SNR}} = -1?\\;\\Rightarrow\\;NF_{\\text{sys}} \\le 9\\,\\text{dB}.$$

(Sensitivity $=$ floor $+ NF + $ SNR, so $NF \\le -95 - (-104) - 10 + 10 = 9\\,\\text{dB}$ — comfortable; budget the chain to $\\sim 4\\,\\text{dB}$ for margin.)

**Step 2 — allocate blocks (Friis & inverse-IP3).** Front-end gain suppresses
later noise but *worsens* linearity. A first cut:

```mermaid
flowchart LR
  ANT["antenna"] --> LNA["LNA: G=15 dB, NF=1.5 dB, IIP3=0 dBm"]
  LNA --> MIX["mixer: G=8 dB, NF=10 dB, IIP3=+5 dBm"]
  MIX --> FILT["IF/BB filter: loss 2 dB"]
  FILT --> VGA["VGA + ADC driver: NF=15 dB, IIP3=+15 dBm"]
```

Apply **Friis**: $F_2$ is divided by the LNA gain ($\\times 31.6$), so the mixer's
$10\\,\\text{dB}$ $NF$ contributes little — total $NF \\approx 2.5\\text{–}3\\,\\text{dB}$. Apply
**inverse IP3** (input-referred): the *highest-gain-ahead* stage hurts linearity
most, so the LNA's IIP3 dominates and the cascade IIP3 lands near
$-7\\,\\text{dBm}$ — meeting the $-10\\,\\text{dBm}$ target with margin.

**Step 3 — the tension, visualised.** Increasing LNA gain *lowers* the NF curve
(better noise) but *lowers* the cascade IIP3 (worse linearity). The design point
is where both specs are met with margin — exactly where the two curves bracket
the target band.

```plot
{"title": "RX front-end: LNA gain trades noise figure vs linearity", "xLabel": "LNA gain (dB)", "yLabel": "level (dB / dBm)", "xRange": [6, 24], "yRange": [-14, 6], "functions": [{"expr": "5 - 0.12*x", "label": "cascade NF (dB) — falls", "color": "#2563eb"}, {"expr": "2 - 0.5*x + 0.008*x^2", "label": "cascade IIP3 (dBm) — falls", "color": "#dc2626"}], "points": [{"x": 15, "y": 3.2, "label": "NF spec met", "color": "#16a34a", "size": 6}, {"x": 15, "y": -7, "label": "IIP3 ≥ −10 dBm met", "color": "#16a34a", "size": 6}]}
```

**The takeaway:** RFIC design is **budgeting** — translate a system spec into a
noise/linearity/gain allocation per block, check it with Friis and inverse-IP3,
then design each block (LNA, mixer, LO, PA) to its slice. Every earlier lesson
plugs into one cell of this table.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


RFIC_COURSES: tuple[SeedCourse, ...] = (_RF_BASICS, _RF_INTERMEDIATE, _RF_ADVANCED)

__all__ = ["RFIC_COURSES"]
