"""Academy seed content - SAR and InSAR.

Radar remote sensing that sees through clouds day and night and measures
millimetre ground motion. This course builds up from the physics of radar
and the Synthetic Aperture Radar (SAR) principle, through image geometry,
backscatter and polarimetry, speckle and multilooking, to interferometry
(InSAR) for deformation and DEMs, time-series methods (PS-InSAR, SBAS),
and the Sentinel-1 mission with the SNAP and ISCE processing tools. Every
lesson is a direct explanation with a concrete formula or computation and
a mermaid diagram, followed by a checkpoint quiz; the course closes with a
comprehensive final quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


_SAR_INSAR = SeedCourse(
    slug="sar-insar",
    title="SAR & InSAR",
    description=(
        "Radar remote sensing that sees through clouds and measures "
        "millimetre ground motion - Synthetic Aperture Radar imaging, "
        "interferometry (InSAR) and time-series (PS-InSAR) with Sentinel-1. "
        "Every lesson pairs a direct explanation with a real formula or "
        "processing snippet and a diagram."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# SAR and InSAR

Optical satellites need sunlight and a clear sky. **Radar** does not: it
carries its own illumination and its microwaves pass through clouds, so a
**Synthetic Aperture Radar (SAR)** sensor images the Earth day and night,
in any weather. Better still, by comparing the **phase** of two radar
passes - **interferometry (InSAR)** - we can measure ground movement to
the millimetre, mapping earthquakes, subsidence, volcanoes and
infrastructure motion from orbit.

This course is **advanced but concrete**: every lesson explains one idea
directly, grounds it in a real formula or a processing snippet (SNAP,
ISCE, GDAL, NumPy), and draws it as a diagram. A short quiz follows each
lesson; a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Radar basics and the SAR principle** - why a synthetic aperture
2. **SAR geometry and image formation** - range, azimuth, slant vs ground
3. **Backscatter and polarimetry** - what the surface returns
4. **Speckle and multilooking** - the grainy noise and how to tame it
5. **Interferometry (InSAR)** - the phase and the interferogram
6. **Deformation and DEM generation** - turning phase into motion or height
7. **Time-series InSAR** - PS-InSAR and SBAS over many images
8. **Sentinel-1 and processing tools** - SNAP and ISCE in practice

Grounded throughout in real missions and standards: **Sentinel-1** (C-band,
Copernicus), TerraSAR-X, ALOS-2, the **SLC** product, WGS84 and UTM
geocoding, and the open toolchains that turn raw radar into maps of motion.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the key advantage of radar (SAR) over optical remote sensing?",
                    (
                        opt("It has far higher colour fidelity"),
                        opt(
                            "It carries its own illumination and its microwaves pass "
                            "through clouds, so it images day and night in any weather",
                            correct=True,
                        ),
                        opt("It needs no satellite"),
                        opt("It only works in bright daylight"),
                    ),
                    "SAR is active and uses microwaves, so cloud, darkness and weather "
                    "do not stop it - unlike passive optical sensors.",
                ),
                q(
                    "What does InSAR add on top of SAR imaging?",
                    (
                        opt("It colourises the radar image"),
                        opt(
                            "It compares the phase of two or more passes to measure "
                            "ground motion or terrain height to the millimetre or metre",
                            correct=True,
                        ),
                        opt("It removes the need for a radar antenna"),
                        opt("It only measures temperature"),
                    ),
                    "Interferometry exploits the phase difference between acquisitions "
                    "to measure deformation and elevation.",
                ),
            ),
        ),
        # -- 1. Radar basics and the SAR principle ---------------------
        _t(
            "Radar basics and the SAR principle",
            "11 min",
            """# Radar basics and the SAR principle

**Radar** (Radio Detection and Ranging) transmits a microwave pulse and
listens for the echo. The time delay gives **range** (distance) and the
returned power tells you about the surface. Because the sensor supplies
its own energy, it is an **active** system - independent of the Sun.

SAR sensors use microwave **bands**, named by wavelength. Longer waves
penetrate vegetation more; shorter waves resolve finer detail:

```text
Band   Wavelength    Example missions
X       ~3.1 cm      TerraSAR-X, COSMO-SkyMed
C       ~5.6 cm      Sentinel-1, RADARSAT-2
L       ~23.5 cm     ALOS-2 PALSAR, NISAR (L)

Frequency and wavelength:  f = c / lambda
For C-band:  f = 3.0e8 / 0.056  =  5.36 GHz
```

The hard problem is **azimuth resolution** (along the flight track). A
real antenna's resolution is set by its beamwidth, which is proportional
to `wavelength / antenna_length`. To get metre-scale resolution from
orbit with a real aperture you would need an antenna kilometres long -
impossible.

The **synthetic aperture** trick: the radar keeps pulsing as the
satellite flies, so any point on the ground is illuminated over a long
stretch of the orbit. By coherently combining all those echoes (using the
Doppler history of the target), the processor **synthesizes** an aperture
as long as that illuminated stretch. The remarkable result:

```text
Azimuth resolution (SAR)  ~=  L / 2
where L is the real antenna length along-track.

A 10 m antenna therefore yields ~5 m azimuth resolution,
INDEPENDENT of range - the further target is illuminated longer,
which exactly compensates. This is the SAR principle.
```

