"""Curated RF & Communication Systems track: Basics, Intermediate, Advanced.

A complete communications curriculum: analog comms fundamentals (the link model,
the decibel, SNR, AM/FM/PM, sampling and PCM, noise), digital communications
(ASK/FSK/PSK/QAM, pulse shaping, channel capacity, multiplexing/multiple access,
error-control coding), and RF/wireless (transceiver architecture, link budget and
propagation, antennas and arrays, OFDM and modern wireless, software-defined
radio, and real applications). Dual MATLAB + Python focus throughout, with
runnable Python labs (numpy + matplotlib), interactive ```plot blocks, Mermaid
diagrams, LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- RF & Communication Systems -- Basics --------------------------------------

_RF_COMMS_BASICS = SeedCourse(
    slug="rf-comms-basics",
    title="RF & Communication Systems -- Basics",
    description=(
        "Analog communications from the ground up: the transmitter/channel/"
        "receiver model, bandwidth and the decibel, signal-to-noise ratio, "
        "amplitude modulation and its sidebands, frequency and phase modulation, "
        "sampling/quantization/PCM, and noise - with side-by-side MATLAB and "
        "Python, interactive plots, and a runnable AM/FM modulation lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Communication system overview",
            "11 min",
            """\
# Communication system overview

Every communication system - a phone call, Wi-Fi, a deep-space probe - is the
same three-box chain: **transmitter**, **channel**, **receiver**.

```mermaid
flowchart LR
  SRC["source (voice, data)"] --> TX["transmitter: modulate + amplify"]
  TX --> CH["channel: cable / fiber / air"]
  CH --> RX["receiver: amplify + demodulate"]
  RX --> SINK["sink (speaker, screen)"]
  NOISE["noise + interference"] --> CH
```

The transmitter turns information into a signal the channel can carry; the
channel adds **attenuation, distortion, and noise**; the receiver recovers the
original information as best it can.

## Bandwidth: the most precious resource

**Bandwidth** $B$ is the span of frequencies a signal occupies (in Hz). It is
finite and shared - regulators auction it, and every system fights to send more
bits in less of it. A voice call needs ~$3.4$ kHz; FM radio ~$200$ kHz; a 5G
channel up to $100$ MHz.

## The decibel: ratios on a log scale

Signals span enormous ranges (a received signal can be a **trillionth** of the
transmitted one), so we use the **decibel**:

$$G_{dB} = 10\\,\\log_{10}\\!\\left(\\frac{P_{out}}{P_{in}}\\right), \\qquad
V_{dB} = 20\\,\\log_{10}\\!\\left(\\frac{V_{out}}{V_{in}}\\right).$$

A gain of $10\\times$ in power is $+10$ dB; $\\times 2$ is ~$+3$ dB; halving is
$-3$ dB. Decibels turn multiply/divide into add/subtract - so a whole signal
chain is just a sum. Slide the power ratio:

```plot
{"title": "The decibel: dB vs power ratio (slide the reference)", "xLabel": "power ratio Pout/Pin", "yLabel": "gain (dB)", "xRange": [0.1, 100], "yRange": [-12, 22], "grid": true, "controls": [{"name": "ref", "range": [0.5, 4], "value": 1, "label": "reference scale"}], "functions": [{"expr": "10*log10(x/ref)", "label": "G_dB = 10 log10(P/ref)"}]}
```

## Signal-to-noise ratio (SNR)

Quality is set not by raw signal strength but by signal **relative to noise**:

$$\\mathrm{SNR} = \\frac{P_{signal}}{P_{noise}}, \\qquad
\\mathrm{SNR_{dB}} = 10\\,\\log_{10}(\\mathrm{SNR}).$$

A high SNR sounds clear; a low SNR is static and dropped bits. Almost every
later idea - modulation choice, coding, capacity - is about spending bandwidth
and power to win SNR.

```matlab
Psig = 1e-3; Pnoise = 1e-6;
snr_dB  = 10*log10(Psig/Pnoise);   % 30 dB
gain_dB = 10*log10(1000);          % +30 dB power gain
```

```python
import numpy as np
Psig, Pnoise = 1e-3, 1e-6
snr_dB = 10*np.log10(Psig/Pnoise)  # 30 dB
gain_dB = 10*np.log10(1000)        # +30 dB
```

**Next:** the oldest way to put information on a carrier - amplitude modulation.
""",
        ),
        _t(
            "Amplitude modulation (AM)",
            "12 min",
            """\
# Amplitude modulation (AM)

To send a low-frequency **message** (audio) over the air you ride it on a
high-frequency **carrier**. **Amplitude modulation** does this by letting the
message vary the carrier's amplitude:

$$s(t) = A_c\\left[1 + m\\,x(t)\\right]\\cos(2\\pi f_c t),$$

where $x(t)$ is the normalized message, $f_c$ the carrier frequency, and $m$ the
**modulation index**. Slide $m$ and watch the envelope grow - past $m = 1$ the
signal **over-modulates** and the envelope distorts:

```plot
{"title": "AM waveform: carrier amplitude follows the message (slide index m)", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [-2.2, 2.2], "grid": true, "controls": [{"name": "m", "range": [0, 1.5], "value": 0.6, "label": "modulation index m"}], "functions": [{"expr": "(1 + m*sin(2*pi*2*x))*cos(2*pi*30*x)", "label": "AM signal", "color": "#2563eb"}, {"expr": "1 + m*sin(2*pi*2*x)", "label": "envelope", "color": "#dc2626"}]}
```

## Sidebands: where the bandwidth goes

Multiplying a carrier $f_c$ by a tone $f_m$ produces components at $f_c \\pm f_m$
- the **upper** and **lower sidebands**. A message of bandwidth $B$ therefore
occupies $2B$ around the carrier:

```plot
{"title": "AM spectrum: carrier plus two sidebands", "xLabel": "frequency (kHz)", "yLabel": "amplitude", "xRange": [990, 1010], "yRange": [0, 1.1], "grid": true, "series": [{"points": [[1000, 0], [1000, 1.0]], "label": "carrier", "color": "#2563eb"}, {"points": [[995, 0], [995, 0.4]], "label": "lower sideband", "color": "#16a34a"}, {"points": [[1005, 0], [1005, 0.4]], "label": "upper sideband", "color": "#16a34a"}]}
```

The carrier itself carries **no information** - it just locates the sidebands.
That waste motivates **DSB-SC** (suppress the carrier) and **SSB** (send only
one sideband, halving bandwidth) - the latter beloved by ham radio operators.

## Envelope detection: why AM won early

A conducting **diode** plus an RC low-pass follows the envelope $1 + m\\,x(t)$ -
a receiver with almost no parts. That cheap demodulator (the "crystal radio") is
why AM broadcast, born in the 1920s, blanketed the world.

```matlab
fc = 1000; fm = 50; m = 0.6; t = 0:1e-5:0.05;
x = sin(2*pi*fm*t);
s = (1 + m*x).*cos(2*pi*fc*t);     % AM signal
```

```python
import numpy as np
fc, fm, m = 1000, 50, 0.6
t = np.arange(0, 0.05, 1e-5)
x = np.sin(2*np.pi*fm*t)
s = (1 + m*x)*np.cos(2*np.pi*fc*t) # AM signal
```

> **Practical insight:** keep $m \\le 1$. Over-modulation clips the envelope,
> splatters energy into adjacent channels, and a simple envelope detector
> recovers garbage.

**Next:** put information in the *angle* instead - FM and PM.
""",
        ),
        _t(
            "Frequency & phase modulation (FM/PM)",
            "12 min",
            """\
# Frequency & phase modulation (FM/PM)

AM is fragile: noise adds to amplitude, and AM lives in amplitude. **Angle
modulation** instead encodes the message in the carrier's **phase** or
**frequency**, which a receiver can clip and limit clean - so it shrugs off
amplitude noise. That is why **FM radio** sounds hiss-free where AM crackles.

- **Phase modulation (PM):** phase follows the message, $\\phi(t) = k_p\\,x(t)$.
- **Frequency modulation (FM):** *instantaneous frequency* follows the message,
  $f(t) = f_c + k_f\\,x(t)$, so the phase is its integral.

$$s_{FM}(t) = A_c\\cos\\!\\left(2\\pi f_c t + 2\\pi k_f\\!\\int_0^t x(\\tau)\\,d\\tau\\right).$$

