"""Analog Communications track: Basics -> Intermediate -> Advanced.

From signals, spectra and bandwidth to amplitude modulation (AM, DSB-SC, SSB,
VSB), angle modulation (FM/PM), the superheterodyne receiver, noise performance
and the analog-to-digital bridge (sampling, PAM, PCM) plus multiplexing. Lessons
are `text` with LaTeX, interactive ```plot blocks (AM/FM waveforms, spectra, SNR
curves) and ```mermaid block diagrams (modulator/demodulator, superheterodyne
receiver). Builds on the Signals and Probability tracks.
"""

# Lesson prose uses typographic characters (×, →, ≈, ±, μ, Δ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Analog Communications — Basics ───────────────────────────────────────────

_AC_BASICS = SeedCourse(
    slug="analog-comms-basics",
    title="Analog Communications — Basics",
    description=(
        "How a message rides a radio wave: signals, spectra and bandwidth, the "
        "communication-system block diagram, and amplitude modulation (AM, "
        "DSB-SC, envelope detection, modulation index). Closes with a first look "
        "at noise and SNR, using interactive waveform and spectrum plots."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Signals, spectra & bandwidth",
            "10 min",
            """\
# Signals, spectra & bandwidth

Communication starts with a **signal** — a voltage that varies in time, $m(t)$.
The same signal can be viewed two ways: in the **time domain** (how it changes
instant to instant) and the **frequency domain**, or **spectrum** (which sine
waves it is built from). The Fourier transform moves between them.

The **bandwidth** $B$ is the span of frequencies a signal occupies. Speech sits
in roughly $300\\text{ Hz}$–$3.4\\text{ kHz}$; music up to $\\approx 20\\text{ kHz}$.
Bandwidth is the currency of communications: it limits how many users a channel
can carry and how fast information can flow.

A pure tone is a single spectral line; richer signals spread out. Below is a
two-tone "message" — drag the second tone's frequency and watch where energy
lands:

```plot
{"title": "A two-tone message and its bandwidth", "xLabel": "time t", "yLabel": "m(t)", "xRange": [0, 6.28], "yRange": [-2.2, 2.2], "controls": [{"name": "f2", "range": [1, 6], "value": 3, "step": 1, "label": "second tone (× base freq)"}], "functions": [{"expr": "sin(x) + 0.8*sin(f2*x)", "label": "m(t) = sin(t) + 0.8 sin(f2·t)", "color": "#2563eb"}]}
```

Two ideas carry through the whole course:

- A signal of bandwidth $B$ needs at least $B$ of spectrum to be sent faithfully.
- **Baseband** signals (centred at $0\\text{ Hz}$) can't travel far as radio; we
  must shift them up to a **carrier** frequency. That shift is **modulation**.

**Next:** the block diagram of a complete communication system.
""",
        ),
        _t(
            "The communication-system block diagram",
            "10 min",
            """\
# The communication-system block diagram

Every analog link, from an AM broadcast to a walkie-talkie, follows the same
chain. The **transmitter** turns a message into a signal suited to the channel;
the **channel** carries it (and corrupts it); the **receiver** recovers the
message:

```mermaid
flowchart LR
  SRC["source: voice / music"] --> MOD["modulator: shift to carrier fc"]
  MOD --> PA["power amplifier"]
  PA --> CH["channel: air / cable"]
  CH --> RX["RX front end: filter + amplify"]
  RX --> DEM["demodulator: recover m(t)"]
  DEM --> SINK["sink: speaker"]
  NOISE["noise + interference"] --> CH
```

The key blocks:

- **Modulator** — impresses the message $m(t)$ onto a high-frequency carrier
  $c(t) = A_c\\cos(2\\pi f_c t)$ so it can radiate efficiently from an antenna
  (antennas need to be a sizeable fraction of a wavelength).
- **Channel** — adds **noise** (random thermal fluctuation), **attenuation**, and
  sometimes interference and fading.
- **Demodulator** — undoes the modulation to recover $m(t)$ at the far end.

Two figures of merit recur: the **bandwidth** the scheme consumes and the
**signal-to-noise ratio (SNR)** it delivers. Analog modulation schemes are really
just different trades between those two. Carrier frequency choice ($f_c \\gg B$)
keeps the modulated signal a narrow band perched high in the spectrum, so many
stations coexist.

**Next:** the simplest modulation — AM.
""",
        ),
        _t(
            "Amplitude modulation (AM) basics",
            "11 min",
            """\
# Amplitude modulation (AM) basics

In **amplitude modulation** the message rides on the *amplitude* of the carrier.
Standard (full-carrier) AM is

$$s(t) = A_c\\,[\\,1 + \\mu\\,m_n(t)\\,]\\cos(2\\pi f_c t),$$

where $m_n(t)$ is the message scaled to peak $\\pm 1$ and $\\mu$ is the
**modulation index**. The carrier's envelope traces out $1 + \\mu m_n(t)$ — the
message is literally the outline of the waveform. Below, a sinusoidal message
shapes a faster carrier:

```plot
{"title": "AM waveform: message rides the carrier envelope", "xLabel": "time t", "yLabel": "s(t)", "xRange": [0, 6.28], "yRange": [-2.2, 2.2], "controls": [{"name": "mu", "range": [0, 1], "value": 0.5, "label": "modulation index μ"}], "functions": [{"expr": "(1 + mu*sin(2*x))*sin(20*x)", "label": "AM signal s(t)", "color": "#2563eb"}, {"expr": "1 + mu*sin(2*x)", "label": "envelope 1 + μ·m(t)", "color": "#dc2626"}]}
```

In the frequency domain, multiplying by $\\cos(2\\pi f_c t)$ **shifts** the message
spectrum up to sit around $f_c$. A single message tone at $f_m$ produces three
lines: the **carrier** at $f_c$ and two **sidebands** at $f_c \\pm f_m$:

```plot
{"title": "AM spectrum: carrier plus upper and lower sidebands", "xLabel": "frequency f", "yLabel": "magnitude", "xRange": [0, 12], "yRange": [0, 1.1], "points": [{"x": 6, "y": 1, "label": "carrier fc", "color": "#dc2626", "size": 7}, {"x": 5, "y": 0.4, "label": "LSB fc − fm", "color": "#2563eb", "size": 6}, {"x": 7, "y": 0.4, "label": "USB fc + fm", "color": "#2563eb", "size": 6}]}
```

So AM of a message of bandwidth $B$ takes up $2B$ of spectrum — twice the
message bandwidth. The big upside: it is trivially cheap to **demodulate** (the
envelope detector, two lessons on). The downside: most transmitted power sits in
the carrier, which conveys no information.

**Next:** drop the carrier — DSB-SC.
""",
        ),
        _t(
            "DSB-SC & coherent detection",
            "11 min",
            """\
# DSB-SC & coherent detection

Standard AM wastes power on a carrier line. **Double-sideband suppressed-carrier
(DSB-SC)** simply multiplies the message by the carrier with no added DC:

$$s(t) = A_c\\,m(t)\\cos(2\\pi f_c t).$$

The spectrum keeps both sidebands but the carrier line vanishes, so all
transmitted power carries information. The catch: the envelope no longer tracks
the message (it follows $|m(t)|$ and flips phase whenever $m(t)$ crosses zero),
so a simple envelope detector fails.

To recover $m(t)$ we use **coherent (synchronous) detection**: multiply the
received signal by a *local* carrier of the same frequency **and phase**, then
low-pass filter. Using $\\cos^2\\theta = \\tfrac12(1+\\cos 2\\theta)$:

$$s(t)\\cos(2\\pi f_c t) = \\tfrac{A_c}{2}m(t) + \\tfrac{A_c}{2}m(t)\\cos(4\\pi f_c t).$$

The low-pass filter keeps the first term ($\\propto m(t)$) and discards the term
near $2f_c$:

```mermaid
flowchart LR
  RX["received s(t)"] --> MIX["× local cos(2π fc t)"]
  LO["local oscillator (phase-locked)"] --> MIX
  MIX --> LPF["low-pass filter"]
  LPF --> OUT["recovered m(t)"]
```

The price of efficiency is a **phase-coherent** local oscillator. A phase error
$\\phi$ scales the output by $\\cos\\phi$ — at $\\phi = 90°$ the signal disappears
entirely (the *quadrature-null* effect). Generating that synchronized reference
is the hard part, and motivates the carrier-recovery loops used in real receivers.

**Next:** the cheap detector that made AM radio ubiquitous.
""",
        ),
        _t(
            "Envelope detection & modulation index",
            "10 min",
            """\
# Envelope detection & modulation index

The reason broadcast AM uses a full carrier is the **envelope detector**: a
diode, a resistor and a capacitor. The diode rectifies the AM signal; the RC
network follows the peaks — tracing the envelope $A_c[1 + \\mu m_n(t)]$ — which is
the message plus a DC offset. No local oscillator, no phase lock: a handful of
cents of parts.

But it only works while the envelope stays **positive**, i.e. while
$1 + \\mu m_n(t) > 0$. That requires

$$\\mu \\le 1 \\quad(\\text{modulation index } \\le 100\\%).$$

If $\\mu > 1$ the envelope folds through zero — **over-modulation** — and the
detector produces a badly distorted message. Slide $\\mu$ past 1 and watch the red
envelope dip below zero:

```plot
{"title": "Over-modulation: envelope goes negative when μ > 1", "xLabel": "time t", "yLabel": "amplitude", "xRange": [0, 6.28], "yRange": [-2.5, 2.5], "controls": [{"name": "mu", "range": [0, 1.8], "value": 0.7, "label": "modulation index μ"}], "functions": [{"expr": "(1 + mu*sin(x))*sin(16*x)", "label": "AM signal", "color": "#2563eb"}, {"expr": "1 + mu*sin(x)", "label": "envelope (must stay > 0)", "color": "#dc2626"}, {"expr": "0", "label": "zero line", "color": "#94a3b8"}]}
```

The modulation index also sets **efficiency**: the fraction of transmitted power
in the (informative) sidebands is $\\eta = \\dfrac{\\mu^2}{2 + \\mu^2}$ for a tone.
Even at $\\mu = 1$ that is only $33\\%$ — two-thirds of the power is the wasted
carrier. That is the standing trade of broadcast AM: cheap receivers, poor power
efficiency.

**Next:** what noise does to all of this.
""",
        ),
        _t(
            "Intro to noise & SNR in comms",
            "10 min",
            """\
# Intro to noise & SNR in comms

Every channel adds **noise** — chiefly **thermal noise**, the random motion of
electrons, modelled as **additive white Gaussian noise (AWGN)**: flat across
frequency, Gaussian in amplitude. The quality of a recovered message is set by
the **signal-to-noise ratio**,

$$\\mathrm{SNR} = \\frac{P_{\\text{signal}}}{P_{\\text{noise}}},\\qquad
\\mathrm{SNR}_{\\mathrm{dB}} = 10\\log_{10}\\mathrm{SNR}.$$

Two levers raise SNR: more **signal power**, or less **noise power**. Noise power
$= N_0 B$ grows with bandwidth, so a wider receiver lets in more noise — one
reason we filter tightly around the wanted signal. Output SNR climbs linearly
with transmitted power; on a dB scale that is the familiar straight line:

```plot
{"title": "Output SNR vs transmitted power (SNR in dB = 10·log10 P)", "xLabel": "transmitted power (linear)", "yLabel": "SNR (dB)", "xRange": [0.5, 20], "yRange": [-4, 16], "functions": [{"expr": "10*log10(x)", "label": "SNR (dB) = 10·log10(P)", "color": "#2563eb"}], "points": [{"x": 2, "y": 3.01, "label": "+3 dB per doubling", "color": "#dc2626", "size": 6}, {"x": 4, "y": 6.02, "color": "#dc2626", "size": 6}]}
```

A few rules of thumb that frame the whole course:

- Doubling signal power adds $\\approx 3\\text{ dB}$ of SNR.
- Halving the receiver bandwidth (when allowed) also adds $\\approx 3\\text{ dB}$.
- Different modulation schemes turn a given received SNR into very different
  *output* SNR — the heart of the Advanced track.

DSB-SC and AM, recovered coherently, give roughly the same output SNR as sending
the baseband signal directly; AM with envelope detection is a few dB worse
because of the carrier. The big SNR wins come from FM — which we build toward
next.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Analog Communications — Intermediate ─────────────────────────────────────

_AC_INTERMEDIATE = SeedCourse(
    slug="analog-comms-intermediate",
    title="Analog Communications — Intermediate",
    description=(
        "Bandwidth-saving and angle modulation: single- and vestigial-sideband "
        "(SSB/VSB), frequency and phase modulation (instantaneous frequency, "
        "Carson's rule), FM generation and detection (discriminator, PLL), and "
        "the superheterodyne receiver with mixing, image frequency and the IF. "
        "Interactive FM waveform plots and receiver block diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "SSB & VSB modulation",
            "11 min",
            """\
# SSB & VSB modulation

DSB-SC sends *both* sidebands, but each is a mirror image of the other — so one
is redundant. **Single-sideband (SSB)** transmits just one, halving the occupied
bandwidth to $B$ (the message bandwidth) and concentrating all power there. It is
the workhorse of long-haul HF voice and amateur radio precisely because it is so
spectrum- and power-efficient.

Two ways to build SSB:

- **Filter method** — generate DSB-SC, then a sharp band-pass filter removes the
  unwanted sideband. Needs a steep filter, hard when the message has energy down
  near DC.
- **Phasing (Hartley) method** — combine two DSB-SC paths in phase quadrature
  ($90°$ shifts of carrier and message) so one sideband cancels.

SSB's weakness is that signals with energy at very low frequencies (video,
sharp edges) have sidebands that crowd the carrier, making the filter
impossible. **Vestigial-sideband (VSB)** is the compromise: pass one full
sideband plus a small *vestige* of the other, using a filter with odd symmetry
about the carrier so the overlapping parts add back to a flat response. VSB is
how analog TV sent its wideband video in a manageable channel:

```plot
{"title": "Sideband content: DSB vs SSB vs VSB (relative occupancy)", "xLabel": "offset from carrier (× B)", "yLabel": "magnitude", "xRange": [-1.5, 1.5], "yRange": [0, 1.2], "functions": [{"expr": "(x > -1)*(x < 0)*1 + (x > 0)*(x < 1)*1", "label": "DSB (both sidebands)", "color": "#94a3b8"}, {"expr": "(x > 0)*(x < 1)*1", "label": "SSB (upper only)", "color": "#2563eb"}, {"expr": "(x > 0)*(x < 1)*1 + (x > -0.25)*(x < 0)*0.5", "label": "VSB (USB + vestige)", "color": "#dc2626"}]}
```

The takeaway: **SSB buys bandwidth and power at the cost of harder hardware**;
VSB trades a little bandwidth back for a realizable filter.

**Next:** modulate the angle instead of the amplitude.
""",
        ),
        _t(
            "Frequency modulation (FM) & Carson's rule",
            "12 min",
            """\
# Frequency modulation (FM) & Carson's rule

Instead of varying amplitude, **angle modulation** varies the *phase* of the
carrier. In **frequency modulation (FM)** the **instantaneous frequency**
deviates in proportion to the message:

$$f_i(t) = f_c + k_f\\,m(t),\\qquad
s(t) = A_c\\cos\\!\\Big(2\\pi f_c t + 2\\pi k_f\\!\\int_0^t m(\\tau)\\,d\\tau\\Big).$$

The amplitude is **constant** — information lives entirely in the changing
spacing of the zero crossings. Below, the wave bunches up where the message is
high and stretches where it is low; the envelope never moves:

```plot
{"title": "FM waveform: frequency tracks the message, amplitude is constant", "xLabel": "time t", "yLabel": "s(t)", "xRange": [0, 6.28], "yRange": [-1.6, 1.6], "controls": [{"name": "beta", "range": [0, 8], "value": 4, "label": "modulation index β"}], "functions": [{"expr": "cos(12*x + beta*sin(x))", "label": "FM signal", "color": "#2563eb"}, {"expr": "1", "label": "constant envelope", "color": "#dc2626"}]}
```

Two defining quantities:

- **Frequency deviation** $\\Delta f = k_f \\max|m(t)|$ — the peak swing of $f_i$.
- **Modulation index** $\\beta = \\dfrac{\\Delta f}{f_m}$ (for a tone of frequency
  $f_m$).

Unlike AM, FM's bandwidth is *not* simply $2B$ — the integral spreads energy into
infinitely many sidebands (Bessel functions). The practical estimate is
**Carson's rule**:

$$B_{\\mathrm{FM}} \\approx 2(\\Delta f + f_m) = 2(\\beta + 1)f_m.$$

Broadcast FM uses $\\Delta f = 75\\text{ kHz}$ with $f_m$ up to $15\\text{ kHz}$, so
$B \\approx 2(75+15) = 180\\text{ kHz}$ — far wider than AM. That wide bandwidth is
not waste: in the Advanced track it buys a large SNR improvement.

**Next:** FM's close cousin, PM.
""",
        ),
        _t(
            "Phase modulation (PM)",
            "10 min",
            """\
# Phase modulation (PM)

**Phase modulation (PM)** varies the carrier phase *directly* with the message:

$$s(t) = A_c\\cos\\!\\big(2\\pi f_c t + k_p\\,m(t)\\big).$$

FM and PM are two faces of the same coin — **angle modulation** — and differ only
by an integrator:

- FM = PM of the **integral** of the message ($\\text{phase} \\propto \\int m$).
- PM = FM of the **derivative** of the message ($\\text{instantaneous freq} \\propto m'$).

So you can build an FM signal by integrating the message and feeding it to a
phase modulator, and vice versa. Both share FM's defining virtue: **constant
envelope**, which means amplitude noise and amplifier nonlinearity barely matter
(you can use efficient saturating Class-C/D amplifiers).

```mermaid
flowchart LR
  MSG["message m(t)"] --> SEL{"FM or PM?"}
  SEL -->|FM| INT["integrate m(t)"]
  SEL -->|PM| DIR["use m(t) directly"]
  INT --> PMOD["phase modulator: φ = k·input"]
  DIR --> PMOD
  PMOD --> OUT["angle-modulated carrier"]
```

The instantaneous frequency of PM is $f_i = f_c + \\dfrac{k_p}{2\\pi}m'(t)$ — so PM
*emphasizes* fast-changing parts of the message. Pure PM is rarer in broadcasting
but central to **digital** modulation (PSK), where phase carries the bits, and it
is the natural language of the phase-locked loop. Carson's rule applies to PM too,
with the deviation set by the *derivative* of the message.

**Next:** how to make and recover an FM signal.
""",
        ),
        _t(
            "FM generation & detection",
            "11 min",
            """\
# FM generation & detection

**Generating FM.** The direct way uses a **voltage-controlled oscillator (VCO)**
whose output frequency is a linear function of an input voltage: feed it the
message and you get $f_i = f_c + k_f m(t)$ by construction. The indirect
(Armstrong) method builds a narrowband FM signal from a phase modulator, then
multiplies the frequency up to widen the deviation — trading hardware for better
frequency stability.

**Detecting FM** means turning frequency changes back into amplitude. Two classic
approaches:

- **Frequency discriminator** — a circuit whose output amplitude is proportional
  to input frequency (a differentiator followed by an envelope detector). It
  converts FM to AM, then detects the envelope. Cheap, but needs a **limiter**
  first to strip any residual amplitude variation.
- **Phase-locked loop (PLL)** — a feedback loop whose VCO tracks the incoming
  phase; the *control voltage* that keeps it locked is exactly the demodulated
  message. The dominant modern detector — robust and easy to integrate:

```mermaid
flowchart LR
  IN["FM input"] --> PD["phase detector"]
  PD --> LF["loop filter"]
  LF --> VCO["VCO"]
  VCO --> PD
  LF --> OUT["recovered m(t)"]
```

The PLL's loop filter output follows the instantaneous frequency, so it doubles
as the demodulator. Because FM has a **constant envelope**, the front end can hard
**limit** the signal — clipping away amplitude noise entirely before detection.
That noise-immunity is why FM sounds so much cleaner than AM.

**Next:** the receiver architecture that ties it all together.
""",
        ),
        _t(
            "The superheterodyne receiver",
            "11 min",
            """\
# The superheterodyne receiver

A radio must select one station out of many, amplify a microvolt signal by a
million, and demodulate it — across a wide tuning range. Doing all that at the
incoming (RF) frequency is hard, because a sharp, high-gain filter that *also*
re-tunes is impractical. The **superheterodyne** receiver, the standard since the
1930s, solves this by shifting *every* station down to one fixed **intermediate
frequency (IF)**, where filtering and gain are easy:

```mermaid
flowchart LR
  ANT["antenna"] --> RFA["RF amp + preselect filter"]
  RFA --> MIX["mixer ×"]
  LO["local oscillator (tunable): fLO = fRF + fIF"] --> MIX
  MIX --> IF["IF filter + amp (fixed fIF)"]
  IF --> DET["detector / demodulator"]
  DET --> AUD["audio amp"]
  AUD --> SPK["speaker"]
```

The trick is **mixing**: multiplying the RF by a local-oscillator (LO) tone
produces sum and difference frequencies. The **difference**,
$f_{\\mathrm{IF}} = |f_{\\mathrm{RF}} - f_{\\mathrm{LO}}|$, is the fixed IF. To tune
a different station you only re-tune the LO so the difference stays at the IF; the
expensive IF filter and IF amplifier never change.

Standard IF values: $455\\text{ kHz}$ for AM broadcast, $10.7\\text{ MHz}$ for FM.
Concentrating gain and selectivity at one frequency gives the receiver its
sensitivity (weak-signal reach) and selectivity (rejecting adjacent stations).

**Next:** the price of mixing — the image frequency.
""",
        ),
        _t(
            "Mixing, image frequency & IF",
            "11 min",
            """\
# Mixing, image frequency & IF

A **mixer** multiplies two signals; for inputs at $f_{\\mathrm{RF}}$ and
$f_{\\mathrm{LO}}$ the output contains the **sum** $f_{\\mathrm{RF}}+f_{\\mathrm{LO}}$
and **difference** $|f_{\\mathrm{RF}}-f_{\\mathrm{LO}}|$. The IF stage keeps the
difference and rejects the rest. But the difference relation has a sting: **two**
input frequencies map to the same IF.

If the LO is set so that $f_{\\mathrm{LO}} = f_{\\mathrm{RF}} + f_{\\mathrm{IF}}$,
then both the wanted $f_{\\mathrm{RF}}$ **and** the **image**

$$f_{\\mathrm{image}} = f_{\\mathrm{LO}} + f_{\\mathrm{IF}} = f_{\\mathrm{RF}} + 2f_{\\mathrm{IF}}$$

produce the same difference frequency and fall straight into the IF passband. A
strong station at the image would interfere with the one you want. Below, the
wanted signal and its image sit symmetrically about the LO, both $f_{\\mathrm{IF}}$
away:

```plot
{"title": "Image frequency: wanted and image straddle the LO, both at fIF offset", "xLabel": "frequency (MHz)", "yLabel": "level", "xRange": [98, 122], "yRange": [0, 1.1], "points": [{"x": 100, "y": 1, "label": "wanted fRF = 100", "color": "#2563eb", "size": 7}, {"x": 110.7, "y": 0.6, "label": "LO = 110.7", "color": "#16a34a", "size": 7}, {"x": 121.4, "y": 0.8, "label": "image = 121.4 (= fRF + 2·fIF)", "color": "#dc2626", "size": 7}]}
```

Two defences, both before the mixer:

- **RF preselector filter** — a band-pass at the front end that passes
  $f_{\\mathrm{RF}}$ but attenuates the image $2f_{\\mathrm{IF}}$ away.
- **Higher IF** — pushes the image *further* from the wanted signal, so the
  preselector has an easier job. (This fights the conflicting wish for a *low* IF
  where selectivity between adjacent channels is easiest — hence many receivers
  use **two** conversions: a high first IF for image rejection, a low second IF
  for selectivity.)

Choosing the IF is therefore a balance: **image rejection vs adjacent-channel
selectivity**. That trade defines superheterodyne design.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Analog Communications — Advanced ─────────────────────────────────────────

_AC_ADVANCED = SeedCourse(
    slug="analog-comms-advanced",
    title="Analog Communications — Advanced",
    description=(
        "Noise performance and the bridge to digital: SNR and threshold in AM, "
        "the FM noise advantage and capture effect, pre-emphasis/de-emphasis, "
        "then sampling, PAM, PCM and quantization, and finally multiplexing "
        "(FDM/TDM) in a full system case study. Interactive SNR and quantization "
        "plots with receiver block diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Noise in AM systems",
            "11 min",
            """\
# Noise in AM systems

Now we quantify how AM handles channel noise. Define the **channel
signal-to-noise ratio** as the received signal power over the noise in the
message bandwidth, $\\mathrm{SNR}_c = S_R / (N_0 B)$. The figure of merit is the
**output SNR** after demodulation, and the ratio
$\\mathrm{SNR}_o / \\mathrm{SNR}_c$ is the modulation's **detection gain**.

For **DSB-SC / SSB with coherent detection**, the math works out to detection
gain $= 1$ (DSB) — the scheme neither helps nor hurts. **Envelope-detected AM**
is worse, for two reasons: power wasted in the carrier, and a **threshold
effect**. At high SNR the envelope detector behaves linearly; but once noise
becomes comparable to the carrier, the recovered signal collapses abruptly rather
than degrading gracefully:

```plot
{"title": "AM threshold: output SNR collapses below ~10 dB input", "xLabel": "input SNR (dB)", "yLabel": "output SNR (dB)", "xRange": [0, 25], "yRange": [-5, 25], "functions": [{"expr": "x - 4.8", "label": "linear region (above threshold)", "color": "#2563eb"}, {"expr": "(x - 4.8) - 18*exp(-(x-2)*0.6)", "label": "actual (threshold knee near 10 dB)", "color": "#dc2626"}], "points": [{"x": 10, "y": 5.2, "label": "threshold", "color": "#16a34a", "size": 7}]}
```

Above threshold, output SNR tracks input linearly; below it, the curve falls off
a cliff. Broadcast AM lives comfortably above threshold for local stations but
suffers on weak distant signals — the familiar fade into hiss and crackle.

The lesson: AM's noise performance is, at best, no better than baseband, and its
envelope detector adds a threshold. To do *better* than baseband we need FM.

**Next:** why FM beats AM in noise.
""",
        ),
        _t(
            "Noise in FM systems & the FM advantage",
            "12 min",
            """\
# Noise in FM systems & the FM advantage

FM's wide bandwidth pays off in noise. Because information is in the *frequency*,
the FM demodulator (a discriminator) differentiates the phase — and
differentiation **suppresses low-frequency noise** while the constant-envelope
limiter strips amplitude noise entirely. The result is the **FM advantage**:
above threshold the output SNR is

$$\\mathrm{SNR}_o \\approx 3\\beta^2(\\beta+1)\\,\\mathrm{SNR}_c
\\;\\;\\propto\\;\\; \\beta^2\\,\\mathrm{SNR}_c.$$

Output SNR grows with the **square** of the modulation index $\\beta$ — spend more
bandwidth (larger $\\Delta f$, larger $\\beta$) and you buy a quadratic SNR gain.
This is FM's defining trade: **bandwidth for SNR**, exactly what AM cannot do.

```plot
{"title": "FM advantage: output SNR gain ≈ 10·log10(3·β²·(β+1)) over baseband", "xLabel": "modulation index β", "yLabel": "SNR gain (dB)", "xRange": [1, 8], "yRange": [0, 35], "functions": [{"expr": "10*log10(3*x^2*(x+1))", "label": "FM gain (dB) ∝ β² (above threshold)", "color": "#2563eb"}], "points": [{"x": 2, "y": 15.6, "label": "β=2", "color": "#94a3b8", "size": 6}, {"x": 5, "y": 26.5, "label": "β=5 (broadcast FM)", "color": "#dc2626", "size": 7}]}
```

But there is no free lunch: FM has its **own threshold**, and a sharper one. Below
about $10\\text{ dB}$ channel SNR the discriminator produces sudden **clicks** as
noise spikes overwhelm the carrier, and the advantage evaporates. There is also
the **capture effect**: when two FM signals share a channel, the stronger one is
demodulated and the weaker is almost entirely suppressed — why FM reception
"locks on" to the nearest station rather than mixing two like AM does.

**Next:** squeezing even more SNR with pre-emphasis.
""",
        ),
        _t(
            "Pre-emphasis & de-emphasis",
            "10 min",
            """\
# Pre-emphasis & de-emphasis

FM noise has a quirk: after the discriminator, the noise **power spectral density
rises with frequency** (a *parabolic*, $f^2$, noise spectrum). So the
high-frequency end of the message — where audio energy is naturally weakest —
suffers the worst SNR. Treble hiss.

The fix is a matched pair of filters:

- **Pre-emphasis** at the transmitter: boost the high frequencies of the message
  *before* modulating, with a high-pass-ish shelf (time constant $\\tau = 75\\,\\mu
  \\text{s}$ in the US, $50\\,\\mu\\text{s}$ in Europe).
- **De-emphasis** at the receiver: the exact inverse low-pass *after* detection,
  cutting the highs back down.

The message comes out flat — but the de-emphasis low-pass also attenuates the
high-frequency *noise*, which was never boosted. Net gain in high-frequency SNR
for free:

```plot
{"title": "Pre-emphasis boosts highs; de-emphasis (inverse) cuts noise there", "xLabel": "frequency (× corner)", "yLabel": "relative gain", "xRange": [0.1, 12], "yRange": [0, 3.5], "functions": [{"expr": "sqrt(1 + x*x)", "label": "pre-emphasis (TX boost)", "color": "#2563eb"}, {"expr": "1/sqrt(1 + x*x)", "label": "de-emphasis (RX cut)", "color": "#dc2626"}, {"expr": "1", "label": "net message response (flat)", "color": "#16a34a"}]}
```

The blue and red curves are reciprocals, so their product (green) is flat — the
*message* is unchanged — but noise added in the channel only meets the red cut,
gaining several dB of high-frequency SNR. Broadcast FM, vinyl records (RIAA), and
tape (Dolby) all use this same trick of shaping the signal to dodge where the
noise lives.

**Next:** crossing the bridge to digital — sampling.
""",
        ),
        _t(
            "Sampling & pulse-amplitude modulation",
            "11 min",
            """\
# Sampling & pulse-amplitude modulation

To digitize a signal we first **sample** it — measure its amplitude at regular
instants $T_s = 1/f_s$ apart. The **Nyquist sampling theorem** is the cornerstone:

$$f_s \\ge 2B,$$

a signal of bandwidth $B$ can be reconstructed *exactly* from samples taken at or
above twice $B$. Sample too slowly and high frequencies masquerade as low ones —
**aliasing** — irreversibly corrupting the signal (hence an **anti-alias filter**
before sampling). Below, the dots are samples of a tone; too few per cycle and the
eye is fooled into seeing a slower wave:

```plot
{"title": "Sampling a tone: enough samples per cycle to avoid aliasing", "xLabel": "time t", "yLabel": "amplitude", "xRange": [0, 6.28], "yRange": [-1.4, 1.4], "functions": [{"expr": "sin(3*x)", "label": "signal (3 cycles)", "color": "#2563eb"}], "points": [{"x": 0, "y": 0, "color": "#dc2626", "size": 6}, {"x": 0.785, "y": 0.924, "color": "#dc2626", "size": 6}, {"x": 1.571, "y": 0.707, "color": "#dc2626", "size": 6}, {"x": 2.356, "y": -0.383, "color": "#dc2626", "size": 6}, {"x": 3.14, "y": -0.99, "color": "#dc2626", "size": 6}, {"x": 3.927, "y": -0.131, "color": "#dc2626", "size": 6}, {"x": 4.712, "y": 0.895, "color": "#dc2626", "size": 6}, {"x": 5.498, "y": 0.546, "color": "#dc2626", "size": 6}]}
```

The samples themselves are the basis of **pulse-amplitude modulation (PAM)**: a
train of pulses whose *heights* equal the sample values. PAM is still analog (the
heights are continuous) but it is **discrete in time** — the crucial first step
that lets many signals share a channel by **interleaving** their pulses, and the
direct precursor to fully digital encoding.

```mermaid
flowchart LR
  ANALOG["analog m(t)"] --> AAF["anti-alias LPF (cut above fs/2)"]
  AAF --> SH["sample & hold @ fs ≥ 2B"]
  SH --> PAM["PAM pulse train (heights = samples)"]
```

**Next:** turn those heights into bits — PCM.
""",
        ),
        _t(
            "PCM & the analog-to-digital bridge",
            "11 min",
            """\
# PCM & the analog-to-digital bridge

PAM samples still take *continuous* heights. **Pulse-code modulation (PCM)**
finishes the job by **quantizing** each sample to one of $L = 2^n$ levels and
encoding that level as an $n$-bit codeword — the complete analog-to-digital
conversion behind CDs, digital telephony and everything downstream:

```mermaid
flowchart LR
  PAM["sampled values"] --> QNT["quantize to L = 2^n levels"]
  QNT --> ENC["encode to n-bit codewords"]
  ENC --> BITS["PCM bit stream"]
```

Quantizing introduces an unavoidable error — **quantization noise** — bounded by
half a step. Rounding a smooth curve to the nearest level produces the staircase
below; the gap between curve and staircase is the quantization error:

```plot
{"title": "Quantization: a smooth signal rounded to discrete levels", "xLabel": "time t", "yLabel": "amplitude", "xRange": [0, 6.28], "yRange": [-1.2, 1.2], "functions": [{"expr": "sin(x)", "label": "original m(t)", "color": "#2563eb"}, {"expr": "floor(sin(x)*4 + 0.5)/4", "label": "quantized (8 levels)", "color": "#dc2626"}]}
```

The headline result links bits to SNR. For a uniform quantizer the
signal-to-quantization-noise ratio is

$$\\mathrm{SNR}_q \\approx (6.02\\,n + 1.76)\\ \\text{dB},$$

the famous **"6 dB per bit"** rule: each extra bit roughly doubles the level count
and adds $\\approx 6\\text{ dB}$ of fidelity. So 8-bit telephony gives $\\approx
50\\text{ dB}$, 16-bit CD audio $\\approx 98\\text{ dB}$. PCM trades **bandwidth**
(more bits/sec) for **noise immunity** — and once a signal is bits, it can be
regenerated perfectly at each repeater, the decisive advantage that ended the
analog era.

**Next:** sharing the channel — multiplexing.
""",
        ),
        _t(
            "Multiplexing (FDM/TDM) & a system case study",
            "12 min",
            """\
# Multiplexing (FDM/TDM) & a system case study

A single channel usually carries **many** signals at once via **multiplexing**.
Two complementary schemes:

- **Frequency-division multiplexing (FDM)** — give each signal its own slice of
  the **spectrum**. Each message modulates a different carrier; they ride
  side-by-side and a bank of band-pass filters separates them at the far end.
  This *is* radio and TV broadcasting, and the FM stereo subcarrier.
- **Time-division multiplexing (TDM)** — give each signal its own slice of
  **time**. Sample several signals in turn and interleave their PAM/PCM samples
  into one fast stream; a synchronized switch sorts them out. The basis of digital
  telephony (the T1/E1 hierarchy).

FDM and TDM are duals — one partitions frequency, the other time — and both end in
a demultiplexer that recovers each user:

```mermaid
flowchart LR
  U1["user 1"] --> MUX["multiplexer (FDM: by freq / TDM: by time slot)"]
  U2["user 2"] --> MUX
  U3["user 3"] --> MUX
  MUX --> CH["shared channel"]
  CH --> DMX["demultiplexer"]
  DMX --> O1["user 1"]
  DMX --> O2["user 2"]
  DMX --> O3["user 3"]
```

**Case study — broadcast FM stereo.** It stacks everything we've covered. The
baseband is built by **FDM**: the L+R sum sits at audio ($0$–$15\\text{ kHz}$), a
$19\\text{ kHz}$ pilot tone marks the reference, and the L−R difference is
DSB-SC-modulated onto a $38\\text{ kHz}$ subcarrier above it. That composite signal
is **pre-emphasized**, then **frequency-modulated** ($\\Delta f = 75\\text{ kHz}$,
$B \\approx 180\\text{ kHz}$ by Carson's rule) onto the station's RF carrier. At the
receiver: a **superheterodyne** front end tunes the station and brings it to the
$10.7\\text{ MHz}$ **IF**, a **limiter + PLL discriminator** demodulates the FM,
**de-emphasis** flattens the audio and tames the highs, and finally the pilot,
sum and difference are de-multiplexed and combined to L and R.

```plot
{"title": "FM stereo composite baseband (FDM of mono, pilot, stereo subcarrier)", "xLabel": "frequency (kHz)", "yLabel": "level", "xRange": [0, 60], "yRange": [0, 1.1], "functions": [{"expr": "(x < 15)*1", "label": "L+R (mono)", "color": "#2563eb"}, {"expr": "(x > 22)*(x < 54)*0.7", "label": "L−R on 38 kHz subcarrier", "color": "#dc2626"}], "points": [{"x": 19, "y": 0.5, "label": "19 kHz pilot", "color": "#16a34a", "size": 7}, {"x": 38, "y": 0.85, "label": "38 kHz subcarrier", "color": "#dc2626", "size": 6}]}
```

That single chain — FDM, DSB-SC, pre-emphasis, FM, superheterodyne, PLL,
de-emphasis — is the whole course in one signal path.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


ANALOG_COMMS_COURSES: tuple[SeedCourse, ...] = (_AC_BASICS, _AC_INTERMEDIATE, _AC_ADVANCED)

__all__ = ["ANALOG_COMMS_COURSES"]
