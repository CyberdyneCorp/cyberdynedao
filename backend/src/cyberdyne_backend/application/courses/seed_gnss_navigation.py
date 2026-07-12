"""Academy seed content - GNSS and Navigation.

How you can know where you are anywhere on Earth: the Global Navigation
Satellite Systems (GPS, Galileo, GLONASS, BeiDou), how ranging and
trilateration turn signal travel time into a position, where the errors
come from (ionosphere, troposphere, multipath, geometry), and the precise
techniques that push accuracy from metres to centimetres (differential
GNSS, RTK, PPP). It closes with inertial navigation and GNSS/INS sensor
fusion via the Kalman filter. Every lesson is a direct explanation with a
concrete formula or computation and a mermaid diagram, followed by a
checkpoint quiz; the course ends with a comprehensive final quiz.
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


_GNSS_NAVIGATION = SeedCourse(
    slug="gnss-navigation",
    title="GNSS & Navigation",
    description=(
        "Positioning anywhere on Earth: how GNSS (GPS, Galileo, GLONASS, "
        "BeiDou) works, how pseudoranges and trilateration produce a fix, "
        "where the errors come from and how geometry (DOP) shapes accuracy, "
        "the precise techniques (differential GNSS, RTK, PPP), and how GNSS "
        "is fused with inertial navigation (INS) through a Kalman filter - "
        "with real formulas, coordinates and Python snippets and a diagram "
        "in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# GNSS and Navigation

A **GNSS** receiver in your phone, drone or survey rover can tell you
where it is anywhere on the planet, to within a few metres - and with the
right techniques, to within a few centimetres. It does this with nothing
but faint radio signals from satellites 20000 km overhead and some careful
arithmetic. This course explains, step by step, how that works and how
engineers make it precise.

The approach is **concrete**: every lesson explains one idea directly,
shows it with a real formula, coordinate example or short Python snippet,
and draws the idea as a diagram. After each lesson there is a short quiz;
at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **GNSS constellations and signals** - GPS, Galileo, GLONASS, BeiDou
2. **Trilateration and pseudoranges** - turning travel time into distance
3. **Position solution and DOP** - solving for position and why geometry matters
4. **Error sources** - ionosphere, troposphere, multipath and more
5. **Differential GNSS and RTK** - reference stations and carrier phase
6. **Precise Point Positioning (PPP)** - global centimetre accuracy without a base
7. **Inertial navigation (INS)** - dead reckoning with accelerometers and gyros
8. **GNSS/INS sensor fusion** - the Kalman filter that combines them

This is the whole chain from raw satellite signal to a fused,
high-rate, robust position. Later lessons build on earlier ones, so work
through them in order.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is GNSS, broadly?",
                    (
                        opt("A single satellite operated by the United States"),
                        opt(
                            "The general term for satellite navigation systems (GPS, "
                            "Galileo, GLONASS, BeiDou) that let a receiver compute its "
                            "position on Earth",
                            correct=True,
                        ),
                        opt("A type of inertial sensor"),
                        opt("A map projection standard"),
                    ),
                    "GNSS = Global Navigation Satellite Systems - GPS is one of several; "
                    "Galileo, GLONASS and BeiDou are the others.",
                ),
                q(
                    "Roughly what accuracy can precise techniques like RTK reach?",
                    (
                        opt("Hundreds of metres"),
                        opt("Kilometres"),
                        opt("A few centimetres", correct=True),
                        opt("Only whole degrees of latitude"),
                    ),
                    "A basic fix is metre-level; RTK and PPP push it to centimetres.",
                ),
            ),
        ),
        # -- 1. Constellations and signals -----------------------------
        _t(
            "GNSS constellations and signals",
            "10 min",
            """# GNSS constellations and signals

**GNSS** is an umbrella term for the four global satellite navigation
systems, each a **constellation** of satellites in medium Earth orbit
(around 20000 km altitude):

- **GPS** - United States, about 31 satellites, six orbital planes.
- **GLONASS** - Russia, about 24 satellites.
- **Galileo** - European Union, about 24 to 30 satellites.
- **BeiDou** - China, about 30 satellites in mixed orbits.

A modern receiver is **multi-constellation**: tracking GPS plus Galileo
plus others at once means more satellites in view, better geometry, and a
fix even in tight urban canyons.

Each satellite continuously broadcasts a low-power **radio signal** on
L-band frequencies (for example GPS **L1 at 1575.42 MHz** and **L5 at
1176.45 MHz**). The signal carries three things layered together:

- A **carrier** - the raw sine wave at the L-band frequency.
- A **ranging code** - a known pseudo-random noise (PRN) sequence unique
  to each satellite, that the receiver correlates against to measure
  travel time and to tell satellites apart.
- The **navigation message** - the satellite's own clock correction and
  **ephemeris** (precise orbit), so the receiver knows exactly where the
  satellite was when it transmitted.

Because the code and carrier travel at the speed of light, timing is
everything. The carrier wavelength is tiny - which is what later makes
centimetre positioning possible:

```text
lambda = c / f
c = 299792458 m/s        (speed of light)
f_L1 = 1575.42e6 Hz      (GPS L1 frequency)

lambda_L1 = 299792458 / 1575.42e6
          = 0.1903 m      (about 19 cm per carrier cycle)
```

