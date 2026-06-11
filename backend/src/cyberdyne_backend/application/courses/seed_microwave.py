"""Curated Antennas & Microwave Engineering track: Basics, Intermediate, Advanced.

A complete RF/microwave curriculum: transmission lines and the Smith chart,
impedance matching, waveguides and resonators, materials and components
(Basics); S-parameters and network analysis, microwave components, antenna
fundamentals, the dipole/monopole, and the Friis link budget (Intermediate);
antenna arrays and beamforming, aperture/specialized antennas, microwave
amplifiers and oscillators, the RF front-end, and mmWave/5G/radar (Advanced).
Dual MATLAB + Python focus throughout, with runnable Python labs (numpy +
matplotlib), interactive ```plot blocks, Mermaid diagrams, LaTeX formulas, and
real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Antennas & Microwave Engineering -- Basics --------------------------------

_MICROWAVE_BASICS = SeedCourse(
    slug="microwave-basics",
    title="Antennas & Microwave Engineering -- Basics",
    description=(
        "RF and microwave foundations: transmission lines and the telegrapher "
        "equations, characteristic impedance, reflection and VSWR, the Smith "
        "chart, impedance matching (quarter-wave, stubs, L-networks), waveguides "
        "and resonators, and microwave materials and components - with "
        "side-by-side MATLAB and Python, interactive plots, and a runnable "
        "reflection/VSWR lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Transmission lines: telegrapher equations, Z0, reflection & VSWR",
            "13 min",
            """\
# Transmission lines: telegrapher equations, Z0, reflection & VSWR

At low frequency a wire is just a wire. But when the signal **wavelength**
becomes comparable to the wire length, voltage and current vary *along* the line
and the wire becomes a **transmission line** - the central object of microwave
engineering. The rule of thumb: treat a line as "long" once it exceeds about
$\\lambda/10$. At 2.4 GHz, $\\lambda \\approx 12.5$ cm, so even a few centimeters
of trace matters.

## The telegrapher equations

Model the line as a ladder of tiny series inductance $L$ and resistance $R$ with
shunt capacitance $C$ and conductance $G$ per unit length. Kirchhoff on an
infinitesimal segment gives the **telegrapher equations**:

$$\\frac{\\partial v}{\\partial z} = -L\\,\\frac{\\partial i}{\\partial t} - R\\,i,
\\qquad
\\frac{\\partial i}{\\partial z} = -C\\,\\frac{\\partial v}{\\partial t} - G\\,v.$$

For a **lossless** line ($R = G = 0$) these combine into the wave equation:
signals propagate at $v_p = 1/\\sqrt{LC}$ in both directions.

## Characteristic impedance Z0

A wave traveling down the line sees a fixed ratio of voltage to current, the
**characteristic impedance**:

$$Z_0 = \\sqrt{\\frac{R + j\\omega L}{G + j\\omega C}} \\;\\xrightarrow{\\text{lossless}}\\;
\\sqrt{\\frac{L}{C}}.$$

This is why coax comes in **50 ohm** (power-handling compromise) and **75 ohm**
(low-loss, used for TV/video) flavors.

## Reflection coefficient and VSWR

Terminate the line in a load $Z_L$. Unless $Z_L = Z_0$, part of the wave
**reflects** back. The **reflection coefficient** at the load is

$$\\Gamma = \\frac{Z_L - Z_0}{Z_L + Z_0}, \\qquad |\\Gamma| \\le 1.$$

The forward and reflected waves interfere to make a **standing wave**, whose
peak-to-trough ratio is the **voltage standing-wave ratio**:

$$\\text{VSWR} = \\frac{1 + |\\Gamma|}{1 - |\\Gamma|}.$$

A perfect match has $\\Gamma = 0$, VSWR $= 1$. Slide the load resistance and watch
VSWR blow up as it departs from 50 ohm:

```plot
{"title": "VSWR vs load resistance on a 50 ohm line (slide Z0)", "xLabel": "load resistance RL (ohm)", "yLabel": "VSWR", "xRange": [1, 300], "yRange": [1, 10], "grid": true, "controls": [{"name": "Z0", "range": [25, 100], "value": 50, "label": "line impedance Z0 (ohm)"}], "functions": [{"expr": "(1 + abs((x-Z0)/(x+Z0)))/(1 - abs((x-Z0)/(x+Z0)))", "label": "VSWR"}]}
```

## Real applications

- **Coaxial cable** feeding an antenna: a bad match wastes transmit power and can
  damage the power amplifier.
- **PCB microstrip** routing a 5 GHz Wi-Fi signal across a board.
- **Cable TV** distribution on 75 ohm coax.

```matlab
Z0 = 50; ZL = 75;
Gamma = (ZL - Z0)/(ZL + Z0);          % 0.2
VSWR  = (1 + abs(Gamma))/(1 - abs(Gamma));  % 1.5
RL_dB = -20*log10(abs(Gamma));        % return loss ~ 14 dB
```

```python
import numpy as np
Z0, ZL = 50, 75
Gamma = (ZL - Z0)/(ZL + Z0)           # 0.2
VSWR = (1 + abs(Gamma))/(1 - abs(Gamma))   # 1.5
RL_dB = -20*np.log10(abs(Gamma))      # return loss ~ 14 dB
```

> **Practical insight:** the load impedance also **rotates** as you move down the
> line; what the source sees depends on line length. That rotation is exactly
> what the Smith chart visualizes - the next lesson.

**Next:** the Smith chart - the RF engineer's slide rule.
""",
        ),
        _t(
            "The Smith chart: impedance, admittance & plotting Gamma",
            "12 min",
            """\
# The Smith chart: impedance, admittance & plotting Gamma

The **Smith chart** is the most iconic tool in RF engineering: a clever map that
turns the messy algebra of complex impedance and reflection into geometry you can
read by eye. It plots the **reflection coefficient** $\\Gamma$ inside the unit
circle, and overlays a grid of constant-resistance and constant-reactance curves.

## The mapping

Normalize the load to the line impedance, $z = Z_L/Z_0 = r + jx$. The chart maps

$$\\Gamma = \\frac{z - 1}{z + 1}$$

into the unit disk $|\\Gamma| \\le 1$. Key landmarks:

- **Center** ($\\Gamma = 0$): a perfect match, $z = 1$ (i.e. $Z_L = Z_0$).
- **Far right** ($\\Gamma = +1$): open circuit, $z = \\infty$.
- **Far left** ($\\Gamma = -1$): short circuit, $z = 0$.
- The **outer circle** ($|\\Gamma| = 1$) is pure reactance - total reflection.

The unit circle on which a matched load sits and the constant-$|\\Gamma|$ (VSWR)
circle you rotate around:

```plot
{"title": "Smith chart: the unit reflection circle and a VSWR=2 circle", "xLabel": "Re(Gamma)", "yLabel": "Im(Gamma)", "xRange": [-1.2, 1.2], "yRange": [-1.2, 1.2], "grid": true, "parametric": [{"x": "cos(t)", "y": "sin(t)", "range": [0, 6.2832], "label": "|Gamma|=1 (outer rim)", "color": "#94a3b8"}, {"x": "0.3333*cos(t)", "y": "0.3333*sin(t)", "range": [0, 6.2832], "label": "VSWR=2 circle", "color": "#2563eb"}]}
```

## Navigating the chart

- **Moving toward the generator** (down the line, away from the load) rotates the
  point **clockwise** on a constant-$|\\Gamma|$ circle. A half wavelength
  ($\\lambda/2$) is one full revolution.
- **Adding series reactance** moves you along constant-resistance circles.
- **Adding shunt elements** is easier on the **admittance** ($y = 1/z$) version of
  the chart, which is the impedance chart rotated 180 degrees.

The combined impedance/admittance chart lets you design matching networks by
hopping between constant-R and constant-G circles - the next lesson.

```mermaid
flowchart LR
  ZL["load z = r + jx"] --> MAP["map Gamma = (z-1)/(z+1)"]
  MAP --> PLOT["plot inside unit circle"]
  PLOT --> ROT["rotate clockwise = move toward source"]
```

## Real applications

- **VNA displays** plot measured $S_{11}$ directly on a Smith chart so you see at
  a glance whether a device is matched.
- **Antenna tuning**: watch the marker spiral toward center as you trim a matching
  network.

```matlab
Z0 = 50; ZL = 30 + 40j;
z = ZL/Z0;
Gamma = (z - 1)/(z + 1);          % plot this point on the chart
VSWR = (1+abs(Gamma))/(1-abs(Gamma));
```

```python
import numpy as np
Z0, ZL = 50, 30 + 40j
z = ZL/Z0
Gamma = (z - 1)/(z + 1)           # plot on the chart
VSWR = (1+abs(Gamma))/(1-abs(Gamma))
```

> **Practical insight:** even with modern software, engineers think in Smith-chart
> moves - "add a shunt cap to slide along this G circle, then a series inductor up
> to center." It encodes the physics of matching in pure geometry.