Slide the **deviation**: more deviation squeezes the cycles tighter on message
peaks and stretches them in the troughs:

```plot
{"title": "FM waveform: frequency follows the message (slide deviation)", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [-1.4, 1.4], "grid": true, "controls": [{"name": "beta", "range": [0, 8], "value": 4, "label": "deviation / beta"}], "functions": [{"expr": "cos(2*pi*20*x + beta*sin(2*pi*2*x))", "label": "FM signal"}]}
```

## Bandwidth: Carson's rule

Angle modulation spreads energy over many sidebands. **Carson's rule** estimates
the bandwidth from the peak frequency deviation $\\Delta f$ and the highest
message frequency $f_m$:

$$B \\approx 2(\\Delta f + f_m).$$

Wideband FM trades **bandwidth for noise immunity** - broadcast FM uses $\\pm 75$
kHz deviation in a $200$ kHz channel to sound pristine.

```mermaid
flowchart LR
  MSG["message x(t)"] --> INT["integrate (FM only)"]
  INT --> VCO["phase = carrier + k * signal"]
  VCO --> OUT["angle-modulated carrier"]
```

```matlab
fc = 2000; fm = 100; kf = 600; t = 0:1e-5:0.05;
x = sin(2*pi*fm*t);
phi = 2*pi*kf*cumsum(x)*1e-5;      % integrate the message
s = cos(2*pi*fc*t + phi);          % FM signal
```

```python
import numpy as np
fc, fm, kf = 2000, 100, 600
t = np.arange(0, 0.05, 1e-5)
x = np.sin(2*np.pi*fm*t)
phi = 2*np.pi*kf*np.cumsum(x)*1e-5 # integrate the message
s = np.cos(2*np.pi*fc*t + phi)     # FM signal
```

> **Practical insight:** FM/PM are the backbone of analog two-way radio, the
> first cellular systems, and the **subcarriers** of digital schemes. The price
> for noise immunity is bandwidth - and a threshold below which FM fails sharply.

**Next:** crossing into the digital world - sampling, quantization, and PCM.
""",
        ),
        _t(
            "Sampling, quantization & PCM",
            "12 min",
            """\
# Sampling, quantization & PCM

To process voice or video with computers we must **digitize** it - three steps:
**sample** in time, **quantize** in amplitude, then **code** into bits (**PCM**,
pulse-code modulation - the format of CDs, telephony, and Wi-Fi voice).

## 1. Sampling and the Nyquist rate

Measure the analog signal at a steady rate $f_s$. The **Nyquist-Shannon theorem**
says you can perfectly reconstruct a signal of bandwidth $B$ if

$$f_s > 2B.$$

Sample too slowly and high frequencies masquerade as low ones - **aliasing**.
Slide the sample rate and watch a slow "alias" appear when $f_s$ drops below
twice the signal frequency:

```plot
{"title": "Aliasing: too few samples create a phantom low frequency (slide fs)", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "fs", "range": [3, 40], "value": 9, "label": "sample rate fs"}], "functions": [{"expr": "sin(2*pi*8*x)", "label": "true 8 Hz signal", "color": "#2563eb"}, {"expr": "sin(2*pi*8*(round(x*fs)/fs))", "label": "sampled + held", "color": "#dc2626"}]}
```

That is why an audio CD samples at $44.1$ kHz (above $2 \\times 20$ kHz) and you
put an **anti-alias filter** before any sampler.

## 2. Quantization and its noise

Each sample is rounded to one of $L = 2^n$ levels for an $n$-bit code. Rounding
introduces **quantization noise**; the resulting SNR climbs ~$6$ dB per bit:

$$\\mathrm{SNR_{dB}} \\approx 6.02\\,n + 1.76.$$

Slide bit depth and watch the staircase get finer:

```plot
{"title": "Quantization staircase: more bits = finer steps (slide bits)", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [-1.2, 1.2], "grid": true, "controls": [{"name": "bits", "range": [1, 5], "value": 3, "label": "resolution (bits)"}], "functions": [{"expr": "sin(2*pi*x)", "label": "analog", "color": "#94a3b8"}, {"expr": "round(sin(2*pi*x)*pow(2,bits-1))/pow(2,bits-1)", "label": "quantized", "color": "#2563eb"}]}
```

## 3. Coding to bits (PCM)

Map each level to a binary word and you have a bit stream ready for the digital
modulation of the next course.

```mermaid
flowchart LR
  ANALOG["analog in"] --> SH["sample + hold (fs > 2B)"]
  SH --> Q["quantize to 2^n levels"]
  Q --> ENC["encode to bits (PCM)"]
  ENC --> BITS["bit stream"]
```

```matlab
n = 8; L = 2^n;
snr_dB = 6.02*n + 1.76;            % ~50 dB for 8-bit
xq = round(x*(L/2))/(L/2);         % quantize a normalized signal
```

```python
import numpy as np
n = 8; L = 2**n
snr_dB = 6.02*n + 1.76             # ~50 dB for 8-bit
xq = np.round(x*(L/2))/(L/2)       # quantize a normalized signal
```

> **Practical insight:** telephone PCM uses 8 bits at 8 kHz (64 kbit/s) with
> companding so quiet sounds get more levels. CD audio uses 16 bits at 44.1 kHz.
> Bits-per-sample buys SNR; samples-per-second buys bandwidth.

**Next:** the enemy that sets all these limits - noise.
""",
        ),
        _t(
            "Noise & SNR",
            "11 min",
            """\
# Noise & SNR

Every receiver fights **noise** - random fluctuations that bury weak signals and
flip bits. Understanding it sets the floor for everything else.

## Thermal (Johnson-Nyquist) noise

Any resistor at temperature $T$ generates noise power proportional to bandwidth:

$$P_n = k_B\\,T\\,B,$$

where $k_B = 1.38 \\times 10^{-23}$ J/K. At room temperature this is about
$-174$ dBm per hertz of bandwidth - the fundamental floor. **Wider bandwidth =
more noise**, one more reason bandwidth is precious. Slide temperature:

```plot
{"title": "Thermal noise power vs bandwidth (slide temperature)", "xLabel": "bandwidth B (MHz)", "yLabel": "noise power (relative)", "xRange": [0, 100], "yRange": [0, 4.5], "grid": true, "controls": [{"name": "T", "range": [100, 400], "value": 290, "label": "temperature T (K)"}], "functions": [{"expr": "(T/290)*(x/100)*4", "label": "Pn = k T B (scaled)"}]}
```

## Noise figure: how much a stage degrades SNR

Every amplifier and mixer adds its own noise. The **noise figure** $F$ (in dB)
measures how much a stage worsens the SNR:

$$F_{dB} = \\mathrm{SNR_{in,dB}} - \\mathrm{SNR_{out,dB}}.$$

Cascaded stages combine by **Friis' noise formula** - the *first* stage
dominates, which is why a receiver's front-end **low-noise amplifier** (LNA)
matters most.

## From SNR to bit errors

For digital links the figure of merit is $E_b/N_0$ (energy per bit over noise
density). Higher $E_b/N_0$ means a lower **bit-error rate** (BER). The
relationship is a steep "waterfall" - a few dB of SNR can take BER from awful to
essentially error-free:

```plot
{"title": "BER waterfall: bit-error rate falls steeply with SNR", "xLabel": "Eb/N0 (dB)", "yLabel": "log10(BER)", "xRange": [0, 12], "yRange": [-7, 0], "grid": true, "functions": [{"expr": "log10(0.5*exp(-pow(10,x/10)/2))", "label": "approx log10(BER)"}]}
```

```matlab
kB = 1.38e-23; T = 290; B = 1e6;
Pn_dBm = 10*log10(kB*T*B/1e-3);    % ~ -114 dBm in 1 MHz
F_dB = SNR_in_dB - SNR_out_dB;     % noise figure
```

```python
import numpy as np
kB, T, B = 1.38e-23, 290, 1e6
Pn_dBm = 10*np.log10(kB*T*B/1e-3)  # ~ -114 dBm in 1 MHz
# F_dB = SNR_in_dB - SNR_out_dB    # noise figure of a stage
```

> **Practical insight:** to improve a link you can raise transmit power, narrow
> bandwidth, lower the receiver noise figure (better LNA, cooler front-end), or
> add coding gain (Intermediate course). Each buys SNR differently.

