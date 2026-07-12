"""Academy seed content - Web GIS Development.

Putting maps on the web: how web mapping is built from tiled imagery, the
XYZ tiling scheme and Web Mercator projection, slippy-map JavaScript
libraries (Leaflet, OpenLayers), vector tiles and MapLibre GL, GeoJSON
and client-side data, the OGC web services (WMS, WFS, WMTS), tile servers
and styling, and how it all assembles into an interactive web map
application. Every lesson is a direct explanation with a concrete code or
data example and a mermaid diagram, followed by a checkpoint quiz; the
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


_WEB_GIS_DEVELOPMENT = SeedCourse(
    slug="web-gis-development",
    title="Web GIS Development",
    description=(
        "Putting maps on the web: tiling and web mapping libraries (Leaflet, "
        "OpenLayers, MapLibre), vector tiles, and OGC web services (WMS, WFS, "
        "WMTS) for interactive geospatial applications. Every lesson pairs a "
        "direct explanation with a real code or data example and a diagram, "
        "grounded in Web Mercator, XYZ tiles, GeoJSON and the OGC standards."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Web GIS Development

A **web map** is a map you pan and zoom in a browser. Behind that simple
experience sits a stack: pre-cut image or vector **tiles**, a projection
that makes tiling work (**Web Mercator**), a JavaScript **mapping
library** that stitches tiles into a smooth slippy map, data formats like
**GeoJSON**, and server-side standards from the **OGC** (WMS, WFS, WMTS)
that publish maps and features. This course walks that stack end to end.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short real example (a tile URL, a Leaflet
snippet, a GeoJSON fragment, a WMS request), and draws the idea as a
diagram. After each lesson there is a short quiz; at the end, a final quiz
covers the whole course.

What you will build understanding for, in order:

1. **Web mapping architecture and tiles** - why maps are cut into tiles
2. **The XYZ tiling scheme and Web Mercator** - the z/x/y grid and EPSG:3857
3. **Slippy map libraries** - Leaflet and OpenLayers
4. **Vector tiles and MapLibre GL** - data-driven, GPU-rendered maps
5. **GeoJSON and client-side data** - drawing your own features
6. **OGC web services** - WMS, WFS, WMTS interoperability standards
7. **Tile servers and styling** - producing and styling the tiles
8. **Building an interactive web map application** - assembling the whole

This is the map of the territory. By the end you will be able to read a
tile URL, choose a library, load your own data, consume an OGC service,
and reason about how a production web map fits together.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is a 'web map' in the sense this course means?",
                    (
                        opt("A static image of a map emailed as a PDF"),
                        opt(
                            "An interactive map you pan and zoom in a browser, built "
                            "from tiles, a mapping library and geospatial data",
                            correct=True,
                        ),
                        opt("A paper atlas scanned at high resolution"),
                        opt("A GPS device you carry in the field"),
                    ),
                    "Web GIS is about interactive, tiled, browser-based maps served "
                    "from standard formats and services.",
                ),
                q(
                    "How is each content lesson structured?",
                    (
                        opt("A long lecture with no examples"),
                        opt(
                            "A direct explanation, one concrete example (tile URL, code "
                            "snippet, or data fragment) and a diagram, then a quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("Video only, no text"),
                    ),
                    "Each lesson pairs a clear explanation with a real example and a "
                    "mermaid diagram, followed by a checkpoint quiz.",
                ),
            ),
        ),
        # -- 1. Web mapping architecture and tiles ---------------------
        _t(
            "Web mapping architecture and tiles",
            "9 min",
            """# Web mapping architecture and tiles

A world map at street-level detail is billions of pixels - far too big to
send to a browser at once. The solution that made modern web maps
possible (Google Maps, 2005) is **tiling**: the map is pre-cut into small,
fixed-size square images, typically **256 by 256 pixels**, arranged in a
grid at each zoom level. The browser only ever downloads the handful of
tiles that cover the current view.

This is why panning a web map feels seamless: as you drag, the library
requests the newly exposed tiles and drops the ones that scroll off
screen. Each tile has a stable address, so it can be **cached** anywhere
between the server and the browser (CDN, proxy, disk) and reused across
users. Pre-rendered tiles move the heavy cartography work to build time,
not request time.

The pieces of a web mapping stack:

- **Tile source** - a server (or static file store) that returns a tile
  image for a given address.
- **Mapping library** - JavaScript in the browser that computes which
  tiles the current view needs, fetches them, and positions them.
- **Base layers and overlays** - a background basemap plus your own data
  drawn on top.

A tile request follows a simple path:

```text
Browser view: center + zoom
  -> library computes needed tile addresses
  -> GET https://tiles.example.com/12/1205/1539.png
  -> CDN/cache hit? return; else origin renders and caches
  -> library places each 256x256 tile in the grid
```

```mermaid
graph LR
    VIEW["Map view center and zoom"] --> CALC["Library computes tile list"]
    CALC --> REQ["Request each tile by address"]
    REQ --> CACHE["CDN or cache"]
    CACHE --> ORIGIN["Tile server renders"]
    CACHE --> GRID["Place tiles in grid"]
    ORIGIN --> GRID
```