```mermaid
graph LR
    TX["Transmit pulse"] --> ECHO["Receive echoes along orbit"]
    ECHO --> DOP["Doppler history per target"]
    DOP --> SYN["Synthesize long aperture"]
    SYN --> FOCUS["Focus into sharp image"]
    FOCUS --> RES["Fine azimuth resolution"]
```

Remember: SAR trades a physically huge antenna for computation - it flies
a small antenna and builds a virtual one from the motion.
""",
        ),
        quiz_lesson(
            "Quiz: Radar basics and the SAR principle",
            (
                q(
                    "Why is SAR called an 'active' remote sensing system?",
                    (
                        opt("Because it is always switched on"),
                        opt(
                            "Because it transmits its own microwave energy and measures "
                            "the echo, rather than relying on sunlight",
                            correct=True,
                        ),
                        opt("Because it moves faster than optical satellites"),
                        opt("Because it needs an active internet connection"),
                    ),
                    "Active sensors supply their own illumination; that is why SAR works "
                    "at night and through cloud.",
                ),
                q(
                    "What is the core idea of a 'synthetic' aperture?",
                    (
                        opt("Using a physically kilometre-long antenna in orbit"),
                        opt(
                            "Coherently combining echoes collected along the flight path "
                            "to synthesize an aperture far longer than the real antenna",
                            correct=True,
                        ),
                        opt("Averaging several optical photos together"),
                        opt("Transmitting at a synthetic, made-up frequency"),
                    ),
                    "The platform motion plus Doppler processing builds a virtual long "
                    "antenna, giving fine azimuth resolution.",
                ),
                q(
                    "Approximately, the finest azimuth resolution of a SAR is…",
                    (
                        opt("equal to the antenna length L"),
                        opt("about L / 2, and independent of range", correct=True),
                        opt("proportional to the range, getting worse far away"),
                        opt("equal to the radar wavelength"),
                    ),
                    "Azimuth resolution tends to L/2; farther targets are illuminated "
                    "longer, which compensates, so it does not degrade with range.",
                ),
            ),
        ),
        # -- 2. SAR geometry and image formation -----------------------
        _t(
            "SAR geometry and image formation",
            "11 min",
            """# SAR geometry and image formation

A SAR looks **sideways**, not straight down - it is a **side-looking**
sensor. Two axes define the image:

- **Range** (across-track) - measured by echo time delay. The radar
  cannot separate two points at the same distance, hence the side-look.
- **Azimuth** (along-track) - the flight direction, resolved by the
  synthetic aperture.

The **look angle** and **incidence angle** describe the viewing geometry.
Range measured along the radar beam is **slant range**; projected onto the
flat Earth it becomes **ground range**:

```text
ground_range = slant_range / sin(incidence_angle)

Slant-to-ground pixel spacing also depends on incidence:
d_ground = d_slant / sin(theta_i)
```

Because the radar orders pixels by distance, terrain relief distorts the
image in ways unique to SAR:

- **Foreshortening** - slopes facing the radar look compressed.
- **Layover** - a tall feature's top is nearer the radar than its base,
  so it is imaged *before* (laid over) the base.
- **Shadow** - ground behind a steep feature receives no pulse and returns
  nothing (black).

The raw echoes are **focused** into a **Single Look Complex (SLC)** image:
each pixel is a complex number with **amplitude** (return strength) and
**phase** (sub-wavelength range info). That phase is what makes InSAR
possible later.

```mermaid
graph TD
    ORBIT["Side looking sensor"] --> RANGE["Range from echo delay"]
    ORBIT --> AZI["Azimuth from synthetic aperture"]
    RANGE --> SLANT["Slant range image"]
    SLANT --> DIST["Foreshortening layover shadow"]
    SLANT --> SLC["Focused SLC complex pixels"]
    SLC --> AMP["Amplitude and phase"]
```

Remember: SAR images live in radar coordinates (slant range and azimuth),
carry complex amplitude and phase, and distort terrain by distance - not
the perspective distortions of an optical camera.
""",
        ),
        quiz_lesson(
            "Quiz: SAR geometry and image formation",
            (
                q(
                    "Why must a SAR look sideways rather than straight down (nadir)?",
                    (
                        opt("To save electrical power"),
                        opt(
                            "Because it orders returns by range; looking straight down, "
                            "points equidistant on either side would be indistinguishable",
                            correct=True,
                        ),
                        opt("Because the antenna cannot point downward"),
                        opt("To keep the Sun out of the image"),
                    ),
                    "Side-looking geometry removes the left-right ambiguity of a "
                    "range-ordered sensor.",
                ),
                q(
                    "What is 'layover' in a SAR image?",
                    (
                        opt("A cloud covering the scene"),
                        opt(
                            "The top of a tall feature is closer to the radar than its "
                            "base, so it is imaged before the base and laid over it",
                            correct=True,
                        ),
                        opt("Two orbits overlapping in time"),
                        opt("The dark region behind a mountain"),
                    ),
                    "Layover is a range-ordering distortion of tall/steep terrain; the "
                    "no-return dark area is radar shadow.",
                ),
                q(
                    "What does each pixel of a Single Look Complex (SLC) product contain?",
                    (
                        opt("Only a brightness value"),
                        opt("An RGB colour"),
                        opt(
                            "A complex number carrying both amplitude and phase",
                            correct=True,
                        ),
                        opt("A temperature reading"),
                    ),
                    "The complex SLC stores amplitude and phase; the phase is what "
                    "interferometry later exploits.",
                ),
            ),
        ),
        # -- 3. Backscatter and polarimetry ----------------------------
        _t(
            "Backscatter and polarimetry",
            "11 min",
            """# Backscatter and polarimetry

