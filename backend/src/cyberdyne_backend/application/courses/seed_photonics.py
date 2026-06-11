"""Curated Optoelectronics & Photonics track: Basics, Intermediate, Advanced.

A complete photonics curriculum: light and the optoelectronic building blocks
(photons, refraction, LEDs, photodetectors, lasers), fibers and optical links
(fiber types, loss and dispersion, sources/detectors, modulation, components),
and photonic systems and integration (coherent optics, DWDM networking, silicon
photonics, solar cells, emerging photonics). Dual MATLAB + Python focus
throughout, with runnable Python labs (numpy + matplotlib), interactive ```plot
blocks, Mermaid diagrams, LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time and authored against the lesson titles below.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Optoelectronics & Photonics -- Basics -------------------------------------

_PHOTONICS_BASICS = SeedCourse(
    slug="photonics-basics",
    title="Optoelectronics & Photonics — Basics",
    description=(
        "Light from the ground up for engineers: photons, wavelength and energy, "
        "the EM spectrum and refractive index, reflection/refraction and total "
        "internal reflection, LEDs, photodetectors, and laser basics - with "
        "side-by-side MATLAB and Python, interactive plots, and a runnable "
        "spectrum/responsivity lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Light fundamentals for engineers",
            "11 min",
            """\
# Light fundamentals for engineers

Photonics is engineering with **light**. Light is an **electromagnetic wave**
*and* a stream of particles called **photons** - both pictures are true, and you
pick whichever makes the math easier.

## Wavelength, frequency and energy

A light wave has a **wavelength** $\\lambda$ (the spacing of the wave, in metres)
and a **frequency** $f$ (cycles per second). In vacuum they multiply to the speed
of light:

$$c = \\lambda f, \\qquad c \\approx 3 \\times 10^8\\ \\text{m/s}.$$

Each photon carries a tiny packet of energy set by the frequency (the Planck
relation):

$$E = h f = \\frac{h c}{\\lambda}, \\qquad h \\approx 6.626 \\times 10^{-34}\\ \\text{J s}.$$

Shorter wavelength = higher frequency = **more energetic** photons. Engineers
usually quote photon energy in **electron-volts (eV)**, with the handy rule
$E(\\text{eV}) \\approx 1240 / \\lambda(\\text{nm})$. Slide the wavelength and watch
the photon energy climb as you move toward the blue:

```plot
{"title": "Photon energy vs wavelength: E(eV) = 1240 / lambda(nm)", "xLabel": "wavelength lambda (nm)", "yLabel": "photon energy (eV)", "xRange": [200, 1600], "yRange": [0, 6.5], "grid": true, "controls": [{"name": "lam", "range": [200, 1600], "value": 550, "label": "wavelength (nm)"}], "functions": [{"expr": "1240/x", "label": "E = 1240/lambda"}], "points": [{"xExpr": "lam", "yExpr": "1240/lam", "label": "selected", "color": "#dc2626", "size": 7}]}
```

## The electromagnetic spectrum

Visible light is a sliver (about 380 to 750 nm) of a vast spectrum. Photonics
engineers care most about the **near-infrared**, where optical fibers and silicon
detectors work best.

| Band | Wavelength | Where it matters |
|------|-----------|------------------|
| Ultraviolet | 10-380 nm | sterilization, lithography |
| Visible | 380-750 nm | displays, lighting, cameras |
| Near-infrared | 750-1600 nm | fiber comms, LiDAR, remotes |
| Mid/far IR | 1.6-1000 um | thermal imaging, gas sensing |

## Refractive index

In a material, light slows to $v = c / n$, where $n$ is the **refractive index**
(about 1.0 for air, 1.5 for glass, 3.5 for silicon). A higher $n$ means slower
light and a shorter wavelength inside the material - the seed of every lens,
fiber and waveguide.

```matlab
h = 6.626e-34; c = 3e8;
lam = 1550e-9;                 % a fiber-comms wavelength
f = c/lam;                     % ~193 THz
E_J = h*f;  E_eV = E_J/1.602e-19;  % photon energy
```

```python
h, c = 6.626e-34, 3e8
lam = 1550e-9                  # a fiber-comms wavelength
f = c/lam                      # ~193 THz
E_J = h*f
E_eV = E_J/1.602e-19           # photon energy in eV
```

> **Real-world hook:** your TV remote, a LiDAR on a self-driving car, and a
> transatlantic fiber all use near-infrared light you cannot see - chosen because
> silicon detectors and glass fibers love those wavelengths.

**Next:** how light bends and gets trapped - the basis of fibers.
""",
        ),
        _t(
            "Reflection, refraction and guiding light",
            "12 min",
            """\
# Reflection, refraction and guiding light

When light hits a boundary between two materials, part **reflects** and part
**refracts** (bends). The bending is governed by **Snell's law**:

$$n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2,$$

where $\\theta$ is measured from the surface **normal**. Going from a slow medium
(high $n$) into a fast one (low $n$), the ray bends *away* from the normal - and
past a certain angle it cannot escape at all.

## Total internal reflection

When light travels from a denser medium toward a less dense one, there is a
**critical angle** beyond which it reflects completely back - **total internal
reflection (TIR)**:

$$\\theta_c = \\arcsin\\!\\left(\\frac{n_2}{n_1}\\right).$$

This is exactly how an **optical fiber** traps light: a high-index glass **core**
surrounded by a lower-index **cladding** keeps the light bouncing along the fiber
for kilometres. Slide the index ratio and watch the critical angle change:

```plot
{"title": "Critical angle for total internal reflection (slide index ratio)", "xLabel": "index ratio n2/n1", "yLabel": "critical angle (degrees)", "xRange": [0.5, 0.99], "yRange": [0, 90], "grid": true, "controls": [{"name": "ratio", "range": [0.6, 0.98], "value": 0.95, "label": "n2/n1 (cladding/core)"}], "functions": [{"expr": "deg(asin(x))", "label": "theta_c"}], "points": [{"xExpr": "ratio", "yExpr": "deg(asin(ratio))", "label": "selected", "color": "#dc2626", "size": 7}]}
```

## Refraction across an interface

The refracted angle follows directly from Snell's law as you tilt the incoming
ray. Going from glass ($n=1.5$) into air ($n=1.0$), the output angle grows faster
than the input until TIR kicks in:

```plot
{"title": "Snell refraction glass(1.5) to air(1.0): output angle vs input", "xLabel": "incident angle (degrees)", "yLabel": "refracted angle (degrees)", "xRange": [0, 41], "yRange": [0, 90], "grid": true, "functions": [{"expr": "deg(asin(1.5*sin(rad(x))))", "label": "refracted angle"}]}
```

```mermaid
flowchart LR
  SRC["light in core"] --> TIR["hits core/cladding boundary"]
  TIR -->|angle > theta_c| BOUNCE["total internal reflection"]
  BOUNCE --> GUIDE["light guided along fiber"]
```

```matlab
n1 = 1.5; n2 = 1.0;            % glass core, air
theta_c = asind(n2/n1);        % critical angle ~ 41.8 deg
theta1 = 20;                   % incident angle (deg)
theta2 = asind(n1/n2*sind(theta1));  % refracted angle
```

```python
import numpy as np
n1, n2 = 1.5, 1.0
theta_c = np.degrees(np.arcsin(n2/n1))   # ~41.8 deg
theta1 = 20.0
theta2 = np.degrees(np.arcsin(n1/n2*np.sin(np.radians(theta1))))
```

> **Real-world hook:** TIR is why a diamond sparkles, why a periscope works, and
> why the entire internet's backbone runs on hair-thin glass fibers. The same law
> designs camera lenses and eyeglasses.

**Next:** turning electricity into light - the LED.
""",
        ),
        _t(
            "LEDs and electroluminescence",
            "11 min",
            """\
# LEDs and electroluminescence

A **light-emitting diode (LED)** is a PN-junction diode that emits light when
current flows through it - **electroluminescence**. It is the inverse of a solar
cell: electricity in, light out.

## The PN junction as an emitter

