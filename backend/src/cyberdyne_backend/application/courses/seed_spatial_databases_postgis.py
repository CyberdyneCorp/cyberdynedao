"""Academy seed content - Spatial Databases with PostGIS.

Storing and querying geospatial data at scale with PostGIS: the geometry
and geography types, spatial SQL for measurements and relationships,
spatial joins and aggregation, GiST spatial indexing, and performance
tuning with EXPLAIN ANALYZE. It also covers raster-in-the-database and
serving spatial data as vector tiles. Every lesson is a direct
explanation with a concrete SQL or Python example and a mermaid diagram,
followed by a checkpoint quiz; the course closes with a comprehensive
final quiz.
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


_SPATIAL_DATABASES_POSTGIS = SeedCourse(
    slug="spatial-databases-postgis",
    title="Spatial Databases with PostGIS",
    description=(
        "Storing and querying geospatial data at scale with PostGIS: the "
        "geometry and geography types, spatial SQL for measurements and "
        "relationships, spatial joins and aggregation, GiST spatial indexing, "
        "and performance tuning for large datasets - with real SQL and Python "
        "examples and a diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Spatial Databases with PostGIS

A spatial database does not just store where things are - it lets you
**ask spatial questions in SQL**: what is within 500 metres of this
point, which parcels a river crosses, how many crimes fell inside each
precinct. **PostGIS** is the extension that turns PostgreSQL, a mature
relational database, into a full spatial engine that scales to hundreds
of millions of rows.

This course is **practical and concrete**: every lesson explains one
idea directly, shows it in a short real example - almost always a piece
of spatial SQL - and draws the idea as a diagram. After each lesson
there is a short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Spatial databases and PostGIS** - what the extension adds and why
2. **Geometry and geography types** - the two spatial column types
3. **Spatial SQL** - measurements and relationships (ST_Distance, ST_Intersects)
4. **Spatial joins and aggregation** - combining layers by location
5. **Spatial indexing with GiST** - making spatial queries fast
6. **Query performance** - reading EXPLAIN ANALYZE and tuning
7. **Raster in the database** - storing and tiling gridded data
8. **Serving spatial data** - pg_tileserv and vector tiles

You are expected to know SQL and basic GIS ideas (coordinates, layers).
By the end you will read, write, and tune spatial queries with
confidence, and know how the data reaches a map.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What does a spatial database like PostGIS let you do that a plain "
                    "table of latitudes and longitudes does not?",
                    (
                        opt("Store numbers in columns"),
                        opt(
                            "Ask spatial questions directly in SQL - distance, "
                            "containment, intersection - over indexed geometry",
                            correct=True,
                        ),
                        opt("Render maps in the browser by itself"),
                        opt("Replace the need for coordinate systems"),
                    ),
                    "PostGIS adds spatial types, functions and indexes so 'what is near "
                    "or inside what' becomes a query, not application code.",
                ),
                q(
                    "What is PostGIS in relation to PostgreSQL?",
                    (
                        opt("A separate database that replaces PostgreSQL"),
                        opt(
                            "An extension that adds spatial types, functions and indexing "
                            "to PostgreSQL",
                            correct=True,
                        ),
                        opt("A web map server"),
                        opt("A file format for storing maps"),
                    ),
                    "PostGIS is loaded with CREATE EXTENSION postgis; it builds on "
                    "PostgreSQL rather than replacing it.",
                ),
            ),
        ),
        # -- 1. Spatial databases and PostGIS --------------------------
        _t(
            "Spatial databases and the PostGIS extension",
            "9 min",
            """# Spatial databases and the PostGIS extension

A **spatial database** stores geometry as a first-class data type and
provides functions and indexes to query it. Instead of pulling every row
into your application and computing distances there, you push the work
into the database, where an index can skip almost everything.

**PostGIS** adds this to PostgreSQL. You enable it once per database:

```sql
-- enable PostGIS in this database (also postgis_raster, postgis_topology)
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT PostGIS_Full_Version();  -- confirm the installed version
```

PostGIS follows the **OGC Simple Features** standard and the SQL/MM
spec, so its behaviour is portable and well defined. What it gives you:

- **Spatial types** - `geometry` and `geography` columns holding points,
  lines, polygons and their multi-variants.
- **Hundreds of `ST_` functions** - `ST_Area`, `ST_Distance`,
  `ST_Intersects`, `ST_Buffer`, `ST_Transform` and many more, all named
  with the OGC `ST_` (spatial type) prefix.
- **Spatial indexing** - GiST indexes on geometry columns.
- **Coordinate reference systems** - every geometry carries an **SRID**
  (for example 4326 for WGS84 lon/lat) via the `spatial_ref_sys` table.

A tiny table with a geometry column, storing points in WGS84:

```sql
CREATE TABLE stations (
    id   serial PRIMARY KEY,
    name text,
    geom geometry(Point, 4326)   -- typed: Point, SRID 4326 (WGS84)
);
INSERT INTO stations (name, geom)
VALUES ('Central', ST_SetSRID(ST_MakePoint(-46.633, -23.550), 4326));
```

