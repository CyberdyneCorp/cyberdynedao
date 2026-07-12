"""Academy seed content - Geodesy.

The science of measuring the Earth: its shape, size and gravity field, and
the reference frames, datums and coordinate transformations that anchor
every geospatial measurement. This course builds intuition for the geoid
and ellipsoid, geodetic datums (WGS84, SIRGAS, NAD83), the coordinate
systems and transformations that connect them, the difference between
ellipsoidal and orthometric heights, the gravity field, modern reference
frames (ITRF) with plate motion, and least-squares network adjustment.
Every lesson is a direct explanation with a concrete formula or
computation and a mermaid diagram, followed by a checkpoint quiz; the
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


_GEODESY = SeedCourse(
    slug="geodesy",
    title="Geodesy",
    description=(
        "The science of measuring the Earth - its shape, size and gravity "
        "field - and the reference frames, datums and coordinate "
        "transformations that anchor every geospatial measurement. Covers the "
        "geoid and ellipsoid, WGS84/SIRGAS/NAD83 datums, geodetic and "
        "cartesian coordinates, Helmert transformations, ellipsoidal versus "
        "orthometric heights, physical geodesy, ITRF and plate motion, and "
        "least-squares network adjustment - with real formulas, EPSG codes "
        "and a diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Geodesy

Every map, GPS fix, cadastral boundary and satellite image rests on a
quiet assumption: that we agree on **where things are** and **on what
surface we measure them**. Geodesy is the science that supplies that
agreement. It measures the Earth's shape, size and gravity field, and
defines the reference frames and datums that turn raw measurements into
coordinates everyone can share.

The approach here is **concrete**: every lesson explains one idea
directly, shows it with a real formula, coordinate example or short
computation, and draws the idea as a diagram. After each lesson there is a
short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **The shape of the Earth** - geoid, ellipsoid and reference surfaces
2. **Geodetic datums** - WGS84, SIRGAS, NAD83
3. **Coordinate types** - geodetic, geocentric and cartesian
4. **Coordinate transformations** - Helmert and seven-parameter
5. **Heights** - ellipsoidal, orthometric and the geoid undulation
6. **The gravity field** - physical geodesy
7. **Reference frames and plate motion** - ITRF
8. **Network adjustment** - least squares

This is the backbone of geospatial engineering. Get the reference
surfaces and datums right and everything downstream - GIS, remote
sensing, surveying, GNSS - lines up. Get them wrong and you get the
classic several-hundred-metre datum shift.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What does geodesy fundamentally study?",
                    (
                        opt("Only the drawing of paper maps"),
                        opt(
                            "The Earth's shape, size and gravity field, plus the "
                            "reference frames and datums that anchor coordinates",
                            correct=True,
                        ),
                        opt("The names of countries and their capitals"),
                        opt("The programming of GIS software"),
                    ),
                    "Geodesy measures the Earth and defines the surfaces and frames "
                    "everything geospatial is referenced to.",
                ),
                q(
                    "Why does getting the reference surface and datum right matter?",
                    (
                        opt("It only affects the map's colour scheme"),
                        opt(
                            "A wrong datum can shift positions by hundreds of metres, so "
                            "GIS, remote sensing and GNSS all depend on it",
                            correct=True,
                        ),
                        opt("It has no measurable effect on coordinates"),
                        opt("It only matters for astronomy"),
                    ),
                    "Mismatched datums produce large systematic position errors - the "
                    "classic datum shift.",
                ),
            ),
        ),
        # -- 1. Shape of the Earth -------------------------------------
        _t(
            "The shape of the Earth: geoid, ellipsoid and reference surfaces",
            "10 min",
            """# The shape of the Earth: geoid, ellipsoid and reference surfaces

The Earth is not a sphere and not a smooth solid. Geodesy uses three
nested ideas of its shape, each useful for a different job.

- **The topographic surface** - the real land and sea floor, mountains and
  valleys. Too irregular to compute on directly.
- **The geoid** - the equipotential surface of the Earth's gravity field
  that best matches **mean sea level** at rest, extended under the
  continents. It is bumpy because gravity varies with mass distribution.
  This is the surface that defines "up" and "down" and true heights.
- **The ellipsoid** - a smooth mathematical surface, an ellipse of
  rotation, chosen to approximate the geoid. Because it has a simple
  equation, we do all coordinate geometry on it.

An ellipsoid is defined by two numbers: the **semi-major axis** `a`
(equatorial radius) and the **flattening** `f`. The **GRS80** and
**WGS84** ellipsoids are almost identical:

```text
GRS80 / WGS84 defining parameters
  a = 6378137.0 m                  (semi-major axis, equator)
  1/f = 298.257222101  (GRS80)     (inverse flattening)
  1/f = 298.257223563  (WGS84)

  flattening        f  = (a - b) / a
  semi-minor axis   b  = a * (1 - f)  = 6356752.314 m
  first eccentricity  e^2 = 2f - f^2  = 0.0066943800

  polar-vs-equator difference: a - b  ~= 21385 m (about 21 km)
```