Remember: web maps are fast because the map is pre-cut into small,
cacheable, individually addressable tiles - the browser fetches only what
the current view needs.
""",
        ),
        quiz_lesson(
            "Quiz: Web mapping architecture and tiles",
            (
                q(
                    "Why are web maps cut into tiles instead of served as one big image?",
                    (
                        opt("Because browsers cannot display PNG files"),
                        opt(
                            "A full-detail world map is far too large to send at once; "
                            "tiles let the browser fetch only the small squares the "
                            "current view needs",
                            correct=True,
                        ),
                        opt("To make the map lower quality on purpose"),
                        opt("Because tiles are required by HTML"),
                    ),
                    "Tiling downloads only the visible area and enables caching, which "
                    "is what makes panning and zooming feel fast.",
                ),
                q(
                    "What is the typical size of a single map tile?",
                    (
                        opt("16 by 16 pixels"),
                        opt("256 by 256 pixels", correct=True),
                        opt("1920 by 1080 pixels"),
                        opt("One tile equals the whole world"),
                    ),
                    "The de facto standard tile is a 256x256 square (some retina "
                    "schemes use 512), arranged in a grid per zoom level.",
                ),
                q(
                    "Why does giving each tile a stable address matter?",
                    (
                        opt("It makes the tiles bigger"),
                        opt(
                            "A stable address lets tiles be cached in CDNs and browsers "
                            "and reused across users, avoiding re-rendering",
                            correct=True,
                        ),
                        opt("It encrypts the map"),
                        opt("It has no effect on performance"),
                    ),
                    "Stable, deterministic tile addresses are what make caching and "
                    "reuse possible across the whole delivery path.",
                ),
            ),
        ),
        # -- 2. XYZ tiling scheme and Web Mercator ---------------------
        _t(
            "The XYZ tiling scheme and Web Mercator",
            "10 min",
            """# The XYZ tiling scheme and Web Mercator

For tiles to line up into a seamless grid, the world must first be
flattened into a **square** that subdivides cleanly. That projection is
**Web Mercator**, code **EPSG:3857** (also seen as 900913). It maps the
Earth onto a square from roughly -85.06 to +85.06 degrees latitude (the
poles would stretch to infinity, so they are cut off). Coordinates are
stored in metres on this square, while your data is usually in longitude
and latitude, **EPSG:4326** (WGS84). The library converts between them.

On top of Web Mercator sits the **XYZ tiling scheme**. At **zoom 0** the
whole world is one tile. Each zoom level **doubles** the grid in each
direction: zoom z has a 2^z by 2^z grid, so 4^z tiles total. A tile is
addressed by three integers:

- **z** - the zoom level (0 = whole world, higher = more detail).
- **x** - the column, counting from 0 at the west (left) edge.
- **y** - the row, counting from 0 at the **north** (top) edge in the
  common XYZ/Google scheme. (The TMS scheme flips y to count from the
  south - a frequent source of upside-down tiles.)

The canonical URL template is:

```text
https://tile.example.com/{z}/{x}/{y}.png

zoom 0:  1 tile      (2^0 x 2^0)
zoom 1:  4 tiles     (2^1 x 2^1)
zoom 2: 16 tiles     (2^2 x 2^2)
zoom z: 2^z x 2^z    (4^z tiles total)

To convert lon/lat (degrees) to tile x/y at zoom z:
  n = 2^z
  x = floor( (lon + 180) / 360 * n )
  y = floor( (1 - ln(tan(lat_rad) + sec(lat_rad)) / pi) / 2 * n )
```

```mermaid
graph TD
    LONLAT["Lon lat in EPSG 4326"] --> PROJ["Project to Web Mercator 3857"]
    PROJ --> ZOOM["Pick zoom level z"]
    ZOOM --> GRID["Grid is 2 to the z squared"]
    GRID --> ADDR["Address tile by z x y"]
    ADDR --> URL["Fill z x y into tile URL"]
```

