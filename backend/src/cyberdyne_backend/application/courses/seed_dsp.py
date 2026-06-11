"""Curated Digital Signal Processing track: Basics, Intermediate, Advanced.

A complete DSP curriculum: discrete-time signals and systems (sequences,
sampling, LTI, convolution, the z-transform, the DFT/FFT, spectral analysis),
filter design (FIR, IIR, structures, multirate, fixed-point), and advanced DSP
(adaptive filters, spectral estimation, communications, real-time/embedded,
multidimensional and modern DSP). Dual MATLAB + Python focus throughout (the
classic DSP pairing), with runnable Python labs (numpy + matplotlib),
interactive ```plot blocks, Mermaid diagrams, LaTeX formulas, and real use
cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/dsp_*.py) at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Digital Signal Processing -- Basics ---------------------------------------

_DSP_BASICS = SeedCourse(
    slug="dsp-basics",
    title="Digital Signal Processing -- Basics",
    description=(
        "DSP from the ground up: discrete-time signals and LTI systems, "
        "convolution and difference equations, the z-transform and the system "
        "function, the DFT and FFT, and practical spectral analysis (windowing, "
        "leakage, zero-padding) - with side-by-side MATLAB and Python, "
        "interactive plots, and a runnable FFT lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Discrete-time signals & systems",
            "12 min",
            """\
# Discrete-time signals & systems

Digital signal processing is about **sequences of numbers** - a signal sampled
at regular instants - and the **systems** that transform one sequence into
another. Audio in your phone, an ECG trace, pixels in a row of an image, daily
stock prices: all are discrete-time signals $x[n]$ where $n$ is an integer index.

## From continuous to discrete: sampling

A continuous signal $x(t)$ becomes a sequence by sampling every $T_s$ seconds:

$$x[n] = x(n T_s), \\qquad f_s = \\frac{1}{T_s}.$$

The **Nyquist-Shannon** theorem is the rule that makes this safe: to capture a
signal with no frequency above $f_{max}$, you must sample faster than twice that,
$f_s > 2 f_{max}$. Break the rule and high frequencies masquerade as low ones -
**aliasing**. That is why a 44.1 kHz audio CD can carry up to ~22 kHz (the edge
of hearing), and why a spinning wheel in a movie can appear to turn backwards.

Slide the sampling rate and watch the samples (red dots) try to capture a 1 Hz
sine - too few and they trace a slower, wrong "alias":

```plot
{"title": "Sampling a 1 Hz sine (slide the number of samples per second)", "xLabel": "time (s)", "yLabel": "amplitude", "xRange": [0, 2], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "fs", "range": [1, 20], "value": 8, "label": "sampling rate fs (Hz)"}], "functions": [{"expr": "sin(2*pi*x)", "label": "continuous x(t)", "color": "#94a3b8"}], "points": [{"xExpr": "round(t*fs)/fs", "yExpr": "sin(2*pi*round(t*fs)/fs)", "label": "sample", "color": "#dc2626", "size": 6, "trail": true}], "animate": {"param": "t", "range": [0, 2], "label": "time"}}
```

## The building-block signals

| Signal | Definition | Role |
|--------|------------|------|
| Unit impulse $\\delta[n]$ | 1 at $n=0$, else 0 | the "test poke" - reveals a system |
| Unit step $u[n]$ | 1 for $n \\ge 0$ | switch-on, accumulation |
| Exponential $a^n$ | geometric sequence | growth/decay, the z-transform's atom |
| Sinusoid $\\cos(\\omega n)$ | $\\omega$ in rad/sample | the frequency-domain atom |

Any sequence is a **sum of shifted, scaled impulses**:
$x[n] = \\sum_k x[k]\\,\\delta[n-k]$ - the idea behind convolution.

## LTI systems: the workhorse

Most useful systems are **Linear and Time-Invariant (LTI)**:

- **Linear** - scaling and adding inputs scales and adds outputs (superposition).
- **Time-invariant** - delaying the input just delays the output.

An LTI system is **completely described by its impulse response** $h[n]$ - poke
it with $\\delta[n]$ and record what comes out. Then *any* output is the input
**convolved** with $h[n]$ (next lesson). That single fact is the foundation of
almost everything in this track.

```mermaid
flowchart LR
  X["x[n]"] --> SYS["LTI system, impulse response h[n]"]
  SYS --> Y["y[n] = x[n] * h[n]"]
```

```matlab
n  = 0:9;
x  = (n==0);              % unit impulse delta[n]
u  = double(n>=0);        % unit step u[n]
g  = 0.8.^n;              % decaying exponential
```

```python
import numpy as np
n = np.arange(10)
x = (n == 0).astype(float)   # unit impulse delta[n]
u = (n >= 0).astype(float)   # unit step u[n]
g = 0.8**n                   # decaying exponential
```

> **Practical insight:** before any spectral or filtering work, fix your
> sampling rate and make sure nothing above $f_s/2$ reaches the ADC - put an
> **anti-aliasing filter** in front. Aliasing cannot be undone after sampling.

**Next:** how an LTI system actually computes its output - convolution.
""",
        ),
        _t(
            "Convolution & difference equations",
            "12 min",
            """\
# Convolution & difference equations

An LTI system's output is the input **convolved** with its impulse response
$h[n]$:

$$y[n] = (x * h)[n] = \\sum_{k=-\\infty}^{\\infty} x[k]\\,h[n-k].$$

Intuitively: **flip** $h$, **slide** it across $x$, and at each position
**multiply and sum** the overlap. Every output sample is a weighted average of
recent inputs, with the weights given by $h$.

## A worked feel for it

A 3-point moving average has $h = [\\tfrac{1}{3}, \\tfrac{1}{3}, \\tfrac{1}{3}]$.
Convolving a noisy signal with it smooths the signal - each output is the mean of
three neighbours. Lengthen $h$ and you smooth harder. This is the simplest
**lowpass filter** and it is everywhere: smoothing sensor readings, a stock
chart's moving average, blurring an image row.

## Difference equations: recursive systems

Many systems are described by a **linear constant-coefficient difference
equation**, relating the output to past outputs and present/past inputs:

$$y[n] = \\sum_{k=0}^{M} b_k\\,x[n-k] \\;-\\; \\sum_{k=1}^{N} a_k\\,y[n-k].$$

- If all $a_k = 0$, the output is a finite sum of inputs - a **FIR** (finite
  impulse response) filter; its $h[n]$ has finite length.
- If some $a_k \\ne 0$, the output **feeds back** - an **IIR** (infinite impulse
  response) filter; $h[n]$ rings on forever (decaying if stable).

A one-pole IIR smoother $y[n] = (1-a)\\,x[n] + a\\,y[n-1]$ has an exponentially
decaying impulse response. Slide the pole $a$ toward 1 for heavier smoothing
(longer memory):

```plot
{"title": "One-pole IIR impulse response h[n] = (1-a) a^n (slide the pole a)", "xLabel": "n (samples)", "yLabel": "h[n]", "xRange": [0, 30], "yRange": [0, 0.6], "grid": true, "controls": [{"name": "a", "range": [0.1, 0.95], "value": 0.7, "label": "pole a"}], "functions": [{"expr": "(1-a)*a^x", "label": "h[n]"}]}
```

```mermaid
flowchart LR
  X["x[n]"] --> SUM(("+"))
  SUM --> Y["y[n]"]
  Y --> DLY["z^-1 (delay)"]
  DLY -->|"* a"| SUM
```

```matlab
x = [0 0 1 2 3 2 1 0 0];          % a little bump
h = [1 1 1]/3;                    % 3-point moving average
y = conv(x, h);                   % convolution
a = 0.7;
yiir = filter(1-a, [1 -a], x);    % one-pole IIR smoother
```

```python
import numpy as np
x = np.array([0, 0, 1, 2, 3, 2, 1, 0, 0], float)
h = np.ones(3)/3                  # 3-point moving average
y = np.convolve(x, h)             # convolution
a = 0.7
yiir = np.zeros_like(x)           # one-pole IIR: y[n] = (1-a)x[n] + a y[n-1]
for n in range(len(x)):
    yiir[n] = (1-a)*x[n] + (a*yiir[n-1] if n > 0 else 0.0)
```

> **Practical insight:** FIR filters are always stable and can have exactly
> **linear phase** (no waveform distortion); IIR filters do far more with fewer
> coefficients but can go unstable and distort phase. The whole Intermediate
> course is about choosing and designing both.

**Next:** the transform that turns difference equations into algebra - the
z-transform.
""",
        ),
        _t(
            "The z-transform & the system function",
            "13 min",
            """\
# The z-transform & the system function

The **z-transform** is to discrete-time systems what the Laplace transform is to
continuous ones: it turns convolution into multiplication and difference
equations into algebra. It maps a sequence to a function of a complex variable
$z$:

$$X(z) = \\sum_{n=-\\infty}^{\\infty} x[n]\\,z^{-n}.$$

