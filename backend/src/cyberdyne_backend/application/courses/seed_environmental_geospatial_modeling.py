"""Academy seed content - Environmental Geospatial Modeling.

An advanced course on modeling Earth systems from geospatial data. It moves
from terrain and hydrology, through meteorology, climate and ocean processes,
into environmental time series and remote sensing, and closes with applied
domains: precision agriculture and forest monitoring, natural-hazard mapping,
and urban digital twins. Every lesson is a direct explanation grounded in real
standards (WGS84, UTM, GDAL, STAC, Sentinel/Landsat, PostGIS, 3D Tiles) with a
concrete formula or code example and a mermaid diagram, followed by a
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


_ENVIRONMENTAL_GEOSPATIAL_MODELING = SeedCourse(
    slug="environmental-geospatial-modeling",
    title="Environmental Geospatial Modeling",
    description=(
        "Model Earth systems from geospatial data: terrain and hydrology, "
        "meteorology and climate, ocean and coastal processes, and remote-sensing "
        "time series - then apply them to precision agriculture, forest monitoring, "
        "disaster mapping and urban digital twins. Every lesson pairs a real "
        "formula or GDAL/rasterio/geopandas example with a diagram."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Environmental Geospatial Modeling

The Earth is a system of coupled processes - water flowing downhill, air
moving heat around the planet, oceans lapping at coasts, vegetation
greening and browning with the seasons. **Geospatial modeling** turns
measurements of these processes, tagged with a location and a time, into
models we can compute on and reason about.

This is an **advanced** course. It assumes you are comfortable with a
coordinate reference system (CRS), a raster versus a vector, and running a
command-line tool. From there we build up the physics-aware side: how to
derive slope from elevation, route water across a landscape, read gridded
climate reanalysis, and track change from satellites.

The approach is **concrete**: every lesson explains one idea directly,
shows it in a short real example (a projection formula, a spectral index,
a rasterio or geopandas snippet, a STAC fragment), and draws the idea as a
diagram. After each lesson there is a short quiz; at the end, a final quiz
covers the whole course.

What you will build understanding for, in order:

1. **Digital elevation models** - terrain, slope and aspect
2. **Hydrological modeling** - flow accumulation and watersheds
3. **Meteorology and climate** - reanalysis and gridded data
4. **Ocean and coastal modeling** - tides, bathymetry, sea level
5. **Environmental time series and remote sensing** - change over time
6. **Precision agriculture and forest monitoring** - vegetation health
7. **Natural hazards and disaster mapping** - flood and fire
8. **Urban analytics and digital twins** - the built environment in 3D

Real data grounds every step: Copernicus DEM, ERA5 reanalysis, Sentinel-1
and Sentinel-2, Landsat, and OGC standards (WMS, WFS, STAC, 3D Tiles).
Let us get started.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What does geospatial modeling fundamentally do?",
                    (
                        opt("Stores photographs of the ground with no location"),
                        opt(
                            "Turns measurements tagged with a location and a time into "
                            "models of Earth processes we can compute on",
                            correct=True,
                        ),
                        opt("Replaces physics with pretty maps"),
                        opt("Only draws country borders"),
                    ),
                    "The location plus time tag is what lets us model coupled Earth "
                    "processes quantitatively.",
                ),
                q(
                    "What level of prior knowledge does this course assume?",
                    (
                        opt("None - it starts from what a map is"),
                        opt(
                            "Advanced comfort with CRSs, raster versus vector, and the "
                            "command line",
                            correct=True,
                        ),
                        opt("A PhD in atmospheric physics"),
                        opt("Only web design experience"),
                    ),
                    "It is an advanced course; the basics of CRS, raster/vector and CLI "
                    "tooling are taken as given.",
                ),
            ),
        ),
        # -- 1. DEM and terrain analysis -------------------------------
        _t(
            "Digital elevation models and terrain analysis",
            "11 min",
            """# Digital elevation models and terrain analysis

A **digital elevation model (DEM)** is a raster where each cell holds a
ground height, usually in metres above a vertical datum such as the EGM2008
geoid. Global DEMs you will meet include **Copernicus GLO-30** (30 m),
**SRTM** (30 m), and **ASTER GDEM**. A DEM is the foundation of almost all
terrain and hydrology work.

Two derivatives dominate terrain analysis, both computed from the local
**gradient** of the surface:

- **Slope** - the steepness of the ground, the magnitude of the gradient.
- **Aspect** - the compass direction the slope faces, the direction of the
  gradient.

The gradient is estimated from a 3x3 window of cells. With cell size `d`
and the eight neighbours labelled by compass point, Horn's method gives the
partial derivatives, then slope and aspect follow:

```text
dz/dx = ((c + 2f + i) - (a + 2d + g)) / (8 * d)
dz/dy = ((g + 2h + i) - (a + 2b + c)) / (8 * d)

slope  = atan( sqrt( (dz/dx)^2 + (dz/dy)^2 ) )        # radians, then to degrees
aspect = atan2( dz/dy, -dz/dx )                        # 0 = east, measured CCW
```

Because slope depends on the horizontal cell size `d`, the DEM and its CRS
must share the **same linear unit**. Compute slope in a projected CRS (UTM,
metres), never in geographic degrees - a degree of longitude is not a fixed
number of metres, so slope in EPSG:4326 is meaningless.

In practice one command does it. GDAL exposes Horn's algorithm directly:

```python
from osgeo import gdal

# reproject to UTM first so x, y and z are all in metres
gdal.Warp("dem_utm.tif", "copernicus_glo30.tif", dstSRS="EPSG:32633")
gdal.DEMProcessing("slope.tif", "dem_utm.tif", "slope")     # degrees
gdal.DEMProcessing("aspect.tif", "dem_utm.tif", "aspect")   # 0-360 from north
gdal.DEMProcessing("hillshade.tif", "dem_utm.tif", "hillshade")
```

Other derivatives build on the same gradient: **hillshade** (a shaded
relief for visualization), **curvature** (rate of change of slope, which
governs where water speeds up or ponds), and **roughness**.

```mermaid
graph LR
    DEM["DEM raster of heights"] --> UTM["Reproject to projected CRS"]
    UTM --> GRAD["Local gradient in 3x3 window"]
    GRAD --> SLOPE["Slope steepness"]
    GRAD --> ASPECT["Aspect facing direction"]
    GRAD --> HS["Hillshade and curvature"]
```

Remember: a DEM plus its gradient gives you slope and aspect - but only if
the horizontal and vertical units match, which means working in a projected
CRS.
""",
        ),
        quiz_lesson(
            "Quiz: Digital elevation models and terrain analysis",
            (
                q(
                    "What does each cell of a digital elevation model store?",
                    (
                        opt("A land-cover class label"),
                        opt("A ground height above a vertical datum", correct=True),
                        opt("A surface temperature"),
                        opt("A street name"),
                    ),
                    "A DEM is a raster of heights, typically metres above a geoid such as EGM2008.",
                ),
                q(
                    "What are slope and aspect derived from?",
                    (
                        opt("The colour of the raster"),
                        opt(
                            "The local gradient of the elevation surface - slope is its "
                            "magnitude, aspect its direction",
                            correct=True,
                        ),
                        opt("The file size of the DEM"),
                        opt("The satellite orbit"),
                    ),
                    "Both come from the gradient estimated over a 3x3 window (Horn's method).",
                ),
                q(
                    "Why should slope be computed in a projected CRS, not EPSG:4326?",
                    (
                        opt("Projected files are smaller"),
                        opt(
                            "Slope needs horizontal and vertical units to match; a degree "
                            "of longitude is not a fixed number of metres, so degrees give "
                            "meaningless slope",
                            correct=True,
                        ),
                        opt("EPSG:4326 cannot store elevation"),
                        opt("GDAL rejects geographic CRSs"),
                    ),
                    "Cell size enters the gradient; mixing degrees of horizontal extent "
                    "with metres of height breaks the calculation.",
                ),
            ),
        ),
        # -- 2. Hydrological modeling ----------------------------------
        _t(
            "Hydrological modeling - flow and watersheds",
            "11 min",
            """# Hydrological modeling - flow and watersheds

Water runs downhill, and a DEM tells us which way is down. **Hydrological
modeling** turns elevation into a picture of where water goes: the streams,
the drainage networks, and the **watersheds** (catchments) that feed them.

The classic pipeline is a sequence of raster steps:

- **Fill sinks** - real DEMs contain spurious pits (single low cells) that
  trap flow. Fill or breach them first, or every downhill path stops there.
- **Flow direction** - for each cell, which neighbour does water drain to?
  The **D8** method points each cell to its single steepest downslope
  neighbour, encoded as one of eight directions.
- **Flow accumulation** - count how many upstream cells drain through each
  cell. High accumulation marks channels; the value is the contributing
  drainage area in cells.
- **Stream network** - threshold the accumulation: cells above a chosen
  area become streams.
- **Watershed** - from an outlet (a pour point), trace all cells that flow
  into it. That set is the catchment.

A cell's contributing area follows directly from accumulation and cell
size:

```text
contributing_area = (flow_accumulation + 1) * cell_size^2

# example: 1250 upstream cells at 30 m resolution
area = (1250 + 1) * 30 * 30 = 1,125,900 m^2  ~= 1.13 km^2
```

Open tools implement the whole chain. Using pysheds in Python:

```python
from pysheds.grid import Grid

grid = Grid.from_raster("dem_utm.tif")
dem  = grid.read_raster("dem_utm.tif")
filled  = grid.fill_depressions(dem)         # remove spurious pits
inflated = grid.resolve_flats(filled)
fdir = grid.flowdir(inflated)                # D8 flow direction
acc  = grid.accumulation(fdir)               # flow accumulation
# delineate the catchment upstream of a pour point (x, y)
catch = grid.catchment(x=x, y=y, fdir=fdir, xytype="coordinate")
```

A key property: watershed boundaries follow ridgelines, and every cell
belongs to exactly one catchment for a given outlet. This is why nested
catchments form a tree - small sub-basins drain into larger ones down to
the river mouth.

```mermaid
graph TD
    DEM["DEM"] --> FILL["Fill sinks"]
    FILL --> DIR["Flow direction D8"]
    DIR --> ACC["Flow accumulation"]
    ACC --> STREAM["Threshold to streams"]
    DIR --> WS["Delineate watershed from outlet"]
    STREAM --> WS
```