**Next:** actually matching the load - quarter-wave, stubs, and L-networks.
""",
        ),
        _t(
            "Impedance matching: quarter-wave, stub & L-networks",
            "13 min",
            """\
# Impedance matching: quarter-wave, stub & L-networks

**Matching** means inserting a lossless network between source and load so the
source sees its own $Z_0$ - no reflection, maximum power transfer, no standing
wave to stress the amplifier. Three classic techniques cover most cases.

## 1. The quarter-wave transformer

A line of length $\\lambda/4$ acts as an impedance inverter. To match a real load
$R_L$ to $Z_0$, insert a quarter-wave section whose impedance is the **geometric
mean**:

$$Z_1 = \\sqrt{Z_0\\,R_L}.$$

To match a 100 ohm load to a 50 ohm line you need a 70.7 ohm quarter-wave line.
The catch: it is only exact at one frequency (and odd harmonics), so its
bandwidth is limited. The match degrades as you move off the design frequency:

```plot
{"title": "Quarter-wave transformer: |Gamma| vs frequency (slide load RL)", "xLabel": "frequency / f0", "yLabel": "|Gamma| at input", "xRange": [0.3, 1.7], "yRange": [0, 0.5], "grid": true, "controls": [{"name": "RL", "range": [60, 200], "value": 100, "label": "load RL (ohm), Z0=50"}], "functions": [{"expr": "abs((RL-50)/(RL+50)) * abs(cos(pi/2*x)) / sqrt(1 - (1-(RL-50)*(RL-50)/((RL+50)*(RL+50)))*sin(pi/2*x)*sin(pi/2*x))", "label": "|Gamma(f)|"}]}
```

## 2. Stub matching

A **stub** is a short open- or short-circuited line stub placed in shunt (or
series). Because a shorted/open stub presents a pure reactance that varies with
its length, you can dial in exactly the susceptance needed to cancel the load and
land on the chart center. A **single-stub tuner** has two knobs (stub position
and stub length); a **double-stub tuner** trades position for a second stub.

## 3. The L-network (lumped elements)

At lower microwave frequencies, two reactive elements (one series, one shunt) in
an **L** shape match any load to any source. The choice of which element is
series vs shunt, and inductor vs capacitor, depends on whether you need to move
the load into or out of the unit circle on the Smith chart.

```mermaid
flowchart LR
  SRC["source Z0"] --> X1["series X"]
  X1 --> NODE(("node"))
  NODE --> X2["shunt B"]
  X2 --> GND["gnd"]
  NODE --> LOAD["load ZL"]
```

The L-network's **loaded Q** (hence bandwidth) is set by the impedance ratio you
are transforming - large ratios force high Q and narrow bandwidth.

## Real applications

- **Antenna matching networks** in every phone and Wi-Fi radio.
- **Power amplifier output matching** to squeeze out efficiency.
- **Quarter-wave transformers** are printed directly as tapered microstrip on RF
  boards.

```matlab
Z0 = 50; RL = 100;
Z1 = sqrt(Z0*RL);                 % quarter-wave: 70.7 ohm
% L-network to match RL > Z0: shunt C then series L
Q = sqrt(RL/Z0 - 1);              % network Q
```

```python
import numpy as np
Z0, RL = 50, 100
Z1 = np.sqrt(Z0*RL)               # 70.7 ohm quarter-wave
Q = np.sqrt(RL/Z0 - 1)            # L-network Q
```

> **Practical insight:** matching is always a **bandwidth vs simplicity** trade.
> A single L-network or quarter-wave section is narrowband; multi-section
> transformers and tapered lines buy bandwidth at the cost of size.

**Next:** when wires give up - waveguides and resonators.
""",
        ),
        _t(
            "Waveguides & resonators: modes, cutoff & cavities",
            "12 min",
            """\
# Waveguides & resonators: modes, cutoff & cavities

Above a few GHz, ordinary coax gets lossy and lossy fast. A **waveguide** - a
hollow metal pipe - carries microwave energy with very low loss by guiding the
electromagnetic fields inside it. There is no center conductor; the walls do all
the guiding.

## Modes and cutoff

A waveguide supports discrete field patterns called **modes**: **TE** (transverse
electric, no $E$ along the axis) and **TM** (transverse magnetic). Each mode only
propagates **above** a **cutoff frequency** set by the guide dimensions. For a
rectangular guide of width $a$, the dominant $TE_{10}$ mode has

$$f_c = \\frac{c}{2a}.$$

Below cutoff the mode is **evanescent** - it decays instead of propagating. The
**guide wavelength** stretches as you approach cutoff:

$$\\lambda_g = \\frac{\\lambda}{\\sqrt{1 - (f_c/f)^2}}.$$

Watch $\\lambda_g$ shoot to infinity as $f \\to f_c$:

```plot
{"title": "Guide wavelength stretches near cutoff (slide cutoff fc)", "xLabel": "frequency f (GHz)", "yLabel": "lambda_g / lambda (free space)", "xRange": [2, 12], "yRange": [0, 6], "grid": true, "controls": [{"name": "fc", "range": [2, 8], "value": 4, "label": "cutoff fc (GHz)"}], "functions": [{"expr": "(x>fc)/sqrt(1 - (fc/x)*(fc/x))", "label": "lambda_g / lambda"}]}
```

## Cavity resonators

Cap both ends of a waveguide section and trapped waves bounce back and forth,
resonating at frequencies where the length is a multiple of half a guide
wavelength. A **cavity resonator** is the microwave version of an LC tank, but
with a far higher **Q** (thousands to hundreds of thousands) because the only
loss is in the conducting walls.

```mermaid
flowchart LR
  IN["microwave power"] --> WG["waveguide (f > fc propagates)"]
  WG --> CAV["closed cavity = high-Q resonator"]
  CAV --> OUT["sharp resonance"]
```

## Real applications

- **Radar** systems and satellite uplinks use waveguide runs for their low loss
  at high power.
- **Microwave ovens**: a waveguide carries 2.45 GHz from the magnetron to the
  cooking cavity (itself a resonator).
- **Cavity filters** in cellular base stations select one band with very sharp
  skirts.
- **Particle accelerators** use superconducting RF cavities with enormous Q.

```matlab
c = 3e8; a = 0.02286;              % WR-90 X-band guide, a = 22.86 mm
fc = c/(2*a)                       % TE10 cutoff ~ 6.56 GHz
f = 10e9;
lambda_g = (c/f)/sqrt(1 - (fc/f)^2);
```

```python
c, a = 3e8, 0.02286               # WR-90 X-band, a = 22.86 mm
fc = c/(2*a)                      # TE10 cutoff ~ 6.56 GHz
f = 10e9
lambda_g = (c/f)/np.sqrt(1 - (fc/f)**2)
```

> **Practical insight:** waveguide is bulky and band-limited (one waveguide size
> per frequency band, e.g. WR-90 for X-band), but unbeatable for low loss and high
> power. You pick waveguide vs coax vs microstrip by frequency, power, and size.

**Next:** the components and the language - connectors, dB, couplers.
""",
        ),
        _t(
            "Microwave materials & components: connectors, dB & couplers",
            "11 min",
            """\
# Microwave materials & components: connectors, dB & couplers

Microwave systems are built from a kit of standard parts joined by standard
connectors and described in a standard unit - the **decibel**. Get fluent in
these and datasheets stop being intimidating.

## The decibel: why everything is in dB

RF spans enormous dynamic ranges (a receiver may handle signals a trillion times
weaker than the transmitter), so we use a **logarithmic** scale:

$$P_{dB} = 10\\log_{10}\\frac{P}{P_{ref}}, \\qquad
V_{dB} = 20\\log_{10}\\frac{V}{V_{ref}}.$$

Gains **add** and losses **subtract** instead of multiplying. Handy anchors:
3 dB = x2 power, 10 dB = x10, 20 dB = x100. **dBm** references 1 milliwatt, so
0 dBm = 1 mW and +30 dBm = 1 W. Notice how a linear power ratio maps to a gentle
log curve:

```plot
{"title": "The decibel scale: 10 log10(power ratio)", "xLabel": "power ratio (linear)", "yLabel": "dB", "xRange": [0.1, 100], "yRange": [-10, 20], "grid": true, "functions": [{"expr": "10*log10(x)", "label": "10 log10(ratio)", "color": "#2563eb"}]}
```

## Connectors and cables

| Connector | Typical use | Notes |
|-----------|-------------|-------|
| **SMA** | up to ~18 GHz | the lab workhorse, 50 ohm |
| **N-type** | up to ~11 GHz | rugged, higher power |
| **BNC** | < 1 GHz | quick-connect, instrumentation |
| **2.92/2.4 mm** | up to 40+ GHz | precision metrology |

Mismatched or worn connectors add reflection and loss - a major source of
measurement error.

## Attenuators, terminations and the directional coupler

- **Attenuator**: a resistive pad that drops power by a fixed dB while staying
  matched (protects inputs, sets levels).
- **Termination (load)**: a 50 ohm "dummy load" that absorbs a wave with no
  reflection.
