"""Academy seed content - Remote Sensing Fundamentals.

The physics of seeing the Earth from above. This course builds intuition
for electromagnetic radiation and the spectrum, how the atmosphere
scatters and absorbs it, the spectral signatures of vegetation, water and
soil, the main sensor families (optical, multispectral, hyperspectral,
thermal and microwave), the four resolutions and their trade-offs, and the
correction chain that turns a raw digital number into physically meaningful
reflectance. Every lesson is a direct explanation with a concrete formula
or code example and a mermaid diagram, followed by a checkpoint quiz; the
course closes with a comprehensive final quiz.
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


_REMOTE_SENSING_FUNDAMENTALS = SeedCourse(
    slug="remote-sensing-fundamentals",
    title="Remote Sensing Fundamentals",
    description=(
        "The physics of seeing the Earth from above - electromagnetic "
        "radiation, spectral signatures, sensor types (optical, "
        "multispectral, hyperspectral, thermal), and resolution trade-offs. "
        "Every lesson pairs a direct explanation with a real formula or "
        "rasterio/NumPy example and a diagram, grounded in Landsat, "
        "Sentinel and Copernicus practice."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Remote Sensing Fundamentals

Remote sensing is measuring the Earth **without touching it** - by reading
the electromagnetic radiation that surfaces reflect and emit. Before you
can classify a crop, map a flood, or track a heat island, you need the
physics underneath: what light is, what the atmosphere does to it, why
grass and water and concrete look different to a sensor, and how a raw
pixel becomes a physical number.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short real example (a formula, a spectral index, a
rasterio snippet), and draws the idea as a diagram. After each lesson there
is a short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Electromagnetic radiation** - waves, the spectrum, energy
2. **Radiation and the atmosphere** - scattering, absorption, windows
3. **Spectral signatures** - why vegetation, water and soil differ
4. **Optical sensors** - panchromatic, multispectral, hyperspectral
5. **Thermal and microwave** - emitted heat and all-weather radar
6. **The four resolutions** - spatial, spectral, radiometric, temporal
7. **Correction** - radiometric and atmospheric
8. **From digital number to reflectance** - the calibration chain

This is the map. Everything downstream - indices, classification, change
detection, GeoAI - rests on these fundamentals, so it pays to get them
solid first.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What does 'remote sensing' fundamentally mean?",
                    (
                        opt("Physically sampling soil and water in the field"),
                        opt(
                            "Measuring the Earth without contact by reading the "
                            "electromagnetic radiation surfaces reflect and emit",
                            correct=True,
                        ),
                        opt("Controlling a satellite remotely"),
                        opt("Streaming video from a drone"),
                    ),
                    "Remote sensing infers surface properties from the radiation a "
                    "sensor detects at a distance.",
                ),
                q(
                    "Why does this course start with physics before applications?",
                    (
                        opt("Physics is required by the software licence"),
                        opt(
                            "Indices, classification and change detection all rest on "
                            "how radiation, the atmosphere and surfaces behave",
                            correct=True,
                        ),
                        opt("Applications are never covered"),
                        opt("It is only for exam purposes"),
                    ),
                    "Get the fundamentals solid and every downstream technique makes sense.",
                ),
            ),
        ),
        # -- 1. EM radiation and the spectrum --------------------------
        _t(
            "Electromagnetic radiation and the spectrum",
            "10 min",
            """# Electromagnetic radiation and the spectrum

All remote sensing begins with **electromagnetic (EM) radiation** - energy
that travels as coupled electric and magnetic waves at the speed of light,
needing no medium. A wave is described by its **wavelength** (lambda, the
distance between crests) and its **frequency** (nu, cycles per second). The
two are tied together by the speed of light:

```text
c = lambda * nu
  c      = speed of light = 3.0 x 10^8 m/s
  lambda = wavelength (m)
  nu     = frequency (Hz)

Photon energy:  E = h * nu = h * c / lambda
  h = Planck constant = 6.626 x 10^-34 J s

Example: green light, lambda = 0.55 micrometers
  nu = c / lambda = 3.0e8 / 0.55e-6 = 5.45 x 10^14 Hz
```

Two consequences matter. Shorter wavelength means **higher frequency and
higher energy** per photon (energy is inversely proportional to lambda).
And the full **electromagnetic spectrum** is just one continuum ordered by
wavelength - remote sensing uses named regions of it:

- **Visible** - about 0.4 to 0.7 micrometers (blue, green, red).
- **Near infrared (NIR)** - about 0.7 to 1.3 micrometers.
- **Shortwave infrared (SWIR)** - about 1.3 to 3 micrometers.
- **Thermal infrared (TIR)** - about 3 to 14 micrometers (emitted heat).
- **Microwave** - about 1 mm to 1 m (radar, all-weather).

The Sun is the dominant source in the visible and near infrared; the Earth
itself emits in the thermal infrared. Wavelength is measured in
**micrometers** (1 micrometer = 10^-6 m) for optical and infrared, and in
centimeters for microwave.