Remember: fill, direction, accumulation, then threshold and delineate - a
DEM becomes streams and watersheds through that fixed order of steps.
""",
        ),
        quiz_lesson(
            "Quiz: Hydrological modeling - flow and watersheds",
            (
                q(
                    "Why must you fill sinks before computing flow?",
                    (
                        opt("To make the DEM smaller"),
                        opt(
                            "Spurious single-cell pits trap flow and stop every downhill "
                            "path that reaches them",
                            correct=True,
                        ),
                        opt("To convert metres to feet"),
                        opt("Sinks change the CRS"),
                    ),
                    "Unfilled pits break the drainage network; fill or breach them first.",
                ),
                q(
                    "What does the D8 flow-direction method assign to each cell?",
                    (
                        opt("A random neighbour"),
                        opt(
                            "Its single steepest downslope neighbour, one of eight directions",
                            correct=True,
                        ),
                        opt("The average of all eight neighbours"),
                        opt("The cell directly north"),
                    ),
                    "D8 routes all of a cell's water to the steepest of its eight neighbours.",
                ),
                q(
                    "What does flow accumulation measure?",
                    (
                        opt("The temperature of the water"),
                        opt(
                            "The number of upstream cells draining through each cell - "
                            "its contributing drainage area",
                            correct=True,
                        ),
                        opt("The elevation of the cell"),
                        opt("The rainfall in millimetres"),
                    ),
                    "High accumulation marks channels; multiply by cell area to get "
                    "contributing area.",
                ),
            ),
        ),
        # -- 3. Meteorology and climate --------------------------------
        _t(
            "Meteorology and climate data",
            "11 min",
            """# Meteorology and climate data

Weather and climate arrive as **gridded data**: values on a regular
latitude-longitude mesh, usually with a **time** dimension and often a
**vertical level** (pressure or height). This is fundamentally different
from a single satellite scene - it is a stack of arrays through time, and
the natural container is **NetCDF** or **GRIB**, addressed as a
multidimensional cube.

Two words you must keep apart:

- **Weather** - the state of the atmosphere now and in the coming days.
- **Climate** - the long-term statistics of weather (means, extremes,
  variability) over decades, typically a 30-year normal.

The workhorse dataset is **reanalysis**: a physics model is run over the
historical period and *nudged toward every available observation*
(stations, balloons, satellites) by data assimilation. The result is a
gap-free, physically consistent record of the past atmosphere. **ERA5**
(from ECMWF/Copernicus) is the reference product - hourly, global, ~31 km,
from 1940 to near-present.

You slice these cubes by named dimensions, not pixel indices. With xarray:

```python
import xarray as xr

ds = xr.open_dataset("era5_t2m.nc")          # 2 m air temperature, K
# a point time series: nearest grid cell to Lisbon
lisbon = ds["t2m"].sel(latitude=38.7, longitude=-9.1, method="nearest")
celsius = lisbon - 273.15                     # Kelvin to Celsius
# a climate normal: 1991-2020 mean of each calendar month
normal = ds["t2m"].sel(time=slice("1991", "2020")).groupby("time.month").mean()
```

Two habits prevent classic errors. First, reanalysis temperature is in
**kelvin** - subtract 273.15 for Celsius. Second, many global grids use
**0 to 360 longitude**, not -180 to 180, so a request for -9.1 may need
wrapping to 350.9.

**Anomalies** are how climate signals are read: subtract the long-term
mean (the climatology) so the departure stands out:

```text
anomaly(t) = value(t) - climatology(month_of(t))
# e.g. +2.3 K means this month was 2.3 K warmer than its 1991-2020 normal
```

```mermaid
graph LR
    OBS["Observations stations and satellites"] --> DA["Data assimilation"]
    MODEL["Physics model"] --> DA
    DA --> RA["Reanalysis gridded cube"]
    RA --> SLICE["Slice by lat lon time level"]
    SLICE --> CLIM["Climatology and anomalies"]
```

Remember: gridded climate data is a labelled cube through time; reanalysis
fuses model and observations into a gap-free record, and you read signals
as anomalies from a climatological normal.
""",
        ),
        quiz_lesson(
            "Quiz: Meteorology and climate data",
            (
                q(
                    "What is reanalysis data?",
                    (
                        opt("A single satellite photograph"),
                        opt(
                            "A physics model run over history and nudged toward every "
                            "available observation, giving a gap-free consistent record",
                            correct=True,
                        ),
                        opt("A hand-drawn weather map"),
                        opt("A forecast of next year's climate"),
                    ),
                    "Data assimilation fuses model and observations; ERA5 is the "
                    "reference reanalysis product.",
                ),
                q(
                    "How does climate differ from weather?",
                    (
                        opt("They are identical"),
                        opt(
                            "Weather is the atmosphere's current and near-term state; "
                            "climate is the long-term statistics of weather over decades",
                            correct=True,
                        ),
                        opt("Climate is only about oceans"),
                        opt("Weather is measured in kelvin, climate in Celsius"),
                    ),
                    "Climate is typically a 30-year normal of weather statistics.",
                ),
                q(
                    "Why subtract a climatology to get an anomaly?",
                    (
                        opt("To convert units to feet"),
                        opt(
                            "So the departure from the long-term normal stands out, "
                            "revealing the climate signal",
                            correct=True,
                        ),
                        opt("To delete the time dimension"),
                        opt("To reproject the grid"),
                    ),
                    "Anomaly = value minus the climatological mean for that period.",
                ),
            ),
        ),
        # -- 4. Ocean and coastal modeling -----------------------------
        _t(
            "Ocean and coastal modeling",
            "11 min",
            """# Ocean and coastal modeling

