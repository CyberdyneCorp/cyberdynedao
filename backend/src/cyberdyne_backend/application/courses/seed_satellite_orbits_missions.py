"""Academy seed content - Satellite Orbits & Missions.

The space segment of geospatial engineering: the orbital mechanics that
govern where a satellite is, the specific orbits Earth-observation
missions use (LEO, sun-synchronous, GEO), how constellations combine to
cover the planet, and the ground segment that commands the spacecraft and
turns raw downlinks into calibrated, usable data products. Every lesson is
a direct explanation with a real formula or computation and a mermaid
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


_SATELLITE_ORBITS_MISSIONS = SeedCourse(
    slug="satellite-orbits-missions",
    title="Satellite Orbits & Missions",
    description=(
        "The space segment of geospatial engineering: orbital mechanics and "
        "Kepler's laws, the orbits observation satellites use (LEO, "
        "sun-synchronous, GEO), constellations and coverage, and the ground "
        "segment that commands the spacecraft and turns downlinks into "
        "calibrated data products - with real formulas, orbital-element "
        "computations, and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Satellite Orbits & Missions

Every pixel in a satellite image starts as a spacecraft in a very
specific orbit, imaging a very specific patch of ground, at a very
specific time. Understanding **where** the satellite is and **why** it is
there is the foundation of the whole space segment of geospatial
engineering. This course connects orbital mechanics to the observation
missions that depend on it, and follows the data all the way down to a
finished product.

The approach is **concrete**: every lesson explains one idea directly,
grounds it in a real formula or computation (an orbital-period equation, a
ground-track shift, a sun-synchronous inclination), and draws the idea as
a diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **Orbital mechanics** - Kepler's laws and the two-body problem
2. **Orbital elements and ground tracks** - describing and projecting an orbit
3. **Orbit types for Earth observation** - LEO, SSO, and GEO trade-offs
4. **Sun-synchronous and repeat-cycle orbits** - the workhorse EO orbits
5. **Constellations and coverage** - many satellites, global revisit
6. **The ground segment and mission operations** - commanding the spacecraft
7. **Sensor calibration and validation** - trusting the numbers
8. **From downlink to product** - ground processing levels L0 to L2

This is the space half of the geospatial pipeline. The remote-sensing and
GIS courses in this track pick up where the ground segment hands off a
calibrated product; knowing how that product was produced makes every
later analysis more trustworthy.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "Why does the space segment matter for geospatial analysis?",
                    (
                        opt("It does not - imagery is imagery"),
                        opt(
                            "The orbit, viewing geometry and acquisition time of a "
                            "spacecraft determine what every pixel actually measures and "
                            "when",
                            correct=True,
                        ),
                        opt("Only the ground software affects data quality"),
                        opt("Satellites are chosen at random"),
                    ),
                    "Where and when a satellite images the Earth is set by its orbit; "
                    "that shapes the resulting data product.",
                ),
                q(
                    "How does this course relate to the remote-sensing and GIS courses "
                    "in the track?",
                    (
                        opt("It replaces them"),
                        opt(
                            "It covers the space segment that produces the calibrated "
                            "product those courses then analyze",
                            correct=True,
                        ),
                        opt("It only covers rocket launches"),
                        opt("It is unrelated to geospatial work"),
                    ),
                    "Learn how the product is made (this course), then analyze it (the "
                    "remote-sensing and GIS courses).",
                ),
            ),
        ),
        # -- 1. Orbital mechanics --------------------------------------
        _t(
            "Orbital mechanics and Kepler's laws",
            "11 min",
            """# Orbital mechanics and Kepler's laws

A satellite in orbit is in continuous **free fall**: gravity pulls it
toward Earth while its forward velocity carries it past, so it keeps
falling around the planet instead of into it. To first order this is the
**two-body problem** - one small satellite orbiting a much larger Earth -
and its solution is described by **Kepler's three laws**.

- **First law** - the orbit is an **ellipse** with Earth at one focus. The
  closest point is **perigee**, the farthest is **apogee**.
- **Second law** - a line from Earth to the satellite sweeps **equal areas
  in equal times**, so the satellite moves fastest at perigee and slowest
  at apogee.
- **Third law** - the orbital period squared is proportional to the
  semi-major axis cubed. This is the equation you use constantly.

For a circular orbit at altitude **h** above an Earth of radius
**R = 6378 km**, the orbital radius is **a = R + h**, and the period is:

```text
T = 2 * pi * sqrt( a^3 / mu )

  mu (Earth GM) = 398600 km^3 / s^2
  R (equatorial radius) = 6378 km

Example: h = 700 km (a typical LEO EO altitude)
  a = 6378 + 700 = 7078 km
  T = 2 * pi * sqrt(7078^3 / 398600)
  T = 5926 s  ~ 98.8 minutes per revolution
  revolutions per day = 86400 / 5926 ~ 14.6
```

That ~99 minute period and ~14-15 revolutions per day is why low-orbit
observation satellites circle the Earth many times daily, each pass
shifted west as the planet rotates beneath them (the next lesson).

