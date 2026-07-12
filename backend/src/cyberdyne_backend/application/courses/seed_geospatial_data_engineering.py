"""Academy seed content - Geospatial Data Engineering and Platforms.

The platform-engineering view of geospatial: how you build the systems
that store, index, process and serve spatial data at scale. It covers
platform architecture, cloud-optimized formats (COG, GeoParquet, Zarr),
the STAC and OGC API standards, a FastAPI and PostGIS backend, object
storage and dynamic tiling (MinIO, TiTiler), distributed processing of
imagery (Dask, Spark), analytical databases (DuckDB, ClickHouse) for
spatial queries, and containerized deployment with CI/CD and monitoring.
Every lesson is a direct explanation with a real config or code example
and a mermaid diagram, followed by a checkpoint quiz; the course closes
with a comprehensive final quiz.
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


_GEOSPATIAL_DATA_ENGINEERING = SeedCourse(
    slug="geospatial-data-engineering",
    title="Geospatial Data Engineering & Platforms",
    description=(
        "Building the platforms that serve geospatial data at scale - "
        "cloud-native formats, STAC and OGC APIs, distributed processing, "
        "and a FastAPI/PostGIS/object-storage backend architecture."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Geospatial Data Engineering and Platforms

This course is about the **systems**, not the maps. Analysts run queries
and make maps; this course is for the engineers who build the platform
underneath - the storage, the indexes, the APIs, and the processing that
let a petabyte of imagery and billions of features be served quickly to
many users.

The approach is **concrete**: every lesson explains one part of the
platform directly, shows a real example (a format layout, a STAC item, a
PostGIS query, a FastAPI route, a Dask graph, a Dockerfile), and draws it
as a diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **Platform architecture** - the layers from storage to API
2. **Cloud-optimized formats** - COG, GeoParquet, Zarr
3. **STAC and OGC API standards** - how clients discover and pull data
4. **A FastAPI and PostGIS backend** - the spatial service layer
5. **Object storage and tiling** - MinIO and TiTiler
6. **Distributed processing** - Dask and Spark over imagery
7. **Analytical databases** - DuckDB and ClickHouse for spatial analytics
8. **Deployment** - containers, CI/CD, and monitoring

The thread through all of it: keep data **cloud-native** (readable in
place, in chunks, over HTTP), make it **discoverable** through open
standards, and **scale the compute to the data** rather than moving the
data to the compute.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "Who is this course aimed at?",
                    (
                        opt("Analysts who only make maps in a desktop GIS"),
                        opt(
                            "Engineers who build the platform underneath - storage, "
                            "indexes, APIs and processing that serve spatial data at "
                            "scale",
                            correct=True,
                        ),
                        opt("Field surveyors collecting GNSS points"),
                        opt("Cartographers designing print layouts"),
                    ),
                    "It is a platform-engineering course: the systems that serve data, "
                    "not the analysis done on top.",
                ),
                q(
                    "What is the recurring principle the course emphasizes?",
                    (
                        opt("Always download the whole dataset before using it"),
                        opt("Store everything in a single relational table"),
                        opt(
                            "Keep data cloud-native and discoverable, and scale compute "
                            "to the data rather than moving data to the compute",
                            correct=True,
                        ),
                        opt("Avoid open standards to keep systems simple"),
                    ),
                    "Cloud-native, standards-based access plus data-local compute is the "
                    "thread through every lesson.",
                ),
            ),
        ),
        # -- 1. Platform architecture ----------------------------------
        _t(
            "Geospatial platform architecture",
            "10 min",
            """# Geospatial platform architecture

A geospatial platform is a stack of **layers**, each solving one job, so
that raw satellite scenes and vector datasets become fast, queryable
services. Draw the layers and most design decisions become obvious.

- **Storage** - cheap, durable **object storage** (S3, GCS, Azure Blob,
  or self-hosted MinIO) holds the bulk data: imagery as **Cloud-Optimized
  GeoTIFF (COG)**, vector as **GeoParquet**, multidimensional arrays as
  **Zarr**. Object storage is the source of truth because it scales
  cheaply and serves ranges over HTTP.
- **Catalog and index** - a **STAC** catalog describes what exists (which
  scene, when, where, which bands) so clients can search without scanning
  files. A spatial database (**PostGIS**) indexes vector features and
  metadata for fast queries.
- **Processing** - **Dask** or **Spark** run analytics and mosaicking
  over many files in parallel, reading directly from object storage.
- **Serving** - an API layer (**FastAPI**, plus **OGC APIs** and dynamic
  tilers like **TiTiler**) turns stored data into query results, tiles,
  and downloads for clients.
- **Clients** - web maps (MapLibre, Cesium), notebooks, and desktop GIS
  (QGIS) consume the services.

```mermaid
graph TD
    STORE["Object storage COG GeoParquet Zarr"] --> CATALOG["STAC catalog and PostGIS index"]
    STORE --> PROC["Processing Dask and Spark"]
    CATALOG --> API["Serving FastAPI OGC APIs TiTiler"]
    PROC --> STORE
    API --> CLIENTS["Clients web maps notebooks QGIS"]
    CATALOG --> API
```

The key architectural choice is **separation of storage and compute**:
the data lives once in object storage, and any number of stateless
processing or serving components read from it on demand. That is what lets
the platform scale each layer independently.