So the Earth is flattened at the poles by roughly 21 km - small relative
to a 6378 km radius (about 0.3%), which is why a sphere is a decent quick
approximation but never good enough for surveying.

```mermaid
graph TD
    TOPO["Topographic surface real terrain"] --> GEOID["Geoid equipotential mean sea level"]
    GEOID --> ELL["Ellipsoid smooth math surface"]
    ELL --> USE["Used for coordinate geometry"]
    GEOID --> HGT["Defines true heights and up"]
```

Remember: the **geoid** is physical reality that gravity defines; the
**ellipsoid** is the convenient model we compute on. The gap between them
is the geoid undulation, covered in a later lesson.
""",
        ),
        quiz_lesson(
            "Quiz: The shape of the Earth: geoid, ellipsoid and reference surfaces",
            (
                q(
                    "What is the geoid?",
                    (
                        opt("A smooth mathematical ellipse of rotation"),
                        opt(
                            "The equipotential surface of gravity that best matches mean "
                            "sea level, extended under the continents",
                            correct=True,
                        ),
                        opt("The actual rocky topographic surface"),
                        opt("A satellite orbit"),
                    ),
                    "The geoid follows gravity's equipotential and defines true up and "
                    "down; the ellipsoid is the smooth model.",
                ),
                q(
                    "Which two parameters define a reference ellipsoid?",
                    (
                        opt("Latitude and longitude"),
                        opt(
                            "Semi-major axis a and flattening f",
                            correct=True,
                        ),
                        opt("Mass and rotation speed"),
                        opt("Temperature and pressure"),
                    ),
                    "a (equatorial radius) plus f (flattening) fully define the "
                    "ellipsoid of revolution; b follows from them.",
                ),
                q(
                    "Roughly how much is the Earth flattened between equator and pole?",
                    (
                        opt("About 2000 km"),
                        opt("About 21 km, roughly 0.3 percent", correct=True),
                        opt("Zero, the Earth is a perfect sphere"),
                        opt("About 500 m"),
                    ),
                    "a - b is about 21 km on a 6378 km radius, so a sphere is only a "
                    "rough approximation.",
                ),
            ),
        ),
        # -- 2. Datums -------------------------------------------------
        _t(
            "Geodetic datums (WGS84, SIRGAS, NAD83)",
            "10 min",
            """# Geodetic datums (WGS84, SIRGAS, NAD83)

An ellipsoid is just a shape. A **geodetic datum** pins that shape to the
Earth: it fixes the ellipsoid's **size, orientation and origin** relative
to the real planet, so that a latitude and longitude actually correspond
to a place. Same lat/lon on two different datums can be hundreds of metres
apart on the ground.

Two families of datum:

- **Geocentric (global) datums** put the ellipsoid centre at the Earth's
  centre of mass, so they work worldwide with GNSS. **WGS84** (used by GPS)
  and the ITRF-based continental frames are geocentric.
- **Local (classical) datums** fit an ellipsoid to one region only, so it
  hugged the geoid well there in the pre-satellite era but has an offset
  origin. Older national datums are like this.

Key modern datums you will meet:

```text
Datum       Ellipsoid   Region / role                  EPSG (geographic)
---------   ---------   ----------------------------   -----------------
WGS84       WGS84       Global, native to GPS          EPSG:4326
NAD83       GRS80       North America                  EPSG:4269
SIRGAS2000  GRS80       Latin America (ITRF-based)     EPSG:4674
ETRS89      GRS80       Europe (fixed to Eurasia)      EPSG:4258
```

**SIRGAS** (Sistema de Referencia Geocentrico para las Americas) is the
modern geocentric datum for Latin America, realised from ITRF and
maintained by a continuous GNSS network. **NAD83** serves North America;
**ETRS89** serves Europe. Because tectonic plates drift, a
plate-fixed datum such as NAD83 or ETRS89 slowly diverges from the
purely global WGS84/ITRF over decades - by design, so coordinates within
the plate stay stable.

```mermaid
graph TD
    ELL["Ellipsoid a shape"] --> DATUM["Datum origin orientation scale"]
    DATUM --> GEO["Geocentric WGS84 SIRGAS NAD83"]
    DATUM --> LOCAL["Local classical regional fit"]
    GEO --> GNSS["Works globally with GNSS"]
    LOCAL --> OFFSET["Has an origin offset"]
```