```mermaid
graph TD
    PG["PostgreSQL"] --> EXT["CREATE EXTENSION postgis"]
    EXT --> TYPES["Spatial types geometry and geography"]
    EXT --> FUNCS["ST functions"]
    EXT --> IDX["GiST spatial index"]
    EXT --> SRS["spatial ref sys and SRID"]
    TYPES --> QUERY["Spatial SQL"]
    FUNCS --> QUERY
    IDX --> QUERY
```

Remember: PostGIS turns PostgreSQL into a spatial engine - typed
geometry columns, OGC-standard functions, coordinate systems, and
indexes - so location becomes just another thing you query in SQL.
""",
        ),
        quiz_lesson(
            "Quiz: Spatial databases and the PostGIS extension",
            (
                q(
                    "How do you enable PostGIS in a PostgreSQL database?",
                    (
                        opt("Install a separate PostGIS server process"),
                        opt("CREATE EXTENSION postgis in that database", correct=True),
                        opt("Rename the database to postgis"),
                        opt("Import a CSV of geometries"),
                    ),
                    "PostGIS is a loadable extension; one CREATE EXTENSION per database "
                    "adds the types, functions and index support.",
                ),
                q(
                    "What standard governs the ST_ function names and geometry model in PostGIS?",
                    (
                        opt("The JPEG image standard"),
                        opt(
                            "The OGC Simple Features standard (and SQL/MM), which defines "
                            "the ST_ spatial-type function naming",
                            correct=True,
                        ),
                        opt("The HTTP protocol"),
                        opt("The POSIX file standard"),
                    ),
                    "OGC Simple Features standardizes the geometry types and the ST_ "
                    "prefixed functions, making behaviour portable.",
                ),
                q(
                    "What does the SRID stored with a geometry record?",
                    (
                        opt("The row's primary key"),
                        opt("The colour to draw it on a map"),
                        opt(
                            "The coordinate reference system the coordinates are in - for "
                            "example 4326 for WGS84 lon/lat",
                            correct=True,
                        ),
                        opt("The number of vertices"),
                    ),
                    "Every geometry carries an SRID identifying its CRS; 4326 is WGS84 "
                    "geographic coordinates.",
                ),
            ),
        ),
        # -- 2. Geometry and geography ---------------------------------
        _t(
            "Geometry and geography types",
            "10 min",
            """# Geometry and geography types

PostGIS offers **two** spatial column types, and choosing correctly
matters for both correctness and speed.

**`geometry`** treats coordinates as points on a **flat Cartesian
plane**. Calculations (distance, area) use fast planar math. This is
exactly right when your data is in a **projected CRS** whose units are
metres - a UTM zone (for example EPSG:32723) or a national grid - so a
distance really is a distance in metres.

**`geography`** treats coordinates as **lon/lat on the spheroid** (WGS84,
EPSG:4326). Its calculations follow the curved surface of the Earth, so
`ST_Distance` returns **metres** even for widely separated points, with
no projection needed. It is more accurate over large areas but slower and
supports fewer functions.

A rule of thumb:

- **Local, projected data, heavy computation** -> `geometry` in a metre
  based projected CRS.
- **Global lon/lat data, correctness over long distances** -> `geography`.

You can always convert. Store lon/lat as geometry(4326) and cast when you
need true ground distance:

```sql
-- distance in metres between two lon/lat points, on the spheroid
SELECT ST_Distance(
    a.geom::geography,          -- cast geometry -> geography
    b.geom::geography
) AS metres
FROM stations a, stations b
WHERE a.name = 'Central' AND b.name = 'Airport';
```

Coordinate order is a classic trap: PostGIS geometry uses
**longitude first, then latitude** (X, Y). `ST_MakePoint(lon, lat)` - not
lat, lon.

To move between coordinate systems, use **`ST_Transform`**, which
reprojects from one SRID to another:

```sql
-- reproject WGS84 lon/lat (4326) into UTM zone 23S (32723), metres
SELECT ST_Transform(geom, 32723) FROM stations;
```

```mermaid
graph TD
    Q{"What is the data"}
    Q -->|"projected metres"| G["geometry planar math fast"]
    Q -->|"global lon lat"| GG["geography spheroid metres"]
    G --> T["ST Transform to reproject"]
    GG --> T
    T --> ANS["Correct distances and areas"]
```

