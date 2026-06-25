"""Radar & Remote Sensing track: Basics -> Intermediate -> Advanced.

From the radar block diagram and the range equation through Doppler, FMCW and
pulse compression, to MTI/pulse-Doppler processing, SAR imaging, phased arrays
and tracking. Lessons are `text` with LaTeX, interactive ```plot blocks and
```mermaid system diagrams. Builds on the Signals & Systems and RF/Comms tracks.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, λ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Radar & Remote Sensing — Basics ──────────────────────────────────────────

_RD_BASICS = SeedCourse(
    slug="radar-basics",
    title="Radar & Remote Sensing — Basics",
    description=(
        "How radar sees: the transmit-receive block diagram, the radar range "
        "equation and why detection range grows so slowly with power, pulse "
        "ranging and PRF/ambiguity, radar cross-section, antenna beamwidth and "
        "angular resolution, and the decibel/SNR view. Interactive plots and "
        "block diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What radar is & the radar block diagram",
            "10 min",
            """\
# What radar is & the radar block diagram

**Radar** (RAdio Detection And Ranging) transmits a radio wave, listens for the
echo bounced off a target, and uses the echo to find the target's **range**,
**angle** and **velocity**. The same physics — send a wave, time the echo —
powers weather radar, air-traffic control, automotive sensors and spaceborne
imaging.

A monostatic radar (transmitter and receiver share one antenna) is built from a
small set of blocks:

```mermaid
flowchart LR
    WG[Waveform generator] --> TX[Transmitter / power amp]
    TX --> DUP[Duplexer / circulator]
    DUP --> ANT[Antenna]
    ANT -. echo .-> DUP
    DUP --> LNA[Low-noise amplifier]
    LNA --> MIX[Mixer / downconverter]
    MIX --> ADC[ADC]
    ADC --> SP[Signal processor]
    SP --> DISP[Detection / display]
    LO[Local oscillator] --> MIX
    LO --> WG
```

The **duplexer** switches the antenna between transmit and receive so one
antenna does both jobs. The **local oscillator** provides a coherent phase
reference shared by transmit and receive — the key to measuring Doppler later.

Three measurements fall out of one echo:

- **Range** $R$ from the round-trip time delay $\\tau$: $R = c\\tau/2$.
- **Angle** from where the antenna beam is pointing when the echo returns.
- **Velocity** from the Doppler shift of the echo (Intermediate course).

**Next:** how strong that returning echo actually is — the range equation.
""",
        ),
        _t(
            "The radar range equation",
            "12 min",
            """\
# The radar range equation

How much power comes back? Transmit power $P_t$ spreads over a sphere, is focused
by antenna gain $G$, illuminates a target of cross-section $\\sigma$, and the
re-radiated power spreads back over another sphere to the antenna of effective
area $A_e$. Chaining those factors gives the **radar range equation**:

$$P_r = \\frac{P_t\\,G^2\\,\\lambda^2\\,\\sigma}{(4\\pi)^3\\,R^4}.$$

The headline is the $R^4$ in the denominator: the echo travels the spreading
loss **twice** (out and back), so received power falls as the *fourth power* of
range. Below, watch how brutally the echo collapses with distance:

```plot
{"title": "Received power falls as 1/R⁴", "xLabel": "range R (relative)", "yLabel": "received power (relative)", "xRange": [1, 6], "yRange": [0, 1.1], "functions": [{"expr": "1/x^4", "label": "Pr ∝ 1/R⁴", "color": "#2563eb"}], "points": [{"x": 1, "y": 1, "label": "reference range", "color": "#16a34a", "size": 7}, {"x": 2, "y": 0.0625, "label": "2× range → 1/16 power", "color": "#dc2626", "size": 7}]}
```

A practical consequence: doubling the **detection range** demands $2^4 = 16$
times more transmit power (everything else fixed). That is why radar designers
chase gain (bigger antennas), low-noise receivers and clever signal processing
rather than just brute-force power.

Rearranging for the maximum range gives

$$R_{\\max} = \\left[\\frac{P_t\\,G^2\\,\\lambda^2\\,\\sigma}{(4\\pi)^3\\,P_{r,\\min}}\\right]^{1/4},$$

where $P_{r,\\min}$ is the smallest echo the receiver can detect — set by noise,
which we quantify in the SNR lesson.

**Next:** turning the echo's timing into a range measurement.
""",
        ),
        _t(
            "Pulse radar & range measurement",
            "11 min",
            """\
