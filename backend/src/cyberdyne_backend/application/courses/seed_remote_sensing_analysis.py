"""Academy seed content - Remote Sensing Analysis.

Turning satellite imagery into information. This course teaches the core
analytical workflow of optical remote sensing: reading spectral bands and
doing band math, computing vegetation, water and burn indices (NDVI,
SAVI, EVI, NDWI, NBR), enhancing and compositing imagery, classifying
scenes with unsupervised and supervised methods, detecting change over
time, and processing rasters in practice with GDAL and rasterio. Every
lesson is a direct explanation grounded in real sensors (Sentinel-2,
Landsat) and standards, with a spectral or code example and a mermaid
diagram, followed by a checkpoint quiz; the course closes with a
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


_REMOTE_SENSING_ANALYSIS = SeedCourse(
    slug="remote-sensing-analysis",
    title="Remote Sensing Analysis",
    description=(
        "Turn satellite imagery into information: spectral bands and band "
        "math, vegetation, water and burn indices (NDVI, NDWI, NBR, SAVI, "
        "EVI), unsupervised and supervised image classification, change "
        "detection, and hands-on raster processing with GDAL and rasterio - "
        "grounded in Sentinel-2 and Landsat data with a formula, a code "
        "example and a diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Remote Sensing Analysis

A satellite image is not a photograph - it is a stack of **measurements**.
Each pixel records how much light the ground reflected in several
wavelength bands, and the whole craft of remote sensing analysis is
turning those numbers into information: how green the vegetation is, where
the water and the burn scars are, what land cover each pixel belongs to,
and what changed since last month.

This course is **practical and concrete**. Every lesson explains one idea
directly, shows it as a real formula or a short GDAL/rasterio/NumPy
snippet, and draws the workflow as a diagram. After each lesson there is a
short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Spectral bands and band math** - what the numbers in a pixel mean
2. **Vegetation indices** - NDVI, SAVI, EVI
3. **Water and burn indices** - NDWI, NBR
4. **Image enhancement and composites** - making imagery readable
5. **Unsupervised classification** - k-means and ISODATA
6. **Supervised classification** - maximum likelihood and random forest
7. **Change detection** - measuring what moved between two dates
8. **Processing rasters** - doing it for real with GDAL and rasterio

The running examples use **Sentinel-2** (10-20 m, 13 bands) and
**Landsat 8/9** (30 m), the two workhorses of open optical imagery. Learn
the analysis here and it transfers to any multispectral sensor.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is a multispectral satellite image, fundamentally?",
                    (
                        opt("A single ordinary color photograph"),
                        opt(
                            "A stack of per-pixel reflectance measurements across "
                            "several wavelength bands",
                            correct=True,
                        ),
                        opt("A vector map of roads and buildings"),
                        opt("A text file of coordinates"),
                    ),
                    "Each pixel stores how much light the surface reflected in each "
                    "band; analysis turns those numbers into information.",
                ),
                q(
                    "Which two open sensors are the running examples in this course?",
                    (
                        opt("Only webcams and drones"),
                        opt("Sentinel-2 and Landsat 8/9", correct=True),
                        opt("GPS and GLONASS"),
                        opt("Radar altimeters only"),
                    ),
                    "Sentinel-2 (10-20 m) and Landsat 8/9 (30 m) are the workhorses of "
                    "open optical imagery.",
                ),
            ),
        ),
        # -- 1. Spectral bands and band math ---------------------------
        _t(
            "Spectral bands and band math",
            "10 min",
            """# Spectral bands and band math

Different surfaces reflect light differently at different wavelengths -
that pattern is a **spectral signature**. A multispectral sensor samples
the signature in discrete **bands**: for example Sentinel-2 has blue
(B2, 490 nm), green (B3, 560 nm), red (B4, 665 nm) and near-infrared
(B8, 842 nm), among 13 bands total. Healthy vegetation absorbs red light
(chlorophyll) and reflects a lot of near-infrared - that gap is the basis
of almost every vegetation index.

Raw pixel values come as **Digital Numbers (DN)**. To compare images or
apply formulas you convert DN to a physical quantity, usually
**surface reflectance** (a 0 to 1 ratio). Sensors ship the linear
scaling; for Landsat Collection 2 surface reflectance the conversion is:

```text
reflectance = DN * scale_factor + offset
Landsat C2 SR: scale_factor = 0.0000275, offset = -0.2

Example: DN = 10000
reflectance = 10000 * 0.0000275 + (-0.2) = 0.075
```

**Band math** is simply doing arithmetic on the aligned band arrays,
pixel by pixel. A ratio or normalized difference cancels much of the
scene-wide brightness variation (illumination, slope), which is why
indices are written as ratios rather than raw differences:

```python
import numpy as np
# red and nir are 2D float arrays of surface reflectance
ratio = nir / red                       # simple band ratio
ndiff = (nir - red) / (nir + red)       # normalized difference in [-1, 1]
```

