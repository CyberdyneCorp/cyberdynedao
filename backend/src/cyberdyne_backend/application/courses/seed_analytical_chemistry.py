"""Analytical & Instrumental Chemistry track: Basics -> Intermediate -> Advanced.

A three-level analytical-chemistry track. Basics builds measurement intuition —
significant figures, error and uncertainty, calibration, acid-base equilibria
and the chemistry of separations. Intermediate develops the core quantitative
instrumental methods — Beer-Lambert spectrophotometry, chromatography (HPLC/GC)
with the van Deemter equation, and potentiometric/voltammetric electrochemistry.
Advanced reaches mass spectrometry, NMR and the LC-MS/NMR-driven omics pipelines
that feed machine-learning analysis. Lessons are `text` with LaTeX, interactive
```plot blocks (calibration lines, peaks, decay) and ```mermaid pipeline/process
diagrams.
"""

# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Analytical & Instrumental Chemistry — Basics ──────────  (pH = −log[H+]) ──

_BASICS = SeedCourse(
    slug="analytical-chemistry-basics",
    title="Analytical & Instrumental Chemistry — Basics",
    description=(
        "The measurement foundations of analytical chemistry: significant "
        "figures and the analytical process, random vs systematic error and "
        "uncertainty, calibration with the least-squares line, the mole and "
        "solution concentration, acid-base equilibria and buffers, and the "
        "partition principle behind every separation. Interactive plots and "
        "process diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The analytical process & significant figures",
            "10 min",
            r"""
# The analytical process & significant figures

Analytical chemistry answers two questions about a sample: **what is in it**
(qualitative) and **how much** (quantitative). A real analysis is a pipeline,
not a single measurement — sampling, sample preparation, the actual measurement,
and finally turning a signal into a concentration with calibration and
statistics.

```mermaid
flowchart LR
  A["Define problem"] --> B["Sampling"]
  B --> C["Sample prep / dissolution"]
  C --> D["Measurement (signal)"]
  D --> E["Calibration & statistics"]
  E --> F["Result + uncertainty"]
```

Every measured value carries **significant figures** that encode its precision.
The digits you are sure of, plus the first uncertain one, are significant: a
balance reading of $1.2340\,\text{g}$ has five. Rules of thumb: leading zeros are
never significant ($0.0042$ has two), trailing zeros after a decimal point are
($4.20$ has three). In addition/subtraction keep the fewest decimal places; in
multiplication/division keep the fewest significant figures.

A result is only as trustworthy as its weakest step — over-reporting digits a
method cannot support is a classic beginner error. Treat the figures you write
as a claim about how well you actually know the number.

**Next:** separating random scatter from systematic bias.
""",
        ),
        _t(
            "Error, precision & uncertainty",
            "11 min",
            r"""
# Error, precision & uncertainty

No measurement is exact. **Random error** scatters repeated readings about a
central value and is quantified by the standard deviation $s$; **systematic
error** (bias) shifts every reading the same way — a miscalibrated pipette, an
interfering species. Random error limits **precision**; systematic error limits
**accuracy**.

For $n$ replicates the sample mean and standard deviation are

$$\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i, \qquad
s=\sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2}.$$

The **relative standard deviation** $\text{RSD}=s/\bar{x}$ (often as a
percentage) lets you compare precision across methods. Replicate results cluster
as a Gaussian; the curve below shows how often a reading lands near the true
value:

```plot
{"title": "Distribution of replicate measurements", "xLabel": "deviation from mean (in s)", "yLabel": "relative frequency", "xRange": [-4, 4], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-(x*x)/2)", "label": "normal curve", "color": "#2563eb"}]}
```

Total **uncertainty** propagates from each step. For a sum $y=a+b$ the variances
add: $u_y^2=u_a^2+u_b^2$. For a product $y=ab$ the *relative* uncertainties add
in quadrature: $(u_y/y)^2=(u_a/a)^2+(u_b/b)^2$. A confidence interval reports the
result as $\bar{x}\pm t\,s/\sqrt{n}$ using Student's $t$.

**Next:** turning a signal into a concentration with calibration.
""",
        ),
        _t(
            "Calibration & the standard curve",
            "11 min",
            r"""
# Calibration & the standard curve

An instrument gives a **signal** (absorbance, peak area, current); calibration
maps signal back to **concentration**. The classic external-standard method
measures a series of known standards and fits a straight line by **ordinary
least squares**:

$$y = m\,c + b,$$

where $m$ is the sensitivity (signal per unit concentration) and $b$ the
intercept (often a blank). Slide the standards along this line — an unknown's
signal is read across to its concentration:

```plot
{"title": "External-standard calibration line", "xLabel": "concentration c (mg/L)", "yLabel": "signal y", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1.1*x + 0.4", "label": "y = m c + b", "color": "#2563eb"}]}
```

Quality of the fit is judged by the correlation coefficient $r$ (want
$|r|>0.995$) and, more honestly, by the residuals — they should be random, not
curved. The **limit of detection** is the smallest concentration giving a signal
distinguishable from the blank, conventionally $\text{LOD}=3\sigma_{\text{blank}}/m$,
and the **limit of quantitation** $\text{LOQ}=10\sigma_{\text{blank}}/m$.

When the sample matrix changes the slope (matrix effects), **standard addition**
spikes known amounts directly into the sample and extrapolates to zero signal.
An **internal standard** corrects for run-to-run variation by ratioing the
analyte signal to a fixed added reference.

**Next:** the mole, concentration and how we express amounts.
""",
        ),
        _t(
            "Moles, concentration & solutions",
            "10 min",
            r"""
# Moles, concentration & solutions

Quantitative chemistry counts particles in **moles**: one mole is Avogadro's
number $N_A = 6.022\times10^{23}$ entities. The amount $n$ relates to mass $m$
through the molar mass $M$:

$$n = \frac{m}{M}.$$

The workhorse concentration unit is **molarity**, $c = n/V$ (mol/L). Trace work
uses mass concentration (mg/L $\approx$ ppm in water) or molality (mol per kg
solvent, temperature-independent). **Dilution** conserves moles, so the master
relation is

$$c_1 V_1 = c_2 V_2.$$

This linear law means a fixed dilution factor scales concentration
proportionally — useful when an unknown reads off the top of a calibration
range:

```plot
{"title": "Serial dilution: concentration vs added solvent", "xLabel": "dilution factor", "yLabel": "concentration (relative)", "xRange": [1, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/x", "label": "c = c0 / DF", "color": "#16a34a"}]}
```

Preparing a standard well is half of analytical accuracy: weigh a primary
standard to constant mass, dissolve quantitatively, and dilute to the mark in a
volumetric flask at a controlled temperature.

```mermaid
flowchart LR
  S["Weigh primary standard"] --> D["Dissolve fully"]
  D --> V["Dilute to mark (volumetric flask)"]
  V --> ST["Stock solution c1"]
  ST --> W["Working standards by c1 V1 = c2 V2"]
```

**Next:** equilibrium — acids, bases and buffers.
""",
        ),
        _t(
            "Acid-base equilibria & buffers",
            "11 min",
            r"""
# Acid-base equilibria & buffers

Most aqueous analysis happens at a controlled **pH**, defined as
$\text{pH}=-\log_{10}[\text{H}^+]$. Water self-ionises with
$K_w=[\text{H}^+][\text{OH}^-]=1.0\times10^{-14}$ at 25 °C, so neutral is
pH 7. A weak acid HA dissociates with

$$K_a=\frac{[\text{H}^+][\text{A}^-]}{[\text{HA}]}, \qquad \text{p}K_a=-\log_{10}K_a.$$

A **buffer** — a weak acid with its conjugate base — resists pH change. The
**Henderson-Hasselbalch** equation gives its pH:

$$\text{pH}=\text{p}K_a+\log_{10}\frac{[\text{A}^-]}{[\text{HA}]}.$$

Buffering is strongest when $[\text{A}^-]\approx[\text{HA}]$, i.e. near
pH $=\text{p}K_a$. A titration curve makes this visible: the steep jump is the
equivalence point, and the flat region around $\text{p}K_a$ is the buffer zone:

```plot
{"title": "Weak-acid titration curve (sigmoidal)", "xLabel": "fraction of base added", "yLabel": "pH", "xRange": [0, 10], "yRange": [2, 12], "grid": true, "functions": [{"expr": "4.7 + 4/(1+exp(-(x-5)))", "label": "pH vs titrant", "color": "#2563eb"}]}
```

Choosing a buffer means matching $\text{p}K_a$ to the target pH and providing
enough **capacity** (concentration) to absorb the protons released during the
analysis.

**Next:** the partition principle behind every separation.
""",
        ),
        _t(
            "Separations & the partition principle",
            "10 min",
            r"""
# Separations & the partition principle

Real samples are mixtures; analysis usually needs the analyte **separated** from
interferences first. Every separation rests on one idea: a species distributes
between two phases according to a **partition (distribution) coefficient**

$$K_D=\frac{[\text{A}]_{\text{stationary}}}{[\text{A}]_{\text{mobile}}}.$$

Two species with different $K_D$ travel at different effective speeds and pull
apart. **Liquid-liquid extraction** shakes the sample with an immiscible
solvent; the fraction extracted depends on $K_D$ and the phase-volume ratio, and
multiple small extractions beat one large one. **Solid-phase extraction (SPE)**
traps analytes on a sorbent cartridge, washes away matrix, then elutes a clean
concentrate.

```mermaid
flowchart LR
  M["Mixture in mobile phase"] --> P["Contact stationary phase"]
  P --> R["Partition by K_D"]
  R --> F["Fast species (low K_D)"]
  R --> S["Slow species (high K_D)"]
  F --> O["Separated outputs"]
  S --> O
```

Repeating partition continuously along a column turns a single equilibrium into
thousands of stages — the basis of chromatography. The more a species favours
the stationary phase, the longer it is retained, and a larger spread in $K_D$
gives cleaner resolution.

```plot
{"title": "Fraction extracted vs partition coefficient", "xLabel": "partition coefficient K_D", "yLabel": "fraction extracted", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating extraction", "color": "#16a34a"}]}
```

**Next:** a quick check of the basics.
""",
        ),
        _quiz(),
    ),
)


