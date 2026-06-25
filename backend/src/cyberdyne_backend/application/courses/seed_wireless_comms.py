"""Wireless & Mobile Communications track: Basics -> Intermediate -> Advanced.

From the radio channel, propagation and the cellular concept, through fading,
digital modulation, OFDM and equalization, to diversity, MIMO, massive MIMO,
LTE/4G and 5G NR. Lessons are `text` with LaTeX, interactive ```plot blocks
(path loss, Shannon capacity, BER) and ```mermaid system diagrams (cellular
reuse, OFDM transceiver, MIMO, handover). Builds on Signals/DSP and RF.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, μ, λ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Wireless & Mobile Communications — Basics ────────────────────────────────

_WC_BASICS = SeedCourse(
    slug="wireless-comms-basics",
    title="Wireless & Mobile Communications — Basics",
    description=(
        "How wireless works end to end: the radio channel and spectrum, how "
        "signals weaken with distance (path loss), the cellular concept that "
        "lets millions share the air, the link budget that decides whether a "
        "call connects, the 1G->5G story, and how users share the channel "
        "(FDMA/TDMA/CDMA/OFDMA). Interactive path-loss plots and cellular "
        "diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The wireless channel & spectrum",
            "10 min",
            """\
# The wireless channel & spectrum

Wireless communication sends information as **electromagnetic waves** through the
air rather than down a wire. The carrier is a sine wave at some **frequency** $f$;
its **wavelength** is

$$\\lambda = \\frac{c}{f}, \\qquad c \\approx 3\\times10^8\\ \\text{m/s}.$$

So 2.4 GHz Wi-Fi has $\\lambda \\approx 12.5$ cm, while a 600 MHz TV-band signal has
$\\lambda \\approx 50$ cm. Wavelength drives almost everything: antenna size,
diffraction around buildings, and how far a signal travels.

**The spectrum is the scarce resource.** Frequencies are split into bands and
licensed (cellular, broadcast) or unlicensed (Wi-Fi, Bluetooth). Rough trade-off:

- **Low bands** (sub-1 GHz): travel far, penetrate walls, but little bandwidth → low data rate.
- **Mid bands** (1–6 GHz): the cellular/Wi-Fi workhorse, a balance of range and capacity.
- **High bands** (mmWave, 24–100 GHz): huge bandwidth → fast, but short range and blocked by walls.

The channel is **shared and hostile**: many users, interference, noise, and a
signal that fades as it travels. The rest of this course is about taming it.

**Next:** exactly how fast a signal weakens with distance.
""",
        ),
        _t(
            "Radio propagation & path loss",
            "11 min",
            """\
# Radio propagation & path loss

A radio signal gets weaker as it spreads out. In **free space** the received
power falls with the **square of distance**:

$$P_r = P_t\\, G_t G_r \\left(\\frac{\\lambda}{4\\pi d}\\right)^2,$$

the **Friis equation**. Doubling the distance cuts power to a quarter (−6 dB).
In the real world — ground reflections, buildings, foliage — power falls even
faster, modelled as $P_r \\propto d^{-n}$ with a **path-loss exponent** $n$:

- $n = 2$: free space / line of sight.
- $n \\approx 3$–$4$: urban and indoor environments.

The plot below shows received power (relative, linear scale) versus distance for
a few exponents — the higher $n$, the steeper the cliff:

```plot
{"title": "Received power vs distance (relative)", "xLabel": "distance d", "yLabel": "relative received power", "xRange": [1, 10], "yRange": [0, 1.05], "functions": [{"expr": "1/x^2", "label": "n = 2 (free space)", "color": "#2563eb"}, {"expr": "1/x^3", "label": "n = 3 (urban)", "color": "#16a34a"}, {"expr": "1/x^4", "label": "n = 4 (dense urban)", "color": "#dc2626"}]}
```

Engineers work in **decibels** because the numbers span huge ranges: path loss
of 120 dB means the received power is $10^{12}$ times weaker than transmitted.
Adding gains and subtracting losses in dB turns multiplication into addition —
which is exactly the link budget we build two lessons from now.