- **Directional coupler**: samples a known fraction of the **forward** wave (and
  separately the reverse) - the heart of power monitoring and VSWR meters.

```mermaid
flowchart LR
  IN["input"] --> THRU["through (most power)"]
  IN --> CPL["coupled port (-20 dB sample)"]
  THRU --> OUT["output"]
```

A coupler's key specs are **coupling** (how much is tapped), **directivity** (how
well it separates forward from reverse), and **insertion loss**.

## Real applications

- A **power meter** taps the line through a directional coupler so it reads
  forward power without interrupting the signal.
- **Reflectometers / VSWR meters** compare coupled forward and reverse waves.
- **dB math** is how every link budget (next course) is computed.

```matlab
P_mW = 100;
P_dBm = 10*log10(P_mW);            % 20 dBm
gain = 30; loss = 6;               % dB
P_out_dBm = P_dBm + gain - loss;   % chain in dB: just add and subtract
```

```python
import numpy as np
P_mW = 100
P_dBm = 10*np.log10(P_mW)          # 20 dBm
gain, loss = 30, 6                 # dB
P_out_dBm = P_dBm + gain - loss    # add gains, subtract losses
```

> **Practical insight:** once you think in dB and dBm, an entire RF chain is just
> addition and subtraction - amplifier gains plus, cable and connector losses
> minus. That is the whole point of the unit.

**Next:** put it together - compute and plot reflection and VSWR yourself.
""",
        ),
        _code(
            "Lab: reflection, VSWR & a Smith-chart trajectory",
            "13 min",
            """\
# Compute the reflection coefficient and VSWR of a complex load on a 50 ohm
# line, then trace how the input reflection rotates as we move down the line
# (the spiral you would see on a Smith chart).
import numpy as np
import matplotlib.pyplot as plt

Z0 = 50.0                          # line impedance (ohm)
ZL = 30.0 + 40.0j                  # complex load
f = 2.4e9                          # 2.4 GHz
c = 3e8
lam = c/f                          # wavelength

# Reflection at the load, and VSWR.
GammaL = (ZL - Z0)/(ZL + Z0)
VSWR = (1 + abs(GammaL))/(1 - abs(GammaL))
RL_dB = -20*np.log10(abs(GammaL))  # return loss
print(f"|GammaL| = {abs(GammaL):.3f}, angle = {np.degrees(np.angle(GammaL)):.1f} deg")
print(f"VSWR = {VSWR:.2f}, return loss = {RL_dB:.1f} dB")

# Move toward the generator: Gamma rotates clockwise, |Gamma| constant.
# Gamma(d) = GammaL * exp(-j 2 beta d), beta = 2 pi / lambda.
beta = 2*np.pi/lam
d = np.linspace(0, lam/2, 400)     # half a wavelength = one full turn
Gamma_d = GammaL*np.exp(-1j*2*beta*d)

# The constant-|Gamma| (VSWR) circle the trajectory rides on.
theta = np.linspace(0, 2*np.pi, 400)
circle = abs(GammaL)*np.exp(1j*theta)

plt.figure(figsize=(5.5, 5.5))
plt.plot(np.cos(theta), np.sin(theta), color="#94a3b8", label="|Gamma|=1 rim")
plt.plot(circle.real, circle.imag, "--", color="#2563eb", label=f"VSWR={VSWR:.1f} circle")
plt.plot(Gamma_d.real, Gamma_d.imag, color="#dc2626", lw=2, label="Gamma moving to source")
plt.plot([GammaL.real], [GammaL.imag], "o", color="#16a34a", label="load")
plt.plot([0], [0], "k+", label="match (center)")
plt.gca().set_aspect("equal")
plt.xlabel("Re(Gamma)"); plt.ylabel("Im(Gamma)")
plt.title("Reflection coefficient on the Smith plane")
plt.legend(loc="upper right", fontsize=8); plt.grid(True); plt.show()

# Sweep load resistance and show VSWR (matched at RL = Z0).
RL = np.linspace(5, 250, 300)
G = (RL - Z0)/(RL + Z0)
vswr = (1 + np.abs(G))/(1 - np.abs(G))
print(f"min VSWR {vswr.min():.2f} occurs at RL ~ {RL[np.argmin(vswr)]:.0f} ohm (= Z0)")

# Try it yourself:
#   1. Set ZL = 50 (matched): the red trajectory collapses to the center.
#   2. The MATLAB way: Gamma = (ZL-Z0)/(ZL+Z0); rotate with exp(-1j*2*beta*d).
""",
        ),
    ),
)


# -- Antennas & Microwave Engineering -- Intermediate --------------------------

_MICROWAVE_INTERMEDIATE = SeedCourse(
    slug="microwave-intermediate",
    title="Antennas & Microwave Engineering -- Intermediate: S-Parameters & Antennas",
    description=(
        "S-parameters and network analysis (insertion/return loss, the VNA, "
        "two-ports), microwave components (couplers, Wilkinson divider, "
        "circulators, filters), antenna fundamentals (gain, directivity, "
        "beamwidth, radiation patterns), the dipole and monopole, and the Friis "
        "link budget - dual MATLAB/Python, interactive plots, and a runnable "
        "radiation-pattern / link-budget lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "S-parameters & network analysis",
            "13 min",
            """\
# S-parameters & network analysis

At microwave frequencies you cannot easily measure voltage and current (probes
load the circuit and standing waves make "the" voltage ambiguous). Instead we
describe a device by how it **scatters waves**: the **scattering parameters**, or
**S-parameters**.

## The S-matrix

For a two-port (input port 1, output port 2), incident waves $a_1, a_2$ produce
reflected waves $b_1, b_2$:

$$\\begin{bmatrix} b_1 \\\\ b_2 \\end{bmatrix} =
\\begin{bmatrix} S_{11} & S_{12} \\\\ S_{21} & S_{22} \\end{bmatrix}
\\begin{bmatrix} a_1 \\\\ a_2 \\end{bmatrix}.$$

Each parameter has a plain-English meaning (measured with the other port
terminated in $Z_0$):

| Parameter | Meaning |
|-----------|---------|
| $S_{11}$ | input **reflection** (how badly the input is matched) |
| $S_{21}$ | **forward transmission** (gain or loss through the device) |
| $S_{12}$ | reverse transmission (isolation / leakage backward) |
| $S_{22}$ | output reflection |

## Return loss and insertion loss

Two everyday numbers fall straight out of the S-parameters, both in dB:

$$\\text{return loss} = -20\\log_{10}|S_{11}|, \\qquad
\\text{insertion loss} = -20\\log_{10}|S_{21}|.$$

A filter's $|S_{21}|$ vs frequency *is* its response. Here is a band-pass
$|S_{21}|$ whose center and width you can slide:

```plot
{"title": "Band-pass |S21| in dB (slide center and Q)", "xLabel": "frequency (GHz)", "yLabel": "|S21| (dB)", "xRange": [1, 5], "yRange": [-40, 2], "grid": true, "controls": [{"name": "f0", "range": [2, 4], "value": 3, "label": "center f0 (GHz)"}, {"name": "Q", "range": [3, 20], "value": 8, "label": "selectivity Q"}], "functions": [{"expr": "-10*log10(1 + Q*Q*(x/f0 - f0/x)*(x/f0 - f0/x))", "label": "|S21| (dB)"}]}
```

## The VNA and two-ports

The **vector network analyzer (VNA)** is the instrument that measures
S-parameters: it sends a known wave into each port and measures the magnitude and
phase of what comes back and through. After a **calibration** (SOLT: short, open,
load, thru) that removes cable and connector errors, it reports the device's true
S-matrix - usually displayed on a Smith chart ($S_{11}$) and a log-magnitude plot
($S_{21}$).

```mermaid
flowchart LR
  VNA["VNA port 1"] -->|a1| DUT["device under test"]
  DUT -->|b1 reflected| VNA
  DUT -->|b2 transmitted| VNA2["VNA port 2"]
```

## Real applications

- **Characterizing a filter, amplifier, or antenna** before it goes into a system.
- **Cascading** blocks: convert S to **T (ABCD)** parameters, multiply, convert
  back - that is how a whole chain's response is predicted.

```matlab
S11 = 0.1; S21 = 0.95;
return_loss    = -20*log10(abs(S11));   % ~20 dB (good match)
insertion_loss = -20*log10(abs(S21));   % ~0.4 dB
```

```python
import numpy as np
S11, S21 = 0.1, 0.95
return_loss = -20*np.log10(abs(S11))    # ~20 dB
insertion_loss = -20*np.log10(abs(S21)) # ~0.4 dB
```

> **Practical insight:** S-parameters are the universal trade language of RF.
> Vendors ship `.s2p` Touchstone files; tools like scikit-rf in Python read,
> cascade, and de-embed them programmatically.

**Next:** the passive building blocks - couplers, dividers, circulators, filters.
""",
        ),
        _t(
            "Microwave components: couplers, Wilkinson divider, circulators & filters",
            "12 min",
            """\
# Microwave components: couplers, Wilkinson divider, circulators & filters