```mermaid
graph TD
    SAT["GNSS satellite"] --> CAR["Carrier L band sine wave"]
    SAT --> CODE["PRN ranging code"]
    SAT --> NAV["Navigation message"]
    NAV --> EPH["Ephemeris satellite orbit"]
    NAV --> CLK["Satellite clock correction"]
    CODE --> RX["Receiver correlates and measures time"]
    CAR --> RX
```

Remember: several independent constellations, each satellite broadcasting
a coded signal plus its own position and clock - that is the raw material
a receiver turns into a fix.
""",
        ),
        quiz_lesson(
            "Quiz: GNSS constellations and signals",
            (
                q(
                    "Which four systems make up the global GNSS constellations?",
                    (
                        opt("GPS, Galileo, GLONASS, BeiDou", correct=True),
                        opt("GPS, WAAS, EGNOS, MSAS"),
                        opt("GPS, Iridium, Starlink, OneWeb"),
                        opt("GPS, WGS84, UTM, ITRF"),
                    ),
                    "GPS (US), GLONASS (Russia), Galileo (EU), BeiDou (China) are the "
                    "four global systems. WAAS/EGNOS are augmentation systems, not "
                    "constellations.",
                ),
                q(
                    "What does the navigation message broadcast by each satellite contain?",
                    (
                        opt("A photo of the ground below"),
                        opt(
                            "The satellite's clock correction and ephemeris (its precise "
                            "orbit), so the receiver knows where and when the signal was sent",
                            correct=True,
                        ),
                        opt("The receiver's position"),
                        opt("The weather forecast"),
                    ),
                    "To range off a satellite you must know exactly where it was and how "
                    "its clock stood - that is the ephemeris and clock correction.",
                ),
                q(
                    "Why is a multi-constellation receiver an advantage?",
                    (
                        opt("It uses less battery"),
                        opt(
                            "Tracking more systems at once means more satellites in view, "
                            "better geometry and a fix even in urban canyons",
                            correct=True,
                        ),
                        opt("It removes the need for the navigation message"),
                        opt("It makes the carrier wavelength longer"),
                    ),
                    "More satellites from multiple systems improves availability and "
                    "geometry, especially where the sky is partly blocked.",
                ),
            ),
        ),
        # -- 2. Trilateration and pseudoranges -------------------------
        _t(
            "Trilateration and pseudoranges",
            "11 min",
            """# Trilateration and pseudoranges

The core idea of GNSS is **trilateration**: if you know your distance to
several satellites whose positions you know, you can solve for your own
position. One distance puts you on a sphere around a satellite; two
spheres intersect in a circle; three narrow it to two points; a fourth
resolves the ambiguity.

How does the receiver measure distance? It measures **travel time**. Each
satellite stamps its signal with the transmit time; the receiver notes the
arrival time; the difference times the speed of light is the range:

```text
range = c * (t_arrival - t_transmit)
```

There is a catch. The satellites carry atomic clocks, but your receiver
has a cheap quartz clock that is **offset** from GNSS time by some unknown
bias. That bias multiplied by the speed of light is a large error in every
range - so the measured range is not the true geometric range. We call it
a **pseudorange**:

```text
P_i = rho_i + c * dt_receiver + errors

  P_i          measured pseudorange to satellite i
  rho_i        true geometric distance to satellite i
  c * dt_recv  receiver clock bias (SAME unknown for all satellites)
  errors       atmosphere, orbit, noise (later lessons)
```

The key insight: the **receiver clock bias is the same unknown in every
pseudorange**. So there are four unknowns - your x, y, z and that clock
bias dt. Four unknowns need **four equations**, which is why you need at
least **four satellites** for a 3D fix (not three, as pure geometry would
suggest).

```mermaid
graph TD
    S1["Satellite 1 range"] --> SOLVE["Solve four unknowns"]
    S2["Satellite 2 range"] --> SOLVE
    S3["Satellite 3 range"] --> SOLVE
    S4["Satellite 4 range"] --> SOLVE
    SOLVE --> XYZ["Receiver position x y z"]
    SOLVE --> DT["Receiver clock bias"]
```

The geometric range itself is just the distance between two points in
Earth-centred Earth-fixed (ECEF) coordinates:

```python
import math

def geometric_range(sat_xyz, rx_xyz):
    # both in ECEF metres
    return math.dist(sat_xyz, rx_xyz)

sat = (15600000.0, 7540000.0, 20140000.0)   # a satellite in ECEF
rx  = (1113000.0, -4850000.0, 3990000.0)     # a receiver on the ground
print(round(geometric_range(sat, rx)))       # -> distance in metres
```