**Next:** the idea that lets millions of users share the same spectrum.
""",
        ),
        _t(
            "The cellular concept",
            "11 min",
            """\
# The cellular concept

Spectrum is scarce, so we cannot give every user their own frequency. The
**cellular** idea splits the coverage area into **cells**, each served by a base
station, and **reuses** the same frequencies in cells far enough apart that they
do not interfere. A group of cells using all the channels once is a **cluster**
of size $N$ (typical $N = 3, 4, 7$); the spectrum is reused every cluster.

```mermaid
flowchart TB
  subgraph Cluster["frequency-reuse cluster (N = 7)"]
    C1["cell f1"]
    C2["cell f2"]
    C3["cell f3"]
    C4["cell f4"]
    C5["cell f5"]
    C6["cell f6"]
    C7["cell f7"]
  end
  Cluster --> R1["repeat cluster: f1 reused here"]
  Cluster --> R2["repeat cluster: f1 reused here"]
```

Smaller cells → more reuse → more total capacity, which is why dense cities use
tiny cells (microcells, femtocells). Halving the cell radius roughly *quadruples*
the number of cells in an area, so total capacity climbs steeply as cells shrink:

```plot
{"title": "Smaller cells → many more cells per area → more capacity", "xLabel": "cell radius (relative)", "yLabel": "cells per unit area (∝ capacity)", "xRange": [0.4, 4], "yRange": [0, 7], "functions": [{"expr": "1/x^2", "label": "cells per area ∝ 1/radius²", "color": "#2563eb"}], "points": [{"x": 1, "y": 1, "label": "baseline cell", "color": "#dc2626", "size": 6}, {"x": 0.5, "y": 4, "label": "half radius → 4× cells", "color": "#16a34a", "size": 6}]}
```

The cost is **co-channel interference** from distant cells reusing your
frequency, controlled by the **reuse distance**.

As a user moves out of one cell and into another, the network performs a
**handover** (handoff): it transfers the active call to the new base station
before the old link dies.

```mermaid
flowchart LR
  MS["mobile moving →"] --> BS1["base station A (signal weakening)"]
  MS --> BS2["base station B (signal rising)"]
  BS1 --> MSC["mobile switching centre: trigger handover"]
  BS2 --> MSC
  MSC --> H["call seamlessly moved A → B"]
```

Cells, reuse and handover together are what make a *mobile* network mobile.

**Next:** the budget that decides whether the link closes at all.
""",
        ),
        _t(
            "Link budget & receiver sensitivity",
            "11 min",
            """\
# Link budget & receiver sensitivity

A **link budget** adds up every gain and loss between transmitter and receiver
to check the signal arrives strong enough to be decoded. In decibels it is just
addition:

$$P_r = P_t + G_t + G_r - L_{\\text{path}} - L_{\\text{other}}\\ \\ [\\text{dBm}].$$

The link **closes** if the received power exceeds the **receiver sensitivity** —
the weakest signal the receiver can decode at the required quality — plus a
**fade margin** for the bad moments.

Receiver sensitivity is set by **noise**. The noise floor is

$$N = kTB + \\text{NF},$$

so wider bandwidth $B$ and a worse **noise figure** (NF) raise the floor and make
the receiver less sensitive. What ultimately matters is the **signal-to-noise
ratio** $\\text{SNR} = P_r - N$, because — via Shannon — SNR caps the data rate:

```plot
{"title": "Shannon capacity: diminishing returns with SNR", "xLabel": "SNR (linear)", "yLabel": "capacity (bits/s per Hz, approx)", "xRange": [0, 100], "yRange": [0, 7], "functions": [{"expr": "0.66*sqrt(x)", "label": "C ≈ log2(1 + SNR) shape", "color": "#2563eb"}], "points": [{"x": 1, "y": 1, "label": "SNR = 1 → 1 bit/Hz", "color": "#dc2626", "size": 6}]}
```

(The axis is linear and `log` is unavailable, so the curve above uses a concave
$\\sqrt{\\cdot}$ proxy with the same diminishing-returns *shape* as the true
$\\log_2(1+\\text{SNR})$.)

The key engineering lever: every extra dB of margin costs power, antenna size or
range. Designing a system is balancing that budget.

