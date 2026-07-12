"""Academy seed content - Introduction to Geospatial Engineering.

An orientation to geospatial engineering: what it is and the disciplines it
combines, the data ecosystem (satellites, drones, GNSS, sensors), the
platforms and market (Google Earth, ArcGIS, QGIS, Cesium, Planet, Maxar),
coordinate systems and the shape of the Earth, the data lifecycle from
acquisition to decision, vector and raster data models, open standards
(OGC, STAC, GeoTIFF), and the modern GeoAI-driven, cloud-native profession.
Every lesson is a direct explanation with a concrete example and a mermaid
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


_INTRO_GEOSPATIAL_ENGINEERING = SeedCourse(
    slug="intro-geospatial-engineering",
    title="Introduction to Geospatial Engineering",
    description=(
        "An orientation to geospatial engineering: what it is, the platforms "
        "it builds (Google Earth, ArcGIS, QGIS, Cesium, Planet), the data "
        "sources (satellites, drones, GNSS), coordinate systems and open "
        "standards (OGC, STAC, GeoTIFF), and the modern GeoAI-driven, "
        "cloud-native industry - with real examples and a diagram in every "
        "lesson."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Introduction to Geospatial Engineering

Geospatial engineering is the practice of capturing, modeling, and
reasoning about **where things are on the Earth** - and turning that into
maps, analysis, and decisions. It powers navigation apps, precision
agriculture, disaster response, climate monitoring, and the digital twins
of entire cities. This course gives you the whole picture before you go
deep on any single tool or technique.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short real example (a coordinate formula, a GDAL
snippet, a STAC fragment, a data table), and draws the idea as a diagram.
After each lesson there is a short quiz; at the end, a final quiz covers
the whole course.

What you will build understanding for, in order:

1. **What geospatial engineering is** - the disciplines it combines
2. **The data ecosystem** - satellites, drones, GNSS, and sensors
3. **Platforms and the market** - Google Earth, ArcGIS, QGIS, Cesium, Planet, Maxar
4. **Coordinates and the shape of the Earth** - a first look
5. **The data lifecycle** - from acquisition to decision
6. **Vector and raster** - the two core data models
7. **Open standards** - OGC, STAC, and GeoTIFF for interoperability
8. **The modern geospatial engineer** - GeoAI, cloud, and digital twins

This is the map. Knowing where each idea fits makes the deeper courses in
the track far easier to learn.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is geospatial engineering, fundamentally?",
                    (
                        opt("A single mapping app you install on a phone"),
                        opt("A job title for someone who only draws paper maps"),
                        opt(
                            "The practice of capturing, modeling and reasoning about "
                            "where things are on Earth, and turning that into maps, "
                            "analysis and decisions",
                            correct=True,
                        ),
                        opt("A programming language for automation"),
                    ),
                    "It is about location data end to end - capture, model, analyze, "
                    "decide - not any single product.",
                ),
                q(
                    "How is each content lesson in this course structured?",
                    (
                        opt("A long video with no text"),
                        opt(
                            "A direct explanation, a concrete example, and a mermaid "
                            "diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("A single unrelated code file"),
                    ),
                    "Explain, show an example, draw the diagram, then check knowledge.",
                ),
            ),
        ),
        # -- 1. What is geospatial engineering -------------------------
        _t(
            "What is geospatial engineering",
            "9 min",
            """# What is geospatial engineering

**Geospatial engineering** is a blend of several older disciplines, all
concerned with the same question: **where is something, and what does that
location tell us?** No single field owns it - the strength is in the
combination.

The disciplines it draws on:

- **Geodesy** - the science of the Earth's exact size and shape, and the
  reference frames we measure position against.
- **Surveying** - measuring precise positions and boundaries on the ground.
- **Cartography** - the design of maps: projection, symbology, and how to
  communicate spatial information clearly.
- **Remote sensing** - observing the Earth from a distance using satellites,
  aircraft, and drones.
- **Geographic Information Systems (GIS)** - software to store, query, and
  analyze spatial data.
- **Photogrammetry** - deriving measurements and 3D models from overlapping
  images.
- **Software and data engineering** - the pipelines, databases, and cloud
  that make all of it scale.

A useful way to think about the output: geospatial work almost always
answers one of a few questions - **where** something is, **what** is at a
place, **how** places relate, and **how they change** over time.

```mermaid
graph TD
    GEO["Geospatial engineering"] --> GD["Geodesy the Earth shape"]
    GEO --> SV["Surveying ground positions"]
    GEO --> RS["Remote sensing from a distance"]
    GEO --> GIS["GIS store query analyze"]
    GEO --> CT["Cartography map design"]
    GEO --> SW["Software and data engineering"]
```

A tiny example of the core idea - a place is a location plus attributes:

```json
{
  "type": "Feature",
  "geometry": { "type": "Point", "coordinates": [-122.4194, 37.7749] },
  "properties": { "name": "San Francisco", "population": 815000 }
}
```

Remember: geospatial engineering is not one skill - it is the disciplined
combination of measuring, observing, modeling, and analyzing location.
""",
        ),
        quiz_lesson(
            "Quiz: What is geospatial engineering",
            (
                q(
                    "Which best describes geospatial engineering?",
                    (
                        opt("A single discipline about drawing maps by hand"),
                        opt(
                            "A blend of geodesy, surveying, remote sensing, cartography, "
                            "GIS and software engineering, all focused on location",
                            correct=True,
                        ),
                        opt("Only the study of satellites"),
                        opt("A branch of accounting"),
                    ),
                    "Its strength is the combination of several location-focused fields.",
                ),
                q(
                    "What does geodesy study?",
                    (
                        opt("The design of map symbols and colors"),
                        opt("The programming of GIS software"),
                        opt(
                            "The Earth's exact size and shape and the reference frames "
                            "we measure position against",
                            correct=True,
                        ),
                        opt("The marketing of mapping products"),
                    ),
                    "Geodesy underpins every coordinate: it defines what we measure "
                    "position relative to.",
                ),
                q(
                    "In the GeoJSON example, what makes a 'feature' more than just a point?",
                    (
                        opt("It has a color"),
                        opt(
                            "It pairs a geometry (the location) with properties "
                            "(attributes like name and population)",
                            correct=True,
                        ),
                        opt("It must be a satellite image"),
                        opt("It has to be three-dimensional"),
                    ),
                    "A place is a location plus what is true at that location.",
                ),
            ),
        ),
        # -- 2. The geospatial data ecosystem --------------------------
        _t(
            "The geospatial data ecosystem",
            "10 min",
            """# The geospatial data ecosystem

Geospatial data comes from many sensors, each with a different trade-off
between **coverage**, **resolution**, and **update frequency**. Knowing
the sources is half of choosing the right data for a job.

The main sources:

- **Satellites** - observe the whole planet repeatedly. Public missions
  like **Landsat** (NASA/USGS, 30 m, ~16-day revisit) and **Sentinel**
  (ESA Copernicus, 10-20 m, ~5-day revisit) provide free imagery;
  commercial providers like **Planet** and **Maxar** offer daily or
  sub-meter imagery.
- **Aircraft and drones (UAVs)** - fly low for very high resolution over a
  small area, on demand. Ideal for surveying a construction site or a
  field down to centimeters.
- **GNSS receivers** - Global Navigation Satellite Systems (GPS, Galileo,
  GLONASS, BeiDou) give a device its own position on the Earth.
- **LiDAR** - laser scanners (airborne or terrestrial) that measure
  distance directly, producing dense 3D **point clouds**.
- **Ground and IoT sensors** - weather stations, traffic sensors, phones -
  huge volumes of location-tagged measurements.

A rough comparison of imaging sources:

```text
Source        Resolution     Coverage        Revisit
Landsat 8/9   30 m           global          ~16 days
Sentinel-2    10-20 m        global          ~5 days
Planet Dove   ~3 m           global          daily
Maxar         ~0.3 m         tasked          on demand
Drone         1-5 cm         small area      on demand
```

```mermaid
graph TD
    SAT["Satellites global repeat"] --> DATA["Geospatial data"]
    DRONE["Drones high resolution local"] --> DATA
    GNSS["GNSS device position"] --> DATA
    LIDAR["LiDAR 3D point clouds"] --> DATA
    IOT["Ground and IoT sensors"] --> DATA
    DATA --> USE["Analysis and decisions"]
```

The trade-off to internalize: **you rarely get high resolution, wide
coverage, and frequent updates all at once** - you pick the sources that
match the question, and often combine them.
""",
        ),
        quiz_lesson(
            "Quiz: The geospatial data ecosystem",
            (
                q(
                    "What do GNSS receivers (GPS, Galileo, GLONASS, BeiDou) provide?",
                    (
                        opt("High-resolution color imagery"),
                        opt("A 3D laser scan of a building"),
                        opt(
                            "A device's own position on the Earth",
                            correct=True,
                        ),
                        opt("Weather forecasts"),
                    ),
                    "GNSS is about positioning - telling a receiver where it is.",
                ),
                q(
                    "You need centimeter-level detail over a single construction site, on "
                    "demand. Which source fits best?",
                    (
                        opt("A 30 m Landsat scene"),
                        opt("A drone (UAV) survey", correct=True),
                        opt("A global weather satellite"),
                        opt("A GNSS receiver alone"),
                    ),
                    "Drones fly low for very high resolution over small areas on demand.",
                ),
                q(
                    "What key trade-off shapes the choice of geospatial data source?",
                    (
                        opt("Color versus black and white only"),
                        opt(
                            "You rarely get high resolution, wide coverage and frequent "
                            "updates all at once - you match sources to the question",
                            correct=True,
                        ),
                        opt("All sources are identical, so it never matters"),
                        opt("Only price matters, never resolution"),
                    ),
                    "Resolution, coverage and revisit trade off against each other.",
                ),
            ),
        ),
        # -- 3. Platforms and the market -------------------------------
        _t(
            "Platforms and the market",
            "10 min",
            """# Platforms and the market

