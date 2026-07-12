"""Academy seed content - Satellite Earth Observation.

The satellites and platforms that watch the planet - the public workhorses
(Sentinel, Landsat, MODIS) and the commercial fleets (Planet, Maxar) - and
the catalogues and cloud platforms (Copernicus, Google Earth Engine, STAC)
that make petabytes of their imagery searchable and usable. Every lesson is
a direct explanation with a concrete example (a STAC JSON fragment, an Earth
Engine snippet, or a data table) and a mermaid diagram, followed by a
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


_SATELLITE_EARTH_OBSERVATION = SeedCourse(
    slug="satellite-earth-observation",
    title="Satellite Earth Observation",
    description=(
        "The satellites and platforms that watch the planet - Sentinel, "
        "Landsat, MODIS, Planet and Maxar - and the catalogues and cloud "
        "platforms (Copernicus, Google Earth Engine, STAC) that make their "
        "data usable. Every lesson pairs a direct explanation with a real "
        "STAC fragment, Earth Engine snippet or data table and a diagram."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Satellite Earth Observation

A fleet of satellites images the entire planet on a schedule - some daily,
some every few days, some at sub-meter detail on demand. The hard part is
no longer taking the picture; it is **finding, accessing, and processing**
the right scene out of petabytes. This course is about the platforms that
watch Earth and the catalogues and cloud tools that make their data
usable.

The approach is **concrete**: every lesson explains one idea directly,
shows it in a real example (a STAC JSON fragment, a Google Earth Engine
snippet, or a data table), and draws the structure as a diagram. After
each lesson there is a short quiz; at the end, a final quiz covers the
whole course.

What you will build understanding for, in order:

1. **Missions and orbits** - how sensors, revisit and swath trade off
2. **The Copernicus Sentinel constellation** - Europe's open backbone
3. **Landsat and MODIS** - the multi-decade heritage record
4. **Commercial constellations** - Planet and Maxar
5. **Data products and processing levels** - L1 vs L2, what is corrected
6. **STAC** - the SpatioTemporal Asset Catalog standard
7. **Cloud-native geospatial** - Cloud Optimized GeoTIFF and Earth Engine
8. **Building an ingestion pipeline** - discover to analysis-ready

This is the map of the observing system and the data plumbing behind it.
Knowing which platform and which product to reach for is most of the skill.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the central challenge this course focuses on?",
                    (
                        opt("Building the rockets that launch satellites"),
                        opt(
                            "Finding, accessing and processing the right scene out of "
                            "petabytes of imagery - the data plumbing, not the optics",
                            correct=True,
                        ),
                        opt("Designing camera lenses for space"),
                        opt("Selling satellite imagery to governments"),
                    ),
                    "Taking the picture is solved; discovering and using the right data "
                    "at scale is the modern skill.",
                ),
                q(
                    "What concrete example does each content lesson include?",
                    (
                        opt("A full satellite hardware schematic"),
                        opt(
                            "A STAC JSON fragment, a Google Earth Engine snippet, or a "
                            "data table, plus a mermaid diagram",
                            correct=True,
                        ),
                        opt("Only a paragraph of prose"),
                        opt("A video walkthrough"),
                    ),
                    "Every lesson grounds the idea in a real fragment or table and a "
                    "diagram of the structure or flow.",
                ),
            ),
        ),
        # -- 1. Missions and orbits ------------------------------------
        _t(
            "Earth observation missions and orbits",
            "10 min",
            """# Earth observation missions and orbits

An Earth observation mission is a marriage of a **sensor** and an
**orbit**. The sensor decides *what* you see; the orbit decides *when* and
*where* you see it. Every design is a trade-off between four properties you
can never maximise at once:

- **Spatial resolution** - the ground size of one pixel (10 m for Sentinel-2,
  30 cm for a Maxar tasking).
- **Temporal resolution (revisit)** - how often the same spot is imaged
  again (5 days for Sentinel-2, daily for Planet).
- **Spectral resolution** - how many and how narrow the wavelength bands.
- **Swath width** - how wide a strip each pass covers. Wide swath buys fast
  revisit; narrow swath buys fine detail.

Most imaging satellites fly a **Sun-synchronous orbit (SSO)**: a low Earth
orbit near 700 to 800 km, inclined so the orbital plane precesses to keep a
**fixed local solar time** at every pass. That means consistent illumination
- a scene at 10:30 local time always has similar shadows, which matters for
comparing images across dates. **Geostationary** weather satellites do the
opposite: they sit at 35786 km over the equator and stare at one hemisphere
continuously.

Sensors split into two families. **Passive** sensors record reflected
sunlight or emitted heat (optical, multispectral, thermal) and are blocked
by cloud and darkness. **Active** sensors carry their own illumination -
**Synthetic Aperture Radar (SAR)** sends microwaves and images day or night,
through cloud.

```mermaid
graph TD
    MISSION["Earth observation mission"] --> SENSOR["Sensor"]
    MISSION --> ORBIT["Orbit"]
    SENSOR --> PASSIVE["Passive optical and thermal"]
    SENSOR --> ACTIVE["Active radar and lidar"]
    ORBIT --> SSO["Sun synchronous low orbit"]
    ORBIT --> GEO["Geostationary weather"]
    SSO --> REVISIT["Fixed local time and revisit"]
```

