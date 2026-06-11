"""Curated Semiconductor Device Physics track: Basics, Intermediate, Advanced.

A complete device-physics curriculum: crystals and energy bands, doping and
carriers, transport, generation/recombination, and the PN junction (Basics);
the diode I-V, the BJT, the MOS capacitor and MOSFET, device capacitances, and
optoelectronics (Intermediate: Devices); short-channel scaling, power and
wide-bandgap devices, IC fabrication, SPICE modeling, reliability physics, and
real applications (Advanced). Dual MATLAB + Python throughout, with runnable
Python labs (numpy + matplotlib), interactive ```plot blocks, Mermaid diagrams,
LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time (authored separately, keyed by exact titles).
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Semiconductor Device Physics -- Basics ------------------------------------

_SEMI_BASICS = SeedCourse(
    slug="semiconductor-basics",
    title="Semiconductor Device Physics -- Basics",
    description=(
        "The physics under every chip: crystal structure and energy bands, "
        "intrinsic and extrinsic (doped) semiconductors and the Fermi level, "
        "carrier transport by drift and diffusion, generation/recombination and "
        "the continuity equation, and the PN junction at equilibrium -- with "
        "side-by-side MATLAB and Python, interactive plots, and a runnable "
        "carrier-concentration lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Crystal structure & energy bands",
            "11 min",
            """\
# Crystal structure & energy bands

A semiconductor is a **crystal**: atoms locked in a repeating lattice. Silicon,
the workhorse, sits in a **diamond cubic** lattice -- each atom shares four
covalent bonds with its neighbours. That perfect periodicity is what gives rise
to **energy bands**.

## From isolated atoms to bands

In a single atom electrons occupy sharp energy levels. Bring $10^{22}$ atoms per
cubic centimetre together and those levels split and smear into continuous
**bands** separated by **forbidden gaps**. The two that matter:

- the **valence band** -- the highest band that is full at absolute zero,
- the **conduction band** -- the next band up, empty at absolute zero,

separated by the **bandgap** $E_g$ (in electron-volts). An electron must gain at
least $E_g$ to jump the gap and become free to carry current.

$$E_g(\\text{Si}) \\approx 1.12\\ \\text{eV}, \\qquad E_g(\\text{GaAs}) \\approx 1.42\\ \\text{eV}.$$

## Conductor vs insulator vs semiconductor

The size of the gap decides everything:

| Material | Bandgap $E_g$ | At room temperature |
|----------|---------------|---------------------|
| Conductor (metal) | none (bands overlap) | swarming with free electrons |
| Semiconductor (Si) | ~1.1 eV | a few carriers, tunable by 12 orders |
| Insulator (SiO2) | ~9 eV | essentially no free carriers |

```mermaid
flowchart TB
  subgraph Conductor
    C1["conduction band"] --- C2["valence band (overlap)"]
  end
  subgraph Semiconductor
    S1["conduction band"]
    S2["valence band"]
    S1 -. "small gap ~1 eV" .- S2
  end
  subgraph Insulator
    I1["conduction band"]
    I2["valence band"]
    I1 -. "large gap ~9 eV" .- I2
  end
```

The magic of a semiconductor is that ~1 eV is *just* climbable: heat, light, or
doping can move its conductivity across a huge range. That tunability is why we
build transistors from silicon and not from copper or glass.

## Carriers come in two flavours

Excite an electron across the gap and you leave behind an empty bond -- a
**hole** -- which behaves like a mobile positive charge. Current in a
semiconductor is carried by **both** electrons (in the conduction band) and holes
(in the valence band). Almost no carriers are thermally generated unless the
material is warm enough; the population grows steeply with temperature:

```plot
{"title": "Thermal carrier population vs temperature (Boltzmann factor, slide gap)", "xLabel": "temperature T (K)", "yLabel": "relative carrier population", "xRange": [200, 600], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "Eg", "range": [0.5, 2], "value": 1.12, "label": "bandgap Eg (eV)"}], "functions": [{"expr": "exp(-Eg*5800/T)/exp(-Eg*5800/600)", "label": "exp(-Eg/2kT), normalized"}]}
```

(The $5800$ here is $1/(2k_B)$ in eV/K rescaled so the curve is visible -- the
real physics is the $\\exp(-E_g/2k_BT)$ Boltzmann factor.)

## Real-world hook

The same band picture explains **why a solar cell needs ~1.1-1.5 eV** (to match
sunlight), **why an LED's colour is set by $E_g$** (photon energy ~ gap), and
**why diamond and SiC make great high-voltage insulating-then-switching power
devices** (wide gap = high breakdown field).

```matlab
Eg = 1.12;                 % silicon bandgap (eV)
kT = 0.02585;              % thermal energy at 300 K (eV)
ratio = exp(-Eg/(2*kT));   % ~ relative intrinsic carrier factor
```

```python
import numpy as np
Eg = 1.12                  # silicon bandgap (eV)
kT = 0.02585               # thermal energy at 300 K (eV)
ratio = np.exp(-Eg/(2*kT)) # ~ relative intrinsic carrier factor
```

**Next:** filling those bands on purpose -- doping.
""",
        ),
        _t(
            "Intrinsic & extrinsic semiconductors",
            "12 min",
            """\
# Intrinsic & extrinsic semiconductors

Pure silicon is a poor conductor: at 300 K its **intrinsic carrier
concentration** is only

$$n_i \\approx 1.0\\times 10^{10}\\ \\text{cm}^{-3},$$

against ~$5\\times 10^{22}$ atoms/cm^3. The art of device physics is changing that
by 10+ orders of magnitude -- on purpose, locally -- by **doping**.

## Doping: adding the right impurity

Replace a few silicon atoms with neighbours from group V or group III:

| Dopant | Group | Adds | Makes | Majority carrier |
|--------|-------|------|-------|------------------|
| Phosphorus, Arsenic | V (5 valence e) | spare electrons (donors) | **n-type** | electrons |
| Boron, Gallium | III (3 valence e) | spare holes (acceptors) | **p-type** | holes |

A donor density $N_D$ gives (at room temperature, fully ionised)
$n \\approx N_D$ free electrons; an acceptor density $N_A$ gives $p \\approx N_A$
holes. Doping levels of $10^{15}$ to $10^{20}$ cm^{-3} set everything from a
lightly-doped drift region to an ohmic contact.

## The law of mass action

Electrons and holes are always linked. In thermal equilibrium their product is
fixed by the material and temperature, not by the doping:

$$n\\,p = n_i^2.$$

So doping n-type ($n \\uparrow$) drives holes *down* ($p = n_i^2/n$), and vice
versa. The doped (boosted) carrier is the **majority**; the suppressed one is the
**minority** -- and minority carriers, scarce as they are, run diodes and
transistors. Slide the doping and watch the two populations trade off:

```plot
{"title": "Mass action n*p = ni^2 (log10 carriers vs log10 doping)", "xLabel": "log10 donor doping Nd (cm^-3)", "yLabel": "log10 carrier density (cm^-3)", "xRange": [12, 20], "yRange": [0, 21], "grid": true, "functions": [{"expr": "x", "label": "electrons n ~ Nd", "color": "#2563eb"}, {"expr": "20 - x", "label": "holes p = ni^2/n", "color": "#dc2626"}]}
```

(Using $n_i \\approx 10^{10}$, so $\\log_{10} n_i^2 = 20$; the two lines cross at
$\\log_{10} N_D = 10$, i.e. intrinsic.)

## The Fermi level

The **Fermi level** $E_F$ is the energy at which a state has a 50% chance of being
filled. In intrinsic material it sits near mid-gap. Doping **moves** it:

- n-type: $E_F$ rises **toward the conduction band**,
- p-type: $E_F$ falls **toward the valence band**.

$$n = n_i\\,e^{(E_F - E_i)/kT}, \\qquad p = n_i\\,e^{(E_i - E_F)/kT}.$$

That shift of $E_F$ is the lever every junction pulls -- when two materials with
different $E_F$ touch, charge flows until the levels line up, building the
**built-in field** that makes diodes and transistors work.

## Real-world hook

Doping is **lithographically patterned** (ion implantation, Advanced course) so a
single wafer holds billions of precisely-doped n and p regions -- the source,
drain, well, and channel of every transistor.

```matlab
ni = 1e10; Nd = 1e17;
n = Nd;                    % majority electrons (n-type)
p = ni^2 / Nd;             % minority holes -> ~1e3 cm^-3
```

```python
ni, Nd = 1e10, 1e17
n = Nd                     # majority electrons (n-type)
p = ni**2 / Nd             # minority holes -> ~1e3 cm^-3
```

**Next:** how those carriers actually move -- transport.
""",
        ),
        _t(
            "Carrier transport: drift, diffusion & mobility",
            "12 min",
            """\
# Carrier transport: drift, diffusion & mobility

Carriers move by **two mechanisms**, and every device current is one or both.

## Drift: pushed by a field