The **electromagnetic spectrum** used in optical remote sensing, from
short to long wavelength, and what each region is good for:

```mermaid
graph LR
    B["Blue 490 nm"] --> G["Green 560 nm"]
    G --> R["Red 665 nm"]
    R --> NIR["Near infrared 842 nm"]
    NIR --> SWIR["Shortwave infrared 1600 nm"]
    B --> WATER["Water and haze"]
    R --> CHLORO["Chlorophyll absorption"]
    NIR --> VEG["Vegetation structure"]
    SWIR --> MOIST["Moisture and burn"]
```

Remember: a pixel is a spectral signature sampled into bands; convert DN
to reflectance first, then let band math turn the physics into an index.
""",
        ),
        quiz_lesson(
            "Quiz: Spectral bands and band math",
            (
                q(
                    "What is a 'spectral signature'?",
                    (
                        opt("The name of the satellite that took the image"),
                        opt(
                            "The pattern of how a surface reflects light across "
                            "different wavelengths",
                            correct=True,
                        ),
                        opt("A digital watermark in the file"),
                        opt("The compression format of the raster"),
                    ),
                    "Each material reflects differently per wavelength; sampling that "
                    "pattern into bands is what a multispectral sensor does.",
                ),
                q(
                    "Why convert Digital Numbers (DN) to surface reflectance before "
                    "applying index formulas?",
                    (
                        opt("To make the file smaller"),
                        opt(
                            "To get a physical 0 to 1 quantity that is comparable across "
                            "images and valid for the formulas",
                            correct=True,
                        ),
                        opt("Because DN cannot be stored on disk"),
                        opt("It is only needed for radar data"),
                    ),
                    "reflectance = DN * scale + offset gives a physical value; raw DN "
                    "differs by scene and is not directly comparable.",
                ),
                q(
                    "Why are indices written as ratios or normalized differences rather "
                    "than raw band differences?",
                    (
                        opt("Ratios look nicer on a chart"),
                        opt(
                            "A ratio cancels much of the scene-wide brightness variation "
                            "from illumination and slope",
                            correct=True,
                        ),
                        opt("Because subtraction is not allowed in NumPy"),
                        opt("To force the result to be an integer"),
                    ),
                    "Normalizing by the sum removes common brightness factors, so the "
                    "index reflects surface type rather than lighting.",
                ),
            ),
        ),
        # -- 2. Vegetation indices -------------------------------------
        _t(
            "Vegetation indices (NDVI, SAVI, EVI)",
            "11 min",
            """# Vegetation indices (NDVI, SAVI, EVI)

Vegetation indices combine the **red** and **near-infrared (NIR)** bands
to measure how much healthy green vegetation is in a pixel. Chlorophyll
absorbs red and leaves scatter NIR, so a large NIR-minus-red gap means
vigorous plants.

The classic is **NDVI**, the Normalized Difference Vegetation Index:

```text
NDVI = (NIR - Red) / (NIR + Red)

Ranges from -1 to +1:
  ~ 0.6 to 0.9   dense, healthy vegetation
  ~ 0.2 to 0.5   sparse vegetation, grassland
  ~ 0.0 to 0.1   bare soil, rock
  < 0            water, snow, clouds

Sentinel-2: NIR = B8, Red = B4
Landsat 8/9: NIR = B5,  Red = B4
```

NDVI has two well-known weaknesses that the other indices fix:

- **Soil brightness** shows through in sparse canopies. **SAVI**, the
  Soil-Adjusted Vegetation Index, adds a soil factor **L** (about 0.5 for
  intermediate cover) to suppress it:

```text
SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L),   L = 0.5
```

- **Saturation** in dense canopies and **atmospheric** effects distort
  NDVI. **EVI**, the Enhanced Vegetation Index, adds the blue band and
  coefficients to correct both, staying sensitive where NDVI flattens:

```text
EVI = G * (NIR - Red) / (NIR + C1*Red - C2*Blue + Lc)
G = 2.5, C1 = 6, C2 = 7.5, Lc = 1   (MODIS/Landsat coefficients)
```

Choosing between them:

```mermaid
graph TD
    START["Need a vegetation index"] --> Q1{"Sparse canopy with bare soil"}
    Q1 -->|"yes"| SAVI["Use SAVI with L 0.5"]
    Q1 -->|"no"| Q2{"Dense canopy or hazy scene"}
    Q2 -->|"yes"| EVI["Use EVI with blue correction"]
    Q2 -->|"no"| NDVI["NDVI is fine"]
```