The ocean and the coast are where a lot of environmental risk concentrates,
and modeling them adds ingredients the land does not have: **tides**, a
moving **sea surface**, and depth below the water (**bathymetry**) rather
than height above it.

Key data and concepts:

- **Bathymetry** - the DEM of the sea floor, depth below a vertical datum.
  **GEBCO** is the standard global grid. Combined land-sea elevation models
  merge a DEM and bathymetry across the coastline.
- **Vertical datums matter more here.** Heights on land often use a geoid
  (mean sea level), but coastal engineering uses tidal datums such as
  **mean sea level (MSL)**, **mean lower low water (MLLW)** for charts, and
  **mean higher high water (MHHW)** for flood lines. Mixing datums is a
  classic coastal-flood error.
- **Tides** - the periodic rise and fall of the sea, driven by the Moon and
  Sun. They are modeled as a sum of **harmonic constituents**, each a
  cosine with its own amplitude, frequency and phase.

Tidal height at time `t` is the sum over constituents (M2, S2, K1, O1...):

```text
h(t) = Z0 + sum_i [ A_i * cos( w_i * t - phi_i ) ]

Z0    = mean water level
A_i   = amplitude of constituent i
w_i   = angular speed (M2 is the ~12.42 h lunar semidiurnal)
phi_i = phase lag
```

Coastal-flood exposure is often estimated with a **bathtub model**: pick a
water level, flood every connected cell below it. It is crude (it ignores
flow dynamics) but fast for first-pass mapping:

```python
import numpy as np
import rasterio

with rasterio.open("coastal_dem_mhhw.tif") as src:
    elev = src.read(1)                 # heights relative to the MHHW datum
water_level = 1.2                      # metres of surge above the datum
flooded = elev < water_level          # boolean inundation mask
frac = np.count_nonzero(flooded) / flooded.size
print(f"{frac:.1%} of cells below {water_level} m")
```

Full coastal models go further - **hydrodynamic** models such as ADCIRC or
Delft3D solve the shallow-water equations to simulate storm surge, currents
and wave setup on an unstructured mesh - but the datum discipline and the
harmonic view of tides carry through all of them.

```mermaid
graph TD
    BATHY["Bathymetry sea floor depth"] --> CDEM["Combined land sea model"]
    DATUM["Tidal datums MSL MLLW MHHW"] --> CDEM
    TIDE["Harmonic tide constituents"] --> LEVEL["Water level at time t"]
    LEVEL --> FLOOD["Inundation mapping"]
    CDEM --> FLOOD
```

Remember: coastal modeling combines bathymetry, a carefully chosen tidal
datum, and tides expressed as a sum of harmonic constituents - get the
datum wrong and the flood map is wrong.
""",
        ),
        quiz_lesson(
            "Quiz: Ocean and coastal modeling",
            (
                q(
                    "What is bathymetry?",
                    (
                        opt("The height of coastal buildings"),
                        opt(
                            "The elevation model of the sea floor - depth below a vertical datum",
                            correct=True,
                        ),
                        opt("The salinity of seawater"),
                        opt("The speed of ocean currents"),
                    ),
                    "Bathymetry is the sea-floor DEM; GEBCO is the standard global grid.",
                ),
                q(
                    "How are tides represented in a harmonic tide model?",
                    (
                        opt("As a single straight line"),
                        opt(
                            "As a sum of harmonic constituents, each a cosine with its "
                            "own amplitude, frequency and phase",
                            correct=True,
                        ),
                        opt("As random noise"),
                        opt("As the DEM slope"),
                    ),
                    "Constituents like M2 (lunar semidiurnal) add up to the tidal curve.",
                ),
                q(
                    "Why is choosing the right vertical datum critical in coastal work?",
                    (
                        opt("It changes the file format"),
                        opt(
                            "Land and coastal data use different datums (geoid vs MSL, "
                            "MLLW, MHHW); mixing them produces wrong flood lines",
                            correct=True,
                        ),
                        opt("It has no effect on results"),
                        opt("Datums only matter on land"),
                    ),
                    "Datum mismatch is a classic coastal-flood error - heights must be "
                    "referenced consistently.",
                ),
            ),
        ),
        # -- 5. Environmental time series and remote sensing -----------
        _t(
            "Environmental time series and remote sensing",
            "11 min",
            """# Environmental time series and remote sensing

Satellites revisit the same ground over and over, so a pixel is not one
value but a **time series** - a signal you can watch change. **Optical**
sensors like **Sentinel-2** (5-day revisit, 10-20 m) and **Landsat** (16-
day, 30 m) measure reflected sunlight in several **spectral bands**; from
those bands you compute **indices** that isolate a physical property.

The most important is the **Normalized Difference Vegetation Index
(NDVI)**. Healthy vegetation reflects strongly in the near-infrared and
absorbs red for photosynthesis, so:

```text
NDVI = (NIR - RED) / (NIR + RED)          # ranges -1 to +1

Sentinel-2: NIR = B8, RED = B4
NDVI > 0.6   dense healthy vegetation
NDVI ~ 0.2   sparse or stressed vegetation
NDVI < 0     water, snow, bare rock
```

Other normalized-difference indices follow the same form: **NDWI** for
water (green and NIR), **NBR** for burn severity (NIR and shortwave IR).
Because they are ratios, they partly cancel illumination differences,
which makes them comparable across dates - the basis for **change
detection**.

