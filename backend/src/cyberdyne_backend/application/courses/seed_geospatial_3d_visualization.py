"""Academy seed content - 3D Geospatial Visualization.

Rendering the planet in 3D: how flat maps give way to digital globes, how
Cesium draws an interactive Earth, how terrain and imagery are streamed and
draped, and how glTF models and 3D Tiles bring massive city-scale and sensor
datasets into the browser. It grounds the graphics pipeline (GPU, shaders),
the geodesy of a virtual globe (ECEF, WGS84 ellipsoid), and camera control,
then closes by assembling a complete 3D geospatial scene. Every lesson is a
direct explanation with a concrete code or data example and a mermaid diagram,
followed by a checkpoint quiz; the course closes with a comprehensive final
quiz.
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


_THREE_D_GEOSPATIAL_VISUALIZATION = SeedCourse(
    slug="3d-geospatial-visualization",
    title="3D Geospatial Visualization",
    description=(
        "Rendering the planet in 3D - digital globes with Cesium, streaming "
        "massive scenes with 3D Tiles and glTF, terrain and the graphics "
        "pipeline behind interactive geospatial worlds. Every lesson pairs a "
        "direct explanation with a real code or data example (CesiumJS, glTF, "
        "3D Tiles JSON, ECEF math) and a diagram."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# 3D Geospatial Visualization

A flat map is a compromise: the Earth is a curved, three-dimensional body,
and every 2D projection distorts something to force it onto a plane. **3D
geospatial visualization** drops that compromise and renders the planet as
it is - a globe you can orbit, tilt, and fly across, draped in real terrain,
imagery, buildings, and streamed sensor data.

This course explains how that works, from first principles to a running
scene. The approach is **small and concrete**: every lesson explains one
idea directly, shows it in a short real example (a CesiumJS snippet, a glTF
or 3D Tiles JSON fragment, an ECEF coordinate calculation), and draws the
idea as a diagram. After each lesson there is a short quiz; at the end, a
final quiz covers the whole course.

What you will build understanding for, in order:

1. **From 2D maps to 3D globes** - why a globe, and what changes
2. **The Cesium digital globe** - the open engine for a virtual Earth
3. **Terrain and imagery in 3D** - elevation and pictures draped on the globe
4. **The glTF 3D model format** - the "JPEG of 3D" for individual models
5. **3D Tiles for massive datasets** - streaming cities and point clouds
6. **The real-time graphics pipeline** - GPU, shaders, and how a frame is drawn
7. **Camera, coordinates and ECEF** - the geodesy behind a virtual globe
8. **Building a 3D geospatial scene** - putting every piece together

By the end you will know how a digital globe is assembled, why 3D Tiles and
glTF are the standards for streaming 3D geospatial content, and how the GPU
turns coordinates into the pixels you see.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the core motivation for 3D geospatial visualization over a flat map?",
                    (
                        opt("3D maps are always faster to render"),
                        opt(
                            "The Earth is a curved 3D body, so a globe avoids the "
                            "distortion every flat projection forces and can show "
                            "terrain, buildings and depth directly",
                            correct=True,
                        ),
                        opt("Flat maps cannot store color"),
                        opt("3D removes the need for coordinates"),
                    ),
                    "Every 2D projection distorts area, angle or distance; a globe "
                    "renders the planet as it is and adds real elevation and structure.",
                ),
                q(
                    "How is this course structured?",
                    (
                        opt("Pure theory with no examples"),
                        opt(
                            "Each lesson gives a direct explanation, one concrete code "
                            "or data example, and a diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Only a single final exam"),
                        opt("Video lectures with no text"),
                    ),
                    "Small and concrete: explain, show a real example, draw it, then "
                    "check understanding with a quiz.",
                ),
            ),
        ),
        # -- 1. From 2D maps to 3D globes ------------------------------
        _t(
            "From 2D maps to 3D globes",
            "9 min",
            """# From 2D maps to 3D globes

A **2D web map** (think a slippy map in Web Mercator, **EPSG:3857**) is a
plane. It is fast, simple, and perfect for street-level navigation, but it
pays a price: Web Mercator badly inflates area near the poles - Greenland
looks the size of Africa though it is about a fourteenth as large. Any flat
map must distort **area, angle, or distance**; you only choose which.

A **3D globe** renders the Earth as a curved surface, typically the **WGS84
ellipsoid** (**EPSG:4979** for 3D geographic coordinates), and lets the
camera orbit and tilt in space. Nothing is forced flat, so there is no
projection distortion; instead the challenge becomes *drawing a sphere-like
body efficiently and streaming enough detail to fill the screen*.

Key differences the rest of the course builds on:

- **Coordinates** - 2D maps work in projected metres (x, y); a globe works
  in geographic **longitude, latitude, height** and, internally, in 3D
  **Cartesian** metres from the Earth's centre (ECEF - a later lesson).
- **The third dimension** - a globe can show real **terrain elevation** and
  **3D structures** (buildings, models), not just a top-down picture.
- **The camera** - instead of pan and zoom on a plane, you have a full 3D
  camera with position, orientation, and field of view.
- **Level of detail** - you cannot load the whole planet at full resolution;
  detail must **stream** based on where the camera looks.

A simple decision of when each shines:

```text
Flat 2D map (EPSG:3857):  turn-by-turn, thematic choropleths, quick embeds
3D globe   (WGS84):       terrain, cityscapes, flight paths, global context,
                          anything where elevation or planetary scale matters
```

```mermaid
graph LR
    EARTH["Curved Earth WGS84"] --> FLAT["Project to a plane"]
    FLAT --> MAP2D["2D map with distortion"]
    EARTH --> GLOBE["Render as a 3D globe"]
    GLOBE --> NODIST["No projection distortion"]
    GLOBE --> TERR["Real terrain and 3D structures"]
    GLOBE --> STREAM["Stream detail by view"]
```