Remember: NDVI is the default and the most comparable across studies; use
SAVI when soil dominates and EVI when the canopy is dense or the air is
hazy.
""",
        ),
        quiz_lesson(
            "Quiz: Vegetation indices (NDVI, SAVI, EVI)",
            (
                q(
                    "What is the NDVI formula?",
                    (
                        opt("(Red - NIR) / (Red * NIR)"),
                        opt("(NIR - Red) / (NIR + Red)", correct=True),
                        opt("NIR / Red only"),
                        opt("(Blue - Green) / (Blue + Green)"),
                    ),
                    "NDVI normalizes the NIR-minus-red difference by their sum, giving "
                    "a value in -1 to +1.",
                ),
                q(
                    "What problem does the L term in SAVI address?",
                    (
                        opt("Cloud shadows"),
                        opt(
                            "Soil brightness showing through a sparse canopy",
                            correct=True,
                        ),
                        opt("Sensor read noise"),
                        opt("Map projection distortion"),
                    ),
                    "SAVI adds a soil-adjustment factor (about 0.5) so bare-soil "
                    "reflectance does not inflate the index in thin vegetation.",
                ),
                q(
                    "Why might you choose EVI over NDVI for a dense tropical canopy?",
                    (
                        opt("EVI is faster to compute"),
                        opt(
                            "EVI uses the blue band and coefficients to reduce "
                            "atmospheric and saturation effects where NDVI flattens",
                            correct=True,
                        ),
                        opt("EVI needs only one band"),
                        opt("NDVI cannot be computed over forests"),
                    ),
                    "NDVI saturates in high-biomass canopies; EVI stays sensitive and "
                    "corrects for aerosols with the blue term.",
                ),
            ),
        ),
        # -- 3. Water and burn indices ---------------------------------
        _t(
            "Water and burn indices (NDWI, NBR)",
            "10 min",
            """# Water and burn indices (NDWI, NBR)

The same normalized-difference recipe maps water and fire, just with
different bands chosen for what those surfaces do to light.

**Water** reflects green but strongly absorbs near-infrared and shortwave
infrared. There are two common "NDWI" indices - watch which one you mean:

```text
McFeeters NDWI (open water):   (Green - NIR)  / (Green + NIR)
Gao NDWI / NDMI (leaf moisture): (NIR - SWIR)  / (NIR + SWIR)

Open water: McFeeters NDWI > 0
Sentinel-2: Green = B3, NIR = B8, SWIR = B11
```

McFeeters NDWI is for delineating **open water bodies**; the Gao version
(often called NDMI) tracks **vegetation and soil moisture**. Naming the
one you use avoids a classic mix-up.

**Burn severity** uses the strong contrast between NIR (high in healthy
vegetation) and SWIR (high in charred, dry ground). The **NBR**,
Normalized Burn Ratio:

```text
NBR = (NIR - SWIR) / (NIR + SWIR)
Sentinel-2: NIR = B8, SWIR = B12

Burn severity from before/after a fire:
dNBR = NBR_prefire - NBR_postfire
  dNBR > 0.66   high severity
  0.27 to 0.66  moderate severity
  0.10 to 0.27  low severity
  < 0.10        unburned
```

The key move for fire is **dNBR** - the difference of NBR between a
pre-fire and post-fire image - which is a change-detection index (the
subject of a later lesson) tuned for burns.

```mermaid
graph TD
    IMG["Reflectance bands"] --> WQ{"Mapping water or fire"}
    WQ -->|"water"| NDWI["McFeeters NDWI Green and NIR"]
    WQ -->|"moisture"| NDMI["Gao NDWI NIR and SWIR"]
    WQ -->|"fire"| NBR["NBR NIR and SWIR"]
    NBR --> DNBR["dNBR prefire minus postfire"]
    DNBR --> SEV["Burn severity classes"]
```

Remember: pick the bands for the physics - green vs NIR for open water,
NIR vs SWIR for moisture and burns - and use the before/after difference
(dNBR) to grade fire severity.
""",
        ),
        quiz_lesson(
            "Quiz: Water and burn indices (NDWI, NBR)",
            (
                q(
                    "Which NDWI variant is used to delineate open water bodies?",
                    (
                        opt(
                            "McFeeters NDWI: (Green - NIR) / (Green + NIR)",
                            correct=True,
                        ),
                        opt("Gao NDWI: (NIR - SWIR) / (NIR + SWIR)"),
                        opt("(Red - Blue) / (Red + Blue)"),
                        opt("NDVI"),
                    ),
                    "McFeeters NDWI uses green and NIR to separate open water; the Gao "
                    "version (NDMI) uses NIR and SWIR for moisture.",
                ),
                q(
                    "What bands does the Normalized Burn Ratio (NBR) combine?",
                    (
                        opt("Blue and green"),
                        opt("Red and green"),
                        opt("NIR and SWIR", correct=True),
                        opt("Blue and red"),
                    ),
                    "NBR = (NIR - SWIR) / (NIR + SWIR); healthy vegetation is high NIR, "
                    "charred ground is high SWIR.",
                ),
                q(
                    "How is dNBR computed to assess burn severity?",
                    (
                        opt("NBR of a single post-fire image"),
                        opt(
                            "Pre-fire NBR minus post-fire NBR",
                            correct=True,
                        ),
                        opt("The average NBR over a year"),
                        opt("NBR divided by NDVI"),
                    ),
                    "dNBR is the before/after difference of NBR - a change-detection "
                    "index tuned for fire; higher dNBR means more severe burn.",
                ),
            ),
        ),
        # -- 4. Image enhancement and composites -----------------------
        _t(
            "Image enhancement and band composites",
            "10 min",
            """# Image enhancement and band composites