Remember: object storage is the source of truth, STAC and PostGIS make it
findable, and stateless services scale the compute to the data.
""",
        ),
        quiz_lesson(
            "Quiz: Geospatial platform architecture",
            (
                q(
                    "In a modern geospatial platform, what is usually the source of "
                    "truth for bulk data?",
                    (
                        opt("A single large relational table"),
                        opt(
                            "Durable object storage (S3, GCS, MinIO) holding COG, "
                            "GeoParquet and Zarr, served in ranges over HTTP",
                            correct=True,
                        ),
                        opt("The web browser's local cache"),
                        opt("A desktop GIS project file"),
                    ),
                    "Object storage scales cheaply and serves byte ranges over HTTP, so "
                    "it holds the bulk data; databases index and catalog it.",
                ),
                q(
                    "What is the point of separating storage from compute?",
                    (
                        opt("It forces all data through one server"),
                        opt("It makes the data harder to access"),
                        opt(
                            "Data lives once in object storage while any number of "
                            "stateless components read it on demand, so each layer scales "
                            "independently",
                            correct=True,
                        ),
                        opt("It removes the need for any API"),
                    ),
                    "Stateless serving and processing read from a shared store, so you "
                    "scale each layer on its own.",
                ),
                q(
                    "Which layer makes the stored data discoverable without scanning every file?",
                    (
                        opt("The client web map"),
                        opt(
                            "The catalog and index layer - a STAC catalog plus a PostGIS "
                            "spatial index",
                            correct=True,
                        ),
                        opt("The object storage bucket alone"),
                        opt("The Dockerfile"),
                    ),
                    "STAC describes what exists and PostGIS indexes it, so clients query "
                    "metadata instead of reading files blindly.",
                ),
            ),
        ),
        # -- 2. Cloud-optimized formats --------------------------------
        _t(
            "Cloud-optimized formats - COG, GeoParquet, Zarr",
            "11 min",
            """# Cloud-optimized formats - COG, GeoParquet, Zarr

Traditional geo files assume you download the whole thing first.
**Cloud-optimized** formats are laid out so a client can read *just the
part it needs* directly from object storage using HTTP **range requests**
- no download, no server-side decoding.

**Cloud-Optimized GeoTIFF (COG)** is a regular GeoTIFF with an internal
layout that makes it cloud-native:

- **Tiling** - the raster is stored in internal tiles (e.g. 512x512), so a
  reader can fetch one tile instead of the whole image.
- **Overviews** - lower-resolution copies are embedded, so a zoomed-out
  map reads a small overview, not full-resolution pixels.
- **Header first** - the metadata sits at the front, so one small read
  tells the client exactly which byte ranges hold the tiles it wants.

Build one with GDAL, then read a window without pulling the whole file:

```python
# Create a COG with GDAL, then read one window via range requests
import rasterio
from rasterio.windows import Window

# gdal_translate in.tif out_cog.tif -of COG -co COMPRESS=DEFLATE
url = "https://data.example.com/scenes/s2_cog.tif"
with rasterio.open(url) as src:          # reads only the header first
    win = Window(col_off=1024, row_off=1024, width=512, height=512)
    patch = src.read(1, window=win)      # fetches only that tile's bytes
    print(patch.shape, src.crs)          # e.g. (512, 512) EPSG:32633
```

The **vector** equivalent is **GeoParquet** - Apache Parquet (columnar,
compressed, splittable) with a standard geometry column, ideal for
analytics over millions of features. The **multidimensional** equivalent
is **Zarr**: chunked N-dimensional arrays for time-series and climate
data cubes, where each chunk is a separately readable object.

```mermaid
graph TD
    NEED["Client needs a small window"] --> HDR["Read header only"]
    HDR --> RANGE["Compute byte ranges for tiles"]
    RANGE --> GET["HTTP range GET from object storage"]
    GET --> TILE["Only the needed tiles transfer"]
    TILE --> OV["Zoomed out uses embedded overviews"]
```

Remember: COG for rasters, GeoParquet for vectors, Zarr for data cubes -
all chunked so a client reads a slice over HTTP instead of downloading the
whole dataset.
""",
        ),
        quiz_lesson(
            "Quiz: Cloud-optimized formats - COG, GeoParquet, Zarr",
            (
                q(
                    "What makes a Cloud-Optimized GeoTIFF 'cloud-optimized'?",
                    (
                        opt("It is stored only in the cloud, never locally"),
                        opt(
                            "Internal tiling, embedded overviews and a header-first "
                            "layout let a client read just the needed tiles via HTTP "
                            "range requests",
                            correct=True,
                        ),
                        opt("It uses a proprietary encryption scheme"),
                        opt("It removes all georeferencing to shrink the file"),
                    ),
                    "Tiling plus overviews plus a front-loaded header means a reader "
                    "fetches only the bytes it needs, no full download.",
                ),
                q(
                    "Which format is the cloud-native choice for large vector datasets "
                    "used in analytics?",
                    (
                        opt("A single Shapefile"),
                        opt("A CSV of coordinates"),
                        opt(
                            "GeoParquet - columnar, compressed and splittable, with a "
                            "standard geometry column",
                            correct=True,
                        ),
                        opt("A screenshot of the map"),
                    ),
                    "GeoParquet brings Parquet's columnar analytics strengths to vector "
                    "geometries.",
                ),
                q(
                    "What kind of data is Zarr designed for?",
                    (
                        opt("Single small photographs"),
                        opt("Plain text documents"),
                        opt(
                            "Chunked N-dimensional arrays - time-series and climate data "
                            "cubes where each chunk is a separately readable object",
                            correct=True,
                        ),
                        opt("Relational join tables only"),
                    ),
                    "Zarr stores multidimensional arrays as independent chunks, ideal "
                    "for data cubes over time.",
                ),
            ),
        ),
        # -- 3. STAC and OGC APIs --------------------------------------
        _t(
            "STAC and OGC API standards",
            "11 min",
            """# STAC and OGC API standards

