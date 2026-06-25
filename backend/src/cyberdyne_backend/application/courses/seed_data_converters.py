"""Data Converters & PLLs track: Basics -> Intermediate -> Advanced.

A mixed-signal journey from the Nyquist sampling theorem and quantization noise,
through DAC/ADC architectures (binary-weighted, R-2R, flash, SAR, pipelined,
sigma-delta) and converter testing, to phase-locked loops, jitter & phase noise,
frequency synthesis, clock & data recovery and mixed-signal layout. Lessons are
`text` with LaTeX, interactive ```plot blocks (sampling/quantization staircases,
sinc, noise shaping, PLL transients) and ```mermaid block diagrams.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Data Converters & PLLs — Basics ──────────────────────────────────────────

_DC_BASICS = SeedCourse(
    slug="data-converters-basics",
    title="Data Converters & PLLs — Basics",
    description=(
        "The mixed-signal bridge between the analog and digital worlds: sampling "
        "and the Nyquist theorem, quantization and resolution, DAC and ADC "
        "fundamentals and key specs, the sample-and-hold, and anti-alias "
        "filtering. The groundwork for every audio codec, sensor front-end and "
        "software-defined radio, with interactive plots."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Sampling & the Nyquist theorem",
            "11 min",
            """\
# Sampling & the Nyquist theorem

A data converter starts by **sampling**: reading a continuous signal $x(t)$ at
regular instants spaced by the **sample period** $T_s$, giving the sequence
$x[n] = x(nT_s)$. The rate is $f_s = 1/T_s$.

The **Nyquist-Shannon sampling theorem** says you can perfectly reconstruct a
signal **only if** you sample faster than twice its highest frequency:

$$f_s > 2 f_{\\max}.$$

The threshold $f_s/2$ is the **Nyquist frequency**. Sample too slowly and
energy above $f_s/2$ folds back to a lower frequency you can no longer tell from
a real low-frequency tone — this is **aliasing**. The classic picture: a
high-frequency sine, sampled too sparsely, masquerades as a slow one.

```plot
{"title": "Aliasing: a fast tone read as a slow one", "xLabel": "time t", "yLabel": "amplitude", "xRange": [0, 6.283], "yRange": [-1.4, 1.4], "functions": [{"expr": "sin(7*x)", "label": "true 7 Hz signal", "color": "#2563eb"}, {"expr": "sin(x)", "label": "aliased 1 Hz (looks identical at the dots)", "color": "#dc2626"}], "points": [{"x": 0, "y": 0, "color": "#16a34a", "size": 5}, {"x": 1.047, "y": 0.866, "color": "#16a34a", "size": 5}, {"x": 2.094, "y": -0.866, "color": "#16a34a", "size": 5}, {"x": 3.142, "y": 0, "color": "#16a34a", "size": 5}, {"x": 4.189, "y": 0.866, "color": "#16a34a", "size": 5}, {"x": 5.236, "y": -0.866, "color": "#16a34a", "size": 5}]}
```

Both curves pass through every green sample, so once sampled they are
indistinguishable. The cure is an **anti-alias filter** before the sampler —
covered later in this course.

**Next:** turning samples into numbers — quantization.
""",
        ),
        _t(
            "Quantization, resolution & quantization noise",
            "12 min",
            """\
# Quantization, resolution & quantization noise

Sampling discretises *time*; **quantization** discretises *amplitude*. An
$N$-bit converter maps the input onto $2^N$ levels. Over a full-scale range
$V_{FS}$ the step between levels — one **LSB** (least-significant bit) — is

$$\\Delta = \\frac{V_{FS}}{2^N}.$$

Each sample is rounded to the nearest level, so the digital output is a
**staircase** approximation of the smooth input:

```plot
{"title": "Quantization staircase: a ramp rounded to discrete levels", "xLabel": "input (volts)", "yLabel": "output code (volts)", "xRange": [0, 8], "yRange": [0, 8], "functions": [{"expr": "x", "label": "ideal (continuous)", "color": "#94a3b8"}, {"expr": "floor(x)+0.5", "label": "quantized output", "color": "#2563eb"}]}
```