```mermaid
graph LR
    GAMMA["Gamma and X ray"] --> UV["Ultraviolet"]
    UV --> VIS["Visible 0.4 to 0.7 um"]
    VIS --> NIR["Near infrared"]
    NIR --> SWIR["Shortwave infrared"]
    SWIR --> TIR["Thermal infrared"]
    TIR --> MW["Microwave and radar"]
```

Remember: one continuum, ordered by wavelength; shorter wavelength carries
more energy; each sensor is built to read specific regions of it.
""",
        ),
        quiz_lesson(
            "Quiz: Electromagnetic radiation and the spectrum",
            (
                q(
                    "How are wavelength and frequency related for EM radiation?",
                    (
                        opt("They are equal"),
                        opt("They are unrelated"),
                        opt(
                            "Their product is the speed of light: c = lambda * nu, so "
                            "they are inversely proportional",
                            correct=True,
                        ),
                        opt("Frequency is always twice the wavelength"),
                    ),
                    "c = lambda * nu, so a shorter wavelength means a higher frequency.",
                ),
                q(
                    "Which statement about photon energy is correct?",
                    (
                        opt("Longer wavelength carries more energy per photon"),
                        opt(
                            "Shorter wavelength carries more energy per photon, since "
                            "E = h * c / lambda",
                            correct=True,
                        ),
                        opt("Energy does not depend on wavelength"),
                        opt("Energy depends only on distance from the source"),
                    ),
                    "Energy is inversely proportional to wavelength.",
                ),
                q(
                    "In which region does the Earth itself mainly emit radiation?",
                    (
                        opt("Visible light"),
                        opt("The thermal infrared, around 8 to 14 micrometers", correct=True),
                        opt("Ultraviolet"),
                        opt("Gamma rays"),
                    ),
                    "The Sun dominates the visible and near infrared; the Earth at "
                    "around 300 K emits in the thermal infrared.",
                ),
            ),
        ),
        # -- 2. Radiation and the atmosphere ---------------------------
        _t(
            "Radiation and the atmosphere",
            "10 min",
            """# Radiation and the atmosphere

Radiation from the Sun must pass **through the atmosphere twice** - down to
the surface and back up to the sensor - and the atmosphere changes it along
the way. Two effects dominate: **scattering** and **absorption**.

**Scattering** redirects radiation off gas molecules and particles.
**Rayleigh scattering** (by molecules much smaller than the wavelength) is
strongly wavelength dependent:

```text
Rayleigh scattering intensity proportional to 1 / lambda^4
  short wavelengths (blue) scatter far more than long (red)
  ratio blue to red = (0.65 / 0.47)^4 = about 3.7x

This is why the clear sky looks blue and why haze adds a bluish
path radiance to imagery that correction must remove.
```

**Mie scattering** (by aerosols and dust of size near the wavelength)
affects longer wavelengths and is what haze and thin cloud do. **Absorption**
is different: water vapor, carbon dioxide and ozone absorb radiation at
specific wavelengths, blocking those bands entirely.

The wavelengths that pass through relatively unabsorbed are the
**atmospheric windows** - and sensors are deliberately designed to look
through them:

```text
Atmospheric windows (wavelengths that transmit well):
  0.4 - 2.5 micrometers   visible, near and shortwave infrared
  3 - 5 micrometers       mid-wave thermal
  8 - 14 micrometers      thermal infrared (land surface temperature)
  above ~1 mm             microwave (passes clouds, day or night)
```

The energy reaching the sensor is the surface signal **plus** an additive
**path radiance** from scattering (haze) and **minus** what absorption
removed. Separating the true surface signal from these atmospheric effects
is the job of atmospheric correction (a later lesson).

```mermaid
graph TD
    SUN["Solar radiation"] --> DOWN["Down through atmosphere"]
    DOWN --> SCAT["Scattering adds path radiance"]
    DOWN --> ABS["Absorption removes bands"]
    SCAT --> SURF["Surface reflects signal"]
    ABS --> SURF
    SURF --> UP["Up through atmosphere"]
    UP --> SENSOR["Sensor reads signal plus haze"]
```