Orbital **velocity** for a circular orbit is `v = sqrt(mu / a)`, about
7.5 km/s at 700 km. Higher orbits are slower and have longer periods -
the trade at the heart of choosing an orbit.

```mermaid
graph LR
    GRAV["Gravity pulls inward"] --> FALL["Continuous free fall"]
    VEL["Forward velocity"] --> FALL
    FALL --> ELL["Elliptical orbit"]
    ELL --> PER["Perigee is fastest"]
    ELL --> APO["Apogee is slowest"]
    ELL --> T3["Period from semi major axis"]
```

Remember: an orbit is falling that keeps missing the ground, and Kepler's
third law ties altitude directly to period - bigger orbit, longer trip.
""",
        ),
        quiz_lesson(
            "Quiz: Orbital mechanics and Kepler's laws",
            (
                q(
                    "Why does a satellite stay in orbit rather than fall to Earth?",
                    (
                        opt("There is no gravity in space"),
                        opt(
                            "It is in continuous free fall - gravity pulls it in while "
                            "its forward velocity carries it past, so it keeps missing "
                            "the Earth",
                            correct=True,
                        ),
                        opt("Its engines fire constantly to hold it up"),
                        opt("The atmosphere pushes it up"),
                    ),
                    "Orbit is free fall with enough sideways speed to keep missing the ground.",
                ),
                q(
                    "What does Kepler's third law relate?",
                    (
                        opt("Colour and temperature"),
                        opt("Mass and velocity only"),
                        opt(
                            "Orbital period squared to semi-major axis cubed - bigger "
                            "orbits have longer periods",
                            correct=True,
                        ),
                        opt("Inclination and longitude"),
                    ),
                    "T^2 is proportional to a^3, so altitude sets the period.",
                ),
                q(
                    "A circular orbit at 700 km altitude has a period near what value?",
                    (
                        opt("About 24 hours"),
                        opt("About 99 minutes, roughly 14-15 revolutions per day", correct=True),
                        opt("About 10 minutes"),
                        opt("Exactly 12 hours"),
                    ),
                    "With a = 7078 km, T = 2*pi*sqrt(a^3/mu) is about 99 minutes.",
                ),
            ),
        ),
        # -- 2. Orbital elements and ground tracks ---------------------
        _t(
            "Orbital elements and ground tracks",
            "11 min",
            """# Orbital elements and ground tracks

To pin down exactly where a satellite is, you need six numbers - the
**classical (Keplerian) orbital elements**. Together they define the size
and shape of the orbit, how it is tilted in space, and where the
satellite sits along it:

- **Semi-major axis (a)** - the size of the orbit (sets the period).
- **Eccentricity (e)** - the shape, from circular (e = 0) to elongated.
- **Inclination (i)** - the tilt of the orbital plane relative to the
  equator. 0 deg is equatorial, 90 deg is polar, above 90 deg is retrograde.
- **Right ascension of the ascending node (RAAN, capital-omega)** - where
  the orbit crosses the equator going north, measured in inertial space.
- **Argument of perigee (small-omega)** - orientation of the ellipse
  within its plane.
- **True anomaly (nu)** - the satellite's position along the orbit right now.

In practice, operators distribute these as a **Two-Line Element set
(TLE)** that propagators (SGP4) turn into position and velocity:

```text
ISS (ZARYA)
1 25544U 98067A   24005.50000000  .00016000  00000-0  29000-3 0  9992
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.49180000 12345

  line 2 fields:  inclination = 51.6416 deg
                  RAAN        = 247.4627 deg
                  eccentricity= 0.0006703  (decimal point implied)
                  mean motion = 15.4918 revs / day
```

The **ground track** is the path of the point directly beneath the
satellite (its **nadir**) traced on the Earth's surface. Because the
planet rotates eastward while the satellite orbits, each successive pass
shifts **westward**. The shift per orbit is:

```text
delta_lon = 360 deg * (T_orbit / T_earth_rotation)

  T_orbit = 98.8 min, T_earth = 1436 min (sidereal day)
  delta_lon = 360 * (98.8 / 1436) ~ 24.8 deg west per revolution
```

The maximum latitude a ground track reaches equals the orbit's
**inclination**, which is why polar-imaging missions need an inclination
near 90 degrees.

```mermaid
graph TD
    SIX["Six orbital elements"] --> A["Size a and shape e"]
    SIX --> ORI["Tilt i and node RAAN"]
    SIX --> POS["Position nu now"]
    A --> TLE["Encoded in a TLE"]
    ORI --> TLE
    POS --> TLE
    TLE --> GT["Propagate to ground track"]
    GT --> SHIFT["Each pass shifts westward"]
```