Remember: Web Mercator (EPSG:3857) makes the world a square, and the XYZ
scheme addresses every tile by z/x/y where each zoom doubles the grid -
watch the y-origin (top for XYZ, bottom for TMS).
""",
        ),
        quiz_lesson(
            "Quiz: The XYZ tiling scheme and Web Mercator",
            (
                q(
                    "Which projection do standard web map tiles use, and what is its code?",
                    (
                        opt("Plate Carree, EPSG:4326"),
                        opt("Web Mercator, EPSG:3857", correct=True),
                        opt("UTM zone 31N, EPSG:32631"),
                        opt("A globe, no projection"),
                    ),
                    "Web Mercator (EPSG:3857) flattens the world into a square that "
                    "subdivides cleanly into the XYZ tile grid.",
                ),
                q(
                    "In the XYZ scheme, how many tiles cover the world at zoom level z?",
                    (
                        opt("Always exactly 256"),
                        opt("z times 2"),
                        opt("2^z by 2^z, which is 4^z tiles total", correct=True),
                        opt("It is constant at every zoom"),
                    ),
                    "Zoom 0 is one tile; each level doubles the grid in each axis, so "
                    "zoom z has a 2^z by 2^z grid.",
                ),
                q(
                    "A common cause of upside-down tiles is what?",
                    (
                        opt("Using PNG instead of JPEG"),
                        opt(
                            "Confusing the XYZ y-origin (counted from the north/top) "
                            "with the TMS y-origin (counted from the south/bottom)",
                            correct=True,
                        ),
                        opt("Zooming in too far"),
                        opt("Using EPSG:4326 data"),
                    ),
                    "XYZ counts y from the top, TMS from the bottom; mixing them flips "
                    "the map vertically.",
                ),
                q(
                    "Why is Web Mercator cut off near +/-85 degrees latitude?",
                    (
                        opt("The data does not exist there"),
                        opt(
                            "In Mercator the poles project to infinity, so the map is "
                            "truncated to keep the world a finite square",
                            correct=True,
                        ),
                        opt("Browsers cannot render the poles"),
                        opt("To save tile storage at the equator"),
                    ),
                    "Mercator's y stretches without bound toward the poles, so the "
                    "square is clipped at about 85.06 degrees.",
                ),
            ),
        ),
        # -- 3. Slippy map libraries -----------------------------------
        _t(
            "Slippy map libraries (Leaflet, OpenLayers)",
            "10 min",
            """# Slippy map libraries (Leaflet, OpenLayers)

The interactive, draggable map is nicknamed a **slippy map**. You do not
build the tile math by hand - a JavaScript **mapping library** does it:
it tracks the view (center, zoom), computes the needed tile addresses,
fetches and positions tiles, handles panning and zooming, and draws your
overlays. Two long-established open-source libraries dominate:

- **Leaflet** - small (about 40 KB), simple, and beginner-friendly. Its
  API is a thin, readable wrapper over tile layers, markers and popups.
  Ideal for straightforward raster-tile maps with some data on top.
- **OpenLayers** - larger and more powerful. It handles many projections
  (not just Web Mercator), WMS/WMTS/WFS out of the box, vector layers,
  and advanced rendering. The choice when you need heavy GIS features.

A complete Leaflet map is famously short - a **tile layer** plus a marker:

```javascript
// Leaflet: a slippy map centred on London
const map = L.map('map').setView([51.505, -0.09], 13);

// raster basemap from an XYZ tile source (OpenStreetMap)
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'Map data OpenStreetMap contributors'
}).addTo(map);

// a marker with a popup
L.marker([51.505, -0.09]).addTo(map)
  .bindPopup('Central London')
  .openPopup();
```

Notice the tile URL uses the same **{z}/{x}/{y}** template from the last
lesson - the library substitutes the numbers for each visible tile. The
core concepts are shared across libraries: a **Map** object, one or more
**layers** (base tiles plus overlays), a **view** (center and zoom), and
**controls** (zoom buttons, attribution, scale).

```mermaid
graph TD
    MAP["Map object"] --> VIEW["View center and zoom"]
    MAP --> BASE["Base tile layer"]
    MAP --> OVER["Overlay layers"]
    MAP --> CTRL["Controls zoom and attribution"]
    BASE --> TILES["XYZ tile source"]
    OVER --> DATA["Markers and geometries"]
```

Remember: a slippy map library turns view state into tile requests and
handles interaction for you. Reach for **Leaflet** for simple, light
maps; **OpenLayers** when you need many projections and native OGC
support.
""",
        ),
        quiz_lesson(
            "Quiz: Slippy map libraries (Leaflet, OpenLayers)",
            (
                q(
                    "What does a slippy map library do for you?",
                    (
                        opt("It renders satellites in orbit"),
                        opt(
                            "It tracks the view, computes which tiles are needed, "
                            "fetches and positions them, and handles pan/zoom and "
                            "overlays",
                            correct=True,
                        ),
                        opt("It stores your database"),
                        opt("It only converts file formats"),
                    ),
                    "The library turns view state (center, zoom) into tile requests and "
                    "manages interaction and layers.",
                ),
                q(
                    "When would you pick OpenLayers over Leaflet?",
                    (
                        opt("When you want the smallest possible library"),
                        opt(
                            "When you need many projections and built-in WMS/WMTS/WFS "
                            "and advanced GIS features",
                            correct=True,
                        ),
                        opt("When you never load any data"),
                        opt("OpenLayers cannot show tiles"),
                    ),
                    "Leaflet is small and simple; OpenLayers is heavier but has native "
                    "multi-projection and OGC support.",
                ),
                q(
                    "In the Leaflet tile URL, what do {z}/{x}/{y} represent?",
                    (
                        opt("Red, green and blue colour channels"),
                        opt(
                            "The zoom level and the tile column and row - substituted "
                            "for each visible tile",
                            correct=True,
                        ),
                        opt("Latitude, longitude and altitude"),
                        opt("Three unrelated random numbers"),
                    ),
                    "They are the XYZ tile address; the library fills them in per tile "
                    "as you pan and zoom.",
                ),
            ),
        ),
        # -- 4. Vector tiles and MapLibre GL ---------------------------
        _t(
            "Vector tiles and MapLibre GL",
            "10 min",
            """# Vector tiles and MapLibre GL