# Pulse radar & range measurement

A **pulsed radar** transmits a short burst of duration $\\tau$, then listens. The
echo's round-trip delay $t$ gives the range directly:

$$R = \\frac{c\\,t}{2}.$$

Pulses repeat at the **pulse repetition frequency** (PRF), so the interval
between pulses is the **PRI** $T = 1/\\text{PRF}$. That interval sets two limits:

- **Maximum unambiguous range.** A radar can't tell whether an echo belongs to
  the pulse just sent or a previous one. If a target is farther than light can
  travel out-and-back within one PRI, its echo arrives *after* the next pulse and
  appears at a false short range — a **range ambiguity**. The unambiguous range is
  $$R_{\\text{ua}} = \\frac{c\\,T}{2} = \\frac{c}{2\\,\\text{PRF}}.$$
- **Range resolution.** Two targets are separable only if their echoes don't
  overlap, which needs them $\\Delta R = c\\tau/2$ apart. Shorter pulses → finer
  resolution (but less energy — the tension pulse compression later resolves).

There's a direct trade: a **low PRF** gives long unambiguous range but coarse
velocity measurement; a **high PRF** gives clean velocity but short unambiguous
range. Watch unambiguous range shrink as PRF rises:

```plot
{"title": "Unambiguous range vs PRF (Rua = c / 2·PRF)", "xLabel": "PRF (kHz)", "yLabel": "unambiguous range (km)", "xRange": [0.5, 10], "yRange": [0, 320], "functions": [{"expr": "150/x", "label": "Rua = 150 / PRF[kHz]", "color": "#2563eb"}], "points": [{"x": 1, "y": 150, "label": "1 kHz → 150 km", "color": "#16a34a", "size": 7}, {"x": 5, "y": 30, "label": "5 kHz → 30 km", "color": "#dc2626", "size": 7}]}
```

**Next:** what makes a target a strong or weak echo — its cross-section.
""",
        ),
        _t(
            "Radar cross-section (RCS)",
            "10 min",
            """\
# Radar cross-section (RCS)

The **radar cross-section** $\\sigma$ (units: square metres) measures how much
power a target scatters *back toward the radar* — not its physical size. A flat
metal plate facing the radar has a huge RCS; angle it away and the RCS collapses
because the energy reflects elsewhere. Formally,

$$\\sigma = \\lim_{R\\to\\infty} 4\\pi R^2 \\frac{S_{\\text{scattered}}}{S_{\\text{incident}}},$$

the equivalent area that would scatter isotropically to give the observed echo.

RCS depends on **geometry, material and aspect angle**, and varies enormously:

| Target | Typical RCS (m²) |
| --- | --- |
| Insect / small bird | 0.00001 – 0.01 |
| Human | ~1 |
| Car | ~100 |
| Cargo ship | thousands |
| Stealth aircraft | 0.001 or less |

Because the range equation carries $\\sigma$ linearly while range enters as $R^4$,
**halving a target's RCS only cuts detection range by about 16%** ($2^{-1/4}$).
This is exactly the stealth design principle: shape facets to deflect energy
away from the radar, and coat surfaces with radar-absorbent material, to drive
$\\sigma$ down by orders of magnitude.

A real target's RCS also **fluctuates** pulse-to-pulse (Swerling models) as its
aspect and the interference of its scattering centres change — which is why
detection is treated statistically (Intermediate course).

**Next:** how the antenna sets where the radar looks and how finely it resolves
angle.
""",
        ),
        _t(
            "Antennas, beamwidth & angular resolution",
            "11 min",
            """\
# Antennas, beamwidth & angular resolution

The antenna focuses transmitted power into a **beam** and, on receive, listens
preferentially in that direction. A larger aperture makes a narrower, higher-gain
beam. For an aperture of width $D$ at wavelength $\\lambda$, the half-power
**beamwidth** is roughly

$$\\theta_{3\\text{dB}} \\approx \\frac{\\lambda}{D}\\ \\text{(radians)}.$$

Narrower beams resolve angle better but cover the search volume more slowly — the
classic radar trade between resolution and coverage rate. Beamwidth narrows as
the aperture grows:

```plot
{"title": "Beamwidth narrows as aperture grows (θ ≈ λ/D)", "xLabel": "aperture D (wavelengths)", "yLabel": "beamwidth (degrees)", "xRange": [2, 40], "yRange": [0, 30], "functions": [{"expr": "57.3/x", "label": "θ ≈ 57.3 / (D/λ)  deg", "color": "#2563eb"}], "points": [{"x": 10, "y": 5.73, "label": "D = 10λ → ~5.7°", "color": "#16a34a", "size": 7}, {"x": 30, "y": 1.91, "label": "D = 30λ → ~1.9°", "color": "#dc2626", "size": 7}]}
```