The magic substitution is the **delay**: a one-sample delay $x[n-1]$ becomes
$z^{-1}X(z)$. So a difference equation in $z^{-1}$ becomes a **ratio of
polynomials**, the **system (transfer) function**:

$$H(z) = \\frac{Y(z)}{X(z)} = \\frac{b_0 + b_1 z^{-1} + \\dots + b_M z^{-M}}{1 + a_1 z^{-1} + \\dots + a_N z^{-N}}.$$

## Poles & zeros: the system's DNA

Factor $H(z)$ and you get **zeros** (roots of the numerator - where $H$ goes to
0) and **poles** (roots of the denominator - where $H$ blows up). Plotted in the
complex **z-plane**, they tell you everything:

- A pole **near** the unit circle gives a **resonant peak** in the response near
  that angle.
- A zero **on** the unit circle puts a **notch** (deep null) at that frequency.
- The angle on the circle is the **frequency** ($z = e^{j\\omega}$, with
  $\\omega = \\pi$ at $f_s/2$).

```plot
{"title": "z-plane: the unit circle is the frequency axis (pole near it = resonance)", "xLabel": "real", "yLabel": "imaginary", "xRange": [-1.4, 1.4], "yRange": [-1.4, 1.4], "grid": true, "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 6.2832], "label": "unit circle |z| = 1", "color": "#94a3b8"}], "points": [{"x": 0.8, "y": 0.45, "label": "pole", "color": "#dc2626", "size": 8}, {"x": 0.8, "y": -0.45, "label": "pole", "color": "#dc2626", "size": 8}, {"x": -1, "y": 0, "label": "zero", "color": "#2563eb", "size": 8}]}
```

## Stability lives inside the unit circle

A causal system is **stable** if and only if **every pole is inside the unit
circle** ($|z| < 1$). Push a pole onto or outside the circle and the impulse
response stops decaying - it rings forever or grows without bound. This is the
discrete-time twin of "poles in the left half plane" from continuous systems.

```mermaid
stateDiagram-v2
  [*] --> Stable
  Stable --> Stable: all poles inside unit circle
  Stable --> Marginal: a pole reaches |z| = 1
  Marginal --> Unstable: pole moves outside
  Unstable --> [*]: output grows without bound
```

## The frequency response falls right out

Evaluate $H(z)$ **on** the unit circle, $z = e^{j\\omega}$, and you get the
**frequency response** $H(e^{j\\omega})$ - the gain and phase the filter applies
at each frequency. The DFT/FFT (next lesson) samples exactly this curve.

```matlab
b = [1 0 -1];                 % zeros at z = +/-1 (a notch pair)
a = [1 -0.9*sqrt(2) 0.81];    % poles at radius 0.9
z = roots(b); p = roots(a);   % zeros and poles
[H, w] = freqz(b, a, 512);    % frequency response on the unit circle
```

```python
import numpy as np
b = np.array([1.0, 0.0, -1.0])          # zeros at z = +/-1
a = np.array([1.0, -0.9*np.sqrt(2), 0.81])  # poles at radius 0.9
z = np.roots(b); p = np.roots(a)        # zeros and poles
w = np.linspace(0, np.pi, 512)
ejw = np.exp(1j*w)
H = np.polyval(b[::-1], ejw) / np.polyval(a[::-1], ejw)  # H(e^jw)
```

> **Practical insight:** designing a filter is largely **placing poles and
> zeros**: zeros where you want nulls, poles (just inside the circle) where you
> want peaks. The closer a pole creeps to the circle, the sharper - and the more
> numerically fragile - the filter becomes.

**Next:** actually computing the spectrum - the DFT and the FFT.
""",
        ),
        _t(
            "The DFT & FFT",
            "13 min",
            """\
# The DFT & FFT

To see a signal's **frequency content** on a computer, we use the **Discrete
Fourier Transform (DFT)**. Given $N$ samples $x[n]$, it produces $N$ complex
**frequency bins** $X[k]$:

$$X[k] = \\sum_{n=0}^{N-1} x[n]\\,e^{-j 2\\pi k n / N}, \\qquad k = 0,\\dots,N-1.$$

Each bin $k$ measures **how much** of the complex sinusoid at frequency
$f_k = k\\,f_s/N$ is present (magnitude) and its **phase**. The DFT is exactly the
z-transform sampled at $N$ equally spaced points on the unit circle.

## Bins and frequency resolution

The mapping from bin index to real frequency is the thing to internalise:

$$f_k = k\\,\\frac{f_s}{N}, \\qquad \\Delta f = \\frac{f_s}{N}.$$

- **Bin spacing** $\\Delta f = f_s/N$ is your **frequency resolution**: collect
  more samples (bigger $N$, longer record) for finer resolution.
- Bins $0 \\dots N/2$ are the positive frequencies up to $f_s/2$ (Nyquist); the
  upper half mirrors them for a real signal.
- Bin 0 is the **DC** (average) component.

A single sinusoid that lands exactly on a bin gives one clean spike. Slide a
tone's frequency across bins to see the spike move and (off-bin) smear:

```plot
{"title": "DFT magnitude of a tone vs frequency (slide the tone, fs = 64)", "xLabel": "frequency bin k", "yLabel": "|X[k]| (approx)", "xRange": [0, 32], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "k0", "range": [2, 28], "value": 8, "label": "tone bin k0"}], "functions": [{"expr": "abs(sin(pi*(x-k0)+0.0001)/(pi*(x-k0)/1+0.0001))/1", "label": "|X[k]| (sinc-like)"}]}
```

## Why the FFT changed the world

A direct DFT costs $O(N^2)$ multiplications - hopeless for big $N$. The **Fast
Fourier Transform (FFT)** computes the *same* result in $O(N \\log N)$ by
recursively splitting the sum (Cooley-Tukey, 1965). For $N = 2^{20}$ that is the
difference between a million-fold more work and a fraction of a second.

```plot
{"title": "Why the FFT matters: N^2 vs N log2 N operations", "xLabel": "transform size N", "yLabel": "operations (relative)", "xRange": [2, 64], "yRange": [0, 600], "grid": true, "functions": [{"expr": "x^2/4", "label": "direct DFT ~ N^2", "color": "#dc2626"}, {"expr": "x*log2(x)", "label": "FFT ~ N log2 N", "color": "#16a34a"}]}
```

The FFT is the engine behind audio spectrum analysers, MP3/JPEG compression, OFDM
in WiFi and 5G, MRI reconstruction, and fast convolution (filter via
$Y[k] = H[k]X[k]$ then inverse-FFT).

```matlab
fs = 1000; N = 256;
n  = 0:N-1;
x  = sin(2*pi*50*n/fs);           % 50 Hz tone
X  = fft(x);                      % length-N FFT
f  = (0:N-1)*fs/N;                % bin frequencies
mag = abs(X)/N;
```

```python
import numpy as np
fs, N = 1000, 256
n = np.arange(N)
x = np.sin(2*np.pi*50*n/fs)       # 50 Hz tone
X = np.fft.fft(x)                 # length-N FFT
f = np.arange(N)*fs/N             # bin frequencies
mag = np.abs(X)/N
```

> **Practical insight:** want finer resolution? **Record longer** (bigger $N$),
> do not just sample faster - resolution is $f_s/N$, and a higher $f_s$ with the
> same $N$ spreads the *same* number of bins over a wider range. Use a power-of-2
> $N$ so the FFT is fastest.

**Next:** the messy reality of real signals - windowing and leakage.
""",
        ),
        _t(
            "Spectral analysis in practice",
            "12 min",
            """\
# Spectral analysis in practice

The DFT silently assumes your $N$ samples are **one period of a periodic
signal**. Real tones almost never fit a whole number of cycles in your record,
so the DFT sees a **discontinuity** at the wrap-around - and the energy of one
clean tone **smears** across many bins. This is **spectral leakage**.

## Leakage and the picket fence

A tone landing exactly on a bin gives one spike; the same tone shifted half a bin
spreads into a broad smear with tall **side lobes** that can bury a nearby weak
signal. Two effects:

- **Leakage** - energy bleeds into neighbouring bins.
- **Scalloping** (the picket-fence effect) - a tone between bins reads low.

## Windowing: taper the edges

The cure is a **window** $w[n]$: multiply the data by a smooth taper that goes to
zero at both ends, killing the edge discontinuity before the FFT.

$$x_w[n] = w[n]\\,x[n], \\qquad X_w[k] = \\mathrm{DFT}\\{x_w[n]\\}.$$

It is always a **trade-off**: a tapered window lowers the side lobes (less
leakage) at the cost of a wider main lobe (less ability to separate two close
tones). Slide a Hann-like taper from rectangular (no taper) to fully tapered:

```plot
{"title": "Window shapes: rectangular -> tapered (slide the taper amount)", "xLabel": "sample n (0..1 of the record)", "yLabel": "window weight w[n]", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "amt", "range": [0, 1], "value": 0.5, "label": "taper amount"}], "functions": [{"expr": "1 - amt*0.5*(1 - cos(2*pi*x))", "label": "w[n]"}]}
```