# ── Analytical & Instrumental Chemistry — Intermediate ───────────────────────

_INTERMEDIATE = SeedCourse(
    slug="analytical-chemistry-intermediate",
    title="Analytical & Instrumental Chemistry — Intermediate",
    description=(
        "The core quantitative instrumental methods: UV-Vis spectrophotometry "
        "and the Beer-Lambert law, the chromatographic theory of retention, "
        "resolution and the van Deemter equation, practical HPLC and GC, and "
        "electroanalytical methods from potentiometry to cyclic voltammetry. "
        "Worked equations, calibration and instrument diagrams throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Spectrophotometry & the Beer-Lambert law",
            "11 min",
            r"""
# Spectrophotometry & the Beer-Lambert law

UV-Vis spectrophotometry measures how much light a solution absorbs.
**Transmittance** is $T=I/I_0$ and **absorbance** $A=-\log_{10}T$. The
**Beer-Lambert law** makes absorbance linear in concentration:

$$A=\varepsilon\,b\,c,$$

where $\varepsilon$ is the molar absorptivity (L mol⁻¹ cm⁻¹), $b$ the path
length (cm) and $c$ the molar concentration. Because $A$ is linear in $c$, a
single calibration line converts measured absorbance into concentration:

```plot
{"title": "Beer-Lambert: absorbance vs concentration", "xLabel": "concentration c (mol/L x 1e-4)", "yLabel": "absorbance A", "xRange": [0, 10], "yRange": [0, 2], "grid": true, "functions": [{"expr": "0.18*x", "label": "A = e b c", "color": "#2563eb"}]}
```

The law is only linear at modest $A$ (roughly $A<1$). At high concentration,
analyte association, stray light and polychromatic source effects bend the curve
downward — a real limitation, not noise. You also choose the wavelength of
maximum absorption $\lambda_{\max}$ for best sensitivity and stability.

```mermaid
flowchart LR
  L["Light source"] --> MC["Monochromator (select lambda)"]
  MC --> C["Sample cuvette (path b)"]
  C --> D["Detector (I)"]
  D --> A["A = -log(I/I0)"]
```

**Next:** the theory of chromatographic separation.
""",
        ),
        _t(
            "Chromatographic theory: retention & resolution",
            "12 min",
            r"""
# Chromatographic theory: retention & resolution

A chromatogram plots detector signal against time; each analyte elutes as a peak
at its **retention time** $t_R$. Subtracting the column dead time $t_M$ gives the
**retention factor**

$$k=\frac{t_R-t_M}{t_M},$$

a dimensionless measure of how strongly the analyte is retained. The relative
retention of two peaks is the **selectivity** $\alpha=k_2/k_1$.

Peak sharpness is captured by the **plate number** $N=16\,(t_R/w)^2$ (with $w$
the baseline width), and the column length per plate is the plate height
$H=L/N$ — smaller $H$ means more efficient separation. Two peaks are resolved
when their **resolution**

$$R_s=\frac{1}{4}\sqrt{N}\;\frac{\alpha-1}{\alpha}\;\frac{k_2}{1+k_2}$$

reaches about $1.5$ (baseline separation). This **master resolution equation**
shows the three independent handles: efficiency ($N$), selectivity ($\alpha$)
and retention ($k$). A model two-peak chromatogram:

```plot
{"title": "Two overlapping chromatographic peaks", "xLabel": "time (min)", "yLabel": "detector signal", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-(x-4)^2/0.3)", "label": "peak 1", "color": "#2563eb"}, {"expr": "exp(-(x-6)^2/0.3)", "label": "peak 2", "color": "#dc2626"}]}
```

Selectivity (changing the chemistry of the phases) is the most powerful lever;
brute-force efficiency helps but costs pressure and time.

**Next:** trading speed against efficiency — the van Deemter equation.
""",
        ),
        _t(
            "Band broadening & the van Deemter equation",
            "11 min",
            r"""
# Band broadening & the van Deemter equation

Why not just run the mobile phase as fast as possible? Because plate height $H$
(band broadening) depends on the linear velocity $u$ through the **van Deemter
equation**:

$$H = A + \frac{B}{u} + C\,u.$$

The **A term** (eddy diffusion) is broadening from multiple flow paths through
the packing — minimised by small, uniform particles. The **B term**
(longitudinal diffusion) dominates at low velocity, as analyte diffuses along
the column the longer it sits. The **C term** (mass-transfer resistance) grows
with velocity because the analyte cannot equilibrate fast enough between phases.

Their sum has a minimum: an **optimum velocity** $u_{\text{opt}}$ giving the
lowest $H$ (highest efficiency). The classic U-shaped curve:

```plot
{"title": "van Deemter curve: plate height vs velocity", "xLabel": "linear velocity u (mm/s)", "yLabel": "plate height H (um)", "xRange": [0.3, 6], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1.5 + 3/x + 1.1*x", "label": "H = A + B/u + C u", "color": "#2563eb"}]}
```

Modern sub-2-µm particles (UHPLC) flatten the C term, so columns stay efficient
at high speed — at the price of very high backpressure. In GC, where diffusion in
gas is fast, the B term matters more and the optimum is shifted.

```mermaid
flowchart LR
  A["A: eddy diffusion"] --> H["Total plate height H"]
  B["B/u: longitudinal diffusion"] --> H
  C["C u: mass transfer"] --> H
  H --> O["Minimum at u_opt"]
```

**Next:** putting it to work — HPLC and GC instruments.
""",
        ),
        _t(
            "HPLC & GC in practice",
            "11 min",
            r"""
# HPLC & GC in practice

Two instrument families dominate. **HPLC** (high-performance liquid
chromatography) pumps a liquid mobile phase at high pressure through a packed
column; **reversed-phase** HPLC (a nonpolar C18 stationary phase, polar
water/acetonitrile mobile phase) is the default for most organic analytes.
**Gradient elution** ramps the mobile-phase strength over the run so early and
late peaks both come off sharply.

**GC** (gas chromatography) carries volatile, thermally stable analytes in an
inert gas (He, H₂) through a long capillary column inside a programmable oven;
temperature programming plays the role gradients play in HPLC.

```mermaid
flowchart LR
  I["Injector"] --> P["Pump / carrier gas"]
  P --> COL["Column (stationary phase)"]
  COL --> DET["Detector"]
  DET --> DATA["Chromatogram + integration"]
```

Detector choice sets sensitivity and selectivity: UV/diode-array and
fluorescence for HPLC; flame-ionisation (FID) and electron-capture (ECD) for GC;
and mass spectrometry coupled to either (LC-MS, GC-MS) for identification.
Quantitation integrates peak area, which is proportional to amount over the
linear range:

```plot
{"title": "Peak area vs injected amount", "xLabel": "injected amount (ng)", "yLabel": "peak area", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1.15*x", "label": "linear response", "color": "#2563eb"}]}
```

Method robustness comes from controlling temperature, flow, injection volume and
column condition — the unglamorous discipline behind reproducible data.

**Next:** measuring with electrons — electroanalysis.
""",
        ),
        _t(
            "Potentiometry & ion-selective electrodes",
            "11 min",
            r"""
# Potentiometry & ion-selective electrodes

Electroanalytical methods read chemistry as a voltage or current.
**Potentiometry** measures the potential of an indicator electrode at
(essentially) zero current, relative to a stable reference. For a redox or
ion-sensing electrode the response follows the **Nernst equation**:

$$E = E^{\circ} - \frac{RT}{nF}\ln Q
   \;=\; E^{\circ} - \frac{0.0592}{n}\log_{10}Q \quad(\text{at }25\,^{\circ}\text{C}),$$

so potential is **linear in the log of activity**. The glass **pH electrode** is
the everyday example: its potential changes about −59 mV per pH unit.
**Ion-selective electrodes (ISEs)** extend this to F⁻, K⁺, Ca²⁺ and many others
with selective membranes.

Because the signal is logarithmic, calibration is a line of $E$ versus
$\log c$:

```plot
{"title": "Nernstian electrode response", "xLabel": "log(concentration)", "yLabel": "potential E (mV)", "xRange": [-6, 0], "yRange": [-100, 280], "grid": true, "functions": [{"expr": "-59*x", "label": "E vs log c (n=1)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  IND["Indicator electrode (e.g. ISE)"] --> CELL["Electrochemical cell (sample)"]
  REF["Reference electrode"] --> CELL
  CELL --> V["High-impedance voltmeter"]
  V --> E["E -> activity via Nernst"]
```

A key strength is that potentiometry senses **activity**, not just
concentration; ionic strength buffers (e.g. TISAB for fluoride) keep activity
coefficients constant so readings track concentration.

**Next:** sweeping the potential — voltammetry.
""",
        ),
        _t(
            "Voltammetry & cyclic voltammetry",
            "11 min",
            r"""
# Voltammetry & cyclic voltammetry

In **voltammetry** we *apply* a potential to a working electrode and measure the
resulting **current**, which reports how fast a species is oxidised or reduced.
**Cyclic voltammetry (CV)** sweeps the potential linearly up and back down,
tracing a current-potential loop that fingerprints the electrochemistry.

For a reversible, diffusion-controlled couple the peak current obeys the
**Randles-Sevcik equation**:

$$i_p = 2.69\times10^{5}\,n^{3/2}\,A\,D^{1/2}\,C\,v^{1/2},$$

so peak current scales with the **square root of scan rate** $v$ and linearly
with concentration $C$ — a diagnostic of diffusion control:

```plot
{"title": "Randles-Sevcik: peak current vs sqrt(scan rate)", "xLabel": "scan rate v (V/s)", "yLabel": "peak current i_p (uA)", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "3.6*sqrt(x)", "label": "i_p ~ sqrt(v)", "color": "#2563eb"}]}
```

A reversible couple shows a forward and reverse peak separated by about
$59/n\,\text{mV}$ with equal heights. **Stripping voltammetry** pre-concentrates
trace metals onto the electrode before the sweep, pushing detection limits into
the parts-per-trillion range.

```mermaid
flowchart LR
  WE["Working electrode"] --> POT["Potentiostat (apply E, read i)"]
  RE["Reference electrode"] --> POT
  CE["Counter electrode"] --> POT
  POT --> CV["Voltammogram (i vs E)"]
```

These current-based methods are cheap, fast and exquisitely sensitive — the
backbone of glucose biosensors and trace-metal monitoring.

**Next:** check your understanding.
""",
        ),
        _quiz(),
    ),
)


