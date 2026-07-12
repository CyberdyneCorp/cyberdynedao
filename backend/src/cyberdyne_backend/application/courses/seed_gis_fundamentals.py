"""Academy seed content - GIS Fundamentals.

The core of Geographic Information Systems: how the world is modelled as
vector and raster data, the software and formats that make up the
geospatial stack (QGIS, ArcGIS, GDAL, PostGIS), and the spatial analysis
that turns geometry into answers - buffers, clip, dissolve and spatial
joins, overlay and map algebra, raster reclassify, zonal statistics and
terrain, and finally scripting whole geoprocessing workflows with Python
and geopandas. Every lesson is a direct explanation with a concrete
geopandas, SQL or coordinate example and a mermaid diagram, followed by a
checkpoint quiz; the course closes with a comprehensive final quiz.
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


_GIS_FUNDAMENTALS = SeedCourse(
    slug="gis-fundamentals",
    title="GIS Fundamentals",
    description=(
        "The core of Geographic Information Systems - vector and raster data, "
        "spatial analysis and geoprocessing (buffers, overlay, spatial joins, "
        "raster algebra) in QGIS, ArcGIS and Python. Every lesson pairs a "
        "direct explanation with a geopandas, PostGIS or coordinate example "
        "and a diagram."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# GIS Fundamentals

A **Geographic Information System (GIS)** stores, analyses and maps data
that has a location on Earth. The power of GIS is not just drawing maps -
it is *asking spatial questions*: what is near what, what overlaps what,
how much of X falls inside Y. This course gives you the core concepts and
the analysis toolbox that every GIS professional relies on.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short real example (a geopandas snippet, a PostGIS
query, or a coordinate formula), and draws the idea as a diagram. After
each lesson there is a short quiz; at the end, a final quiz covers the
whole course.

What you will build understanding for, in order:

1. **Vector data** - points, lines, polygons and their attributes
2. **Raster data** - grids, bands and resolution
3. **The geospatial stack** - QGIS, ArcGIS, GDAL and the formats
4. **Spatial relationships** - topology, intersects, contains, DE-9IM
5. **Vector geoprocessing** - buffer, clip, dissolve, spatial join
6. **Overlay and map algebra** - combining layers
7. **Raster analysis** - reclassify, zonal statistics, terrain
8. **Workflows and automation** - scripting with Python and geopandas

This is the map. The two data models (vector and raster) and the analysis
operations built on them are the vocabulary of every GIS task, from an
ArcGIS Pro toolbox to a Python pipeline.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What fundamentally distinguishes GIS data from ordinary data?",
                    (
                        opt("It is always stored as images"),
                        opt("It can only be opened in ArcGIS"),
                        opt(
                            "Every record has a location on Earth, so you can ask "
                            "spatial questions like what is near or inside what",
                            correct=True,
                        ),
                        opt("It never has attributes attached"),
                    ),
                    "GIS ties data to geography, enabling spatial analysis - not just cartography.",
                ),
                q(
                    "What is the teaching approach of this course?",
                    (
                        opt("Pure theory with no examples"),
                        opt(
                            "Each lesson: a direct explanation, a concrete code or "
                            "coordinate example, and a diagram, then a short quiz",
                            correct=True,
                        ),
                        opt("Only video, no reading"),
                        opt("Memorising every EPSG code"),
                    ),
                ),
            ),
        ),
        # -- 1. Vector data model --------------------------------------
        _t(
            "The vector data model",
            "10 min",
            """# The vector data model

The **vector data model** represents the world as discrete **geometries**
built from coordinates. There are three basic geometry types:

- **Point** - a single coordinate pair, e.g. a well, a tree, a bus stop.
- **Line (LineString)** - an ordered list of points, e.g. a road, a river.
- **Polygon** - a closed ring of points bounding an area, e.g. a lake, a
  parcel, a country. Polygons may have holes (inner rings).

