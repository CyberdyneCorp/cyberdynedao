"""Curated Digital Communications & Coding Theory track: Basics, Intermediate,
Advanced.

A complete digital comms curriculum: the end-to-end communication system
(sampling, quantization, PCM, baseband signaling, pulse shaping, digital
modulation, the AWGN channel and detection), modulation and information theory
(M-ary/QAM, BER vs SNR, entropy and Shannon capacity, source coding, channel
impairments), and coding/OFDM/MIMO (block and cyclic codes, convolutional codes
and Viterbi, turbo/LDPC/polar, OFDM, MIMO, and the throughline across 5G, Wi-Fi
and satellite). Dual MATLAB + Python focus throughout, with runnable Python
labs (numpy + matplotlib), interactive ```plot blocks, Mermaid diagrams, LaTeX
formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Digital Communications & Coding Theory -- Basics --------------------------

_DIGITAL_COMMS_BASICS = SeedCourse(
    slug="digital-comms-basics",
    title="Digital Communications & Coding Theory -- Basics",
    description=(
        "The digital communication system end to end: source/encoder/modulator/"
        "channel, sampling, quantization and PCM, baseband signaling and pulse "
        "shaping, digital modulation (ASK/FSK/PSK), and the AWGN channel with "
        "matched-filter detection -- dual MATLAB/Python, interactive plots, and a "
        "runnable constellation/eye/BER lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The digital communication system",
            "10 min",
            """\
# The digital communication system

Every text, call, photo and stream travels the same pipeline: a **source** of
bits, encoded for protection, modulated onto a waveform, sent through a noisy
**channel**, and reconstructed at the far end. Digital communications is the art
of moving bits **reliably** and **efficiently** across an imperfect channel.

## The block diagram

```mermaid
flowchart LR
  SRC["source (bits)"] --> SC["source coder (compress)"]
  SC --> CC["channel coder (add redundancy)"]
  CC --> MOD["modulator"]
  MOD --> CH["channel (noise, fading)"]
  CH --> DEM["demodulator / detector"]
  DEM --> CD["channel decoder (correct errors)"]
  CD --> SD["source decoder (decompress)"]
  SD --> SINK["sink"]
```

Each block fights one enemy:

| Block | Job | Real example |
|-------|-----|--------------|
| Source coder | remove redundancy (compress) | JPEG, MP3, H.264 |
| Channel coder | add structured redundancy | LDPC in 5G, Reed-Solomon on a CD |
| Modulator | map bits to a transmittable waveform | QAM in Wi-Fi, QPSK on GPS |
| Channel | the physical medium | air, copper, fiber, deep space |
| Detector | decide which symbol was sent | the matched filter |

## Two figures of merit

Everything trades off between two numbers:

$$\\eta_{bw} = \\frac{R_b}{B} \\;\\left[\\frac{\\text{bits/s}}{\\text{Hz}}\\right], \\qquad
\\frac{E_b}{N_0} \\;[\\text{energy per bit over noise density}].$$

**Bandwidth efficiency** $\\eta_{bw}$ says how many bits per second you pack into
each hertz; **$E_b/N_0$** says how much energy each bit needs to survive the
noise. The whole field is pushing both as far as physics allows.

## Same idea, two languages

```matlab
Rb = 1e6;        % 1 Mbit/s
B  = 500e3;      % 500 kHz
eta = Rb / B;    % 2 bits/s/Hz
```

```python
Rb = 1e6         # 1 Mbit/s
B = 500e3        # 500 kHz
eta = Rb / B     # 2 bits/s/Hz
```

**Next:** turning a real-world analog signal into bits -- sampling and PCM.
""",
        ),
        _t(
            "Sampling, quantization & PCM",
            "11 min",
            """\
# Sampling, quantization & PCM

A microphone, a camera sensor, a temperature probe -- all produce **analog**
signals. To send them digitally we run an **ADC**: sample in time, then quantize
in amplitude.

## Sampling: the Nyquist rate

Sample a signal of bandwidth $B$ at rate $f_s$. The **Nyquist-Shannon** theorem
says you recover it perfectly only if

$$f_s \\geq 2B.$$

Sample too slowly and high frequencies fold down to masquerade as low ones --
**aliasing**. Slide the sampling rate and watch a fast tone alias into a slow
imposter once you drop below the Nyquist rate:

```plot
{"title": "Aliasing: a 5 Hz tone seen through a sampler (slide fs)", "xLabel": "time (s)", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "fs", "range": [4, 40], "value": 8, "label": "sample rate fs (Hz)"}], "functions": [{"expr": "sin(2*pi*5*x)", "label": "true 5 Hz tone", "color": "#94a3b8"}, {"expr": "sin(2*pi*5*round(x*fs)/fs)", "label": "reconstructed from samples", "color": "#dc2626"}]}
```

This is why telephone audio is sampled at 8 kHz (it carries 0-4 kHz speech) and
CD audio at 44.1 kHz (above $2 \\times 20$ kHz hearing).

## Quantization: bits cost SNR

Round each sample to one of $2^n$ levels with an $n$-bit quantizer. The rounding
error behaves like noise, and for a full-scale signal the **signal-to-quantization-
noise ratio** is the famous "6 dB per bit" rule:

$$\\text{SQNR}_{dB} \\approx 6.02\\,n + 1.76.$$

Slide the bit depth and watch SQNR climb 6 dB per bit:

```plot
{"title": "Quantization SQNR vs bit depth (6 dB per bit)", "xLabel": "bits n", "yLabel": "SQNR (dB)", "xRange": [1, 16], "yRange": [0, 100], "grid": true, "functions": [{"expr": "6.02*x + 1.76", "label": "SQNR = 6.02 n + 1.76"}]}
```

## PCM and companding

**Pulse-Code Modulation** is sample + quantize + binary-encode -- the format of
the classic digital phone network. Because quiet speech needs fine steps but
loud speech does not, telephony **compands** (compress then expand) with the
**mu-law** (North America) or **A-law** (Europe) curve: a logarithmic step size
that gives near-constant SNR across a wide loudness range.

```matlab
n = 8;                       % 8-bit PCM (telephone)
sqnr_db = 6.02*n + 1.76;     % ~ 49.8 dB
mu = 255;                    % mu-law companding parameter
y = sign(x).*log(1+mu*abs(x))/log(1+mu);
```

```python
import numpy as np
n = 8                              # 8-bit PCM
sqnr_db = 6.02*n + 1.76            # ~ 49.8 dB
mu = 255
y = np.sign(x)*np.log(1+mu*np.abs(x))/np.log(1+mu)
```

> **Practical insight:** always put an **anti-alias filter** (analog low-pass)
> *before* the ADC. Once aliasing happens, no later processing can undo it.

**Next:** shaping the bits into pulses that fit the channel.
""",
        ),
        _t(
            "Baseband signaling & pulse shaping",
            "12 min",
            """\
# Baseband signaling & pulse shaping

Before any radio carrier, bits become a **baseband** waveform: a stream of
pulses. *How* you shape those pulses sets the bandwidth and the error rate.

## Line codes

A **line code** maps bits to voltage levels. Common choices:

| Line code | 1 / 0 mapping | Property |
|-----------|---------------|----------|
| NRZ | +V / -V held | simple, but no guaranteed transitions |
| RZ | pulse returns to 0 mid-bit | more transitions, double the bandwidth |
| Manchester | edge mid-bit | self-clocking (used in 10BASE-T Ethernet) |
| Bipolar/AMI | alternate polarity for 1s | no DC, used in T1 lines |

## The ISI problem and the Nyquist criterion

Real pulses spread in time. If pulse $k$ still has energy at the sampling instant
of pulse $k+1$, symbols smear into each other -- **inter-symbol interference
(ISI)**. The **Nyquist ISI criterion** says a pulse causes zero ISI if it is
**zero at every other symbol instant**. The ideal sinc pulse does this but is
fragile; the practical fix is the **raised-cosine** pulse, which trades a little
extra bandwidth (the **roll-off** $\\alpha$) for graceful, realizable behavior:

$$B = \\frac{R_s}{2}(1 + \\alpha), \\qquad 0 \\le \\alpha \\le 1.$$