Remember: six elements fix an orbit in space, and projecting the nadir
point down gives the ground track - which marches west as Earth turns.
""",
        ),
        quiz_lesson(
            "Quiz: Orbital elements and ground tracks",
            (
                q(
                    "What does the inclination element describe?",
                    (
                        opt("The size of the orbit"),
                        opt(
                            "The tilt of the orbital plane relative to the equator - and "
                            "the maximum latitude the ground track reaches",
                            correct=True,
                        ),
                        opt("The satellite's current position"),
                        opt("The shape of the ellipse"),
                    ),
                    "Inclination sets the plane's tilt; a 90 deg orbit is polar and "
                    "reaches the poles.",
                ),
                q(
                    "Why does a satellite's ground track shift westward each orbit?",
                    (
                        opt("The satellite fires thrusters westward"),
                        opt(
                            "The Earth rotates eastward beneath the orbit, so the nadir "
                            "point of the next pass falls farther west",
                            correct=True,
                        ),
                        opt("Because of magnetic fields"),
                        opt("The orbit itself moves west"),
                    ),
                    "delta_lon = 360 * (T_orbit / T_earth); about 25 deg west per rev for a LEO.",
                ),
                q(
                    "What is a TLE used for?",
                    (
                        opt("Storing pixel values"),
                        opt(
                            "Encoding orbital elements so a propagator (SGP4) can compute "
                            "the satellite's position and velocity over time",
                            correct=True,
                        ),
                        opt("Calibrating the camera"),
                        opt("Naming the ground stations"),
                    ),
                    "A Two-Line Element set packs the elements for propagation.",
                ),
            ),
        ),
        # -- 3. Orbit types for EO -------------------------------------
        _t(
            "Orbit types for Earth observation (LEO, SSO, GEO)",
            "11 min",
            """# Orbit types for Earth observation (LEO, SSO, GEO)

Different missions need different orbits, and the choice is a trade
between **resolution**, **coverage**, and **revisit time**. Three regimes
dominate Earth observation.

- **Low Earth Orbit (LEO)** - roughly 500 to 900 km. Close to the ground,
  so high spatial resolution, but a narrow instantaneous footprint and a
  fast-moving nadir. A single satellite sees any given place only every
  few days. Most imaging missions (Landsat, Sentinel-2) live here.
- **Sun-synchronous Orbit (SSO)** - a special near-polar LEO (covered in
  the next lesson) that crosses each latitude at the **same local solar
  time**, giving consistent illumination for comparing images over time.
- **Geostationary Orbit (GEO)** - a circular equatorial orbit at
  **35786 km** with a period of exactly one sidereal day, so the satellite
  appears **fixed** over one spot on the equator. It sees a whole
  hemisphere continuously - ideal for weather (GOES, Meteosat) - but at
  coarse resolution because it is so far away.

The GEO altitude comes straight from Kepler's third law - solve for the
radius whose period equals one sidereal day:

```text
Solve T = 2*pi*sqrt(a^3 / mu) = 86164 s (one sidereal day)

  a^3 = mu * (T / (2*pi))^2
  a   = (398600 * (86164 / 6.2832)^2) ^ (1/3)
  a   ~ 42164 km  (from Earth's centre)
  altitude = 42164 - 6378 ~ 35786 km
```

The core trade-off: get **closer** for resolution (LEO) and you sacrifice
continuous, wide coverage; go **far** for a hemispheric, always-on view
(GEO) and you sacrifice resolution.

```mermaid
graph TD
    NEED["Mission need"] --> Q1{"Resolution or continuous view"}
    Q1 -->|"high resolution"| LEO["LEO 500 to 900 km"]
    Q1 -->|"always on hemisphere"| GEO["GEO 35786 km"]
    LEO --> SSO["Sun synchronous variant"]
    LEO --> REV["Revisit every few days"]
    GEO --> WX["Weather and full disc"]
```

Remember: LEO trades coverage for resolution, GEO trades resolution for a
continuous hemispheric view, and SSO is the LEO variant that fixes the
lighting.
""",
        ),
        quiz_lesson(
            "Quiz: Orbit types for Earth observation (LEO, SSO, GEO)",
            (
                q(
                    "Why do most high-resolution imaging missions use Low Earth Orbit?",
                    (
                        opt("It is cheaper to reach than any other orbit"),
                        opt(
                            "Being close to the surface gives high spatial resolution, "
                            "accepting a narrow footprint and multi-day revisit",
                            correct=True,
                        ),
                        opt("LEO satellites never need station keeping"),
                        opt("It provides a continuous hemispheric view"),
                    ),
                    "Closer means sharper; the cost is limited instantaneous coverage.",
                ),
                q(
                    "What makes a geostationary satellite appear fixed over one spot?",
                    (
                        opt("It stops moving entirely"),
                        opt(
                            "Its circular equatorial orbit at 35786 km has a period of one "
                            "sidereal day, matching Earth's rotation",
                            correct=True,
                        ),
                        opt("It is towed by a cable"),
                        opt("It orbits over the poles"),
                    ),
                    "Period equals one sidereal day over the equator, so it hovers "
                    "relative to the ground.",
                ),
                q(
                    "What is the main trade-off of a GEO weather satellite?",
                    (
                        opt("It has too much resolution to be useful"),
                        opt(
                            "Its great distance gives a continuous hemispheric view but "
                            "coarse spatial resolution",
                            correct=True,
                        ),
                        opt("It can only see the poles"),
                        opt("It revisits only once per year"),
                    ),
                    "GEO buys always-on wide coverage at the price of resolution.",
                ),
            ),
        ),
        # -- 4. Sun-synchronous and repeat-cycle -----------------------
        _t(
            "Sun-synchronous and repeat-cycle orbits",
            "11 min",
            """# Sun-synchronous and repeat-cycle orbits