A microwave system is assembled from a handful of passive blocks, each defined by
its S-matrix. Knowing what each does (and its limits) lets you read a block
diagram fluently.

## Power dividers and the Wilkinson

A **power divider** splits one input into two outputs. The **Wilkinson power
divider** is the favorite: two quarter-wave lines plus an **isolation resistor**
give an equal, in-phase 3 dB split that is matched at all ports **and** isolates
the two outputs from each other - so a reflection off one output does not couple
into the other. The lines are $\\sqrt{2}\\,Z_0 \\approx 70.7$ ohm for a 50 ohm
system.

## Directional couplers and hybrids

A **directional coupler** taps a fixed fraction of the forward wave. The **90
degree hybrid** (branch-line) and **180 degree hybrid (rat-race)** split power
with a defined phase difference - the workhorses of balanced amplifiers and
mixers.

## Circulators and isolators

A **circulator** is a non-reciprocal three-port (using a magnetized ferrite):
power entering port 1 leaves only at port 2, port 2 to port 3, port 3 to port 1.
Terminate one port and it becomes an **isolator** that passes the forward wave but
absorbs the reflected one - protecting a transmitter's power amplifier from a bad
antenna match. It also lets a radar share one antenna for transmit and receive.

```mermaid
flowchart LR
  P1["port 1 (TX)"] --> P2["port 2 (antenna)"]
  P2 --> P3["port 3 (RX)"]
  P3 --> P1
```

## Filters

A **filter** passes one band and rejects others. Key specs are **center
frequency**, **bandwidth**, **insertion loss** in-band, and **rejection** out of
band. Slide the order and watch the skirts get steeper:

```plot
{"title": "Low-pass filter rolloff steepens with order (slide order n)", "xLabel": "frequency / cutoff", "yLabel": "|H| (dB)", "xRange": [0.2, 5], "yRange": [-60, 3], "grid": true, "controls": [{"name": "n", "range": [1, 6], "value": 3, "label": "filter order n"}], "functions": [{"expr": "-10*log10(1 + x^(2*n))", "label": "Butterworth |H| (dB)"}]}
```

Implementations: **lumped LC** at lower frequencies, **coupled microstrip lines**
on a PCB, and high-Q **cavity/waveguide filters** in base stations and radar.

## Real applications

- A **Wilkinson** feeds two antennas equally from one transmitter.
- An **isolator** protects a 100 W base-station amplifier from antenna mismatch.
- **Duplexer filters** let a phone transmit and receive on nearby frequencies
  through one antenna.

```matlab
Z0 = 50;
Z_wilkinson = sqrt(2)*Z0;          % 70.7 ohm quarter-wave arms
R_iso = 2*Z0;                      % 100 ohm isolation resistor
coupling_dB = 20;                  % a 20 dB coupler taps 1% of the power
```

```python
import numpy as np
Z0 = 50
Z_wilkinson = np.sqrt(2)*Z0        # 70.7 ohm arms
R_iso = 2*Z0                       # 100 ohm isolation resistor
coupling_dB = 20                   # taps 1% of forward power
```

> **Practical insight:** circulators/isolators are **non-reciprocal** - they break
> the usual "what goes forward can go back" symmetry, which is exactly why they
> protect amplifiers and enable single-antenna radar.

**Next:** launching energy into space - antenna fundamentals.
""",
        ),
        _t(
            "Antenna fundamentals: radiation, fields, gain, directivity & beamwidth",
            "13 min",
            """\
# Antenna fundamentals: radiation, fields, gain, directivity & beamwidth

An **antenna** is a transducer between a guided wave (on a line) and a radiated
wave (in free space). Accelerating charges radiate; an antenna is just a
structure shaped to do that efficiently in the directions you want.

## Near field and far field

Close to the antenna (the **near field**, reactive zone) energy sloshes back and
forth without radiating. Beyond roughly the **Fraunhofer distance**

$$d_{far} = \\frac{2 D^2}{\\lambda}$$

(with $D$ the largest antenna dimension) you are in the **far field**, where the
pattern stops changing shape and the wave looks locally planar. Antenna specs and
range measurements assume the far field.

## Directivity, gain and efficiency

- **Directivity** $D$: how concentrated the radiation is compared to an
  isotropic (equal-in-all-directions) radiator.
- **Gain** $G = e_{rad}\\,D$: directivity reduced by **radiation efficiency**
  $e_{rad}$ (ohmic and mismatch losses). Usually quoted in **dBi** (dB over
  isotropic).
- A useful approximation links gain to the beam solid angle:
  $G \\approx \\dfrac{4\\pi}{\\theta_E\\,\\theta_H}$ (beamwidths in radians).

So a **narrower beam means higher gain** - you trade coverage for reach. Slide the
beamwidth and watch the peak gain climb:

```plot
{"title": "Narrower beam -> higher gain (slide beamwidth)", "xLabel": "beamwidth (degrees)", "yLabel": "approx gain (dBi)", "xRange": [2, 120], "yRange": [0, 45], "grid": true, "controls": [{"name": "k", "range": [25000, 41000], "value": 32400, "label": "aperture constant"}], "functions": [{"expr": "10*log10(k/(x*x))", "label": "G ~ 10 log10(k / BW^2)"}]}
```

## The radiation pattern and beamwidth

The **radiation pattern** is gain vs direction. Key features: the **main lobe**
(the beam), the **half-power beamwidth (HPBW)** where it drops 3 dB, and the
**sidelobes** (unwanted minor lobes). A normalized power pattern of a typical
beam:

```plot
{"title": "Antenna power pattern: main lobe, 3 dB beamwidth & sidelobes", "xLabel": "angle (degrees)", "yLabel": "normalized power (dB)", "xRange": [-90, 90], "yRange": [-40, 2], "grid": true, "functions": [{"expr": "10*log10(max(0.0001, (sin(rad(x)*4)/(rad(x)*4 + 0.0001))^2))", "label": "pattern (dB)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  TX["transmit chain"] --> ANT["antenna"]
  ANT --> NF["near field (reactive)"]
  NF --> FF["far field (radiating, pattern fixed)"]
```

## Real applications

- A **dish antenna** for satellite TV has high gain (narrow beam) so it must be
  pointed precisely.
- A **base station sector antenna** is shaped to flood a 120 degree wedge of
  cells.
- **Sidelobe control** matters in radar (to reject clutter and jamming).

```matlab
D = 0.5; lambda = 0.06;            % 0.5 m dish at 5 GHz
d_far = 2*D^2/lambda               % far-field distance ~ 8.3 m
G_dBi = 10*log10(32400/(10*10));   % ~25 dBi for a 10 deg x 10 deg beam
```

```python
import numpy as np
D, lam = 0.5, 0.06                 # 0.5 m dish at 5 GHz
d_far = 2*D**2/lam                 # ~8.3 m
G_dBi = 10*np.log10(32400/(10*10)) # ~25 dBi for a 10x10 deg beam
```

> **Practical insight:** gain, beamwidth, and aperture size are three views of one
> thing. Bigger aperture (in wavelengths) = narrower beam = higher gain. You
> cannot have an omnidirectional high-gain antenna.

**Next:** the simplest real antennas - the dipole and monopole.
""",
        ),
        _t(
            "The dipole & monopole: half-wave dipole, radiation resistance & pattern",
            "12 min",
            """\
# The dipole & monopole: half-wave dipole, radiation resistance & pattern

The **half-wave dipole** is the reference antenna of all of RF: a straight
conductor about $\\lambda/2$ long, fed in the middle. Almost every antenna spec is
quoted relative to it (**dBd**) or to isotropic (**dBi**), with
$0\\,\\text{dBd} = 2.15\\,\\text{dBi}$.

## Why half a wavelength?

At $\\lambda/2$ the current distribution forms a half-sine standing wave - maximum
in the middle (where it is fed), zero at the tips. This length puts the feedpoint
**resistance** near a convenient value and the reactance near zero (resonant), so
it is easy to match.

## Radiation resistance

The power an antenna radiates looks, to the feed, like a resistance - the
**radiation resistance** $R_r$. For a half-wave dipole $R_r \\approx 73$ ohm
(close to 50 or 75 ohm coax, hence its popularity). The fields drop the input
reactance to ~0 at resonance; trimming length tunes it. Input resistance vs
length (electrical):

```plot
{"title": "Dipole input resistance vs length (resonance near 0.48 lambda)", "xLabel": "dipole length / lambda", "yLabel": "input resistance (ohm)", "xRange": [0.3, 0.7], "yRange": [0, 200], "grid": true, "controls": [{"name": "Rr", "range": [60, 90], "value": 73, "label": "resonant Rr (ohm)"}], "functions": [{"expr": "Rr*(1 + 9*(x - 0.48)*(x - 0.48))", "label": "approx R_in"}]}
```

## The pattern: the classic doughnut

A dipole radiates best **broadside** (perpendicular to the wire) and not at all
off its ends - a doughnut-shaped pattern. The normalized field is