Traditional **raster tiles** are pre-rendered pictures: the cartography is
baked in, so you cannot restyle them in the browser, and text does not
rotate cleanly. **Vector tiles** send the raw **geometry and attributes**
instead of a picture - roads as lines, buildings as polygons, places as
points - encoded compactly in the **Mapbox Vector Tile (MVT)** format
(protocol-buffer binary). The browser then draws them with the GPU using
**WebGL**.

Because the client has the actual data, vector tiles bring big
advantages:

- **Style at runtime** - change colours, widths, and which layers show
  without regenerating any tiles.
- **Smooth zoom and rotation** - geometry is drawn at any scale and angle;
  labels stay upright and crisp.
- **Smaller and sharper** - one vector tileset serves every zoom and
  looks crisp on high-density (retina) screens.
- **Interactivity** - features carry attributes, so hover and click can
  read real properties.

**MapLibre GL JS** is the leading open-source library for vector tiles
(a community fork of Mapbox GL JS). You give it a **style document** -
JSON that names the tile **sources** and the **layers** that paint them:

```json
{
  "version": 8,
  "sources": {
    "osm": {
      "type": "vector",
      "tiles": ["https://tiles.example.com/{z}/{x}/{y}.pbf"],
      "maxzoom": 14
    }
  },
  "layers": [
    { "id": "bg", "type": "background",
      "paint": { "background-color": "#f0f0e8" } },
    { "id": "roads", "type": "line", "source": "osm",
      "source-layer": "transportation",
      "paint": { "line-color": "#c88", "line-width": 1.5 } }
  ]
}
```

The tile URL still uses **{z}/{x}/{y}**, but ends in **.pbf** (or .mvt)
because the payload is vector data, not an image.

```mermaid
graph LR
    SRC["Vector tile source pbf"] --> DEC["Decode MVT geometry"]
    DEC --> STYLE["Apply style document"]
    STYLE --> GPU["Render with WebGL"]
    GPU --> INT["Interact hover and click"]
    STYLE --> RESTYLE["Restyle live no re render"]
```

Remember: vector tiles ship geometry plus attributes, not pixels, so the
client can restyle live, zoom and rotate smoothly, and read feature
properties - MapLibre GL renders them on the GPU from a JSON style.
""",
        ),
        quiz_lesson(
            "Quiz: Vector tiles and MapLibre GL",
            (
                q(
                    "What is the key difference between raster tiles and vector tiles?",
                    (
                        opt("Vector tiles are always larger files"),
                        opt(
                            "Raster tiles are pre-rendered images; vector tiles ship "
                            "geometry and attributes that the client draws and can "
                            "restyle",
                            correct=True,
                        ),
                        opt("Raster tiles carry attributes, vector tiles do not"),
                        opt("There is no difference"),
                    ),
                    "Vector tiles send data (MVT geometry) rather than a picture, "
                    "enabling client-side styling and interaction.",
                ),
                q(
                    "Which advantage comes from vector tiles carrying data rather than pixels?",
                    (
                        opt("They cannot be styled"),
                        opt(
                            "You can restyle colours and layers at runtime and read "
                            "feature attributes on hover or click - no re-rendering",
                            correct=True,
                        ),
                        opt("They only work at one zoom level"),
                        opt("They disable interactivity"),
                    ),
                    "Because the client has the geometry and attributes, styling and "
                    "interaction happen live in the browser.",
                ),
                q(
                    "What does a MapLibre GL style document define?",
                    (
                        opt("The server's database password"),
                        opt(
                            "The tile sources and the layers that paint them - colours, "
                            "widths and which features show",
                            correct=True,
                        ),
                        opt("The physical size of the monitor"),
                        opt("Only the map's title text"),
                    ),
                    "The style JSON names sources (where tiles come from) and layers "
                    "(how to paint each kind of feature).",
                ),
            ),
        ),
        # -- 5. GeoJSON and client-side data ---------------------------
        _t(
            "GeoJSON and client-side data",
            "10 min",
            """# GeoJSON and client-side data

Beyond the basemap, you draw **your own data**: store locations, a
delivery route, sensor readings. On the web the lingua franca for this is
**GeoJSON** (RFC 7946) - a plain JSON format for geographic features that
every mapping library reads directly.

GeoJSON building blocks:

- A **Geometry** has a `type` and `coordinates`. Types are `Point`,
  `LineString`, `Polygon`, and their `Multi...` variants.
- A **Feature** wraps one geometry plus a free-form `properties` object
  (its attributes - name, category, value).
- A **FeatureCollection** is an array of features - the usual top-level
  object you load.

