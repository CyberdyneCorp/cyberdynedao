"""Academy seed content - LiDAR and Point Clouds.

An advanced tour of laser scanning: how LiDAR measures range with light,
the airborne, terrestrial and mobile platforms that collect it, the
LAS/LAZ point cloud formats, and the processing pipeline that turns
billions of raw returns into clean, classified points, terrain models and
extracted features. Every lesson is a direct explanation with a concrete
formula or code example and a mermaid diagram, followed by a checkpoint
quiz; the course closes with a comprehensive final quiz.
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


_LIDAR_POINT_CLOUDS = SeedCourse(
    slug="lidar-point-clouds",
    title="LiDAR & Point Clouds",
    description=(
        "Laser scanning the world - how LiDAR works, the LAS/LAZ formats, "
        "point cloud processing and classification, and deriving terrain "
        "models and features from billions of points. Every lesson pairs a "
        "direct explanation with a real formula or PDAL/Open3D snippet and a "
        "diagram."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# LiDAR and Point Clouds

**LiDAR** (Light Detection and Ranging) measures distance by timing pulses
of laser light. Sweep that beam across a landscape from a plane, a tripod
or a moving vehicle and you capture the shape of the world as a **point
cloud** - millions to billions of 3D points, each with a position and
extra attributes. This course takes you from the physics of a single
range measurement to classifying whole clouds and deriving terrain models
and features from them.

The approach is **advanced but concrete**: every lesson explains one idea
directly, shows it with a real formula or a short PDAL/LAStools/Open3D
snippet, and draws the idea as a diagram. After each lesson there is a
short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **LiDAR principles and ranging** - how a time-of-flight measurement works
2. **Airborne, terrestrial and mobile LiDAR** - the platforms and their geometry
3. **The LAS and LAZ formats** - how point clouds are stored and compressed
4. **Filtering and noise removal** - cleaning the raw cloud
5. **Ground classification and DTM extraction** - separating bare earth
6. **Feature extraction** - buildings, vegetation and powerlines
7. **Point cloud tools** - PDAL, LAStools and Open3D
8. **Fusion with imagery and applications** - colorized clouds and use cases

This is the map. Each stage builds on the last: you cannot classify a
cloud you have not cleaned, or extract terrain from points you cannot
read. Ground everything in real practice - WGS84 and UTM coordinates,
EPSG codes, the ASPRS LAS standard - and the pipeline becomes routine.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What does LiDAR fundamentally measure?",
                    (
                        opt("The color of a surface"),
                        opt(
                            "Distance to a surface, by timing pulses of laser light "
                            "(range), which becomes 3D points",
                            correct=True,
                        ),
                        opt("The temperature of the ground"),
                        opt("Radio signal strength"),
                    ),
                    "LiDAR = Light Detection and Ranging; it ranges with light and "
                    "builds a 3D point cloud.",
                ),
                q(
                    "What is a 'point cloud'?",
                    (
                        opt("A weather formation over a survey area"),
                        opt("A single averaged elevation value for a region"),
                        opt(
                            "A large collection of 3D points, each with a position and "
                            "attributes, describing the shape of scanned surfaces",
                            correct=True,
                        ),
                        opt("A raster image of the ground"),
                    ),
                    "A point cloud is millions to billions of measured 3D points - the "
                    "raw product of laser scanning.",
                ),
            ),
        ),
        # -- 1. LiDAR principles and ranging ---------------------------
        _t(
            "LiDAR principles and ranging",
            "10 min",
            """# LiDAR principles and ranging

A LiDAR sensor fires a short pulse of laser light, then measures how long
the reflection takes to return. Because light travels at a known speed,
that round-trip time gives the **range** to whatever the pulse hit. This
is **time-of-flight (ToF)** ranging.

The core equation - light goes out and comes back, so divide by two:

```text
R = (c * t) / 2

R = range to the target (metres)
c = speed of light ~= 299,792,458 m/s
t = round-trip time of the pulse (seconds)

Example: a return arrives 1.0 microsecond after the pulse leaves.
R = (299,792,458 * 1.0e-6) / 2 = 149.9 m
```

Two ranging methods exist:

- **Pulsed (direct time-of-flight)** - time a discrete pulse. Standard for
  long-range airborne and terrestrial mapping.
- **Phase-based (or AMCW)** - modulate a continuous beam and measure the
  phase shift of the return. Very precise at short range, used in many
  terrestrial scanners.

A single outgoing pulse can produce **multiple returns**. Part of the beam
reflects off a treetop (**first return**), part off a branch, and part
reaches the ground (**last return**). Recording each return - or the full
**waveform** - is what lets LiDAR see *through* vegetation to the surface
below. Each return also carries an **intensity** value: how strong the
reflection was, a rough proxy for surface reflectivity.

```mermaid
graph LR
    LASER["Laser fires pulse"] --> OUT["Pulse travels out"]
    OUT --> HIT["Hits surfaces"]
    HIT --> R1["First return canopy"]
    HIT --> R2["Intermediate return branch"]
    HIT --> R3["Last return ground"]
    R1 --> TIME["Detector times each return"]
    R2 --> TIME
    R3 --> TIME
    TIME --> RANGE["Range from time of flight"]
```