Remember: a GNSS receiver does not measure distance directly - it measures
time, corrupted by its own clock, giving a pseudorange. Solving four of
them together recovers both position and the clock bias.
""",
        ),
        quiz_lesson(
            "Quiz: Trilateration and pseudoranges",
            (
                q(
                    "Why is the measured range called a 'pseudorange' rather than a true range?",
                    (
                        opt("Because satellites move too fast to measure"),
                        opt(
                            "Because the receiver's cheap clock is offset from GNSS time, "
                            "adding an unknown bias to every measured range",
                            correct=True,
                        ),
                        opt("Because it is measured in the wrong units"),
                        opt("Because the Earth is not a perfect sphere"),
                    ),
                    "The receiver clock bias times the speed of light corrupts every "
                    "range identically - so it is a pseudorange, not the true distance.",
                ),
                q(
                    "Why do you need at least four satellites for a 3D fix?",
                    (
                        opt("Three fail too often, four is just for safety"),
                        opt(
                            "There are four unknowns - x, y, z and the receiver clock "
                            "bias - so you need four equations",
                            correct=True,
                        ),
                        opt("Because there are four constellations"),
                        opt("To average out the speed of light"),
                    ),
                    "Position is three unknowns, plus the common clock bias makes four; "
                    "four pseudoranges give four equations.",
                ),
                q(
                    "What does the receiver actually measure to get a range?",
                    (
                        opt("The angle to each satellite with a camera"),
                        opt("The Doppler shift only"),
                        opt(
                            "The signal travel time (arrival minus transmit), multiplied "
                            "by the speed of light",
                            correct=True,
                        ),
                        opt("The satellite's altitude"),
                    ),
                    "GNSS ranging is fundamentally a timing measurement: range = c times "
                    "travel time.",
                ),
            ),
        ),
        # -- 3. Position solution and DOP ------------------------------
        _t(
            "Position solution and dilution of precision (DOP)",
            "11 min",
            """# Position solution and dilution of precision (DOP)

The four pseudorange equations are **non-linear** (distance involves a
square root), so receivers solve them by **linearizing** around an initial
guess and iterating - a least-squares fix. Starting from a guessed
position, you compute the predicted ranges, compare to the measured ones,
and correct. Written in matrix form, one iteration is:

```text
delta_x = (G^T G)^-1 G^T * delta_rho

  delta_rho   measured minus predicted pseudoranges (the residuals)
  G           geometry matrix - unit vectors from receiver to each
              satellite, with a 1 in the clock column
  delta_x     the correction to [x, y, z, clock_bias]
```

You repeat until the correction is tiny. With more than four satellites
the system is **over-determined** and least squares finds the best fit.

The interesting part is that same **geometry matrix G**. It captures where
the satellites sit in the sky, and it decides how much the unavoidable
ranging noise gets amplified into position error. That amplification is
called **Dilution of Precision (DOP)** and it comes straight from G:

```python
import numpy as np

# G rows: [-ux, -uy, -uz, 1] unit line-of-sight vectors + clock column
Q = np.linalg.inv(G.T @ G)     # cofactor matrix
gdop = np.sqrt(np.trace(Q))            # Geometric DOP
pdop = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])  # Position DOP
# position_error ~= PDOP * ranging_error
```

Lower DOP is better. Common flavours: **PDOP** (position), **HDOP**
(horizontal), **VDOP** (vertical), **TDOP** (time), **GDOP** (all
together). Rules of thumb: a PDOP under 2 is excellent, 2 to 5 is good,
above 6 is poor.

The intuition: satellites **spread wide across the sky** give strong,
well-conditioned geometry and low DOP. Satellites **bunched together**
give slivered intersections and high DOP - the same ranging noise now
smears position badly. Vertical accuracy is usually worse than horizontal
because you only see satellites above you, never below the horizon.

```mermaid
graph TD
    SPREAD["Satellites spread across sky"] --> LOW["Low DOP"]
    LOW --> GOOD["Small position error"]
    BUNCH["Satellites bunched together"] --> HIGH["High DOP"]
    HIGH --> BAD["Large position error"]
    NOISE["Ranging noise"] --> BOTH["Multiplied by DOP"]
    BOTH --> RESULT["Position error"]
```

Remember: the solution is least squares over the pseudoranges, and DOP -
purely a function of satellite geometry - tells you how kindly or cruelly
that geometry turns ranging noise into position error.
""",
        ),
        quiz_lesson(
            "Quiz: Position solution and dilution of precision (DOP)",
            (
                q(
                    "What does Dilution of Precision (DOP) describe?",
                    (
                        opt("The number of satellites in orbit"),
                        opt(
                            "How the satellite geometry amplifies ranging errors into "
                            "position error - lower DOP is better",
                            correct=True,
                        ),
                        opt("The strength of the radio signal"),
                        opt("The receiver's battery drain"),
                    ),
                    "DOP is a pure geometry factor: position error is roughly DOP times "
                    "ranging error.",
                ),
                q(
                    "Which satellite arrangement gives the best (lowest) DOP?",
                    (
                        opt("All satellites bunched together in one part of the sky"),
                        opt("All satellites near the horizon in a line"),
                        opt(
                            "Satellites well spread across the sky, giving strong geometry",
                            correct=True,
                        ),
                        opt("A single satellite directly overhead"),
                    ),
                    "Wide angular spread gives well-conditioned geometry and low DOP; "
                    "bunched satellites give high DOP.",
                ),
                q(
                    "Why is a GNSS position solved iteratively with least squares?",
                    (
                        opt("Because the receiver clock is perfect"),
                        opt(
                            "The pseudorange equations are non-linear, so the receiver "
                            "linearizes around a guess and iterates to the best fit",
                            correct=True,
                        ),
                        opt("Because there are always exactly four satellites"),
                        opt("To make the DOP larger"),
                    ),
                    "Distance is non-linear; linearize, correct, repeat - and with extra "
                    "satellites least squares finds the best over-determined fit.",
                ),
            ),
        ),
        # -- 4. Error sources ------------------------------------------
        _t(
            "Error sources (ionosphere, troposphere, multipath)",
            "11 min",
            """# Error sources (ionosphere, troposphere, multipath)