| Window | Side-lobe level | Main lobe | Use |
|--------|-----------------|-----------|-----|
| Rectangular | -13 dB (poor) | narrowest | separating equal-strength close tones |
| Hann | -31 dB | medium | the safe general-purpose default |
| Hamming | -42 dB | medium | speech, communications |
| Blackman | -58 dB | wide | finding a weak tone next to a strong one |
| Flat-top | very low | very wide | accurate amplitude measurement |

## Zero-padding: interpolate the picture

Appending zeros before the FFT does **not** add information or resolution - it
**interpolates** the existing spectrum onto a finer grid, drawing a smoother
curve through the same underlying shape. Useful to read a peak's location more
precisely or to make a nicer plot, but it cannot separate two tones that the
record length cannot resolve.

```mermaid
flowchart LR
  REC["record N samples"] --> WIN["apply window w[n]"]
  WIN --> ZP["zero-pad to Nfft"]
  ZP --> FFT["FFT"]
  FFT --> MAG["|X[k]| in dB"]
```

```matlab
N = 256; fs = 1000;
n = 0:N-1;
x = sin(2*pi*50.3*n/fs);          % off-bin tone -> leakage
w = hann(N)';                     % Hann window
Xw = fft(x.*w, 1024);             % windowed + zero-padded to 1024
mag = 20*log10(abs(Xw)/max(abs(Xw)));
```

```python
import numpy as np
N, fs = 256, 1000
n = np.arange(N)
x = np.sin(2*np.pi*50.3*n/fs)     # off-bin tone -> leakage
w = np.hanning(N)                 # Hann window
Xw = np.fft.fft(x*w, 1024)        # windowed + zero-padded to 1024
mag = 20*np.log10(np.abs(Xw)/np.abs(Xw).max() + 1e-12)
```

> **Practical insight:** default to a **Hann** window for general analysis, a
> **flat-top** when you need accurate amplitudes, and **rectangular** only when
> you must resolve two equal close tones. Always window before you FFT real-world
> data.

**Next:** put it all together - compute a windowed FFT in code.
""",
        ),
        _code(
            "Lab: compute an FFT with windowing",
            "14 min",
            """\
# Compute the spectrum of a two-tone signal in noise, with and without a window.
# See how a Hann window tames leakage so a weak tone next to a strong one shows.
import numpy as np
import matplotlib.pyplot as plt

fs = 1000.0                 # sampling rate (Hz)
N = 512                     # record length
n = np.arange(N)
t = n / fs

# Two tones: a strong one at 100 Hz and a weak one at 120 Hz, plus noise.
rng = np.random.default_rng(0)
x = (1.0*np.sin(2*np.pi*100.0*t)        # strong tone, off-bin on purpose
     + 0.05*np.sin(2*np.pi*120.0*t)     # weak nearby tone
     + 0.01*rng.standard_normal(N))     # broadband noise

# Hann window built inline (no scipy): w[n] = 0.5 - 0.5 cos(2 pi n / (N-1)).
w = 0.5 - 0.5*np.cos(2*np.pi*n/(N-1))
cg = w.mean()               # coherent gain, to keep amplitudes comparable

# FFT magnitude in dB for the rectangular (no window) and Hann cases.
Xrect = np.fft.rfft(x) / N
Xhann = np.fft.rfft(x*w) / (N*cg)
f = np.fft.rfftfreq(N, 1/fs)

mag_rect = 20*np.log10(np.abs(Xrect) + 1e-12)
mag_hann = 20*np.log10(np.abs(Xhann) + 1e-12)

plt.figure(figsize=(8, 4))
plt.plot(f, mag_rect, color="#94a3b8", label="rectangular (leakage hides 120 Hz)")
plt.plot(f, mag_hann, color="#dc2626", lw=2, label="Hann window (120 Hz emerges)")
plt.xlim(0, 250)
plt.xlabel("frequency (Hz)"); plt.ylabel("magnitude (dB)")
plt.title("Two-tone spectrum: windowing reveals the weak tone")
plt.legend(); plt.grid(True); plt.show()

# Report the bin resolution and the two strongest peaks of the windowed spectrum.
df = fs / N
peak = f[np.argmax(np.abs(Xhann))]
print(f"frequency resolution df = fs/N = {df:.2f} Hz")
print(f"strongest peak at ~ {peak:.1f} Hz")
print(f"weak 120 Hz tone level (Hann): {mag_hann[np.argmin(np.abs(f-120))]:.1f} dB")

# Try it yourself:
#   1. Drop the window (use x instead of x*w): the 120 Hz tone vanishes in leakage.
#   2. Double N to 1024: df halves and the peaks sharpen.
#   3. The MATLAB way: X = fft(x.*hann(N)'); semilogx(f, 20*log10(abs(X)));
""",
        ),
    ),
)


# -- Digital Signal Processing -- Intermediate ---------------------------------

_DSP_INTERMEDIATE = SeedCourse(
    slug="dsp-intermediate",
    title="Digital Signal Processing -- Intermediate: Filter Design",
    description=(
        "Designing real filters: FIR design (windowing and Parks-McClellan, "
        "linear phase), IIR design (Butterworth/Chebyshev via the bilinear "
        "transform), filter structures (direct form, cascade, lattice), "
        "multirate DSP (decimation, interpolation, polyphase, filter banks), and "
        "fixed-point/quantization effects - with dual MATLAB/Python, interactive "
        "plots, and a runnable FIR/IIR design lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "FIR filter design",
            "13 min",
            """\
# FIR filter design

A **Finite Impulse Response (FIR)** filter computes each output as a weighted sum
of the last $M+1$ inputs - no feedback:

$$y[n] = \\sum_{k=0}^{M} h[k]\\,x[n-k].$$

The coefficients $h[k]$ **are** the impulse response. FIR filters are the
workhorses of audio EQ, image processing, and communications because they are
**always stable** and can have **exactly linear phase**.

## Why linear phase matters

If $h[n]$ is **symmetric**, every frequency is delayed by the *same* amount, so
the filter shifts the signal in time without distorting its shape. That is
crucial for audio (no smearing of transients), ECG/EEG (preserve waveform
morphology), and digital communications (no inter-symbol distortion). The price
is a constant **group delay** of $M/2$ samples.

## The windowing method (the intuitive one)

The ideal lowpass filter has a $\\mathrm{sinc}$ impulse response that is infinitely
long. **Truncate** it to $M+1$ taps and you get ripples (Gibbs phenomenon) at the
band edge; **multiply by a window** (Hann, Hamming, Kaiser) to tame them - the
same leakage/side-lobe trade-off as in spectral analysis. The Kaiser window even
gives a formula to hit a target ripple and transition width.

More taps = a **sharper** transition. Slide the tap count and watch the lowpass
edge steepen:

```plot
{"title": "FIR lowpass: more taps -> sharper transition (slide tap count)", "xLabel": "normalized frequency (0 = DC, 1 = Nyquist)", "yLabel": "|H|", "xRange": [0, 1], "yRange": [0, 1.15], "grid": true, "controls": [{"name": "M", "range": [4, 40], "value": 12, "label": "filter order M (taps-1)"}], "functions": [{"expr": "abs(sin((M+1)*pi*(x-0.4)/2 + 0.001)/((M+1)*sin(pi*(x-0.4)/2 + 0.001)))", "label": "|H| (windowed-sinc approx)"}]}
```

## Parks-McClellan (the optimal one)

The **Parks-McClellan** algorithm (a.k.a. Remez exchange, `firpm`/`remez`)
designs the **optimal equiripple** FIR for a given order: it spreads the error
evenly as **equal-height ripples** in the pass and stop bands, giving the
**shortest** filter that meets a spec. It is the professional default when you
have a tight transition and ripple budget.

```mermaid
flowchart LR
  SPEC["spec: bands, ripple, transition"] --> ALG["Parks-McClellan (Remez)"]
  ALG --> H["optimal equiripple h[n]"]
  H --> CONV["y[n] = sum h[k] x[n-k]"]
```

```matlab
M = 40; fc = 0.25;                 % cutoff (x pi rad/sample)
h_win = fir1(M, fc, hamming(M+1)); % windowing method
h_pm  = firpm(M, [0 0.2 0.3 1], [1 1 0 0]);  % Parks-McClellan
[H, w] = freqz(h_win, 1, 512);
```

```python
import numpy as np
M, fc = 40, 0.25                   # cutoff in cycles/sample (0..0.5)
k = np.arange(M+1) - M/2
ideal = 2*fc*np.sinc(2*fc*k)       # ideal lowpass sinc
win = 0.54 - 0.46*np.cos(2*np.pi*np.arange(M+1)/M)  # Hamming
h_win = ideal*win                  # windowed-sinc FIR
w = np.linspace(0, np.pi, 512)
H = np.polyval(h_win[::-1], np.exp(-1j*w)) * np.exp(1j*w*(len(h_win)-1)/2)
```