Remember: a datum is what makes a coordinate mean a real place. Always
record which datum a coordinate is on - EPSG:4326 (WGS84) versus
EPSG:4674 (SIRGAS2000) can differ by metres depending on epoch and region.
""",
        ),
        quiz_lesson(
            "Quiz: Geodetic datums (WGS84, SIRGAS, NAD83)",
            (
                q(
                    "What does a geodetic datum add to a bare ellipsoid?",
                    (
                        opt("A colour for the map"),
                        opt(
                            "It fixes the ellipsoid's origin, orientation and scale "
                            "relative to the real Earth, so coordinates mean real places",
                            correct=True,
                        ),
                        opt("It changes the ellipsoid into a sphere"),
                        opt("Nothing - datum and ellipsoid are the same"),
                    ),
                    "The datum ties the shape to the planet; without it a lat/lon does "
                    "not correspond to a location.",
                ),
                q(
                    "What is SIRGAS?",
                    (
                        opt("A GPS satellite constellation"),
                        opt(
                            "The modern geocentric, ITRF-based reference system for Latin "
                            "America, maintained by a continuous GNSS network",
                            correct=True,
                        ),
                        opt("A European local datum"),
                        opt("A map projection"),
                    ),
                    "SIRGAS is the geocentric datum for the Americas, realised from ITRF "
                    "(EPSG:4674 for SIRGAS2000).",
                ),
                q(
                    "Why does a plate-fixed datum like NAD83 or ETRS89 slowly drift "
                    "from global WGS84/ITRF?",
                    (
                        opt("Because of measurement mistakes"),
                        opt(
                            "By design it moves with its tectonic plate, so intra-plate "
                            "coordinates stay stable while the global frame does not",
                            correct=True,
                        ),
                        opt("Because the ellipsoid changes shape yearly"),
                        opt("It does not drift at all"),
                    ),
                    "Plate-fixed frames keep local coordinates stable; the trade-off is "
                    "divergence from the global frame over decades.",
                ),
            ),
        ),
        # -- 3. Coordinate types ---------------------------------------
        _t(
            "Geodetic, geocentric and cartesian coordinates",
            "10 min",
            """# Geodetic, geocentric and cartesian coordinates

The same point can be written in several coordinate systems. Three matter
most in geodesy, and you must be able to convert between them.

- **Geodetic (ellipsoidal) coordinates** - latitude `phi`, longitude
  `lambda`, and ellipsoidal height `h`. This is the familiar lat/lon/height
  measured relative to the ellipsoid. Latitude here is *geodetic*: the
  angle of the ellipsoid normal, not a line to the centre.
- **Geocentric cartesian coordinates** - `X, Y, Z` in a right-handed frame
  with origin at the Earth's centre of mass, Z toward the pole, X toward
  the prime meridian at the equator. This is what GNSS actually solves in,
  often called **ECEF** (Earth-Centred, Earth-Fixed).
- **Geocentric latitude** - the angle from the equator of a straight line
  to the Earth's centre. It differs from geodetic latitude because the
  ellipsoid normal does not pass through the centre (except at the equator
  and poles).

The forward conversion **geodetic to ECEF** is exact and closed-form:

```text
Given phi, lambda, h on an ellipsoid (a, e^2):

  N(phi) = a / sqrt(1 - e^2 * sin^2(phi))     (prime vertical radius)

  X = (N + h) * cos(phi) * cos(lambda)
  Y = (N + h) * cos(phi) * sin(lambda)
  Z = (N * (1 - e^2) + h) * sin(phi)

Example: phi = -23.5 deg, lambda = -46.6 deg, h = 760 m (Sao Paulo area)
  N ~= 6385590 m
  X ~=  4020 km, Y ~= -4254 km, Z ~= -2530 km
```

The reverse (ECEF back to phi, lambda, h) needs iteration or a closed
approximation such as Bowring's method, because latitude and height are
coupled through `N(phi)`.

```mermaid
graph LR
    GEO["Geodetic phi lambda h"] --> ECEF["ECEF cartesian X Y Z"]
    ECEF --> GEO2["Back to geodetic by iteration"]
    GEO --> NOTE["Geodetic latitude is the normal angle"]
    ECEF --> GNSS["GNSS solves natively in ECEF"]
```

Remember: geodetic lat/lon/height is what humans read, ECEF X/Y/Z is what
GNSS computes, and geodetic latitude is not the same as geocentric
latitude - never confuse the two.
""",
        ),
        quiz_lesson(
            "Quiz: Geodetic, geocentric and cartesian coordinates",
            (
                q(
                    "What are ECEF coordinates?",
                    (
                        opt("Latitude and longitude only"),
                        opt(
                            "Earth-Centred Earth-Fixed cartesian X Y Z with origin at the "
                            "centre of mass, the frame GNSS solves in",
                            correct=True,
                        ),
                        opt("A map projection grid"),
                        opt("Heights above the geoid"),
                    ),
                    "ECEF is the geocentric cartesian frame: origin at the mass centre, "
                    "Z toward the pole.",
                ),
                q(
                    "How does geodetic latitude differ from geocentric latitude?",
                    (
                        opt("They are always identical"),
                        opt(
                            "Geodetic latitude is the angle of the ellipsoid normal; "
                            "geocentric is the angle of a line to the Earth's centre - "
                            "they differ except at equator and poles",
                            correct=True,
                        ),
                        opt("Geodetic latitude is measured in metres"),
                        opt("Geocentric latitude ignores the equator"),
                    ),
                    "The ellipsoid normal does not pass through the centre except at the "
                    "equator and poles, so the two latitudes differ.",
                ),
                q(
                    "In the geodetic-to-ECEF conversion, what is N(phi)?",
                    (
                        opt("The north coordinate"),
                        opt(
                            "The prime vertical radius of curvature, a / sqrt(1 - e^2 sin^2 phi)",
                            correct=True,
                        ),
                        opt("The ellipsoidal height"),
                        opt("The longitude in radians"),
                    ),
                    "N is the prime vertical radius of curvature and couples latitude and "
                    "height, which is why the reverse needs iteration.",
                ),
            ),
        ),
        # -- 4. Transformations ----------------------------------------
        _t(
            "Coordinate transformations (Helmert, seven-parameter)",
            "11 min",
            """# Coordinate transformations (Helmert, seven-parameter)