The one rule that trips people up: GeoJSON coordinates are
**[longitude, latitude]** - **X, Y**, longitude first - and always in
**WGS84 (EPSG:4326)** decimal degrees. That is the opposite order from the
`[lat, lng]` many map APIs use for a center point, so mixing them lands
your points in the wrong hemisphere.

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": { "type": "Point", "coordinates": [-0.09, 51.505] },
      "properties": { "name": "Central London", "kind": "office" }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [[-0.09, 51.505], [-0.08, 51.51]]
      },
      "properties": { "name": "Short route" }
    }
  ]
}
```

Loading it is a one-liner, and you can style and bind popups from the
feature `properties`:

```javascript
// Leaflet: draw a GeoJSON FeatureCollection and label each feature
L.geoJSON(data, {
  onEachFeature: (feature, layer) =>
    layer.bindPopup(feature.properties.name)
}).addTo(map);
```

For large datasets, fetch GeoJSON over HTTP, or move to **vector tiles**
when there are too many features to send at once.

```mermaid
graph TD
    FC["FeatureCollection"] --> F["Feature"]
    F --> G["Geometry type and coordinates"]
    F --> P["Properties attributes"]
    G --> LNGLAT["Coordinates are lon lat WGS84"]
    P --> STYLE["Style and popups from properties"]
```

Remember: GeoJSON is the web's standard for features - FeatureCollection
of Features, each a geometry plus properties, with coordinates as
**[lon, lat]** in WGS84. Watch the axis order.
""",
        ),
        quiz_lesson(
            "Quiz: GeoJSON and client-side data",
            (
                q(
                    "In GeoJSON, what order are coordinates written in?",
                    (
                        opt("[latitude, longitude]"),
                        opt("[longitude, latitude] - X then Y", correct=True),
                        opt("[x, y, z, time]"),
                        opt("Any order the author prefers"),
                    ),
                    "GeoJSON is longitude-first ([lon, lat]) in WGS84 - the opposite of "
                    "the [lat, lng] many map centre APIs use.",
                ),
                q(
                    "What is the usual top-level object you load from GeoJSON?",
                    (
                        opt("A single Geometry with no attributes"),
                        opt(
                            "A FeatureCollection - an array of Features, each a geometry "
                            "plus a properties object",
                            correct=True,
                        ),
                        opt("A raster image"),
                        opt("A CSS stylesheet"),
                    ),
                    "FeatureCollection -> Features -> each has a geometry and free-form "
                    "properties.",
                ),
                q(
                    "Which coordinate reference system does standard GeoJSON assume?",
                    (
                        opt("Web Mercator EPSG:3857 in metres"),
                        opt("WGS84 EPSG:4326 in decimal degrees", correct=True),
                        opt("The local UTM zone"),
                        opt("Whatever the browser locale is"),
                    ),
                    "RFC 7946 GeoJSON is WGS84 longitude/latitude in decimal degrees; "
                    "the library reprojects to Web Mercator for display.",
                ),
            ),
        ),
        # -- 6. OGC web services ---------------------------------------
        _t(
            "OGC web services (WMS, WFS, WMTS)",
            "10 min",
            """# OGC web services (WMS, WFS, WMTS)

Not all map data is your own GeoJSON or a tidy XYZ tileset. Governments,
agencies and GIS platforms publish data through **OGC** (Open Geospatial
Consortium) standards - vendor-neutral protocols so any client can consume
any compliant server. Three are essential for the web:

- **WMS - Web Map Service.** The server renders the map and returns a
  **picture** for a requested bounding box, size and layers. You get an
  image you cannot restyle, but it is universal and simple. Every WMS
  supports **GetCapabilities** (what layers exist) and **GetMap** (draw
  this area).
- **WFS - Web Feature Service.** Returns the actual **vector features**
  (as GML or GeoJSON), which you can style, query and edit client-side -
  the data itself, not a picture.
- **WMTS - Web Map Tile Service.** Serves **pre-rendered tiles** on a
  fixed grid, like XYZ but with a formal OGC capabilities description. It
  is cacheable and fast, unlike the dynamic per-request WMS GetMap.

The quick way to choose: **WMS** = a rendered image on demand; **WFS** =
the raw features to work with; **WMTS** = cached tiles for speed.

A WMS GetMap request is just a URL with query parameters:

```text
https://ows.example.com/wms?
  SERVICE=WMS&
  VERSION=1.3.0&
  REQUEST=GetMap&
  LAYERS=topo:contours&
  CRS=EPSG:3857&
  BBOX=-14000,6700000,-13000,6710000&
  WIDTH=512&HEIGHT=512&
  FORMAT=image/png
```

The server draws the requested `LAYERS` inside `BBOX` in the given `CRS`
and returns a PNG. A WMTS request instead names a tile by
`TileMatrix/TileRow/TileCol` - the OGC equivalent of z/x/y.

```mermaid
graph TD
    CLIENT["Web map client"] --> WMS["WMS GetMap"]
    CLIENT --> WFS["WFS GetFeature"]
    CLIENT --> WMTS["WMTS GetTile"]
    WMS --> IMG["Rendered image"]
    WFS --> FEAT["Vector features GML or GeoJSON"]
    WMTS --> TILE["Pre rendered tile on a grid"]