> **Practical insight:** reach for **windowing** when you want a quick, robust
> filter and can spare taps; reach for **Parks-McClellan** when taps (and hence
> latency and compute) are precious and the spec is tight. Either way, symmetric
> taps buy you linear phase for free.

**Next:** fewer coefficients, sharper cutoffs - IIR design.
""",
        ),
        _t(
            "IIR filter design",
            "13 min",
            """\
# IIR filter design

An **Infinite Impulse Response (IIR)** filter feeds output back into itself, so a
**handful of coefficients** can give a razor-sharp cutoff that would need
hundreds of FIR taps. The catch: it can be **unstable**, and its phase is
**nonlinear** (it distorts waveform shape). IIR is the right choice when compute
or latency is tight and phase linearity does not matter (control loops, audio
tone controls, real-time effects).

## Borrow from a century of analog design

The smart move is to **start from a proven analog prototype** and convert it to
digital. The classic prototypes trade flatness against sharpness:

| Prototype | Passband | Stopband | Roll-off | Phase |
|-----------|----------|----------|----------|-------|
| **Butterworth** | maximally flat | smooth | gentlest | best |
| **Chebyshev I** | ripple | smooth | steeper | worse |
| **Chebyshev II** | flat | ripple | steeper | worse |
| **Elliptic** | ripple | ripple | steepest | worst |

Higher **order** $N$ means a steeper roll-off (more poles). For Butterworth the
magnitude response is

$$|H(j\\Omega)|^2 = \\frac{1}{1 + (\\Omega/\\Omega_c)^{2N}}.$$

Slide the order and watch the Butterworth skirt steepen while the passband stays
flat:

```plot
{"title": "Butterworth lowpass: higher order -> steeper roll-off (slide N)", "xLabel": "frequency / cutoff", "yLabel": "|H|", "xRange": [0, 3], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "N", "range": [1, 8], "value": 2, "label": "filter order N"}], "functions": [{"expr": "1/sqrt(1 + x^(2*N))", "label": "|H| Butterworth"}]}
```

## The bilinear transform: analog -> digital

The **bilinear transform** maps the analog plane to the digital z-plane by

$$s = \\frac{2}{T}\\,\\frac{1 - z^{-1}}{1 + z^{-1}}.$$

It squashes the entire infinite analog frequency axis onto the unit circle, so a
stable analog filter (poles in the left half plane) maps to a stable digital one
(poles inside the unit circle) - guaranteed. The squashing is nonlinear
(**frequency warping**), so you **pre-warp** the critical frequency before
designing, and it lands where you want after the transform.

```mermaid
flowchart LR
  PROTO["analog prototype (Butterworth...)"] --> WARP["pre-warp critical freq"]
  WARP --> BLT["bilinear transform s -> z"]
  BLT --> HZ["digital H(z), stable"]
```

```matlab
fs = 1000; fc = 100;               % cutoff 100 Hz
[b, a] = butter(4, fc/(fs/2));     % 4th-order digital Butterworth
[H, w] = freqz(b, a, 512);
% Chebyshev with 1 dB passband ripple:
[bc, ac] = cheby1(4, 1, fc/(fs/2));
```

```python
import numpy as np
# Pre-warp + bilinear for a 1st-order analog prototype 1/(s+1), shown by hand:
fs, fc = 1000.0, 100.0
wc = 2*fs*np.tan(np.pi*fc/fs)      # pre-warped analog cutoff (rad/s)
# Bilinear of H(s) = wc/(s+wc): gives a 1st-order digital lowpass b, a.
K = wc/(2*fs)
b = np.array([K, K]) / (1+K)
a = np.array([1.0, (K-1)/(1+K)])
w = np.linspace(0, np.pi, 512)
ejw = np.exp(-1j*w)
H = (b[0] + b[1]*ejw) / (a[0] + a[1]*ejw)
```

> **Practical insight:** always **check pole locations** after design ($|z| < 1$)
> and implement high-order IIRs as a **cascade of second-order sections** (next
> lesson) - a single high-order polynomial is numerically explosive.

**Next:** how you actually wire a filter up - structures and implementation.
""",
        ),
        _t(
            "Filter structures & implementation",
            "12 min",
            """\
# Filter structures & implementation

A transfer function $H(z)$ is just math; a **structure** is the actual arrangement
of **multipliers, adders, and delays** ($z^{-1}$) that computes it. Different
structures compute the *same* response but differ wildly in **numerical
behaviour, coefficient sensitivity, and hardware cost** - which matters enormously
in fixed-point hardware.

## Direct forms

The most literal mapping of the difference equation:

- **Direct Form I** - all the feedforward ($b$) delays, then all the feedback
  ($a$) delays. Uses $M + N$ delay elements.
- **Direct Form II** - shares the delay line between numerator and denominator,
  using only $\\max(M,N)$ delays (**canonical** - minimum memory).
- **Transposed Direct Form II** - flip the signal-flow graph; often the best
  numerical behaviour and the common library default.

```mermaid
flowchart LR
  X["x[n]"] --> B["feedforward taps b_k"]
  B --> SUM(("+"))
  SUM --> Y["y[n]"]
  Y --> A["feedback taps a_k"]
  A --> SUM
```

## Cascade and parallel forms

Factor $H(z)$ into **second-order sections (SOS / biquads)** and chain them:

$$H(z) = \\prod_i \\frac{b_{0i} + b_{1i}z^{-1} + b_{2i}z^{-2}}{1 + a_{1i}z^{-1} + a_{2i}z^{-2}}.$$

A high-order IIR implemented as one big polynomial is hopelessly sensitive - a
tiny coefficient error moves the poles disastrously. Split into **biquads** and
each section is robust; this is **the** standard way to ship an IIR. The
**parallel form** (partial fractions) is the additive cousin.

## Lattice structures

The **lattice** realises the filter as a ladder of reflection coefficients
$k_i$. It is the natural structure for **linear prediction** and **speech coding**
(LPC, the math behind GSM and early cell-phone voice), and has a beautiful
stability test: the filter is stable **iff every $|k_i| < 1$**. It is also
robust to coefficient quantization.

Coefficient quantization nudges the poles; a direct form can shove them past the
unit circle while a cascade barely flinches. Slide the rounding step to see a
pole pair drift toward instability:

```plot
{"title": "Coefficient quantization nudges a pole pair (slide rounding step)", "xLabel": "real part of pole", "yLabel": "imag part of pole", "xRange": [0, 1.2], "yRange": [-0.1, 1.1], "grid": true, "controls": [{"name": "q", "range": [0, 0.15], "value": 0.03, "label": "quantization step q"}], "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 1.5708], "label": "unit circle", "color": "#94a3b8"}], "points": [{"x": 0.85, "y": 0.45, "label": "ideal pole", "color": "#2563eb", "size": 7}, {"xExpr": "0.85 + q*5", "yExpr": "0.45 + q*4", "label": "quantized pole", "color": "#dc2626", "size": 7}]}
```

```matlab
[b, a] = butter(6, 0.2);           % 6th-order: do NOT run as one polynomial
[sos, g] = tf2sos(b, a);           % convert to second-order sections
y = sosfilt(sos, x);               % stable cascade implementation
```

```python
import numpy as np
# Cascade two biquads by filtering through each in turn (Direct Form I).
def_b1 = np.array([0.2, 0.4, 0.2]); def_a1 = np.array([1.0, -0.5, 0.1])
def_b2 = np.array([0.3, 0.3, 0.0]); def_a2 = np.array([1.0, -0.3, 0.0])
# In practice numpy's lfilter / a hand-rolled biquad loop applies each section.
```

> **Practical insight:** never ship a high-order IIR as a single direct-form
> polynomial. Use **second-order sections** (biquads) with a transposed
> Direct-Form-II per section - the universal, numerically safe recipe.

**Next:** changing the sample rate - multirate DSP.
""",
        ),
        _t(
            "Multirate DSP",
            "12 min",
            """\
# Multirate DSP

**Multirate** systems run different parts at different sample rates - because
processing a signal at a lower rate is cheaper, and because converting between
rates is a daily need (44.1 kHz audio to 48 kHz, sensor downsampling, software
radio).

## Decimation: rate down by M

To lower the rate by an integer factor $M$ you **decimate**: keep every $M$-th
sample. But you must **lowpass filter first** to below the new Nyquist
($f_s/2M$), or everything above it **aliases** down into your band - the same
sampling rule from the Basics course, applied internally.

$$\\text{decimate} = \\text{anti-alias lowpass} \\;\\to\\; \\downarrow M.$$

## Interpolation: rate up by L

To raise the rate by $L$ you **interpolate**: insert $L-1$ zeros between samples
(**upsampling**), which creates spectral **images**, then **lowpass filter** to
remove the images and fill in the gaps smoothly.

$$\\text{interpolate} = \\uparrow L \\;\\to\\; \\text{anti-imaging lowpass}.$$

Arbitrary rational rate changes (like 44.1k -> 48k = $\\times 160/147$) combine
both: upsample by $L$, filter, downsample by $M$.

