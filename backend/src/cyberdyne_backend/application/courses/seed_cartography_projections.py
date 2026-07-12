"""Academy seed content - Cartography and Map Projections.

How the round Earth becomes a flat map. This course builds the mental
model beneath every GIS tool: geographic coordinates on an ellipsoid,
the map projections that flatten them and the distortion that flattening
forces, map scale and generalization, and the EPSG registry of coordinate
reference systems that ties it all together. Every lesson is a direct
explanation with a concrete coordinate or projection example and a mermaid
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


_CARTOGRAPHY_PROJECTIONS = SeedCourse(
    slug="cartography-projections",
    title="Cartography & Map Projections",
    description=(
        "How the round Earth becomes a flat map: geographic coordinate "
        "systems, the map projections that flatten them and their unavoidable "
        "distortions, map scale and generalization, and the EPSG registry of "
        "coordinate reference systems that ties it all together - with real "
        "coordinate examples, PROJ and GDAL snippets, and a diagram in every "
        "lesson."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Cartography and Map Projections

The Earth is (nearly) a sphere, but maps and screens are flat. Turning
one into the other is the oldest problem in geospatial work, and getting
it wrong is the most common source of "my layers do not line up" bugs.
This course gives you the whole picture: where coordinates come from, why
no flat map can be perfect, how the standard projections trade one kind
of accuracy for another, and how the **EPSG** registry lets tools agree
on what a coordinate means.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it with a real coordinate or a short PROJ/GDAL example,
and draws the idea as a diagram. After each lesson there is a short quiz;
at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Coordinate systems** - latitude, longitude, and the shape of the Earth
2. **Why a perfect map is impossible** - the sphere will not flatten
3. **Projection families** - cylindrical, conic, azimuthal
4. **Mercator, UTM and Web Mercator** - the projections you meet daily
5. **Distortion** - scale, area, angle, and Tissot's indicatrix
6. **Coordinate reference systems and EPSG** - the registry that ties it together
7. **Scale, generalization and symbolization** - making a readable map
8. **Reprojecting in practice** - GDAL and PROJ on real data

This is the foundation. Once projections and CRS click, the rest of GIS -
remote sensing, spatial databases, web maps - stops fighting you.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What core problem does cartography have to solve?",
                    (
                        opt("How to store images on disk"),
                        opt(
                            "How to represent the curved surface of the Earth on a "
                            "flat map or screen without misleading the reader",
                            correct=True,
                        ),
                        opt("How to make GPS receivers cheaper"),
                        opt("How to compress satellite imagery"),
                    ),
                    "A round Earth on a flat surface is the central problem; every "
                    "projection is one answer to it.",
                ),
                q(
                    "What is the most common practical symptom of getting projections wrong?",
                    (
                        opt("The map prints in the wrong colour"),
                        opt(
                            "Layers do not line up - data lands in the wrong place "
                            "because the coordinate reference systems disagree",
                            correct=True,
                        ),
                        opt("The file will not open at all"),
                        opt("The computer runs out of memory"),
                    ),
                    "Mismatched CRS is the classic 'my layers are in the ocean' bug; "
                    "this course prevents it.",
                ),
            ),
        ),
        # -- 1. Coordinate systems -------------------------------------
        _t(
            "Coordinate systems and geographic coordinates",
            "10 min",
            """# Coordinate systems and geographic coordinates

To locate anything on Earth we need agreed numbers. **Geographic
coordinates** use two angles measured from the centre of the Earth:

- **Latitude** (often written the Greek letter phi) - the angle north or
  south of the **equator**, from 0 degrees at the equator to plus 90 at
  the North Pole and minus 90 at the South Pole. Lines of equal latitude
  are **parallels**.
- **Longitude** (often written lambda) - the angle east or west of the
  **prime meridian** (through Greenwich), from 0 to plus or minus 180
  degrees. Lines of equal longitude are **meridians**.

These angles only mean something once we fix the **shape** we are
measuring against. The Earth is not a perfect sphere; it bulges at the
equator, so we model it as an **ellipsoid** (a flattened sphere). A
**datum** ties that ellipsoid to the real Earth - it defines where the
model sits. The modern global datum is **WGS84**, what GPS reports, with
EPSG code **4326**.

A coordinate is meaningless without its datum. The same numbers on NAD27
versus WGS84 can differ by hundreds of metres on the ground.

Coordinates are written **latitude, longitude** in most geographic
contexts, but many tools (and GeoJSON) use **longitude, latitude** - the
math order x, y. Always check.

```text
The Eiffel Tower in WGS84 (EPSG:4326):
    latitude  =  48.8584 degrees N   (phi)
    longitude =   2.2945 degrees E   (lambda)

Degrees-minutes-seconds <-> decimal degrees:
    48 deg 51 min 30.2 sec N
    = 48 + 51/60 + 30.2/3600
    = 48.8584 degrees

GeoJSON writes it x,y (lon,lat):  [2.2945, 48.8584]
```