**Next:** build a modulator yourself and see its spectrum.
""",
        ),
        _code(
            "Lab: AM/FM modulate a tone & plot the spectrum",
            "13 min",
            """\
# Modulate a message tone with AM and FM, then view the time waveforms and
# their spectra with the FFT. Watch AM make two sidebands and FM spread many.
import numpy as np
import matplotlib.pyplot as plt

fs = 100000                      # sample rate (Hz)
T = 0.05                         # 50 ms
t = np.arange(0, T, 1/fs)

fc = 5000.0                      # carrier frequency (Hz)
fm = 200.0                       # message tone (Hz)
m = 0.7                          # AM modulation index
kf = 3000.0                      # FM frequency deviation (Hz)

msg = np.sin(2*np.pi*fm*t)
carrier = np.cos(2*np.pi*fc*t)

# AM: amplitude follows (1 + m*msg)
am = (1 + m*msg)*carrier

# FM: instantaneous phase is the integral of the message
phase = 2*np.pi*fc*t + 2*np.pi*kf*np.cumsum(msg)/fs
fm_sig = np.cos(phase)

# Single-sided magnitude spectra via the FFT
N = len(t)
freqs = np.fft.rfftfreq(N, 1/fs)
AM_spec = np.abs(np.fft.rfft(am))/N
FM_spec = np.abs(np.fft.rfft(fm_sig))/N

fig, ax = plt.subplots(2, 2, figsize=(11, 6))
ax[0, 0].plot(t[:500]*1e3, am[:500], color="#2563eb")
ax[0, 0].set_title("AM time waveform"); ax[0, 0].set_xlabel("time (ms)")
ax[0, 1].plot(freqs, AM_spec, color="#2563eb")
ax[0, 1].set_xlim(fc-1500, fc+1500); ax[0, 1].set_title("AM spectrum (carrier + 2 sidebands)")
ax[1, 0].plot(t[:500]*1e3, fm_sig[:500], color="#dc2626")
ax[1, 0].set_title("FM time waveform"); ax[1, 0].set_xlabel("time (ms)")
ax[1, 1].plot(freqs, FM_spec, color="#dc2626")
ax[1, 1].set_xlim(fc-6000, fc+6000); ax[1, 1].set_title("FM spectrum (many sidebands)")
for a in ax.ravel():
    a.grid(True)
plt.tight_layout(); plt.show()

carson_bw = 2*(kf + fm)
print(f"AM occupies ~ {2*fm:.0f} Hz around the carrier")
print(f"FM Carson bandwidth ~ {carson_bw:.0f} Hz")

# Try it yourself:
#   1. Raise kf to 8000: the FM spectrum spreads much wider (Carson's rule).
#   2. Set m = 1.2 (over-modulation) and inspect the distorted AM envelope.
#   3. The MATLAB equivalent uses fft() and abs() the same way.
""",
        ),
    ),
)


# -- RF & Communication Systems -- Intermediate --------------------------------

_RF_COMMS_INTERMEDIATE = SeedCourse(
    slug="rf-comms-intermediate",
    title="RF & Communication Systems -- Intermediate: Digital Comms",
    description=(
        "Digital communications: ASK/FSK/PSK/QAM and constellation diagrams, "
        "spectra and pulse shaping (raised cosine, ISI), channel capacity and the "
        "Shannon limit, multiplexing and multiple access (FDM/TDM/CDMA/OFDM), and "
        "error-control coding (parity, Hamming, FEC, interleaving) - with dual "
        "MATLAB/Python, interactive plots, and a runnable QAM constellation lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Digital modulation: ASK, FSK, PSK & QAM",
            "12 min",
            """\
# Digital modulation: ASK, FSK, PSK & QAM

Digital modulation maps **bits** onto a carrier by varying one of its three
properties - amplitude, frequency, or phase:

| Scheme | Varies | Bit carried by | Real use |
|--------|--------|----------------|----------|
| **ASK** | amplitude | on/off level | optical fiber, RFID |
| **FSK** | frequency | one of two tones | Bluetooth, old modems |
| **PSK** | phase | phase shift | Wi-Fi, satellite |
| **QAM** | amplitude + phase | a point in the I/Q plane | cable, LTE, Wi-Fi |

Binary phase-shift keying (**BPSK**) flips the carrier $180^\\circ$ for a 0 vs a
1. Slide the bit value and watch the phase invert:

```plot
{"title": "BPSK: a bit flips the carrier phase by 180 degrees (slide bit)", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "bit", "range": [0, 1], "value": 1, "label": "transmitted bit"}], "functions": [{"expr": "cos(2*pi*5*x + (bit<0.5)*pi)", "label": "BPSK carrier"}]}
```

## The constellation diagram

Plot each symbol as a point in the **I/Q plane** (in-phase vs quadrature) and you
get a **constellation**. More points = more bits per symbol, but points crowd
closer and noise more easily confuses them. **QPSK** packs 2 bits into 4 phases:

```plot
{"title": "QPSK constellation: 4 phases, 2 bits per symbol", "xLabel": "I (in-phase)", "yLabel": "Q (quadrature)", "xRange": [-1.5, 1.5], "yRange": [-1.5, 1.5], "grid": true, "points": [{"x": 0.707, "y": 0.707, "label": "00", "color": "#2563eb", "size": 8}, {"x": -0.707, "y": 0.707, "label": "01", "color": "#2563eb", "size": 8}, {"x": -0.707, "y": -0.707, "label": "11", "color": "#2563eb", "size": 8}, {"x": 0.707, "y": -0.707, "label": "10", "color": "#2563eb", "size": 8}]}
```

**16-QAM** packs **4 bits** into 16 points on a grid - quadrupling data rate over
BPSK at the cost of needing more SNR:

```plot
{"title": "16-QAM constellation: 16 points, 4 bits per symbol", "xLabel": "I", "yLabel": "Q", "xRange": [-4, 4], "yRange": [-4, 4], "grid": true, "points": [{"x": -3, "y": -3, "color": "#16a34a", "size": 6}, {"x": -3, "y": -1, "color": "#16a34a", "size": 6}, {"x": -3, "y": 1, "color": "#16a34a", "size": 6}, {"x": -3, "y": 3, "color": "#16a34a", "size": 6}, {"x": -1, "y": -3, "color": "#16a34a", "size": 6}, {"x": -1, "y": -1, "color": "#16a34a", "size": 6}, {"x": -1, "y": 1, "color": "#16a34a", "size": 6}, {"x": -1, "y": 3, "color": "#16a34a", "size": 6}, {"x": 1, "y": -3, "color": "#16a34a", "size": 6}, {"x": 1, "y": -1, "color": "#16a34a", "size": 6}, {"x": 1, "y": 1, "color": "#16a34a", "size": 6}, {"x": 1, "y": 3, "color": "#16a34a", "size": 6}, {"x": 3, "y": -3, "color": "#16a34a", "size": 6}, {"x": 3, "y": -1, "color": "#16a34a", "size": 6}, {"x": 3, "y": 1, "color": "#16a34a", "size": 6}, {"x": 3, "y": 3, "color": "#16a34a", "size": 6}]}
```

Bits per symbol is $\\log_2 M$ for an $M$-point constellation: QPSK gives 2,
16-QAM gives 4, 256-QAM (cable, Wi-Fi 6) gives 8.

```matlab
M = 16; k = log2(M);               % 4 bits/symbol
bits = [1 0 1 1];
I = 2*bits(1) - 1; Q = 2*bits(3) - 1;   % map to I/Q (toy)
sym = I + 1j*Q;
```

```python
import numpy as np
M = 16; k = np.log2(M)             # 4 bits/symbol
bits = [1, 0, 1, 1]
I = 2*bits[0] - 1; Q = 2*bits[2] - 1
sym = I + 1j*Q
```

> **Practical insight:** modern links **adapt** the constellation to the channel
> - 256-QAM when SNR is high (close to the router), dropping to QPSK at the cell
> edge. Denser constellations need more SNR for the same error rate.

**Next:** the pulse shape that decides how much bandwidth those symbols cost.
""",
        ),
        _t(
            "Spectra & pulse shaping",
            "12 min",
            """\
# Spectra & pulse shaping

A symbol is sent as a **pulse**. The pulse's *shape* sets the signal's bandwidth
and whether neighboring symbols smear into each other - **inter-symbol
interference** (ISI).

## The problem with square pulses