Data on one datum often has to move to another - SIRGAS to WGS84, an old
local datum to a modern geocentric one. The workhorse is the **Helmert
(seven-parameter) similarity transformation**, which relates two sets of
ECEF cartesian coordinates with a rigid motion plus a uniform scale.

The seven parameters:

- **Three translations** `Tx, Ty, Tz` - shift of the origin (metres).
- **Three rotations** `Rx, Ry, Rz` - small tilts of the axes (arc-seconds).
- **One scale factor** `s` - a uniform stretch (parts per million, ppm).

For the small rotations of a datum shift, the linearised form is:

```text
Seven-parameter Helmert (position-vector convention):

  [ X' ]   [ Tx ]           [  1   -Rz   Ry ] [ X ]
  [ Y' ] = [ Ty ] + (1 + s) [  Rz   1   -Rx ] [ Y ]
  [ Z' ]   [ Tz ]           [ -Ry   Rx   1  ] [ Z ]

  Rx, Ry, Rz in radians (from arc-seconds: rad = arcsec * pi / 648000)
  s in ppm as a fraction: s = ppm * 1e-6

Special cases:
  - 3-parameter (Molodensky-Badekas simplified): Tx, Ty, Tz only
  - 4-parameter (2D Helmert): 2 translations, 1 rotation, 1 scale
```

Practical notes that trip people up:

- **Convention matters.** The *position-vector* and *coordinate-frame*
  conventions differ by the sign of the rotations. EPSG records which one a
  parameter set uses. Using the wrong sign gives a small, sneaky error.
- **Estimate from common points.** With at least three points known in both
  datums you can least-squares solve for the seven parameters.
- **Datum shifts are not exact.** A seven-parameter fit absorbs the bulk of
  the difference; residual distortions may need a grid (NTv2) for cm work.

```mermaid
graph LR
    SRC["Source datum ECEF"] --> HELM["Seven parameter Helmert"]
    HELM --> DST["Target datum ECEF"]
    P1["Three plus common points"] --> EST["Least squares estimate parameters"]
    EST --> HELM
    HELM --> GRID["Residuals need NTv2 grid for cm"]
```

Remember: Helmert with three translations, three rotations and one scale
moves coordinates cleanly between datums - just get the rotation sign
convention right and remember it is an approximation, not a perfect fit.
""",
        ),
        quiz_lesson(
            "Quiz: Coordinate transformations (Helmert, seven-parameter)",
            (
                q(
                    "What are the seven parameters of a Helmert transformation?",
                    (
                        opt("Seven latitudes"),
                        opt(
                            "Three translations, three rotations and one scale factor",
                            correct=True,
                        ),
                        opt("Seven map projections"),
                        opt("Three ellipsoids and four datums"),
                    ),
                    "Tx Ty Tz, Rx Ry Rz, and scale s - a rigid motion plus uniform scale "
                    "between two cartesian frames.",
                ),
                q(
                    "Why does the rotation sign convention matter in a Helmert transform?",
                    (
                        opt("It changes the scale to kilometres"),
                        opt(
                            "Position-vector and coordinate-frame conventions differ by "
                            "the sign of the rotations, so the wrong sign gives a "
                            "systematic error",
                            correct=True,
                        ),
                        opt("It has no effect on the result"),
                        opt("It only matters for 2D transforms"),
                    ),
                    "EPSG records the convention; mixing them flips rotation signs and "
                    "introduces a small error.",
                ),
                q(
                    "How many common points known in both datums are needed to solve for "
                    "all seven parameters?",
                    (
                        opt("Exactly one"),
                        opt("At least three (giving nine coordinate equations)", correct=True),
                        opt("Zero, the parameters are universal"),
                        opt("At least fifty"),
                    ),
                    "Each point gives three equations; three points give nine, enough to "
                    "solve for seven parameters (more allows least squares).",
                ),
            ),
        ),
        # -- 5. Heights ------------------------------------------------
        _t(
            "Heights: ellipsoidal, orthometric and the geoid undulation",
            "10 min",
            """# Heights: ellipsoidal, orthometric and the geoid undulation

"Height" is ambiguous until you say **above what surface**. Geodesy uses
two very different heights, and confusing them is a classic, expensive
mistake.