Remember: a flat map trades truth for simplicity; a 3D globe keeps the
geometry honest and trades it for the harder problems of streaming and 3D
rendering - which the tools in this course solve.
""",
        ),
        quiz_lesson(
            "Quiz: From 2D maps to 3D globes",
            (
                q(
                    "Why does Greenland look far too big on a standard Web Mercator "
                    "(EPSG:3857) map?",
                    (
                        opt("Its imagery is a higher resolution"),
                        opt(
                            "Web Mercator inflates area increasingly toward the poles - "
                            "a distortion inherent to flattening a curved Earth",
                            correct=True,
                        ),
                        opt("Greenland really is that large"),
                        opt("The map uses the wrong colors"),
                    ),
                    "Every flat projection distorts something; Mercator preserves "
                    "angles but grossly exaggerates high-latitude area.",
                ),
                q(
                    "What new hard problem does a 3D globe introduce that a flat "
                    "tile map largely avoids?",
                    (
                        opt("Storing color values"),
                        opt(
                            "You cannot load the whole planet at full resolution, so "
                            "detail must stream based on where the camera looks (level "
                            "of detail)",
                            correct=True,
                        ),
                        opt("Choosing a font"),
                        opt("Supporting mouse clicks"),
                    ),
                    "A globe swaps projection distortion for the challenge of "
                    "streaming and level-of-detail management.",
                ),
                q(
                    "Internally, how does a virtual globe typically represent "
                    "positions on the Earth?",
                    (
                        opt("Only as pixel coordinates on the screen"),
                        opt(
                            "As geographic longitude, latitude and height, and as 3D "
                            "Cartesian metres from the Earth's centre",
                            correct=True,
                        ),
                        opt("As street addresses"),
                        opt("As Web Mercator tiles only"),
                    ),
                    "Geographic lon/lat/height for authoring, ECEF Cartesian metres "
                    "for the actual 3D math.",
                ),
            ),
        ),
        # -- 2. The Cesium digital globe -------------------------------
        _t(
            "The Cesium digital globe",
            "10 min",
            """# The Cesium digital globe

**CesiumJS** is the open-source JavaScript engine that most 3D geospatial
work in the browser is built on. It renders a **WGS84 digital globe** with
WebGL, streams terrain and imagery, and understands geospatial formats
(**glTF**, **3D Tiles**, GeoJSON, KML, CZML) natively. Cesium authored the
**3D Tiles** and (with the Khronos Group) uses **glTF** - the two OGC and
industry standards this course centres on.

The central object is the **Viewer**: it owns the globe, a **Scene**
(everything drawn), a **Camera**, and **entities** (your data). Creating a
globe and placing a point is only a few lines:

```javascript
// A full digital globe in the browser with CesiumJS
Cesium.Ion.defaultAccessToken = "YOUR_TOKEN";
const viewer = new Cesium.Viewer("cesiumContainer", {
  terrain: Cesium.Terrain.fromWorldTerrain(),   // streamed global terrain
});

// Longitude, latitude, height (metres) -> a point on the globe
viewer.entities.add({
  name: "Sydney Opera House",
  position: Cesium.Cartesian3.fromDegrees(151.2153, -33.8568, 10),
  point: { pixelSize: 12, color: Cesium.Color.CYAN },
});

viewer.zoomTo(viewer.entities);   // fly the camera to the data
```

A few ideas make Cesium a *geospatial* engine rather than a generic 3D one:

- **The globe is the coordinate system** - you author in real longitude,
  latitude, and height; Cesium converts to the internal 3D frame for you.
- **Streaming by default** - terrain, imagery, and 3D Tiles load
  progressively at the resolution the current view needs.
- **Ion and asset services** - **Cesium ion** hosts and tiles global terrain,
  imagery, and your uploaded datasets, but Cesium also reads open sources
  (OGC WMS/WMTS imagery, self-hosted 3D Tiles, glTF).
- **Entities vs primitives** - high-level **entities** (a point, a model, a
  path over time) are convenient; low-level **primitives** give raw control
  for performance.

```mermaid
graph TD
    VIEWER["Cesium Viewer"] --> SCENE["Scene"]
    VIEWER --> CAM["Camera"]
    SCENE --> GLOBE["WGS84 globe"]
    GLOBE --> TERR["Streamed terrain"]
    GLOBE --> IMG["Streamed imagery"]
    SCENE --> TILES["3D Tiles datasets"]
    SCENE --> MODELS["glTF models"]
    VIEWER --> ENT["Entities your data"]
```

Remember: Cesium gives you a real, streaming digital Earth addressed in
geographic coordinates - the platform on which terrain, glTF models, and 3D
Tiles all come together.
""",
        ),
        quiz_lesson(
            "Quiz: The Cesium digital globe",
            (
                q(
                    "What is CesiumJS?",
                    (
                        opt("A raster image editor"),
                        opt(
                            "An open-source WebGL engine that renders a streaming WGS84 "
                            "digital globe and natively reads geospatial 3D formats like "
                            "glTF and 3D Tiles",
                            correct=True,
                        ),
                        opt("A relational database"),
                        opt("A projection library only for 2D maps"),
                    ),
                    "Cesium draws a virtual Earth in the browser and authored the 3D "
                    "Tiles standard for streaming 3D geospatial content.",
                ),
                q(
                    "In CesiumJS, how do you specify where to place a point on the globe?",
                    (
                        opt("In screen pixel coordinates"),
                        opt(
                            "In real longitude, latitude and height - Cesium converts "
                            "to its internal 3D frame for you",
                            correct=True,
                        ),
                        opt("By naming a country"),
                        opt("Only by clicking with the mouse"),
                    ),
                    "You author in geographic coordinates (e.g. "
                    "Cartesian3.fromDegrees(lon, lat, height)); the engine handles "
                    "the conversion.",
                ),
                q(
                    "Why is terrain and imagery loaded 'progressively' in Cesium?",
                    (
                        opt("To make the code shorter"),
                        opt(
                            "The whole planet cannot fit in memory, so data streams at "
                            "the resolution the current camera view needs",
                            correct=True,
                        ),
                        opt("Because WebGL forbids preloading"),
                        opt("To avoid using coordinates"),
                    ),
                    "Streaming by view is how a globe shows global context and local "
                    "detail without loading everything.",
                ),
            ),
        ),
        # -- 3. Terrain and imagery in 3D ------------------------------
        _t(
            "Terrain and imagery in 3D",
            "10 min",
            """# Terrain and imagery in 3D