Cloud-optimized files are useless if clients cannot **find** them. Open
standards solve discovery and access so any compliant client works with
your platform.

**STAC (SpatioTemporal Asset Catalog)** is a JSON specification for
describing geospatial assets. Its core objects:

- **Item** - a single spatiotemporal thing (one scene) as a GeoJSON
  Feature, with a datetime, a bounding box, and **assets** (links to the
  COG bands, thumbnails, metadata).
- **Collection** - a group of related items (all Sentinel-2 L2A scenes)
  sharing metadata and extent.
- **Catalog** - a tree that ties collections and items together.

A trimmed STAC Item:

```json
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "S2A_33UUP_20240614",
  "collection": "sentinel-2-l2a",
  "bbox": [13.0, 52.3, 13.8, 52.7],
  "properties": {
    "datetime": "2024-06-14T10:12:19Z",
    "eo:cloud_cover": 4.1,
    "proj:epsg": 32633
  },
  "assets": {
    "red":  { "href": "s3://scenes/B04.tif", "type": "image/tiff; application=geotiff; profile=cloud-optimized" },
    "nir":  { "href": "s3://scenes/B08.tif", "type": "image/tiff; application=geotiff; profile=cloud-optimized" }
  }
}
```

A **STAC API** adds search: `POST /search` with a bbox, a datetime range,
and property filters returns matching items - the query layer over the
catalog.

The **OGC APIs** are the modern, JSON and OpenAPI-based successors to the
old WMS/WFS/WMTS web services:

- **OGC API - Features** - serve and query vector features (the successor
  to WFS).
- **OGC API - Tiles** - serve map tiles (successor to WMTS).
- **OGC API - Coverages / Maps** - serve raster coverages and rendered
  maps.

STAC (often aligned with OGC API - Features) tells clients *what exists*;
OGC APIs let them *pull the actual data*.

```mermaid
graph TD
    CAT["STAC catalog of items and collections"] --> SEARCH["STAC API search by bbox and time"]
    SEARCH --> ITEMS["Matching items with asset links"]
    ITEMS --> FEATURES["OGC API Features for vectors"]
    ITEMS --> TILES["OGC API Tiles for map tiles"]
    ITEMS --> COV["OGC API Coverages for rasters"]
```

Remember: STAC is the discovery index and the OGC APIs are the access
protocols - together they make your platform interoperable with any
standards-based client.
""",
        ),
        quiz_lesson(
            "Quiz: STAC and OGC API standards",
            (
                q(
                    "What does a STAC Item represent?",
                    (
                        opt("An entire satellite mission"),
                        opt(
                            "A single spatiotemporal asset (e.g. one scene) as a GeoJSON "
                            "Feature with a datetime, bbox and links to its assets",
                            correct=True,
                        ),
                        opt("A user account on the platform"),
                        opt("A database connection string"),
                    ),
                    "An Item is one scene: datetime, bounding box, and asset hrefs to "
                    "the COG bands and metadata.",
                ),
                q(
                    "How does a client find scenes over Berlin from last week using STAC?",
                    (
                        opt("It downloads every file and inspects each one"),
                        opt(
                            "It calls the STAC API search with a bbox, a datetime range "
                            "and property filters, and gets back matching items",
                            correct=True,
                        ),
                        opt("It guesses the file names by convention"),
                        opt("It emails the data provider"),
                    ),
                    "The STAC API search endpoint queries the catalog by space, time and "
                    "properties - no file scanning.",
                ),
                q(
                    "How do the OGC APIs relate to the older WMS/WFS/WMTS services?",
                    (
                        opt("They are unrelated binary protocols"),
                        opt(
                            "They are the modern JSON and OpenAPI-based successors - "
                            "Features replaces WFS, Tiles replaces WMTS",
                            correct=True,
                        ),
                        opt("They replace STAC entirely"),
                        opt("They only work with proprietary desktop clients"),
                    ),
                    "OGC API - Features, Tiles and Coverages are the RESTful, JSON "
                    "successors to WFS, WMTS and WCS.",
                ),
            ),
        ),
        # -- 4. FastAPI + PostGIS backend ------------------------------
        _t(
            "A FastAPI and PostGIS backend",
            "11 min",
            """# A FastAPI and PostGIS backend

The service layer that answers spatial queries is typically **PostGIS**
(PostgreSQL with spatial types and functions) behind a **FastAPI**
application. PostGIS does the spatial heavy lifting; FastAPI exposes it as
a clean, typed HTTP API.

**PostGIS** adds a `geometry` (and `geography`) column type and hundreds
of `ST_` functions. The critical performance feature is a **GiST spatial
index** - without it, every spatial query scans the whole table.