```mermaid
graph TD
    EARTH["Real Earth surface"] --> ELL["Ellipsoid model WGS84"]
    ELL --> DATUM["Datum ties model to Earth"]
    DATUM --> LAT["Latitude phi north south"]
    DATUM --> LON["Longitude lambda east west"]
    LAT --> COORD["A located point"]
    LON --> COORD
```

Remember: latitude and longitude are angles on an ellipsoid fixed by a
datum. State the datum (usually WGS84) or the numbers are ambiguous.
""",
        ),
        quiz_lesson(
            "Quiz: Coordinate systems and geographic coordinates",
            (
                q(
                    "What do latitude and longitude measure?",
                    (
                        opt("Distances in metres from the nearest city"),
                        opt(
                            "Angles from the centre of the Earth - north or south of "
                            "the equator (latitude) and east or west of the prime "
                            "meridian (longitude)",
                            correct=True,
                        ),
                        opt("The elevation and depth of a point"),
                        opt("Pixel rows and columns in an image"),
                    ),
                    "They are angular coordinates: latitude 0 to plus or minus 90, "
                    "longitude 0 to plus or minus 180 degrees.",
                ),
                q(
                    "Why must a coordinate always state its datum (for example WGS84)?",
                    (
                        opt("Because datums change the colour of the map"),
                        opt(
                            "The same latitude and longitude numbers on different "
                            "datums can point to locations hundreds of metres apart",
                            correct=True,
                        ),
                        opt("Because GPS only works on one datum"),
                        opt("Datums are only needed for elevation"),
                    ),
                    "A datum fixes the ellipsoid to the real Earth; without it the "
                    "numbers are ambiguous.",
                ),
                q(
                    "Which EPSG code identifies plain WGS84 latitude and longitude?",
                    (
                        opt("EPSG:3857"),
                        opt("EPSG:4326", correct=True),
                        opt("EPSG:32633"),
                        opt("EPSG:27700"),
                    ),
                    "EPSG:4326 is WGS84 geographic (lat/lon); 3857 is Web Mercator.",
                ),
            ),
        ),
        # -- 2. Impossibility of a perfect map -------------------------
        _t(
            "Map projections and the impossibility of a perfect map",
            "10 min",
            """# Map projections and the impossibility of a perfect map

A **map projection** is a rule - a set of equations - that turns
geographic coordinates (lat, lon) on the curved Earth into flat map
coordinates (x, y). Every digital map applies one.

Here is the hard truth: **no projection can be perfect.** A sphere has
non-zero curvature and a flat plane has zero curvature; you cannot flatten
a sphere without stretching, tearing or squashing it. This is not an
engineering limitation - it is a theorem of geometry (Gauss's *Theorema
Egregium*). Try to flatten an orange peel and it must crack or distort.

So every projection **distorts** something. The four properties a
projection might try to keep are:

- **Area** - regions keep their true relative size (**equal-area**).
- **Angle/shape** - local angles are correct, shapes look right in the
  small (**conformal**).
- **Distance** - distances from a point or along lines are true
  (**equidistant**, only ever partially).
- **Direction** - bearings from a point are true (**azimuthal**).

A projection can preserve **at most one** of area or shape, never both.
You choose a projection by deciding **which distortion you can tolerate**
for the task: a thematic map of population needs equal-area; a navigation
chart needs conformal.

```text
A projection is just two functions:
    x = f(lambda, phi)      map easting  from lon, lat
    y = g(lambda, phi)      map northing from lon, lat

Simple equirectangular (plate carree) example:
    x = R * lambda          (radians)
    y = R * phi
It is neither equal-area nor conformal - only simple.
```

```mermaid
graph TD
    GLOBE["Curved Earth lat lon"] --> PROJ["Projection equations"]
    PROJ --> MAP["Flat map x y"]
    PROJ --> COST["Must distort something"]
    COST --> AREA["Area equal area"]
    COST --> SHAPE["Shape conformal"]
    COST --> DIST["Distance equidistant"]
```

Remember: flattening a sphere always distorts. The only real question is
**what you preserve and what you sacrifice** - so pick the projection that
protects the property your map depends on.
""",
        ),
        quiz_lesson(
            "Quiz: Map projections and the impossibility of a perfect map",
            (
                q(
                    "What is a map projection?",
                    (
                        opt("A type of satellite sensor"),
                        opt(
                            "A set of equations that convert curved-Earth lat/lon "
                            "coordinates into flat map x/y coordinates",
                            correct=True,
                        ),
                        opt("A file format for storing maps"),
                        opt("The brightness setting of a display"),
                    ),
                    "A projection is the mathematical rule x = f(lon,lat), y = "
                    "g(lon,lat) that flattens the Earth.",
                ),
                q(
                    "Why can no map projection be free of distortion?",
                    (
                        opt("Because computers round the numbers"),
                        opt(
                            "A curved surface cannot be flattened onto a plane without "
                            "stretching or tearing - it is a fact of geometry",
                            correct=True,
                        ),
                        opt("Because ink smudges on paper"),
                        opt("Because the Earth keeps moving"),
                    ),
                    "Gauss's Theorema Egregium: surfaces of different curvature cannot "
                    "match without distortion.",
                ),
                q(
                    "A single projection can preserve at most which of these?",
                    (
                        opt("Both area and shape at the same time everywhere"),
                        opt(
                            "Either area (equal-area) or shape (conformal), but not both",
                            correct=True,
                        ),
                        opt("Every property perfectly if resolution is high enough"),
                        opt("Nothing at all - all projections are equally wrong"),
                    ),
                    "You choose which property to protect; equal-area and conformal are "
                    "mutually exclusive.",
                ),
            ),
        ),
        # -- 3. Projection families ------------------------------------
        _t(
            "Projection families: cylindrical, conic, azimuthal",
            "10 min",
            """# Projection families: cylindrical, conic, azimuthal