Clouds are the enemy of optical time series. The fix is to build a
**cloud-free composite**: mask cloudy pixels per scene, then reduce the
stack (median is robust). This is trivial on **Google Earth Engine**, which
hosts the archives and computes server-side:

```python
import ee
ee.Initialize()

def ndvi(img):
    return img.normalizedDifference(["B8", "B4"]).rename("NDVI")

coll = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate("2024-05-01", "2024-09-30")
        .filterBounds(aoi)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(ndvi))
summer_ndvi = coll.median()               # cloud-robust composite
```

To find data in the first place, use **STAC** (SpatioTemporal Asset
Catalog), the open standard for searchable imagery archives. A STAC item is
GeoJSON with time and asset links:

```json
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "S2B_33UUP_20240712",
  "properties": { "datetime": "2024-07-12T10:20:31Z", "eo:cloud_cover": 4.1 },
  "assets": { "B08": { "href": "s3://.../B08.tif", "type": "image/tiff" } }
}
```

When optical fails - persistent cloud, night, smoke - **radar** (Sentinel-1
SAR) sees through it, and **change detection** compares two dates to flag
what moved: deforestation, flooding, new construction.

```mermaid
graph LR
    STAC["STAC search archive"] --> SCENES["Time stack of scenes"]
    SCENES --> MASK["Cloud mask per scene"]
    MASK --> INDEX["Spectral index NDVI NDWI NBR"]
    INDEX --> COMP["Composite median over time"]
    COMP --> CHANGE["Change detection over dates"]
```