```sql
-- One-time setup: enable PostGIS and index the geometry column
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE INDEX idx_parcels_geom ON parcels USING GIST (geom);

-- A spatial query: parcels within 500 metres of a point (EPSG:4326)
-- ST_DWithin uses the GiST index; geography gives metres, not degrees
SELECT id, owner
FROM parcels
WHERE ST_DWithin(
        geom::geography,
        ST_SetSRID(ST_MakePoint(-73.985, 40.758), 4326)::geography,
        500
      );
```

`ST_DWithin`, `ST_Intersects`, and `ST_Contains` are **index-aware** -
they use the GiST index to shrink the candidate set before exact geometry
math. Always store the geometry's **SRID** (spatial reference id, e.g.
4326 for WGS84 lon/lat) so the database knows the coordinate system.

**FastAPI** wraps this in an async, validated API. Return **GeoJSON** so
web clients can render results directly:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/parcels/near")
async def parcels_near(lon: float, lat: float, radius_m: float = 500):
    rows = await db.fetch(
        \"\"\"
        SELECT id, owner, ST_AsGeoJSON(geom) AS geojson
        FROM parcels
        WHERE ST_DWithin(geom::geography,
              ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography, $3)
        \"\"\",
        lon, lat, radius_m,
    )
    return {"type": "FeatureCollection", "features": [_feature(r) for r in rows]}
```

Let the database do spatial work (`ST_AsGeoJSON`, `ST_Transform`,
clipping) - it is far faster than pulling raw geometries into Python.

```mermaid
graph LR
    CLIENT["Client request lon lat radius"] --> API["FastAPI async route"]
    API --> SQL["Parameterized spatial SQL"]
    SQL --> GIST["PostGIS GiST index narrows candidates"]
    GIST --> EXACT["Exact geometry test"]
    EXACT --> GJSON["Return GeoJSON FeatureCollection"]
    GJSON --> CLIENT
```

Remember: PostGIS plus a GiST index does the spatial computation, FastAPI
exposes it as typed GeoJSON endpoints, and you always carry the SRID.
""",
        ),
        quiz_lesson(
            "Quiz: A FastAPI and PostGIS backend",
            (
                q(
                    "Why is a GiST index critical on a PostGIS geometry column?",
                    (
                        opt("It compresses the geometries to save disk"),
                        opt(
                            "Without it, spatial queries scan the whole table; the GiST "
                            "index lets ST_DWithin and ST_Intersects narrow candidates "
                            "first",
                            correct=True,
                        ),
                        opt("It converts geometries to images"),
                        opt("It is required to store any geometry at all"),
                    ),
                    "Index-aware spatial functions use the GiST index to shrink the "
                    "candidate set before exact geometry math.",
                ),
                q(
                    "What does the SRID stored with a geometry tell the database?",
                    (
                        opt("The file size of the geometry"),
                        opt(
                            "The spatial reference / coordinate system it is in (e.g. "
                            "4326 for WGS84 lon/lat)",
                            correct=True,
                        ),
                        opt("The color to draw it in"),
                        opt("The user who created it"),
                    ),
                    "SRID identifies the coordinate reference system so transforms and "
                    "distance math are correct.",
                ),
                q(
                    "Where should the spatial computation (distance, clipping, GeoJSON "
                    "conversion) happen?",
                    (
                        opt("In the browser after downloading all rows"),
                        opt(
                            "In PostGIS via ST_ functions - far faster than pulling raw "
                            "geometries into Python",
                            correct=True,
                        ),
                        opt("Nowhere; it is not needed"),
                        opt("Only in a separate C++ microservice"),
                    ),
                    "Let the database do the spatial work with ST_AsGeoJSON, "
                    "ST_Transform and clipping; ship compact results.",
                ),
            ),
        ),
        # -- 5. Object storage and tiling ------------------------------
        _t(
            "Object storage and tiling services - MinIO, TiTiler",
            "11 min",
            """# Object storage and tiling services - MinIO, TiTiler

The bulk of a geospatial platform's bytes live in **object storage** -
imagery, archives, tiles. **MinIO** is a self-hosted, **S3-compatible**
object store: the same API and SDKs as Amazon S3, so code that talks to S3
works unchanged against MinIO on your own hardware. Buckets hold objects
addressed by key; clients read **byte ranges** over HTTP - exactly what
COG needs.

```python
# MinIO speaks the S3 API - boto3 works unchanged
import boto3

s3 = boto3.client("s3", endpoint_url="https://minio.internal:9000",
                  aws_access_key_id="KEY", aws_secret_access_key="SECRET")
s3.upload_file("s2_cog.tif", "scenes", "2024/06/s2_cog.tif")

# A range GET fetches only part of an object (how COG reads a tile)
head = s3.get_object(Bucket="scenes", Key="2024/06/s2_cog.tif",
                     Range="bytes=0-16383")   # just the header