Most operational imaging satellites fly a **sun-synchronous orbit (SSO)** -
a near-polar LEO engineered so the orbital plane rotates in step with the
Earth's motion around the Sun. The payoff: the satellite crosses every
latitude at the **same local solar time** on every pass, so illumination
and shadow geometry stay consistent, which is exactly what you need to
compare images across days, seasons, and years.

The trick uses a perturbation, not a fuel-hungry maneuver. The Earth's
equatorial bulge (the **J2** term) drags the orbital plane's RAAN around
over time. Choose the altitude and inclination so that this **nodal
precession** equals one full turn per year (about **0.9856 deg/day**), and
the plane always keeps the same angle to the Sun.

Because that precession rate depends on both altitude and inclination, a
sun-synchronous orbit is **slightly retrograde** - its inclination is a bit
above 90 degrees:

```text
Required precession: d(RAAN)/dt = +0.9856 deg / day  (one turn per year)

  For a ~700 km circular orbit, the J2 relation gives:
    inclination i ~ 98.2 deg   (retrograde, above 90 deg)

  Local solar crossing time is fixed by the orbit's node,
  e.g. a "10:30 descending node" means the satellite crosses
  the equator southbound at 10:30 local mean solar time.
```

Layered on top is the **repeat cycle**: after a whole number of orbits and
days, the ground track exactly retraces itself, so the satellite re-images
the same swaths on a fixed calendar. Sentinel-2 repeats every **10 days**
per satellite (5 days with two satellites); Landsat repeats every **16
days**. Between repeats, adjacent tracks tile the globe.

```mermaid
graph TD
    J2["Earth equatorial bulge J2"] --> PREC["Nodal precession of RAAN"]
    PREC --> TUNE["Tune altitude and inclination"]
    TUNE --> SSO["Sun synchronous i near 98 deg"]
    SSO --> LST["Same local solar time each pass"]
    LST --> COMP["Consistent illumination over time"]
    SSO --> REP["Repeat cycle re images same swaths"]
```

Remember: J2 precession tuned to one turn per year gives a fixed
crossing time (consistent lighting), and the repeat cycle guarantees the
same ground gets re-imaged on a predictable schedule.
""",
        ),
        quiz_lesson(
            "Quiz: Sun-synchronous and repeat-cycle orbits",
            (
                q(
                    "What is the defining property of a sun-synchronous orbit?",
                    (
                        opt("It never enters the Earth's shadow"),
                        opt(
                            "It crosses each latitude at the same local solar time on "
                            "every pass, giving consistent illumination",
                            correct=True,
                        ),
                        opt("It stays fixed over one spot like GEO"),
                        opt("It has zero inclination"),
                    ),
                    "Same local solar crossing time means comparable lighting across "
                    "dates - ideal for change detection.",
                ),
                q(
                    "How is sun-synchronicity achieved?",
                    (
                        opt("Continuous thruster firing to rotate the plane"),
                        opt(
                            "By tuning altitude and inclination so the J2 nodal "
                            "precession equals one full turn per year",
                            correct=True,
                        ),
                        opt("By flying at exactly the equator"),
                        opt("By using a very eccentric orbit"),
                    ),
                    "The equatorial bulge (J2) precesses the plane; tune it to about "
                    "0.9856 deg/day.",
                ),
                q(
                    "Why is a sun-synchronous orbit slightly retrograde (i just above 90 deg)?",
                    (
                        opt("To save fuel on launch"),
                        opt(
                            "The required precession rate is only met at an inclination a "
                            "bit above 90 degrees for typical LEO altitudes",
                            correct=True,
                        ),
                        opt("To avoid other satellites"),
                        opt("Retrograde orbits are always cheaper"),
                    ),
                    "For ~700 km the J2 relation gives about 98.2 deg - just past polar.",
                ),
            ),
        ),
        # -- 5. Constellations and coverage ----------------------------
        _t(
            "Satellite constellations and coverage",
            "10 min",
            """# Satellite constellations and coverage

A single LEO satellite revisits a given place only every few days. When a
mission needs **frequent global coverage**, the answer is a
**constellation** - multiple satellites sharing the workload, arranged so
their ground tracks interleave and their revisit time drops.

Key ideas:

- **Swath width** - the strip of ground an instrument images on each pass.
  Wider swaths tile the globe with fewer orbits, at the cost of resolution.
