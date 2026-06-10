"""Curated Signals & Systems track: Basics, Intermediate, Advanced.

Teaches signals and systems with a dual MATLAB + Python focus: every concept
shows both languages side by side (illustrative ```matlab / ```python fences),
runnable Python ``code`` lessons (numpy + matplotlib) the learner executes in
the sandbox, interactive ```plot blocks for sinusoids / spectra / convolution /
Fourier synthesis, Mermaid system diagrams, LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/signals_*.py) at assembly time, so this module
holds content lessons only.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ── Signals & Systems — Basics ────────────────────────────────────────────────

_SIGNALS_BASICS = SeedCourse(
    slug="signals-basics",
    title="Signals & Systems — Basics",
    description=(
        "What signals are and how to describe them: continuous vs. discrete "
        "time, the elementary signals every engineer reuses, signal operations, "
        "and sampling — with side-by-side MATLAB and Python, interactive plots, "
        "and a runnable synthesis lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is a signal?",
            "8 min",
            """\
# What is a signal?

A **signal** is a function that carries information by varying with an
independent variable — almost always **time**. Audio is air pressure vs. time;
an ECG is voltage vs. time; a stock price is value vs. time.

Two big families, by the **time axis**:

- **Continuous-time (CT)** — defined for every instant, written $x(t)$.
- **Discrete-time (DT)** — defined only at integer indices, written $x[n]$,
  usually obtained by **sampling** a CT signal.

```mermaid
flowchart LR
  W[Real world: sound, light, voltage] --> S[Sensor] --> CT["x(t) continuous"]
  CT --> ADC[Sampler / ADC] --> DT["x[n] discrete"]
  DT --> P[Computer: MATLAB / Python]
```

## A first signal: the sinusoid

The most important signal of all is the sinusoid
$x(t) = A\\cos(2\\pi f t + \\phi)$ — amplitude $A$, frequency $f$ (Hz), phase
$\\phi$. Drag the controls and watch it change:

```plot
{"title": "A sinusoid x(t) = A cos(2 pi f t + phi)", "xLabel": "t (s)", "yLabel": "x(t)", "xRange": [0, 1], "yRange": [-2.2, 2.2], "grid": true, "controls": [{"name": "A", "range": [0.2, 2], "value": 1, "label": "amplitude A"}, {"name": "f", "range": [1, 10], "value": 3, "label": "frequency f (Hz)"}, {"name": "phi", "range": [0, 6.28], "value": 0, "label": "phase phi (rad)"}], "functions": [{"expr": "A*cos(2*pi*f*x + phi)", "label": "x(t)"}]}
```

## Same signal, two languages

```matlab
fs = 500; t = 0:1/fs:1;          % time vector, 500 samples/sec
x = cos(2*pi*3*t);               % 3 Hz cosine
plot(t, x); xlabel('t (s)'); ylabel('x(t)');
```

```python
import numpy as np
fs = 500
t = np.arange(0, 1, 1/fs)        # time vector
x = np.cos(2*np.pi*3*t)          # 3 Hz cosine
```

Notice the symmetry: MATLAB's `0:1/fs:1` is numpy's `np.arange`, and the math is
identical. Throughout this track you'll see both.

**Next:** the handful of elementary signals everything is built from.
""",
        ),
        _t(
            "Elementary signals",
            "11 min",
            """\
# Elementary signals

A few building blocks reappear everywhere. Learn these and you can describe
almost any signal as a combination of them.

| Signal | CT form | What it models |
|--------|---------|----------------|
| Sinusoid | $\\cos(2\\pi f t)$ | tones, AC, oscillation |
| Real exponential | $e^{at}$ | growth ($a>0$) / decay ($a<0$) |
| Unit step | $u(t)$ = 0 then 1 | a switch turning on |
| Unit impulse | $\\delta(t)$ | an instantaneous "kick" |
| Ramp | $r(t) = t\\,u(t)$ | a steadily rising input |

## Exponentials: growth and decay

$$x(t) = e^{a t}.$$