Remember: design your bands to sit inside atmospheric windows, expect haze
to add a wavelength-dependent bias (worst in the blue), and expect
absorption bands to be unusable.
""",
        ),
        quiz_lesson(
            "Quiz: Radiation and the atmosphere",
            (
                q(
                    "Rayleigh scattering is proportional to 1 / lambda^4. What does that imply?",
                    (
                        opt("Long wavelengths scatter most"),
                        opt(
                            "Short wavelengths (blue) scatter far more than long ones "
                            "(red), which is why the sky is blue and haze is bluish",
                            correct=True,
                        ),
                        opt("All wavelengths scatter equally"),
                        opt("Scattering does not depend on wavelength"),
                    ),
                    "The strong inverse-fourth-power dependence hits the blue end hardest.",
                ),
                q(
                    "What is an 'atmospheric window'?",
                    (
                        opt("A gap in the clouds"),
                        opt(
                            "A range of wavelengths that transmits through the atmosphere "
                            "with little absorption, so sensors are designed to use it",
                            correct=True,
                        ),
                        opt("The field of view of the sensor"),
                        opt("A software setting for contrast"),
                    ),
                    "Sensor bands are placed inside windows (for example 8 to 14 "
                    "micrometers for land surface temperature) and away from absorption "
                    "features.",
                ),
                q(
                    "Which effect adds an unwanted additive signal (path radiance) to imagery?",
                    (
                        opt("Absorption by water vapor"),
                        opt(
                            "Scattering of radiation into the sensor's view, worst in the blue",
                            correct=True,
                        ),
                        opt("The Earth's rotation"),
                        opt("Sensor dark current only"),
                    ),
                    "Scattering adds path radiance on top of the surface signal; "
                    "correction estimates and removes it.",
                ),
            ),
        ),
        # -- 3. Spectral signatures ------------------------------------
        _t(
            "Spectral signatures of surfaces",
            "10 min",
            """# Spectral signatures of surfaces

Every material reflects and absorbs radiation differently at different
wavelengths. Plot reflectance against wavelength and you get that
material's **spectral signature** - the fingerprint remote sensing uses to
tell surfaces apart. Three signatures anchor most land analysis:

- **Healthy vegetation** - absorbs red and blue light for photosynthesis
  (low reflectance there), reflects a little green (why leaves look green),
  and reflects **strongly in the near infrared** because of leaf cell
  structure. The sharp jump from low red to high NIR is the **red edge**,
  the single most useful feature in optical remote sensing.
- **Water** - reflects a little in the blue and green but **absorbs almost
  everything in the NIR and beyond**, so clear water is very dark in
  infrared bands. Sediment and algae raise visible reflectance.
- **Bare soil** - reflectance rises gently and steadily from visible into
  the infrared, with dips where soil moisture and clay absorb. It has no
  red edge, which separates it cleanly from vegetation.

That red-edge contrast is captured by the **Normalized Difference
Vegetation Index (NDVI)**, the workhorse of the field:

```python
import numpy as np

# Surface reflectance (0..1) for: vegetation, bare soil, water
red = np.array([0.04, 0.30, 0.05])
nir = np.array([0.45, 0.35, 0.02])

ndvi = (nir - red) / (nir + red)
print(ndvi)   # ~ [ 0.84  0.08 -0.43 ]
# high positive -> dense vegetation
# near zero     -> bare soil or rock
# negative      -> water, snow or cloud
```

NDVI ranges from -1 to +1: it is high where NIR far exceeds red (vegetation)
and negative over water. Because it is a **normalized ratio**, it partly
cancels differences in illumination and slope.

```mermaid
graph LR
    VEG["Vegetation"] --> RE["Strong red edge, high NIR"]
    WAT["Water"] --> LOWNIR["Absorbs NIR, dark in infrared"]
    SOIL["Bare soil"] --> RISE["Gentle steady rise, no red edge"]
    RE --> IDX["NDVI separates the classes"]
    LOWNIR --> IDX
    RISE --> IDX
```

Remember: surfaces differ by wavelength, the vegetation red edge is the key
optical feature, and simple band ratios like NDVI turn those differences
into a number you can map.
""",
        ),
        quiz_lesson(
            "Quiz: Spectral signatures of surfaces",
            (
                q(
                    "What is the 'red edge' in a vegetation spectral signature?",
                    (
                        opt("A calibration error at the edge of the sensor"),
                        opt(
                            "The sharp rise in reflectance from low in the red to high "
                            "in the near infrared - the key feature of healthy vegetation",
                            correct=True,
                        ),
                        opt("The red border drawn around a map"),
                        opt("A type of atmospheric absorption"),
                    ),
                    "Chlorophyll absorbs red while leaf structure reflects NIR, producing "
                    "the steep red edge.",
                ),
                q(
                    "Why is clear water very dark in near-infrared bands?",
                    (
                        opt("Water reflects NIR strongly"),
                        opt(
                            "Water absorbs almost all near-infrared radiation, so little "
                            "is reflected back to the sensor",
                            correct=True,
                        ),
                        opt("NIR cannot reach the ground"),
                        opt("Sensors ignore water pixels"),
                    ),
                    "Strong NIR absorption makes water appear dark, which helps map water bodies.",
                ),
                q(
                    "For the values red = 0.04 and nir = 0.45, what is NDVI = (nir - red) / (nir + red)?",
                    (
                        opt("About -0.84"),
                        opt("About 0.0"),
                        opt("About 0.84, indicating dense vegetation", correct=True),
                        opt("Exactly 1.0"),
                    ),
                    "(0.45 - 0.04) / (0.45 + 0.04) = 0.41 / 0.49 = about 0.84.",
                ),
            ),
        ),
        # -- 4. Optical sensors ----------------------------------------
        _t(
            "Sensors: optical, multispectral and hyperspectral",
            "10 min",
            """# Sensors: optical, multispectral and hyperspectral

