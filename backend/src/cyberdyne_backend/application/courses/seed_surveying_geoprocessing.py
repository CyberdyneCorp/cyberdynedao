"""Academy seed content - Surveying and Geoprocessing.

The measuring-and-modeling foundation for civil projects: how we fix
position on the Earth (coordinate systems, datums, georeferencing), how we
measure distances, angles and heights, how traverses are computed and
error-compensated, how terrain is modeled for earthwork, and how modern
digital surveying works - total stations, GNSS (RTK and PPP), drones and
photogrammetry, and GIS with remote sensing. Every lesson is a direct
explanation with a concrete formula or computation and a mermaid diagram,
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


_SURVEYING_GEOPROCESSING = SeedCourse(
    slug="surveying-geoprocessing",
    title="Surveying & Geoprocessing",
    description=(
        "Measuring and modeling the land - from total-station traverses and "
        "leveling to GNSS, drones, photogrammetry and GIS for civil projects. "
        "Every lesson gives a direct explanation, a worked formula or "
        "computation, and a diagram, grounded in real practice and standards "
        "(NBR 13133, ABNT, IBGE/SIRGAS2000)."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Surveying and Geoprocessing

Every civil work starts by answering one question: **where is it, and
what does the ground look like there?** Surveying is how we measure the
land - positions, distances, angles and heights - and geoprocessing is
how we model and analyze that data on a computer. Together they turn a
piece of terrain into coordinates, contour lines, volumes and maps a
project can be designed on.

The approach here is **small and concrete**: every lesson explains one
idea directly, shows it with a real formula or a short computation, and
draws the idea as a diagram. After each lesson there is a short quiz; at
the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Coordinate systems, datums and georeferencing** - how position is
   defined on the Earth
2. **Distance, angle and leveling measurement** - the raw observations
3. **Traverses and planimetric surveys** - computing position and
   distributing error
4. **Altimetry, contour lines and earthwork volumes** - modeling height
5. **Total stations and electronic data collection** - the modern field
   instrument
6. **GNSS positioning (RTK, PPP)** - satellite positioning
7. **Drones and photogrammetry** - measuring from images
8. **GIS and remote sensing** - analyzing spatial data for engineering

This is the map from a stake in the ground to a georeferenced model.
Keep a calculator handy - the worked examples are the point.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What do surveying and geoprocessing together accomplish?",
                    (
                        opt("They design the structure's foundations"),
                        opt(
                            "They measure the land (positions, distances, angles, "
                            "heights) and model and analyze it on a computer, turning "
                            "terrain into coordinates, contours, volumes and maps",
                            correct=True,
                        ),
                        opt("They only produce legal property documents"),
                        opt("They replace the need for a project design"),
                    ),
                    "Surveying measures the ground; geoprocessing models and analyzes "
                    "that data - the two feed the design.",
                ),
                q(
                    "How is each lesson in this course structured?",
                    (
                        opt("A long theory text with no examples"),
                        opt(
                            "A direct explanation, one concrete formula or computation, "
                            "and a diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("A video with no reading"),
                    ),
                    "Explain, show a worked example, draw it, then check with a quiz.",
                ),
            ),
        ),
        # -- 1. Coordinate systems, datums, georeferencing -------------
        _t(
            "Coordinate systems, datums and georeferencing",
            "10 min",
            """# Coordinate systems, datums and georeferencing

The Earth is not a sphere - it is closer to an **ellipsoid** (flattened
at the poles). To give any point a position we first agree on a
**reference model**:

- **Ellipsoid** - the smooth mathematical surface (e.g. GRS80) that
  approximates the Earth's shape.
- **Datum** - an ellipsoid *plus* its orientation and origin fixed to the
  Earth. In Brazil the official datum is **SIRGAS2000**; older maps used
  SAD69 or Corrego Alegre, so you must know which datum your data uses or
  points shift by tens of metres.
- **Geoid** - the equipotential surface (mean sea level extended under the
  continents). Heights are usually referenced to it, not the ellipsoid.

A position can be given as **geographic coordinates** (latitude,
longitude, and height) or projected onto a flat plane so we can use metres
and simple geometry. The standard projection for surveying is **UTM
(Universal Transverse Mercator)**, which divides the world into 6-degree
zones and gives each point an **Easting (E)** and **Northing (N)** in
metres.

**Georeferencing** means tying a survey, an image or a drawing to a known
coordinate system so it lines up with everything else.

A key height relationship - the ellipsoidal height h from GNSS is not the
orthometric height H the project needs:

```text
h = H + N

where:
  h = ellipsoidal height (measured by GNSS, relative to the ellipsoid)
  H = orthometric height (relative to the geoid / mean sea level)
  N = geoid undulation (from a model such as MAPGEO2015)

Example: GNSS gives h = 812.400 m, model gives N = -6.200 m
  H = h - N = 812.400 - (-6.200) = 818.600 m
```