```plot
{"title": "Real exponential e^(a t)", "xLabel": "t", "yLabel": "x(t)", "xRange": [0, 3], "yRange": [0, 4], "grid": true, "controls": [{"name": "a", "range": [-2, 1], "value": -1, "label": "rate a"}], "functions": [{"expr": "exp(a*x)", "label": "e^(a t)"}]}
```

Negative $a$ decays (an RC circuit discharging); positive $a$ grows.

## Step and impulse

The **unit step** $u(t)$ jumps from 0 to 1 at $t=0$ — the model of "switch on".
The **unit impulse** $\\delta(t)$ is its derivative: infinitely narrow, unit area,
the idealized "tap". In discrete time they're concrete:
$\\delta[n] = 1$ at $n=0$ (else 0), and $u[n]=1$ for $n\\ge 0$.

```matlab
n = -5:10;
delta = (n == 0);                % unit impulse
step  = (n >= 0);                % unit step
stem(n, step);
```

```python
import numpy as np
n = np.arange(-5, 11)
delta = (n == 0).astype(float)   # unit impulse
step  = (n >= 0).astype(float)   # unit step
```

> Why care about $\\delta$? Because the response of a linear system to an impulse
> — its **impulse response** — tells you its response to *everything* (next
> course).

**Next:** reshaping signals with time and amplitude operations.
""",
        ),
        _t(
            "Signal operations",
            "10 min",
            """\
# Signal operations

You transform signals by operating on the **amplitude** or the **time axis**.

- **Amplitude scaling:** $y(t) = c\\,x(t)$ (volume knob).
- **Time shift:** $y(t) = x(t - t_0)$ — shift **right** (delay) for $t_0 > 0$.
- **Time scaling:** $y(t) = x(a t)$ — $a>1$ speeds up / compresses.
- **Time reversal:** $y(t) = x(-t)$ — play it backwards.

Watch a shift and a reversal of the same pulse:

```plot
{"title": "Original vs shifted vs reversed", "xLabel": "t", "yLabel": "x(t)", "xRange": [-3, 5], "yRange": [-0.2, 1.2], "grid": true, "functions": [{"expr": "exp(-(x-1)^2)", "label": "x(t)", "color": "#2563eb"}, {"expr": "exp(-(x-3)^2)", "label": "x(t-2) delay", "color": "#dc2626"}, {"expr": "exp(-(x+1)^2)", "label": "x(-t) reversed-ish", "color": "#16a34a"}]}
```

## The order matters

For $y(t) = x(a t - t_0)$, **shift then scale** — it's $x(a(t - t_0/a))$. Getting
the order wrong is the classic exam mistake.

```matlab
t = -3:0.01:5;
x = exp(-(t-1).^2);
y = exp(-((t-2)-1).^2);          % x(t-2): delay by 2
```

```python
import numpy as np
t = np.arange(-3, 5, 0.01)
x = np.exp(-(t-1)**2)
y = np.exp(-((t-2)-1)**2)         # x(t-2): delay by 2
```

**Next:** crossing from the continuous world to the discrete one — sampling.
""",
        ),
        _t(
            "Sampling & the discrete world",
            "11 min",
            """\
# Sampling & the discrete world

Computers can't store $x(t)$ for every instant — they store **samples** taken
every $T_s$ seconds at rate $f_s = 1/T_s$:

$$x[n] = x(n T_s).$$

```plot
{"title": "Sampling a 3 Hz sine", "xLabel": "t (s)", "yLabel": "x", "xRange": [0, 1], "yRange": [-1.3, 1.3], "grid": true, "functions": [{"expr": "sin(2*pi*3*x)", "label": "x(t)", "color": "#94a3b8"}], "series": [{"points": [[0, 0], [0.083, 1], [0.167, 0], [0.25, -1], [0.333, 0], [0.417, 1], [0.5, 0], [0.583, -1], [0.667, 0], [0.75, 1], [0.833, 0], [0.917, -1], [1, 0]], "label": "samples (fs=12)", "color": "#dc2626"}]}
```

## How fast must you sample? Nyquist

The **Nyquist-Shannon theorem**: to capture a signal whose highest frequency is
$f_{max}$, sample at