Two targets at the same range are **angularly resolved** only if they fall in
separate beam positions — their cross-range separation must exceed about
$R\\,\\theta_{3\\text{dB}}$, which *grows with range*. That is why a radar's
cross-range resolution is poor at long range, and why synthetic aperture radar
(Advanced course) was invented to beat the aperture limit.

The antenna pattern also has **sidelobes** — weaker lobes off the main beam — that
can let strong off-axis targets or clutter leak in. Tapering the aperture
illumination lowers sidelobes at the cost of a slightly wider main beam.

**Next:** the decibel bookkeeping that ties power, gain and noise together.
""",
        ),
        _t(
            "The decibel link & SNR view",
            "11 min",
            """\
# The decibel link & SNR view

Radar quantities span many orders of magnitude, so engineers work in
**decibels**. A power ratio becomes

$$X_{\\text{dB}} = 10\\log_{10}\\!\\left(\\frac{P}{P_{\\text{ref}}}\\right),$$

which turns the range equation's products and divisions into additions and
subtractions — a **link budget** you can do on paper.

What matters for detection is not raw echo power but the **signal-to-noise
ratio** (SNR). The receiver itself generates **thermal noise** of power
$N = k T_s B$, where $k$ is Boltzmann's constant, $T_s$ the system noise
temperature and $B$ the bandwidth. Combining with the range equation:

$$\\text{SNR} = \\frac{P_t\\,G^2\\,\\lambda^2\\,\\sigma}{(4\\pi)^3\\,R^4\\,k T_s B\\,L},$$

with $L$ lumping system losses. Detection requires SNR above a threshold set by
the tolerable false-alarm rate (detection theory, Intermediate course).

Two free wins fall out of dB thinking:

- **Pulse integration.** Summing $n$ echoes coherently raises SNR by a factor
  $n$ (10·log₁₀ n dB) — collecting more looks beats raising power.
- **Lowering noise.** Every dB shaved off the noise figure is a dB of SNR, often
  cheaper than a dB of transmit power.

Since SNR ∝ 1/R⁴, in dB the SNR falls **40·log₁₀** per decade of range — a steep
but *linear-in-dB* line that makes range/power trade-offs easy to read off a
budget.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Radar & Remote Sensing — Intermediate ────────────────────────────────────