Slide the roll-off and watch the raised-cosine spectrum widen from a brick wall
($\\alpha = 0$) to a gentle skirt:

```plot
{"title": "Raised-cosine spectrum vs roll-off alpha (Rs/2 = 1)", "xLabel": "frequency f (normalized to Rs/2)", "yLabel": "|H(f)|", "xRange": [0, 2.2], "yRange": [0, 1.2], "grid": true, "controls": [{"name": "a", "range": [0.05, 1], "value": 0.35, "label": "roll-off alpha"}], "functions": [{"expr": "(abs(x) <= 1-a)*1 + (abs(x) > 1-a)*(abs(x) <= 1+a)*0.5*(1 + cos(pi/(2*a)*(abs(x)-1+a)))", "label": "raised-cosine |H(f)|"}]}
```

## The eye diagram

Overlay many symbol periods of the received waveform and you get the **eye
diagram** -- the single most useful picture in digital comms. A wide-open eye
means easy detection; ISI and noise close the eye. Its vertical opening is the
noise margin; its horizontal opening is the timing margin.

```mermaid
flowchart LR
  BITS["bit stream"] --> LC["line coder"]
  LC --> PS["pulse-shaping filter (raised-cosine)"]
  PS --> CH["channel"]
  CH --> RX["receive filter + sampler"]
```

```matlab
alpha = 0.35; Rs = 1e6;
B = Rs/2*(1+alpha);          % occupied bandwidth -> 675 kHz
```

```python
alpha, Rs = 0.35, 1e6
B = Rs/2*(1+alpha)           # 675 kHz
```

> **Practical insight:** roll-off is a knob you tune. Wi-Fi and LTE use modest
> roll-off (around 0.1-0.3) to save spectrum; simpler links use 0.5 for easier
> filters.

**Next:** lifting baseband onto a carrier -- digital modulation.
""",
        ),
        _t(
            "Digital modulation basics",
            "12 min",
            """\
# Digital modulation basics

To send bits over the air or a cable you ride them on a sinusoidal **carrier**
by varying one of its three properties:

| Scheme | What varies | Bit example |
|--------|-------------|-------------|
| **ASK** (amplitude) | amplitude | on/off keying (optical fiber, IR remotes) |
| **FSK** (frequency) | frequency | Bluetooth GFSK, old modems, LoRa |
| **PSK** (phase) | phase | BPSK on GPS, QPSK on satellite/Wi-Fi |

$$s(t) = A(t)\\cos\\!\\big(2\\pi f_c t + \\phi(t)\\big).$$

Watch all three keying the *same* bit pattern 1 0 1 1 0 onto a carrier:

```plot
{"title": "Three modulations of the same bits 1 0 1 1 0", "xLabel": "time (symbol units)", "yLabel": "amplitude", "xRange": [0, 5], "yRange": [-2, 8], "grid": true, "functions": [{"expr": "6 + ((floor(x)==0)+(floor(x)==2)+(floor(x)==3))*cos(2*pi*3*x)", "label": "ASK (on/off)", "color": "#2563eb"}, {"expr": "3 + cos(2*pi*if((floor(x)==0)+(floor(x)==2)+(floor(x)==3) > 0, 4, 2)*x)", "label": "FSK (freq)", "color": "#16a34a"}, {"expr": "cos(2*pi*3*x + pi*(((floor(x)==1)+(floor(x)==4)) > 0))", "label": "PSK (phase)", "color": "#dc2626"}]}
```

## The constellation: the I/Q plane

The cleanest way to picture digital modulation is the **constellation**: plot
each symbol as a point on the in-phase ($I$) / quadrature ($Q$) plane. Any symbol
is $I\\cos(2\\pi f_c t) - Q\\sin(2\\pi f_c t)$, so a point $(I, Q)$ *is* a waveform.

**BPSK** uses two antipodal points (1 bit/symbol); **QPSK** uses four points at
the corners (2 bits/symbol) for the same bandwidth:

```plot
{"title": "BPSK (2 points) vs QPSK (4 points) constellations", "xLabel": "in-phase I", "yLabel": "quadrature Q", "xRange": [-1.5, 1.5], "yRange": [-1.5, 1.5], "grid": true, "points": [{"x": 1, "y": 0, "label": "BPSK 1", "color": "#2563eb", "size": 9}, {"x": -1, "y": 0, "label": "BPSK 0", "color": "#2563eb", "size": 9}, {"x": 0.707, "y": 0.707, "label": "QPSK 00", "color": "#dc2626", "size": 7}, {"x": -0.707, "y": 0.707, "label": "QPSK 01", "color": "#dc2626", "size": 7}, {"x": -0.707, "y": -0.707, "label": "QPSK 11", "color": "#dc2626", "size": 7}, {"x": 0.707, "y": -0.707, "label": "QPSK 10", "color": "#dc2626", "size": 7}]}
```

QPSK doubles the data rate of BPSK in the same bandwidth at the **same** energy
per bit -- a free lunch that explains its popularity (GPS, satellite, cellular
control channels).

```matlab
bits = [0 0 0 1 1 1 1 0];
sym  = bits(1:2:end)*2-1 + 1j*(bits(2:2:end)*2-1);   % QPSK symbols
sym  = sym/sqrt(2);                                  % unit energy
```

```python
import numpy as np
bits = np.array([0,0,0,1,1,1,1,0])
I = bits[0::2]*2 - 1
Q = bits[1::2]*2 - 1
sym = (I + 1j*Q)/np.sqrt(2)                           # QPSK, unit energy
```

**Next:** the channel that fights you -- AWGN and how to detect through it.
""",
        ),
        _t(
            "The AWGN channel & detection",
            "12 min",
            """\
# The AWGN channel & detection

The simplest, most fundamental channel adds **Additive White Gaussian Noise**
(AWGN): the received sample is the sent symbol plus a Gaussian random number.
Every received constellation point is a fuzzy cloud:

$$r = s + n, \\qquad n \\sim \\mathcal{N}(0, N_0/2).$$

## The matched filter: best SNR before deciding

Given a known pulse shape in noise, the **matched filter** -- correlating the
received signal with a time-reversed copy of the pulse -- maximizes the
signal-to-noise ratio at the sampling instant. It is provably the optimal front
end for an AWGN channel, which is why every receiver has one.

```mermaid
flowchart LR
  RX["received r(t)"] --> MF["matched filter"]
  MF --> SMP["sample at symbol time"]
  SMP --> DEC["decision rule (nearest symbol)"]
  DEC --> BITS["bits out"]
```

## The decision rule

After the matched filter, decide which symbol was most likely sent. For equal
priors and Gaussian noise this is the **minimum-distance rule**: pick the
constellation point closest to the received sample. The boundaries between
regions are the **decision boundaries** (for BPSK, simply $r > 0$ means "1").

## BER intuition: it is all about distance over noise

The bit error rate falls **exponentially** as you separate the symbols relative
to the noise. For BPSK and QPSK,

$$P_b = Q\\!\\left(\\sqrt{\\tfrac{2E_b}{N_0}}\\right).$$

Small increases in $E_b/N_0$ buy huge drops in error rate -- the curve plunges
off a cliff (here approximated with $0.5\\,e^{-E_b/N_0}$ for the in-browser plot):

```plot
{"title": "BPSK BER falls off a cliff with Eb/N0 (approx)", "xLabel": "Eb/N0 (linear)", "yLabel": "bit error rate (approx)", "xRange": [0, 12], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "0.5*exp(-x)", "label": "approx Pb ~ 0.5 exp(-Eb/N0)"}]}
```

```matlab
EbN0_dB = 8;
EbN0 = 10^(EbN0_dB/10);
Pb = qfunc(sqrt(2*EbN0));        % BPSK BER (uses Communications Toolbox)
```

```python
import numpy as np
from math import erfc
EbN0_dB = 8
EbN0 = 10**(EbN0_dB/10)
Pb = 0.5*erfc(np.sqrt(EbN0))     # BPSK BER, Q(x) = 0.5 erfc(x/sqrt(2))
```