$$f_s > 2 f_{max}.$$

Sample too slowly and high frequencies masquerade as low ones — **aliasing**
(the wagon-wheel effect in old films, where spokes appear to spin backwards).
CD audio uses $f_s = 44.1\\,\\text{kHz}$ to cover the $\\sim 20\\,\\text{kHz}$ limit
of human hearing.

```matlab
fs = 1000; t = 0:1/fs:1;         % 1 kHz sampling
x  = sin(2*pi*50*t);             % 50 Hz tone -> fine (1000 > 2*50)
```

```python
import numpy as np
fs = 1000
t  = np.arange(0, 1, 1/fs)
x  = np.sin(2*np.pi*50*t)        # 50 Hz tone -> fine (1000 > 2*50)
```

> Rule of thumb: pick $f_s$ at least **2x** (in practice 5-10x) your highest
> frequency of interest, and filter out anything above $f_s/2$ *before*
> sampling (an anti-aliasing filter).

**Next:** put it together — synthesize and plot a real signal yourself.
""",
        ),
        _code(
            "Lab: synthesize & plot a signal",
            "10 min",
            """\
# Synthesize a two-tone signal and plot it.
# Edit the frequencies/amplitudes and press Run.
import numpy as np
import matplotlib.pyplot as plt

fs = 500                          # sampling rate (Hz)
t = np.arange(0, 1, 1/fs)         # 1 second of time

# Two sinusoids plus a little noise:
x = 1.0*np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*20*t)
x = x + 0.2*np.random.randn(len(t))

plt.figure(figsize=(8, 3))
plt.plot(t, x, color="#2563eb")
plt.xlabel("t (s)"); plt.ylabel("x(t)")
plt.title("x(t) = sin(2 pi 5 t) + 0.5 sin(2 pi 20 t) + noise")
plt.grid(True)
plt.show()

print(f"samples: {len(x)},  fs: {fs} Hz,  duration: {t[-1]:.2f} s")
print(f"min={x.min():.2f}  max={x.max():.2f}  mean={x.mean():.3f}")

# Try it yourself:
#   1. Change 20 -> 60 and watch the wiggles get faster.
#   2. Raise the noise from 0.2 to 1.0 — can you still see the tones?
#   3. The MATLAB equivalent:
#        fs=500; t=0:1/fs:1; x=sin(2*pi*5*t)+0.5*sin(2*pi*20*t); plot(t,x)
""",
        ),
    ),
)


# ── Signals & Systems — Intermediate ──────────────────────────────────────────

_SIGNALS_INTERMEDIATE = SeedCourse(
    slug="signals-intermediate",
    title="Signals & Systems — Intermediate",
    description=(
        "Systems and the frequency domain: LTI system properties, impulse "
        "response and convolution, Fourier series and the spectrum, the Fourier "
        "transform (FFT), and basic filtering — with dual MATLAB/Python, "
        "interactive plots, and a runnable FFT lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Systems & their properties",
            "10 min",
            """\
# Systems & their properties

A **system** takes an input signal and produces an output: $y = T\\{x\\}$. An
amplifier, a room's echo, a moving average — all systems.

```mermaid
flowchart LR
  X["x(t) input"] --> SYS["System T"] --> Y["y(t) output"]
```

Two properties matter most, because together they unlock all the theory:

- **Linear** — scaling and adding inputs scales and adds outputs:
  $T\\{a x_1 + b x_2\\} = a\\,T\\{x_1\\} + b\\,T\\{x_2\\}$ (superposition).
- **Time-invariant** — delaying the input just delays the output:
  if $x(t)\\to y(t)$ then $x(t - t_0) \\to y(t - t_0)$.

A system with **both** is **LTI** — *linear, time-invariant* — the class this
whole course is built around.

| Property | Means | Example that fails it |
|----------|-------|------------------------|
| Linear | superposition holds | $y = x^2$ (squaring) |
| Time-invariant | behaviour doesn't drift | $y(t) = t\\,x(t)$ |
| Causal | output uses only past/present | an ideal predictor |
| Stable (BIBO) | bounded in -> bounded out | an integrator of a step |