```mermaid
flowchart LR
  X["x[n] @ fs"] --> LP1["lowpass (anti-alias)"]
  LP1 --> DOWN["down-sample by M"]
  DOWN --> Y["y[m] @ fs/M"]
```

## Polyphase: do not compute what you throw away

Naively you filter at the high rate then discard most outputs - wasteful. The
**polyphase decomposition** splits the filter into $M$ sub-filters so you compute
**only the samples you keep**, an $M$-fold speedup. This is what makes real-time
sample-rate conversion and software-defined radio practical.

## Filter banks

Split a signal into frequency **sub-bands**, process each at its own (lower) rate,
then recombine. **Perfect-reconstruction** filter banks underpin **MP3/AAC** audio
and the **wavelet** transform (Advanced course). Slide the number of bands to see
the spectrum carved up:

```plot
{"title": "A uniform filter bank carving the band into sub-bands (slide bands)", "xLabel": "normalized frequency (0..1 Nyquist)", "yLabel": "|H| of each band", "xRange": [0, 1], "yRange": [0, 1.2], "grid": true, "controls": [{"name": "bands", "range": [2, 8], "value": 4, "label": "number of sub-bands"}], "functions": [{"expr": "abs(cos(pi*bands*x))", "label": "overlapping band responses"}]}
```

```matlab
M = 4;
h = fir1(48, 1/M);                 % anti-alias lowpass at fs/(2M)
xf = filter(h, 1, x);
y  = xf(1:M:end);                  % decimate by M
xup = upsample(x, M);              % interpolate: insert zeros ...
yi  = filter(h, 1, xup)*M;         % ... then lowpass
```

```python
import numpy as np
M = 4
h = np.sinc(np.arange(-24, 25)/M)/M            # crude anti-alias lowpass
h *= 0.5 - 0.5*np.cos(2*np.pi*np.arange(49)/48)  # window it
x = np.sin(2*np.pi*0.05*np.arange(400))
xf = np.convolve(x, h, mode="same")
y = xf[::M]                                    # decimate by M
```

> **Practical insight:** the cardinal rule of multirate - **filter before you
> downsample, filter after you upsample**. Forget the anti-alias filter and you
> get irreversible aliasing; forget the anti-imaging filter and you get spectral
> images. Polyphase makes both cheap.

**Next:** what happens with finite-precision arithmetic - fixed-point effects.
""",
        ),
        _t(
            "Fixed-point & quantization effects",
            "12 min",
            """\
# Fixed-point & quantization effects

Textbook DSP assumes infinite-precision real numbers. Real DSP runs on hardware
with **finite word length** - 16-bit fixed-point on a cheap microcontroller, or
floating-point on a DSP core - and that finiteness introduces errors you must
budget for.

## Quantization of the signal: the noise floor

An ADC with $B$ bits represents a signal in $2^B$ levels; rounding to the nearest
level adds **quantization noise**. For a full-scale signal the best-case
signal-to-quantization-noise ratio is the famous rule:

$$\\mathrm{SQNR} \\approx 6.02\\,B + 1.76 \\;\\text{dB}.$$

**Every bit buys about 6 dB.** A 16-bit ADC gives ~98 dB of dynamic range; a
12-bit one ~74 dB. Slide the bit depth to see the noise floor drop ~6 dB per bit:

```plot
{"title": "ADC dynamic range: SQNR = 6.02 B + 1.76 dB (slide bit depth)", "xLabel": "signal amplitude (relative)", "yLabel": "SQNR (dB)", "xRange": [0, 1], "yRange": [0, 110], "grid": true, "controls": [{"name": "B", "range": [4, 16], "value": 12, "label": "ADC bits B"}], "functions": [{"expr": "6.02*B + 1.76 + 20*log10(x + 0.001)", "label": "SQNR vs level"}]}
```

## Word length, overflow, and scaling

In fixed-point, sums can exceed the largest representable value - **overflow**.
Two-s-complement overflow **wraps** (a big positive becomes a big negative -
catastrophic), so DSP hardware offers **saturation** (clamp at the rail) instead.
The defence is careful **scaling**: keep intermediate values inside range, often
using guard bits in the accumulator.

## Coefficient quantization

Rounding the **filter coefficients** to finite word length moves the poles and
zeros (we saw this in the structures lesson). A sharp, high-order filter with
poles hugging the unit circle is the most fragile - which is exactly why you ship
it as **second-order sections**, where each pole pair is far less sensitive.

## Limit cycles and dither

- **Limit cycles** - quantization inside an IIR feedback loop can trap it in a
  small self-sustaining oscillation even with zero input. Mitigate with enough
  word length or specific rounding.
- **Dither** - adding a tiny bit of noise *before* quantizing **decorrelates** the
  quantization error from the signal, trading a faint hiss for the removal of ugly
  harmonic distortion. Audio and imaging rely on it.

```mermaid
flowchart LR
  X["analog x(t)"] --> SH["sample & hold"]
  SH --> DTH["+ dither"]
  DTH --> Q["quantize to B bits"]
  Q --> XD["x[n] (with noise floor)"]
```

```matlab
B = 12; full = 1.0;
q = full/2^(B-1);                  % quantization step
xq = round(x/q)*q;                 % quantize
sqnr = 6.02*B + 1.76;              % dB, full-scale sinusoid
xd = round((x + (rand(size(x))-0.5)*q)/q)*q;  % with dither
```

```python
import numpy as np
B, full = 12, 1.0
q = full/2**(B-1)                  # quantization step
xq = np.round(x/q)*q               # quantize
sqnr = 6.02*B + 1.76               # dB
rng = np.random.default_rng(0)
xd = np.round((x + (rng.random(x.shape)-0.5)*q)/q)*q   # with dither
```

> **Practical insight:** pick your number format by the job - **16-bit
> fixed-point** is plenty for voice and control loops and is cheap/low-power;
> **floating-point** saves you from scaling headaches when dynamic range is wide.
> When in doubt, simulate the fixed-point effects before committing to hardware.

**Next:** design and apply real FIR and IIR filters in code.
""",
        ),
        _code(
            "Lab: design & apply an FIR and IIR filter",
            "15 min",
            """\
# Design a windowed-sinc FIR lowpass and a one-pole-pair IIR, then filter a
# noisy two-tone signal. Compare how each cleans a 200 Hz tone out of a 30 Hz one.
import numpy as np
import matplotlib.pyplot as plt

fs = 1000.0                 # sampling rate (Hz)
N = 800
n = np.arange(N)
t = n / fs

# Signal: want the 30 Hz tone, reject the 200 Hz tone, plus a little noise.
rng = np.random.default_rng(1)
x = (np.sin(2*np.pi*30*t)
     + 0.8*np.sin(2*np.pi*200*t)
     + 0.05*rng.standard_normal(N))

# --- FIR lowpass via the windowing method (cutoff 80 Hz) ---
fc = 80.0
M = 64                                  # filter order (even -> odd taps)
k = np.arange(M+1) - M/2
fcn = fc/fs                             # cutoff in cycles/sample
ideal = 2*fcn*np.sinc(2*fcn*k)          # ideal lowpass sinc
ham = 0.54 - 0.46*np.cos(2*np.pi*np.arange(M+1)/M)  # Hamming window
h = ideal*ham                           # FIR coefficients
h /= h.sum()                            # unity DC gain
y_fir = np.convolve(x, h, mode="same")  # apply the FIR

# --- IIR lowpass: a 2nd-order section via the bilinear transform (cutoff 80 Hz) ---
wc = 2*fs*np.tan(np.pi*fc/fs)           # pre-warped analog cutoff
K = wc/(2*fs)
# Bilinear of a critically-damped 2nd-order lowpass wc^2/(s^2 + sqrt(2) wc s + wc^2).
norm = K*K + np.sqrt(2)*K + 1
b = np.array([K*K, 2*K*K, K*K]) / norm
a = np.array([1.0,
              2*(K*K - 1)/norm,
              (K*K - np.sqrt(2)*K + 1)/norm])
y_iir = np.zeros_like(x)                # Direct Form I biquad loop
for i in range(N):
    x1 = x[i-1] if i >= 1 else 0.0
    x2 = x[i-2] if i >= 2 else 0.0
    y1 = y_iir[i-1] if i >= 1 else 0.0
    y2 = y_iir[i-2] if i >= 2 else 0.0
    y_iir[i] = b[0]*x[i] + b[1]*x1 + b[2]*x2 - a[1]*y1 - a[2]*y2

# Frequency responses on the unit circle (no scipy).
w = np.linspace(0, np.pi, 512)
fhz = w*fs/(2*np.pi)
ejw = np.exp(-1j*w)
H_fir = np.polyval(h[::-1], ejw)
H_iir = (b[0] + b[1]*ejw + b[2]*ejw**2) / (a[0] + a[1]*ejw + a[2]*ejw**2)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
ax1.plot(fhz, 20*np.log10(np.abs(H_fir)+1e-12), color="#dc2626",
         label=f"FIR ({M+1} taps)")