> **Practical insight:** "link budget" engineering is exactly this -- add up gains
> and losses to find the $E_b/N_0$ at the receiver, then read the BER off the
> curve. A 3 dB margin is cheap insurance against fading.

**Next:** build it and see the constellation, eye, and BER yourself.
""",
        ),
        _code(
            "Lab: constellation, eye diagram & BER",
            "13 min",
            """\
# Simulate a QPSK link over AWGN: send symbols, add noise, detect, count errors,
# and plot the noisy constellation, an eye diagram, and a BER-vs-Eb/N0 curve.
import math

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
N = 20000                                   # symbols
bits = rng.integers(0, 2, size=2*N)         # 2 bits per QPSK symbol

# Gray-mapped QPSK, unit average energy
I = bits[0::2]*2 - 1
Q = bits[1::2]*2 - 1
tx = (I + 1j*Q)/np.sqrt(2)

# --- Constellation + eye at one Eb/N0 ---
EbN0_dB = 9.0
EbN0 = 10**(EbN0_dB/10)
# QPSK: 2 bits/symbol, Es = 1, so noise variance per complex dim = 1/(2*2*EbN0)
sigma = np.sqrt(1/(4*EbN0))
noise = sigma*(rng.standard_normal(N) + 1j*rng.standard_normal(N))
rx = tx + noise

# Pulse-shaped baseband for the eye diagram (rectangular upsample, simple RC tap)
sps = 8
up = np.zeros(N*sps)
up[::sps] = (I/np.sqrt(2))
h = np.hanning(2*sps+1)                     # smoothing pulse (no scipy)
h = h/h.sum()
wave = np.convolve(up, h, mode="same")

fig, ax = plt.subplots(1, 3, figsize=(13, 4))
ax[0].plot(rx.real, rx.imag, ".", ms=1, color="#2563eb", alpha=0.4)
ax[0].plot([0.707,-0.707,-0.707,0.707], [0.707,0.707,-0.707,-0.707],
           "x", ms=12, color="#dc2626")
ax[0].set_title(f"QPSK constellation @ {EbN0_dB:.0f} dB")
ax[0].set_xlabel("I"); ax[0].set_ylabel("Q"); ax[0].grid(True); ax[0].axis("equal")

for k in range(0, 400*sps, 2*sps):          # overlay 2-symbol windows
    ax[1].plot(wave[k:k+2*sps], color="#16a34a", alpha=0.15)
ax[1].set_title("eye diagram (I rail)")
ax[1].set_xlabel("sample within 2 symbols"); ax[1].grid(True)

# --- BER vs Eb/N0 sweep ---
ebn0_db = np.arange(0, 11)
ber = np.zeros_like(ebn0_db, dtype=float)
for j, db in enumerate(ebn0_db):
    snr = 10**(db/10)
    s = np.sqrt(1/(4*snr))
    r = tx + s*(rng.standard_normal(N) + 1j*rng.standard_normal(N))
    bI = (r.real > 0).astype(int)
    bQ = (r.imag > 0).astype(int)
    dec = np.empty(2*N, dtype=int)
    dec[0::2] = bI
    dec[1::2] = bQ
    ber[j] = np.mean(dec != bits)

theory = 0.5*np.array([math.erfc(np.sqrt(10**(d/10))) for d in ebn0_db])
ax[2].semilogy(ebn0_db, np.maximum(ber, 1e-5), "o-", color="#2563eb", label="simulated")
ax[2].semilogy(ebn0_db, np.maximum(theory, 1e-5), "--", color="#dc2626", label="theory")
ax[2].set_title("QPSK BER vs Eb/N0")
ax[2].set_xlabel("Eb/N0 (dB)"); ax[2].set_ylabel("BER")
ax[2].grid(True, which="both"); ax[2].legend()

plt.tight_layout(); plt.show()

print(f"simulated BER at {EbN0_dB:.0f} dB ~ {ber[int(EbN0_dB)]:.2e}")
print("BER halves roughly every dB in this range -- the waterfall curve.")

# Try it yourself:
#   1. Drop EbN0_dB to 4: the constellation clouds overlap and BER climbs.
#   2. The MATLAB way uses comm.QPSKModulator + awgn() + biterr().
""",
        ),
    ),
)


# -- Digital Communications -- Intermediate ------------------------------------

_DIGITAL_COMMS_INTERMEDIATE = SeedCourse(
    slug="digital-comms-intermediate",
    title=(
        "Digital Communications & Coding Theory -- Intermediate: Modulation & Information Theory"
    ),
    description=(
        "Higher-order modulation and the limits of communication: M-ary/QAM and "
        "Gray coding, BER vs SNR and the power-bandwidth tradeoff, entropy and "
        "mutual information and the Shannon capacity bound, source coding "
        "(Huffman), and channel impairments (fading, equalization, "
        "synchronization) -- dual MATLAB/Python, interactive plots, and a runnable "
        "QAM BER / Shannon-capacity lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "M-ary and quadrature modulation",
            "12 min",
            """\
# M-ary and quadrature modulation

BPSK sends 1 bit per symbol; QPSK sends 2. To go faster in the same bandwidth,
pack **more points** into the I/Q plane. An **M-ary** scheme carries
$\\log_2 M$ bits per symbol.

## M-PSK and QAM

- **M-PSK** spreads $M$ points evenly around a circle (8-PSK = 3 bits/symbol).
  Beyond 8-PSK the points crowd and errors rise.
- **QAM** (Quadrature Amplitude Modulation) uses a **grid** of points, varying
  *both* amplitude and phase. 16-QAM = 4 bits/symbol, 64-QAM = 6, 256-QAM = 8.
  Wi-Fi 6 and 5G push to 1024-QAM (10 bits/symbol) on clean links.

Slide the order and watch a square QAM grid grow denser (points get closer, so
you need a cleaner channel):

```plot
{"title": "QAM grid spacing shrinks as order M grows", "xLabel": "log2(M) bits/symbol", "yLabel": "min distance / scale", "xRange": [2, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(sqrt(pow(2, x)) - 1)", "label": "min distance ~ 1/(sqrt(M)-1)"}]}
```

Here is a 16-QAM constellation (4 bits per symbol):

```plot
{"title": "16-QAM constellation (4 bits/symbol)", "xLabel": "I", "yLabel": "Q", "xRange": [-4, 4], "yRange": [-4, 4], "grid": true, "points": [{"x": -3, "y": 3, "color": "#2563eb"}, {"x": -1, "y": 3, "color": "#2563eb"}, {"x": 1, "y": 3, "color": "#2563eb"}, {"x": 3, "y": 3, "color": "#2563eb"}, {"x": -3, "y": 1, "color": "#2563eb"}, {"x": -1, "y": 1, "color": "#2563eb"}, {"x": 1, "y": 1, "color": "#2563eb"}, {"x": 3, "y": 1, "color": "#2563eb"}, {"x": -3, "y": -1, "color": "#2563eb"}, {"x": -1, "y": -1, "color": "#2563eb"}, {"x": 1, "y": -1, "color": "#2563eb"}, {"x": 3, "y": -1, "color": "#2563eb"}, {"x": -3, "y": -3, "color": "#2563eb"}, {"x": -1, "y": -3, "color": "#2563eb"}, {"x": 1, "y": -3, "color": "#2563eb"}, {"x": 3, "y": -3, "color": "#2563eb"}]}
```

## Bit-to-symbol mapping and Gray coding

When noise nudges a received point into a neighboring cell, you want as **few
bits** wrong as possible. **Gray coding** assigns bit patterns so adjacent
symbols differ in exactly **one** bit -- so the most likely error flips only one
bit, roughly halving the BER for the same symbol error rate.

```matlab
M = 16;                      % 16-QAM
k = log2(M);                 % 4 bits/symbol
g = bitxor(0:M-1, floor((0:M-1)/2));   % binary -> Gray code
```

```python
import numpy as np
M = 16
k = int(np.log2(M))          # 4 bits/symbol
idx = np.arange(M)
gray = idx ^ (idx >> 1)      # binary -> Gray code
```

> **Practical insight:** higher QAM needs a higher SNR. Adaptive systems (Wi-Fi,
> LTE, DOCSIS cable) measure the link and **switch** modulation/coding on the fly
> -- QPSK at the cell edge, 256-QAM up close.