> Why obsess over LTI? Because an LTI system is **completely** described by one
> signal — its impulse response — and its action becomes simple multiplication
> in the frequency domain. That's the next two lessons.

**Next:** the impulse response and convolution.
""",
        ),
        _t(
            "Impulse response & convolution",
            "12 min",
            """\
# Impulse response & convolution

Hit an LTI system with an impulse $\\delta$ and record what comes out — that's the
**impulse response** $h$. The magic: the output for *any* input is the input
**convolved** with $h$:

$$y(t) = (x * h)(t) = \\int_{-\\infty}^{\\infty} x(\\tau)\\,h(t-\\tau)\\,d\\tau,$$

and in discrete time

$$y[n] = \\sum_{k} x[k]\\,h[n-k].$$

Convolution = **flip** $h$, **slide** it across $x$, and at each position
**multiply-and-sum** the overlap.

```plot
{"title": "Convolving two pulses: overlap grows then shrinks", "xLabel": "t", "yLabel": "amplitude", "xRange": [-1, 4], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "exp(-(x-1)^2*6)", "label": "x", "color": "#2563eb"}, {"expr": "exp(-(x-2)^2*6)", "label": "h (slides)", "color": "#dc2626"}]}
```

## Both languages

```matlab
x = [1 2 3];  h = [1 1 1]/3;     % a 3-point moving average
y = conv(x, h);                  % length = len(x)+len(h)-1
```

```python
import numpy as np
x = np.array([1, 2, 3]);  h = np.ones(3)/3
y = np.convolve(x, h)            # 'full' by default
```

A moving-average filter *is* convolution with a rectangular $h$ — it smooths by
averaging neighbours. Choose $h$ and you choose what the system does.

> Convolution in time becomes **multiplication** in frequency — the single most
> useful fact in signal processing, and the reason the Fourier transform is
> everywhere.

**Next:** building signals from sinusoids — Fourier series.
""",
        ),
        _t(
            "Fourier series: building signals from sinusoids",
            "11 min",
            """\
# Fourier series: building signals from sinusoids

**Fourier's idea:** any periodic signal is a sum of sinusoids at multiples
(**harmonics**) of its fundamental frequency. A square wave, for instance, is

$$x(t) = \\frac{4}{\\pi}\\sum_{k=1,3,5,\\dots} \\frac{1}{k}\\sin(2\\pi k f_0 t).$$

Add more harmonics and the sum sharpens toward the square. Drag $N$:

```plot
{"title": "Square wave from N odd harmonics", "xLabel": "t", "yLabel": "x(t)", "xRange": [0, 2], "yRange": [-1.4, 1.4], "grid": true, "controls": [{"name": "N", "range": [1, 11], "value": 1, "label": "harmonics (odd k up to)"}], "functions": [{"expr": "(4/pi)*( sin(2*pi*x) + (N>=3)*sin(2*pi*3*x)/3 + (N>=5)*sin(2*pi*5*x)/5 + (N>=7)*sin(2*pi*7*x)/7 + (N>=9)*sin(2*pi*9*x)/9 + (N>=11)*sin(2*pi*11*x)/11 )", "label": "partial sum"}]}
```

The little overshoot at the edges that never quite goes away is the **Gibbs
phenomenon**.

## The takeaway: the spectrum

If a signal is a sum of sinusoids, the most natural way to describe it is by
**how much of each frequency** it contains — its **spectrum**. A pure 5 Hz tone
is a single spike at 5 Hz; a square wave is spikes at $f_0, 3f_0, 5f_0,\\dots$
with shrinking heights.

```matlab
% Fourier coefficients of a square wave (odd harmonics, 1/k):
k = 1:2:11;  ak = (4/pi)./k;
```

```python
import numpy as np
k  = np.arange(1, 12, 2)         # 1,3,5,...
ak = (4/np.pi)/k                 # coefficient sizes
```

**Next:** computing the spectrum of *any* signal — the Fourier transform.
""",
        ),
        _t(
            "The Fourier transform & the spectrum",
            "12 min",
            """\