Apply an electric field $E$ and carriers accelerate, then scatter off lattice
vibrations and impurities, reaching an average **drift velocity** proportional to
the field:

$$v_d = \\mu E,$$

where $\\mu$ is the **mobility** (cm^2/V.s). Electrons are nimbler than holes
($\\mu_n \\approx 1350$, $\\mu_p \\approx 480$ in silicon). The drift current density
adds both carriers:

$$J_{drift} = q\\,(n\\,\\mu_n + p\\,\\mu_p)\\,E = \\sigma E,$$

which is just **Ohm's law** with **conductivity** $\\sigma = q(n\\mu_n + p\\mu_p)$.
Conductivity scales straight with doping -- slide it:

```plot
{"title": "Conductivity vs doping (n-type, log10 Nd)", "xLabel": "log10 doping Nd (cm^-3)", "yLabel": "conductivity sigma (S/cm)", "xRange": [14, 19], "yRange": [0, 250], "grid": true, "controls": [{"name": "mu", "range": [200, 1400], "value": 1350, "label": "electron mobility mu (cm^2/Vs)"}], "functions": [{"expr": "0.00000000000000000016*mu*pow(10,x)", "label": "sigma = q*mu*Nd"}]}
```

(That leading constant is the electron charge $q = 1.6\\times 10^{-19}$ C written
as a decimal so the plot compiler accepts it.)

## Diffusion: spreading down a gradient

Where carrier density is uneven, random thermal motion makes carriers spread from
crowded to sparse regions -- **diffusion** -- exactly like a drop of ink in water:

$$J_{n,diff} = q\\,D_n\\,\\frac{dn}{dx}, \\qquad J_{p,diff} = -q\\,D_p\\,\\frac{dp}{dx}.$$

The **diffusion coefficient** $D$ and mobility are not independent; thermal
physics ties them by the **Einstein relation**:

$$\\frac{D}{\\mu} = \\frac{kT}{q} = V_T \\approx 0.0259\\ \\text{V at 300 K}.$$

A concentration that decays exponentially into the bulk (the minority-carrier
profile in a diode) sets up a constant diffusion current:

```plot
{"title": "Minority-carrier diffusion profile into the bulk", "xLabel": "distance x (diffusion lengths)", "yLabel": "excess carrier density (normalized)", "xRange": [0, 5], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-x)", "label": "excess n(x) ~ exp(-x/L)"}]}
```

## Velocity saturation (a preview)

$v_d = \\mu E$ only holds at low fields. Push the field hard and the velocity
**saturates** near $10^7$ cm/s (carriers dump energy to the lattice as fast as
they gain it). That ceiling caps how fast a short transistor can switch -- a
recurring theme in the Advanced course.

## Real-world hook

A **Hall-effect sensor** measures a magnetic field by deflecting drifting
carriers; a **strain gauge** and a **thermistor** exploit how $\\mu$ and carrier
density change with stress and temperature. The mobility/temperature dependence
is also why chips slow down as they heat up.

```matlab
q = 1.602e-19; mun = 1350; Nd = 1e17;
sigma = q*mun*Nd;          % conductivity (S/cm)
Dn = 0.02585*mun;          % Einstein relation -> diffusion coeff
```

```python
q, mun, Nd = 1.602e-19, 1350, 1e17
sigma = q*mun*Nd           # conductivity (S/cm)
Dn = 0.02585*mun           # Einstein relation -> diffusion coeff
```

**Next:** carriers appearing and vanishing -- generation & recombination.
""",
        ),
        _t(
            "Generation, recombination & the continuity equation",
            "12 min",
            """\
# Generation, recombination & the continuity equation

Carriers are not permanent. They are **generated** (an electron-hole pair is
created) and **recombine** (a pair annihilates). The balance of the two, plus the
transport from the last lesson, is bookkept by the **continuity equation** -- the
master equation of device physics.

## Generation and recombination

- **Generation** $G$: thermal energy, light (a photon with $h\\nu > E_g$), or
  impact ionisation lifts an electron across the gap, making a pair.
- **Recombination** $R$: an electron falls back into a hole. In silicon this is
  usually **Shockley-Read-Hall** (via trap states), set by the **minority-carrier
  lifetime** $\\tau$.

Inject excess carriers $\\Delta n$ and, left alone, they decay exponentially back
to equilibrium with that lifetime:

$$\\Delta n(t) = \\Delta n_0\\,e^{-t/\\tau}.$$

Slide the lifetime and watch the decay speed change:

```plot
{"title": "Excess-carrier recombination decay (slide lifetime tau)", "xLabel": "time (microseconds)", "yLabel": "excess carriers (normalized)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "tau", "range": [0.5, 5], "value": 2, "label": "minority lifetime tau (us)"}], "functions": [{"expr": "exp(-x/tau)", "label": "excess Dn(t) = exp(-t/tau)"}]}
```

A carrier diffuses an average **diffusion length** $L = \\sqrt{D\\tau}$ before it
recombines -- the length scale that sets a diode's stored charge and a solar
cell's collection efficiency.

## The continuity equation

Track the carrier density in a slab: it changes by what **flows in/out** (the
divergence of current) plus what is **generated minus recombined**:

$$\\frac{\\partial n}{\\partial t} = \\frac{1}{q}\\frac{\\partial J_n}{\\partial x} + G - R.$$

```mermaid
flowchart LR
  IN["carriers drift/diffuse IN"] --> BOX["slab dx"]
  GEN["generation G"] --> BOX
  BOX --> OUT["carriers drift/diffuse OUT"]
  BOX --> REC["recombination R"]
```

Combine the continuity equation with drift+diffusion and you get the
**minority-carrier diffusion equation**, whose steady-state solution is the
exponential profile from the last lesson. Every analytic device model -- the
Shockley diode, the BJT, the solar cell -- is this equation solved with the right
boundary conditions.

## Real-world hook

- **Photodiodes / solar cells**: photogeneration $G$ is the signal; you want long
  $\\tau$ and $L$ so generated carriers reach the junction before recombining.
- **LEDs**: you want fast *radiative* recombination (every recombination emits a
  photon).
- **Fast switching diodes**: you want *short* $\\tau$ so stored charge clears
  quickly (reverse recovery).

```matlab
tau = 2e-6; Dn = 35;            % lifetime, diffusion coeff (cm^2/s)
L = sqrt(Dn*tau);               % diffusion length (cm)
```

```python
import numpy as np
tau, Dn = 2e-6, 35              # lifetime, diffusion coeff
L = np.sqrt(Dn*tau)             # diffusion length
```

**Next:** put n and p together -- the PN junction.
""",
        ),
        _t(
            "The PN junction at equilibrium",
            "12 min",
            """\
# The PN junction at equilibrium

Bring a p-type and an n-type region into contact and you get the single most
important structure in electronics. Even with **no battery attached**, physics
builds a field across the boundary -- the foundation of every diode, transistor,
and solar cell.

## What happens the instant they touch

The n-side is crowded with electrons, the p-side with holes, so carriers
**diffuse** across the junction. But the atoms they leave behind are charged
(ionised donors/acceptors), so the n-side near the junction goes **positive** and
the p-side **negative**. That exposed charge is the **depletion region** (or
space-charge region) -- swept clean of mobile carriers -- and it sets up an
electric field that **opposes** further diffusion.

Equilibrium is the standoff where **drift exactly cancels diffusion**, and the
Fermi level is **flat** across the whole device.

```mermaid
flowchart LR
  P["p-side: holes, ionised acceptors (-)"] --- DEP["depletion region (built-in field ->)"]
  DEP --- N["n-side: electrons, ionised donors (+)"]
```

## The built-in potential

The energy bands bend by the **built-in potential** $V_{bi}$ across the depletion
region:

$$V_{bi} = \\frac{kT}{q}\\,\\ln\\!\\left(\\frac{N_A N_D}{n_i^2}\\right).$$

For typical silicon doping, $V_{bi} \\approx 0.6$ to $0.8$ V. Slide the doping and
watch it climb (it grows only logarithmically):

```plot
{"title": "Built-in potential vs n-side doping (Vbi = Vt ln(Na*Nd/ni^2))", "xLabel": "log10 donor doping Nd (cm^-3)", "yLabel": "Vbi (V)", "xRange": [14, 19], "yRange": [0, 1], "grid": true, "controls": [{"name": "logNa", "range": [14, 19], "value": 16, "label": "log10 acceptor doping Na"}], "functions": [{"expr": "0.02585*ln(pow(10,x)*pow(10,logNa)/100000000000000000000)", "label": "Vbi (V)"}]}
```

(The $10^{20}$ in the denominator is $n_i^2$ with $n_i = 10^{10}$, written out so
the plot compiler accepts it.)

## Depletion width

For a one-sided abrupt junction the depletion region spreads mostly into the
**lightly doped** side. Its width grows with the voltage across it (built-in plus
any reverse bias):

$$W = \\sqrt{\\frac{2\\varepsilon_s}{q}\\left(\\frac{N_A + N_D}{N_A N_D}\\right)(V_{bi} - V)}.$$