Most projections come from imagining the Earth's surface projected onto a
**developable surface** - a shape you *can* unroll flat without
distortion: a cylinder, a cone, or a plane. This gives three big families,
each faithful along the line or point where the surface touches the globe
(the **standard line** or standard parallel) and worse as you move away.

- **Cylindrical** - wrap a cylinder around the globe, usually touching at
  the equator. Meridians become straight vertical lines. Good for the
  **tropics and world maps**; distortion grows badly toward the poles.
  (Mercator, Web Mercator, Plate Carree.)
- **Conic** - set a cone over the globe, touching along one or two
  **standard parallels** in the mid-latitudes. Excellent for **mid-latitude
  regions wider east-west than north-south** - the USA, Europe. (Albers
  equal-area, Lambert conformal conic.)
- **Azimuthal (planar)** - touch a flat plane at a single point. All
  directions from that centre point are true. Ideal for the **poles** or
  for centring on one location. (Stereographic, orthographic, azimuthal
  equidistant.)

Each surface can also be **tangent** (touching along one line/point) or
**secant** (slicing through, touching along two lines) - secant spreads
the distortion more evenly across the mapped band.

```text
Match the family to the region shape:
    world / tropics, equator band  -> cylindrical
    mid-latitude, wide E-W country -> conic (2 standard parallels)
    polar region / point-centred   -> azimuthal
```

```mermaid
graph TD
    GLOBE["Globe"] --> CYL["Cylinder touches equator"]
    GLOBE --> CON["Cone touches mid latitudes"]
    GLOBE --> AZ["Plane touches one point"]
    CYL --> CYLU["World and tropics maps"]
    CON --> CONU["Mid latitude regions"]
    AZ --> AZU["Polar and point centred maps"]
```

Remember: cylinder for the equator band and world maps, cone for
mid-latitude regions, plane for the poles or a chosen centre. Pick the
family whose faithful zone matches where your data lives.
""",
        ),
        quiz_lesson(
            "Quiz: Projection families: cylindrical, conic, azimuthal",
            (
                q(
                    "What is a 'developable surface' in projections?",
                    (
                        opt("A surface still under construction"),
                        opt(
                            "A cylinder, cone or plane - a shape that can be unrolled "
                            "flat without further distortion",
                            correct=True,
                        ),
                        opt("The developer's screen resolution"),
                        opt("Any curved surface at all"),
                    ),
                    "Cylinder, cone and plane unroll to a flat sheet, which is why the "
                    "three families are built on them.",
                ),
                q(
                    "Which family is best suited to a mid-latitude country that is wide "
                    "east-to-west, such as the USA?",
                    (
                        opt("Cylindrical"),
                        opt("Conic - touching along standard parallels", correct=True),
                        opt("Azimuthal"),
                        opt("None can map mid-latitudes"),
                    ),
                    "Conic projections (Albers, Lambert conformal conic) fit "
                    "mid-latitude, east-west regions well.",
                ),
                q(
                    "Why is an azimuthal (planar) projection the natural choice for a "
                    "map of the Arctic or Antarctic?",
                    (
                        opt("Because planes are cheaper to compute"),
                        opt(
                            "It touches at a single point, so centring it on a pole "
                            "keeps directions from that pole true and distortion "
                            "symmetric",
                            correct=True,
                        ),
                        opt("Because cylinders cannot show ice"),
                        opt("Because the poles have no coordinates"),
                    ),
                    "Azimuthal projections are true in direction from their centre - "
                    "ideal centred on a pole.",
                ),
            ),
        ),
        # -- 4. Mercator, UTM, Web Mercator ----------------------------
        _t(
            "Mercator, UTM and Web Mercator",
            "11 min",
            """# Mercator, UTM and Web Mercator

Three cylindrical projections dominate everyday geospatial work, and
knowing how they differ prevents real mistakes.

**Mercator (1569)** is **conformal** - it preserves angles, so a line of
constant compass bearing (a rhumb line) is straight. That made it perfect
for **sea navigation**. The cost: area distortion explodes toward the
poles. Greenland looks as big as Africa but is about 14 times smaller.
Never use plain Mercator to compare sizes.