**Next:** how the generations of cellular spent that budget differently.
""",
        ),
        _t(
            "From 1G to 5G: the cellular generations",
            "10 min",
            """\
# From 1G to 5G: the cellular generations

Cellular has reinvented itself roughly every decade. The throughline is a march
from **analog voice** to **all-IP broadband** and beyond.

- **1G (1980s)** — *analog*. FM voice, FDMA. No security, no data, easily cloned.
- **2G (1990s)** — *digital voice*. GSM (TDMA) and IS-95 (CDMA). Digital meant
  encryption, error correction, SMS and a tiny data pipe (GPRS/EDGE).
- **3G (2000s)** — *mobile data*. UMTS/CDMA2000 brought real internet to phones,
  measured in Mbps.
- **4G / LTE (2010s)** — *all-IP broadband*. OFDMA, MIMO; voice itself became
  data (VoLTE). Tens to hundreds of Mbps.
- **5G NR (2020s)** — *flexible & fast*. mmWave + massive MIMO, network slicing,
  ultra-low latency; aims at Gbps peaks and machine-to-machine (IoT) at scale.

The deeper pattern is the move from **analog** (the waveform *is* the message,
vulnerable to noise) to **digital** (the message is bits, protected by coding and
recoverable from a noisy waveform). Every later lesson — modulation, OFDM, MIMO —
is a tool that made the higher generations possible.

**Next:** the schemes that let many users share one channel.
""",
        ),
        _t(
            "Multiple access: FDMA, TDMA, CDMA, OFDMA",
            "11 min",
            """\
# Multiple access: FDMA, TDMA, CDMA, OFDMA

How do many users share one channel without clobbering each other? Each
generation answered differently by dividing a different **resource**:

- **FDMA** (frequency) — give each user their own **frequency** slice. Simple
  (1G), but slices sit idle when a user is quiet.
- **TDMA** (time) — everyone shares a frequency but takes turns in **time slots**
  (2G GSM). Bursty, needs tight timing.
- **CDMA** (code) — everyone transmits at once on the same frequency, separated by
  orthogonal **spreading codes** (2G IS-95, 3G). Robust, soft capacity limit.
- **OFDMA** (frequency + time) — split the band into many narrow **subcarriers**
  and assign each user a block of subcarriers *and* time (4G/5G). Flexible and
  spectrally efficient — the modern winner.

```mermaid
flowchart TB
  R["one shared channel"] --> F["FDMA: split by FREQUENCY"]
  R --> T["TDMA: split by TIME slot"]
  R --> C["CDMA: split by CODE (all share freq+time)"]
  R --> O["OFDMA: split by subcarrier blocks (freq + time)"]
```

The trend is from rigid single-axis division (FDMA) toward **two-dimensional,
schedulable** resources (OFDMA), which lets the network hand each user exactly
the slice they need, when they need it.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Wireless & Mobile Communications — Intermediate ──────────────────────────