Reverse-biasing **widens** $W$; forward-biasing **shrinks** it. That voltage-
dependent width is a voltage-controlled charge -- i.e. a **capacitor** (the
junction capacitance, key to varactors and the next course).

## Real-world hook

The depletion region is the diode's "valve seat," the BJT's base-collector
isolation, the CMOS well isolation, and the light-collecting volume of a
photodiode or solar cell. A reverse-biased junction is also a **radiation
detector** (each particle creates a pulse of carriers in the depletion volume) --
how CCD/CMOS imagers and particle detectors work.

```matlab
kT_q = 0.02585; ni = 1e10; Na = 1e16; Nd = 1e17;
Vbi = kT_q * log(Na*Nd/ni^2);   % ~0.75 V
```

```python
import numpy as np
kT_q, ni, Na, Nd = 0.02585, 1e10, 1e16, 1e17
Vbi = kT_q * np.log(Na*Nd/ni**2)  # ~0.75 V
```

**Next:** see carrier concentration and Fermi-Dirac statistics come alive in code.
""",
        ),
        _code(
            "Lab: carrier concentration & Fermi-Dirac vs temperature",
            "13 min",
            """\
# Explore semiconductor statistics: the intrinsic carrier concentration ni(T),
# the Fermi-Dirac occupation, and how doped carriers freeze out / saturate.
# Pure numpy + matplotlib, module level only.
import numpy as np
import matplotlib.pyplot as plt

# Physical constants (eV-based units keep the numbers friendly)
kB = 8.617e-5          # Boltzmann constant (eV/K)
Eg = 1.12              # silicon bandgap (eV)
Nc = 2.8e19            # conduction-band effective DOS at 300 K (cm^-3)
Nv = 1.04e19           # valence-band effective DOS at 300 K (cm^-3)

# 1) Intrinsic carrier concentration vs temperature: ni = sqrt(Nc Nv) exp(-Eg/2kT)
T = np.linspace(250, 600, 400)
kT = kB * T
Nc_T = Nc * (T/300.0)**1.5         # effective DOS scales as T^1.5
Nv_T = Nv * (T/300.0)**1.5
ni = np.sqrt(Nc_T * Nv_T) * np.exp(-Eg/(2*kT))

ni_300 = np.interp(300.0, T, ni)
print(f"intrinsic ni at 300 K ~ {ni_300:.3e} cm^-3 (textbook ~1e10)")

# 2) Fermi-Dirac occupation f(E) at a few temperatures (E measured from E_F)
E = np.linspace(-0.3, 0.3, 400)    # energy relative to Fermi level (eV)
fd = {}
for Tx in (100.0, 300.0, 600.0):
    fd[Tx] = 1.0 / (1.0 + np.exp(E/(kB*Tx)))

# 3) Electrons in an n-type sample vs T: freeze-out -> extrinsic -> intrinsic
Nd = 1e15
n_majority = 0.5*Nd + np.sqrt((0.5*Nd)**2 + ni**2)   # charge neutrality + mass action
print(f"electrons at 300 K (Nd=1e15) ~ {np.interp(300.0, T, n_majority):.3e} cm^-3")
print(f"electrons at 600 K          ~ {np.interp(600.0, T, n_majority):.3e} cm^-3 (intrinsic takes over)")

fig, ax = plt.subplots(1, 3, figsize=(13, 4))

ax[0].semilogy(T, ni, color="#2563eb")
ax[0].set_xlabel("temperature (K)"); ax[0].set_ylabel("ni (cm^-3)")
ax[0].set_title("Intrinsic carrier conc. ni(T)"); ax[0].grid(True, which="both")

for Tx, color in zip((100.0, 300.0, 600.0), ("#16a34a", "#2563eb", "#dc2626")):
    ax[1].plot(E, fd[Tx], color=color, label=f"T = {Tx:.0f} K")
ax[1].axvline(0.0, ls="--", color="#94a3b8")
ax[1].set_xlabel("E - E_F (eV)"); ax[1].set_ylabel("occupation f(E)")
ax[1].set_title("Fermi-Dirac distribution"); ax[1].legend(); ax[1].grid(True)

ax[2].semilogy(T, n_majority, color="#dc2626", label="n (Nd=1e15)")
ax[2].semilogy(T, ni, color="#94a3b8", ls="--", label="ni (intrinsic)")
ax[2].set_xlabel("temperature (K)"); ax[2].set_ylabel("electron density (cm^-3)")
ax[2].set_title("Doped carriers vs intrinsic"); ax[2].legend(); ax[2].grid(True, which="both")

plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Raise Eg to 3.26 (SiC): ni plummets -> why wide-bandgap parts handle heat.
#   2. Lower Nd to 1e12: the doped curve meets the intrinsic curve sooner.
#   3. The MATLAB way: same arithmetic with .* and ./, semilogy() for the plots.
""",
        ),
    ),
)


# -- Semiconductor Device Physics -- Intermediate: Devices ---------------------

_SEMI_INTERMEDIATE = SeedCourse(
    slug="semiconductor-intermediate",
    title="Semiconductor Device Physics -- Intermediate: Devices",
    description=(
        "From junction to device: the diode I-V and the Shockley equation, BJT "
        "physics and current gain, the MOS capacitor and MOSFET (inversion, "
        "threshold, channel, I-V), device capacitances and high-frequency limits, "
        "and optoelectronics (LED, photodiode, solar cell) -- with dual "
        "MATLAB/Python, interactive plots, and a runnable diode/MOSFET I-V lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "PN junction I-V and the diode",
            "12 min",
            """\
# PN junction I-V and the diode

Apply a voltage to the equilibrium junction and the standoff breaks. The result
is the **diode**: an exponential, one-way current.

## Forward and reverse bias

- **Forward bias** (p-side positive): the applied voltage **opposes** the built-in
  field, shrinking the depletion region. Majority carriers flood across, get
  injected as minority carriers, and recombine -- current rises **exponentially**.
- **Reverse bias** (p-side negative): the applied voltage **adds** to the built-in
  field, widening depletion. Only a tiny **saturation current** $I_S$ leaks.

The whole curve is the **Shockley diode equation**:

$$I = I_S\\left(e^{V/(n V_T)} - 1\\right), \\qquad V_T = \\frac{kT}{q} \\approx 26\\ \\text{mV}.$$

The ideality factor $n$ is 1 (ideal diffusion) to 2 (recombination-dominated).
The exponential gives the famous **knee** near 0.6-0.7 V for silicon:

```plot
{"title": "Diode I-V: the exponential forward knee (slide ideality n)", "xLabel": "diode voltage V (V)", "yLabel": "current (mA)", "xRange": [-0.2, 0.8], "yRange": [-2, 60], "grid": true, "controls": [{"name": "n", "range": [1, 2], "value": 1, "label": "ideality factor n"}], "functions": [{"expr": "0.00000001*(exp(x/(n*0.02585)) - 1)", "label": "I = Is(exp(V/nVt)-1), mA"}]}
```

## Saturation current and temperature

$I_S$ scales with $n_i^2$, so it **doubles roughly every 5-8 K**. That is why a
diode's forward drop **falls about 2 mV per degree C** at fixed current -- the
basis of a cheap temperature sensor, and a headache for current mirrors.

## Breakdown

Push reverse bias far enough and current suddenly soars at the **breakdown
voltage** $V_{BR}$, by two mechanisms:

- **Avalanche** -- carriers gain enough energy to knock out more carriers (impact
  ionisation); dominant above ~6 V.
- **Zener (tunneling)** -- in heavily-doped, thin junctions, electrons tunnel
  straight through; dominant below ~5 V.

```mermaid
stateDiagram-v2
  [*] --> Reverse
  Reverse --> Forward: V > 0 (knee ~0.7V)
  Reverse --> Breakdown: V < -Vbr
  Forward --> Reverse: V < 0
```

## Real-world hook

- **Rectifiers** turn AC to DC (power supplies).
- **Zener / TVS diodes** clamp and protect (deliberate breakdown).
- **Schottky diodes** (metal-semiconductor) have a low ~0.3 V drop and no stored
  charge -- fast switching supplies.
- **Varactors** use the bias-dependent junction capacitance to tune RF circuits.

```matlab
Is = 1e-12; Vt = 0.02585; n = 1;
V = linspace(-0.2, 0.8, 200);
I = Is*(exp(V/(n*Vt)) - 1);     % Shockley equation (A)
```

```python
import numpy as np
Is, Vt, n = 1e-12, 0.02585, 1
V = np.linspace(-0.2, 0.8, 200)
I = Is*(np.exp(V/(n*Vt)) - 1)   # Shockley equation
```

**Next:** stack two junctions -- the BJT.
""",
        ),
        _t(
            "BJT physics: injection & current gain",
            "12 min",
            """\
# BJT physics: injection & current gain

A **bipolar junction transistor** is two PN junctions sharing a thin middle
layer: **emitter-base-collector** (NPN or PNP). Its genius is **minority-carrier
injection** across a base thin enough that carriers cross it before recombining.