- **Revisit time** - how often any point is re-imaged. Adding satellites
  in the same orbit plane, or phasing them across several planes, cuts
  revisit roughly in proportion to the number of satellites.
- **Phasing** - spacing satellites evenly (in mean anomaly within a plane,
  and in RAAN across planes) so coverage gaps are filled rather than
  duplicated. A **Walker constellation** parameterizes this as
  total/planes/phasing.

The revisit improvement is close to linear in satellite count:

```text
revisit_constellation ~ revisit_single / N   (for N well-phased satellites)

  Sentinel-2 single satellite repeat = 10 days
  Two satellites (2A + 2B), phased 180 deg apart in the same plane:
    effective revisit at the equator = 10 / 2 = 5 days
    (better at higher latitudes, where tracks overlap)

  Large commercial constellations (100+ small satellites) push
  revisit to daily or even sub-daily.
```

Constellations changed the economics of EO: instead of one large, costly
satellite, many small ones give **temporal density** - the ability to see
change as it happens, which is what most modern monitoring (agriculture,
disasters, security) actually needs.

```mermaid
graph LR
    ONE["Single satellite"] --> SLOW["Revisit every few days"]
    SLOW --> ADD["Add satellites and planes"]
    ADD --> PHASE["Phase them evenly Walker"]
    PHASE --> INTER["Ground tracks interleave"]
    INTER --> FAST["Daily or sub daily revisit"]
    FAST --> TEMPORAL["High temporal density"]
```

Remember: one satellite gives resolution; a well-phased constellation
gives revisit - and modern monitoring is mostly about revisit.
""",
        ),
        quiz_lesson(
            "Quiz: Satellite constellations and coverage",
            (
                q(
                    "What is the main benefit of a satellite constellation?",
                    (
                        opt("Higher spatial resolution per satellite"),
                        opt(
                            "Shorter revisit time - any point is re-imaged far more "
                            "often when satellites are well phased",
                            correct=True,
                        ),
                        opt("It removes the need for an orbit"),
                        opt("It eliminates cloud cover"),
                    ),
                    "More phased satellites means more frequent revisit - temporal density.",
                ),
                q(
                    "Why does phasing matter in a constellation?",
                    (
                        opt("It makes the satellites lighter"),
                        opt(
                            "Even spacing across planes and within planes fills coverage "
                            "gaps instead of duplicating the same tracks",
                            correct=True,
                        ),
                        opt("It is only about aesthetics"),
                        opt("It lets satellites share one battery"),
                    ),
                    "Walker phasing spreads satellites so ground tracks interleave.",
                ),
                q(
                    "Sentinel-2 has a 10-day repeat per satellite. With two phased "
                    "satellites, the effective equatorial revisit is about…",
                    (
                        opt("20 days"),
                        opt("10 days"),
                        opt("5 days", correct=True),
                        opt("1 hour"),
                    ),
                    "Revisit scales roughly as single/N; two satellites give about 5 days.",
                ),
            ),
        ),
        # -- 6. Ground segment -----------------------------------------
        _t(
            "The ground segment and mission operations",
            "11 min",
            """# The ground segment and mission operations

A mission is not just the spacecraft. The **space segment** (the
satellite) is paired with a **ground segment** - the antennas, control
centres, and software on Earth that command the spacecraft and receive its
data. Operations split into two distinct streams.

- **Telemetry, Tracking and Command (TT&C)** - the housekeeping link.
  Downlink **telemetry** reports the satellite's health (battery, temper-
  ature, attitude, position); uplink **commands** tell it what to do (slew,
  image, adjust orbit). This runs over a low-rate, highly reliable link.
- **Payload data downlink** - the science stream: the actual imagery, sent
  at high data rate to ground stations during the few minutes the
  satellite is in view.

Because a LEO satellite passes over any one ground station only briefly,
operators use a **network of stations** (or relay satellites) and plan
**contact windows** - the intervals a station can see the spacecraft above
its horizon. A pass is short:

```text
Contact window (rough): a 700 km satellite is above ~10 deg elevation
for only about 8 to 12 minutes per overpass.

Data budget check - can one pass empty the recorder?
  onboard data collected per orbit = 500 Gbit
  downlink rate                    = 1.2 Gbit / s (X-band)
  contact time available           = 9 min = 540 s
  data downlinked per pass = 1.2 * 540 = 648 Gbit  > 500 Gbit  OK
```

The **flight dynamics** team maintains the orbit: over time atmospheric
drag lowers a LEO satellite, so periodic **station-keeping** burns raise
it back and keep the repeat cycle on schedule. The **mission planning**
system turns user requests into a conflict-free timeline of imaging,
downlink, and maneuver commands, respecting power, thermal, and memory
limits.

```mermaid
graph TD
    SAT["Spacecraft"] --> TTC["TTC health and commands"]
    SAT --> PAY["Payload data downlink"]
    TTC --> CTRL["Control centre"]
    PAY --> STN["Ground station network"]
    CTRL --> FD["Flight dynamics station keeping"]
    CTRL --> PLAN["Mission planning timeline"]
    STN --> ARCH["Data archive"]
```