Every geometry carries **attributes** - the non-spatial columns that
describe it (a road's name, a parcel's owner, a city's population). A
vector layer is therefore a table where one special column holds geometry
and the rest hold attributes. This is exactly what a **GeoDataFrame** is.

Coordinates only mean something with a **Coordinate Reference System
(CRS)** - the rules mapping numbers to positions on Earth. The most common
is **WGS84 (EPSG:4326)**, longitude and latitude in degrees; projected
systems like **UTM** use metres, which you need for correct distances and
areas.

```python
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

gdf = gpd.GeoDataFrame(
    {"name": ["depot", "route", "zone"]},
    geometry=[
        Point(-46.63, -23.55),                       # lon, lat
        LineString([(-46.63, -23.55), (-46.60, -23.50)]),
        Polygon([(-46.7, -23.6), (-46.5, -23.6), (-46.5, -23.4)]),
    ],
    crs="EPSG:4326",                                 # WGS84 lon/lat
)
print(gdf.geometry.geom_type.tolist())               # Point, LineString, Polygon
```

The common file formats are the **Shapefile** (an older multi-file format,
.shp/.shx/.dbf), **GeoJSON** (text, web-friendly), and **GeoPackage**
(.gpkg, a modern single-file SQLite database - preferred today).

```mermaid
graph TD
    LAYER["Vector layer"] --> GEOM["Geometry column"]
    LAYER --> ATTR["Attribute columns"]
    GEOM --> PT["Point"]
    GEOM --> LN["LineString"]
    GEOM --> PG["Polygon"]
    GEOM --> CRS["Coordinate reference system"]
```

Remember: vector = discrete features (points, lines, polygons) plus their
attributes, all anchored by a CRS. It is ideal for things with sharp
boundaries and identities.
""",
        ),
        quiz_lesson(
            "Quiz: The vector data model",
            (
                q(
                    "What are the three basic vector geometry types?",
                    (
                        opt("Grid, band, pixel"),
                        opt("Point, line, and polygon", correct=True),
                        opt("Raster, vector, and tile"),
                        opt("Row, column, and cell"),
                    ),
                    "Point (one coordinate), line (ordered points), polygon (closed "
                    "ring bounding an area).",
                ),
                q(
                    "In a vector layer, what do the attributes represent?",
                    (
                        opt("The pixel brightness values"),
                        opt(
                            "The non-spatial descriptive columns - name, owner, "
                            "population - attached to each geometry",
                            correct=True,
                        ),
                        opt("The screen colour of the feature"),
                        opt("The file size on disk"),
                    ),
                    "A vector layer is a table: one geometry column plus attribute "
                    "columns describing each feature.",
                ),
                q(
                    "Why does a coordinate pair need a CRS to be meaningful?",
                    (
                        opt("Because files require a header"),
                        opt(
                            "The CRS defines how the numbers map to real positions on "
                            "Earth; without it -46.63, -23.55 is ambiguous",
                            correct=True,
                        ),
                        opt("Because geometry cannot be stored otherwise"),
                        opt("Only rasters need a CRS"),
                    ),
                    "WGS84 (EPSG:4326) is degrees lon/lat; projected systems like UTM "
                    "give metres for correct distance and area.",
                ),
            ),
        ),
        # -- 2. Raster data model --------------------------------------
        _t(
            "The raster data model",
            "10 min",
            """# The raster data model

The **raster data model** represents the world as a **grid of cells
(pixels)**, each holding a value. Instead of discrete features, a raster
covers space *continuously* - ideal for things that vary everywhere:
elevation, temperature, rainfall, satellite reflectance, land cover.

Key properties of a raster:

- **Resolution** - the ground size of one cell. A 10 m Sentinel-2 pixel
  covers a 10 by 10 m patch; smaller cells mean more detail and bigger
  files.
- **Extent** - the bounding box the grid covers.
- **Bands** - a raster can have multiple layers of values for the same
  grid. A photo has red, green, blue bands; satellite imagery adds
  near-infrared and more.
- **NoData** - a special value marking cells with no measurement (e.g. off
  the edge of a scene).
- **Geotransform** - six numbers mapping a (row, column) cell to a
  real-world coordinate: origin plus cell size.

The dominant format is the **GeoTIFF** (.tif), which embeds the CRS and
geotransform inside the image; **Cloud-Optimized GeoTIFF (COG)** organises
it for efficient access over HTTP.

```python
import rasterio

with rasterio.open("elevation.tif") as src:
    print(src.width, src.height)     # grid size in cells
    print(src.count)                 # number of bands
    print(src.res)                   # (x, y) cell size in CRS units
    print(src.crs)                   # e.g. EPSG:32723 (UTM 23S)
    band1 = src.read(1)              # a NumPy array of values
```

To convert a cell index to a coordinate, the geotransform is:

```text
x = origin_x + col * pixel_width
y = origin_y + row * pixel_height   (pixel_height is usually negative)
```

```mermaid
graph TD
    RAST["Raster grid"] --> RES["Resolution cell size"]
    RAST --> EXT["Extent bounding box"]
    RAST --> BANDS["One or more bands"]
    RAST --> GT["Geotransform"]
    GT --> COORD["Cell maps to coordinate"]
    BANDS --> VAL["Each cell holds a value"]
```

Remember: raster = a georeferenced grid of valued cells. Choose it for
continuous phenomena; choose vector for discrete features with identities.
""",
        ),
        quiz_lesson(
            "Quiz: The raster data model",
            (
                q(
                    "How does the raster model represent the world?",
                    (
                        opt("As points, lines and polygons"),
                        opt(
                            "As a grid of cells (pixels), each holding a value, covering "
                            "space continuously",
                            correct=True,
                        ),
                        opt("As a table of attributes only"),
                        opt("As a list of coordinates"),
                    ),
                    "Rasters suit continuous phenomena like elevation, temperature and "
                    "reflectance.",
                ),
                q(
                    "What does raster 'resolution' mean?",
                    (
                        opt("The number of colours on screen"),
                        opt(
                            "The ground size covered by one cell - e.g. a 10 m cell "
                            "spans a 10 by 10 m patch",
                            correct=True,
                        ),
                        opt("The number of files in the dataset"),
                        opt("The compression ratio"),
                    ),
                    "Smaller cells mean more detail and larger files.",
                ),
                q(
                    "What are raster 'bands'?",
                    (
                        opt("The edges of the image"),
                        opt("Rows that contain NoData"),
                        opt(
                            "Multiple stacked layers of values on the same grid, e.g. "
                            "red, green, blue and near-infrared",
                            correct=True,
                        ),
                        opt("The file format version"),
                    ),
                    "Satellite imagery stacks many spectral bands over one grid.",
                ),
            ),
        ),
        # -- 3. Geospatial stack ---------------------------------------
        _t(
            "GIS software and the geospatial stack",
            "10 min",
            """# GIS software and the geospatial stack

You do GIS with a **stack** of software layered on shared open standards
and formats, so a file made in one tool opens in another.

The main desktop applications:

- **QGIS** - free and open-source, cross-platform, huge plugin ecosystem.
- **ArcGIS Pro** - the commercial Esri suite, deep toolbox and ecosystem.

Both sit on top of the same engines and libraries:

- **GDAL/OGR** - the workhorse translation library. **GDAL** handles
  raster formats, **OGR** handles vector formats. Almost everything reads
  and writes through it. Its command-line tools are everywhere:

```text
gdalinfo scene.tif                 # report CRS, size, bands, stats
ogr2ogr out.gpkg in.shp            # convert Shapefile to GeoPackage
gdalwarp -t_srs EPSG:3857 a.tif b.tif   # reproject a raster
```

- **PROJ** - the library that performs CRS definitions and
  reprojection (the maths behind EPSG codes).
- **GEOS** - the geometry engine for spatial predicates and operations
  (intersects, buffer, union) used by PostGIS, Shapely and QGIS.
- **PostGIS** - the spatial extension for PostgreSQL, turning a database
  into a GIS server that runs spatial SQL.

Interoperability rests on **OGC standards**: **WMS** (map images),
**WFS** (vector features), **WMTS** (tiled maps), and formats like
**GeoPackage**, **GeoTIFF** and **GeoJSON**.

```mermaid
graph TD
    APPS["QGIS and ArcGIS Pro"] --> GDAL["GDAL and OGR formats"]
    APPS --> GEOS["GEOS geometry engine"]
    APPS --> PROJ["PROJ reprojection"]
    GDAL --> FMT["GeoTIFF GeoPackage GeoJSON"]
    GEOS --> DB["PostGIS spatial SQL"]
    APPS --> OGC["OGC services WMS WFS WMTS"]
```

Remember: GDAL/OGR, PROJ and GEOS are the shared foundation; QGIS,
ArcGIS and PostGIS are different front doors to the same core, tied
together by open OGC standards and formats.
""",
        ),
        quiz_lesson(
            "Quiz: GIS software and the geospatial stack",
            (
                q(
                    "What is GDAL/OGR's role in the geospatial stack?",
                    (
                        opt("It is a web map viewer only"),
                        opt(
                            "The workhorse translation library - GDAL for raster, OGR "
                            "for vector formats - that most tools read and write through",
                            correct=True,
                        ),
                        opt("It is a proprietary Esri format"),
                        opt("It stores user passwords"),
                    ),
                    "gdalinfo, ogr2ogr and gdalwarp are its ubiquitous command-line tools.",
                ),
                q(
                    "How do QGIS, ArcGIS Pro and PostGIS relate?",
                    (
                        opt("They cannot share any data"),
                        opt(
                            "They are different front doors sitting on the same core "
                            "engines (GDAL, PROJ, GEOS) and open formats",
                            correct=True,
                        ),
                        opt("Only ArcGIS can open GeoTIFFs"),
                        opt("PostGIS replaces the need for any file format"),
                    ),
                    "Shared libraries and OGC standards make files portable between tools.",
                ),
                q(
                    "What is PostGIS?",
                    (
                        opt("A raster image format"),
                        opt("A QGIS plugin for printing maps"),
                        opt(
                            "The spatial extension for PostgreSQL that runs spatial SQL, "
                            "turning the database into a GIS engine",
                            correct=True,
                        ),
                        opt("A satellite constellation"),
                    ),
                    "PostGIS adds geometry types and spatial functions to Postgres, "
                    "built on GEOS and PROJ.",
                ),
            ),
        ),
        # -- 4. Spatial relationships and topology ---------------------
        _t(
            "Spatial relationships and topology",
            "10 min",
            """# Spatial relationships and topology

**Topology** is the study of how geometries relate in space -
relationships that stay true regardless of the exact coordinates:
adjacency, containment, connectivity. GIS answers spatial questions by
testing **spatial predicates** between geometries.

The core predicates (each returns true or false):

- **Intersects** - the geometries share any point at all.
- **Contains / Within** - one geometry fully encloses the other.
- **Touches** - they share only a boundary, not an interior.
- **Overlaps** - interiors partially coincide but neither contains the
  other.
- **Disjoint** - they share nothing.
- **Crosses** - e.g. a road line crossing a river line.

These are formalised by the **DE-9IM** model, which classifies the
intersection of two geometries' interiors, boundaries and exteriors.

```python
import geopandas as gpd

cities = gpd.read_file("cities.gpkg")     # points
regions = gpd.read_file("regions.gpkg")   # polygons

# which region contains each city? relies on the 'within' predicate
tagged = gpd.sjoin(cities, regions, predicate="within")
```

The same predicates power spatial SQL in PostGIS:

```sql
-- count the cities inside each region
SELECT r.name, COUNT(c.*) AS n_cities
FROM regions r
JOIN cities c ON ST_Contains(r.geom, c.geom)
GROUP BY r.name;
```

**Topological correctness** also matters when editing: shared borders of
adjacent polygons must line up exactly, with no **slivers** (thin gaps) or
overlaps. GIS tools enforce **topology rules** ("must not overlap", "must
not have gaps") to keep a dataset clean.

```mermaid
graph TD
    A["Geometry A"] --> PRED["Spatial predicate"]
    B["Geometry B"] --> PRED
    PRED --> INT["Intersects"]
    PRED --> CON["Contains or within"]
    PRED --> TCH["Touches"]
    PRED --> DIS["Disjoint"]
    PRED --> DE9["DE-9IM matrix"]
```

Remember: spatial predicates (intersects, contains, touches, disjoint)
are how GIS reasons about relationships; DE-9IM is the formal model
underneath, and topology rules keep shared boundaries clean.
""",
        ),
        quiz_lesson(
            "Quiz: Spatial relationships and topology",
            (
                q(
                    "What does the 'intersects' predicate test?",
                    (
                        opt("Whether two geometries share any point at all", correct=True),
                        opt("Whether two geometries are exactly equal"),
                        opt("Whether a raster has NoData"),
                        opt("Whether the file is valid"),
                    ),
                    "Intersects is the most general predicate: true if the geometries "
                    "share anything. Disjoint is its opposite.",
                ),
                q(
                    "What does the DE-9IM model formalise?",
                    (
                        opt("The compression of GeoTIFFs"),
                        opt(
                            "The classification of spatial relationships via the "
                            "intersection of two geometries' interiors, boundaries and "
                            "exteriors",
                            correct=True,
                        ),
                        opt("The number of bands in a raster"),
                        opt("The projection maths"),
                    ),
                    "DE-9IM underlies predicates like contains, touches and overlaps.",
                ),
                q(
                    "What is a 'sliver' in topological editing?",
                    (
                        opt("A type of satellite band"),
                        opt("A very fast query"),
                        opt(
                            "A thin gap or overlap where adjacent polygon borders fail "
                            "to line up exactly",
                            correct=True,
                        ),
                        opt("A NoData cell in a raster"),
                    ),
                    "Topology rules (must not overlap, must not have gaps) prevent "
                    "slivers and keep shared boundaries clean.",
                ),
            ),
        ),
        # -- 5. Vector geoprocessing -----------------------------------
        _t(
            "Vector geoprocessing",
            "11 min",
            """# Vector geoprocessing

**Geoprocessing** transforms geometries to produce new layers. Four
operations do most of the everyday work:

- **Buffer** - grow a zone of a given distance around features. A 500 m
  buffer around schools finds everything within walking distance. Distance
  is in the CRS units, so buffer in a **projected CRS (metres)**, not in
  degrees.
- **Clip** - cut one layer to the boundary of another (a cookie cutter):
  keep only the roads that fall inside a study area.
- **Dissolve** - merge features that share an attribute value into one
  geometry: dissolve counties into their states.
- **Spatial join** - attach attributes from one layer to another based on
  a spatial predicate (which region each point falls in), rather than a
  shared key.

```python
import geopandas as gpd

schools = gpd.read_file("schools.gpkg").to_crs(32723)   # UTM, metres
roads = gpd.read_file("roads.gpkg").to_crs(32723)

near = schools.buffer(500)                 # 500 m zones
zones = gpd.GeoDataFrame(geometry=near, crs=32723)

roads_in = gpd.clip(roads, zones)          # roads within the zones
by_type = roads.dissolve(by="road_class")  # merge by class

# spatial join: which zone does each accident fall in?
acc = gpd.read_file("accidents.gpkg").to_crs(32723)
joined = gpd.sjoin(acc, zones, predicate="within")
```

A frequent full task chains them: *buffer* the schools, *clip* the road
network to those buffers, then *spatial-join* accident points to count how
many happened near each school. That chain is a **geoprocessing model**.

```mermaid
graph LR
    SCH["Schools points"] --> BUF["Buffer 500 m"]
    BUF --> CLP["Clip roads to zones"]
    RD["Roads"] --> CLP
    CLP --> SJ["Spatial join accidents"]
    ACC["Accidents"] --> SJ
    SJ --> OUT["Counts per zone"]
```

Remember: buffer creates proximity zones, clip cuts to an area, dissolve
merges by attribute, and spatial join transfers attributes by location -
and you must work in a metric CRS for distances and areas to be correct.
""",
        ),
        quiz_lesson(
            "Quiz: Vector geoprocessing",
            (
                q(
                    "What does a buffer operation produce?",
                    (
                        opt("A reprojected raster"),
                        opt(
                            "A zone of a given distance around features - e.g. a 500 m "
                            "proximity zone around each school",
                            correct=True,
                        ),
                        opt("A merged single polygon per attribute"),
                        opt("A table with no geometry"),
                    ),
                    "Buffer measures distance in CRS units, so use a projected (metric) CRS.",
                ),
                q(
                    "What is the difference between clip and dissolve?",
                    (
                        opt("They are the same operation"),
                        opt(
                            "Clip cuts a layer to another's boundary; dissolve merges "
                            "features sharing an attribute value into one geometry",
                            correct=True,
                        ),
                        opt("Clip merges polygons; dissolve cuts them"),
                        opt("Both only apply to rasters"),
                    ),
                    "Clip is a cookie cutter; dissolve aggregates by attribute (counties "
                    "into states).",
                ),
                q(
                    "How does a spatial join differ from a normal table join?",
                    (
                        opt("It requires a shared ID column"),
                        opt(
                            "It matches records by a spatial predicate (e.g. which "
                            "polygon a point falls within) instead of a shared key",
                            correct=True,
                        ),
                        opt("It only works on raster bands"),
                        opt("It deletes the geometry column"),
                    ),
                    "Spatial join transfers attributes based on location, using "
                    "predicates like within or intersects.",
                ),
            ),
        ),
        # -- 6. Overlay and map algebra --------------------------------
        _t(
            "Overlay analysis and map algebra",
            "11 min",
            """# Overlay analysis and map algebra

**Overlay** combines two layers so their geometries *and* attributes
interact. The classic idea (from map layering) is stacking themes -
soils, slope, flood zones - to find where conditions coincide.

For **vector overlay**, the set operations are:

- **Intersection** - keep only the area common to both layers; output
  carries attributes from both. "Where is forest AND on steep slope?"
- **Union** - keep all area from both, split along every boundary.
- **Difference (erase)** - keep the part of A not covered by B. "Land
  parcels minus the flood zone."
- **Symmetric difference** - the area in one layer or the other, not both.

```python
import geopandas as gpd

forest = gpd.read_file("forest.gpkg").to_crs(32723)
steep = gpd.read_file("steep_slope.gpkg").to_crs(32723)

# forest AND steep: candidate erosion-risk areas, attributes from both
risk = gpd.overlay(forest, steep, how="intersection")
risk["area_ha"] = risk.area / 10_000        # square metres to hectares
```

The raster equivalent is **map algebra**: apply arithmetic or logical
expressions cell by cell across aligned rasters. To find cells that are
both wet and warm you combine two rasters:

```python
import numpy as np
suitable = (rainfall > 800) & (temperature > 15)   # boolean grid
score = 0.6 * slope_norm + 0.4 * rainfall_norm      # weighted overlay
```

**Weighted overlay** (as above) is the heart of **suitability analysis**:
reclassify each factor to a common scale, weight them by importance, and
sum - the standard way to pick a site for a road, a store or a reserve.

```mermaid
graph TD
    L1["Layer A forest or rainfall"] --> OV["Overlay"]
    L2["Layer B slope or temperature"] --> OV
    OV --> INT["Vector intersection"]
    OV --> ALG["Raster map algebra"]
    INT --> RES["Combined attributes"]
    ALG --> SUIT["Weighted suitability"]
```

Remember: vector overlay uses set operations (intersection, union,
difference) that combine geometry and attributes; raster map algebra
combines aligned grids cell by cell, and weighted overlay is how you build
a suitability model.
""",
        ),
        quiz_lesson(
            "Quiz: Overlay analysis and map algebra",
            (
                q(
                    "What does a vector 'intersection' overlay return?",
                    (
                        opt("All area from both layers"),
                        opt(
                            "Only the area common to both layers, carrying attributes "
                            "from both inputs",
                            correct=True,
                        ),
                        opt("The part of A not covered by B"),
                        opt("The raster cell values"),
                    ),
                    "Intersection is the AND of two layers; union keeps everything, "
                    "difference erases.",
                ),
                q(
                    "What is raster 'map algebra'?",
                    (
                        opt("Renaming raster files"),
                        opt(
                            "Applying arithmetic or logical expressions cell by cell "
                            "across aligned rasters",
                            correct=True,
                        ),
                        opt("Converting a raster to points"),
                        opt("Compressing a GeoTIFF"),
                    ),
                    "For example (rainfall > 800) & (temperature > 15) yields a boolean "
                    "suitability grid.",
                ),
                q(
                    "In weighted overlay for suitability analysis, what do you do?",
                    (
                        opt("Delete all but one layer"),
                        opt(
                            "Reclassify each factor to a common scale, weight the "
                            "factors by importance, and sum them into a score",
                            correct=True,
                        ),
                        opt("Buffer every layer by the same distance"),
                        opt("Reproject to EPSG:4326 only"),
                    ),
                    "Weighted overlay is the standard site-selection method: normalise, "
                    "weight, sum.",
                ),
            ),
        ),
        # -- 7. Raster analysis ----------------------------------------
        _t(
            "Raster analysis - reclassify, zonal stats, terrain",
            "11 min",
            """# Raster analysis - reclassify, zonal stats, terrain

Beyond map algebra, three raster operations appear constantly.

**Reclassify** maps input cell values to new classes - turning a
continuous surface into meaningful categories. Elevation becomes low /
medium / high; a land-cover code map becomes a simpler legend.

```python
import numpy as np
elev = src.read(1).astype("float32")
cls = np.select(
    [elev < 200, elev < 800, elev >= 800],
    [1, 2, 3],                       # low, medium, high
    default=0,
)
```

**Zonal statistics** summarise a *value* raster within the *zones* of
another layer (vector polygons or a category raster): the mean elevation
per watershed, total rainfall per municipality, majority land cover per
parcel. It is how a raster feeds numbers back into a vector table.

```python
from rasterstats import zonal_stats
stats = zonal_stats(
    "watersheds.gpkg", "elevation.tif",
    stats=["mean", "min", "max"],
)   # one summary row per watershed polygon
```

**Terrain analysis** derives products from a **Digital Elevation Model
(DEM)**:

- **Slope** - steepness, from the rate of elevation change between cells.
- **Aspect** - the compass direction a slope faces.
- **Hillshade** - simulated shading from a light source, for relief maps.
- **Flow direction and accumulation** - which way water runs and where it
  collects, for watershed and drainage analysis.

Slope at a cell comes from the elevation differences with its neighbours:

```text
slope = arctan( sqrt( (dz/dx)^2 + (dz/dy)^2 ) )
```

```mermaid
graph TD
    DEM["Digital elevation model"] --> SLOPE["Slope"]
    DEM --> ASPECT["Aspect"]
    DEM --> HILL["Hillshade"]
    DEM --> FLOW["Flow direction"]
    VAL["Value raster"] --> ZONAL["Zonal statistics"]
    ZONES["Zone polygons"] --> ZONAL
    ZONAL --> TABLE["Summary per zone"]
```

Remember: reclassify buckets values into classes, zonal statistics summarise
a raster within zones (bridging raster to vector tables), and terrain
analysis derives slope, aspect, hillshade and flow from a DEM.
""",
        ),
        quiz_lesson(
            "Quiz: Raster analysis - reclassify, zonal stats, terrain",
            (
                q(
                    "What does 'reclassify' do to a raster?",
                    (
                        opt("Changes its file format"),
                        opt(
                            "Maps input cell values to new classes - e.g. continuous "
                            "elevation into low, medium and high",
                            correct=True,
                        ),
                        opt("Reprojects it to a new CRS"),
                        opt("Removes all its bands"),
                    ),
                    "Reclassify turns continuous values into meaningful categories.",
                ),
                q(
                    "What do zonal statistics compute?",
                    (
                        opt("The file size of each band"),
                        opt(
                            "Summaries of a value raster within the zones of another "
                            "layer - e.g. mean elevation per watershed",
                            correct=True,
                        ),
                        opt("The projection parameters"),
                        opt("The colour ramp of a map"),
                    ),
                    "Zonal statistics bridge raster values back into a vector "
                    "attribute table, one row per zone.",
                ),
                q(
                    "Which products are derived from a Digital Elevation Model?",
                    (
                        opt("Land ownership and parcel IDs"),
                        opt(
                            "Slope, aspect, hillshade, and flow direction and accumulation",
                            correct=True,
                        ),
                        opt("Road names and speed limits"),
                        opt("Only the CRS"),
                    ),
                    "Terrain analysis reads a DEM to describe steepness, orientation, "
                    "shading and drainage.",
                ),
            ),
        ),
        # -- 8. Workflows and automation -------------------------------
        _t(
            "Geoprocessing workflows and automation",
            "10 min",
            """# Geoprocessing workflows and automation

Real GIS work is rarely one operation - it is a **workflow**: a repeatable
chain of steps from raw data to a finished product. Clicking through them
by hand once is fine; doing it monthly for 50 datasets is not. **Automate
the workflow** so it is reproducible, reviewable and fast.

The Python geospatial ecosystem makes workflows into scripts:

- **geopandas** - vector layers as GeoDataFrames (built on Shapely, GDAL,
  and pandas). Read, transform, geoprocess, write.
- **rasterio** - read and write rasters as NumPy arrays.
- **Shapely** - individual-geometry operations.
- **pyproj** - CRS handling and reprojection.

A complete workflow reads inputs, aligns their CRS, runs the analysis and
writes the result - the same steps you would click, now in code:

```python
import geopandas as gpd

# 1. read
schools = gpd.read_file("schools.gpkg")
census = gpd.read_file("census.gpkg")

# 2. align CRS to a metric system (essential before distance/area)
schools = schools.to_crs(32723)
census = census.to_crs(32723)

# 3. analyse: 1 km catchments, then population within each
catch = gpd.GeoDataFrame(geometry=schools.buffer(1000), crs=32723)
served = gpd.sjoin(census, catch, predicate="within")
by_school = served.groupby("index_right")["population"].sum()

# 4. write a reproducible output
catch.join(by_school.rename("pop_served")).to_file("catchments.gpkg")
```

Both major desktops offer visual workflow builders too - QGIS **Graphical
Modeler** and ArcGIS **ModelBuilder** - and ArcGIS exposes the same tools
through the **arcpy** Python library. The principle is identical: capture
the steps once so they run the same way every time.

```mermaid
graph LR
    IN["Read inputs"] --> CRS["Align CRS to metric"]
    CRS --> PROC["Geoprocess buffer join"]
    PROC --> AGG["Aggregate results"]
    AGG --> OUT["Write output layer"]
    OUT --> REPEAT["Re-run on new data"]
```

Remember: turn manual GIS steps into scripted, version-controlled
workflows with geopandas and rasterio (or a visual modeler). Always align
the CRS before spatial analysis, and you gain reproducibility, review and
scale.
""",
        ),
        quiz_lesson(
            "Quiz: Geoprocessing workflows and automation",
            (
                q(
                    "Why automate a geoprocessing workflow as a script?",
                    (
                        opt("Scripts look more impressive"),
                        opt(
                            "It makes the chain of steps reproducible, reviewable and "
                            "fast to re-run on new data",
                            correct=True,
                        ),
                        opt("Because GIS cannot be done by clicking"),
                        opt("To avoid ever using a CRS"),
                    ),
                    "Clicking once is fine; a scripted workflow scales to many datasets reliably.",
                ),
                q(
                    "Which library represents vector layers as GeoDataFrames?",
                    (
                        opt("rasterio"),
                        opt("geopandas", correct=True),
                        opt("matplotlib"),
                        opt("NumPy alone"),
                    ),
                    "geopandas builds on Shapely, GDAL and pandas; rasterio handles "
                    "rasters as arrays.",
                ),
                q(
                    "What critical step must come before distance or area analysis in a workflow?",
                    (
                        opt("Deleting the attributes"),
                        opt("Converting to a Shapefile"),
                        opt(
                            "Aligning the layers to a projected (metric) CRS, e.g. UTM, "
                            "so measurements are correct",
                            correct=True,
                        ),
                        opt("Removing the geometry column"),
                    ),
                    "Distances and areas are wrong in degrees; reproject to a metric CRS first.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "When is the vector model preferable to the raster model?",
                    (
                        opt("Always - raster is obsolete"),
                        opt(
                            "For discrete features with identities and sharp boundaries "
                            "(roads, parcels, wells); raster suits continuous phenomena",
                            correct=True,
                        ),
                        opt("Only for satellite imagery"),
                        opt("Only when there is no CRS"),
                    ),
                    "Vector = discrete features plus attributes; raster = a grid for "
                    "continuous surfaces.",
                ),
                q(
                    "What three properties define a raster besides its cell values?",
                    (
                        opt("Owner, name and colour"),
                        opt(
                            "Resolution (cell size), extent, and bands - plus a "
                            "geotransform and CRS to georeference it",
                            correct=True,
                        ),
                        opt("Points, lines and polygons"),
                        opt("Buffer, clip and dissolve"),
                    ),
                    "The geotransform maps cell (row, col) to real coordinates.",
                ),
                q(
                    "What is the shared foundation under QGIS, ArcGIS and PostGIS?",
                    (
                        opt("A single proprietary file"),
                        opt(
                            "Common engines and libraries - GDAL/OGR, PROJ, GEOS - and "
                            "open OGC standards and formats",
                            correct=True,
                        ),
                        opt("They share nothing"),
                        opt("Only a web browser"),
                    ),
                    "This shared core is why a GeoPackage made in QGIS opens in ArcGIS "
                    "and PostGIS.",
                ),
                q(
                    "Which spatial predicate is true when two geometries share any point?",
                    (
                        opt("Disjoint"),
                        opt("Equals"),
                        opt("Intersects", correct=True),
                        opt("NoData"),
                    ),
                    "Intersects is the most general predicate; disjoint is its opposite.",
                ),
                q(
                    "A 500 m buffer around features requires what for a correct distance?",
                    (
                        opt("Working in a geographic CRS in degrees"),
                        opt(
                            "Working in a projected (metric) CRS such as UTM, so 500 "
                            "means 500 metres",
                            correct=True,
                        ),
                        opt("Removing the CRS entirely"),
                        opt("Converting to a raster first"),
                    ),
                    "Buffer distance is in CRS units; in EPSG:4326 that would be 500 "
                    "degrees, which is meaningless.",
                ),
                q(
                    "How does a spatial join differ from an ordinary table join?",
                    (
                        opt("It needs a matching ID column"),
                        opt(
                            "It matches records by a spatial predicate, such as which "
                            "polygon a point falls within, rather than by a shared key",
                            correct=True,
                        ),
                        opt("It only works on rasters"),
                        opt("It always drops geometry"),
                    ),
                    "Spatial join transfers attributes by location.",
                ),
                q(
                    "In a vector overlay, what does 'difference' (erase) return?",
                    (
                        opt("Everything in both layers"),
                        opt("Only the common area of both"),
                        opt(
                            "The part of layer A not covered by layer B - e.g. parcels "
                            "minus the flood zone",
                            correct=True,
                        ),
                        opt("The raster cell values"),
                    ),
                    "Intersection is AND, union keeps all, difference erases B from A.",
                ),
                q(
                    "What do zonal statistics produce?",
                    (
                        opt("A reprojected raster"),
                        opt(
                            "A summary of a value raster within each zone - e.g. mean "
                            "elevation per watershed - bridging raster to a vector table",
                            correct=True,
                        ),
                        opt("A buffer around each polygon"),
                        opt("A new colour ramp"),
                    ),
                    "Zonal statistics give one summary row per zone.",
                ),
                q(
                    "Which products come from terrain analysis of a DEM?",
                    (
                        opt("Population and land value"),
                        opt(
                            "Slope, aspect, hillshade, and flow direction and accumulation",
                            correct=True,
                        ),
                        opt("Road names and speed limits"),
                        opt("The file compression ratio"),
                    ),
                    "A DEM yields steepness, orientation, shaded relief and drainage.",
                ),
                q(
                    "What is the key benefit of scripting a geoprocessing workflow with "
                    "geopandas and rasterio?",
                    (
                        opt("It hides the results from review"),
                        opt(
                            "Reproducibility, review and scale - the same steps run "
                            "identically on new data every time",
                            correct=True,
                        ),
                        opt("It removes the need for a CRS"),
                        opt("It converts everything to Shapefiles"),
                    ),
                    "Automating the chain turns a one-off click-through into a reliable, "
                    "repeatable pipeline.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

GIS_FUNDAMENTALS_COURSES: tuple[SeedCourse, ...] = (_GIS_FUNDAMENTALS,)