Optical sensors measure reflected sunlight. They differ mainly in **how
they divide the spectrum into bands** - a trade-off between spectral detail
and other resolutions.

- **Panchromatic** - one broad band covering most of the visible. No color
  information, but it collects a lot of light, so it delivers the **finest
  spatial detail** (for example the 15 m panchromatic band on Landsat 8).
- **Multispectral** - a handful of discrete, fairly wide bands placed at
  informative wavelengths (blue, green, red, NIR, SWIR). Landsat and
  Sentinel-2 are multispectral; enough color and infrared to compute
  indices and classify land cover.
- **Hyperspectral** - hundreds of very narrow, contiguous bands that
  reconstruct a nearly continuous spectrum for every pixel. This resolves
  fine absorption features and can identify specific minerals, crop stress,
  or materials - at the cost of huge data volumes and lower spatial or
  temporal coverage.

A quick comparison of common optical missions:

```text
Sensor          Type            Bands   Typical GSD
--------------- --------------- ------- -----------
Landsat 8 PAN   panchromatic    1       15 m
Landsat 8 OLI   multispectral   ~9      30 m
Sentinel-2 MSI  multispectral   13      10 to 60 m
PRISMA / EnMAP  hyperspectral   ~200+   30 m
```

You read these bands as a stacked raster (often a GeoTIFF). With rasterio:

```python
import rasterio

with rasterio.open("sentinel2_scene.tif") as src:
    print(src.count)          # number of bands, e.g. 13
    print(src.crs)            # coordinate reference system, e.g. EPSG:32633
    red = src.read(4)         # Sentinel-2 band 4 (red)
    nir = src.read(8)         # Sentinel-2 band 8 (NIR, 10 m)
```

The core idea: more bands means richer spectral discrimination, but light
is finite, so gains in spectral resolution usually trade against spatial
detail, swath width, or revisit frequency.

```mermaid
graph TD
    LIGHT["Reflected sunlight"] --> PAN["Panchromatic one wide band"]
    LIGHT --> MULTI["Multispectral few bands"]
    LIGHT --> HYPER["Hyperspectral hundreds of bands"]
    PAN --> DETAIL["Best spatial detail"]
    MULTI --> INDEX["Indices and land cover"]
    HYPER --> MATERIAL["Material identification"]
```

Remember: panchromatic for detail, multispectral for practical land
analysis and indices, hyperspectral for identifying materials - each buys
spectral richness by spending some other resolution.
""",
        ),
        quiz_lesson(
            "Quiz: Sensors: optical, multispectral and hyperspectral",
            (
                q(
                    "What distinguishes a hyperspectral sensor from a multispectral one?",
                    (
                        opt("It has higher spatial resolution by definition"),
                        opt(
                            "It records hundreds of very narrow, contiguous bands, "
                            "reconstructing a near-continuous spectrum per pixel",
                            correct=True,
                        ),
                        opt("It only records a single broad band"),
                        opt("It works only at night"),
                    ),
                    "Multispectral uses a handful of wide bands; hyperspectral uses "
                    "hundreds of narrow ones for fine spectral detail.",
                ),
                q(
                    "Why does a panchromatic band usually offer the finest spatial detail?",
                    (
                        opt("It uses a longer wavelength"),
                        opt(
                            "One broad band collects more light, so smaller pixels still "
                            "receive enough signal for a sharp image",
                            correct=True,
                        ),
                        opt("It has more bands"),
                        opt("It ignores the atmosphere"),
                    ),
                    "Trading color for light-gathering lets panchromatic pixels be "
                    "smaller (for example 15 m on Landsat 8).",
                ),
                q(
                    "In the rasterio snippet, what does src.read(8) return for the Sentinel-2 scene?",
                    (
                        opt("The coordinate reference system"),
                        opt("The number of bands"),
                        opt("The pixel values of band 8 (the NIR band)", correct=True),
                        opt("The file size"),
                    ),
                    "read(n) returns the array of pixel values for band n; band 8 is "
                    "Sentinel-2's 10 m NIR band.",
                ),
            ),
        ),
        # -- 5. Thermal and microwave ----------------------------------
        _t(
            "Thermal and microwave remote sensing",
            "10 min",
            """# Thermal and microwave remote sensing

Not all remote sensing reads reflected sunlight. Two families read
different physics entirely.

**Thermal infrared** sensors measure the radiation an object **emits**
because it is warm, not what it reflects - so they work day and night. A
warmer object emits more, and at a shorter peak wavelength. Two laws
govern it:

```text
Stefan-Boltzmann (total emitted power):
  M = epsilon * sigma * T^4
    sigma   = 5.67 x 10^-8 W m^-2 K^-4
    epsilon = emissivity (0..1, how efficiently a surface radiates)
    T       = temperature in kelvin

Wien displacement (peak wavelength):
  lambda_max = b / T,   b = 2898 micrometers K
  Earth at T = 300 K -> lambda_max = 2898 / 300 = 9.66 micrometers
```