```

Serving a raster as a slippy **map** means turning it into **tiles** -
small 256x256 images at fixed zoom levels in the **Web Mercator**
(EPSG:3857) tiling scheme, addressed as `z/x/y`. You can **pre-render**
tiles (fast, but huge storage and stale on update) or generate them
**dynamically**.

**TiTiler** is a FastAPI-based **dynamic tiler**: it reads a COG straight
from object storage and renders `z/x/y` tiles on request, applying
rescaling, colormaps, and band math (like NDVI) on the fly. Because COGs
have overviews and internal tiles, TiTiler only reads the few bytes each
output tile needs.

```text
# TiTiler renders a tile on demand from a COG in object storage
GET /cog/tiles/12/2200/1343.png?url=s3://scenes/2024/06/s2_cog.tif
    &rescale=0,3000&colormap_name=viridis

# z/x/y -> Web Mercator tile bounds -> COG overview + range reads -> PNG
```

Dynamic tiling means **no pre-rendering**: add a new scene to the bucket
and it is instantly viewable, at the cost of compute per tile (mitigated
by a CDN or tile cache in front).

```mermaid
graph LR
    COG["COG in MinIO object storage"] --> TITILER["TiTiler dynamic tiler"]
    REQ["Map requests z x y tile"] --> TITILER
    TITILER --> RANGE["Range reads only needed COG bytes"]
    RANGE --> RENDER["Rescale colormap band math"]
    RENDER --> PNG["PNG tile to the map"]
    PNG --> CACHE["CDN or tile cache"]
```

Remember: MinIO gives you S3-compatible object storage on your own
hardware, and TiTiler turns COGs into map tiles on demand - no giant
pre-rendered tile pyramid to build and keep fresh.
""",
        ),
        quiz_lesson(
            "Quiz: Object storage and tiling services - MinIO, TiTiler",
            (
                q(
                    "What is MinIO?",
                    (
                        opt("A desktop GIS application"),
                        opt(
                            "A self-hosted, S3-compatible object store - the same API and "
                            "SDKs as Amazon S3, run on your own hardware",
                            correct=True,
                        ),
                        opt("A JavaScript mapping library"),
                        opt("A coordinate reference system"),
                    ),
                    "MinIO exposes the S3 API, so S3 client code works unchanged against "
                    "your own object storage.",
                ),
                q(
                    "What does a dynamic tiler like TiTiler do?",
                    (
                        opt("Pre-renders every tile ahead of time and stores them all"),
                        opt(
                            "Reads a COG from object storage and renders z/x/y tiles on "
                            "request, applying rescaling, colormaps and band math on the "
                            "fly",
                            correct=True,
                        ),
                        opt("Converts vectors into a relational database"),
                        opt("Signs the tiles cryptographically"),
                    ),
                    "TiTiler renders tiles on demand straight from the COG, reading only "
                    "the bytes each tile needs.",
                ),
                q(
                    "What is the main trade-off of dynamic tiling versus pre-rendering?",
                    (
                        opt("Dynamic tiling needs no compute at all"),
                        opt(
                            "New data is instantly viewable with no pyramid to build, at "
                            "the cost of compute per tile - mitigated by a CDN or tile "
                            "cache",
                            correct=True,
                        ),
                        opt("Pre-rendering is always instantly up to date"),
                        opt("Dynamic tiling cannot use COG overviews"),
                    ),
                    "Dynamic = fresh and no storage of a pyramid, but you pay compute per "
                    "request, so you cache in front.",
                ),
            ),
        ),
        # -- 6. Distributed processing ---------------------------------
        _t(
            "Distributed processing of imagery - Dask, Spark",
            "11 min",
            """# Distributed processing of imagery - Dask, Spark

A single scene fits in memory; a **year of continental imagery** does not.
Distributed frameworks split the work across many workers and read
directly from object storage, so you **scale the compute to the data**.

**Dask** parallelizes Python and integrates natively with the geo stack.
Libraries like **xarray**, **rioxarray**, and **dask-geopandas** hand Dask
a **lazy graph** of chunked operations; nothing runs until you call
`.compute()`, and then it runs across all cores or a cluster.

```python
# Compute NDVI over a large stack lazily, then run it distributed
import stackstac, xarray as xr
from dask.distributed import Client

client = Client(n_workers=8)               # local or cluster scheduler
stack = stackstac.stack(stac_items, assets=["red", "nir"],
                        chunksize=2048)     # a lazy Dask-backed DataArray

nir, red = stack.sel(band="nir"), stack.sel(band="red")
ndvi = (nir - red) / (nir + red)           # still lazy - just a graph
result = ndvi.median(dim="time").compute() # executes across workers
```

The core idea is a **task graph**: each chunk (a tile of a scene) is a
node, operations are edges, and the scheduler runs independent chunks in
parallel, moving as little data as possible. Because chunks map to COG
internal tiles, a worker reads only the bytes for its chunk.

**Apache Spark** takes the same split-and-parallelize idea to very large
**tabular and vector** workloads on a JVM cluster. **Apache Sedona**
(formerly GeoSpark) adds spatial types, spatial joins, and spatial
partitioning to Spark - the tool of choice for joining billions of points
against polygons.

Rule of thumb: **Dask** for array and raster science in the Python
ecosystem; **Spark plus Sedona** for massive vector and tabular spatial
joins.

```mermaid
graph TD
    DATA["Many scenes in object storage"] --> CHUNK["Split into chunks per tile"]
    CHUNK --> GRAPH["Lazy task graph"]
    GRAPH --> SCHED["Scheduler assigns chunks"]
    SCHED --> W1["Worker reads its chunk bytes"]
    SCHED --> W2["Worker reads its chunk bytes"]
    W1 --> AGG["Combine partial results"]
    W2 --> AGG
    AGG --> OUT["Final output back to storage"]