The rounding error $e = x - x_q$ lives in $[-\\Delta/2, +\\Delta/2]$. Treated as
uniform noise, it has power $\\sigma_e^2 = \\Delta^2/12$. For a full-scale sine the
best-case **signal-to-quantization-noise ratio** is

$$\\mathrm{SQNR} \\approx 6.02\\,N + 1.76 \\ \\text{dB}.$$

The headline rule: **each extra bit buys about 6 dB** of dynamic range. A 16-bit
audio converter therefore reaches roughly 98 dB.

**Next:** building the converter that turns codes back into voltages — the DAC.
""",
        ),
        _t(
            "DAC fundamentals & architectures",
            "11 min",
            """\
# DAC fundamentals & architectures

A **digital-to-analog converter (DAC)** turns an $N$-bit code into an analog
voltage or current. The ideal transfer is

$$V_{out} = V_{FS}\\,\\frac{D}{2^N}, \\qquad D = \\sum_{k=0}^{N-1} b_k 2^{k}.$$

Two classic resistor architectures:

- **Binary-weighted** — one resistor per bit, scaled $R, 2R, 4R, \\dots$ (each
  ×2). Simple
  in concept, but the spread of resistor values for many bits is impractical and
  hard to match.
- **R-2R ladder** — uses only **two** resistor values ($R$ and $2R$) repeated in
  a ladder. Each rung halves the current, so matching and scalability are far
  better. It dominates real designs.

```mermaid
flowchart LR
  D["N-bit code"] --> SW["bit switches b0..bN-1"]
  SW --> LAD["R-2R ladder (two resistor values)"]
  LAD --> SUM["current summing node"]
  SUM --> BUF["output buffer / I-to-V"]
  BUF --> VO["Vout"]
```

Other families: **string DACs** (a resistor divider tapped by a switch tree —
inherently monotonic), **current-steering** DACs (fast, used in RF/video) and
**capacitive** (charge-redistribution) DACs that pair naturally with SAR ADCs.
Key trade-offs are speed, glitch energy, monotonicity and area.

**Next:** the converter going the other way — the ADC.
""",
        ),
        _t(
            "ADC fundamentals & key specs",
            "12 min",
            """\
# ADC fundamentals & key specs

An **analog-to-digital converter (ADC)** maps an input voltage to the nearest
$N$-bit code. Beyond resolution, real parts are judged by **static** and
**dynamic** specs.

**Static (linearity)**
- **DNL** (differential non-linearity): how much each code's width deviates from
  one ideal LSB. $\\mathrm{DNL} < -1\\,\\mathrm{LSB}$ means a **missing code**.
- **INL** (integral non-linearity): the running sum of DNL — how far the
  transfer curve bends away from the ideal straight line.

**Dynamic (from an FFT of the output)**
- **SNR** — signal power over noise power.
- **SFDR** (spurious-free dynamic range) — distance from the signal to the
  largest spur (often a harmonic).
- **ENOB** (effective number of bits): the *real* resolution after all noise and
  distortion,

$$\\mathrm{ENOB} = \\frac{\\mathrm{SINAD} - 1.76}{6.02}.$$

So a "12-bit" ADC measuring an ENOB of 10.5 is honestly a 10.5-bit part. The
INL/DNL curve below shows a transfer that bends and has one wide code:

```plot
{"title": "INL: real transfer bending away from the ideal line", "xLabel": "input code", "yLabel": "output (LSB)", "xRange": [0, 8], "yRange": [0, 9], "functions": [{"expr": "x", "label": "ideal", "color": "#94a3b8"}, {"expr": "x + 0.5*sin(x)", "label": "real (INL error)", "color": "#dc2626"}]}
```

**Next:** the circuit that freezes the input while the ADC decides.
""",
        ),
        _t(
            "The sample-and-hold",
            "10 min",
            """\
# The sample-and-hold

An ADC needs the input to stand **still** while it resolves the code — otherwise
the value is moving as the bits are decided. The **sample-and-hold (S/H)** (or
track-and-hold) does exactly that: a switch and a capacitor.

- **Track / sample phase** — the switch closes; the cap follows the input.
- **Hold phase** — the switch opens; the cap holds the last value steady for the
  ADC to digitise.