## How it works (NPN, active region)

1. The **base-emitter** junction is **forward** biased: the heavily-doped emitter
   injects a flood of electrons into the thin, lightly-doped base.
2. The **base-collector** junction is **reverse** biased.
3. Because the base is **thin** (much less than a diffusion length), almost all
   injected electrons diffuse across and are swept into the collector before they
   can recombine. Only a tiny fraction recombines, supplied by the base current.

So a **small base current controls a large collector current**:

$$I_C = \\beta\\,I_B, \\qquad I_E = I_C + I_B = (\\beta + 1)\\,I_B,$$

with current gain $\\beta$ (or $h_{FE}$) typically 50-300. The collector current
also follows an exponential in $V_{BE}$ (it is a forward-biased junction):

$$I_C = I_S\\,e^{V_{BE}/V_T}.$$

```mermaid
flowchart LR
  E["emitter (n+) : injects electrons"] --> B["base (p, thin)"]
  B --> C["collector (n) : collects them"]
  IB["small base current"] --> B
```

## The output characteristic and the Early effect

Sweep $V_{CE}$ at fixed $I_B$ and $I_C$ stays nearly flat (a current source) once
past **saturation** (~0.2 V). The gentle upward slope is the **Early effect**: more
$V_{CE}$ widens the base-collector depletion, thinning the effective base, nudging
$I_C$ up. Slide the base drive and watch the family of curves shift:

```plot
{"title": "BJT output characteristic Ic vs Vce (slide base current)", "xLabel": "Vce (V)", "yLabel": "Ic (mA)", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "controls": [{"name": "Ib", "range": [10, 80], "value": 40, "label": "base current Ib (uA)"}], "functions": [{"expr": "(x>0.2)*0.1*Ib*(1 + x/80)", "label": "Ic = beta*Ib*(1 + Vce/Va)"}]}
```

## Gummel and the limits of beta

Gain is not free: $\\beta$ falls at very low and very high currents, varies with
temperature, and spreads enormously part-to-part. Good circuits never rely on a
specific $\\beta$ -- they use feedback (the Electronics track's biasing lesson).

## Real-world hook

BJTs dominate where you want **low noise and high transconductance**: audio and RF
amplifiers, precision references (the **bandgap reference** exploits the
predictable $V_{BE}$ temperature drift), high-speed logic (ECL), and as the output
stage of many op-amps. Power BJTs and **Darlington pairs** switch motors and lamps.

```matlab
beta = 150; Ib = 40e-6;
Ic = beta*Ib;                   % 6 mA collector current
Ie = (beta+1)*Ib;               % emitter current
```

```python
beta, Ib = 150, 40e-6
Ic = beta*Ib                    # 6 mA collector current
Ie = (beta+1)*Ib                # emitter current
```

**Next:** the device in every chip -- the MOSFET.
""",
        ),
        _t(
            "The MOS capacitor & MOSFET physics",
            "13 min",
            """\
# The MOS capacitor & MOSFET physics

The **MOSFET** is the most-manufactured object in history. Its heart is the **MOS
capacitor**: metal (gate) / oxide (insulator) / semiconductor (body). Understand
the capacitor and the transistor falls out.

## The MOS capacitor: three regimes

Apply a gate voltage to a MOS capacitor over p-type silicon and the surface passes
through three states:

| Gate voltage | Surface state | What is there |
|--------------|---------------|---------------|
| Negative | **accumulation** | holes pile up at the surface |
| Small positive | **depletion** | surface swept clean, a depletion layer grows |
| Large positive ($> V_{th}$) | **inversion** | electrons gather -- an n-type channel forms |

The gate voltage at which the surface **inverts** (becomes n-type at a p body) is
the **threshold voltage** $V_{th}$. Above it, a conductive **channel** of
electrons connects source to drain.

```mermaid
stateDiagram-v2
  [*] --> Accumulation
  Accumulation --> Depletion: Vg rises past 0
  Depletion --> Inversion: Vg > Vth (channel forms)
  Inversion --> Depletion: Vg < Vth
```

## The MOSFET I-V

With a channel formed, the drain voltage $V_{DS}$ pushes current through it. Two
regions:

- **Triode / linear** ($V_{DS} < V_{GS} - V_{th}$): the channel acts like a
  voltage-controlled resistor.
  $$I_D = k\\left[(V_{GS}-V_{th})V_{DS} - \\tfrac{1}{2}V_{DS}^2\\right].$$
- **Saturation** ($V_{DS} \\ge V_{GS} - V_{th}$): the channel **pinches off** at the
  drain; current saturates and depends (to first order) only on the gate:
  $$I_D = \\tfrac{1}{2}k\\,(V_{GS}-V_{th})^2, \\qquad k = \\mu C_{ox}\\frac{W}{L}.$$

That square-law saturation current is the amplifier's workhorse. Slide $V_{GS}$ to
move between the family of curves; note the parabolic onset then the flat plateau:

```plot
{"title": "MOSFET output characteristic Id vs Vds (slide Vgs), Vth=1", "xLabel": "Vds (V)", "yLabel": "Id (mA)", "xRange": [0, 5], "yRange": [0, 12], "grid": true, "controls": [{"name": "Vgs", "range": [1, 4], "value": 3, "label": "gate voltage Vgs (V)"}], "functions": [{"expr": "(Vgs>1)*((x < (Vgs-1))*2*((Vgs-1)*x - 0.5*x*x) + (x >= (Vgs-1))*(Vgs-1)*(Vgs-1))", "label": "Id (triode then saturation)"}]}
```

And the transfer curve -- the square-law turn-on above threshold (slide $V_{th}$):

```plot
{"title": "MOSFET transfer: Id = 0.5 k (Vgs - Vth)^2 in saturation (slide Vth)", "xLabel": "Vgs (V)", "yLabel": "Id (mA)", "xRange": [0, 5], "yRange": [0, 18], "grid": true, "controls": [{"name": "Vth", "range": [0.5, 3], "value": 1, "label": "threshold Vth (V)"}], "functions": [{"expr": "(x>Vth)*2*(x-Vth)*(x-Vth)", "label": "Id (saturation)"}]}
```

## What sets the threshold

$V_{th}$ depends on the gate-body work-function difference, the oxide thickness and
charge, the body doping, and the **body bias** (the body effect: reverse-biasing
the body raises $V_{th}$). Setting $V_{th}$ precisely is a central goal of the
fabrication process (Advanced course).

## Real-world hook

MOSFETs are **everything digital** (CMOS logic = complementary n- and p-MOS),
**power switching** (a power MOSFET's on-resistance $R_{DS(on)}$ sets supply
efficiency), and **analog** (the square law gives gain). The same device, scaled,
is in a wristwatch and a data-center GPU.

```matlab
k = 1e-3; Vth = 1; Vgs = 3;     % device params
Id_sat = 0.5*k*(Vgs - Vth)^2;   % saturation current (A)
```

```python
k, Vth, Vgs = 1e-3, 1, 3
Id_sat = 0.5*k*(Vgs - Vth)**2   # saturation current
```

**Next:** what limits how fast these devices run -- capacitances.
""",
        ),
        _t(
            "Device capacitances & high-frequency limits",
            "11 min",
            """\
# Device capacitances & high-frequency limits

A transistor that switched instantly would be magic. Real devices are slowed by
**capacitances** that must be charged and discharged through finite resistance.
Understanding them tells you a device's top speed.

## Where the capacitance comes from

Two sources:

- **Junction (depletion) capacitance** -- a reverse-biased junction is a charged
  depletion region whose width changes with voltage. It **decreases** as reverse
  bias widens the depletion layer:
  $$C_j = \\frac{C_{j0}}{\\sqrt{1 - V/V_{bi}}}.$$
- **Gate-oxide capacitance** -- the MOS gate is literally a parallel-plate
  capacitor, $C_{ox} = \\varepsilon_{ox}/t_{ox}$ per area, plus overlap and
  channel capacitances ($C_{gs}$, $C_{gd}$).

The voltage-dependent junction capacitance is exactly the **varactor** -- a
voltage-tuned capacitor for oscillators and RF tuning. Slide the built-in voltage
and see the curve shape:

```plot
{"title": "Junction capacitance vs reverse bias Cj = Cj0/sqrt(1 - V/Vbi)", "xLabel": "applied voltage V (V), reverse = negative", "yLabel": "Cj / Cj0", "xRange": [-5, 0.5], "yRange": [0, 3], "grid": true, "controls": [{"name": "Vbi", "range": [0.6, 1], "value": 0.8, "label": "built-in potential Vbi (V)"}], "functions": [{"expr": "1/sqrt(1 - x/Vbi)", "label": "Cj/Cj0"}]}
```

## The figures of merit

How fast a device can switch is captured by two frequencies:

- **Transition frequency** $f_T$ -- where the current gain falls to 1. For a BJT
  $f_T = g_m/(2\\pi C)$; for a MOSFET $f_T \\approx \\mu (V_{GS}-V_{th})/(2\\pi L^2)$ --
  note the **$1/L^2$**: shorter channels are dramatically faster, the engine of
  Moore's law.
- **Maximum oscillation frequency** $f_{max}$ -- where power gain falls to 1.

```plot
{"title": "Transition frequency fT vs channel length (fT ~ 1/L^2)", "xLabel": "channel length L (relative)", "yLabel": "relative fT", "xRange": [0.2, 2], "yRange": [0, 30], "grid": true, "functions": [{"expr": "1/(x*x)", "label": "fT ~ 1/L^2"}]}
```

## The RC speed limit

A logic gate's delay is roughly $\\tau \\approx R_{on} C_{load}$: the driving
transistor's on-resistance charging the next gate's input capacitance plus wire
capacitance. Shrinking devices cuts $C$ but interconnect $RC$ grows -- which is
why wires, not transistors, now often set the clock.

## Real-world hook

- **RF transistors and amplifiers** live and die by $f_T$/$f_{max}$ (mobile radios,
  radar, mm-wave 5G).
- **Varactors** tune the local oscillator in every radio and phase-locked loop.
- **Gate charge** $Q_g$ -- the integral of gate capacitance -- sets the driver
  current and switching loss in power converters.

```matlab
Cj0 = 2e-12; Vbi = 0.8; V = -3;
Cj = Cj0 / sqrt(1 - V/Vbi);     % junction cap at -3 V reverse
```

```python
import numpy as np
Cj0, Vbi, V = 2e-12, 0.8, -3
Cj = Cj0 / np.sqrt(1 - V/Vbi)   # junction cap at -3 V reverse
```

**Next:** devices that trade carriers for photons -- optoelectronics.
""",
        ),
        _t(
            "Optoelectronic devices: LED, photodiode & solar cell",
            "12 min",
            """\
# Optoelectronic devices: LED, photodiode & solar cell

The PN junction also connects electricity and **light**. Run carriers and photons
together and you get LEDs, photodiodes, and solar cells -- the same junction, used
in different quadrants of its I-V curve.

## Photon energy meets the bandgap

A photon is absorbed only if it carries at least the bandgap energy; an emitted
photon carries about the bandgap energy:

$$E_{photon} = h\\nu = \\frac{hc}{\\lambda} \\approx E_g, \\qquad \\lambda(\\mu m) \\approx \\frac{1.24}{E_g(\\text{eV})}.$$

So the gap sets the colour. Slide the bandgap and read off the wavelength
(everything left of visible is infrared, right is ultraviolet):

```plot
{"title": "Emission/absorption wavelength vs bandgap: lambda = 1.24/Eg", "xLabel": "bandgap Eg (eV)", "yLabel": "wavelength (um)", "xRange": [0.5, 3.5], "yRange": [0, 2.5], "grid": true, "functions": [{"expr": "1.24/x", "label": "lambda (um)"}], "points": [{"x": 1.42, "y": 0.873, "label": "GaAs (near-IR)", "color": "#dc2626", "size": 7}, {"x": 2.25, "y": 0.551, "label": "green", "color": "#16a34a", "size": 7}]}
```

## The three devices

- **LED** -- forward-biased **direct-bandgap** material (GaAs, GaN, InGaN);
  injected carriers recombine **radiatively**, emitting photons. Silicon is an
  *indirect* gap -- it recombines without light, which is why LEDs are not silicon.
- **Photodiode** -- reverse-biased; incoming photons generate carriers in the
  depletion region, producing a photocurrent proportional to light intensity. Fast
  and linear: optical receivers, light meters, barcode scanners.
- **Solar cell** -- a large photodiode operated **without** bias, in the
  power-generating (fourth) quadrant: light delivers both a current and a voltage.

## The solar cell I-V and the maximum power point

A solar cell's current is the diode equation **minus** the photogenerated current:

$$I = I_S\\left(e^{V/V_T} - 1\\right) - I_{ph}.$$

The illuminated curve dips into the power-generating region; the
**maximum-power-point** (MPP) is the knee, tracked by every solar inverter:

```plot
{"title": "Solar cell I-V under illumination (slide photocurrent / sunlight)", "xLabel": "cell voltage V (V)", "yLabel": "current (A), generating = negative", "xRange": [0, 0.7], "yRange": [-4, 1], "grid": true, "controls": [{"name": "Iph", "range": [1, 4], "value": 3, "label": "photocurrent Iph (A, ~sunlight)"}], "functions": [{"expr": "0.000000001*(exp(x/0.02585) - 1) - Iph", "label": "I = Is(exp(V/Vt)-1) - Iph"}]}
```

The useful corners are the **short-circuit current** $I_{SC}$ (at $V=0$) and the
**open-circuit voltage** $V_{OC}$ (where $I=0$); their product times the **fill
factor** is the output power.

## Real-world hook

LEDs (lighting, displays, lidar), laser diodes (fiber optics, Blu-ray), photodiodes
and avalanche photodiodes (optical comms, medical imaging), CMOS image sensors
(every phone camera), and photovoltaics (rooftop to grid scale) -- a multi-hundred-
billion-dollar industry built on this one junction.

```matlab
Is = 1e-9; Vt = 0.02585; Iph = 3; V = 0.5;
I = Is*(exp(V/Vt) - 1) - Iph;   % solar cell current (A)
```

```python
import numpy as np
Is, Vt, Iph, V = 1e-9, 0.02585, 3, 0.5
I = Is*(np.exp(V/Vt) - 1) - Iph  # solar cell current
```

**Next:** plot real device I-V curves from these equations.
""",
        ),
        _code(
            "Lab: diode & MOSFET I-V from the device equations",
            "13 min",
            """\
# Plot device I-V curves straight from the physics: the Shockley diode equation
# and the MOSFET square-law (triode + saturation). Pure numpy + matplotlib.
import numpy as np
import matplotlib.pyplot as plt

Vt = 0.02585           # thermal voltage at 300 K (V)

# --- 1) Diode I-V: vary the ideality factor n ---
Is = 1e-12
Vd = np.linspace(-0.2, 0.75, 400)

# --- 2) MOSFET output family: Id vs Vds for several Vgs ---
k = 2e-3               # transconductance parameter (A/V^2)
Vth = 1.0
Vds = np.linspace(0, 5, 400)
Vgs_list = [1.5, 2.0, 2.5, 3.0]

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))