Remember: a satellite pixel is a time series; spectral indices distil bands
into a physical signal, composites beat clouds, and comparing dates detects
change.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental time series and remote sensing",
            (
                q(
                    "What does NDVI measure and how is it computed?",
                    (
                        opt("Temperature, from thermal bands only"),
                        opt(
                            "Vegetation greenness, as (NIR - RED) / (NIR + RED)",
                            correct=True,
                        ),
                        opt("Elevation, from the DEM"),
                        opt("Rainfall, from radar"),
                    ),
                    "Healthy vegetation is bright in NIR and dark in red; the normalized "
                    "difference captures that.",
                ),
                q(
                    "Why build a median composite over a stack of scenes?",
                    (
                        opt("To make the image larger"),
                        opt(
                            "To produce a cloud-robust image by masking clouds and "
                            "reducing the time stack",
                            correct=True,
                        ),
                        opt("To change the projection"),
                        opt("To remove the NIR band"),
                    ),
                    "Median over masked scenes is robust to residual clouds and gaps.",
                ),
                q(
                    "What is STAC used for?",
                    (
                        opt("Rendering 3D buildings"),
                        opt(
                            "A standard, searchable catalog of imagery assets described "
                            "as GeoJSON with time and asset links",
                            correct=True,
                        ),
                        opt("Computing slope from a DEM"),
                        opt("Storing tide constituents"),
                    ),
                    "SpatioTemporal Asset Catalog is the open standard for finding "
                    "satellite data by space and time.",
                ),
                q(
                    "When optical imagery is blocked by cloud or night, what still sees "
                    "the ground?",
                    (
                        opt("Nothing - you must wait"),
                        opt("Radar such as Sentinel-1 SAR", correct=True),
                        opt("A brighter optical band"),
                        opt("The DEM"),
                    ),
                    "Synthetic aperture radar penetrates cloud and works day or night.",
                ),
            ),
        ),
        # -- 6. Precision agriculture and forest monitoring ------------
        _t(
            "Precision agriculture and forest monitoring",
            "11 min",
            """# Precision agriculture and forest monitoring

Vegetation is where remote sensing pays off directly. Two applied domains
share the same toolkit but ask different questions: **precision
agriculture** manages a single field intensively over a season, while
**forest monitoring** watches large areas for slow growth and sudden loss.

**Precision agriculture** treats a field as spatially variable, not
uniform. NDVI (and its saturation-resistant cousins) maps crop vigour
within the field, revealing zones that need different treatment:

- **Management zones** - cluster the vigour map into a few zones and apply
  variable-rate fertiliser or irrigation per zone rather than a flat rate.
- **In-season monitoring** - a rising then plateauing NDVI curve tracks the
  crop's phenology; an unexpected dip flags stress, pest or water problems
  early.
- **Yield estimation** - integrated growing-season NDVI correlates with
  final yield.

Zonal statistics summarise a raster within each field polygon - the core
operation. With rasterstats over a GeoJSON of field boundaries:

```python
from rasterstats import zonal_stats

zs = zonal_stats("fields.geojson", "ndvi.tif",
                 stats=["mean", "min", "max", "std"])
# zs[0] -> {'mean': 0.71, 'min': 0.32, 'max': 0.88, 'std': 0.09}
# high std within a field => heterogeneous vigour => candidate for zoning
```

**Forest monitoring** works at landscape scale. The same indices, plus
radar, drive two products the world relies on:

- **Change / loss detection** - annual comparison flags deforestation;
  Global Forest Watch and the Hansen dataset map tree-cover loss yearly.
- **Biomass and structure** - **lidar** and, from space, **GEDI** and
  **NISAR** estimate canopy height and above-ground biomass, which optical
  indices alone cannot see because NDVI saturates over dense canopy.

Above-ground biomass is commonly related to canopy height through an
**allometric power law** fitted from field plots:

```text
AGB = a * H^b

AGB = above-ground biomass (Mg per hectare)
H   = canopy height from lidar or GEDI (metres)
a, b = coefficients fitted to field measurements
```

Modern practice adds machine learning: a **CNN or vision transformer**
performs **semantic segmentation** to label every pixel (crop type, forest
versus non-forest), and **geospatial foundation models** pretrained on
Sentinel and Landsat archives are fine-tuned for these tasks with far fewer
labels than training from scratch.

```mermaid
graph TD
    S2["Sentinel-2 time series"] --> IDX["Vegetation indices"]
    IDX --> ZONE["Field zonal statistics"]
    ZONE --> VRA["Variable rate management"]
    IDX --> LOSS["Forest loss detection"]
    LIDAR["Lidar and GEDI"] --> BIO["Canopy height and biomass"]
    LOSS --> ALERT["Deforestation alerts"]
```

Remember: the same vegetation indices serve precision farming (zonal, per
field, in season) and forest monitoring (change and biomass at landscape
scale), with lidar and ML filling in what optical indices cannot.
""",
        ),
        quiz_lesson(
            "Quiz: Precision agriculture and forest monitoring",
            (
                q(
                    "What is the purpose of management zones in precision agriculture?",
                    (
                        opt("To make the field a single uniform block"),
                        opt(
                            "To cluster within-field vigour so inputs like fertiliser and "
                            "irrigation are varied per zone instead of applied flat",
                            correct=True,
                        ),
                        opt("To change the field's CRS"),
                        opt("To remove all vegetation"),
                    ),
                    "Fields are spatially variable; zoning targets variable-rate "
                    "application where it is needed.",
                ),
                q(
                    "Which operation summarises a raster within each field polygon?",
                    (
                        opt("Flow accumulation"),
                        opt("Zonal statistics", correct=True),
                        opt("Hillshading"),
                        opt("Tide harmonic analysis"),
                    ),
                    "Zonal statistics aggregate raster values (mean, std, min, max) "
                    "inside each vector polygon.",
                ),
                q(
                    "Why are lidar or GEDI used for forest biomass rather than NDVI alone?",
                    (
                        opt("They are cheaper"),
                        opt(
                            "NDVI saturates over dense canopy; lidar and GEDI measure "
                            "canopy height and structure that optical indices cannot see",
                            correct=True,
                        ),
                        opt("NDVI cannot be computed over forests"),
                        opt("Lidar measures temperature"),
                    ),
                    "Structure and biomass need a height signal; allometric laws relate "
                    "canopy height to above-ground biomass.",
                ),
            ),
        ),
        # -- 7. Natural hazards and disaster mapping -------------------
        _t(
            "Natural hazards and disaster mapping",
            "11 min",
            """# Natural hazards and disaster mapping

When disaster strikes, geospatial models answer two questions: **before**,
where is the risk? and **after**, what was hit? Two hazards illustrate the
whole workflow: **floods** and **wildfires**.

**Risk** is conventionally decomposed as a product of three factors, and
each is a map layer you can build:

```text
Risk = Hazard x Exposure x Vulnerability

Hazard        - probability and intensity of the event (e.g. flood depth)
Exposure      - people and assets in the hazard footprint
Vulnerability - how badly those assets are harmed at that intensity
```

**Flood mapping** builds on the hydrology lessons. A fast first pass over a
DEM is the **HAND** model - Height Above Nearest Drainage - which gives each
cell its elevation relative to the stream it drains to; cells with low HAND
flood first. During an event, **Sentinel-1 SAR** maps the water extent
through cloud, because calm water is smooth and returns almost no radar
signal - it appears dark:

```python
import numpy as np, rasterio

with rasterio.open("s1_vv_db.tif") as src:      # SAR backscatter in dB
    vv = src.read(1)
# smooth open water backscatters weakly -> low dB -> threshold it out
water = vv < -18.0                               # simple flood-water mask
# compare pre-event and during-event masks to isolate NEW flooding
new_flood = water & ~np.load("baseline_water.npy")
```

**Wildfire mapping** uses the shortwave-infrared bands. **Active fire** is
detected from thermal anomalies (VIIRS and MODIS hotspots, distributed as
NASA FIRMS). **Burn severity** after the fire uses the **Normalized Burn
Ratio (NBR)** before and after:

```text
NBR  = (NIR - SWIR) / (NIR + SWIR)              # Sentinel-2: B8 and B12
dNBR = NBR_prefire - NBR_postfire              # higher dNBR = more severe burn
```

The output of hazard mapping is **actionable geospatial products**: an
inundation extent to prioritise rescue, a burn-severity map to plan
recovery, an exposure count of buildings inside the footprint. These are
served fast to responders through **OGC web services** (WMS for a picture,
WFS for the vectors) and increasingly through cloud-native **COG** tiles
streamed on demand. Machine-learning segmentation now automates the
extraction of flood and burn extents from imagery at scale.

```mermaid
graph TD
    DEM["DEM and hydrology"] --> HAZ["Hazard layer flood or fire"]
    SAR["Sentinel-1 SAR water"] --> HAZ
    HAZ --> RISK["Risk from hazard and exposure"]
    EXP["Exposure people and assets"] --> RISK
    RISK --> PROD["Response products maps and counts"]
    PROD --> OGC["Serve via WMS WFS and COG"]
```

Remember: risk is hazard times exposure times vulnerability; SAR maps flood
water through cloud and dNBR maps burn severity, and the product must reach
responders fast through open web services.
""",
        ),
        quiz_lesson(
            "Quiz: Natural hazards and disaster mapping",
            (
                q(
                    "How is disaster risk conventionally decomposed?",
                    (
                        opt("Risk equals elevation times slope"),
                        opt(
                            "Risk equals hazard times exposure times vulnerability",
                            correct=True,
                        ),
                        opt("Risk equals rainfall minus runoff"),
                        opt("Risk equals NDVI times NBR"),
                    ),
                    "Each factor - hazard, exposure, vulnerability - is a separate map "
                    "layer you combine.",
                ),
                q(
                    "Why does calm flood water appear dark in Sentinel-1 SAR imagery?",
                    (
                        opt("Water absorbs all radar and emits none"),
                        opt(
                            "A smooth water surface reflects radar away from the sensor, "
                            "returning almost no backscatter",
                            correct=True,
                        ),
                        opt("SAR only works at night over land"),
                        opt("Water is warmer than land"),
                    ),
                    "Specular reflection off smooth water gives low backscatter, so it "
                    "thresholds out as dark - useful through cloud.",
                ),
                q(
                    "What does dNBR (differenced Normalized Burn Ratio) map?",
                    (
                        opt("Flood depth"),
                        opt("Burn severity, from pre-fire minus post-fire NBR", correct=True),
                        opt("Canopy height"),
                        opt("Tidal range"),
                    ),
                    "NBR uses NIR and SWIR; the pre/post difference grades how severely "
                    "each pixel burned.",
                ),
            ),
        ),
        # -- 8. Urban analytics and digital twins ----------------------
        _t(
            "Urban analytics and digital twins",
            "11 min",
            """# Urban analytics and digital twins

Cities are where people, infrastructure and environment collide, and the
frontier of environmental geospatial modeling is the **urban digital twin**
- a living 3D replica of a city, fed by data, used to simulate and manage
it. Getting there means moving from 2D maps to 3D and from static files to
streaming.

**Urban analytics** in 2D and 2.5D already answers a lot. A DEM captures
the bare earth; a **DSM (digital surface model)** captures the tops of
buildings and trees. Their difference is object height:

```text
nDSM = DSM - DEM        # normalized height of buildings and vegetation

# a building's height comes straight from the nDSM under its footprint
building_height = zonal_mean(nDSM, footprint_polygon)
```

Vector analysis over a street and parcel network answers accessibility and
equity questions - who lives within a 10-minute walk of a park, how heat or
flooding is distributed across neighbourhoods. **PostGIS** is the standard
engine; spatial SQL does the work:

```sql
-- residential buildings within 300 m of a green space
SELECT b.id, b.height
FROM   buildings b
JOIN   parks p
  ON   ST_DWithin(b.geom, p.geom, 300)   -- geom in a metric CRS, metres
WHERE  b.use = 'residential';
```

The **3D** step needs open standards so the twin is not locked to one
viewer:

- **CityGML / CityJSON** - semantic 3D city models with levels of detail
  (LoD1 boxes up to LoD3 detailed facades).
- **3D Tiles and glTF** - OGC streaming formats that page massive city
  models into a browser (Cesium) at interactive frame rates.

A **digital twin** is more than a 3D model: it is the model **plus live
data plus simulation**. Sensors (IoT, traffic, air-quality, weather) stream
in; simulations run on top - flood inundation, solar potential per rooftop,
urban heat island, pedestrian flow - and results feed back into planning
decisions. This closes the same loop as the rest of the course: observe,
model, decide, act.

```mermaid
graph TD
    DSM["DSM minus DEM gives heights"] --> B3D["3D building models"]
    B3D --> CITY["CityJSON city model"]
    CITY --> TILES["Stream as 3D Tiles and glTF"]
    SENSORS["Live sensor feeds"] --> TWIN["Digital twin"]
    TILES --> TWIN
    TWIN --> SIM["Simulate flood heat and solar"]
    SIM --> PLAN["Planning decisions"]
```

Remember: an urban digital twin is a 3D city model served through open
streaming standards, fused with live data and simulation - the culmination
of terrain, hydrology, climate, remote sensing and hazard modeling applied
to the built environment.
""",
        ),
        quiz_lesson(
            "Quiz: Urban analytics and digital twins",
            (
                q(
                    "How do you get object height such as a building's from elevation data?",
                    (
                        opt("Read it from the DEM directly"),
                        opt(
                            "Subtract the DEM (bare earth) from the DSM (surface with "
                            "objects) to get the normalized height nDSM",
                            correct=True,
                        ),
                        opt("Compute NDVI"),
                        opt("Sum the tide constituents"),
                    ),
                    "nDSM = DSM - DEM isolates building and vegetation height above the ground.",
                ),
                q(
                    "What distinguishes a digital twin from a plain 3D city model?",
                    (
                        opt("Nothing - they are the same"),
                        opt(
                            "A digital twin adds live data feeds and simulation on top of "
                            "the 3D model, closing the observe-model-decide loop",
                            correct=True,
                        ),
                        opt("A twin has no geometry"),
                        opt("A twin is only a paper map"),
                    ),
                    "Model plus live sensors plus simulation is what makes it a twin, not "
                    "just a scene.",
                ),
                q(
                    "Which standards stream massive 3D city models into a browser?",
                    (
                        opt("NetCDF and GRIB"),
                        opt("3D Tiles and glTF", correct=True),
                        opt("Shapefile and CSV"),
                        opt("NDVI and NBR"),
                    ),
                    "OGC 3D Tiles page large models (often authored as CityJSON) into "
                    "viewers like Cesium at interactive rates.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What must be true of the CRS before computing slope from a DEM?",
                    (
                        opt("It must be EPSG:4326 geographic"),
                        opt(
                            "It must be a projected CRS so horizontal and vertical units "
                            "both being metres makes the gradient meaningful",
                            correct=True,
                        ),
                        opt("It must have no datum"),
                        opt("Any CRS works equally"),
                    ),
                    "Slope mixes cell size and height; degrees of longitude are not fixed "
                    "metres, so use a projected CRS.",
                ),
                q(
                    "Put the core hydrology steps in order.",
                    (
                        opt("Accumulate, then fill, then find direction"),
                        opt(
                            "Fill sinks, compute flow direction, compute flow "
                            "accumulation, then threshold to streams and delineate "
                            "watersheds",
                            correct=True,
                        ),
                        opt("Delineate watershed first, then fill sinks"),
                        opt("Threshold streams before any flow direction"),
                    ),
                    "Fill, direction, accumulation, threshold, delineate - the fixed order.",
                ),
                q(
                    "What is ERA5?",
                    (
                        opt("A single cloud-free Sentinel-2 scene"),
                        opt(
                            "A global hourly atmospheric reanalysis that fuses a physics "
                            "model with observations into a gap-free record",
                            correct=True,
                        ),
                        opt("A vector street network"),
                        opt("A tide gauge station"),
                    ),
                    "Reanalysis products like ERA5 assimilate observations into a "
                    "physically consistent gridded cube.",
                ),
                q(
                    "Why must coastal flood mapping fix its vertical datum carefully?",
                    (
                        opt("Datums change the raster resolution"),
                        opt(
                            "Land and tidal datums (geoid, MSL, MLLW, MHHW) differ; mixing "
                            "them shifts the water line and corrupts the flood map",
                            correct=True,
                        ),
                        opt("Datums only affect colours"),
                        opt("There is only one datum worldwide"),
                    ),
                    "Consistent referencing of heights and water levels is essential in "
                    "coastal work.",
                ),
                q(
                    "How is NDVI defined?",
                    (
                        opt("(RED - NIR) / (RED + NIR)"),
                        opt("(NIR - RED) / (NIR + RED)", correct=True),
                        opt("NIR - RED"),
                        opt("(SWIR - NIR) / (SWIR + NIR)"),
                    ),
                    "Near-infrared minus red over their sum; vegetation is bright in NIR "
                    "and dark in red.",
                ),
                q(
                    "What is STAC and what is it for?",
                    (
                        opt("A 3D rendering engine for cities"),
                        opt(
                            "SpatioTemporal Asset Catalog - an open standard for searching "
                            "imagery archives by space and time",
                            correct=True,
                        ),
                        opt("A tide-prediction algorithm"),
                        opt("A NetCDF compression codec"),
                    ),
                    "STAC items are GeoJSON with datetime and asset links, making "
                    "archives searchable.",
                ),
                q(
                    "Which operation summarises a raster inside each vector polygon, used "
                    "for per-field crop vigour?",
                    (
                        opt("Hillshading"),
                        opt("Zonal statistics", correct=True),
                        opt("Flow accumulation"),
                        opt("Harmonic analysis"),
                    ),
                    "Zonal statistics aggregate raster values within polygons - the core "
                    "of field-level analytics.",
                ),
                q(
                    "Why does calm open water read as dark in Sentinel-1 SAR, making it "
                    "useful for flood mapping?",
                    (
                        opt("Water heats up and glows"),
                        opt(
                            "A smooth surface reflects the radar away from the sensor, so "
                            "backscatter is very low",
                            correct=True,
                        ),
                        opt("SAR cannot see water at all"),
                        opt("Water blocks all microwaves"),
                    ),
                    "Specular reflection off smooth water gives low backscatter, and SAR "
                    "sees through cloud day or night.",
                ),
                q(
                    "How is disaster risk conventionally expressed?",
                    (
                        opt("Hazard plus DEM plus slope"),
                        opt(
                            "Hazard times exposure times vulnerability",
                            correct=True,
                        ),
                        opt("Exposure minus vulnerability"),
                        opt("NDVI times NBR"),
                    ),
                    "Three multiplicative factors, each mappable, combine into risk.",
                ),
                q(
                    "What makes an urban digital twin more than a static 3D city model?",
                    (
                        opt("It has more polygons"),
                        opt(
                            "It fuses the 3D model with live sensor data and simulation, "
                            "feeding results back into decisions",
                            correct=True,
                        ),
                        opt("It drops the third dimension"),
                        opt("It is stored as a shapefile"),
                    ),
                    "Model plus live data plus simulation, streamed via 3D Tiles and "
                    "glTF, is what defines a twin.",
                ),
            ),
            duration="12 min",
        ),
    ),
)

ENVIRONMENTAL_GEOSPATIAL_MODELING_COURSES: tuple[SeedCourse, ...] = (
    _ENVIRONMENTAL_GEOSPATIAL_MODELING,
)