The brightness of a SAR pixel is its **backscatter** - the fraction of
transmitted power the surface scatters back to the antenna. It is reported
as a calibrated coefficient, usually **sigma nought** (per unit ground
area), in **decibels**:

```text
sigma0_dB = 10 * log10(sigma0_linear)

Typical C-band values:
  calm water            ~ -20 dB   (specular, dark)
  bare smooth soil      ~ -12 dB
  rough soil / crops    ~ -8 dB
  urban / double bounce ~  0 dB    (very bright)
```

Backscatter depends on **surface roughness** (relative to wavelength),
**geometry** (incidence angle) and **dielectric properties** (moisture -
wet soil returns more). Three scattering mechanisms dominate:

- **Surface (rough) scattering** - fields, bare ground.
- **Volume scattering** - forest canopies, dry snow (many small scatterers).
- **Double-bounce** - ground-then-wall corners, very bright in cities.

**Polarimetry** exploits the wave's **polarization**. The radar can
transmit and receive Horizontally (H) or Vertically (V), giving channels
**VV, VH, HH, HV**. The cross-pol channels (VH, HV) are sensitive to
volume scattering, so combining channels separates surface types - a
**dual-pol** Sentinel-1 VV+VH pair already distinguishes water, crops and
urban areas well. A **fully polarimetric** system measures all four to
form a scattering matrix and decompose the mechanisms.

```mermaid
graph TD
    PULSE["Polarized pulse"] --> SURF["Surface scattering fields"]
    PULSE --> VOL["Volume scattering canopy"]
    PULSE --> DB["Double bounce urban"]
    SURF --> POL["VV VH HH HV channels"]
    VOL --> POL
    DB --> POL
    POL --> CLASS["Classify surface types"]
```

Remember: backscatter (in dB) encodes roughness, geometry and moisture;
polarization channels add a second dimension that tells scattering
mechanisms apart.
""",
        ),
        quiz_lesson(
            "Quiz: Backscatter and polarimetry",
            (
                q(
                    "Why does calm open water appear very dark in a SAR image?",
                    (
                        opt("Water absorbs all microwaves"),
                        opt(
                            "It is a smooth specular surface that reflects energy away "
                            "from the antenna, so little backscatter returns",
                            correct=True,
                        ),
                        opt("Water is too cold to reflect radar"),
                        opt("The radar cannot see water at all"),
                    ),
                    "Smooth surfaces reflect specularly (away from the sensor); rough "
                    "surfaces scatter energy back and look bright.",
                ),
                q(
                    "What scattering mechanism makes urban areas appear very bright?",
                    (
                        opt("Volume scattering in the concrete"),
                        opt(
                            "Double-bounce off ground-then-wall corner reflectors that "
                            "send energy strongly back to the radar",
                            correct=True,
                        ),
                        opt("Specular reflection from windows"),
                        opt("Thermal emission from buildings"),
                    ),
                    "Corner (double-bounce) geometry returns a strong signal; that is "
                    "why cities are bright and coherent.",
                ),
                q(
                    "What are the polarization channels VV and VH?",
                    (
                        opt("Two different radar frequencies"),
                        opt(
                            "Transmit/receive polarization combinations - VV is transmit "
                            "and receive vertical, VH is transmit vertical receive horizontal",
                            correct=True,
                        ),
                        opt("Vertical and horizontal orbit passes"),
                        opt("Two brightness scales"),
                    ),
                    "The first letter is transmit, the second receive; cross-pol (VH) is "
                    "sensitive to volume scattering.",
                ),
            ),
        ),
        # -- 4. Speckle and multilooking -------------------------------
        _t(
            "Speckle and multilooking",
            "10 min",
            """# Speckle and multilooking

Look at any single-look SAR image and it appears **grainy**, salt-and-
pepper even over uniform fields. That is **speckle** - not sensor noise
but a real interference effect: each resolution cell holds many tiny
scatterers whose coherent returns add with random phases, so the summed
amplitude fluctuates from cell to cell.

Speckle is **multiplicative** (it scales with the signal) and, for
single-look intensity, follows an exponential distribution whose standard
deviation equals its mean - a signal-to-noise ratio of 1. It must be
reduced before you can read or classify the image.

**Multilooking** is the classic remedy: average `N` independent looks (in
frequency sub-bands or by averaging neighbouring pixels). Averaging
independent intensity samples cuts the relative noise:

```text
Speckle standard deviation after averaging N looks:
  sigma / mean  =  1 / sqrt(N)

Averaging 4 looks halves the relative speckle (1/sqrt(4) = 0.5)
but coarsens resolution by ~4x. It is a resolution-vs-noise trade.
```

A simple boxcar multilook in NumPy:

```python
import numpy as np

def multilook(intensity, looks=(1, 4)):
    az, rg = looks              # average 1 in azimuth, 4 in range
    a, r = intensity.shape
    a, r = a - a % az, r - r % rg
    block = intensity[:a, :r].reshape(a // az, az, r // rg, rg)
    return block.mean(axis=(1, 3))   # mean over each look window
```

Beyond boxcar averaging, **adaptive speckle filters** (Lee, Refined Lee,
Frost) smooth flat areas while preserving edges and points. Multilooking
also makes pixels roughly square on the ground, easing later geocoding.

```mermaid
graph LR
    SLC["Single look image"] --> SPK["Grainy speckle SNR one"]
    SPK --> ML["Multilook average N looks"]
    ML --> RED["Speckle down by root N"]
    ML --> COARSE["Resolution coarsened"]
    RED --> READ["Cleaner for classification"]
```

Remember: speckle is coherent interference, not random noise; average
independent looks to reduce it by 1/sqrt(N), trading away resolution.
""",
        ),
        quiz_lesson(
            "Quiz: Speckle and multilooking",
            (
                q(
                    "What causes speckle in SAR images?",
                    (
                        opt("Dust on the antenna"),
                        opt(
                            "Coherent interference of many small scatterers within each "
                            "resolution cell adding with random phases",
                            correct=True,
                        ),
                        opt("Electronic thermal noise only"),
                        opt("Compression artefacts in the data file"),
                    ),
                    "Speckle is a real multiplicative interference effect, not additive "
                    "sensor noise.",
                ),
                q(
                    "Averaging N independent looks reduces the relative speckle by…",
                    (
                        opt("1 / N"),
                        opt("1 / sqrt(N)", correct=True),
                        opt("N squared"),
                        opt("it does not reduce speckle at all"),
                    ),
                    "The speckle standard deviation over mean falls as 1/sqrt(N); 4 "
                    "looks gives a factor of 0.5.",
                ),
                q(
                    "What is the main cost of multilooking?",
                    (
                        opt("It corrupts the phase permanently"),
                        opt(
                            "It coarsens spatial resolution - you trade detail for lower noise",
                            correct=True,
                        ),
                        opt("It doubles the file size"),
                        opt("It removes all backscatter information"),
                    ),
                    "Averaging looks smooths noise but enlarges the effective pixel; it "
                    "is a resolution-versus-noise trade-off.",
                ),
            ),
        ),
        # -- 5. Interferometry (InSAR) and the phase -------------------
        _t(
            "Interferometry (InSAR) and the phase",
            "12 min",
            """# Interferometry (InSAR) and the phase

Here is where SAR becomes extraordinary. Each SLC pixel has a **phase**
that encodes the two-way distance to the target in fractions of a
wavelength. A single phase is meaningless (it wraps every half
wavelength), but the **difference** between two co-registered SLCs of the
same area is rich with information. That difference image is an
**interferogram**.

Form it by multiplying the first image by the complex conjugate of the
second - the amplitudes multiply and the phases subtract:

```python
import numpy as np

# master and slave are co-registered complex SLC arrays
interferogram = master * np.conj(slave)
int_phase = np.angle(interferogram)     # wrapped phase in (-pi, pi]
coherence = (np.abs(np.mean(master * np.conj(slave))) /
             np.sqrt(np.mean(np.abs(master)**2) *
                     np.mean(np.abs(slave)**2)))   # 0..1 quality
```

The interferometric phase is a **sum of contributions**:

```text
phi_int = phi_flat + phi_topo + phi_defo + phi_atmos + phi_noise

phi_flat  - flat-Earth (reference ellipsoid) phase ramp
phi_topo  - terrain height (depends on the perpendicular baseline B_perp)
phi_defo  - ground movement between the two passes
phi_atmos - differing atmospheric delay on each date
phi_noise - decorrelation noise
```

The observed phase is **wrapped** into `(-pi, pi]`, producing the coloured
**fringes** of an interferogram - each full colour cycle is one wavelength
step of change. **Phase unwrapping** restores the continuous field by
counting the whole cycles between pixels.

Two conditions make an interferogram usable:

- **Coherence** - the pixel must scatter similarly on both dates. Water,
  dense vegetation and long time gaps **decorrelate** (coherence toward 0);
  rock, cities and bare ground stay coherent (toward 1).
- **Small baselines** - the two orbits must be close (small perpendicular
  baseline) or topographic sensitivity and geometric decorrelation grow.

```mermaid
graph TD
    M["Master SLC"] --> CONJ["Multiply by conjugate slave"]
    S["Slave SLC"] --> CONJ
    CONJ --> IFG["Interferogram wrapped phase"]
    IFG --> COH["Coherence quality map"]
    IFG --> FLAT["Remove flat Earth phase"]
    FLAT --> UNW["Phase unwrapping"]
    UNW --> USE["Height or deformation"]
```