# The Fourier transform & the spectrum

The **Fourier transform** turns a time signal into its frequency content:

$$X(f) = \\int_{-\\infty}^{\\infty} x(t)\\,e^{-j 2\\pi f t}\\,dt.$$

On a computer we use the **DFT**, computed fast by the **FFT** algorithm. The
**magnitude spectrum** $|X(f)|$ shows the strength of each frequency. A
two-tone signal (5 Hz + 20 Hz) shows two clean spikes:

```plot
{"title": "Magnitude spectrum of a 5 Hz + 20 Hz signal", "xLabel": "frequency (Hz)", "yLabel": "|X(f)|", "xRange": [0, 40], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "exp(-((x-5)^2)*4) + 0.5*exp(-((x-20)^2)*4)", "label": "|X(f)|"}]}
```

## FFT in both languages

```matlab
fs = 500; t = 0:1/fs:1-1/fs;
x  = sin(2*pi*5*t) + 0.5*sin(2*pi*20*t);
X  = fft(x);
f  = (0:length(x)-1)*fs/length(x);
plot(f, abs(X)/length(x)); xlim([0 40]);
```

```python
import numpy as np
fs = 500; t = np.arange(0, 1, 1/fs)
x  = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*20*t)
X  = np.fft.rfft(x)              # real FFT
f  = np.fft.rfftfreq(len(x), 1/fs)
```

Key facts: the spectrum is symmetric for real signals (use `rfft` to keep just
the positive half), bin spacing is $f_s/N$, and the highest representable
frequency is $f_s/2$ (Nyquist again).

> **Convolution theorem:** convolving in time = multiplying spectra. Filtering is
> just shaping $|X(f)|$ — which is exactly the next lesson.

**Next:** run the FFT yourself.
""",
        ),
        _code(
            "Lab: the FFT of a signal",
            "10 min",
            """\
# Compute and plot the magnitude spectrum of a two-tone signal.
import numpy as np
import matplotlib.pyplot as plt

fs = 500                              # sampling rate
t  = np.arange(0, 1, 1/fs)
x  = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*20*t)

X = np.fft.rfft(x)                    # real FFT -> positive frequencies
f = np.fft.rfftfreq(len(x), 1/fs)     # the frequency axis (Hz)
mag = np.abs(X) / len(x) * 2          # scale to amplitude

plt.figure(figsize=(8, 3))
plt.plot(f, mag, color="#dc2626")
plt.xlim(0, 40)
plt.xlabel("frequency (Hz)"); plt.ylabel("|X(f)|")
plt.title("Magnitude spectrum (peaks at 5 and 20 Hz)")
plt.grid(True)
plt.show()

peak = f[np.argmax(mag)]
print(f"strongest frequency: {peak:.1f} Hz")
print(f"bin spacing: {f[1]-f[0]:.2f} Hz,  Nyquist: {fs/2} Hz")

# Try it yourself:
#   1. Add a 60 Hz tone and raise the xlim to 80 — see the third spike.
#   2. MATLAB: X = fft(x); f = (0:N-1)*fs/N; plot(f, abs(X)/N)
""",
        ),
        _t(
            "Filtering basics",
            "10 min",
            """\
# Filtering basics

A **filter** is an LTI system that keeps some frequencies and rejects others.
Four canonical shapes:

| Filter | Keeps | Use |
|--------|-------|-----|
| Low-pass | low freqs | smoothing, anti-alias, bass |
| High-pass | high freqs | removing drift/DC, treble |
| Band-pass | a band | tuning a radio station |
| Band-stop (notch) | all but a band | killing 50/60 Hz mains hum |

```plot
{"title": "Ideal filter magnitude responses", "xLabel": "frequency", "yLabel": "|H(f)|", "xRange": [0, 10], "yRange": [-0.1, 1.2], "grid": true, "functions": [{"expr": "(x<3)*1", "label": "low-pass", "color": "#2563eb"}, {"expr": "(x>6)*1", "label": "high-pass", "color": "#dc2626"}, {"expr": "(x>3)*(x<6)*1", "label": "band-pass", "color": "#16a34a"}]}
```