A useful rule of thumb for how many pixels wide a swath is:

```text
pixels_across_track = swath_width / ground_sample_distance
Sentinel-2:  290000 m / 10 m  = 29000 pixels across a 290 km swath
```

Remember: there is no best satellite, only the best trade-off for a
question. Fine detail, fast revisit, wide coverage - pick the two that
matter and accept the third.
""",
        ),
        quiz_lesson(
            "Quiz: Earth observation missions and orbits",
            (
                q(
                    "Why do most imaging satellites use a Sun-synchronous orbit?",
                    (
                        opt("It is the cheapest orbit to reach"),
                        opt(
                            "It keeps a fixed local solar time at every pass, giving "
                            "consistent illumination for comparing images across dates",
                            correct=True,
                        ),
                        opt("It lets the satellite hover over one city"),
                        opt("It avoids all atmospheric drag"),
                    ),
                    "SSO precesses with the Sun so shadows and lighting stay comparable "
                    "between acquisitions.",
                ),
                q(
                    "What is the key advantage of an active SAR sensor over a passive optical one?",
                    (
                        opt("It has higher spectral resolution"),
                        opt("It is always cheaper to build"),
                        opt(
                            "It provides its own illumination, so it images day or night "
                            "and sees through cloud",
                            correct=True,
                        ),
                        opt("It never needs an orbit"),
                    ),
                    "SAR sends its own microwaves; passive sensors depend on sunlight and "
                    "are blocked by cloud and darkness.",
                ),
                q(
                    "In the resolution trade-off, what does a wider swath typically buy?",
                    (
                        opt("Finer spatial resolution"),
                        opt("More spectral bands"),
                        opt(
                            "Faster revisit - a wide strip covers the same spot again sooner",
                            correct=True,
                        ),
                        opt("A geostationary orbit"),
                    ),
                    "Wide swath means more ground per pass and quicker revisit, usually "
                    "at the cost of pixel detail.",
                ),
            ),
        ),
        # -- 2. Copernicus Sentinel ------------------------------------
        _t(
            "The Copernicus Sentinel constellation",
            "10 min",
            """# The Copernicus Sentinel constellation

**Copernicus** is the European Union's Earth observation programme, run
with the European Space Agency (ESA). Its **Sentinel** satellites are the
open backbone of modern remote sensing: full, free and open data, each
mission a numbered pair of identical satellites flown 180 degrees apart to
halve the revisit time.

The core missions, each specialised:

| Mission | Sensor | Resolution | Revisit | Watches |
|---------|--------|-----------|---------|---------|
| Sentinel-1 | C-band SAR | 5 to 20 m | 6 days | Land and ocean, any weather |
| Sentinel-2 | Multispectral, 13 bands | 10 to 60 m | 5 days | Land, vegetation, water |
| Sentinel-3 | Ocean and land colour, thermal | 300 m to 1 km | under 2 days | Ocean, climate |
| Sentinel-5P | Tropomi spectrometer | 3.5 x 5.5 km | daily | Atmosphere, air quality |

**Sentinel-2** is the workhorse for land: 13 bands from visible through
near-infrared to shortwave infrared, at 10 m for the visible and NIR bands.
Those bands feed spectral indices. The most common, the **Normalized
Difference Vegetation Index**, separates healthy vegetation (bright in NIR,
dark in red) from bare ground:

```text
NDVI = (NIR - Red) / (NIR + Red)
Sentinel-2:  NDVI = (B08 - B04) / (B08 + B04)
Range -1 to +1; dense green canopy is roughly 0.6 to 0.9
```

Data reaches you through the **Copernicus Data Space Ecosystem**, which
exposes a browser, an OpenSearch and STAC API, and S3-compatible object
storage. You search by area, date and cloud cover, then download or stream
the assets.

```mermaid
graph LR
    COP["Copernicus programme"] --> S1["Sentinel-1 SAR"]
    COP --> S2["Sentinel-2 multispectral"]
    COP --> S3["Sentinel-3 ocean and land"]
    COP --> S5["Sentinel-5P atmosphere"]
    S2 --> CDSE["Copernicus Data Space"]
    CDSE --> USER["Search stream and download"]
```