```

Remember: build a lazy graph of chunked operations, let a scheduler run
the chunks in parallel next to the data, and pick Dask for arrays or
Spark plus Sedona for huge vector joins.
""",
        ),
        quiz_lesson(
            "Quiz: Distributed processing of imagery - Dask, Spark",
            (
                q(
                    "What does 'lazy' mean in a Dask geospatial workflow?",
                    (
                        opt("The code runs slowly on purpose"),
                        opt(
                            "Operations build a task graph and nothing executes until "
                            "you call compute; then chunks run in parallel across workers",
                            correct=True,
                        ),
                        opt("The workers sleep between tasks"),
                        opt("It skips reading the data entirely"),
                    ),
                    "Lazy evaluation records a graph of chunked operations and only runs "
                    "it on compute, enabling parallel, out-of-core work.",
                ),
                q(
                    "Why does chunking imagery map so well onto COG?",
                    (
                        opt("COGs cannot be chunked at all"),
                        opt(
                            "Chunks correspond to COG internal tiles, so each worker "
                            "reads only the byte ranges for its chunk from object storage",
                            correct=True,
                        ),
                        opt("Because COGs must be fully downloaded first"),
                        opt("Because chunks are stored in the database"),
                    ),
                    "A chunk lines up with a COG tile, so a worker fetches just its "
                    "bytes - compute goes to the data.",
                ),
                q(
                    "When would you reach for Spark with Sedona rather than Dask?",
                    (
                        opt("For a single small raster on a laptop"),
                        opt(
                            "For massive vector and tabular spatial joins - e.g. joining "
                            "billions of points against polygons on a JVM cluster",
                            correct=True,
                        ),
                        opt("Only when there is no data at all"),
                        opt("Never; Spark cannot do spatial work"),
                    ),
                    "Dask suits array/raster science in Python; Spark plus Sedona is "
                    "built for huge distributed spatial joins.",
                ),
            ),
        ),
        # -- 7. Analytical databases -----------------------------------
        _t(
            "Analytical databases for geospatial - DuckDB, ClickHouse",
            "10 min",
            """# Analytical databases for geospatial - DuckDB, ClickHouse

PostGIS is a superb **transactional** spatial database - great for serving
individual features and moderate queries. But scanning **billions of rows**
for an aggregate ("average NDVI per country per month") is a job for
**columnar analytical (OLAP)** engines.

**DuckDB** is an in-process analytical database - like "SQLite for
analytics" - with a **spatial extension** and, crucially, the ability to
query **GeoParquet directly from object storage**. No server, no load
step: point SQL at the files.

```sql
-- DuckDB: query GeoParquet in object storage, no import step
INSTALL spatial; LOAD spatial;
INSTALL httpfs;  LOAD httpfs;

SELECT country,
       COUNT(*) AS n,
       AVG(ndvi) AS mean_ndvi
FROM read_parquet('s3://analytics/observations/*.parquet')
WHERE ST_Within(geom, ST_GeomFromText('POLYGON((...))'))
GROUP BY country
ORDER BY mean_ndvi DESC;
```

Why columnar wins here: analytical queries touch a **few columns across
many rows**. A **columnar** store reads only those columns (not whole
rows), compresses each column tightly, and vectorizes the scan - so
aggregates over huge tables run far faster than in a row store.

**ClickHouse** is a distributed columnar database for **very large,
high-ingest** analytical workloads - trillions of rows, sub-second
aggregations, real-time dashboards. It has geo functions (points,
polygons, `pointInPolygon`, H3 and S2 grid helpers) and scales across a
cluster, making it a fit for telemetry, sensor, and movement data at
platform scale.

Use the right tool: **PostGIS** for transactional serving and rich
geometry operations, **DuckDB** for serverless analytics over GeoParquet
files, **ClickHouse** for massive real-time analytical aggregations.

```mermaid
graph TD
    Q["Aggregate over billions of rows"] --> COL["Columnar OLAP engine"]
    COL --> DUCK["DuckDB in process over GeoParquet"]
    COL --> CH["ClickHouse distributed high ingest"]
    DUCK --> SCAN["Read only needed columns"]
    CH --> SCAN
    SCAN --> FAST["Vectorized compressed fast aggregate"]
    PG["PostGIS"] --> TXN["Transactional serving and geometry ops"]