The geospatial industry is a mix of **consumer maps**, **professional GIS
software**, **imagery providers**, and **cloud analysis platforms**.
Knowing who does what helps you place any tool you meet.

Consumer and 3D visualization:

- **Google Earth / Google Maps** - the platforms that put a browsable
  globe and Street View in front of billions of people, and popularized
  the idea of a searchable digital Earth.
- **Cesium** - open-source 3D globe and map engine for the web, built on
  the **3D Tiles** standard for streaming massive terrain and city models
  (a foundation for digital twins).

Professional GIS software:

- **ArcGIS** (Esri) - the dominant commercial GIS platform: desktop, server,
  and the ArcGIS Online cloud. Deep analysis, cartography, and enterprise
  integration.
- **QGIS** - the leading **free and open-source** desktop GIS. Feature-rich,
  extensible with Python plugins, and widely used in government and
  academia.

Imagery and data providers:

- **Planet** - operates the largest fleet of small satellites, imaging the
  entire landmass daily.
- **Maxar** - very high resolution (sub-meter) commercial imagery, often
  used for detailed mapping and defense.
- **Copernicus / Sentinel** (ESA) and **Landsat** (NASA/USGS) - free,
  open, government satellite programs.

Cloud analysis platforms:

- **Google Earth Engine** - petabytes of satellite imagery plus planetary
  scale compute, analyzed in the cloud without downloading data.
- **Microsoft Planetary Computer**, AWS, and others host open geospatial
  data next to compute.

```mermaid
graph TD
    MKT["Geospatial market"] --> CON["Consumer and 3D Google Earth Cesium"]
    MKT --> GIS["Professional GIS ArcGIS and QGIS"]
    MKT --> IMG["Imagery Planet Maxar Sentinel Landsat"]
    MKT --> CLOUD["Cloud platforms Earth Engine"]
```

A quick who-does-what table:

```text
Category        Examples                    Role
Consumer 3D     Google Earth, Cesium        browse and visualize
GIS software    ArcGIS, QGIS                analyze and map
Imagery         Planet, Maxar, Sentinel     supply the pixels
Cloud compute   Earth Engine, Planetary     analyze at scale
```

Remember: consumer maps made geospatial data mainstream; GIS software is
where analysis happens; imagery providers supply the raw pixels; and cloud
platforms increasingly bring the compute to the data.
""",
        ),
        quiz_lesson(
            "Quiz: Platforms and the market",
            (
                q(
                    "Which is the leading free and open-source desktop GIS?",
                    (
                        opt("ArcGIS"),
                        opt("QGIS", correct=True),
                        opt("Google Earth"),
                        opt("Maxar"),
                    ),
                    "QGIS is the open-source desktop GIS; ArcGIS is the dominant commercial one.",
                ),
                q(
                    "What is Cesium best known for?",
                    (
                        opt("Selling sub-meter satellite imagery"),
                        opt(
                            "An open-source 3D globe engine that streams massive terrain "
                            "and city models via the 3D Tiles standard",
                            correct=True,
                        ),
                        opt("A GNSS receiver brand"),
                        opt("A weather forecasting service"),
                    ),
                    "Cesium plus 3D Tiles is a common foundation for web 3D and digital twins.",
                ),
                q(
                    "What does Google Earth Engine let you do?",
                    (
                        opt("Only view Street View panoramas"),
                        opt(
                            "Analyze petabytes of satellite imagery with cloud compute, "
                            "without downloading the data",
                            correct=True,
                        ),
                        opt("Fly drones remotely"),
                        opt("Replace all GIS desktop software for cartography"),
                    ),
                    "Earth Engine brings planetary-scale compute to the imagery archive.",
                ),
            ),
        ),
        # -- 4. Coordinates, maps and the shape of the Earth -----------
        _t(
            "Coordinates, maps and the shape of the Earth",
            "11 min",
            """# Coordinates, maps and the shape of the Earth

To say *where* something is, you need a **coordinate reference system
(CRS)** - and that starts with the shape of the Earth. The Earth is not a
sphere; it bulges at the equator. We model it in layers:

- **Ellipsoid** - a smooth mathematical approximation of the Earth's shape
  (for example the **WGS84** ellipsoid used by GPS).