A rectangular pulse is compact in time but its spectrum is a **sinc** - wide
tails that spill into adjacent channels. Conversely an ideal **brick-wall**
spectrum gives a sinc pulse in time, whose ringing causes ISI. You cannot have
both perfectly; you engineer the trade.

```plot
{"title": "Sinc pulse: a band-limited symbol shape (zeros at integer symbol times)", "xLabel": "time / symbol", "yLabel": "amplitude", "xRange": [-4, 4], "yRange": [-0.35, 1.1], "grid": true, "functions": [{"expr": "sin(pi*x)/(pi*x + (x==0))", "label": "sinc pulse"}]}
```

Notice the sinc is **zero at every other integer** - so if you sample exactly at
the symbol centers, neighbors contribute nothing. That is the **Nyquist ISI
criterion**.

## The raised-cosine pulse

The practical workhorse is the **raised-cosine** pulse, with a **roll-off
factor** $\\alpha$ between 0 and 1. It keeps the zero-ISI property while trading a
little excess bandwidth ($1+\\alpha$ times the minimum) for gentler, shorter
tails. Slide $\\alpha$ to widen the spectrum but tame the time-domain ringing:

```plot
{"title": "Raised-cosine spectrum: roll-off alpha trades bandwidth for gentleness", "xLabel": "frequency / symbol rate", "yLabel": "|H|", "xRange": [-1, 1], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "a", "range": [0.05, 1], "value": 0.35, "label": "roll-off alpha"}], "functions": [{"expr": "(abs(x) < (1-a)/2)*1 + (abs(x) >= (1-a)/2)*(abs(x) <= (1+a)/2)*0.5*(1 + cos(pi/a*(abs(x) - (1-a)/2)))", "label": "raised cosine |H|"}]}
```

Typical systems use $\\alpha = 0.2$ to $0.35$ (LTE uses ~$0.22$): a small
bandwidth penalty for robust, ISI-free detection.

```mermaid
flowchart LR
  BITS["bit stream"] --> MAP["map to symbols (QAM)"]
  MAP --> RRC["root-raised-cosine filter"]
  RRC --> UP["upconvert to carrier"]
```

```matlab
alpha = 0.35; Rs = 1e6;            % roll-off, symbol rate
BW = (1 + alpha)*Rs;               % occupied bandwidth -> 1.35 MHz
```

```python
alpha, Rs = 0.35, 1e6
BW = (1 + alpha)*Rs                # occupied bandwidth -> 1.35 MHz
```

> **Practical insight:** the filter is usually split as **root-raised-cosine** at
> both transmitter and receiver; the two multiply to a full raised cosine, and
> the receiver half also acts as a matched filter that maximizes SNR.

**Next:** the hard ceiling on data rate - Shannon's law.
""",
        ),
        _t(
            "Channel capacity & the Shannon limit",
            "11 min",
            """\
# Channel capacity & the Shannon limit

How fast can you *possibly* send data, error-free, over a noisy channel? In 1948
Claude Shannon answered it exactly - founding information theory. The
**capacity** of a channel of bandwidth $B$ with signal-to-noise ratio SNR is:

$$C = B\\,\\log_2\\!\\left(1 + \\mathrm{SNR}\\right) \\quad \\text{bits per second}.$$

No code, no modulation, no cleverness can beat $C$. Below it, error-free
communication is possible; above it, impossible. Slide the SNR (in dB) and watch
capacity climb - roughly linearly in dB, since each doubling of SNR adds ~$1$
bit/s/Hz:

```plot
{"title": "Shannon capacity vs SNR (per Hz of bandwidth)", "xLabel": "SNR (dB)", "yLabel": "capacity (bits/s per Hz)", "xRange": [0, 40], "yRange": [0, 14], "grid": true, "controls": [{"name": "B", "range": [1, 5], "value": 1, "label": "bandwidth scale"}], "functions": [{"expr": "B*log2(1 + pow(10, x/10))", "label": "C/B = log2(1 + SNR)"}]}
```

## The two ways to buy bits

Capacity grows **linearly with bandwidth** but only **logarithmically with
power/SNR**. So:

- Doubling bandwidth roughly doubles capacity (cheap, if you have spectrum).
- Doubling power adds only ~$1$ bit/s/Hz (diminishing returns).

This is why 5G chases wide millimeter-wave bandwidth rather than brute power, and
why deep-space links - power-starved but bandwidth-rich - lean on heavy coding.

## Spectral efficiency and the modulation ladder

**Spectral efficiency** (bits/s/Hz) is how close a real system gets to $C/B$.
Each step up the constellation ladder needs more SNR:

```plot
{"title": "SNR needed climbs as you add bits per symbol", "xLabel": "bits per symbol", "yLabel": "approx required SNR (dB)", "xRange": [1, 8], "yRange": [0, 35], "grid": true, "series": [{"points": [[1, 7], [2, 10], [4, 17], [6, 24], [8, 30]], "label": "BPSK to 256-QAM", "color": "#2563eb"}]}
```

```matlab
B = 20e6; snr_dB = 25;
snr = 10^(snr_dB/10);
C = B*log2(1 + snr);               % ~166 Mbit/s in 20 MHz at 25 dB
```

```python
import numpy as np
B, snr_dB = 20e6, 25
snr = 10**(snr_dB/10)
C = B*np.log2(1 + snr)             # ~166 Mbit/s
```

> **Practical insight:** Shannon promises capacity is *reachable* but does not
> say how. Modern **turbo** and **LDPC** codes get within a fraction of a dB of
> the limit - the payoff of the error-control coding lesson.

**Next:** sharing one channel among many users.
""",
        ),
        _t(
            "Multiplexing & multiple access",
            "12 min",
            """\
# Multiplexing & multiple access

One physical medium - a fiber, a cable, the air - must usually carry **many**
signals or serve **many** users. **Multiplexing** combines signals; **multiple
access** lets many users share. They split the same resources: frequency, time,
code, or space.

```mermaid
flowchart LR
  U1["user 1"] --> MUX["multiplexer"]
  U2["user 2"] --> MUX
  U3["user 3"] --> MUX
  MUX --> CH["shared channel"]
  CH --> DEMUX["demultiplexer"]
  DEMUX --> O1["user 1"]
  DEMUX --> O2["user 2"]
  DEMUX --> O3["user 3"]
```

| Method | Splits by | Example |
|--------|-----------|---------|
| **FDM / FDMA** | frequency bands | radio/TV channels, 1G cellular |
| **TDM / TDMA** | time slots | 2G GSM, digital telephony trunks |
| **CDMA** | orthogonal codes | 3G cellular, GPS |
| **OFDM / OFDMA** | many narrow orthogonal subcarriers | Wi-Fi, LTE, 5G |
| **SDMA** | space (beams/antennas) | MIMO, massive MIMO |

## FDM: stack signals in frequency

Give each signal its own frequency band with **guard bands** between them. Slide
the channel spacing - too tight and the bands overlap and interfere:

```plot
{"title": "FDM: signals in separate frequency bands (slide spacing)", "xLabel": "frequency", "yLabel": "amplitude", "xRange": [0, 10], "yRange": [0, 1.2], "grid": true, "controls": [{"name": "d", "range": [1.5, 4], "value": 3, "label": "channel spacing"}], "functions": [{"expr": "exp(-pow((x-2)*3, 2))", "label": "channel 1", "color": "#2563eb"}, {"expr": "exp(-pow((x-2-d)*3, 2))", "label": "channel 2", "color": "#dc2626"}]}
```

## TDM: take turns in time

Interleave users into repeating **time slots**. Each user gets the full bandwidth
but only part of the time. Tight synchronization is the catch.

## CDMA: everyone at once, separated by code

All users transmit in the same band at the same time, each multiplied by a unique
**spreading code**. Because the codes are (near-)orthogonal, a receiver
correlating with one user's code recovers it and treats the others as low-level
noise. This **spread spectrum** also resists jamming and interception - which is
why it began in the military and powers GPS.

```matlab
% TDMA: N users share a frame of duration Tframe
N = 8; Tframe = 1e-3;
slot = Tframe/N;                   % each user's slot length
```

```python
N, Tframe = 8, 1e-3
slot = Tframe/N                    # each user's time slot
```

> **Practical insight:** real systems mix these. LTE uses **OFDMA** (frequency +
> time tiles) plus **SDMA** via MIMO; Wi-Fi 6 added OFDMA so an access point can
> serve many devices in one transmission. OFDM gets its own Advanced lesson.