Indices reduce bands to a number; **composites** put three bands into the
red, green and blue channels of a display so a human can see the scene.
Which bands you assign changes what pops out.

- **True color** - Red, Green, Blue in R,G,B. Looks natural.
  Sentinel-2: B4, B3, B2.
- **False color (NIR)** - NIR, Red, Green in R,G,B. Vegetation glows
  bright red because it reflects so much NIR. Sentinel-2: B8, B4, B3.
- **SWIR composite** - SWIR, NIR, Red. Good for burn scars, geology and
  moisture. Sentinel-2: B12, B8, B4.

Raw reflectance usually looks dark and flat because real values crowd
into a narrow range. **Contrast enhancement** stretches that range to fill
the display. A simple **percentile (min-max) stretch** maps the 2nd and
98th percentiles to 0 and 255, clipping outliers:

```python
import numpy as np
def stretch(band, low=2, high=98):
    lo, hi = np.percentile(band, (low, high))
    out = (band - lo) / (hi - lo)          # scale the middle 96 percent
    return np.clip(out, 0, 1)              # clip the tails

rgb = np.dstack([stretch(red), stretch(green), stretch(blue)])
```

Other common enhancements: **histogram equalization** (spreads values so
every brightness level is about equally common) and **pan-sharpening**
(fuses a high-resolution panchromatic band with lower-resolution color
bands to sharpen the picture - Landsat B8 is 15 m, its color bands 30 m).

```mermaid
graph LR
    BANDS["Reflectance bands"] --> PICK["Assign three bands to R G B"]
    PICK --> TC["True color B4 B3 B2"]
    PICK --> FC["False color B8 B4 B3"]
    PICK --> SW["SWIR B12 B8 B4"]
    TC --> STR["Contrast stretch"]
    FC --> STR
    SW --> STR
    STR --> DISP["Readable display image"]
```

Remember: a composite is a choice of which physics to show in which color;
enhancement (stretching, equalization, pan-sharpening) then makes that
choice visible.
""",
        ),
        quiz_lesson(
            "Quiz: Image enhancement and band composites",
            (
                q(
                    "In a standard NIR false-color composite, why does vegetation "
                    "appear bright red?",
                    (
                        opt("Because leaves are physically red"),
                        opt(
                            "NIR is mapped to the red channel and vegetation reflects NIR strongly",
                            correct=True,
                        ),
                        opt("Because of a rendering bug"),
                        opt("Because red light is absorbed by the sensor"),
                    ),
                    "False color puts NIR in the red channel; high NIR reflectance from "
                    "vegetation therefore glows red.",
                ),
                q(
                    "What does a 2-98 percentile contrast stretch do?",
                    (
                        opt("Deletes the darkest and brightest pixels"),
                        opt(
                            "Maps the 2nd and 98th percentile values to the display "
                            "range and clips the outlier tails",
                            correct=True,
                        ),
                        opt("Changes the map projection"),
                        opt("Converts the image to a single band"),
                    ),
                    "It spreads the central 96 percent of values across the display, "
                    "clipping extremes so the scene is not washed out by outliers.",
                ),
                q(
                    "What is pan-sharpening?",
                    (
                        opt("Deleting the panchromatic band"),
                        opt(
                            "Fusing a high-resolution panchromatic band with "
                            "lower-resolution color bands to sharpen the image",
                            correct=True,
                        ),
                        opt("Averaging every band into one"),
                        opt("A type of vegetation index"),
                    ),
                    "The sharp panchromatic detail (e.g. Landsat 15 m B8) is combined "
                    "with the 30 m color bands to raise apparent resolution.",
                ),
            ),
        ),
        # -- 5. Unsupervised classification ----------------------------
        _t(
            "Unsupervised classification (k-means, ISODATA)",
            "11 min",
            """# Unsupervised classification (k-means, ISODATA)

**Classification** assigns every pixel to a class (water, forest, urban,
bare soil...). In **unsupervised** classification you provide **no labeled
examples**; the algorithm groups pixels by how similar their spectral
values are (clustering), and you assign meaning to the clusters
afterwards. It answers "what natural groupings exist in this scene?"

Each pixel is a **feature vector** of its band values - a point in an
N-dimensional spectral space (N = number of bands). Clustering finds tight
groups of those points.

**k-means** is the workhorse:

```text
1. Choose k (number of clusters). Place k cluster centers.
2. Assign each pixel to the nearest center (Euclidean distance in
   band space).
3. Move each center to the mean of its assigned pixels.
4. Repeat 2 and 3 until the centers stop moving.

Distance between pixel p and center c across bands b:
d = sqrt( sum_b (p_b - c_b)^2 )
```

**ISODATA** (Iterative Self-Organizing Data Analysis) is k-means with
extra rules: it **splits** clusters that are too spread out and **merges**
clusters that are too close, so the number of classes adapts within a
range instead of being fixed. That makes it more forgiving when you do not
know k in advance.

```python
from sklearn.cluster import KMeans
import numpy as np
# stack: rows x cols x bands -> (pixels, bands)
h, w, b = stack.shape
X = stack.reshape(-1, b)
labels = KMeans(n_clusters=6, n_init=10).fit_predict(X)
classes = labels.reshape(h, w)   # cluster id per pixel
```

The result is a map of **cluster IDs** with no names yet. The analyst then
**labels** each cluster by inspecting it (cluster 3 sits on the rivers ->
water). This human labeling step is what turns clusters into land cover.

```mermaid
graph TD
    PIX["Pixels as band vectors"] --> INIT["Place k cluster centers"]
    INIT --> ASSIGN["Assign each pixel to nearest center"]
    ASSIGN --> UPDATE["Move centers to cluster means"]
    UPDATE --> CONV{"Centers stopped moving"}
    CONV -->|"no"| ASSIGN
    CONV -->|"yes"| MAP["Cluster ID map"]
    MAP --> LABEL["Analyst labels clusters"]
```

Remember: unsupervised methods find spectral groupings without training
data - fast and objective, but you still assign the class names yourself.
""",
        ),
        quiz_lesson(
            "Quiz: Unsupervised classification (k-means, ISODATA)",
            (
                q(
                    "What defines an unsupervised classification?",
                    (
                        opt("It uses many labeled training pixels"),
                        opt(
                            "It groups pixels by spectral similarity with no labeled "
                            "examples; the analyst names the clusters afterward",
                            correct=True,
                        ),
                        opt("It requires a neural network"),
                        opt("It only works on a single band"),
                    ),
                    "No training labels go in; clustering finds natural groups and the "
                    "analyst assigns meaning to them.",
                ),
                q(
                    "In k-means, how is a pixel assigned to a cluster each iteration?",
                    (
                        opt("Randomly"),
                        opt("By its row and column position"),
                        opt(
                            "To the nearest cluster center by distance in band space",
                            correct=True,
                        ),
                        opt("By file order"),
                    ),
                    "Each pixel joins the closest center (Euclidean distance across "
                    "bands); centers then move to the mean of their pixels.",
                ),
                q(
                    "How does ISODATA differ from plain k-means?",
                    (
                        opt("It needs labeled training data"),
                        opt(
                            "It can split over-dispersed clusters and merge close ones, "
                            "so the class count adapts within a range",
                            correct=True,
                        ),
                        opt("It ignores the spectral bands"),
                        opt("It always produces exactly two classes"),
                    ),
                    "ISODATA adds split/merge rules on top of k-means so k is not fixed up front.",
                ),
            ),
        ),
        # -- 6. Supervised classification ------------------------------
        _t(
            "Supervised classification (maximum likelihood, random forest)",
            "11 min",
            """# Supervised classification (maximum likelihood, random forest)

In **supervised** classification you first draw **training samples** -
pixels you know the class of (this polygon is water, that one is forest).
The algorithm learns each class's spectral pattern from those samples,
then labels every pixel in the scene. It answers "map these specific
classes I care about."

Two widely used classifiers:

**Maximum Likelihood (MLC)** is the classic statistical method. It models
each class as a multivariate normal distribution in band space (a mean
vector and covariance from the training pixels) and assigns each pixel to
the class under which it is **most probable**:

```text
For pixel x, pick the class k that maximizes the probability
density p(x | class_k), estimated from each class's training
mean and covariance. Assign x to argmax_k p(x | class_k).
```

**Random Forest (RF)** is the modern default: an **ensemble** of many
decision trees, each trained on a random subset of the pixels and bands;
the class is the **majority vote** of the trees. It handles nonlinear
boundaries, mixes band and index inputs freely, and rarely overfits:

```python
from sklearn.ensemble import RandomForestClassifier
# X_train: (n_samples, n_features) band + index values
# y_train: known class label per sample
rf = RandomForestClassifier(n_estimators=300, random_state=42)
rf.fit(X_train, y_train)
class_map = rf.predict(X_all).reshape(h, w)
```

You must judge how good the map is. Hold back some labeled pixels as a
**test set** and build a **confusion matrix** comparing predicted vs true
classes; the headline number is **overall accuracy**, and per-class you
report producer's and user's accuracy (or the **kappa** coefficient):

```text
overall accuracy = correctly classified test pixels / total test pixels
```