That is why thermal bands sit near 8 to 14 micrometers: it is both an
atmospheric window and where the Earth peaks. Applications include land
surface temperature, urban heat islands, wildfire detection, and
evapotranspiration. The catch: recovering true temperature requires knowing
the surface **emissivity** (water, soil and metal differ).

**Microwave** sensing uses wavelengths of centimeters. **Passive**
microwave measures naturally emitted microwaves (soil moisture, sea ice).
**Active** microwave - **radar / SAR** - sends its own pulse and times the
echo, so it needs no sunlight and, crucially, **penetrates clouds, haze and
rain**. That makes SAR the all-weather, day-or-night workhorse for flood
mapping, deformation (InSAR), and monitoring cloudy tropics. Radar responds
to surface roughness, geometry and moisture rather than color.

```mermaid
graph TD
    SRC["Energy source"] --> THERM["Thermal emitted heat"]
    SRC --> PASS["Passive microwave emitted"]
    SRC --> ACT["Active radar own pulse"]
    THERM --> TEMP["Surface temperature day and night"]
    PASS --> MOIST["Soil moisture and sea ice"]
    ACT --> ALLW["All weather cloud penetrating"]
```

Remember: thermal reads emitted heat (needs emissivity, works at night);
radar makes its own illumination and sees through clouds - both fill the
gaps that sunlit optical sensors cannot.
""",
        ),
        quiz_lesson(
            "Quiz: Thermal and microwave remote sensing",
            (
                q(
                    "Why can thermal infrared sensors operate at night?",
                    (
                        opt("They use a powerful lamp"),
                        opt(
                            "They measure radiation the surface emits because it is warm, "
                            "not reflected sunlight",
                            correct=True,
                        ),
                        opt("They only work with moonlight"),
                        opt("They are actually radar"),
                    ),
                    "Emitted thermal radiation is present day and night, unlike reflected "
                    "sunlight.",
                ),
                q(
                    "By Wien's law, a warmer object's emission peak moves which way?",
                    (
                        opt("To longer wavelengths"),
                        opt("To shorter wavelengths, since lambda_max = b / T", correct=True),
                        opt("It does not move"),
                        opt("It disappears"),
                    ),
                    "lambda_max is inversely proportional to temperature, so hotter means "
                    "a shorter peak wavelength.",
                ),
                q(
                    "What is the key advantage of active radar (SAR) over optical sensors?",
                    (
                        opt("It produces natural color images"),
                        opt("It has the finest spectral resolution"),
                        opt(
                            "It supplies its own illumination and penetrates clouds, so it "
                            "works day or night in any weather",
                            correct=True,
                        ),
                        opt("It requires bright sunlight"),
                    ),
                    "SAR is the all-weather, day-or-night workhorse, ideal for cloudy "
                    "regions and flood mapping.",
                ),
            ),
        ),
        # -- 6. The four resolutions -----------------------------------
        _t(
            "Spatial, spectral, radiometric and temporal resolution",
            "10 min",
            """# Spatial, spectral, radiometric and temporal resolution

Every sensor is described by **four resolutions**, and they trade against
each other - improving one usually costs another.

- **Spatial resolution** - the ground size of one pixel, the **ground
  sample distance (GSD)**. Smaller GSD sees finer detail. Landsat is 30 m,
  Sentinel-2 is 10 m, commercial satellites reach under 1 m.
- **Spectral resolution** - how many bands and how narrow. More, narrower
  bands distinguish more materials (multispectral versus hyperspectral).
- **Radiometric resolution** - how finely brightness is quantized, in
  **bits**. 8-bit stores 256 levels; 12-bit stores 4096; more bits capture
  subtle differences between dark and bright targets.
- **Temporal resolution** - the **revisit time**, how often the sensor
  images the same place. Landsat is about 16 days; Sentinel-2 is about 5
  days; geostationary weather satellites, minutes.

Spatial resolution follows directly from the optics and orbit:

```text
Ground sample distance (GSD):
  GSD = (pixel_pitch * H) / f
    pixel_pitch = detector pixel size (m)
    H = sensor altitude (m)
    f = focal length (m)

Example: pitch = 6.5 micrometers, H = 700 km, f = 0.5 m
  GSD = (6.5e-6 * 700000) / 0.5 = 9.1 m per pixel
```

Radiometric depth is just how many discrete levels the analog signal is
mapped to:

```text
Number of brightness levels = 2 ^ bits
  8-bit  -> 256 levels
  12-bit -> 4096 levels   (Landsat 8, Sentinel-2)
  16-bit -> 65536 levels
```

The trade-offs are physical: a finer GSD collects less light per pixel, so
you often widen the band (less spectral resolution) or accept a narrower
swath (less frequent revisit). Choose the sensor by which resolution your
application needs most - detail, spectra, subtle contrast, or frequent
updates.