Remember: LiDAR turns *time* into *distance*. Multiple returns per pulse
and per-return intensity are what make it far richer than a single
distance reading.
""",
        ),
        quiz_lesson(
            "Quiz: LiDAR principles and ranging",
            (
                q(
                    "Why is the round-trip time divided by two in the range equation R = (c * t) / 2?",
                    (
                        opt("To convert seconds to microseconds"),
                        opt(
                            "The light travels to the target and back, so the measured "
                            "time covers twice the distance",
                            correct=True,
                        ),
                        opt("To account for two lasers firing"),
                        opt("Because light travels at half its speed in air"),
                    ),
                    "Time-of-flight measures the round trip; the one-way range is half of it.",
                ),
                q(
                    "What allows LiDAR to map the ground beneath a forest canopy?",
                    (
                        opt("It uses radar instead of light"),
                        opt(
                            "A single pulse can produce multiple returns - first off the "
                            "canopy, last off the ground - recorded separately",
                            correct=True,
                        ),
                        opt("The laser melts through the leaves"),
                        opt("It only works over bare ground"),
                    ),
                    "Multiple returns per pulse capture canopy and the surface below in one shot.",
                ),
                q(
                    "What does a return's intensity value indicate?",
                    (
                        opt("The exact material name of the surface"),
                        opt("The GPS time of the pulse"),
                        opt(
                            "The strength of the reflected pulse - a rough proxy for "
                            "surface reflectivity",
                            correct=True,
                        ),
                        opt("The number of returns from that pulse"),
                    ),
                    "Intensity is how much light came back; it hints at reflectivity but "
                    "is not a calibrated material ID.",
                ),
            ),
        ),
        # -- 2. Platforms ----------------------------------------------
        _t(
            "Airborne, terrestrial and mobile LiDAR",
            "10 min",
            """# Airborne, terrestrial and mobile LiDAR

The same ranging physics is deployed from very different platforms, and
the platform decides coverage, density and accuracy.

- **Airborne LiDAR (ALS)** - a scanner in a plane or drone sweeps the beam
  side to side while flying forward, mapping wide areas from above. It is
  the standard for terrain, forestry and flood mapping. Point density is
  modest (often 1-30 points per square metre); it sees roofs and canopy
  tops well.
- **Terrestrial LiDAR (TLS)** - a tripod-mounted scanner spins to capture
  an extremely dense, precise scan from a fixed station. Used for
  buildings, heritage and detailed surveys. Multiple scans from different
  stations are **registered** together into one cloud.
- **Mobile LiDAR (MLS)** - a scanner on a car, train or boat maps
  corridors (roads, rail, coastline) at driving speed, dense along the
  route.

Turning raw ranges into geographic points needs **georeferencing**. The
scanner only knows range and beam angle; to place a point on the Earth it
combines that with the sensor's position and orientation, measured by
**GNSS** (a GPS receiver, often RTK/PPK corrected) and an **IMU** (inertial
measurement unit) tracking roll, pitch and yaw. This fusion is
**direct georeferencing**.

```text
Point position = Sensor position (GNSS)
               + Rotation (IMU roll, pitch, yaw)
               applied to the beam vector (range R, scan angle theta)

Any error in aircraft attitude is amplified by the range:
horizontal error ~= R * sin(attitude error in radians)
e.g. R = 1000 m, attitude error 0.01 deg -> ~0.17 m on the ground
```

```mermaid
graph TD
    ALS["Airborne scanner"] --> GEO["Direct georeferencing"]
    TLS["Terrestrial scanner"] --> REG["Register scan stations"]
    MLS["Mobile scanner"] --> GEO
    GNSS["GNSS position"] --> GEO
    IMU["IMU orientation"] --> GEO
    GEO --> PTS["Georeferenced points WGS84 or UTM"]
    REG --> PTS
```

Remember: the platform sets the trade between area and density, and every
airborne or mobile point is only as accurate as the GNSS and IMU that
place it - attitude errors grow with range.
""",
        ),
        quiz_lesson(
            "Quiz: Airborne, terrestrial and mobile LiDAR",
            (
                q(
                    "Which platform is standard for mapping wide-area terrain and forestry?",
                    (
                        opt("Terrestrial (tripod) LiDAR"),
                        opt(
                            "Airborne LiDAR (ALS) - a scanner in a plane or drone sweeping "
                            "the beam while flying",
                            correct=True,
                        ),
                        opt("Handheld phase-based scanners only"),
                        opt("A fixed weather station"),
                    ),
                    "ALS covers large areas from above; TLS is dense but station-bound, "
                    "MLS follows corridors.",
                ),
                q(
                    "What two sensors provide the position and orientation needed to "
                    "georeference airborne LiDAR points?",
                    (
                        opt("A barometer and a thermometer"),
                        opt("Two laser scanners"),
                        opt(
                            "GNSS (position) and an IMU (roll, pitch, yaw orientation), "
                            "fused with the beam range and angle",
                            correct=True,
                        ),
                        opt("A camera and a compass only"),
                    ),
                    "Direct georeferencing combines GNSS position and IMU attitude with "
                    "the scanner's range and scan angle.",
                ),
                q(
                    "Why do attitude (orientation) errors matter more at long range?",
                    (
                        opt("They do not - range has no effect"),
                        opt(
                            "The angular error is multiplied by the range, so the same "
                            "small attitude error produces a larger ground error far away",
                            correct=True,
                        ),
                        opt("Long range disables the IMU"),
                        opt("Only intensity is affected by range"),
                    ),
                    "Horizontal error scales roughly as range times the attitude error - "
                    "small angles become large distances at 1000 m.",
                ),
            ),
        ),
        # -- 3. LAS / LAZ formats --------------------------------------
        _t(
            "The LAS and LAZ point cloud formats",
            "10 min",
            """# The LAS and LAZ point cloud formats

