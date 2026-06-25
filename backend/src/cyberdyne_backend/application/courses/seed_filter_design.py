"""Filter Design track: Basics -> Intermediate -> Advanced.

From what a filter is and how to read a Bode plot, through passive RC/RL/RLC
networks and op-amp active topologies (Sallen-Key, multiple-feedback), to the
classical approximations (Butterworth, Chebyshev, elliptic, Bessel), pole-zero
placement, switched-capacitor filters and the bridge to digital IIR design.
Lessons are `text` with LaTeX, interactive ```plot magnitude/step responses and
```mermaid topology diagrams. Builds on the Signals and Electronics courses.
"""

# Lesson prose uses typographic characters (×, →, ≈, ω, Ω, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Filter Design — Basics ───────────────────────────────────────────────────

_FD_BASICS = SeedCourse(
    slug="filter-design-basics",
    title="Filter Design — Basics",
    description=(
        "What a filter is and the four response types, reading decibels and Bode "
        "plots, passive first-order RC/RL filters, second-order RLC resonance and "
        "Q, reading a frequency-response specification, and the transfer function "
        "H(s). The vocabulary and intuition behind every filter, with interactive "
        "magnitude plots."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What a filter is & the four response types",
            "10 min",
            r"""\
# What a filter is & the four response types

A **filter** is a circuit (or algorithm) that passes some frequencies and
attenuates others. Feed in a signal made of many frequencies and the filter
reshapes its spectrum — keeping the **passband**, suppressing the **stopband**.

Four canonical responses cover almost everything:

- **Low-pass (LP)** — passes low frequencies, blocks high ones (smoothing,
  anti-aliasing).
- **High-pass (HP)** — passes high frequencies, blocks low ones (DC blocking,
  rumble removal).
- **Band-pass (BP)** — passes a band around a centre frequency (radio tuning).
- **Band-stop / notch (BS)** — rejects a narrow band (killing 50/60 Hz hum).

Here is an ideal-ish low-pass magnitude rolling off past its cutoff — everything
to the right is increasingly attenuated:

```plot
{"title": "Low-pass magnitude rolls off past the cutoff", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 5], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+x^2)", "label": "|H(jω)| low-pass", "color": "#2563eb"}], "points": [{"x": 1, "y": 0.707, "label": "cutoff (−3 dB)", "color": "#dc2626", "size": 7}]}
```

A high-pass is the mirror image; a band-pass is a low-pass and high-pass stacked
together. The block-level picture of the four types:

```mermaid
flowchart LR
    IN([input spectrum]) --> LP[Low-pass: keep lows]
    IN --> HP[High-pass: keep highs]
    IN --> BP[Band-pass: keep a band]
    IN --> BS[Band-stop: reject a band]
    LP --> OUT([output spectrum])
    HP --> OUT
    BP --> OUT
    BS --> OUT
```

**Next:** the language of decibels, cutoff and roll-off.
""",
        ),
        _t(
            "Decibels, cutoff & roll-off: reading a Bode plot",
            "11 min",
            r"""\
# Decibels, cutoff & roll-off: reading a Bode plot

Filter response is read on a **Bode plot**: magnitude in **decibels** versus
frequency.

- **Decibel** of a voltage ratio: $|H|_{\mathrm{dB}} = 20\log_{10}|H|$. So a gain
  of $1$ is $0\,$dB, $0.707$ is $-3\,$dB, $0.5$ is $-6\,$dB, $0.1$ is $-20\,$dB.
- **Cutoff frequency** $\omega_c$ — where the magnitude has fallen to
  $1/\sqrt2 \approx 0.707$ of its passband value, i.e. **$-3\,$dB** (half power).
- **Roll-off** — the slope in the stopband, measured in **dB/decade** (per ×10 in
  frequency) or **dB/octave** (per ×2). A first-order filter rolls off at
  $-20\,$dB/decade ($-6\,$dB/octave); each extra order adds another $-20$.

The $-3\,$dB point (red) is the agreed border between passband and stopband:

```plot
{"title": "Cutoff is the −3 dB point (|H| = 0.707)", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 5], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+x^2)", "label": "first-order low-pass", "color": "#2563eb"}], "points": [{"x": 1, "y": 0.707, "label": "−3 dB cutoff", "color": "#dc2626", "size": 7}]}
```

Because Bode plots use a logarithmic frequency axis, the asymptotes become
straight lines and you can sketch a response by hand from poles and zeros alone.

**Next:** the simplest real filters — passive RC and RL.
""",
        ),
        _t(
            "Passive first-order filters: RC & RL",
            "11 min",
            r"""\
# Passive first-order filters: RC & RL

The simplest filter is one resistor and one reactive element.

**RC low-pass** — output across the capacitor:

$$H(j\omega) = \frac{1}{1 + j\omega RC}, \qquad \omega_c = \frac{1}{RC}.$$

Its magnitude is $|H| = 1/\sqrt{1+(\omega/\omega_c)^2}$ and its phase lags from
$0°$ toward $-90°$, passing $-45°$ exactly at the cutoff. The **RL filter** does
the same job with an inductor ($\omega_c = R/L$). Swap which element you tap and
LP becomes HP. Magnitude (blue) crosses $0.707$ at the cutoff:

```plot
{"title": "First-order RC low-pass magnitude", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 6], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+x^2)", "label": "|H(jω)|", "color": "#2563eb"}], "points": [{"x": 1, "y": 0.707, "label": "−3 dB", "color": "#dc2626", "size": 6}]}
```

The high-pass is the complement — it climbs from $0$ to $1$:

```plot
{"title": "First-order RC high-pass magnitude", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 6], "yRange": [0, 1.1], "functions": [{"expr": "x/sqrt(1+x^2)", "label": "|H(jω)| high-pass", "color": "#16a34a"}], "points": [{"x": 1, "y": 0.707, "label": "−3 dB", "color": "#dc2626", "size": 6}]}
```

The RC low-pass as a voltage divider of frequency-dependent impedances:

```mermaid
flowchart LR
    VIN([Vin]) --> R[R]
    R --> N((node))
    N --> VOUT([Vout])
    N --> C[C]
    C --> GND([ground])
```

First-order filters are gentle ($-20\,$dB/decade) — fine for smoothing, too soft
when you need a sharp edge.

**Next:** add an inductor and a capacitor for resonance.
""",
        ),
        _t(
            "Second-order RLC filters: resonance & Q",
            "11 min",
            r"""\
# Second-order RLC filters: resonance & Q

Put R, L and C together and you get a **second-order** filter that can be sharp —
and can **resonate**. Its low-pass transfer function is

$$H(s) = \frac{\omega_0^2}{s^2 + \dfrac{\omega_0}{Q}\,s + \omega_0^2},$$

with **natural frequency** $\omega_0 = 1/\sqrt{LC}$ and **quality factor** $Q$
setting how peaked the response is. High $Q$ → a tall resonant bump near
$\omega_0$ and a fast $-40\,$dB/decade roll-off; low $Q$ → a smooth, well-damped
curve. Slide $Q$ and watch the peak grow:

```plot
{"title": "Second-order low-pass: Q controls the resonant peak", "xLabel": "ω/ω₀", "yLabel": "|H|", "xRange": [0, 3], "yRange": [0, 4], "controls": [{"name": "Q", "range": [0.4, 8], "value": 2, "label": "quality factor Q"}], "functions": [{"expr": "1/sqrt((1-x^2)^2 + (x/Q)^2)", "label": "|H(jω)|", "color": "#2563eb"}], "points": [{"x": 1, "y": 0, "label": "ω₀", "color": "#dc2626", "size": 6}]}
```

- $Q = 0.707$ (**maximally flat**, Butterworth) — no peak, the flattest passband.
- $Q < 0.5$ — overdamped, two real poles.
- $Q$ large — a sharp, narrow band-pass when tapped across the resistor.

The series RLC topology:

```mermaid
flowchart LR
    VIN([Vin]) --> L[L]
    L --> R[R]
    R --> N((node))
    N --> VOUT([Vout])
    N --> C[C]
    C --> GND([ground])
```

Resonance is power: it makes band-pass and notch filters possible, but a high-Q
circuit also rings and is sensitive to component values.

**Next:** how a spec sheet describes all of this.
""",
        ),
        _t(
            "Reading a frequency-response specification",
            "10 min",
            r"""\
# Reading a frequency-response specification

A filter **specification** is a contract drawn as a tolerance template the
response must fit inside. Four numbers define it:

- **Passband edge** $\omega_p$ and **maximum passband ripple** $A_p$ (dB) — how
  much the gain may wobble where signal should pass.
- **Stopband edge** $\omega_s$ and **minimum stopband attenuation** $A_s$ (dB) —
  how far down unwanted frequencies must be pushed.

The **transition band** sits between $\omega_p$ and $\omega_s$; the narrower you
demand it, the higher the filter **order** you will need. A response that stays
above $-A_p$ in the passband and below $-A_s$ in the stopband "meets spec":

```plot
{"title": "A spec: stay in the passband, drop below the stopband limit", "xLabel": "ω/ωp", "yLabel": "|H|", "xRange": [0, 4], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+x^6)", "label": "candidate |H|", "color": "#2563eb"}], "points": [{"x": 1, "y": 0.95, "label": "passband edge ωp", "color": "#16a34a", "size": 6}, {"x": 2, "y": 0.1, "label": "stopband edge ωs (≤ −20 dB)", "color": "#dc2626", "size": 6}]}
```

Reading a spec is the first design step: it tells you the **type** (LP/HP/BP/BS),
the **steepness** (order) and the **flavour** (flat vs rippled vs sharp) before
you choose a single component.

**Next:** the compact mathematical description — H(s).
""",
        ),
        _t(
            "The transfer function H(s) of a filter",
            "12 min",
            r"""\
# The transfer function H(s) of a filter

Every linear filter is captured by one object: its **transfer function**

$$H(s) = \frac{N(s)}{D(s)} = \frac{b_m s^m + \dots + b_0}{a_n s^n + \dots + a_0},$$

a ratio of polynomials in the complex frequency $s = \sigma + j\omega$.

- The roots of the numerator $N(s)$ are the **zeros** — frequencies the filter
  *kills* (a notch sits on the $j\omega$ axis at its zero).
- The roots of the denominator $D(s)$ are the **poles** — they set the resonances
  and must lie in the **left half-plane** for the filter to be stable.
- The **order** $n$ is the number of poles; it fixes the ultimate roll-off,
  $-20n\,$dB/decade.

Evaluate $H$ on the imaginary axis, $s = j\omega$, to read the steady-state
**frequency response** $H(j\omega)$ — exactly the magnitude curves you have been
plotting. A second-order low-pass written this way gives the familiar shape:

```plot
{"title": "Magnitude of H(jω) for a 2nd-order low-pass (Q = 0.707)", "xLabel": "ω/ω₀", "yLabel": "|H|", "xRange": [0, 3], "yRange": [0, 1.2], "functions": [{"expr": "1/sqrt((1-x^2)^2 + (x*1.414)^2)", "label": "|H(jω)|", "color": "#2563eb"}], "points": [{"x": 1, "y": 0.707, "label": "ω₀ (−3 dB)", "color": "#dc2626", "size": 6}]}
```

From $H(s)$ you can read everything: the magnitude, the phase, the step response
and the stability. The rest of this track is about *choosing* $H(s)$ — its order
and pole-zero pattern — to meet a spec, then realising it in hardware.

**Next:** test what you have learned.
""",
        ),
        _quiz(),
    ),
)