ax1.plot(fhz, 20*np.log10(np.abs(H_iir)+1e-12), color="#2563eb",
         label="IIR (3 coeffs)")
ax1.axvline(fc, ls="--", color="#94a3b8")
ax1.set_xlim(0, 300); ax1.set_ylim(-80, 5)
ax1.set_xlabel("frequency (Hz)"); ax1.set_ylabel("|H| (dB)")
ax1.set_title("FIR vs IIR magnitude response (cutoff 80 Hz)")
ax1.legend(); ax1.grid(True)

ax2.plot(t, x, color="#cbd5e1", label="noisy input")
ax2.plot(t, y_fir, color="#dc2626", lw=1.5, label="FIR output")
ax2.plot(t, y_iir, color="#2563eb", lw=1.5, label="IIR output")
ax2.set_xlim(0, 0.2)
ax2.set_xlabel("time (s)"); ax2.set_ylabel("amplitude")
ax2.set_title("Both pass the 30 Hz tone and reject the 200 Hz tone")
ax2.legend(); ax2.grid(True)
plt.tight_layout(); plt.show()

print(f"FIR taps = {M+1} (linear phase), IIR coeffs = {len(b)+len(a)} (sharper, cheaper)")
print(f"FIR group delay ~ {M/2:.0f} samples = {M/2/fs*1000:.1f} ms")

# Try it yourself:
#   1. Halve M to 32: the FIR transition gets wider (less sharp).
#   2. The MATLAB way: h = fir1(64, 80/(fs/2)); [b,a] = butter(2, 80/(fs/2));
""",
        ),
    ),
)


# -- Digital Signal Processing -- Advanced -------------------------------------

_DSP_ADVANCED = SeedCourse(
    slug="dsp-advanced",
    title="Digital Signal Processing -- Advanced: Adaptive, Spectral & Real-Time",
    description=(
        "Advanced DSP: adaptive filters (LMS/RLS for echo and noise "
        "cancellation), spectral estimation (periodogram, Welch, parametric/AR), "
        "DSP for communications (matched filter, equalization, synchronization), "
        "real-time and embedded DSP (MAC/SIMD, block processing, latency), and "
        "multidimensional/modern DSP (2D, wavelets, ties to machine learning) - "
        "with dual MATLAB/Python, interactive plots, and a runnable LMS noise-"
        "canceller lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Adaptive filters: LMS & RLS",
            "13 min",
            """\
# Adaptive filters: LMS & RLS

A fixed filter assumes you know the signal in advance. An **adaptive filter**
**learns and adjusts its own coefficients** in real time to minimise an error -
the system identifies the environment as it runs. This is the DSP that cancels the
echo on your phone call and the noise under your headphones.

## The setup

The filter produces $y[n] = \\mathbf{w}^T \\mathbf{x}[n]$ from its current weights
$\\mathbf{w}$, compares it to a **desired** signal $d[n]$ to get an error
$e[n] = d[n] - y[n]$, and **nudges the weights** to shrink that error.

```mermaid
flowchart LR
  X["x[n]"] --> FIR["adaptive FIR (weights w)"]
  FIR --> Y["y[n]"]
  D["desired d[n]"] --> SUB(("-"))
  Y --> SUB
  SUB --> E["error e[n]"]
  E --> UPD["update rule (LMS / RLS)"]
  UPD --> FIR
```

## LMS: the simple, robust one

The **Least Mean Squares** algorithm does gradient descent on the squared error:

$$\\mathbf{w}[n+1] = \\mathbf{w}[n] + \\mu\\,e[n]\\,\\mathbf{x}[n].$$

One multiply-add per tap - dirt cheap, which is why it is everywhere. The **step
size** $\\mu$ is the whole game: too small and it crawls; too large and it
overshoots or diverges. Slide $\\mu$ to watch the error curve converge fast,
slowly, or blow up:

```plot
{"title": "LMS learning curve: error vs iteration (slide step size mu)", "xLabel": "iteration n", "yLabel": "mean-square error", "xRange": [0, 100], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "mu", "range": [0.01, 0.6], "value": 0.2, "label": "step size mu"}], "functions": [{"expr": "exp(-mu*x) + 0.03", "label": "MSE(n) (faster as mu rises)"}]}
```

## RLS: faster, costlier

**Recursive Least Squares** uses the full correlation history (a running inverse
of the input correlation matrix) to converge in far fewer iterations - at
$O(L^2)$ cost per sample versus LMS's $O(L)$. Use RLS when fast convergence is
worth the compute (channel equalization); use LMS when cheap and robust wins.

## The four canonical applications

| Mode | $d[n]$ is | Does |
|------|-----------|------|
| **System identification** | unknown system's output | learn a model of it |
| **Noise cancellation** | signal + noise | subtract a correlated noise reference |
| **Echo cancellation** | near + echo of far end | model and remove the echo path |
| **Equalization** | known training symbols | invert a distorting channel |

Acoustic **echo cancellers** (speakerphones, conferencing) and **active noise
cancelling** headphones are LMS/RLS running millions of times a second.

```matlab
mu = 0.01; L = 32; w = zeros(L,1);
for n = L:length(x)
  xn = x(n:-1:n-L+1);
  y(n)  = w' * xn;
  e(n)  = d(n) - y(n);
  w = w + mu * e(n) * xn;          % LMS update
end
```

```python
import numpy as np
mu, L = 0.01, 32
w = np.zeros(L)
y = np.zeros(len(x)); e = np.zeros(len(x))
for n in range(L, len(x)):
    xn = x[n:n-L:-1]
    y[n] = w @ xn
    e[n] = d[n] - y[n]
    w += mu*e[n]*xn                # LMS update
```

> **Practical insight:** stability of LMS needs $0 < \\mu < 2/(L\\,P_x)$ where
> $P_x$ is the input power - so engineers use **normalized LMS (NLMS)**, dividing
> the step by the instantaneous input energy, which makes $\\mu$ easy to tune and
> robust to signal level.

**Next:** estimating a spectrum properly - spectral estimation.
""",
        ),
        _t(
            "Spectral estimation",
            "13 min",
            """\
# Spectral estimation

A single FFT of a noisy, finite record is a **terrible** spectrum estimate - it
is wildly variable and biased by leakage. **Spectral estimation** is the science
of getting a trustworthy estimate of the **power spectral density (PSD)**, the
distribution of power over frequency. It powers radar, vibration monitoring,
speech, radio astronomy, and EEG analysis.

## The periodogram and its flaw

The **periodogram** is just the squared FFT magnitude:

$$\\hat{S}(f) = \\frac{1}{N}\\,|X(f)|^2.$$

Its fatal flaw: its **variance does not shrink** as you collect more data - more
samples give finer resolution but an equally jagged, noisy estimate. You must
**average** to tame it.

## Welch's method: average to reduce variance

**Welch's method** is the practical default: chop the signal into **overlapping
segments**, window each, periodogram each, and **average** the periodograms.
Averaging $K$ segments cuts the variance by about $K$ - the spectrum smooths out -
at the cost of coarser frequency resolution (shorter segments). It is the
**bias-variance trade-off** in spectral form. More averages give a smoother PSD:

```plot
{"title": "Welch averaging smooths a noisy spectrum (slide # of segments)", "xLabel": "frequency bin", "yLabel": "PSD estimate", "xRange": [0, 50], "yRange": [0, 1.4], "grid": true, "controls": [{"name": "K", "range": [1, 20], "value": 4, "label": "segments averaged K"}], "functions": [{"expr": "0.6 + 0.5*exp(-((x-25)/4)^2) + (0.5/sqrt(K))*sin(2*x)", "label": "PSD (ripple ~ 1/sqrt(K))"}]}
```

```mermaid
flowchart LR
  SIG["long signal"] --> SEG["overlapping segments"]
  SEG --> WIN["window each"]
  WIN --> PER["periodogram each"]
  PER --> AVG["average -> Welch PSD"]
```

## Parametric (model-based) methods