Remember: Sentinel gives you global, frequent, multi-sensor coverage for
free. Sentinel-2 for land and vegetation, Sentinel-1 when cloud or night
would defeat an optical sensor.
""",
        ),
        quiz_lesson(
            "Quiz: The Copernicus Sentinel constellation",
            (
                q(
                    "What is the Copernicus programme's defining data policy?",
                    (
                        opt("Data is sold per scene to licensed resellers"),
                        opt(
                            "Full, free and open data - anyone can access Sentinel "
                            "imagery at no cost",
                            correct=True,
                        ),
                        opt("Data is available only to EU governments"),
                        opt("Data is free only for the first year after launch"),
                    ),
                    "Free and open access is the reason Sentinel became the backbone of "
                    "so many operational and research pipelines.",
                ),
                q(
                    "Which Sentinel mission would you choose to map flooding under thick "
                    "cloud cover?",
                    (
                        opt("Sentinel-2, because it has 13 bands"),
                        opt(
                            "Sentinel-1, because its C-band SAR images through cloud, day or night",
                            correct=True,
                        ),
                        opt("Sentinel-5P, because it is daily"),
                        opt("Sentinel-3, because it is high resolution"),
                    ),
                    "Optical Sentinel-2 is blocked by cloud; Sentinel-1 radar sees "
                    "through it, which is why it is the go-to for flood mapping.",
                ),
                q(
                    "Using Sentinel-2 bands, how is NDVI computed?",
                    (
                        opt("(Red - Blue) / (Red + Blue)"),
                        opt(
                            "(NIR - Red) / (NIR + Red), i.e. (B08 - B04) / (B08 + B04)",
                            correct=True,
                        ),
                        opt("(Green + Red) / 2"),
                        opt("NIR multiplied by Red"),
                    ),
                    "NDVI contrasts near-infrared (high for healthy leaves) against red "
                    "(absorbed by chlorophyll).",
                ),
            ),
        ),
        # -- 3. Landsat and MODIS --------------------------------------
        _t(
            "Landsat and MODIS heritage missions",
            "10 min",
            """# Landsat and MODIS heritage missions

Before Sentinel there was **Landsat**, and its record is what makes
long-term change detection possible. A joint NASA and USGS programme,
Landsat has imaged Earth **continuously since 1972** - the longest
unbroken record of the planet's surface from space. Landsat 8 and 9 carry
the OLI and TIRS sensors: 30 m multispectral, 15 m panchromatic, 100 m
thermal, on a 16-day revisit. Two satellites together give an 8-day
effective revisit, and the full archive is **free and open**.

Landsat's continuity is the point. Because band definitions have been kept
comparable across generations, you can build a consistent time series from
the 1980s to today and ask questions like how a coastline, a glacier, or a
city has changed over four decades.

**MODIS** (Moderate Resolution Imaging Spectroradiometer), on NASA's Terra
and Aqua satellites, trades detail for coverage: 36 spectral bands, coarse
resolution (250 m to 1 km), but a **daily global** view. MODIS is built for
science products - vegetation, fire, snow, ocean colour, land surface
temperature - delivered as ready-to-use gridded datasets. Its successor,
**VIIRS** on the Suomi-NPP and NOAA satellites, continues the daily record.

The three occupy different niches:

| Program | Resolution | Revisit | Best for |
|---------|-----------|---------|----------|
| Landsat | 30 m | 16 days (8 with two) | Long-term change, detail |
| MODIS | 250 m to 1 km | Daily | Global monitoring, science |
| Sentinel-2 | 10 m | 5 days | Current high-cadence land |

A frequent pattern is to **fuse** them: MODIS for daily temporal richness,
Landsat or Sentinel-2 for spatial detail.

```mermaid
graph TD
    HERITAGE["Heritage optical record"] --> LANDSAT["Landsat since 1972"]
    HERITAGE --> MODIS["MODIS daily global"]
    LANDSAT --> CHANGE["Multi decade change detection"]
    MODIS --> SCIENCE["Global science products"]
    MODIS --> VIIRS["VIIRS continues the record"]
    CHANGE --> FUSE["Fuse detail with cadence"]
    SCIENCE --> FUSE
```

Remember: Landsat gives you *history and detail*, MODIS and VIIRS give you
*daily reach*. For anything about change over decades, Landsat's unbroken
archive is irreplaceable.
""",
        ),
        quiz_lesson(
            "Quiz: Landsat and MODIS heritage missions",
            (
                q(
                    "Why is the Landsat archive uniquely valuable for change detection?",
                    (
                        opt("It has the highest spatial resolution of any satellite"),
                        opt(
                            "It provides the longest unbroken record of Earth's surface, "
                            "continuous since 1972 with comparable bands",
                            correct=True,
                        ),
                        opt("It images every location every day"),
                        opt("It is the only free dataset"),
                    ),
                    "Over 50 years of comparable observations lets you measure decadal "
                    "change no newer mission can reach back to.",
                ),
                q(
                    "What does MODIS trade to achieve a daily global view?",
                    (
                        opt("Spectral bands - it has only three"),
                        opt(
                            "Spatial resolution - it is coarse (250 m to 1 km) in "
                            "exchange for daily coverage",
                            correct=True,
                        ),
                        opt("It is not free to access"),
                        opt("It only images the oceans"),
                    ),
                    "MODIS is built for coverage and science products, not fine detail; "
                    "Landsat or Sentinel-2 supply the detail.",
                ),
                q(
                    "A common fusion strategy combines which strengths?",
                    (
                        opt("Two coarse sensors for redundancy"),
                        opt(
                            "MODIS daily cadence with Landsat or Sentinel-2 spatial detail",
                            correct=True,
                        ),
                        opt("SAR and geostationary weather only"),
                        opt("Panchromatic bands from two satellites"),
                    ),
                    "Fusion borrows daily temporal richness from MODIS and fine spatial "
                    "detail from the 10 to 30 m sensors.",
                ),
            ),
        ),
        # -- 4. Commercial constellations ------------------------------
        _t(
            "Commercial constellations (Planet, Maxar)",
            "10 min",
            """# Commercial constellations (Planet, Maxar)