In a forward-biased PN junction, electrons and holes are pushed together and
**recombine**. In the right semiconductor (a *direct-bandgap* material like
gallium arsenide or gallium nitride), each recombination releases a photon whose
energy equals the material's **bandgap** $E_g$:

$$E_{photon} = E_g = \\frac{h c}{\\lambda} \\;\\Rightarrow\\; \\lambda \\approx \\frac{1240}{E_g(\\text{eV})}\\ \\text{nm}.$$

So the **bandgap sets the color**. A wider gap gives a bluer photon; a narrower
gap gives red or infrared. Slide the bandgap to see the emission wavelength move
across the spectrum:

```plot
{"title": "LED color from bandgap: lambda(nm) = 1240 / Eg(eV)", "xLabel": "bandgap Eg (eV)", "yLabel": "emission wavelength (nm)", "xRange": [1, 3.5], "yRange": [300, 1300], "grid": true, "controls": [{"name": "Eg", "range": [1.1, 3.2], "value": 1.9, "label": "bandgap Eg (eV)"}], "functions": [{"expr": "1240/x", "label": "lambda(Eg)"}], "points": [{"xExpr": "Eg", "yExpr": "1240/Eg", "label": "selected", "color": "#dc2626", "size": 7}]}
```

| Material | Bandgap | Color |
|----------|---------|-------|
| AlGaInP | ~1.9 eV | red |
| GaP | ~2.2 eV | green |
| InGaN | ~2.7 eV | blue |
| InGaN + phosphor | mixed | white |

## Efficiency and the diode curve

Like any diode, an LED has a forward voltage knee (about 1.8 V for red, 3.2 V for
blue) and current grows steeply past it. You **never** drive an LED from a
voltage source - you set the current with a **series resistor** or a current
driver, because a tiny voltage change makes a huge current change.

```plot
{"title": "LED current vs forward voltage (exponential knee)", "xLabel": "forward voltage (V)", "yLabel": "current (mA)", "xRange": [0, 3.5], "yRange": [0, 40], "grid": true, "functions": [{"expr": "max(0, 5*exp((x-2.8)/0.13))", "label": "blue LED current"}]}
```

Modern white LEDs reach over 150 lumens per watt - far beyond incandescent bulbs
(~15) - which is why they took over lighting. **External quantum efficiency**
(photons out per electron in) and **luminous efficacy** are the figures of merit.

```matlab
Vsupply = 5; Vled = 2.0; Iled = 0.015;   % red LED at 15 mA
Rseries = (Vsupply - Vled)/Iled;          % current-limiting resistor ~200 ohm
```

```python
Vsupply, Vled, Iled = 5, 2.0, 0.015       # red LED at 15 mA
Rseries = (Vsupply - Vled)/Iled           # ~200 ohm
```

> **Real-world hook:** LEDs light your home, backlight every phone and TV, signal
> in fiber links, and the invisible infrared LED in your remote talks to your TV.
> Blue LEDs (Nobel Prize, 2014) unlocked white lighting and full-color displays.

**Next:** running the diode in reverse - photodetectors.
""",
        ),
        _t(
            "Photodetectors and the photoelectric effect",
            "11 min",
            """\
# Photodetectors and the photoelectric effect

A **photodetector** does the opposite of an LED: light in, electricity out. The
foundation is the **photoelectric effect** - a photon with enough energy frees an
electron. Einstein explained it in 1905 (his Nobel work), proving light comes in
quantized packets.

## The photodiode

Shine light on a reverse-biased PN junction and absorbed photons create
**electron-hole pairs**; the junction's field sweeps them out as a measurable
**photocurrent**. The photon must carry at least the bandgap energy
($\\lambda < hc/E_g$), so each detector material has a **cutoff wavelength**:
silicon detects visible to ~1100 nm, while fiber comms at 1550 nm needs
**InGaAs**.

## PIN photodiode

The workhorse is the **PIN** photodiode - an intrinsic (undoped) layer is
sandwiched between P and N regions. That wide depletion region absorbs more light
and responds **fast**, which is why PINs dominate optical receivers.

```mermaid
flowchart LR
  PH["incoming photons"] --> ABS["absorbed in intrinsic layer"]
  ABS --> EHP["electron-hole pairs created"]
  EHP --> FIELD["swept out by junction field"]
  FIELD --> I["photocurrent out"]
```

## Responsivity

The key spec is **responsivity** $R$ - amps of photocurrent per watt of light:

$$R = \\frac{I_{photo}}{P_{optical}} = \\frac{\\eta\\, q\\, \\lambda}{h c},$$

where $\\eta$ is the quantum efficiency. Responsivity **rises with wavelength**
(longer-wavelength photons are more numerous per watt) until it falls off a cliff
at the cutoff. Slide the quantum efficiency:

```plot
{"title": "Photodiode responsivity vs wavelength (slide quantum efficiency)", "xLabel": "wavelength (nm)", "yLabel": "responsivity (A/W)", "xRange": [400, 1100], "yRange": [0, 1], "grid": true, "controls": [{"name": "eta", "range": [0.4, 1.0], "value": 0.8, "label": "quantum efficiency"}], "functions": [{"expr": "eta*x/1240*(x<1050)", "label": "R = eta*q*lambda/hc"}]}
```

The ideal line $R = \\eta\\lambda/1240$ (A/W, $\\lambda$ in nm) shows responsivity
climbing linearly until the material's cutoff drops it to zero.

```matlab
q = 1.602e-19; h = 6.626e-34; c = 3e8;
eta = 0.8; lam = 850e-9;
R = eta*q*lam/(h*c);          % responsivity ~0.55 A/W
Iphoto = R * 1e-6;            % 1 uW of light -> photocurrent
```

```python
q, h, c = 1.602e-19, 6.626e-34, 3e8
eta, lam = 0.8, 850e-9
R = eta*q*lam/(h*c)           # ~0.55 A/W
Iphoto = R * 1e-6            # 1 uW of light
```

> **Real-world hook:** photodiodes are the eyes of optical communication, the
> sensor in every digital camera (millions of them), the receiver in your TV
> remote, and the cell in a solar panel. Avalanche photodiodes (next course) add
> internal gain for the faintest signals.

**Next:** the most coherent light source of all - the laser.
""",
        ),
        _t(
            "Laser basics: stimulated emission and gain",
            "12 min",
            """\
# Laser basics: stimulated emission and gain

A **laser** (Light Amplification by Stimulated Emission of Radiation) produces an
intense, narrow, **coherent** beam - one color, one direction, waves marching in
lockstep. Three ingredients make it work.

## 1. Stimulated emission

An excited atom can drop to a lower state by emitting a photon. **Stimulated
emission** is the magic: an incoming photon triggers the atom to emit a *second*
photon that is an exact clone - same wavelength, direction, and phase. One photon
becomes two identical ones; light is **amplified**.

## 2. Population inversion

Normally most atoms sit in the ground state and *absorb* light. To get net
amplification you need more atoms **excited** than not - a **population
inversion** - achieved by **pumping** energy in (electrically or optically). Only
then does stimulated emission win over absorption and the medium shows **gain**.

```mermaid
stateDiagram-v2
  [*] --> Ground
  Ground --> Excited: pump energy in
  Excited --> Ground: stimulated emission (clone photon)
  Excited --> Ground: spontaneous emission (random)
```

## 3. Optical feedback (the cavity)

Two mirrors form a **resonant cavity**: photons bounce back and forth through the
gain medium, each pass cloning more photons. One mirror is partly transparent and
lets a fraction out as the beam. Lasing starts once **gain exceeds loss** - the
**threshold**. Below threshold you get faint, incoherent light; above it, output
power climbs almost linearly with pump current. Slide the threshold current:

```plot
{"title": "Laser diode output power vs drive current (slide threshold)", "xLabel": "drive current (mA)", "yLabel": "optical output (mW)", "xRange": [0, 100], "yRange": [0, 30], "grid": true, "controls": [{"name": "Ith", "range": [10, 50], "value": 20, "label": "threshold current Ith (mA)"}], "functions": [{"expr": "(x>Ith)*0.4*(x-Ith)", "label": "P_out (L-I curve)"}]}
```