```mermaid
flowchart LR
  IN["analog input"] --> SW["sampling switch (clock)"]
  SW --> CAP["hold capacitor"]
  CAP --> BUF["high-Z buffer"]
  BUF --> ADC["to ADC core"]
```

The held voltage settles toward the input with an $RC$ time constant set by the
switch resistance and the hold cap — it must settle to within ½ LSB inside the
sampling window:

```plot
{"title": "S/H acquisition: settling to within 1/2 LSB", "xLabel": "time (RC constants)", "yLabel": "held voltage (fraction of step)", "xRange": [0, 8], "yRange": [0, 1.1], "functions": [{"expr": "1 - exp(-x)", "label": "capacitor voltage", "color": "#2563eb"}], "points": [{"x": 0, "y": 1, "label": "target input", "color": "#16a34a", "size": 0}]}
```

Real S/H errors include **aperture jitter** (clock-edge uncertainty), **droop**
(leakage during hold) and **charge injection** from the switch. The S/H is often
the true bandwidth limit of the whole converter.

**Next:** where it all fits — the analog and digital domains.
""",
        ),
        _t(
            "Analog vs digital domains & anti-alias filtering",
            "11 min",
            """\
# Analog vs digital domains & anti-alias filtering

A mixed-signal system lives in two worlds. The **analog domain** is continuous
in time and amplitude — sensors, amplifiers, real voltages. The **digital
domain** is discrete in both — numbers a processor can store and compute on.
Converters are the gateways: the ADC goes analog → digital, the DAC digital →
analog.

```mermaid
flowchart LR
  SENS["sensor (analog)"] --> AAF["anti-alias filter"]
  AAF --> SH["sample & hold"]
  SH --> ADC["ADC"]
  ADC --> DSP["DSP / CPU (digital)"]
  DSP --> DAC["DAC"]
  DAC --> RCF["reconstruction filter"]
  RCF --> OUT["analog output"]
```

The **anti-alias filter (AAF)** is non-negotiable. From the sampling lesson, any
energy above $f_s/2$ folds back as an alias you can never remove later. So a
low-pass filter must attenuate everything above the Nyquist frequency **before**
the sampler:

```plot
{"title": "Anti-alias filter: reject everything above f_s/2", "xLabel": "frequency / (f_s/2)", "yLabel": "gain", "xRange": [0, 4], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+(x)^8)", "label": "low-pass AAF response", "color": "#2563eb"}], "points": [{"x": 1, "y": 0, "label": "Nyquist f_s/2", "color": "#dc2626", "size": 6}]}
```

A sharp brick-wall filter is hard, so designers often **oversample** to push the
Nyquist edge well above the band of interest, relaxing the filter — the idea the
Intermediate course builds on with sigma-delta converters.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Data Converters & PLLs — Intermediate ────────────────────────────────────