LiDAR is stored and exchanged mostly in **LAS**, an open binary format
standardized by **ASPRS** (the American Society for Photogrammetry and
Remote Sensing). **LAZ** is its losslessly compressed twin (LASzip),
typically 5-10x smaller with identical points on decompression.

A LAS file has three parts: a **public header block** (bounding box, point
count, scale and offset, CRS info), optional **variable length records
(VLRs)** that carry things like the coordinate reference system, and the
**point records** themselves.

Coordinates are stored as **integers** and reconstructed with a scale and
offset - this keeps files compact and precise:

```text
X_real = X_int * x_scale + x_offset      (same for Y and Z)

Header: x_scale = 0.01, x_offset = 500000
Stored X_int = 1234567
X_real = 1234567 * 0.01 + 500000 = 512345.67 m (e.g. UTM easting)
```

Each point record carries standard fields. The **point format** id sets
which fields exist:

```text
Common LAS point fields
-----------------------
X, Y, Z               integer coordinates (scaled as above)
Intensity             return strength
Return Number         which return of the pulse (1 = first)
Number of Returns     total returns for that pulse
Classification        ASPRS class code (see below)
GPS Time              when the pulse was fired
Red, Green, Blue      colour (point formats 2, 3, 5, 7, 8 ...)

ASPRS standard classification codes (excerpt)
0 = Created never classified   2 = Ground        5 = High vegetation
1 = Unclassified               3 = Low veg       6 = Building
9 = Water                      4 = Medium veg     7 = Low point noise
```

Newer **LAS 1.4** adds point formats 6-10 with a 16-bit classification
field (many more classes), up to 15 returns per pulse, and better support
for large files - now the default for national datasets.

```mermaid
graph TD
    LAS["LAS file"] --> HDR["Public header block"]
    LAS --> VLR["Variable length records"]
    LAS --> PTS["Point records"]
    HDR --> BBOX["Bounds scale and offset"]
    VLR --> CRS["Coordinate reference system EPSG"]
    PTS --> FIELDS["X Y Z intensity return class GPS time"]
    LAS --> LAZ["LAZ lossless compression"]
```

Remember: LAS is the ASPRS standard container, LAZ is its lossless
compression, coordinates are integers rebuilt via scale and offset, and
the **classification** field is where semantic meaning lives.
""",
        ),
        quiz_lesson(
            "Quiz: The LAS and LAZ point cloud formats",
            (
                q(
                    "What is the relationship between LAS and LAZ?",
                    (
                        opt("They are unrelated formats from different vendors"),
                        opt(
                            "LAZ is the losslessly compressed form of LAS (LASzip) - "
                            "much smaller, identical points when decompressed",
                            correct=True,
                        ),
                        opt("LAZ is a lossy, lower-quality version of LAS"),
                        opt("LAS stores color, LAZ never can"),
                    ),
                    "LAZ compresses LAS losslessly, commonly 5-10x smaller with no data loss.",
                ),
                q(
                    "Why are LAS coordinates stored as integers with a scale and offset?",
                    (
                        opt("Because computers cannot store decimals"),
                        opt(
                            "To keep files compact and precise - real coordinates are "
                            "rebuilt as X_int * scale + offset",
                            correct=True,
                        ),
                        opt("To hide the true coordinates"),
                        opt("Because LAS cannot store large numbers at all"),
                    ),
                    "Integer storage plus scale/offset gives small files with controlled "
                    "precision (e.g. 0.01 m).",
                ),
                q(
                    "In the ASPRS classification scheme, which code is 'Ground'?",
                    (
                        opt("Class 6"),
                        opt("Class 2", correct=True),
                        opt("Class 9"),
                        opt("Class 1"),
                    ),
                    "ASPRS class 2 = Ground; 6 = Building, 5 = high vegetation, 9 = water.",
                ),
            ),
        ),
        # -- 4. Filtering and noise removal ----------------------------
        _t(
            "Point cloud filtering and noise removal",
            "10 min",
            """# Point cloud filtering and noise removal

Raw clouds contain **outliers** - birds and dust high above the surface,
multipath returns below it, and scattered sensor noise. Before any
classification or modelling you clean the cloud, or every downstream step
inherits the errors.

Two workhorse statistical filters:

- **Statistical Outlier Removal (SOR)** - for each point, look at its *k*
  nearest neighbours and compute the mean distance to them. Points whose
  mean neighbour distance is far above the global average (more than a set
  number of standard deviations) are isolated, so they are dropped.
- **Radius Outlier Removal (ROR)** - drop any point that has fewer than a
  minimum number of neighbours within a fixed radius. Sparse, lonely
  points are noise.

The SOR test in one line:

```text
Keep a point if:  mean_dist(point) <= global_mean + (m * global_std)

k                = neighbours per point (e.g. 8)
m                = std-dev multiplier / threshold (e.g. 1.0)
global_mean/std  = statistics of all points' mean neighbour distances
Higher m keeps more points; lower m is more aggressive.
```

A PDAL pipeline that applies SOR and writes a cleaned LAZ:

```json
{
  "pipeline": [
    "dirty.laz",
    {
      "type": "filters.outlier",
      "method": "statistical",
      "mean_k": 8,
      "multiplier": 1.0
    },
    {
      "type": "filters.range",
      "limits": "Classification![7:7]"
    },
    "clean.laz"
  ]
}
```

PDAL's `filters.outlier` marks outliers as classification **7 (low point
noise)**; the `filters.range` step then keeps everything that is *not*
class 7. Other cleanups include **deduplication** (removing exact
duplicate points) and **voxel-grid downsampling** (one representative
point per small 3D cell) to thin dense data uniformly.

```mermaid
graph LR
    RAW["Raw noisy cloud"] --> KNN["Find k nearest neighbours"]
    KNN --> STAT["Mean neighbour distance"]
    STAT --> TEST["Compare to global mean plus m sigma"]
    TEST --> KEEP["Inlier keep"]
    TEST --> DROP["Outlier mark noise"]
    KEEP --> CLEAN["Clean cloud"]
```

Remember: clean first. Statistical and radius filters remove isolated
outliers by neighbourhood density; voxel downsampling thins uniformly
without discarding structure.
""",
        ),
        quiz_lesson(
            "Quiz: Point cloud filtering and noise removal",
            (
                q(
                    "How does Statistical Outlier Removal (SOR) decide a point is noise?",
                    (
                        opt("It removes every point below the mean elevation"),
                        opt(
                            "Its mean distance to k nearest neighbours is more than m "
                            "standard deviations above the global average - it is isolated",
                            correct=True,
                        ),
                        opt("It removes points with the highest intensity"),
                        opt("It deletes points at random until the file is smaller"),
                    ),
                    "SOR flags points whose neighbourhood is unusually sparse compared to "
                    "the whole cloud.",
                ),
                q(
                    "In the PDAL example, what does filters.outlier do to the points it "
                    "flags, and how are they then removed?",
                    (
                        opt("It deletes them immediately with no trace"),
                        opt(
                            "It marks them as classification 7 (noise); a later "
                            "filters.range step keeps only points that are not class 7",
                            correct=True,
                        ),
                        opt("It changes their color to red"),
                        opt("It moves them to the ground class"),
                    ),
                    "Outliers are tagged class 7, then a range filter drops class 7 - "
                    "mark-then-filter.",
                ),
                q(
                    "What does voxel-grid downsampling achieve?",
                    (
                        opt("It removes all ground points"),
                        opt("It doubles the number of points"),
                        opt(
                            "It thins dense data uniformly by keeping one representative "
                            "point per small 3D cell",
                            correct=True,
                        ),
                        opt("It compresses the file like LAZ does"),
                    ),
                    "One point per voxel gives an even density without discarding overall "
                    "structure.",
                ),
            ),
        ),
        # -- 5. Ground classification / DTM ----------------------------
        _t(
            "Ground classification and DTM extraction",
            "11 min",
            """# Ground classification and DTM extraction

The single most valuable product from LiDAR is the **bare-earth terrain**.
That means separating **ground** points from everything above them
(buildings, trees, cars) and interpolating a surface. Get this right and
the derived models follow.

Three surfaces to keep straight:

- **DSM (Digital Surface Model)** - the top of everything: rooftops and
  canopy included. Built from first returns.
- **DTM / DEM (Digital Terrain Model)** - the bare ground with objects
  removed. Built from ground-classified points.
- **nDSM / CHM (normalized surface / canopy height model)** - DSM minus
  DTM, giving the **height above ground** of each object:

```text
nDSM(x, y) = DSM(x, y) - DTM(x, y)

A rooftop return at Z = 42.0 m over ground DTM = 30.0 m
-> object height = 12.0 m
This is how building and tree heights are measured.
```

The classic ground filter is **Cloth Simulation Filter (CSF)**: imagine
turning the terrain upside down and dropping a stiff cloth onto it; the
cloth settles onto the high points (which, inverted, are the ground). CSF
is intuitive and widely used. Other approaches include
**Progressive Morphological Filter (PMF)** and **Progressive TIN
Densification (PTD)**, which grow a triangulated ground surface by adding
points that fit within angle and distance thresholds.

A PDAL ground-then-DTM pipeline using the SMRF filter:

```json
{
  "pipeline": [
    "clean.laz",
    { "type": "filters.smrf" },
    { "type": "filters.range", "limits": "Classification[2:2]" },
    {
      "type": "writers.gdal",
      "resolution": 1.0,
      "output_type": "idw",
      "filename": "dtm.tif"
    }
  ]
}
```

