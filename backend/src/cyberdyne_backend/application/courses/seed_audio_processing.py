"""Speech, Audio & Acoustics track: Basics -> Intermediate -> Advanced.

From pressure waves, sampling and the human ear to spectrograms, digital filters,
speech production, LPC/vocoders, perceptual coding, ASR/TTS pipelines, room
acoustics and modern deep-learning audio. Lessons are `text` with LaTeX,
interactive ```plot blocks (waveforms, windows, spectra, loudness/masking curves)
and ```mermaid block diagrams (audio chains, speech production/recognition,
codecs).
"""

# Lesson prose uses typographic characters (×, →, ≈, π, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Speech, Audio & Acoustics — Basics ───────────────────────────────────────

_AU_BASICS = SeedCourse(
    slug="audio-processing-basics",
    title="Speech, Audio & Acoustics — Basics",
    description=(
        "What sound is and how machines hear it: pressure waves, frequency and "
        "decibels; sampling, bit depth and the Nyquist limit for audio; the human "
        "ear and psychoacoustics; the time-vs-frequency view via the FFT; basic "
        "filtering and equalization; and the full microphone-to-speaker signal "
        "chain — with interactive waveform and spectrum plots."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Sound & acoustics: pressure waves, frequency, decibels",
            "11 min",
            """\
# Sound & acoustics: pressure waves, frequency, decibels

**Sound** is a tiny, fast fluctuation of air pressure travelling outward from a
vibrating source at roughly $343\\,\\text{m/s}$. A microphone (or your eardrum)
senses that pressure $p(t)$ over time.

The simplest sound is a **pure tone** — a sinusoid

$$p(t) = A\\,\\sin(2\\pi f t),$$

with **amplitude** $A$ (how loud) and **frequency** $f$ in hertz (how high). Humans
hear roughly $20\\,\\text{Hz}$ to $20\\,\\text{kHz}$. Here is a $4\\,\\text{Hz}$ tone (slowed
so you can see the wave) — change the frequency and watch the wave compress:

```plot
{"title": "A pure tone: pressure vs time", "xLabel": "time (s)", "yLabel": "pressure (rel.)", "xRange": [0, 1], "yRange": [-1.2, 1.2], "controls": [{"name": "f", "range": [1, 10], "value": 4, "step": 1, "label": "frequency f (Hz)"}], "functions": [{"expr": "sin(2*pi*f*x)", "label": "p(t) = sin(2π f t)", "color": "#2563eb"}]}
```

Loudness spans a *huge* range of pressures, so we use a logarithmic scale, the
**decibel sound-pressure level**:

$$L = 20\\,\\log_{10}\\!\\frac{p_\\text{rms}}{p_0}\\ \\text{dB SPL}, \\qquad p_0 = 20\\,\\mu\\text{Pa}.$$

A whisper is about $30\\,\\text{dB}$, conversation $\\approx 60\\,\\text{dB}$, a rock concert
$\\approx 110\\,\\text{dB}$. Every $+6\\,\\text{dB}$ **doubles** the pressure; every $+20\\,\\text{dB}$
multiplies it by ten. The dB is logarithmic because the ear is too — the next
lessons build on that.

**Next:** how we turn that continuous pressure wave into numbers.
""",
        ),
        _t(
            "Digital audio: sampling, bit depth & Nyquist",
            "12 min",
            """\
# Digital audio: sampling, bit depth & Nyquist

To store sound, we **sample** the pressure wave — measure it at a fixed rate
$f_s$ (the **sample rate**) and round each measurement to a finite number of
levels (the **bit depth**).

**Sample rate.** CD audio uses $f_s = 44\\,100\\,\\text{Hz}$, i.e. 44 100 numbers per
second per channel. The **Nyquist–Shannon theorem** says you can perfectly
capture every frequency *below* half the sample rate:

$$f_\\text{max} = \\frac{f_s}{2}\\quad\\text{(the Nyquist frequency)}.$$

So $44.1\\,\\text{kHz}$ covers the whole $20\\,\\text{kHz}$ hearing range with margin. Sample
too slowly and frequencies above Nyquist **alias** — they fold back and
masquerade as lower tones, an unfixable artefact. An **anti-aliasing** low-pass
filter before the sampler prevents it. Below, a fast tone (blue) sampled too
slowly is mistaken for the slow red alias:

```plot
{"title": "Aliasing: an under-sampled fast tone looks slow", "xLabel": "time (s)", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [-1.2, 1.2], "functions": [{"expr": "sin(2*pi*9*x)", "label": "true 9 Hz tone", "color": "#2563eb"}, {"expr": "sin(2*pi*1*x)", "label": "1 Hz alias seen by sampler", "color": "#dc2626"}]}
```

**Bit depth.** 16-bit audio has $2^{16}=65\\,536$ levels; the rounding error
(**quantization noise**) sets the dynamic range at about $6\\,\\text{dB}$ per bit, so
16-bit gives $\\approx 96\\,\\text{dB}$ — quiet noise floor under loud peaks. 24-bit studio
audio buys extra headroom.

**Next:** the listener those numbers are ultimately for.
""",
        ),
        _t(
            "The human ear & psychoacoustics",
            "11 min",
            """\
# The human ear & psychoacoustics

Audio is meant for a human, and the ear is **not** a flat, linear instrument —
exploiting its quirks is the heart of audio engineering.

**Anatomy in one line.** The outer ear funnels pressure to the eardrum; the
middle-ear bones amplify it; the spiral **cochlea** acts as a bank of tuned
filters, mapping frequency to position (high frequencies at the base, low at the
apex) and firing nerves — a biological spectrum analyser.

**Loudness is frequency-dependent.** Equal physical level does *not* mean equal
perceived loudness. The **equal-loudness contours** show the ear is most
sensitive around $2\\!-\\!5\\,\\text{kHz}$ (speech!) and needs much more energy at the low
and high extremes. This stylised "how many dB to sound equally loud" curve dips
in the middle and rises at the edges:

```plot
{"title": "Equal-loudness: dB needed to sound equally loud (stylised)", "xLabel": "log-frequency (arb.)", "yLabel": "level needed (dB)", "xRange": [0, 10], "yRange": [0, 80], "functions": [{"expr": "20 + 0.9*(x-4)^2", "label": "threshold of hearing", "color": "#2563eb"}], "points": [{"x": 4, "y": 20, "label": "most sensitive ~3 kHz", "color": "#dc2626", "size": 7}]}
```

**Pitch and loudness perception are logarithmic.** Doubling frequency raises
pitch by one **octave** regardless of the starting note; loudness tracks dB, not
raw pressure. **Masking** — a loud tone hides a nearby quiet one — is the basis
of MP3 (covered in Advanced). Perception, not physics, decides what matters.

**Next:** the frequency view that makes all of this measurable.
""",
        ),
        _t(
            "Time vs frequency: the FFT & the spectrum",
            "11 min",
            """\
# Time vs frequency: the FFT & the spectrum

A waveform $p(t)$ tells you the pressure at each instant. But the *useful*
information — which notes, which formants, which hiss — lives in its
**frequencies**. The **Fourier transform** rewrites a signal as a sum of
sinusoids; its magnitude is the **spectrum**, energy versus frequency.

Real audio is sampled, so we use the **Discrete Fourier Transform (DFT)**,
computed quickly by the **Fast Fourier Transform (FFT)** in $O(N\\log N)$ instead
of $O(N^2)$ — the single most-used algorithm in audio.

A signal that looks like noise in time can be three clean spikes in frequency.
Below is the magnitude spectrum of a sound built from three tones; the peaks are
its three component frequencies:

```plot
{"title": "Magnitude spectrum: three tones show as three peaks", "xLabel": "frequency (Hz)", "yLabel": "magnitude", "xRange": [0, 10], "yRange": [0, 1.2], "functions": [{"expr": "exp(-8*(x-2)^2) + 0.7*exp(-8*(x-5)^2) + 0.4*exp(-8*(x-8)^2)", "label": "|spectrum|", "color": "#2563eb"}], "points": [{"x": 2, "y": 1, "label": "fundamental", "color": "#dc2626", "size": 6}, {"x": 5, "y": 0.7, "color": "#16a34a", "size": 5}, {"x": 8, "y": 0.4, "color": "#16a34a", "size": 5}]}
```

The full signal-processing identity: **time domain and frequency domain are two
views of the same signal**, linked by the FFT and its inverse. Filtering, EQ,
compression and coding all become simple in whichever domain suits them.

**Next:** shaping that spectrum with filters.
""",
        ),
        _t(
            "Basic audio filtering & equalization",
            "10 min",
            """\
# Basic audio filtering & equalization

A **filter** boosts or cuts chosen frequency bands; its **frequency response**
$|H(f)|$ is the gain at each frequency. The four staples:

- **Low-pass** — keep lows, remove highs (anti-aliasing, removing hiss).
- **High-pass** — remove rumble and DC.
- **Band-pass** — keep a band (telephone speech ≈ $300\\!-\\!3400\\,\\text{Hz}$).
- **Band-stop / notch** — kill one frequency (e.g. $50/60\\,\\text{Hz}$ mains hum).

A simple first-order low-pass has $|H(f)| = 1/\\sqrt{1+(f/f_c)^2}$, flat in the
**passband** and rolling off past the **cutoff** $f_c$. The cutoff is the
$-3\\,\\text{dB}$ point (half power). Drag $f_c$:

```plot
{"title": "First-order low-pass response |H(f)|", "xLabel": "frequency (rel.)", "yLabel": "gain |H(f)|", "xRange": [0, 10], "yRange": [0, 1.2], "controls": [{"name": "fc", "range": [0.5, 6], "value": 2, "label": "cutoff f_c"}], "functions": [{"expr": "1/sqrt(1+(x/fc)^2)", "label": "|H(f)|", "color": "#2563eb"}], "points": [{"xExpr": "fc", "yExpr": "1/sqrt(2)", "label": "−3 dB cutoff", "color": "#dc2626", "size": 7}]}
```

**Equalization (EQ)** is just a set of these filters in parallel: a graphic EQ
boosts/cuts fixed bands; a parametric EQ lets you pick centre frequency, gain and
**Q** (bandwidth). EQ is how you brighten a dull recording, remove hum, or carve
space for a voice in a mix.

**Next:** where filters sit in the whole audio path.
""",
        ),
        _t(
            "The audio signal chain: mic to speaker",
            "10 min",
            """\
# The audio signal chain: mic to speaker

Every audio system — phone call, hearing aid, streaming app — is the same chain
turning sound into numbers, processing, and back to sound:

```mermaid
flowchart LR
  SRC["Sound source"] --> MIC["Microphone (acoustic → voltage)"]
  MIC --> PRE["Pre-amp + anti-alias low-pass"]
  PRE --> ADC["ADC (sample + quantize)"]
  ADC --> DSP["DSP (filter, EQ, compress, code)"]
  DSP --> DAC["DAC (numbers → voltage)"]
  DAC --> AMP["Power amp + reconstruction filter"]
  AMP --> SPK["Speaker (voltage → acoustic)"]
```

Stage by stage:

- **Microphone** — a transducer turning pressure into a small voltage.
- **Pre-amp + anti-alias filter** — boost the signal and remove anything above
  Nyquist *before* sampling (Lesson 2).
- **ADC** — the **analog-to-digital converter** samples and quantizes.
- **DSP** — everything digital: filtering, EQ, dynamics, effects, compression.
- **DAC** — the **digital-to-analog converter** turns numbers back into voltage,
  followed by a **reconstruction** low-pass that smooths the staircase.
- **Power amp + speaker** — drive a cone that pushes air, recreating sound.

The unifying idea: a **transducer** at each end, an ADC/DAC pair as the
digital boundary, and DSP doing the interesting work in between. Latency,
noise and distortion at any stage degrade the result — engineering is keeping
the chain clean end to end.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Speech, Audio & Acoustics — Intermediate ─────────────────────────────────

_AU_INTERMEDIATE = SeedCourse(
    slug="audio-processing-intermediate",
    title="Speech, Audio & Acoustics — Intermediate",
    description=(
        "Working with real audio: the short-time Fourier transform and "
        "spectrograms; windowing and spectral leakage; designing FIR/IIR digital "
        "filters and EQ; reverb, delay and dynamic-range compression; the "
        "source-filter model of speech and formants; and pitch / fundamental-"
        "frequency estimation — with interactive window and spectrum plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The short-time Fourier transform & spectrograms",
            "12 min",
            """\
# The short-time Fourier transform & spectrograms

A single FFT of a whole song tells you *which* frequencies are present but not
*when*. Speech and music change constantly, so we chop the signal into short,
overlapping **frames** (e.g. $20\\!-\\!40\\,\\text{ms}$), window each one, and FFT it. That
is the **short-time Fourier transform (STFT)**:

$$X(m, f) = \\sum_n x[n]\\,w[n - mH]\\,e^{-j 2\\pi f n},$$

where $w$ is the window and $H$ the **hop** between frames. Stack the magnitude
spectra into an image — time across, frequency up, energy as colour — and you
have a **spectrogram**, the central display of all speech and audio analysis.

**The fundamental trade-off.** A *long* window gives fine **frequency**
resolution but smears **time**; a *short* window does the reverse. You cannot win
both — this is the time–frequency uncertainty principle. Below, a short window
(wide in frequency) vs a long one (narrow), same energy:

```plot
{"title": "Window length trades time vs frequency resolution", "xLabel": "frequency (rel.)", "yLabel": "spectral magnitude", "xRange": [-5, 5], "yRange": [0, 1.2], "functions": [{"expr": "exp(-0.5*x^2)", "label": "short window → wide (poor freq. res.)", "color": "#2563eb"}, {"expr": "exp(-4*x^2)", "label": "long window → narrow (poor time res.)", "color": "#dc2626"}]}
```

Choosing frame length, hop and window is the first decision in any
spectrogram-based pipeline (speech recognition, music analysis, denoising).

**Next:** why windows matter and what happens without them.
""",
        ),
        _t(
            "Windowing & spectral leakage",
            "11 min",
            """\
# Windowing & spectral leakage

Each STFT frame is a finite chunk cut from a longer signal. Cutting abruptly with
a **rectangular window** is like multiplying by a box — and a sharp edge in time
splatters energy across frequency, called **spectral leakage**. A single pure
tone smears into a peak with tall **side-lobes** that can hide nearby quiet tones.

The fix is to **taper** the frame to zero at both ends with a smooth window. The
**Hann window**

$$w[n] = 0.5 - 0.5\\cos\\!\\left(\\frac{2\\pi n}{N-1}\\right)$$

is the workhorse; **Hamming**, **Blackman** and others trade main-lobe width
against side-lobe height. A wider main lobe (worse resolution) buys far lower
side-lobes (less leakage). Here is the Hann taper one frame is multiplied by:

```plot
{"title": "The Hann window tapers a frame smoothly to zero", "xLabel": "sample n within frame (0..1)", "yLabel": "weight w[n]", "xRange": [0, 1], "yRange": [0, 1.2], "functions": [{"expr": "0.5 - 0.5*cos(2*pi*x)", "label": "Hann window", "color": "#2563eb"}, {"expr": "1", "label": "rectangular (no taper)", "color": "#dc2626"}]}
```

Rule of thumb: **always window** before an FFT of real audio. Use Hann/Hamming for
general spectra; pick a low-side-lobe window when a weak tone hides next to a loud
one.

**Next:** filters that run on the samples themselves.
""",
        ),
        _t(
            "Digital filters for audio: FIR, IIR, EQ & shelving",
            "12 min",
            """\
# Digital filters for audio: FIR, IIR, EQ & shelving

A digital filter computes each output sample from recent inputs (and outputs).
Two families:

- **FIR (finite impulse response)** — output is a weighted sum of past *inputs*:
  $y[n] = \\sum_{k=0}^{M} b_k\\,x[n-k]$. Always stable; can have exactly **linear
  phase** (no frequency-dependent delay) — prized for audio. Cost: many taps for a
  sharp response.
- **IIR (infinite impulse response)** — also feeds back past *outputs*:
  $y[n] = \\sum b_k x[n-k] - \\sum a_k y[n-k]$. Very efficient (a sharp cut in a few
  taps) but can be unstable and has nonlinear phase. Digital versions of classic
  Butterworth / Chebyshev analog filters.

**Shelving and peaking filters** are the EQ building blocks. A **low-shelf**
boosts/cuts everything below a corner; a **high-shelf** does the highs; a
**peaking (bell)** filter boosts a band around a centre. Here a low-shelf adds
bass below the corner while leaving the highs flat — drag the gain:

```plot
{"title": "Low-shelf EQ: boost the lows, leave highs flat", "xLabel": "frequency (rel.)", "yLabel": "gain", "xRange": [0, 10], "yRange": [0, 3], "controls": [{"name": "g", "range": [0.5, 2.5], "value": 2, "label": "low-shelf gain"}], "functions": [{"expr": "1 + (g-1)/(1+(x/2)^2)", "label": "|H(f)| low-shelf", "color": "#2563eb"}, {"expr": "1", "label": "flat (0 dB)", "color": "#94a3b8"}]}
```

Choose FIR when phase linearity matters (mastering, crossovers), IIR when CPU is
tight (real-time EQ on every channel). A bank of shelving + peaking IIR filters is
exactly a studio parametric equalizer.

**Next:** effects that work in time — reverb, delay and dynamics.
""",
        ),
        _t(
            "Reverb, delay & dynamic-range compression",
            "11 min",
            """\
# Reverb, delay & dynamic-range compression

Beyond shaping frequency, audio effects shape **time** and **level**.

**Delay** simply replays the signal later: $y[n] = x[n] + g\\,x[n - D]$. A single
short delay is an **echo**; feeding the delayed output back gives repeating
echoes that fade by the feedback gain $g$.

**Reverb** is the dense smear of thousands of reflections in a real room — the
sound of *space*. Digital reverbs build it from networks of delays and all-pass
filters, controlled by **decay time (RT60)**, the time for the tail to drop
$60\\,\\text{dB}$. It is what makes a dry vocal sound like it is in a hall.

**Dynamic-range compression** tames level instead of frequency. Above a
**threshold** $T$, gain is reduced by a **ratio** $R$, so loud parts are pulled
down and the whole signal can be turned up — more consistent, "louder" audio.
The static curve maps input level to output level: $1\\!:\\!1$ below $T$, then a
gentler slope $1/R$ above. Drag the ratio:

```plot
{"title": "Compressor static curve (threshold T = 5)", "xLabel": "input level (dB)", "yLabel": "output level (dB)", "xRange": [0, 10], "yRange": [0, 10], "controls": [{"name": "R", "range": [1, 8], "value": 4, "label": "ratio R (x:1)"}], "functions": [{"expr": "x", "label": "below threshold (1:1)", "color": "#94a3b8"}, {"expr": "5 + (x-5)/R", "label": "above threshold (1/R)", "color": "#2563eb"}], "points": [{"x": 5, "y": 5, "label": "threshold", "color": "#dc2626", "size": 7}]}
```

**Attack** and **release** set how fast it reacts. Related cousins: the
**limiter** ($R \\to \\infty$, brick-wall peak control), the **expander** and the
**noise gate** (which cut *below* a threshold). These are everywhere — broadcast,
mastering, voice processing.

**Next:** how the human voice itself is produced.
""",
        ),
        _t(
            "Speech production: the source-filter model & formants",
            "12 min",
            """\
# Speech production: the source-filter model & formants

Speech analysis rests on one beautifully simple idea, the **source-filter
model**:

```mermaid
flowchart LR
  LUNGS["Lungs (air supply)"] --> SRC["Source: vocal-fold buzz (voiced)\\nor turbulent noise (unvoiced)"]
  SRC --> FILT["Filter: vocal tract\\n(throat, mouth, lips, nose)"]
  FILT --> OUT["Radiated speech"]
  ART["Tongue / jaw / lips position"] -. shapes .-> FILT
```

- The **source** is excitation. For **voiced** sounds (vowels, "m", "z") the vocal
  folds vibrate, producing a buzz at the **fundamental frequency** $f_0$ (perceived
  pitch) rich in harmonics. For **unvoiced** sounds ("s", "f") it is turbulent
  noise.
- The **filter** is the **vocal tract** — throat, mouth, nasal cavity — an acoustic
  tube whose resonances shape that source. Move tongue, jaw and lips and you change
  the resonances.

Those resonances are the **formants** $F_1, F_2, F_3, \\dots$ — peaks in the speech
spectrum that *define which vowel you hear*. "ee", "ah" and "oo" differ almost
entirely by where $F_1$ and $F_2$ sit. Below is a stylised vowel spectrum with
three formant peaks — drag the second formant to morph the vowel:

```plot
{"title": "Vowel spectrum: formants F1, F2, F3 define the vowel", "xLabel": "frequency (rel.)", "yLabel": "spectral magnitude", "xRange": [0, 10], "yRange": [0, 1.2], "controls": [{"name": "f2", "range": [3, 6], "value": 4, "label": "second formant F2"}], "functions": [{"expr": "exp(-6*(x-1)^2) + 0.8*exp(-6*(x-f2)^2) + 0.5*exp(-6*(x-7.5)^2)", "label": "vocal-tract response", "color": "#2563eb"}], "points": [{"x": 1, "y": 1, "label": "F1", "color": "#dc2626", "size": 6}, {"xExpr": "f2", "y": 0.8, "label": "F2", "color": "#16a34a", "size": 6}]}
```

This model is why we can separate **what** is said (the filter / formants) from
**who/how** (the source / pitch) — the foundation of LPC, vocoders, recognition
and synthesis in the Advanced track.

**Next:** measuring that source pitch.
""",
        ),
        _t(
            "Pitch & fundamental-frequency estimation",
            "11 min",
            """\
# Pitch & fundamental-frequency estimation

The **fundamental frequency** $f_0$ — the vocal-fold vibration rate, or a note's
base frequency — drives perceived **pitch**, intonation and melody. Estimating it
from a noisy, harmonic-rich signal is a classic, surprisingly hard problem.

A voiced sound is **quasi-periodic**: it nearly repeats every $T_0 = 1/f_0$
seconds. The main families of estimators:

- **Autocorrelation** — slide the signal against a delayed copy; the lag of the
  first strong peak (after lag 0) is the period $T_0$. Below, the autocorrelation
  of a periodic sound peaks again at the period — drag the candidate period:

```plot
{"title": "Autocorrelation peaks at the pitch period T0", "xLabel": "lag (samples)", "yLabel": "correlation", "xRange": [0, 10], "yRange": [-1.2, 1.2], "controls": [{"name": "T0", "range": [2, 6], "value": 4, "label": "candidate period T0"}], "functions": [{"expr": "cos(2*pi*x/4)*exp(-0.12*x)", "label": "autocorrelation r(lag)", "color": "#2563eb"}], "points": [{"xExpr": "T0", "yExpr": "cos(2*pi*T0/4)*exp(-0.12*T0)", "label": "candidate period", "color": "#dc2626", "size": 7}]}
```

- **Cepstrum** — take the FFT of the *log* spectrum; evenly spaced harmonics
  collapse to a single peak whose position is $T_0$.
- **YIN / pYIN** — a refined difference-function method, the modern default for
  monophonic pitch.

Pitfalls: **octave errors** (picking $2f_0$ or $f_0/2$), confusion in noise, and
unvoiced frames that have *no* pitch at all. Robust trackers add voicing
detection and temporal smoothing. $f_0$ feeds prosody analysis, auto-tune,
music transcription and the vocoders ahead.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Speech, Audio & Acoustics — Advanced ─────────────────────────────────────

_AU_ADVANCED = SeedCourse(
    slug="audio-processing-advanced",
    title="Speech, Audio & Acoustics — Advanced",
    description=(
        "The modern speech & audio stack: linear predictive coding and vocoders; "
        "perceptual audio coding and masking (MP3/AAC); the speech-recognition "
        "pipeline from MFCC features to models; text-to-speech synthesis; room "
        "acoustics, beamforming and noise/echo cancellation; and an introduction "
        "to deep-learning audio — with masking curves and codec/ASR block diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Linear predictive coding (LPC) & vocoders",
            "13 min",
            """\
# Linear predictive coding (LPC) & vocoders

**Linear predictive coding** is the source-filter model turned into math. It
predicts each speech sample from a weighted sum of the previous $p$ samples:

$$\\hat x[n] = \\sum_{k=1}^{p} a_k\\,x[n-k],$$

and chooses the coefficients $a_k$ to minimise the prediction error. Those
coefficients describe an all-pole filter $1/A(z)$ — a compact model of the
**vocal tract** whose resonances are exactly the **formants**. The leftover
prediction error (the **residual**) is the **source** excitation.

That split is hugely efficient: instead of sending the waveform, send a few LPC
coefficients per frame plus a description of the excitation. A **vocoder**
(voice-coder) does exactly this — at the decoder, drive the LPC filter with a
pitch-pulse train (voiced) or noise (unvoiced) and regenerate speech. The LPC
spectrum traces the **envelope** over the detailed harmonic spectrum:

```plot
{"title": "LPC models the spectral envelope (formant peaks)", "xLabel": "frequency (rel.)", "yLabel": "magnitude (dB, rel.)", "xRange": [0, 10], "yRange": [0, 1.2], "functions": [{"expr": "exp(-5*(x-1.5)^2)+0.75*exp(-5*(x-4.5)^2)+0.5*exp(-5*(x-7.5)^2)", "label": "LPC envelope (vocal tract)", "color": "#2563eb"}, {"expr": "(exp(-5*(x-1.5)^2)+0.75*exp(-5*(x-4.5)^2)+0.5*exp(-5*(x-7.5)^2))*(0.6+0.4*cos(2*pi*x))", "label": "detailed harmonic spectrum", "color": "#94a3b8"}]}
```

LPC powered early cellular speech codecs (GSM, the famous Speak & Spell) and its
descendants — **CELP** and the **LSP/LSF** coefficient representations — still
underlie modern low-bitrate speech coding. It is also the bridge to neural
vocoders (last lesson).

**Next:** coding for music, where the *ear* sets the budget.
""",
        ),
        _t(
            "Perceptual audio coding & masking (MP3/AAC)",
            "13 min",
            """\
# Perceptual audio coding & masking (MP3/AAC)

Music codecs like **MP3** and **AAC** shrink audio 10× with no audible loss by a
single trick: **don't code what you can't hear.** They exploit psychoacoustic
**masking** — a loud tone raises the hearing threshold around it, hiding quieter
sounds nearby in frequency (and just after in time).

Below, the **masking curve** (dashed) sits above the quiet-threshold; sounds under
it are inaudible and can be discarded or coarsely quantized. Drag the masker:

```plot
{"title": "Masking: a loud tone hides quieter neighbours", "xLabel": "frequency (rel.)", "yLabel": "level (dB)", "xRange": [0, 10], "yRange": [0, 80], "controls": [{"name": "fm", "range": [3, 7], "value": 5, "label": "masker frequency"}], "functions": [{"expr": "10 + 0.6*(x-3)^2", "label": "quiet threshold", "color": "#94a3b8"}, {"expr": "60 - 14*(x-fm)^2", "label": "masking threshold", "color": "#dc2626"}], "points": [{"xExpr": "fm", "y": 60, "label": "masker", "color": "#2563eb", "size": 7}]}
```

The encoder block diagram:

```mermaid
flowchart LR
  IN["PCM audio"] --> FB["Filter bank (MDCT, sub-bands)"]
  IN --> PSY["Psychoacoustic model (masking thresholds)"]
  PSY -->|bits per band| QUANT["Quantize + allocate bits"]
  FB --> QUANT
  QUANT --> HUFF["Entropy / Huffman coding"]
  HUFF --> BIT["Bitstream (MP3 / AAC)"]
```

Quantization noise is shaped to stay *below* the masking threshold in every band,
so the discarded information is — by design — inaudible. AAC improves on MP3 with
a better filter bank and tools; **Opus** unifies speech and music coding for the
web. The decoder just reverses the chain. The lesson: perceptual coding spends
bits where the **ear** can tell, not where the **signal** has energy.

**Next:** turning audio into words.
""",
        ),
        _t(
            "The speech-recognition pipeline: MFCC features to models",
            "13 min",
            """\
# The speech-recognition pipeline: MFCC features to models

**Automatic speech recognition (ASR)** maps a waveform to text. Classic and
modern systems share a front end and differ in the back end:

```mermaid
flowchart LR
  WAV["Speech waveform"] --> FRAME["Frame + window (25 ms / 10 ms hop)"]
  FRAME --> SPEC["FFT → power spectrum"]
  SPEC --> MEL["Mel filter bank (perceptual freq.)"]
  MEL --> LOG["log → DCT → MFCCs"]
  LOG --> AM["Acoustic model (HMM-GMM / DNN / end-to-end)"]
  AM --> LM["Language model + decoder"]
  LM --> TXT["Recognised text"]
```

**Front end — MFCC features.** The classic feature set, **Mel-frequency cepstral
coefficients**:

1. Frame and window the signal (the STFT from the Intermediate track).
2. Take the power spectrum, then sum it into **mel** bands — spaced like the ear,
   fine at low frequency, coarse at high (the **mel scale** $m = 2595\\log_{10}(1+f/700)$).
3. Take the **log** (loudness is logarithmic), then a **DCT** to decorrelate —
   the first ~13 coefficients are the MFCCs, a compact, robust description of the
   spectral envelope.

**Back end — the model.** Classic ASR used **HMM-GMM**: hidden Markov models for
the time sequence of phonemes, Gaussian mixtures for the acoustics, plus a
**language model** ($n$-gram) scoring word sequences. Modern systems replace the
acoustics with deep nets and increasingly use **end-to-end** models (CTC,
attention/transformer encoder-decoders) that map audio directly to text, learning
their own features. The front end persists; the back end is where the deep-learning
revolution landed.

**Next:** going the other way — text to speech.
""",
        ),
        _t(
            "Speech synthesis (TTS) overview",
            "11 min",
            """\
# Speech synthesis (TTS) overview

**Text-to-speech** is recognition in reverse: text in, natural speech out. It
splits into a **front end** (linguistic analysis) and a **back end** (waveform
generation).

**Front end.** Normalise text ("Dr." → "doctor", "2026" → "twenty twenty-six"),
convert letters to phonemes (**grapheme-to-phoneme**), and predict **prosody** —
the pitch ($f_0$) contour, durations and stress that make speech sound human
rather than robotic.

**Back end — three eras:**

- **Concatenative** — stitch together tiny recorded units from a large database.
  High quality on in-domain text, but brittle at the joins.
- **Statistical parametric (HMM/DSP)** — predict vocoder parameters (LPC-style
  spectral envelope + $f_0$) frame by frame and synthesise. Smooth and tiny, but
  buzzy.
- **Neural** — the modern stack. A sequence model (e.g. **Tacotron**,
  **FastSpeech**) predicts a **mel-spectrogram** from text, and a **neural
  vocoder** (**WaveNet**, **WaveRNN**, **HiFi-GAN**) turns that spectrogram into a
  waveform. Near-human quality, controllable speaker and style.

The common thread is the same source-filter / spectral-envelope picture from the
Intermediate track: TTS predicts a time-varying spectrum (often a mel-spectrogram)
and then reconstructs the waveform. Naturalness now hinges on prosody and the
vocoder — the spectral content is largely solved.

**Next:** sound in real, noisy, echoey spaces.
""",
        ),
        _t(
            "Room acoustics, beamforming & noise/echo cancellation",
            "12 min",
            """\
# Room acoustics, beamforming & noise/echo cancellation

Real microphones live in **rooms**, with reflections, noise and other talkers.
Three problems and their fixes:

**Room acoustics.** A room adds reflections described by its **impulse response**;
the sound reaching the mic is the speech **convolved** with that response (the
**reverberation** of the Intermediate track). Long **RT60** smears speech and hurts
recognition; **dereverberation** tries to invert it.

**Beamforming.** With a **microphone array** you can listen *directionally*. Sound
from the target arrives at each mic at slightly different times; delay each
channel to realign that direction and sum — signals from the target add up while
off-axis noise partly cancels. The array's **directivity pattern** has a main lobe
steered at the talker; steer it:

```plot
{"title": "Beamformer directivity: a steerable main lobe", "xLabel": "angle (rel.)", "yLabel": "array gain", "xRange": [-5, 5], "yRange": [0, 1.2], "controls": [{"name": "th", "range": [-3, 3], "value": 0, "label": "steering angle"}], "functions": [{"expr": "exp(-2*(x-th)^2)", "label": "beam (gain vs angle)", "color": "#2563eb"}], "points": [{"xExpr": "th", "y": 1, "label": "steered toward talker", "color": "#dc2626", "size": 7}]}
```

**Echo & noise cancellation.** In a speakerphone, the mic re-captures the far-end
voice from the loudspeaker — an **echo**. **Acoustic echo cancellation (AEC)** uses
an **adaptive filter** (LMS/NLMS) that models the echo path and subtracts a
predicted echo, since the reference (what was played) is known. **Adaptive noise
cancellation** likewise subtracts an estimate of correlated noise. These run in
every hands-free call, smart speaker and conferencing system.

**Next:** how deep learning is rewriting all of this.
""",
        ),
        _t(
            "Modern deep-learning audio & applications",
            "12 min",
            """\
# Modern deep-learning audio & applications

Deep learning now dominates audio, often by *learning* the front end and model
end to end instead of hand-designing features.

**Representations.** Many models still take a **mel-spectrogram** as input (the
STFT lives on), but **self-supervised** models — **wav2vec 2.0**, **HuBERT**,
**Whisper** — learn powerful representations directly from raw audio with little or
no labelling, then fine-tune for recognition, language ID or keyword spotting.

**Generation.** **Neural vocoders** (WaveNet, HiFi-GAN) and full generative models
produce strikingly natural speech and music; **diffusion** and transformer audio
models generate sound effects, music and singing from text prompts. Voice
**conversion** and cloning recombine the source-filter split with neural nets.

**Tasks that surged with deep learning:**

- **Source separation** — split a mix into stems (vocals, drums) or isolate one
  speaker from a crowd (the "cocktail-party" problem), e.g. Conv-TasNet, Demucs.
- **Speech enhancement / denoising** — far beyond classic spectral subtraction.
- **Sound event detection / audio tagging** — "what is making this sound?"
- **End-to-end ASR & TTS** — the pipelines of the last lessons, now single models.

The throughline of this whole track: **time–frequency analysis, the source-filter
model, and perceptual weighting** remain the conceptual backbone — deep learning
supplies the flexible function that maps between waveform, spectrogram and meaning.
Master the fundamentals and the neural systems become far less mysterious.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


AUDIO_PROCESSING_COURSES: tuple[SeedCourse, ...] = (
    _AU_BASICS,
    _AU_INTERMEDIATE,
    _AU_ADVANCED,
)

__all__ = ["AUDIO_PROCESSING_COURSES"]