**Next:** how that choice trades error rate against bandwidth.
""",
        ),
        _t(
            "Performance over channels",
            "12 min",
            """\
# Performance over channels

Picking a modulation is choosing a point in a tradeoff space. Two axes matter:
**how reliable** (BER vs SNR) and **how efficient** (bits/s/Hz).

## BER vs SNR: the waterfall curves

Plot BER against $E_b/N_0$ and every scheme makes a **waterfall**: nearly flat,
then a cliff. Denser constellations (higher-order QAM) need **more** $E_b/N_0$ to
hit the same BER, because their points sit closer together. Slide $E_b/N_0$ and
compare BPSK/QPSK against a denser scheme (illustrative exponential approxima-
tions for in-browser plotting):

```plot
{"title": "BER waterfalls: dense schemes need more Eb/N0 (approx)", "xLabel": "Eb/N0 (linear)", "yLabel": "BER (approx)", "xRange": [1, 15], "yRange": [0, 0.4], "grid": true, "controls": [{"name": "shift", "range": [0, 6], "value": 3, "label": "extra Eb/N0 needed by 16-QAM"}], "functions": [{"expr": "0.5*exp(-x)", "label": "BPSK/QPSK (approx)", "color": "#2563eb"}, {"expr": "0.5*exp(-x/(1 + shift))", "label": "16-QAM (approx, shifted)", "color": "#dc2626"}]}
```

## Bandwidth efficiency and the power-bandwidth tradeoff

Bandwidth efficiency is $\\eta = \\log_2 M$ bits/s/Hz (before pulse-shaping
overhead). You can buy more bits/s/Hz (denser modulation) **or** more robustness
(spread spectrum, lower order), but not both for free -- spend **power** to get
bandwidth back, or spend **bandwidth** to get power back:

| Regime | Strategy | Example |
|--------|----------|---------|
| **Power-limited** (deep space, IoT) | low-order modulation + heavy coding | Voyager, LoRa, NB-IoT |
| **Bandwidth-limited** (urban cellular, cable) | high-order QAM | 5G mid-band, DOCSIS |

```mermaid
flowchart LR
  P["more power / Eb/N0"] --> R["robust link"]
  BW["more bandwidth"] --> R
  R --> CAP["target throughput at target BER"]
```

```matlab
M = [2 4 16 64 256];
eta = log2(M);               % 1 2 4 6 8 bits/s/Hz
```

```python
import numpy as np
M = np.array([2, 4, 16, 64, 256])
eta = np.log2(M)             # 1 2 4 6 8 bits/s/Hz
```

> **Practical insight:** deep-space probes are power-limited (tiny received
> power, unlimited bandwidth) so they use low-order modulation + powerful codes;
> a cable modem is bandwidth-limited so it cranks QAM as high as the SNR allows.

**Next:** the theoretical ceiling on all of this -- information theory.
""",
        ),
        _t(
            "Information theory",
            "13 min",
            """\
# Information theory

In 1948 Claude Shannon founded the entire field with one paper. It answers two
questions exactly: how few bits can represent a source (**entropy**), and how
fast can a channel carry them reliably (**capacity**).

## Entropy: the irreducible bits

The **entropy** of a source is the average information per symbol, in bits:

$$H(X) = -\\sum_i p_i \\log_2 p_i.$$

A fair coin has $H = 1$ bit; a biased coin carries **less** (you can guess it).
Entropy is the floor: no lossless compressor can beat it. For a binary source it
is maximal at $p = 0.5$ and zero at the certain extremes:

```plot
{"title": "Binary entropy: maximal at p = 0.5", "xLabel": "probability p of a 1", "yLabel": "H(p) (bits)", "xRange": [0.001, 0.999], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "-(x*log2(x) + (1-x)*log2(1-x))", "label": "H(p)"}]}
```

## Mutual information

**Mutual information** $I(X;Y)$ measures how many bits the channel output $Y$
tells you about the input $X$ -- the actual information that survives the noise:

$$I(X;Y) = H(X) - H(X\\mid Y).$$

Capacity is the mutual information **maximized** over all input distributions.

## The Shannon capacity bound

For an AWGN channel of bandwidth $B$ and signal-to-noise ratio $S/N$, the maximum
error-free rate is the celebrated:

$$C = B\\,\\log_2\\!\\left(1 + \\frac{S}{N}\\right) \\;[\\text{bits/s}].$$

No code, no modulation, no cleverness can beat $C$. Slide bandwidth and watch the
capacity climb (with $S/N$ fixed); note capacity grows **linearly** with
bandwidth but only **logarithmically** with power:

```plot
{"title": "Shannon capacity vs bandwidth (slide SNR), B in MHz", "xLabel": "bandwidth B (MHz)", "yLabel": "capacity C (Mbit/s)", "xRange": [0, 100], "yRange": [0, 800], "grid": true, "controls": [{"name": "snr", "range": [1, 1000], "value": 100, "label": "linear SNR (S/N)"}], "functions": [{"expr": "x*log2(1 + snr)", "label": "C = B log2(1+SNR)"}]}
```

```matlab
B = 20e6; SNR_dB = 30;
SNR = 10^(SNR_dB/10);
C = B*log2(1 + SNR);          % ~ 199 Mbit/s
```

```python
import numpy as np
B, SNR_dB = 20e6, 30
SNR = 10**(SNR_dB/10)
C = B*np.log2(1 + SNR)        # ~ 199 Mbit/s
```

> **Practical insight:** every "Gbps" headline is a race toward Shannon. Modern
> LDPC and polar codes get within a fraction of a dB of $C$ -- the gap that took
> 50 years to close.

**Next:** squeezing the source down to its entropy -- source coding.
""",
        ),
        _t(
            "Source coding",
            "11 min",
            """\
# Source coding

**Source coding** (compression) removes redundancy so you spend channel
resources only on real information. The target is the source entropy $H$.

## Variable-length codes and the prefix property

Frequent symbols deserve short codewords. To decode a stream with no separators,
codewords must satisfy the **prefix property**: no codeword is a prefix of
another. Then decoding is unambiguous.

## Huffman coding

**Huffman's** algorithm builds the optimal prefix code by repeatedly merging the
two least-likely symbols into a binary tree:

```mermaid
flowchart TB
  ROOT(("root"))
  ROOT -->|0| A["A (p=0.5) -> 0"]
  ROOT -->|1| N1(("."))
  N1 -->|0| B["B (p=0.25) -> 10"]
  N1 -->|1| N2(("."))
  N2 -->|0| C["C (p=0.125) -> 110"]
  N2 -->|1| D["D (p=0.125) -> 111"]
```

For that source the average length is $0.5(1)+0.25(2)+0.125(3)+0.125(3) = 1.75$
bits/symbol -- exactly the entropy here, so it is optimal.

The closer a symbol's probability is to a power of $1/2$, the closer its ideal
length $-\\log_2 p$ is to an integer -- and the tighter Huffman packs:

```plot
{"title": "Ideal codeword length = -log2(p)", "xLabel": "symbol probability p", "yLabel": "ideal length (bits)", "xRange": [0.01, 1], "yRange": [0, 7], "grid": true, "functions": [{"expr": "-log2(x)", "label": "-log2(p)"}]}
```

## The compression toolbox

| Method | Idea | Used in |
|--------|------|---------|
| **Huffman** | optimal symbol-by-symbol prefix code | JPEG, MP3, DEFLATE |
| **Arithmetic / range** | code a whole message as one fraction | H.264/265, JPEG2000 |
| **LZ77 / LZ78** | replace repeats with back-references | gzip, PNG, ZIP |
| **Run-length** | count runs of repeats | fax, simple images |

These are **lossless**. Media codecs (JPEG, MP3, H.265) first throw away
perceptually irrelevant detail (**lossy**), then entropy-code the rest.

```matlab
p = [0.5 0.25 0.125 0.125];
H = -sum(p .* log2(p));       % 1.75 bits/symbol
```

```python
import numpy as np
p = np.array([0.5, 0.25, 0.125, 0.125])
H = -np.sum(p*np.log2(p))     # 1.75 bits/symbol
```