Instead of transforming the data, **fit a model** and read the spectrum from its
parameters. The **autoregressive (AR)** model assumes the signal is white noise
through an all-pole filter; solve the **Yule-Walker** equations (or use
Burg's method) for the coefficients. AR methods give **sharp peaks from short
records** - excellent when you know the signal is a few sinusoids/resonances
(speech formants, vibration modes), but they can hallucinate peaks if the model
order is wrong. **MUSIC** and **ESPRIT** are subspace methods that resolve
closely spaced sinusoids beyond the FFT's resolution limit.

```matlab
[Pxx, f] = pwelch(x, hann(256), 128, 512, fs);   % Welch PSD
arc = arburg(x, 12);                              % 12th-order AR (Burg)
[Har, fa] = freqz(1, arc, 512, fs);               % AR spectrum (all-pole)
```

```python
import numpy as np
seg, nover = 256, 128
win = np.hanning(seg); step = seg - nover
psd = np.zeros(seg//2 + 1)
count = 0
for start in range(0, len(x)-seg+1, step):
    Xs = np.fft.rfft(x[start:start+seg]*win)
    psd += (np.abs(Xs)**2)                        # accumulate periodograms
    count += 1
psd /= count                                      # Welch average
f = np.fft.rfftfreq(seg, 1/fs)
```

> **Practical insight:** for a robust general PSD use **Welch** (longer segments
> = better resolution, more segments = less variance - you cannot max both at a
> fixed record length). Reach for **AR/MUSIC** only when you genuinely have a few
> narrow tones and a short record, and always sanity-check the model order.

**Next:** DSP that moves data - communications.
""",
        ),
        _t(
            "DSP for communications",
            "13 min",
            """\
# DSP for communications

Every modern radio - WiFi, 5G, GPS, a TV remote, a satellite link - is mostly
**DSP**. The analog front end just shifts frequency; the real work of shaping,
recovering, and cleaning up symbols happens in the digital domain.

## The matched filter: best detection in noise

To decide which symbol was sent through a noisy channel, correlate the received
signal with a **template** of the expected pulse. The **matched filter**
(impulse response = the time-reversed transmit pulse) **maximises the
signal-to-noise ratio** at the sampling instant - it is provably the optimal
linear detector in white noise. It is why your receiver still works at the edge
of range, and it is mathematically the same correlation that **radar** and **GPS**
use to find a faint echo or lock a code.

$$\\mathrm{SNR}_{out} \\text{ is maximised when } h[n] = s[-n].$$

## Equalization: undo the channel

A real channel **smears** each symbol into the next - **inter-symbol interference
(ISI)** - because of multipath and limited bandwidth. An **equalizer** is an
(often adaptive, LMS/RLS) filter that **inverts the channel** to reopen the eye.
The **eye diagram** is the field's favourite tool: overlay many symbol periods and
a wide-open "eye" means clean detection; a closed eye means errors. Slide the ISI
to watch the eye close:

```plot
{"title": "Eye diagram opening: more ISI closes the eye (slide ISI)", "xLabel": "time within symbol", "yLabel": "amplitude", "xRange": [-1, 1], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "isi", "range": [0, 0.9], "value": 0.2, "label": "inter-symbol interference"}], "functions": [{"expr": "(1-isi)*cos(pi*x/2)", "label": "upper trace", "color": "#16a34a"}, {"expr": "-(1-isi)*cos(pi*x/2)", "label": "lower trace", "color": "#dc2626"}]}
```

## Synchronization: line up in time and frequency

The receiver does not know exactly when a symbol starts (**timing recovery**) or
the transmitter's exact carrier frequency/phase (**carrier recovery**). DSP loops
- the **PLL (phase-locked loop)**, early-late gate, Costas loop - track and lock
these. Get synchronization wrong and even a perfect equalizer reads garbage.

```mermaid
flowchart LR
  RX["received samples"] --> MF["matched filter"]
  MF --> SYNC["timing & carrier sync (PLL)"]
  SYNC --> EQ["adaptive equalizer (LMS)"]
  EQ --> DEC["symbol decision"]
  DEC --> BITS["bits out"]
```

```matlab
pulse = ones(1,8)/sqrt(8);          % transmit pulse
mf = fliplr(pulse);                 % matched filter = time-reversed pulse
r  = conv(rx, mf);                  % correlate
sym = r(8:8:end);                   % sample at symbol centres
```

```python
import numpy as np
pulse = np.ones(8)/np.sqrt(8)       # transmit pulse
mf = pulse[::-1]                    # matched filter = time-reversed pulse
r = np.convolve(rx, mf)             # correlate
sym = r[7::8]                       # sample at symbol centres
```

> **Practical insight:** the receiver chain is an order of operations - matched
> filter, **then** synchronize, **then** equalize, **then** decide. Modern systems
> (OFDM in WiFi/5G) lean hard on the FFT to turn a messy multipath channel into
> many simple flat subchannels, each easy to equalize with one complex multiply.

**Next:** making it run in real time - embedded DSP.
""",
        ),
        _t(
            "Real-time & embedded DSP",
            "12 min",
            """\
# Real-time & embedded DSP

An algorithm that works in a notebook is half the job. **Real-time** DSP must
keep up with the data **forever**, within a tight latency and power budget, on
constrained hardware. This is where the elegant math meets the silicon.

## The DSP processor and the MAC

The inner loop of almost all DSP is the **multiply-accumulate**:
$\\mathrm{acc} \\mathrel{+}= h[k]\\,x[n-k]$. DSP processors and modern CPUs build
hardware to do this in **one cycle**, often many in parallel:

- **MAC unit** - multiply and add in a single instruction, with a wide
  accumulator (guard bits) to avoid overflow.
- **SIMD** (NEON, AVX) - one instruction processes a vector of samples at once.
- **Circular buffers** and **zero-overhead loops** - hardware addressing for the
  delay line so no cycles are wasted on bookkeeping.

A direct convolution of $N$ taps over $M$ samples is $N M$ MACs - throughput is
counted in **MACs per second**, and it sets whether your filter fits the budget.
Slide the tap count to see the MAC load (and thus power/clock) climb:

```plot
{"title": "Compute load: MACs per second vs FIR tap count (fs = 48 kHz)", "xLabel": "FIR taps N", "yLabel": "MACs/sec (millions)", "xRange": [0, 256], "yRange": [0, 14], "grid": true, "controls": [{"name": "fs_k", "range": [8, 192], "value": 48, "label": "sample rate (kHz)"}], "functions": [{"expr": "x*fs_k/1000", "label": "N * fs (M MAC/s)"}]}
```

## Block processing and latency

Processing **sample-by-sample** has minimal latency but poor efficiency; processing
in **blocks** (frames) amortises overhead and unlocks the FFT for **fast
convolution** (overlap-add / overlap-save) and SIMD - but a block of $B$ samples
adds $B/f_s$ of **latency**. That trade-off is a hard product constraint: live
monitoring and hearing aids need sub-10 ms; streaming audio can buffer more.

```mermaid
stateDiagram-v2
  [*] --> Fill
  Fill --> Process: block of B samples ready
  Process --> Output: filtered block
  Output --> Fill: next block (latency = B / fs)
```

## Fixed vs floating point on real hardware

Revisiting the Intermediate lesson with a hardware hat on: **fixed-point** DSPs
and MCUs are cheaper and lower power (great for billions of earbuds and sensors)
but need careful scaling; **floating-point** cores and GPUs cost more power but
free you from overflow and scaling headaches. Many chips now do both, and
energy-per-sample is often the real design driver.

```matlab
% Overlap-add fast convolution of a long signal with FIR h.
Nfft = 1024; L = Nfft - length(h) + 1;
H = fft(h, Nfft);
% loop blocks of length L, FFT, multiply by H, ifft, overlap-add ...
```

```python
import numpy as np
Nfft = 1024
h = np.ones(64)/64
L = Nfft - len(h) + 1               # block (hop) length
H = np.fft.rfft(h, Nfft)            # precompute filter spectrum once
# Each block: Y = rfft(block, Nfft) * H; y = irfft(Y); overlap-add the tails.
```

> **Practical insight:** profile the **inner loop** and count MACs before
> optimising anything else - that is where the cycles and the power go. Choose
> block size by your **latency budget**, then use FFT-based fast convolution and
> SIMD to hit throughput.

**Next:** beyond one dimension and into the modern era.
""",
        ),
        _t(
            "Multidimensional & modern DSP",
            "13 min",
            """\
# Multidimensional & modern DSP

Everything so far has been **1-D** signals in time. The same ideas generalise to
**images, video, and volumes**, and connect directly to the wavelet transform and
machine learning that dominate modern signal work.

## 2-D DSP: images

An image is a 2-D signal $x[m,n]$. Convolution becomes a **2-D kernel** sliding
over the image: a blur kernel is a 2-D lowpass, an edge detector (Sobel,
Laplacian) is a 2-D highpass, and the **2-D FFT** reveals spatial frequencies
(used in JPEG, which actually uses the related **DCT** on 8x8 blocks). Sampling
theory still rules - downscale an image without an anti-alias blur and you get
**moire** aliasing, the same effect as audio aliasing in 2-D.

## Wavelets: when frequency is not enough

The FFT tells you **which** frequencies are present but not **when** - it smears
a transient across the whole spectrum. **Wavelets** give a **time-frequency**
view: good time resolution for high frequencies (sharp transients) and good
frequency resolution for low ones (slow trends). Built from the multirate filter
banks of the Intermediate course, they underpin **JPEG-2000** image compression,
denoising, and biomedical transient detection. The trade-off is fundamental
(the uncertainty principle): you cannot have arbitrarily sharp time **and**
frequency resolution at once. Slide the analysis scale to trade one for the other:

```plot
{"title": "Time-frequency trade-off: wide-in-time = narrow-in-frequency (slide scale)", "xLabel": "time", "yLabel": "wavelet amplitude", "xRange": [-5, 5], "yRange": [-1.1, 1.1], "grid": true, "controls": [{"name": "scale", "range": [0.4, 3], "value": 1, "label": "wavelet scale"}], "functions": [{"expr": "exp(-(x/scale)^2/2)*cos(5*x/scale)", "label": "Morlet wavelet"}]}
```

## Modern DSP meets machine learning

The boundary between classical DSP and ML has blurred:

- A **convolutional neural network** is literally banks of **learned FIR filters**
  - the convolution you have used all course, with weights found by training
  instead of by design.
- **Feature front-ends** - the **MFCC** (mel-frequency cepstral coefficients)
  behind speech recognition is FFT + filter bank + log + DCT, pure DSP feeding the
  model.
- DSP still does the **conditioning** (resampling, filtering, denoising, framing,
  spectrograms) that makes the learned model work, and physical-model DSP often
  beats data-hungry ML when the math is known.

```mermaid
flowchart LR
  RAW["raw signal"] --> DSP["DSP front-end: filter, resample, FFT/wavelet"]
  DSP --> FEAT["features (spectrogram / MFCC)"]
  FEAT --> ML["learned model (CNN/RNN)"]
  ML --> OUT["decision"]
```

```matlab
img = imread('cameraman.tif');
kx = [-1 0 1; -2 0 2; -1 0 1];        % Sobel horizontal edge kernel
edges = conv2(double(img), kx, 'same');% 2-D convolution
F = fft2(double(img));                 % 2-D spectrum
```

```python
import numpy as np
img = np.random.rand(64, 64)           # stand-in image
kx = np.array([[-1, 0, 1],             # Sobel horizontal edge kernel
               [-2, 0, 2],
               [-1, 0, 1]])
# 2-D convolution via two nested correlations / FFT2 in practice:
F = np.fft.fft2(img)                    # 2-D spectrum
```

> **Practical insight:** the single most reusable idea in all of DSP is
> **convolution / filtering** - it is the moving average, the FIR filter, the
> image kernel, and the CNN layer, all the same operation. Master it and most of
> signal processing is variations on a theme.

**Next:** where all of this lands in the real world.
""",
        ),
        _t(
            "Applications & the throughline",
            "11 min",
            """\
# Applications & the throughline

DSP is invisible infrastructure - it runs inside almost every device you touch.
Here is where the ideas from all three courses land in real systems.

## Real systems, mapped to what you learned

| Application | DSP doing the work |
|-------------|--------------------|
| **Phone call / VoIP** | echo cancellation (LMS), voice codecs (LPC/lattice), noise suppression |
| **Active-noise headphones** | adaptive filtering (NLMS) cancelling ambient noise in real time |
| **WiFi / 5G / LTE** | FFT-based OFDM, matched filtering, channel equalization, synchronization |
| **Music streaming (MP3/AAC)** | filter banks + perceptual coding; the DCT/MDCT |
| **Image / video (JPEG, H.264)** | 2-D DCT, motion-compensated prediction, quantization |
| **Radar / sonar / GPS** | matched filtering and correlation to find faint echoes/codes |
| **MRI / ultrasound / CT** | FFT-based reconstruction from frequency-space data |
| **Speech assistants** | MFCC front-end (FFT + filter bank) feeding a neural net |
| **Industrial / automotive** | vibration spectral analysis, sensor filtering, control loops |
| **Hearing aids** | multiband compression with hard real-time latency limits |

## The throughline

Everything in this track is one short story. **Sample** a signal (respect Nyquist
or pay in aliasing). Describe systems by their **impulse response** and combine
them by **convolution**. Move to the frequency domain with the **z-transform** and
compute it with the **FFT**, mindful of **windowing and leakage**. **Design
filters** - FIR for linear phase, IIR for sharp-and-cheap - and **implement** them
in robust structures at the right sample rate and word length. When the
environment is unknown or changing, let the filter **adapt** (LMS/RLS). Estimate
**spectra** honestly (Welch, AR). Move bits through channels with **matched
filtering, equalization, and synchronization**. Make it run in **real time** on
real hardware. And generalise to **images, wavelets, and learned filters** - where
classical DSP and machine learning meet.

```mermaid
flowchart LR
  SAMPLE["sample (Nyquist)"] --> LTI["LTI + convolution"]
  LTI --> FREQ["z-transform / FFT"]
  FREQ --> DESIGN["filter design (FIR/IIR)"]
  DESIGN --> IMPL["structures, multirate, fixed-point"]
  IMPL --> ADAPT["adaptive + spectral estimation"]
  ADAPT --> APPS["comms, real-time, images, ML"]
```

## Where to go next

The same backbone powers the **Communications**, **Control**, and **Signals**
tracks; the linear algebra of subspace methods links to **Statistics/ML**; and the
hardware side runs straight into **Embedded** and **FPGA** design. Pick a real
signal you care about - your voice, a sensor, an image - and rebuild one block of
this pipeline end to end. The tools (MATLAB and Python with numpy) you have used
all track are exactly the ones practising engineers reach for.

> **Practical insight:** the fastest way to internalise DSP is to **measure and
> plot** at every stage - look at the time signal, then its spectrum, then the
> filtered result. Most real bugs (an alias, a leakage artefact, an unstable
> pole, a fixed-point overflow) are obvious the moment you plot them.

**Next:** the final check.
""",
        ),
        _code(
            "Lab: an LMS adaptive noise canceller",
            "15 min",
            """\
# Adaptive noise cancellation with the LMS algorithm.
# A clean tone is buried in noise; a correlated noise reference lets an adaptive
# FIR learn to subtract the noise out - the math behind noise-cancelling headsets.
import numpy as np
import matplotlib.pyplot as plt

fs = 8000.0                 # sampling rate (Hz)
N = 4000
n = np.arange(N)
t = n / fs

# The signal we want to recover: a 300 Hz tone (think: speech, simplified).
signal = np.sin(2*np.pi*300*t)

# The interfering noise reaches the mic through an unknown "acoustic path"
# (a short FIR), and we also have a reference of the raw noise nearby.
rng = np.random.default_rng(2)
noise_ref = rng.standard_normal(N)                 # reference noise (e.g. outer mic)
path = np.array([0.6, -0.3, 0.2, 0.1, -0.05])      # unknown room/leakage path
noise_at_mic = np.convolve(noise_ref, path)[:N]    # noise as it hits the main mic

primary = signal + noise_at_mic                    # what the main mic records

# --- LMS adaptive filter learns the path and predicts the noise to subtract ---
L = 16                       # adaptive FIR length
mu = 0.05                    # NLMS step size (normalized below)
w = np.zeros(L)
e = np.zeros(N)              # error = cleaned output (signal estimate)
yhat = np.zeros(N)          # filter's estimate of the noise at the mic
eps = 1e-6

for i in range(L, N):
    xvec = noise_ref[i:i-L:-1]          # last L reference samples
    yhat[i] = w @ xvec                  # estimate of the noise at the mic
    e[i] = primary[i] - yhat[i]         # remove it -> recovered signal + residual
    norm = xvec @ xvec + eps            # NLMS normalization (robust step)
    w += (mu/norm) * e[i] * xvec        # LMS/NLMS weight update

# Learning curve: short-time error power should drop as the filter converges.
win = 200
err_power = np.array([np.mean(e[max(0, k-win):k+1]**2) for k in range(N)])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
ax1.plot(t, primary, color="#cbd5e1", label="mic: signal + noise")
ax1.plot(t, e, color="#dc2626", lw=1.2, label="LMS output (cleaned)")
ax1.plot(t, signal, color="#16a34a", lw=0.8, alpha=0.7, label="true signal")
ax1.set_xlim(0.3, 0.36)
ax1.set_xlabel("time (s)"); ax1.set_ylabel("amplitude")
ax1.set_title("LMS noise canceller: the 300 Hz tone re-emerges")
ax1.legend(loc="upper right"); ax1.grid(True)

ax2.plot(t, err_power, color="#2563eb")
ax2.set_xlabel("time (s)"); ax2.set_ylabel("short-time error power")
ax2.set_title("Learning curve: error power falls as the weights converge")
ax2.grid(True)
plt.tight_layout(); plt.show()

snr_before = 10*np.log10(np.mean(signal**2)/np.mean(noise_at_mic**2))
resid = e[N//2:] - signal[N//2:]
snr_after = 10*np.log10(np.mean(signal**2)/np.mean(resid**2))
print(f"SNR before cancellation: {snr_before:6.2f} dB")
print(f"SNR after  cancellation: {snr_after:6.2f} dB")
print(f"improvement: {snr_after - snr_before:6.2f} dB")

# Try it yourself:
#   1. Raise mu toward 0.3: faster convergence but a noisier steady state.
#   2. Shorten L to 4 (< path length): the filter cannot model the path -> worse.
#   3. The MATLAB way: dsp.LMSFilter, or the hand loop with w = w + mu*e*xvec.
""",
        ),
    ),
)


DSP_COURSES: tuple[SeedCourse, ...] = (
    _DSP_BASICS,
    _DSP_INTERMEDIATE,
    _DSP_ADVANCED,
)

__all__ = ["DSP_COURSES"]