_WC_INTERMEDIATE = SeedCourse(
    slug="wireless-comms-intermediate",
    title="Wireless & Mobile Communications — Intermediate",
    description=(
        "Why wireless links wobble and how we fight back: large- vs small-scale "
        "fading, multipath and delay spread, Rayleigh/Rician statistics, digital "
        "modulation (PSK/QAM) and BER, and OFDM with its cyclic prefix and "
        "equalization against intersymbol interference. With fading-envelope, "
        "BER and OFDM diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Large-scale vs small-scale fading",
            "11 min",
            """\
# Large-scale vs small-scale fading

A received signal's strength varies on **two scales** at once.

- **Large-scale fading** — the slow trend as you move tens or hundreds of metres:
  average path loss plus **shadowing** (buildings, hills) that adds a slow,
  log-normal wobble. This sets *coverage*.
- **Small-scale fading** — fast, deep dips over fractions of a wavelength, caused
  by **multipath** waves adding constructively or destructively. This sets
  *link reliability* moment to moment.

The plot sketches received power versus position: a smooth large-scale trend with
fast small-scale ripples riding on it:

```plot
{"title": "Two scales of fading vs position", "xLabel": "distance (wavelengths)", "yLabel": "relative power", "xRange": [0, 12], "yRange": [0, 1.4], "functions": [{"expr": "exp(-x/10)", "label": "large-scale trend", "color": "#94a3b8"}, {"expr": "exp(-x/10)*(0.75 + 0.45*sin(6*x)*cos(2.3*x))", "label": "with small-scale fading", "color": "#2563eb"}]}
```

A receiver might sit in a fade so deep the link drops even though the *average*
power is fine — which is exactly why we later add **diversity**. Distinguishing
the two scales lets engineers attack each with the right tool: more transmit
power and better siting for large-scale, diversity and coding for small-scale.

**Next:** the mechanism behind small-scale fading — multipath.
""",
        ),
        _t(
            "Multipath & delay spread",
            "11 min",
            """\
# Multipath & delay spread

In any real environment a transmitted pulse reaches the receiver by **many
paths** — direct, plus reflections off buildings, ground and vehicles. Each
copy arrives at a slightly different time and amplitude. The spread between the
first and last meaningful arrival is the **delay spread** $\\tau$.

Delay spread matters because it smears symbols into each other:

- If the symbol period $T_s$ is **much longer** than $\\tau$, copies overlap
  harmlessly — the channel is **flat**.
- If $T_s$ is **comparable to or shorter** than $\\tau$, a symbol's echoes land on
  top of the *next* symbol → **intersymbol interference (ISI)**, the central enemy
  of high-rate wireless.

The matching frequency-domain quantity is the **coherence bandwidth**
$B_c \\approx \\frac{1}{\\tau}$: frequencies closer than $B_c$ fade together
(**flat fading**), while a signal wider than $B_c$ sees different fading across
its band (**frequency-selective fading**).

```mermaid
flowchart LR
  TX["transmitter"] -->|direct, 0 µs| RX["receiver"]
  TX -->|reflection 1, +1 µs| RX
  TX -->|reflection 2, +3 µs| RX
  RX --> DS["delay spread τ ≈ 3 µs → ISI if Ts < τ"]
```

The faster you want to go (shorter $T_s$), the worse ISI gets — motivating OFDM,
which sidesteps it by using *many slow* symbols at once.

**Next:** the statistics of those fading dips.
""",
        ),
        _t(
            "Rayleigh & Rician fading",
            "11 min",
            """\
# Rayleigh & Rician fading

When many multipath components add up with random phases, the envelope of the
received signal becomes a **random variable** with a characteristic distribution.

- **Rayleigh fading** — *no* dominant path (e.g. a non-line-of-sight city
  street). The envelope $r$ follows the **Rayleigh distribution**

  $$p(r) = \\frac{r}{\\sigma^2}\\,e^{-r^2/(2\\sigma^2)},\\qquad r \\ge 0.$$

  Deep fades are common, which is brutal for reliability.
- **Rician fading** — a *strong* line-of-sight path plus scatter. Parametrised by
  the **K-factor** (ratio of LOS power to scattered power); large $K$ → fades are
  shallow and the link behaves almost like free space, small $K$ → it degrades
  toward Rayleigh.

The plot shows the Rayleigh envelope density — note the long tail of low values
(the dangerous deep fades):

```plot
{"title": "Rayleigh fading envelope density", "xLabel": "envelope r", "yLabel": "probability density", "xRange": [0, 5], "yRange": [0, 0.7], "functions": [{"expr": "x*exp(-x^2/2)", "label": "Rayleigh (σ = 1)", "color": "#2563eb"}, {"expr": "(x/2.25)*exp(-x^2/4.5)", "label": "Rayleigh (σ = 1.5)", "color": "#16a34a"}]}
```

These models tell us how *often* the link is in a fade, which drives the **fade
margin** in the link budget and the case for diversity. Mobility also adds the
**Doppler shift** $f_d = \\frac{v}{\\lambda}$, which sets how *fast* the fading
changes.

**Next:** how we actually put bits on the carrier.
""",
        ),
        _t(
            "Digital modulation & BER: PSK and QAM",
            "12 min",
            """\
# Digital modulation & BER: PSK and QAM

To send bits we vary the carrier. The two workhorses:

- **PSK** (phase-shift keying) — encode bits in the carrier's **phase**. BPSK = 2
  phases (1 bit/symbol), QPSK = 4 phases (2 bits/symbol).
- **QAM** (quadrature amplitude modulation) — vary **amplitude *and* phase**,
  packing more bits per symbol: 16-QAM = 4 bits, 64-QAM = 6 bits, 256-QAM = 8 bits.

A **constellation diagram** plots the allowed symbols as points in the I/Q plane.
The catch: the more points you cram in, the closer they sit, so noise more easily
pushes a received point into a neighbour's region → a **bit error**.

We measure this with the **bit error rate (BER)** versus $E_b/N_0$ (energy per bit
over noise). BER falls steeply as SNR rises, and denser constellations need *more*
SNR for the same BER:

```plot
{"title": "BER falls as SNR rises (denser modulation needs more SNR)", "xLabel": "Eb/N0 (linear)", "yLabel": "bit error rate (relative)", "xRange": [0.2, 10], "yRange": [0, 0.55], "functions": [{"expr": "0.5*exp(-x)", "label": "BPSK/QPSK (robust)", "color": "#16a34a"}, {"expr": "0.5*exp(-x/4)", "label": "16-QAM (denser)", "color": "#dc2626"}]}
```

This is the core trade-off of **adaptive modulation** in LTE/5G: when SNR is high,
use 256-QAM for speed; when it drops, fall back to QPSK to stay connected. The
modulation is chosen per user, per moment, from the measured channel.

**Next:** the technique that made wideband wireless practical — OFDM.
""",
        ),
        _t(
            "OFDM: why & how",
            "12 min",
            """\
# OFDM: why & how

A single fast data stream suffers badly from ISI (recall delay spread). **OFDM**
(orthogonal frequency-division multiplexing) flips the problem: instead of one
fast carrier, send **hundreds of slow subcarriers** in parallel. Each subcarrier
carries a low-rate stream, so each symbol is *long* compared to the delay spread —
and the channel looks **flat** on each narrow subcarrier.

Two ideas make it work:

1. **Orthogonality.** The subcarriers are spaced so each one's peak sits on the
   others' nulls; they overlap in frequency yet do not interfere. The whole
   transform is computed cheaply with an **IFFT/FFT**.
2. **Cyclic prefix (CP).** A copy of the symbol's tail is pasted to its front as
   a guard interval. As long as the delay spread is shorter than the CP, all the
   echoes land within the guard and ISI is **completely absorbed** — and the
   channel becomes a simple per-subcarrier multiply, trivial to equalize.

```mermaid
flowchart LR
  BITS["bit stream"] --> MAP["QAM mapper"]
  MAP --> SP["serial → parallel"]
  SP --> IFFT["IFFT (build subcarriers)"]
  IFFT --> CP["add cyclic prefix"]
  CP --> CH["channel (multipath)"]
  CH --> RCP["remove cyclic prefix"]
  RCP --> FFT["FFT"]
  FFT --> EQ["1-tap equalizer / subcarrier"]
  EQ --> DET["QAM detector → bits"]
```

OFDM (and its multi-user form OFDMA) underpins Wi-Fi, LTE and 5G. The price is
sensitivity to frequency offset and a high **peak-to-average power ratio**, which
later systems manage carefully.

**Next:** what to do when ISI does leak through — equalization.
""",
        ),
        _t(
            "Equalization & the ISI problem",
            "11 min",
            """\
# Equalization & the ISI problem

When you *don't* use OFDM (or the delay spread exceeds the cyclic prefix),
intersymbol interference smears symbols together and the receiver must **undo**
the channel. That job is **equalization**.

The channel acts like a filter $H(f)$ that distorts the signal. An equalizer
applies an inverse-like response $\\approx \\frac{1}{H(f)}$ to flatten it:

- **Zero-forcing (ZF)** — invert $H(f)$ exactly. Perfect in principle, but where
  the channel has a deep null, $1/H$ blows up and **amplifies noise**.
- **MMSE** — minimise mean-squared error, balancing ISI removal against noise
  enhancement. The practical default.
- **Decision-feedback (DFE)** — subtract the ISI contribution of already-decided
  symbols; powerful but can propagate errors.
- **Adaptive equalizers** track a *changing* channel using **training/pilot**
  symbols the transmitter inserts on a known schedule.

In OFDM the equalizer collapses to a single complex multiply per subcarrier —
which is the whole reason OFDM is so attractive: it turns a hard time-domain
deconvolution into trivial per-tone division.

The fundamental tension is always the same: **remove ISI without blowing up
noise**. That balance, and how it scales with channel conditions, is what
separates a link that just works from one that drops.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Wireless & Mobile Communications — Advanced ──────────────────────────────

_WC_ADVANCED = SeedCourse(
    slug="wireless-comms-advanced",
    title="Wireless & Mobile Communications — Advanced",
    description=(
        "The techniques behind modern mobile capacity: diversity and combining, "
        "MIMO and spatial multiplexing, massive MIMO and beamforming, LTE/4G "
        "architecture and resource blocks, 5G NR (numerology, mmWave, slicing), "
        "and a worked link-budget/throughput case study. With MIMO and capacity "
        "plots and architecture diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Diversity & combining",
            "12 min",
            """\
# Diversity & combining

Small-scale fading causes deep, random dips — but a dip is **localised**. If we
send the same information over *independent* channels, it's unlikely they all fade
at once. That is **diversity**, and it's the single most effective weapon against
fading.

Three axes of diversity:

- **Time diversity** — repeat / interleave + coding across time, so a burst fade
  hits only part of a codeword.
- **Frequency diversity** — spread the signal across frequencies wider than the
  coherence bandwidth (spread spectrum, OFDM with coding).
- **Space diversity** — multiple antennas separated by more than $\\lambda/2$, so
  each sees a different fade. The cheapest and most common.

The receiver then **combines** the copies:

- **Selection combining** — just pick the strongest branch.
- **Maximal-ratio combining (MRC)** — weight each branch by its SNR and sum;
  optimal, and the combined SNR is the *sum* of branch SNRs.

The payoff is a steep BER improvement: each extra independent branch raises the
**diversity order** and bends the BER-vs-SNR curve sharply downward.

```plot
{"title": "Diversity bends BER down: more branches, steeper fall", "xLabel": "SNR (linear)", "yLabel": "bit error rate (relative)", "xRange": [0.3, 10], "yRange": [0, 0.55], "functions": [{"expr": "0.5/x", "label": "no diversity (1 antenna)", "color": "#dc2626"}, {"expr": "0.5/x^2", "label": "2-branch diversity", "color": "#16a34a"}, {"expr": "0.5/x^3", "label": "3-branch diversity", "color": "#2563eb"}]}
```

Diversity is also the conceptual bridge to MIMO: once you have several antennas,
you can do far more than just fight fading.

**Next:** turning multiple antennas into multiple parallel pipes.
""",
        ),
        _t(
            "MIMO & spatial multiplexing",
            "12 min",
            """\
# MIMO & spatial multiplexing

**MIMO** (multiple-input multiple-output) uses $N_t$ transmit and $N_r$ receive
antennas. Diversity uses the extra antennas for *reliability*; **spatial
multiplexing** uses them for *throughput* — sending **independent data streams**
over the same time and frequency.

The trick: in a rich-scattering channel the $N_t \\times N_r$ paths form a matrix
$\\mathbf{H}$ that is **invertible**, so the receiver can untangle the streams by
solving a linear system. The number of simultaneous streams is the channel's
**rank**, up to $\\min(N_t, N_r)$. Capacity grows roughly **linearly** with that
minimum — for free, without more bandwidth or power:

$$C \\approx \\min(N_t, N_r)\\,\\log_2(1 + \\text{SNR}).$$

```plot
{"title": "MIMO capacity scales with the number of streams", "xLabel": "SNR (linear)", "yLabel": "capacity (bits/s per Hz, approx)", "xRange": [0, 60], "yRange": [0, 24], "functions": [{"expr": "0.77*sqrt(x)", "label": "1×1 SISO", "color": "#94a3b8"}, {"expr": "2*0.77*sqrt(x)", "label": "2×2 MIMO", "color": "#16a34a"}, {"expr": "4*0.77*sqrt(x)", "label": "4×4 MIMO", "color": "#2563eb"}]}
```

(Each curve shares the concave per-stream capacity shape — a $\\sqrt{\\cdot}$ proxy
for $\\log_2(1+\\text{SNR})$ on this linear axis — scaled by the stream count to
show capacity growing *linearly* with $\\min(N_t,N_r)$.)

```mermaid
flowchart LR
  D["2 data streams"] --> TX["Tx: 2 antennas"]
  TX -->|H: 2×2 matrix| RX["Rx: 2 antennas"]
  RX --> DEC["solve H⁻¹ → separate streams"]
  DEC --> OUT["2 streams recovered"]
```

The diversity–multiplexing trade-off says you can spend antennas on robustness or
rate (or a mix). MIMO is why a 4×4 LTE link can quadruple throughput in good
conditions — and the foundation for what comes next.

**Next:** scaling MIMO up by an order of magnitude.
""",
        ),
        _t(
            "Massive MIMO & beamforming",
            "12 min",
            """\
# Massive MIMO & beamforming

**Massive MIMO** takes MIMO to the extreme: a base station with **tens to
hundreds** of antennas. With so many elements, two things become possible.

**Beamforming.** By adjusting the **phase** of the signal at each antenna, the
array makes the wavefronts add up constructively toward one user and cancel
elsewhere — steering a focused **beam** instead of broadcasting everywhere. This
raises the target's SNR and slashes interference to others. The narrower beam also
recovers the range lost at high frequencies, which is why beamforming is essential
for mmWave.

```mermaid
flowchart LR
  subgraph Array["antenna array (phase-steered)"]
    A1["el 1: φ1"]
    A2["el 2: φ2"]
    A3["el 3: φ3"]
    A4["el N: φN"]
  end
  A1 --> B["constructive sum → focused beam"]
  A2 --> B
  A3 --> B
  A4 --> B
  B --> U["user (high SNR)"]
  B -.->|nulls| I["other users (low interference)"]
```

**Spatial multiplexing of many users (MU-MIMO).** With far more antennas than
served users, the base station gives each user their own beam and serves dozens
simultaneously on the same time/frequency — a huge capacity multiplier.

Massive MIMO leans on **channel reciprocity** in TDD (uplink and downlink share
the band) to estimate the downlink channel from uplink pilots, avoiding crippling
feedback overhead. It is the headline capacity technology of 5G.

**Next:** the architecture that ties a 4G network together.
""",
        ),
        _t(
            "LTE/4G architecture & resource blocks",
            "11 min",
            """\
# LTE/4G architecture & resource blocks

**LTE** is an all-IP, OFDMA network. Its architecture splits cleanly into radio
and core:

- **E-UTRAN** (radio) — the **eNodeB** base stations, which handle radio,
  scheduling and handover and talk to each other directly over the **X2**
  interface.
- **EPC** (Evolved Packet Core) — the **MME** (mobility/signalling), **S-GW** and
  **P-GW** (user-data routing to the internet), and **HSS** (subscriber database).

```mermaid
flowchart LR
  UE["UE (phone)"] -->|radio| ENB["eNodeB"]
  ENB -->|S1-MME| MME["MME (signalling/mobility)"]
  ENB -->|S1-U| SGW["Serving Gateway"]
  SGW --> PGW["PDN Gateway"]
  PGW --> NET["internet / IP networks"]
  MME --> HSS["HSS (subscriber DB)"]
  ENB -.->|X2| ENB2["neighbour eNodeB"]
```

On the air, LTE schedules the **OFDMA** grid in **resource blocks (RBs)**: a RB is
**12 subcarriers** (15 kHz each → 180 kHz) over a **0.5 ms** slot. The scheduler
hands each user a set of RBs every millisecond based on their channel quality
(reported as CQI) — fast, fine-grained, opportunistic sharing in both frequency
and time. Wider channels simply have more RBs (a 20 MHz channel ≈ 100 RBs).

This RB grid plus per-user adaptive modulation and MIMO is what delivers LTE's
flexible, high throughput. 5G keeps the structure but makes it configurable.

**Next:** how 5G NR generalises all of this.
""",
        ),
        _t(
            "5G NR: numerology, mmWave & slicing",
            "12 min",
            """\
# 5G NR: numerology, mmWave & slicing

**5G New Radio (NR)** keeps OFDMA but makes it **flexible** to serve wildly
different needs — broadband, ultra-reliable low-latency control, and massive IoT.

**Numerology.** LTE fixed subcarrier spacing at 15 kHz; NR allows **scalable
spacing** $\\Delta f = 15 \\times 2^{\\mu}$ kHz ($\\mu = 0,1,2,\\dots$ → 15, 30, 60,
120 kHz). Wider spacing → shorter symbols → lower latency and robustness to the
big Doppler/phase noise at high frequencies. The network picks the numerology to
fit the band and service.

**mmWave.** NR adds bands at **24–100 GHz** with enormous bandwidth (hundreds of
MHz) for multi-Gbps speeds. The cost is severe path loss and blockage, so mmWave
*requires* beamforming and dense small cells — the techniques from earlier
lessons all converge here.

**Network slicing.** A single physical 5G network is partitioned into multiple
**virtual networks**, each tuned to a use case:

```mermaid
flowchart TB
  PHY["one physical 5G network"] --> EMBB["eMBB slice: high throughput (video)"]
  PHY --> URLLC["URLLC slice: ultra-low latency (control, vehicles)"]
  PHY --> MMTC["mMTC slice: massive IoT (sensors)"]
```

Slicing is enabled by a **cloud-native, service-based core** (SBA) where network
functions are software that can be scaled and placed flexibly (including at the
edge). 5G is thus as much a *software* leap as a radio one.

**Next:** put the whole stack together in a worked example.
""",
        ),
        _t(
            "Case study: link budget & throughput",
            "12 min",
            """\
# Case study: link budget & throughput

Let's size a downlink end to end, reusing everything in the track.

**1. Link budget (does the link close?).** A base station at $P_t = 46$ dBm with
$G_t = 15$ dBi serves a user with $G_r = 0$ dBi. Path loss at the cell edge is
$L = 130$ dB. Received power:

$$P_r = 46 + 15 + 0 - 130 = -69\\ \\text{dBm}.$$

Noise floor over $B = 20$ MHz: $N = -174 + 10\\log_{10}(20\\times10^6) + \\text{NF}(7)
\\approx -94\\ \\text{dBm}$. So

$$\\text{SNR} = P_r - N \\approx -69 - (-94) = 25\\ \\text{dB} \\;(\\approx 316\\ \\text{linear}).$$

Plenty of margin — the link closes comfortably.

**2. Throughput (how fast?).** Shannon caps it at
$C = B\\log_2(1+\\text{SNR}) \\approx 20\\text{e}6 \\times \\log_2(317) \\approx 166$
Mbps per stream. Real systems hit a fraction of Shannon, but the **levers** are
clear:

```plot
{"title": "Throughput levers: capacity vs SNR, scaled by MIMO streams", "xLabel": "SNR (linear)", "yLabel": "capacity (bits/s per Hz, approx)", "xRange": [0, 320], "yRange": [0, 30], "functions": [{"expr": "0.42*sqrt(x)", "label": "1 stream", "color": "#94a3b8"}, {"expr": "2*0.42*sqrt(x)", "label": "2 MIMO streams", "color": "#16a34a"}, {"expr": "4*0.42*sqrt(x)", "label": "4 MIMO streams", "color": "#2563eb"}]}
```

**Putting it together:** raising SNR (more power, beamforming, closer cells) only
buys you a *logarithmic* gain, but adding **MIMO streams** multiplies capacity
linearly, and adding **bandwidth** (mmWave) multiplies it directly. That is why
5G chases all three — massive MIMO, beamforming and wide mmWave channels — rather
than just turning up the power. A wireless engineer's job is balancing this budget
against range, interference and cost.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


WIRELESS_COMMS_COURSES: tuple[SeedCourse, ...] = (_WC_BASICS, _WC_INTERMEDIATE, _WC_ADVANCED)

__all__ = ["WIRELESS_COMMS_COURSES"]