That kinked **L-I curve** (light vs current) is the signature of a **laser
diode** - the tiny semiconductor laser in every fiber transmitter, barcode
scanner, and laser pointer. It is basically an LED with mirrored end facets and
enough current to reach inversion and threshold.

## Why coherence matters

Spontaneous emission (an LED) sends photons every which way; stimulated emission
(a laser) makes them identical. That coherence lets a laser focus to a tiny spot
(cutting, surgery, reading a disc), stay one pure color (spectroscopy, sensing),
and carry data over long fibers without smearing.

```matlab
Ith = 20e-3; slope = 0.4;     % slope efficiency W/A -> 0.4 mW/mA
Idrive = 60e-3;
Pout = max(0, slope*(Idrive - Ith)*1e3);  % mW above threshold
```

```python
Ith, slope = 20e-3, 0.4       # threshold, slope efficiency
Idrive = 60e-3
Pout = max(0, slope*(Idrive - Ith)*1e3)   # mW above threshold
```

> **Real-world hook:** laser diodes read your data off fiber, scan barcodes,
> point in presentations, and pump the fiber amplifiers under the oceans.
> Big lasers cut steel and perform LASIK eye surgery.

**Next:** plot real optoelectronic spectra and responsivity in code.
""",
        ),
        _code(
            "Lab: blackbody, LED spectrum and photodiode responsivity",
            "13 min",
            """\
# Plot three core optoelectronic curves over wavelength:
#   1. a blackbody (thermal source) spectrum,
#   2. an LED emission spectrum (a Gaussian-ish bump),
#   3. silicon photodiode responsivity (rises with lambda, cuts off ~1100 nm).
import numpy as np
import matplotlib.pyplot as plt

h = 6.626e-34
c = 3.0e8
kB = 1.381e-23
q = 1.602e-19

lam_nm = np.linspace(300, 1200, 900)     # wavelength axis in nm
lam = lam_nm * 1e-9                       # metres

# 1. Blackbody spectral radiance (Planck's law) at T = 3000 K (a warm bulb)
T = 3000.0
planck = (2*h*c**2) / (lam**5) / (np.exp(h*c/(lam*kB*T)) - 1.0)
planck_norm = planck / planck.max()       # normalize for plotting

# 2. LED spectrum: a narrow bump centered at 630 nm (red), ~25 nm wide
led_center = 630.0
led_width = 25.0
led = np.exp(-0.5*((lam_nm - led_center)/led_width)**2)

# 3. Silicon photodiode responsivity R = eta*q*lambda/(h*c), cutoff at 1100 nm
eta = 0.85
resp = eta*q*lam/(h*c)
resp = resp * (lam_nm < 1100)             # hard cutoff past silicon's band

peak_lam = lam_nm[np.argmax(planck)]
print(f"blackbody (3000 K) peaks near {peak_lam:.0f} nm")
print(f"silicon responsivity at 850 nm = {eta*q*850e-9/(h*c):.3f} A/W")
print(f"LED centered at {led_center:.0f} nm, FWHM ~ {2.355*led_width:.0f} nm")

fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.plot(lam_nm, planck_norm, color="#f59e0b", label="blackbody 3000 K (norm.)")
ax1.plot(lam_nm, led, color="#dc2626", label="red LED spectrum")
ax1.set_xlabel("wavelength (nm)")
ax1.set_ylabel("normalized intensity")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(lam_nm, resp, color="#2563eb", lw=2, label="Si responsivity (A/W)")
ax2.set_ylabel("responsivity (A/W)")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)
plt.title("Optoelectronic spectra and detector responsivity")
plt.show()

# Try it yourself:
#   1. Raise T to 5800 K (the Sun): the blackbody peak shifts into the visible.
#   2. Move led_center to 850 nm (infrared) - past where the eye can see.
""",
        ),
    ),
)


# -- Optoelectronics & Photonics -- Intermediate -------------------------------

_PHOTONICS_INTERMEDIATE = SeedCourse(
    slug="photonics-intermediate",
    title="Optoelectronics & Photonics — Intermediate: Fibers & Optical Links",
    description=(
        "Optical fibers and full optical links: step vs graded index and modes, "
        "fiber loss and dispersion, sources and detectors for comms and the link "
        "budget, optical modulation and detection, and passive/active components "
        "(WDM, isolators, EDFAs) - with dual MATLAB/Python, interactive plots, "
        "and a runnable dispersion / link-budget lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Optical fibers: modes and numerical aperture",
            "12 min",
            """\
# Optical fibers: modes and numerical aperture

An **optical fiber** is a hair-thin glass waveguide: a high-index **core** trapping
light by total internal reflection inside a lower-index **cladding**. How that
core is shaped sets everything about the fiber.

## Step-index vs graded-index

- **Step-index:** uniform core index with an abrupt step down to the cladding.
  Rays zig-zag; different paths take different times.
- **Graded-index:** the core index decreases smoothly from center to edge, so
  rays follow gentle curves and arrive nearly together - far less spreading.

## Single-mode vs multimode

A **mode** is an allowed light path (field pattern) the fiber supports. The count
depends on core size and the **V-number**:

$$V = \\frac{2\\pi a}{\\lambda}\\,\\mathrm{NA},$$

where $a$ is the core radius. When $V < 2.405$ only **one** mode propagates -
**single-mode fiber** (tiny ~9 um core, used for long-haul). Larger cores carry
**many modes** - **multimode fiber** (50-62.5 um, cheap, short links).

## Numerical aperture

The **numerical aperture (NA)** is the light-gathering cone - how steeply light
can enter and still be guided:

$$\\mathrm{NA} = \\sqrt{n_{core}^2 - n_{clad}^2} = \\sin\\theta_{max}.$$

Slide the cladding index and watch the acceptance angle shrink as the two indices
get closer:

```plot
{"title": "Fiber acceptance angle vs cladding index (core n=1.48)", "xLabel": "cladding index n_clad", "yLabel": "acceptance angle (degrees)", "xRange": [1.4, 1.479], "yRange": [0, 30], "grid": true, "controls": [{"name": "ncore", "range": [1.46, 1.50], "value": 1.48, "label": "core index n_core"}], "functions": [{"expr": "deg(asin(sqrt(max(0, ncore^2 - x^2))))", "label": "acceptance angle"}]}
```

The number of modes in a multimode fiber grows roughly as $V^2/2$, so a larger
core or higher NA carries more modes (more light, but more spreading):

```plot
{"title": "Approx mode count vs V-number (multimode regime)", "xLabel": "V-number", "yLabel": "number of modes (approx)", "xRange": [2.405, 30], "yRange": [0, 450], "grid": true, "functions": [{"expr": "x^2/2", "label": "modes ~ V^2/2"}]}
```

```matlab
ncore = 1.48; nclad = 1.46;
NA = sqrt(ncore^2 - nclad^2);      % ~0.24
theta_max = asind(NA);             % acceptance half-angle
a = 4.5e-6; lam = 1310e-9;
V = 2*pi*a/lam*NA;                 % V-number
```

```python
import numpy as np
ncore, nclad = 1.48, 1.46
NA = np.sqrt(ncore**2 - nclad**2)  # ~0.24
theta_max = np.degrees(np.arcsin(NA))
a, lam = 4.5e-6, 1310e-9
V = 2*np.pi*a/lam*NA               # V-number
```

> **Real-world hook:** single-mode fiber carries the entire long-haul internet
> and undersea cables; cheap multimode fiber wires up data centers and buildings.
> NA also describes how much light a fiber can grab from an LED or laser.

**Next:** why a signal weakens and smears - loss and dispersion.
""",
        ),
        _t(
            "Fiber loss and dispersion",
            "12 min",
            """\
# Fiber loss and dispersion

Two effects limit how far and how fast a fiber can carry data: the signal gets
**weaker** (loss) and the pulses **smear out** (dispersion).

## Attenuation and the transmission windows

Power falls **exponentially** with distance, quoted in **dB per km**:

$$P(L) = P_0\\,10^{-\\alpha L / 10}.$$