`filters.smrf` classifies ground (class 2), the range filter keeps only
ground, and `writers.gdal` rasterizes those points into a 1 m GeoTIFF DTM
by inverse-distance weighting. From a DTM you derive **slope, aspect,
hillshade and contours** for hydrology, engineering and flood work.

```mermaid
graph TD
    CLEAN["Clean cloud"] --> GF["Ground filter CSF or SMRF"]
    GF --> GND["Ground points class 2"]
    GF --> OBJ["Non ground points"]
    GND --> DTM["Interpolate DTM bare earth"]
    OBJ --> DSM["First returns give DSM"]
    DSM --> NDSM["nDSM equals DSM minus DTM"]
    DTM --> NDSM
    DTM --> DERIV["Slope aspect hillshade contours"]
```

Remember: ground classification is the gateway. DTM is bare earth, DSM is
the top of everything, and their difference (nDSM) is object height - the
basis for measuring buildings and trees.
""",
        ),
        quiz_lesson(
            "Quiz: Ground classification and DTM extraction",
            (
                q(
                    "What is the difference between a DSM and a DTM?",
                    (
                        opt("They are two names for the same surface"),
                        opt(
                            "A DSM is the top of everything (roofs, canopy); a DTM is the "
                            "bare ground with objects removed",
                            correct=True,
                        ),
                        opt("A DSM is bare earth; a DTM includes buildings"),
                        opt("A DTM is a color image, a DSM is elevation"),
                    ),
                    "DSM = surface including objects (first returns); DTM = terrain, ground only.",
                ),
                q(
                    "How is an object's height above ground (nDSM) computed?",
                    (
                        opt("By multiplying the DSM by the DTM"),
                        opt(
                            "By subtracting the DTM from the DSM at each location, giving "
                            "height above ground",
                            correct=True,
                        ),
                        opt("By counting the returns per pulse"),
                        opt("By reading intensity values"),
                    ),
                    "nDSM = DSM - DTM; a 42 m rooftop over 30 m ground is a 12 m object.",
                ),
                q(
                    "What is the idea behind the Cloth Simulation Filter (CSF)?",
                    (
                        opt("It photographs the terrain from above"),
                        opt("It removes every point below sea level"),
                        opt(
                            "It drops a simulated stiff cloth onto the inverted terrain; "
                            "where the cloth settles marks the ground surface",
                            correct=True,
                        ),
                        opt("It averages all Z values into one plane"),
                    ),
                    "CSF inverts the surface and lets a cloth settle onto the high points, "
                    "which are the ground once flipped back.",
                ),
            ),
        ),
        # -- 6. Feature extraction -------------------------------------
        _t(
            "Feature extraction - buildings, vegetation, powerlines",
            "11 min",
            """# Feature extraction - buildings, vegetation, powerlines

With ground separated, the **non-ground** points describe the built and
natural world. Feature extraction assigns them to classes and turns them
into usable objects (building footprints, tree inventories, powerline
catenaries).

Useful per-point and neighbourhood cues:

- **Height above ground** (from the nDSM) - separates low clutter from
  tall objects.
- **Return structure** - vegetation scatters the beam and produces
  **multiple returns**; a solid roof usually gives a **single return**.
- **Local geometry** via the covariance of a point's neighbourhood - its
  eigenvalues describe whether the neighbourhood is planar, linear or
  scattered:

```text
From neighbourhood eigenvalues L1 >= L2 >= L3 >= 0:

Planarity  = (L2 - L3) / L1     high on roofs and walls
Linearity  = (L1 - L2) / L1     high on wires and poles
Sphericity =  L3 / L1           high in scattered foliage

A roof plane -> high planarity; a powerline -> high linearity;
a tree crown -> high sphericity.
```

How the main features fall out:

- **Buildings** - clusters of tall, **planar**, single-return points.
  Region-grow planar patches, then trace and regularize the outline into a
  footprint polygon.
- **Vegetation** - tall points with **multiple returns** and high
  sphericity. Individual trees are found by locating local maxima in the
  CHM and segmenting crowns; height and canopy metrics feed forestry.
- **Powerlines** - thin, **linear**, elevated points forming long
  catenary curves between towers; high linearity plus height isolates them,
  and a catenary is fit for sag and clearance analysis:

```text
Powerline sag follows a catenary:
z(x) = z0 + a * (cosh(x / a) - 1)
where a = H / w (horizontal tension over cable weight per length).
Clearance = catenary height minus DTM below - critical for utilities.
```

```mermaid
graph TD
    NG["Non ground points"] --> FEAT["Compute height returns geometry"]
    FEAT --> PLAN["Planar single return"]
    FEAT --> SCAT["Multi return scattered"]
    FEAT --> LIN["Linear elevated thin"]
    PLAN --> BLD["Buildings footprints"]
    SCAT --> VEG["Vegetation tree crowns"]
    LIN --> PWR["Powerlines catenary sag"]
```