Public missions give you free, medium-resolution, scheduled coverage. The
commercial sector fills two gaps the public fleet cannot: **daily
everywhere** and **very high resolution on demand**. Two companies define
the market.

**Planet** operates the largest imaging constellation ever flown -
**hundreds of small "Dove" satellites** in a line, each about the size of a
loaf of bread, that together **image the entire land surface every day** at
roughly 3 m. This is a different philosophy from a handful of exquisite
satellites: many cheap ones, refreshed often, giving a daily "scan" of the
planet. Planet also flies **SkySat** for higher-resolution (about 50 cm)
tasking.

**Maxar** takes the opposite approach - a few very capable satellites
(WorldView, GeoEye) delivering **sub-30 cm** imagery, the sharpest
commercially available. You do not get daily global coverage; you **task**
the satellite to point at a specific area, and it captures it on the next
suitable pass.

That distinction - **archive** versus **tasking** - is fundamental to
commercial imagery:

- **Archive** - already-captured imagery you can browse and buy now.
- **Tasking** - you request a fresh capture of an area on a future pass,
  paying for priority and a delivery window.

| Provider | Approach | Resolution | Cadence | Model |
|----------|----------|-----------|---------|-------|
| Planet Dove | Many small sats | ~3 m | Daily global | Subscription |
| Planet SkySat | High-res agile | ~50 cm | Tasked | Archive and tasking |
| Maxar WorldView | Few large sats | Under 30 cm | Tasked | Archive and tasking |

```mermaid
graph TD
    COMMERCIAL["Commercial imagery"] --> PLANET["Planet many small sats"]
    COMMERCIAL --> MAXAR["Maxar few large sats"]
    PLANET --> DAILY["Daily global at medium detail"]
    MAXAR --> VHR["Sub 30 cm very high resolution"]
    COMMERCIAL --> ARCHIVE["Archive buy existing"]
    COMMERCIAL --> TASKING["Tasking request new capture"]
```

Remember: reach for commercial when free public data is too infrequent or
too coarse. Planet when you need *every day*, Maxar when you need *every
detail* - and know whether you are buying from the archive or tasking a new
shot.
""",
        ),
        quiz_lesson(
            "Quiz: Commercial constellations (Planet, Maxar)",
            (
                q(
                    "What is Planet's core operating philosophy?",
                    (
                        opt("A single very large satellite in geostationary orbit"),
                        opt(
                            "Hundreds of small Dove satellites that image the entire "
                            "land surface every day at medium resolution",
                            correct=True,
                        ),
                        opt("Sub-10 cm imagery of a few cities only"),
                        opt("Radar imaging through cloud"),
                    ),
                    "Planet flies many cheap small sats for daily global cadence, a "
                    "different bet from a few exquisite satellites.",
                ),
                q(
                    "What does Maxar specialise in?",
                    (
                        opt("Daily global coverage at 3 m"),
                        opt("Free and open medium-resolution data"),
                        opt(
                            "A few very capable satellites delivering the sharpest "
                            "commercial imagery, under 30 cm",
                            correct=True,
                        ),
                        opt("Atmospheric air-quality monitoring"),
                    ),
                    "Maxar's WorldView and GeoEye satellites are tasked for sub-30 cm "
                    "detail, not daily blanket coverage.",
                ),
                q(
                    "What is the difference between archive and tasking?",
                    (
                        opt("Archive is free; tasking is paid"),
                        opt(
                            "Archive is already-captured imagery you can buy now; tasking "
                            "requests a fresh capture on a future pass",
                            correct=True,
                        ),
                        opt("Archive is radar; tasking is optical"),
                        opt("They are two names for the same thing"),
                    ),
                    "Tasking pays for a new, prioritised acquisition; archive sells what "
                    "has already been imaged.",
                ),
            ),
        ),
        # -- 5. Data products and processing levels --------------------
        _t(
            "Data products and processing levels (L1, L2)",
            "10 min",
            """# Data products and processing levels (L1, L2)

Raw sensor output is not something you analyse directly. Between the
satellite and your map lies a **processing chain**, and each stage has a
**level number**. Knowing which level you have tells you exactly what has
and has not been corrected - and getting this wrong silently corrupts every
result downstream.

The widely used NASA and ESA level scheme:

- **Level 0** - raw instrument data, as downlinked. Not for users.
- **Level 1** - calibrated and **georeferenced**. Pixel values are
  **top-of-atmosphere (TOA) reflectance**: what the sensor saw, including
  whatever the atmosphere added. (Sentinel-2 calls this **L1C**.)
- **Level 2** - **atmospherically corrected** to **surface (bottom-of-
  atmosphere) reflectance**: the atmosphere's effect is modelled and
  removed, so pixels represent the actual ground. (Sentinel-2 **L2A**;
  Landsat "Surface Reflectance".)
- **Level 3** - resampled onto a regular grid and often **composited** over
  time (for example a cloud-free monthly mosaic).