```

Remember: the OGC standards make maps interoperable - **WMS** returns a
rendered image, **WFS** returns editable features, **WMTS** returns cached
tiles - and all describe themselves via **GetCapabilities**.
""",
        ),
        quiz_lesson(
            "Quiz: OGC web services (WMS, WFS, WMTS)",
            (
                q(
                    "What does a WMS GetMap request return?",
                    (
                        opt("The raw vector features as GeoJSON"),
                        opt(
                            "A rendered map image for the requested bounding box, layers and size",
                            correct=True,
                        ),
                        opt("A database dump"),
                        opt("A list of user accounts"),
                    ),
                    "WMS renders server-side and returns a picture; you cannot restyle "
                    "it client-side.",
                ),
                q(
                    "Which OGC service gives you the actual editable vector features?",
                    (
                        opt("WMS"),
                        opt("WFS - Web Feature Service", correct=True),
                        opt("WMTS"),
                        opt("None of them return features"),
                    ),
                    "WFS returns the features themselves (GML or GeoJSON), which you can "
                    "query, style and edit client-side.",
                ),
                q(
                    "How does WMTS differ from a dynamic WMS GetMap?",
                    (
                        opt("WMTS returns nothing"),
                        opt(
                            "WMTS serves pre-rendered, cacheable tiles on a fixed grid "
                            "(like XYZ), while WMS renders each request on demand",
                            correct=True,
                        ),
                        opt("WMTS only works offline"),
                        opt("WMTS returns editable features"),
                    ),
                    "WMTS is the tiled, cacheable OGC counterpart to XYZ; WMS GetMap is "
                    "rendered per request and not tile-cached.",
                ),
                q(
                    "What is the purpose of the GetCapabilities request?",
                    (
                        opt("To delete a layer"),
                        opt(
                            "To describe the service - which layers, formats and "
                            "projections it offers - so a client can discover it",
                            correct=True,
                        ),
                        opt("To pay for the service"),
                        opt("To restart the server"),
                    ),
                    "Every OGC service self-describes via GetCapabilities so any "
                    "compliant client can discover and consume it.",
                ),
            ),
        ),
        # -- 7. Tile servers and styling -------------------------------
        _t(
            "Tile servers and styling",
            "10 min",
            """# Tile servers and styling

Where do the tiles come from? Something has to turn your source data
(OpenStreetMap extracts, PostGIS tables, GeoTIFF rasters) into the tiles
the browser requests. That is a **tile server**, and there are two broad
approaches:

- **Pre-rendered (cached) tiles** - generate every tile ahead of time and
  store them as files or in a **MBTiles**/**PMTiles** archive. Serving is
  then just static file delivery - extremely fast and cheap, ideal for a
  stable basemap. The cost is storage and a slow build.
- **On-the-fly (dynamic) tiles** - render each tile when first requested,
  then cache it. Best when data changes often, at the cost of CPU on the
  first hit.

Common open-source tile servers include **GeoServer** and **MapServer**
(full OGC WMS/WFS/WMTS), **TileServer GL** and **Martin** (vector tiles
from MBTiles or PostGIS), and **tippecanoe** for building vector tilesets.

**Styling** is where the tiles become a map you want to look at, and it
differs by tile type:

- **Raster tiles** are styled at **render time** on the server (e.g. a
  Mapnik or SLD stylesheet). To change the look you regenerate the tiles.
- **Vector tiles** are styled in the **browser** with a style document.
  The same tiles can power a light theme, a dark theme, or a data
  overlay - no re-rendering.

The **SLD (Styled Layer Descriptor)** is the OGC XML standard for
server-side styling; a rule sets the paint for a feature type:

```text
Rule: roads (motorway)
  Filter:  class = 'motorway'
  Stroke:  color #e892a2, width 3px
  Label:   name, font 10px, halo white 1.5px

Zoom control (scale denominators):
  show motorways   when 1:zoom >= 1:2,000,000
  show local roads when 1:zoom >= 1:50,000
```

```mermaid
graph LR
    DATA["Source data OSM PostGIS raster"] --> SERVER["Tile server"]
    SERVER --> PRE["Pre rendered cached tiles"]
    SERVER --> DYN["On the fly rendered tiles"]
    PRE --> RASTERSTYLE["Raster styled at render time"]
    DYN --> VECTORSTYLE["Vector styled in the browser"]
    VECTORSTYLE --> THEMES["Many themes one tileset"]