Loss depends strongly on wavelength. Modern silica fiber has famous low-loss
**windows**, with the best around **1550 nm** (~0.2 dB/km) - which is why long-haul
systems live there. Slide the loss coefficient and see how far the signal
survives:

```plot
{"title": "Optical power vs distance (slide fiber loss)", "xLabel": "distance (km)", "yLabel": "power (fraction of input)", "xRange": [0, 100], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "alpha", "range": [0.15, 1.0], "value": 0.2, "label": "loss alpha (dB/km)"}], "functions": [{"expr": "10^(-alpha*x/10)", "label": "P(L)/P0"}]}
```

```mermaid
flowchart LR
  TX["transmitter P0"] --> F1["fiber: -0.2 dB/km"]
  F1 --> SP["splices/connectors loss"]
  SP --> RX["receiver Prx"]
```

## Dispersion: pulses spread in time

Even with plenty of power, pulses **broaden** as they travel and eventually
overlap, garbling the data. Two main kinds:

- **Modal dispersion** (multimode only): different modes take different paths and
  times. Killed by going single-mode or graded-index.
- **Chromatic dispersion:** different wavelengths travel at slightly different
  speeds, so a real (non-monochromatic) pulse spreads. Measured in
  $\\text{ps}/(\\text{nm}\\cdot\\text{km})$.

Pulse spreading grows with distance and source linewidth
($\\Delta t = D \\cdot L \\cdot \\Delta\\lambda$). Slide the dispersion parameter:

```plot
{"title": "Pulse broadening vs distance (slide chromatic dispersion D)", "xLabel": "distance (km)", "yLabel": "pulse spread (ps)", "xRange": [0, 100], "yRange": [0, 200], "grid": true, "controls": [{"name": "D", "range": [1, 20], "value": 17, "label": "D (ps/(nm*km)), dlambda=0.1 nm"}], "functions": [{"expr": "D*x*0.1", "label": "delta_t = D*L*dlambda"}]}
```

## The bandwidth-distance product

The fundamental trade-off: you can send fast *or* far, but their product is
roughly fixed. A fiber rated at $500\\ \\text{MHz}\\cdot\\text{km}$ carries 500 MHz
over 1 km, or 250 MHz over 2 km. This single number captures a fiber's
information-carrying capacity.

```matlab
alpha = 0.2; L = 80;              % dB/km, km
P_frac = 10^(-alpha*L/10);        % fraction of power surviving 80 km
D = 17; dlam = 0.1;               % ps/(nm km), source linewidth nm
spread_ps = D*L*dlam;             % pulse broadening
```

```python
alpha, L = 0.2, 80
P_frac = 10**(-alpha*L/10)        # power surviving 80 km
D, dlam = 17, 0.1
spread_ps = D*L*dlam              # pulse broadening (ps)
```

> **Real-world hook:** the 1550 nm window plus erbium amplifiers (later lesson)
> are why a single fiber crosses an ocean. Dispersion is why old multimode links
> are slow, and why long-haul uses dispersion-compensating fiber and coherent DSP.

**Next:** the lasers, diodes and detectors that drive a real link.
""",
        ),
        _t(
            "Sources and detectors for communications",
            "12 min",
            """\
# Sources and detectors for communications

A fiber link needs a **source** to launch light, a **detector** to receive it,
and a **link budget** to prove the photons make it across.

## Sources: LED vs laser diode vs DFB

| Source | Spectrum | Speed | Use |
|--------|----------|-------|-----|
| LED | broad (~50 nm) | low (Mb/s) | cheap, short multimode |
| Fabry-Perot laser | several lines | high | medium links |
| **DFB laser** | one very narrow line | very high | long-haul, DWDM |

The **DFB (distributed feedback) laser** builds a grating into the laser so it
emits a single, ultra-pure wavelength - essential when you pack dozens of
channels at different colors onto one fiber (WDM) and to fight chromatic
dispersion (a narrow source spreads less).

## Detectors: PIN vs APD

- **PIN photodiode:** simple, low-noise, needs a decent signal.
- **APD (avalanche photodiode):** a high reverse bias makes each photo-electron
  trigger an avalanche of more - **internal gain** ($M$ of 10-100x). Great for the
  faintest signals, at the cost of extra noise and a hungry bias supply.

```mermaid
flowchart LR
  DFB["DFB laser source"] --> MOD["modulated data"]
  MOD --> FIB["fiber (loss + dispersion)"]
  FIB --> DET["PIN or APD detector"]
  DET --> AMP["amplifier + decision"]
```

## The link budget

The link budget tallies every gain and loss in **dB** to check the receiver gets
enough power above its **sensitivity**:

$$P_{rx} = P_{tx} - \\alpha L - L_{conn} - L_{splice}.$$

The **margin** is $P_{rx}$ minus the receiver sensitivity - keep a few dB spare
for aging and repairs. Slide the launch power and watch where the link crosses the
sensitivity floor:

```plot
{"title": "Received power vs distance (slide launch power), sensitivity = -28 dBm", "xLabel": "distance (km)", "yLabel": "received power (dBm)", "xRange": [0, 120], "yRange": [-40, 5], "grid": true, "controls": [{"name": "Ptx", "range": [-5, 5], "value": 0, "label": "launch power Ptx (dBm)"}], "functions": [{"expr": "Ptx - 0.22*x - 2", "label": "P_rx (0.22 dB/km + 2 dB connectors)"}, {"expr": "0*x - 28", "label": "receiver sensitivity", "color": "#dc2626"}]}
```

Where the blue line drops below the red one, the link fails - that crossover sets
the maximum reach for that launch power.

```matlab
Ptx = 0; alpha = 0.22; L = 80; Lconn = 2;   % dBm, dB/km, km, dB
Prx = Ptx - alpha*L - Lconn;                 % received power dBm
margin = Prx - (-28);                        % vs -28 dBm sensitivity
```

```python
Ptx, alpha, L, Lconn = 0, 0.22, 80, 2
Prx = Ptx - alpha*L - Lconn                  # received power (dBm)
margin = Prx - (-28)                         # margin vs sensitivity
```

> **Real-world hook:** every deployed fiber link - from a data-center patch to a
> transoceanic cable - is signed off with a link budget. DFB + APD pushes
> unrepeatered spans past 100 km; add amplifiers and it spans the planet.

**Next:** how data rides on the light - modulation and detection.
""",
        ),
        _t(
            "Optical modulation and detection",
            "12 min",
            """\
# Optical modulation and detection

To send data, you **modulate** the light - vary it in step with the bits - and at
the far end **detect** and decide what was sent.

## Direct vs external modulation

- **Direct modulation:** switch the laser's drive current on and off. Simple and
  cheap, but turning a laser on/off fast smears its wavelength (**chirp**), which
  worsens dispersion - so it is limited to shorter or slower links.
- **External modulation:** run the laser steadily (clean, narrow line) and put a
  separate **modulator** (a Mach-Zehnder or electro-absorption device) in the
  beam to gate it. Low chirp, used for long-haul and high-speed.

## OOK: the simplest scheme

The basic format is **On-Off Keying (OOK)**: light on = 1, light off = 0. The
detector's photocurrent follows the optical power, $I = R \\cdot P$, where $R$ is
responsivity. Slide the bit rate and watch a square data pattern get bandwidth-
limited into a rounded signal:

```plot
{"title": "OOK data eye: ideal bits vs bandwidth-limited (slide smoothing)", "xLabel": "time (bit periods)", "yLabel": "optical power (norm.)", "xRange": [0, 8], "yRange": [-0.2, 1.3], "grid": true, "controls": [{"name": "bw", "range": [1, 8], "value": 3, "label": "receiver bandwidth (rel.)"}], "functions": [{"expr": "0.5 + 0.5*sign(sin(pi*x))", "label": "ideal bits", "color": "#94a3b8"}, {"expr": "0.5 + 0.4*sin(pi*x)*bw/(bw+1)", "label": "received (smoothed)", "color": "#2563eb"}]}
```

## Detection and noise

The receiver converts photocurrent to a voltage and compares it to a threshold.
Two fundamental noises blur the decision:

- **Shot noise:** light arrives as discrete photons, so even a steady beam has
  statistical fluctuation - it scales with the square root of the current.