for n, color in zip((1.0, 1.5, 2.0), ("#2563eb", "#16a34a", "#dc2626")):
    Id = Is*(np.exp(Vd/(n*Vt)) - 1.0)
    ax[0].plot(Vd, Id*1e3, color=color, label=f"n = {n}")
ax[0].set_xlabel("diode voltage (V)"); ax[0].set_ylabel("current (mA)")
ax[0].set_ylim(-2, 60); ax[0].set_title("Diode I-V (Shockley)")
ax[0].axhline(0, color="#94a3b8", lw=0.8); ax[0].legend(); ax[0].grid(True)

for Vgs, color in zip(Vgs_list, ("#0ea5e9", "#16a34a", "#f59e0b", "#dc2626")):
    Vov = Vgs - Vth                                   # overdrive
    triode = k*(Vov*Vds - 0.5*Vds**2)
    sat = 0.5*k*Vov**2 * np.ones_like(Vds)
    Id = np.where(Vds < Vov, triode, sat)
    Id = np.clip(Id, 0, None)
    ax[1].plot(Vds, Id*1e3, color=color, label=f"Vgs = {Vgs} V")
ax[1].set_xlabel("Vds (V)"); ax[1].set_ylabel("Id (mA)")
ax[1].set_title(f"MOSFET output family (Vth = {Vth} V)")
ax[1].legend(); ax[1].grid(True)

plt.tight_layout(); plt.show()

# Saturation current at one bias, printed for reference
Vgs0 = 3.0
Id_sat = 0.5*k*(Vgs0 - Vth)**2
print(f"diode current at 0.7 V (n=1) = {Is*(np.exp(0.7/Vt)-1)*1e3:.2f} mA")
print(f"MOSFET Id,sat at Vgs={Vgs0} V  = {Id_sat*1e3:.2f} mA")

# Try it yourself:
#   1. Halve Vth: every MOSFET curve jumps up (more overdrive at the same Vgs).
#   2. Raise k (wider W/L): steeper triode slope, higher saturation current.
#   3. The MATLAB way: use exp(), element-wise .* ./, and the function step().
""",
        ),
    ),
)


# -- Semiconductor Device Physics -- Advanced ----------------------------------

_SEMI_ADVANCED = SeedCourse(
    slug="semiconductor-advanced",
    title="Semiconductor Device Physics -- Advanced: Scaling, Fabrication & Reliability",
    description=(
        "The frontier: short-channel effects and Moore-law scaling (leakage, DIBL, "
        "velocity saturation), power and wide-bandgap devices (SiC/GaN, the IGBT), "
        "IC fabrication (litho, implant, oxidation, etch, deposition, the CMOS "
        "flow), device modeling and SPICE (BSIM, extraction), reliability physics "
        "(hot carriers, electromigration, TDDB, ESD), and real applications -- with "
        "dual MATLAB/Python, interactive plots, and a runnable scaling lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Short-channel effects & scaling",
            "13 min",
            """\