## The simplest filter: a moving average

Averaging $M$ neighbours is a low-pass filter — it smooths fast wiggles (noise)
while keeping the slow trend. It's convolution with $h = \\tfrac{1}{M}[1,1,\\dots,1]$.

```matlab
M = 15;  h = ones(1, M)/M;
y = conv(noisy, h, 'same');      % smoothed
```

```python
import numpy as np
M = 15;  h = np.ones(M)/M
y = np.convolve(noisy, h, mode="same")   # smoothed
```

The longer the window $M$, the smoother the output — but the more it lags and
blurs real features. Filter design (next course) is about making that trade-off
precisely in the frequency domain.

**Next:** check your knowledge, then move on to transforms and filter design.
""",
        ),
    ),
)


# ── Signals & Systems — Advanced ──────────────────────────────────────────────

_SIGNALS_ADVANCED = SeedCourse(
    slug="signals-advanced",
    title="Signals & Systems — Advanced",
    description=(
        "Transforms and design: the Laplace transform and transfer functions, "
        "the z-transform and difference equations, frequency response and Bode "
        "plots, FIR/IIR filter design, and real-world applications — dual "
        "MATLAB/Python with a runnable filter-design lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The Laplace transform & transfer functions",
            "12 min",
            """\
# The Laplace transform & transfer functions

The **Laplace transform** generalises the Fourier transform to a complex
frequency $s = \\sigma + j\\omega$, handling growing/decaying signals and turning
calculus into algebra:

$$X(s) = \\int_0^{\\infty} x(t)\\,e^{-st}\\,dt.$$

Its superpower: differentiation becomes multiplication by $s$, so an LTI
differential equation becomes a ratio of polynomials — the **transfer
function**:

$$H(s) = \\frac{Y(s)}{X(s)} = \\frac{b_m s^m + \\dots + b_0}{a_n s^n + \\dots + a_0}.$$

## Poles and zeros

The roots of the numerator are **zeros**; of the denominator, **poles**. Their
location in the $s$-plane tells you everything about stability and response.
A continuous LTI system is **stable** iff every pole has **negative real part**
(lies in the left half-plane).

```plot
{"title": "s-plane: a stable pole pair (left half-plane)", "xLabel": "Re(s) = sigma", "yLabel": "Im(s) = omega", "xRange": [-3, 1], "yRange": [-3, 3], "grid": true, "points": [{"x": -1, "y": 2, "label": "pole", "color": "#dc2626", "size": 9}, {"x": -1, "y": -2, "label": "pole", "color": "#dc2626", "size": 9}, {"x": 0, "y": 0, "label": "zero", "color": "#2563eb", "size": 9}]}
```

```matlab
H = tf([1 0], [1 2 5]);          % H(s) = s / (s^2 + 2s + 5)
pole(H), zero(H)                 % poles at -1 +/- 2j (stable)
```

```python
import numpy as np
# poles = roots of s^2 + 2s + 5:
poles = np.roots([1, 2, 5])      # -1 +/- 2j  -> stable (Re < 0)
```

**Next:** the discrete-time counterpart — the z-transform.
""",
        ),
        _t(
            "The z-transform & difference equations",
            "11 min",
            """\
# The z-transform & difference equations

For **discrete** systems, the **z-transform** plays Laplace's role:

$$X(z) = \\sum_{n=0}^{\\infty} x[n]\\,z^{-n}.$$

A digital filter is a **difference equation** — each output sample from past
inputs and outputs:

$$y[n] = \\sum_{k} b_k\\,x[n-k] - \\sum_{k\\ge 1} a_k\\,y[n-k],$$

whose transfer function is

$$H(z) = \\frac{b_0 + b_1 z^{-1} + \\dots}{1 + a_1 z^{-1} + \\dots}.$$

## Stability flips to a circle

Where CT stability was "left half-plane", DT stability is **all poles inside
the unit circle** $|z| < 1$.