# ── Filter Design — Intermediate ─────────────────────────────────────────────

_FD_INTERMEDIATE = SeedCourse(
    slug="filter-design-intermediate",
    title="Filter Design — Intermediate",
    description=(
        "Building active filters with op-amps: the ideal op-amp and inverting / "
        "non-inverting stages, active first-order filters, the Sallen-Key 2nd-order "
        "low-pass and high-pass, the multiple-feedback band-pass, filter order and "
        "cascading stages, and sensitivity & component selection. Where filter "
        "design becomes practical, with interactive plots and stage diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Op-amp basics for filters",
            "11 min",
            r"""\
# Op-amp basics for filters

Active filters replace lossy inductors with **op-amps**, capacitors and
resistors. Start from the **ideal op-amp**:

- Infinite open-loop gain, infinite input impedance, zero output impedance.
- With negative feedback, the two **golden rules** hold: no current flows into
  the inputs, and the inputs sit at the **same voltage** ("virtual short").

Two building blocks recur everywhere:

- **Inverting amplifier:** $V_{out} = -\dfrac{R_f}{R_{in}}V_{in}$. The "−" input
  is a **virtual ground**, which makes node equations easy.
- **Non-inverting amplifier:** $V_{out} = \left(1 + \dfrac{R_f}{R_g}\right)V_{in}$,
  with very high input impedance.

The non-inverting stage's gain vs the feedback ratio $R_f/R_g$:

```plot
{"title": "Non-inverting gain = 1 + Rf/Rg", "xLabel": "Rf/Rg", "yLabel": "gain", "xRange": [0, 10], "yRange": [0, 12], "functions": [{"expr": "1 + x", "label": "1 + Rf/Rg", "color": "#2563eb"}]}
```

The inverting and non-inverting stages side by side:

```mermaid
flowchart LR
    subgraph Inverting
      VINA([Vin]) --> RIN[Rin] --> M((−))
      M --> OPA[op-amp] --> VOA([Vout])
      OPA -. Rf .-> M
      P((+)) --> GNDA([ground])
      P --> OPA
    end
    subgraph NonInverting
      VINB([Vin]) --> PP((+)) --> OPB[op-amp] --> VOB([Vout])
      OPB -. Rf .-> MM((−))
      MM -. Rg .-> GNDB([ground])
    end
```

Because the op-amp **buffers** the output, you can cascade stages without each
one loading the last — the key advantage over passive filters.

**Next:** the first active filters.
""",
        ),
        _t(
            "Active first-order filters",
            "10 min",
            r"""\
# Active first-order filters

Take the inverting amplifier and make one impedance frequency-dependent.

**Active low-pass:** put a capacitor $C_f$ across the feedback resistor $R_f$. The
feedback impedance falls at high frequency, so gain rolls off:

$$H(s) = -\frac{R_f}{R_{in}}\cdot\frac{1}{1 + s R_f C_f}, \qquad
\omega_c = \frac{1}{R_f C_f}.$$

You now get **passband gain and filtering at once** — something a passive RC
cannot do. **Active high-pass:** instead put a capacitor in series with the input
resistor. The magnitude of the active low-pass (with passband gain $K = 2$):

```plot
{"title": "Active first-order low-pass with gain K = 2", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 6], "yRange": [0, 2.2], "functions": [{"expr": "2/sqrt(1+x^2)", "label": "|H| = K/√(1+(ω/ωc)²)", "color": "#2563eb"}], "points": [{"x": 1, "y": 1.414, "label": "−3 dB from K", "color": "#dc2626", "size": 6}]}
```

The active low-pass stage:

```mermaid
flowchart LR
    VIN([Vin]) --> RIN[Rin] --> M((− / virtual gnd))
    M --> OP[op-amp] --> VOUT([Vout])
    M -. Rf .-> VOUT
    M -. Cf .-> VOUT
    P((+)) --> GND([ground])
    P --> OP
```

Still only $-20\,$dB/decade — but buffered, with gain, and ready to cascade. For
a steeper edge we need second-order stages.

**Next:** the Sallen-Key topology.
""",
        ),
        _t(
            "Sallen-Key second-order LP & HP",
            "12 min",
            r"""\
# Sallen-Key second-order LP & HP

The **Sallen-Key** stage is the workhorse second-order active filter: one op-amp
(usually as a unity-gain buffer), two resistors and two capacitors. Its low-pass
transfer function has the standard form

$$H(s) = \frac{K\,\omega_0^2}{s^2 + \dfrac{\omega_0}{Q}\,s + \omega_0^2},$$

where the RC values set $\omega_0$ and the **Q is chosen by the component
ratios** — no inductor needed. Picking $Q = 0.707$ gives the maximally flat
(Butterworth) response; higher Q sharpens the knee at the cost of a peak:

```plot
{"title": "Sallen-Key low-pass: choose Q via component ratios", "xLabel": "ω/ω₀", "yLabel": "|H|", "xRange": [0, 3], "yRange": [0, 3], "controls": [{"name": "Q", "range": [0.5, 6], "value": 0.707, "label": "design Q"}], "functions": [{"expr": "1/sqrt((1-x^2)^2 + (x/Q)^2)", "label": "|H(jω)|", "color": "#2563eb"}], "points": [{"x": 1, "y": 0, "label": "ω₀", "color": "#dc2626", "size": 6}]}
```

Swap the positions of the resistors and capacitors and the **same topology
becomes a high-pass** — a clean mirror image:

```plot
{"title": "Sallen-Key high-pass (Q = 0.707)", "xLabel": "ω/ω₀", "yLabel": "|H|", "xRange": [0, 4], "yRange": [0, 1.2], "functions": [{"expr": "x^2/sqrt((1-x^2)^2 + (x*1.414)^2)", "label": "|H(jω)| high-pass", "color": "#16a34a"}], "points": [{"x": 1, "y": 0.707, "label": "ω₀ (−3 dB)", "color": "#dc2626", "size": 6}]}
```

The Sallen-Key low-pass network:

```mermaid
flowchart LR
    VIN([Vin]) --> R1[R1] --> A((node A))
    A --> R2[R2] --> P((+ op-amp))
    P --> OP[op-amp buffer] --> VOUT([Vout])
    P -. C2 .-> GND([ground])
    A -. C1 .-> VOUT
    OP --> M((−))
    M --> VOUT
```

Sallen-Key is popular because it is simple and low-Q-friendly; at very high Q it
becomes sensitive, which the multiple-feedback topology handles better.

**Next:** an active band-pass.
""",
        ),
        _t(
            "Multiple-feedback band-pass",
            "11 min",
            r"""\
# Multiple-feedback band-pass

For a band-pass you want gain over a band centred on $\omega_0$ and attenuation
on both sides. The **multiple-feedback (MFB)** topology uses one inverting op-amp
with two feedback paths to realise

$$H(s) = \frac{-K\,(\omega_0/Q)\,s}{s^2 + \dfrac{\omega_0}{Q}\,s + \omega_0^2}.$$

The **bandwidth** is $\mathrm{BW} = \omega_0/Q$, so a high $Q$ means a narrow,
selective band. Slide $Q$ to trade selectivity against bandwidth:

```plot
{"title": "Band-pass: Q sets selectivity (BW = ω₀/Q)", "xLabel": "ω/ω₀", "yLabel": "|H| (normalised)", "xRange": [0, 3], "yRange": [0, 1.1], "controls": [{"name": "Q", "range": [1, 12], "value": 4, "label": "quality factor Q"}], "functions": [{"expr": "(x/Q)/sqrt((1-x^2)^2 + (x/Q)^2)", "label": "|H(jω)| band-pass", "color": "#2563eb"}], "points": [{"x": 1, "y": 1, "label": "centre ω₀", "color": "#dc2626", "size": 6}]}
```

The MFB band-pass stage — note the two feedback elements returning to the
virtual-ground node:

```mermaid
flowchart LR
    VIN([Vin]) --> R1[R1] --> N((node))
    N -. C1 .-> M((− / virtual gnd))
    N -. R2 .-> GND([ground])
    M --> OP[op-amp] --> VOUT([Vout])
    M -. C2 .-> VOUT
    M -. R3 .-> VOUT
    P((+)) --> GND
    P --> OP
```

MFB holds its Q better than Sallen-Key and inverts the signal; it is the default
choice for moderate-Q active band-pass filters.

**Next:** getting steeper by cascading.
""",
        ),
        _t(
            "Filter order & cascading stages",
            "11 min",
            r"""\
# Filter order & cascading stages

One second-order stage rolls off at $-40\,$dB/decade. Need steeper? **Cascade**
stages: because each op-amp stage is buffered, the overall response is just the
**product** of the individual transfer functions, so

$$H_{\text{total}}(s) = H_1(s)\,H_2(s)\cdots H_k(s),$$

and the orders simply add. An $n$-th-order filter is built from
$\lfloor n/2\rfloor$ second-order sections plus one first-order section if $n$ is
odd. Higher order = sharper transition: compare orders 1, 2 and 6 of a low-pass:

```plot
{"title": "Roll-off sharpens with order (1, 2, 6)", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 4], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+x^2)", "label": "order 1", "color": "#94a3b8"}, {"expr": "1/sqrt(1+x^4)", "label": "order 2", "color": "#16a34a"}, {"expr": "1/sqrt(1+x^12)", "label": "order 6", "color": "#2563eb"}]}
```

Crucially, each stage is **not** designed to be Butterworth on its own — instead
the stages are assigned specific $\omega_0$ and $Q$ values from a design table so
their *product* gives the target response. The cascade as a signal chain:

```mermaid
flowchart LR
    IN([Vin]) --> S1[2nd-order section: ω₀₁, Q₁]
    S1 --> S2[2nd-order section: ω₀₂, Q₂]
    S2 --> S3[1st-order section if n odd]
    S3 --> OUT([Vout])
```

Order is the main knob for steepness — but more stages mean more components,
more noise and tighter tolerances.

**Next:** how sensitive the result is to those components.
""",
        ),
        _t(
            "Sensitivity & component selection",
            "10 min",
            r"""\
# Sensitivity & component selection

A design on paper assumes exact components; real resistors and capacitors carry
**tolerances** (±1%, ±5%, ±20%). **Sensitivity** measures how much a filter
parameter moves when a component does:

$$S_x^{y} = \frac{\partial y / y}{\partial x / x}
= \frac{x}{y}\,\frac{\partial y}{\partial x}.$$

A sensitivity of $1$ means a 1% part error gives a 1% shift in $\omega_0$ or $Q$.
High-Q stages are the troublemakers: **Q sensitivity grows roughly with Q**, so a
sharp filter built from loose parts drifts badly. The rough trend of Q error
against the design Q for a fixed component tolerance:

```plot
{"title": "Q error grows with the design Q (fixed part tolerance)", "xLabel": "design Q", "yLabel": "relative Q spread (a.u.)", "xRange": [0, 10], "yRange": [0, 3], "functions": [{"expr": "0.05*x + 0.03*x^2/10", "label": "≈ tolerance × sensitivity", "color": "#dc2626"}]}
```

Practical rules:

- Use **tighter-tolerance, low-temperature-coefficient** parts (C0G/NP0 caps,
  metal-film resistors) on the frequency-setting elements.
- Prefer topologies with **low sensitivity** (Sallen-Key at low Q; split a high-Q
  spec across more stages rather than one extreme stage).
- Pick **standard E-series** values and recompute the actual $\omega_0$, $Q$.

Good component selection is what separates a circuit that works on the bench from
one that works across temperature and across a production run.

**Next:** test what you have learned.
""",
        ),
        _quiz(),
    ),
)