# Short-channel effects & scaling

For decades the industry shrank the MOSFET on a schedule -- **Moore's law**:
transistor count per chip roughly doubling every ~2 years. The physics that makes
shrinking *useful*, and the physics that fights it, are this lesson.

## Dennard scaling -- the golden age

The original recipe (Dennard, 1974): scale every dimension and the voltage by the
same factor $1/\\kappa$. Then per-transistor delay, power, and area all fall
together -- more transistors, faster, at constant power **density**. A transistor
count doubling every two years looks like this:

```plot
{"title": "Moore's law: transistor count doubles every ~2 years (log scale)", "xLabel": "years from start", "yLabel": "log10 transistors", "xRange": [0, 30], "yRange": [3, 11], "grid": true, "functions": [{"expr": "3 + x*0.1505", "label": "log10(count): doubling / 2 yr"}]}
```

## Why scaling got hard

Below ~1 V and ~100 nm, the clean picture breaks:

- **Velocity saturation** -- carriers hit their ~$10^7$ cm/s ceiling, so $I_D$ grows
  only **linearly** (not quadratically) with overdrive, and gets longer-channel-like.
- **DIBL (drain-induced barrier lowering)** -- in a short channel the drain field
  reaches across and lowers the source barrier, so $V_{th}$ **drops** as $V_{DS}$
  rises (the gate loses some control).
- **Subthreshold leakage** -- below threshold $I_D$ falls *exponentially*, not to
  zero, set by the **subthreshold swing** $S$ (mV/decade). Lower $V_{th}$ for speed
  means **exponentially more** off-state leakage. Slide the swing:

```plot
{"title": "Subthreshold current: Id falls exponentially below Vth (slide swing S)", "xLabel": "gate voltage Vgs (V), Vth = 0.4", "yLabel": "log10 Id (arb)", "xRange": [0, 0.4], "yRange": [-9, 0], "grid": true, "controls": [{"name": "S", "range": [60, 120], "value": 90, "label": "subthreshold swing S (mV/decade)"}], "functions": [{"expr": "(x - 0.4)*1000/S", "label": "log10 Id = (Vgs - Vth)/S"}]}
```

The **60 mV/decade** floor (at room temperature) is a thermodynamic limit for a
classical MOSFET -- the reason supply voltage stopped scaling and power density
plateaued (the "power wall").

## How the industry kept going

When Dennard scaling stalled (~2005), invention took over:

- **Strained silicon** and **high-k/metal-gate** (replace SiO2 with HfO2 to cut gate
  leakage while keeping capacitance).
- **3D transistors** -- **FinFET**, then **gate-all-around (GAA) nanosheets** -- wrap
  the gate around the channel for far better electrostatic control of leakage.
- **Multi-core, then specialised accelerators** -- architecture instead of frequency.

```mermaid
flowchart LR
  PLANAR["planar MOSFET"] --> FINFET["FinFET (3D fin)"]
  FINFET --> GAA["gate-all-around nanosheet"]
  GAA --> NEXT["CFET / stacked devices"]
```

## Real-world hook

Every "5 nm" or "3 nm" process node, every leakage-vs-speed trade in a phone SoC's
power management, and every data-center power bill is governed by this lesson.

```matlab
S = 90; Vth = 0.4; Vgs = 0.2;        % subthreshold swing (mV/dec)
logId = (Vgs - Vth)*1000/S;          % decades below the on-current
Ioff_ratio = 10^logId;               % off/on current ratio
```

```python
S, Vth, Vgs = 90, 0.4, 0.2
logId = (Vgs - Vth)*1000/S           # decades below on-current
Ioff_ratio = 10**logId               # off/on current ratio
```

**Next:** the other extreme -- high power and wide bandgaps.
""",
        ),
        _t(
            "Power & wide-bandgap devices",
            "12 min",
            """\
# Power & wide-bandgap devices

Logic shrinks toward zero volts; **power electronics** goes the other way --
hundreds to thousands of volts, tens to hundreds of amps. Different physics
dominates, and a new class of materials is taking over.

## What a power device must do

A power switch wants to be a perfect switch: zero drop when on, zero current when
off, instant transitions, and able to hold off a high voltage. Real silicon trades
these off:

- A **power MOSFET** -- low on-resistance $R_{DS(on)}$, fast, but $R_{DS(on)}$ rises
  steeply with rated voltage in silicon (the "silicon limit").
- The **IGBT (insulated-gate bipolar transistor)** -- a MOSFET gate driving a BJT
  output. It gets the easy voltage drive of a MOSFET **and** the low conduction drop
  of a bipolar at high current -- the workhorse of motor drives, trains, and welders
  from ~600 V to several kV.

```mermaid
flowchart LR
  GATE["MOS gate (easy voltage drive)"] --> IGBT["IGBT"]
  IGBT --> OUT["bipolar output (low Vce drop, high current)"]
```

## The breakdown / on-resistance trade-off

Holding off high voltage needs a thick, lightly-doped **drift region** -- which
adds resistance. The on-resistance of a unipolar device scales roughly as the
**square (or worse) of the rated voltage**:

```plot
{"title": "Specific on-resistance vs rated voltage (lower is better)", "xLabel": "rated breakdown voltage (relative)", "yLabel": "relative Ron-area", "xRange": [1, 10], "yRange": [0, 60], "grid": true, "controls": [{"name": "Ecrit", "range": [1, 10], "value": 1, "label": "critical field (x vs silicon)"}], "functions": [{"expr": "x*x/(Ecrit*Ecrit)", "label": "Ron ~ V^2 / Ecrit^2"}]}
```

## Wide-bandgap: SiC and GaN

The breakthrough is materials with a **bigger bandgap**, and so a **higher critical
breakdown field** $E_{crit}$ (~10x silicon). A higher $E_{crit}$ lets the drift
region be **thinner and more heavily doped** for the same voltage -- collapsing
$R_{DS(on)}$:

| Material | $E_g$ (eV) | Strength |
|----------|-----------|----------|
| Silicon | 1.12 | cheap, mature |
| **SiC** (silicon carbide) | 3.26 | high voltage, high temperature, rugged |
| **GaN** (gallium nitride) | 3.4 | very fast, high frequency, compact |

Wider gap also means **lower intrinsic carrier concentration**, so devices keep
working at **higher temperature** (less leakage) -- crucial under the hood of a car
or in a satellite.

## Real-world hook

- **SiC** -- electric-vehicle traction inverters (Tesla, etc.), solar inverters,
  grid converters. Smaller, cooler, more efficient than silicon IGBTs.
- **GaN** -- the tiny, cool phone "fast chargers," data-center power, RF power
  amplifiers in 5G base stations and radar.
- **IGBTs** -- still king for the very highest power (rail traction, HVDC, industrial
  drives).

```matlab
Eg_si = 1.12; Eg_sic = 3.26;
Ecrit_ratio = (Eg_sic/Eg_si)^2;      % SiC critical field ~ Eg^2-ish higher
Ron_improvement = Ecrit_ratio^2;     % Ron drops ~ Ecrit^2
```

```python
Eg_si, Eg_sic = 1.12, 3.26
Ecrit_ratio = (Eg_sic/Eg_si)**2      # critical field gain
Ron_improvement = Ecrit_ratio**2     # Ron drops ~ Ecrit^2
```

**Next:** how any of these get built -- IC fabrication.
""",
        ),
        _t(
            "IC fabrication & the CMOS process flow",
            "13 min",
            """\
# IC fabrication & the CMOS process flow

A chip is built **layer by layer** on a silicon wafer, repeating a small set of
unit steps dozens to hundreds of times. Understanding the steps demystifies why a
transistor looks and behaves the way it does.

## The unit steps

| Step | What it does | How |
|------|--------------|-----|
| **Oxidation** | grow insulating SiO2 | heat the wafer in oxygen/steam |
| **Photolithography** | print a pattern | coat photoresist, expose through a **mask**, develop |
| **Etch** | remove material in the pattern | plasma (dry) or chemical (wet) etch |
| **Ion implantation** | dope selectively | fire dopant ions, then **anneal** to activate |
| **Deposition** | add a film (metal, oxide, poly) | CVD, PVD/sputtering, ALD |
| **CMP** | flatten the surface | chemical-mechanical polish |

Lithography is the **pattern-defining** step and the one that sets the node: the
smallest feature is limited by the exposure wavelength and optics. The industry
moved from deep-UV (193 nm, with multi-patterning tricks) to **EUV (13.5 nm)** to
keep printing ever-smaller features.