- **Level 4** - modelled or derived variables (biomass, evapotranspiration).

The critical jump is **L1 to L2**. The atmosphere scatters and absorbs
light, so the same field looks different on a hazy day and a clear one at
L1. **Atmospheric correction** removes that so a spectral index is
comparable across dates and places. **For any quantitative time series -
NDVI trends, classification, change detection - start from L2 surface
reflectance.** Use L1 only when you intend to run your own atmospheric
correction.

```mermaid
graph LR
    L0["L0 raw instrument"] --> L1["L1 top of atmosphere"]
    L1 --> L2["L2 surface reflectance"]
    L2 --> L3["L3 gridded composite"]
    L3 --> L4["L4 derived variables"]
    L1 --> TOA["Includes atmosphere"]
    L2 --> BOA["Atmosphere removed"]
```

A compact way to remember the reflectance conversion at L1:

```text
TOA reflectance = pi * L * d^2 / (ESUN * cos(theta_z))
  L      = at-sensor radiance
  d      = Earth to Sun distance in AU
  ESUN   = mean solar irradiance for the band
  theta_z = solar zenith angle
```

Remember: the level number is a contract about what has been corrected.
L1C is top-of-atmosphere, L2A is surface. For comparable, quantitative
work, insist on L2.
""",
        ),
        quiz_lesson(
            "Quiz: Data products and processing levels (L1, L2)",
            (
                q(
                    "What is the key difference between Level 1 and Level 2 optical products?",
                    (
                        opt("Level 2 is lower resolution"),
                        opt(
                            "Level 1 is top-of-atmosphere reflectance; Level 2 is "
                            "atmospherically corrected to surface reflectance",
                            correct=True,
                        ),
                        opt("Level 1 is free and Level 2 is paid"),
                        opt("Level 2 has fewer spectral bands"),
                    ),
                    "The L1 to L2 jump removes the atmosphere's effect, giving values "
                    "that represent the actual ground.",
                ),
                q(
                    "For a multi-date NDVI time series, which level should you start from and why?",
                    (
                        opt("Level 0, because it is the rawest and most accurate"),
                        opt(
                            "Level 2 surface reflectance, so the index is comparable "
                            "across dates regardless of atmospheric haze",
                            correct=True,
                        ),
                        opt("Level 1, because atmosphere adds useful signal"),
                        opt("Any level works identically"),
                    ),
                    "Atmospheric correction (L2) makes indices comparable over time; L1 "
                    "values shift with haze and would corrupt the trend.",
                ),
                q(
                    "In Sentinel-2 terms, which pairing is correct?",
                    (
                        opt("L1C is surface reflectance, L2A is top-of-atmosphere"),
                        opt(
                            "L1C is top-of-atmosphere reflectance, L2A is surface "
                            "(bottom-of-atmosphere) reflectance",
                            correct=True,
                        ),
                        opt("L1C and L2A are identical products"),
                        opt("L2A is the raw Level 0 data"),
                    ),
                    "Sentinel-2 L1C = TOA, L2A = atmospherically corrected surface reflectance.",
                ),
            ),
        ),
        # -- 6. STAC ---------------------------------------------------
        _t(
            "The SpatioTemporal Asset Catalog (STAC)",
            "10 min",
            """# The SpatioTemporal Asset Catalog (STAC)

Every provider once had its own metadata format and its own search API, so
combining Landsat, Sentinel and commercial imagery meant writing bespoke
code for each. **STAC - the SpatioTemporal Asset Catalog** - is the open
standard that ended that. It is a simple JSON specification for describing
**any asset with a footprint and a timestamp**, so one client can search
many archives the same way.

STAC has a small vocabulary:

- **Item** - a single scene: a GeoJSON Feature with a geometry (footprint),
  a `datetime`, `properties`, and **assets** (links to the actual files -
  each band, a thumbnail, metadata).
- **Collection** - a group of related Items sharing a description and
  licence (for example "Sentinel-2 L2A").
- **Catalog** - a tree that organises Collections and Items.
- **STAC API** - a dynamic search endpoint: `POST /search` with a bounding
  box, datetime range and property filters returns matching Items.

A trimmed STAC Item shows the shape:

```json
{
  "stac_version": "1.0.0",
  "type": "Feature",
  "id": "S2B_MSIL2A_20240115_T31UDQ",
  "collection": "sentinel-2-l2a",
  "geometry": { "type": "Polygon", "coordinates": [[[2.0,48.8],[2.5,48.8],[2.5,49.1],[2.0,49.1],[2.0,48.8]]] },
  "properties": {
    "datetime": "2024-01-15T10:36:19Z",
    "eo:cloud_cover": 4.2,
    "proj:epsg": 32631
  },
  "assets": {
    "red":  { "href": "s3://.../B04.tif", "type": "image/tiff; application=geotiff; profile=cloud-optimized" },
    "nir":  { "href": "s3://.../B08.tif", "type": "image/tiff; application=geotiff; profile=cloud-optimized" }
  }
}
```

A STAC API search is uniform across providers:

```json
{
  "collections": ["sentinel-2-l2a"],
  "bbox": [2.0, 48.8, 2.5, 49.1],
  "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
  "query": { "eo:cloud_cover": { "lt": 10 } }
}
```