A raw single-frequency fix is good to only a few metres because the
pseudorange is corrupted by several **error sources**. Understanding them
is the key to every precise technique that follows - each technique is
really just a way to remove one or more of these errors.

The main contributors, with rough magnitudes:

- **Ionospheric delay** (up to ~5 m, largest) - free electrons in the
  upper atmosphere slow the code. Crucially it is **dispersive**: it
  depends on frequency, so a **dual-frequency** receiver (L1 and L5) can
  measure and cancel most of it.
- **Tropospheric delay** (~0.5 to 3 m) - the lower, wet atmosphere delays
  the signal. It is **not** frequency-dependent, so dual frequency does
  not help; it is handled with models and by estimating it.
- **Multipath** (up to a few metres) - the signal bounces off buildings,
  water or the ground and arrives via a longer path. Highly local, hard to
  model, worst in cities. Good antennas and choke rings suppress it.
- **Satellite clock and orbit (ephemeris) errors** (~1 m) - the broadcast
  clock and orbit are slightly off; precise products correct them.
- **Receiver noise** (a few decimetres) - thermal noise in the receiver.

The pseudorange error budget adds up like this (errors are largely
independent, so combine as a root-sum-of-squares):

```text
sigma_UERE = sqrt( sigma_iono^2 + sigma_tropo^2 + sigma_mp^2
                   + sigma_clk^2 + sigma_orb^2 + sigma_noise^2 )

position_error ~= DOP * sigma_UERE     (UERE = User Equivalent Range Error)
```

The dual-frequency ionosphere cancellation is worth seeing - because the
delay scales as 1 over frequency squared, combining two frequencies
removes the first-order term:

```text
P_ionofree = (f1^2 * P_L1 - f5^2 * P_L5) / (f1^2 - f5^2)
```

```mermaid
graph TD
    SAT["Satellite signal"] --> IONO["Ionosphere delay dispersive"]
    IONO --> TROPO["Troposphere delay wet"]
    TROPO --> MP["Multipath reflections"]
    MP --> RX["Receiver noise"]
    RX --> PR["Corrupted pseudorange"]
    IONO --> DF["Dual frequency cancels iono"]
    MP --> ANT["Good antenna suppresses multipath"]
```

Remember: iono (cancel with dual frequency), tropo (model it), multipath
(better antenna and siting), plus clock and orbit errors - the total
User Equivalent Range Error, multiplied by DOP, is your position error.
""",
        ),
        quiz_lesson(
            "Quiz: Error sources (ionosphere, troposphere, multipath)",
            (
                q(
                    "Why can a dual-frequency receiver largely remove the ionospheric "
                    "delay but not the tropospheric delay?",
                    (
                        opt("The troposphere is farther away"),
                        opt(
                            "The ionospheric delay is dispersive (frequency-dependent) "
                            "so two frequencies can cancel it; the tropospheric delay is "
                            "not frequency-dependent",
                            correct=True,
                        ),
                        opt("The troposphere only affects the carrier"),
                        opt("Dual frequency removes both equally"),
                    ),
                    "Iono delay scales with 1/f^2, so an iono-free combination cancels "
                    "it; tropo delay is the same at all frequencies and must be modelled.",
                ),
                q(
                    "What characterizes multipath error?",
                    (
                        opt("It is identical for every receiver on Earth"),
                        opt(
                            "It comes from the signal reflecting off nearby surfaces, is "
                            "highly local, and is worst in built-up areas",
                            correct=True,
                        ),
                        opt("It is removed by dual frequency"),
                        opt("It only affects the satellite clock"),
                    ),
                    "Multipath is a local reflection effect - hard to model, suppressed "
                    "with good antennas, choke rings and careful siting.",
                ),
                q(
                    "Position error is roughly which product?",
                    (
                        opt("Number of satellites times signal strength"),
                        opt("DOP times the User Equivalent Range Error (UERE)", correct=True),
                        opt("Carrier frequency times wavelength"),
                        opt("Receiver clock bias times the speed of light"),
                    ),
                    "The combined ranging error (UERE) is amplified by the geometry "
                    "factor DOP to give position error.",
                ),
            ),
        ),
        # -- 5. Differential GNSS and RTK ------------------------------
        _t(
            "Differential GNSS and RTK",
            "12 min",
            """# Differential GNSS and RTK

Many of the biggest errors - ionosphere, troposphere, satellite clock and
orbit - are **almost identical for two receivers that are close together**,
because their signals travel through nearly the same atmosphere from the
same satellites. This is the whole idea behind **differential GNSS**.

Put one receiver on a precisely surveyed point (the **base station**).
Because it knows its true position, it can compute how far off each
pseudorange is and broadcast those **corrections** to nearby **rover**
receivers. The rover applies them and cancels the shared errors, improving
a metre-level fix to sub-metre or better. This works because the errors
are **spatially correlated**; accuracy degrades as the rover moves farther
from the base (the "baseline" grows).

**RTK (Real-Time Kinematic)** takes this much further by using the
**carrier phase** instead of the code. Recall the L1 carrier wavelength is
about 19 cm; the receiver can measure its phase to a few percent of a
cycle - millimetres. The problem is the **integer ambiguity N**: the
receiver measures the fractional phase but not how many whole cycles fit
in the range.