Remember: an interferogram is the phase difference of two SLCs; its
fringes mix topography, motion and atmosphere, and only coherent,
small-baseline pairs give a clean, unwrappable signal.
""",
        ),
        quiz_lesson(
            "Quiz: Interferometry (InSAR) and the phase",
            (
                q(
                    "How is an interferogram formed from two co-registered SLC images?",
                    (
                        opt("By adding their amplitudes"),
                        opt(
                            "By multiplying one by the complex conjugate of the other, so "
                            "amplitudes multiply and phases subtract",
                            correct=True,
                        ),
                        opt("By averaging their brightness"),
                        opt("By subtracting their intensities in dB"),
                    ),
                    "master * conj(slave) yields a complex product whose angle is the "
                    "phase difference.",
                ),
                q(
                    "What does 'coherence' measure in InSAR?",
                    (
                        opt("The brightness of the scene"),
                        opt(
                            "How similarly a pixel scatters on both dates - a 0-to-1 "
                            "quality measure of interferometric phase",
                            correct=True,
                        ),
                        opt("The satellite battery level"),
                        opt("The number of looks averaged"),
                    ),
                    "High coherence (near 1) means a reliable phase; water and dense "
                    "vegetation decorrelate toward 0.",
                ),
                q(
                    "The interferometric phase is a sum of several terms. Which set is correct?",
                    (
                        opt("Only deformation and noise"),
                        opt(
                            "Flat-Earth, topographic, deformation, atmospheric and noise "
                            "contributions",
                            correct=True,
                        ),
                        opt("Only the satellite clock and Doppler"),
                        opt("Amplitude, colour and temperature"),
                    ),
                    "Separating those terms (especially topo, defo and atmosphere) is "
                    "the whole challenge of InSAR processing.",
                ),
                q(
                    "Why must the two acquisition orbits have a small perpendicular baseline?",
                    (
                        opt("To save fuel"),
                        opt(
                            "Large baselines increase topographic sensitivity and "
                            "geometric decorrelation, degrading the interferogram",
                            correct=True,
                        ),
                        opt("So the images have the same brightness"),
                        opt("Because the antenna cannot rotate"),
                    ),
                    "Small baselines keep geometric decorrelation low and reduce unwanted "
                    "topographic phase.",
                ),
            ),
        ),
        # -- 6. Deformation and DEM generation -------------------------
        _t(
            "Deformation and DEM generation",
            "12 min",
            """# Deformation and DEM generation

Once you have an unwrapped interferometric phase, two products fall out
depending on what dominates the phase.

**DEM generation** uses the **topographic** term. With two passes
separated by a **perpendicular baseline** `B_perp` (or two antennas at
once, as on the SRTM mission), phase maps to terrain height. The height
that produces one full fringe (2 pi) is the **ambiguity height**:

```text
h_amb = (lambda * R * sin(theta_i)) / (2 * B_perp)

lambda = wavelength, R = slant range, theta_i = incidence angle.
Larger B_perp  ->  smaller h_amb  ->  more sensitive to topography.
So DEM interferometry WANTS a large baseline.
```

**Deformation mapping** uses the **displacement** term. If you remove
topography (using an existing DEM) and flat-Earth, the residual is
**differential InSAR (DInSAR)** and each fringe is half a wavelength of
motion **along the line of sight (LOS)**:

```text
One 2*pi fringe  =  lambda / 2  of LOS displacement.

Sentinel-1 C-band, lambda = 5.6 cm:
  one fringe  =  2.8 cm of LOS motion.

LOS is not vertical - project it:
  d_LOS = d_vertical * cos(theta_i) - d_horizontal(...) * sin(theta_i)
```

This is how a single earthquake interferogram reveals centimetres of
crustal slip as a bullseye of fringes, or how a city subsiding over an
aquifer shows a slow phase gradient. Note the LOS caveat: InSAR measures
motion **toward or away from the satellite**, not pure vertical - combine
ascending and descending passes to separate vertical and east-west
components.

```mermaid
graph TD
    UNW["Unwrapped phase"] --> TOPO["Topographic term"]
    UNW --> DEFO["Deformation term"]
    TOPO --> BASE["Large baseline sensitive"]
    BASE --> DEM["Digital elevation model"]
    DEFO --> DIN["Remove DEM and flat Earth"]
    DIN --> LOS["Line of sight displacement"]
    LOS --> COMB["Combine ascending and descending"]
    COMB --> VERT["Vertical and east west motion"]
```

Remember: large baseline plus the topographic phase gives a DEM; removing
topography leaves deformation, where each fringe is lambda/2 of
line-of-sight motion - so ascending and descending passes are combined to
recover true 3D-ish displacement.
""",
        ),
        quiz_lesson(
            "Quiz: Deformation and DEM generation",
            (
                q(
                    "For a Sentinel-1 (C-band, 5.6 cm) differential interferogram, one "
                    "full 2*pi fringe corresponds to how much line-of-sight motion?",
                    (
                        opt("5.6 cm (one full wavelength)"),
                        opt("2.8 cm (half a wavelength)", correct=True),
                        opt("11.2 cm (two wavelengths)"),
                        opt("1 mm exactly"),
                    ),
                    "The two-way path means one fringe equals lambda/2 of LOS "
                    "displacement, i.e. 2.8 cm at C-band.",
                ),
                q(
                    "For DEM generation by InSAR, what kind of baseline is desirable?",
                    (
                        opt("A zero baseline"),
                        opt(
                            "A larger perpendicular baseline - it lowers the ambiguity "
                            "height and increases sensitivity to topography",
                            correct=True,
                        ),
                        opt("A baseline of exactly one wavelength"),
                        opt("Baseline is irrelevant to DEMs"),
                    ),
                    "h_amb is inversely proportional to B_perp; DEM work wants a large "
                    "baseline, deformation work wants a small one.",
                ),
                q(
                    "Why are ascending and descending passes combined for deformation?",
                    (
                        opt("To double the image resolution"),
                        opt(
                            "InSAR measures only line-of-sight motion; two viewing "
                            "geometries let you separate vertical and east-west components",
                            correct=True,
                        ),
                        opt("To remove speckle"),
                        opt("Because one pass is always cloudy"),
                    ),
                    "A single LOS is ambiguous about direction; two geometries decompose "
                    "the displacement vector.",
                ),
            ),
        ),
        # -- 7. Time-series InSAR (PS-InSAR, SBAS) ---------------------
        _t(
            "Time-series InSAR (PS-InSAR, SBAS)",
            "12 min",
            """# Time-series InSAR (PS-InSAR, SBAS)