```

Remember: row-store PostGIS serves features; columnar DuckDB and
ClickHouse crush large-scale aggregations by reading only the columns they
need.
""",
        ),
        quiz_lesson(
            "Quiz: Analytical databases for geospatial - DuckDB, ClickHouse",
            (
                q(
                    "Why do columnar (OLAP) engines beat a row store for large aggregations?",
                    (
                        opt("They store data as images"),
                        opt(
                            "Analytical queries touch a few columns across many rows; a "
                            "columnar store reads only those columns, compresses them "
                            "tightly and vectorizes the scan",
                            correct=True,
                        ),
                        opt("They keep all data in the client browser"),
                        opt("They never use SQL"),
                    ),
                    "Column-oriented reads plus compression and vectorization make "
                    "wide-table aggregates far faster than row-by-row scans.",
                ),
                q(
                    "What makes DuckDB convenient for geospatial analytics?",
                    (
                        opt("It requires a large dedicated cluster to start"),
                        opt(
                            "It is in-process with a spatial extension and can query "
                            "GeoParquet directly from object storage - no server, no load "
                            "step",
                            correct=True,
                        ),
                        opt("It only reads Shapefiles"),
                        opt("It cannot run SQL"),
                    ),
                    "DuckDB is 'SQLite for analytics': point SQL at GeoParquet in a "
                    "bucket and aggregate, no import.",
                ),
                q(
                    "Which engine fits trillions of rows with high ingest and real-time "
                    "aggregations?",
                    (
                        opt("A single Shapefile"),
                        opt("PostGIS as the only option"),
                        opt(
                            "ClickHouse - a distributed columnar database with geo "
                            "functions built for very large, high-ingest analytical "
                            "workloads",
                            correct=True,
                        ),
                        opt("A spreadsheet"),
                    ),
                    "ClickHouse scales across a cluster for sub-second aggregations over "
                    "enormous, fast-growing tables.",
                ),
            ),
        ),
        # -- 8. Deployment, CI/CD, monitoring --------------------------
        _t(
            "Containerized deployment, CI/CD and monitoring",
            "11 min",
            """# Containerized deployment, CI/CD and monitoring

A geospatial platform is many services - FastAPI, TiTiler, a STAC API,
PostGIS, MinIO, workers. **Containers** package each with its native
dependencies (GDAL, PROJ, GEOS), which are notoriously painful to install
by hand, so every environment runs the exact same stack.

```dockerfile
# Dockerfile - a geospatial API image with GDAL preinstalled
FROM ghcr.io/osgeo/gdal:ubuntu-small-3.9.0   # GDAL, PROJ, GEOS ready
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt   # fastapi, rasterio
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**CI/CD** builds and ships these images automatically: on every push, run
tests, build the image, and deploy. Spatial platforms add data-aware
steps - validate STAC items against the spec, check that outputs are valid
COGs.

```yaml
# .github/workflows/deploy.yml
on: { push: { branches: [main] } }
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest                              # unit and spatial tests
      - run: stac-validator catalog.json         # validate STAC
      - run: rio cogeo validate out.tif          # confirm valid COG
      - run: docker build -t registry/geo-api:${{ github.sha }} .
      - run: docker push registry/geo-api:${{ github.sha }}
```

An orchestrator (Kubernetes, or Compose for smaller setups) runs the
images, scales the stateless tilers and workers under load, and keeps them
healthy.

**Monitoring** matters doubly here because geospatial workloads are
heavy - a single tile request can trigger many range reads. Track the
signals that reveal spatial-specific pain:

- **Latency** - especially tile p95/p99; slow tiles ruin the map.
- **Throughput and errors** - requests per second, error rate per service.
- **Object-storage reads** - GET count and bytes per tile (a spike means a
  COG lost its overviews or internal tiling).
- **Database** - slow spatial queries, whether GiST indexes are used.
- **Cache hit rate** - the tile cache / CDN effectiveness.

**Prometheus** scrapes metrics, **Grafana** dashboards and alerts on them;
**structured logs** and **traces** (OpenTelemetry) show where a slow tile
spent its time.

```mermaid
graph LR
    PUSH["Push to main"] --> CI["CI test validate STAC and COG"]
    CI --> IMG["Build and push image"]
    IMG --> ORCH["Orchestrator runs and scales services"]
    ORCH --> METRICS["Prometheus metrics"]
    METRICS --> GRAF["Grafana dashboards and alerts"]
    ORCH --> TRACE["Traces locate slow tiles"]
```