Remember: features emerge from **height plus local geometry plus return
structure**. Planar means building, scattered multi-return means
vegetation, thin and linear and elevated means powerline.
""",
        ),
        quiz_lesson(
            "Quiz: Feature extraction - buildings, vegetation, powerlines",
            (
                q(
                    "Which geometric cue best distinguishes a powerline from a rooftop?",
                    (
                        opt("Powerlines are highly planar; roofs are linear"),
                        opt(
                            "Powerlines have high linearity (thin, elongated neighbourhood); "
                            "roofs have high planarity",
                            correct=True,
                        ),
                        opt("Both have identical geometry - only color differs"),
                        opt("Powerlines are always on the ground"),
                    ),
                    "Neighbourhood eigenvalues: linearity is high on wires, planarity is "
                    "high on roofs and walls.",
                ),
                q(
                    "Why does vegetation typically produce multiple returns per pulse?",
                    (
                        opt("Because leaves are brightly colored"),
                        opt(
                            "The beam partially reflects off leaves and branches at "
                            "several depths, so one pulse yields several returns",
                            correct=True,
                        ),
                        opt("Because trees are warmer than roofs"),
                        opt("Vegetation only ever gives a single return"),
                    ),
                    "Foliage scatters the beam at multiple heights; a solid roof usually "
                    "gives a single return.",
                ),
                q(
                    "How are individual trees commonly located for a forest inventory?",
                    (
                        opt("By reading the LAS header bounding box"),
                        opt("By removing all ground points"),
                        opt(
                            "By finding local maxima in the canopy height model (CHM) and "
                            "segmenting the surrounding crown",
                            correct=True,
                        ),
                        opt("By counting the number of VLRs"),
                    ),
                    "Local maxima in the CHM mark treetops; crown segmentation gives per-"
                    "tree height and canopy metrics.",
                ),
            ),
        ),
        # -- 7. Tools --------------------------------------------------
        _t(
            "Point cloud tools - PDAL, LAStools, Open3D",
            "10 min",
            """# Point cloud tools - PDAL, LAStools, Open3D

You rarely write point cloud algorithms from scratch. Three toolsets cover
most work; knowing which to reach for is half the job.

- **PDAL (Point Data Abstraction Library)** - the "GDAL of point clouds".
  You describe a **pipeline** as JSON: a reader, a chain of filters, and a
  writer. It reads and writes LAS/LAZ and many other formats, reprojects
  between CRSs, classifies ground, and rasterizes to GeoTIFF. Ideal for
  scripted, reproducible batch processing.
- **LAStools** - a fast suite of command-line programs (`lasground`,
  `lasclassify`, `las2dem`, `lasheight`, `lasclip`...). Extremely quick on
  huge airborne datasets; the industry workhorse for production terrain
  pipelines. (Some tools are open, others licensed.)
- **Open3D** - a Python/C++ library for **interactive and algorithmic** 3D
  work: visualization, registration (ICP), voxel downsampling, normal
  estimation, plane and cluster segmentation. Best for research,
  prototyping and TLS registration rather than georeferenced batch mapping.

A PDAL reproject-and-thin pipeline (CRS by EPSG code):

```json
{
  "pipeline": [
    "input.laz",
    { "type": "filters.reprojection", "out_srs": "EPSG:32631" },
    { "type": "filters.voxelcentroidnearestneighbor", "cell": 0.5 },
    "output_utm.laz"
  ]
}
```

The same downsample-and-plane-fit idea in Open3D Python:

```python
import open3d as o3d

pcd = o3d.io.read_point_cloud("scan.ply")
pcd = pcd.voxel_down_sample(voxel_size=0.5)      # thin uniformly

# fit the dominant plane (e.g. a wall or floor) with RANSAC
plane, inliers = pcd.segment_plane(
    distance_threshold=0.05, ransac_n=3, num_iterations=1000
)
a, b, c, d = plane                                # plane ax+by+cz+d=0
ground = pcd.select_by_index(inliers)
```

```mermaid
graph LR
    JOB["Point cloud job"] --> Q1{"Scripted batch mapping"}
    Q1 -->|"yes"| PDAL["PDAL pipelines and LAStools"]
    Q1 -->|"no"| Q2{"Interactive or research 3D"}
    Q2 -->|"yes"| O3D["Open3D"]
    Q2 -->|"no"| GIS["QGIS or ArcGIS viewers"]
```