A single interferogram is corrupted by **atmosphere** (water vapour delay
changes each date) and by **decorrelation**. To measure slow motion (a few
mm/year) reliably you process a **stack** of many acquisitions over years
and exploit the fact that atmosphere is random in time while deformation
is steady. Two complementary methods lead.

**Persistent Scatterer InSAR (PS-InSAR)** finds individual pixels - rocks,
rooftops, poles, corner reflectors - whose scattering stays **coherent
over the whole stack**. On those persistent scatterers the phase is
clean, so you fit a temporal model (linear velocity plus topographic error
plus atmospheric phase screen) and solve for millimetre-per-year rates.
PS points are dense in cities, sparse in fields.

**Small Baseline Subset (SBAS)** instead forms many interferograms among
image pairs with **small temporal and perpendicular baselines** (to
maximize coherence), then inverts the network for a consistent
displacement time series - typically after multilooking, so it favours
**distributed scatterers** (fields, deserts) rather than single points.

```text
Select PS candidates by amplitude stability:
  D_A = sigma_amplitude / mean_amplitude     (dispersion index)
  keep pixels with D_A < 0.25  as persistent scatterer candidates.

Fit per-PS temporal model over dates t_k:
  phi(t_k) = (4*pi/lambda) * v * t_k  +  phi_topo(B_perp,k)  +  phi_atmos,k
  solve for velocity v and residual height; APS separated by
  spatial-low / temporal-high filtering across the stack.
```

Both build a **deformation velocity map** plus a **time series** per point.
The atmospheric phase screen (APS) is estimated as spatially smooth but
temporally uncorrelated and removed - the key that turns noisy single
interferograms into millimetre trends.

```mermaid
graph TD
    STACK["Stack of many SLCs"] --> PS["PS select stable pixels"]
    STACK --> SB["SBAS small baseline pairs"]
    PS --> MODEL["Fit velocity plus topo error"]
    SB --> INV["Invert network for time series"]
    MODEL --> APS["Estimate and remove atmosphere"]
    INV --> APS
    APS --> VEL["Velocity map mm per year"]
    VEL --> TS["Per point displacement time series"]
```

Remember: single interferograms are noisy; stacking many dates and
separating steady deformation from random atmosphere - via persistent
points (PS) or small-baseline networks (SBAS) - yields mm/year velocities.
""",
        ),
        quiz_lesson(
            "Quiz: Time-series InSAR (PS-InSAR, SBAS)",
            (
                q(
                    "Why process a time-series stack instead of one interferogram for "
                    "slow deformation?",
                    (
                        opt("To make the image prettier"),
                        opt(
                            "Deformation is steady over time while atmospheric delay is "
                            "random, so a stack lets you separate them and reach mm/year",
                            correct=True,
                        ),
                        opt("Because one image is always missing"),
                        opt("To increase the wavelength"),
                    ),
                    "Temporal filtering distinguishes a steady signal from the random "
                    "atmospheric phase screen.",
                ),
                q(
                    "What is a 'persistent scatterer' in PS-InSAR?",
                    (
                        opt("A pixel that is always dark"),
                        opt(
                            "A pixel (rock, rooftop, pole) that stays coherent and stable "
                            "in amplitude across the whole stack, giving clean phase",
                            correct=True,
                        ),
                        opt("A moving object like a car"),
                        opt("A cloud that persists over the scene"),
                    ),
                    "PS points are temporally stable strong reflectors, dense in urban "
                    "areas; their phase supports a mm/year fit.",
                ),
                q(
                    "How does SBAS differ from PS-InSAR?",
                    (
                        opt("SBAS uses only one image"),
                        opt(
                            "SBAS forms many small temporal and spatial baseline "
                            "interferograms and inverts the network, favouring "
                            "distributed scatterers",
                            correct=True,
                        ),
                        opt("SBAS ignores coherence entirely"),
                        opt("SBAS measures only topography, never motion"),
                    ),
                    "SBAS builds a small-baseline network for distributed scatterers; "
                    "PS-InSAR isolates single persistent points.",
                ),
            ),
        ),
        # -- 8. Sentinel-1 and processing tools ------------------------
        _t(
            "Sentinel-1 and processing tools (SNAP, ISCE)",
            "12 min",
            """# Sentinel-1 and processing tools (SNAP, ISCE)

The workhorse of open InSAR is **Sentinel-1**, the Copernicus C-band
radar mission. Its free, systematic global coverage on a short repeat
cycle made routine InSAR possible for everyone.