Remember: the ground segment keeps the satellite healthy and on-orbit
(TT&C and flight dynamics) and captures its data during short contact
windows (payload downlink) - both are needed for a mission to work.
""",
        ),
        quiz_lesson(
            "Quiz: The ground segment and mission operations",
            (
                q(
                    "What is the difference between the TT&C link and the payload downlink?",
                    (
                        opt("They are the same link"),
                        opt(
                            "TT&C is the low-rate, reliable housekeeping link for health "
                            "and commands; payload downlink is the high-rate science "
                            "data stream",
                            correct=True,
                        ),
                        opt("TT&C carries the imagery, payload carries commands"),
                        opt("Payload downlink is only used on the ground"),
                    ),
                    "TT&C = command and telemetry; payload downlink = the actual "
                    "imagery at high rate.",
                ),
                q(
                    "Why must operators plan contact windows carefully?",
                    (
                        opt("Ground stations are only on at night"),
                        opt(
                            "A LEO satellite is visible to any one station for only a few "
                            "minutes per pass, so downlink time is scarce",
                            correct=True,
                        ),
                        opt("The satellite chooses when to talk"),
                        opt("There is unlimited contact time"),
                    ),
                    "A pass above ~10 deg lasts only about 8-12 minutes; that limits how "
                    "much data can come down.",
                ),
                q(
                    "Why does a LEO satellite need periodic station-keeping burns?",
                    (
                        opt("To change its colour"),
                        opt(
                            "Atmospheric drag slowly lowers the orbit, so burns raise it "
                            "back and keep the repeat cycle on schedule",
                            correct=True,
                        ),
                        opt("To spin faster"),
                        opt("Station-keeping is never needed in LEO"),
                    ),
                    "Drag decays the orbit; flight dynamics maintains altitude and the "
                    "repeat ground track.",
                ),
            ),
        ),
        # -- 7. Calibration and validation -----------------------------
        _t(
            "Sensor calibration and validation",
            "11 min",
            """# Sensor calibration and validation

Raw sensor counts are just numbers until you know what they mean. Turning
detector output into a trustworthy physical measurement is the job of
**calibration**; confirming it against independent truth is
**validation** (together, **cal/val**).

- **Radiometric calibration** - converts raw **digital numbers (DN)** into
  physical **radiance**, then often into **reflectance**. It corrects for
  each detector's gain and offset, and tracks how the sensor **degrades**
  over its lifetime. On-board references (solar diffusers, calibration
  lamps, deep-space views) provide known signals to check against.
- **Geometric calibration** - ensures every pixel is placed at the right
  location: correcting for the sensor's internal geometry, the pointing,
  and terrain, so the image **georeferences** correctly. Ground control
  points and a terrain model refine this.
- **Spectral calibration** - confirms each band actually measures the
  wavelength range it claims.

The basic radiometric conversion applies a per-band gain and offset:

```python
# DN -> at-sensor spectral radiance, then top-of-atmosphere reflectance
import numpy as np

def dn_to_radiance(dn, gain, offset):
    # gain and offset from the sensor's calibration file
    return gain * dn + offset

def radiance_to_toa_reflectance(radiance, esun, sun_elev_deg, earth_sun_au):
    theta_z = np.radians(90.0 - sun_elev_deg)      # solar zenith angle
    d = earth_sun_au                                # Earth-Sun distance (AU)
    return (np.pi * radiance * d**2) / (esun * np.cos(theta_z))

# Example: one band
rad = dn_to_radiance(dn=1820, gain=0.0135, offset=-0.21)   # W/m2/sr/um
ref = radiance_to_toa_reflectance(rad, esun=1560.0,
                                  sun_elev_deg=52.0, earth_sun_au=1.004)
```

**Validation** closes the loop: compare the calibrated product against
**in-situ** measurements - field spectrometers, buoys, reference targets
(deserts, dry lakebeds), or another well-characterized sensor
(cross-calibration). Cal/val is continuous over a mission's life, because
detectors drift; without it, a "reflectance" value cannot be compared
across sensors or over time.

```mermaid
graph TD
    DN["Raw digital numbers"] --> RAD["Radiometric to radiance"]
    RAD --> REF["To reflectance"]
    DN --> GEO["Geometric to correct location"]
    REF --> PROD["Calibrated product"]
    GEO --> PROD
    PROD --> VAL["Validate against in situ truth"]
    VAL --> DRIFT["Track detector drift over time"]
    DRIFT --> RAD
```