```mermaid
graph TD
    CATALOG["STAC Catalog"] --> COLLECTION["Collection Sentinel-2 L2A"]
    COLLECTION --> ITEM["Item one scene"]
    ITEM --> GEOM["Geometry footprint"]
    ITEM --> TIME["Datetime"]
    ITEM --> ASSETS["Assets band files"]
    API["STAC API search"] --> ITEM
```

Remember: STAC is the lingua franca of geospatial discovery. Learn the
Item-Collection-Catalog model once and you can query Copernicus, USGS,
Planet, Microsoft and AWS archives with the same client.
""",
        ),
        quiz_lesson(
            "Quiz: The SpatioTemporal Asset Catalog (STAC)",
            (
                q(
                    "What problem does STAC solve?",
                    (
                        opt("It compresses satellite imagery"),
                        opt(
                            "It is one open JSON standard for describing and searching "
                            "geospatial assets, so a single client works across many "
                            "archives",
                            correct=True,
                        ),
                        opt("It replaces the need for atmospheric correction"),
                        opt("It launches new satellites"),
                    ),
                    "Before STAC every provider had a bespoke format and API; STAC "
                    "unifies discovery across them.",
                ),
                q(
                    "In the STAC model, what is an Item?",
                    (
                        opt("A whole satellite constellation"),
                        opt(
                            "A single scene - a GeoJSON Feature with a footprint, a "
                            "datetime, properties and asset links",
                            correct=True,
                        ),
                        opt("The company that owns the data"),
                        opt("A compression codec"),
                    ),
                    "An Item is one scene; Collections group Items and a Catalog "
                    "organises Collections.",
                ),
                q(
                    "What does a STAC API /search request typically take?",
                    (
                        opt("Only a filename"),
                        opt(
                            "A bounding box, a datetime range and property filters such "
                            "as maximum cloud cover",
                            correct=True,
                        ),
                        opt("The raw pixel array"),
                        opt("A satellite serial number only"),
                    ),
                    "You query by space (bbox), time (datetime range) and properties "
                    "(e.g. eo:cloud_cover), and get matching Items back.",
                ),
            ),
        ),
        # -- 7. Cloud-native geospatial --------------------------------
        _t(
            "Cloud-native geospatial (COG, Google Earth Engine)",
            "10 min",
            """# Cloud-native geospatial (COG, Google Earth Engine)

The old workflow was **download then process**: copy whole scenes to your
machine, then open them. At petabyte scale that breaks - you cannot
download the archive. **Cloud-native geospatial** flips it: leave the data
in object storage and read only the bytes you need, or push your
computation to where the data already lives.

Two technologies make this work.

**Cloud Optimized GeoTIFF (COG)** is an ordinary GeoTIFF laid out so it can
be **read partially over HTTP**. It stores internal **tiles** and
**overviews** (downsampled pyramids), and the layout is described up front.
A client issues an HTTP **range request** for just the tiles covering your
area of interest, at just the zoom you need - reading a few megabytes of a
multi-gigabyte file without downloading the rest. STAC assets are
overwhelmingly COGs, which is what makes streaming search results practical.

```python
# rioxarray reads only the window it needs from a remote COG - no full download
import rioxarray
url = "https://storage.example.com/sentinel-2/B08.tif"
da = rioxarray.open_rasterio(url)                 # opens headers only
window = da.rio.clip_box(2.30, 48.85, 2.36, 48.88)  # HTTP range reads
print(window.mean().item())
```

**Google Earth Engine (GEE)** takes the other route: instead of you pulling
data, you send *code* to Google's servers, where the entire public archive
(Sentinel, Landsat, MODIS and more) already sits. You describe a
computation over image collections and it runs, parallelised, next to the
petabytes:

```python
import ee
ee.Initialize()
aoi = ee.Geometry.Rectangle([2.0, 48.8, 2.5, 49.1])
col = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
       .filterBounds(aoi)
       .filterDate("2024-06-01", "2024-08-31")
       .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20)))
composite = col.median()                          # cloud-light summer mosaic
ndvi = composite.normalizedDifference(["B8", "B4"])  # server-side NDVI
```

```mermaid
graph LR
    OLD["Download then process"] --> LIMIT["Breaks at petabyte scale"]
    CLOUD["Cloud native geospatial"] --> COG["COG partial range reads"]
    CLOUD --> GEE["Earth Engine bring code to data"]
    COG --> STREAM["Stream only tiles you need"]
    GEE --> PARALLEL["Compute beside the archive"]
```