Key facts to know:

- **C-band**, ~5.6 cm wavelength; **sun-synchronous** orbit.
- Main land mode is **Interferometric Wide (IW)** swath, ~250 km wide,
  acquired with **TOPS** (Terrain Observation by Progressive Scans).
- **Revisit** ~12 days per satellite (6 days when two satellites fly).
- Products: **SLC** (complex, for InSAR) and **GRD** (detected amplitude,
  geocoded-friendly, for backscatter work).

TOPS mode steers the beam in azimuth, which demands **very precise
co-registration** (better than ~1/1000 of a pixel) and an extra
**Enhanced Spectral Diversity (ESD)** step to align bursts - a detail
every Sentinel-1 InSAR workflow handles.

Two open toolchains dominate:

- **SNAP** (ESA Sentinel Application Platform) - GUI plus the `gpt`
  command-line graph processor. Friendly for standard IW interferograms.
- **ISCE2 / ISCE3** (JPL) and **MintPy** - scriptable, research-grade,
  strong for full time-series (SBAS/PS) processing; ISCE also underpins
  NISAR.

A minimal SNAP `gpt` interferogram workflow (each step is a graph
operator):

```text
Read master and slave SLC
  -> TOPSAR-Split (pick sub-swath and bursts)
  -> Apply-Orbit-File (precise orbits)
  -> Back-Geocoding + Enhanced-Spectral-Diversity (co-register)
  -> Interferogram (form complex product, estimate coherence)
  -> TOPSAR-Deburst
  -> TopoPhaseRemoval (subtract DEM/flat-Earth phase)
  -> GoldsteinPhaseFiltering (reduce phase noise)
  -> export to SNAPHU for unwrapping
  -> Phase-to-Displacement or Phase-to-Elevation
  -> Terrain-Correction (geocode to WGS84 / UTM GeoTIFF)
```

The final **Range-Doppler terrain correction** step warps the result from
radar (slant-range/azimuth) coordinates into a map projection (e.g.
EPSG:4326 or a UTM zone) so it overlays a GIS. **SNAPHU** does the phase
unwrapping in both toolchains.

```mermaid
graph LR
    S1["Sentinel-1 SLC pair"] --> COREG["Co-register and ESD"]
    COREG --> IFG["Form interferogram"]
    IFG --> FILT["Goldstein filter"]
    FILT --> UNW["SNAPHU unwrapping"]
    UNW --> DISP["Phase to displacement or height"]
    DISP --> GEO["Terrain correction to map CRS"]
```