- **Geoid** - the true, lumpy surface of equal gravity (mean sea level).
  Elevations are usually measured against the geoid.
- **Datum** - ties the ellipsoid to real points on the ground, so
  coordinates line up with reality. WGS84 is the global datum GPS uses.

**Geographic coordinates** are latitude and longitude in degrees on the
ellipsoid. The most common system is **WGS84 / EPSG:4326**:

```text
San Francisco City Hall
  latitude  =  37.7793 deg N
  longitude = -122.4193 deg W
  CRS       = WGS84 (EPSG:4326)
```

Every CRS has an **EPSG code** - a short number that names it exactly.
EPSG:4326 is lat/lon on WGS84.

A globe is round but screens and paper are flat, so we use a **map
projection** to flatten the Earth - and every projection distorts
something (area, shape, distance, or direction). You cannot preserve all
of them at once:

- **Web Mercator (EPSG:3857)** - used by nearly every web map; preserves
  shape and direction but badly inflates area near the poles (Greenland
  looks huge).
- **UTM (Universal Transverse Mercator)** - splits the world into 60 zones,
  each with meter-based coordinates and low distortion. Great for
  measurement and engineering.

```mermaid
graph TD
    EARTH["Real Earth lumpy"] --> GEOID["Geoid mean sea level"]
    EARTH --> ELL["Ellipsoid WGS84"]
    ELL --> DATUM["Datum ties to the ground"]
    DATUM --> GEOG["Geographic lat lon EPSG 4326"]
    GEOG --> PROJ["Projection to a flat map"]
    PROJ --> WM["Web Mercator EPSG 3857"]
    PROJ --> UTM["UTM zones meters"]
```

The one rule to carry forward: **coordinates are meaningless without their
CRS**. Always know whether numbers are degrees or meters, and which datum
and projection they use, before you compare or combine them.
""",
        ),
        quiz_lesson(
            "Quiz: Coordinates, maps and the shape of the Earth",
            (
                q(
                    "What does an EPSG code such as EPSG:4326 identify?",
                    (
                        opt("A satellite model"),
                        opt(
                            "A specific coordinate reference system (here, WGS84 "
                            "latitude and longitude)",
                            correct=True,
                        ),
                        opt("A file format for imagery"),
                        opt("A drone flight plan"),
                    ),
                    "EPSG codes name a CRS exactly; 4326 is lat/lon on WGS84.",
                ),
                q(
                    "Why does every flat map projection distort something?",
                    (
                        opt("Because screens are low resolution"),
                        opt(
                            "You cannot flatten a curved Earth onto a plane without "
                            "distorting area, shape, distance or direction",
                            correct=True,
                        ),
                        opt("Because coordinates are always wrong"),
                        opt("Because GPS is inaccurate"),
                    ),
                    "Flattening a curved surface forces a trade-off; no projection "
                    "preserves everything.",
                ),
                q(
                    "What is a good reason to use UTM instead of Web Mercator?",
                    (
                        opt("UTM works only in the browser"),
                        opt(
                            "UTM gives meter-based coordinates with low distortion, "
                            "which is better for measurement and engineering",
                            correct=True,
                        ),
                        opt("Web Mercator cannot show any map"),
                        opt("UTM has no zones and covers the globe in one piece"),
                    ),
                    "Web Mercator is convenient for web tiles but badly distorts area; "
                    "UTM is meter-accurate per zone.",
                ),
                q(
                    "What does the geoid represent?",
                    (
                        opt("A smooth mathematical ellipsoid"),
                        opt(
                            "The true, lumpy equal-gravity surface (mean sea level) that "
                            "elevations are measured against",
                            correct=True,
                        ),
                        opt("The path of a GPS satellite"),
                        opt("A projection for web maps"),
                    ),
                    "Ellipsoid = smooth model; geoid = real gravity surface for heights.",
                ),
            ),
        ),
        # -- 5. The geospatial data lifecycle --------------------------
        _t(
            "The geospatial data lifecycle",
            "10 min",
            """# The geospatial data lifecycle

Raw pixels and coordinates are not answers. Geospatial work follows a
**lifecycle** that turns observations into decisions - and each stage adds
value (and can add error if skipped).

The stages:

1. **Acquisition** - collect the data (task a satellite, fly a drone, run a
   GNSS survey, pull an open archive).
2. **Pre-processing** - make it usable: **georeferencing** (giving pixels
   real-world coordinates), correcting for atmosphere and terrain,
   removing clouds, and reprojecting to a common CRS.
3. **Storage and management** - organize it in a spatial database
   (**PostGIS**), a file store, or a cloud data cube, with metadata so it
   can be found again.
4. **Analysis** - the actual question: overlay layers, compute indices,
   classify land cover, detect change, run a model.