**UTM (Universal Transverse Mercator)** solves the distortion problem by
**dividing the world into 60 zones**, each 6 degrees of longitude wide,
and applying a Transverse Mercator (cylinder turned on its side, tangent
along a central meridian) to each. Within a zone, distortion is tiny and
coordinates are in **metres** - ideal for surveying and engineering. The
catch: a UTM coordinate is only valid **within its zone**. Each zone has
its own EPSG code.

**Web Mercator (EPSG:3857)** is what Google Maps, OpenStreetMap and nearly
every web map use. It is Mercator computed on a **sphere** for speed,
which makes it *not quite* conformal and definitely not equal-area, but it
tiles cleanly into a square and renders fast. Great for a slippy web map,
wrong for area analysis.

```text
UTM zone from longitude:
    zone = floor((lon + 180) / 6) + 1

    lon = 2.29 E  ->  floor(182.29 / 6) + 1 = 31   (Paris = zone 31N)

EPSG codes for that zone:
    32631  = WGS84 / UTM zone 31N   (northern hemisphere)
    32731  = WGS84 / UTM zone 31S   (southern hemisphere)
```

```mermaid
graph TD
    MERC["Mercator conformal"] --> NAV["Straight rhumb lines for navigation"]
    MERC --> BADAREA["Area exaggerated toward poles"]
    UTM["UTM 60 zones of 6 degrees"] --> METRES["Metre coordinates low distortion"]
    UTM --> ZONE["Valid only inside one zone"]
    WEB["Web Mercator EPSG 3857"] --> TILES["Fast square web map tiles"]
    WEB --> NOAREA["Not for area analysis"]
```

Remember: Mercator preserves angles not area; UTM gives low-distortion
metres but only within its 6-degree zone; Web Mercator (3857) is the web
map default - convenient to draw, wrong for measuring area.
""",
        ),
        quiz_lesson(
            "Quiz: Mercator, UTM and Web Mercator",
            (
                q(
                    "Why does the classic Mercator projection make Greenland look "
                    "roughly the size of Africa?",
                    (
                        opt("Greenland really is that large"),
                        opt(
                            "Mercator is conformal, so it hugely exaggerates area "
                            "toward the poles - it is wrong for comparing sizes",
                            correct=True,
                        ),
                        opt("The map was drawn incorrectly"),
                        opt("Ice reflects more light"),
                    ),
                    "Mercator preserves angles and inflates area with latitude; "
                    "Greenland is about 14 times smaller than Africa.",
                ),
                q(
                    "How does UTM keep distortion low across the whole world?",
                    (
                        opt("By using a single global projection"),
                        opt(
                            "It splits the world into 60 zones of 6 degrees longitude, "
                            "each with its own Transverse Mercator in metres",
                            correct=True,
                        ),
                        opt("By projecting onto a cone"),
                        opt("By ignoring the poles entirely"),
                    ),
                    "Narrow 6-degree zones keep each Transverse Mercator nearly "
                    "distortion-free, but coordinates are only valid in-zone.",
                ),
                q(
                    "What is Web Mercator (EPSG:3857) good and bad for?",
                    (
                        opt("Good for area analysis, bad for web maps"),
                        opt(
                            "Good for fast, square-tiling web maps; bad for measuring "
                            "area because it is not equal-area",
                            correct=True,
                        ),
                        opt("Good for polar navigation only"),
                        opt("Equally correct for everything"),
                    ),
                    "3857 tiles cleanly and renders fast but distorts area - do not "
                    "measure areas in it.",
                ),
            ),
        ),
        # -- 5. Distortion / Tissot ------------------------------------
        _t(
            "Distortion: scale, area, angle and Tissot's indicatrix",
            "10 min",
            """# Distortion: scale, area, angle and Tissot's indicatrix

Since every projection distorts, we need a way to **see and measure** the
distortion. Four things vary across a projected map:

- **Scale distortion** - the ratio of distance on the map to true distance
  changes from place to place. The **scale factor** is 1.0 only along the
  standard line(s); elsewhere it is greater or less than 1.
- **Area distortion** - regions grow or shrink. Zero in equal-area
  projections, large near the poles in Mercator.
- **Angular (shape) distortion** - the shape of small features is skewed.
  Zero in conformal projections.
- **Direction distortion** - bearings are wrong except from special points.

The classic tool for visualising all of this at once is **Tissot's
indicatrix**: draw a tiny circle at points across the globe and see what
the projection does to it.

- On a **conformal** map the indicatrix stays a **circle** (shape kept)
  but changes **size** (scale/area vary).
- On an **equal-area** map the indicatrix becomes an **ellipse** of the
  **same area** everywhere (area kept) but changing **shape**.
- A circle that stays a circle of constant size would mean no distortion -
  impossible except along the standard line.