```mermaid
graph TD
    EARTH["Real Earth surface"] --> ELL["Ellipsoid GRS80"]
    ELL --> DATUM["Datum SIRGAS2000"]
    DATUM --> GEO["Geographic lat lon height"]
    DATUM --> UTM["UTM projection Easting Northing"]
    GEO --> REF["Georeferenced data"]
    UTM --> REF
```

Remember: always know your **datum and projection**. Coordinates without
them are meaningless - and mixing datums is a classic, costly mistake.
""",
        ),
        quiz_lesson(
            "Quiz: Coordinate systems, datums and georeferencing",
            (
                q(
                    "What is a geodetic datum?",
                    (
                        opt("A single point measured in the field"),
                        opt(
                            "A reference ellipsoid plus its orientation and origin fixed "
                            "to the Earth (for example SIRGAS2000 in Brazil)",
                            correct=True,
                        ),
                        opt("The elevation of the sea at one moment"),
                        opt("A brand of survey instrument"),
                    ),
                    "A datum ties a mathematical ellipsoid to the real Earth; different "
                    "datums shift the same point by tens of metres.",
                ),
                q(
                    "GNSS gives an ellipsoidal height h = 700.000 m and the geoid model "
                    "gives N = -5.000 m. What is the orthometric height H?",
                    (
                        opt("695.000 m"),
                        opt("705.000 m", correct=True),
                        opt("700.000 m"),
                        opt("-5.000 m"),
                    ),
                    "H = h - N = 700.000 - (-5.000) = 705.000 m.",
                ),
                q(
                    "What does the UTM projection provide?",
                    (
                        opt("Latitude and longitude in degrees only"),
                        opt(
                            "A flat plane with Easting and Northing in metres, in "
                            "6-degree zones, so simple planar geometry can be used",
                            correct=True,
                        ),
                        opt("The exact shape of the geoid"),
                        opt("A 3D model of the building"),
                    ),
                    "UTM projects the curved Earth onto zones so distances and areas "
                    "can be computed in metres.",
                ),
            ),
        ),
        # -- 2. Distance, angle, leveling measurement ------------------
        _t(
            "Distance, angle and leveling measurement",
            "10 min",
            """# Distance, angle and leveling measurement

Every survey is built from three basic observations: **distances**,
**angles**, and **height differences**.

**Distances.** Modern instruments measure distance electronically (EDM -
electronic distance measurement) by timing an infrared or laser signal to
a prism or surface. A distance measured along the slope must be reduced to
the **horizontal distance** used on plans:

```text
Horizontal distance from slope distance and zenith angle:
  DH = DI * sin(Z)

  DI = slope (inclined) distance
  Z  = zenith angle (measured from vertical)

Example: DI = 152.480 m, Z = 87 deg 30'
  sin(87.5 deg) = 0.99905
  DH = 152.480 * 0.99905 = 152.335 m
```

**Angles.** Two kinds matter. A **horizontal angle** is the angle between
two directions measured in the horizontal plane; a **vertical (zenith)
angle** is measured from the vertical. Directions are given as a
**bearing** or **azimuth** (azimuth = angle clockwise from North, 0 to
360 degrees).

**Leveling.** A height difference between two points is found by reading a
graduated staff through a level. The **backsight (BS)** is the reading on
the known point; the **foresight (FS)** is on the new point:

```text
Height difference and new elevation:
  dH = BS - FS
  H_new = H_known + (BS - FS)

Example: H_known = 100.000 m, BS = 1.235 m, FS = 1.867 m
  dH = 1.235 - 1.867 = -0.632 m
  H_new = 100.000 - 0.632 = 99.368 m
```

```mermaid
graph LR
    INS["Field observation"] --> D["Distance by EDM"]
    INS --> A["Angle horizontal and zenith"]
    INS --> L["Level reading staff"]
    D --> DH["Horizontal distance"]
    A --> AZ["Azimuth or bearing"]
    L --> HD["Height difference"]
    DH --> POS["Point position"]
    AZ --> POS
    HD --> POS
```