_RD_INTERMEDIATE = SeedCourse(
    slug="radar-intermediate",
    title="Radar & Remote Sensing — Intermediate",
    description=(
        "Measuring motion and squeezing performance: the Doppler effect and "
        "moving targets, CW & FMCW ranging from beat frequency, pulse compression "
        "and the matched filter, range and velocity resolution, the radar equation "
        "with clutter, noise and losses, and detection theory (threshold, Pd/Pfa, "
        "CFAR). Interactive waveform and spectrum plots throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The Doppler effect & moving targets",
            "12 min",
            """\
# The Doppler effect & moving targets

A target moving relative to the radar shifts the echo's frequency — the **Doppler
effect**. For a radial velocity $v_r$ (closing positive) at wavelength $\\lambda$,
the round-trip Doppler shift is

$$f_d = \\frac{2 v_r}{\\lambda}.$$

The factor of **2** is the round trip: the moving target both receives a
Doppler-shifted wave and re-radiates a further-shifted one. A closing target
raises the echo frequency; a receding one lowers it. Stationary clutter sits at
$f_d = 0$, so Doppler is what lets radar pull a moving car out of a mountain of
ground return.

The Doppler frequency is linear in velocity — and the slope steepens at shorter
wavelength (higher carrier), which is why automotive radars at 77 GHz measure
velocity so cleanly:

```plot
{"title": "Doppler shift vs radial velocity (fd = 2v/λ)", "xLabel": "radial velocity v (m/s)", "yLabel": "Doppler shift (kHz)", "xRange": [0, 60], "yRange": [-2, 32], "functions": [{"expr": "0.2*x", "label": "λ = 10 cm (S-band)", "color": "#2563eb"}, {"expr": "0.5*x", "label": "λ = 4 cm (X-band)", "color": "#dc2626"}], "points": [{"x": 30, "y": 6, "label": "S-band: 30 m/s → 6 kHz", "color": "#2563eb", "size": 6}, {"x": 30, "y": 15, "label": "X-band: 30 m/s → 15 kHz", "color": "#dc2626", "size": 6}]}
```

A processed Doppler spectrum shows targets as peaks displaced from the zero-Doppler
clutter spike — measuring a peak's offset reads out velocity directly. This is the
foundation of MTI and pulse-Doppler processing (Advanced course).

**Next:** measuring range continuously with CW and FMCW radar.
""",
        ),
        _t(
            "CW & FMCW radar",
            "12 min",
            """\
# CW & FMCW radar

A **continuous-wave (CW)** radar transmits an unbroken tone. It measures velocity
beautifully (pure Doppler) but, having no timing marker, **cannot measure range**.
The fix is to *sweep* the frequency: **FMCW** (frequency-modulated continuous
wave) ramps the transmit frequency linearly over a bandwidth $B$ in time $T_c$.

Because the echo is delayed by the round-trip time, at any instant the received
ramp is offset from the transmitted ramp. Mixing them yields a constant **beat
frequency** proportional to range:

$$f_b = \\frac{2 B}{c\\,T_c}\\,R \\quad\\Rightarrow\\quad R = \\frac{c\\,T_c}{2 B}\\,f_b.$$

The blue line is the transmitted up-chirp; the red line is the delayed echo — the
fixed vertical gap between them, read after mixing, is the beat frequency:

```plot
{"title": "FMCW: transmitted ramp and delayed echo → constant beat", "xLabel": "time (within one chirp)", "yLabel": "instantaneous frequency", "xRange": [0, 1], "yRange": [0, 1.2], "functions": [{"expr": "x", "label": "transmitted chirp", "color": "#2563eb"}, {"expr": "x-0.15", "label": "echo (delayed by τ)", "color": "#dc2626"}], "points": [{"x": 0.6, "y": 0.6, "color": "#2563eb", "size": 5}, {"x": 0.6, "y": 0.45, "label": "beat fb (gap)", "color": "#dc2626", "size": 5}]}
```

A real FMCW radar measures **range and velocity together**: a moving target adds a
Doppler term to the beat, so two or more chirps (a fast/slow-time grid) separate
the two. FMCW is cheap, low-power and dominant in **automotive radar** — the same
chirps reappear in pulse compression next.

**Next:** how chirps and the matched filter buy long range *and* fine resolution.
""",
        ),
        _t(
            "Pulse compression & the matched filter",
            "12 min",
            """\
# Pulse compression & the matched filter

The Basics course exposed a tension: long pulses carry the energy needed for
range, but **short** pulses give fine range resolution. **Pulse compression**
escapes it. Transmit a long pulse whose frequency sweeps — a **chirp** of
bandwidth $B$ — then on receive pass it through a **matched filter**.

The matched filter is the time-reversed conjugate of the transmitted waveform; it
maximises output SNR and compresses the long chirp into a narrow peak whose width
is set by the **bandwidth**, not the pulse length:

$$\\Delta R = \\frac{c}{2 B}.$$

You get the energy of a long pulse and the resolution of a short one. The
**compression ratio** is $\\tau B$ (time-bandwidth product). The matched-filter
output is a sharp peak (a sinc-like main lobe) flanked by **range sidelobes**:

```plot
{"title": "Matched-filter output: a sharp compressed peak", "xLabel": "range offset (resolution cells)", "yLabel": "normalised output", "xRange": [-6, 6], "yRange": [-0.3, 1.1], "functions": [{"expr": "sin(3.14159*x)/(3.14159*x)", "label": "compressed response", "color": "#2563eb"}], "points": [{"x": 0, "y": 1, "label": "target peak", "color": "#dc2626", "size": 7}]}
```

Those sidelobes can mask a weak target near a strong one, so the chirp is usually
**windowed** (tapered) to suppress them, trading a slightly wider main lobe for
much lower sidelobes — the same window trade-off as in antenna design and the FFT.

**Next:** stating range and velocity resolution precisely.
""",
        ),
        _t(
            "Range & velocity resolution",
            "11 min",
            """\
# Range & velocity resolution

Two limits decide whether a radar can tell two targets apart.

**Range resolution** depends only on the **waveform bandwidth** $B$:

$$\\Delta R = \\frac{c}{2 B}.$$

More bandwidth → finer range cells. A 150 MHz bandwidth gives $\\Delta R = 1$ m;
1.5 GHz gives 10 cm. This is why high-resolution and imaging radars are
wideband — and why pulse compression (large $\\tau B$) matters.

**Velocity (Doppler) resolution** depends on the **coherent dwell time** $T_d$ —
how long you observe the target across a burst of pulses:

$$\\Delta f_d = \\frac{1}{T_d} \\quad\\Rightarrow\\quad \\Delta v = \\frac{\\lambda}{2 T_d}.$$

Longer dwell → finer velocity bins. Both follow the same Fourier rule:
**resolution is the reciprocal of the observation extent** — in frequency for
range, in time for velocity.

Range resolution improves (the cell shrinks) as bandwidth grows:

```plot
{"title": "Range resolution vs bandwidth (ΔR = c / 2B)", "xLabel": "bandwidth B (MHz)", "yLabel": "range resolution (m)", "xRange": [10, 500], "yRange": [0, 16], "functions": [{"expr": "150/x", "label": "ΔR = 150 / B[MHz]  m", "color": "#2563eb"}], "points": [{"x": 150, "y": 1, "label": "150 MHz → 1 m", "color": "#16a34a", "size": 7}, {"x": 50, "y": 3, "label": "50 MHz → 3 m", "color": "#dc2626", "size": 7}]}
```

The waveform's joint range-Doppler behaviour is captured by the **ambiguity
function**, which makes explicit that you cannot have arbitrarily fine range *and*
velocity resolution from the same finite waveform.

**Next:** the full equation once clutter, noise and losses are in.
""",
        ),
        _t(
            "Clutter, noise & the radar equation with losses",
            "11 min",
            """\
# Clutter, noise & the radar equation with losses

The clean range equation assumed an empty world. Reality adds three corruptions.

**Receiver noise.** Thermal noise of power $N = k T_s B$ sets the noise floor; the
**noise figure** measures how much the receiver degrades SNR beyond the ideal.

**System losses.** A loss factor $L > 1$ collects atmospheric attenuation,
waveguide and radome losses, beam-shape and integration losses, and signal-
processing imperfections. Folded in, the SNR per pulse is

$$\\text{SNR} = \\frac{P_t\\,G^2\\,\\lambda^2\\,\\sigma}{(4\\pi)^3\\,R^4\\,k T_s B\\,L}.$$

**Clutter.** Unwanted echoes from ground, sea, rain or buildings can dwarf the
target. Crucially, clutter often scales with **range² (or less)**, while the
target scales with **range⁴** — so at long range a target may be *noise-limited*,
but at short range it is **clutter-limited**, and more transmit power doesn't
help (it lifts target and clutter together). The relevant ratio becomes the
**signal-to-clutter ratio (SCR)**, not SNR.

```mermaid
flowchart LR
    RX[Received echo] --> SUM[+]
    NOISE[Thermal noise kTsB] --> SUM
    CLUT[Clutter: ground / sea / rain] --> SUM
    SUM --> SP[Signal processor]
    SP -->|Doppler filtering| MTI[Reject zero-Doppler clutter]
    SP -->|matched filter| GAIN[Raise SNR]
    MTI --> DET[Detector]
    GAIN --> DET
    DET --> OUT[Declared targets]
```

The escape from clutter is **Doppler discrimination**: stationary clutter sits at
zero Doppler, so a moving target can be filtered out of it (MTI / pulse-Doppler,
Advanced course) even when raw clutter power is far larger.

**Next:** deciding *when* an echo counts as a detection.
""",
        ),
        _t(
            "Detection theory: threshold, Pd/Pfa & CFAR",
            "12 min",
            """\
# Detection theory: threshold, Pd/Pfa & CFAR

After processing, the radar compares each cell's output against a **threshold**.
Two outcomes matter:

- **Probability of detection** $P_d$ — a real target exceeds the threshold.
- **Probability of false alarm** $P_{fa}$ — noise alone exceeds it.

Because noise is random, the threshold is a trade: lower it to catch weak targets
and false alarms explode; raise it to suppress false alarms and you miss targets.
Below, the blue curve is noise-only and the red curve is target-plus-noise; the
green threshold splits them. The area of the noise curve beyond the threshold is
$P_{fa}$; the area of the target curve beyond it is $P_d$:

```plot
{"title": "Detection: threshold splits noise (Pfa) from target (Pd)", "xLabel": "matched-filter output", "yLabel": "probability density", "xRange": [-3, 9], "yRange": [0, 0.45], "controls": [{"name": "thr", "range": [0, 6], "value": 3, "label": "threshold"}], "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "noise only", "color": "#2563eb"}, {"expr": "exp(-(x-4)^2/2)/sqrt(2*pi)", "label": "target + noise", "color": "#dc2626"}], "points": [{"xExpr": "thr", "y": 0, "label": "threshold", "color": "#16a34a", "size": 7}]}
```

Raising SNR slides the red curve right, lifting $P_d$ at a fixed $P_{fa}$ — exactly
why integration and matched filtering pay off.

A fixed threshold fails when the noise/clutter level varies across the scene. The
fix is **CFAR** (Constant False-Alarm Rate): estimate the local background from
neighbouring **reference cells** around each **cell under test** (excluding guard
cells), then set the threshold a fixed multiple above that estimate. Cell-averaging
CFAR keeps $P_{fa}$ constant as the background drifts; ordered-statistic CFAR is
more robust near clutter edges and interfering targets.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Radar & Remote Sensing — Advanced ────────────────────────────────────────

_RD_ADVANCED = SeedCourse(
    slug="radar-advanced",
    title="Radar & Remote Sensing — Advanced",
    description=(
        "Systems that image and track: MTI and pulse-Doppler processing, synthetic "
        "aperture radar and imaging, phased arrays and electronic beam steering, "
        "tracking with range/Doppler gates and an intro to Kalman filtering, remote "
        "sensing across the radar bands, and a worked end-to-end system design. "
        "Processing-chain diagrams, SAR geometry and interactive plots throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "MTI & pulse-Doppler processing",
            "12 min",
            """\
# MTI & pulse-Doppler processing

To dig moving targets out of strong stationary clutter, radar exploits the one
thing that separates them: **Doppler**. Clutter sits near zero Doppler; a moving
target does not.

**Moving-target indication (MTI)** subtracts successive pulses. A single-delay
canceller forms $y[n] = x[n] - x[n-1]$, which **nulls** any echo unchanged between
pulses (clutter) while passing changing echoes. Its frequency response is a
high-pass notch at zero Doppler; a double canceller deepens the notch.

**Pulse-Doppler** processing goes further: collect a coherent burst of $M$ pulses
and run an **FFT across the pulses** (slow time) for each range cell. This sorts
echoes into **Doppler bins**, simultaneously rejecting clutter and *measuring*
velocity, with a Doppler resolution of $1/T_d$ (the dwell rule from before).

```mermaid
flowchart LR
    ADC[Digitised echoes] --> RC[Range compression / matched filter]
    RC --> RD[Build range × pulse data cube]
    RD --> DF[Doppler FFT across pulses]
    DF --> CL[Clutter / zero-Doppler rejection]
    CL --> CFAR[CFAR detection]
    CFAR --> RDMAP[Range-Doppler map]
    RDMAP --> TR[To tracker]
```

Two artefacts must be managed. **Blind speeds**: targets whose Doppler is a
multiple of the PRF alias onto the clutter notch and vanish — dodged by
**staggering the PRF** (multiple PRFs so a target blind at one is visible at
another). **Range-Doppler ambiguity**: high PRF gives clean Doppler but ambiguous
range, low PRF the reverse — medium-PRF schemes resolve both by combining bursts.

**Next:** synthesising a giant antenna to image the ground.
""",
        ),
        _t(
            "Synthetic aperture radar (SAR) & imaging",
            "13 min",
            """\
# Synthetic aperture radar (SAR) & imaging

A real antenna's cross-range resolution degrades with range ($R\\,\\theta \\approx
R\\lambda/D$) — useless for fine imaging from orbit. **Synthetic aperture radar**
beats this by moving the radar along a track and **coherently combining** echoes
collected over a long flight path, synthesising an aperture far larger than the
physical antenna.

```mermaid
flowchart TB
    PLAT[Moving platform: aircraft / satellite] --> PATH[Flies along-track]
    PATH --> P1[Pulse 1 echo]
    PATH --> P2[Pulse 2 echo]
    PATH --> P3[Pulse N echo]
    P1 --> COMB[Coherent combination = synthetic aperture]
    P2 --> COMB
    P3 --> COMB
    COMB --> AZ[Azimuth focusing]
    GEO[Range = slant timing] --> IMG[2-D SAR image]
    AZ --> IMG
```

The striking result: SAR **azimuth resolution** depends only on the real antenna
length $L$, and is *independent of range*:

$$\\Delta x_{\\text{az}} \\approx \\frac{L}{2}.$$

A **shorter** real antenna gives **finer** resolution (it has a wider beam, so any
ground patch is seen over a longer synthetic aperture). Range resolution still
comes from bandwidth, so SAR pairs a wideband chirp (range) with along-track
coherent integration (azimuth) to form a true 2-D image.

The processing is demanding — precise platform motion, phase coherence over the
aperture, and azimuth compression matched to the changing target range (a chirp in
slow time). Variants extend it: **spotlight** SAR steers the beam to dwell on a
patch for higher resolution; **interferometric** SAR (InSAR) uses two passes to
extract terrain height and millimetre ground deformation; **GMTI** detects moving
targets that smear in ordinary SAR.

**Next:** steering the beam with no moving parts.
""",
        ),
        _t(
            "Phased arrays & electronic beam steering",
            "12 min",
            """\
# Phased arrays & electronic beam steering

A **phased array** replaces a single dish with many small radiating elements whose
relative **phases** are controlled electronically. Adding a progressive phase shift
across the elements tilts the combined wavefront, steering the beam **without
moving the antenna** — in microseconds.

For elements spaced $d$ apart, a phase increment $\\Delta\\phi$ between adjacent
elements steers the main beam to

$$\\sin\\theta = \\frac{\\lambda\\,\\Delta\\phi}{2\\pi d}.$$

Electronic steering enables agile multifunction radar: interleave search and track,
revisit threats instantly, and form **multiple simultaneous beams**. Modern systems
are **active electronically scanned arrays (AESA)**, with a transmit/receive module
behind every element — graceful degradation, high reliability, and adaptive nulling
of jammers.

Two constraints shape the design. **Grating lobes**: if elements are spaced more
than about $\\lambda/2$, the array radiates strong spurious beams (the spatial
analogue of aliasing) — so element spacing must stay near a half wavelength.
**Scan loss**: as the beam steers off broadside, the projected aperture shrinks,
so gain falls and the beam broadens roughly as $1/\\cos\\theta$, limiting useful
scan to roughly ±60°.

Element-level phase control also enables **digital beamforming** and adaptive
arrays that place pattern nulls on interference directions — the bridge from
hardware steering to the space-time adaptive processing used against clutter and
jamming.

**Next:** keeping a track on a target over time.
""",
        ),
        _t(
            "Tracking: gates & an intro to the Kalman filter",
            "12 min",
            """\
# Tracking: gates & an intro to the Kalman filter

Detection finds a target *now*; **tracking** maintains its identity and estimates
its state (position, velocity) over many scans, smoothing noisy measurements and
predicting where it will be next.

**Gating.** Rather than test every detection against every track, the tracker
**predicts** each track's next position and opens a **range/Doppler gate** — a small
acceptance window — around the prediction. Only detections inside the gate are
candidate updates, which slashes the **data-association** problem (which plot
belongs to which track). When several plots compete, association rules (nearest
neighbour, or probabilistic methods) decide.

**The Kalman filter** is the workhorse estimator. It alternates two steps:

1. **Predict** — propagate the state and its uncertainty forward with a motion
   model (e.g. constant velocity).
2. **Update** — blend the prediction with the new measurement, weighted by their
   relative uncertainties via the **Kalman gain** $K$:

$$\\hat{x} \\leftarrow \\hat{x}_{\\text{pred}} + K\\,(z - H\\hat{x}_{\\text{pred}}).$$

A noisy measurement → small gain (trust the model); a precise measurement → large
gain (trust the data). The estimate (red) tracks the true path (blue) while
filtering measurement noise:

```plot
{"title": "Tracking: filtered estimate follows the true trajectory", "xLabel": "time (scans)", "yLabel": "position", "xRange": [0, 10], "yRange": [0, 12], "functions": [{"expr": "x", "label": "true trajectory", "color": "#2563eb"}, {"expr": "x + 0.6*sin(2*x)/(1+0.4*x)", "label": "Kalman estimate (noise filtered)", "color": "#dc2626"}]}
```

Manoeuvring targets break the constant-velocity assumption, handled by tuning
process noise, interacting-multiple-model (IMM) filters, or the extended/unscented
Kalman filter for nonlinear range-angle measurements.

**Next:** the radar bands and what they sense.
""",
        ),
        _t(
            "Remote sensing & radar bands",
            "11 min",
            """\
# Remote sensing & radar bands

Radar choices begin with **frequency band**, because wavelength governs antenna
size, resolution, atmospheric penetration and achievable bandwidth.

| Band | Frequency | Typical use |
| --- | --- | --- |
| HF/VHF | 3–300 MHz | Over-the-horizon, foliage/ground penetration |
| L | 1–2 GHz | Long-range surveillance, spaceborne SAR |
| S | 2–4 GHz | Air-traffic and weather radar |
| C | 4–8 GHz | Weather radar, SAR |
| X | 8–12 GHz | High-resolution imaging, marine, airborne |
| Ku/K/Ka | 12–40 GHz | Short-range, automotive, high resolution |
| W | 75–110 GHz | 77 GHz automotive, cloud radar |

The pattern: **lower bands** (long wavelength) penetrate weather, foliage and even
soil, but need large antennas and offer little bandwidth (coarse range
resolution). **Higher bands** (short wavelength) allow compact antennas, wide
bandwidth and fine resolution, but suffer more atmospheric and rain attenuation.

**Remote sensing** applications follow from this. **Weather radar** measures
rainfall from backscatter and (with dual polarisation) drop shape, and storm winds
from Doppler. **Spaceborne SAR** maps terrain, sea ice, deforestation and crops day
or night through cloud. **InSAR** measures ground subsidence and earthquake
deformation to the millimetre. **Scatterometers** infer ocean surface wind from sea
clutter; **altimeters** measure sea-surface height. **GPR** (ground-penetrating
radar) images buried utilities and archaeology. **Automotive radar** at 77 GHz
brings the whole toolkit — FMCW, Doppler, arrays — to every new car.

**Next:** put the pieces together in a system design.
""",
        ),
        _t(
            "System design example: detect a target at range R",
            "12 min",
            """\
# System design example: detect a target at range R

Tie the track together by sizing a radar to **detect a 1 m² target at 50 km** with
$P_d = 0.9$, $P_{fa} = 10^{-6}$. Work in decibels, where the range equation is a
sum and difference of terms.

**1. Required SNR.** From detection theory, $P_d = 0.9$ at $P_{fa} = 10^{-6}$
(non-fluctuating target) needs roughly **13 dB** single-pulse SNR. Integrating
$n$ pulses relaxes the per-pulse requirement by about $10\\log_{10} n$ dB.

**2. The link budget.** Start from

$$\\text{SNR} = \\frac{P_t\\,G^2\\,\\lambda^2\\,\\sigma}{(4\\pi)^3\\,R^4\\,k T_s B\\,L}.$$

Pick a band — say **X-band**, $\\lambda = 3$ cm — for a compact high-gain antenna.
Choose $G$, $B$ (which also fixes range resolution $\\Delta R = c/2B$), system
noise $kT_sB$ and a loss budget $L$ (atmosphere + processing). Solve for the $P_t$
that yields ≥ 13 dB SNR at 50 km, then verify the implied transmitter is feasible.

**3. Confront the $R^4$ wall.** Detection SNR collapses as $1/R^4$. The plot shows
the SNR ratio vs range against the required detection threshold (≈ 20× linear,
i.e. 13 dB); the crossing is the achievable range. If 50 km falls short, the
cheapest levers are usually **integration** and **lower noise**, not raw power:

```plot
{"title": "Link budget: SNR ∝ 1/R⁴ crosses the detection threshold", "xLabel": "range (relative to design point)", "yLabel": "SNR (linear ratio)", "xRange": [0.4, 2.2], "yRange": [0, 120], "functions": [{"expr": "20/x^4", "label": "SNR ∝ 1/R⁴", "color": "#2563eb"}, {"expr": "20", "label": "required SNR ≈ 20 (13 dB)", "color": "#16a34a"}], "points": [{"x": 1, "y": 20, "label": "design point (50 km)", "color": "#dc2626", "size": 7}]}
```

**4. Choose PRF and waveform.** Set the PRF so $R_{\\text{ua}} = c/2\\,\\text{PRF}$
clears 50 km (low enough) while keeping velocity coverage adequate (high enough) —
or stagger PRFs. Pick bandwidth for the needed range resolution and a chirp with
time-bandwidth product $\\tau B$ large enough for both energy and resolution.

**5. Iterate.** Adjust gain, dwell, PRF and band until SNR, unambiguous range,
resolution and clutter rejection all close at once. That simultaneous balancing —
power vs antenna vs waveform vs processing — *is* radar system engineering.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


RADAR_COURSES: tuple[SeedCourse, ...] = (_RD_BASICS, _RD_INTERMEDIATE, _RD_ADVANCED)

__all__ = ["RADAR_COURSES"]