A globe without relief is a smooth ball. Two distinct layers give it a real
surface:

- **Terrain** - the *shape* of the ground: elevation values (a **digital
  elevation model**, DEM) that push the globe's surface up into mountains
  and down into valleys. Cesium World Terrain and open sources like **SRTM**
  or **Copernicus DEM** provide global elevation.
- **Imagery** - the *appearance* draped over that shape: satellite or aerial
  pictures, or styled basemaps, served as tiles (often **OGC WMTS** or an
  XYZ tile scheme) and painted onto the terrain surface.

The two are decoupled on purpose: you can drape any imagery over any terrain.
Under the hood the globe is a **quantized-mesh** terrain surface, tiled and
served per view; imagery tiles are looked up by the same tile pyramid and
textured on.

```javascript
// Add streamed world terrain plus an imagery layer over it
const viewer = new Cesium.Viewer("cesiumContainer", {
  terrain: Cesium.Terrain.fromWorldTerrain(),        // the elevation shape
});
// Drape a WMTS/tiled imagery source on top of the terrain
const imagery = await Cesium.IonImageryProvider.fromAssetId(3954);
viewer.imageryLayers.addImageryProvider(imagery);    // the appearance
// Vertical exaggeration makes subtle relief readable
viewer.scene.verticalExaggeration = 1.5;
```

Because both layers are **tiled pyramids**, the globe requests only the tiles
that cover the current view, at the zoom level that matches the camera
distance - close in, high-detail tiles; far away, coarse ones. This is the
same **level-of-detail** idea that runs through all 3D geospatial streaming.

Practical points that trip people up:

- **Heights need a datum** - a terrain height is above a reference (an
  ellipsoid or a geoid/mean-sea-level model). Mixing datums misplaces things
  vertically.
- **Imagery and terrain resolution differ** - crisp imagery over coarse
  terrain still looks flat; you need both to be detailed for realism.
- **Draping vs clamping** - vector features and models can be **clamped to
  terrain** so they sit on the ground rather than floating or sinking.

```mermaid
graph TD
    DEM["Elevation model DEM"] --> TMESH["Quantized mesh terrain"]
    TMESH --> SURFACE["Globe surface shape"]
    IMGSRC["Imagery tiles WMTS or XYZ"] --> DRAPE["Drape over surface"]
    SURFACE --> DRAPE
    DRAPE --> VIEW["Detailed 3D ground by view"]
    CAM["Camera distance"] --> LOD["Pick tile level of detail"]
    LOD --> VIEW
```

Remember: terrain is the shape, imagery is the skin, and both stream as tile
pyramids chosen by the camera - detail where you look, coarse everywhere else.
""",
        ),
        quiz_lesson(
            "Quiz: Terrain and imagery in 3D",
            (
                q(
                    "What is the difference between terrain and imagery on a globe?",
                    (
                        opt("They are two names for the same layer"),
                        opt(
                            "Terrain is the elevation shape of the ground (a DEM); "
                            "imagery is the picture draped over that shape",
                            correct=True,
                        ),
                        opt("Terrain is the color, imagery is the height"),
                        opt("Imagery only works in 2D"),
                    ),
                    "Shape vs skin: they are decoupled, so any imagery can drape over any terrain.",
                ),
                q(
                    "Why can you drape different imagery over the same terrain?",
                    (
                        opt("Because imagery includes elevation"),
                        opt(
                            "Terrain (the elevation mesh) and imagery (the texture) are "
                            "separate layers indexed by the same tile pyramid",
                            correct=True,
                        ),
                        opt("Because terrain is always flat"),
                        opt("They cannot be combined at all"),
                    ),
                    "Decoupling shape from appearance lets you swap basemaps or "
                    "satellite imagery over one elevation surface - both are tiled "
                    "pyramids, so the texture is sampled onto the terrain mesh.",
                ),
                q(
                    "Why must terrain heights reference a stated datum (ellipsoid or geoid)?",
                    (
                        opt("To make the file smaller"),
                        opt(
                            "A height is only meaningful relative to a reference "
                            "surface; mixing datums misplaces features vertically",
                            correct=True,
                        ),
                        opt("Datums are only needed for imagery"),
                        opt("Heights never need a reference"),
                    ),
                    "An elevation is a height above something - get the reference "
                    "wrong and everything sits at the wrong altitude.",
                ),
            ),
        ),
        # -- 4. The glTF 3D model format -------------------------------
        _t(
            "The glTF 3D model format",
            "10 min",
            """# The glTF 3D model format

To place a building, a vehicle, or a sensor model on the globe you need a
**3D model format**. **glTF** (GL Transmission Format), from the Khronos
Group, is the standard - often called the **"JPEG of 3D"** because it is a
compact, runtime-ready format that GPUs and engines load directly, with no
heavy conversion. Cesium, three.js, Babylon.js, Unreal, and browsers all
read it.