**Next:** detecting and fixing the errors noise causes - coding.
""",
        ),
        _t(
            "Error-control coding",
            "12 min",
            """\
# Error-control coding

Noise will flip bits no matter how clean the link. **Error-control coding** adds
structured **redundancy** so the receiver can *detect* and even *correct* errors
- trading a little rate for a lot of reliability.

## Detect: parity and checksums

Append a **parity bit** so every codeword has an even number of ones; a single
flipped bit breaks parity and is detected (but not located). **CRCs** generalize
this to catch bursts - they guard Ethernet frames, ZIP files, and disk sectors.

## Correct: the Hamming code

Add several parity bits, each checking an overlapping subset of data bits. Their
combined "yes/no" answers form a **syndrome** that points straight at the flipped
bit. The **Hamming(7,4)** code sends 4 data bits as 7 and corrects any single-bit
error:

```mermaid
flowchart LR
  D["4 data bits"] --> ENC["Hamming(7,4) encoder"]
  ENC --> TX["7-bit codeword"]
  TX --> CH["noisy channel"]
  CH --> DEC["decoder: compute syndrome"]
  DEC --> FIX["locate + flip the bad bit"]
  FIX --> OUT["4 data bits recovered"]
```

## Forward error correction (FEC) and coding gain

**FEC** corrects at the receiver with no retransmission - essential for
broadcast and deep space. Stronger codes give more **coding gain**: the same BER
at lower SNR. The effect is to shift the BER waterfall **left** - slide the gain:

```plot
{"title": "Coding gain shifts the BER curve left (slide gain in dB)", "xLabel": "Eb/N0 (dB)", "yLabel": "log10(BER)", "xRange": [0, 12], "yRange": [-7, 0], "grid": true, "controls": [{"name": "g", "range": [0, 6], "value": 3, "label": "coding gain (dB)"}], "functions": [{"expr": "log10(0.5*exp(-pow(10,x/10)/2))", "label": "uncoded", "color": "#94a3b8"}, {"expr": "log10(0.5*exp(-pow(10,(x+g)/10)/2))", "label": "coded", "color": "#2563eb"}]}
```

A code's **rate** is data bits over total bits: Hamming(7,4) is rate $4/7$. Modern
**turbo** and **LDPC** codes operate within a fraction of a dB of the Shannon
limit and protect LTE, 5G, Wi-Fi, and satellite links.

## Interleaving: defeating burst errors

Fading and scratches cause **bursts** of adjacent errors, which overwhelm codes
that fix scattered errors. **Interleaving** shuffles bits before transmission and
unshuffles them after, so a burst is spread into isolated errors the code can
handle - the trick behind CD scratch-resistance and mobile reception.

```matlab
% Code rate of Hamming(7,4)
k = 4; n = 7;
rate = k/n;                        % 0.571
```

```python
k, n = 4, 7
rate = k/n                         # 0.571
```

> **Practical insight:** there is no free lunch - coding spends bandwidth/rate to
> buy reliability. The art is matching code strength to the channel: light coding
> on a clean fiber, heavy LDPC + interleaving on a fading mobile link.

**Next:** see noise corrupt a real constellation - the QAM lab.
""",
        ),
        _code(
            "Lab: QAM constellation with noise & an eye diagram",
            "13 min",
            """\
# Generate a 16-QAM signal, add channel noise, and view the constellation as
# SNR varies - plus an eye diagram showing ISI margin. Pure numpy + matplotlib.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)
num_symbols = 800
snr_dB = 18.0                    # try 25 (clean) vs 10 (smeared)

# 16-QAM: I and Q each take levels {-3,-1,1,3}
levels = np.array([-3, -1, 1, 3])
I = rng.choice(levels, num_symbols)
Q = rng.choice(levels, num_symbols)
symbols = I + 1j*Q

# Add complex Gaussian noise scaled to the chosen SNR
sig_power = np.mean(np.abs(symbols)**2)
snr_lin = 10**(snr_dB/10)
noise_power = sig_power/snr_lin
noise = np.sqrt(noise_power/2)*(rng.standard_normal(num_symbols)
                                + 1j*rng.standard_normal(num_symbols))
rx = symbols + noise

# Eye diagram: oversample raised-cosine-ish pulses for one I rail
sps = 20                         # samples per symbol
bits = rng.choice([-1, 1], 60)
t = np.linspace(-2, 2, sps)
pulse = np.sinc(t)*np.cos(0.5*np.pi*t)   # damped sinc-like pulse
wave = np.zeros((len(bits)-1)*sps)
for i, b in enumerate(bits[:-1]):
    wave[i*sps:(i+1)*sps] += b*pulse[:sps]

fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
ax[0].scatter(rx.real, rx.imag, s=8, alpha=0.5, color="#2563eb")
ax[0].scatter(levels.repeat(4), np.tile(levels, 4), s=60,
              marker="x", color="#dc2626")
ax[0].set_title(f"16-QAM constellation at {snr_dB:.0f} dB SNR")
ax[0].set_xlabel("I"); ax[0].set_ylabel("Q"); ax[0].grid(True)
ax[0].set_aspect("equal")

for i in range(len(bits)-2):
    seg = wave[i*sps:(i+2)*sps]
    if len(seg) == 2*sps:
        ax[1].plot(seg, color="#16a34a", alpha=0.3)
ax[1].set_title("Eye diagram (open eye = good margin)")
ax[1].set_xlabel("sample within 2 symbols"); ax[1].grid(True)
plt.tight_layout(); plt.show()

# Decision: round each received symbol to the nearest constellation point
def nearest(v):
    return levels[np.argmin(np.abs(levels - v))]

I_hat = np.array([nearest(v) for v in rx.real])
Q_hat = np.array([nearest(v) for v in rx.imag])
errors = np.sum((I_hat != I) | (Q_hat != Q))
print(f"symbol errors: {errors} / {num_symbols} at {snr_dB:.0f} dB SNR")

# Try it yourself:
#   1. Drop snr_dB to 10: the clusters merge and errors jump.
#   2. Raise it to 25: tight clusters, near-zero errors, wide-open eye.
""",
        ),
    ),
)


# -- RF & Communication Systems -- Advanced ------------------------------------

_RF_COMMS_ADVANCED = SeedCourse(
    slug="rf-comms-advanced",
    title="RF & Communication Systems -- Advanced: RF & Wireless",
    description=(
        "RF and wireless engineering: transceiver architecture (LNA, mixer, "
        "superheterodyne, IQ conversion), the link budget and propagation (Friis, "
        "path loss, fading), antennas and arrays (gain, beamforming, MIMO), OFDM "
        "and modern wireless (Wi-Fi/LTE/5G, cyclic prefix), software-defined radio "
        "and DSP, and real applications (5G, satellite, IoT, radar) - with dual "
        "MATLAB/Python, interactive plots, and a runnable link-budget/OFDM lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "RF front-end & transceiver architecture",
            "13 min",
            """\
# RF front-end & transceiver architecture

A radio's **front-end** is the chain of analog blocks between the antenna and the
digital signal processor. Its job: take a femtowatt signal buried in noise and
deliver clean baseband bits - or the reverse on transmit.

```mermaid
flowchart LR
  ANT["antenna"] --> LNA["LNA: low-noise amplify"]
  LNA --> MIX["mixer: shift frequency"]
  LO["local oscillator"] --> MIX
  MIX --> IF["IF filter + amplify"]
  IF --> ADC["ADC -> DSP"]
```

## The key building blocks

- **LNA (low-noise amplifier):** the *first* stage. By Friis' formula it sets the
  whole receiver's noise figure, so it must add almost no noise of its own.
- **Mixer:** multiplies the signal by a **local oscillator (LO)**, shifting it to
  a new frequency. Multiplying two sinusoids creates sum and difference
  frequencies - the **heterodyne** principle.
- **Filters:** select the wanted band and reject images and out-of-band junk.
- **PA (power amplifier):** on transmit, boosts the signal to watts. Its
  efficiency and linearity dominate a phone's battery and signal quality.

## Mixing: the heart of frequency conversion

Multiply $\\cos(2\\pi f_{RF} t)$ by $\\cos(2\\pi f_{LO} t)$ and you get components at
$f_{RF} \\pm f_{LO}$:

$$\\cos(A)\\cos(B) = \\tfrac{1}{2}\\cos(A-B) + \\tfrac{1}{2}\\cos(A+B).$$

Slide the LO frequency to see the difference (downconverted) tone move:

```plot
{"title": "Mixer output: product of RF and LO makes sum + difference tones (slide LO)", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [-1.2, 1.2], "grid": true, "controls": [{"name": "flo", "range": [6, 14], "value": 8, "label": "LO frequency"}], "functions": [{"expr": "0.5*cos(2*pi*(10-flo)*x) + 0.5*cos(2*pi*(10+flo)*x)", "label": "mixer output (RF=10)"}]}
```

## Superheterodyne vs direct conversion

- **Superheterodyne** (Armstrong, 1918): mix down to a fixed **intermediate
  frequency (IF)** where high-quality, fixed filters and amplifiers do the work.
  Dominated radio for a century. Its weakness: the **image frequency**, a second
  band $2 f_{IF}$ away that also lands on the IF and must be filtered out first.
- **Direct conversion (zero-IF):** mix straight to baseband ($f_{IF} = 0$). No
  image problem and highly integrable - but suffers DC offset and LO leakage.
  Dominates modern integrated transceivers.

## I/Q: the universal representation

Modern radios split the signal into **in-phase (I)** and **quadrature (Q)** paths
- mixing by $\\cos$ and $\\sin$. Any modulation (AM, FM, QAM, OFDM) is just a
trajectory in the I/Q plane, generated and recovered in DSP. This is what makes
**software-defined radio** possible.

```matlab
fRF = 1e9; fLO = 0.99e9; t = 0:1e-11:1e-7;
rf  = cos(2*pi*fRF*t);
lo  = cos(2*pi*fLO*t);
ifsig = rf.*lo;                    % mixer: yields 10 MHz + 1.99 GHz
```

```python
import numpy as np
fRF, fLO = 1e9, 0.99e9
t = np.arange(0, 1e-7, 1e-11)
rf = np.cos(2*np.pi*fRF*t)
lo = np.cos(2*np.pi*fLO*t)
ifsig = rf*lo                      # 10 MHz IF + 1.99 GHz sum
```

> **Practical insight:** the front-end's noise figure and linearity (IP3,
> spurious-free dynamic range) set what the whole radio can hear. A great DSP
> behind a poor LNA is wasted.

**Next:** how much signal actually arrives - the link budget.
""",
        ),
        _t(
            "The RF link budget & propagation",
            "12 min",
            """\
# The RF link budget & propagation

Will the signal arrive strong enough to decode? A **link budget** answers it by
accounting every gain and loss from transmitter to receiver - in dB, so it is
just addition.

$$P_{rx} = P_{tx} + G_{tx} + G_{rx} - L_{path} - L_{misc}.$$

If $P_{rx}$ exceeds the receiver **sensitivity** (noise floor plus the required
SNR), with margin to spare, the link closes.

## Free-space path loss: the Friis equation

In empty space, power spreads over a sphere, so received power falls as the
**inverse square of distance** and rises with the square of wavelength:

$$P_{rx} = P_{tx}\\,G_{tx}\\,G_{rx}\\left(\\frac{\\lambda}{4\\pi d}\\right)^2.$$

In dB the free-space path loss is $\\mathrm{FSPL_{dB}} = 20\\log_{10} d +
20\\log_{10} f + 32.45$ (km, MHz). Slide frequency - higher bands lose more,
which is why millimeter-wave 5G needs dense cells:

```plot
{"title": "Free-space path loss vs distance (slide frequency)", "xLabel": "distance (km)", "yLabel": "path loss (dB)", "xRange": [0.1, 20], "yRange": [60, 140], "grid": true, "controls": [{"name": "fGHz", "range": [0.7, 6], "value": 2, "label": "frequency (GHz)"}], "functions": [{"expr": "20*log10(x) + 20*log10(fGHz*1000) + 32.45", "label": "FSPL (dB)"}]}
```

## Real propagation: it is worse than free space

- **Path-loss exponent:** in cities power falls faster than the square law
  (exponent 3-4) due to obstruction and ground effects.
- **Shadowing:** buildings and terrain block paths (log-normal fades over
  meters).
- **Multipath fading:** reflections arrive with different delays and phases and
  **interfere**. Where they cancel, the signal drops into a deep **fade**. Move a
  half wavelength and it returns - why your phone reception changes when you take
  one step. Slide the reflection delay and watch the fading nulls move:

```plot
{"title": "Multipath fading: direct + reflected paths interfere (slide delay)", "xLabel": "frequency (relative)", "yLabel": "received |H|", "xRange": [0, 10], "yRange": [0, 2.1], "grid": true, "controls": [{"name": "tau", "range": [0.3, 3], "value": 1, "label": "reflection delay"}], "functions": [{"expr": "abs(1 + cos(2*pi*x*tau))", "label": "|1 + reflection|"}]}
```

## Fading types

**Flat fading** dips the whole signal; **frequency-selective fading** dips only
parts of the band (the cause of those nulls above) - which is exactly what OFDM
and equalizers are built to fight.

```matlab
Ptx_dBm = 30; Gtx = 15; Grx = 15; f_MHz = 2000; d_km = 5;
FSPL = 20*log10(d_km) + 20*log10(f_MHz) + 32.45;
Prx_dBm = Ptx_dBm + Gtx + Grx - FSPL;     % received power
```

```python
import numpy as np
Ptx_dBm, Gtx, Grx, f_MHz, d_km = 30, 15, 15, 2000, 5
FSPL = 20*np.log10(d_km) + 20*np.log10(f_MHz) + 32.45
Prx_dBm = Ptx_dBm + Gtx + Grx - FSPL      # received power
```

> **Practical insight:** always design with **margin** (typically 10-20 dB over
> sensitivity) to survive fading, rain, and aging. The link budget is the first
> spreadsheet of any radio system - satellite, cellular, or IoT.

**Next:** the components that supply those gains - antennas and arrays.
""",
        ),
        _t(
            "Antennas & arrays for comms",
            "12 min",
            """\
# Antennas & arrays for comms

The **antenna** converts guided waves to radiated ones and back. Its key spec for
a link budget is **gain** - not amplification, but how it *concentrates* power in
a direction relative to an isotropic radiator (dBi).

## Radiation pattern, gain, and directivity

A dipole radiates a doughnut; a dish or array focuses a narrow beam. More gain
means a narrower **beamwidth** and longer reach in that direction. **Effective
aperture** links gain to physical size: bigger (in wavelengths) = more gain.

## The phased array: steer the beam electronically

Feed an array of elements with progressive **phase shifts** and the wavefronts
add up in a chosen direction - **beam steering** with no moving parts. The array
factor for $N$ elements spaced $d$ with phase step controlled by steering angle
sharpens as $N$ grows. Slide the number of elements and watch the main beam
narrow:

```plot
{"title": "Phased-array pattern: more elements = narrower beam (slide N)", "xLabel": "angle (radians from broadside)", "yLabel": "normalized array factor", "xRange": [-1.5, 1.5], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "N", "range": [2, 12], "value": 6, "label": "number of elements"}], "functions": [{"expr": "abs(sin(N*pi*sin(x)/2)/(N*sin(pi*sin(x)/2) + (x==0)*0.0001))", "label": "array factor"}]}
```

Steering electronically (a slider on the *phase*) sweeps that beam across the sky
- the basis of 5G base stations, radar, and satellite ground terminals:

```plot
{"title": "Beam steering: a phase ramp points the beam (slide steer angle)", "xLabel": "angle (radians)", "yLabel": "array factor", "xRange": [-1.5, 1.5], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "s", "range": [-1, 1], "value": 0, "label": "steer angle (rad)"}], "functions": [{"expr": "abs(sin(8*pi*(sin(x)-sin(s))/2)/(8*sin(pi*(sin(x)-sin(s))/2) + ((x-s)==0)*0.0001))", "label": "steered beam (N=8)"}]}
```

## MIMO: many antennas, more capacity

**MIMO** (multiple-input multiple-output) uses several antennas at both ends.
Multipath - usually the enemy - becomes an asset: independent paths form parallel
**spatial streams**, multiplying capacity *without more bandwidth or power*.

```mermaid
flowchart LR
  TX1["Tx antenna 1"] --> CH["rich scattering channel"]
  TX2["Tx antenna 2"] --> CH
  CH --> RX1["Rx antenna 1"]
  CH --> RX2["Rx antenna 2"]
  RX1 --> EQ["MIMO decoder: separate streams"]
  RX2 --> EQ
```