# ── Filter Design — Advanced ─────────────────────────────────────────────────

_FD_ADVANCED = SeedCourse(
    slug="filter-design-advanced",
    title="Filter Design — Advanced",
    description=(
        "The professional toolkit: the classical approximations (Butterworth, "
        "Chebyshev I/II, elliptic, Bessel) and their trade-offs, pole-zero "
        "placement on the s-plane, switched-capacitor filters, the analog-to-digital "
        "bridge via the bilinear transform and IIR filters, a complete worked design "
        "example, and practical issues (noise, tolerance, GBW). With interactive "
        "magnitude families and a full design walk-through."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Approximation theory: Butterworth, Chebyshev, elliptic, Bessel",
            "12 min",
            r"""\
# Approximation theory: Butterworth, Chebyshev, elliptic, Bessel

An ideal "brick-wall" filter is unrealisable, so we **approximate** it. Each
classical family optimises something different:

- **Butterworth** — maximally **flat** passband, monotonic, gentle knee.
  $|H|^2 = 1/(1+(\omega/\omega_c)^{2n})$.
- **Chebyshev I** — allows equal **ripple in the passband** to buy a much steeper
  transition for the same order.
- **Chebyshev II (inverse)** — flat passband, equal ripple in the **stopband**.
- **Elliptic (Cauer)** — ripple in **both** bands; the **steepest** transition for
  a given order, at the cost of worse phase.
- **Bessel** — sacrifices steepness for **maximally flat group delay** (linear
  phase), so pulse shapes pass through undistorted.

Butterworth magnitude sharpens as the order $n$ rises but stays flat in the
passband:

```plot
{"title": "Butterworth magnitude: flatter & steeper as order n grows", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 3], "yRange": [0, 1.1], "controls": [{"name": "n", "range": [1, 8], "value": 4, "step": 1, "label": "order n"}], "functions": [{"expr": "1/sqrt(1+x^(2*n))", "label": "1/√(1+(ω/ωc)^2n)", "color": "#2563eb"}], "points": [{"x": 1, "y": 0.707, "label": "−3 dB", "color": "#dc2626", "size": 6}]}
```

Butterworth vs a 4th-order Chebyshev with passband ripple — the rippled curve
falls faster past the edge:

```plot
{"title": "Butterworth vs Chebyshev I (same order): ripple buys steepness", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 3], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+x^8)", "label": "Butterworth n=4", "color": "#2563eb"}, {"expr": "1/sqrt(1+0.5*(8*x^4-8*x^2+1)^2)", "label": "Chebyshev I n=4 (ripple)", "color": "#dc2626"}]}
```

The choice is a **trade-off triangle**: flatness, steepness and phase/transient
behaviour — you cannot have all three.

**Next:** where these come from — the pole-zero pattern.
""",
        ),
        _t(
            "Pole-zero placement & the s-plane",
            "12 min",
            r"""\
# Pole-zero placement & the s-plane

Every approximation is really a **pattern of poles and zeros** in the complex
$s$-plane.

- **Poles** must lie in the **left half-plane** ($\sigma < 0$) for stability; their
  distance from the $j\omega$ axis sets damping (and Q), their height sets the
  resonant frequency.
- **Butterworth poles** sit on a **circle** of radius $\omega_c$, equally spaced —
  that even spacing is exactly what makes the passband maximally flat.
- **Chebyshev poles** lie on an **ellipse** (closer to the axis → higher Q →
  steeper but peakier).
- **Zeros** on the $j\omega$ axis create transmission **nulls** (notches);
  elliptic filters place finite zeros just past the band edge to crush the
  stopband.

The pole angles for an order-4 Butterworth, distributed around the unit circle:

```plot
{"title": "Butterworth poles lie on a circle (order 4 shown by angle)", "xLabel": "σ (real)", "yLabel": "jω (imag)", "xRange": [-1.3, 1.3], "yRange": [-1.3, 1.3], "functions": [{"expr": "sqrt(1-x^2)", "label": "unit circle (upper)", "color": "#cbd5e1"}], "points": [{"x": -0.383, "y": 0.924, "label": "pole", "color": "#dc2626", "size": 6}, {"x": -0.924, "y": 0.383, "label": "pole", "color": "#dc2626", "size": 6}, {"x": -0.383, "y": -0.924, "color": "#dc2626", "size": 6}, {"x": -0.924, "y": -0.383, "color": "#dc2626", "size": 6}]}
```

Mapping each conjugate pole pair to a second-order section is exactly how the
cascade of the Intermediate course is designed: read $\omega_0$ and $Q$ off the
pole location, build a stage. **Design flows from geometry to circuit.**

**Next:** realising filters with switches and capacitors.
""",
        ),
        _t(
            "Switched-capacitor filters",
            "11 min",
            r"""\
# Switched-capacitor filters

On an integrated circuit, accurate resistors are large and inaccurate, but
**capacitor ratios** are precise. The trick: **simulate a resistor with a
switched capacitor**. Toggling a small capacitor $C$ between two nodes at clock
frequency $f_{clk}$ moves charge at an average rate equivalent to

$$R_{eq} = \frac{1}{f_{clk}\,C}.$$

Substitute that into an RC filter and the cutoff becomes

$$\omega_c = \frac{1}{R_{eq}C_2} = f_{clk}\,\frac{C_1}{C_2}.$$

The corner frequency now depends only on a **capacitor ratio and the clock** —
both excellent on silicon — so the filter is **digitally tunable**: change the
clock, move the cutoff. Cutoff scales linearly with clock frequency:

```plot
{"title": "Switched-capacitor cutoff tracks the clock", "xLabel": "clock frequency (norm.)", "yLabel": "cutoff ωc (norm.)", "xRange": [0, 5], "yRange": [0, 5], "controls": [{"name": "ratio", "range": [0.2, 2], "value": 1, "label": "C1/C2 ratio"}], "functions": [{"expr": "ratio*x", "label": "ωc = fclk·(C1/C2)", "color": "#2563eb"}]}
```

The charge-transfer idea, one clock phase to the next:

```mermaid
flowchart LR
    V1([node 1]) --> SW1{phase φ1} --> CAP[C] --> SW2{phase φ2} --> V2([node 2])
    CLK([clock fclk]) -.drives.-> SW1
    CLK -.drives.-> SW2
```

Caveats: the signal is **sampled**, so you need anti-alias and reconstruction
filtering, and clock feedthrough adds noise. But for tunable, IC-friendly filters
they are everywhere (codecs, sensor front-ends).

**Next:** crossing fully into the digital domain.
""",
        ),
        _t(
            "From analog prototype to digital: the bilinear transform & IIR",
            "12 min",
            r"""\
# From analog prototype to digital: the bilinear transform & IIR

To build a filter in software, take a known analog prototype $H(s)$ and map it to
a digital $H(z)$. The **bilinear transform** substitutes

$$s \;\leftarrow\; \frac{2}{T}\,\frac{1 - z^{-1}}{1 + z^{-1}},$$

which maps the entire left-half $s$-plane into the unit circle of the $z$-plane —
so a **stable analog filter becomes a stable digital one**. The result is an
**IIR** (infinite impulse response) filter: a recursive difference equation

$$y[n] = \sum b_k x[n-k] - \sum a_k y[n-k].$$

The mapping warps frequencies nonlinearly: $\omega_{analog} = \frac{2}{T}\tan(\omega_d/2)$,
so you **pre-warp** the critical frequency before transforming. The frequency
warping between digital and analog axes:

```plot
{"title": "Bilinear frequency warping ω_a = tan(ω_d/2)", "xLabel": "digital frequency ω_d (rad)", "yLabel": "analog frequency (norm.)", "xRange": [0, 3], "yRange": [0, 6], "functions": [{"expr": "x/2", "label": "linear (ideal)", "color": "#cbd5e1"}, {"expr": "sin(x/2)/cos(x/2)", "label": "tan(ω_d/2) (actual)", "color": "#2563eb"}]}
```

The analog-to-digital design pipeline:

```mermaid
flowchart LR
    SPEC([digital spec]) --> PW[pre-warp critical freqs]
    PW --> PROTO[analog prototype H of s]
    PROTO --> BLT[bilinear transform s to z]
    BLT --> HZ[H of z: IIR coefficients]
    HZ --> IMPL([difference equation in code])
```

IIR filters are efficient (few coefficients) but, unlike FIR, can be unstable if
mis-implemented and lack exactly linear phase — the same trade-offs that drive
the analog families reappear in digital form.

**Next:** put it all together in one design.
""",
        ),
        _t(
            "A complete design example: spec to components",
            "12 min",
            r"""\
# A complete design example: spec to components

Let us walk a full low-pass design end to end.

**1. Spec.** Passband to $1\,$kHz with $\le 0.5\,$dB ripple is fine; by $4\,$kHz we
need $\ge 40\,$dB attenuation. Phase is not critical.

**2. Choose a family.** Phase doesn't matter and we want a clean passband but a
fairly steep edge → **Butterworth** (or Chebyshev if order must be lower).

**3. Find the order.** For Butterworth, $n \ge \dfrac{\log_{10}\!\big((10^{A_s/10}-1)/(10^{A_p/10}-1)\big)}{2\log_{10}(\omega_s/\omega_p)}$.
With $A_s = 40$, a transition ratio of $4$, this gives $n \approx 4$. A 4th-order
Butterworth meets the spec with margin:

```plot
{"title": "Order-4 Butterworth meets the 40 dB-at-4×ωc spec", "xLabel": "ω/ωc", "yLabel": "|H|", "xRange": [0, 5], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+x^8)", "label": "Butterworth n=4", "color": "#2563eb"}], "points": [{"x": 1, "y": 0.707, "label": "1 kHz (−3 dB)", "color": "#16a34a", "size": 6}, {"x": 4, "y": 0.0156, "label": "4 kHz (≈ −36 dB)", "color": "#dc2626", "size": 6}]}
```

**4. Pick the topology.** Two **Sallen-Key** second-order sections in cascade,
with the table Q values $Q_1 = 0.541$ and $Q_2 = 1.307$ (the two Butterworth pole
pairs).

**5. Compute components.** Fix the caps, solve $\omega_0 = 1/\sqrt{R_aR_bC_aC_b}$
and the Q expression for the resistors, then round to E-96 values and recheck.

The realised filter:

```mermaid
flowchart LR
    IN([Vin]) --> S1[Sallen-Key LP: 1 kHz, Q=0.541]
    S1 --> S2[Sallen-Key LP: 1 kHz, Q=1.307]
    S2 --> OUT([Vout, 4th-order Butterworth])
```

**6. Verify** with simulation and on the bench over tolerance and temperature.
That sequence — *spec → family → order → topology → components → verify* — is the
universal filter-design recipe.

**Next:** the non-ideal effects that bite in practice.
""",
        ),
        _t(
            "Practical issues: noise, tolerance & GBW limits",
            "11 min",
            r"""\
# Practical issues: noise, tolerance & GBW limits

The textbook filter is ideal; the bench one is not. Three effects dominate.

**Noise.** Every resistor adds thermal (Johnson) noise $\overline{v_n^2}=4kTR\,\Delta f$
and the op-amp adds its own; high-Q stages **amplify noise near $\omega_0$**.
Keep resistor values moderate and avoid stacking gain in early stages.

**Tolerance.** As in the Intermediate course, part spread shifts $\omega_0$ and
$Q$; **Monte-Carlo** the design and budget margin into the spec.

**Gain-bandwidth (GBW).** A real op-amp's open-loop gain falls with frequency.
Once the required closed-loop gain approaches the op-amp's available gain, the
stage's actual $Q$ and $\omega_0$ drift — a stage designed for $f_0$ misbehaves
when $f_0$ is a non-negligible fraction of **GBW**. A useful rule of thumb is to
keep GBW well above $Q^2 \times f_0$. The realised $\omega_0$ sagging as the
design frequency approaches the op-amp's GBW:

```plot
{"title": "Realised ω₀ sags as f₀ approaches the op-amp GBW", "xLabel": "f₀ / GBW", "yLabel": "realised ω₀ / ideal", "xRange": [0, 0.5], "yRange": [0, 1.1], "functions": [{"expr": "1/(1+2*x)", "label": "ω₀ degradation", "color": "#dc2626"}], "points": [{"x": 0, "y": 1, "label": "ideal", "color": "#16a34a", "size": 6}]}
```

The practical design loop that wraps the ideal recipe:

```mermaid
flowchart LR
    DES([ideal design]) --> CHK{noise, tolerance, GBW OK?}
    CHK -- no --> ADJ[raise GBW / tighten parts / rescale impedances]
    ADJ --> DES
    CHK -- yes --> BUILD([build & verify])
```

Mastering filters means respecting these limits as much as the math: choose the
right op-amp, the right impedance level and the right part grade, and the elegant
$H(s)$ on paper survives contact with the real world.

**Next:** test what you have learned.
""",
        ),
        _quiz(),
    ),
)


FILTER_DESIGN_COURSES: tuple[SeedCourse, ...] = (_FD_BASICS, _FD_INTERMEDIATE, _FD_ADVANCED)

__all__ = ["FILTER_DESIGN_COURSES"]