- **Thermal noise:** the receiver's load resistor adds Johnson noise.

The quality metric is the **signal-to-noise ratio** and, for digital links, the
**bit error rate (BER)** and the **eye diagram** - overlay many bits and a clean,
open "eye" means easy decisions. Higher data rates need more received power to
keep the BER low.

```mermaid
flowchart LR
  LASER["CW laser"] --> MZM["Mach-Zehnder modulator"]
  DATA["electrical data"] --> MZM
  MZM --> FIB["fiber"]
  FIB --> PD["photodiode I = R*P"]
  PD --> TIA["transimpedance amp + decision"]
```

```matlab
R = 0.9; Popt = 1e-6;             % A/W, 1 uW received
Iph = R*Popt;                     % photocurrent
q = 1.602e-19; B = 10e9;          % bandwidth 10 GHz
i_shot = sqrt(2*q*Iph*B);         % shot-noise current (rms)
SNR = (Iph/i_shot)^2;
```

```python
import numpy as np
R, Popt = 0.9, 1e-6               # responsivity, received power
Iph = R*Popt                      # photocurrent
q, B = 1.602e-19, 10e9            # charge, bandwidth
i_shot = np.sqrt(2*q*Iph*B)       # shot-noise rms current
SNR = (Iph/i_shot)**2
```

> **Real-world hook:** your home fiber (GPON) uses OOK; 100G+ data-center and
> long-haul links use external modulation and advanced formats (next course).
> The eye diagram on an oscilloscope is how engineers judge a link's health.

**Next:** the passive and active glue of optical systems - components.
""",
        ),
        _t(
            "Optical components: couplers, WDM, isolators and EDFAs",
            "11 min",
            """\
# Optical components: couplers, WDM, isolators and EDFAs

Between the transmitter and receiver sits a toolbox of optical components that
split, combine, steer, protect and amplify light - all without converting it back
to electricity.

## Couplers and splitters

A **coupler** splits one fiber's light into several (or combines several into
one) - the basis of **passive optical networks (PON)** that fan one fiber out to
many homes. A 1:2 coupler nominally halves the power (a 3 dB loss each way).

## WDM: many colors, one fiber

**Wavelength-division multiplexing (WDM)** sends many independent channels at
**different wavelengths** down a single fiber, multiplying its capacity. A
multiplexer combines the colors; a demultiplexer separates them.

```mermaid
flowchart LR
  L1["laser 1550.1 nm"] --> MUX["WDM mux"]
  L2["laser 1550.9 nm"] --> MUX
  L3["laser 1551.7 nm"] --> MUX
  MUX --> FIB["one fiber, many colors"]
  FIB --> DEMUX["WDM demux"]
  DEMUX --> R1["rx 1"]
  DEMUX --> R2["rx 2"]
  DEMUX --> R3["rx 3"]
```

## Isolators and circulators

An **optical isolator** is a one-way valve for light: it passes the forward beam
and blocks reflections that would otherwise destabilize a laser. A **circulator**
routes light port-to-port in a fixed cycle, used in amplifiers and sensing.

## The EDFA: amplifying light directly

The breakthrough that made long-haul WDM practical is the **erbium-doped fiber
amplifier (EDFA)**. A length of fiber doped with erbium ions is **pumped** by a
980 or 1480 nm laser, creating a population inversion; signal photons passing
through trigger stimulated emission and are **amplified in the optical domain** -
no conversion to electricity. It boosts **all WDM channels at once** across the
1550 nm band, typically 20-30 dB of gain.

The amplified signal grows exponentially through the doped fiber until the pump
saturates. Slide the per-metre gain and watch the output build:

```plot
{"title": "EDFA signal gain along the doped fiber (slide gain coefficient)", "xLabel": "doped fiber length (m)", "yLabel": "signal power (relative)", "xRange": [0, 12], "yRange": [0, 100], "grid": true, "controls": [{"name": "g", "range": [0.1, 0.6], "value": 0.35, "label": "gain coefficient (per m)"}], "functions": [{"expr": "exp(g*x)", "label": "P(z)/P_in (small-signal)"}]}
```

```matlab
gain_dB = 25; Pin_dBm = -20;      % EDFA gain, input
Pout_dBm = Pin_dBm + gain_dB;     % +5 dBm out
NF_dB = 5;                        % typical noise figure
```

```python
gain_dB, Pin_dBm = 25, -20        # EDFA gain, input power
Pout_dBm = Pin_dBm + gain_dB      # +5 dBm
NF_dB = 5                         # typical noise figure
```

> **Real-world hook:** EDFAs spaced every ~80-100 km are why undersea cables span
> oceans without electrical repeaters; WDM + EDFA multiplies one fiber into
> terabits per second. Couplers fan PON fiber to entire neighborhoods.

**Next:** put loss, dispersion and the link budget together in code.
""",
        ),
        _code(
            "Lab: fiber pulse broadening and link budget",
            "13 min",
            """\
# Two-in-one optical-link lab:
#   A. Watch a Gaussian pulse broaden with chromatic dispersion over distance.
#   B. Compute and plot an optical link budget (power vs distance) with margin.
import numpy as np
import matplotlib.pyplot as plt

# ---- Part A: pulse broadening from chromatic dispersion ----
D = 17.0                       # ps/(nm*km), standard SMF at 1550 nm
dlam = 0.1                     # source spectral width (nm)
t0 = 25.0                      # initial pulse half-width (ps)
t = np.linspace(-200, 200, 600)

distances = [0.0, 30.0, 60.0, 100.0]   # km
fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 4.2))
for L in distances:
    spread = D * L * dlam                # extra width from dispersion (ps)
    width = np.sqrt(t0**2 + spread**2)   # broadened pulse width
    pulse = np.exp(-(t**2)/(2*width**2))
    axA.plot(t, pulse, label=f"{L:.0f} km (width {width:.0f} ps)")
axA.set_xlabel("time (ps)"); axA.set_ylabel("amplitude")
axA.set_title("Chromatic dispersion broadens the pulse")
axA.legend(fontsize=8); axA.grid(True)

# ---- Part B: link budget ----
Ptx = 3.0                      # launch power (dBm)
alpha = 0.22                   # fiber loss (dB/km)
conn = 2.0                     # total connector/splice loss (dB)
sens = -28.0                   # receiver sensitivity (dBm)

L_km = np.linspace(0, 140, 400)
Prx = Ptx - alpha*L_km - conn               # received power along the link
reach = (Ptx - conn - sens) / alpha         # distance where Prx == sensitivity

axB.plot(L_km, Prx, color="#2563eb", lw=2, label="received power")
axB.axhline(sens, color="#dc2626", ls="--", label=f"sensitivity {sens:.0f} dBm")
axB.axvline(reach, color="#16a34a", ls=":", label=f"max reach {reach:.0f} km")
axB.set_xlabel("distance (km)"); axB.set_ylabel("power (dBm)")
axB.set_title("Optical link budget")
axB.legend(fontsize=8); axB.grid(True)

plt.tight_layout(); plt.show()

print(f"dispersion-limited width at 100 km: {np.sqrt(t0**2 + (D*100*dlam)**2):.0f} ps")
print(f"link budget max reach: {reach:.1f} km (Ptx={Ptx} dBm, sens={sens} dBm)")

# Try it yourself:
#   1. Set alpha = 0.2 and add an EDFA: bump Ptx by +20 to model amplified spans.
#   2. Lower dlam to 0.01 nm (a DFB laser): dispersion broadening nearly vanishes.
""",
        ),
    ),
)


# -- Optoelectronics & Photonics -- Advanced -----------------------------------

_PHOTONICS_ADVANCED = SeedCourse(
    slug="photonics-advanced",
    title="Optoelectronics & Photonics — Advanced: Photonic Systems & Integration",
    description=(
        "Photonic systems and integration: coherent optics and QAM on light, DWDM "
        "and optical networking, silicon photonics and ring resonators, solar "
        "cells and the IV curve, and emerging photonics (LiDAR, sensing, photonic/"
        "quantum computing) - with dual MATLAB/Python, interactive plots, and a "
        "runnable ring-resonator / solar-cell lab, closing on real applications."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Advanced modulation and coherent optics",
            "13 min",
            """\