Remember: Sentinel-1 (C-band, IW/TOPS, SLC) plus SNAP or ISCE/MintPy is
the standard open path - co-register precisely, form and filter the
interferogram, unwrap with SNAPHU, convert to motion or height, and
geocode to a real CRS.
""",
        ),
        quiz_lesson(
            "Quiz: Sentinel-1 and processing tools (SNAP, ISCE)",
            (
                q(
                    "Which describes Sentinel-1's main interferometric acquisition?",
                    (
                        opt("An X-band spotlight over 5 km"),
                        opt(
                            "A C-band Interferometric Wide (IW) swath acquired in TOPS "
                            "mode, ~250 km wide, with ~12-day repeat per satellite",
                            correct=True,
                        ),
                        opt("An L-band nadir-looking profile"),
                        opt("An optical multispectral scan"),
                    ),
                    "Sentinel-1 IW/TOPS at C-band with a short repeat is what made "
                    "routine open InSAR possible.",
                ),
                q(
                    "Why does Sentinel-1 TOPS mode demand Enhanced Spectral Diversity (ESD)?",
                    (
                        opt("To colourise the interferogram"),
                        opt(
                            "The azimuth beam steering makes phase extremely sensitive to "
                            "misregistration, so bursts need sub-pixel co-registration "
                            "refinement",
                            correct=True,
                        ),
                        opt("To compress the file"),
                        opt("To remove speckle"),
                    ),
                    "TOPS needs co-registration far better than a thousandth of a pixel; "
                    "ESD refines the azimuth alignment across bursts.",
                ),
                q(
                    "What does the final Range-Doppler terrain-correction step do?",
                    (
                        opt("Unwraps the phase"),
                        opt(
                            "Warps the result from radar slant-range/azimuth geometry "
                            "into a map projection such as WGS84 or UTM",
                            correct=True,
                        ),
                        opt("Forms the interferogram"),
                        opt("Selects the sub-swath and bursts"),
                    ),
                    "Geocoding (terrain correction) moves the product into a real CRS so "
                    "it overlays a GIS; SNAPHU handles the unwrapping earlier.",
                ),
                q(
                    "Which pairing of open tools is standard for Sentinel-1 InSAR?",
                    (
                        opt("Photoshop and Excel"),
                        opt(
                            "ESA SNAP (with gpt) for standard interferograms, and "
                            "ISCE/MintPy for scriptable time-series processing",
                            correct=True,
                        ),
                        opt("Only a web browser"),
                        opt("A word processor and a spreadsheet"),
                    ),
                    "SNAP is the friendly graph-based path; ISCE2/3 with MintPy is the "
                    "research-grade scriptable path.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What fundamentally lets SAR image at night and through clouds?",
                    (
                        opt("It uses a very bright flash"),
                        opt(
                            "It is an active microwave sensor that supplies its own "
                            "illumination, and microwaves penetrate cloud",
                            correct=True,
                        ),
                        opt("It waits for clear-sky days only"),
                        opt("It measures thermal infrared"),
                    ),
                    "Active microwave sensing is independent of sunlight and largely "
                    "unaffected by cloud and weather.",
                ),
                q(
                    "The 'synthetic aperture' achieves fine azimuth resolution by…",
                    (
                        opt("using a kilometre-long physical antenna"),
                        opt(
                            "coherently combining echoes along the orbit to synthesize a "
                            "long virtual antenna, giving resolution near L/2",
                            correct=True,
                        ),
                        opt("increasing the transmit power"),
                        opt("flying much lower"),
                    ),
                    "Doppler processing of the along-track echoes builds a virtual "
                    "aperture; resolution tends to L/2, independent of range.",
                ),
                q(
                    "In a SAR image, what is radar 'shadow'?",
                    (
                        opt("A bright corner return"),
                        opt(
                            "A dark no-return region behind a steep feature that the "
                            "pulse never reached",
                            correct=True,
                        ),
                        opt("The compressed near slope of a hill"),
                        opt("A cloud over the scene"),
                    ),
                    "Shadow is un-illuminated ground (black); the compressed near slope "
                    "is foreshortening, and layover is the top imaged before the base.",
                ),
                q(
                    "Backscatter coefficient sigma nought is usually reported in…",
                    (
                        opt("degrees Celsius"),
                        opt("decibels, computed as 10 * log10(sigma0)", correct=True),
                        opt("metres per second"),
                        opt("pixels"),
                    ),
                    "sigma0 is a calibrated ratio expressed in dB; water is very dark, "
                    "double-bounce urban returns are bright.",
                ),
                q(
                    "Speckle in a single-look SAR image is best reduced by…",
                    (
                        opt("increasing the wavelength"),
                        opt(
                            "multilooking - averaging N independent looks, cutting "
                            "relative speckle by 1/sqrt(N) at the cost of resolution",
                            correct=True,
                        ),
                        opt("deleting dark pixels"),
                        opt("adding random noise"),
                    ),
                    "Averaging independent looks (or adaptive Lee/Frost filters) trades "
                    "resolution for lower speckle.",
                ),
                q(
                    "How is an interferogram formed and what does its phase represent?",
                    (
                        opt("Sum of two amplitudes; it represents brightness"),
                        opt(
                            "master times conjugate slave; its phase is the two-way path "
                            "difference mixing topography, motion and atmosphere",
                            correct=True,
                        ),
                        opt("Difference of intensities in dB; it represents temperature"),
                        opt("Product of two DEMs; it represents slope"),
                    ),
                    "The complex product's angle is the interferometric phase, a sum of "
                    "flat-Earth, topographic, deformation, atmospheric and noise terms.",
                ),
                q(
                    "For a C-band (5.6 cm) differential interferogram, one full fringe "
                    "equals how much line-of-sight displacement?",
                    (
                        opt("5.6 cm"),
                        opt("2.8 cm - half the wavelength", correct=True),
                        opt("28 cm"),
                        opt("0.56 mm"),
                    ),
                    "Two-way travel means one 2*pi fringe corresponds to lambda/2 of LOS motion.",
                ),
                q(
                    "For DEM generation versus deformation mapping, the baseline should be…",
                    (
                        opt("small for DEMs, large for deformation"),
                        opt(
                            "large for DEMs (high topographic sensitivity), small for "
                            "deformation (low topographic and geometric decorrelation)",
                            correct=True,
                        ),
                        opt("zero in both cases"),
                        opt("irrelevant in both cases"),
                    ),
                    "h_amb is inversely proportional to B_perp: DEM work wants a large "
                    "baseline, deformation work wants a small one.",
                ),
                q(
                    "What distinguishes PS-InSAR from a single interferogram?",
                    (
                        opt("It uses only one acquisition"),
                        opt(
                            "It processes a long stack, isolating persistent stable "
                            "scatterers and separating steady deformation from random "
                            "atmosphere to reach mm/year",
                            correct=True,
                        ),
                        opt("It ignores phase entirely"),
                        opt("It works only over open water"),
                    ),
                    "Stacking plus persistent-scatterer selection and atmospheric-phase "
                    "removal yields millimetre-per-year velocities.",
                ),
                q(
                    "Which is the standard open Sentinel-1 InSAR pipeline outline?",
                    (
                        opt("Colour balance, crop, sharpen, export JPEG"),
                        opt(
                            "Co-register (with ESD), form and filter the interferogram, "
                            "unwrap with SNAPHU, convert to displacement or height, then "
                            "terrain-correct to a map CRS",
                            correct=True,
                        ),
                        opt("Download GRD, classify clouds, mosaic"),
                        opt("Take two optical images and difference them"),
                    ),
                    "That SNAP/ISCE flow - co-registration, interferogram, unwrapping, "
                    "phase-to-motion, geocoding - is the standard path.",
                ),
            ),
            duration="12 min",
        ),
    ),
)

SAR_INSAR_COURSES: tuple[SeedCourse, ...] = (_SAR_INSAR,)