$$F(\\theta) = \\frac{\\cos\\!\\left(\\tfrac{\\pi}{2}\\cos\\theta\\right)}{\\sin\\theta}.$$

Its HPBW is about 78 degrees and gain ~2.15 dBi. The pattern cross-section
(field vs angle) - press Play to sweep a marker around the lobe:

```plot
{"title": "Half-wave dipole pattern cross-section (marker sweeps the lobe)", "xLabel": "x", "yLabel": "y", "xRange": [-1.2, 1.2], "yRange": [-1.2, 1.2], "grid": true, "animate": {"param": "t", "range": [0.01, 3.13], "label": "angle theta"}, "parametric": [{"x": "(cos(1.5708*cos(t))/sin(t))*sin(t)", "y": "(cos(1.5708*cos(t))/sin(t))*cos(t)", "range": [0.01, 3.13], "label": "upper lobe", "color": "#2563eb"}], "points": [{"xExpr": "(cos(1.5708*cos(t))/sin(t))*sin(t)", "yExpr": "(cos(1.5708*cos(t))/sin(t))*cos(t)", "label": "now", "color": "#dc2626", "size": 7, "trail": true}]}
```

## The monopole: half a dipole over a ground plane

Stand a $\\lambda/4$ rod on a conducting **ground plane** and the plane's image
makes it behave like a full dipole, but radiating into the upper half-space only.
Its radiation resistance is **half** the dipole's (~36 ohm), and gain is ~3 dB
higher in the upper hemisphere. Car whip antennas, AM broadcast towers, and the
ground-plane "rubber duck" are all monopoles.

```mermaid
flowchart TB
  FEED["coax feed"] --> ROD["lambda/4 rod"]
  GND["ground plane"] --> IMG["image makes it look like a dipole"]
```

## Real applications

- **FM/TV reception**, ham radio, and countless reference antennas use dipoles.
- **Monopoles**: car radios, AM towers (the tower *is* the antenna), and base
  whips.

```matlab
c = 3e8; f = 100e6;                % FM broadcast
lambda = c/f;                      % 3 m
L_dipole = 0.48*lambda;            % ~1.44 m (trimmed half-wave)
Rr = 73;                           % radiation resistance (ohm)
```

```python
c, f = 3e8, 100e6                  # FM broadcast
lam = c/f                          # 3 m
L_dipole = 0.48*lam                # ~1.44 m
Rr = 73                            # radiation resistance (ohm)
```

> **Practical insight:** a real dipole is trimmed slightly **shorter** than
> $\\lambda/2$ (about $0.48\\lambda$) to cancel the small inductive reactance and
> hit pure resonance. Wire diameter and nearby objects shift this too.

**Next:** how much of that signal arrives - the Friis link budget.
""",
        ),
        _t(
            "The link budget & the Friis equation",
            "12 min",
            """\
# The link budget & the Friis equation

A **link budget** adds up every gain and loss between a transmitter and a
receiver, in dB, to predict the received power - and therefore whether the link
will work. It is the single most useful calculation in wireless engineering.

## Free-space path loss

Even with perfect antennas, power spreads over an ever-larger sphere, so it falls
as $1/r^2$. Expressed as **free-space path loss (FSPL)** in dB:

$$\\text{FSPL(dB)} = 20\\log_{10} d + 20\\log_{10} f + 20\\log_{10}\\!\\frac{4\\pi}{c}.$$

Doubling the distance costs **6 dB**; doubling the frequency costs another 6 dB.
Watch path loss climb with distance:

```plot
{"title": "Free-space path loss vs distance (slide frequency)", "xLabel": "distance (km)", "yLabel": "path loss (dB)", "xRange": [0.1, 50], "yRange": [60, 160], "grid": true, "controls": [{"name": "fGHz", "range": [0.5, 30], "value": 2.4, "label": "frequency (GHz)"}], "functions": [{"expr": "20*log10(x) + 20*log10(fGHz) + 92.45", "label": "FSPL (dB), d in km, f in GHz"}]}
```

(The 92.45 constant bundles the units for km and GHz.)

## The Friis transmission equation

Friis ties it all together. In linear form:

$$P_r = P_t\\,G_t\\,G_r\\left(\\frac{\\lambda}{4\\pi d}\\right)^2.$$

In **dB** it becomes pure addition - the form engineers actually use:

$$P_r(\\text{dBm}) = P_t + G_t + G_r - \\text{FSPL}.$$

## EIRP and the full budget

**EIRP** (effective isotropic radiated power) $= P_t + G_t$ is what the antenna
effectively shouts in its best direction (and what regulators cap). A full link
budget chains everything:

$$P_r = \\text{EIRP} + G_r - \\text{FSPL} - L_{cable} - L_{misc}.$$

Compare $P_r$ to the receiver **sensitivity** (noise floor + required SNR); the
difference is your **link margin**.

```mermaid
flowchart LR
  PT["Pt (TX power)"] --> EIRP["+ Gt = EIRP"]
  EIRP --> LOSS["- FSPL - cable losses"]
  LOSS --> RX["+ Gr = Pr at receiver"]
  RX --> MARGIN["- sensitivity = link margin"]
```

## Real applications

- **GPS**: a ~27 W satellite signal arrives near -130 dBm at your phone - the
  budget shows why you need spreading gain to dig it out of noise.
- **Wi-Fi / 5G cell planning**: how far does coverage reach at a given data rate.
- **Deep-space (e.g. Voyager)**: huge dish gain and ultra-low-noise receivers
  close a link across billions of kilometers.

```matlab
Pt = 20; Gt = 6; Gr = 6;           % dBm, dBi, dBi
fGHz = 2.4; d_km = 1;
FSPL = 20*log10(d_km) + 20*log10(fGHz) + 92.45;  % ~100 dB
Pr = Pt + Gt + Gr - FSPL;          % received power (dBm)
```

```python
import numpy as np
Pt, Gt, Gr = 20, 6, 6              # dBm, dBi, dBi
fGHz, d_km = 2.4, 1
FSPL = 20*np.log10(d_km) + 20*np.log10(fGHz) + 92.45
Pr = Pt + Gt + Gr - FSPL           # dBm
```

> **Practical insight:** because everything is in dB, designing a link is
> bookkeeping: list every plus (powers, antenna gains) and minus (path loss,
> cables, fades) and keep a few dB of **margin** for rain, fading, and aging.

**Next:** plot a radiation pattern and a real link budget yourself.
""",
        ),
        _code(
            "Lab: radiation pattern & Friis link budget",
            "13 min",
            """\
# Plot a half-wave dipole's radiation pattern and compute a Friis link budget
# sweep, all with numpy + matplotlib.
import numpy as np
import matplotlib.pyplot as plt

# --- Part 1: half-wave dipole radiation pattern (polar) ---
theta = np.linspace(0.001, np.pi, 400)        # 0..180 deg
# Normalized field pattern of a half-wave dipole.
F = np.cos(np.pi/2*np.cos(theta))/np.sin(theta)
P_dB = 20*np.log10(np.abs(F)/np.abs(F).max())
P_dB = np.clip(P_dB, -40, 0)                   # floor for the polar plot

hpbw_mask = P_dB > -3.0
hpbw = np.degrees(theta[hpbw_mask].max() - theta[hpbw_mask].min())

ax = plt.subplot(1, 2, 1, projection="polar")
ax.plot(theta, P_dB + 40, color="#2563eb")     # shift so -40 dB is at center
ax.plot(-theta, P_dB + 40, color="#2563eb")    # mirror to the other side
ax.set_title(f"Half-wave dipole (HPBW ~ {hpbw:.0f} deg)")

# --- Part 2: Friis link budget vs distance ---
Pt_dBm = 20.0        # 100 mW transmitter
Gt, Gr = 6.0, 6.0    # antenna gains (dBi)
fGHz = 2.4           # 2.4 GHz
d_km = np.linspace(0.05, 20, 400)
FSPL = 20*np.log10(d_km) + 20*np.log10(fGHz) + 92.45
Pr_dBm = Pt_dBm + Gt + Gr - FSPL
sensitivity = -90.0  # receiver sensitivity (dBm)

max_range = d_km[Pr_dBm > sensitivity].max()

plt.subplot(1, 2, 2)
plt.plot(d_km, Pr_dBm, color="#dc2626", label="received power")
plt.axhline(sensitivity, ls="--", color="#16a34a", label="sensitivity")
plt.xlabel("distance (km)"); plt.ylabel("Pr (dBm)")
plt.title(f"Friis link: range ~ {max_range:.1f} km"); plt.legend(); plt.grid(True)

plt.tight_layout(); plt.show()

print(f"dipole HPBW ~ {hpbw:.0f} deg")
print(f"EIRP = {Pt_dBm + Gt:.1f} dBm; usable range ~ {max_range:.1f} km")