Remember: `geometry` is fast flat math for projected data; `geography`
is accurate curved-Earth math for lon/lat; reproject with `ST_Transform`,
and always put longitude before latitude.
""",
        ),
        quiz_lesson(
            "Quiz: Geometry and geography types",
            (
                q(
                    "What is the core difference between the geometry and geography types?",
                    (
                        opt("geometry is for points, geography is for polygons"),
                        opt(
                            "geometry uses flat Cartesian math; geography computes on the "
                            "curved spheroid so distances come back in metres for lon/lat",
                            correct=True,
                        ),
                        opt("geometry cannot be indexed"),
                        opt("They are two names for the same type"),
                    ),
                    "geometry = planar/projected and fast; geography = spheroidal and "
                    "accurate over long lon/lat distances.",
                ),
                q(
                    "In PostGIS, what is the coordinate order for a point?",
                    (
                        opt("Latitude then longitude"),
                        opt("Longitude then latitude - ST_MakePoint(lon, lat)", correct=True),
                        opt("Whatever order you like; it is ignored"),
                        opt("Altitude then latitude"),
                    ),
                    "Geometry is X, Y = longitude, latitude; swapping them silently puts "
                    "points in the wrong place.",
                ),
                q(
                    "Which function reprojects a geometry from one CRS to another?",
                    (
                        opt("ST_Buffer"),
                        opt("ST_Area"),
                        opt("ST_Transform", correct=True),
                        opt("ST_AsText"),
                    ),
                    "ST_Transform(geom, target_srid) converts coordinates between "
                    "spatial reference systems, e.g. 4326 -> 32723.",
                ),
            ),
        ),
        # -- 3. Spatial SQL --------------------------------------------
        _t(
            "Spatial SQL: measurements and relationships",
            "11 min",
            """# Spatial SQL: measurements and relationships

The heart of PostGIS is a large family of **`ST_` functions** that fall
into two broad groups: those that **measure** geometry and those that
test the **spatial relationship** between two geometries.

**Measurement** functions return a number:

- **`ST_Distance(a, b)`** - shortest distance between two geometries (in
  CRS units for geometry; in metres for geography).
- **`ST_Length(line)`**, **`ST_Area(polygon)`**, **`ST_Perimeter(poly)`**.

**Relationship predicates** return true/false and are the basis of
spatial filtering and joins:

- **`ST_Intersects(a, b)`** - do they share any point at all? The most
  common predicate.
- **`ST_Contains(a, b)`** / **`ST_Within(a, b)`** - is one fully inside
  the other?
- **`ST_DWithin(a, b, d)`** - are they within distance `d`? This one is
  special: it is **index-assisted**, so it is the right way to ask
  "within 500 metres", far better than `ST_Distance(...) < 500`.

Find every station within 500 metres of a given point, using geography so
`d` is in metres:

```sql
SELECT name
FROM stations
WHERE ST_DWithin(
    geom::geography,
    ST_SetSRID(ST_MakePoint(-46.63, -23.55), 4326)::geography,
    500                          -- 500 metres
);
```

Which district a point falls in - a relationship join in the WHERE clause:

```sql
SELECT d.name
FROM districts d
WHERE ST_Contains(d.geom, ST_SetSRID(ST_MakePoint(-46.63, -23.55), 4326));
```

A subtlety worth knowing: predicates like `ST_Intersects` and
`ST_DWithin` first use the geometry's **bounding box** (via the index)
to reject far-apart candidates cheaply, then do the exact test only on
survivors. `ST_Distance < x` cannot use the index that way - prefer
`ST_DWithin`.

```mermaid
graph TD
    ST["ST functions"] --> M["Measurements"]
    ST --> R["Relationship predicates"]
    M --> DIST["ST Distance ST Length ST Area"]
    R --> INT["ST Intersects"]
    R --> CON["ST Contains and ST Within"]
    R --> DW["ST DWithin index assisted"]
    DW --> FAST["Fast within a distance query"]
```

Remember: measure with `ST_Distance`/`ST_Area`, test overlap with
`ST_Intersects`/`ST_Contains`, and always express "within N metres" as
`ST_DWithin` so the spatial index can help.
""",
        ),
        quiz_lesson(
            "Quiz: Spatial SQL: measurements and relationships",
            (
                q(
                    "What does ST_Intersects(a, b) return?",
                    (
                        opt("The distance between a and b"),
                        opt("A new geometry of the overlap"),
                        opt(
                            "A boolean - true if the two geometries share at least one point",
                            correct=True,
                        ),
                        opt("The area of a"),
                    ),
                    "ST_Intersects is a relationship predicate returning true/false; it "
                    "is the most common spatial filter.",
                ),
                q(
                    "Why prefer ST_DWithin(a, b, 500) over ST_Distance(a, b) < 500?",
                    (
                        opt("ST_DWithin is more precise"),
                        opt(
                            "ST_DWithin is index-assisted - it uses the bounding-box "
                            "index to reject far candidates cheaply; ST_Distance < x "
                            "cannot",
                            correct=True,
                        ),
                        opt("ST_Distance does not exist in PostGIS"),
                        opt("They behave identically in every way"),
                    ),
                    "ST_DWithin can exploit the GiST index; a comparison on ST_Distance "
                    "forces a full computation on every row.",
                ),
                q(
                    "Which function measures the shortest distance between two geometries?",
                    (
                        opt("ST_Contains"),
                        opt("ST_Distance", correct=True),
                        opt("ST_Intersects"),
                        opt("ST_AsGeoJSON"),
                    ),
                    "ST_Distance returns the minimum distance; units are CRS units for "
                    "geometry and metres for geography.",
                ),
            ),
        ),
        # -- 4. Spatial joins and aggregation --------------------------
        _t(
            "Spatial joins and aggregation",
            "11 min",
            """# Spatial joins and aggregation