> **Practical insight:** compress *before* you encrypt or channel-code.
> Compressed data looks random, so adding error-correction redundancy afterward
> is what protects it on the wire.

**Next:** the messy realities the AWGN model ignores -- channel impairments.
""",
        ),
        _t(
            "Channel impairments",
            "12 min",
            """\
# Channel impairments

The pristine AWGN channel is a teaching fiction. Real wireless links suffer
**fading**, and real receivers must fight **distortion** and align their clocks
-- **equalization** and **synchronization**.

## Multipath and fading

A radio signal reaches the receiver via many paths (direct, reflected off walls,
buildings, the ground). They add with different delays and phases -- sometimes
constructively, sometimes destructively. The result is **fading**: the received
amplitude fluctuates, deeply and randomly, as you move. Watch a fading envelope
deep-fade as you move through a standing-wave pattern (press Play):

```plot
{"title": "Multipath fading envelope along a path (press Play)", "xLabel": "distance (wavelengths)", "yLabel": "received amplitude", "xRange": [0, 12], "yRange": [0, 2.4], "grid": true, "animate": {"param": "t", "range": [0, 12], "label": "position"}, "functions": [{"expr": "abs(1 + 0.9*cos(2*pi*x) + 0.5*sin(2*pi*1.7*x))", "label": "|received| vs position", "color": "#2563eb"}], "points": [{"xExpr": "t", "yExpr": "abs(1 + 0.9*cos(2*pi*t) + 0.5*sin(2*pi*1.7*t))", "label": "you are here", "color": "#dc2626", "size": 7, "trail": true}]}
```

- **Flat fading** scales the whole signal; **frequency-selective** fading distorts
  it (different frequencies fade differently), causing ISI.
- **Doppler** from motion spreads the signal in frequency and sets how fast the
  fade changes.

## Equalization: undo the channel

A frequency-selective channel smears symbols (ISI). An **equalizer** estimates
the channel and applies its inverse so the eye reopens. Forms range from a simple
**zero-forcing** filter to an **adaptive** LMS/RLS equalizer that tracks a
changing channel, to the per-subcarrier equalizer that makes **OFDM** so elegant
(Advanced course).

## Synchronization: line up in time, frequency, and phase

Before detection the receiver must lock onto the signal:

| Sync type | What it aligns | Tool |
|-----------|----------------|------|
| **Carrier** | frequency + phase of the carrier | PLL, Costas loop |
| **Symbol/timing** | the sampling instant | early-late, Gardner |
| **Frame** | where a packet starts | known preamble/pilot |

```mermaid
flowchart LR
  RX["received"] --> CS["carrier sync (PLL)"]
  CS --> TS["timing sync"]
  TS --> EQ["equalizer"]
  EQ --> DET["detector"]
```

```matlab
% Two-tap multipath channel then a zero-forcing equalizer
h = [1 0.5];                 % channel impulse response
heq = [1 -0.5 0.25 -0.125];  % truncated inverse (1/(1+0.5 z^-1))
```

```python
import numpy as np
h = np.array([1.0, 0.5])           # channel
heq = np.array([1, -0.5, 0.25, -0.125])  # truncated zero-forcing inverse
```

> **Practical insight:** pilots and preambles are not wasted overhead -- they are
> how the receiver learns the channel and clock. GPS, Wi-Fi, and LTE all spend a
> few percent of the air time on known reference symbols.

**Next:** put modulation and capacity together in code.
""",
        ),
        _code(
            "Lab: QAM BER curves & the Shannon bound",
            "13 min",
            """\
# Simulate BER vs Eb/N0 for QPSK and 16-QAM over AWGN, and overlay the Shannon
# capacity bound to see how far each scheme sits from the theoretical limit.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)
N = 40000

# 16-QAM Gray-mapped levels {-3,-1,1,3} on each rail, normalized to unit energy
levels = np.array([-3, -1, 1, 3])
norm16 = np.sqrt(10.0)                      # avg energy of 16-QAM with these levels

ebn0_db = np.arange(0, 16)
ber_qpsk = np.zeros_like(ebn0_db, dtype=float)
ber_16 = np.zeros_like(ebn0_db, dtype=float)

for j, db in enumerate(ebn0_db):
    ebn0 = 10**(db/10)

    # --- QPSK: 2 bits/symbol ---
    bq = rng.integers(0, 2, size=2*N)
    txq = ((bq[0::2]*2 - 1) + 1j*(bq[1::2]*2 - 1))/np.sqrt(2)
    sq = np.sqrt(1/(4*ebn0))
    rq = txq + sq*(rng.standard_normal(N) + 1j*rng.standard_normal(N))
    decq = np.empty(2*N, dtype=int)
    decq[0::2] = (rq.real > 0).astype(int)
    decq[1::2] = (rq.imag > 0).astype(int)
    ber_qpsk[j] = np.mean(decq != bq)

    # --- 16-QAM: 4 bits/symbol, Es/N0 = (log2 M) * Eb/N0 ---
    iq = levels[rng.integers(0, 4, size=N)]
    qq = levels[rng.integers(0, 4, size=N)]
    tx16 = (iq + 1j*qq)/norm16
    esn0 = 4*ebn0
    s16 = np.sqrt(1/(2*esn0))
    r16 = tx16*norm16 + s16*norm16*(rng.standard_normal(N) + 1j*rng.standard_normal(N))
    # nearest-level decision per rail
    di = levels[np.argmin(np.abs(r16.real[:, None] - levels[None, :]), axis=1)]
    dq = levels[np.argmin(np.abs(r16.imag[:, None] - levels[None, :]), axis=1)]
    symerr = (di != iq) | (dq != qq)
    ber_16[j] = np.mean(symerr) / 4.0       # approx bits/symbol with Gray mapping

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].semilogy(ebn0_db, np.maximum(ber_qpsk, 1e-5), "o-", color="#2563eb", label="QPSK")
ax[0].semilogy(ebn0_db, np.maximum(ber_16, 1e-5), "s-", color="#dc2626", label="16-QAM")
ax[0].set_title("BER vs Eb/N0: 16-QAM needs more SNR")
ax[0].set_xlabel("Eb/N0 (dB)"); ax[0].set_ylabel("BER")
ax[0].grid(True, which="both"); ax[0].legend()

# --- Shannon bound: spectral efficiency vs Eb/N0 ---
snr_lin = np.logspace(-1, 3, 400)
eta = np.log2(1 + snr_lin)                  # C/B bits/s/Hz
ebn0_lim = snr_lin/eta                       # Eb/N0 = SNR / spectral efficiency
ax[1].plot(10*np.log10(ebn0_lim), eta, color="#16a34a", lw=2, label="Shannon limit")
ax[1].axvline(-1.59, ls="--", color="#94a3b8", label="-1.59 dB floor")
ax[1].set_title("Shannon: spectral efficiency vs Eb/N0")
ax[1].set_xlabel("Eb/N0 (dB)"); ax[1].set_ylabel("bits/s/Hz")
ax[1].set_xlim(-3, 25); ax[1].grid(True); ax[1].legend()

plt.tight_layout(); plt.show()

print(f"QPSK BER at 10 dB ~ {ber_qpsk[10]:.2e}")
print(f"16-QAM BER at 10 dB ~ {ber_16[10]:.2e}  (worse -- denser constellation)")
print("Shannon floor: no scheme works below Eb/N0 = -1.59 dB.")

# Try it yourself:
#   1. Push the loop to 64-QAM (levels -7..7) -- the curve shifts further right.
#   2. The MATLAB way: berawgn(EbN0,'qam',M) gives the theory curves directly.
""",
        ),
    ),
)


# -- Digital Communications -- Advanced ----------------------------------------

_DIGITAL_COMMS_ADVANCED = SeedCourse(
    slug="digital-comms-advanced",
    title="Digital Communications & Coding Theory -- Advanced: Coding, OFDM & MIMO",
    description=(
        "The modern physical layer: linear block and cyclic codes (Hamming, CRC, "
        "syndrome decoding), convolutional codes and the Viterbi algorithm, modern "
        "near-capacity codes (turbo, LDPC, polar), OFDM (multicarrier, FFT, cyclic "
        "prefix, PAPR), MIMO and spatial multiplexing, and the throughline across "
        "5G, Wi-Fi and satellite -- dual MATLAB/Python, interactive plots, and a "
        "runnable OFDM / coding-gain lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Linear block and cyclic codes",
            "12 min",
            """\