5. **Visualization** - communicate the result as a map, dashboard, or 3D
   scene.
6. **Decision** - act: route a truck, issue an alert, plan a field, direct
   a response.

A tiny analysis example - a spatial query in **PostGIS** finding every
school within 500 meters of a flood zone:

```sql
SELECT s.name
FROM schools s
JOIN flood_zones f
  ON ST_DWithin(s.geom, f.geom, 500);   -- 500 meters
```

```mermaid
graph LR
    ACQ["Acquisition"] --> PRE["Pre-processing georeference and correct"]
    PRE --> STORE["Storage and management"]
    STORE --> ANALYZE["Analysis"]
    ANALYZE --> VIS["Visualization"]
    VIS --> DECIDE["Decision and action"]
    DECIDE --> ACQ
```

Two ideas make the lifecycle trustworthy: **provenance** (track where each
dataset came from and how it was processed) and **fitness for purpose**
(3 m imagery is fine for regional land cover but useless for property
boundaries). The lifecycle also loops - decisions raise new questions,
which drive the next acquisition.

Remember: value is created by moving data along the lifecycle - and the
answer is only as good as the weakest stage.
""",
        ),
        quiz_lesson(
            "Quiz: The geospatial data lifecycle",
            (
                q(
                    "What is 'georeferencing' in the pre-processing stage?",
                    (
                        opt("Compressing the file to save space"),
                        opt(
                            "Giving pixels or features real-world coordinates so they "
                            "line up with the Earth",
                            correct=True,
                        ),
                        opt("Deleting cloudy images"),
                        opt("Printing the map"),
                    ),
                    "Georeferencing anchors data to a coordinate system so layers align.",
                ),
                q(
                    "Why is 'fitness for purpose' important in the lifecycle?",
                    (
                        opt("All data is equally good for every task"),
                        opt(
                            "Data must match the question - 3 m imagery suits regional "
                            "land cover but not precise property boundaries",
                            correct=True,
                        ),
                        opt("Higher resolution is always required"),
                        opt("It only matters for visualization"),
                    ),
                    "The right resolution and accuracy depend on the decision you are supporting.",
                ),
                q(
                    "In the PostGIS example, what does ST_DWithin(s.geom, f.geom, 500) do?",
                    (
                        opt("Deletes rows within 500 meters"),
                        opt(
                            "Selects features whose geometries are within 500 meters of each other",
                            correct=True,
                        ),
                        opt("Reprojects the data to EPSG:500"),
                        opt("Counts the total number of schools only"),
                    ),
                    "ST_DWithin is a spatial proximity test - here, schools near flood zones.",
                ),
            ),
        ),
        # -- 6. Vector and raster data models --------------------------
        _t(
            "Vector and raster data models",
            "10 min",
            """# Vector and raster data models

Almost all geospatial data is one of two models. Choosing the right one is
a core engineering decision.

**Vector data** represents the world as discrete **geometries** with
attributes:

- **Points** - a well, a tree, a GPS reading.
- **Lines** - a road, a river, a pipeline.
- **Polygons** - a country, a lake, a building footprint.

Vectors are exact and compact for **discrete features** with sharp
boundaries, and they carry rich attributes in a table. Common formats:
**GeoJSON**, **Shapefile**, and **GeoPackage**. A GeoJSON line:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "LineString",
    "coordinates": [[-122.42, 37.77], [-122.41, 37.78]]
  },
  "properties": { "road": "Market St" }
}
```

**Raster data** represents the world as a **grid of cells (pixels)**, each
holding a value: elevation, temperature, or a color band. Rasters are
ideal for **continuous phenomena** that vary everywhere - imagery,
terrain, rainfall. A satellite scene is a raster with multiple **bands**
(red, green, blue, near-infrared). Common formats: **GeoTIFF** and its
cloud-friendly variant, the Cloud-Optimized GeoTIFF (COG).

A concrete raster operation - the **NDVI** vegetation index, computed per
pixel from the near-infrared and red bands:

```text
NDVI = (NIR - RED) / (NIR + RED)
   value near +1  -> dense healthy vegetation
   value near  0  -> bare soil or built-up
   value below 0  -> water
```

```mermaid
graph TD
    MODEL["Geospatial data models"] --> VEC["Vector features and attributes"]
    MODEL --> RAS["Raster grid of cells"]
    VEC --> PT["Points"]
    VEC --> LN["Lines"]
    VEC --> PG["Polygons"]
    RAS --> IMG["Imagery bands"]
    RAS --> DEM["Elevation and continuous fields"]