Remember: do not move the data if you do not have to. COG lets a client
read only the window it needs; Earth Engine lets you run analysis where the
whole archive already lives.
""",
        ),
        quiz_lesson(
            "Quiz: Cloud-native geospatial (COG, Google Earth Engine)",
            (
                q(
                    "What makes a Cloud Optimized GeoTIFF cloud-optimized?",
                    (
                        opt("It is stored in a proprietary compressed format"),
                        opt(
                            "Its internal tiles and overviews let a client read just the "
                            "bytes it needs over HTTP range requests, without "
                            "downloading the whole file",
                            correct=True,
                        ),
                        opt("It can only be opened in the cloud, never locally"),
                        opt("It removes all metadata to shrink the file"),
                    ),
                    "Tiling plus overviews plus a known layout enables partial reads - "
                    "the foundation of streaming geospatial data.",
                ),
                q(
                    "How does Google Earth Engine differ from the download-then-process model?",
                    (
                        opt("It emails you the scenes faster"),
                        opt(
                            "You send code to Google's servers where the archive already "
                            "lives, computing next to the data instead of pulling it",
                            correct=True,
                        ),
                        opt("It only works on data already on your laptop"),
                        opt("It converts imagery to CSV before processing"),
                    ),
                    "GEE brings the computation to the petabytes; you never download the "
                    "underlying archive.",
                ),
                q(
                    "Why are STAC assets overwhelmingly stored as COGs?",
                    (
                        opt("COGs are the only format satellites can produce"),
                        opt(
                            "Because partial HTTP range reads let clients stream just "
                            "the window of a search result, making STAC search "
                            "practical at scale",
                            correct=True,
                        ),
                        opt("COGs cannot store georeferencing"),
                        opt("STAC forbids any other format by law"),
                    ),
                    "STAC discovery plus COG streaming is the pairing that makes working "
                    "with huge archives feasible.",
                ),
            ),
        ),
        # -- 8. Building an ingestion pipeline -------------------------
        _t(
            "Building an ingestion pipeline",
            "10 min",
            """# Building an ingestion pipeline