```mermaid
graph TD
    SENSOR["Sensor design"] --> SPAT["Spatial pixel size GSD"]
    SENSOR --> SPEC["Spectral number of bands"]
    SENSOR --> RAD["Radiometric bit depth"]
    SENSOR --> TEMP["Temporal revisit time"]
    SPAT --> TRADE["Resolutions trade off"]
    SPEC --> TRADE
    RAD --> TRADE
    TEMP --> TRADE
```

Remember: spatial for detail, spectral for material, radiometric for subtle
contrast, temporal for change - you cannot maximize all four at once, so
match the sensor to the job.
""",
        ),
        quiz_lesson(
            "Quiz: Spatial, spectral, radiometric and temporal resolution",
            (
                q(
                    "What does radiometric resolution describe?",
                    (
                        opt("The ground size of a pixel"),
                        opt("The revisit time of the satellite"),
                        opt(
                            "How finely brightness is quantized, expressed in bits (for "
                            "example 12-bit stores 4096 levels)",
                            correct=True,
                        ),
                        opt("The number of spectral bands"),
                    ),
                    "More bits means more brightness levels and finer contrast between "
                    "dark and bright targets.",
                ),
                q(
                    "Using GSD = (pixel_pitch * H) / f with pitch = 6.5 um, H = 700 km, f = 0.5 m, the GSD is about:",
                    (
                        opt("About 0.9 m"),
                        opt("About 9.1 m", correct=True),
                        opt("About 91 m"),
                        opt("About 700 m"),
                    ),
                    "(6.5e-6 * 700000) / 0.5 = 4.55 / 0.5 = 9.1 m per pixel.",
                ),
                q(
                    "Why can a sensor not maximize all four resolutions at once?",
                    (
                        opt("Software limits the file size"),
                        opt(
                            "They trade off physically - finer pixels collect less light, "
                            "so you give up spectral bands, swath, or revisit frequency",
                            correct=True,
                        ),
                        opt("Governments forbid it"),
                        opt("They do not actually trade off"),
                    ),
                    "Light is finite; gains in one resolution usually cost another, so you "
                    "match the sensor to the application.",
                ),
            ),
        ),
        # -- 7. Radiometric and atmospheric correction -----------------
        _t(
            "Radiometric and atmospheric correction",
            "10 min",
            """# Radiometric and atmospheric correction

A raw image is not yet physically meaningful. Getting from raw counts to
comparable surface reflectance is a **correction chain**, and it runs in a
sensible order.

- **Radiometric correction** first fixes the sensor itself: it converts raw
  **digital numbers** to physical **radiance** using the sensor's
  calibration (gain and offset), and repairs artifacts like dropped lines,
  striping between detectors, and dark-current bias. This makes bands and
  scenes comparable in physical units.
- **Atmospheric correction** then removes what the air did (from the
  atmosphere lesson): the additive **path radiance** from scattering and the
  **transmission losses** from absorption. The goal is **surface
  reflectance** - what the ground would look like with no atmosphere - so
  images from different dates and angles can be compared and indices behave
  consistently.

The simplest atmospheric method is **Dark Object Subtraction (DOS)**: assume
the darkest pixels in a scene (deep shadow, clear water) should be near
zero, so whatever brightness they show is haze, and subtract it:

```python
import numpy as np

# Dark Object Subtraction - a first-order haze removal
def dark_object_subtract(band: np.ndarray) -> np.ndarray:
    haze = np.percentile(band, 1)     # ~ darkest real pixels = path radiance
    corrected = band - haze
    return np.clip(corrected, 0, None)  # no negative reflectance
```

DOS is a rough approximation. Physically based models (6S, MODTRAN, Sen2Cor
for Sentinel-2, LaSRC for Landsat) model scattering and absorption from
aerosol and water-vapor estimates and are what analysis-ready products use.
The order matters: **DN to radiance, then radiance to surface reflectance** -
never mix scenes from before and after correction.

```mermaid
graph LR
    DN["Raw digital numbers"] --> RAD["Radiometric correction to radiance"]
    RAD --> TOA["Top of atmosphere reflectance"]
    TOA --> ATM["Atmospheric correction"]
    ATM --> SR["Surface reflectance"]
    SR --> READY["Analysis ready and comparable"]
```