# Advanced modulation and coherent optics

On-off keying wastes most of light's information capacity. Modern high-speed
links encode bits in the **amplitude AND phase** of the optical carrier and
recover them with **coherent detection** plus digital signal processing - exactly
the techniques that built wireless and now run optical backbones.

## QAM on light

**Quadrature amplitude modulation (QAM)** places symbols on a 2D
**constellation** of in-phase ($I$) and quadrature ($Q$) components. Each point is
several bits: QPSK carries 2 bits/symbol, 16-QAM carries 4, 64-QAM carries 6.
Light has two independent **polarizations**, so polarization-multiplexed QAM
doubles it again. A 16-QAM constellation is a 4x4 grid of symbols:

```plot
{"title": "16-QAM constellation (each point = 4 bits)", "xLabel": "in-phase I", "yLabel": "quadrature Q", "xRange": [-4, 4], "yRange": [-4, 4], "grid": true, "points": [{"x": -3, "y": -3, "color": "#2563eb", "size": 7}, {"x": -3, "y": -1, "color": "#2563eb", "size": 7}, {"x": -3, "y": 1, "color": "#2563eb", "size": 7}, {"x": -3, "y": 3, "color": "#2563eb", "size": 7}, {"x": -1, "y": -3, "color": "#2563eb", "size": 7}, {"x": -1, "y": -1, "color": "#2563eb", "size": 7}, {"x": -1, "y": 1, "color": "#2563eb", "size": 7}, {"x": -1, "y": 3, "color": "#2563eb", "size": 7}, {"x": 1, "y": -3, "color": "#2563eb", "size": 7}, {"x": 1, "y": -1, "color": "#2563eb", "size": 7}, {"x": 1, "y": 1, "color": "#2563eb", "size": 7}, {"x": 1, "y": 3, "color": "#2563eb", "size": 7}, {"x": 3, "y": -3, "color": "#2563eb", "size": 7}, {"x": 3, "y": -1, "color": "#2563eb", "size": 7}, {"x": 3, "y": 1, "color": "#2563eb", "size": 7}, {"x": 3, "y": 3, "color": "#2563eb", "size": 7}]}
```

## Coherent detection

Instead of just measuring power, a **coherent receiver** mixes the incoming light
with a **local-oscillator laser**. The beat between them recovers both amplitude
and phase (the full $I$ and $Q$), giving far more sensitivity and information than
direct detection. Press Play to trace the optical carrier whose phase carries one
symbol:

```plot
{"title": "Phase-modulated optical carrier (animated): a symbol's phase", "xLabel": "time", "yLabel": "field amplitude", "xRange": [0, 12], "yRange": [-1.3, 1.3], "grid": true, "controls": [{"name": "phi", "range": [0, 6.2832], "value": 1.5, "label": "symbol phase phi (rad)"}], "animate": {"param": "t", "range": [0, 12], "label": "time"}, "functions": [{"expr": "cos(3*x + phi)", "label": "E(t) = cos(wt + phi)"}], "points": [{"xExpr": "t", "yExpr": "cos(3*t + phi)", "label": "now", "color": "#dc2626", "size": 6, "trail": true}]}
```

## DSP cleans up the rest

Once digitized, **DSP** undoes the impairments that used to need exotic optics:
it compensates **chromatic and polarization-mode dispersion**, tracks laser phase
noise, and equalizes the channel - all in software. This is why a single fiber
now carries hundreds of gigabits per wavelength.

```matlab
bits_per_symbol = log2(16);       % 16-QAM -> 4 bits/symbol
symbol_rate = 64e9;               % 64 Gbaud
pol = 2;                          % two polarizations
rate = bits_per_symbol*symbol_rate*pol;   % ~512 Gb/s per wavelength
```

```python
import numpy as np
bits_per_symbol = np.log2(16)     # 16-QAM
symbol_rate = 64e9                # 64 Gbaud
pol = 2                           # two polarizations
rate = bits_per_symbol*symbol_rate*pol    # ~512 Gb/s per wavelength
```

> **Real-world hook:** every modern long-haul and subsea cable uses coherent
> QAM with DSP - the same constellation math as 5G and Wi-Fi, but on light.
> Upgrading a route is now often a transceiver swap, not new fiber.

**Next:** packing many such channels and switching them - optical networking.
""",
        ),
        _t(
            "WDM and optical networking",
            "12 min",
            """\
# WDM and optical networking

A single coherent channel is powerful; an optical **network** runs dozens of them
on one fiber and switches them across continents - all in the optical domain.

## DWDM: dense channels on a grid

**Dense WDM (DWDM)** packs ~40-96 wavelengths onto one fiber on a standard
frequency grid (e.g. 50 GHz spacing around 1550 nm). Each carries a full coherent
channel, so one fiber moves **tens of terabits per second**. The colors share
amplifiers (EDFAs) and fiber, multiplying capacity without laying new glass.

```plot
{"title": "DWDM channels on the 50 GHz grid (each peak = one wavelength)", "xLabel": "relative frequency (x50 GHz from grid start)", "yLabel": "channel power (norm.)", "xRange": [0, 8], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "exp(-30*(x-1)^2) + exp(-30*(x-2)^2) + exp(-30*(x-3)^2) + exp(-30*(x-4)^2) + exp(-30*(x-5)^2) + exp(-30*(x-6)^2) + exp(-30*(x-7)^2)", "label": "DWDM comb"}]}
```

## ROADMs: switching colors without electronics

A **reconfigurable optical add-drop multiplexer (ROADM)** lets a node **add**,
**drop**, or **pass through** individual wavelengths under software control,
without converting them to electrical signals. Built from **wavelength-selective
switches**, ROADMs turn point-to-point links into a flexible mesh - operators
re-route a wavelength remotely instead of sending a technician.

```mermaid
flowchart LR
  WEST["west fiber (many colors)"] --> ROADM["ROADM (WSS)"]
  EAST["east fiber (many colors)"] --> ROADM
  ROADM --> THRU["express through-traffic"]
  ROADM --> DROP["drop local wavelengths"]
  ADD["add local wavelengths"] --> ROADM
```

## The optical transport network

Carriers organize all this as the **optical transport network (OTN)**: a layered
hierarchy that wraps client signals (Ethernet, IP) into standardized optical
containers with forward error correction and performance monitoring. The **GMPLS**
control plane and modern SDN controllers provision and protect wavelength paths
end to end.

A channel's reach before it needs regeneration depends on accumulated noise; the
**OSNR** (optical signal-to-noise ratio) degrades as it passes more amplifiers:

```plot
{"title": "OSNR degrades along an amplified DWDM chain (slide span loss)", "xLabel": "number of amplified spans", "yLabel": "OSNR (dB)", "xRange": [1, 40], "yRange": [10, 45], "grid": true, "controls": [{"name": "NF", "range": [4, 8], "value": 5, "label": "amplifier noise figure (dB)"}], "functions": [{"expr": "58 - NF - 10*log10(x) - 16.8", "label": "OSNR after N spans"}]}
```

```matlab
channels = 80; per_ch_Gbps = 400;
capacity_Tbps = channels*per_ch_Gbps/1000;   % 32 Tbps on one fiber
osnr_dB = 58 - 5 - 10*log10(20) - 16.8;       % after 20 spans
```

```python
import numpy as np
channels, per_ch_Gbps = 80, 400
capacity_Tbps = channels*per_ch_Gbps/1000     # 32 Tbps
osnr_dB = 58 - 5 - 10*np.log10(20) - 16.8      # after 20 spans
```

> **Real-world hook:** DWDM + ROADMs are the physical internet backbone and
> cloud-provider inter-data-center links. When you stream a video, your bits ride
> one wavelength through ROADM-switched mesh networks across the country.

**Next:** shrinking all of this onto a chip - integrated photonics.
""",
        ),
        _t(
            "Integrated photonics and silicon photonics",
            "13 min",
            """\
# Integrated photonics and silicon photonics