A glTF asset describes a **scene graph** - a tree of **nodes**, each with a
transform, referencing **meshes** (geometry), **materials** (how surfaces
look, using **PBR** - physically based rendering), **textures**, and
optionally **animations** and **skins**. The geometry itself lives in
compact **binary buffers** rather than verbose text.

The JSON is human-readable at the top level:

```json
{
  "asset": { "version": "2.0", "generator": "cyberdyne-exporter" },
  "scene": 0,
  "scenes": [{ "nodes": [0] }],
  "nodes": [
    { "mesh": 0, "translation": [0, 0, 0], "name": "sensor_tower" }
  ],
  "meshes": [
    { "primitives": [{ "attributes": { "POSITION": 1, "NORMAL": 2 },
                       "indices": 0, "material": 0 }] }
  ],
  "materials": [
    { "pbrMetallicRoughness": { "baseColorFactor": [0.6, 0.6, 0.65, 1.0],
                                 "metallicFactor": 0.9, "roughnessFactor": 0.4 } }
  ]
}
```

Two packagings you will meet:

- **.gltf** - the JSON plus separate `.bin` buffers and image files.
- **.glb** - a single binary file bundling the JSON, buffers, and textures.
  Preferred for the web: one request, no missing-asset surprises.

Why glTF fits geospatial work specifically:

- **Runtime-ready** - it maps almost directly onto what the GPU needs, so it
  loads fast (the whole point of a streaming globe).
- **PBR materials** - surfaces respond to lighting consistently across
  engines, so a model looks right under the globe's sun position.
- **It is the leaf of 3D Tiles** - a 3D Tiles tileset (next lesson) is, at
  the bottom, a tree of glTF content. Learn glTF and you understand what 3D
  Tiles actually stream.
- **Compression** - **Draco** (geometry) and **KTX2/Basis** (textures) shrink
  assets dramatically for delivery.

```mermaid
graph TD
    GLTF["glTF asset"] --> SCENE["Scene graph nodes"]
    SCENE --> MESH["Meshes geometry"]
    SCENE --> MAT["PBR materials"]
    MESH --> BUF["Binary buffers"]
    MAT --> TEX["Textures"]
    GLTF --> ANIM["Animations optional"]
    BUF --> GPU["Loaded straight by the GPU"]
    TEX --> GPU
```

Remember: glTF is the compact, runtime-ready model format the GPU loads
directly - the building block that 3D Tiles streams to fill a whole city.
""",
        ),
        quiz_lesson(
            "Quiz: The glTF 3D model format",
            (
                q(
                    "Why is glTF nicknamed the 'JPEG of 3D'?",
                    (
                        opt("It can only store photographs"),
                        opt(
                            "It is a compact, runtime-ready 3D format that engines and "
                            "GPUs load directly, without heavy conversion",
                            correct=True,
                        ),
                        opt("It is limited to 2D images"),
                        opt("It is an Adobe product"),
                    ),
                    "Like JPEG for images, glTF is the interchange-and-delivery "
                    "standard for 3D models across engines.",
                ),
                q(
                    "What does a glTF file describe?",
                    (
                        opt("Only a flat texture"),
                        opt(
                            "A scene graph of nodes referencing meshes (geometry), PBR "
                            "materials, textures, and optional animations, with "
                            "geometry in binary buffers",
                            correct=True,
                        ),
                        opt("A database schema"),
                        opt("A map projection definition"),
                    ),
                    "Nodes with transforms point at meshes and materials; the heavy "
                    "geometry lives in compact binary buffers.",
                ),
                q(
                    "What is the practical advantage of a .glb file over a .gltf plus "
                    "separate files for the web?",
                    (
                        opt("It supports more colors"),
                        opt(
                            "It bundles the JSON, binary buffers and textures into one "
                            "self-contained file - a single request with no missing "
                            "assets",
                            correct=True,
                        ),
                        opt("It is always uncompressed"),
                        opt("It cannot be read by browsers"),
                    ),
                    ".glb packages everything together, which is why it is preferred for delivery.",
                ),
            ),
        ),
        # -- 5. 3D Tiles for massive datasets --------------------------
        _t(
            "3D Tiles for massive datasets",
            "10 min",
            """# 3D Tiles for massive datasets

A single glTF model is fine for one building. But a **whole city**, a
country-wide photogrammetry mesh, or a **billion-point LiDAR cloud** is far
too large to load at once. **3D Tiles** - an **OGC community standard**
created by Cesium - is how you *stream* such massive, heterogeneous 3D
geospatial datasets efficiently.

The core idea is a **spatial tree with level of detail**. The dataset is cut
into a **bounding-volume hierarchy**: a root tile covers the whole area at
coarse detail; its children cover smaller areas at finer detail, recursively.
The renderer walks the tree and loads a tile only if its bounding volume is
in view and its detail is warranted by the camera distance - the **geometric
error** (in metres) tells it when a tile is too coarse and it must descend to
children.

A `tileset.json` sketches this hierarchy; the leaf **content** is glTF (or
point-cloud) data:

```json
{
  "asset": { "version": "1.1" },
  "geometricError": 500,
  "root": {
    "boundingVolume": { "region": [-1.32, 0.70, -1.31, 0.71, 0, 240] },
    "geometricError": 250,
    "refine": "REPLACE",
    "content": { "uri": "city_root.glb" },
    "children": [
      { "boundingVolume": { "region": [-1.32, 0.70, -1.315, 0.705, 0, 180] },
        "geometricError": 60,
        "content": { "uri": "tiles/block_0.glb" } }
    ]
  }
}
```

Concepts worth pinning down:

- **Geometric error** - the screen-space error (roughly, how wrong a tile
  looks) if you stop here. When it exceeds a threshold, the engine loads the
  finer children. This is the streaming decision.
- **Refinement: REPLACE vs ADD** - a finer tile either *replaces* its parent
  (photogrammetry meshes) or *adds* to it (point clouds accumulate detail).
- **Heterogeneous content** - the same standard streams photogrammetry,
  BIM/CAD, 3D buildings, and massive point clouds, because leaves are just
  glTF or point data.
- **Metadata** - per-feature properties (e.g. each building's height, ID) ride
  along, so tiles are queryable and stylable, not just pretty geometry.

```mermaid
graph TD
    ROOT["Root tile coarse detail"] --> C1["Child tile finer"]
    ROOT --> C2["Child tile finer"]
    C1 --> G1["glTF or point content"]
    C2 --> G2["glTF or point content"]
    CAM["Camera view and distance"] --> GE["Check geometric error"]
    GE --> LOAD["Load only visible warranted tiles"]
    LOAD --> ROOT
```

Remember: 3D Tiles is a bounding-volume tree with per-tile geometric error;
the engine descends only where the view needs detail, so a planet-scale
dataset streams into a browser a few tiles at a time.
""",
        ),
        quiz_lesson(
            "Quiz: 3D Tiles for massive datasets",
            (
                q(
                    "What problem does 3D Tiles solve?",
                    (
                        opt("Editing 2D vector polygons"),
                        opt(
                            "Streaming massive, heterogeneous 3D datasets (cities, "
                            "photogrammetry, point clouds) that are far too large to "
                            "load all at once",
                            correct=True,
                        ),
                        opt("Compressing JPEG images"),
                        opt("Storing tabular attributes only"),
                    ),
                    "It is the OGC standard, created by Cesium, for efficient "
                    "streaming of huge 3D geospatial content.",
                ),
                q(
                    "In 3D Tiles, what does a tile's 'geometric error' control?",
                    (
                        opt("The file's color depth"),
                        opt(
                            "How wrong the tile looks if rendering stops there - when "
                            "it exceeds a threshold, the engine loads finer child tiles",
                            correct=True,
                        ),
                        opt("The map projection used"),
                        opt("The network port number"),
                    ),
                    "Geometric error (in metres) is the level-of-detail decision that "
                    "drives when to descend the tree - larger camera distance "
                    "tolerates more error, getting closer forces finer tiles.",
                ),
                q(
                    "What sits at the leaves (the actual content) of a 3D Tiles tileset?",
                    (
                        opt("Only plain text"),
                        opt(
                            "glTF geometry or point-cloud data - which is why learning "
                            "glTF explains what 3D Tiles streams",
                            correct=True,
                        ),
                        opt("SQL tables"),
                        opt("PDF documents"),
                    ),
                    "The tileset.json is the spatial tree; the content it points to "
                    "is glTF or point data.",
                ),
            ),
        ),
        # -- 6. The real-time graphics pipeline ------------------------
        _t(
            "The real-time graphics pipeline (GPU, shaders)",
            "10 min",
            """# The real-time graphics pipeline (GPU, shaders)

Every frame you see on a digital globe is produced by the **GPU** running the
**real-time graphics pipeline**: a fixed sequence of stages that turns 3D
geometry into 2D pixels, tens of times per second. Cesium (via **WebGL** or
**WebGPU**) drives this pipeline; understanding it demystifies performance
and appearance.

The essential stages:

1. **Vertex processing** - a **vertex shader** runs once per vertex. It
   transforms each 3D position through **model -> view -> projection**
   matrices into clip/screen space. On a globe this is where ECEF metre
   coordinates become on-screen positions.
2. **Primitive assembly and rasterization** - transformed vertices form
   triangles; rasterization figures out which **pixels (fragments)** each
   triangle covers.
3. **Fragment processing** - a **fragment (pixel) shader** runs once per
   covered pixel to compute its color: sampling textures (imagery), applying
   **PBR lighting** from the sun, fog, atmosphere.
4. **Output merging** - the **depth (z) buffer** keeps the nearest surface at
   each pixel so far things are hidden behind near ones; blending handles
   transparency. The result is written to the framebuffer and shown.

Shaders are small programs (in GLSL/WGSL) you can write. A minimal vertex
shader is just a matrix multiply:

```javascript
// GLSL vertex shader: transform a model-space position to clip space
const vertexShader = `
  attribute vec3 position;          // vertex in model space
  uniform mat4 u_modelViewProjection;
  void main() {
    // model -> view -> projection, all in one matrix here
    gl_Position = u_modelViewProjection * vec4(position, 1.0);
  }
`;
```

What this buys you as a geospatial developer:

- **Performance intuition** - too many vertices strains the vertex stage;
  overdraw and heavy lighting strain the fragment stage. Level of detail
  (fewer tiles/vertices far away) directly protects the pipeline.
- **The matrices are the coordinates** - the model-view-projection chain is
  exactly how a global ECEF position ends up as a pixel; camera moves change
  the view matrix.
- **The depth buffer and scale** - a planet spans millions of metres, so
  naive depth precision fails at global scale; engines use tricks
  (logarithmic depth) to avoid **z-fighting**.

```mermaid
graph LR
    GEO["3D geometry vertices"] --> VS["Vertex shader transform"]
    VS --> RAST["Rasterize to fragments"]
    RAST --> FS["Fragment shader shade"]
    FS --> DEPTH["Depth test and blend"]
    DEPTH --> FB["Framebuffer pixels on screen"]
    MVP["Model view projection matrices"] --> VS
```

Remember: the GPU pipeline transforms vertices, rasterizes triangles, shades
fragments, and depth-tests to pixels - every frame. Level of detail keeps
that pipeline fed with only what the view needs.
""",
        ),
        quiz_lesson(
            "Quiz: The real-time graphics pipeline (GPU, shaders)",
            (
                q(
                    "What does the vertex shader stage do?",
                    (
                        opt("Picks the file format to load"),
                        opt(
                            "Runs once per vertex, transforming each 3D position "
                            "through model-view-projection matrices toward screen space",
                            correct=True,
                        ),
                        opt("Compresses textures on disk"),
                        opt("Writes logs to the console"),
                    ),
                    "The vertex shader is where global 3D coordinates become on-screen "
                    "positions via the MVP matrix chain.",
                ),
                q(
                    "What is the job of the depth (z) buffer?",
                    (
                        opt("To store the file name"),
                        opt(
                            "To keep the nearest surface at each pixel so farther "
                            "objects are correctly hidden behind nearer ones",
                            correct=True,
                        ),
                        opt("To increase the frame rate directly"),
                        opt("To hold the imagery tiles"),
                    ),
                    "Depth testing resolves visibility per pixel; at planetary scale, "
                    "engines use logarithmic depth to avoid z-fighting.",
                ),
                q(
                    "How does level of detail (loading fewer tiles far away) help the "
                    "GPU pipeline?",
                    (
                        opt("It changes the map projection"),
                        opt(
                            "It reduces the vertices and fragments the pipeline must "
                            "process for distant geometry, protecting performance",
                            correct=True,
                        ),
                        opt("It disables the fragment shader"),
                        opt("It removes the need for a camera"),
                    ),
                    "Fewer vertices ease the vertex stage and less overdraw eases the "
                    "fragment stage - LOD feeds the pipeline only what the view needs.",
                ),
            ),
        ),
        # -- 7. Camera, coordinates and ECEF ---------------------------
        _t(
            "Camera, coordinates and the virtual globe (ECEF)",
            "10 min",
            """# Camera, coordinates and the virtual globe (ECEF)

You author in longitude and latitude, but the globe's math happens in a 3D
Cartesian frame. That frame is **ECEF** - **Earth-Centered, Earth-Fixed**
(the geocentric datum **EPSG:4978**). Its origin is the Earth's centre of
mass; the axes rotate *with* the Earth, so a fixed point on the ground keeps
constant coordinates:

```text
ECEF axes (metres from Earth's centre):
  X -> through the equator at the prime meridian (0 lon, 0 lat)
  Y -> through the equator at 90 deg East
  Z -> through the North Pole
```

To go from geographic (**lon L, lat B, height h**) on the WGS84 ellipsoid to
ECEF (**X, Y, Z**), with semi-major axis **a** and first eccentricity squared
**e2**:

```text
N = a / sqrt(1 - e2 * sin(B)^2)          (prime vertical radius)
X = (N + h) * cos(B) * cos(L)
Y = (N + h) * cos(B) * sin(L)
Z = (N * (1 - e2) + h) * sin(B)
WGS84:  a = 6378137.0 m,  e2 = 0.00669437999014
```

Cesium wraps this for you - `Cartesian3.fromDegrees(lon, lat, h)` returns the
ECEF vector - but knowing it explains why the globe behaves as it does.

The **camera** lives in the same frame. It has a **position** (an ECEF point),
an orientation (**heading, pitch, roll**), and a field of view. Flying the
camera is just moving that ECEF position and re-aiming it:

```javascript
// Fly the camera to an ECEF position looking down at a slight tilt
viewer.camera.flyTo({
  destination: Cesium.Cartesian3.fromDegrees(151.215, -33.856, 4000),
  orientation: {
    heading: Cesium.Math.toRadians(0),     // north
    pitch:   Cesium.Math.toRadians(-45),   // look down at 45 degrees
    roll:    0,
  },
});
```

Consequences worth remembering:

- **"Up" is local, not global** - up is away from the Earth's centre, so it
  differs at every location. Placing an upright model uses a **local
  east-north-up (ENU)** frame derived from its ECEF position.
- **Large coordinates, precision care** - ECEF values are millions of metres;
  32-bit floats lose precision, so engines subtract a local origin (relative
  to eye) before sending geometry to the GPU.
- **Great-circle reality** - straight lines in lon/lat are not straight in 3D;
  a flight path is a curve over the ellipsoid, computed in ECEF.

```mermaid
graph LR
    GEO["Longitude latitude height"] --> CONV["Ellipsoid to ECEF formula"]
    CONV --> ECEF["ECEF X Y Z metres"]
    ECEF --> CAMPOS["Camera position"]
    CAMPOS --> ORIENT["Heading pitch roll"]
    ORIENT --> VIEWM["View matrix"]
    ECEF --> ENU["Local east north up"]
    ENU --> UPRIGHT["Place upright models"]
```

Remember: geographic coordinates are for humans; ECEF Cartesian metres are
for the globe. The camera is an ECEF position plus an orientation, and "up"
is always local - away from the planet's centre.
""",
        ),
        quiz_lesson(
            "Quiz: Camera, coordinates and the virtual globe (ECEF)",
            (
                q(
                    "What is the ECEF (Earth-Centered, Earth-Fixed) coordinate system?",
                    (
                        opt("A 2D pixel grid on the screen"),
                        opt(
                            "A 3D Cartesian frame in metres with its origin at the "
                            "Earth's centre and axes that rotate with the Earth",
                            correct=True,
                        ),
                        opt("A color space for imagery"),
                        opt("A file compression scheme"),
                    ),
                    "ECEF (EPSG:4978) is the geocentric frame the globe does its 3D "
                    "math in; fixed ground points keep constant coordinates.",
                ),
                q(
                    "Why is 'up' different at every location on a virtual globe?",
                    (
                        opt("Because imagery tiles rotate"),
                        opt(
                            "Up points away from the Earth's centre, so its direction "
                            "changes with position - upright models use a local "
                            "east-north-up frame",
                            correct=True,
                        ),
                        opt("Because the camera has no orientation"),
                        opt("Up is always the global Z axis everywhere"),
                    ),
                    "On a globe, local up is radial; placing things upright needs the "
                    "ENU frame at that point.",
                ),
                q(
                    "Why do globe engines subtract a local origin before sending "
                    "geometry to the GPU?",
                    (
                        opt("To change the map projection"),
                        opt(
                            "ECEF values are millions of metres, and 32-bit floats lose "
                            "precision at that scale, causing jitter",
                            correct=True,
                        ),
                        opt("To hide the coordinates from users"),
                        opt("Because the GPU cannot do addition"),
                    ),
                    "Relative-to-eye (or relative-to-center) positioning preserves "
                    "precision for the GPU's 32-bit floats.",
                ),
            ),
        ),
        # -- 8. Building a 3D geospatial scene -------------------------
        _t(
            "Building a 3D geospatial scene",
            "9 min",
            """# Building a 3D geospatial scene

Now assemble every piece into one running scene. A realistic 3D geospatial
view layers, in order:

1. **The globe** - a WGS84 digital Earth (Cesium Viewer).
2. **Terrain** - streamed elevation gives the ground its shape.
3. **Imagery** - satellite or basemap tiles drape appearance over terrain.
4. **3D Tiles** - a city, photogrammetry mesh, or point cloud streams in by
   geometric error, its leaves being glTF.
5. **glTF models** - individual assets (a sensor, a vehicle) placed at ECEF
   positions with local ENU orientation.
6. **The camera** - flown to an ECEF position with heading/pitch/roll to
   frame the story; the GPU pipeline renders each frame.

One coherent CesiumJS scene does all of it:

```javascript
// A complete 3D geospatial scene: globe + terrain + tiles + model + camera
const viewer = new Cesium.Viewer("cesiumContainer", {
  terrain: Cesium.Terrain.fromWorldTerrain(),            // 2. terrain shape
});

// 4. Stream a massive 3D Tiles city dataset (leaves are glTF)
const city = await Cesium.Cesium3DTileset.fromIonAssetId(75343);
viewer.scene.primitives.add(city);

// 5. Place one glTF model at a real position, clamped upright via ENU
const pos = Cesium.Cartesian3.fromDegrees(-75.152, 39.947, 20);
viewer.entities.add({
  position: pos,
  orientation: Cesium.Transforms.headingPitchRollQuaternion(
    pos, new Cesium.HeadingPitchRoll(0, 0, 0)),          // local ENU upright
  model: { uri: "sensor.glb", minimumPixelSize: 64 },    // a .glb model
});

// 6. Fly the camera in to frame the scene
viewer.camera.flyTo({
  destination: Cesium.Cartesian3.fromDegrees(-75.152, 39.945, 900),
  orientation: { pitch: Cesium.Math.toRadians(-35) },
});
```

Everything you learned is present: geographic authoring converted to **ECEF**,
**terrain** and **imagery** as streamed tile pyramids, **3D Tiles** descending
by **geometric error**, **glTF** leaves and models loaded straight by the
**GPU pipeline**, and a **camera** positioned in the globe's 3D frame.

Good scenes also mind the details: enable lighting and the sun for realistic
**PBR** shading, clamp ground features to terrain, budget tiles for the
device, and keep level of detail honest so the pipeline stays fast.

```mermaid
graph TD
    GLOBE["WGS84 globe"] --> TERR["Streamed terrain"]
    TERR --> IMG["Draped imagery"]
    IMG --> TILES["3D Tiles by geometric error"]
    TILES --> MODELS["glTF models at ECEF"]
    MODELS --> CAM["Camera position and orientation"]
    CAM --> GPU["GPU pipeline renders frame"]
    GPU --> SCENE["Interactive 3D geospatial scene"]
```

Remember: a 3D geospatial scene is the whole course in one place - a
streaming globe of terrain, imagery, 3D Tiles, and glTF, addressed in ECEF
and drawn by the GPU. Start with the globe and add one layer at a time.
""",
        ),
        quiz_lesson(
            "Quiz: Building a 3D geospatial scene",
            (
                q(
                    "In a layered 3D geospatial scene, what is the correct base that "
                    "everything else builds on?",
                    (
                        opt("The glTF models"),
                        opt(
                            "The WGS84 digital globe, onto which terrain, imagery, 3D "
                            "Tiles and models are then added",
                            correct=True,
                        ),
                        opt("The camera flight path"),
                        opt("The fragment shader"),
                    ),
                    "Start with the globe, add terrain and imagery, then stream 3D "
                    "Tiles and place models, then frame with the camera.",
                ),
                q(
                    "When you place a single glTF model in the scene, why use a local "
                    "east-north-up (ENU) orientation?",
                    (
                        opt("To compress the model"),
                        opt(
                            "So the model stands upright relative to the ground at that "
                            "location, since 'up' is local on a globe",
                            correct=True,
                        ),
                        opt("To change its color"),
                        opt("To skip the GPU"),
                    ),
                    "Up is radial and location-dependent; the ENU frame at the model's "
                    "ECEF position makes it stand correctly.",
                ),
                q(
                    "Which statement best captures how the pieces fit together?",
                    (
                        opt("Each format works in complete isolation"),
                        opt(
                            "Geographic coordinates convert to ECEF; terrain and "
                            "imagery stream as tiles; 3D Tiles descend by geometric "
                            "error to glTF leaves; the GPU pipeline renders each frame",
                            correct=True,
                        ),
                        opt("Only 2D tiles are ever used"),
                        opt("The GPU is not involved in a globe"),
                    ),
                    "The scene ties every lesson together: authoring, coordinates, "
                    "streaming standards, and the rendering pipeline.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the fundamental advantage of a 3D globe over a flat projected map?",
                    (
                        opt("It uses fewer colors"),
                        opt(
                            "It renders the Earth as a curved body, avoiding the area/"
                            "angle/distance distortion every flat projection forces and "
                            "adding real terrain and 3D structure",
                            correct=True,
                        ),
                        opt("It never needs to stream data"),
                        opt("It removes the need for coordinates"),
                    ),
                    "A globe keeps the geometry honest and can show elevation and "
                    "planetary-scale context.",
                ),
                q(
                    "What is CesiumJS's role in 3D geospatial visualization?",
                    (
                        opt("A 2D charting library"),
                        opt(
                            "An open WebGL engine that renders a streaming WGS84 globe "
                            "and natively reads glTF and 3D Tiles",
                            correct=True,
                        ),
                        opt("A spreadsheet tool"),
                        opt("A raster DEM file format"),
                    ),
                    "Cesium is the platform on which terrain, imagery, glTF and 3D "
                    "Tiles come together, and it authored the 3D Tiles standard.",
                ),
                q(
                    "How do terrain and imagery differ on a globe?",
                    (
                        opt("They are the same layer"),
                        opt(
                            "Terrain is the elevation shape (a DEM); imagery is the "
                            "picture draped over that shape - decoupled layers",
                            correct=True,
                        ),
                        opt("Terrain is 2D, imagery is 3D"),
                        opt("Imagery stores heights"),
                    ),
                    "Shape vs skin; both stream as tile pyramids chosen by camera distance.",
                ),
                q(
                    "Why is glTF called the 'JPEG of 3D'?",
                    (
                        opt("It only stores photos"),
                        opt(
                            "It is a compact, runtime-ready 3D model format that GPUs "
                            "and engines load directly, without heavy conversion",
                            correct=True,
                        ),
                        opt("It is limited to 2D"),
                        opt("It cannot store geometry"),
                    ),
                    "glTF is the interchange-and-delivery standard for 3D models, and "
                    "it is the leaf content of 3D Tiles.",
                ),
                q(
                    "In 3D Tiles, what drives the decision to load finer child tiles?",
                    (
                        opt("The file name"),
                        opt(
                            "A tile's geometric error exceeding a threshold for the "
                            "current camera distance - so the engine descends the "
                            "bounding-volume tree",
                            correct=True,
                        ),
                        opt("The imagery color"),
                        opt("The time of day"),
                    ),
                    "Geometric error is the level-of-detail signal; only visible, "
                    "detail-warranting tiles load.",
                ),
                q(
                    "What sits at the leaves of a 3D Tiles tileset?",
                    (
                        opt("SQL tables"),
                        opt(
                            "glTF geometry or point-cloud data - which is why glTF and "
                            "3D Tiles are complementary standards",
                            correct=True,
                        ),
                        opt("Plain CSV files"),
                        opt("2D map tiles only"),
                    ),
                    "The tileset.json is the spatial tree; its content is glTF or point data.",
                ),
                q(
                    "In the GPU graphics pipeline, what does the vertex shader do?",
                    (
                        opt("Samples imagery textures per pixel"),
                        opt(
                            "Transforms each vertex through model-view-projection "
                            "matrices toward screen space, once per vertex",
                            correct=True,
                        ),
                        opt("Writes the final pixel color"),
                        opt("Compresses the geometry on disk"),
                    ),
                    "Per-pixel color and texture sampling happen in the fragment "
                    "shader; the vertex shader handles the coordinate transform.",
                ),
                q(
                    "What is the ECEF coordinate system used for on a virtual globe?",
                    (
                        opt("Screen pixel positions"),
                        opt(
                            "A 3D Cartesian frame in metres, centred on the Earth, in "
                            "which the globe does its math and the camera is positioned",
                            correct=True,
                        ),
                        opt("A color palette"),
                        opt("A 2D tile index"),
                    ),
                    "You author in lon/lat/height; the engine converts to ECEF "
                    "(EPSG:4978) for the actual 3D geometry and camera.",
                ),
                q(
                    "Why is 'up' location-dependent on a globe, and why does it "
                    "matter for placing models?",
                    (
                        opt("Up is a fixed global axis, so it never matters"),
                        opt(
                            "Up points away from the Earth's centre and changes with "
                            "position, so upright models must use a local east-north-up "
                            "frame at their location",
                            correct=True,
                        ),
                        opt("Up depends on the imagery provider"),
                        opt("Models never need orientation"),
                    ),
                    "Local ENU derived from a point's ECEF position is what makes a "
                    "placed model stand upright on the curved surface.",
                ),
                q(
                    "Which statement best summarizes how a full 3D geospatial scene fits together?",
                    (
                        opt("Each standard works in isolation with no shared frame"),
                        opt(
                            "A WGS84 globe carries streamed terrain and imagery, 3D "
                            "Tiles descend by geometric error to glTF leaves, models "
                            "sit at ECEF positions, and the GPU pipeline renders each "
                            "frame",
                            correct=True,
                        ),
                        opt("Only flat 2D tiles are involved"),
                        opt("The GPU plays no part in rendering the globe"),
                    ),
                    "The scene is the whole course in one place: authoring, "
                    "coordinates, streaming standards, and the rendering pipeline.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

GEOSPATIAL_3D_VISUALIZATION_COURSES: tuple[SeedCourse, ...] = (_THREE_D_GEOSPATIAL_VISUALIZATION,)