# ── Analytical & Instrumental Chemistry — Advanced ───────────────────────────

_ADVANCED = SeedCourse(
    slug="analytical-chemistry-advanced",
    title="Analytical & Instrumental Chemistry — Advanced",
    description=(
        "State-of-the-art instrumental analysis and the data it produces: mass "
        "spectrometry from ionisation to the mass spectrum, hyphenated LC-MS/MS "
        "and quantitation, the physics and chemistry of NMR, and how these "
        "platforms generate metabolomics and proteomics datasets analysed with "
        "chemometrics and machine learning. Equations, pipelines and spectra "
        "throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Mass spectrometry: ionisation & the mass spectrum",
            "12 min",
            r"""
# Mass spectrometry: ionisation & the mass spectrum

A mass spectrometer weighs molecules. It **ionises** the analyte, **separates**
ions by mass-to-charge ratio $m/z$, and **detects** their abundance, producing a
spectrum of intensity versus $m/z$. Three stages, always:

```mermaid
flowchart LR
  S["Sample"] --> ION["Ion source (ESI / MALDI / EI)"]
  ION --> ANA["Mass analyzer (TOF / quadrupole / Orbitrap)"]
  ANA --> DET["Detector"]
  DET --> SPEC["Mass spectrum (m/z vs intensity)"]
```

**Soft** ionisation — **electrospray (ESI)** and **MALDI** — transfers intact
biomolecules into the gas phase, key for proteins and metabolites. **Hard**
electron ionisation (EI) fragments molecules reproducibly, giving library-
searchable GC-MS spectra. ESI often produces multiply charged ions, so a
$10\,\text{kDa}$ protein appears at modest $m/z$.

**Resolving power** $R=m/\Delta m$ determines whether two near-isobaric ions are
distinguished; high-resolution analyzers (Orbitrap, TOF) reach $R>10^5$, giving
accurate masses good to a few ppm — enough to assign molecular formulae. A
simulated isotope cluster shows the resolved peaks:

```plot
{"title": "Resolved isotope peaks in a mass spectrum", "xLabel": "m/z (offset)", "yLabel": "relative intensity", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-(x-3)^2/0.05)", "label": "monoisotopic", "color": "#2563eb"}, {"expr": "0.6*exp(-(x-4)^2/0.05)", "label": "M+1", "color": "#dc2626"}]}
```

**Next:** coupling MS to chromatography for quantitation.
""",
        ),
        _t(
            "Tandem MS & hyphenated LC-MS/MS",
            "12 min",
            r"""
# Tandem MS & hyphenated LC-MS/MS

Coupling a separation to MS — **LC-MS** or **GC-MS** — adds a retention-time
axis, so co-eluting or isobaric species are resolved before detection.
**Tandem MS (MS/MS)** goes further: a first analyzer selects a **precursor**
ion, a collision cell fragments it, and a second analyzer scans the
**product** ions, giving structural specificity.

For targeted quantitation, triple-quadrupole instruments run **selected/multiple
reaction monitoring (SRM/MRM)**: only a specific precursor-to-product
transition is recorded, suppressing background and yielding the field's lowest
detection limits.

```mermaid
flowchart LR
  LC["LC separation"] --> ESI["ESI source"]
  ESI --> Q1["Q1: select precursor"]
  Q1 --> Q2["q2: collision cell (CID)"]
  Q2 --> Q3["Q3: select product"]
  Q3 --> DET["Detector (MRM transition)"]
```

Quantitation uses a **stable-isotope-labelled internal standard** (the same
molecule with ¹³C/¹⁵N) that co-elutes and ionises identically, correcting for
ion-suppression matrix effects. The analyte/IS area ratio is linear in
concentration over orders of magnitude:

```plot
{"title": "Isotope-dilution calibration (analyte/IS ratio)", "xLabel": "concentration (ng/mL)", "yLabel": "analyte/IS area ratio", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1.2*x", "label": "linear response", "color": "#2563eb"}]}
```

Accurate-mass full-scan acquisition (DDA/DIA) instead supports **untargeted**
discovery, where thousands of features are catalogued for later annotation.

**Next:** the other great structural probe — NMR.
""",
        ),
        _t(
            "Nuclear magnetic resonance spectroscopy",
            "12 min",
            r"""
# Nuclear magnetic resonance spectroscopy

**NMR** probes nuclei with spin (¹H, ¹³C, ³¹P) placed in a strong magnetic field
$B_0$. The field splits spin states by an energy gap that sets the **Larmor
frequency**:

$$\nu = \frac{\gamma}{2\pi}\,B_0,$$

where $\gamma$ is the nucleus's gyromagnetic ratio. A radio-frequency pulse tips
the magnetisation; as it relaxes it induces a decaying signal, the **free
induction decay (FID)**, whose Fourier transform is the spectrum. The FID is an
exponentially damped oscillation:

```plot
{"title": "Free induction decay (FID) envelope", "xLabel": "time (arb.)", "yLabel": "signal", "xRange": [0, 10], "yRange": [-1.1, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)*cos(4*x)", "label": "damped FID", "color": "#2563eb"}]}
```

The diagnostic axis is the **chemical shift** $\delta$ (ppm), the resonance
frequency relative to a reference, normalised by spectrometer frequency so it is
field-independent. Shift reports the electronic environment; **spin-spin
coupling** ($J$, in Hz) splits peaks and reveals neighbouring nuclei; and peak
**integral** is proportional to the number of equivalent nuclei.

```mermaid
flowchart LR
  B0["Static field B0"] --> RF["RF pulse"]
  RF --> FID["Acquire FID"]
  FID --> FT["Fourier transform"]
  FT --> SPEC["Spectrum: shift, coupling, integral"]
```

NMR is inherently **quantitative** and nondestructive — a single calibrated
internal standard turns integrals into absolute concentrations (qNMR), and 2D
experiments (COSY, HSQC) resolve crowded biological mixtures.

**Next:** how these platforms generate omics data.
""",
        ),
        _t(
            "Generating omics data: metabolomics & proteomics",
            "12 min",
            r"""
# Generating omics data: metabolomics & proteomics

LC-MS/MS and NMR are the engines of **omics** — measuring whole classes of small
molecules (**metabolomics**) or proteins (**proteomics**) at once. In
shotgun proteomics, proteins are digested (trypsin) into peptides, separated by
nano-LC, fragmented by MS/MS, and matched to a sequence database. In
metabolomics, untargeted LC-MS catalogues thousands of features per sample.

```mermaid
flowchart LR
  SAMP["Biological sample"] --> EXT["Extraction / digestion"]
  EXT --> LC["LC separation"]
  LC --> MS["High-res MS/MS"]
  MS --> FEAT["Feature detection & alignment"]
  FEAT --> ANNO["Annotation / database search"]
  ANNO --> MAT["Feature x sample matrix"]
```

The output is a high-dimensional **feature x sample matrix** — often more
features ($p$) than samples ($n$), the classic "large $p$, small $n$" regime.
Raw data need careful preprocessing: peak picking, retention-time alignment,
normalisation (to total ion current or internal standards), missing-value
imputation, and log transformation to stabilise variance.

A central challenge is **multiple testing**: with thousands of features tested at
once, false positives explode unless controlled. The false discovery rate grows
sharply with the number of tests, motivating Benjamini-Hochberg correction:

```plot
{"title": "Expected false positives vs number of features tested", "xLabel": "features tested (thousands)", "yLabel": "false positives at alpha=0.05", "xRange": [0, 10], "yRange": [0, 520], "grid": true, "functions": [{"expr": "50*x", "label": "0.05 x N", "color": "#dc2626"}]}
```

Identification confidence is reported at defined levels (e.g. Metabolomics
Standards Initiative levels 1-4), because an accurate mass alone rarely pins down
a single compound.

**Next:** turning these matrices into knowledge with chemometrics and AI.
""",
        ),
        _t(
            "Chemometrics & machine learning for analytical data",
            "12 min",
            r"""
# Chemometrics & machine learning for analytical data

**Chemometrics** applies statistics and machine learning to chemical
measurements. The first move on a wide spectral or omics matrix is **dimension
reduction**: **principal component analysis (PCA)** finds orthogonal directions
of maximum variance, projecting samples into a few interpretable components for
unsupervised exploration and outlier detection.

For prediction, the field's workhorse is **partial least squares (PLS)**, which
unlike PCA finds components that maximise covariance with the response — ideal
for NIR/Raman quantitation and PLS-DA classification of disease vs control. The
explained variance accumulates and saturates with added components, guiding how
many to keep:

```plot
{"title": "Cumulative variance explained vs components", "xLabel": "number of components", "yLabel": "cumulative variance (fraction)", "xRange": [1, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating fit", "color": "#16a34a"}]}
```

Modern pipelines add regularised regression (LASSO for biomarker selection),
random forests and gradient boosting, and — for raw spectra and chromatograms —
**convolutional neural networks** and transformers that learn features directly.
Deep models also now **predict spectra** (e.g. peptide fragmentation, retention
time, NMR shifts) to improve identification.

```mermaid
flowchart LR
  RAW["Raw spectra / feature matrix"] --> PRE["Preprocess + scale"]
  PRE --> DR["PCA / PLS dimension reduction"]
  DR --> MOD["ML model (PLS-DA / RF / CNN)"]
  MOD --> CV["Cross-validation + permutation test"]
  CV --> RES["Biomarkers / prediction"]
```

The cardinal rule with "large $p$, small $n$" data is **honest validation**:
nested cross-validation, an untouched test set, and permutation tests, because
flexible models overfit noise and produce confident nonsense otherwise.

**Next:** the final assessment.
""",
        ),
        _t(
            "Validation, QA/QC & reproducibility",
            "11 min",
            r"""
# Validation, QA/QC & reproducibility

State-of-the-art instruments are worthless without **method validation** —
documented evidence that a method is fit for purpose. Core figures of merit:
**accuracy** (closeness to a reference/spike recovery), **precision** (repeat-
ability and intermediate precision), **linearity** and range, **LOD/LOQ**,
**selectivity/specificity**, and **robustness** to small deliberate changes.

```mermaid
flowchart LR
  DEV["Method development"] --> VAL["Validation (accuracy, precision, LOD)"]
  VAL --> QC["Routine QA/QC"]
  QC --> CHK["Blanks, spikes, control charts"]
  CHK --> REL["Released result"]
  CHK -->|"out of control"| INV["Investigate / recalibrate"]
```

In routine operation, **QA/QC** keeps a validated method honest: method blanks
catch contamination, spiked recoveries track accuracy, and **control charts**
flag drift when a check standard wanders beyond warning ($\pm2\sigma$) or action
($\pm3\sigma$) limits. The expected fraction of in-control points outside
$\pm k\sigma$ falls steeply with $k$:

```plot
{"title": "Control-chart: out-of-limit probability vs k sigma", "xLabel": "limit width k (sigma)", "yLabel": "fraction beyond +/- k", "xRange": [0, 4], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-x*x/2)", "label": "tail probability proxy", "color": "#dc2626"}]}
```

For omics and ML results, reproducibility also demands **reported uncertainty**,
shared raw data and code, batch-effect correction, and independent-cohort
validation. The discipline of QA/QC is what separates a publishable signal from
an irreproducible artefact.

**Next:** check your mastery of the advanced material.
""",
        ),
        _quiz(),
    ),
)


ANALYTICAL_CHEMISTRY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ANALYTICAL_CHEMISTRY_COURSES"]