Remember: correct the sensor first (DN to radiance), then remove the
atmosphere (to surface reflectance); only then are indices and multi-date
comparisons trustworthy.
""",
        ),
        quiz_lesson(
            "Quiz: Radiometric and atmospheric correction",
            (
                q(
                    "What does radiometric correction primarily fix?",
                    (
                        opt("The map projection"),
                        opt(
                            "Sensor effects - converting digital numbers to physical "
                            "radiance and repairing striping, dropped lines and bias",
                            correct=True,
                        ),
                        opt("The scattering of the atmosphere"),
                        opt("The file format"),
                    ),
                    "Radiometric correction addresses the sensor; atmospheric correction "
                    "addresses the air.",
                ),
                q(
                    "What assumption underlies Dark Object Subtraction?",
                    (
                        opt("The brightest pixels are pure vegetation"),
                        opt(
                            "The darkest pixels (deep shadow, clear water) should be near "
                            "zero, so their brightness estimates the haze to subtract",
                            correct=True,
                        ),
                        opt("Every pixel has the same reflectance"),
                        opt("The atmosphere adds no signal"),
                    ),
                    "DOS treats the residual brightness of dark objects as path radiance "
                    "and removes it.",
                ),
                q(
                    "What is the correct order of the correction chain?",
                    (
                        opt("Atmospheric correction, then radiometric correction"),
                        opt(
                            "Digital number to radiance (radiometric), then radiance to "
                            "surface reflectance (atmospheric)",
                            correct=True,
                        ),
                        opt("Only atmospheric correction is ever needed"),
                        opt("The order does not matter"),
                    ),
                    "Fix the sensor first, then remove the atmosphere, to reach comparable "
                    "surface reflectance.",
                ),
            ),
        ),
        # -- 8. DN to reflectance --------------------------------------
        _t(
            "From digital number to reflectance",
            "10 min",
            """# From digital number to reflectance