```

Remember: a tile server turns source data into tiles, pre-rendered for
speed or dynamic for freshness. Raster tiles bake the style in at render
time; vector tiles are styled live in the browser from one tileset.
""",
        ),
        quiz_lesson(
            "Quiz: Tile servers and styling",
            (
                q(
                    "What is the trade-off of pre-rendering all tiles ahead of time?",
                    (
                        opt("It is slower to serve but uses no storage"),
                        opt(
                            "Serving becomes very fast static file delivery, at the "
                            "cost of storage and a slow build that must be redone when "
                            "data changes",
                            correct=True,
                        ),
                        opt("It makes the map interactive automatically"),
                        opt("It has no downsides at all"),
                    ),
                    "Pre-rendered tiles are fast and cheap to serve but need storage "
                    "and rebuilding; dynamic tiles trade first-hit CPU for freshness.",
                ),
                q(
                    "Where are raster tiles styled versus vector tiles?",
                    (
                        opt("Both are styled only in the browser"),
                        opt(
                            "Raster tiles are styled at render time on the server; "
                            "vector tiles are styled live in the browser",
                            correct=True,
                        ),
                        opt("Both are styled only on the server"),
                        opt("Neither can be styled"),
                    ),
                    "Raster styling is baked in when tiles are rendered; vector tiles "
                    "carry data and are styled client-side.",
                ),
                q(
                    "What is SLD?",
                    (
                        opt("A JavaScript mapping library"),
                        opt(
                            "The OGC Styled Layer Descriptor - an XML standard for "
                            "describing server-side map styling rules",
                            correct=True,
                        ),
                        opt("A tile file format"),
                        opt("A satellite constellation"),
                    ),
                    "SLD is the OGC XML standard used by servers like GeoServer to "
                    "define how feature types are painted.",
                ),
            ),
        ),
        # -- 8. Building an interactive web map application ------------
        _t(
            "Building an interactive web map application",
            "9 min",
            """# Building an interactive web map application

Now assemble the whole stack into a real application. Every piece from
this course has a place: a projection and tiling scheme, a base tile
source, a mapping library, your own GeoJSON data, an OGC service, and
interaction that ties it to the user.

A typical interactive web map is built in layers:

1. **Base layer** - an XYZ raster or vector-tile basemap for context
   (streets, terrain, satellite).
2. **Data layers (overlays)** - your features: GeoJSON you fetch, a WFS
   feed, or a vector tileset. Style them by their attributes.
3. **Interaction** - popups on click, hover highlights, a layer switcher,
   search/geocoding, and filtering that reads feature `properties`.
4. **State and performance** - fetch data lazily, cluster or switch to
   vector tiles when there are many features, and keep the base tiles on a
   CDN.

A common pattern: draw a basemap, load live data over HTTP, and react to
clicks:

```javascript
// Base map + live GeoJSON overlay + click interaction (Leaflet)
const map = L.map('map').setView([51.505, -0.09], 12);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
  { attribution: 'OpenStreetMap' }).addTo(map);

fetch('/api/sensors.geojson')            // your data endpoint
  .then(r => r.json())
  .then(data => {
    L.geoJSON(data, {
      onEachFeature: (f, layer) =>
        layer.on('click', () =>
          showPanel(f.properties.name, f.properties.reading))
    }).addTo(map);
  });
```

The whole architecture, end to end:

```mermaid
graph LR
    USER["User pans and clicks"] --> LIB["Mapping library"]
    LIB --> BASE["Base tile source XYZ"]
    LIB --> OVER["Overlay GeoJSON or WFS"]
    OVER --> API["Your data API"]
    LIB --> UI["Popups search and filters"]
    UI --> USER