```

The rule of thumb: **discrete objects with boundaries -> vector**;
**continuous fields sampled everywhere -> raster**. Real projects mix both -
classify a raster image, then extract vector building footprints from it.
""",
        ),
        quiz_lesson(
            "Quiz: Vector and raster data models",
            (
                q(
                    "Which data is best represented as vector?",
                    (
                        opt("Continuous surface temperature across a region"),
                        opt(
                            "Discrete features with sharp boundaries, like roads, "
                            "buildings and administrative areas",
                            correct=True,
                        ),
                        opt("A satellite image's pixel grid"),
                        opt("Elevation sampled everywhere"),
                    ),
                    "Vector = discrete geometries with attributes; raster = continuous grids.",
                ),
                q(
                    "What is raster data?",
                    (
                        opt("A table of points, lines and polygons"),
                        opt(
                            "A grid of cells (pixels), each holding a value such as "
                            "elevation, temperature or a color band",
                            correct=True,
                        ),
                        opt("A list of EPSG codes"),
                        opt("A 3D city model only"),
                    ),
                    "Rasters suit continuous phenomena; imagery and terrain are rasters.",
                ),
                q(
                    "What does the NDVI index measure, using (NIR - RED) / (NIR + RED)?",
                    (
                        opt("The altitude of a satellite"),
                        opt(
                            "Vegetation health - values near +1 mean dense healthy "
                            "vegetation, near 0 bare soil, below 0 water",
                            correct=True,
                        ),
                        opt("The map projection in use"),
                        opt("The number of vector features"),
                    ),
                    "NDVI is a classic per-pixel raster index combining the near-infrared "
                    "and red bands.",
                ),
            ),
        ),
        # -- 7. Open standards and interoperability --------------------
        _t(
            "Open standards and interoperability",
            "10 min",
            """# Open standards and interoperability

Geospatial data is useless if tools cannot exchange it. **Open standards**,
mostly from the **Open Geospatial Consortium (OGC)**, let ArcGIS, QGIS,
Cesium, and custom code all speak the same language.

Key OGC **web service** standards - ways one server offers data to any
client:

- **WMS (Web Map Service)** - serves rendered map *images* (pictures of a
  map).
- **WMTS** - serves pre-rendered map *tiles* for fast web maps.
- **WFS (Web Feature Service)** - serves the actual *vector features* (the
  geometries and attributes), not just a picture.
- **WCS** - serves raw *raster coverage* data.
- The newer **OGC API** family modernizes these as clean REST/JSON APIs.

Key **file formats and encodings**:

- **GeoTIFF** - a TIFF image with embedded georeferencing (CRS and extent);
  the workhorse raster format. Its cloud-native form, the
  **Cloud-Optimized GeoTIFF (COG)**, lets a client read just the part of a
  huge file it needs over HTTP.
- **GeoJSON**, **GeoPackage**, **Shapefile** - vector encodings.

**STAC (SpatioTemporal Asset Catalog)** is a fast-growing standard for
*describing and finding* imagery. It is a simple JSON model that makes
petabytes of satellite data searchable by location and time:

```json
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "S2A_20240115_T10SEG",
  "properties": {
    "datetime": "2024-01-15T18:45:00Z",
    "eo:cloud_cover": 4.2
  },
  "assets": {
    "red":  { "href": "https://.../B04.tif", "type": "image/tiff" },
    "nir":  { "href": "https://.../B08.tif", "type": "image/tiff" }
  }
}
```

```mermaid
graph TD
    STD["Open standards OGC and STAC"] --> SVC["Web services"]
    STD --> FMT["Formats"]
    STD --> CAT["Catalogs"]
    SVC --> WMS["WMS map images"]
    SVC --> WFS["WFS vector features"]
    FMT --> GTIFF["GeoTIFF and COG"]
    CAT --> STAC["STAC find imagery by time and place"]