Just as electronics moved from discrete transistors to integrated circuits,
photonics is moving onto **chips**. **Photonic integrated circuits (PICs)** route
and process light in micron-scale **waveguides** etched into a substrate.

## Silicon photonics

**Silicon photonics** builds optical circuits in the same CMOS foundries that make
processors. Silicon's high index ($n \\approx 3.5$) confines light tightly, so
waveguides and devices shrink to microns - and you get optics and electronics on
one wafer at scale. (Silicon cannot emit light efficiently, so lasers are bonded
on from III-V materials, but everything else integrates.)

## On-chip building blocks

| Device | Made from | Does |
|--------|-----------|------|
| Waveguide | etched silicon strip | route light on chip |
| Directional coupler | two close waveguides | split/combine |
| **Ring resonator** | looped waveguide | wavelength filter, modulator, sensor |
| Mach-Zehnder modulator | split-phase-recombine | encode data |
| Grating coupler | periodic etch | get light on/off the chip |

## The ring resonator

A **ring resonator** is a loop of waveguide coupled to a straight bus. Wavelengths
whose round-trip equals a whole number of wavelengths build up **resonance** and
are dropped from the bus, producing sharp periodic notches in transmission. Their
spacing is the **free spectral range (FSR)**. Slide the coupling and watch the
notches deepen:

```plot
{"title": "Ring resonator transmission (slide coupling depth)", "xLabel": "detuning (round-trip phase, rad)", "yLabel": "bus transmission", "xRange": [0, 12.566], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "k", "range": [0.1, 0.95], "value": 0.6, "label": "coupling depth"}], "functions": [{"expr": "1 - k/(1 + 8*sin(x/2)^2)", "label": "transmission notches"}]}
```

A heater or a charge-injection junction shifts the ring's index, moving the
resonance - that is a compact, low-power **modulator** or **tunable filter**. Its
through-port transmission swings as you tune it:

```plot
{"title": "Ring modulator: transmission shifts as you tune the resonance", "xLabel": "wavelength detuning (a.u.)", "yLabel": "transmission", "xRange": [-3, 3], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "shift", "range": [-2, 2], "value": 0, "label": "applied tuning (volts -> shift)"}], "functions": [{"expr": "1 - 0.9/(1 + 9*(x - shift)^2)", "label": "through-port"}]}
```

```mermaid
flowchart LR
  IN["bus input"] --> COUP["coupling region"]
  COUP --> RING["ring (resonant loop)"]
  RING --> COUP
  COUP --> OUT["bus output (notched)"]
```

```matlab
n_eff = 2.4; R_um = 10;           % effective index, ring radius (um)
L = 2*pi*R_um*1e-6;               % round-trip length
lam = 1550e-9;
FSR = lam^2/(n_eff*L);            % free spectral range (m)
```

```python
import numpy as np
n_eff, R_um = 2.4, 10             # eff. index, radius (um)
L = 2*np.pi*R_um*1e-6             # round-trip length (m)
lam = 1550e-9
FSR = lam**2/(n_eff*L)            # free spectral range (m)
```

> **Real-world hook:** silicon-photonic transceivers move data inside data centers
> and between AI accelerators; co-packaged optics put fiber right next to the
> switch chip. Ring resonators also make ultra-sensitive biosensors.

**Next:** light into electricity at scale - solar cells.
""",
        ),
        _t(
            "Solar cells and energy harvesting",
            "12 min",
            """\
# Solar cells and energy harvesting

A **solar cell** is a large photodiode optimized to turn sunlight into power -
the **photovoltaic effect**. Photons with energy above the bandgap create
electron-hole pairs that the junction separates into a voltage and current.

## The IV curve

A solar cell's current-voltage curve is a diode curve shifted down by the
light-generated current $I_L$:

$$I = I_L - I_s\\left(e^{V/V_T} - 1\\right).$$

Power $P = VI$ is zero at both ends (short circuit: $V=0$; open circuit:
$I=0$) and peaks in between at the **maximum power point (MPP)**. Slide the
illumination and watch the whole curve scale - more sun, more current:

```plot
{"title": "Solar cell I-V curve (slide illumination)", "xLabel": "voltage (V)", "yLabel": "current (A)", "xRange": [0, 0.65], "yRange": [0, 6], "grid": true, "controls": [{"name": "sun", "range": [0.2, 1.2], "value": 1.0, "label": "illumination (suns)"}], "functions": [{"expr": "max(0, 5*sun - 0.0000001*exp(x/0.026))", "label": "I(V)"}]}
```

The corresponding power curve makes the maximum power point obvious - it bulges
to a peak then collapses as the diode turns on:

```plot
{"title": "Solar cell power vs voltage: the maximum power point", "xLabel": "voltage (V)", "yLabel": "power (W)", "xRange": [0, 0.65], "yRange": [0, 2.5], "grid": true, "functions": [{"expr": "x*max(0, 5 - 0.0000001*exp(x/0.026))", "label": "P = V*I"}]}
```

## Efficiency and its limits

Key figures of merit:

- **Open-circuit voltage** $V_{oc}$ and **short-circuit current** $I_{sc}$.
- **Fill factor** $FF = \\dfrac{V_{mp} I_{mp}}{V_{oc} I_{sc}}$ - how "square" the
  curve is.
- **Efficiency** $\\eta = \\dfrac{P_{max}}{P_{sunlight}}$.

A single-junction silicon cell is capped near the **Shockley-Queisser limit**
(~33%) because low-energy photons are not absorbed and high-energy ones waste
their excess as heat. Real silicon panels reach ~20-22%. **Multi-junction** cells
stack different bandgaps to grab more of the spectrum and exceed 45% under
concentrated light.

## Energy harvesting and MPP tracking

Because the MPP moves with sun and temperature, panels use a **maximum power point
tracker (MPPT)** - a switching converter (from the power-electronics track) that
continuously loads the panel at its sweet spot. The same photovoltaic idea, scaled
down, harvests indoor light to run sensors and IoT nodes battery-free.

```matlab
IL = 5; Is = 1e-9; Vt = 0.026;    % photocurrent, sat. current, thermal V
V = linspace(0, 0.6, 200);
I = IL - Is*(exp(V/Vt) - 1);
P = V.*I;  [Pmax, k] = max(P);    % maximum power point
```

```python
import numpy as np
IL, Is, Vt = 5, 1e-9, 0.026
V = np.linspace(0, 0.6, 200)
I = IL - Is*(np.exp(V/Vt) - 1)
P = V*I
Pmax = P.max()                    # maximum power point
```

> **Real-world hook:** rooftop and utility solar, satellite power, solar-powered
> calculators, and self-powered IoT sensors all ride this IV curve. MPPT inverters
> squeeze every watt; multi-junction cells power Mars rovers and concentrators.

**Next:** where photonics is heading - emerging technologies.
""",
        ),
        _t(
            "Emerging photonics: LiDAR, sensing and quantum",
            "12 min",
            """\
# Emerging photonics: LiDAR, sensing and quantum

Beyond communications and power, light is becoming a universal sensor and even a
computing medium. Three frontiers stand out.

## LiDAR: seeing with light

**LiDAR (Light Detection and Ranging)** fires laser pulses and times the echo to
build a 3D point cloud. The range follows the simplest physics in photonics:

$$d = \\frac{c\\,\\Delta t}{2}.$$

Time-of-flight LiDAR resolves distance to centimetres; **FMCW LiDAR** (frequency-
modulated continuous wave, borrowed from coherent optics) also measures velocity
via Doppler. Slide the target distance and watch the round-trip time grow:

```plot
{"title": "LiDAR round-trip time vs distance (light travels 0.3 m/ns)", "xLabel": "target distance (m)", "yLabel": "round-trip time (ns)", "xRange": [0, 200], "yRange": [0, 1400], "grid": true, "controls": [{"name": "d", "range": [10, 200], "value": 100, "label": "target distance (m)"}], "functions": [{"expr": "2*x/0.3", "label": "round-trip time"}], "points": [{"xExpr": "d", "yExpr": "2*d/0.3", "label": "selected", "color": "#dc2626", "size": 7}]}
```