# Try it yourself:
#   1. Raise Gt to 20 dBi (a directional antenna): range jumps.
#   2. The MATLAB way: same formulas; use polarplot for the pattern.
""",
        ),
    ),
)


# -- Antennas & Microwave Engineering -- Advanced ------------------------------

_MICROWAVE_ADVANCED = SeedCourse(
    slug="microwave-advanced",
    title="Antennas & Microwave Engineering -- Advanced: Arrays, Active & mmWave",
    description=(
        "Antenna arrays and beamforming (array factor, phased arrays, beam "
        "steering, sidelobes), aperture and specialized antennas (horn, patch, "
        "parabolic), microwave amplifiers and oscillators (gain, stability, noise "
        "figure, the LNA), the RF front-end (mixers, receiver chain, "
        "intermodulation), and mmWave/5G/radar - dual MATLAB/Python, interactive "
        "plots, a runnable phased-array lab, and a real-world applications "
        "capstone."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Antenna arrays & beamforming: array factor, phased arrays & sidelobes",
            "13 min",
            """\
# Antenna arrays & beamforming: array factor, phased arrays & sidelobes

A single antenna has a fixed pattern. Put many of them in an **array** and the
combined pattern is something you can **shape and steer electronically** - the
idea behind every modern radar and 5G base station.

## The array factor

For $N$ identical elements spaced $d$ apart, fed with progressive phase shift
$\\beta$, the array's pattern is the single-element pattern times the **array
factor**:

$$AF(\\theta) = \\sum_{n=0}^{N-1} e^{\\,j n(kd\\cos\\theta + \\beta)},
\\qquad k = \\frac{2\\pi}{\\lambda}.$$

The elements interfere **constructively** in the direction where the path delay
matches the feed phase. Add more elements and the main beam narrows while
sidelobes appear - slide the element count:

```plot
{"title": "Array factor: more elements -> narrower beam (slide N)", "xLabel": "angle from broadside (degrees)", "yLabel": "|AF| normalized", "xRange": [-90, 90], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "N", "range": [2, 12], "value": 6, "label": "number of elements N"}], "functions": [{"expr": "abs(sin(N*pi/2*sin(rad(x)))/(N*sin(pi/2*sin(rad(x))) + 0.0001))", "label": "|AF| (half-wave spacing)"}]}
```

## Beam steering

Here is the magic: change the **progressive phase** $\\beta$ and the beam points in
a new direction with **no moving parts**. The main beam aims where
$kd\\cos\\theta_0 + \\beta = 0$, i.e.

$$\\theta_0 = \\cos^{-1}\\!\\left(-\\frac{\\beta}{kd}\\right).$$

A **phased array** sets each element's phase electronically to sweep the beam in
microseconds. Slide the steering phase and watch the beam move:

```plot
{"title": "Phased-array beam steering by progressive phase (slide phase)", "xLabel": "angle (degrees)", "yLabel": "|AF| normalized", "xRange": [-90, 90], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "ph", "range": [-2, 2], "value": 0, "label": "phase shift per element (rad)"}], "functions": [{"expr": "abs(sin(8*(pi/2*sin(rad(x)) + ph/2))/(8*sin(pi/2*sin(rad(x)) + ph/2) + 0.0001))", "label": "|AF|, N=8"}]}
```

## Sidelobes and tapering

Uniform feeding gives the narrowest beam but high (-13 dB) sidelobes. **Amplitude
tapering** (feeding edge elements weaker - Chebyshev, Taylor windows) lowers
sidelobes at the cost of a slightly wider beam - the same window trade-off as in
DSP. **Grating lobes** (false copies of the beam) appear if spacing exceeds
$\\lambda/2$, so elements are usually spaced about a half wavelength.

```mermaid
flowchart LR
  SIG["RF signal"] --> SPLIT["split to N elements"]
  SPLIT --> PH["per-element phase shifters"]
  PH --> ANT["N antennas"]
  ANT --> BEAM["steerable combined beam"]
```

## Real applications

- **5G mmWave** base stations use phased arrays to beamform to individual users.
- **AESA radar** (active electronically scanned array) on fighter jets steers
  instantly and tracks many targets.
- **Starlink** user terminals are flat phased arrays that track satellites
  electronically.

```matlab
N = 8; d_over_lambda = 0.5; theta0 = 30;  % steer to 30 deg
k = 2*pi; beta = -k*d_over_lambda*cos(deg2rad(90 - theta0));
% feed element n with phase n*beta
```

```python
import numpy as np
N, d_lam, theta0 = 8, 0.5, np.deg2rad(30)
k = 2*np.pi
beta = -k*d_lam*np.cos(np.pi/2 - theta0)  # progressive phase to steer
phases = np.arange(N)*beta
```

> **Practical insight:** the array factor narrows the beam; the elements' own
> pattern caps how far you can steer before gain falls off (**scan loss**). Real
> arrays combine both, and add taper to tame sidelobes.

**Next:** specialized high-gain antennas - horns, patches, dishes.
""",
        ),
        _t(
            "Aperture & specialized antennas: horn, patch & parabolic",
            "12 min",
            """\
# Aperture & specialized antennas: horn, patch & parabolic

Beyond wire antennas lie the **aperture antennas**, which radiate through a
physical opening. Their gain follows one master rule: bigger electrical aperture =
higher gain.

## The aperture gain law

For an aperture of physical area $A$ and aperture efficiency $e_{ap}$ (typically
0.5-0.7):

$$G = e_{ap}\\,\\frac{4\\pi A}{\\lambda^2}.$$

Gain rises with area and with frequency squared. A 1 m dish is mediocre at
1 GHz but spectacular at 30 GHz. Slide aperture diameter and watch gain climb:

```plot
{"title": "Parabolic dish gain vs diameter (slide frequency)", "xLabel": "dish diameter (m)", "yLabel": "gain (dBi)", "xRange": [0.2, 5], "yRange": [10, 60], "grid": true, "controls": [{"name": "fGHz", "range": [1, 40], "value": 12, "label": "frequency (GHz)"}], "functions": [{"expr": "10*log10(0.6*9.8696*x*x*fGHz*fGHz/0.09)", "label": "G ~ 10 log10(eff 4pi A / lambda^2)"}]}
```

## The antenna zoo

| Antenna | Idea | Typical gain | Used in |
|---------|------|--------------|---------|
| **Horn** | flared waveguide | 10-25 dBi | feeds, gain standards |
| **Microstrip / patch** | printed metal patch over ground | 6-9 dBi | phones, GPS, arrays |
| **Parabolic dish** | reflector focuses to a feed | 30-60 dBi | satellite, deep space |
| **Lens / reflectarray** | shapes the wavefront | high | mmWave, imaging |

## The microstrip patch - flat and printable

A **patch** is a metal rectangle about $\\lambda/2$ long over a grounded substrate.
It is cheap, flat, and conformal - which is why it dominates phones, GPS, and
array elements. Its bandwidth is narrow (a few percent), traded for size. The
resonant length sets the frequency:

```plot
{"title": "Microstrip patch resonant frequency vs length (slide permittivity)", "xLabel": "patch length (mm)", "yLabel": "resonant frequency (GHz)", "xRange": [5, 60], "yRange": [1, 12], "grid": true, "controls": [{"name": "er", "range": [2, 10], "value": 4.4, "label": "substrate permittivity er"}], "functions": [{"expr": "150/(x*sqrt(er))", "label": "f ~ c/(2 L sqrt(er)), L in mm"}]}
```

## The parabolic dish - the gain champion

A **parabolic reflector** turns a feed's spherical wave into a plane wave (or
focuses an incoming plane wave to the feed). Larger and higher-frequency = a
pencil beam with enormous gain, but it must be pointed precisely and is bulky.

```mermaid
flowchart LR
  FEED["feed horn"] --> DISH["parabolic reflector"]
  DISH --> PLANE["collimated plane wave (pencil beam)"]
```

## Real applications

- **Satellite TV / VSAT**: parabolic dishes, 30-45 dBi.
- **GPS patch antenna** on a phone or car roof.
- **Radio astronomy** dishes and arrays of dishes (interferometers).
- **mmWave imaging and automotive radar** lenses.

```matlab
D = 1.2; lambda = 0.025;           % 1.2 m dish at 12 GHz
A = pi*(D/2)^2; eff = 0.6;
G_dBi = 10*log10(eff*4*pi*A/lambda^2)   % ~41 dBi
```

```python
import numpy as np
D, lam = 1.2, 0.025                # 1.2 m dish at 12 GHz
A, eff = np.pi*(D/2)**2, 0.6
G_dBi = 10*np.log10(eff*4*np.pi*A/lam**2)  # ~41 dBi
```

> **Practical insight:** aperture antennas trade size and pointing accuracy for
> gain. Patches give up gain and bandwidth for being flat and cheap - which is why
> arrays of patches (last lesson) get back the gain while staying conformal.

**Next:** putting energy and intelligence into the signal - active devices.
""",
        ),
        _t(
            "Microwave amplifiers & oscillators: gain, stability, noise figure & the LNA",
            "13 min",
            """\
# Microwave amplifiers & oscillators: gain, stability, noise figure & the LNA

Passive components only lose power; **active** devices (transistors) add gain and
generate signals. At microwave frequencies they are characterized - like
everything else - by S-parameters.