```mermaid
graph TD
    TRAIN["Labeled training samples"] --> FIT["Fit classifier MLC or RF"]
    FIT --> PREDICT["Predict class for every pixel"]
    PREDICT --> MAP["Land cover map"]
    TEST["Held out test pixels"] --> CM["Confusion matrix"]
    MAP --> CM
    CM --> ACC["Overall accuracy and kappa"]
```

Remember: supervised means you supply the classes as training data;
random forest is the robust default, and you always validate on held-out
pixels with a confusion matrix.
""",
        ),
        quiz_lesson(
            "Quiz: Supervised classification (maximum likelihood, random forest)",
            (
                q(
                    "What distinguishes supervised from unsupervised classification?",
                    (
                        opt("Supervised uses no bands"),
                        opt(
                            "Supervised learns from labeled training samples of known "
                            "classes, then labels the whole scene",
                            correct=True,
                        ),
                        opt("Supervised runs only on radar"),
                        opt("Supervised cannot be validated"),
                    ),
                    "You provide training pixels of known classes; the model learns "
                    "their patterns and predicts the rest.",
                ),
                q(
                    "How does a random forest assign a pixel's class?",
                    (
                        opt("By the single deepest decision tree"),
                        opt(
                            "By majority vote across many decision trees trained on "
                            "random subsets of data and features",
                            correct=True,
                        ),
                        opt("By the pixel's row number"),
                        opt("By nearest cluster center"),
                    ),
                    "RF is an ensemble; each tree votes and the majority wins, which "
                    "handles nonlinear class boundaries and resists overfitting.",
                ),
                q(
                    "What is a confusion matrix used for?",
                    (
                        opt("Stretching the image contrast"),
                        opt("Choosing the map projection"),
                        opt(
                            "Comparing predicted vs true classes on held-out pixels to "
                            "compute accuracy",
                            correct=True,
                        ),
                        opt("Compressing the GeoTIFF"),
                    ),
                    "It cross-tabulates predicted against reference labels; overall "
                    "accuracy and kappa summarize how good the map is.",
                ),
            ),
        ),
        # -- 7. Change detection ---------------------------------------
        _t(
            "Change detection",
            "10 min",
            """# Change detection

**Change detection** compares imagery of the same place at two (or more)
dates to find what changed - deforestation, new construction, flooding,
burn scars, crop rotation. The output is either a change/no-change mask or
a map of change types.

The non-negotiable prerequisite is **alignment**. Both dates must share
the same **CRS**, grid and pixel positions (**co-registration**), and
ideally be **radiometrically comparable** (surface reflectance,
cloud-masked, similar sun angle) so that real surface change is not
drowned out by geometry or atmosphere.

Common techniques, from simple to structured:

- **Image differencing** - subtract one date's band or index from the
  other; large magnitude means change. On NDVI this flags vegetation loss
  or gain directly:

```python
import numpy as np
d_ndvi = ndvi_after - ndvi_before        # per-pixel change
# threshold at a couple of standard deviations to make a change mask
thr = 2 * np.nanstd(d_ndvi)
change = np.abs(d_ndvi) > thr
```

- **Index differencing for a purpose** - dNBR (burns), dNDWI (water
  extent), dNDVI (vegetation) target a specific process.
- **Post-classification comparison** - classify each date independently,
  then compare the class maps to get a **from-to** change matrix (forest
  -> bare, water -> vegetation). Interpretable, but errors in either map
  add up.
- **Change Vector Analysis (CVA)** - treat the multiband change as a
  vector per pixel; its **magnitude** says how much changed and its
  **direction** hints at the type of change.

Set the change **threshold** deliberately - too low flags noise, too high
misses real change; a few standard deviations of the difference is a
common starting point.

```mermaid
graph TD
    T1["Image date 1"] --> COREG["Co-register and mask clouds"]
    T2["Image date 2"] --> COREG
    COREG --> METHOD{"Change method"}
    METHOD -->|"magnitude"| DIFF["Index differencing dNDVI dNBR"]
    METHOD -->|"from to"| PCC["Post classification comparison"]
    METHOD -->|"multiband"| CVA["Change vector analysis"]
    DIFF --> THR["Threshold to change mask"]
    PCC --> MAT["From to change matrix"]
    CVA --> THR
```