# Linear block and cyclic codes

**Channel coding** adds *structured* redundancy so the receiver can detect and
correct errors -- trading a little rate for a lot of reliability. The simplest
family is **linear block codes**: take $k$ data bits, append $n-k$ parity bits to
make an $n$-bit codeword.

## Parity, distance, and what you can fix

A code's power is its **minimum Hamming distance** $d_{min}$ -- the fewest bit
flips between any two codewords. It can:

$$\\text{detect } d_{min}-1 \\text{ errors}, \\qquad
\\text{correct } \\left\\lfloor \\frac{d_{min}-1}{2} \\right\\rfloor \\text{ errors}.$$

A single parity bit has $d_{min} = 2$: detects one error, corrects none. The
**Hamming(7,4)** code has $d_{min} = 3$: corrects any single-bit error in 7.

## The generator and parity-check matrices

Encoding is $\\mathbf{c} = \\mathbf{m}\\,G$ over GF(2); checking is the **syndrome**
$\\mathbf{s} = \\mathbf{r}\\,H^\\top$. If $\\mathbf{s} = 0$ the word is valid; otherwise
the syndrome **points at the error location**:

```mermaid
flowchart LR
  M["message m (k bits)"] --> ENC["encode c = m G"]
  ENC --> CH["channel (flips some bits)"]
  CH --> SYN["syndrome s = r H^T"]
  SYN --> DEC["s -> error position -> correct"]
```

## Cyclic codes and the CRC

**Cyclic codes** are linear codes where any cyclic shift of a codeword is also a
codeword -- which lets you encode with simple shift-register polynomial division
instead of matrix math. The everyday workhorse is the **CRC** (Cyclic Redundancy
Check): treat the message as a polynomial, divide by a generator polynomial, and
append the remainder. CRCs guard Ethernet frames, ZIP files, and disk sectors --
they **detect** errors (you retransmit) rather than correct them.

Coding gives you a **coding gain**: the dB of $E_b/N_0$ you save at a target BER.
More redundancy buys more gain but costs rate -- a tradeoff curve:

```plot
{"title": "Coding gain vs code rate (illustrative)", "xLabel": "code rate k/n", "yLabel": "coding gain (dB, illustrative)", "xRange": [0.2, 1], "yRange": [0, 8], "grid": true, "functions": [{"expr": "7*(1 - x)", "label": "more redundancy -> more gain"}]}
```

```matlab
% Hamming(7,4) single-error correction
n = 7; k = 4; dmin = 3;
t = floor((dmin-1)/2);        % corrects t = 1 error
```

```python
n, k, dmin = 7, 4, 3
t = (dmin - 1)//2             # corrects 1 error
```

> **Practical insight:** detection (CRC + retransmit) is cheap and perfect when a
> back-channel exists (Wi-Fi, TCP); correction (FEC) is essential when it does not
> (broadcast, deep space, storage).

**Next:** coding that works on a continuous stream -- convolutional codes.
""",
        ),
        _t(
            "Convolutional codes and the Viterbi algorithm",
            "12 min",
            """\
# Convolutional codes and the Viterbi algorithm

Block codes chop data into independent blocks. **Convolutional codes** instead
slide a small **shift register** over the bit stream, so each output bit depends
on the current and a few past input bits -- coding *with memory*.

## The encoder and the trellis

A rate-1/2, constraint-length-3 encoder outputs 2 bits per input bit, computed
from the 2-bit register state. Because there are finitely many states, the
encoder is a **finite state machine**:

```mermaid
stateDiagram-v2
  [*] --> S00
  S00 --> S00: in 0 / out 00
  S00 --> S10: in 1 / out 11
  S10 --> S01: in 0 / out 10
  S10 --> S11: in 1 / out 01
  S01 --> S00: in 0 / out 11
  S01 --> S10: in 1 / out 00
  S11 --> S01: in 0 / out 01
  S11 --> S11: in 1 / out 10
```

Unrolling that machine over time gives the **trellis**: a grid of states across
time, with every valid bit sequence a path through it.

## The Viterbi algorithm: the best path through the trellis

Decoding asks: which transmitted path is *closest* to what I received? Brute
force is exponential, but the **Viterbi algorithm** finds the maximum-likelihood
path in *linear* time by keeping, at each state, only the single best surviving
path (dynamic programming). Its cost grows with the number of states, which is
exponential in constraint length -- the practical reason constraint lengths stay
around 7-9:

```plot
{"title": "Viterbi cost grows as 2^(K-1) states", "xLabel": "constraint length K", "yLabel": "trellis states 2^(K-1)", "xRange": [2, 10], "yRange": [0, 300], "grid": true, "functions": [{"expr": "pow(2, x-1)", "label": "states = 2^(K-1)"}]}
```

## Soft vs hard decision

- **Hard-decision**: the demodulator first slices each sample to a 0 or 1, then
  Viterbi uses **Hamming distance**.
- **Soft-decision**: Viterbi uses the *analog* received values (a confidence)
  with **Euclidean distance**. Soft decoding buys roughly **2 dB** of coding gain
  -- almost free, just keep more bits.

```matlab
K = 7; rate = 1/2;
states = 2^(K-1);             % 64-state trellis (the classic K=7 code)
```

```python
K = 7
states = 2**(K-1)            # 64-state trellis
```

> **Practical insight:** the K=7, rate-1/2 convolutional code with soft Viterbi
> was the workhorse of GSM, Wi-Fi (802.11a/g), and deep-space links for decades --
> often concatenated with a Reed-Solomon outer code (CD, DVB, Voyager).

**Next:** codes that reach the Shannon limit -- turbo, LDPC, polar.
""",
        ),
        _t(
            "Modern codes: turbo, LDPC & polar",
            "12 min",
            """\
# Modern codes: turbo, LDPC & polar

For 50 years a stubborn gap separated real codes from Shannon's limit. Three
families closed it, and they run inside every modern standard.

## Turbo codes (1993): iterate to near-capacity

Two simple convolutional encoders separated by an **interleaver**, decoded by
passing **soft probabilities** back and forth between two decoders that refine
each other's guesses -- "turbo" iteration. Suddenly engineers were within ~0.5 dB
of Shannon. Turbo codes powered 3G/4G data channels and many space missions.

## LDPC codes (1962, revived 1996): sparse parity, message passing

**Low-Density Parity-Check** codes use a huge but *sparse* parity-check matrix,
visualized as a bipartite **Tanner graph** of variable and check nodes. Decoding
passes belief messages along the edges until they agree:

```mermaid
flowchart TB
  V1["bit 1"] --- C1["check A"]
  V2["bit 2"] --- C1
  V2 --- C2["check B"]
  V3["bit 3"] --- C2
  V4["bit 4"] --- C1
  V4 --- C2
```

LDPC is now everywhere: Wi-Fi 6, 5G data channels, DVB-S2 satellite, 10G
Ethernet, SSDs. With long blocks it sits within a fraction of a dB of capacity.

## Polar codes (2009): provably capacity-achieving

**Channel polarization** transforms many identical channels into a set that are
either nearly **perfect** or nearly **useless**; you send data only on the good
ones. Polar codes are the first **provably** capacity-achieving construction and
were chosen for 5G **control** channels.

The story across the decades is a march toward the Shannon limit -- each
generation shaves the gap (illustrative):

```plot
{"title": "Gap to the Shannon limit shrinks over the decades (illustrative)", "xLabel": "code generation", "yLabel": "gap to capacity (dB, illustrative)", "xRange": [1, 5], "yRange": [0, 9], "grid": true, "series": [{"points": [[1, 8], [2, 4], [3, 2], [4, 0.5], [5, 0.3]], "label": "Hamming -> conv -> turbo -> LDPC -> polar", "color": "#2563eb"}]}
```

```matlab
% 5G NR uses LDPC for data, polar for control
data_code    = "LDPC";
control_code = "polar";
```