Remember: raw field readings are along the slope and relative to the
instrument - you always **reduce** them (to horizontal, to azimuth, to a
datum) before they become coordinates.
""",
        ),
        quiz_lesson(
            "Quiz: Distance, angle and leveling measurement",
            (
                q(
                    "A slope distance DI = 100.000 m is measured with a zenith angle "
                    "Z = 90 deg. What is the horizontal distance DH = DI * sin(Z)?",
                    (
                        opt("0.000 m"),
                        opt("100.000 m", correct=True),
                        opt("50.000 m"),
                        opt("90.000 m"),
                    ),
                    "At Z = 90 deg the line of sight is horizontal, sin(90) = 1, so "
                    "DH = DI = 100.000 m.",
                ),
                q(
                    "In differential leveling, how is the elevation of a new point found?",
                    (
                        opt("H_new = backsight only"),
                        opt(
                            "H_new = H_known + (backsight - foresight)",
                            correct=True,
                        ),
                        opt("H_new = foresight - backsight"),
                        opt("H_new = the average of the two staff readings"),
                    ),
                    "Add the backsight on the known point and subtract the foresight on "
                    "the new point: H_new = H_known + BS - FS.",
                ),
                q(
                    "What is an azimuth?",
                    (
                        opt("The vertical angle from the horizon"),
                        opt(
                            "A direction measured clockwise from North, from 0 to 360 degrees",
                            correct=True,
                        ),
                        opt("The slope distance between two points"),
                        opt("The height of the instrument above the ground"),
                    ),
                    "Azimuth is the clockwise angle from North; it orients each line of "
                    "the survey.",
                ),
            ),
        ),
        # -- 3. Traverses and planimetric surveys ----------------------
        _t(
            "Traverses and planimetric surveys (error compensation)",
            "11 min",
            """# Traverses and planimetric surveys (error compensation)

A **traverse** (poligonal) is a connected series of survey lines whose
lengths and directions are measured, walking from a known point around
the property or corridor and (ideally) back to a known point. It is the
backbone of a **planimetric survey** - the 2D map of horizontal position.

For each line you convert distance and azimuth into coordinate
increments:

```text
Departure (East) and Latitude (North) of a line:
  dE = D * sin(Az)
  dN = D * cos(Az)

  D  = horizontal distance,  Az = azimuth of the line

Then walk the coordinates around:
  E_next = E_prev + dE
  N_next = N_prev + dN
```

Because every measurement has small errors, a **closed traverse** never
closes perfectly - when you sum all increments back to the start there is
a **misclosure**:

```text
Closure error and relative precision:
  eE = sum(dE),   eN = sum(dN)          (should be 0 for a closed loop)
  linear closure  e  = sqrt(eE^2 + eN^2)
  relative precision = e / perimeter  ->  express as 1 : (perimeter / e)

Example: eE = +0.030 m, eN = -0.040 m, perimeter = 1000 m
  e = sqrt(0.030^2 + 0.040^2) = 0.050 m
  relative precision = 0.050 / 1000 = 1 : 20000
```

NBR 13133 sets minimum precisions (for example 1:20000 for many surveys);
if you meet it, you **compensate** (adjust) the error back into the
coordinates. The simple, common method is the **Compass (Bowditch)
rule**, which distributes the misclosure to each line **in proportion to
its length**:

```text
Correction to a line of length D_i:
  correction_E,i = -eE * (D_i / perimeter)
  correction_N,i = -eN * (D_i / perimeter)
```

```mermaid
graph TD
    FIELD["Measure distances and azimuths"] --> INC["Compute dE and dN per line"]
    INC --> SUM["Sum increments around loop"]
    SUM --> ERR["Misclosure eE and eN"]
    ERR --> PREC["Relative precision check NBR 13133"]
    PREC --> ADJ["Compensate by Compass rule"]
    ADJ --> COORD["Adjusted coordinates"]
```

Remember: a good traverse is not one with **zero** error - it is one whose
error is **small enough** to meet spec and is then distributed fairly
across the lines.
""",
        ),
        quiz_lesson(
            "Quiz: Traverses and planimetric surveys (error compensation)",
            (
                q(
                    "For a traverse line, how are the coordinate increments computed "
                    "from distance D and azimuth Az?",
                    (
                        opt("dE = D * cos(Az), dN = D * sin(Az)"),
                        opt(
                            "dE = D * sin(Az), dN = D * cos(Az)",
                            correct=True,
                        ),
                        opt("dE = D + Az, dN = D - Az"),
                        opt("dE = D / Az, dN = D * Az"),
                    ),
                    "East uses the sine of the azimuth, North uses the cosine, since "
                    "azimuth is measured from North.",
                ),
                q(
                    "A closed loop has eE = +0.030 m and eN = +0.040 m. What is the "
                    "linear closure error e = sqrt(eE^2 + eN^2)?",
                    (
                        opt("0.070 m"),
                        opt("0.050 m", correct=True),
                        opt("0.010 m"),
                        opt("0.025 m"),
                    ),
                    "sqrt(0.030^2 + 0.040^2) = sqrt(0.0025) = 0.050 m (a 3-4-5 triangle).",
                ),
                q(
                    "What does the Compass (Bowditch) rule do?",
                    (
                        opt("Removes the need to measure azimuths"),
                        opt(
                            "Distributes the misclosure to each line in proportion to "
                            "its length to adjust the coordinates",
                            correct=True,
                        ),
                        opt("Deletes the line with the largest error"),
                        opt("Doubles every measured distance"),
                    ),
                    "Bowditch spreads the closure error across lines proportionally to "
                    "length - longer lines get a larger correction.",
                ),
            ),
        ),
        # -- 4. Altimetry, contours, earthwork -------------------------
        _t(
            "Altimetry, contour lines and earthwork volumes",
            "11 min",
            """# Altimetry, contour lines and earthwork volumes