Remember: calibration turns counts into physical, comparable numbers and
places each pixel correctly; validation proves those numbers against
independent truth - and both must run for the life of the mission.
""",
        ),
        quiz_lesson(
            "Quiz: Sensor calibration and validation",
            (
                q(
                    "What does radiometric calibration do?",
                    (
                        opt("Places pixels at the right map location"),
                        opt(
                            "Converts raw digital numbers into physical radiance or "
                            "reflectance, correcting detector gain, offset and drift",
                            correct=True,
                        ),
                        opt("Renames the spectral bands"),
                        opt("Compresses the downlink"),
                    ),
                    "Radiometric cal = DN to physical units; geometric cal handles location.",
                ),
                q(
                    "What is the role of validation in cal/val?",
                    (
                        opt("It replaces calibration entirely"),
                        opt(
                            "It confirms the calibrated product against independent "
                            "in-situ or reference measurements",
                            correct=True,
                        ),
                        opt("It only checks file formats"),
                        opt("It deletes bad pixels at random"),
                    ),
                    "Validation compares against ground truth or another sensor to "
                    "prove the numbers.",
                ),
                q(
                    "Why must cal/val continue over a mission's whole life?",
                    (
                        opt("The orbit changes the wavelengths"),
                        opt(
                            "Detectors drift and degrade over time, so calibration must "
                            "be tracked continuously to keep measurements comparable",
                            correct=True,
                        ),
                        opt("Ground stations move"),
                        opt("It is only needed once at launch"),
                    ),
                    "Sensor degradation means a single launch calibration would go stale.",
                ),
            ),
        ),
        # -- 8. Downlink to product ------------------------------------
        _t(
            "From downlink to product (ground processing)",
            "11 min",
            """# From downlink to product (ground processing)

The raw bits that reach a ground station are a long way from an image you
can analyze. **Ground processing** transforms them through a standard
ladder of **processing levels**, each adding correction and meaning. The
level naming (Level 0 through Level 4) is broadly shared across agencies.

- **Level 0 (L0)** - raw instrument data, reconstructed from the downlink:
  frames reassembled in time order, transmission artifacts removed, but no
  radiometric or geometric correction. Essentially the sensor's counts.
- **Level 1 (L1)** - calibrated and georeferenced. L1 applies the
  radiometric calibration (to radiance or top-of-atmosphere reflectance)
  and the geometric model. Sub-levels are common: **L1B** radiometrically
  calibrated, **L1C** map-projected and orthorectified (Sentinel-2 L1C is
  ortho TOA reflectance in UTM tiles).
- **Level 2 (L2)** - geophysical product. L2 removes atmospheric effects
  to give **surface** reflectance (**L2A** for Sentinel-2), or derives a
  variable like surface temperature, chlorophyll, or soil moisture. This
  is what most analysts actually use.
- **Level 3 (L3)** - resampled onto a uniform space-time grid, often
  gap-filled or composited (for example a cloud-free monthly mosaic).
- **Level 4 (L4)** - model output derived from lower levels (for example a
  net primary productivity estimate).

Modern products are catalogued with **STAC (SpatioTemporal Asset
Catalog)** so they are discoverable and cloud-friendly:

```json
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "S2B_MSIL2A_20240115_T31UDQ",
  "properties": {
    "datetime": "2024-01-15T10:36:19Z",
    "processing:level": "L2A",
    "proj:epsg": 32631,
    "eo:cloud_cover": 4.2
  },
  "assets": {
    "B04_red":  {"href": "s3://.../B04.tif", "type": "image/tiff"},
    "B08_nir":  {"href": "s3://.../B08.tif", "type": "image/tiff"}
  }
}
```

The pixels themselves are usually stored as **Cloud-Optimized GeoTIFF
(COG)**, so tools can read just the tiles they need over HTTP without
downloading the whole scene. From here the remote-sensing and GIS courses
take over: an L2A surface-reflectance product in a STAC catalog is exactly
what an NDVI or land-cover workflow consumes.

```mermaid
graph LR
    DL["Downlinked raw bits"] --> L0["L0 reconstructed counts"]
    L0 --> L1["L1 calibrated and georeferenced"]
    L1 --> L2["L2 surface or geophysical"]
    L2 --> L3["L3 gridded composite"]
    L3 --> L4["L4 model output"]
    L2 --> CAT["Catalogued in STAC as COG"]
```