Now assemble the pieces into one repeatable flow that turns a question ("how
did this farm's vegetation change this summer?") into **analysis-ready
data**. A modern Earth observation ingestion pipeline has five stages.

1. **Discover** - query a STAC API by area of interest, date range and
   cloud cover. You get back Items with COG asset links - no bulk download.
2. **Access** - stream the exact bands and window you need via HTTP range
   reads from the COGs (or push the work to Earth Engine).
3. **Prepare** - reproject to a common CRS, mask cloud using the scene's
   quality band, and clip to the area of interest.
4. **Analyse** - compute indices (NDVI), classify, detect change, or feed
   the stack to a model.
5. **Publish** - write the result as a COG, register it as a new STAC Item,
   and serve it (a tile service, or straight into a dashboard).

The pattern is **Analysis Ready Data (ARD)**: consistently corrected,
gridded, cloud-masked imagery you can stack directly without per-scene
fiddling - the goal every ingestion pipeline is trying to reach.

A discover-and-stream skeleton with `pystac-client` and `stackstac`:

```python
from pystac_client import Client
import stackstac

cat = Client.open("https://earth-search.aws.element84.com/v1")
items = cat.search(
    collections=["sentinel-2-l2a"],
    bbox=[2.30, 48.85, 2.36, 48.88],
    datetime="2024-06-01/2024-08-31",
    query={"eo:cloud_cover": {"lt": 20}},
).item_collection()

stack = stackstac.stack(items, assets=["red", "nir"])   # lazy, streams COGs
ndvi = (stack.sel(band="nir") - stack.sel(band="red")) / \\
       (stack.sel(band="nir") + stack.sel(band="red"))
summer_ndvi = ndvi.median(dim="time")                   # cloud-light composite
```

```mermaid
graph LR
    DISCOVER["Discover via STAC search"] --> ACCESS["Access stream COG bands"]
    ACCESS --> PREPARE["Prepare reproject mask clip"]
    PREPARE --> ANALYSE["Analyse indices and change"]
    ANALYSE --> PUBLISH["Publish COG and STAC Item"]
    PUBLISH --> DISCOVER
```

Notice the loop closes: your published result is itself a STAC Item other
pipelines can discover. Remember the five stages - discover, access,
prepare, analyse, publish - and lean on STAC and COG so you move code and
metadata, not petabytes of pixels.
""",
        ),
        quiz_lesson(
            "Quiz: Building an ingestion pipeline",
            (
                q(
                    "What are the five stages of the ingestion pipeline, in order?",
                    (
                        opt("Launch, orbit, image, downlink, archive"),
                        opt(
                            "Discover, access, prepare, analyse, publish",
                            correct=True,
                        ),
                        opt("Download, compress, email, print, delete"),
                        opt("Task, buy, license, resell, bill"),
                    ),
                    "STAC discovery, streamed access, preparation, analysis, then "
                    "publishing the result as a new STAC Item.",
                ),
                q(
                    "What is Analysis Ready Data (ARD)?",
                    (
                        opt("Raw Level 0 data straight from the sensor"),
                        opt(
                            "Consistently corrected, gridded, cloud-masked imagery you "
                            "can stack directly without per-scene fiddling",
                            correct=True,
                        ),
                        opt("A proprietary format only Maxar can read"),
                        opt("Imagery that has not yet been georeferenced"),
                    ),
                    "ARD is the goal of the pipeline: data prepared so analysis can "
                    "consume it directly.",
                ),
                q(
                    "Why does the pipeline lean on STAC and COG rather than bulk downloads?",
                    (
                        opt("Because bulk downloads are illegal"),
                        opt(
                            "So you move code and metadata instead of petabytes - "
                            "discovering with STAC and streaming only the needed COG "
                            "windows",
                            correct=True,
                        ),
                        opt("Because COGs are smaller than the original scenes"),
                        opt("Because STAC deletes the original data"),
                    ),
                    "At archive scale you cannot download everything; STAC plus COG lets "
                    "you fetch just what each step needs.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Which orbit keeps a fixed local solar time for consistent "
                    "illumination across passes?",
                    (
                        opt("Geostationary orbit"),
                        opt("Sun-synchronous low Earth orbit", correct=True),
                        opt("Highly elliptical Molniya orbit"),
                        opt("Lunar transfer orbit"),
                    ),
                    "Sun-synchronous orbits precess with the Sun so lighting stays "
                    "comparable between acquisitions.",
                ),
                q(
                    "Which Sentinel mission images through cloud, day or night?",
                    (
                        opt("Sentinel-2 multispectral"),
                        opt("Sentinel-1 C-band SAR", correct=True),
                        opt("Sentinel-3 ocean colour"),
                        opt("Sentinel-5P atmosphere"),
                    ),
                    "Radar provides its own illumination and penetrates cloud; optical "
                    "sensors cannot.",
                ),
                q(
                    "What makes the Landsat archive irreplaceable?",
                    (
                        opt("Its sub-meter resolution"),
                        opt(
                            "The longest unbroken surface record, continuous since 1972 "
                            "with comparable bands",
                            correct=True,
                        ),
                        opt("Its daily global coverage"),
                        opt("Its geostationary vantage point"),
                    ),
                    "Over 50 years of comparable data enables decadal change detection.",
                ),
                q(
                    "Planet and Maxar fill which two gaps in public coverage?",
                    (
                        opt("Cheaper launches and bigger rockets"),
                        opt(
                            "Daily-everywhere coverage (Planet) and very high resolution "
                            "on demand (Maxar)",
                            correct=True,
                        ),
                        opt("Free data and open licences"),
                        opt("Atmospheric and ocean science products"),
                    ),
                    "Planet's Doves give daily global cadence; Maxar tasks sub-30 cm detail.",
                ),
                q(
                    "For a comparable multi-date NDVI time series, which product level "
                    "do you want?",
                    (
                        opt("Level 0 raw"),
                        opt("Level 1 top-of-atmosphere"),
                        opt(
                            "Level 2 surface reflectance, atmospherically corrected",
                            correct=True,
                        ),
                        opt("It does not matter"),
                    ),
                    "L2 surface reflectance removes atmospheric variation so indices are "
                    "comparable across dates.",
                ),
                q(
                    "In STAC, what is a Collection?",
                    (
                        opt("A single scene's footprint"),
                        opt(
                            "A group of related Items sharing a description and licence, "
                            "such as Sentinel-2 L2A",
                            correct=True,
                        ),
                        opt("A compression codec for imagery"),
                        opt("The HTTP range request itself"),
                    ),
                    "Items are scenes; a Collection groups related Items; a Catalog "
                    "organises Collections.",
                ),
                q(
                    "What does a Cloud Optimized GeoTIFF enable?",
                    (
                        opt("Faster rocket launches"),
                        opt(
                            "Reading just the tiles and zoom level you need over HTTP "
                            "range requests, without downloading the whole file",
                            correct=True,
                        ),
                        opt("Storing imagery without any georeferencing"),
                        opt("Removing the need for a CRS"),
                    ),
                    "Internal tiling plus overviews plus a known layout make partial "
                    "reads possible.",
                ),
                q(
                    "How does Google Earth Engine change where computation happens?",
                    (
                        opt("It downloads the archive to your laptop first"),
                        opt(
                            "You send code to Google's servers, computing beside the "
                            "petabyte archive instead of pulling the data",
                            correct=True,
                        ),
                        opt("It runs only on data you upload yourself"),
                        opt("It converts everything to spreadsheets"),
                    ),
                    "GEE brings the code to the data - the opposite of download then process.",
                ),
                q(
                    "What are the five stages of an ingestion pipeline?",
                    (
                        opt("Launch, orbit, image, sell, bill"),
                        opt(
                            "Discover, access, prepare, analyse, publish",
                            correct=True,
                        ),
                        opt("Plan, code, build, test, deploy"),
                        opt("Logs, metrics, traces, alerts, dashboards"),
                    ),
                    "Discover with STAC, stream via COG, prepare, analyse, then publish "
                    "the result as a new STAC Item.",
                ),
                q(
                    "What is Analysis Ready Data the pipeline aims to produce?",
                    (
                        opt("Uncorrected raw sensor counts"),
                        opt(
                            "Consistently corrected, gridded, cloud-masked imagery you "
                            "can stack directly",
                            correct=True,
                        ),
                        opt("A proprietary single-vendor format"),
                        opt("Imagery with the atmosphere still included"),
                    ),
                    "ARD is prepared so analysis consumes it directly, without per-scene fiddling.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SATELLITE_EARTH_OBSERVATION_COURSES: tuple[SeedCourse, ...] = (_SATELLITE_EARTH_OBSERVATION,)