```text
Phi = rho + c*dt + lambda * N + small_errors

  Phi       carrier-phase measurement (very precise, but ambiguous)
  lambda    carrier wavelength (~0.19 m on L1)
  N         unknown INTEGER number of whole cycles - the ambiguity
```

RTK's job is **ambiguity resolution**: using the base-rover differences
and a few epochs of data, algorithms (such as LAMBDA) fix N to the correct
integers. Once the ambiguities are **fixed**, the carrier measurements
give **centimetre-level** positioning in real time - hence RTK for
surveying, machine control and precision agriculture. Until they are
fixed, the solution is "float" and less accurate.

```mermaid
graph LR
    BASE["Base on known point"] --> CORR["Compute corrections"]
    CORR --> LINK["Radio or network link"]
    LINK --> ROVER["Rover applies corrections"]
    ROVER --> AMB["Resolve integer ambiguity"]
    AMB --> FIX["Fixed centimetre solution"]
    SAT["Shared satellites and atmosphere"] --> BASE
    SAT --> ROVER
```

Networked versions (**Network RTK**, VRS) use many permanent base stations
to model errors over a region, so a single rover gets corrections without
its own nearby base. The trade-off across all differential methods:
accuracy depends on baseline length and on keeping a live correction link.

Remember: differential GNSS cancels the errors two nearby receivers share;
RTK adds precise carrier-phase ranging plus integer ambiguity resolution
to reach centimetres in real time.
""",
        ),
        quiz_lesson(
            "Quiz: Differential GNSS and RTK",
            (
                q(
                    "Why does differential GNSS improve a rover's accuracy?",
                    (
                        opt("It gives the rover a faster clock"),
                        opt(
                            "A base on a known point measures the shared errors "
                            "(atmosphere, orbit, clock) and sends corrections the nearby "
                            "rover applies to cancel them",
                            correct=True,
                        ),
                        opt("It adds more satellites to the sky"),
                        opt("It removes the need for the carrier signal"),
                    ),
                    "Nearby receivers see nearly identical atmospheric and orbit errors; "
                    "the base measures and broadcasts them so the rover can subtract them.",
                ),
                q(
                    "What is the 'integer ambiguity' that RTK must resolve?",
                    (
                        opt("The satellite's identity"),
                        opt("The receiver's battery level"),
                        opt(
                            "The unknown whole number of carrier cycles in the range - "
                            "the receiver measures fractional phase but not the integer "
                            "count",
                            correct=True,
                        ),
                        opt("The number of satellites in view"),
                    ),
                    "Carrier phase is precise but ambiguous by an integer number of "
                    "wavelengths; resolving N is what unlocks centimetre RTK.",
                ),
                q(
                    "What mainly limits differential GNSS and RTK accuracy?",
                    (
                        opt("The colour of the antenna"),
                        opt(
                            "The baseline length - errors are only shared while the rover "
                            "stays reasonably close to the base - plus needing a live "
                            "correction link",
                            correct=True,
                        ),
                        opt("The time of day only"),
                        opt("The number of constellations disabled"),
                    ),
                    "The shared-error assumption weakens as the baseline grows; RTK also "
                    "needs a continuous correction stream.",
                ),
            ),
        ),
        # -- 6. Precise Point Positioning ------------------------------
        _t(
            "Precise Point Positioning (PPP)",
            "11 min",
            """# Precise Point Positioning (PPP)

RTK is superb but needs a nearby base station or network. **Precise Point
Positioning (PPP)** achieves high accuracy with a **single receiver
anywhere on Earth** - no local base - by replacing local corrections with
**precise global products**.

The key ingredients:

- **Precise satellite orbit and clock products** - instead of trusting the
  broadcast ephemeris, PPP uses precise orbits and clocks computed
  globally (for example by the **IGS**, the International GNSS Service).
  This removes the satellite clock and orbit errors.
- **Dual-frequency measurements** - to form the iono-free combination and
  cancel the ionosphere.
- **Careful modelling** of everything else - tropospheric delay (estimated
  as an unknown), solid-earth tides, antenna phase centres, relativity.
- **Carrier phase** for precision, so PPP also estimates float ambiguities.

Because PPP has no base to difference against, it must **estimate more
unknowns itself** (receiver clock, tropospheric delay, ambiguities), which
takes time to settle - the classic drawback is a **convergence period** of
tens of minutes to reach centimetre accuracy. Modern **PPP-AR**
(ambiguity resolution) and **PPP-RTK** hybrids using regional corrections
shorten this dramatically.

The processing model, in words: start from the iono-free pseudorange and
carrier, apply the precise clock and orbit, and estimate the rest in a
filter:

```python
# PPP observation model (conceptual, iono-free combination)
def ppp_residual(P_if, Phi_if, sat_pos_precise, sat_clk_precise,
                 rx_pos, rx_clk, tropo, amb_if):
    rho = geometric_range(sat_pos_precise, rx_pos)
    code_pred    = rho + rx_clk - sat_clk_precise + tropo
    carrier_pred = rho + rx_clk - sat_clk_precise + tropo + amb_if
    return (P_if - code_pred, Phi_if - carrier_pred)
# a Kalman filter estimates rx_pos, rx_clk, tropo and amb_if over time
```