This lesson makes the chain concrete with real numbers. A pixel arrives as
a **digital number (DN)** - an integer count with no physical meaning on its
own. The satellite provider ships **metadata** (Landsat's MTL file,
Sentinel-2's product XML) with the calibration coefficients that convert it.

For **Landsat 8**, going straight to **top-of-atmosphere (TOA) reflectance**
uses a simple linear rescale plus a solar-angle correction:

```python
import numpy as np

# Landsat 8 - DN to top-of-atmosphere reflectance
# rho' = M_rho * DN + A_rho   (coefficients from the MTL metadata)
M_rho = 2.0e-5     # REFLECTANCE_MULT_BAND_x
A_rho = -0.1       # REFLECTANCE_ADD_BAND_x

def dn_to_toa_reflectance(dn: np.ndarray, sun_elevation_deg: float) -> np.ndarray:
    rho_prime = M_rho * dn + A_rho              # uncorrected reflectance
    rho = rho_prime / np.sin(np.radians(sun_elevation_deg))  # solar angle
    return np.clip(rho, 0, 1)

# Example: DN = 12000, sun 55 deg above horizon
#   rho' = 2.0e-5 * 12000 - 0.1 = 0.14
#   rho  = 0.14 / sin(55 deg) = 0.14 / 0.819 = 0.171
```

Why divide by the sine of the **sun elevation**? When the Sun is low, the
same surface receives less illumination per unit area, so the raw value must
be scaled up to recover true reflectance. This normalization lets scenes
from different seasons and latitudes be compared.

TOA reflectance still includes the atmosphere. Applying the previous
lesson's atmospheric correction converts TOA to **surface reflectance** -
the analysis-ready value, typically stored 0 to 1 (or scaled to integers).
Only at this point should you compute indices like NDVI or run a classifier,
because the numbers now mean the same thing across bands, dates and places.

```mermaid
graph LR
    DN["Digital number integer"] --> SCALE["Apply gain and offset"]
    SCALE --> TOAP["Uncorrected reflectance"]
    TOAP --> SUN["Divide by sine of sun elevation"]
    SUN --> TOA["Top of atmosphere reflectance"]
    TOA --> ATMC["Atmospheric correction"]
    ATMC --> SR["Surface reflectance zero to one"]
```

Remember: DN is meaningless until you apply the metadata coefficients; a
gain-and-offset rescale plus a solar-angle term gives TOA reflectance, and
atmospheric correction finishes the job at surface reflectance - the value
every downstream analysis should use.
""",
        ),
        quiz_lesson(
            "Quiz: From digital number to reflectance",
            (
                q(
                    "What is a digital number (DN) before calibration?",
                    (
                        opt("A physically meaningful reflectance"),
                        opt(
                            "A raw integer count from the detector with no physical "
                            "meaning until metadata coefficients are applied",
                            correct=True,
                        ),
                        opt("The surface temperature in kelvin"),
                        opt("A coordinate in the projection"),
                    ),
                    "You must apply the provider's gain and offset (from the MTL or "
                    "product XML) to give a DN physical meaning.",
                ),
                q(
                    "Why divide the rescaled value by the sine of the sun elevation angle?",
                    (
                        opt("To convert to kelvin"),
                        opt(
                            "A low Sun delivers less illumination per unit area, so "
                            "dividing by sin(elevation) recovers true reflectance and "
                            "lets scenes be compared",
                            correct=True,
                        ),
                        opt("To remove clouds"),
                        opt("To change the map projection"),
                    ),
                    "The solar-angle term normalizes for illumination geometry across "
                    "seasons and latitudes.",
                ),
                q(
                    "At what stage should you compute indices like NDVI or run a classifier?",
                    (
                        opt("On the raw digital numbers"),
                        opt("On uncorrected reflectance before the solar term"),
                        opt(
                            "On surface reflectance, after both radiometric and "
                            "atmospheric correction, so values are comparable",
                            correct=True,
                        ),
                        opt("It never matters which stage"),
                    ),
                    "Only at surface reflectance do the numbers mean the same thing across "
                    "bands, dates and places.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "How are wavelength and frequency related for electromagnetic radiation?",
                    (
                        opt("They are independent"),
                        opt(
                            "c = lambda * nu, so they are inversely proportional - shorter "
                            "wavelength means higher frequency",
                            correct=True,
                        ),
                        opt("Frequency equals wavelength"),
                        opt("Both increase together without limit"),
                    ),
                    "The product of wavelength and frequency is the constant speed of light.",
                ),
                q(
                    "Rayleigh scattering is proportional to 1 / lambda^4. What follows?",
                    (
                        opt("Red light scatters most"),
                        opt(
                            "Blue (short wavelength) scatters far more than red, adding a "
                            "bluish haze that correction must remove",
                            correct=True,
                        ),
                        opt("Scattering is wavelength independent"),
                        opt("Only the thermal band scatters"),
                    ),
                    "The steep inverse dependence hits short wavelengths hardest.",
                ),
                q(
                    "What is an atmospheric window?",
                    (
                        opt("A gap in the satellite's orbit"),
                        opt(
                            "A wavelength range that transmits through the atmosphere with "
                            "little absorption, where sensor bands are placed",
                            correct=True,
                        ),
                        opt("A user-interface panel"),
                        opt("The sensor's dark current"),
                    ),
                    "Bands are designed to sit in windows and avoid absorption features.",
                ),
                q(
                    "What is the vegetation 'red edge'?",
                    (
                        opt("A defect at the image border"),
                        opt(
                            "The sharp rise from low red reflectance to high near-infrared "
                            "reflectance - the signature of healthy vegetation",
                            correct=True,
                        ),
                        opt("An atmospheric absorption band"),
                        opt("A radar echo"),
                    ),
                    "The red edge is the most useful feature in optical vegetation "
                    "analysis and drives NDVI.",
                ),
                q(
                    "NDVI is defined as which expression?",
                    (
                        opt("(red - nir) / (red * nir)"),
                        opt("(nir - red) / (nir + red)", correct=True),
                        opt("nir + red"),
                        opt("red / nir only"),
                    ),
                    "The normalized difference of NIR and red ranges from -1 to +1 and is "
                    "high over vegetation.",
                ),
                q(
                    "What distinguishes hyperspectral from multispectral sensors?",
                    (
                        opt("Hyperspectral always has finer spatial resolution"),
                        opt(
                            "Hyperspectral records hundreds of narrow contiguous bands "
                            "versus a handful of wide multispectral bands",
                            correct=True,
                        ),
                        opt("Multispectral works only at night"),
                        opt("They are identical"),
                    ),
                    "Hundreds of narrow bands let hyperspectral identify specific "
                    "materials, at the cost of data volume.",
                ),
                q(
                    "Why can radar (SAR) image through clouds day or night?",
                    (
                        opt("It uses reflected sunlight efficiently"),
                        opt(
                            "It is active - it transmits its own microwave pulse, which "
                            "penetrates clouds and needs no sunlight",
                            correct=True,
                        ),
                        opt("It measures visible color"),
                        opt("It only works in clear skies"),
                    ),
                    "Active microwave supplies its own illumination and penetrates "
                    "weather, unlike optical sensors.",
                ),
                q(
                    "Which four resolutions describe a remote sensing system?",
                    (
                        opt("Speed, cost, weight, power"),
                        opt(
                            "Spatial (pixel size), spectral (bands), radiometric (bit "
                            "depth), and temporal (revisit time)",
                            correct=True,
                        ),
                        opt("Red, green, blue, infrared"),
                        opt("Gain, offset, bias, noise"),
                    ),
                    "The four resolutions trade against one another, so you match the "
                    "sensor to the application.",
                ),
                q(
                    "Using GSD = (pixel_pitch * H) / f, larger pixel_pitch or altitude does what to GSD?",
                    (
                        opt("Decreases GSD, giving finer detail"),
                        opt(
                            "Increases GSD, giving coarser detail, while a longer focal "
                            "length decreases it",
                            correct=True,
                        ),
                        opt("Has no effect on GSD"),
                        opt("Changes only the number of bands"),
                    ),
                    "GSD grows with pixel pitch and altitude and shrinks with focal length.",
                ),
                q(
                    "What is the correct order to turn a raw pixel into analysis-ready data?",
                    (
                        opt("Compute NDVI first, then correct"),
                        opt(
                            "DN to radiance/TOA reflectance (radiometric, with solar "
                            "angle), then atmospheric correction to surface reflectance",
                            correct=True,
                        ),
                        opt("Atmospheric correction before any sensor calibration"),
                        opt("No correction is ever needed"),
                    ),
                    "Calibrate the sensor, apply the solar term, then remove the "
                    "atmosphere - only then compute indices.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

REMOTE_SENSING_FUNDAMENTALS_COURSES: tuple[SeedCourse, ...] = (_REMOTE_SENSING_FUNDAMENTALS,)