A **spatial join** combines two tables not on a shared key but on a
**spatial relationship** - the join condition is a predicate like
`ST_Intersects` or `ST_Contains`. This is how you overlay layers: assign
each point to the polygon that contains it, or find every road crossing a
flood zone.

Count how many crimes fell inside each police precinct - a classic
point-in-polygon join followed by aggregation:

```sql
SELECT p.name,
       COUNT(c.id) AS crime_count
FROM precincts p
LEFT JOIN crimes c
       ON ST_Contains(p.geom, c.geom)   -- spatial join predicate
GROUP BY p.name
ORDER BY crime_count DESC;
```

The `LEFT JOIN` keeps precincts with zero crimes; the `ST_Contains`
condition is what makes it a spatial join. With a GiST index on
`crimes.geom` (next lesson), the planner uses a **nested-loop join** that
probes the index per precinct - fast even for millions of points.

Beyond joining, PostGIS has **spatial aggregate** functions that combine
many geometries into one:

- **`ST_Union(geom)`** - dissolve many geometries into one (merge all
  parcels of a zoning class into a single multipolygon).
- **`ST_Collect(geom)`** - gather geometries into a collection without
  dissolving boundaries (faster than union).
- **`ST_Extent(geom)`** - the bounding box of a whole set of rows.

Dissolve neighbourhoods into their boroughs:

```sql
SELECT borough,
       ST_Union(geom) AS borough_geom,   -- dissolve shared borders
       SUM(population) AS total_pop
FROM neighbourhoods
GROUP BY borough;
```

```mermaid
graph TD
    A["Points layer crimes"] --> J["Spatial join ST Contains"]
    B["Polygons layer precincts"] --> J
    J --> G["GROUP BY precinct"]
    G --> AGG["COUNT and SUM per area"]
    B --> U["ST Union dissolve"]
    U --> BOR["Merged boroughs"]
```

Remember: a spatial join uses a relationship predicate as the join
condition to overlay layers; combine it with `GROUP BY` and spatial
aggregates like `ST_Union` to summarize data by area.
""",
        ),
        quiz_lesson(
            "Quiz: Spatial joins and aggregation",
            (
                q(
                    "What makes a join a 'spatial join'?",
                    (
                        opt("It joins more than two tables"),
                        opt(
                            "The join condition is a spatial relationship predicate (such "
                            "as ST_Contains or ST_Intersects) rather than a shared key",
                            correct=True,
                        ),
                        opt("It always uses a full table scan"),
                        opt("It can only join a table to itself"),
                    ),
                    "A spatial join relates rows by geometry - e.g. each point to the "
                    "polygon that contains it - not by matching column values.",
                ),
                q(
                    "What does ST_Union do as an aggregate?",
                    (
                        opt("Counts the rows"),
                        opt(
                            "Dissolves many input geometries into a single merged geometry",
                            correct=True,
                        ),
                        opt("Splits a geometry into pieces"),
                        opt("Returns the distance between geometries"),
                    ),
                    "ST_Union merges geometries, dissolving shared boundaries; "
                    "ST_Collect gathers them without dissolving.",
                ),
                q(
                    "In the crimes-per-precinct query, why use LEFT JOIN instead of an inner join?",
                    (
                        opt("It runs faster in all cases"),
                        opt(
                            "So precincts with zero crimes still appear in the result "
                            "with a count of 0",
                            correct=True,
                        ),
                        opt("Inner joins cannot use spatial predicates"),
                        opt("It avoids the need for GROUP BY"),
                    ),
                    "An inner join would drop precincts that contain no crimes; LEFT "
                    "JOIN keeps them with a zero count.",
                ),
            ),
        ),
        # -- 5. GiST indexing ------------------------------------------
        _t(
            "Spatial indexing with GiST",
            "11 min",
            """# Spatial indexing with GiST

Without an index, a spatial query must test **every row** - compute the
relationship against all geometries. On large tables that is far too
slow. The fix is a **spatial index**, and in PostGIS that means a
**GiST** (Generalized Search Tree) index.

A B-tree cannot index geometry usefully - there is no linear ordering of
shapes. GiST instead builds a tree over each geometry's **bounding box**
(its minimum bounding rectangle). It is an **R-tree-like** structure:
nearby boxes are grouped into parent boxes, recursively, so a query can
descend the tree and prune whole branches that cannot possibly match.

Create one on a geometry column:

```sql
CREATE INDEX idx_crimes_geom ON crimes USING GIST (geom);
ANALYZE crimes;   -- refresh planner statistics after building
```

The key idea is the **two-phase filter**:

1. **Index (bounding-box) filter** - the GiST index quickly returns
   candidate rows whose bounding box overlaps the query box. This is
   cheap and eliminates almost everything.
2. **Exact filter** - PostGIS runs the precise predicate
   (`ST_Intersects`, `ST_Contains`, ...) only on the surviving
   candidates.

Predicates such as `ST_Intersects`, `ST_Contains` and `ST_DWithin`
automatically use the index for phase one. The bounding-box overlap
operator is **`&&`**, and it is what the index accelerates under the hood:

```sql
-- && tests bounding-box overlap using the GiST index directly
SELECT COUNT(*) FROM crimes
WHERE geom && ST_MakeEnvelope(-46.7, -23.6, -46.6, -23.5, 4326);
```

For `geography` columns you also create a GiST index; the same two-phase
approach applies. After large data loads, run `ANALYZE` (or let autovacuum
do it) so the planner knows the table is big enough to prefer the index.

```mermaid
graph TD
    Q["Spatial query"] --> IDX["GiST index bounding boxes"]
    IDX --> CAND["Candidate rows boxes overlap"]
    CAND --> EXACT["Exact predicate ST Intersects"]
    EXACT --> RES["Matching rows"]
    NOIDX["No index"] --> SCAN["Test every row slow"]
```

Remember: geometry needs a **GiST** index, not a B-tree; it works on
bounding boxes and drives a two-phase filter - cheap box overlap first,
exact test on the few survivors - which is what makes spatial queries
scale.
""",
        ),
        quiz_lesson(
            "Quiz: Spatial indexing with GiST",
            (
                q(
                    "Why can't a normal B-tree index a geometry column usefully?",
                    (
                        opt("Geometries are too large to store"),
                        opt(
                            "There is no meaningful linear ordering of 2D shapes; GiST "
                            "instead indexes bounding boxes in an R-tree-like structure",
                            correct=True,
                        ),
                        opt("B-trees only work on text"),
                        opt("PostGIS forbids B-trees entirely"),
                    ),
                    "Spatial data has no single sort order, so PostGIS uses a GiST "
                    "(R-tree-like) index over bounding boxes.",
                ),
                q(
                    "What are the two phases of an index-assisted spatial query?",
                    (
                        opt("Sort then merge"),
                        opt(
                            "A cheap bounding-box index filter to get candidates, then "
                            "the exact predicate run only on those candidates",
                            correct=True,
                        ),
                        opt("Encrypt then decrypt"),
                        opt("Backup then restore"),
                    ),
                    "Phase one uses the GiST box index to prune; phase two runs the "
                    "precise ST_ test on the survivors.",
                ),
                q(
                    "How do you create a spatial index on crimes.geom?",
                    (
                        opt("CREATE INDEX ON crimes (geom)  -- default B-tree"),
                        opt("CREATE INDEX idx ON crimes USING GIST (geom)", correct=True),
                        opt("CREATE SPATIAL TABLE crimes"),
                        opt("ALTER TABLE crimes ADD INDEX geom"),
                    ),
                    "USING GIST builds the spatial index; remember to ANALYZE afterward "
                    "so the planner has fresh statistics.",
                ),
            ),
        ),
        # -- 6. Query performance --------------------------------------
        _t(
            "Query performance and EXPLAIN ANALYZE",
            "11 min",
            """# Query performance and EXPLAIN ANALYZE

Having an index is not the same as **using** it. The way to know what
PostgreSQL actually does is **`EXPLAIN ANALYZE`**, which runs the query
and prints the real execution plan with timings and row counts.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT p.name, COUNT(c.id)
FROM precincts p
JOIN crimes c ON ST_Contains(p.geom, c.geom)
GROUP BY p.name;
```

Read the plan from the **inside out**. The signals that matter:

- **`Index Scan` / `Bitmap Index Scan`** using your GiST index on
  `geom` - good, the index is doing its job.
- **`Seq Scan`** on a big spatial table inside a spatial filter - a
  warning: the index is being skipped.
- **Estimated vs actual rows** - if the planner estimates 5 rows but
  gets 5 million, its statistics are stale. Run **`ANALYZE`**.
- **Actual time** and **loops** - a nested loop that runs millions of
  times signals a missing or unused index on the inner table.

Common causes of a slow spatial query and their fixes:

- **No GiST index** on the geometry being filtered -> create one.
- **Function wrapping the indexed column**, e.g.
  `ST_Distance(geom, ...) < 500` -> rewrite as `ST_DWithin(geom, ..., 500)`
  so the index applies.
- **Mixed SRIDs**, forcing an implicit transform per row -> store all
  layers in the same SRID, or index on a transformed column.
- **Stale statistics after a bulk load** -> `ANALYZE` the table.

You can also cache an expensive reprojection with an
**expression index**, or precompute it as a **generated column**:

```sql
-- index the reprojected geometry so filters in metres use the index
CREATE INDEX idx_crimes_utm
ON crimes USING GIST (ST_Transform(geom, 32723));
```

Cluster physically-nearby rows together and keep the cache warm; for very
large tables also consider **partitioning** by region or time.

```mermaid
graph TD
    SLOW["Slow spatial query"] --> EXP["EXPLAIN ANALYZE"]
    EXP --> SEQ{"Seq Scan on geom"}
    SEQ -->|"yes"| FIX["Add GiST index or rewrite predicate"]
    SEQ -->|"no"| STAT{"Estimates far off"}
    STAT -->|"yes"| AN["Run ANALYZE"]
    STAT -->|"no"| OK["Plan is healthy"]