- **Ellipsoidal height `h`** - height above the reference ellipsoid,
  measured along the ellipsoid normal. This is what **GNSS gives you
  directly**. It is a pure geometric quantity with no physical meaning:
  water does not necessarily flow from higher `h` to lower `h`.
- **Orthometric height `H`** - height above the **geoid** (mean sea level),
  measured along the curved plumb line. This is the height that matters
  physically - it is what levelling measures, what "elevation" on a
  topographic map means, and it determines which way water flows.

They are linked by the **geoid undulation `N`**, the separation between the
geoid and the ellipsoid at that point:

```text
Fundamental height relationship:

  h = H + N

  h = ellipsoidal height   (from GNSS)
  H = orthometric height   (elevation above mean sea level)
  N = geoid undulation     (geoid minus ellipsoid, can be + or -)

Example: a GNSS receiver reports h = 812.4 m.
A geoid model (e.g. EGM2008) gives N = -3.6 m at that point.
  H = h - N = 812.4 - (-3.6) = 816.0 m orthometric elevation.

Global N ranges roughly from -106 m (south of India) to +85 m (New Guinea).
```

So you never publish a GNSS ellipsoidal height as an elevation. You apply
a **geoid model** - a grid of `N` values such as EGM2008 or a regional
model like GEOID18 (US) or MAPGEO (Brazil) - to convert `h` to `H`.

```mermaid
graph TD
    GNSS["GNSS gives ellipsoidal height h"] --> MODEL["Apply geoid model N"]
    MODEL --> ORTHO["Orthometric height H equals h minus N"]
    ELL["Ellipsoid surface"] --> UND["Undulation N is geoid minus ellipsoid"]
    GEOID["Geoid mean sea level"] --> UND
    ORTHO --> USE["Elevation for maps and water flow"]
```

Remember: `h = H + N`. GNSS gives `h`; maps and physics want `H`; the
geoid model supplies `N` to connect them. Never report an ellipsoidal
height as an elevation.
""",
        ),
        quiz_lesson(
            "Quiz: Heights: ellipsoidal, orthometric and the geoid undulation",
            (
                q(
                    "What is the fundamental relationship between the heights?",
                    (
                        opt("H = h * N"),
                        opt("h = H + N (ellipsoidal = orthometric + undulation)", correct=True),
                        opt("N = h * H"),
                        opt("h = H - 2N"),
                    ),
                    "Ellipsoidal height equals orthometric height plus geoid undulation; "
                    "N connects the geometric and physical heights.",
                ),
                q(
                    "Which height does a GNSS receiver give directly?",
                    (
                        opt("Orthometric height above mean sea level"),
                        opt("Ellipsoidal height h above the reference ellipsoid", correct=True),
                        opt("The geoid undulation"),
                        opt("Height above the terrain"),
                    ),
                    "GNSS is geometric: it gives h above the ellipsoid. You apply a geoid "
                    "model to get orthometric H.",
                ),
                q(
                    "Why must you not publish a raw GNSS height as an elevation?",
                    (
                        opt("Because GNSS heights are always negative"),
                        opt(
                            "Ellipsoidal height h is geometric, not physical; elevation "
                            "means orthometric H above the geoid, so you must apply N",
                            correct=True,
                        ),
                        opt("Because elevations must be in feet"),
                        opt("Because h and H are identical anyway"),
                    ),
                    "Elevation is height above mean sea level (orthometric); using h "
                    "directly can be off by tens of metres via N.",
                ),
            ),
        ),
        # -- 6. Gravity field ------------------------------------------
        _t(
            "The gravity field and physical geodesy",
            "11 min",
            """# The gravity field and physical geodesy

**Physical geodesy** studies the Earth's **gravity field** and how it
shapes the geoid. Because the geoid is an equipotential of gravity, you
cannot understand heights and reference surfaces without it.