```text
Tissot at a point gives two principal scale factors, h and k:
    conformal   ->  h == k        (circle, varying size)
    equal area  ->  h * k == 1    (ellipse, constant area)

Mercator scale factor grows with latitude:
    k = 1 / cos(phi)
    phi = 60 deg  ->  k = 1 / cos(60) = 2.0   (twice too long)
```

```mermaid
graph TD
    PROJ["Any projection"] --> TIS["Tissot indicatrix tiny circle"]
    TIS --> CONF["Conformal keeps circle shape"]
    TIS --> EQA["Equal area keeps ellipse area"]
    CONF --> SCALE["Scale and area distortion remain"]
    EQA --> SHAPE["Shape distortion remains"]
```

Remember: Tissot's indicatrix makes distortion visible - circles that keep
their shape mean conformal, ellipses that keep their area mean equal-area,
and the scale factor tells you exactly how stretched each spot is.
""",
        ),
        quiz_lesson(
            "Quiz: Distortion: scale, area, angle and Tissot's indicatrix",
            (
                q(
                    "What does Tissot's indicatrix show?",
                    (
                        opt("The colour scheme of a map"),
                        opt(
                            "How a tiny circle on the globe is deformed by the "
                            "projection, revealing scale, area and angular distortion",
                            correct=True,
                        ),
                        opt("The number of pixels in an image"),
                        opt("The elevation of the terrain"),
                    ),
                    "It is a small circle drawn across the map; its deformation "
                    "visualises the local distortion.",
                ),
                q(
                    "On a conformal projection, what happens to Tissot's indicatrix?",
                    (
                        opt("It becomes an ellipse of constant area"),
                        opt(
                            "It stays a circle (shape preserved) but changes size as scale varies",
                            correct=True,
                        ),
                        opt("It disappears completely"),
                        opt("It turns into a square"),
                    ),
                    "Conformal keeps shape: the indicatrix stays circular but its size "
                    "changes with the scale factor.",
                ),
                q(
                    "In Mercator the scale factor is k = 1/cos(phi). At latitude 60 "
                    "degrees, what is it?",
                    (
                        opt("0.5"),
                        opt("1.0 - no distortion"),
                        opt(
                            "2.0 - distances are stretched to twice their true length", correct=True
                        ),
                        opt("60"),
                    ),
                    "cos(60) = 0.5, so k = 1/0.5 = 2.0 - hence the extreme area "
                    "inflation toward the poles.",
                ),
            ),
        ),
        # -- 6. CRS and EPSG -------------------------------------------
        _t(
            "Coordinate reference systems and the EPSG registry",
            "11 min",
            """# Coordinate reference systems and the EPSG registry

Latitude/longitude, a datum, and a projection together make a **Coordinate
Reference System (CRS)** - the full recipe that says exactly what a pair of
numbers means on the Earth. Two kinds:

- **Geographic CRS** - angular lat/lon on an ellipsoid (for example
  WGS84, EPSG:4326). Units are degrees.
- **Projected CRS** - a geographic CRS plus a projection, giving flat x/y
  in metres or feet (for example UTM zone 31N, EPSG:32631; British
  National Grid, EPSG:27700).

The problem: there are thousands of CRS in use worldwide. To let tools
agree, the **EPSG registry** (originally the European Petroleum Survey
Group, now maintained by OGP/IOGP) gives every CRS a **unique integer
code**. "EPSG:4326" is a global, unambiguous name that GDAL, PostGIS,
QGIS and web maps all understand.

Common codes worth memorising:

```text
EPSG:4326   WGS84 geographic lat/lon         (GPS, GeoJSON)      degrees
EPSG:3857   Web Mercator                     (web map tiles)     metres
EPSG:32631  WGS84 / UTM zone 31N             (survey, N. hemi)   metres
EPSG:27700  OSGB36 / British National Grid   (UK mapping)        metres
EPSG:4269   NAD83 geographic                 (US data)           degrees
```

Under the hood a CRS is defined by machine-readable **WKT** (Well-Known
Text) or the compact **PROJ** string:

```text
PROJ string for UTM zone 31N on WGS84:
    +proj=utm +zone=31 +datum=WGS84 +units=m +no_defs

Equivalent short name that every tool resolves:
    EPSG:32631
```

The golden rule of GIS: **every dataset must declare its CRS**, and before
you overlay, measure, or analyse, all layers must be in the **same** CRS.
A shapefile without a `.prj` file, or a mismatch between 4326 and 3857, is
the number-one cause of misaligned data.

```mermaid
graph TD
    DATUM["Datum WGS84"] --> GEO["Geographic CRS 4326"]
    GEO --> PROJCRS["Add projection"]
    PROJCRS --> PRJ["Projected CRS 32631 metres"]
    GEO --> EPSG["EPSG code names it"]
    PRJ --> EPSG
    EPSG --> TOOLS["GDAL PostGIS QGIS agree"]
```