```mermaid
graph TD
    IGS["Precise orbit and clock products"] --> PPP["PPP engine"]
    DUAL["Dual frequency iono free"] --> PPP
    MODEL["Tropo tides antenna models"] --> PPP
    RX["Single receiver anywhere"] --> PPP
    PPP --> CONV["Converges over tens of minutes"]
    CONV --> CM["Centimetre to decimetre position"]
```

Remember: RTK differences against a nearby base; PPP instead uses precise
global orbit and clock products and models everything, giving worldwide
high accuracy from one receiver - at the cost of a convergence time.
""",
        ),
        quiz_lesson(
            "Quiz: Precise Point Positioning (PPP)",
            (
                q(
                    "How does PPP differ fundamentally from RTK?",
                    (
                        opt("PPP needs two nearby base stations"),
                        opt(
                            "PPP uses precise global orbit and clock products with a "
                            "single receiver anywhere, instead of differencing against a "
                            "nearby base station",
                            correct=True,
                        ),
                        opt("PPP does not use the carrier phase"),
                        opt("PPP only works indoors"),
                    ),
                    "PPP replaces a local base with precise global products (e.g. from "
                    "IGS), so one receiver can position anywhere on Earth.",
                ),
                q(
                    "What is the classic drawback of PPP?",
                    (
                        opt("It only works at the equator"),
                        opt(
                            "A convergence period of tens of minutes before it reaches "
                            "centimetre accuracy, because it must estimate many unknowns "
                            "itself",
                            correct=True,
                        ),
                        opt("It requires disabling all but one constellation"),
                        opt("It cannot use dual-frequency signals"),
                    ),
                    "With no base to difference against, PPP estimates clock, tropo and "
                    "ambiguities itself, which takes time to settle. PPP-AR shortens it.",
                ),
                q(
                    "Which products let PPP remove satellite clock and orbit errors?",
                    (
                        opt("The broadcast navigation message alone"),
                        opt("Local base station corrections"),
                        opt(
                            "Precise global orbit and clock products, such as those from the IGS",
                            correct=True,
                        ),
                        opt("A barometric altimeter"),
                    ),
                    "Precise orbit and clock products computed globally replace the less "
                    "accurate broadcast ephemeris.",
                ),
            ),
        ),
        # -- 7. Inertial navigation (INS) ------------------------------
        _t(
            "Inertial navigation (INS) and integration",
            "11 min",
            """# Inertial navigation (INS) and integration

GNSS tells you where you are, but only when it can see the sky and only a
few times a second. **Inertial navigation** is the complementary
technology: it needs no external signal at all. An **Inertial Measurement
Unit (IMU)** contains **accelerometers** (measuring specific force) and
**gyroscopes** (measuring angular rate) on three axes.

An **INS** turns those raw measurements into position, velocity and
orientation by **dead reckoning** - integrating the motion over time,
starting from a known initial state:

```text
orientation:  integrate gyro rate      -> attitude (roll, pitch, yaw)
velocity:     integrate acceleration   -> velocity
position:     integrate velocity       -> position

  a_nav = R(attitude) * a_body - g      (rotate to nav frame, remove gravity)
  v = v0 + integral(a_nav dt)
  p = p0 + integral(v dt)
```

The strengths are exactly where GNSS is weak: an INS runs at **high rate**
(hundreds of Hz), is **self-contained** (works in tunnels, indoors, under
jamming), and gives **smooth attitude** and short-term motion.

The fatal weakness is **drift**. Every sensor has small errors - a
**bias**, noise, scale-factor error - and integration accumulates them.
Worse, position comes from a **double integration** of acceleration, so a
constant accelerometer bias grows as time **squared**:

```python
# position error from a constant accelerometer bias b (double integration)
def drift_position_error(bias_accel, t):
    return 0.5 * bias_accel * t**2

# a modest 0.01 m/s^2 bias, unaided, after 60 s:
print(drift_position_error(0.01, 60))   # -> 18 metres, and growing
```

That is why a standalone INS is unusable for long unaided periods - and
exactly why it is paired with GNSS. GNSS is drift-free but low-rate and
sky-dependent; INS is high-rate and self-contained but drifts. Each covers
the other's weakness.

```mermaid
graph TD
    IMU["IMU accelerometers and gyros"] --> GYRO["Integrate rate to attitude"]
    IMU --> ACC["Rotate and remove gravity"]
    GYRO --> ACC
    ACC --> VEL["Integrate to velocity"]
    VEL --> POS["Integrate to position"]
    POS --> DRIFT["Drift grows over time"]
    DRIFT --> AID["Needs external aiding like GNSS"]
```