```

Remember: standards are what make a geospatial *ecosystem* possible - WMS
and WFS to serve data, GeoTIFF and GeoJSON to store it, and STAC to find
it, all without locking you into one vendor.
""",
        ),
        quiz_lesson(
            "Quiz: Open standards and interoperability",
            (
                q(
                    "What is the difference between OGC WMS and WFS?",
                    (
                        opt("They are identical"),
                        opt(
                            "WMS serves rendered map images (pictures); WFS serves the "
                            "actual vector features with geometry and attributes",
                            correct=True,
                        ),
                        opt("WMS is for vectors and WFS is for images"),
                        opt("Both only serve 3D models"),
                    ),
                    "WMS gives you a picture of the map; WFS gives you the data behind it.",
                ),
                q(
                    "What does a Cloud-Optimized GeoTIFF (COG) enable?",
                    (
                        opt("Storing only vector points"),
                        opt(
                            "Reading just the needed portion of a huge raster over HTTP, "
                            "without downloading the whole file",
                            correct=True,
                        ),
                        opt("Removing all georeferencing"),
                        opt("Encrypting the imagery"),
                    ),
                    "COG is the cloud-native form of GeoTIFF built for partial HTTP reads.",
                ),
                q(
                    "What problem does STAC solve?",
                    (
                        opt("Rendering 3D city models"),
                        opt(
                            "Describing and finding imagery - a simple JSON model that "
                            "makes satellite archives searchable by location and time",
                            correct=True,
                        ),
                        opt("Compressing GeoJSON files"),
                        opt("Flying drones autonomously"),
                    ),
                    "STAC is a catalog standard: it makes petabytes of imagery discoverable.",
                ),
            ),
        ),
        # -- 8. The modern geospatial engineer -------------------------
        _t(
            "The modern geospatial engineer",
            "11 min",
            """# The modern geospatial engineer

The field has shifted from desktop maps to a **cloud-native, AI-driven**
discipline. The modern geospatial engineer combines classic GIS knowledge
with data engineering and machine learning.

Three forces defining the modern practice:

**1. GeoAI - machine learning on spatial data.** Deep learning now does at
scale what once needed manual interpretation:

- **Semantic segmentation** - label every pixel (building, road, water,
  crop) using convolutional neural networks (CNNs) and, increasingly,
  **vision transformers**.
- **Object detection** - find and count cars, ships, or solar panels in
  imagery.
- **Change detection** - compare imagery over time to spot new
  construction, deforestation, or flood extent.
- **Geospatial foundation models** - large models (such as Prithvi and
  Clay) pre-trained on huge satellite archives, then fine-tuned for a task
  with far less labeled data.

**2. Cloud and scale.** Data is too big to download. Platforms like
**Google Earth Engine** and the **Microsoft Planetary Computer** bring the
compute to the data, with STAC catalogs and COGs making planetary-scale
analysis routine. **MLOps** practices keep satellite model pipelines
reproducible and monitored.

**3. Digital twins.** Living 3D models of cities, factories, and
infrastructure - built on standards like **3D Tiles** and streamed with
**Cesium** - fuse live sensor data with geospatial models for simulation
and planning.

A minimal, modern GeoAI-flavored snippet - open imagery and run an
inference model per tile:

```python
import rasterio
import numpy as np

with rasterio.open("scene_cog.tif") as src:
    red = src.read(3).astype("float32")
    nir = src.read(4).astype("float32")

ndvi = (nir - red) / (nir + red + 1e-6)   # per-pixel index
mask = model.predict(ndvi)                # a trained segmentation model
```

```mermaid
graph TD
    ENG["Modern geospatial engineer"] --> AI["GeoAI segmentation and change detection"]
    ENG --> CLOUD["Cloud scale Earth Engine and STAC"]
    ENG --> TWIN["Digital twins 3D Tiles and Cesium"]
    AI --> FM["Geospatial foundation models"]
    CLOUD --> MLOPS["MLOps for satellite pipelines"]
    TWIN --> DECISION["Simulation and planning"]