## Gain and matching

A transistor's available gain depends on how its input and output are matched. The
**transducer gain** combines the device's intrinsic $|S_{21}|^2$ with the source
and load match. Designers use the Smith chart to plot **constant-gain circles**
and choose a match that hits a gain target while staying stable.

## Stability: do not build an accidental oscillator

An amplifier is **unconditionally stable** if no passive source/load can make it
oscillate. The test uses the **Rollet stability factor**:

$$K = \\frac{1 - |S_{11}|^2 - |S_{22}|^2 + |\\Delta|^2}{2\\,|S_{12}\\,S_{21}|}
> 1, \\quad |\\Delta| < 1.$$

If $K < 1$ the device is only **conditionally** stable - certain source/load
impedances will make it oscillate. **Stability circles** on the Smith chart mark
the dangerous regions to avoid.

## Noise figure and the LNA

Every amplifier adds noise. The **noise figure** $F$ measures how much it degrades
the signal-to-noise ratio. In a chain, the **Friis noise formula** shows the
**first** stage dominates:

$$F_{total} = F_1 + \\frac{F_2 - 1}{G_1} + \\frac{F_3 - 1}{G_1 G_2} + \\dots$$

So the **low-noise amplifier (LNA)** comes first and must have low $F$ and decent
gain - it sets the whole receiver's noise floor. Notice how a high first-stage
gain crushes the contribution of later stages:

```plot
{"title": "Cascade noise figure: a good LNA hides later stages (slide LNA gain)", "xLabel": "LNA gain G1 (dB)", "yLabel": "total noise figure (dB)", "xRange": [5, 30], "yRange": [1, 8], "grid": true, "controls": [{"name": "F2dB", "range": [3, 12], "value": 8, "label": "2nd-stage NF (dB)"}], "functions": [{"expr": "10*log10(1.585 + (10^(F2dB/10) - 1)/10^(x/10))", "label": "F_total (F1=2dB)"}]}
```

## Oscillators: gain plus feedback

Take an amplifier, feed its output back **in phase** through a frequency-selective
network with loop gain >= 1, and it oscillates (the Barkhausen idea). At microwave
frequencies the resonator is a **dielectric resonator**, a cavity, or a varactor-
tuned tank (a **VCO**). Oscillators provide the **local oscillator** for mixers
and the carrier for transmitters; their **phase noise** is the key spec.

```mermaid
flowchart LR
  ANT["antenna"] --> LNA["LNA (low NF, sets noise floor)"]
  LNA --> MIX["mixer"]
  LO["oscillator / VCO"] --> MIX
  MIX --> IF["IF stages"]
```

## Real applications

- **Satellite LNB**: the LNA sits right at the dish feed to set a low noise floor
  before any cable loss.
- **Cellular power amplifiers** push tens of watts efficiently (and must stay
  stable into a varying antenna match).
- **VCOs/PLLs** synthesize the precise frequencies every radio tunes to.

```matlab
F1 = 10^(2/10); G1 = 10^(15/10);   % LNA: 2 dB NF, 15 dB gain
F2 = 10^(8/10);                    % next stage 8 dB NF
F_tot = F1 + (F2 - 1)/G1;
NF_dB = 10*log10(F_tot)            % ~2.2 dB total
```

```python
import numpy as np
F1, G1 = 10**(2/10), 10**(15/10)   # 2 dB NF, 15 dB gain LNA
F2 = 10**(8/10)
F_tot = F1 + (F2 - 1)/G1
NF_dB = 10*np.log10(F_tot)         # ~2.2 dB
```

> **Practical insight:** put your **best (lowest-NF) amplifier first** and give it
> enough gain to swamp later stages. After ~15-20 dB of low-noise gain, the rest
> of the chain barely matters for noise.

**Next:** assembling the whole radio - the RF front-end.
""",
        ),
        _t(
            "The RF front-end & system: mixers, the receiver chain & intermodulation",
            "12 min",
            """\
# The RF front-end & system: mixers, the receiver chain & intermodulation

Individual blocks become a **radio** when chained into a front-end. The dominant
architecture is the **superheterodyne** receiver: translate the incoming signal to
a fixed **intermediate frequency (IF)** where filtering and amplification are easy.

## The mixer: frequency translation

A **mixer** multiplies the incoming RF by a **local oscillator (LO)**, producing
sum and difference frequencies:

$$\\cos(\\omega_{RF}t)\\cos(\\omega_{LO}t) =
\\tfrac{1}{2}\\cos((\\omega_{RF}-\\omega_{LO})t) +
\\tfrac{1}{2}\\cos((\\omega_{RF}+\\omega_{LO})t).$$

A filter keeps the difference (the IF). This shifts a station from, say, 100 MHz
down to a 10.7 MHz IF where the selective filter lives - the same IF regardless of
which station you tune, because you retune the LO.

## The receiver chain

```mermaid
flowchart LR
  ANT["antenna"] --> PRE["preselect filter"]
  PRE --> LNA["LNA"]
  LNA --> MIX["mixer"]
  LO["tunable LO"] --> MIX
  MIX --> IF["IF filter + gain"]
  IF --> DET["demodulator / ADC"]
```

Order matters: the **LNA before the mixer** (mixers are noisy and lossy), the
**preselect filter** before the LNA to reject out-of-band energy, and the sharp
**IF filter** doing the channel selection.

## Intermodulation and dynamic range

Real amplifiers and mixers are slightly **nonlinear**, so two input tones $f_1,
f_2$ create **intermodulation** products. The nasty ones are **third-order** at
$2f_1 - f_2$ and $2f_2 - f_1$ - they land *in band* and cannot be filtered out.
Their power rises **3x faster** (in dB) than the wanted signal, so they cross at
the extrapolated **third-order intercept point (IP3)**:

```plot
{"title": "Output power vs input: fundamental and 3rd-order IM meet at IP3", "xLabel": "input power (dBm)", "yLabel": "output power (dBm)", "xRange": [-40, 5], "yRange": [-80, 20], "grid": true, "functions": [{"expr": "x + 20", "label": "fundamental (slope 1)", "color": "#2563eb"}, {"expr": "3*x + 20", "label": "3rd-order IM (slope 3)", "color": "#dc2626"}]}
```

The higher the IP3, the more **linear** the device and the larger its **spurious-
free dynamic range** - the gap between the noise floor and where distortion
appears. Receivers trade gain (sensitivity) against linearity (handling strong
nearby signals).

## Other system effects

- **Image frequency**: a signal at the "mirror" of the LO also lands on the IF -
  killed by the preselect filter or an **image-reject** mixer.
- **Direct-conversion (zero-IF)** receivers mix straight to baseband - simpler,
  but face DC offset and 1/f noise. Dominant in modern integrated radios.

## Real applications

- Your **phone's radio** is a highly integrated direct-conversion transceiver.
- A **spectrum analyzer** is a precision swept superheterodyne receiver.
- **Software-defined radio (SDR)** digitizes near the antenna and does the rest in
  DSP.

```matlab
f_RF = 100e6; f_LO = 89.3e6;
f_IF = f_RF - f_LO                 % 10.7 MHz IF
% IP3 example: IIP3 from a two-tone test
P_fund = -20; P_im3 = -60;         % dBm
IIP3 = P_fund + (P_fund - P_im3)/2;  % -10 dBm
```

```python
f_RF, f_LO = 100e6, 89.3e6
f_IF = f_RF - f_LO                 # 10.7 MHz
P_fund, P_im3 = -20, -60           # dBm
IIP3 = P_fund + (P_fund - P_im3)/2 # -10 dBm
```

> **Practical insight:** sensitivity is set at the **front** (LNA noise figure);
> linearity (IP3) is usually limited at the **back** (mixer, later amps handling
> the biggest signals). Good receiver design balances both against each other.

**Next:** the cutting edge - mmWave, 5G, and radar.
""",
        ),
        _t(
            "mmWave, 5G & radar: propagation, MIMO arrays & FMCW",
            "12 min",
            """\
# mmWave, 5G & radar: propagation, MIMO arrays & FMCW

The frontier of microwave engineering is **millimeter wave (mmWave)** - roughly
30-300 GHz - where huge bandwidths enable multi-gigabit links and centimeter-
accurate radar, at the price of brutal propagation.

## mmWave propagation: bandwidth vs reach

Short wavelengths mean tiny antennas (so big arrays fit in a phone) and oceans of
spectrum - but also high path loss, and serious **atmospheric absorption** at
certain bands. Oxygen absorbs hard near **60 GHz**; water vapor peaks elsewhere.
These windows and notches shape which bands are used:

```plot
{"title": "Atmospheric attenuation peaks (oxygen ~60 GHz, water ~22/183 GHz)", "xLabel": "frequency (GHz)", "yLabel": "attenuation (dB/km, schematic)", "xRange": [10, 200], "yRange": [0, 20], "grid": true, "functions": [{"expr": "0.05 + 15*exp(-((x-60)/6)^2) + 2*exp(-((x-22)/3)^2) + 10*exp(-((x-183)/8)^2)", "label": "attenuation (schematic)", "color": "#2563eb"}]}
```