Remember: containerize services with their GDAL/PROJ/GEOS stack, let CI/CD
validate STAC and COG outputs before shipping, and monitor tile latency
and object-storage reads - the signals unique to a geospatial platform.
""",
        ),
        quiz_lesson(
            "Quiz: Containerized deployment, CI/CD and monitoring",
            (
                q(
                    "Why are containers especially valuable for geospatial services?",
                    (
                        opt("They remove the need for any code"),
                        opt(
                            "They package native dependencies like GDAL, PROJ and GEOS - "
                            "painful to install by hand - so every environment runs the "
                            "exact same stack",
                            correct=True,
                        ),
                        opt("They convert rasters to vectors automatically"),
                        opt("They eliminate the need for object storage"),
                    ),
                    "The C spatial stack (GDAL/PROJ/GEOS) is hard to install "
                    "consistently; a container pins it identically everywhere.",
                ),
                q(
                    "What data-aware checks belong in a geospatial CI/CD pipeline?",
                    (
                        opt("Only checking code style"),
                        opt(
                            "Validating STAC items against the spec and confirming "
                            "outputs are valid COGs, alongside the usual tests and image "
                            "build",
                            correct=True,
                        ),
                        opt("Deleting the test data"),
                        opt("Rendering the whole tile pyramid every push"),
                    ),
                    "Spatial pipelines validate STAC and COG outputs so bad data is "
                    "caught before it ships.",
                ),
                q(
                    "A sudden spike in object-storage GET count and bytes per tile most "
                    "likely means what?",
                    (
                        opt("The CDN is working perfectly"),
                        opt(
                            "A COG may have lost its overviews or internal tiling, so "
                            "each tile now reads far more bytes",
                            correct=True,
                        ),
                        opt("The database has too few rows"),
                        opt("The map has stopped being used"),
                    ),
                    "More reads per tile points to a non-cloud-optimized raster; monitor "
                    "storage reads to catch it.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is usually the source of truth for bulk data in a geospatial platform?",
                    (
                        opt("A desktop GIS project"),
                        opt(
                            "Durable object storage holding cloud-optimized data (COG, "
                            "GeoParquet, Zarr), served in ranges over HTTP",
                            correct=True,
                        ),
                        opt("The web browser cache"),
                        opt("A single spreadsheet"),
                    ),
                    "Object storage scales cheaply and serves byte ranges; databases and "
                    "catalogs index it.",
                ),
                q(
                    "What makes a Cloud-Optimized GeoTIFF readable in slices over HTTP?",
                    (
                        opt("It is encrypted"),
                        opt(
                            "Internal tiling, embedded overviews and a header-first "
                            "layout, read via HTTP range requests",
                            correct=True,
                        ),
                        opt("It stores no metadata"),
                        opt("It must be fully downloaded first"),
                    ),
                    "COG's layout lets a client fetch just the tiles and overview level it needs.",
                ),
                q(
                    "In STAC, what is an Item?",
                    (
                        opt("A whole satellite constellation"),
                        opt(
                            "A single spatiotemporal asset as a GeoJSON Feature with a "
                            "datetime, bbox and asset links",
                            correct=True,
                        ),
                        opt("A billing record"),
                        opt("A tiling scheme"),
                    ),
                    "An Item describes one scene and links to its COG assets; a STAC API "
                    "search finds items by space, time and properties.",
                ),
                q(
                    "How do the OGC APIs relate to WMS/WFS/WMTS?",
                    (
                        opt("They are unrelated"),
                        opt(
                            "They are the modern JSON and OpenAPI-based successors "
                            "(Features, Tiles, Coverages)",
                            correct=True,
                        ),
                        opt("They replace STAC"),
                        opt("They only serve PDFs"),
                    ),
                    "OGC API - Features/Tiles/Coverages succeed WFS/WMTS/WCS with RESTful JSON.",
                ),
                q(
                    "Why is a GiST index essential in a PostGIS backend?",
                    (
                        opt("It renders map tiles"),
                        opt(
                            "It lets spatial functions like ST_DWithin narrow candidates "
                            "instead of scanning the whole table",
                            correct=True,
                        ),
                        opt("It compresses images"),
                        opt("It stores the SRID"),
                    ),
                    "Index-aware spatial predicates use the GiST index to shrink the "
                    "candidate set before exact geometry math.",
                ),
                q(
                    "What does a dynamic tiler such as TiTiler do?",
                    (
                        opt("Pre-builds and stores the whole tile pyramid"),
                        opt(
                            "Reads a COG from object storage and renders z/x/y tiles on "
                            "request with rescaling, colormaps and band math",
                            correct=True,
                        ),
                        opt("Imports vectors into ClickHouse"),
                        opt("Validates STAC items"),
                    ),
                    "TiTiler renders tiles on demand from the COG, reading only the "
                    "needed bytes; a CDN caches the output.",
                ),
                q(
                    "What is 'lazy' evaluation in a Dask imagery workflow?",
                    (
                        opt("The workers idle"),
                        opt(
                            "Operations build a task graph and only execute on compute, "
                            "running chunks in parallel next to the data",
                            correct=True,
                        ),
                        opt("It skips reading data"),
                        opt("It runs everything on one core"),
                    ),
                    "A lazy graph of chunked ops runs in parallel across workers when you "
                    "call compute - scaling compute to the data.",
                ),
                q(
                    "When is a columnar engine like DuckDB or ClickHouse the right choice?",
                    (
                        opt("For single-feature transactional serving"),
                        opt(
                            "For large-scale aggregations over many rows, where reading "
                            "only the needed columns and vectorizing wins",
                            correct=True,
                        ),
                        opt("For storing the STAC catalog tree"),
                        opt("For rendering PNG tiles"),
                    ),
                    "Columnar OLAP engines crush wide-table aggregates; PostGIS remains "
                    "for transactional serving and geometry ops.",
                ),
                q(
                    "Which tool fits massive distributed vector spatial joins?",
                    (
                        opt("DuckDB in a browser"),
                        opt("TiTiler"),
                        opt(
                            "Apache Spark with Sedona - spatial types, joins and "
                            "partitioning on a JVM cluster",
                            correct=True,
                        ),
                        opt("A single Shapefile"),
                    ),
                    "Dask suits Python array/raster science; Spark plus Sedona handles "
                    "huge distributed spatial joins.",
                ),
                q(
                    "A spike in object-storage GET count and bytes per rendered tile most "
                    "likely indicates what?",
                    (
                        opt("The GiST index is too large"),
                        opt("The SRID is missing"),
                        opt(
                            "A raster lost its overviews or internal tiling, so it is no "
                            "longer cloud-optimized and each tile reads far more bytes",
                            correct=True,
                        ),
                        opt("The STAC catalog is empty"),
                    ),
                    "Monitoring storage reads per tile catches non-cloud-optimized "
                    "rasters - a signal unique to geospatial platforms.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

GEOSPATIAL_DATA_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_GEOSPATIAL_DATA_ENGINEERING,)