Remember: co-register and radiometrically match first, then difference or
compare classifications; the threshold decides signal from noise.
""",
        ),
        quiz_lesson(
            "Quiz: Change detection",
            (
                q(
                    "What must be true of the two images before change detection?",
                    (
                        opt("They must be from different satellites"),
                        opt(
                            "They must be co-registered to the same grid and CRS and be "
                            "radiometrically comparable",
                            correct=True,
                        ),
                        opt("They must be in true color only"),
                        opt("They must be exactly one year apart"),
                    ),
                    "Misalignment or differing radiometry creates false change; "
                    "co-registration and reflectance matching come first.",
                ),
                q(
                    "What does post-classification comparison produce?",
                    (
                        opt("A single stretched RGB image"),
                        opt(
                            "A from-to change matrix by comparing independently "
                            "classified maps of each date",
                            correct=True,
                        ),
                        opt("A pan-sharpened composite"),
                        opt("A cluster ID map with no dates"),
                    ),
                    "Each date is classified, then the class maps are compared to get "
                    "class transitions - interpretable but sensitive to map errors.",
                ),
                q(
                    "Why does the change threshold on an image difference matter?",
                    (
                        opt("It sets the map projection"),
                        opt(
                            "Too low flags noise as change, too high misses real change",
                            correct=True,
                        ),
                        opt("It controls the file compression"),
                        opt("It has no effect on the result"),
                    ),
                    "The threshold separates real change from noise; a few standard "
                    "deviations of the difference is a common starting point.",
                ),
            ),
        ),
        # -- 8. Processing rasters with GDAL and rasterio --------------
        _t(
            "Processing rasters with GDAL and rasterio",
            "11 min",
            """# Processing rasters with GDAL and rasterio

All the analysis above runs on **raster files** - and **GDAL** (Geospatial
Data Abstraction Library) is the engine underneath almost every tool that
reads them (QGIS, rasterio, Google Earth Engine exports). It handles
GeoTIFF and hundreds of formats, plus reprojection and mosaicking.

Every raster carries **georeferencing**: a **CRS** (e.g. EPSG:4326 lon/lat
or a projected UTM zone) and a **geotransform** mapping pixel row/col to
map coordinates. Inspect it with the GDAL command line:

```text
gdalinfo scene.tif        # CRS, size, bands, geotransform, stats
gdal_translate -of COG in.tif out.tif   # write a Cloud Optimized GeoTIFF
gdalwarp -t_srs EPSG:32633 in.tif utm.tif   # reproject to UTM 33N
```

For analysis in Python, **rasterio** wraps GDAL with a NumPy-friendly API.
Read bands into arrays, compute an index, and write a new georeferenced
GeoTIFF that keeps the CRS and transform:

```python
import rasterio
import numpy as np

with rasterio.open("sentinel2.tif") as src:
    red = src.read(4).astype("float32")   # band index is 1-based
    nir = src.read(8).astype("float32")
    profile = src.profile                 # CRS, transform, size, dtype

ndvi = (nir - red) / (nir + red)
profile.update(count=1, dtype="float32")

with rasterio.open("ndvi.tif", "w", **profile) as dst:
    dst.write(ndvi, 1)                     # georeferencing preserved
```

Two practical habits: use a **windowed / block read** to process huge
rasters in tiles instead of loading everything into memory, and write
**Cloud Optimized GeoTIFFs (COG)** so files can be read partially over the
network. GDAL and rasterio also handle **nodata** masks, reprojection
(`rasterio.warp`) and reading remote data directly (`/vsicurl/`).

```mermaid
graph LR
    FILE["GeoTIFF on disk"] --> OPEN["rasterio open reads GDAL"]
    OPEN --> META["CRS and transform in profile"]
    OPEN --> ARR["Bands as NumPy arrays"]
    ARR --> CALC["Compute index or classify"]
    META --> WRITE["Write new GeoTIFF"]
    CALC --> WRITE
    WRITE --> COG["Cloud Optimized GeoTIFF"]
```

