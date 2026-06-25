"""Optical Fiber Communications track: Basics -> Intermediate -> Advanced.

A fiber *systems* curriculum (complementary to the photonics *devices* course):
the optical link, light guidance, single- vs multi-mode fiber, attenuation and
the transmission windows, transmitters and receivers (Basics); dispersion, the
power budget, bit-rate*distance limits, IM-DD, noise/BER, and practical losses
(Intermediate); WDM/DWDM, optical amplifiers, coherent detection and DSP,
nonlinear effects, PON/FTTH access, and a long-haul/datacenter design example
(Advanced). Lessons are `text` with LaTeX, interactive ```plot blocks and
```mermaid link diagrams. Quizzes are attached from the QUIZ_REGISTRY
(seed_quizzes/fiber_optics_*.py) at assembly time, keyed by the lesson titles
below.
"""

# Lesson prose uses typographic characters (×, →, ≈, μ, λ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Optical Fiber Communications — Basics ─────────────────────────────────────

_FO_BASICS = SeedCourse(
    slug="fiber-optics-basics",
    title="Optical Fiber Communications — Basics",
    description=(
        "How light carries the internet: why optical fiber, the optical link "
        "block diagram, total internal reflection and waveguiding, single-mode "
        "vs multi-mode fiber, attenuation and the transmission windows, and the "
        "transmitter (LED vs laser) and receiver (PIN/APD) ends of the link. A "
        "systems-first companion to the photonics devices course, with "
        "interactive plots and link diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why optical fiber & the optical link",
            "10 min",
            """\
# Why optical fiber & the optical link

Every long-distance call, streamed video and cloud request travels — for most of
its journey — as **pulses of light inside a glass fiber**. Optical fiber won
because it offers what copper cannot:

- **Enormous bandwidth.** The optical carrier sits near $200\\,$THz, so even a
  tiny fractional bandwidth is *terabits per second* on one fiber.
- **Low loss.** Good fiber attenuates only $\\approx 0.2\\,$dB/km — light travels
  tens of kilometres before needing a boost. Coaxial cable loses that much in
  metres.
- **Immunity & size.** Glass is an insulator: no electromagnetic interference, no
  crosstalk, no ground loops, and a hair-thin fiber replaces a thick cable.

Every fiber link, from a 2 m datacenter patch to a transoceanic cable, is the
same three blocks: a **transmitter** turns electrical bits into light, the
**fiber** carries that light, and a **receiver** turns it back into bits.

```mermaid
flowchart LR
  DATA["data in (bits)"] --> TX["transmitter\\n(laser/LED + driver)"]
  TX -->|optical power| FIBER["optical fiber\\n(attenuation + dispersion)"]
  FIBER --> RX["receiver\\n(photodiode + amplifier)"]
  RX --> OUT["data out (bits)"]
```

Two impairments dominate the rest of this course: the fiber **attenuates** the
signal (it gets weaker) and **disperses** it (pulses spread and blur). Manage
those two and you have a working link.

**Next:** how the glass traps the light in the first place.
""",
        ),
        _t(
            "Light guidance & total internal reflection",
            "11 min",
            """\
# Light guidance & total internal reflection

A fiber is glass-in-glass: a **core** of refractive index $n_1$ surrounded by a
**cladding** of slightly lower index $n_2 < n_1$. Light that hits the core–cladding
boundary at a shallow enough angle is **totally internally reflected** and bounces
along the core, trapped.

Snell's law sets the threshold. **Total internal reflection** occurs for angles of
incidence beyond the **critical angle** $\\theta_c$:

$$\\sin\\theta_c = \\frac{n_2}{n_1}.$$

Light entering the end face is captured only if it falls inside the **acceptance
cone**, summarised by the **numerical aperture**:

$$\\mathrm{NA} = \\sqrt{n_1^2 - n_2^2} = n_0 \\sin\\theta_{\\max}.$$

A larger index contrast accepts more light but, as we'll see, also lets in more
*modes*. Below, the fraction of light captured grows with NA (more contrast =
wider acceptance cone), then saturates:

```plot
{"title": "Acceptance: captured fraction vs numerical aperture", "xLabel": "numerical aperture NA", "yLabel": "relative captured light", "xRange": [0, 0.5], "yRange": [0, 1.1], "functions": [{"expr": "1 - exp(-12*x*x)", "label": "captured fraction (∝ NA²)", "color": "#2563eb"}], "points": [{"x": 0.14, "y": 0.21, "label": "single-mode NA ≈ 0.14", "color": "#16a34a", "size": 6}, {"x": 0.275, "y": 0.6, "label": "multi-mode NA ≈ 0.275", "color": "#dc2626", "size": 6}]}
```

The ray picture (bouncing rays) is intuitive, but strictly the fiber is a
**waveguide** that supports a discrete set of allowed field patterns — **modes** —
which is where we go next.

**Next:** one mode or many — single-mode vs multi-mode fiber.
""",
        ),
        _t(
            "Single-mode vs multi-mode fiber",
            "11 min",
            """\
# Single-mode vs multi-mode fiber

How many distinct light paths (**modes**) a fiber supports depends on the core
size and the index contrast, captured by the dimensionless **V-number**:

$$V = \\frac{2\\pi a}{\\lambda}\\,\\mathrm{NA},$$

where $a$ is the core radius and $\\lambda$ the wavelength. When $V < 2.405$ only
**one mode** propagates.

**Multi-mode fiber (MMF)** — big core ($\\approx 50$–$62.5\\,\\mu$m). Many modes travel
at slightly different speeds, so a sharp input pulse arrives **smeared**
(*modal dispersion*). Cheap LEDs and connectors suffice, but reach is short — it
dominates short datacenter and building links ($\\le$ a few hundred metres).

**Single-mode fiber (SMF)** — tiny core ($\\approx 9\\,\\mu$m). Only one mode, so no
modal dispersion: this is the fiber for every long-haul, metro and access link.
It needs a laser source and tighter alignment.

```mermaid
flowchart LR
  subgraph MMF["multi-mode (large core)"]
    M1["mode 1 (fast)"]
    M2["mode 2 (slow)"]
  end
  subgraph SMF["single-mode (tiny core)"]
    S1["single mode"]
  end
  MMF -->|pulse spreads → short reach| OUT1["smeared pulse"]
  SMF -->|no modal spread → long reach| OUT2["clean pulse"]
```

The takeaway: **more modes = more spreading = less reach.** A bigger core is
easier to couple into but trades away the distance you can run.

**Next:** how strongly the glass itself attenuates light, and at which colours.
""",
        ),
        _t(
            "Attenuation & the transmission windows",
            "11 min",
            """\
# Attenuation & the transmission windows

Even the best glass slowly absorbs and scatters light. **Attenuation** is
measured in **decibels per kilometre**, and power falls *exponentially* with
distance:

$$P(L) = P_0\\,10^{-\\alpha L/10}, \\qquad \\alpha \\approx 0.2\\,\\text{dB/km at }1550\\,\\text{nm}.$$

Loss depends strongly on **wavelength**. Two effects fight: **Rayleigh
scattering** falls as $1/\\lambda^4$ (worse at short wavelengths), while
**infrared absorption** rises at long wavelengths. Between them sit low-loss
**transmission windows**, with a historical **water-absorption peak** near
$1383\\,$nm. The minimum near $1550\\,$nm (the **C-band**) is why long-haul systems
live there:

```plot
{"title": "Fiber attenuation vs wavelength (approx, with windows)", "xLabel": "wavelength (nm)", "yLabel": "attenuation (dB/km)", "xRange": [800, 1700], "yRange": [0, 3], "functions": [{"expr": "0.2 + 7e10/(x^4) + exp((x-1700)/40) + 1.3*exp(-((x-1383)/22)^2)", "label": "total loss α(λ)", "color": "#2563eb"}], "points": [{"x": 850, "y": 1.94, "label": "1st window 850 nm", "color": "#16a34a", "size": 6}, {"x": 1310, "y": 0.44, "label": "2nd window 1310 nm (zero dispersion)", "color": "#f59e0b", "size": 6}, {"x": 1550, "y": 0.21, "label": "3rd window 1550 nm (min loss)", "color": "#dc2626", "size": 6}]}
```

- **850 nm** — first window, cheap sources, used with MMF in datacenters.
- **1310 nm** — second window, where standard fiber has near-**zero chromatic
  dispersion**.
- **1550 nm** — third window, **minimum loss** and where optical amplifiers work;
  the backbone of long-haul.

Low loss is why a fiber can run $80$–$100\\,$km between amplifiers. The exact
windows set which lasers and which fiber a system designer picks.

**Next:** the source end — how we turn bits into light.
""",
        ),
        _t(
            "The optical transmitter: LED vs laser diode",
            "10 min",
            """\
# The optical transmitter: LED vs laser diode

The transmitter converts an electrical bit stream into modulated light. Two
semiconductor sources dominate, both built from direct-bandgap III–V materials.

**LED (light-emitting diode)**
- Spontaneous emission: **broad spectrum** (tens of nm), **incoherent**, emits in
  many directions.
- Cheap and robust, but the wide spectrum causes lots of chromatic dispersion and
  little power couples into a fiber.
- Limited to low bit rates over MMF (short links).

**Laser diode (LD)**
- Stimulated emission in an optical cavity: **narrow spectrum**, **coherent**,
  directional beam that couples efficiently into SMF.
- **DFB lasers** emit essentially one wavelength — essential for high-speed and
  WDM systems.
- Faster modulation, higher power, longer reach.

A key transmitter parameter is the **L–I curve**: output optical power vs drive
current. A laser stays dark until the **threshold current** $I_{th}$, then power
rises steeply and almost linearly. We bias just above threshold and swing the
current to send 1s and 0s:

```plot
{"title": "Laser L–I curve: output power vs drive current", "xLabel": "drive current I (mA)", "yLabel": "optical power (mW)", "xRange": [0, 60], "yRange": [0, 6], "functions": [{"expr": "0.02*x", "label": "LED (gradual, low power)", "color": "#94a3b8"}, {"expr": "(x>15)*0.16*(x-15)", "label": "laser (threshold then linear)", "color": "#2563eb"}], "points": [{"x": 15, "y": 0, "label": "threshold I_th", "color": "#dc2626", "size": 6}]}
```

For most modern links the source is **directly modulated** (switch the laser
current) or driven through an **external modulator** for the highest speeds —
more on intensity modulation in the Intermediate track.

**Next:** the far end — detecting the light.
""",
        ),
        _t(
            "The optical receiver: PIN & APD photodiodes",
            "10 min",
            """\
# The optical receiver: PIN & APD photodiodes

At the far end a **photodiode** converts the arriving light back to current. An
incoming photon with enough energy lifts an electron across the bandgap, creating
a measurable photocurrent. The efficiency is the **responsivity**:

$$R = \\frac{I_{ph}}{P_{opt}} \\;[\\text{A/W}], \\qquad R = \\eta\\,\\frac{q\\lambda}{hc},$$

where $\\eta$ is the quantum efficiency. Two detectors dominate:

**PIN photodiode** — an intrinsic region between p and n layers widens the
absorption zone. Simple, fast, low-noise, no internal gain. The default receiver.

**APD (avalanche photodiode)** — a high reverse bias makes carriers **multiply**
by impact ionisation, giving internal gain $M$ (typically $\\times 10$). It improves
sensitivity when the following electronics are noisy, at the cost of extra
**excess noise** and temperature sensitivity.

After the photodiode comes a **transimpedance amplifier (TIA)** that turns the
small photocurrent into a usable voltage, then a decision circuit that recovers
the bits.

```mermaid
flowchart LR
  LIGHT["arriving light"] --> PD["photodiode\\n(PIN or APD) → I_ph"]
  PD --> TIA["transimpedance amp"]
  TIA --> DEC["decision / clock recovery"]
  DEC --> BITS["recovered bits"]
```

The smallest optical power a receiver can still decode reliably is its
**sensitivity** — set by noise and the required error rate, which the
Intermediate track quantifies with the Q-factor and BER.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Optical Fiber Communications — Intermediate ───────────────────────────────

_FO_INTERMEDIATE = SeedCourse(
    slug="fiber-optics-intermediate",
    title="Optical Fiber Communications — Intermediate",
    description=(
        "Engineering a real link: dispersion (modal, chromatic, PMD) and pulse "
        "broadening, the optical power/loss budget, the bit-rate*distance product "
        "and its limits, intensity-modulation/direct-detection (IM-DD), noise and "
        "sensitivity (BER, Q-factor, eye diagram), and the practical losses of "
        "connectors and splices. The systems-design core, with interactive plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Dispersion: modal, chromatic & PMD",
            "12 min",
            """\
# Dispersion: modal, chromatic & PMD

Attenuation weakens a pulse; **dispersion spreads it in time** until adjacent bits
overlap. Three mechanisms:

- **Modal dispersion** (MMF only): different modes travel different path lengths,
  so they arrive at different times. Eliminated by single-mode fiber.
- **Chromatic dispersion** (CD): a real source has a spread of wavelengths, and
  each travels at a slightly different speed. Broadening scales with the
  **dispersion parameter** $D$ $[\\text{ps}/(\\text{nm}\\cdot\\text{km})]$, the
  source linewidth $\\Delta\\lambda$ and length $L$:
  $$\\Delta t_{CD} = D\\,L\\,\\Delta\\lambda.$$
  Standard fiber has $D \\approx 0$ near $1310\\,$nm and $D \\approx 17\\,\\text{ps/(nm·km)}$
  at $1550\\,$nm.
- **Polarization-mode dispersion (PMD)**: tiny asymmetries split the two
  polarizations; it grows only as $\\sqrt{L}$ but limits the very highest rates.

A pulse of initial width $T_0$ broadens; the wider it gets, the more it leaks into
neighbouring bit slots. Increase the link length and watch the output pulse
flatten and spread:

```plot
{"title": "Chromatic dispersion broadens a pulse with distance", "xLabel": "time (a.u.)", "yLabel": "amplitude", "xRange": [-6, 6], "yRange": [0, 1.1], "controls": [{"name": "L", "range": [0, 100], "value": 0, "step": 5, "label": "fiber length L (km)"}], "functions": [{"expr": "exp(-x^2/(1 + 0.0016*L*L))/sqrt(1 + 0.0016*L*L)", "label": "pulse after L km", "color": "#2563eb"}], "points": [{"x": 0, "y": 1, "label": "input pulse (L = 0)", "color": "#dc2626", "size": 6}]}
```

Once $\\Delta t$ approaches a bit period, bits blur into one another
(intersymbol interference). Dispersion, not loss, sets the reach of high-speed
links — which leads straight to the bit-rate*distance limit.

**Next:** budgeting the power that survives the link.
""",
        ),
        _t(
            "The optical power & loss budget",
            "11 min",
            """\
# The optical power & loss budget

A link works only if the receiver still gets *more* power than its sensitivity.
The **power budget** is plain bookkeeping, all in **decibels** so losses simply
add:

$$P_{rx} = P_{tx} - \\alpha L - L_{conn} - L_{splice} - M,$$

where $P_{tx}$ is launched power (dBm), $\\alpha L$ the fiber loss, the connector and
splice terms account for joints, and $M$ is a **safety margin** (often $3$–$6\\,$dB)
for ageing and repairs. The link is feasible when $P_{rx} \\ge$ **receiver
sensitivity**.

The available **link margin** is $P_{tx} - \\text{sensitivity}$; everything else
eats into it. Below, received power falls linearly (in dB) with distance until it
crosses the sensitivity floor — that crossing is your maximum loss-limited reach:

```plot
{"title": "Power budget: received power vs distance", "xLabel": "distance (km)", "yLabel": "power (dBm)", "xRange": [0, 140], "yRange": [-40, 5], "functions": [{"expr": "0 - 0.22*x - 2", "label": "received power (0 dBm launch)", "color": "#2563eb"}, {"expr": "-28", "label": "receiver sensitivity", "color": "#dc2626"}], "points": [{"x": 118, "y": -28, "label": "max loss-limited reach ≈ 118 km", "color": "#16a34a", "size": 6}]}
```

In practice you tabulate every term, sum the losses, subtract from launch power,
and confirm a positive margin. If not: launch more power, use lower-loss fiber,
fewer connectors, a more sensitive receiver — or add an amplifier (Advanced).

**Next:** when *dispersion*, not power, is what runs out.
""",
        ),
        _t(
            "Bit rate × distance product & limits",
            "11 min",
            """\
# Bit rate × distance product & limits

Two ceilings cap a link:

1. **Loss-limited** — the power budget runs out (previous lesson).
2. **Dispersion-limited** — pulses spread until they overlap.

For the second, a useful rule is the **bit-rate*distance product**: roughly,
the broadening $\\Delta t$ must stay below a fraction of the bit period $1/B$.
For chromatic dispersion this gives a hyperbolic limit — **doubling the bit rate
halves the reach**:

$$B \\cdot L \\lesssim \\frac{1}{4\\,|D|\\,\\Delta\\lambda} \\quad\\Rightarrow\\quad L_{\\max} \\propto \\frac{1}{B}.$$

That single product — Gb/s × km — lets you compare systems at a glance. Below,
the dispersion-limited reach falls as $1/B$; the horizontal line is a fixed
loss-limited reach. The *lower* of the two curves wins at each bit rate:

```plot
{"title": "Reach vs bit rate: dispersion vs loss limit", "xLabel": "bit rate B (Gb/s)", "yLabel": "max reach L (km)", "xRange": [1, 40], "yRange": [0, 160], "functions": [{"expr": "1600/x", "label": "dispersion-limited (∝ 1/B)", "color": "#2563eb"}, {"expr": "100", "label": "loss-limited (fixed)", "color": "#dc2626"}], "points": [{"x": 16, "y": 100, "label": "crossover: limit switches", "color": "#16a34a", "size": 6}]}
```

Below the crossover the link is loss-limited (add amplifiers); above it the link
is dispersion-limited (use lower-$D$ fiber, dispersion compensation, or narrower
sources). Coherent systems (Advanced) sidestep this by undoing dispersion in DSP.

**Next:** how the bits are actually impressed on the light.
""",
        ),
        _t(
            "Intensity modulation & direct detection (IM-DD)",
            "11 min",
            """\
# Intensity modulation & direct detection (IM-DD)

The simplest, cheapest and still most common scheme is **IM-DD**: modulate the
**intensity** (on/off, more or less light) and at the receiver simply detect
**power** with a photodiode. The photodiode is a *square-law* device — its current
follows optical power, discarding the optical phase entirely.

Two ways to modulate:
- **Directly modulated laser (DML)** — swing the drive current. Simple, but the
  current also shifts the wavelength (**chirp**), worsening chromatic dispersion.
- **External modulator** (e.g. Mach–Zehnder) — keep the laser steady (CW) and gate
  its output. Low chirp, used at the highest IM-DD rates.

The plain on/off format is **NRZ-OOK** (non-return-to-zero on-off keying): a 1 is
light, a 0 is dark. Because detection throws away phase, IM-DD is limited to
intensity-only formats (OOK, and multi-level **PAM4**):

```mermaid
flowchart LR
  CW["CW laser"] --> MOD["intensity modulator"]
  BITS["bit stream"] --> MOD
  MOD -->|optical power = data| FIBER["fiber"]
  FIBER --> PD["photodiode (square-law)\\nI ∝ optical power"]
  PD --> RX["decision → bits"]
```

IM-DD dominates short reach and datacenters (cheap, low power). When dispersion or
reach pushes back, **PAM4** packs 2 bits/symbol to halve the symbol rate — and
beyond that, coherent detection (Advanced) recovers amplitude *and* phase.

**Next:** how noise decides whether a bit is read correctly.
""",
        ),
        _t(
            "Noise & sensitivity: BER, Q-factor & the eye",
            "12 min",
            """\
# Noise & sensitivity: BER, Q-factor & the eye

A receiver decides "1 or 0" by comparing the signal to a threshold. Noise
(thermal noise, **shot noise**, amplifier and APD excess noise) blurs the 1 and 0
levels; when they overlap enough, the decision flips and we get a **bit error**.
Link quality is the **bit error ratio (BER)**, with $10^{-9}$ to $10^{-12}$ typical
before forward error correction.

A clean summary is the **Q-factor** — the separation of the 1 and 0 levels
measured in noise units:

$$Q = \\frac{\\mu_1 - \\mu_0}{\\sigma_1 + \\sigma_0}, \\qquad \\text{BER} \\approx \\tfrac12\\,\\mathrm{erfc}\\!\\left(\\tfrac{Q}{\\sqrt2}\\right).$$

A bigger $Q$ means an exponentially smaller BER: $Q = 6$ gives BER $\\approx 10^{-9}$,
$Q = 7$ gives $\\approx 10^{-12}$. BER falls off a cliff as $Q$ rises:

```plot
{"title": "BER plunges as the Q-factor rises (log-like decay)", "xLabel": "Q-factor", "yLabel": "−log₁₀(BER)", "xRange": [3, 8], "yRange": [0, 14], "functions": [{"expr": "0.22*x*x - 0.1", "label": "≈ −log₁₀ BER", "color": "#2563eb"}], "points": [{"x": 6, "y": 9, "label": "Q = 6 → BER 1e−9", "color": "#dc2626", "size": 6}, {"x": 7, "y": 12, "label": "Q = 7 → BER 1e−12", "color": "#16a34a", "size": 6}]}
```

Engineers *see* $Q$ in the **eye diagram** — overlay many bit periods and the
1s/0s trace an open "eye". A tall, wide eye = healthy margin; noise closes it
vertically, jitter and dispersion close it horizontally. Below is the upper rail
of an eye opening and re-closing across a bit period:

```plot
{"title": "Eye diagram envelope: opening over one bit period", "xLabel": "time within bit (UI)", "yLabel": "amplitude", "xRange": [0, 1], "yRange": [0, 1.1], "functions": [{"expr": "0.5 + 0.45*sin(pi*x)", "label": "upper rail (1-level)", "color": "#2563eb"}, {"expr": "0.5 - 0.45*sin(pi*x)", "label": "lower rail (0-level)", "color": "#dc2626"}], "points": [{"x": 0.5, "y": 0.95, "label": "best sampling instant (eye widest)", "color": "#16a34a", "size": 6}]}
```

**Sensitivity** is the smallest received power that still meets the target BER.
The gap between received power and sensitivity is the same link margin from the
power budget — now expressed as confidence in the bits.

**Next:** the real-world losses at every joint.
""",
        ),
        _t(
            "Connectors, splices & practical losses",
            "10 min",
            """\
# Connectors, splices & practical losses

Theory assumes a continuous fiber; real links are stitched from segments joined by
**connectors** (mateable) and **splices** (permanent). Every joint costs power and
can reflect light back.

**Loss mechanisms at a joint**
- **Lateral / angular misalignment** of the two cores — the biggest culprit in
  single-mode fiber with its $9\\,\\mu$m core.
- **End-gap and end-face quality** — air gaps, dirt, scratches.
- **Mode-field / core-diameter mismatch** between dissimilar fibers.

Typical numbers to budget:

| Joint type | Insertion loss | Notes |
|---|---|---|
| Fusion splice | $\\sim 0.02$–$0.1$ dB | melted together; lowest loss |
| Mechanical splice | $\\sim 0.1$–$0.3$ dB | quick field repair |
| Connector (mated pair) | $\\sim 0.2$–$0.5$ dB | reusable, plus back-reflection |

**Return loss / reflectance** also matters: reflections destabilise lasers and
add noise. Angled polished connectors (**APC**) bounce reflections into the
cladding, giving far better return loss than flat **PC** connectors.

The whole point of the earlier power budget is to **count every one of these
joints**. A long route with dozens of connectors can lose several dB before the
fiber attenuation is even considered.

```mermaid
flowchart LR
  TX["Tx"] -->|launch| C1["connector\\n0.3 dB"]
  C1 --> F1["fiber span\\nα·L"]
  F1 --> SP["fusion splice\\n0.05 dB"]
  SP --> F2["fiber span\\nα·L"]
  F2 --> C2["connector\\n0.3 dB"]
  C2 --> RX["Rx (≥ sensitivity?)"]
```

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Optical Fiber Communications — Advanced ───────────────────────────────────

_FO_ADVANCED = SeedCourse(
    slug="fiber-optics-advanced",
    title="Optical Fiber Communications — Advanced",
    description=(
        "Modern optical networks: wavelength-division multiplexing (WDM/DWDM), "
        "optical amplifiers (EDFA, Raman), coherent detection and DSP, fiber "
        "nonlinearities (SPM, XPM, FWM), passive optical networks (PON/FTTH) for "
        "access, and a worked long-haul and datacenter system-design example. The "
        "technologies behind the global backbone, with interactive plots and "
        "network diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Wavelength-division multiplexing (WDM/DWDM)",
            "12 min",
            """\
# Wavelength-division multiplexing (WDM/DWDM)

A single fiber can carry many independent channels at once if each uses a
**different wavelength** — like many radio stations on one cable. **WDM**
multiplexes several lasers into one fiber and de-multiplexes them at the far end.

- **CWDM** (coarse) — wide $20\\,$nm spacing, no temperature control, cheap; a
  handful of channels for metro/access.
- **DWDM** (dense) — tight spacing on the **ITU grid** ($100\\,$GHz $\\approx 0.8\\,$nm,
  or $50/25\\,$GHz), packing **dozens to 100+ channels** into the C-band. The
  workhorse of long-haul, multiplying one fiber's capacity into the tens of Tb/s.

Channels occupy the low-loss C-band so a single **EDFA** (next lesson) can amplify
them all together. **ROADMs** (reconfigurable optical add-drop multiplexers) then
route individual wavelengths through a mesh network without converting back to
electronics.

```mermaid
flowchart LR
  L1["λ₁ Tx"] --> MUX["WDM mux"]
  L2["λ₂ Tx"] --> MUX
  L3["λ₃ Tx"] --> MUX
  MUX -->|all λ on one fiber| AMP["EDFA"]
  AMP --> DEMUX["WDM demux"]
  DEMUX --> R1["λ₁ Rx"]
  DEMUX --> R2["λ₂ Rx"]
  DEMUX --> R3["λ₃ Rx"]
```

The channels must stay on their assigned grid slots; laser drift, crosstalk and
nonlinear mixing (later in this course) set how tightly they can be packed.

**Next:** amplifying all those channels at once.
""",
        ),
        _t(
            "Optical amplifiers: EDFA & Raman",
            "12 min",
            """\
# Optical amplifiers: EDFA & Raman

Before optical amplifiers, every span needed an **electrical repeater** that
detected, retimed and re-transmitted *each* channel — impossible for dozens of
DWDM wavelengths. Optical amplifiers boost **all channels together, in the optical
domain**, and revolutionised long-haul.

**EDFA (Erbium-Doped Fiber Amplifier).** A length of erbium-doped fiber is pumped
at $980$ or $1480\\,$nm; the excited erbium ions amplify signals by stimulated
emission right across the **C-band** ($1530$–$1565\\,$nm) — exactly the DWDM band.
High gain ($20$–$30\\,$dB), transparent to bit rate and format. Its cost: it adds
**ASE noise** (amplified spontaneous emission), so the chain's **OSNR** (optical
signal-to-noise ratio) degrades with every amplifier.

**Raman amplification.** Pump light transfers energy to signal photons via
**stimulated Raman scattering** *in the transmission fiber itself* — distributed
gain that improves OSNR, often combined with EDFAs.

Each span loses $\\alpha L$ dB and each amplifier restores it. The OSNR drifts down
in steps along the chain; when it nears the receiver's required value, you've hit
the system reach:

```plot
{"title": "Amplified link: OSNR degrades along the chain (≈ 10·log₁₀ N)", "xLabel": "number of amplifiers N in chain", "yLabel": "OSNR (dB)", "xRange": [1, 16], "yRange": [10, 40], "functions": [{"expr": "37 - 10*sqrt(x)", "label": "OSNR ≈ 37 − 10·log₁₀N (approx)", "color": "#2563eb"}, {"expr": "16", "label": "minimum OSNR for target BER", "color": "#dc2626"}], "points": [{"x": 11, "y": 16, "label": "OSNR floor → reach limit", "color": "#16a34a", "size": 7}]}
```

OSNR, not power alone, becomes the currency of long-haul design: amplifiers fight
loss but slowly spend OSNR.

**Next:** recovering amplitude *and* phase — coherent detection.
""",
        ),
        _t(
            "Coherent optical communication & DSP",
            "13 min",
            """\
# Coherent optical communication & DSP

IM-DD throws away the optical phase. **Coherent detection** keeps it: the incoming
signal is mixed with a **local-oscillator laser**, so the receiver recovers the
full complex field — **amplitude and phase, on both polarizations**. That unlocks
two huge gains.

**More bits per symbol.** With phase available we use QAM constellations:
**QPSK** (2 bits/symbol), **16-QAM** (4), **64-QAM** (6) — and **polarization
multiplexing** doubles it again. A $400\\,$G channel fits in one DWDM slot.

**DSP fixes the fiber in software.** Because the receiver has the full field, a
**digital signal processor** can *undo* impairments that used to be fatal:
chromatic dispersion and PMD are equalised numerically, and carrier-phase
recovery tracks laser phase noise. Dispersion compensation modules vanish.

```mermaid
flowchart LR
  SIG["incoming signal"] --> HYB["90° optical hybrid"]
  LO["local oscillator laser"] --> HYB
  HYB --> ADC["balanced detectors → ADC"]
  ADC --> DSP["DSP: CD/PMD equalize,\\ncarrier recovery, demap"]
  DSP --> BITS["bits"]
```

The constellation packs more points as the format scales, but each point sits
closer to its neighbours, so higher-order QAM needs a *higher OSNR* — the same
OSNR currency from the amplifier lesson. Coherent + DSP is why modern long-haul
runs hundreds of Gb/s per wavelength over thousands of km.

**Next:** the nonlinear effects that ultimately cap how much you can push.
""",
        ),
        _t(
            "Nonlinear effects: SPM, XPM & FWM",
            "12 min",
            """\
# Nonlinear effects: SPM, XPM & FWM

At low power a fiber is linear. Push more power (or pack many DWDM channels) and
the glass's refractive index starts to depend on **intensity** (the **Kerr
effect**, $n = n_0 + n_2 I$). This sets an *upper* limit on launch power — the
opposite worry to attenuation:

- **Self-phase modulation (SPM)** — a pulse modulates its *own* phase, broadening
  its spectrum and interacting with dispersion.
- **Cross-phase modulation (XPM)** — one channel's intensity shifts the phase of
  its *neighbours*; a penalty that grows with channel count.
- **Four-wave mixing (FWM)** — three wavelengths beat together to generate new
  tones $f_i + f_j - f_k$ that land on *other* channels as crosstalk. Worst when
  channels are evenly spaced and dispersion is low.

The result is a sweet spot. Too *little* launch power and OSNR/noise dominate
(linear regime); too *much* and nonlinear penalties explode. Total penalty is
U-shaped, and the bottom is the **nonlinear Shannon-limit-like optimum**:

```plot
{"title": "Optimal launch power: noise vs nonlinear penalty", "xLabel": "launch power per channel (dBm)", "yLabel": "performance penalty (dB)", "xRange": [-6, 6], "yRange": [0, 8], "functions": [{"expr": "9/(x+8)", "label": "noise/OSNR penalty (falls)", "color": "#94a3b8"}, {"expr": "0.12*(x+2)^2", "label": "nonlinear penalty (rises)", "color": "#cbd5e1"}, {"expr": "9/(x+8) + 0.12*(x+2)^2", "label": "total penalty", "color": "#2563eb"}], "points": [{"x": 0, "y": 1.7, "label": "optimum launch power", "color": "#dc2626", "size": 6}]}
```

This is why you can't just "turn up the laser": nonlinearity, not loss, is the
final ceiling on a fully loaded DWDM line. Managing dispersion maps and channel
spacing keeps FWM and XPM in check.

**Next:** bringing fiber to homes — passive optical networks.
""",
        ),
        _t(
            "Passive optical networks (PON) & FTTH access",
            "11 min",
            """\
# Passive optical networks (PON) & FTTH access

Long-haul moves bulk traffic between cities; the **access network** is the
last-mile fiber to homes and businesses — **FTTH** (fiber to the home). The
dominant architecture is the **passive optical network (PON)**: a single fiber
from the operator is split by a **passive optical splitter** (no power, no
electronics) to serve many subscribers, cutting cost dramatically.

```mermaid
flowchart TD
  OLT["OLT (operator central office)"] -->|single feeder fiber| SPL["passive splitter\\n1 : 32"]
  SPL --> ONT1["ONT (home 1)"]
  SPL --> ONT2["ONT (home 2)"]
  SPL --> ONT3["ONT (home 3)"]
  SPL --> ONTN["ONT (home N)"]
```

- **OLT** (optical line terminal) sits at the central office; each home has an
  **ONT/ONU**.
- **Downstream** the OLT **broadcasts** to all ONTs on one wavelength; each ONT
  picks out its own packets (encrypted).
- **Upstream** the ONTs share one wavelength by **TDMA** — the OLT grants each a
  time slot to avoid collisions.
- Different wavelengths separate the two directions (WDM), so one fiber carries
  both.

Splitting divides the light: a $1{:}N$ splitter imposes $\\approx 10\\log_{10}N$ dB
of loss, so the PON power budget caps the split ratio and reach. Standards step
the rate up — GPON ($2.5\\,$G), XGS-PON ($10\\,$G), and beyond — while keeping the
same passive plant.

**Next:** put it all together in a system design.
""",
        ),
        _t(
            "System design: long-haul & datacenter examples",
            "12 min",
            """\
# System design: long-haul & datacenter examples

Designing a link is choosing technologies so that **both** the power budget and
the dispersion/OSNR budget close, at the target BER, with margin. Two very
different regimes show the trade-offs.

## Long-haul DWDM (e.g. 1500 km)

- **Fiber/band:** SMF in the C-band ($1550\\,$nm, $\\alpha \\approx 0.2\\,$dB/km).
- **Capacity:** DWDM, ~80 channels on the $50\\,$GHz grid.
- **Reach vs loss:** EDFAs every $\\sim 80\\,$km; the chain is **OSNR-limited**, so
  set launch power to the nonlinear optimum from the previous lesson.
- **Reach vs dispersion:** **coherent + DSP** equalises CD and PMD; QPSK or
  16-QAM per the available OSNR; strong **FEC** buys several dB of margin.

## Datacenter interconnect (e.g. 100 m – 2 km)

- **Fiber/band:** MMF at $850\\,$nm (very short) or SMF at $1310\\,$nm (zero
  dispersion) for a few km.
- **Scheme:** cheap, low-power **IM-DD** with **PAM4**; no amplifiers, no coherent
  DSP — cost and power per bit dominate, not reach.
- **Budget:** loss-limited and connector-loss-sensitive; dispersion is negligible
  at these lengths.

A first-pass feasibility check is just the loss-limited reach again — received
power must stay above sensitivity over the whole span:

```plot
{"title": "Design check: received power vs span for two regimes", "xLabel": "distance (km)", "yLabel": "received power (dBm)", "xRange": [0, 100], "yRange": [-35, 5], "functions": [{"expr": "0 - 0.22*x", "label": "C-band 1550 nm (0.22 dB/km)", "color": "#2563eb"}, {"expr": "3 - 0.35*x", "label": "1310 nm DC link (0.35 dB/km)", "color": "#f59e0b"}, {"expr": "-28", "label": "receiver sensitivity", "color": "#dc2626"}]}
```

The discipline is always the same: **list every gain and loss, confirm the worst
case still has margin, then pick the cheapest technology that closes both
budgets.** Long-haul spends money on coherent optics and amplifiers; datacenters
spend it on the lowest cost-per-bit.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


FIBER_OPTICS_COURSES = (_FO_BASICS, _FO_INTERMEDIATE, _FO_ADVANCED)

__all__ = ["FIBER_OPTICS_COURSES"]