```python
data_code = "LDPC"           # 5G NR data channels
control_code = "polar"       # 5G NR control channels
```

> **Practical insight:** there is no single "best" code -- LDPC wins on long data
> blocks, polar on short control messages, and a CRC often rides *inside* the
> polar decoder to help it pick the right path (CRC-aided list decoding).

**Next:** beating multipath with many narrow carriers -- OFDM.
""",
        ),
        _t(
            "OFDM",
            "13 min",
            """\
# OFDM

A single wideband carrier suffers badly from frequency-selective fading (ISI).
**OFDM** (Orthogonal Frequency-Division Multiplexing) sidesteps this by sending
many **narrow** subcarriers in parallel -- each so narrow that its own channel
looks **flat**.

## Orthogonal subcarriers via the FFT

The subcarriers are spaced so their peaks land on each other's nulls --
**orthogonal** -- so they overlap in frequency yet do not interfere. The magic:
this exact set of orthogonal tones is computed by an **inverse FFT** at the
transmitter and an **FFT** at the receiver. Cheap silicon does the modulation:

```mermaid
flowchart LR
  BITS["bits"] --> QAM["map to QAM symbols"]
  QAM --> IFFT["IFFT (subcarriers -> time)"]
  IFFT --> CP["add cyclic prefix"]
  CP --> CH["channel"]
  CH --> RCP["remove CP"]
  RCP --> FFT["FFT (time -> subcarriers)"]
  FFT --> EQ["1-tap per-subcarrier equalize"]
```

Three overlapping orthogonal subcarriers -- each peaks where the others are zero:

```plot
{"title": "Orthogonal subcarriers: each peaks at the others' nulls", "xLabel": "frequency (subcarrier spacings)", "yLabel": "subcarrier response", "xRange": [-3, 3], "yRange": [-0.4, 1.1], "grid": true, "functions": [{"expr": "sin(pi*(x+1))/(pi*(x+1) + 0.0001)", "label": "k=-1", "color": "#2563eb"}, {"expr": "sin(pi*x)/(pi*x + 0.0001)", "label": "k=0", "color": "#16a34a"}, {"expr": "sin(pi*(x-1))/(pi*(x-1) + 0.0001)", "label": "k=+1", "color": "#dc2626"}]}
```

## The cyclic prefix: ISI immunity for free

OFDM copies the **end** of each symbol to its front -- the **cyclic prefix
(CP)**. As long as the channel's delay spread is shorter than the CP, multipath
echoes only smear into the disposable prefix, and each subcarrier sees a clean
**single complex multiply** as its channel. Equalization becomes one division per
subcarrier -- the per-subcarrier equalizer mentioned in the Intermediate course.

## PAPR: the catch

Summing many subcarriers occasionally lines them all up, producing a large
**peak-to-average power ratio (PAPR)**. That stresses the power amplifier (which
must stay linear up to the peaks, hurting efficiency). Slide the number of
subcarriers and watch the worst-case PAPR grow:

```plot
{"title": "OFDM worst-case PAPR grows with subcarrier count N", "xLabel": "number of subcarriers N", "yLabel": "peak/average power (dB)", "xRange": [4, 256], "yRange": [0, 25], "grid": true, "controls": [{"name": "scale", "range": [0.5, 1.5], "value": 1, "label": "PAPR back-off factor"}], "functions": [{"expr": "scale*10*log10(x)", "label": "PAPR ~ 10 log10(N)"}]}
```

```matlab
N = 64; cp = 16;
x = ifft(X, N);              % subcarrier symbols X -> time
xcp = [x(end-cp+1:end) x];   % prepend cyclic prefix
```

```python
import numpy as np
N, cp = 64, 16
x = np.fft.ifft(X)                 # X = subcarrier symbols
xcp = np.concatenate([x[-cp:], x]) # prepend cyclic prefix
```

> **Practical insight:** OFDM is the backbone of Wi-Fi (since 802.11a), 4G LTE,
> 5G NR downlink, DVB, and DSL. PAPR is its Achilles heel -- 5G uplink offers a
> lower-PAPR variant (DFT-spread OFDM) to spare phone battery and amplifier.

**Next:** using many antennas at once -- MIMO.
""",
        ),
        _t(
            "MIMO and spatial multiplexing",
            "12 min",
            """\
# MIMO and spatial multiplexing

**MIMO** (Multiple-Input Multiple-Output) puts several antennas at both ends and
exploits the *spatial* dimension. With $N_t$ transmit and $N_r$ receive antennas
the channel becomes a **matrix** $\\mathbf{H}$, and you can do remarkable things.

## Two prizes: multiplexing and diversity

- **Spatial multiplexing** sends **independent** data streams from each antenna.
  In a rich-scattering channel the receiver separates them by solving a linear
  system, multiplying capacity by $\\min(N_t, N_r)$ -- *more antennas, more bits*,
  no extra bandwidth or power.
- **Diversity** sends the **same** data over independent fading paths so it is
  unlikely *all* fade at once -- dramatically more reliable.

You cannot max both at once; you pick a point on the **diversity-multiplexing
tradeoff**. MIMO capacity grows linearly with the antenna count (slide $N_r$):

```plot
{"title": "MIMO capacity grows with min(Nt,Nr) (slide Nr)", "xLabel": "transmit antennas Nt", "yLabel": "capacity (x SISO)", "xRange": [1, 8], "yRange": [0, 9], "grid": true, "controls": [{"name": "Nr", "range": [1, 8], "value": 4, "label": "receive antennas Nr"}], "functions": [{"expr": "min(x, Nr)", "label": "approx capacity ~ min(Nt,Nr)"}]}
```

## Beamforming: aim the energy

With channel knowledge the transmitter can **weight** its antennas so the signals
**add in phase** at the intended receiver and cancel elsewhere -- a steerable
beam, with no moving parts. **Massive MIMO** (dozens to hundreds of antennas at a
5G base station) sharpens these beams and serves many users on the same
time/frequency by separating them in space:

```mermaid
flowchart LR
  TX1["antenna 1 (weight w1)"] --> AIR["combine in the air"]
  TX2["antenna 2 (weight w2)"] --> AIR
  TX3["antenna 3 (weight w3)"] --> AIR
  AIR --> UE["user (signals add in phase)"]
```

```matlab
H = (randn(4,4) + 1j*randn(4,4))/sqrt(2);   % 4x4 Rayleigh channel
SNR = 100;
C = log2(det(eye(4) + (SNR/4)*(H*H')));     % MIMO capacity (bits/s/Hz)
```

```python
import numpy as np
H = (np.random.randn(4,4) + 1j*np.random.randn(4,4))/np.sqrt(2)
SNR = 100
C = np.log2(np.real(np.linalg.det(np.eye(4) + (SNR/4)*(H @ H.conj().T))))
```

> **Practical insight:** MIMO + OFDM is the combination behind every modern high
> rate link -- the OFDM cyclic prefix turns the frequency-selective MIMO channel
> into many flat MIMO sub-channels you can solve one subcarrier at a time.

**Next:** simulate an OFDM symbol and the coding gain in code.
""",
        ),
        _code(
            "Lab: OFDM symbol & coding gain",
            "14 min",
            """\
# Two experiments: (1) build and recover one OFDM symbol through a multipath
# channel using the cyclic prefix; (2) measure the real coding gain of a
# Hamming(7,4) single-error-correcting code (BER with and without coding) over
# AWGN, with both links given the SAME energy per information bit.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2)

# ---------- 1) OFDM symbol through multipath ----------
N = 64                                   # subcarriers
cp = 16                                  # cyclic prefix length
qpsk = np.array([1+1j, 1-1j, -1+1j, -1-1j])/np.sqrt(2)
X = qpsk[rng.integers(0, 4, size=N)]     # subcarrier QAM symbols

x = np.fft.ifft(X)                       # OFDM time samples
xcp = np.concatenate([x[-cp:], x])       # add cyclic prefix