LiDAR guides self-driving cars and drones, maps terrain from aircraft, and the
small ToF sensor in your phone autofocuses the camera and powers face unlock.

## Optical sensing

Light is an exquisite probe because its wavelength and phase shift with tiny
changes in the environment:

- **Fiber-optic sensors** measure temperature, strain, and pressure along a whole
  cable - structural health of bridges, pipelines, and oil wells.
- **Interferometers** detect sub-wavelength displacement; LIGO used kilometre-scale
  ones to detect gravitational waves.
- **Spectroscopy** identifies gases and materials by the wavelengths they absorb -
  pulse oximeters, breath analyzers, environmental monitors.

```mermaid
flowchart LR
  LASER["laser"] --> SPLIT["beam splitter"]
  SPLIT --> REF["reference arm"]
  SPLIT --> SENSE["sensing arm (sees the world)"]
  REF --> COMB["recombine -> interference"]
  SENSE --> COMB
  COMB --> DET["detector reads phase shift"]
```

## Photonic and quantum computing

- **Photonic computing:** light does matrix multiplication by interference -
  fast, parallel, low-energy - attractive for AI accelerators and on-chip optical
  neural networks.
- **Quantum photonics:** single photons make excellent **qubits** that travel at
  light speed and barely decohere, powering **quantum key distribution** (provably
  secure communication) and one leading approach to quantum computing.

```matlab
c = 3e8; t_round = 666e-9;        % measured round-trip time
distance = c*t_round/2;           % ~100 m
```

```python
c, t_round = 3e8, 666e-9          # speed, round-trip time
distance = c*t_round/2            # ~100 m
```

> **Real-world hook:** LiDAR sits on robotaxis and iPhones; fiber sensors watch
> oil wells and bridges; quantum key distribution already secures some banking and
> government links over fiber. Photonic AI chips are an active commercial race.

**Next:** simulate a ring resonator and a solar cell in code.
""",
        ),
        _code(
            "Lab: ring-resonator response and solar-cell IV curve",
            "14 min",
            """\
# Two photonic-systems simulations side by side:
#   A. A microring resonator's through-port transmission vs wavelength.
#   B. A solar cell's I-V and P-V curves, finding the maximum power point.
import numpy as np
import matplotlib.pyplot as plt

# ---- Part A: ring resonator through-port transmission ----
# All-pass ring: T = (a^2 - 2 a r cos(phi) + r^2) / (1 - 2 a r cos(phi) + (a r)^2)
r = 0.90                       # self-coupling coefficient
a = 0.95                       # round-trip amplitude transmission (loss)
phi = np.linspace(0, 6*np.pi, 1200)   # round-trip phase (sweeps wavelength)
num = a**2 - 2*a*r*np.cos(phi) + r**2
den = 1 - 2*a*r*np.cos(phi) + (a*r)**2
T = num/den                    # through-port transmission

# ---- Part B: solar cell I-V and P-V ----
IL = 5.0                       # light-generated current (A)
Is = 1e-9                      # diode saturation current (A)
Vt = 0.026                     # thermal voltage (V)
V = np.linspace(0, 0.62, 500)
I = IL - Is*(np.exp(V/Vt) - 1.0)
I = np.clip(I, 0, None)        # ignore the negative tail past Voc
P = V*I
imp = np.argmax(P)             # index of the maximum power point
Vmp, Imp, Pmax = V[imp], I[imp], P[imp]
Voc = V[np.argmin(np.abs(I))]  # open-circuit voltage (where I ~ 0)
FF = Pmax/(Voc*IL)             # fill factor (Isc ~ IL)

print(f"ring: min transmission {T.min():.3f} at resonance (notch depth)")
print(f"solar MPP: Vmp={Vmp:.3f} V, Imp={Imp:.2f} A, Pmax={Pmax:.2f} W")
print(f"solar: Voc~{Voc:.3f} V, fill factor FF~{FF:.2f}")

fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 4.2))
axA.plot(phi/np.pi, T, color="#7c3aed")
axA.set_xlabel("round-trip phase (units of pi)")
axA.set_ylabel("through-port transmission")
axA.set_title("Microring resonator notches")
axA.grid(True)

axB.plot(V, I, color="#2563eb", label="I-V")
axB.plot(V, P, color="#f59e0b", label="P-V")
axB.scatter([Vmp], [Pmax], color="#dc2626", zorder=5, label="max power point")
axB.set_xlabel("voltage (V)"); axB.set_ylabel("current (A) / power (W)")
axB.set_title("Solar cell I-V and P-V")
axB.legend(fontsize=8); axB.grid(True)

plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Raise a toward 1.0 (lower loss): ring notches get sharper (higher Q).
#   2. Double IL (more sun): the MPP power roughly doubles, Voc barely moves.
""",
        ),
        _t(
            "Applications and the photonics throughline",
            "11 min",
            """\
# Applications and the photonics throughline

Every idea in this track converges on real systems that run the modern world.
This final lesson ties them together through where photonics actually lives.

## The photonic value chain

```mermaid
flowchart LR
  GEN["generate: LED / laser diode"] --> GUIDE["guide: fiber / waveguide"]
  GUIDE --> MOD["modulate: MZM / ring / coherent QAM"]
  MOD --> NET["network: WDM / ROADM / OTN"]
  NET --> DET["detect: PIN / APD / coherent + DSP"]
  DET --> USE["use: data, sensing, energy"]
```

## Where photonics powers the world today

| Domain | Photonics inside | Lessons it draws on |
|--------|------------------|---------------------|
| **Internet backbone** | DFB lasers, coherent QAM, DWDM, EDFAs, ROADMs | sources, coherent optics, networking |
| **Data centers / AI** | silicon-photonic transceivers, co-packaged optics | integrated photonics, modulation |
| **Lighting & displays** | LEDs, micro-LED, laser projectors | electroluminescence, color/bandgap |
| **Imaging & cameras** | photodiode arrays, infrared sensors | photodetectors, responsivity |
| **Autonomy** | LiDAR, time-of-flight sensors | lasers, emerging photonics |
| **Energy** | solar cells, MPPT, concentrators | photovoltaics, the IV curve |
| **Sensing & medicine** | fiber sensors, pulse oximeters, OCT, LASIK | optical sensing, lasers |
| **Security** | quantum key distribution | quantum photonics |

## A worked perspective: streaming a video

Tap play and your request crosses the planet on **light**: a DFB laser launches a
coherent QAM channel, one of ~80 DWDM colors on a fiber boosted by EDFAs every
~80 km, switched through ROADMs, dropped into a data center over silicon-photonic
links, where a coherent receiver and DSP recover the bits - all in milliseconds.
The screen you watch on is lit by **LEDs**, and the sensor that filmed it was an
array of **photodiodes**.

## The throughline

Light is a wave and a stream of photons; bend and trap it with refractive index
and total internal reflection; create it with electroluminescence and stimulated
emission; detect it with the photoelectric effect; carry data on its amplitude,
phase and color; amplify and switch it without ever leaving the optical domain;
and harvest it for power. The wavelengths and devices change with the application,
but the physics - $c = \\lambda f$, $E = hf$, Snell, and gain above threshold -
never does.

```matlab
% A back-of-envelope capacity of one modern fiber:
channels = 96; rate_per_ch_Gbps = 400;
total_Tbps = channels*rate_per_ch_Gbps/1000;   % ~38 Tbps on one strand of glass
```

```python
channels, rate_per_ch_Gbps = 96, 400
total_Tbps = channels*rate_per_ch_Gbps/1000     # ~38 Tbps on one fiber
```

> **Real-world hook:** the device you are reading this on used photonics at every
> layer - the fiber that delivered it, the LEDs lighting the screen, and the
> photodiodes in its camera. Photonics is the quiet infrastructure of the digital
> age, and the next decade pushes it into computing itself.

**Next:** the final check.
""",
        ),
    ),
)


PHOTONICS_COURSES: tuple[SeedCourse, ...] = (
    _PHOTONICS_BASICS,
    _PHOTONICS_INTERMEDIATE,
    _PHOTONICS_ADVANCED,
)

__all__ = ["PHOTONICS_COURSES"]