```

Remember: `EXPLAIN ANALYZE` shows the truth. Look for an index scan on
the geometry column, keep statistics fresh with `ANALYZE`, avoid wrapping
the indexed column in a function, and keep SRIDs consistent.
""",
        ),
        quiz_lesson(
            "Quiz: Query performance and EXPLAIN ANALYZE",
            (
                q(
                    "What does EXPLAIN ANALYZE give you that plain EXPLAIN does not?",
                    (
                        opt("Nothing; they are identical"),
                        opt(
                            "It actually runs the query and reports real timings and row "
                            "counts alongside the plan",
                            correct=True,
                        ),
                        opt("It rewrites the query for you"),
                        opt("It creates the missing index automatically"),
                    ),
                    "EXPLAIN estimates; EXPLAIN ANALYZE executes and shows actual time, "
                    "rows and loops so you can compare with the estimates.",
                ),
                q(
                    "You see a Seq Scan on a large table inside a spatial filter. What is likely wrong?",
                    (
                        opt("The query is optimal; Seq Scan is always best"),
                        opt(
                            "The GiST index is missing or not being used - add one, or "
                            "rewrite a predicate that wraps the indexed column",
                            correct=True,
                        ),
                        opt("PostGIS is not installed"),
                        opt("The table has too few rows to matter"),
                    ),
                    "A sequential scan on a big spatial table signals the index is "
                    "absent or defeated (e.g. ST_Distance(...) < x instead of ST_DWithin).",
                ),
                q(
                    "The planner estimates 5 rows but the query actually returns millions. What should you do first?",
                    (
                        opt("Drop the index"),
                        opt("Restart the database"),
                        opt(
                            "Run ANALYZE to refresh the table statistics the planner relies on",
                            correct=True,
                        ),
                        opt("Rewrite the app in another language"),
                    ),
                    "Wildly wrong estimates mean stale statistics, common after a bulk "
                    "load; ANALYZE updates them so the planner chooses well.",
                ),
            ),
        ),
        # -- 7. Raster in the database ---------------------------------
        _t(
            "Raster in the database and tiling",
            "10 min",
            """# Raster in the database and tiling

So far everything has been **vector** - points, lines, polygons. PostGIS
also stores **raster** data: gridded pixels such as elevation models,
satellite imagery, or temperature surfaces. Enable it with a second
extension:

```sql
CREATE EXTENSION IF NOT EXISTS postgis_raster;
```

The key idea for scale is **tiling**. You never store one giant raster in
a single row; you cut it into many small **tiles** (for example 256 x 256
pixels), one per row, each with its own bounding box. A GiST index on the
tile footprints then lets a query touch only the tiles that overlap the
area of interest - the same box-pruning that makes vector queries fast.

The command-line loader `raster2pgsql` tiles and imports in one step:

```text
# tile a GeoTIFF into 256x256 blocks, build overviews, create a GiST index
raster2pgsql -s 4326 -t 256x256 -I -C -l 2,4 dem.tif public.dem \\
  | psql -d gis
#   -t 256x256  tile size      -I  spatial index
#   -l 2,4      overview levels -C  apply raster constraints
```

Once loaded, you query rasters with `ST_` raster functions, and crucially
you can **combine raster and vector**. Sample the elevation at a set of
points, or clip a raster to a polygon:

```sql
-- elevation (band 1) at each station point, from the DEM tiles
SELECT s.name,
       ST_Value(d.rast, 1, s.geom) AS elevation_m
FROM stations s
JOIN dem d ON ST_Intersects(d.rast, s.geom);   -- only overlapping tiles
```

**Overviews** are pre-reduced, lower-resolution copies (the `-l 2,4`
above): when a map is zoomed out you read a coarse overview instead of
full-resolution tiles, saving huge amounts of work - the raster analogue
of a pyramid.

```mermaid
graph TD
    TIF["Large GeoTIFF"] --> LOAD["raster2pgsql tiling"]
    LOAD --> TILES["Many small tiles one per row"]
    TILES --> IDX["GiST index on tile footprints"]
    TILES --> OV["Overviews coarse copies"]
    IDX --> Q["Query touches overlapping tiles only"]
    OV --> ZOOM["Zoomed out reads coarse overview"]