Planimetry gives horizontal position; **altimetry** gives **height**.
Modeled together they describe the terrain surface, usually as a **DTM
(Digital Terrain Model)** built from a cloud of surveyed points.

**Contour lines (curvas de nivel)** connect points of equal elevation.
The vertical spacing between them is the **contour interval**; closely
spaced contours mean steep ground, widely spaced means flat. They let you
read slope and shape straight off a plan.

Civil earthwork asks: how much soil to **cut** or **fill** to reach the
design grade? Two classic volume methods:

**1. Average end area** - between two cross-sections a distance L apart:

```text
V = (A1 + A2) / 2 * L

Example: A1 = 12.0 m2, A2 = 18.0 m2, L = 20.0 m
  V = (12.0 + 18.0) / 2 * 20.0 = 15.0 * 20.0 = 300.0 m3
```

**2. Grid (borrow-pit) method** - overlay a grid on the site, take the
cut/fill height at each grid corner, and weight each height by how many
cells share it:

```text
V = (A_cell / 4) * ( sum(h1) + 2*sum(h2) + 3*sum(h3) + 4*sum(h4) )

  h1 = corner shared by 1 cell, h2 by 2 cells, etc.
  A_cell = area of one grid square
```

Cut and fill are often summarized in a **mass-haul** view to balance
earth movement and minimize hauling.

```mermaid
graph TD
    PTS["Surveyed height points"] --> DTM["Digital terrain model"]
    DTM --> CONT["Contour lines"]
    DTM --> XS["Cross sections"]
    XS --> AEA["Average end area volume"]
    DTM --> GRID["Grid method volume"]
    AEA --> CF["Cut and fill balance"]
    GRID --> CF
```

Remember: heights become a **surface**, the surface becomes **contours and
sections**, and sections become **volumes** - the numbers that drive
earthmoving cost.
""",
        ),
        quiz_lesson(
            "Quiz: Altimetry, contour lines and earthwork volumes",
            (
                q(
                    "What do contour lines represent?",
                    (
                        opt("Lines of equal slope"),
                        opt("Property boundaries"),
                        opt("Lines connecting points of equal elevation", correct=True),
                        opt("The path of surface water only"),
                    ),
                    "Each contour joins points at the same height; their spacing shows "
                    "how steep the ground is.",
                ),
                q(
                    "Two cross-sections A1 = 20 m2 and A2 = 40 m2 are L = 10 m apart. "
                    "By average end area, V = (A1 + A2)/2 * L equals?",
                    (
                        opt("300 m3", correct=True),
                        opt("600 m3"),
                        opt("60 m3"),
                        opt("150 m3"),
                    ),
                    "V = (20 + 40)/2 * 10 = 30 * 10 = 300 m3.",
                ),
                q(
                    "Where contour lines are drawn very close together, the ground is…",
                    (
                        opt("flat"),
                        opt("steep", correct=True),
                        opt("underwater"),
                        opt("perfectly level"),
                    ),
                    "Close spacing means a large height change over a short horizontal "
                    "distance - a steep slope.",
                ),
            ),
        ),
        # -- 5. Total stations -----------------------------------------
        _t(
            "Total stations and electronic data collection",
            "10 min",
            """# Total stations and electronic data collection

A **total station** combines three instruments in one: an **EDM** for
distance, an **electronic theodolite** for horizontal and vertical
angles, and an on-board **computer** that records and processes readings.
Aim at a **prism** (reflector) on a pole, press measure, and it captures
slope distance, horizontal angle and zenith angle at once - then computes
the point's coordinates on the spot.

The core computation the instrument does for every shot, given the
occupied station coordinates and the reduced observations:

```text
For a sighted point, from station (E0, N0, H0):
  DH = DI * sin(Z)                 horizontal distance
  dE = DH * sin(Az)                easting increment
  dN = DH * cos(Az)                northing increment
  dH = DI * cos(Z) + hi - ht       height increment

  E = E0 + dE
  N = N0 + dN
  H = H0 + dH

  hi = instrument height, ht = target (prism) height
```

Field data is stored in a **collector** and exported (commonly as a
**CSV** of Point, E, N, H, code) into CAD or GIS - no more transcribing
notebooks by hand, which removes a whole class of errors.

A typical exported record:

```text
PT,      E,          N,           H,       CODE
101, 742310.482, 7195402.115, 812.640,  TREE
102, 742318.905, 7195397.220, 812.180,  CURB
103, 742325.117, 7195390.640, 811.905,  CURB
```

**Reflectorless** total stations can measure to a surface without a prism
(useful for facades or hazardous points), and **robotic** ones track the
prism so one person can run the survey alone.

```mermaid
graph TD
    TS["Total station"] --> EDM["EDM distance"]
    TS --> THEO["Electronic theodolite angles"]
    TS --> CPU["Onboard computer"]
    EDM --> COMP["Compute E N H per point"]
    THEO --> COMP
    CPU --> COMP
    COMP --> COLL["Data collector"]
    COLL --> EXP["Export CSV to CAD and GIS"]
```

Remember: the total station turns each aim-and-measure into finished
**coordinates and a code**, recorded digitally - the field-to-office
workflow with the least manual error.
""",
        ),
        quiz_lesson(
            "Quiz: Total stations and electronic data collection",
            (
                q(
                    "What three functions does a total station combine?",
                    (
                        opt("GPS receiver, camera and radio"),
                        opt(
                            "Electronic distance measurement, an electronic theodolite "
                            "for angles, and an onboard computer to record and compute",
                            correct=True,
                        ),
                        opt("Level, plumb bob and measuring tape"),
                        opt("Drone, prism and staff"),
                    ),
                    "EDM (distance) + theodolite (angles) + computer (record and "
                    "process) in a single instrument.",
                ),
                q(
                    "Why is exporting field data as a coordinate file (for example CSV) "
                    "an improvement over hand-written notebooks?",
                    (
                        opt("It makes the instrument cheaper"),
                        opt(
                            "It removes manual transcription, eliminating a whole class "
                            "of copying errors and feeding CAD and GIS directly",
                            correct=True,
                        ),
                        opt("It increases the measurement range"),
                        opt("It removes the need to know the datum"),
                    ),
                    "Digital capture and export cuts out re-typing readings, a common "
                    "source of blunders.",
                ),
                q(
                    "What can a robotic total station do that a conventional one cannot?",
                    (
                        opt("Measure without any target at all times"),
                        opt(
                            "Track the prism automatically so a single person can run the survey",
                            correct=True,
                        ),
                        opt("Position points using satellites only"),
                        opt("Fly over the site"),
                    ),
                    "Robotic instruments lock onto and follow the prism, enabling "
                    "one-person operation.",
                ),
            ),
        ),
        # -- 6. GNSS ---------------------------------------------------
        _t(
            "GNSS positioning (RTK, PPP)",
            "11 min",
            """# GNSS positioning (RTK, PPP)

**GNSS (Global Navigation Satellite System)** is the family of satellite
constellations - **GPS** (USA), **GLONASS**, **Galileo**, **BeiDou** -
that a receiver uses to fix its position. The receiver measures the
distance to several satellites and **trilaterates** its location; you need
at least **four** satellites to solve for the three coordinates plus the
receiver clock error.

A phone's GNSS is accurate to a few metres - fine for navigation, useless
for surveying. Survey accuracy comes from **differential** techniques that
cancel the shared errors (atmosphere, orbits) between receivers:

- **RTK (Real-Time Kinematic)** - a **base** receiver on a known point
  streams corrections (by radio or internet/NTRIP) to a moving **rover**,
  which computes **centimetre**-level positions **in real time**. Ideal
  for staking out and detailed survey. Range is limited by the baseline to
  the base (or you use a network of reference stations, like the Brazilian
  **RBMC**).
- **PPP (Precise Point Positioning)** - a **single** receiver logs data
  and uses precise satellite orbit and clock products (from IGS/IBGE) to
  reach centimetre-to-decimetre accuracy **without a local base**. It
  needs a longer occupation to converge but works anywhere.

Remember the height caveat from lesson 1 - GNSS gives ellipsoidal height,
so apply the geoid model:

```text
Positioning mode vs typical accuracy:
  Standalone (single receiver, code):   ~2 to 5 m
  RTK (base + rover, real time):        ~1 to 3 cm  (horizontal)
  PPP (single receiver, post-process):  ~a few cm to dm

Orthometric height still needs the geoid model:
  H = h - N     (e.g. MAPGEO2015 in Brazil)
```

```mermaid
graph TD
    SATS["GNSS satellites four or more"] --> ROVER["Rover receiver"]
    BASE["Base on known point"] --> CORR["Corrections by radio or NTRIP"]
    CORR --> ROVER
    ROVER --> RTK["RTK centimetre in real time"]
    SATS --> PPP["Single receiver logs data"]
    PPP --> PROD["Precise orbit and clock products"]
    PROD --> POST["PPP centimetre post processed"]
```