Remember: an INS dead-reckons position from accelerometers and gyros at
high rate with no external signal, but drift from sensor bias grows
without bound - so it must be periodically corrected by an absolute source
like GNSS.
""",
        ),
        quiz_lesson(
            "Quiz: Inertial navigation (INS) and integration",
            (
                q(
                    "What does an Inertial Measurement Unit (IMU) directly measure?",
                    (
                        opt("Absolute latitude and longitude"),
                        opt(
                            "Specific force (accelerometers) and angular rate "
                            "(gyroscopes) on three axes",
                            correct=True,
                        ),
                        opt("Distance to satellites"),
                        opt("The Earth's magnetic declination"),
                    ),
                    "Accelerometers measure specific force, gyros measure angular rate; "
                    "an INS integrates these into position, velocity and attitude.",
                ),
                q(
                    "Why does a standalone INS drift so badly over time?",
                    (
                        opt("It loses satellite lock"),
                        opt(
                            "Sensor errors like bias accumulate through integration - "
                            "and position comes from double-integrating acceleration, so "
                            "a constant bias grows with time squared",
                            correct=True,
                        ),
                        opt("The gyroscopes run out of power"),
                        opt("The troposphere delays the IMU"),
                    ),
                    "Dead reckoning integrates errors; the double integration for "
                    "position makes a constant accelerometer bias grow as t^2.",
                ),
                q(
                    "How do INS and GNSS complement each other?",
                    (
                        opt("Both are low-rate and sky-dependent"),
                        opt(
                            "GNSS is drift-free but low-rate and needs sky view; INS is "
                            "high-rate and self-contained but drifts - each covers the "
                            "other's weakness",
                            correct=True,
                        ),
                        opt("They measure the same quantity, so one is redundant"),
                        opt("INS provides the satellite ephemeris to GNSS"),
                    ),
                    "GNSS bounds the INS drift with absolute fixes; INS bridges GNSS "
                    "outages and provides high-rate smooth motion.",
                ),
            ),
        ),
        # -- 8. GNSS/INS sensor fusion ---------------------------------
        _t(
            "GNSS/INS sensor fusion (Kalman filter)",
            "12 min",
            """# GNSS/INS sensor fusion (Kalman filter)

To get the best of both worlds - GNSS's absolute, drift-free accuracy and
INS's high rate and continuity - you **fuse** them. The standard tool is
the **Kalman filter**, an optimal recursive estimator that combines a
prediction with a measurement, weighting each by how much you trust it.

The filter runs a two-step cycle:

- **Predict** - use the INS (the fast sensor) to propagate the state
  (position, velocity, attitude) forward and grow the uncertainty
  covariance. This runs at the IMU rate, hundreds of times a second.
- **Update** - when a GNSS fix arrives (say 1 to 10 Hz), correct the
  predicted state toward the measurement and shrink the uncertainty. The
  **Kalman gain** decides the blend: trust GNSS more when the INS is
  uncertain, trust the INS more when GNSS is noisy or briefly gone.

The core update equations:

```text
K = P_pred H^T (H P_pred H^T + R)^-1        # Kalman gain
x = x_pred + K (z - H x_pred)               # corrected state
P = (I - K H) P_pred                        # reduced covariance

  x   state (position, velocity, attitude, IMU biases)
  z   GNSS measurement
  P   state covariance (uncertainty)
  R   measurement noise; H maps state to measurement
```

A crucial trick: the filter's state includes the **IMU biases**, so each
GNSS update also **estimates and removes the accelerometer and gyro
biases** - actively calibrating the INS. That is what keeps drift bounded.

Two coupling architectures:

- **Loosely coupled** - fuse the GNSS position/velocity solution with the
  INS. Simple, but needs 4+ satellites to have a GNSS fix at all.
- **Tightly coupled** - fuse the raw GNSS pseudoranges with the INS, so
  even **one or two satellites** still help. More robust in urban canyons,
  more complex.

During a GNSS outage (tunnel, canyon) the filter **coasts** on the INS,
its now-calibrated biases keeping drift small until GNSS returns and
snaps the estimate back.

```mermaid
graph LR
    IMU["IMU high rate"] --> PRED["Predict state and covariance"]
    PRED --> STATE["Fused state"]
    GNSS["GNSS one to ten Hz"] --> UPD["Update with Kalman gain"]
    PRED --> UPD
    UPD --> STATE
    STATE --> BIAS["Estimate IMU biases"]
    BIAS --> PRED
    STATE --> OUT["High rate drift bounded position"]
```