Remember: a CRS is datum plus (optional) projection; the EPSG registry
gives each one an unambiguous integer code; always tag your data with its
CRS and match CRS before you overlay.
""",
        ),
        quiz_lesson(
            "Quiz: Coordinate reference systems and the EPSG registry",
            (
                q(
                    "What is a Coordinate Reference System (CRS)?",
                    (
                        opt("A brand of GPS receiver"),
                        opt(
                            "The full recipe - datum and optional projection - that "
                            "defines exactly what a coordinate pair means on Earth",
                            correct=True,
                        ),
                        opt("A single latitude value"),
                        opt("The resolution of a raster"),
                    ),
                    "A CRS ties numbers to real locations; it is geographic (lat/lon) "
                    "or projected (x/y in metres).",
                ),
                q(
                    "What does the EPSG registry provide?",
                    (
                        opt("Free satellite imagery"),
                        opt(
                            "A unique integer code for each coordinate reference "
                            "system so different tools name the same CRS unambiguously",
                            correct=True,
                        ),
                        opt("A map-drawing program"),
                        opt("Cloud storage for maps"),
                    ),
                    "EPSG:4326, EPSG:3857 and so on are shared identifiers understood "
                    "by GDAL, PostGIS, QGIS and web maps.",
                ),
                q(
                    "You overlay a layer in EPSG:4326 with one in EPSG:3857 and they do "
                    "not line up. Why?",
                    (
                        opt("One file is corrupted"),
                        opt(
                            "They are in different coordinate reference systems - the "
                            "layers must be reprojected into a common CRS first",
                            correct=True,
                        ),
                        opt("Web Mercator is always broken"),
                        opt("Degrees and metres are the same thing"),
                    ),
                    "Mismatched CRS is the classic misalignment bug; reproject to a "
                    "single CRS before overlaying or measuring.",
                ),
            ),
        ),
        # -- 7. Scale, generalization, symbolization -------------------
        _t(
            "Map scale, generalization and symbolization",
            "10 min",
            """# Map scale, generalization and symbolization

Beyond projections, a *readable* map depends on three ideas: scale,
generalization, and symbolization.

**Scale** is the ratio of map distance to ground distance, written as a
**representative fraction** like 1:25,000 - one unit on the map equals
25,000 on the ground. Note the wording:

- A **large-scale** map (1:1,000) covers a **small area** in **great
  detail** - a city block, a site plan.
- A **small-scale** map (1:10,000,000) covers a **large area** with
  **little detail** - a whole continent.

The fraction is larger (1/1,000 > 1/10,000,000) for the large-scale map -
that is the source of the everyday confusion.

**Generalization** is simplifying reality to fit the scale. You cannot
draw every bend of a coastline on a world map, so you **simplify**
geometry, **select** what to keep, **aggregate** small features, and
**displace** symbols that would collide. The **Douglas-Peucker** algorithm
is the classic line-simplification method.

**Symbolization** turns data into visual marks using the **visual
variables** - position, size, shape, colour hue, colour value, and pattern
- so a reader decodes the map at a glance. Sequential data (population
density) maps to a light-to-dark **colour value** ramp; categorical data
(land-use type) maps to distinct **hues**.

```text
Scale rule of thumb (representative fraction):
    1:1 000          large scale,  small area,  high detail
    1:25 000         topographic map
    1:10 000 000     small scale,  large area,  low detail

Ground distance from map distance:
    map length x scale denominator = ground length
    4 cm on a 1:25 000 map = 4 cm x 25 000 = 100 000 cm = 1.0 km
```

```mermaid
graph TD
    DATA["Geographic data"] --> SCALE["Choose scale ratio"]
    SCALE --> GEN["Generalize simplify select aggregate"]
    GEN --> SYM["Symbolize visual variables"]
    SYM --> HUE["Hue for categories"]
    SYM --> VALUE["Value ramp for quantities"]
    HUE --> MAP["Readable map"]
    VALUE --> MAP
```

Remember: large scale means small area and fine detail (the fraction is
larger); generalization simplifies to fit the scale; symbolization uses
visual variables - hue for categories, value for quantities - to make the
map legible.
""",
        ),
        quiz_lesson(
            "Quiz: Map scale, generalization and symbolization",
            (
                q(
                    "Which describes a large-scale map such as 1:1,000?",
                    (
                        opt("A large area with little detail, like a continent"),
                        opt(
                            "A small area shown in great detail, like a city block or site plan",
                            correct=True,
                        ),
                        opt("A map with no coordinate system"),
                        opt("A map printed on large paper only"),
                    ),
                    "Large scale = larger representative fraction = small area, high "
                    "detail. Small scale is the opposite.",
                ),
                q(
                    "What is cartographic generalization?",
                    (
                        opt("Guessing coordinates without measuring"),
                        opt(
                            "Simplifying reality - simplifying geometry, selecting, "
                            "aggregating and displacing features - to suit the map scale",
                            correct=True,
                        ),
                        opt("Converting a raster to a vector"),
                        opt("Encrypting the map data"),
                    ),
                    "You cannot show every detail at every scale; generalization "
                    "(for example Douglas-Peucker line simplification) fits data to scale.",
                ),
                q(
                    "How much ground distance is 4 cm on a 1:25,000 map?",
                    (
                        opt("25 metres"),
                        opt("100 metres"),
                        opt("1 kilometre", correct=True),
                        opt("25 kilometres"),
                    ),
                    "4 cm x 25,000 = 100,000 cm = 1,000 m = 1 km.",
                ),
            ),
        ),
        # -- 8. Reprojecting in practice -------------------------------
        _t(
            "Reprojecting data in practice: GDAL and PROJ",
            "11 min",
            """# Reprojecting data in practice: GDAL and PROJ

