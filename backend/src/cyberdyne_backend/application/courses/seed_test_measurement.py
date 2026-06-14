"""Academy seed content — the Test & Measurement / Instrumentation track.

* ``test-measurement-basics``        — accuracy vs precision, multimeter, oscilloscope, sources, error
* ``test-measurement-intermediate``  — uncertainty, spectrum analyzer, probing, ADC/digitizing
* ``test-measurement-advanced``      — VNA & calibration, jitter/phase noise, automated test, averaging

Runnable ``code`` lessons use numpy + builtins to compute accuracy/precision
statistics, demonstrate oscilloscope aliasing, propagate measurement uncertainty,
show FFT windowing/leakage, compute ADC ENOB/SNR, fit a sensor calibration, and
quantify noise reduction by averaging. Part of the Electronic Engineering
curriculum.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, ±, µ, Ω, ², ×, √) in diagrams.
# ruff: noqa: RUF001, RUF003

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# test-measurement-basics
# ──────────────────────────────────────────────────────────────────────

_TM_BASICS = SeedCourse(
    slug="test-measurement-basics",
    title="Test & Measurement — Basics",
    description=(
        "Measure electronics correctly: accuracy vs precision and error, the "
        "multimeter and its loading effects, the oscilloscope (bandwidth, sample "
        "rate, probes, triggering), signal sources, and the basics of measurement "
        "error. With runnable accuracy/precision and aliasing labs."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why measure? Accuracy, precision & error",
            "10 min",
            r"""# Why measure? Accuracy, precision & error

Engineering runs on measurement: you can't design, debug, or verify what you can't
measure. But **every measurement is an estimate with error** — the art of test &
measurement is knowing **how good** a measurement is, not just its number. The
foundational vocabulary, which people constantly confuse:

- **Accuracy** — how close a measurement is to the **true value** (freedom from
  **bias / systematic error**).
- **Precision** — how **repeatable** measurements are (freedom from **random
  scatter**). High precision = low spread, *regardless* of whether it's centred on
  the truth.

The classic dartboard:

```
accurate + precise:  tight cluster on the bullseye
precise, not accurate: tight cluster, but off-centre (a bias)
accurate, not precise: scattered, but averaging to the bullseye
neither:               scattered and off-centre
```

This split matters because the **cures differ**: a **systematic** error (bias) is
fixed by **calibration**; **random** error (scatter) is reduced by **averaging**.
You must know which you have.

**Types of error:**

- **Systematic** — a consistent offset/scaling (a miscalibrated meter, loading
  effect, temperature drift, a constant bias). Repeats every time; **averaging
  won't help**; calibration and technique do.
- **Random** — unpredictable fluctuation (noise, quantization, last-digit jitter).
  Averaging N readings reduces it (later lessons).
- **Gross/blunders** — wrong range, wrong connection, misreading — eliminated by
  good practice.

Two more essentials:

- **Units & SI** — always carry units and use consistent SI; most real-world errors
  are unit/scale slips (mV vs V, the factor-of-1000 disaster).
- **Resolution ≠ accuracy.** A meter showing 4.000 V (mV resolution) might be
  accurate only to ±0.5%. **Significant figures** should reflect the true accuracy,
  not the display's digit count.

Underpinning trustworthy measurement is **traceability**: an instrument's accuracy
is meaningful only if it's **calibrated** against standards traceable to national
references (NIST etc.). That chain — and the discipline of stating **uncertainty**
with every result (next lessons) — is what separates a number you can stake a
decision on from a guess. This track teaches both the **instruments** and the
**rigour** to use them well.
""",
        ),
        _code(
            "Accuracy vs precision",
            "12 min",
            r"""# Accuracy = closeness to truth (bias); precision = repeatability (scatter).
# They are independent, and the cures differ: calibration fixes bias, averaging
# reduces scatter. Quantify both for a set of readings. Uses numpy.

import numpy as np

true_value = 5.000     # the real voltage (V)

# Two instruments measuring the same 5.000 V source, 8 readings each.
inst_a = np.array([5.21, 5.19, 5.20, 5.22, 5.18, 5.21, 5.20, 5.19])   # tight but offset
inst_b = np.array([4.97, 5.06, 4.92, 5.10, 4.95, 5.08, 4.90, 5.02])   # centred but scattered

for name, data in [("Instrument A", inst_a), ("Instrument B", inst_b)]:
    mean = float(np.mean(data))
    std = float(np.std(data, ddof=1))
    bias = mean - true_value                    # systematic error (accuracy)
    print(name)
    print("  mean = %.3f V   std (precision) = %.3f V" % (mean, std))
    print("  bias (accuracy) = %+.3f V   = %+.2f%%" % (bias, 100 * bias / true_value))
    print("  -> %s accuracy, %s precision" % (
        "poor" if abs(bias) > 0.05 else "good",
        "high" if std < 0.03 else "low"))
    print()

print("Instrument A: precise but biased -> CALIBRATE it (subtract the +0.20 V offset).")
print("Instrument B: accurate on average but noisy -> AVERAGE more readings.")
print("averaging A does NOT remove its bias; calibrating B does NOT reduce its scatter.")
""",
        ),
        _t(
            "The multimeter",
            "10 min",
            r"""# The multimeter

The **digital multimeter (DMM)** is the most-used instrument in electronics —
voltage, current, resistance, and more. Using one *correctly* (vs just reading the
display) is a real skill, full of subtle traps.

**What it measures and how you connect it:**

- **Voltage (in parallel)** — across the two points. A good voltmeter has **very
  high input impedance** (≥ 10 MΩ) so it draws almost no current.
- **Current (in series)** — you **break the circuit** and route current through the
  meter. A good ammeter has **very low impedance** (a shunt). *Never* put it across
  a voltage — a low-impedance ammeter across a supply is a short (blown fuse).
- **Resistance** — the meter sources a known current and measures voltage; only on a
  **powered-off, isolated** component.

**The loading effect — the classic measurement error.** Connecting the meter
**changes the circuit you're trying to measure**:

- A voltmeter's finite input impedance forms a divider with high source impedances,
  reading **low**. Measuring a 1 MΩ node with a 10 MΩ meter reads ~9% low. Rule:
  the meter impedance must be **≫** the circuit impedance at that node.
- An ammeter's **burden voltage** (its small series resistance × current) drops
  voltage and disturbs the circuit.

Loading is **systematic** — predictable and correctable if you know the impedances.

**True-RMS vs averaging.** AC measurement matters here: a cheap "average-responding"
meter is only accurate for **pure sine waves**; a **true-RMS** meter correctly
measures the **heating value** of *any* waveform (PWM, distorted, spiky) — essential
for modern electronics with non-sinusoidal signals.

**Specs to read:** accuracy is quoted as **±(% of reading + number of counts/
digits)** — e.g. ±(0.5% + 2 digits). The "+digits" term dominates at low readings.
A "**6½-digit**" bench DMM resolves far finer (and is more accurate) than a 3½-digit
handheld — but remember **resolution ≠ accuracy**.