```

Remember: store rasters as many small indexed **tiles** with
**overviews**, load them with `raster2pgsql`, and mix raster with vector
using functions like `ST_Value` and `ST_Clip` - so gridded data scales
the same way vector data does.
""",
        ),
        quiz_lesson(
            "Quiz: Raster in the database and tiling",
            (
                q(
                    "Why is a large raster stored as many small tiles rather than one big row?",
                    (
                        opt("Because PostGIS cannot store large values"),
                        opt(
                            "So a GiST index on tile footprints lets a query read only "
                            "the tiles overlapping the area of interest",
                            correct=True,
                        ),
                        opt("Tiles use less coordinate precision"),
                        opt("It is required by the SQL standard"),
                    ),
                    "Tiling plus a spatial index on the footprints means queries touch "
                    "only relevant tiles - the same box-pruning as vector data.",
                ),
                q(
                    "What are raster 'overviews'?",
                    (
                        opt("Text descriptions of each tile"),
                        opt(
                            "Pre-computed lower-resolution copies read when zoomed out, "
                            "to avoid processing full-resolution tiles",
                            correct=True,
                        ),
                        opt("Backups of the original file"),
                        opt("The list of SRIDs in use"),
                    ),
                    "Overviews are a resolution pyramid; coarse copies serve zoomed-out "
                    "views cheaply, like image pyramids.",
                ),
                q(
                    "Which tool tiles and loads a GeoTIFF into a PostGIS raster table?",
                    (
                        opt("pg_dump"),
                        opt("raster2pgsql", correct=True),
                        opt("ST_Union"),
                        opt("EXPLAIN ANALYZE"),
                    ),
                    "raster2pgsql cuts the raster into tiles, can build overviews and a "
                    "GiST index, and pipes the SQL into psql.",
                ),
            ),
        ),
        # -- 8. Serving spatial data -----------------------------------
        _t(
            "Serving spatial data with pg_tileserv and vector tiles",
            "10 min",
            """# Serving spatial data with pg_tileserv and vector tiles

Data in PostGIS eventually needs to reach a **map in a browser**. Sending
raw geometry as GeoJSON works for small layers, but for large datasets the
modern approach is **vector tiles**: the map is divided into a pyramid of
tiles (by zoom / x / y), and each tile carries only the features in its
area, compactly encoded in the **Mapbox Vector Tile (MVT)** format
(protobuf). The client requests only the tiles it needs at its current
zoom and pan.

PostGIS can generate MVT **directly in SQL** with `ST_AsMVT` and
`ST_AsMVTGeom`, which clips and encodes geometry into a tile's coordinate
space:

```sql
-- build one vector tile (z, x, y) of the roads layer
WITH bounds AS (SELECT ST_TileEnvelope(12, 1205, 2196) AS geom)
SELECT ST_AsMVT(t, 'roads')       -- encode as an MVT layer named roads
FROM (
  SELECT id, name,
         ST_AsMVTGeom(ST_Transform(r.geom, 3857), b.geom) AS geom
  FROM roads r, bounds b
  WHERE ST_Intersects(ST_Transform(r.geom, 3857), b.geom)
) AS t;
```

Writing that per request is tedious, so tools automate it. **`pg_tileserv`**
is a tiny stateless service that inspects your tables and **publishes each
as a vector-tile endpoint** automatically, calling `ST_AsMVT` for you:

```text
# point it at the database and it serves /{schema}.{table}/{z}/{x}/{y}.pbf
export DATABASE_URL=postgres://user:pass@localhost/gis
./pg_tileserv
# a web map then requests tiles like /public.roads/12/1205/2196.pbf
```

Its sibling **`pg_featureserv`** publishes tables as **OGC API - Features**
(GeoJSON) for feature-level access. Both are thin layers over the same
PostGIS functions - the database does the spatial work.

```mermaid
graph LR
    DB["PostGIS tables"] --> SRV["pg tileserv"]
    SRV --> MVT["ST AsMVT vector tiles"]
    MVT --> Z["Tiles by zoom x y"]
    Z --> MAP["Web map client"]
    MAP --> REQ["Requests only visible tiles"]
    REQ --> SRV