Remember: GDAL is the georaster engine; rasterio gives you NumPy arrays
plus the CRS and transform, so always carry the georeferencing through to
your output.
""",
        ),
        quiz_lesson(
            "Quiz: Processing rasters with GDAL and rasterio",
            (
                q(
                    "What role does GDAL play in the raster ecosystem?",
                    (
                        opt("It is a web mapping front end"),
                        opt(
                            "It is the underlying library that reads, writes and "
                            "reprojects geospatial raster formats for most tools",
                            correct=True,
                        ),
                        opt("It is a vegetation index"),
                        opt("It is a satellite constellation"),
                    ),
                    "GDAL is the engine beneath rasterio, QGIS and many pipelines - "
                    "GeoTIFF and hundreds of formats plus warp and mosaic.",
                ),
                q(
                    "When you write an index result with rasterio, why reuse the source profile?",
                    (
                        opt("To make the file larger"),
                        opt(
                            "To carry the CRS and geotransform through so the output "
                            "stays correctly georeferenced",
                            correct=True,
                        ),
                        opt("It is required to open the file"),
                        opt("To change the pixel values"),
                    ),
                    "The profile holds CRS, transform and dtype; updating and reusing "
                    "it keeps the new GeoTIFF aligned to the ground.",
                ),
                q(
                    "Why process a very large raster with windowed (block) reads?",
                    (
                        opt("To change its projection automatically"),
                        opt(
                            "To handle it in tiles instead of loading the whole scene "
                            "into memory at once",
                            correct=True,
                        ),
                        opt("Because rasterio cannot read whole bands"),
                        opt("To convert it to a vector"),
                    ),
                    "Windowed reads stream the raster in blocks so memory stays bounded "
                    "on scenes too big to fit in RAM.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does converting Digital Numbers to surface reflectance give you?",
                    (
                        opt("A smaller file"),
                        opt(
                            "A physical 0 to 1 quantity that is comparable across images "
                            "and valid for index formulas",
                            correct=True,
                        ),
                        opt("A vector layer"),
                        opt("A change mask"),
                    ),
                    "reflectance = DN * scale + offset; raw DN is not directly "
                    "comparable between scenes.",
                ),
                q(
                    "Which formula is NDVI?",
                    (
                        opt("(NIR - Red) / (NIR + Red)", correct=True),
                        opt("(Green - NIR) / (Green + NIR)"),
                        opt("(NIR - SWIR) / (NIR + SWIR)"),
                        opt("(Red - Blue) / (Red + Blue)"),
                    ),
                    "NDVI normalizes NIR minus red; the green/NIR form is NDWI and the "
                    "NIR/SWIR form is NBR or NDMI.",
                ),
                q(
                    "When is SAVI preferred over NDVI?",
                    (
                        opt("Over deep open water"),
                        opt(
                            "Where sparse vegetation lets soil brightness affect the index",
                            correct=True,
                        ),
                        opt("Only for nighttime imagery"),
                        opt("When there are no NIR bands"),
                    ),
                    "SAVI adds a soil factor L to suppress background soil in thin canopies.",
                ),
                q(
                    "The McFeeters NDWI is designed to map what?",
                    (
                        opt("Burn severity"),
                        opt("Open water bodies", correct=True),
                        opt("Urban rooftops"),
                        opt("Cloud height"),
                    ),
                    "McFeeters NDWI = (Green - NIR) / (Green + NIR) delineates open "
                    "water; the Gao NDWI/NDMI tracks moisture.",
                ),
                q(
                    "How is burn severity graded with NBR?",
                    (
                        opt("A single post-fire NDVI"),
                        opt(
                            "dNBR, the pre-fire NBR minus the post-fire NBR",
                            correct=True,
                        ),
                        opt("The average blue reflectance"),
                        opt("The image histogram"),
                    ),
                    "dNBR is the before/after difference of NBR; larger values mean "
                    "more severe burns.",
                ),
                q(
                    "What is the key difference between unsupervised and supervised "
                    "classification?",
                    (
                        opt("Unsupervised needs more bands"),
                        opt(
                            "Unsupervised clusters with no labels and the analyst names "
                            "the groups; supervised learns from labeled training samples",
                            correct=True,
                        ),
                        opt("Supervised cannot be validated"),
                        opt("They produce identical maps"),
                    ),
                    "No training data goes into clustering; supervised methods learn "
                    "the classes you provide as training pixels.",
                ),
                q(
                    "How does a random forest classify a pixel?",
                    (
                        opt("By nearest cluster center"),
                        opt(
                            "By majority vote of many decision trees trained on random "
                            "subsets of the data and features",
                            correct=True,
                        ),
                        opt("By the pixel row index"),
                        opt("By the largest single band value"),
                    ),
                    "RF is an ensemble of trees that vote; it handles nonlinear "
                    "boundaries and resists overfitting.",
                ),
                q(
                    "What does a confusion matrix measure?",
                    (
                        opt("Image contrast"),
                        opt("File size"),
                        opt(
                            "Classification accuracy by comparing predicted vs true "
                            "classes on held-out pixels",
                            correct=True,
                        ),
                        opt("Pixel resolution"),
                    ),
                    "It cross-tabulates predictions against reference labels; overall "
                    "accuracy and kappa summarize map quality.",
                ),
                q(
                    "What is the essential prerequisite for change detection between two dates?",
                    (
                        opt("The images must be from different sensors"),
                        opt(
                            "They must be co-registered to the same grid and CRS and be "
                            "radiometrically comparable",
                            correct=True,
                        ),
                        opt("They must be pan-sharpened"),
                        opt("They must be in false color"),
                    ),
                    "Alignment and comparable radiometry ensure the difference reflects "
                    "real surface change, not geometry or atmosphere.",
                ),
                q(
                    "In rasterio, why update and reuse the source profile when writing "
                    "an output raster?",
                    (
                        opt("To compress the file"),
                        opt(
                            "To carry the CRS and geotransform through so the output "
                            "stays correctly georeferenced",
                            correct=True,
                        ),
                        opt("To convert it to vectors"),
                        opt("To change the band math"),
                    ),
                    "The profile holds CRS, transform and dtype; reusing it keeps the "
                    "new GeoTIFF aligned to the ground.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

REMOTE_SENSING_ANALYSIS_COURSES: tuple[SeedCourse, ...] = (_REMOTE_SENSING_ANALYSIS,)