Remember: **RTK** buys you real-time centimetres with a base and radio
link; **PPP** buys you centimetres from one receiver but needs
post-processing and time to converge. Both beat a standalone fix by orders
of magnitude.
""",
        ),
        quiz_lesson(
            "Quiz: GNSS positioning (RTK, PPP)",
            (
                q(
                    "What is the key idea of RTK positioning?",
                    (
                        opt("A single receiver working alone in real time"),
                        opt(
                            "A base on a known point streams corrections to a moving "
                            "rover, giving centimetre positions in real time",
                            correct=True,
                        ),
                        opt("Averaging a phone GPS for an hour"),
                        opt("Using only one satellite"),
                    ),
                    "RTK = base + rover + real-time corrections -> centimetre accuracy "
                    "as you move.",
                ),
                q(
                    "How does PPP differ from RTK?",
                    (
                        opt("PPP needs two receivers and a radio link"),
                        opt(
                            "PPP uses a single receiver with precise orbit and clock "
                            "products and no local base, but needs longer to converge",
                            correct=True,
                        ),
                        opt("PPP is only accurate to several metres"),
                        opt("PPP works without any satellites"),
                    ),
                    "PPP reaches high accuracy from one receiver using precise products, "
                    "trading real-time speed for convergence time.",
                ),
                q(
                    "At minimum, how many satellites does a receiver need to fix its 3D position?",
                    (
                        opt("One"),
                        opt("Two"),
                        opt("Four - three coordinates plus the receiver clock error", correct=True),
                        opt("Ten"),
                    ),
                    "Four unknowns (X, Y, Z and clock bias) require at least four "
                    "satellite ranges.",
                ),
            ),
        ),
        # -- 7. Drones & photogrammetry --------------------------------
        _t(
            "Drones and photogrammetry",
            "11 min",
            """# Drones and photogrammetry

**Photogrammetry** extracts 3D measurements from **2D photographs**. Take
many overlapping photos of a scene from different positions, and software
can reconstruct the geometry - the same way two eyes give depth. Fly a
**drone (UAV)** on an automated grid over a site and you capture hundreds
of overlapping images in minutes, then process them into survey products.

The modern pipeline is **Structure from Motion (SfM)**: match features
across photos, solve for every camera position and a dense **3D point
cloud**, then build products:

- **Orthomosaic** - a single, geometrically corrected aerial image where
  every pixel is at true map scale (you can measure distances on it).
- **DSM / DTM** - a digital surface/terrain model of heights.
- **3D mesh and contours** - for volumes, cross-sections and inspection.

Two things control accuracy: **overlap** and **ground control**. Photos
must overlap heavily so features appear in many images, and **GCPs
(Ground Control Points)** - targets surveyed with GNSS/RTK - georeference
and scale the model.

**GSD (Ground Sampling Distance)** is the size of one image pixel on the
ground - the resolution that drives detail and accuracy:

```text
GSD = (sensor_pixel_size * flight_height) / focal_length

Example:
  sensor_pixel_size = 0.0024 mm (2.4 micron)
  focal_length      = 8.8 mm
  flight_height     = 100 m = 100000 mm
  GSD = (0.0024 * 100000) / 8.8 = 240 / 8.8 = 27.3 mm/pixel  (~2.7 cm)
```

Lower flight height -> smaller GSD -> more detail, but more photos and
flight time.

```mermaid
graph TD
    FLIGHT["Drone flight overlapping photos"] --> SFM["Structure from motion"]
    GCP["Ground control points RTK"] --> SFM
    SFM --> CLOUD["Dense 3D point cloud"]
    CLOUD --> ORTHO["Orthomosaic"]
    CLOUD --> DSM["Surface and terrain model"]
    DSM --> VOL["Volumes and contours"]
    ORTHO --> MAP["Georeferenced map"]
```

Remember: overlapping photos plus surveyed control points become a
georeferenced 3D model - a fast way to survey large or unsafe sites, with
accuracy set by **GSD** and **ground control**.
""",
        ),
        quiz_lesson(
            "Quiz: Drones and photogrammetry",
            (
                q(
                    "What is an orthomosaic?",
                    (
                        opt("A single raw drone photo"),
                        opt(
                            "A geometrically corrected aerial image at true map scale, "
                            "on which distances can be measured",
                            correct=True,
                        ),
                        opt("A list of GNSS coordinates"),
                        opt("A contour map with no image"),
                    ),
                    "An orthomosaic removes perspective and relief distortion so every "
                    "pixel sits at its true map position.",
                ),
                q(
                    "Why are Ground Control Points (GCPs) used in drone mapping?",
                    (
                        opt("To make the drone fly faster"),
                        opt(
                            "They are targets surveyed with GNSS/RTK that georeference "
                            "and scale the photogrammetric model accurately",
                            correct=True,
                        ),
                        opt("To increase battery life"),
                        opt("To replace the camera"),
                    ),
                    "GCPs tie the image-based model to real coordinates, controlling "
                    "position and scale.",
                ),
                q(
                    "If you halve the flight height (all else equal), the Ground "
                    "Sampling Distance (GSD) will…",
                    (
                        opt("double, giving coarser pixels"),
                        opt("halve, giving finer detail", correct=True),
                        opt("stay the same"),
                        opt("become zero"),
                    ),
                    "GSD is proportional to flight height, so flying lower halves the "
                    "GSD and increases detail (at the cost of more photos).",
                ),
            ),
        ),
        # -- 8. GIS & remote sensing -----------------------------------
        _t(
            "GIS and remote sensing for civil engineering",
            "11 min",
            """# GIS and remote sensing for civil engineering