```

Remember: the modern engineer still needs the fundamentals - coordinates,
data models, standards - but applies them with machine learning, cloud
compute, and 3D digital twins to answer questions at a scale that was
impossible a decade ago.
""",
        ),
        quiz_lesson(
            "Quiz: The modern geospatial engineer",
            (
                q(
                    "What is 'semantic segmentation' in GeoAI?",
                    (
                        opt("Compressing a GeoTIFF"),
                        opt(
                            "Labeling every pixel of imagery (building, road, water, "
                            "crop) with a neural network",
                            correct=True,
                        ),
                        opt("Choosing a map projection"),
                        opt("Serving map tiles over WMTS"),
                    ),
                    "Segmentation classifies imagery pixel by pixel, typically with CNNs "
                    "or vision transformers.",
                ),
                q(
                    "Why are geospatial foundation models (such as Prithvi or Clay) useful?",
                    (
                        opt("They remove the need for any coordinates"),
                        opt(
                            "Pre-trained on huge satellite archives, they can be "
                            "fine-tuned for a task with far less labeled data",
                            correct=True,
                        ),
                        opt("They only work on vector data"),
                        opt("They replace the need for cloud compute"),
                    ),
                    "Foundation models transfer general learning, reducing the labeled "
                    "data a specific task needs.",
                ),
                q(
                    "What is a digital twin in the geospatial context?",
                    (
                        opt("A backup copy of a shapefile"),
                        opt(
                            "A living 3D model of a city or asset that fuses geospatial "
                            "models with live sensor data for simulation and planning",
                            correct=True,
                        ),
                        opt("A second GPS satellite"),
                        opt("A duplicate map projection"),
                    ),
                    "Digital twins, streamed via 3D Tiles and Cesium, combine models "
                    "with live data.",
                ),
                q(
                    "Why do modern platforms bring compute to the data (Earth Engine, "
                    "Planetary Computer)?",
                    (
                        opt("To make maps prettier"),
                        opt(
                            "Satellite archives are too big to download, so analysis "
                            "runs in the cloud next to the data",
                            correct=True,
                        ),
                        opt("Because desktop GIS is illegal"),
                        opt("To avoid using any standards"),
                    ),
                    "Petabyte-scale imagery makes downloading impractical; the compute "
                    "goes to the data.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is geospatial engineering?",
                    (
                        opt("A single mapping app"),
                        opt(
                            "The disciplined combination of measuring, observing, "
                            "modeling and analyzing location to turn where-questions into "
                            "maps, analysis and decisions",
                            correct=True,
                        ),
                        opt("Only the study of GPS satellites"),
                        opt("A cloud billing service"),
                    ),
                    "It blends geodesy, surveying, remote sensing, GIS and software "
                    "around location.",
                ),
                q(
                    "Which source gives a device its own position on Earth?",
                    (
                        opt("A GeoTIFF file"),
                        opt("GNSS (GPS, Galileo, GLONASS, BeiDou)", correct=True),
                        opt("A WMS server"),
                        opt("A digital twin"),
                    ),
                    "GNSS is about positioning the receiver itself.",
                ),
                q(
                    "Which is the leading free and open-source desktop GIS?",
                    (
                        opt("ArcGIS"),
                        opt("QGIS", correct=True),
                        opt("Cesium"),
                        opt("Planet"),
                    ),
                    "QGIS is open-source; ArcGIS is the dominant commercial GIS.",
                ),
                q(
                    "Coordinates are meaningless without which piece of information?",
                    (
                        opt("The file size"),
                        opt(
                            "Their coordinate reference system (CRS) - the datum, units "
                            "and projection, named by an EPSG code",
                            correct=True,
                        ),
                        opt("The color of the map"),
                        opt("The name of the drone pilot"),
                    ),
                    "Always know whether numbers are degrees or meters and which CRS "
                    "they use before combining them.",
                ),
                q(
                    "What does EPSG:4326 refer to?",
                    (
                        opt("Web Mercator tiles"),
                        opt("WGS84 latitude and longitude", correct=True),
                        opt("A UTM zone in meters"),
                        opt("A satellite mission"),
                    ),
                    "EPSG:4326 is geographic lat/lon on the WGS84 datum.",
                ),
                q(
                    "When should you choose the vector data model over raster?",
                    (
                        opt("For continuous fields like temperature"),
                        opt(
                            "For discrete features with sharp boundaries, such as roads, "
                            "buildings and parcels",
                            correct=True,
                        ),
                        opt("For every satellite image"),
                        opt("Never - raster always wins"),
                    ),
                    "Discrete objects -> vector; continuous fields sampled everywhere -> raster.",
                ),
                q(
                    "What does STAC (SpatioTemporal Asset Catalog) standardize?",
                    (
                        opt("The design of map legends"),
                        opt(
                            "Describing and finding imagery, making satellite archives "
                            "searchable by location and time",
                            correct=True,
                        ),
                        opt("The wiring of GNSS receivers"),
                        opt("The pixels inside a GeoTIFF"),
                    ),
                    "STAC is a JSON catalog standard for discovering imagery.",
                ),
                q(
                    "What is the difference between OGC WMS and WFS?",
                    (
                        opt("Nothing"),
                        opt(
                            "WMS serves rendered map images; WFS serves the actual vector "
                            "features with geometry and attributes",
                            correct=True,
                        ),
                        opt("WMS is a file format, WFS is a satellite"),
                        opt("Both serve only 3D tiles"),
                    ),
                    "WMS = a picture of the map; WFS = the underlying vector data.",
                ),
                q(
                    "What is the NDVI index used for?",
                    (
                        opt(
                            "Measuring vegetation health per pixel from the NIR and red bands",
                            correct=True,
                        ),
                        opt("Naming coordinate systems"),
                        opt("Compressing vector files"),
                        opt("Scheduling drone flights"),
                    ),
                    "NDVI = (NIR - RED) / (NIR + RED); high values indicate dense healthy "
                    "vegetation.",
                ),
                q(
                    "What defines the modern, GeoAI-era geospatial engineer?",
                    (
                        opt("Only drawing paper maps by hand"),
                        opt(
                            "Applying the fundamentals with machine learning, cloud-scale "
                            "compute and 3D digital twins - segmentation, change "
                            "detection, foundation models, and STAC-driven pipelines",
                            correct=True,
                        ),
                        opt("Avoiding all standards and cloud tools"),
                        opt("Working only offline on a single laptop"),
                    ),
                    "Fundamentals still matter, but they are now applied with GeoAI, "
                    "cloud compute and digital twins at planetary scale.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

INTRO_GEOSPATIAL_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_INTRO_GEOSPATIAL_ENGINEERING,)