The discipline: pick the right **mode and connection**, respect **input impedance/
burden** so you don't load the circuit, use **true-RMS** for non-sine AC, and
interpret the **accuracy spec** — so the number on the display actually means what
you think it means.
""",
        ),
        _t(
            "The oscilloscope",
            "11 min",
            r"""# The oscilloscope

The **oscilloscope** shows **voltage vs time** — the window into what signals
*actually* do (edges, glitches, ringing, timing). It's the central debugging
instrument, and its specs directly determine what you can and can't trust.

**The specs that matter most:**

- **Bandwidth** — the frequency at which the scope attenuates a signal by −3 dB
  (to ~70%). The **#1 spec**. To measure a signal faithfully you need bandwidth
  **well above** its content — including its **edges** (rise-time/bandwidth from the
  SI track: a scope's rise time ≈ 0.35/BW). Rule of thumb: scope BW ≥ **5×** the
  highest signal frequency (or fast enough for the **edge**, not just the clock).
- **Sample rate (Sa/s)** — how often the ADC samples. Must satisfy **Nyquist**
  (> 2× the highest frequency) and in practice **≫** that (≥ 5×) to render edges and
  avoid **aliasing** (next lab). Bandwidth and sample rate are different specs — both
  must be adequate.
- **Memory depth** — how many samples it can store. Determines how long a window you
  can capture **while keeping a high sample rate** (capture time = memory ÷ sample
  rate).
- **Vertical resolution** — ADC bits (8-bit is typical; 12-bit "high-res" scopes
  exist) — the voltage granularity.

**Probing is part of the measurement** (next course goes deeper):

- A **10× passive probe** divides the signal by 10 but raises input impedance and
  lowers capacitance — better for high frequency; you must **compensate** it
  (adjust the trimmer using the cal square wave) or edges read wrong.
- The **ground lead** matters enormously at high speed: a long ground clip adds
  inductance that makes edges **ring** — an artifact of the *probe*, not the signal.

**Triggering** is what turns a chaotic blur into a stable display: the scope starts
each sweep when a condition is met (**edge** at a level, **pulse width**, **serial
pattern**, etc.). Mastering triggers — edge, holdoff, single-shot for capturing a
rare glitch — is most of practical scope skill.

The key cautions: a scope shows you the signal **as filtered by its bandwidth, its
sample rate, and your probe** — measure a fast edge with too little bandwidth or a
bad ground lead and you'll measure the *instrument*, not the circuit. Knowing those
limits is what makes scope readings trustworthy. You'll see aliasing — a sample-rate
failure — next.
""",
        ),
        _code(
            "Oscilloscope sampling & aliasing",
            "12 min",
            r"""# If you sample a signal slower than 2x its frequency (Nyquist), it ALIASES —
# appearing as a false, lower frequency. This is why scope sample rate matters.
# Compute the aliased frequency for various sample rates. Uses numpy.

import numpy as np

def alias_freq(f_signal, f_sample):
    # The apparent frequency after sampling: fold f_signal about multiples of fs.
    f = f_signal % f_sample
    if f > f_sample / 2.0:
        f = f_sample - f          # fold back below Nyquist
    return f

f_signal = 90e6        # a 90 MHz signal
print("true signal frequency: %.0f MHz" % (f_signal / 1e6))
print("sample rate(MS/s)   Nyquist(MHz)   apparent freq(MHz)   verdict")
for fs_msps in [500, 250, 200, 100, 50]:
    fs = fs_msps * 1e6
    nyq = fs / 2e6
    app = alias_freq(f_signal, fs) / 1e6
    aliased = abs(app - f_signal / 1e6) > 0.01
    print("  %-16d   %-12.0f   %-18.1f   %s" % (fs_msps, nyq, app, "ALIASED (false!)" if aliased else "ok"))

print()
print("Below 180 MS/s (2x90) the 90 MHz signal aliases to a bogus lower frequency.")
print("Always sample >> 2x the highest frequency; a bandwidth-limit filter prevents")
print("out-of-band signals from aliasing into your measurement.")
""",
        ),
        _t(
            "Signal sources & function generators",
            "9 min",
            r"""# Signal sources & function generators

Measurement is half the lab; the other half is **stimulus** — generating known
signals to drive a circuit so you can observe its response. The instruments:

- **Function generator** — produces standard waveforms (**sine, square, triangle,
  pulse, ramp**) with adjustable **frequency, amplitude, offset, and duty cycle**.
  The everyday source for testing.
- **Arbitrary Waveform Generator (AWG)** — plays back **any** waveform you define
  point-by-point (a captured glitch, a modulated signal, a specific test pattern).
  Maximum flexibility.
- **RF signal generator** — high-frequency, spectrally pure sources with precise
  level control and modulation, for RF/wireless test.
- **DC power supplies** — stable, adjustable DC; bench supplies add **current
  limiting** (set a max current to protect a circuit under test) and often
  **constant-voltage/constant-current** modes.
- **SMU (Source-Measure Unit)** — sources voltage **and** measures current (or vice
  versa) simultaneously and precisely — ideal for **I–V curves** of devices (diodes,
  transistors, solar cells).

**Source characteristics that bite you:**

- **Output impedance.** A generator is often specified into a **50 Ω** load (the
  source's own impedance). Drive a high-impedance input and the actual voltage is
  **2×** the set value (the source expected a 50 Ω divider) — a common
  amplitude-doubling surprise. Match impedances or account for it (ties to the SI
  transmission-line lessons).
- **Loading & regulation** — a real source's output sags under load; a good supply
  **regulates** (holds voltage as current changes).
- **Purity & distortion** — a "sine" has harmonics; an RF source has phase noise.
  For sensitive tests the source's own imperfections set the floor.

**Current limiting is your friend.** Setting a power supply's current limit before
powering a new board turns a wiring mistake from a destroyed prototype (and smoke)
into a harmless "supply went into CC mode" — standard practice when bringing up
hardware.

The principle: a measurement is only as good as the **stimulus** behind it. Know
your source's **impedance, regulation, and purity**, set **current limits** for
safety, and choose the right generator (function/AWG/RF/SMU) for the test — so that
when you measure the response, you're seeing the **circuit's** behaviour, not the
source's artifacts.
""",
        ),
        quiz_lesson(
            "Quiz: Measurement & Instruments",
            (
                q(
                    "What is the difference between accuracy and precision?",
                    (
                        opt(
                            "Accuracy = closeness to the true value (bias); precision = repeatability (scatter) — they're independent",
                            correct=True,
                        ),
                        opt("They are the same thing"),
                        opt("Accuracy is about repeatability; precision about the true value"),
                        opt("Both only depend on resolution"),
                    ),
                    "Systematic bias (accuracy) is fixed by calibration; random scatter (precision) is reduced by averaging — you must know which you have.",
                ),
                q(
                    "Why must a voltmeter have very high input impedance?",
                    (
                        opt(
                            "So it draws negligible current and doesn't load (alter) the node it measures",
                            correct=True,
                        ),
                        opt("To measure current accurately"),
                        opt("To increase the reading"),
                        opt("Impedance doesn't matter"),
                    ),
                    "A finite-impedance meter forms a divider with the source impedance (the loading effect), reading low; meter impedance must be ≫ circuit impedance.",
                ),
                q(
                    "Which oscilloscope spec is most important for faithfully capturing a fast edge?",
                    (
                        opt(
                            "Bandwidth (scope rise time ≈ 0.35/BW; choose BW well above the signal's edge content)",
                            correct=True,
                        ),
                        opt("The color of the display"),
                        opt("The number of channels"),
                        opt("The weight of the probe"),
                    ),
                    "Bandwidth limits what edges you can see (and combines with the signal's rise time); sample rate and probing matter too, but BW is #1.",
                ),
                q(
                    "What happens if you sample a 90 MHz signal at 100 MS/s?",
                    (
                        opt(
                            "It aliases — appears as a false lower frequency (you're below 2× Nyquist)",
                            correct=True,
                        ),
                        opt("It is measured perfectly"),
                        opt("Nothing is displayed"),
                        opt("The frequency doubles"),
                    ),
                    "Below 2× the signal frequency, content folds (aliases) to a bogus lower frequency; sample ≫ 2× and band-limit to prevent it.",
                ),
                q(
                    "Why use a true-RMS multimeter for non-sinusoidal AC?",
                    (
                        opt(
                            "It correctly measures the heating (RMS) value of any waveform; averaging meters are only right for pure sines",
                            correct=True,
                        ),
                        opt("It is cheaper"),
                        opt("It only works on DC"),
                        opt("It increases resolution"),
                    ),
                    "Average-responding meters assume a sine; true-RMS handles PWM/distorted/spiky signals correctly — common in modern electronics.",
                ),
                q(
                    "A function generator set to 1 V into 50 Ω drives a high-impedance input. What voltage appears?",
                    (
                        opt(
                            "About 2 V — the source expected a 50 Ω load to halve it", correct=True
                        ),
                        opt("Exactly 1 V"),
                        opt("0.5 V"),
                        opt("0 V"),
                    ),
                    "A 50 Ω source set for a matched load delivers 2× the set value into an open/high-Z input — a common amplitude-doubling surprise.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# test-measurement-intermediate
# ──────────────────────────────────────────────────────────────────────

_TM_INTERMEDIATE = SeedCourse(
    slug="test-measurement-intermediate",
    title="Test & Measurement — Intermediate",
    description=(
        "Quantifying and improving measurements: measurement uncertainty and its "
        "propagation, the spectrum analyzer and FFT windowing, probing and loading "
        "effects, and the digitizing chain (quantization, ENOB, SNR). With "
        "runnable uncertainty, FFT-window, and ADC-ENOB labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Measurement uncertainty",
            "11 min",
            r"""# Measurement uncertainty

A measurement without an **uncertainty** is incomplete — "the voltage is 5.02 V" is
meaningless without "± how much?". **Uncertainty** quantifies the doubt about a
result, and stating it properly (per the **GUM** — Guide to the expression of
Uncertainty in Measurement) is what makes a measurement scientific rather than
anecdotal.

**Error vs uncertainty** (distinct ideas):

- **Error** is the (unknown) difference between the measured and true value.
- **Uncertainty** is the **quantified doubt** — a range within which the true value
  is *believed* to lie, with a stated confidence.

**Two ways to evaluate uncertainty:**

- **Type A** — by **statistics** on repeated measurements: the **standard
  deviation** of the readings, and the **standard error of the mean** (σ/√N) for the
  average. This captures **random** effects.
- **Type B** — by **other means** when you can't repeat: manufacturer **accuracy
  specs**, calibration certificates, resolution limits, judgement. (For a spec like
  ±a with no other info, assume a **uniform distribution** → standard uncertainty
  = a/√3.)

**Standard, combined, expanded:**

- **Standard uncertainty (u)** — each component expressed as a **standard
  deviation** (1σ equivalent).
- **Combined uncertainty (u_c)** — components combined (next lesson) — usually by
  **root-sum-of-squares** for independent sources.
- **Expanded uncertainty (U)** — `U = k · u_c`, where the **coverage factor k**
  (typically **k = 2** for ~95% confidence) widens the interval to a stated
  confidence level. Reported as **value ± U (k=2)**.

**Why RSS, not simple addition?** Independent random errors **partly cancel** — it's
unlikely they all peak in the same direction at once — so they add **in
quadrature** (√(u₁²+u₂²+…)), giving a realistic combined uncertainty rather than a
pessimistic worst-case sum. (Correlated/systematic errors *do* add linearly.)

The professional habit: for every important measurement, **identify the uncertainty
sources** (instrument accuracy, resolution, repeatability, environmental, loading),
express each as a **standard uncertainty**, **combine** them, apply a **coverage
factor**, and **report value ± U**. This turns "5.02 V" into "5.02 V ± 0.03 V (k=2)"
— a statement you can actually base a pass/fail decision on. You'll propagate
uncertainty through a calculation next.
""",
        ),
        _code(
            "Uncertainty propagation",
            "12 min",
            r"""# When you compute a result from measurements (e.g. R = V / I), each input's
# uncertainty propagates. For independent errors, RELATIVE uncertainties add in
# quadrature (root-sum-of-squares). Propagate uncertainty through R = V/I and
# P = V*I. Uses numpy.

import numpy as np

# Measurements with standard uncertainties.
v = 5.00
u_v = 0.02      # +/- 0.02 V (1 sigma)
i = 0.100
u_i = 0.002     # +/- 2 mA

# For products/quotients, relative uncertainties combine in quadrature:
rel_v = u_v / v
rel_i = u_i / i
print("relative uncertainty: V = %.3f%%, I = %.3f%%" % (100 * rel_v, 100 * rel_i))

# R = V / I
r = v / i
rel_r = float(np.sqrt(rel_v ** 2 + rel_i ** 2))
u_r = rel_r * r
print()
print("R = V/I = %.2f ohm" % r)
print("  combined relative uncertainty = sqrt(%.4f^2 + %.4f^2) = %.3f%%" % (rel_v, rel_i, 100 * rel_r))
print("  standard uncertainty u_R = %.3f ohm" % u_r)
print("  expanded (k=2, ~95%%): R = %.1f +/- %.1f ohm" % (r, 2 * u_r))

# P = V * I (same rule for products)
p = v * i
u_p = float(np.sqrt(rel_v ** 2 + rel_i ** 2)) * p
print()
print("P = V*I = %.3f W   ->  %.3f +/- %.3f W (k=2)" % (p, p, 2 * u_p))
print("note: RSS (quadrature) combine, since independent errors partly cancel;")
print("the LARGER relative uncertainty (here I, 2%%) dominates the result.")
""",
        ),
        _t(
            "The spectrum analyzer",
            "10 min",
            r"""# The spectrum analyzer

Where an oscilloscope shows **voltage vs time**, a **spectrum analyzer** shows
**power vs frequency** — the signal's spectral content. It's indispensable for RF,
EMC (you met it there), distortion, noise, and anything where *what frequencies are
present and at what level* is the question.

**Two architectures:**

- **Swept (superheterodyne)** — sweeps a narrow filter across the frequency range,
  measuring power in each slice. Huge frequency range and dynamic range; the
  classic RF instrument.
- **FFT-based** — digitizes the signal and computes the spectrum by **FFT** (like a
  scope's math). Fast, captures everything at once (good for transients), but
  limited by the digitizer's bandwidth. Modern analyzers blend both.

**The key settings (and their trade-offs):**

- **RBW (Resolution Bandwidth)** — the width of the analysis filter / FFT bin. It
  sets **frequency resolution** (can you separate two close tones?) **and** the
  **noise floor**: a **narrower RBW** resolves finer detail and **lowers the noise
  floor** (less noise power per bin → see smaller signals) — but **sweeps slower**.
  The fundamental RBW trade-off: **resolution & sensitivity vs speed**.
- **VBW (Video Bandwidth)** — smooths the trace to average noise and reveal signals
  near the floor.
- **Span & center frequency** — the window you view.
- **Reference level & attenuation** — set the top of the display and protect the
  input; too little attenuation overloads and creates **false (intermodulation)
  products**.

**What you read off it:**

- **Dynamic range** — the span from the largest signal to the noise floor you can
  measure simultaneously; limited by the analyzer's own distortion and noise.
- **Harmonics & spurs** — a "pure" tone shows harmonics (distortion) and spurious
  products; their level vs the fundamental quantifies signal quality (THD, SFDR).
- **Noise floor & phase noise** — the skirt around a carrier reveals phase noise
  (advanced course).

The mental model: a spectrum analyzer trades **time information for frequency
information** (you see *what frequencies*, not *when*) — the Fourier counterpart of
the scope. Choosing **RBW** is the core skill: narrow to resolve and sensitise,
wide to go fast. Misreading the **noise floor as signal**, or overloading the input
into false products, are the classic mistakes the careful engineer avoids.
""",
        ),
        _code(
            "FFT windowing & spectral leakage",
            "13 min",
            r"""# An FFT assumes the captured signal repeats exactly. If a tone doesn't fit a
# whole number of cycles in the window, its energy SMEARS across bins ('spectral
# leakage'). A WINDOW function tapers the edges to suppress it. Compare no-window
# vs a Hann window. Uses numpy.

import numpy as np

n = 256
fs = 256.0                      # sample rate (Hz), so bin spacing = 1 Hz
t = np.arange(n) / fs

# A tone at 20.5 Hz -> NOT an integer number of cycles in the window -> leakage.
f0 = 20.5
sig = np.sin(2 * np.pi * f0 * t)

# Spectra computed at module level (numpy isn't visible inside a function here).
xr = np.fft.rfft(sig)                                    # rectangular (no window)
magr = np.abs(xr)
magr = magr / magr.max()
rect = 20.0 * np.log10(magr + 1e-12)

xh = np.fft.rfft(sig * np.hanning(n))                    # Hann window
magh = np.abs(xh)
magh = magh / magh.max()
hann = 20.0 * np.log10(magh + 1e-12)

# How much energy leaks far from the tone? Look at a bin 10 Hz away (~bin 30).
far = 30
print("tone at %.1f Hz (between bins -> leakage)" % f0)
print("  level 10 bins away from the peak:")
print("    rectangular (no window): %.1f dB" % float(rect[far]))
print("    Hann window            : %.1f dB" % float(hann[far]))
print("  -> the window suppresses far-off leakage by %.0f dB" % (float(rect[far]) - float(hann[far])))
print()
print("peak bin (rect): %d Hz   peak bin (hann): %d Hz" % (int(np.argmax(rect)), int(np.argmax(hann))))
print("windowing trades a slightly WIDER main lobe for far LOWER side lobes ->")
print("essential when a small signal sits near a large one (don't let leakage hide it).")
""",
        ),
        _t(
            "Probing & loading effects",
            "10 min",
            r"""# Probing & loading effects

A recurring, humbling truth of measurement: **the probe is part of the circuit.**
Connecting any instrument perturbs what you're measuring, and at high frequency the
probe's own characteristics can dominate — you end up measuring the **probe**, not
the signal. Mastering probing is what separates trustworthy measurements from
artifacts.

**The loading a probe adds** (an impedance in parallel with your node):

- **Input resistance** — a **1× passive probe** loads with ~1 MΩ; a **10× probe**
  raises it to ~10 MΩ (and divides the signal by 10). Higher R = less DC/low-freq
  loading.
- **Input capacitance** — the killer at high frequency. Even ~10 pF of probe
  capacitance is a **low impedance** at high frequency (Z_C = 1/(2πfC)), shunting
  the signal and **rounding fast edges**. A 10× probe's lower capacitance is why
  it's preferred for fast signals; **active/FET probes** push capacitance to ~1 pF
  for the fastest work.

**The ground lead is a hidden inductor.** A long ground clip forms a loop with the
probe tip; that **inductance** resonates with the probe capacitance and makes edges
**ring** — an artifact entirely created by the measurement setup. Rule: **keep the
ground connection as short as possible** (use a ground spring/tip, not the long
clip) for high-speed work.

**Probe compensation.** A 10× passive probe has a trimmer that must be adjusted
against the scope's **calibration square wave** so the probe's RC matches the scope
input: over/under-compensated probes distort amplitude and edges. **Always check
compensation** — a 5-second habit that prevents wrong readings.

**Specialised probes:**

- **Current probes** (clamp around a wire; Hall-effect or transformer) measure
  current **without breaking the circuit** — essential for power and EMC
  (common-mode current).
- **Differential probes** measure across two points neither of which is ground
  (floating measurements) — vital for power electronics (you can't just clip ground
  to a high-side node).
- **High-voltage probes** scale dangerous voltages safely.

The discipline: **choose the probe for the measurement** (bandwidth, loading,
floating vs grounded, voltage/current), **minimise loading** (10×/active for fast
signals), **keep ground leads short**, and **compensate** passive probes. The probe
is the first link in the measurement chain — get it wrong and everything downstream,
no matter how good the instrument, is suspect.
""",
        ),
        _t(
            "Digitizing: quantization, ENOB & SNR",
            "11 min",
            r"""# Digitizing: quantization, ENOB & SNR

Almost every modern instrument **digitizes** the signal with an **ADC**, so the
quality of that conversion sets a hard floor on the measurement. Understanding the
digitizing chain — quantization, SNR, and effective bits — is essential to knowing
what your numbers really mean (and ties to the sampling/aliasing lessons).

**Quantization** — an N-bit ADC maps a continuous voltage to one of **2ᴺ** levels,
each a step of `Δ = V_range / 2ᴺ`. The rounding to the nearest level introduces
**quantization error** of up to ±½ LSB — an unavoidable noise.

**The ideal SNR of an N-bit ADC** (the famous formula):

$$ \text{SNR} \approx 6.02N + 1.76 \ \text{dB} $$

Each **bit adds ~6 dB** of dynamic range. An 8-bit ADC → ~50 dB; 12-bit → ~74 dB;
16-bit → ~98 dB. This is the **best case** (ideal, full-scale sine, Nyquist
sampling).

```plot
{"title": "Ideal ADC SNR vs resolution (SNR ≈ 6.02·N + 1.76 dB)", "xLabel": "ADC bits (N)", "yLabel": "ideal SNR (dB)", "xRange": [1, 24], "yRange": [0, 150], "functions": [{"expr": "6.02 * x + 1.76", "label": "6.02N + 1.76", "color": "#2563eb"}]}
```

**ENOB (Effective Number Of Bits)** — real converters fall short of the ideal
because of added noise, distortion, jitter, and nonlinearity. ENOB is the **actual**
resolution, back-calculated from the **measured** SINAD (signal-to-noise-and-
distortion):

$$ \text{ENOB} = \frac{\text{SINAD(dB)} - 1.76}{6.02} $$

A "16-bit" ADC delivering 13 ENOB has the *real* performance of a perfect 13-bit
part — so **ENOB, not the marketing bit count, is the spec that matters.**

**What steals ENOB:**

- **Thermal/electronic noise** in the front end.
- **Clock jitter** — timing uncertainty on the sample clock causes amplitude error
  that **worsens with signal frequency** (a fast-slewing signal sampled a little
  early/late has a big voltage error). At high frequencies, jitter often **limits
  ENOB** more than the ADC bits do.
- **Distortion / nonlinearity** (INL/DNL) — adds harmonics that count against
  SINAD.

**Improving effective resolution:**

- **Oversampling & averaging** — sampling faster than needed and averaging spreads
  quantization noise over more bandwidth; decimating recovers **extra bits**
  (~½ bit per 4× oversampling). The basis of **delta-sigma** ADCs and scope
  "high-res" modes.
- **Dithering** — adding a tiny noise can *linearise* and, with averaging, resolve
  below 1 LSB.

The takeaway: digitizing imposes a **quantization noise floor** (~6 dB/bit), but
real-world noise, jitter, and distortion mean **ENOB < N**. Knowing the **ENOB** of
your instrument's front end tells you the true smallest signal you can resolve —
which you'll compute next.
""",
        ),
        _code(
            "ADC ENOB & quantization SNR",
            "12 min",
            r"""# An ideal N-bit ADC has SNR = 6.02N + 1.76 dB (each bit ~ 6 dB). Real parts
# fall short -> ENOB = (measured SINAD - 1.76)/6.02. Compute both and see what
# jitter/noise cost you. Uses numpy.

import numpy as np

print("ideal ADC SNR (full-scale sine):")
print("  bits   ideal SNR(dB)")
for bits in [8, 10, 12, 14, 16, 24]:
    snr = 6.02 * bits + 1.76
    print("   %-4d   %.1f" % (bits, snr))

print()
# A '16-bit' ADC, but the measured SINAD is only 80 dB (noise+jitter+distortion).
nominal_bits = 16
measured_sinad = 80.0
enob = (measured_sinad - 1.76) / 6.02
print("nominal 16-bit ADC, measured SINAD = %.0f dB" % measured_sinad)
print("  ideal 16-bit SNR would be %.1f dB" % (6.02 * 16 + 1.76))
print("  ENOB = (%.0f - 1.76)/6.02 = %.1f effective bits" % (measured_sinad, enob))
print("  -> it really performs like a perfect %.0f-bit converter, not 16-bit." % round(enob))

print()
# Jitter limits SNR at high frequency: SNR_jitter = -20*log10(2*pi*f*t_jitter).
t_jitter = 1e-12      # 1 ps RMS clock jitter
print("clock jitter = 1 ps RMS -> SNR limited by jitter vs signal frequency:")
for f_mhz in [1, 10, 100, 1000]:
    f = f_mhz * 1e6
    snr_j = -20.0 * float(np.log10(2 * np.pi * f * t_jitter))
    print("   f = %-5d MHz -> jitter-limited SNR = %.1f dB (ENOB ~ %.1f)" % (f_mhz, snr_j, (snr_j - 1.76) / 6.02))
print("at high frequency, jitter -- not the bit count -- caps the effective resolution.")
""",
        ),
        quiz_lesson(
            "Quiz: Uncertainty, Spectra & ADCs",
            (
                q(
                    "How are independent uncertainty components combined into a combined uncertainty?",
                    (
                        opt(
                            "Root-sum-of-squares (in quadrature), because independent errors partly cancel",
                            correct=True,
                        ),
                        opt("By simple addition of all of them"),
                        opt("By multiplying them"),
                        opt("By taking the smallest one"),
                    ),
                    "Independent random errors add in quadrature √(u₁²+u₂²+…); the largest component dominates. (Correlated/systematic errors add linearly.)",
                ),
                q(
                    "What does a narrower resolution bandwidth (RBW) on a spectrum analyzer give you?",
                    (
                        opt(
                            "Finer frequency resolution and a lower noise floor (more sensitivity) — at the cost of slower sweeps",
                            correct=True,
                        ),
                        opt("Faster sweeps with no downside"),
                        opt("A higher noise floor"),
                        opt("More output power"),
                    ),
                    "Narrow RBW resolves close tones and lowers noise per bin (see smaller signals) but sweeps slower — the core RBW trade-off.",
                ),
                q(
                    "Why does FFT spectral leakage happen, and how is it reduced?",
                    (
                        opt(
                            "A tone that isn't an integer number of cycles in the window smears across bins; a window function tapers the edges to suppress side lobes",
                            correct=True,
                        ),
                        opt("It's caused by too few channels"),
                        opt("It only happens on DC signals"),
                        opt("Leakage cannot be reduced"),
                    ),
                    "The FFT assumes periodic repetition; non-integer cycles cause discontinuities and leakage. Windows (Hann, etc.) lower side lobes at the cost of a wider main lobe.",
                ),
                q(
                    "What's the approximate ideal SNR of a 12-bit ADC?",
                    (
                        opt("~74 dB (6.02×12 + 1.76)", correct=True),
                        opt("~12 dB"),
                        opt("~120 dB"),
                        opt("~6 dB"),
                    ),
                    "SNR ≈ 6.02N + 1.76; each bit adds ~6 dB. 12 bits → ~74 dB (ideal, full-scale sine).",
                ),
                q(
                    "Why is ENOB more meaningful than an ADC's nominal bit count?",
                    (
                        opt(
                            "ENOB is the actual resolution after real noise, jitter, and distortion — a '16-bit' ADC may deliver only ~13 effective bits",
                            correct=True,
                        ),
                        opt("ENOB is always equal to the bit count"),
                        opt("Bit count already includes noise"),
                        opt("ENOB measures speed, not resolution"),
                    ),
                    "ENOB = (measured SINAD−1.76)/6.02 captures real-world degradation; it's the true smallest signal you can resolve.",
                ),
                q(
                    "Why does a long ground lead on a passive scope probe make edges ring?",
                    (
                        opt(
                            "Its inductance resonates with the probe capacitance — an artifact of the measurement setup, not the signal",
                            correct=True,
                        ),
                        opt("It increases the signal frequency"),
                        opt("It adds DC offset"),
                        opt("Ground leads have no effect"),
                    ),
                    "The ground-loop inductance + probe capacitance form a resonant circuit that rings; keep the ground connection as short as possible for fast signals.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# test-measurement-advanced
# ──────────────────────────────────────────────────────────────────────

_TM_ADVANCED = SeedCourse(
    slug="test-measurement-advanced",
    title="Test & Measurement — Advanced",
    description=(
        "Precision and automation: the VNA and S-parameter calibration, "
        "traceability and calibration methods, jitter and phase-noise "
        "measurement, automated test (SCPI/DAQ), and noise reduction by "
        "averaging. With runnable calibration-fit and averaging labs."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The VNA & S-parameter measurement",
            "10 min",
            r"""# The VNA & S-parameter measurement

The **Vector Network Analyzer (VNA)** is the premier instrument for characterising
high-frequency components and channels — filters, antennas, cables, amplifiers,
PCB interconnects (you met S-parameters in the Signal Integrity track; here's how
they're *measured*). "**Vector**" means it measures both **magnitude and phase** of
the reflected and transmitted waves — full complex S-parameters.

**What it does:** the VNA sends a known **stimulus** (a swept sine) into a port and
measures the **incident, reflected, and transmitted** waves at each port, computing
the **S-parameters** (S11 reflection/return loss, S21 transmission/insertion loss,
etc.) vs frequency. From S-parameters you derive impedance, match, gain, group
delay, and more.

**Why calibration is everything for a VNA:** at GHz frequencies, the **cables,
connectors, and test fixtures** between the VNA and your device have their own loss,
delay, and reflections that **dwarf** the tiny effects you're trying to measure.
Raw VNA data is meaningless until you mathematically **remove** those systematic
errors by measuring **known standards** — moving the **measurement reference plane**
right up to your device.

**SOLT calibration** — the classic method — measures four known standards at the
cable ends:

```
Short, Open, Load (50 Ω), Thru
```

From these the VNA solves for its systematic **error terms** (directivity, source/
load match, tracking) and corrects every subsequent measurement. Other methods —
**TRL** (Thru-Reflect-Line, for fixtures/on-wafer), **electronic cal (ECal)** —
trade convenience for accuracy.

**Error correction** is the heart of it: a calibrated VNA can resolve return losses
of −40 dB or better because the cal **subtracts** the fixture's own reflections.
Skip or botch the cal and you measure your cables, not your device.

The professional reality: a VNA measurement is only as good as its **calibration and
reference-plane definition**. Mastering "measure the standards, set the reference
plane at the DUT, then trust the corrected data" is the core VNA skill — and a
direct application of the reflection/transmission physics from the SI track. This
makes calibration itself the next, broader topic.
""",
        ),
        _t(
            "Calibration & traceability",
            "10 min",
            r"""# Calibration & traceability

Every measurement number is a **claim**, and **calibration** is what backs the
claim. Calibration is the documented comparison of an instrument against a
**reference of known accuracy**, and **traceability** is the unbroken chain of such
comparisons up to **national/international standards** (NIST, NPL, BIPM — ultimately
the SI definitions). Without traceability, "accurate to 0.1%" is just marketing.

**The traceability pyramid:**

```
SI definitions (e.g. the second via atomic clocks)
        ↑
National standards (NIST/NPL)
        ↑
Accredited calibration labs (ISO/IEC 17025)
        ↑
Your reference/standards
        ↑
Your working instruments  ← what you measure with
```

Each step adds uncertainty, so a working DMM's accuracy is **looser** than the lab
standard it's traced to — and you must account for that.

**Key calibration concepts:**

- **Calibration ≠ adjustment.** A *calibration* **measures and documents** the
  error (vs a standard), producing a **certificate** with the deviations and their
  uncertainties. *Adjustment* then **corrects** the instrument to bring it back into
  spec. Sometimes you just apply a **correction factor** from the cert rather than
  adjusting.
- **Calibration interval & drift.** Instruments **drift** with time, temperature,
  and use, so they're recalibrated on a schedule (e.g. annually). An out-of-cal
  instrument's readings are unsupported — and if it's found **out of tolerance** at
  cal, every measurement since the last cal may be suspect (a real quality risk).
- **Error correction in software.** Modern instruments store cal data and **correct
  in real time** (the VNA's SOLT, a DMM's internal cal constants, a sensor's
  cal coefficients).
- **Environmental conditions** — accuracy specs assume a temperature range and
  warm-up time; precision work controls the environment and lets gear stabilise.

**Standards and metrology** underpin it: **voltage** (Josephson junction), **time/
frequency** (atomic/GPS-disciplined references — the most accurate of all),
**resistance** (quantum Hall), etc., with **transfer standards** carrying accuracy
down the chain.

The discipline: a credible measurement states **what it's traceable to**, was made
with **in-calibration** equipment, and reports **uncertainty** that includes the
calibration's contribution. This is the difference between data that holds up in an
audit, a courtroom, or a safety case — and a number someone simply read off a
screen. You'll fit a sensor calibration curve next.
""",
        ),
        _code(
            "Sensor calibration (least-squares fit)",
            "13 min",
            r"""# Calibration often means fitting a curve that maps a sensor's RAW output to the
# TRUE quantity, using measurements against known standards. Fit a straight line
# (least squares), then use it to correct readings and report the residual error.
# Uses numpy.

import numpy as np

# Calibration points: known reference temperature vs the sensor's raw reading.
ref_temp = np.array([0.0, 25.0, 50.0, 75.0, 100.0])        # true (deg C), from a standard
raw = np.array([0.51, 1.52, 2.49, 3.55, 4.48])             # sensor output (V)

# Fit true = a*raw + b (least squares) -> the calibration coefficients.
a, b = np.polyfit(raw, ref_temp, 1)
print("calibration fit: temp = %.3f * V + %.3f" % (a, b))

# Apply the calibration and check residuals (fit error at each point).
predicted = a * raw + b
residuals = predicted - ref_temp
rms_error = float(np.sqrt(np.mean(residuals ** 2)))
print()
print("  ref(C)   raw(V)   calibrated(C)   residual(C)")
for i in range(len(ref_temp)):
    print("  %5.0f    %.2f     %7.2f         %+.3f" % (ref_temp[i], raw[i], predicted[i], residuals[i]))
print()
print("RMS calibration residual: %.3f C" % rms_error)

# Use the calibration on a NEW raw reading.
new_raw = 3.00
print("new reading %.2f V -> calibrated %.2f C" % (new_raw, a * new_raw + b))
print("the fit removes the sensor's offset/scale (systematic error); residual ~ its")
print("remaining nonlinearity/noise -> part of the measurement uncertainty budget.")
""",
        ),
        _t(
            "Jitter & phase-noise measurement",
            "10 min",
            r"""# Jitter & phase-noise measurement

In high-speed and RF systems, the **purity of timing** is as important as amplitude.
**Jitter** (time-domain) and **phase noise** (frequency-domain) are two views of the
**same** imperfection — a clock or carrier whose edges/phase deviate from ideal —
and measuring them is advanced, demanding work.

**Jitter (time domain)** — the deviation of signal edges from their ideal positions
(you met it in the SI track). Measured on a high-bandwidth scope or a dedicated
**Time Interval Analyzer / BERT**, and decomposed:

- **Random jitter (RJ)** — Gaussian, unbounded (thermal); quoted as **RMS**, and
  extrapolated to a **peak-to-peak at a target BER** (e.g. ×14 for 1e-12).
- **Deterministic jitter (DJ)** — bounded, with causes: **periodic** (PJ, from
  coupling), **data-dependent** (DDJ/ISI), **duty-cycle distortion**.
- **Total jitter (TJ)** = combined, evaluated at a BER — the number that closes the
  horizontal eye.

Tools: the **eye diagram** and **jitter bathtub** (BER vs sampling position) show
the timing margin directly; **TIE (Time Interval Error)** tracks edge-by-edge
deviation.

**Phase noise (frequency domain)** — the same instability seen as **noise skirts**
around a carrier, quantified as **dBc/Hz** (power relative to the carrier, per Hz of
bandwidth) at an **offset frequency** from the carrier (e.g. −110 dBc/Hz at 10 kHz
offset). Measured with a spectrum/signal-source analyzer. Crucial for RF: phase
noise sets the noise floor of receivers, limits modulation accuracy (EVM), and
**integrating** the phase-noise curve over an offset range gives the **RMS jitter**
— directly linking the two domains.

**Why it's hard:** you're measuring **tiny timing deviations** (femtoseconds to
picoseconds) or noise **far below** the carrier (−100+ dBc/Hz), so the
**measurement instrument's own jitter/phase noise must be better than the device's**
— the same "the gear must out-perform the signal" rule as bandwidth and ENOB. Cross-
correlation techniques and very low-noise references are used to push the
measurement floor down.

The unifying insight: **jitter and phase noise are the time- and frequency-domain
faces of timing instability**, related by Fourier (integrate phase noise → jitter).
Advanced timing measurement is about driving the **instrument's own noise floor**
below the device's, then decomposing the result (RJ/DJ, or phase noise vs offset) to
predict link BER or RF performance. It's where measurement rigour meets the SI and
communications tracks.
""",
        ),
        _t(
            "Automated test & data acquisition",
            "10 min",
            r"""# Automated test & data acquisition

Manual measurement doesn't scale: production test, long characterisation sweeps,
and repeatable validation demand **automation**. Modern test & measurement is as
much **software** as hardware — instruments are programmable nodes in a system.

**Controlling instruments — SCPI & interfaces:**

- **SCPI (Standard Commands for Programmable Instruments)** — a standardised ASCII
  command language most instruments speak: you send text like
  `MEAS:VOLT:DC?` and read back the value. Standardised commands mean code is
  largely **portable** across vendors.
- **Interfaces / buses** — historically **GPIB (IEEE-488)**; now **USB**, **LAN
  (LXI)**, and **PXI** (modular instruments in a chassis for high-density automated
  test). **VISA** is the common software API that abstracts the bus.
- **Drivers & frameworks** — **IVI** drivers, and ecosystems like **LabVIEW**,
  **Python (PyVISA)**, MATLAB — to script sweeps, sequence instruments, and log
  data.

**Data acquisition (DAQ):**

- **DAQ hardware** — multi-channel ADCs/DACs and digital I/O that turn a PC into a
  measurement system, sampling many sensors at once. Key specs echo the digitizing
  lesson: **resolution (bits), sample rate, channel count, simultaneous vs
  multiplexed** sampling.
- **Sensors → conditioning → digitize** — real DAQ needs **signal conditioning**
  (amplification, filtering — anti-alias filters!, isolation, bridge excitation for
  strain gauges, cold-junction comp for thermocouples) **before** the ADC.
- **Sampling discipline** — apply the Nyquist/anti-aliasing rules from the basics;
  timestamp and synchronise channels.

**Automated Test Equipment (ATE) & production test:**

- **ATE** runs a defined **test sequence** on each unit (power-up, stimulus,
  measure, compare to limits, pass/fail, log), often with a **fixture/bed-of-nails**
  or **boundary scan (JTAG)** to reach test points.
- Goals: **throughput**, **repeatability**, **traceable logging** (every unit's data
  stored), and **test coverage** (catching the defects that matter).

**Good automation practice:** check **instrument status/errors** after commands,
account for **settling time** (don't read before the measurement stabilises), handle
**ranges/overloads** programmatically, and **record metadata** (instrument IDs, cal
dates, settings) with every dataset for traceability.

The shift at the advanced level: a measurement is rarely a single reading — it's an
**automated system** that stimulates, measures, decides, and logs at scale, with the
**software** ensuring repeatability and traceability. Mastering SCPI/VISA + DAQ +
sound sampling/conditioning turns one-off lab measurements into reliable
characterisation and production test. You'll quantify a core automation payoff —
averaging to cut noise — next.
""",
        ),
        _code(
            "Averaging to reduce noise",
            "12 min",
            r"""# Averaging N independent readings reduces RANDOM noise by sqrt(N): the SNR
# improves by 10*log10(N) dB. (It does NOTHING for systematic bias.) Demonstrate
# the sqrt(N) law and the dB improvement. Uses numpy.

import numpy as np

true_value = 1.000        # the real signal level (V)
noise_sigma = 0.050       # random noise std on a single reading (V)
bias = 0.010              # a SYSTEMATIC offset the instrument has (V)

# Deterministic pseudo-noise (no RNG in the sandbox): a mix of sinusoids, ~unit std.
m = 4096
base = (np.sin(np.arange(m) * 1.1) + np.sin(np.arange(m) * 2.7 + 1.0)
        + np.sin(np.arange(m) * 0.37 + 2.0))
base = base / float(np.std(base))            # normalise to std 1
readings = true_value + bias + noise_sigma * base

print("single-reading noise std = %.3f V, systematic bias = %.3f V" % (noise_sigma, bias))
print("  N      mean        noise std of mean   SNR improvement")
for n in [1, 4, 16, 64, 256, 1024]:
    chunk = readings[:n]
    mean = float(np.mean(chunk))
    # std of the MEAN of n readings ~ sigma/sqrt(n)
    std_of_mean = noise_sigma / float(np.sqrt(n))
    improvement_db = 10.0 * float(np.log10(n))
    print("  %-5d  %.4f V    %.4f V            +%.1f dB" % (n, mean, std_of_mean, improvement_db))

print()
print("noise falls as 1/sqrt(N) (e.g. 256x readings -> 16x less noise, +24 dB SNR).")
print("BUT the %.3f V bias never averages away -> only CALIBRATION removes it." % bias)
""",
        ),
        _t(
            "Best practices & pitfalls",
            "9 min",
            r"""# Best practices & pitfalls

Advanced measurement is as much **discipline** as equipment. The instruments are
capable; most bad data comes from **technique**. A consolidated field guide to
getting trustworthy numbers — and the classic traps that produce confident,
wrong ones.

**The measurement mindset:**

- **State uncertainty, always.** A number without a ± and a confidence level is
  incomplete. Budget the uncertainty (Type A + B), combine in quadrature, report
  with a coverage factor.
- **Know your error type.** Systematic (bias) → **calibrate**; random (scatter) →
  **average**. Applying the wrong cure wastes effort (averaging a biased meter
  forever won't fix it).
- **The instrument must out-perform the signal.** Bandwidth ≫ signal, ENOB/noise
  floor below your smallest signal, instrument jitter/phase noise below the
  device's. Otherwise you measure the **instrument**.

**The classic pitfalls:**

- **Loading / probing artifacts** — the probe changes the circuit; high capacitance
  rounds edges, long ground leads ring, low meter impedance loads the node.
  *Cross-check with a different probe/method if a result looks odd.*
- **Aliasing** — sampling too slowly fabricates false frequencies; always band-limit
  and sample ≫ 2×.
- **Ground loops in the measurement setup** — connecting instrument grounds via
  different paths injects hum/noise into the reading (a measurement EMC problem!);
  use single-point grounding, isolation, or differential/battery-powered
  instruments. (Never defeat a safety ground — isolate properly instead.)
- **Out-of-calibration / un-warmed-up gear** — drift and thermal transients;
  let precision instruments stabilise.
- **Reading resolution as accuracy** — extra digits aren't extra truth; report
  significant figures the accuracy supports.
- **Autoranging / wrong range** — overloads create false products; too coarse a
  range throws away resolution.
- **Confirmation bias** — stopping when you get the "expected" answer. Sanity-check
  against an independent method or a back-of-envelope estimate.

**Sound workflow:** plan the measurement and its uncertainty budget → use
in-cal, warmed-up gear → choose the right probe/range/settings → minimise loading and
ground loops → take enough readings (average random noise) → cross-check
suspicious results → record everything (settings, conditions, instrument/cal IDs)
for traceability.

The throughline of the whole track: **a measurement is a claim about reality with a
quantified doubt.** Great test engineers are skeptical of their own data — they know
the instrument's limits, anticipate the artifacts, control the systematic errors,
quantify the random ones, and can defend every number they report. That rigour —
not the price of the equipment — is what makes measurements trustworthy.
""",
        ),
        quiz_lesson(
            "Quiz: Calibration, Timing & Automation",
            (
                q(
                    "Why must a VNA be calibrated (e.g. SOLT) before measuring?",
                    (
                        opt(
                            "To remove the systematic errors of the cables/fixtures and move the reference plane to the device",
                            correct=True,
                        ),
                        opt("To increase the output power"),
                        opt("To make it sweep faster"),
                        opt("Calibration is optional for a VNA"),
                    ),
                    "At GHz the fixture's loss/reflections dwarf the device's; measuring known standards (Short/Open/Load/Thru) lets the VNA correct them.",
                ),
                q(
                    "What does traceability mean for a measurement?",
                    (
                        opt(
                            "An unbroken chain of calibrations linking the instrument to national/SI standards, each adding documented uncertainty",
                            correct=True,
                        ),
                        opt("That the instrument is expensive"),
                        opt("That the result was written down"),
                        opt("That no calibration is needed"),
                    ),
                    "Traceability backs an accuracy claim; without it, a stated accuracy is unsupported. Each step up to NIST/SI adds uncertainty you account for.",
                ),
                q(
                    "How are jitter (time domain) and phase noise (frequency domain) related?",
                    (
                        opt(
                            "They are two views of the same timing instability — integrating the phase-noise curve over offset gives RMS jitter",
                            correct=True,
                        ),
                        opt("They are completely unrelated"),
                        opt("Jitter is about amplitude, phase noise about frequency error"),
                        opt("Only one of them is real"),
                    ),
                    "A clock's timing instability appears as jitter (edges) or phase-noise skirts (dBc/Hz); Fourier links them (∫ phase noise → jitter).",
                ),
                q(
                    "What is SCPI?",
                    (
                        opt(
                            "A standardised text command language for programming instruments (e.g. MEAS:VOLT:DC?)",
                            correct=True,
                        ),
                        opt("A type of oscilloscope probe"),
                        opt("A calibration standard"),
                        opt("A noise-reduction algorithm"),
                    ),
                    "SCPI standardises instrument commands so automated test code is largely portable across vendors (over GPIB/USB/LAN via VISA).",
                ),
                q(
                    "Averaging 256 independent noisy readings improves SNR by about…",
                    (
                        opt(
                            "+24 dB (10·log10(256)); noise falls as 1/√N — but bias is unaffected",
                            correct=True,
                        ),
                        opt("+256 dB"),
                        opt("Nothing"),
                        opt("It removes systematic bias"),
                    ),
                    "Random noise drops as 1/√N (256× → 16× less noise → +24 dB); averaging does nothing for systematic bias, which needs calibration.",
                ),
                q(
                    "A ground loop in your measurement setup will…",
                    (
                        opt(
                            "Inject hum/noise into the reading via current flowing between differently-grounded points",
                            correct=True,
                        ),
                        opt("Improve accuracy"),
                        opt("Have no effect"),
                        opt("Only matter for DC"),
                    ),
                    "Different ground paths form a loop that picks up noise — a measurement EMC problem; cure with single-point grounding, isolation, or differential instruments (never defeat safety ground).",
                ),
            ),
        ),
    ),
)


TEST_MEASUREMENT_COURSES = (_TM_BASICS, _TM_INTERMEDIATE, _TM_ADVANCED)