```plot
{"title": "z-plane: unit circle; poles inside = stable", "xLabel": "Re(z)", "yLabel": "Im(z)", "xRange": [-1.5, 1.5], "yRange": [-1.5, 1.5], "grid": true, "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 6.2832], "label": "unit circle", "color": "#94a3b8"}], "points": [{"x": 0.6, "y": 0.5, "label": "pole (stable)", "color": "#16a34a", "size": 9}, {"x": 0.6, "y": -0.5, "label": "pole", "color": "#16a34a", "size": 9}]}
```

```matlab
b = [1 0]; a = [1 -0.6];         % y[n] = x[n] + 0.6 y[n-1]
y = filter(b, a, x);             % run the difference equation
```

```python
# y[n] = x[n] + 0.6 y[n-1], implemented directly:
import numpy as np
y = np.zeros_like(x)
for n in range(len(x)):
    y[n] = x[n] + (0.6*y[n-1] if n > 0 else 0)
```

**Next:** how a filter treats each frequency — the frequency response.
""",
        ),
        _t(
            "Frequency response & Bode plots",
            "11 min",
            """\
# Frequency response & Bode plots

Evaluate the transfer function on the frequency axis ($s = j\\omega$, or
$z = e^{j\\omega}$ for digital) and you get the **frequency response**
$H(j\\omega)$ — a complex number per frequency. Its **magnitude** says how much
each frequency is amplified; its **phase** says how much it's delayed.

A **Bode plot** shows magnitude (in dB, $20\\log_{10}|H|$) and phase vs.
$\\log$-frequency. A first-order low-pass $H(s) = \\dfrac{1}{1 + s/\\omega_c}$ rolls
off above its **cutoff** $\\omega_c$ at $-20$ dB/decade:

```plot
{"title": "First-order low-pass magnitude (cutoff wc = 1)", "xLabel": "frequency w (rad/s)", "yLabel": "|H(jw)|", "xRange": [0, 8], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/sqrt(1 + x^2)", "label": "|H(jw)| = 1/sqrt(1+(w/wc)^2)"}]}
```

At $\\omega = \\omega_c$ the magnitude is $1/\\sqrt{2} \\approx 0.707$ — the
**-3 dB point** (half power).

```matlab
w = logspace(-1, 2, 500);
H = 1 ./ (1 + 1j*w);             % wc = 1
bode(tf(1, [1 1]));              % magnitude + phase
```

```python
import numpy as np
w = np.logspace(-1, 2, 500)
H = 1 / (1 + 1j*w)               # wc = 1
mag_db = 20*np.log10(np.abs(H))
phase  = np.angle(H, deg=True)
```

**Next:** designing filters with a chosen response.
""",
        ),
        _t(
            "FIR & IIR filter design",
            "11 min",
            """\
# FIR & IIR filter design

Two families of digital filters:

| | FIR (finite impulse response) | IIR (infinite impulse response) |
|--|------------------------------|---------------------------------|
| Feedback | none ($a_k = 0$) | yes (recursive) |
| Stability | always stable | can be unstable |
| Phase | can be exactly linear | nonlinear |
| Cost | more taps for sharp cutoff | cheap, sharp |
| Analog kin | -- | Butterworth, Chebyshev |

**FIR** = convolution with a finite $h[n]$. A practical low-pass is a
**windowed sinc**: the ideal low-pass impulse response is a sinc, truncated and
tapered by a window to tame ripple.

```plot
{"title": "Windowed-sinc FIR low-pass impulse response", "xLabel": "n", "yLabel": "h[n]", "xRange": [-10, 10], "yRange": [-0.1, 0.35], "grid": true, "functions": [{"expr": "0.3*sin(0.9*x+0.0001)/(0.9*x+0.0001)*(0.54+0.46*cos(pi*x/10))", "label": "h[n] (sinc x Hamming)"}]}
```

```matlab
h = fir1(40, 0.3);               % 40-tap FIR, cutoff 0.3 (x Nyquist)
y = filter(h, 1, x);
% IIR Butterworth:
[b, a] = butter(4, 0.3);  y = filter(b, a, x);
```