```mermaid
flowchart LR
  OXIDE["grow oxide"] --> RESIST["coat photoresist"]
  RESIST --> EXPOSE["expose through mask (litho)"]
  EXPOSE --> DEV["develop"]
  DEV --> ETCH["etch"]
  ETCH --> IMPLANT["implant + anneal"]
  IMPLANT --> STRIP["strip resist"]
  STRIP --> REPEAT["repeat for next layer"]
```

## Ion implantation -- doping by the numbers

Dopants are ionised, accelerated to keV-MeV energies, and slammed into the wafer.
Energy sets the **depth**, dose sets the **concentration**. The implant lands in a
roughly Gaussian profile about a projected range $R_p$; a thermal **anneal** then
repairs lattice damage and activates the dopants. Slide the implant energy (range)
and watch the doping profile move deeper:

```plot
{"title": "Implant doping profile (Gaussian); slide implant energy / range", "xLabel": "depth into wafer (relative)", "yLabel": "dopant concentration (normalized)", "xRange": [0, 4], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "Rp", "range": [0.3, 3], "value": 1, "label": "projected range Rp (energy)"}], "functions": [{"expr": "exp(-(x-Rp)*(x-Rp)/0.3)", "label": "N(x) ~ exp(-(x-Rp)^2/2dRp^2)"}]}
```

## Thermal oxidation -- the Deal-Grove growth

Oxide grows fast at first (reaction-limited) then slows (diffusion-limited, as
oxygen must cross the existing oxide). The thickness follows a square-root-like law
in time -- a classic Deal-Grove curve:

```plot
{"title": "Thermal oxide growth: thin film linear, thick film sqrt(time)", "xLabel": "oxidation time (relative)", "yLabel": "oxide thickness (relative)", "xRange": [0, 10], "yRange": [0, 4], "grid": true, "functions": [{"expr": "sqrt(1 + 1.5*x) - 1", "label": "thickness ~ Deal-Grove"}]}
```

## The CMOS flow in one breath

Define wells (n-well, p-well) -> grow gate oxide -> deposit and pattern the
**polysilicon (or metal) gate** -> implant lightly-doped source/drain extensions ->
spacers -> heavy source/drain implant + anneal -> silicide the contacts -> then
**back-end-of-line**: many layers of oxide and metal interconnect, separated by
vias, tied together by CMP. A modern chip has 10-20 metal layers above the
transistors.

## Real-world hook

This is a multi-hundred-billion-dollar global industry: **fabs** costing tens of
billions, **EUV scanners** (ASML) costing hundreds of millions each, and a supply
chain whose disruption stalls cars and electronics worldwide. **Yield** -- the
fraction of working dies -- is the economic heartbeat of the whole business.

```matlab
q = 1.602e-19; dose = 1e13; depth = 100e-7;   % atoms/cm^2, cm
peak_conc = dose/depth;                        % rough peak doping (cm^-3)
```

```python
q, dose, depth = 1.602e-19, 1e13, 100e-7      # atoms/cm^2, cm
peak_conc = dose/depth                         # rough peak doping (cm^-3)
```

**Next:** turning these devices into equations a simulator can use -- SPICE models.
""",
        ),
        _t(
            "Device modeling & SPICE models",
            "12 min",
            """\
# Device modeling & SPICE models

A circuit designer never re-derives device physics for every simulation. Instead
the physics is packaged into a **compact model** -- equations plus extracted
parameters -- that **SPICE** evaluates millions of times. This lesson bridges the
device physics you have learned to the models that engineers actually use.

## Model levels: a hierarchy of fidelity

| Level | Captures | Use |
|-------|----------|-----|
| **Square-law (Shichman-Hodges)** | the basic MOSFET I-V | hand analysis, teaching |
| **Level 2/3** | short-channel, mobility degradation | older nodes |
| **BSIM3/4/CMG** | DIBL, velocity sat, leakage, FinFET/GAA | modern foundry decks |
| **EKV / PSP** | continuous all-region, surface-potential | analog/RF precision |

**BSIM** (Berkeley Short-channel IGFET Model) is the industry standard -- a foundry
ships a **process design kit (PDK)** with hundreds of BSIM parameters per device,
fit to measured silicon.

```mermaid
flowchart LR
  PHYS["device physics"] --> MODEL["compact model (e.g. BSIM)"]
  MEAS["measured silicon"] --> EXTRACT["parameter extraction"]
  EXTRACT --> MODEL
  MODEL --> SPICE["SPICE: solve the circuit"]
```

## Parameter extraction

Extraction fits model parameters to measured I-V and C-V curves. For a MOSFET you
extract $V_{th}$, the transconductance parameter, mobility degradation, the DIBL
coefficient, and so on -- typically by sweeping bias and fitting regions of the
curve. A simple example: $V_{th}$ is the gate-voltage intercept of the linear-region
$I_D$ vs $V_{GS}$ extrapolation. Slide a fitted threshold against "measured" data:

```plot
{"title": "Vth extraction: fit a line, read the intercept (slide model Vth)", "xLabel": "Vgs (V)", "yLabel": "Id (mA)", "xRange": [0, 4], "yRange": [0, 12], "grid": true, "controls": [{"name": "Vth_fit", "range": [0.5, 2.5], "value": 1, "label": "model Vth (V)"}], "functions": [{"expr": "(x>Vth_fit)*4*(x-Vth_fit)", "label": "model: Id ~ (Vgs - Vth_fit)"}], "series": [{"points": [[1, 0], [1.5, 2], [2, 4], [2.5, 6], [3, 8], [3.5, 10]], "label": "measured data", "color": "#dc2626"}]}
```

## Temperature and corners

Models also carry **temperature coefficients** ($V_{th}$, mobility, and $I_S$ all
drift) and **process corners** -- the foundry characterises fast/slow N and P
transistors (FF, SS, FS, SF, TT) so designers can verify the circuit works across
the full manufacturing spread, not just the typical case.

## Real-world hook

Every chip you own was signed off in SPICE against a foundry PDK across corners,
voltages, and temperatures (**PVT**) before tape-out. Verilog-A lets engineers
write custom compact models for new devices (memristors, GaN HEMTs, photodiodes)
that standard simulators do not yet ship.

```matlab
% Square-law model evaluated like SPICE would, with a temperature shift
Vth0 = 1.0; tc = -2e-3; T = 85;       % Vth drifts -2 mV/degC
Vth = Vth0 + tc*(T - 27);
k = 2e-3; Vgs = 3;
Id = 0.5*k*max(0, Vgs - Vth)^2;
```

```python
Vth0, tc, T = 1.0, -2e-3, 85          # Vth drifts -2 mV/degC
Vth = Vth0 + tc*(T - 27)
k, Vgs = 2e-3, 3
Id = 0.5*k*max(0, Vgs - Vth)**2
```

**Next:** what wears a chip out -- reliability physics.
""",
        ),
        _t(
            "Reliability physics: hot carriers, electromigration, TDDB & ESD",
            "12 min",
            """\
# Reliability physics: hot carriers, electromigration, TDDB & ESD

A chip that works on day one must keep working for ten years. **Reliability
physics** studies the slow (and fast) wear-out mechanisms, so designers can keep
fields, currents, and temperatures inside safe limits.

## The wear-out mechanisms

- **Hot-carrier injection (HCI)** -- in the high field near the drain, carriers gain
  enough energy to be injected into the gate oxide, trapping charge and **shifting
  $V_{th}$** over time. Worse for short channels and high voltage.
- **Bias-temperature instability (NBTI/PBTI)** -- gate-bias + temperature slowly
  creates oxide/interface traps, again drifting $V_{th}$. A leading aging mechanism
  in modern nodes.
- **Time-dependent dielectric breakdown (TDDB)** -- the gate oxide accumulates
  defects under field until a conductive path punches through and the gate fails.
- **Electromigration (EM)** -- high current density in a metal wire literally pushes
  metal atoms along, opening voids (and growing hillocks) until the wire fails. Set
  by **Black's equation**.

## Acceleration: why heat and field are the enemy