h = np.array([1.0, 0.0, 0.3, 0.0, 0.15])  # 5-tap multipath (shorter than CP)
y = np.convolve(xcp, h)[:len(xcp)]       # channel
y = y[cp:]                               # drop the prefix
Y = np.fft.fft(y)                        # back to subcarriers
Hf = np.fft.fft(h, N)                    # channel frequency response
Xeq = Y / Hf                             # one-tap per-subcarrier equalizer

# ---------- 2) Coding gain: Hamming(7,4) vs uncoded BPSK ----------
# Generator G (4x7) and parity-check H (3x7) over GF(2), systematic form.
G = np.array([
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
])
Hp = np.array([
    [1, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1],
])
# Syndrome (as a 0..7 integer) -> which of the 7 bit positions to flip (0 = none).
synd_int = (Hp[0] * 1 + Hp[1] * 2 + Hp[2] * 4).astype(int)   # syndrome of each unit error
err_pos = np.zeros(8, dtype=int)
for pos in range(7):
    err_pos[synd_int[pos]] = pos                              # map syndrome -> position

K = 40000                                                    # message blocks (x4 bits)
msg = rng.integers(0, 2, size=(K, 4))
code = (msg @ G) % 2                                         # 7-bit codewords

ebn0_db = np.arange(0, 11)
ber_unc = np.zeros_like(ebn0_db, dtype=float)
ber_cod = np.zeros_like(ebn0_db, dtype=float)
for j, db in enumerate(ebn0_db):
    ebn0 = 10**(db/10)

    # uncoded BPSK at full Eb
    ub = rng.integers(0, 2, size=4*K)
    nu = np.sqrt(1/(2*ebn0))*rng.standard_normal(4*K)
    ber_unc[j] = np.mean(((ub*2 - 1) + nu > 0).astype(int) != ub)

    # coded: rate 4/7, so each channel bit carries Ec = (4/7) Eb
    ec = (4/7)*ebn0
    tx = code*2 - 1
    nc = np.sqrt(1/(2*ec))*rng.standard_normal(code.shape)
    rx = (tx + nc > 0).astype(int)                           # hard decision
    syn = (rx @ Hp.T) % 2                                    # 3-bit syndrome per block
    syn_idx = syn[:, 0] + 2*syn[:, 1] + 4*syn[:, 2]
    flip = err_pos[syn_idx]                                  # position to correct
    corr = rx.copy()
    rows = np.arange(K)
    nz = syn_idx != 0
    corr[rows[nz], flip[nz]] ^= 1                            # flip the suspected bit
    dec = corr[:, :4]                                        # systematic -> data is first 4
    ber_cod[j] = np.mean(dec != msg)

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].plot(np.real(Xeq), np.imag(Xeq), "o", color="#2563eb", label="equalized")
ax[0].plot(np.real(qpsk), np.imag(qpsk), "x", ms=14, color="#dc2626", label="ideal")
ax[0].set_title("OFDM: recovered subcarriers after 1-tap equalize")
ax[0].set_xlabel("I"); ax[0].set_ylabel("Q")
ax[0].grid(True); ax[0].axis("equal"); ax[0].legend()

ax[1].semilogy(ebn0_db, np.maximum(ber_unc, 1e-6), "o-", color="#dc2626", label="uncoded BPSK")
ax[1].semilogy(ebn0_db, np.maximum(ber_cod, 1e-6), "s-", color="#16a34a", label="Hamming(7,4)")
ax[1].set_title("Coding gain: Hamming(7,4) beats uncoded at high SNR")
ax[1].set_xlabel("Eb/N0 (dB)"); ax[1].set_ylabel("BER")
ax[1].grid(True, which="both"); ax[1].legend()

plt.tight_layout(); plt.show()

evm = np.sqrt(np.mean(np.abs(Xeq - X)**2))
print(f"OFDM EVM after equalization ~ {evm:.3f} (small -> good recovery)")
print(f"uncoded BER     at 9 dB ~ {ber_unc[9]:.2e}")
print(f"Hamming(7,4) BER at 9 dB ~ {ber_cod[9]:.2e}  (lower -- that gap is coding gain)")

# Try it yourself:
#   1. Lengthen h beyond the CP (e.g. 20 taps): ISI returns, EVM blows up.
#   2. The MATLAB way: comm.OFDMModulator / ofdmmod and encode/decode(...,'hamming/binary').
""",
        ),
        _t(
            "Applications: 5G, Wi-Fi & satellite",
            "11 min",
            """\
# Applications: 5G, Wi-Fi & satellite

Everything in this track shows up, together, in the systems you use daily. The
**same toolbox** -- coding, modulation, OFDM, MIMO -- is retuned for each
environment's constraints.

## 5G NR (cellular)

- **Modulation**: adaptive QPSK up to 256-QAM (1024-QAM on great links).
- **Coding**: **LDPC** for the data channel, **polar** for control.
- **Waveform**: **OFDM** downlink; **DFT-spread OFDM** uplink (lower PAPR to save
  phone battery and amplifier headroom).
- **Antennas**: **massive MIMO** beamforming at the base station; mmWave bands
  for huge bandwidth at short range.

## Wi-Fi (802.11)

- **OFDM** since 802.11a; Wi-Fi 6/6E adds **OFDMA** (subcarrier groups to
  different users), up to 1024-QAM, MU-MIMO, and **LDPC**.
- Operates in unlicensed bands, so it leans on robust coding and retransmission
  (a CRC + ARQ back-channel) rather than raw link margin.

## Satellite and deep space

- **Power-limited**, bandwidth-rich: low-order modulation (QPSK, 8-PSK, APSK) plus
  the **strongest** codes. DVB-S2 uses **LDPC + BCH**; deep-space probes use
  concatenated convolutional + Reed-Solomon, and now LDPC/turbo, squeezing every
  fraction of a dB toward Shannon. The Voyager probes still phone home from
  interstellar space on a handful of watts thanks to coding gain.

```mermaid
flowchart LR
  TB["this track's toolbox"] --> FIVEG["5G: LDPC/polar + OFDM + massive MIMO"]
  TB --> WIFI["Wi-Fi: OFDMA + 1024-QAM + MU-MIMO"]
  TB --> SAT["satellite/deep space: APSK + LDPC/turbo"]
```

## The throughline

Compress to the entropy, protect with a near-capacity code, map to a
constellation as dense as the SNR allows, carry it on OFDM subcarriers to defeat
multipath, and multiply it across antennas with MIMO -- all to push as close to
$C = B\\log_2(1 + S/N)$ as physics permits. Different bands, different power
budgets, different standards; one unifying goal. Picking *where* each system sits
on the power-bandwidth plane is the whole game:

```plot
{"title": "Where systems sit on the power-bandwidth plane (illustrative)", "xLabel": "Eb/N0 available (dB)", "yLabel": "spectral efficiency (bits/s/Hz)", "xRange": [-2, 25], "yRange": [0, 11], "grid": true, "points": [{"x": 2, "y": 1, "label": "deep space / IoT", "color": "#16a34a", "size": 8}, {"x": 10, "y": 4, "label": "satellite TV", "color": "#2563eb", "size": 8}, {"x": 22, "y": 10, "label": "5G / Wi-Fi close-in", "color": "#dc2626", "size": 8}], "functions": [{"expr": "log2(1 + pow(10, x/10))", "label": "Shannon limit", "color": "#94a3b8"}]}
```

```matlab
B = 100e6; SNR_dB = 20;       % 5G mid-band, 100 MHz
C = B*log2(1 + 10^(SNR_dB/10));   % ~ 665 Mbit/s ceiling per stream
```

```python
import numpy as np
B, SNR_dB = 100e6, 20
C = B*np.log2(1 + 10**(SNR_dB/10))   # ~ 665 Mbit/s per stream
```

> **Practical insight:** when you read a standard, locate each block from this
> track -- the source codec, the FEC, the constellation, the OFDM numerology, the
> MIMO mode. They are always there, just retuned for the channel.

**Next:** the final check.
""",
        ),
    ),
)


DIGITAL_COMMS_COURSES: tuple[SeedCourse, ...] = (
    _DIGITAL_COMMS_BASICS,
    _DIGITAL_COMMS_INTERMEDIATE,
    _DIGITAL_COMMS_ADVANCED,
)

__all__ = ["DIGITAL_COMMS_COURSES"]