```python
import numpy as np
# A simple FIR low-pass by windowing a sinc:
n  = np.arange(-20, 21)
fc = 0.15                          # cutoff (x Nyquist)
h  = np.sinc(2*fc*n) * np.hamming(len(n))
h /= h.sum()
y  = np.convolve(x, h, mode="same")
```

Pick **FIR** when you need linear phase (audio, comms) and **IIR** when you need
a sharp cutoff cheaply (control loops, embedded). Next, build one and hear it
work.

**Next:** design and apply a filter yourself.
""",
        ),
        _code(
            "Lab: design & apply a low-pass filter",
            "12 min",
            """\
# Build a windowed-sinc FIR low-pass and clean a noisy signal.
import numpy as np
import matplotlib.pyplot as plt

fs = 500
t  = np.arange(0, 1, 1/fs)
clean = np.sin(2*np.pi*4*t)               # the signal we want (4 Hz)
noisy = clean + 0.6*np.sin(2*np.pi*80*t)  # plus 80 Hz interference

# Windowed-sinc FIR low-pass:
n  = np.arange(-30, 31)
fc = 0.05                                 # cutoff as fraction of fs (~25 Hz)
h  = np.sinc(2*fc*n) * np.hamming(len(n))
h /= h.sum()                              # unit DC gain

filtered = np.convolve(noisy, h, mode="same")

fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
ax[0].plot(t, noisy, color="#94a3b8"); ax[0].set_title("noisy (4 Hz + 80 Hz)")
ax[1].plot(t, filtered, color="#16a34a"); ax[1].set_title("after low-pass (80 Hz removed)")
ax[1].set_xlabel("t (s)")
for a in ax: a.grid(True)
plt.tight_layout(); plt.show()

err = np.sqrt(np.mean((filtered - clean)**2))
print(f"filter taps: {len(h)},  cutoff ~ {fc*fs:.0f} Hz,  RMS error vs clean: {err:.3f}")

# Try it yourself:
#   1. Lower fc to 0.02 — smoother, but watch the edges lag.
#   2. MATLAB: h = fir1(60, 0.1); y = filter(h, 1, noisy);
""",
        ),
        _t(
            "Applications & use cases",
            "9 min",
            """\
# Applications & use cases

Everything in this track powers real systems:

- **Audio** — equalizers are banks of band filters; MP3/AAC throw away
  spectrum your ear can't hear (FFT + masking); noise cancellation subtracts an
  estimated noise spectrum.
- **Biomedical** — ECG/EEG pipelines notch out 50/60 Hz mains hum and band-pass
  the physiological band; the FFT reveals heart-rate and brain-wave bands.
- **Communications** — modulation shifts a message up to a carrier frequency;
  matched filters (correlation = convolution) pull weak signals out of noise;
  OFDM (Wi-Fi, 5G, LTE) is built directly on the FFT.
- **Radar / sonar** — pulse compression and Doppler processing are convolutions
  and FFTs; the spectrum gives range and velocity.
- **Images** — 2-D convolution is blur/sharpen/edge-detect; JPEG compresses
  using the DCT, a cousin of the Fourier transform.
- **Control systems** — transfer functions, poles/zeros and Bode plots size
  and stabilise feedback loops (motors, drones, thermostats).

```mermaid
flowchart LR
  A["Acquire: sensor + ADC (sampling)"] --> B["Transform: FFT / Laplace / z"]
  B --> C["Process: filter / convolve / modulate"]
  C --> D["Act: audio out, control, decision"]
```

## The throughline

Sample a signal, look at its **spectrum**, shape it with an **LTI filter**
(convolution in time = multiplication in frequency), and reason about stability
with **poles and zeros**. Those four ideas — sampling, spectra, convolution,
poles/zeros — are the whole subject, and they recur in every domain above.

Whether you reach for MATLAB or Python, the workflow and the math are the same;
only the syntax changes.

**Next:** the final check.
""",
        ),
    ),
)


SIGNALS_COURSES: tuple[SeedCourse, ...] = (
    _SIGNALS_BASICS,
    _SIGNALS_INTERMEDIATE,
    _SIGNALS_ADVANCED,
)

__all__ = ["SIGNALS_COURSES"]