```

Choosing the pieces: **Leaflet** plus GeoJSON for a simple points map;
**OpenLayers** when you need OGC services and many projections;
**MapLibre GL** with vector tiles when you want live styling, rotation and
large datasets. Put the base tiles on a CDN, serve your data as GeoJSON or
vector tiles, and let the library do the tile math.

Remember: an interactive web map is a base layer plus data overlays plus
interaction. Pick the library for your needs, feed it standard tiles and
GeoJSON, and the same tiling and projection foundations carry through.
""",
        ),
        quiz_lesson(
            "Quiz: Building an interactive web map application",
            (
                q(
                    "How is a typical interactive web map layered?",
                    (
                        opt("A single image with nothing on top"),
                        opt(
                            "A base tile layer for context, data overlays (your "
                            "features), and interaction like popups and filtering",
                            correct=True,
                        ),
                        opt("Only a database, no browser code"),
                        opt("Just a list of coordinates in text"),
                    ),
                    "Base layer + overlays + interaction is the standard composition of "
                    "a web map application.",
                ),
                q(
                    "For a simple points map with your own data, which combination fits best?",
                    (
                        opt("MapLibre GL with custom vector tiles and a tile pipeline"),
                        opt("Leaflet with a GeoJSON overlay", correct=True),
                        opt("A raw WMS image with no library"),
                        opt("A spreadsheet emailed to users"),
                    ),
                    "Leaflet plus GeoJSON is the lightweight, straightforward choice "
                    "for a modest set of point features.",
                ),
                q(
                    "When should you move from raw GeoJSON overlays to vector tiles?",
                    (
                        opt("Never - GeoJSON scales infinitely"),
                        opt(
                            "When there are too many features to send at once and you "
                            "want live styling, rotation and smooth performance",
                            correct=True,
                        ),
                        opt("Only when the map is black and white"),
                        opt("Whenever the user is offline"),
                    ),
                    "Large datasets and a need for client-side styling/rotation are the "
                    "signal to switch from bulk GeoJSON to vector tiles.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Why are web maps built from tiles?",
                    (
                        opt("Because HTML forbids large images"),
                        opt(
                            "A full-detail world map is too big to send at once; tiles "
                            "let the browser fetch only the visible squares and cache "
                            "them",
                            correct=True,
                        ),
                        opt("To make maps look pixelated"),
                        opt("Tiles are slower but prettier"),
                    ),
                    "Tiling downloads only the current view and enables caching - the "
                    "core reason web maps feel fast.",
                ),
                q(
                    "Which projection and code underpin standard web map tiles?",
                    (
                        opt("Plate Carree, EPSG:4326"),
                        opt("Web Mercator, EPSG:3857", correct=True),
                        opt("British National Grid, EPSG:27700"),
                        opt("No projection is used"),
                    ),
                    "Web Mercator (EPSG:3857) flattens the world into the square that "
                    "the XYZ grid subdivides.",
                ),
                q(
                    "In the XYZ scheme, what do z, x and y address?",
                    (
                        opt("Red, green and blue channels"),
                        opt(
                            "The zoom level and the tile's column and row in the grid "
                            "for that zoom",
                            correct=True,
                        ),
                        opt("Longitude, latitude and altitude"),
                        opt("Three random cache keys"),
                    ),
                    "z is zoom (grid is 2^z per side); x is the column, y is the row - "
                    "watch the top-vs-bottom y-origin (XYZ vs TMS).",
                ),
                q(
                    "What distinguishes vector tiles from raster tiles?",
                    (
                        opt("Vector tiles are pre-rendered pictures"),
                        opt(
                            "Vector tiles ship geometry and attributes the client draws "
                            "and can restyle live; raster tiles are baked images",
                            correct=True,
                        ),
                        opt("Raster tiles carry attributes"),
                        opt("They are identical"),
                    ),
                    "Vector tiles send data (MVT), enabling client-side styling, "
                    "rotation and interaction; raster tiles are fixed images.",
                ),
                q(
                    "In GeoJSON, coordinates are written as:",
                    (
                        opt("[latitude, longitude]"),
                        opt("[longitude, latitude] in WGS84 decimal degrees", correct=True),
                        opt("[easting, northing] in metres"),
                        opt("[x, y] in screen pixels"),
                    ),
                    "GeoJSON is longitude-first in WGS84 (EPSG:4326) - the opposite of "
                    "many [lat, lng] centre APIs.",
                ),
                q(
                    "Which library is the light, beginner-friendly choice for simple raster maps?",
                    (
                        opt("OpenLayers"),
                        opt("Leaflet", correct=True),
                        opt("GeoServer"),
                        opt("tippecanoe"),
                    ),
                    "Leaflet is small and simple; OpenLayers is heavier with native "
                    "multi-projection and OGC support.",
                ),
                q(
                    "A WMS GetMap request returns what?",
                    (
                        opt("Editable vector features"),
                        opt(
                            "A server-rendered map image for a bounding box, layers and size",
                            correct=True,
                        ),
                        opt("A list of tile addresses"),
                        opt("A style document"),
                    ),
                    "WMS renders on the server and returns a picture; WFS returns the "
                    "features themselves.",
                ),
                q(
                    "Which OGC service returns cached, pre-rendered tiles on a fixed grid?",
                    (
                        opt("WMS"),
                        opt("WFS"),
                        opt("WMTS - Web Map Tile Service", correct=True),
                        opt("GML"),
                    ),
                    "WMTS is the tiled, cacheable OGC counterpart to XYZ; WMS GetMap is "
                    "rendered per request.",
                ),
                q(
                    "Where are raster tiles styled compared with vector tiles?",
                    (
                        opt("Both only in the browser"),
                        opt(
                            "Raster tiles are styled at render time on the server; "
                            "vector tiles are styled live in the browser",
                            correct=True,
                        ),
                        opt("Both only on the server"),
                        opt("Neither can be styled"),
                    ),
                    "Raster styling is baked in when tiles are generated; vector tiles "
                    "carry data and are painted client-side from a style document.",
                ),
                q(
                    "What are the three layers of a typical interactive web map application?",
                    (
                        opt("HTML, CSS and a database"),
                        opt(
                            "A base tile layer, data overlays (your features), and "
                            "interaction such as popups, search and filtering",
                            correct=True,
                        ),
                        opt("Only markers with no basemap"),
                        opt("Three separate websites"),
                    ),
                    "Base layer for context + data overlays + interaction is the "
                    "standard composition, on top of the tiling and projection "
                    "foundations.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

WEB_GIS_DEVELOPMENT_COURSES: tuple[SeedCourse, ...] = (_WEB_GIS_DEVELOPMENT,)