_DC_INTERMEDIATE = SeedCourse(
    slug="data-converters-intermediate",
    title="Data Converters & PLLs — Intermediate",
    description=(
        "The converter architectures that actually ship: flash, successive-"
        "approximation (SAR) and pipelined ADCs, the oversampling and "
        "noise-shaping magic of sigma-delta, DAC reconstruction and the "
        "zero-order-hold sinc droop, and FFT-based converter testing. The "
        "working knowledge behind every modern data-acquisition chain, with "
        "interactive plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Flash ADC",
            "11 min",
            """\
# Flash ADC

The **flash** (or parallel) ADC is the fastest architecture: it compares the
input against **all** thresholds at once. An $N$-bit flash uses a resistor string
of $2^N - 1$ taps, each feeding a comparator, and a **thermometer-to-binary**
encoder collapses the comparator outputs into a code — in a single clock cycle.

```mermaid
flowchart LR
  VIN["analog input"] --> CMP["2^N - 1 comparators vs resistor-string taps"]
  CMP --> TH["thermometer code"]
  TH --> ENC["priority / thermometer-to-binary encoder"]
  ENC --> OUT["N-bit code"]
```

The price is **exponential**: the comparator and resistor count doubles with
every bit. An 8-bit flash needs 255 comparators; 10 bits is already 1023. That
makes flash hot, power-hungry and area-expensive, so it tops out around 6-8 bits.

Where it wins: **speed**. GHz-class oscilloscopes and the back-end stages of
pipelined ADCs use small flash sub-converters because nothing resolves a few
bits faster. The classic engineering trade — latency vs hardware — is at its
extreme here.

**Next:** the opposite trade — one comparator, many cycles: the SAR ADC.
""",
        ),
        _t(
            "Successive-approximation (SAR) ADC",
            "12 min",
            """\
# Successive-approximation (SAR) ADC

The **successive-approximation register (SAR)** ADC plays a binary-search game.
With a single comparator and an internal DAC it resolves one bit per cycle, from
the **MSB down**:

1. Guess the MSB is 1; the DAC outputs $V_{FS}/2$.
2. Compare to the input. If the input is larger, **keep** the bit; else clear it.
3. Move to the next bit (next DAC level) and repeat.

```mermaid
flowchart LR
  SH["sample & hold"] --> CMP["comparator"]
  DAC["internal DAC"] --> CMP
  CMP --> LOGIC["SAR logic"]
  LOGIC --> DAC
  LOGIC --> OUT["N-bit result after N cycles"]
```

After $N$ comparisons the code converges, like weighing on a balance with halving
weights. The internal DAC is usually a **charge-redistribution capacitor array**,
which also performs the sample-and-hold — elegant and low-power.

SAR ADCs hit the sweet spot for **medium speed, medium resolution** (8-18 bits,
up to tens of MS/s) at very low power, which is why nearly every microcontroller
and sensor front-end embeds one. The cost is $N$ cycles of latency per sample —
the mirror image of flash.

**Next:** combining flash speed with SAR-like efficiency — the pipeline.
""",
        ),
        _t(
            "Pipelined ADC",
            "11 min",
            """\
# Pipelined ADC

A **pipelined** ADC chains several low-resolution stages so they work in
parallel, like an assembly line. Each stage resolves a few bits, then passes the
**residue** (what it could not yet resolve, amplified) to the next stage:

1. A small (e.g. flash) sub-ADC resolves $k$ bits.
2. A DAC reconstructs that estimate and subtracts it from the held input.
3. The remainder is amplified by $2^k$ — the **residue** — and handed downstream.

```mermaid
flowchart LR
  IN["S/H"] --> S1["Stage 1: k-bit ADC + DAC + xGain"]
  S1 --> S2["Stage 2: residue amplified"]
  S2 --> S3["Stage 3 ... Stage M"]
  S1 --> AL["digital align + error-correction"]
  S2 --> AL
  S3 --> AL
  AL --> OUT["N-bit output"]
```

Because stages run **concurrently** on different samples (deep but pipelined),
throughput is one sample per clock — fast — while each stage stays simple. The
penalty is **latency** (a sample exits several clocks after it entered) and a need
for precise inter-stage gain. **Digital error correction** (overlapping stage
ranges, often 1.5 bits/stage) relaxes the comparator accuracy.

Pipelined ADCs own the **high-speed, medium-to-high resolution** corner: 10-16
bits at tens to hundreds of MS/s — the heart of communications and imaging.

**Next:** trading speed for resolution with oversampling — sigma-delta.
""",
        ),
        _t(
            "Sigma-delta: oversampling & noise shaping",
            "13 min",
            """\
# Sigma-delta: oversampling & noise shaping

A **sigma-delta ($\\Sigma\\Delta$)** converter wins resolution with two tricks
instead of precise analog parts.

**1. Oversampling.** Sample far above Nyquist by the **oversampling ratio**
$\\mathrm{OSR} = f_s / (2 f_B)$. Quantization noise power is unchanged but now
spread over a much wider band, so only a small slice lands in the signal band —
worth about $\\tfrac12\\log_2(\\mathrm{OSR})$ extra bits on its own.

**2. Noise shaping.** A loop with an integrator and 1-bit quantizer feeds the
error back so it is **high-pass shaped** — pushed up out of the band of interest,
where a digital filter removes it.

```mermaid
flowchart LR
  IN["analog input"] --> SUM["+/- summer"]
  SUM --> INT["integrator (loop filter)"]
  INT --> QNT["1-bit quantizer (comparator)"]
  QNT --> BIT["bitstream out"]
  QNT --> DACFB["1-bit DAC feedback"]
  DACFB --> SUM
  BIT --> DEC["digital decimation filter"]
  DEC --> OUT["high-resolution code"]
```

A first-order loop shapes the noise as $|N(f)| \\propto |\\sin(\\pi f/f_s)|$ — tiny
in-band, large out-of-band where it is harmless:

```plot
{"title": "Noise shaping: quantization noise pushed out of the band", "xLabel": "frequency / (f_s/2)", "yLabel": "noise gain", "xRange": [0, 1], "yRange": [0, 2.2], "functions": [{"expr": "2*sin(1.5708*x)", "label": "shaped noise |2 sin(pi f / fs)|", "color": "#dc2626"}, {"expr": "1+0*x", "label": "flat (un-shaped) noise", "color": "#94a3b8"}], "points": [{"x": 0.1, "y": 0, "label": "signal band (low f)", "color": "#16a34a", "size": 6}]}
```

Higher-order loops shape harder. The result: 16-24 effective bits with a crude
1-bit modulator and a digital **decimation filter** — which is why $\\Sigma\\Delta$
dominates audio and precision instrumentation. The trade is **speed**: high OSR
means it suits lower-bandwidth signals.

**Next:** the DAC side of the chain — reconstruction and the sinc droop.
""",
        ),
        _t(
            "DAC reconstruction & the zero-order hold",
            "12 min",
            """\
# DAC reconstruction & the zero-order hold

A DAC does not emit ideal impulses; it **holds** each sample value constant until
the next one — a **zero-order hold (ZOH)**. The output is a staircase, not a
smooth wave.

```plot
{"title": "Zero-order hold: a sine reconstructed as a staircase", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 6.283], "yRange": [-1.3, 1.3], "functions": [{"expr": "sin(x)", "label": "ideal signal", "color": "#94a3b8"}, {"expr": "sin(0.7854*floor(x/0.7854)+0.3927)", "label": "ZOH staircase output", "color": "#2563eb"}]}
```

Holding has a frequency cost. The ZOH multiplies the spectrum by a **sinc**
envelope,

$$H(f) = \\operatorname{sinc}\\!\\left(\\frac{f}{f_s}\\right) = \\frac{\\sin(\\pi f/f_s)}{\\pi f/f_s},$$

which droops toward the band edge (about $-3.9$ dB at Nyquist) and creates
**images** of the signal around multiples of $f_s$:

```plot
{"title": "Sinc droop of the zero-order hold", "xLabel": "frequency / f_s", "yLabel": "gain", "xRange": [0, 3], "yRange": [-0.3, 1.1], "functions": [{"expr": "sin(3.1416*x)/(3.1416*x)", "label": "sinc(f / f_s)", "color": "#2563eb"}], "points": [{"x": 0.5, "y": 0.637, "label": "Nyquist droop", "color": "#dc2626", "size": 6}, {"x": 1, "y": 0, "label": "first image at f_s", "color": "#16a34a", "size": 6}]}
```

Two fixes: a **reconstruction (smoothing) low-pass filter** to kill the images
above $f_s/2$, and **sinc compensation** (a slight pre-emphasis, in the digital
filter or analog stage) to flatten the in-band droop. Higher sample rates push
the images out and shrink the droop.

**Next:** how we actually measure all of this — FFT testing.
""",
        ),
        _t(
            "Converter testing & FFT-based measurement",
            "11 min",
            """\
# Converter testing & FFT-based measurement

You verify a converter by driving it with a clean, full-scale **sine** and taking
an **FFT** of the captured samples. The spectrum exposes everything at once.

```mermaid
flowchart LR
  GEN["low-distortion sine source"] --> DUT["converter under test"]
  DUT --> CAP["capture N samples"]
  CAP --> WIN["window (or coherent sampling)"]
  WIN --> FFT["FFT"]
  FFT --> METR["SNR, SINAD, SFDR, THD, ENOB"]
```

From the spectrum:

- **SNR** — signal bin over the summed noise bins.
- **THD** — total power in the harmonics.
- **SINAD** — signal over (noise + distortion); feeds **ENOB**
  $= (\\mathrm{SINAD} - 1.76)/6.02$.
- **SFDR** — signal to the tallest spur.

```plot
{"title": "FFT of an ADC output: fundamental, harmonics, noise floor", "xLabel": "frequency bin", "yLabel": "level (dB)", "xRange": [0, 10], "yRange": [-110, 5], "functions": [{"expr": "-100 + 0*x", "label": "noise floor", "color": "#94a3b8"}], "points": [{"x": 1, "y": 0, "label": "fundamental", "color": "#2563eb", "size": 7}, {"x": 2, "y": -68, "label": "2nd harmonic (SFDR spur)", "color": "#dc2626", "size": 6}, {"x": 3, "y": -80, "label": "3rd harmonic", "color": "#dc2626", "size": 5}]}
```

Two practical rules: use a **coherent** number of cycles (an integer number of
input periods in the record) or a good **window** to avoid spectral leakage
smearing the bins; and pick a prime-ish ratio so harmonics do not land on the
fundamental. **Static** tests (INL/DNL) use a histogram from a slow ramp or a
busy sine instead.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Data Converters & PLLs — Advanced ────────────────────────────────────────

_DC_ADVANCED = SeedCourse(
    slug="data-converters-advanced",
    title="Data Converters & PLLs — Advanced",
    description=(
        "Clocks and timing as a discipline: the phase-locked loop and its parts "
        "(phase detector, charge pump, VCO, loop filter), PLL dynamics and lock "
        "time, jitter and phase noise, integer-N and fractional-N frequency "
        "synthesis, clock & data recovery, and the mixed-signal layout that keeps "
        "noise from wrecking it all. The timing backbone of every radio and "
        "high-speed link, with interactive plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Phase-locked loops: the building blocks",
            "12 min",
            """\
# Phase-locked loops: the building blocks

A **phase-locked loop (PLL)** is a feedback system that forces an oscillator's
phase to track a reference. In lock, the output frequency is an exact (and
optionally multiplied) copy of the input. Four blocks:

```mermaid
flowchart LR
  REF["reference clock"] --> PFD["phase/frequency detector"]
  PFD --> CP["charge pump"]
  CP --> LF["loop filter (low-pass)"]
  LF --> VCO["voltage-controlled oscillator"]
  VCO --> OUT["output clock"]
  OUT --> DIV["divide by N"]
  DIV --> PFD
```

- **Phase/frequency detector (PFD)** — outputs UP/DOWN pulses proportional to the
  phase error between the reference and the divided feedback.
- **Charge pump (CP)** — converts those pulses into a current that dumps charge
  onto the loop filter, nudging the control voltage.
- **Loop filter** — a low-pass that turns the charge into a smooth control voltage
  and sets the loop's dynamics (it is the compensator).
- **VCO** — its frequency $f_{out} = f_0 + K_{VCO}\\,V_{ctrl}$ follows the control
  voltage; gain $K_{VCO}$ in Hz/V.

With a **÷N** in the feedback, the loop drives the *divided* output to match the
reference, so $f_{out} = N f_{ref}$ — a frequency multiplier. That single idea is
the basis of frequency synthesis, covered later.

**Next:** how fast and how stably the loop locks — PLL dynamics.
""",
        ),
        _t(
            "PLL dynamics: bandwidth, stability & lock time",
            "13 min",
            """\
# PLL dynamics: bandwidth, stability & lock time

A PLL is a control loop, so it has a **loop bandwidth** and a **damping factor**.
A second-order loop behaves like the canonical system

$$H(s) = \\frac{2\\zeta\\omega_n s + \\omega_n^2}{s^2 + 2\\zeta\\omega_n s + \\omega_n^2},$$

with natural frequency $\\omega_n$ and damping $\\zeta$. The loop's step response to
a phase/frequency disturbance shows the trade directly — too little damping rings
and overshoots, too much is sluggish:

```plot
{"title": "PLL lock transient: damping shapes the settling", "xLabel": "time (1/wn)", "yLabel": "phase error -> 0", "xRange": [0, 12], "yRange": [-0.5, 1.4], "functions": [{"expr": "exp(-0.3*x)*cos(x)", "label": "underdamped (zeta=0.3): rings", "color": "#dc2626"}, {"expr": "exp(-0.707*x)*cos(0.707*x)", "label": "zeta=0.707: fast, minimal overshoot", "color": "#2563eb"}, {"expr": "exp(-1.5*x)", "label": "overdamped: slow", "color": "#94a3b8"}]}
```

Design tensions:

- **Loop bandwidth** — wide locks fast and tracks the reference (cleaning VCO
  noise) but lets through more reference noise and spurs; narrow does the reverse.
- **Stability** — set by the loop-filter zero; $\\zeta \\approx 0.707$ is the usual
  sweet spot for fast, low-overshoot locking.
- **Lock time** — roughly several $1/\\omega_n$; tighter frequency tolerance and
  larger frequency jumps lengthen it.

A useful rule: the PLL **high-pass filters** VCO noise and **low-pass filters**
reference noise, so the loop bandwidth is chosen where those two cross to minimise
total output jitter.

**Next:** the noise that the loop is fighting — jitter & phase noise.
""",
        ),
        _t(
            "Jitter & phase noise",
            "12 min",
            """\
# Jitter & phase noise

No clock edge lands exactly on time. **Jitter** is that timing error in the *time*
domain; **phase noise** is the same thing in the *frequency* domain — they are two
views of one phenomenon.

- **Jitter** — deviation of edges from their ideal instants, measured as
  **period jitter**, **cycle-to-cycle**, or accumulated **long-term** jitter (in
  picoseconds RMS).
- **Phase noise** $\\mathcal{L}(f)$ — the power in noise sidebands a distance
  $f$ from the carrier, in **dBc/Hz**. A clean oscillator's spectrum is a sharp
  spike; a noisy one has fat skirts.

```plot
{"title": "Phase noise: skirts around the carrier (sidebands)", "xLabel": "offset from carrier (arb.)", "yLabel": "relative power", "xRange": [-4, 4], "yRange": [0, 1.1], "functions": [{"expr": "exp(-8*x^2)", "label": "clean oscillator", "color": "#2563eb"}, {"expr": "exp(-0.7*x^2)", "label": "noisy: wide skirts", "color": "#dc2626"}]}
```

Integrating the phase-noise curve over a frequency band gives the **RMS jitter**
in that band — the bridge between the two domains. Jitter sources include
**thermal/flicker** noise inside the oscillator, **supply/substrate** coupling,
and **reference** noise filtered by the PLL.

Why it matters: in a high-speed link, jitter eats into the **eye diagram** and
raises the bit-error rate; in an ADC, **aperture jitter** $\\sigma_t$ caps the SNR
of a sine at frequency $f_{in}$ to $\\mathrm{SNR} = -20\\log_{10}(2\\pi f_{in}\\sigma_t)$
— at GHz inputs even femtoseconds of jitter dominate.

**Next:** using PLLs to build any frequency you want — synthesis.
""",
        ),
        _t(
            "Frequency synthesis: integer-N & fractional-N",
            "12 min",
            """\
# Frequency synthesis: integer-N & fractional-N

A **frequency synthesizer** generates a programmable output from one fixed
reference using a PLL with a divider.

**Integer-N.** Put a ÷N in the feedback and the loop locks to

$$f_{out} = N\\,f_{ref}.$$

The output can only change in steps of $f_{ref}$ — the **channel spacing**. Fine
resolution therefore needs a **small** $f_{ref}$, which forces a narrow loop
bandwidth (slow lock) and multiplies reference noise by the large $N$. A built-in
tension.

```mermaid
flowchart LR
  REF["reference"] --> PFD["PFD + charge pump"]
  PFD --> LF["loop filter"]
  LF --> VCO["VCO"]
  VCO --> OUT["f_out = N * f_ref"]
  VCO --> DIV["divider control"]
  DIV --> MOD["integer N (or sigma-delta modulated N)"]
  MOD --> PFD
```

**Fractional-N.** Make the *average* divide ratio fractional, $N.f$, by
**dithering** the integer divider between $N$ and $N{+}1$. Now $f_{ref}$ can be
large (fast lock, low noise multiplication) while resolution is fine. The dither
pattern would create **fractional spurs**, so a **sigma-delta modulator** shapes
the divider sequence — pushing the resulting noise to high offsets where the loop
filter removes it (the same noise-shaping idea as the $\\Sigma\\Delta$ ADC).

The catch is exactly that quantization noise from the modulator; careful loop-
bandwidth and modulator-order choices keep in-band phase noise low. Fractional-N
synthesizers are the workhorse of modern radios and clock generators.

**Next:** recovering a clock that was never sent — CDR.
""",
        ),
        _t(
            "Clock & data recovery",
            "11 min",
            """\
# Clock & data recovery

A high-speed serial link (SerDes, USB, Ethernet, PCIe) sends **data with no
separate clock**. The receiver must extract timing from the data edges
themselves — **clock and data recovery (CDR)** — then sample each bit at its
centre.

A CDR is a PLL whose phase detector looks at **data transitions** instead of a
clean reference:

```mermaid
flowchart LR
  RX["incoming serial data"] --> PD["phase detector (e.g. bang-bang / Hogge)"]
  PD --> LF["loop filter"]
  LF --> VCO["VCO / phase interpolator"]
  VCO --> SMP["sampler"]
  RX --> SMP
  SMP --> DATA["recovered data"]
  VCO --> CLK["recovered clock"]
```

Key issues unique to CDR:

- **No transitions, no information** — long runs of identical bits starve the
  loop, so links use **8b/10b** or scrambling to guarantee edge density, and the
  loop filter must hold frequency through the gaps.
- **Jitter tolerance / transfer** — the CDR must track slow input jitter (wander)
  but reject fast jitter; this is exactly a PLL bandwidth choice.
- **The eye diagram** — overlaying many bit periods shows the **eye**; the CDR
  aims to sample at its widest, most open point, and jitter/ISI closing the eye
  is what limits the bit-error rate.

A **bang-bang** (Alexander) phase detector only reports *early or late* (a 1-bit
quantizer in the loop), giving a nonlinear but robust, low-power CDR that
dominates multi-Gb/s links.

**Next:** keeping all this clean on silicon — layout.
""",
        ),
        _t(
            "Mixed-signal layout & noise coupling",
            "11 min",
            """\
# Mixed-signal layout & noise coupling

A beautiful ADC or PLL schematic can be ruined by layout. Fast digital switching
injects current spikes that couple into sensitive analog nodes through shared
**supplies**, the **substrate** and **parasitic capacitance** — turning into
spurs, raised noise floors and degraded ENOB.

Defensive practice:

- **Separate analog and digital domains** — split supplies (AVDD/DVDD) and grounds
  (AGND/DGND), joining at a single star point so digital return current never flows
  under analog circuits.
- **Guard rings and substrate taps** — surround sensitive blocks with grounded
  rings to collect substrate noise; use many well/substrate ties.
- **Decoupling** — local bypass caps right at each supply pin to give switching
  current a short local loop instead of a long noisy one.
- **Differential signalling** — sensitive analog runs differentially so coupled
  noise is common-mode and rejected.
- **Floorplan and clock routing** — keep noisy clocks and digital buses away from
  the converter's reference, VCO and S/H; shield with grounded traces.

```plot
{"title": "Decoupling: supply bounce vs power-supply rejection (PSRR)", "xLabel": "frequency / corner", "yLabel": "noise coupled to analog node", "xRange": [0, 4], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1+(x)^4)", "label": "poor PSRR / weak decoupling", "color": "#dc2626"}, {"expr": "0.15/sqrt(1+(x)^4)", "label": "good decoupling + guarding", "color": "#2563eb"}]}
```

The discipline matters most where it is least visible: a converter's last bit and
a PLL's phase noise are decided as much by grounding and guarding as by the
circuit itself. **Power-supply rejection (PSRR)** and **substrate isolation** are
first-class specs, not afterthoughts.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


DATA_CONVERTERS_COURSES: tuple[SeedCourse, ...] = (_DC_BASICS, _DC_INTERMEDIATE, _DC_ADVANCED)

__all__ = ["DATA_CONVERTERS_COURSES"]