Theory meets the command line. Under almost every GIS tool sits **PROJ**,
the open-source library that actually does the coordinate math, and
**GDAL/OGR**, which reads and writes raster and vector formats and calls
PROJ to **reproject** them. **Reprojection** (or a **datum
transformation**) converts data from one CRS to another.

Two everyday operations:

- **Assign** a CRS - the data has no CRS tag but you *know* what it is.
  This only labels it; it does not move any coordinates.
- **Reproject/warp** - the data has a known CRS and you want it in a
  different one. This recomputes every coordinate.

Do not confuse them: assigning the wrong CRS mislabels correct data;
reprojecting recomputes it. If a layer is in the wrong place, decide
whether the label is wrong (re-assign) or the numbers need converting
(reproject).

```python
# Vector reprojection with ogr2ogr (GDAL command line)
# WGS84 lat/lon (4326)  ->  UTM zone 31N (32631) for metre measurements
#   ogr2ogr -t_srs EPSG:32631 out_utm.gpkg in_wgs84.geojson

# Raster warp with gdalwarp: reproject a GeoTIFF to Web Mercator for tiling
#   gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3857 dem.tif dem_3857.tif

# In Python with pyproj + GeoPandas
import geopandas as gpd
gdf = gpd.read_file("in_wgs84.geojson")   # CRS read from the file
gdf_utm = gdf.to_crs(epsg=32631)          # reproject to UTM 31N (metres)
print(gdf.crs, "->", gdf_utm.crs)

# Reproject a single point with pyproj directly
from pyproj import Transformer
tr = Transformer.from_crs("EPSG:4326", "EPSG:32631", always_xy=True)
easting, northing = tr.transform(2.2945, 48.8584)   # lon, lat  (always_xy)
```

**Watch out for axis order.** EPSG:4326 officially lists latitude first,
but most software and GeoJSON use longitude, latitude. Libraries expose an
`always_xy=True` flag to force lon/lat and avoid swapped-coordinate bugs.

```mermaid
graph LR
    SRC["Source data with CRS 4326"] --> GDAL["GDAL or OGR reads it"]
    GDAL --> PROJ["PROJ computes transform"]
    PROJ --> WARP["Reproject each coordinate"]
    WARP --> OUT["Output in target CRS 32631"]
    OUT --> ANALYZE["Overlay and measure in metres"]
```

