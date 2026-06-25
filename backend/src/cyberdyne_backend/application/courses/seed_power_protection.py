"""Power System Protection & Relaying track: Basics -> Intermediate -> Advanced.

From why we protect power systems and the anatomy of faults, through overcurrent
coordination, differential and distance protection, to numerical relays, IEC
61850 and the challenges of inverter-based renewables. Lessons are `text` with
LaTeX, interactive ```plot blocks (inverse-time curves, fault-current decay,
coordination intervals) and ```mermaid schematics (protection zones,
differential schemes, distance reach, instrument transformers).
"""

# Lesson prose uses typographic characters (×, →, ≈, Ω, φ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Power System Protection & Relaying — Basics ──────────────────────────────

_PP_BASICS = SeedCourse(
    slug="power-protection-basics",
    title="Power System Protection & Relaying — Basics",
    description=(
        "Why power systems need protection, the kinds of faults that occur, how "
        "fault current is set by impedance, the instrument transformers that feed "
        "relays, and the protection-zone and backup philosophy — finishing with "
        "the fuses and circuit breakers that actually clear the fault. Interactive "
        "plots and schematics throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why we protect power systems",
            "10 min",
            """\
# Why we protect power systems

A power system carries enormous energy. When insulation breaks down or a
conductor touches ground, a **fault** lets that energy pour into the wrong place.
Protection exists to **detect** the fault and **disconnect** only the faulted
part, as fast as possible, for four reasons:

- **Safety** — fault currents and arcs are lethal to people nearby.
- **Equipment** — fault current of tens of kiloamps melts conductors and explodes
  transformers within cycles.
- **Stability** — a fault left on the system drags voltage down and can make
  generators lose synchronism, cascading into a blackout.
- **Service continuity** — clearing *only* the faulted zone keeps the rest of the
  grid energised.

The job of a **protective relay** is to measure currents and voltages, decide
"fault or no fault", and command a **circuit breaker** to open. The two
competing goals are **speed** (clear fast to limit damage) and **selectivity**
(trip only the right breaker). The whole subject is the art of balancing them.

A protection scheme is judged on five qualities: **reliability** (it operates
when it should), **selectivity** (it isolates only the fault), **speed**,
**sensitivity** (it sees small faults) and **security** (it does *not* trip on
load or external faults).

**Next:** the kinds of faults a relay must recognise.
""",
        ),
        _t(
            "Types of faults",
            "11 min",
            """\
# Types of faults

Faults are short circuits between conductors or to ground. On a three-phase
system there are a handful of types, and they are not equally common.

- **Three-phase fault (3φ)** — all three phases shorted together. The most
  severe (highest current) but the **rarest** (~5%). It is *balanced*, so it can
  be analysed on a single phase.
- **Line-to-line (LL)** — two phases shorted, no ground. ~10%.
- **Single line-to-ground (LG)** — one phase to earth. By far the **most common**
  (~70–80%) and usually the least severe in current.
- **Double line-to-ground (LLG)** — two phases to earth. ~10%.

The LG, LL and LLG faults are **unbalanced** — the three phases no longer carry
equal, symmetric currents, which is why the Intermediate course introduces
*symmetrical components* to analyse them.

```mermaid
flowchart TB
  subgraph ThreePhase["three-phase system"]
    A["phase a"]
    B["phase b"]
    C["phase c"]
    G["ground"]
  end
  A -. "LG fault (~75%)" .-> G
  A -. "LL fault (~10%)" .-> B
  B -. "LLG fault (~10%)" .-> G
  A == "3-phase fault (~5%)" ==> B
  B ==> C
```

Faults can be **transient** (a lightning flashover that self-clears once the line
is de-energised) or **permanent** (a fallen tree). This distinction drives
**auto-reclosing**: open, wait, and re-close — if the fault was transient, service
is restored in under a second.

**Next:** how big the fault current actually gets.
""",
        ),
        _t(
            "Fault current & the role of impedance",
            "11 min",
            """\
# Fault current & the role of impedance

How large is a fault current? In the simplest model it is just Ohm's law: the
source voltage divided by the impedance between the source and the fault,

$$I_\\text{fault} = \\frac{V}{Z_\\text{source} + Z_\\text{line}}.$$

A fault **close to the source** sees little line impedance, so the current is
huge; a fault far down a long feeder sees more $Z_\\text{line}$ and the current is
smaller. This falling-current-with-distance relationship is what lets a relay
*locate* and *grade* faults. Watch fault current drop as the fault moves away:

```plot
{"title": "Fault current falls as the fault moves down the feeder", "xLabel": "distance to fault (km)", "yLabel": "fault current (kA)", "xRange": [0, 40], "yRange": [0, 14], "functions": [{"expr": "12/(1 + 0.18*x)", "label": "I_fault = V/(Z_src + Z_line)", "color": "#2563eb"}], "points": [{"x": 0, "y": 12, "label": "fault at the bus (max)", "color": "#dc2626", "size": 7}]}
```

Two more effects matter:

- **The DC offset.** At the instant of the fault the current cannot jump
  instantly, so a decaying **DC component** rides on top of the AC, making the
  first peak (the *asymmetrical* current) larger than the steady value. Breakers
  must be rated for it.
- **Synchronous-machine decay.** A generator's contribution starts at a high
  *sub-transient* level and decays to a lower *steady-state* value over many
  cycles.

```plot
{"title": "Fault-current envelope decays after the instant of fault", "xLabel": "time (cycles)", "yLabel": "current magnitude (kA)", "xRange": [0, 12], "yRange": [0, 16], "functions": [{"expr": "5 + 10*exp(-x/3)", "label": "rms envelope (sub-transient -> steady)", "color": "#2563eb"}, {"expr": "5", "label": "steady-state level", "color": "#16a34a"}]}
```

Relays exploit the difference between **load current** (amps) and **fault
current** (kiloamps): a fault is simply far more current than the line ever
carries normally.

**Next:** how relays actually measure those kiloamps safely.
""",
        ),
        _t(
            "Instrument transformers: CTs & VTs",
            "11 min",
            """\
# Instrument transformers: CTs & VTs

A relay cannot connect directly to a line carrying kiloamps at hundreds of
kilovolts. **Instrument transformers** scale those quantities down to safe,
standard levels — typically **5 A** (or 1 A) and **110 V** — and isolate the
relay from the primary circuit.

- **Current transformer (CT)** — its primary is in series with the line; it
  outputs a current *proportional* to the line current. A 1000:5 CT turns 1000 A
  into 5 A. **Never open-circuit a CT secondary under load** — the voltage
  spikes dangerously.
- **Voltage transformer (VT/PT)** — its primary is across the line; it outputs a
  scaled voltage. A 132 kV : 110 V VT lets a relay "see" system voltage.

```mermaid
flowchart LR
  subgraph Primary["high-voltage line"]
    L1["line current (kA)"]
    L2["line voltage (kV)"]
  end
  L1 --> CT["CT 1000:5"]
  L2 --> VT["VT 132kV:110V"]
  CT --> R["protective relay<br/>(5 A, 110 V)"]
  VT --> R
  R --> CB["trip -> circuit breaker"]
```

The key non-ideal effect is **CT saturation**: at very high fault currents the
core saturates and the secondary output is no longer proportional — it collapses
and distorts. Saturation can blind or mis-operate a relay, so CTs are
deliberately sized (knee-point voltage, accuracy class such as **5P20**) for the
maximum fault current they must reproduce.

**Next:** how relays divide the system into zones and back each other up.
""",
        ),
        _t(
            "Protection zones & backup",
            "10 min",
            """\
# Protection zones & backup

A power system is carved into overlapping **protection zones**, each bounded by
the CTs of its circuit breakers. Every piece of equipment — generator,
transformer, bus, line — sits inside a zone whose relays will trip the breakers
on its boundary if a fault occurs there.

```mermaid
flowchart LR
  G["generator"] --- B1["bus 1"]
  B1 --- T["transformer"]
  T --- B2["bus 2"]
  B2 --- LINE["transmission line"]
  subgraph Z1["zone: generator"]
    G
  end
  subgraph Z2["zone: transformer"]
    T
  end
  subgraph Z3["zone: line"]
    LINE
  end
```

Two principles:

- **Overlap.** Adjacent zones overlap around each breaker so there is **no blind
  spot** — every point is covered by at least one zone.
- **Primary vs backup.** The relay closest to the fault is the **primary**
  protection; it should clear first. If it (or its breaker) fails, **backup**
  protection — either *local* (a second relay) or *remote* (the relay one zone
  upstream, after a deliberate time delay) — must clear the fault instead.

Backup is intentionally **slower** and trips **more** of the system. That is the
price of the guarantee that *some* relay always clears the fault. The
**coordination time interval** (typically 0.2–0.4 s) is the margin we leave so
the primary always gets its chance before the backup acts.

**Next:** the devices that physically interrupt the current.
""",
        ),
        _t(
            "Fuses & circuit breakers",
            "10 min",
            """\
# Fuses & circuit breakers

A relay only *decides*; the **interrupting device** actually breaks the current.

## Fuses

A **fuse** is the simplest protection: a metal element that melts and opens when
too much current flows for too long. It is **self-sensing and self-interrupting**
— no relay, no CT — and it follows an inverse **time-current characteristic**:
the larger the current, the faster it melts.

```plot
{"title": "Fuse melting time vs current (inverse characteristic)", "xLabel": "current (multiples of rating)", "yLabel": "melting time (s)", "xRange": [1.1, 10], "yRange": [0, 8], "functions": [{"expr": "6/(x^2 - 1)", "label": "melt time ~ 1/I^2", "color": "#2563eb"}]}
```

Fuses are cheap and fast but **single-use** (one blows and must be replaced) and
they protect **one phase** only — a blown fuse on one phase leaves a motor
single-phasing.

## Circuit breakers

A **circuit breaker (CB)** is a mechanical switch that can interrupt fault
current on command from a relay, and **re-close** afterwards. The arc that forms
when contacts part is quenched by a medium:

- **Vacuum** (medium voltage, most common today),
- **SF₆ gas** (high voltage, excellent insulation),
- older **oil** and **air-blast** designs.

Key ratings are the **interrupting capacity** (the maximum fault current it can
break, e.g. 40 kA) and the **operating time** (e.g. 2–3 cycles). The breaker
clears when the AC current passes through a natural **zero crossing** — the
medium must de-ionise fast enough to withstand the recovering voltage.

Fuse + relay-and-breaker schemes are combined across the grid: fuses on small
laterals, breakers with relays everywhere current and selectivity matter.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Power System Protection & Relaying — Intermediate ────────────────────────

_PP_INTERMEDIATE = SeedCourse(
    slug="power-protection-intermediate",
    title="Power System Protection & Relaying — Intermediate",
    description=(
        "The working toolkit of relaying: inverse-time overcurrent curves, "
        "time and current grading for coordination, directional overcurrent, "
        "differential protection of transformers and busbars, the per-unit "
        "system for short-circuit calculation, and symmetrical components for "
        "unbalanced faults. Interactive coordination plots throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Overcurrent protection & inverse-time curves",
            "12 min",
            """\
# Overcurrent protection & inverse-time curves

The most widespread relay is the **overcurrent relay**: it trips when current
exceeds a **pickup** setting. A plain *definite-time* relay trips after a fixed
delay; far more useful is the **inverse-time** relay, where the trip time **falls
as the current rises** — small overloads are tolerated briefly, big faults are
cleared fast.

The IEC/IEEE standard curves follow

$$t(I) = \\mathrm{TMS}\\cdot\\frac{k}{\\left(I/I_p\\right)^{n} - 1},$$

where $I_p$ is the pickup current, $\\mathrm{TMS}$ is the **time multiplier
setting** (it scales the whole curve up or down), and $(k,n)$ select the curve
shape: **Standard Inverse** ($k{=}0.14,\\,n{=}0.02$), **Very Inverse** ($n{=}1$)
and **Extremely Inverse** ($n{=}2$). The $-1$ in the denominator pushes trip time
to infinity as current approaches pickup. Here is the characteristic shape — note
how the steeper curves clear high faults much faster:

```plot
{"title": "Inverse-time overcurrent curves (trip time vs fault current)", "xLabel": "current (multiples of pickup I/Ip)", "yLabel": "trip time (s)", "xRange": [1.2, 12], "yRange": [0, 8], "functions": [{"expr": "3/(x^1 - 1)", "label": "very inverse (n=1)", "color": "#2563eb"}, {"expr": "5/(x^2 - 1)", "label": "extremely inverse (n=2)", "color": "#dc2626"}]}
```

Raising the **TMS** lifts the whole curve (slower); lowering the pickup shifts it
left (more sensitive). These two knobs are exactly what we turn in the next
lesson to make neighbouring relays **coordinate**.

**Next:** grading those curves so the right relay trips first.
""",
        ),
        _t(
            "Coordination & discrimination",
            "12 min",
            """\
# Coordination & discrimination

When relays in series both see the same downstream fault, only the one
**closest** to the fault should trip — that is **discrimination** (selectivity).
We achieve it by **grading**.

- **Time grading.** Each relay upstream is set with a longer delay than the one
  downstream, separated by a **coordination time interval (CTI)** of about
  **0.3 s**. The downstream relay always operates first; the upstream relay waits
  out the CTI as backup.
- **Current grading.** Because fault current falls with distance, an upstream
  relay can be set to pick up only at the *higher* current of a near fault,
  ignoring the smaller current of a far one.
- **Combined (inverse-time) grading.** Inverse curves naturally give both — at
  high current the downstream relay is much faster, and the curves are stacked a
  CTI apart.

The two curves below are a downstream relay (R1, faster) and its upstream backup
(R2). At every current R2 stays **above** R1 by the coordination margin, so R1
always clears first:

```plot
{"title": "Coordinated relay pair: backup R2 stays a CTI above primary R1", "xLabel": "current (multiples of pickup)", "yLabel": "trip time (s)", "xRange": [1.3, 12], "yRange": [0, 9], "functions": [{"expr": "2/(x^1 - 1)", "label": "R1 primary (downstream)", "color": "#2563eb"}, {"expr": "2/(x^1 - 1) + 0.3 + 2/x", "label": "R2 backup (upstream)", "color": "#dc2626"}]}
```

Coordination studies march from the **furthest-out** relay back toward the
source, stacking each relay a CTI above the last. Too small a margin risks the
backup tripping unnecessarily; too large a margin leaves faults on too long.

**Next:** making overcurrent relays *directional*.
""",
        ),
        _t(
            "Directional overcurrent protection",
            "11 min",
            """\
# Directional overcurrent protection

Plain overcurrent relays only see **magnitude** — they cannot tell *which way*
the fault current flows. On a **ring main** or a line fed from **both ends**,
fault current can arrive from either direction, and a non-directional relay would
trip for faults behind it as well as in front.

A **directional relay** adds a **polarising** reference (a voltage from a VT) and
compares its **phase angle** with the current. If the current leads/lags the
reference within the *forward* window, it trips; current flowing the other way is
**blocked**.

$$\\text{operate if } \\cos\\!\\left(\\theta_I - \\theta_\\text{pol} - \\theta_\\text{MTA}\\right) > 0,$$

where $\\theta_\\text{MTA}$ is the **maximum-torque angle**, chosen to align the
relay's most-sensitive direction with the expected fault-current angle.

```mermaid
flowchart LR
  SA["source A"] --> CBA["CB + dir. relay"]
  CBA --> F(("fault"))
  F --> CBB["CB + dir. relay"]
  CBB --> SB["source B"]
  CBA -. "looks right -> trips" .-> F
  CBB -. "looks left -> trips" .-> F
```

With directionality, two relays guarding a doubly-fed line each trip only for
faults **in front of them**, isolating the line from both ends while leaving the
sources connected. Directional comparison is also the basis of the pilot schemes
in the Advanced course.

**Next:** protection that needs no coordination delay at all — differential.
""",
        ),
        _t(
            "Differential protection",
            "12 min",
            """\
# Differential protection

**Differential protection** is the gold standard for protecting a discrete piece
of equipment — a transformer, a busbar, a generator. The idea is **Kirchhoff's
current law**: in a healthy zone, *what flows in must flow out*, so the sum of the
currents at the boundary is (ideally) zero.

We measure current with a CT at **every** terminal of the zone and compute the
**differential current** $I_d = |\\,I_\\text{in} - I_\\text{out}\\,|$:

- **No internal fault** → $I_d \\approx 0$ (the relay restrains).
- **Internal fault** → current pours in and does not come out → $I_d$ is large →
  trip **instantly**.

```mermaid
flowchart LR
  CT1["CT in"] --> Z["protected zone<br/>(transformer / bus)"]
  Z --> CT2["CT out"]
  CT1 --> D{"I_d = |I_in − I_out|"}
  CT2 --> D
  D -- "I_d ≈ 0" --> REST["restrain (healthy)"]
  D -- "I_d large" --> TRIP["trip (internal fault)"]
```

Because it compares *inside* the zone, differential protection is inherently
**selective** — it cannot see external faults — so it needs **no time grading**
and trips fast. The complications:

- **CT mismatch and saturation** create a spurious $I_d$ on heavy *through*
  faults. The cure is a **percentage (biased) differential** characteristic: the
  trip threshold rises with the through current, so only a *proportionally* large
  $I_d$ trips.
- **Transformers** add **magnetising inrush** (a large one-sided current at
  energisation) and a turns-ratio/phase shift; relays restrain on inrush using
  **2nd-harmonic** content and correct the ratio/phase in software.
- **Busbar** differential sums many feeders and must ride through external faults
  where one CT may saturate.

**Next:** the per-unit system that makes the short-circuit sums tractable.
""",
        ),
        _t(
            "Per-unit system & short-circuit calculation",
            "12 min",
            """\
# Per-unit system & short-circuit calculation

Real networks span many voltage levels through transformers. Working in volts and
ohms means constantly referring impedances across turns ratios. The **per-unit
(pu) system** removes that pain by expressing every quantity as a fraction of a
**base**:

$$\\text{quantity in pu} = \\frac{\\text{actual quantity}}{\\text{base quantity}}.$$

Pick a system-wide **base power** $S_\\text{base}$ (e.g. 100 MVA) and a **base
voltage** per zone (the nominal kV). Then

$$Z_\\text{base} = \\frac{V_\\text{base}^2}{S_\\text{base}}, \\qquad
Z_\\text{pu} = \\frac{Z_\\Omega}{Z_\\text{base}}.$$

The magic: across an ideal transformer the **per-unit impedance is the same** on
both sides, so the whole network collapses into one impedance diagram with no
turns ratios. A symmetrical (three-phase) short circuit is then just

$$I_\\text{fault,pu} = \\frac{V_\\text{pu}}{Z_\\text{th,pu}} \\;\\approx\\; \\frac{1}{Z_\\text{th,pu}},$$

with $Z_\\text{th}$ the Thévenin impedance looking into the fault point. The
**fault level** (MVA) is $S_\\text{base}/Z_\\text{th,pu}$. Fault current falls as
the path impedance to the fault grows:

```plot
{"title": "Per-unit fault current vs source-to-fault impedance", "xLabel": "Thevenin impedance to fault (pu)", "yLabel": "fault current (pu, on 1.0 pu source)", "xRange": [0.05, 1], "yRange": [0, 22], "functions": [{"expr": "1/x", "label": "I_fault = 1 / Z_th", "color": "#2563eb"}], "points": [{"x": 0.1, "y": 10, "label": "stiff bus: low Z, high I", "color": "#dc2626", "size": 6}]}
```

Convert the base when combining equipment rated on different MVA bases
($Z_\\text{new} = Z_\\text{old}\\,(S_\\text{new}/S_\\text{old})$), add up the series
and parallel impedances, and the fault current at any bus drops out directly. This
fault level is what sets relay pickups and breaker ratings.

**Next:** handling the unbalanced faults that pu alone cannot.
""",
        ),
        _t(
            "Symmetrical components for unbalanced faults",
            "12 min",
            """\
# Symmetrical components for unbalanced faults

A balanced three-phase fault can be solved on one phase. But LG, LL and LLG
faults are **unbalanced** — the phases are no longer symmetric, and a single-phase
model breaks down. **Symmetrical components** (Fortescue) rescue us by splitting
*any* set of three unbalanced phasors into three **balanced** sets:

- **Positive sequence** (1) — balanced, normal a-b-c rotation (what flows in
  healthy operation).
- **Negative sequence** (2) — balanced, *reversed* rotation (appears under
  unbalance; overheats machines).
- **Zero sequence** (0) — three in-phase phasors (the path through **ground** /
  neutral).

Each sequence has its own network with its own impedance $Z_1, Z_2, Z_0$. The
beauty is that the three sequence networks are **decoupled**, and a given fault
type simply **connects them** in a fixed pattern:

- **3φ:** positive only → $I = \\dfrac{V}{Z_1}$.
- **LG:** the three networks in **series** → $I = \\dfrac{3V}{Z_1 + Z_2 + Z_0}$.
- **LL:** positive and negative in series → $I = \\dfrac{\\sqrt3\\,V}{Z_1 + Z_2}$.

```mermaid
flowchart TB
  V["pre-fault voltage source"]
  V --> Z1["positive-seq Z1"]
  Z1 --> Z2["negative-seq Z2"]
  Z2 --> Z0["zero-seq Z0"]
  Z0 --> G["ground (LG fault: series connection)"]
```

The **zero-sequence** path exists only when there is a connection to ground, which
is exactly why ground faults are detected by summing the three phase currents
(the **residual** $3I_0$) — the basis of **earth-fault relays**. Negative-sequence
relays likewise catch unbalance that phase-overcurrent relays miss. Symmetrical
components are the analytical engine behind every distance and ground relay in the
Advanced course.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Power System Protection & Relaying — Advanced ────────────────────────────

_PP_ADVANCED = SeedCourse(
    slug="power-protection-advanced",
    title="Power System Protection & Relaying — Advanced",
    description=(
        "Transmission-grade and modern protection: distance (impedance) relays and "
        "their zones, teleprotection and pilot schemes, generator/motor/transformer "
        "protection, numerical relays and IEC 61850, the challenges that "
        "inverter-based renewables pose, and a worked relay-coordination case study. "
        "Interactive reach and coordination plots throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Distance (impedance) protection & zones",
            "12 min",
            """\
# Distance (impedance) protection & zones

On transmission lines, overcurrent grading becomes impractical — fault levels vary
with system conditions. **Distance protection** instead measures the **impedance**
from the relay to the fault: $Z = V/I$ at the relay. Because line impedance is
roughly proportional to **length**, impedance is a proxy for *distance to fault*,
and it barely depends on the source strength.

The relay trips if the measured $Z$ falls **inside** a region of the
resistance–reactance (R–X) plane (a *mho* or *quadrilateral* characteristic).
Protection is staged in **zones** of increasing reach and delay:

- **Zone 1** — ~**80–90%** of the line, **instantaneous**. Stops short of the
  remote bus so it never overreaches into the next line.
- **Zone 2** — ~**120–150%** (whole line + into the next), **delayed** (~0.3–0.5 s);
  backup for the far end.
- **Zone 3** — reaches into the adjacent line(s), longer delay; remote backup.

```mermaid
flowchart LR
  R["distance relay"] --- BUS1["local bus"]
  BUS1 --- L1["protected line"]
  L1 --- BUS2["remote bus"]
  BUS2 --- L2["next line"]
  R -. "Zone 1: 80% — instant" .-> L1
  R -. "Zone 2: 120% — delayed" .-> BUS2
  R -. "Zone 3: into next line — backup" .-> L2
```

The stepped reach-vs-time picture is the heart of distance protection — closer
faults clear instantly, faults beyond the protected line are backed up after a
delay:

```plot
{"title": "Distance protection: trip time vs fault location (stepped zones)", "xLabel": "fault distance (% of protected line)", "yLabel": "trip time (s)", "xRange": [0, 200], "yRange": [0, 1.4], "functions": [{"expr": "0.02 + 0*x", "label": "Zone 1 reach (to 80%)", "color": "#2563eb"}, {"expr": "0.4 + 0*x", "label": "Zone 2 delay", "color": "#16a34a"}, {"expr": "1.0 + 0*x", "label": "Zone 3 delay", "color": "#dc2626"}], "points": [{"x": 80, "y": 0.02, "label": "Zone 1 ends at ~80%", "color": "#2563eb", "size": 6}, {"x": 150, "y": 0.4, "label": "Zone 2 ends at ~150%", "color": "#16a34a", "size": 6}]}
```

Distance relays must cope with **fault resistance**, **load encroachment** (heavy
load looks like a low impedance) and **power swings**, all handled by the shape of
the characteristic and supervisory logic.

**Next:** making the far end clear instantly too — pilot schemes.
""",
        ),
        _t(
            "Teleprotection & pilot schemes",
            "11 min",
            """\
# Teleprotection & pilot schemes

Zone 1 only covers ~80% of a line, so a fault in the last 20% is cleared
**instantly at one end** but only after a **Zone 2 delay at the other**. For
critical lines that is too slow. **Pilot (teleprotection) schemes** add a
**communication channel** between the two line ends so *both* breakers trip
**high-speed** for *any* in-line fault.

Two families:

- **Permissive schemes** — a relay sends a "permit to trip" signal when it sees a
  forward fault. **PUTT** (permissive underreach) keys on a Zone-1 pickup; **POTT**
  (permissive overreach) keys on a Zone-2 (overreaching) pickup. The remote end
  trips fast only if it *also* sees a forward fault **and** receives the permit.
- **Blocking schemes** — a relay sends a **block** signal when it sees a
  *reverse* (external) fault, restraining the remote end; absence of a block lets
  it trip.

```mermaid
flowchart LR
  RA["relay A (forward pickup)"] -- "permit / block signal" --> CH(("comm channel"))
  CH -- "signal" --> RB["relay B (forward pickup)"]
  RA --- LINE["protected line"]
  RB --- LINE
  RA -- "trip A fast" --> LINE
  RB -- "trip B fast" --> LINE
```

Channels range from **fibre** (today's choice — fast, immune to the fault),
**power-line carrier**, microwave, to direct copper pilot wires. **Line current
differential** is the modern extreme: each end shares its *current samples* over
fibre so the relays compute a true differential of the whole line — selective,
fast and reach-independent. Channel **delay, security and dependability** trade
off: a blocking scheme is secure if the channel fails open; a permissive scheme is
dependable if it fails closed.

**Next:** protecting the rotating and static plant.
""",
        ),
        _t(
            "Generator, motor & transformer protection",
            "12 min",
            """\
# Generator, motor & transformer protection

Big plant items each have a tailored protection package, far richer than line
overcurrent.

## Generators

A generator is a source *and* an expensive machine, so it is heavily protected:

- **Differential (87G)** — fast clearing of internal stator faults.
- **Stator earth-fault** — 95–100% coverage using neutral and third-harmonic
  measurements.
- **Loss-of-field (40)** — excitation lost → it absorbs reactive power and can
  lose synchronism.
- **Reverse power (32)** — it motors when the prime mover fails.
- **Negative-sequence (46)** — unbalance overheats the rotor; limited by an
  $I_2^2 t$ withstand.
- **Over/under-frequency, over-excitation (V/Hz, 24)**.

## Motors

- **Thermal overload** (an $I^2t$ model of winding heating),
- **Locked rotor / stall**, **unbalance / single-phasing** (negative sequence),
- **Undervoltage** and **too-frequent starts**.

## Transformers

- **Percentage differential (87T)** with **2nd-harmonic** inrush restraint and
  **5th-harmonic** over-excitation restraint, plus ratio/phase compensation.
- **Restricted earth fault (REF)** for sensitive ground-fault coverage.
- **Buchholz / gas relay** — mechanical, senses gas from internal arcing in
  oil-filled units.
- **Overcurrent backup** and **winding/oil temperature**.

```mermaid
flowchart TB
  GEN["generator"] --> P87["87G differential"]
  GEN --> P40["40 loss-of-field"]
  GEN --> P46["46 negative-seq"]
  GEN --> P32["32 reverse power"]
  TX["transformer"] --> T87["87T differential + 2nd harmonic"]
  TX --> REF["restricted earth fault"]
  TX --> BUCH["Buchholz gas relay"]
```

These functions historically meant a rack of devices; in a numerical relay they
are all software elements sharing the same CT/VT inputs — the subject of the next
lesson.

**Next:** numerical relays and the IEC 61850 substation.
""",
        ),
        _t(
            "Numerical/digital relays & IEC 61850",
            "11 min",
            """\
# Numerical/digital relays & IEC 61850

Protection has passed through three eras: **electromechanical** (induction discs,
1900s–), **static/solid-state** (analogue electronics, 1960s–), and today's
**numerical (digital) relays** — microprocessor devices that **sample** the CT/VT
waveforms, run a DSP/phasor estimator, and execute the protection logic in
**software**.

What numerical relays add:

- **Multi-function** — one device runs distance, overcurrent, differential, etc.,
  selected by setting.
- **Self-monitoring** — they detect their own failures and alarm.
- **Disturbance recording / event logs** for post-fault analysis.
- **Communications** — they report and can be coordinated over a network.
- **Adaptive settings** that follow the system state.

**IEC 61850** is the standard that turns a substation into a network. Instead of
copper wiring per signal, devices (**IEDs**) exchange standardised messages over
Ethernet:

- **GOOSE** — fast, multicast status/trip messages between IEDs (e.g. a breaker-
  fail or interlock signal in milliseconds), replacing hard-wired trip contacts.
- **Sampled Values (SV)** — digitised CT/VT samples streamed from a **merging
  unit** in the yard, so relays no longer need analogue CT wiring (the *process
  bus*).
- A standard **data model** (logical nodes like `PTOC`, `PDIS`, `XCBR`) and **SCL**
  configuration files make IEDs from different vendors interoperate.

```mermaid
flowchart TB
  CTVT["CT / VT in yard"] --> MU["merging unit"]
  MU -- "Sampled Values (process bus)" --> IED1["protection IED"]
  IED1 -- "GOOSE trip / interlock (station bus)" --> IED2["bay controller / other IED"]
  IED1 --> CB["circuit breaker (XCBR)"]
  IED1 --> SCADA["station SCADA / engineering"]
```

The benefits — less copper, testability, interoperability — come with new
concerns: **time synchronisation** (PTP/IEEE 1588 for SV), **network determinism**
and **cyber-security**.

**Next:** what happens when the sources are inverters, not machines.
""",
        ),
        _t(
            "Protection with inverter-based renewables",
            "11 min",
            """\
# Protection with inverter-based renewables

Classic protection assumes **synchronous machines**: a fault draws a large,
predictable, mostly-inductive fault current (3–6× rated) that decays slowly.
**Inverter-based resources (IBRs)** — solar, wind, batteries connected through
power electronics — break almost every one of those assumptions.

- **Current-limited.** An inverter protects its semiconductors by capping fault
  current near **1.1–1.5× rated** — nowhere near the kiloamps an overcurrent or
  distance relay expects. Relays set for machine fault levels may **fail to
  pick up**.
- **Controlled, not physical, response.** The fault "current" is whatever the
  control software injects (often controlled to a target angle/sequence). It can
  even inject little/no **negative-sequence** current, blinding negative-sequence
  and some directional elements.
- **Low inertia / weak grid.** Fewer spinning machines means **less inertia** and
  lower fault levels, so frequency moves faster (high **RoCoF**) and **voltage**
  is softer — distance relays see distorted impedance.
- **Variable and intermittent** infeed changes fault levels with the weather and
  state of charge.

```plot
{"title": "Fault-current infeed: synchronous machine vs inverter (IBR)", "xLabel": "time (cycles)", "yLabel": "current (multiples of rated)", "xRange": [0, 12], "yRange": [0, 6.5], "functions": [{"expr": "1 + 5*exp(-x/3.5)", "label": "synchronous machine (high, decaying)", "color": "#2563eb"}, {"expr": "1.2 + 0*x", "label": "inverter (current-limited ~1.2x)", "color": "#dc2626"}]}
```

Mitigations being adopted: **grid codes** requiring **fault ride-through** and
defined **reactive/negative-sequence current injection**; protection that leans on
**differential** (magnitude-independent), **directional/undervoltage** and
**travelling-wave** principles; and **adaptive, communication-assisted** schemes
that no longer trust raw fault-current magnitude. Protecting an inverter-dominated
grid is one of the field's active frontiers.

**Next:** put it together in a coordination case study.
""",
        ),
        _t(
            "Relay-coordination case study",
            "12 min",
            """\
# Relay-coordination case study

Let's coordinate a small radial feeder, source → **R3** → **R2** → **R1** → load,
with a fault possible just past R1. All three are inverse-time overcurrent relays;
**R1** is the primary, **R2** backs up R1, **R3** backs up R2.

## Step 1 — fault levels (per-unit)

On a 100 MVA base, the Thévenin impedance to each bus gives the fault current
(from the Intermediate course, $I \\approx 1/Z_\\text{th}$). Suppose:

| Fault at | $Z_\\text{th}$ (pu) | $I_\\text{fault}$ (pu) |
|----------|--------------------|------------------------|
| past R1  | 0.20               | 5.0                    |
| past R2  | 0.13               | 7.7                    |
| past R3  | 0.10               | 10.0                   |

## Step 2 — pickups

Set each pickup above its **maximum load** but below the **minimum fault** it must
see. R1 lowest, R3 highest (nearer the stiff source).

## Step 3 — grade from the far end inward

Start at **R1** with the fastest acceptable TMS, then lift **R2** so it trips one
**CTI ≈ 0.3 s** *slower* than R1 at the R1-fault current, and **R3** another CTI
above R2. The three curves stack a margin apart:

```plot
{"title": "Case study: three coordinated relays, each a CTI apart", "xLabel": "current (multiples of pickup)", "yLabel": "trip time (s)", "xRange": [1.3, 12], "yRange": [0, 10], "functions": [{"expr": "1.6/(x^1 - 1)", "label": "R1 primary", "color": "#16a34a"}, {"expr": "1.6/(x^1 - 1) + 0.3 + 1.6/x", "label": "R2 backup", "color": "#2563eb"}, {"expr": "1.6/(x^1 - 1) + 0.6 + 3.2/x", "label": "R3 backup", "color": "#dc2626"}]}
```

## Step 4 — verify

Check the margin at **every** common fault current, not just one point — CT
saturation and curve crossover can erode the CTI at high currents. Confirm the
furthest relay still clears within the equipment's **damage curve** and the
breaker **interrupting rating** covers the highest fault level.

```mermaid
flowchart LR
  SRC["source"] --> R3["R3 (slowest, backup)"]
  R3 --> R2["R2 (backup)"]
  R2 --> R1["R1 (primary, fastest)"]
  R1 --> F(("fault / load"))
  R1 -. "clears first" .-> F
  R2 -. "+1 CTI" .-> F
  R3 -. "+2 CTI" .-> F
```

The same march-from-the-end logic scales to meshed networks (with directional and
distance relays) — but the principle never changes: **the relay nearest the fault
trips first; every other relay waits its coordination margin as backup.**

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


POWER_PROTECTION_COURSES: tuple[SeedCourse, ...] = (
    _PP_BASICS,
    _PP_INTERMEDIATE,
    _PP_ADVANCED,
)

__all__ = ["POWER_PROTECTION_COURSES"]