Because path loss is so high, mmWave **leans on phased arrays** (last lessons) to
form high-gain beams that recover the link - 5G mmWave is fundamentally a
beamforming technology.

## Massive MIMO and beamforming

**MIMO** (multiple-input multiple-output) uses many antennas at both ends to send
**parallel data streams** over the same frequency, multiplying capacity. **Massive
MIMO** base stations (dozens to hundreds of elements) form narrow beams per user
(**spatial multiplexing**) - the core capacity trick of 5G. Capacity grows with
the number of spatial streams and SNR (Shannon):

```plot
{"title": "MIMO capacity scales with antenna streams (slide SNR)", "xLabel": "number of spatial streams", "yLabel": "capacity (bits/s/Hz)", "xRange": [1, 16], "yRange": [0, 100], "grid": true, "controls": [{"name": "snr_dB", "range": [0, 30], "value": 15, "label": "SNR per stream (dB)"}], "functions": [{"expr": "x*log2(1 + 10^(snr_dB/10))", "label": "C ~ N log2(1 + SNR)"}]}
```

## FMCW radar: range from frequency

**Frequency-modulated continuous-wave (FMCW)** radar sweeps (chirps) the
transmit frequency linearly. The echo returns delayed, so mixing it with the
current transmit signal yields a **beat frequency** proportional to **range**:

$$f_{beat} = \\frac{2 R}{c}\\,\\frac{B}{T_{chirp}}, \\qquad
R = \\frac{c\\,f_{beat}\\,T_{chirp}}{2 B}.$$

A Doppler shift across chirps gives **velocity**. Cheap, robust, and the basis of
automotive radar at 77 GHz.

```mermaid
flowchart LR
  CHIRP["chirp generator"] --> TX["TX antenna"]
  TX --> TGT["target (delay + Doppler)"]
  TGT --> RX["RX antenna"]
  RX --> MIX["mix with TX"]
  MIX --> FFT["FFT -> range & velocity"]
```

## Real applications

- **5G mmWave**: multi-gigabit fixed wireless and dense urban capacity.
- **77 GHz automotive radar**: adaptive cruise, collision avoidance, parking.
- **60 GHz WiGig / gesture radar** (Google Soli) for short-range sensing.
- **mmWave imaging**: airport body scanners.

```matlab
B = 4e9; Tchirp = 40e-6; c = 3e8;  % 4 GHz sweep over 40 us
R = 50;                            % target range (m)
f_beat = 2*R/c * B/Tchirp          % beat frequency -> range
```

```python
import numpy as np
B, Tchirp, c = 4e9, 40e-6, 3e8     # 4 GHz sweep, 40 us chirp
R = 50                             # target range (m)
f_beat = 2*R/c * B/Tchirp          # beat frequency
```

> **Practical insight:** mmWave trades reach for bandwidth and resolution, and pays
> for it with phased-array beamforming. The same array that closes a 5G link also
> steers an automotive radar - the technologies are converging.

**Next:** put a phased array in code and steer the beam.
""",
        ),
        _code(
            "Lab: phased-array factor & beam steering",
            "13 min",
            """\
# Simulate an N-element uniform linear phased array. Plot the array factor and
# steer the beam by applying a progressive phase across the elements.
import numpy as np
import matplotlib.pyplot as plt

N = 8                              # number of elements
d_lam = 0.5                        # spacing in wavelengths (half-wave)
k = 2*np.pi                        # wavenumber * lambda (work in wavelengths)

theta = np.linspace(-np.pi/2, np.pi/2, 721)   # -90..90 deg from broadside
n = np.arange(N)

plt.figure(figsize=(8, 4.5))
for steer_deg, color in [(0, "#2563eb"), (30, "#16a34a"), (-45, "#dc2626")]:
    steer = np.deg2rad(steer_deg)
    # Progressive phase to point the beam at steer.
    beta = -k*d_lam*np.sin(steer)
    # Array factor = sum over elements of exp(j n (k d sin(theta) + beta)).
    psi = k*d_lam*np.sin(theta) + beta
    AF = np.abs(np.sum(np.exp(1j*np.outer(n, psi)), axis=0))/N
    AF_dB = 20*np.log10(np.clip(AF, 1e-3, None))
    peak = np.degrees(theta[np.argmax(AF)])
    plt.plot(np.degrees(theta), AF_dB, color=color,
             label=f"steer {steer_deg} deg (peak at {peak:.0f} deg)")

# Uniform-array first-sidelobe level is about -13 dB; mark it.
plt.axhline(-13.0, ls="--", color="#94a3b8", label="-13 dB (uniform sidelobe)")
plt.ylim(-40, 2); plt.xlabel("angle from broadside (degrees)")
plt.ylabel("|AF| (dB)"); plt.title(f"{N}-element phased array: beam steering")
plt.legend(fontsize=8); plt.grid(True); plt.show()

# Half-power beamwidth of the broadside beam.
steer = 0.0
psi = k*d_lam*np.sin(theta)
AF = np.abs(np.sum(np.exp(1j*np.outer(n, psi)), axis=0))/N
AF_dB = 20*np.log10(np.clip(AF, 1e-3, None))
above = np.degrees(theta[AF_dB > -3.0])
hpbw = above.max() - above.min()
print(f"N={N}, spacing={d_lam} lambda -> broadside HPBW ~ {hpbw:.1f} deg")
print("Steering shifts the main beam with NO moving parts (electronic scan).")

# Try it yourself:
#   1. Raise N to 16: the beam narrows (higher gain, finer steering).
#   2. Set d_lam = 0.9 and steer 45 deg: a grating lobe appears (spacing > lambda/2).
#   3. The MATLAB way: same outer-product sum; use 20*log10 and plot.
""",
        ),
        _t(
            "Applications & the throughline: from transmission line to mmWave system",
            "11 min",
            """\
# Applications & the throughline: from transmission line to mmWave system

Every concept in this track converges in real systems. This capstone walks
through a few and ties the ideas together.

## Case study 1: a 5G mmWave base station

```mermaid
flowchart LR
  BB["baseband / MIMO processor"] --> TRX["transceivers"]
  TRX --> PA["per-element power amps"]
  PA --> PH["phase shifters"]
  PH --> ARR["patch phased array"]
  ARR --> BEAM["steered beams per user"]
```

It uses **microstrip transmission lines** and **matching** to feed a **patch
array**; **phased-array beamforming** steers narrow beams to recover the harsh
**mmWave path loss**; **massive MIMO** sends parallel streams; **LNAs** set the
uplink noise floor; **circulators/duplexers** share the array between transmit and
receive. Everything you learned, in one box.

## Case study 2: automotive radar (77 GHz FMCW)

A chirp generator drives a transmit antenna; echoes mix down to a **beat
frequency** that an FFT turns into **range and velocity**. A small **patch array**
beamforms to scan azimuth. **Link budget** and **noise figure** set detection
range; **antenna sidelobes** must be low to reject road clutter.

## Case study 3: a satellite link

A ground **parabolic dish** (high aperture gain) and a low-noise **LNB** at the
feed; the **Friis equation** with huge path loss but high antenna gains closes the
link; **waveguide** runs handle high power with low loss; **polarization** reuse
doubles capacity. Deep-space links (Voyager) push this to the extreme.

## The fields where this matters

| Field | What microwave engineering provides |
|-------|-------------------------------------|
| **Wireless (5G/6G, Wi-Fi)** | the entire RF front-end and antenna array |
| **Radar** | automotive, weather, defense, altimetry |
| **Satellite & space** | links, dishes, low-noise receivers |
| **Medical** | MRI RF coils, microwave ablation, imaging |
| **Industrial** | microwave heating, sensing, RFID |
| **Test & metrology** | VNAs, spectrum analyzers, EMC compliance |

## The throughline

A signal launched onto a **transmission line**, matched so it does not reflect
(**Smith chart**, matching networks), guided by **lines, waveguides, and
components** all described by **S-parameters**, amplified with low **noise figure**
and adequate **linearity**, radiated by an **antenna** (a dipole, patch, dish, or
steerable **phased array**), across a path whose loss the **Friis budget**
predicts - that is the whole chain, from a few centimeters of trace to a beam
across deep space. The frequencies climb into **mmWave**, the antennas multiply
into **MIMO arrays**, but the physics - **Maxwell's equations**, reflection, and
matching - never changes.

> **Practical insight:** master the four pillars - **transmission lines and
> matching, S-parameters, antennas, and the link budget** - and you can read,
> design, and debug essentially any RF system. The hardware changes; these
> fundamentals do not.

**Next:** the final check.
""",
        ),
    ),
)


MICROWAVE_COURSES: tuple[SeedCourse, ...] = (
    _MICROWAVE_BASICS,
    _MICROWAVE_INTERMEDIATE,
    _MICROWAVE_ADVANCED,
)

__all__ = ["MICROWAVE_COURSES"]