Remember: PROJ does the math and GDAL/OGR moves the data; **assign** only
labels a CRS while **reproject** recomputes coordinates; and always mind
axis order (use always_xy) so lon/lat never get swapped.
""",
        ),
        quiz_lesson(
            "Quiz: Reprojecting data in practice: GDAL and PROJ",
            (
                q(
                    "What is the role of the PROJ library under GDAL, QGIS and PostGIS?",
                    (
                        opt("It stores the map images"),
                        opt(
                            "It performs the coordinate math - the projection and "
                            "datum transformations - that reprojection needs",
                            correct=True,
                        ),
                        opt("It draws the map legend"),
                        opt("It downloads satellite data"),
                    ),
                    "PROJ is the shared engine that converts coordinates between CRS; "
                    "GDAL/OGR call it to warp data.",
                ),
                q(
                    "What is the difference between assigning a CRS and reprojecting?",
                    (
                        opt("They are identical operations"),
                        opt(
                            "Assigning only labels the data with a CRS without moving "
                            "coordinates; reprojecting recomputes every coordinate into "
                            "a new CRS",
                            correct=True,
                        ),
                        opt("Assigning deletes the data; reprojecting saves it"),
                        opt("Reprojecting only changes the file name"),
                    ),
                    "Assign fixes a wrong or missing label; reproject converts correctly "
                    "labelled data into another CRS.",
                ),
                q(
                    "Why do libraries offer an always_xy=True option when transforming "
                    "coordinates?",
                    (
                        opt("To make transforms run faster"),
                        opt(
                            "Because EPSG:4326 officially lists latitude first while "
                            "most software uses longitude, latitude - always_xy forces "
                            "lon/lat and prevents swapped-coordinate bugs",
                            correct=True,
                        ),
                        opt("To convert metres into degrees automatically"),
                        opt("To pick the map colours"),
                    ),
                    "Axis-order confusion is a classic bug; always_xy pins the order to lon, lat.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What are latitude and longitude?",
                    (
                        opt("Distances in metres from the equator"),
                        opt(
                            "Angles on an ellipsoid - north/south of the equator and "
                            "east/west of the prime meridian - fixed by a datum",
                            correct=True,
                        ),
                        opt("Image pixel coordinates"),
                        opt("Elevation and depth"),
                    ),
                    "Geographic coordinates are angles; they need a datum (usually "
                    "WGS84) to be unambiguous.",
                ),
                q(
                    "Why is a perfectly accurate flat map impossible?",
                    (
                        opt("Because paper is too small"),
                        opt(
                            "A curved surface cannot be flattened without distorting "
                            "area, shape, distance or direction",
                            correct=True,
                        ),
                        opt("Because coordinates are secret"),
                        opt("Because screens are rectangular"),
                    ),
                    "Flattening a sphere always distorts something; you choose which "
                    "property to protect.",
                ),
                q(
                    "A single projection can preserve at most which pair-mate?",
                    (
                        opt("Both area and shape everywhere"),
                        opt(
                            "Area (equal-area) OR shape (conformal), never both",
                            correct=True,
                        ),
                        opt("Every property with enough resolution"),
                        opt("Only colour accuracy"),
                    ),
                    "Equal-area and conformal are mutually exclusive; pick per task.",
                ),
                q(
                    "Match the projection family to its best use.",
                    (
                        opt("Azimuthal for the tropics"),
                        opt(
                            "Cylindrical for world/tropics, conic for mid-latitude "
                            "regions, azimuthal for the poles",
                            correct=True,
                        ),
                        opt("Conic for the poles"),
                        opt("Cylindrical for a single point"),
                    ),
                    "Cylinder-equator, cone-midlatitudes, plane-poles: match the "
                    "faithful zone to your data.",
                ),
                q(
                    "Why should you never use plain Mercator to compare the sizes of countries?",
                    (
                        opt("It has too few colours"),
                        opt(
                            "Mercator is conformal and massively exaggerates area toward the poles",
                            correct=True,
                        ),
                        opt("It only shows the oceans"),
                        opt("It cannot show large countries"),
                    ),
                    "Mercator preserves angles, not area; Greenland looks far larger than it is.",
                ),
                q(
                    "What does the UTM system do and what is its main limitation?",
                    (
                        opt("One global projection with no limits"),
                        opt(
                            "60 zones of 6 degrees each give low-distortion metre "
                            "coordinates, but a coordinate is valid only within its zone",
                            correct=True,
                        ),
                        opt("It only works at the equator"),
                        opt("It measures in degrees, not metres"),
                    ),
                    "UTM trades global coverage for local accuracy; each zone has its "
                    "own EPSG code.",
                ),
                q(
                    "On an equal-area projection, what does Tissot's indicatrix do?",
                    (
                        opt("Stays a circle of constant size"),
                        opt(
                            "Becomes an ellipse whose area is the same everywhere, "
                            "though its shape changes",
                            correct=True,
                        ),
                        opt("Vanishes"),
                        opt("Turns into a straight line"),
                    ),
                    "Equal-area keeps area (h*k = 1); the indicatrix is an ellipse of "
                    "constant area, distorted in shape.",
                ),
                q(
                    "What does the EPSG code 4326 identify, and 3857?",
                    (
                        opt("4326 is Web Mercator, 3857 is WGS84 lat/lon"),
                        opt(
                            "4326 is WGS84 geographic lat/lon; 3857 is Web Mercator "
                            "used by web map tiles",
                            correct=True,
                        ),
                        opt("Both are UTM zones"),
                        opt("Both are the British National Grid"),
                    ),
                    "4326 = WGS84 degrees; 3857 = Web Mercator metres for slippy maps.",
                ),
                q(
                    "You have data in EPSG:4326 and need to measure areas in metres. "
                    "What should you do?",
                    (
                        opt("Measure directly in degrees"),
                        opt(
                            "Reproject the data into a suitable projected CRS such as "
                            "the local UTM zone before measuring",
                            correct=True,
                        ),
                        opt("Assign it EPSG:3857 and measure area there"),
                        opt("Nothing - degrees are metres"),
                    ),
                    "Degrees are not metres and Web Mercator distorts area; reproject "
                    "to a local projected CRS (UTM) to measure.",
                ),
                q(
                    "In GDAL/PROJ workflows, what is the difference between assigning a "
                    "CRS and reprojecting?",
                    (
                        opt("They are the same command"),
                        opt(
                            "Assigning only labels the data without moving coordinates; "
                            "reprojecting recomputes coordinates into a new CRS",
                            correct=True,
                        ),
                        opt("Assigning always corrupts the file"),
                        opt("Reprojecting only renames the layer"),
                    ),
                    "Assign labels; reproject (ogr2ogr -t_srs, gdalwarp, to_crs) "
                    "recomputes - mind axis order with always_xy.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

CARTOGRAPHY_PROJECTIONS_COURSES: tuple[SeedCourse, ...] = (_CARTOGRAPHY_PROJECTIONS,)