The gravity you feel is the sum of **gravitational attraction** (from the
Earth's mass) and the **centrifugal effect** of rotation. On the reference
ellipsoid a smooth theoretical value called **normal gravity** is defined
by the closed **Somigliana formula**:

```text
Somigliana normal gravity on the ellipsoid (GRS80):

  gamma(phi) = gamma_e * (1 + k * sin^2(phi)) / sqrt(1 - e^2 * sin^2(phi))

  gamma_e = 9.7803267715 m/s^2   (normal gravity at the equator)
  gamma_p = 9.8321863685 m/s^2   (normal gravity at the pole)
  k       = (b*gamma_p)/(a*gamma_e) - 1 = 0.001931851353

  So gravity is about 0.5 percent stronger at the poles than the equator,
  because the poles are closer to the Earth's centre and rotation adds no
  centrifugal reduction there.
```

The real measured gravity minus this normal gravity (reduced properly) is
the **gravity anomaly** - it reveals mass excess or deficit below. The
**gravity disturbance** and anomalies feed **Stokes' integral**, the
classical way to compute the geoid undulation `N` from gravity data over
the whole Earth.

Modern practice models the field as a **spherical-harmonic expansion**.
**EGM2008** goes to degree and order 2159, resolving features down to
about 5 arc-minutes; the **GRACE** and **GOCE** satellite missions measured
the long and medium wavelengths of the field with unprecedented accuracy.

```mermaid
graph TD
    MASS["Earth mass distribution"] --> FIELD["Gravity field potential"]
    ROT["Rotation centrifugal"] --> FIELD
    FIELD --> NORMAL["Normal gravity on ellipsoid"]
    FIELD --> ANOM["Gravity anomalies mass excess"]
    ANOM --> STOKES["Stokes integral gives geoid N"]
    FIELD --> SH["Spherical harmonics EGM2008 GRACE GOCE"]
```

Remember: gravity defines the geoid, normal gravity is the smooth
ellipsoidal reference, anomalies expose hidden mass, and Stokes' integral
plus spherical harmonics turn gravity measurements into the geoid model
that heights depend on.
""",
        ),
        quiz_lesson(
            "Quiz: The gravity field and physical geodesy",
            (
                q(
                    "Gravity as we feel it is the sum of which two effects?",
                    (
                        opt("Magnetism and pressure"),
                        opt(
                            "Gravitational attraction from mass plus the centrifugal "
                            "effect of the Earth's rotation",
                            correct=True,
                        ),
                        opt("Temperature and altitude"),
                        opt("Tides and wind"),
                    ),
                    "Measured gravity combines mass attraction and rotational "
                    "centrifugal reduction.",
                ),
                q(
                    "Why is normal gravity stronger at the poles than at the equator?",
                    (
                        opt("The poles are warmer"),
                        opt(
                            "The poles are closer to the Earth's centre and rotation adds "
                            "no centrifugal reduction there",
                            correct=True,
                        ),
                        opt("There is more mass at the equator"),
                        opt("It is actually weaker at the poles"),
                    ),
                    "Flattening brings the poles nearer the centre and the centrifugal "
                    "term vanishes there, so gravity is about 0.5 percent higher.",
                ),
                q(
                    "What is a gravity anomaly?",
                    (
                        opt("A GPS clock error"),
                        opt(
                            "Measured gravity (properly reduced) minus normal gravity, "
                            "revealing mass excess or deficit below",
                            correct=True,
                        ),
                        opt("The height of a mountain"),
                        opt("A rotation of the ellipsoid"),
                    ),
                    "Anomalies expose subsurface mass variations and feed Stokes' "
                    "integral to compute the geoid.",
                ),
            ),
        ),
        # -- 7. Reference frames / ITRF --------------------------------
        _t(
            "Reference frames and plate motion (ITRF)",
            "10 min",
            """# Reference frames and plate motion (ITRF)

A datum is a concept; a **reference frame** is its concrete realisation - a
set of physical stations with published coordinates and velocities that let
you actually measure positions. The global gold standard is the
**International Terrestrial Reference Frame (ITRF)**, maintained by the IERS
and rebuilt every few years (ITRF2008, ITRF2014, ITRF2020) from four space
techniques: **GNSS, VLBI, SLR and DORIS**.

The crucial fact: the Earth's crust is **not rigid**. Tectonic plates move
a few centimetres per year, so a station's coordinates are only meaningful
**at a specific epoch**. ITRF therefore publishes, for each station, both a
position and a **velocity**:

```text
Position of an ITRF station at epoch t:

  X(t) = X(t0) + Vx * (t - t0)
  Y(t) = Y(t0) + Vy * (t - t0)
  Z(t) = Z(t0) + Vz * (t - t0)

Example: a station on the South American plate moving ~1.2 cm/yr.
  Over 10 years it shifts about 12 cm - larger than survey tolerance.

This is why a coordinate must always carry its epoch, e.g.
  "SIRGAS2000, epoch 2000.4"  or  "ITRF2014, epoch 2020.0".
```

To keep everyday coordinates stable, continental frames are **fixed to a
plate**: ETRS89 rotates with the stable part of Eurasia, NAD83 with North
America, and SIRGAS realisations are tied to ITRF at a reference epoch.
Within the plate the numbers barely change; the whole frame drifts relative
to global ITRF, which is exactly the point.

```mermaid
graph TD
    TECH["GNSS VLBI SLR DORIS"] --> ITRF["ITRF global frame"]
    ITRF --> POSVEL["Station position plus velocity"]
    PLATE["Plate motion cm per year"] --> POSVEL
    POSVEL --> EPOCH["Coordinate valid at an epoch"]
    ITRF --> PLATEFIX["Plate fixed frames ETRS89 NAD83 SIRGAS"]
    PLATEFIX --> STABLE["Local coordinates stay stable"]
```

Remember: ITRF gives positions and velocities so coordinates make sense
through time; always tag a coordinate with its **epoch** and frame, because
the ground itself is moving.
""",
        ),
        quiz_lesson(
            "Quiz: Reference frames and plate motion (ITRF)",
            (
                q(
                    "What is the ITRF?",
                    (
                        opt("A single GPS satellite"),
                        opt(
                            "The global terrestrial reference frame realised from GNSS, "
                            "VLBI, SLR and DORIS, giving station positions and velocities",
                            correct=True,
                        ),
                        opt("A map projection for Europe"),
                        opt("A type of ellipsoid"),
                    ),
                    "ITRF is the concrete global frame maintained by the IERS from four "
                    "space-geodetic techniques.",
                ),
                q(
                    "Why must a precise coordinate carry an epoch?",
                    (
                        opt("Because time zones change the longitude"),
                        opt(
                            "Tectonic plates move a few cm per year, so a station's "
                            "position is only valid at a specific point in time",
                            correct=True,
                        ),
                        opt("Because the ellipsoid rotates daily"),
                        opt("Epochs are only decorative"),
                    ),
                    "Plate motion means X(t) = X(t0) + V*(t - t0); without an epoch the "
                    "coordinate is ambiguous.",
                ),
                q(
                    "Why are continental frames like ETRS89 and NAD83 fixed to a plate?",
                    (
                        opt("To make them incompatible with GNSS"),
                        opt(
                            "So everyday intra-plate coordinates stay stable over time, "
                            "even though the frame drifts relative to global ITRF",
                            correct=True,
                        ),
                        opt("Because plates never move"),
                        opt("To avoid using velocities entirely"),
                    ),
                    "Plate-fixed frames keep local numbers steady; the whole frame moving "
                    "relative to ITRF is the intended trade-off.",
                ),
            ),
        ),
        # -- 8. Network adjustment -------------------------------------
        _t(
            "Network adjustment and least squares",
            "11 min",
            """# Network adjustment and least squares

A geodetic network has more measurements than strictly needed - extra
GNSS baselines, angles, distances and levelling that all constrain the same
station coordinates. These **redundant** observations never agree
perfectly. **Least-squares adjustment** finds the single most probable set
of coordinates and, just as importantly, tells you how good they are.

The principle: choose the unknowns that **minimise the sum of squared,
weighted residuals**. In matrix form this is the classic Gauss-Markov
solution:

```text
Linearised least-squares (Gauss-Markov) model:

  l = A x + v        l  = observations minus computed (misclosure)
                     A  = design matrix (partials of obs w.r.t. unknowns)
                     x  = corrections to the unknown coordinates
                     v  = residuals
                     P  = weight matrix = sigma0^2 * Cov^-1

  Normal equations:  (A^T P A) x = A^T P l
  Solution:          x = (A^T P A)^-1 A^T P l
  Cofactor of x:     Qxx = (A^T P A)^-1   -> covariance sigma0^2 * Qxx

  A posteriori variance of unit weight:
     sigma0^2 = (v^T P v) / (n - u)      n observations, u unknowns
```

What the adjustment buys you beyond a best-fit answer:

- **Weights** let precise observations (say GNSS) pull harder than rough
  ones; `P` encodes each observation's uncertainty.
- **Redundancy** `n - u` (degrees of freedom) enables **statistical
  testing** - a chi-square test on `sigma0^2`, and **data snooping** to
  flag individual outliers (blunders) by their standardised residuals.
- **Error ellipses** come straight from `Qxx`: the covariance of each
  station's coordinates, so you can report and visualise precision.

```mermaid
graph TD
    OBS["Redundant observations"] --> MODEL["Linearise l equals A x plus v"]
    MODEL --> NORMAL["Normal equations A T P A x"]
    NORMAL --> SOL["Solve for corrections x"]
    SOL --> QXX["Covariance Qxx and error ellipses"]
    SOL --> TEST["Chi square test and data snooping"]
    TEST --> BLUNDER["Flag outliers"]
```

Remember: least squares turns many imperfect, redundant measurements into
one best estimate **with** a rigorous statement of its precision - the
coordinates plus their covariance, outlier detection and error ellipses.
That is how a geodetic network becomes trustworthy.
""",
        ),
        quiz_lesson(
            "Quiz: Network adjustment and least squares",
            (
                q(
                    "What does least-squares adjustment minimise?",
                    (
                        opt("The number of stations"),
                        opt(
                            "The sum of squared, weighted residuals of the redundant observations",
                            correct=True,
                        ),
                        opt("The longitude of the network"),
                        opt("The number of observations taken"),
                    ),
                    "It finds the unknowns that minimise v^T P v, the weighted squared residuals.",
                ),
                q(
                    "What is the role of the weight matrix P?",
                    (
                        opt("It stores the map projection"),
                        opt(
                            "It encodes each observation's uncertainty so precise "
                            "observations influence the solution more than rough ones",
                            correct=True,
                        ),
                        opt("It counts the number of unknowns"),
                        opt("It converts metres to degrees"),
                    ),
                    "P is built from the observation covariance; more precise "
                    "measurements get higher weight.",
                ),
                q(
                    "Why is redundancy (more observations than unknowns) valuable?",
                    (
                        opt("It makes the network cheaper"),
                        opt(
                            "It enables statistical testing - checking sigma0^2 and data "
                            "snooping to detect outliers - and yields covariance for error "
                            "ellipses",
                            correct=True,
                        ),
                        opt("It removes the need for weights"),
                        opt("It guarantees zero residuals"),
                    ),
                    "Degrees of freedom n - u drive quality control, blunder detection "
                    "and precision estimates.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the difference between the geoid and the ellipsoid?",
                    (
                        opt("They are the same surface"),
                        opt(
                            "The geoid is the physical equipotential of gravity near mean "
                            "sea level; the ellipsoid is the smooth math surface we "
                            "compute coordinates on",
                            correct=True,
                        ),
                        opt("The geoid is smooth and the ellipsoid is bumpy"),
                        opt("The ellipsoid defines true up and down"),
                    ),
                    "Geoid = gravity reality; ellipsoid = convenient model. Their gap is "
                    "the undulation N.",
                ),
                q(
                    "Which two numbers define a reference ellipsoid?",
                    (
                        opt("Latitude and height"),
                        opt("Semi-major axis a and flattening f", correct=True),
                        opt("Mass and rotation rate"),
                        opt("Two eccentricities only"),
                    ),
                    "a and f fully define the ellipsoid of revolution; b and e^2 derive from them.",
                ),
                q(
                    "What does a geodetic datum provide that a bare ellipsoid does not?",
                    (
                        opt("A projection to a flat map"),
                        opt(
                            "It fixes the ellipsoid's origin, orientation and scale to the "
                            "real Earth so coordinates mean real places",
                            correct=True,
                        ),
                        opt("A colour scheme"),
                        opt("A gravity value"),
                    ),
                    "WGS84, SIRGAS and NAD83 are datums: they pin the shape to the planet.",
                ),
                q(
                    "In which coordinate frame does GNSS natively compute positions?",
                    (
                        opt("A UTM grid"),
                        opt("Geocentric cartesian ECEF X Y Z", correct=True),
                        opt("Orthometric heights only"),
                        opt("Geocentric latitude alone"),
                    ),
                    "GNSS solves in ECEF; geodetic lat/lon/height is derived from it.",
                ),
                q(
                    "The seven parameters of a Helmert transformation are:",
                    (
                        opt("Seven translations"),
                        opt(
                            "Three translations, three rotations and one scale factor",
                            correct=True,
                        ),
                        opt("Three datums and four ellipsoids"),
                        opt("Seven rotations"),
                    ),
                    "A rigid motion (3 shifts, 3 rotations) plus a uniform scale between "
                    "two cartesian frames.",
                ),
                q(
                    "What is the height relationship h = H + N?",
                    (
                        opt(
                            "Ellipsoidal height equals orthometric height plus geoid undulation",
                            correct=True,
                        ),
                        opt("Orthometric height equals ellipsoidal height plus latitude"),
                        opt("Height equals half the flattening"),
                        opt("Undulation equals gravity times height"),
                    ),
                    "GNSS gives h; a geoid model gives N; H = h - N is the orthometric elevation.",
                ),
                q(
                    "Why does normal gravity vary with latitude?",
                    (
                        opt("Because longitude changes"),
                        opt(
                            "Flattening puts the poles closer to the centre and removes "
                            "the centrifugal reduction, so gravity is stronger there",
                            correct=True,
                        ),
                        opt("Because the ellipsoid is a sphere"),
                        opt("It does not vary with latitude"),
                    ),
                    "The Somigliana formula gives about 0.5 percent higher gravity at the "
                    "poles than the equator.",
                ),
                q(
                    "Why must a precise coordinate carry an epoch in a modern frame like ITRF?",
                    (
                        opt("Because daylight saving changes it"),
                        opt(
                            "Tectonic plate motion of a few cm per year means the position "
                            "is only valid at a given time",
                            correct=True,
                        ),
                        opt("Because the ellipsoid changes yearly"),
                        opt("Epochs only matter for maps"),
                    ),
                    "ITRF gives positions and velocities; without an epoch a coordinate "
                    "is ambiguous.",
                ),
                q(
                    "What does least-squares network adjustment produce besides best-fit "
                    "coordinates?",
                    (
                        opt("Only a single number"),
                        opt(
                            "A rigorous precision statement - covariance, error ellipses "
                            "and outlier detection from the redundancy",
                            correct=True,
                        ),
                        opt("A new ellipsoid"),
                        opt("The map projection to use"),
                    ),
                    "Redundant observations give both the estimate and Qxx-based "
                    "precision plus statistical testing.",
                ),
                q(
                    "Which EPSG code corresponds to WGS84 geographic coordinates?",
                    (
                        opt("EPSG:4674"),
                        opt("EPSG:4326", correct=True),
                        opt("EPSG:4269"),
                        opt("EPSG:4258"),
                    ),
                    "EPSG:4326 is WGS84 geographic; 4674 is SIRGAS2000, 4269 NAD83, 4258 ETRS89.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

GEODESY_COURSES: tuple[SeedCourse, ...] = (_GEODESY,)