Remember: PDAL for reproducible pipelines, LAStools for fast production
terrain, Open3D for interactive and algorithmic 3D. They interoperate
through LAS/LAZ.
""",
        ),
        quiz_lesson(
            "Quiz: Point cloud tools - PDAL, LAStools, Open3D",
            (
                q(
                    "How do you specify a processing job in PDAL?",
                    (
                        opt("By drawing it in a GUI only"),
                        opt(
                            "As a JSON pipeline: a reader, a chain of filters, and a "
                            "writer - scripted and reproducible",
                            correct=True,
                        ),
                        opt("By emailing the points to a server"),
                        opt("PDAL cannot read LAS files"),
                    ),
                    "PDAL is the 'GDAL of point clouds' - declarative JSON pipelines of "
                    "reader, filters and writer.",
                ),
                q(
                    "Which toolset is the best fit for interactive 3D work and TLS scan "
                    "registration (ICP)?",
                    (
                        opt("LAStools"),
                        opt(
                            "Open3D - a Python/C++ library for visualization, "
                            "registration, segmentation and prototyping",
                            correct=True,
                        ),
                        opt("A LAS header editor"),
                        opt("A spreadsheet"),
                    ),
                    "Open3D shines at interactive and algorithmic 3D; PDAL/LAStools are "
                    "for georeferenced batch mapping.",
                ),
                q(
                    "In the Open3D snippet, what does segment_plane with RANSAC return?",
                    (
                        opt("A color histogram of the cloud"),
                        opt("The LAS classification codes"),
                        opt(
                            "The coefficients of the dominant plane (a, b, c, d) and the "
                            "indices of the points that fit it (inliers)",
                            correct=True,
                        ),
                        opt("The GPS time of every point"),
                    ),
                    "RANSAC plane segmentation gives the plane equation ax+by+cz+d=0 and "
                    "the inlier indices - handy for walls, floors and ground patches.",
                ),
            ),
        ),
        # -- 8. Fusion and applications --------------------------------
        _t(
            "Fusion with imagery and applications",
            "10 min",
            """# Fusion with imagery and applications

LiDAR gives precise **geometry** but no true color and little semantic
context. **Imagery** (aerial photos, satellite, or cameras on the same
platform) gives rich **spectral** detail but no direct 3D. Fusing them
combines the strengths.

The core operation is **colorization**: project each 3D point into an
image and sample the pixel it lands on. With a calibrated camera you use
the collinearity/projection relationship:

```text
Project a 3D point into an image:
[u, v, 1]^T ~ K * [R | t] * [X, Y, Z, 1]^T

K       = camera intrinsics (focal length, principal point)
[R | t] = camera pose (rotation and translation, from GNSS/IMU)
(u, v)  = pixel the point lands on -> copy its RGB (and NIR) to the point
```

For airborne data a simpler route is **orthophoto draping**: sample an
orthorectified image at each point's (X, Y). Once points carry spectral
bands you can compute indices per point - for example **NDVI** to separate
live vegetation:

```text
NDVI = (NIR - Red) / (NIR + Red)

High NDVI + tall + multi-return  -> confident live vegetation
Low  NDVI + tall + planar        -> confident building
Fusion makes classification far more reliable than geometry alone.
```

Where this all lands - real applications:

- **Topographic mapping and contours** - national DTM/DEM programs.
- **Flood and hydrology modelling** - accurate bare-earth surfaces.
- **Forestry** - canopy height, biomass and tree counts.
- **Cities and BIM** - 3D building models, **3D Tiles/glTF** and CityGML
  for the web; **digital twins** of infrastructure.
- **Autonomous vehicles and robotics** - real-time LiDAR SLAM.
- **Corridor and utility mapping** - roads, rail, powerline clearance.
- **Archaeology** - stripping vegetation to reveal hidden structures.

```mermaid
graph TD
    LID["LiDAR geometry"] --> FUSE["Fuse and colorize"]
    IMG["Imagery spectral bands"] --> FUSE
    FUSE --> RGBPTS["Colorized classified cloud"]
    RGBPTS --> DTM["Terrain and hydrology"]
    RGBPTS --> CITY["3D city models and digital twins"]
    RGBPTS --> FOR["Forestry and biomass"]
    RGBPTS --> AV["Autonomous vehicles SLAM"]
```