Remember: the Kalman filter predicts with the fast INS and corrects with
absolute GNSS, estimating the IMU biases as it goes - delivering a
high-rate, smooth, drift-bounded navigation solution that survives brief
GNSS outages.
""",
        ),
        quiz_lesson(
            "Quiz: GNSS/INS sensor fusion (Kalman filter)",
            (
                q(
                    "In a GNSS/INS Kalman filter, what do the predict and update steps do?",
                    (
                        opt("Both simply average the last ten GNSS fixes"),
                        opt(
                            "Predict propagates the state forward using the high-rate "
                            "INS; update corrects it toward each GNSS measurement, "
                            "weighted by the Kalman gain",
                            correct=True,
                        ),
                        opt("Predict uses GNSS, update uses a map"),
                        opt("Neither step uses the INS"),
                    ),
                    "The fast INS drives prediction between fixes; each GNSS fix updates "
                    "and re-anchors the estimate.",
                ),
                q(
                    "Why is it valuable that the filter's state includes the IMU biases?",
                    (
                        opt("It makes the filter run faster"),
                        opt(
                            "Each GNSS update estimates and removes the accelerometer and "
                            "gyro biases, actively calibrating the INS so drift stays "
                            "bounded",
                            correct=True,
                        ),
                        opt("It replaces the need for gyroscopes"),
                        opt("It lets the receiver skip the ephemeris"),
                    ),
                    "Estimating the biases online is what keeps INS drift small, "
                    "especially while coasting through GNSS outages.",
                ),
                q(
                    "What is the advantage of tight coupling over loose coupling?",
                    (
                        opt("It never needs an IMU"),
                        opt("It only works with a single constellation"),
                        opt(
                            "It fuses the raw pseudoranges, so even one or two satellites "
                            "still help - more robust in urban canyons",
                            correct=True,
                        ),
                        opt("It requires more satellites than loose coupling"),
                    ),
                    "Loose coupling needs a full GNSS fix (4+ satellites); tight coupling "
                    "uses raw measurements and benefits from even a few satellites.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does GNSS stand for and include?",
                    (
                        opt("A single US satellite called GPS"),
                        opt(
                            "Global Navigation Satellite Systems - the umbrella for GPS, "
                            "Galileo, GLONASS and BeiDou",
                            correct=True,
                        ),
                        opt("A ground-based radio beacon network"),
                        opt("A map projection like UTM"),
                    ),
                    "GNSS covers all four global constellations; GPS is just one of them.",
                ),
                q(
                    "Why does a 3D GNSS fix need at least four satellites?",
                    (
                        opt("Because there are four constellations"),
                        opt(
                            "There are four unknowns - x, y, z and the receiver clock "
                            "bias - so four pseudorange equations are needed",
                            correct=True,
                        ),
                        opt("To average the speed of light"),
                        opt("Three satellites give no distance"),
                    ),
                    "The common receiver clock bias adds a fourth unknown to the three "
                    "position coordinates.",
                ),
                q(
                    "What is a pseudorange?",
                    (
                        opt("The exact geometric distance to a satellite"),
                        opt(
                            "The measured range corrupted by the unknown receiver clock "
                            "bias (and other errors)",
                            correct=True,
                        ),
                        opt("The distance between two satellites"),
                        opt("The carrier wavelength"),
                    ),
                    "Receiver clock bias times c corrupts every measured range, making it "
                    "a pseudorange rather than the true distance.",
                ),
                q(
                    "What does DOP (Dilution of Precision) tell you?",
                    (
                        opt("The signal strength"),
                        opt(
                            "How satellite geometry amplifies ranging error into position "
                            "error - lower is better",
                            correct=True,
                        ),
                        opt("The number of visible constellations"),
                        opt("The receiver clock drift rate"),
                    ),
                    "Position error is roughly DOP times ranging error; wide sky spread "
                    "gives low DOP.",
                ),
                q(
                    "Which error can a dual-frequency receiver largely cancel on its own?",
                    (
                        opt("Multipath"),
                        opt("Tropospheric delay"),
                        opt("Ionospheric delay (it is dispersive)", correct=True),
                        opt("Receiver thermal noise"),
                    ),
                    "The ionosphere is frequency-dependent, so an iono-free combination "
                    "of two frequencies removes most of it; the troposphere is not.",
                ),
                q(
                    "How does RTK reach centimetre accuracy?",
                    (
                        opt("By using only the broadcast ephemeris"),
                        opt(
                            "By using precise carrier-phase measurements and resolving "
                            "the integer ambiguity, with base-station corrections",
                            correct=True,
                        ),
                        opt("By adding more receiver noise"),
                        opt("By disabling all but one satellite"),
                    ),
                    "Carrier phase is precise to millimetres once the integer ambiguity "
                    "is fixed, and base corrections cancel the shared errors.",
                ),
                q(
                    "What distinguishes PPP from RTK?",
                    (
                        opt("PPP needs a nearby base station; RTK does not"),
                        opt(
                            "PPP uses precise global orbit and clock products with a "
                            "single receiver anywhere, at the cost of a convergence time",
                            correct=True,
                        ),
                        opt("PPP is always faster to converge than RTK"),
                        opt("PPP ignores the carrier phase"),
                    ),
                    "PPP trades RTK's local base for precise global products, working "
                    "worldwide but needing tens of minutes to converge.",
                ),
                q(
                    "Why does a standalone INS drift over time?",
                    (
                        opt("It loses radio contact with satellites"),
                        opt(
                            "Sensor biases accumulate through integration; position "
                            "double-integrates acceleration, so a constant bias grows as "
                            "time squared",
                            correct=True,
                        ),
                        opt("The gyroscopes overheat"),
                        opt("The ionosphere delays its signal"),
                    ),
                    "Dead reckoning integrates small sensor errors without bound - the "
                    "reason an INS must be aided.",
                ),
                q(
                    "In GNSS/INS fusion, what role does the Kalman filter's predict step play?",
                    (
                        opt("It downloads new ephemeris"),
                        opt(
                            "It propagates the state forward at high rate using the INS "
                            "between GNSS fixes",
                            correct=True,
                        ),
                        opt("It resolves the RTK integer ambiguity"),
                        opt("It computes the map projection"),
                    ),
                    "The fast INS drives prediction; GNSS fixes then update and re-anchor "
                    "the estimate.",
                ),
                q(
                    "What keeps INS drift bounded during a GNSS outage in a fused system?",
                    (
                        opt("The receiver simply turns off"),
                        opt(
                            "The filter has already estimated and removed the IMU biases, "
                            "so it can coast on the calibrated INS until GNSS returns",
                            correct=True,
                        ),
                        opt("The troposphere stops delaying the signal"),
                        opt("DOP drops to zero automatically"),
                    ),
                    "Online bias estimation calibrates the INS so it coasts accurately "
                    "through short outages, then GNSS snaps the estimate back.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

GNSS_NAVIGATION_COURSES: tuple[SeedCourse, ...] = (_GNSS_NAVIGATION,)