- **Spatial multiplexing:** send different data on each stream (more throughput).
- **Diversity:** send the same data on each path (more reliability).
- **Beamforming:** shape the combined pattern toward a user (more range/SNR).
- **Massive MIMO** (5G): dozens-to-hundreds of elements serve many users at once.

```matlab
N = 8; d = 0.5;                    % elements, spacing in wavelengths
theta = linspace(-pi/2, pi/2, 400);
AF = abs(sin(N*pi*d*sin(theta)) ./ (N*sin(pi*d*sin(theta)) + eps));
```

```python
import numpy as np
N, d = 8, 0.5
theta = np.linspace(-np.pi/2, np.pi/2, 400)
AF = np.abs(np.sin(N*np.pi*d*np.sin(theta))
            / (N*np.sin(np.pi*d*np.sin(theta)) + 1e-9))
```

> **Practical insight:** antenna gain is cheaper than transmit power and adds at
> *both* ends of a link. Phased arrays and MIMO are why 5G and Wi-Fi keep scaling
> capacity in fixed spectrum.

**Next:** the modulation that beats fading - OFDM.
""",
        ),
        _t(
            "OFDM & modern wireless",
            "13 min",
            """\
# OFDM & modern wireless

Frequency-selective fading punches nulls into a wideband signal, and high symbol
rates cause severe ISI. **OFDM** (orthogonal frequency-division multiplexing)
sidesteps both by splitting one fast data stream across **many slow, narrow
subcarriers** carried in parallel.

## Why it works

Each subcarrier is narrow enough that the channel looks **flat** across it - so a
deep fade kills only a few subcarriers (recovered by coding) instead of
corrupting everything. The subcarriers are **orthogonal**: spaced exactly so each
one's spectrum is zero at every other's center, letting them overlap without
interfering. The whole symbol is generated with one **IFFT** and recovered with
one **FFT** - cheap in silicon.

```plot
{"title": "OFDM subcarriers: orthogonal sincs overlap but do not interfere", "xLabel": "frequency (subcarrier spacings)", "yLabel": "amplitude", "xRange": [-3, 3], "yRange": [-0.4, 1.1], "grid": true, "functions": [{"expr": "sin(pi*(x))/(pi*(x) + (x==0))", "label": "subcarrier 0", "color": "#2563eb"}, {"expr": "sin(pi*(x-1))/(pi*(x-1) + ((x-1)==0))", "label": "subcarrier +1", "color": "#dc2626"}, {"expr": "sin(pi*(x+1))/(pi*(x+1) + ((x+1)==0))", "label": "subcarrier -1", "color": "#16a34a"}]}
```

## The cyclic prefix: killing ISI between symbols

OFDM copies the tail of each symbol to its front - the **cyclic prefix (CP)**. As
long as the channel's delay spread is shorter than the CP, the multipath echoes
of the previous symbol decay within the prefix and the FFT window sees a clean,
periodic symbol. The CP costs a little overhead to make the channel a simple
per-subcarrier multiply.

```mermaid
flowchart LR
  BITS["bits"] --> QAM["map to QAM per subcarrier"]
  QAM --> IFFT["IFFT: build time symbol"]
  IFFT --> CP["add cyclic prefix"]
  CP --> CHAN["multipath channel"]
  CHAN --> RMCP["remove CP"]
  RMCP --> FFT["FFT: recover subcarriers"]
  FFT --> EQ["1-tap equalize per subcarrier"]
```

## Where it runs the world

OFDM (and its multi-user form **OFDMA**) is the air interface of **Wi-Fi
(802.11a/g/n/ac/ax)**, **LTE**, **5G NR**, **DVB** digital TV, and **DSL**.
Numbers vary - LTE uses $15$ kHz subcarrier spacing; 5G scales it ($15$ to $240$
kHz) to trade latency against robustness.

## The catch

OFDM's sum of many subcarriers can momentarily peak high - a high
**peak-to-average power ratio (PAPR)** that stresses the power amplifier. It is
also sensitive to frequency offset and phase noise, which break orthogonality.

```matlab
Nsc = 64; cp = 16;
data = (2*randi([0 1],1,Nsc)-1) + 1j*(2*randi([0 1],1,Nsc)-1);
sym = ifft(data);                  % time-domain OFDM symbol
tx = [sym(end-cp+1:end) sym];      % prepend cyclic prefix
```

```python
import numpy as np
rng = np.random.default_rng(0)
Nsc, cp = 64, 16
data = (2*rng.integers(0,2,Nsc)-1) + 1j*(2*rng.integers(0,2,Nsc)-1)
sym = np.fft.ifft(data)            # time-domain OFDM symbol
tx = np.concatenate([sym[-cp:], sym])  # prepend cyclic prefix
```

> **Practical insight:** OFDM turns a nasty multipath channel into a bank of easy
> flat channels you equalize with one complex multiply each. That simplicity is
> why it won - despite the PAPR headache.

**Next:** doing all of this in software - SDR and DSP.
""",
        ),
        _t(
            "Software-defined radio & DSP in comms",
            "12 min",
            """\
# Software-defined radio & DSP in comms

For most of radio history, each function lived in dedicated analog hardware.
**Software-defined radio (SDR)** moves the boundary: digitize as close to the
antenna as possible, then do filtering, mixing, modulation, and demodulation in
**software/DSP**. Change the waveform by changing code, not soldering.

```mermaid
flowchart LR
  ANT["antenna"] --> RF["minimal RF: amplify + filter"]
  RF --> ADC["wideband ADC"]
  ADC --> DSP["DSP / FPGA / CPU: all the rest in software"]
  DSP --> DAC["DAC (transmit)"]
  DAC --> RFTX["RF out"]
```

## The I/Q sample stream

An SDR delivers a stream of complex **I/Q samples** - the same in-phase/quadrature
representation from the front-end lesson. In this form every operation is DSP:

- **Mixing** = multiply by a complex exponential $e^{j 2\\pi f t}$.
- **Filtering** = convolve with FIR/IIR taps.
- **Demodulation** = geometry on I/Q (phase angle for FM, nearest constellation
  point for QAM).

Multiplying a complex sample by $e^{j\\theta}$ **rotates** it - a tunable digital
mixer. Press Play to watch a sample rotate around the I/Q plane as the digital
LO advances:

```plot
{"title": "Digital downconversion: multiply by e^(j*theta) rotates the sample", "xLabel": "I", "yLabel": "Q", "xRange": [-1.3, 1.3], "yRange": [-1.3, 1.3], "grid": true, "animate": {"param": "t", "range": [0, 6.2832], "label": "LO phase"}, "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 6.2832], "label": "unit circle", "color": "#94a3b8"}], "points": [{"xExpr": "cos(t)", "yExpr": "sin(t)", "label": "rotating sample", "color": "#dc2626", "size": 7, "trail": true}]}
```

## The decimation / interpolation trick

A wideband ADC produces a torrent of samples. DSP **filters then decimates**
(keeps every $M$-th sample) to focus on the channel of interest at a manageable
rate - and **interpolates** on transmit. This polyphase resampling is the
bread-and-butter of any SDR receiver.

## Why it matters

- **One radio, many standards:** the same hardware runs FM, ADS-B, LTE, or your
  own protocol by loading software.
- **Rapid prototyping & research:** test a new waveform in an afternoon.
- **The ecosystem:** **GNU Radio**, **RTL-SDR** dongles, and **USRP** boards, with
  DSP in Python (`numpy`, `scipy.signal`) and C++.

```matlab
fs = 1e6; t = (0:fs-1)/fs;
iq = exp(1j*2*pi*1e5*t);           % a complex tone at 100 kHz
lo = exp(-1j*2*pi*1e5*t);
baseband = iq.*lo;                 % digital downconversion to DC
```

```python
import numpy as np
fs = 1_000_000
t = np.arange(fs)/fs
iq = np.exp(1j*2*np.pi*1e5*t)      # complex tone at 100 kHz
lo = np.exp(-1j*2*np.pi*1e5*t)
baseband = iq*lo                   # digital downconversion to DC
```

> **Practical insight:** SDR pushes the analog/digital line ever closer to the
> antenna as ADCs get faster. The skills that matter become **DSP and software**
> - the same numpy you use in these labs is the language of modern radio.