A **GIS (Geographic Information System)** stores, analyzes and displays
data that has a **location**. Every feature carries geometry *and*
attributes, organized in **layers** you overlay and query. Two data
models:

- **Vector** - points, lines and polygons (a manhole, a road centerline,
  a lot boundary), each with an attribute table.
- **Raster** - a grid of cells, each holding a value (elevation in a DTM,
  reflectance in a satellite image, land-use class).

**Remote sensing** feeds the GIS: measuring the surface from a distance
with satellites or aircraft. Sensors record energy in several **spectral
bands**, and combining bands reveals things the eye cannot - vegetation
health, water, bare soil, urban surfaces. A classic index is the **NDVI**:

```text
NDVI = (NIR - RED) / (NIR + RED)

  NIR = near-infrared reflectance, RED = red reflectance
  Range: -1 to +1;  high (~0.6-0.9) = healthy vegetation,
  near 0 = bare soil/rock, negative = water

Example: NIR = 0.50, RED = 0.10
  NDVI = (0.50 - 0.10) / (0.50 + 0.10) = 0.40 / 0.60 = 0.67  (vegetated)
```

For civil engineering, GIS is where surveying pays off: **route selection**
for roads and pipelines, **flood and drainage** analysis on a DTM,
**site suitability** by overlaying slope, soil, zoning and access, and
**asset management** of a utility network. Analysis often stacks layers -
a **suitability overlay** scores each cell from several criteria - and
increasingly links to **BIM** and **digital twins** so the design and the
real terrain share one coordinated model.

```mermaid
graph TD
    RS["Remote sensing imagery"] --> RAST["Raster layers"]
    SURVEY["Survey and GNSS data"] --> VECT["Vector layers"]
    RAST --> GIS["GIS database"]
    VECT --> GIS
    GIS --> OVER["Overlay and suitability analysis"]
    OVER --> ROUTE["Route selection"]
    OVER --> FLOOD["Flood and drainage"]
    OVER --> BIM["Link to BIM and digital twin"]
```