Remember: processing climbs L0 raw counts to L1 calibrated to L2 surface
product, then catalogues it (STAC and COG) so downstream analysis can find
and open exactly the pixels it needs.
""",
        ),
        quiz_lesson(
            "Quiz: From downlink to product (ground processing)",
            (
                q(
                    "What distinguishes a Level 0 product from a Level 1 product?",
                    (
                        opt("L0 is already surface reflectance"),
                        opt(
                            "L0 is raw reconstructed instrument counts; L1 adds "
                            "radiometric calibration and georeferencing",
                            correct=True,
                        ),
                        opt("L1 has no calibration at all"),
                        opt("They are identical"),
                    ),
                    "L0 = raw counts reassembled; L1 = calibrated and georeferenced.",
                ),
                q(
                    "What does Level 2 processing add that Level 1 lacks?",
                    (
                        opt("It removes the georeferencing"),
                        opt(
                            "Atmospheric correction to surface reflectance, or a derived "
                            "geophysical variable - the product most analysts use",
                            correct=True,
                        ),
                        opt("It converts back to raw counts"),
                        opt("Nothing - L2 equals L1"),
                    ),
                    "L2 gives surface reflectance (e.g. Sentinel-2 L2A) or a geophysical quantity.",
                ),
                q(
                    "Why are products catalogued with STAC and stored as Cloud-Optimized GeoTIFF?",
                    (
                        opt("To make files larger"),
                        opt(
                            "So products are discoverable and tools can read just the "
                            "needed tiles over HTTP without downloading whole scenes",
                            correct=True,
                        ),
                        opt("Because raw downlink cannot be stored otherwise"),
                        opt("To hide the metadata"),
                    ),
                    "STAC makes assets discoverable; COG enables partial, cloud-native reads.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Why does a satellite stay in orbit?",
                    (
                        opt("Space has no gravity"),
                        opt(
                            "It is in continuous free fall with enough forward velocity "
                            "to keep missing the Earth",
                            correct=True,
                        ),
                        opt("Its engines fire nonstop"),
                        opt("It is held by a tether"),
                    ),
                    "Orbit is falling sideways fast enough to keep missing the ground.",
                ),
                q(
                    "Kepler's third law lets you compute what from an orbit's altitude?",
                    (
                        opt("Its colour"),
                        opt(
                            "Its period - period squared is proportional to semi-major axis cubed",
                            correct=True,
                        ),
                        opt("Its cloud cover"),
                        opt("Its data rate"),
                    ),
                    "T^2 proportional to a^3; altitude sets the period.",
                ),
                q(
                    "The maximum latitude a ground track reaches equals which orbital element?",
                    (
                        opt("Eccentricity"),
                        opt("Semi-major axis"),
                        opt("Inclination", correct=True),
                        opt("True anomaly"),
                    ),
                    "A polar (90 deg) orbit reaches the poles; inclination caps the "
                    "track latitude.",
                ),
                q(
                    "Which orbit appears fixed over one point on the equator?",
                    (
                        opt("Low Earth orbit"),
                        opt("Sun-synchronous orbit"),
                        opt(
                            "Geostationary orbit at 35786 km, period one sidereal day",
                            correct=True,
                        ),
                        opt("Polar orbit"),
                    ),
                    "GEO matches Earth's rotation over the equator, so it hovers.",
                ),
                q(
                    "What makes a sun-synchronous orbit valuable for change detection?",
                    (
                        opt("It never sees clouds"),
                        opt(
                            "It crosses each latitude at the same local solar time, "
                            "giving consistent illumination across dates",
                            correct=True,
                        ),
                        opt("It has the highest resolution possible"),
                        opt("It stays fixed over one spot"),
                    ),
                    "Fixed local crossing time means comparable lighting over time.",
                ),
                q(
                    "How does a constellation improve on a single satellite?",
                    (
                        opt("It increases the resolution of each pixel"),
                        opt(
                            "Multiple well-phased satellites shorten revisit time, "
                            "roughly in proportion to their number",
                            correct=True,
                        ),
                        opt("It eliminates the need for calibration"),
                        opt("It removes atmospheric effects"),
                    ),
                    "Revisit scales about as single/N; constellations buy temporal density.",
                ),
                q(
                    "What is the difference between the TT&C link and the payload downlink?",
                    (
                        opt("They are the same link"),
                        opt(
                            "TT&C is the reliable low-rate housekeeping and command link; "
                            "payload downlink carries the high-rate imagery",
                            correct=True,
                        ),
                        opt("TT&C carries the images"),
                        opt("Payload downlink sends commands to the satellite"),
                    ),
                    "TT&C = health and commands; payload downlink = the science data.",
                ),
                q(
                    "What does radiometric calibration produce from raw digital numbers?",
                    (
                        opt("A map projection"),
                        opt(
                            "Physical radiance or reflectance, correcting detector gain, "
                            "offset and drift",
                            correct=True,
                        ),
                        opt("A new orbit"),
                        opt("A STAC catalog"),
                    ),
                    "DN times gain plus offset yields radiance, then reflectance.",
                ),
                q(
                    "Which processing level gives atmospherically corrected surface reflectance?",
                    (
                        opt("Level 0"),
                        opt("Level 1"),
                        opt("Level 2 (for example Sentinel-2 L2A)", correct=True),
                        opt("Raw downlink"),
                    ),
                    "L0 raw counts, L1 calibrated and georeferenced, L2 surface product.",
                ),
                q(
                    "Why are satellite products catalogued with STAC and stored as COG?",
                    (
                        opt("To make them impossible to search"),
                        opt(
                            "To make them discoverable and allow tools to read only the "
                            "needed tiles over HTTP, cloud-natively",
                            correct=True,
                        ),
                        opt("Because raw bits cannot be archived"),
                        opt("To increase file size on purpose"),
                    ),
                    "STAC = discovery, COG = partial cloud-native reads - the handoff to "
                    "downstream analysis.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SATELLITE_ORBITS_MISSIONS_COURSES: tuple[SeedCourse, ...] = (_SATELLITE_ORBITS_MISSIONS,)