Remember: LiDAR contributes geometry, imagery contributes spectrum; fused,
colorized clouds classify better and drive everything from flood models to
digital twins.
""",
        ),
        quiz_lesson(
            "Quiz: Fusion with imagery and applications",
            (
                q(
                    "What does fusing LiDAR with imagery add to the point cloud?",
                    (
                        opt("Nothing useful - they conflict"),
                        opt(
                            "Spectral information (true color, NIR) that LiDAR lacks, by "
                            "projecting points into images and sampling pixels",
                            correct=True,
                        ),
                        opt("It removes the 3D geometry"),
                        opt("It only makes the file larger with no benefit"),
                    ),
                    "LiDAR is geometry; imagery is spectrum. Colorization copies image "
                    "bands onto each point.",
                ),
                q(
                    "Once points carry a NIR and Red band, how does NDVI help classification?",
                    (
                        opt("It measures the point's elevation"),
                        opt(
                            "NDVI = (NIR - Red)/(NIR + Red) is high for live vegetation, "
                            "so combining it with geometry separates trees from buildings "
                            "more reliably",
                            correct=True,
                        ),
                        opt("It replaces the need for any geometry"),
                        opt("It compresses the point cloud"),
                    ),
                    "High NDVI plus tall multi-return points is confidently vegetation; "
                    "spectral plus geometric cues beat geometry alone.",
                ),
                q(
                    "Which application relies on LiDAR to strip vegetation and reveal "
                    "surfaces hidden beneath it?",
                    (
                        opt("Real-time stock trading"),
                        opt(
                            "Archaeology - bare-earth DTMs expose structures hidden under "
                            "forest canopy",
                            correct=True,
                        ),
                        opt("Audio processing"),
                        opt("Spreadsheet accounting"),
                    ),
                    "Multiple returns reach the ground through canopy; the bare-earth DTM "
                    "reveals features invisible in imagery.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does LiDAR measure, and how does it become 3D points?",
                    (
                        opt("It measures color and stacks photos"),
                        opt(
                            "It measures range by timing laser pulses (time of flight); "
                            "combined with sensor position and orientation, ranges become "
                            "georeferenced 3D points",
                            correct=True,
                        ),
                        opt("It measures temperature over time"),
                        opt("It records radio echoes only"),
                    ),
                    "Time of flight gives range; GNSS and IMU place each point in a CRS.",
                ),
                q(
                    "Why can one LiDAR pulse yield several returns?",
                    (
                        opt("The sensor fires several lasers at once"),
                        opt(
                            "Parts of the beam reflect off surfaces at different depths - "
                            "canopy, branches, ground - each recorded as a return",
                            correct=True,
                        ),
                        opt("Returns are duplicated for backup"),
                        opt("Only one return is ever possible"),
                    ),
                    "Multiple returns per pulse let LiDAR see canopy and the ground "
                    "beneath in a single shot.",
                ),
                q(
                    "What is the difference between LAS and LAZ?",
                    (
                        opt("LAZ is a lossy, degraded version"),
                        opt(
                            "LAS is the ASPRS point format; LAZ is its lossless "
                            "compression (LASzip), much smaller with identical points",
                            correct=True,
                        ),
                        opt("They are for different sensors"),
                        opt("LAS cannot store classification, LAZ can"),
                    ),
                    "LAZ losslessly compresses LAS, typically 5-10x smaller.",
                ),
                q(
                    "How are real coordinates reconstructed from a LAS point record?",
                    (
                        opt("They are stored directly as decimals"),
                        opt(
                            "Integer values are multiplied by the header scale and added "
                            "to the offset: X_real = X_int * scale + offset",
                            correct=True,
                        ),
                        opt("They are computed from intensity"),
                        opt("They come from the file name"),
                    ),
                    "Integer storage plus scale/offset keeps files compact and precise.",
                ),
                q(
                    "Which ASPRS classification code represents ground?",
                    (
                        opt("Class 6 (building)"),
                        opt("Class 2 (ground)", correct=True),
                        opt("Class 5 (high vegetation)"),
                        opt("Class 9 (water)"),
                    ),
                    "Ground is class 2 - the basis for the DTM.",
                ),
                q(
                    "How does Statistical Outlier Removal identify noise points?",
                    (
                        opt("By their color"),
                        opt(
                            "By flagging points whose mean distance to k nearest "
                            "neighbours is many standard deviations above the global mean",
                            correct=True,
                        ),
                        opt("By deleting the highest points always"),
                        opt("By file size"),
                    ),
                    "SOR uses neighbourhood sparsity relative to the whole cloud to find "
                    "isolated outliers.",
                ),
                q(
                    "What is a DTM, and how does an nDSM (object height) come from it?",
                    (
                        opt("A DTM includes rooftops; nDSM is the color"),
                        opt(
                            "A DTM is the bare-earth surface (ground points); nDSM = DSM - "
                            "DTM gives each object's height above ground",
                            correct=True,
                        ),
                        opt("A DTM is a photograph; nDSM is its negative"),
                        opt("They are unrelated"),
                    ),
                    "DTM bare earth, DSM top of everything, nDSM their difference = object height.",
                ),
                q(
                    "Local neighbourhood geometry says a set of points is thin, "
                    "elongated and elevated. What feature is it most likely?",
                    (
                        opt("A flat roof (high planarity)"),
                        opt("Bare ground"),
                        opt(
                            "A powerline (high linearity, elevated) - fit a catenary for "
                            "sag and clearance",
                            correct=True,
                        ),
                        opt("A tree crown (high sphericity)"),
                    ),
                    "High linearity plus height isolates wires; planar means building, "
                    "scattered multi-return means vegetation.",
                ),
                q(
                    "Which tool is the 'GDAL of point clouds', driven by JSON pipelines?",
                    (
                        opt("Open3D"),
                        opt("PDAL - reader, filters and writer described as JSON", correct=True),
                        opt("A LAS header editor"),
                        opt("QGIS layout designer"),
                    ),
                    "PDAL runs reproducible reader-filters-writer pipelines over LAS/LAZ "
                    "and rasters.",
                ),
                q(
                    "Why fuse LiDAR with imagery for classification?",
                    (
                        opt("To make the file smaller"),
                        opt(
                            "LiDAR gives geometry and imagery gives spectrum; together "
                            "(e.g. geometry plus NDVI) they classify features far more "
                            "reliably than geometry alone",
                            correct=True,
                        ),
                        opt("Imagery replaces the need for 3D points"),
                        opt("It removes all noise automatically"),
                    ),
                    "Colorized clouds combine geometric and spectral cues - trees vs "
                    "buildings become much clearer.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

LIDAR_POINT_CLOUDS_COURSES: tuple[SeedCourse, ...] = (_LIDAR_POINT_CLOUDS,)