```

Remember: serve large layers as **vector tiles** (MVT) built by
`ST_AsMVT`, let **pg_tileserv** publish tables as tile endpoints
automatically, and the client fetches only the tiles it can see - the
database stays the single source of truth.
""",
        ),
        quiz_lesson(
            "Quiz: Serving spatial data with pg_tileserv and vector tiles",
            (
                q(
                    "Why serve a large layer as vector tiles instead of one big GeoJSON response?",
                    (
                        opt("GeoJSON cannot store polygons"),
                        opt(
                            "Tiles let the client fetch only the features in its current "
                            "view at its zoom, in a compact encoding - scaling to huge layers",
                            correct=True,
                        ),
                        opt("Vector tiles are required by SQL"),
                        opt("GeoJSON only works offline"),
                    ),
                    "Vector tiles partition data by zoom/x/y so the client transfers "
                    "only what is visible, unlike shipping the whole layer at once.",
                ),
                q(
                    "What does the ST_AsMVT function do?",
                    (
                        opt("Creates a GiST index"),
                        opt("Reprojects a raster"),
                        opt(
                            "Encodes a set of features into a Mapbox Vector Tile (MVT) "
                            "inside PostGIS",
                            correct=True,
                        ),
                        opt("Deletes a table"),
                    ),
                    "ST_AsMVT (with ST_AsMVTGeom to clip into tile space) produces the "
                    "protobuf MVT the map client consumes.",
                ),
                q(
                    "What does pg_tileserv do?",
                    (
                        opt("Edits geometries in place"),
                        opt(
                            "Inspects PostGIS tables and automatically publishes each as "
                            "a vector-tile endpoint, calling ST_AsMVT for you",
                            correct=True,
                        ),
                        opt("Replaces PostgreSQL"),
                        opt("Stores rasters as tiles"),
                    ),
                    "pg_tileserv is a thin, stateless tile server over PostGIS; "
                    "pg_featureserv is its OGC API - Features (GeoJSON) sibling.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is PostGIS?",
                    (
                        opt("A standalone GIS desktop application"),
                        opt(
                            "An extension that adds spatial types, ST_ functions and GiST "
                            "indexing to PostgreSQL",
                            correct=True,
                        ),
                        opt("A file format for satellite imagery"),
                        opt("A JavaScript mapping library"),
                    ),
                    "PostGIS turns PostgreSQL into a spatial database, following the OGC "
                    "Simple Features standard.",
                ),
                q(
                    "When should you use the geography type instead of geometry?",
                    (
                        opt("Never; geometry is always better"),
                        opt(
                            "For global lon/lat data where you need accurate distances "
                            "and areas on the curved Earth (results in metres)",
                            correct=True,
                        ),
                        opt("Only for storing text labels"),
                        opt("When you have no coordinate system"),
                    ),
                    "geography computes on the spheroid so lon/lat distances are correct "
                    "in metres; geometry is fast planar math for projected data.",
                ),
                q(
                    "In PostGIS geometry, which coordinate comes first?",
                    (
                        opt("Latitude"),
                        opt("Longitude (X, Y = lon, lat)", correct=True),
                        opt("Elevation"),
                        opt("It is random"),
                    ),
                    "ST_MakePoint(lon, lat) - longitude before latitude; swapping them "
                    "misplaces every point.",
                ),
                q(
                    "Which query correctly finds features within 500 metres and can use the index?",
                    (
                        opt("WHERE ST_Distance(geom, p) < 500"),
                        opt("WHERE ST_DWithin(geom::geography, p::geography, 500)", correct=True),
                        opt("WHERE ST_Area(geom) < 500"),
                        opt("WHERE geom = p"),
                    ),
                    "ST_DWithin is index-assisted and expresses 'within a distance'; a "
                    "comparison on ST_Distance defeats the index.",
                ),
                q(
                    "What is a spatial join?",
                    (
                        opt("A join on a shared primary key"),
                        opt(
                            "A join whose condition is a spatial relationship predicate, "
                            "like ST_Contains, used to overlay layers",
                            correct=True,
                        ),
                        opt("A join that always produces a Cartesian product"),
                        opt("A way to merge two databases"),
                    ),
                    "Spatial joins relate rows by geometry - e.g. each point to its "
                    "containing polygon - not by matching keys.",
                ),
                q(
                    "What kind of index accelerates spatial queries in PostGIS?",
                    (
                        opt("A B-tree on the geometry"),
                        opt("A hash index"),
                        opt(
                            "A GiST index over the geometries' bounding boxes (R-tree-like)",
                            correct=True,
                        ),
                        opt("No index is possible"),
                    ),
                    "GiST indexes bounding boxes and drives the cheap box-overlap first "
                    "phase of spatial filtering.",
                ),
                q(
                    "In an index-assisted spatial query, what happens in the two phases?",
                    (
                        opt("Compile then run"),
                        opt(
                            "A cheap bounding-box index filter returns candidates, then "
                            "the exact predicate runs only on those candidates",
                            correct=True,
                        ),
                        opt("Encrypt then transmit"),
                        opt("Sort then deduplicate"),
                    ),
                    "Box overlap via the GiST index prunes almost everything; the "
                    "precise ST_ test runs on the few survivors.",
                ),
                q(
                    "You run EXPLAIN ANALYZE and see a Seq Scan on a huge spatial table. What is the usual fix?",
                    (
                        opt("Add more RAM only"),
                        opt(
                            "Create a GiST index on the geometry, and/or rewrite a "
                            "predicate that wraps the indexed column so the index applies",
                            correct=True,
                        ),
                        opt("Delete half the rows"),
                        opt("Nothing - Seq Scan is optimal for spatial data"),
                    ),
                    "A sequential scan inside a spatial filter means the index is missing "
                    "or defeated; add it and keep predicates index-friendly.",
                ),
                q(
                    "How are large rasters stored efficiently in PostGIS?",
                    (
                        opt("As one enormous row"),
                        opt(
                            "As many small tiles (one per row) with a GiST index on their "
                            "footprints and overviews for zoomed-out views",
                            correct=True,
                        ),
                        opt("As plain text"),
                        opt("They cannot be stored at all"),
                    ),
                    "postgis_raster stores tiled, indexed rasters; raster2pgsql loads "
                    "them with overviews so queries touch only relevant tiles.",
                ),
                q(
                    "What is the role of ST_AsMVT and pg_tileserv when serving data to a web map?",
                    (
                        opt("They reproject rasters to WGS84"),
                        opt(
                            "ST_AsMVT encodes features as vector tiles in SQL; pg_tileserv "
                            "publishes tables as tile endpoints so clients fetch only "
                            "visible tiles",
                            correct=True,
                        ),
                        opt("They compress the whole database into one file"),
                        opt("They replace the need for PostgreSQL"),
                    ),
                    "Vector tiles (MVT) let the client request only what it can see; "
                    "pg_tileserv automates the ST_AsMVT calls over your tables.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SPATIAL_DATABASES_POSTGIS_COURSES: tuple[SeedCourse, ...] = (_SPATIAL_DATABASES_POSTGIS,)