Most mechanisms accelerate with temperature via an **Arrhenius** law, and EM also
with current density (Black's equation):

$$\\text{MTTF} = \\frac{A}{J^{n}}\\,\\exp\\!\\left(\\frac{E_a}{k_B T}\\right).$$

Lifetime falls **exponentially** as temperature rises -- a few tens of degrees can
halve it. Slide the activation energy and watch how steeply lifetime drops with
temperature:

```plot
{"title": "Arrhenius lifetime vs temperature (slide activation energy Ea)", "xLabel": "temperature (deg C)", "yLabel": "relative log10 lifetime", "xRange": [25, 150], "yRange": [-4, 1], "grid": true, "controls": [{"name": "Ea", "range": [0.3, 1.2], "value": 0.7, "label": "activation energy Ea (eV)"}], "functions": [{"expr": "Ea*5040*(1/(x+273) - 1/398)", "label": "log10 MTTF (Arrhenius)"}]}
```

(The $5040$ folds in $1/(k_B \\ln 10)$ in eV/K so the curve is readable; reference
temperature 125 C = 398 K.)

Electromigration risk rises sharply with current density, so wide power rails and
current-density design rules exist for exactly this:

```plot
{"title": "Electromigration MTTF vs current density (Black's law, slide exponent)", "xLabel": "current density J (relative)", "yLabel": "relative MTTF", "xRange": [1, 5], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "nexp", "range": [1, 2], "value": 2, "label": "Black exponent n"}], "functions": [{"expr": "1/pow(x, nexp)", "label": "MTTF ~ 1/J^n"}]}
```

## ESD -- the fast killer

**Electrostatic discharge** is the *sudden* failure: a few kilovolts from a human
touch dump amps into a pin in nanoseconds, blowing oxides and melting junctions.
Chips include on-die **ESD protection** (clamps and diodes that shunt the surge to
the rails) and fabs enforce grounded wrist-straps and ionisers.

```mermaid
stateDiagram-v2
  [*] --> Healthy
  Healthy --> Aged: HCI / NBTI / EM (years)
  Healthy --> Dead: ESD / TDDB punch-through (instant)
  Aged --> Dead: parameter drift past spec
```

## Real-world hook

Reliability physics sets a chip's **operating voltage, max current density, and
junction-temperature limits**, and the **burn-in** and qualification tests
(JEDEC). Automotive (AEC-Q100), aerospace, and medical parts are derated and
screened far harder than consumer parts for exactly these mechanisms.

```matlab
Ea = 0.7; kB = 8.617e-5;              % activation energy (eV), Boltzmann
T1 = 273+55; T2 = 273+125;
accel = exp(Ea/kB*(1/T1 - 1/T2));     % how much faster aging is at 125C vs 55C
```

```python
import numpy as np
Ea, kB = 0.7, 8.617e-5                # eV, Boltzmann (eV/K)
T1, T2 = 273+55, 273+125
accel = np.exp(Ea/kB*(1/T1 - 1/T2))   # aging acceleration 125C vs 55C
```

**Next:** simulate scaling and subthreshold leakage yourself.
""",
        ),
        _code(
            "Lab: MOSFET scaling & subthreshold leakage",
            "14 min",
            """\
# Simulate the central tension of scaling: lowering Vth speeds a gate up but
# raises off-state leakage exponentially. Plus a velocity-saturation drain current.
# Pure numpy + matplotlib, module level only.
import numpy as np
import matplotlib.pyplot as plt

kT_q = 0.02585          # thermal voltage (V)
Vdd = 1.0               # supply

# --- 1) Subthreshold I-V: exponential below Vth, set by the swing S ---
Vgs = np.linspace(0, 1.0, 400)
S_list = [70, 90, 110]                          # mV/decade
Vth = 0.35
Ion = 1e-3              # on-current reference (A)

# --- 2) Drain current with velocity saturation vs ideal square law ---
Vov = np.linspace(0, 0.7, 400)                  # gate overdrive Vgs - Vth
k = 2e-3
Esat = 0.5                                       # saturation "knee" overdrive
Id_ideal = 0.5*k*Vov**2
Id_velsat = 0.5*k*Vov**2 / (1 + Vov/Esat)        # velocity-saturated: more linear

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))

for S, color in zip(S_list, ("#16a34a", "#2563eb", "#dc2626")):
    # log10(Id) = log10(Ion) + (Vgs - Vth)/(S/1000) for Vgs < Vth, capped at Ion
    log_id = np.log10(Ion) + (Vgs - Vth)/(S/1000.0)
    Id = np.minimum(10**log_id, Ion)
    ax[0].semilogy(Vgs, Id, color=color, label=f"S = {S} mV/dec")
ax[0].axvline(Vth, ls="--", color="#94a3b8", label="Vth")
ax[0].set_xlabel("Vgs (V)"); ax[0].set_ylabel("Id (A, log)")
ax[0].set_title("Subthreshold leakage vs swing S")
ax[0].legend(); ax[0].grid(True, which="both")

# report the off-current (Vgs = 0) for each swing -- the leakage penalty
for S in S_list:
    Ioff = 10**(np.log10(Ion) + (0 - Vth)/(S/1000.0))
    print(f"S = {S} mV/dec -> Ioff at Vgs=0 is {Ioff:.2e} A ({Ion/Ioff:.0e}x below Ion)")

ax[1].plot(Vov, Id_ideal*1e3, color="#94a3b8", ls="--", label="ideal square law")
ax[1].plot(Vov, Id_velsat*1e3, color="#dc2626", label="velocity saturated")
ax[1].set_xlabel("gate overdrive Vgs - Vth (V)"); ax[1].set_ylabel("Id (mA)")
ax[1].set_title("Velocity saturation flattens Id")
ax[1].legend(); ax[1].grid(True)

plt.tight_layout(); plt.show()

# Gate-delay scaling estimate: tau ~ C*Vdd/Ion, with C falling as 1/kappa
kappa = np.array([1.0, 1.4, 2.0, 2.8])           # successive scaling factors
rel_delay = 1.0/kappa                            # delay improves ~ 1/kappa
print("relative gate delay across nodes:", np.round(rel_delay, 3))

# Try it yourself:
#   1. Raise Vth to 0.5: Ioff drops a lot, but on-current overdrive shrinks (slower).
#   2. Shrink Esat: velocity saturation bites earlier (shorter channel).
#   3. The MATLAB way: semilogy(), element-wise .^ and ./, min()/max().
""",
        ),
        _t(
            "Applications & the throughline",
            "11 min",
            """\
# Applications & the throughline

You have walked from a single covalent bond to a billion-transistor chip. This
final lesson ties the physics to the devices that run the modern world, and to the
one idea that connects them all.

## One junction, a whole industry

Almost everything in this track is the **PN junction and the MOS structure**, used
in different ways:

| Device | Built from | Powers |
|--------|-----------|--------|
| Diode / rectifier | one PN junction | every power supply |
| BJT | two junctions, thin base | analog, RF, references |
| MOSFET / CMOS | MOS capacitor + channel | all digital, most analog |
| Power MOSFET / IGBT / SiC / GaN | thick drift + gate | EVs, grid, chargers, motors |
| LED / laser diode | direct-gap junction | lighting, displays, fiber, lidar |
| Photodiode / solar cell / image sensor | reverse junction + light | cameras, comms, photovoltaics |
| Memory cell (DRAM/Flash) | capacitor / floating gate | all storage |

```mermaid
flowchart TB
  PHYS["bands, doping, carriers, junctions"] --> DIODE["diodes"]
  PHYS --> BJT["BJTs"]
  PHYS --> MOS["MOSFETs / CMOS"]
  PHYS --> OPTO["optoelectronics"]
  MOS --> LOGIC["CPUs, GPUs, memory"]
  MOS --> POWER["power conversion (with SiC/GaN)"]
  OPTO --> LIGHT["lighting, displays, solar, sensors"]
```

## Worked theme: where the physics shows up in a phone

A single smartphone is this whole track at once:

- **CMOS logic** (the SoC) -- billions of scaled FinFET/GAA MOSFETs, every one a
  threshold-voltage and leakage trade-off (Advanced lessons 1 and 6).
- **Power management** -- buck converters using fast switching MOSFETs/GaN, junction
  capacitances and gate charge setting efficiency (Intermediate lesson 4).
- **Camera** -- a CMOS image sensor: millions of reverse-biased photodiodes
  (Intermediate lesson 6, Basics lesson 6).
- **Display** -- OLED/LED emission set by the bandgap (Basics lesson 1).
- **Radio (5G/Wi-Fi)** -- GaN and SiGe RF transistors chosen for $f_T$ (Intermediate
  lesson 4).
- **Battery charger brick** -- a GaN switch (Advanced lesson 2).

## The throughline

Charge in a periodic crystal forms **bands**; **doping** moves the Fermi level and
sets the carrier populations; carriers move by **drift and diffusion**, appear and
vanish by **generation and recombination**, all bookkept by the **continuity
equation**; joining n and p builds a **junction** with a built-in field; bias that
junction (or gate a channel) and you get **diodes, transistors, and light-emitters**;
**scale** them and the same physics gives both Moore's law and the leakage that
fights it; **build** them with litho/implant/oxide/etch; **model** them in SPICE; and
**keep** them alive against hot carriers, electromigration, and ESD.

The materials and dimensions change every few years. The physics -- bands, carriers,
junctions, and fields -- does not. Master it once and every new device, from a
GaN charger to a quantum dot to a 2D-material transistor, is a variation on a theme
you already know.

## Where to go next

Build the **circuits** around these devices (the Electronics track), the **signals**
they process, and the **control** loops they close. Device physics is the floor the
whole electronic world stands on.
""",
        ),
    ),
)


SEMICONDUCTOR_COURSES: tuple[SeedCourse, ...] = (
    _SEMI_BASICS,
    _SEMI_INTERMEDIATE,
    _SEMI_ADVANCED,
)

__all__ = ["SEMICONDUCTOR_COURSES"]