**Next:** put a link budget and an OFDM symbol together in code.
""",
        ),
        _code(
            "Lab: link budget & an OFDM symbol",
            "14 min",
            """\
# Two practical RF computations: (1) a full link budget that tells you whether a
# cellular link closes, and (2) building/recovering an OFDM symbol through a
# multipath channel. Pure numpy + matplotlib.
import numpy as np
import matplotlib.pyplot as plt

# --- Part 1: link budget ---------------------------------------------------
Ptx_dBm = 43.0                   # base-station transmit power (~20 W)
Gtx = 17.0                       # antenna gains (dBi)
Grx = 0.0                        # phone antenna
f_MHz = 2100.0                   # carrier
d_km = np.linspace(0.05, 10, 200)

FSPL = 20*np.log10(d_km) + 20*np.log10(f_MHz) + 32.45
Prx_dBm = Ptx_dBm + Gtx + Grx - FSPL

# Receiver sensitivity = thermal noise floor + noise figure + required SNR
B = 20e6                         # 20 MHz channel
NF = 7.0                         # receiver noise figure (dB)
req_snr = 10.0                   # required SNR (dB)
noise_dBm = -174 + 10*np.log10(B) + NF
sensitivity = noise_dBm + req_snr
margin = Prx_dBm - sensitivity

# range where the link closes (margin >= 0)
closes = d_km[margin >= 0]
max_range = closes.max() if closes.size else 0.0

# --- Part 2: OFDM symbol through multipath ---------------------------------
rng = np.random.default_rng(3)
Nsc, cp = 64, 16
qpsk = (2*rng.integers(0, 2, Nsc) - 1) + 1j*(2*rng.integers(0, 2, Nsc) - 1)
time_sym = np.fft.ifft(qpsk)
tx = np.concatenate([time_sym[-cp:], time_sym])     # add cyclic prefix

channel = np.array([1.0, 0.0, 0.3, 0.0, 0.15])      # 3-tap multipath
rx = np.convolve(tx, channel)[:len(tx)]
rx_nocp = rx[cp:cp+Nsc]                              # remove cyclic prefix
H = np.fft.fft(channel, Nsc)
recovered = np.fft.fft(rx_nocp)/H                    # 1-tap equalize

# --- plots -----------------------------------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
ax[0].plot(d_km, Prx_dBm, color="#2563eb", label="received power")
ax[0].axhline(sensitivity, ls="--", color="#dc2626", label="sensitivity")
ax[0].set_title(f"Link budget: closes out to ~{max_range:.1f} km")
ax[0].set_xlabel("distance (km)"); ax[0].set_ylabel("dBm")
ax[0].legend(); ax[0].grid(True)

ax[1].scatter(qpsk.real, qpsk.imag, s=70, marker="x",
              color="#dc2626", label="sent")
ax[1].scatter(recovered.real, recovered.imag, s=20,
              color="#2563eb", alpha=0.7, label="recovered")
ax[1].set_title("OFDM QPSK: sent vs equalized")
ax[1].set_xlabel("I"); ax[1].set_ylabel("Q")
ax[1].legend(); ax[1].grid(True); ax[1].set_aspect("equal")
plt.tight_layout(); plt.show()

print(f"noise floor = {noise_dBm:.1f} dBm, sensitivity = {sensitivity:.1f} dBm")
print(f"link closes out to about {max_range:.1f} km")
print(f"OFDM recovery error (rms) = {np.sqrt(np.mean(np.abs(recovered-qpsk)**2)):.3f}")

# Try it yourself:
#   1. Raise NF or req_snr: sensitivity worsens, max range shrinks.
#   2. Make the channel taps stronger/longer than the CP: recovery degrades.
""",
        ),
        _t(
            "Applications: 5G, satellite, IoT & radar",
            "12 min",
            """\
# Applications: 5G, satellite, IoT & radar

Everything in this track converges in real systems. Here is how the pieces -
modulation, coding, link budgets, antennas, OFDM, SDR - assemble into the radios
that run the modern world.

## 5G cellular: capacity by every means at once

5G stacks **every** trick: **OFDMA** air interface, adaptive **QAM** up to
256-QAM, **LDPC/polar coding** near the Shannon limit, **massive MIMO** and
**beamforming** for spatial reuse, and **millimeter-wave** bands for huge
bandwidth (paying the path-loss price with dense small cells). Three service
classes share it: enhanced mobile broadband, ultra-reliable low-latency comms
(URLLC, for automation), and massive machine-type comms (the IoT below).

## Satellite communications: the link-budget extreme

A geostationary satellite is $\\sim 36{,}000$ km away, so path loss is enormous
and the **link budget** rules everything - high-gain dishes, low-noise front-ends,
and heavy **FEC**. **LEO constellations** (Starlink, OneWeb) fly low ($\\sim 550$
km) to cut latency and path loss, using **phased arrays** that electronically
track fast-moving satellites. GPS is a satellite link too: **CDMA spread
spectrum** so weak you receive it *below the noise floor*, recovered by
correlation gain.

```plot
{"title": "Why LEO: path loss vs orbit altitude (lower is closer is louder)", "xLabel": "altitude (thousands of km)", "yLabel": "free-space path loss at 12 GHz (dB)", "xRange": [0.5, 36], "yRange": [160, 210], "grid": true, "functions": [{"expr": "20*log10(x*1000) + 20*log10(12000) + 32.45", "label": "FSPL (dB)"}]}
```

## IoT: low power, low rate, long range

Sensors must run years on a coin cell, so IoT radios optimize **energy per bit**,
not speed. **LPWAN** technologies - **LoRa** (chirp spread spectrum), **NB-IoT**,
**Sigfox** - use narrow bandwidth, heavy coding, and tiny duty cycles to reach
kilometers at milliwatts. **Bluetooth Low Energy** and **Zigbee** cover the short
range. The design lever is the link budget run in reverse: minimize transmit
power while still closing the link.

## Radar: communication's sibling

Radar sends a known waveform and listens for the **echo**. Round-trip delay gives
**range** ($d = c\\,\\tau/2$); the **Doppler shift** gives velocity. It shares the
same DSP, antennas, and phased-array beam steering - **automotive radar** at
77 GHz, **weather radar**, and **air-traffic** radar. The Doppler shift scales
with velocity and carrier frequency:

```plot
{"title": "Radar Doppler shift vs target speed (slide carrier frequency)", "xLabel": "target radial speed (m/s)", "yLabel": "Doppler shift (kHz)", "xRange": [0, 60], "yRange": [0, 35], "grid": true, "controls": [{"name": "fc_GHz", "range": [10, 77], "value": 24, "label": "carrier (GHz)"}], "functions": [{"expr": "2*x*fc_GHz/300", "label": "fd = 2 v fc / c"}]}
```

## The throughline

Information rides a carrier (analog or digital), shaped to fit a bandwidth,
hardened by coding against noise and fading, launched and gathered by antennas,
carried over a budgeted link, and increasingly processed in software. The bands
and standards change; **Shannon, Friis, and the decibel** do not.

```mermaid
flowchart LR
  INFO["information"] --> MOD["modulate + code"]
  MOD --> RF["RF front-end + antenna"]
  RF --> CHAN["channel: loss, noise, fading"]
  CHAN --> RX["antenna + LNA + DSP"]
  RX --> DEMOD["equalize + decode"]
  DEMOD --> OUT["information recovered"]
```

```matlab
c = 3e8; fc = 24e9; v = 30;        % automotive radar
fd = 2*v*fc/c;                     % Doppler shift ~ 4.8 kHz
range = c*1e-6/2;                  % range from 1 us round-trip delay
```

```python
c, fc, v = 3e8, 24e9, 30           # automotive radar
fd = 2*v*fc/c                      # Doppler shift ~ 4.8 kHz
rng_m = c*1e-6/2                   # range from 1 us round-trip delay
```

> **Practical insight:** when you meet any new wireless system, decode it with the
> same checklist - what modulation, what coding, what bandwidth, what antennas,
> what link budget? Every radio is a different balance of the same trade-offs.
""",
        ),
    ),
)


RF_COMMS_COURSES: tuple[SeedCourse, ...] = (
    _RF_COMMS_BASICS,
    _RF_COMMS_INTERMEDIATE,
    _RF_COMMS_ADVANCED,
)

__all__ = ["RF_COMMS_COURSES"]