Remember: GIS turns located data into **decisions** - overlay the layers,
run the analysis, and the survey becomes route choices, flood maps and a
managed asset base. It is the destination of the whole surveying pipeline.
""",
        ),
        quiz_lesson(
            "Quiz: GIS and remote sensing for civil engineering",
            (
                q(
                    "What is the difference between vector and raster data in a GIS?",
                    (
                        opt("Vector is 3D, raster is 2D"),
                        opt(
                            "Vector stores points, lines and polygons with attributes; "
                            "raster stores a grid of cells each holding a value",
                            correct=True,
                        ),
                        opt("They are the same thing"),
                        opt("Vector is only for satellite images"),
                    ),
                    "Vector = discrete features with attribute tables; raster = a value "
                    "grid (e.g. a DTM or an image).",
                ),
                q(
                    "For a pixel with NIR = 0.60 and RED = 0.20, NDVI = (NIR - RED) / "
                    "(NIR + RED) equals?",
                    (
                        opt("0.50", correct=True),
                        opt("0.80"),
                        opt("0.40"),
                        opt("1.00"),
                    ),
                    "(0.60 - 0.20) / (0.60 + 0.20) = 0.40 / 0.80 = 0.50 - a vegetated pixel.",
                ),
                q(
                    "How does GIS support a civil project like a new road?",
                    (
                        opt("It pours the concrete"),
                        opt(
                            "By overlaying layers (slope, soil, zoning, flood) to "
                            "analyze route selection and site suitability",
                            correct=True,
                        ),
                        opt("It replaces the structural design"),
                        opt("It measures angles in the field"),
                    ),
                    "GIS overlays and analyzes located data to inform routing, drainage "
                    "and suitability decisions.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Why must every coordinate be accompanied by its datum and projection?",
                    (
                        opt("It is a legal formality with no practical effect"),
                        opt(
                            "Different datums shift the same point by tens of metres and "
                            "the projection defines how curved Earth maps to the plane - "
                            "without them a coordinate is ambiguous",
                            correct=True,
                        ),
                        opt("Because instruments require it to power on"),
                        opt("Only for coordinates measured by drone"),
                    ),
                    "Mixing datums (e.g. SAD69 vs SIRGAS2000) or ignoring the projection "
                    "is a classic, costly mistake.",
                ),
                q(
                    "GNSS gives h = 850.000 m and the geoid model gives N = -8.000 m. "
                    "The orthometric height H = h - N is…",
                    (
                        opt("842.000 m"),
                        opt("858.000 m", correct=True),
                        opt("850.000 m"),
                        opt("8.000 m"),
                    ),
                    "H = 850.000 - (-8.000) = 858.000 m.",
                ),
                q(
                    "A slope distance of 200.000 m is measured with a zenith angle of "
                    "90 deg. The horizontal distance DH = DI * sin(Z) is…",
                    (
                        opt("0.000 m"),
                        opt("100.000 m"),
                        opt("200.000 m", correct=True),
                        opt("141.400 m"),
                    ),
                    "sin(90 deg) = 1, so DH = DI = 200.000 m (the line of sight is horizontal).",
                ),
                q(
                    "A closed traverse has misclosure eE = 0.060 m, eN = 0.080 m over a "
                    "2000 m perimeter. The linear closure e = sqrt(eE^2 + eN^2) is…",
                    (
                        opt("0.100 m", correct=True),
                        opt("0.140 m"),
                        opt("0.020 m"),
                        opt("0.050 m"),
                    ),
                    "sqrt(0.060^2 + 0.080^2) = sqrt(0.010) = 0.100 m; relative precision "
                    "0.100/2000 = 1:20000.",
                ),
                q(
                    "What does the Compass (Bowditch) rule do to a traverse?",
                    (
                        opt("Eliminates the need to measure the last line"),
                        opt(
                            "Distributes the closure error across the lines in "
                            "proportion to their length to adjust the coordinates",
                            correct=True,
                        ),
                        opt("Converts azimuths to bearings"),
                        opt("Sets the contour interval"),
                    ),
                    "Bowditch spreads misclosure proportionally to line length - the "
                    "standard planimetric adjustment.",
                ),
                q(
                    "Two cross-sections A1 = 30 m2 and A2 = 50 m2 lie L = 25 m apart. "
                    "The average-end-area volume V = (A1 + A2)/2 * L is…",
                    (
                        opt("1000 m3", correct=True),
                        opt("2000 m3"),
                        opt("500 m3"),
                        opt("80 m3"),
                    ),
                    "V = (30 + 50)/2 * 25 = 40 * 25 = 1000 m3.",
                ),
                q(
                    "What three instruments does a total station integrate?",
                    (
                        opt("GNSS receiver, camera and drone"),
                        opt(
                            "EDM for distance, an electronic theodolite for angles, and "
                            "an onboard computer to record and compute coordinates",
                            correct=True,
                        ),
                        opt("Level, tape and plumb bob"),
                        opt("Prism, staff and tripod"),
                    ),
                    "Distance + angles + computing in one instrument, exporting "
                    "coordinates digitally.",
                ),
                q(
                    "Which statement about RTK versus PPP is correct?",
                    (
                        opt("Both need two receivers and a radio link"),
                        opt(
                            "RTK uses a base and rover for real-time centimetres; PPP "
                            "uses a single receiver with precise products and needs "
                            "convergence time",
                            correct=True,
                        ),
                        opt("PPP is real-time, RTK is post-processed only"),
                        opt("Neither can reach centimetre accuracy"),
                    ),
                    "RTK trades a base station for instant centimetres; PPP trades a "
                    "base for convergence time from one receiver.",
                ),
                q(
                    "In drone photogrammetry, what most directly sets the resolution and "
                    "accuracy of the products?",
                    (
                        opt("The colour of the drone"),
                        opt(
                            "The Ground Sampling Distance (driven by flight height and "
                            "sensor) together with ground control points",
                            correct=True,
                        ),
                        opt("The number of propellers"),
                        opt("The time of day only"),
                    ),
                    "Smaller GSD (lower flight) plus surveyed GCPs give a sharper, "
                    "well-georeferenced model.",
                ),
                q(
                    "For a pixel with NIR = 0.40 and RED = 0.40, the NDVI = "
                    "(NIR - RED)/(NIR + RED) is…",
                    (
                        opt("1.00"),
                        opt("0.00", correct=True),
                        opt("-1.00"),
                        opt("0.50"),
                    ),
                    "(0.40 - 0.40)/(0.40 + 0.40) = 0/0.80 = 0.00 - near-zero NDVI "
                    "indicates bare soil or non-vegetated surface.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SURVEYING_GEOPROCESSING_COURSES: tuple[SeedCourse, ...] = (_SURVEYING_GEOPROCESSING,)
