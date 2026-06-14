"""Academy seed content — the EMC / EMI track (Beginner → Advanced).

* ``emc-basics``        — emissions vs immunity, dB units, coupling paths, grounding, shielding, standards
* ``emc-intermediate``  — radiated/conducted emissions, filtering, shielding detail, ESD
* ``emc-advanced``      — EMC by design, spread spectrum, cables/chokes, pre-compliance debugging

Runnable ``code`` lessons use numpy + builtins to convert dB/EMC units, estimate
shielding effectiveness, model a current-loop's radiated field, compute LC filter
attenuation, show spread-spectrum peak reduction, and track an emissions margin
budget. Part of the Electronic Engineering curriculum.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, µ, Ω, ², ×) in diagrams and labels.
# ruff: noqa: RUF001, RUF003

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


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# emc-basics
# ──────────────────────────────────────────────────────────────────────

_EMC_BASICS = SeedCourse(
    slug="emc-basics",
    title="EMC / EMI — Basics",
    description=(
        "Electromagnetic compatibility from the ground up: emissions vs immunity, "
        "the decibel units EMC engineers live in, how interference couples "
        "(source–path–victim), grounding and return current, shielding, and the "
        "regulatory standards. With runnable dB-unit and shielding labs."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is EMC?",
            "10 min",
            r"""# What is EMC?

**Electromagnetic Compatibility (EMC)** is a device's ability to **work correctly
in its electromagnetic environment** without itself being a source of intolerable
interference to others. Every switching circuit both **radiates** electromagnetic
energy and is **susceptible** to it, so EMC is the discipline of keeping electronics
electromagnetically "polite" and "robust" at once.

It splits into two halves — and you must engineer both:

- **Emissions** — the interference your device **produces** (and must keep below
  legal limits). Conversely, the source side.
- **Immunity / Susceptibility** — your device's ability to **withstand**
  interference from outside without malfunctioning. The victim side.

Each of those has two coupling categories:

```
              Emissions            Immunity
Conducted   noise OUT on cables   noise IN on cables/power
Radiated    fields OUT through    fields IN through the
            air/space             air/space
```

**Why it's not optional:**

- **It's the law.** You **cannot legally sell** most electronics without passing
  EMC: **FCC** (USA), the **CE/EMC Directive** (Europe), and equivalents worldwide.
  Failing EMC late is a classic, expensive product-launch killer.
- **It's about function.** Interference causes real failures: a switching regulator
  corrupting a sensor reading, a motor drive resetting a microcontroller, a phone
  buzzing in a speaker, a medical device misbehaving near a transmitter.
- **EMI ≠ EMC.** **EMI** (ElectroMagnetic Interference) is the *problem* — the
  unwanted energy. **EMC** is the *goal* — coexisting compatibly. EMC engineering
  manages EMI.

The unifying model for everything in this track is **source → coupling path →
victim**: interference needs all three. You fix an EMC problem by attacking any one
— **reduce the source** (slow edges, spread spectrum), **break the path** (shield,
filter, separate, ground properly), or **harden the victim** (filtering, immunity
design). EMC is often called a "black art," but it's really disciplined application
of a few physical principles — return current, dB budgets, loops as antennas — that
this track makes concrete. And designing for it **early** is vastly cheaper than
chasing failures in the test chamber.
""",
        ),
        _t(
            "Decibels & EMC units",
            "11 min",
            r"""# Decibels & EMC units

EMC engineers live in **decibels** and **dB-referenced units**, because emissions
span an enormous dynamic range and limits/measurements are specified that way.
Getting fluent in these units is step one.

**The decibel** is a **logarithmic ratio**. For power and for field/voltage
quantities respectively:

$$ \text{dB} = 10\log_{10}\frac{P_1}{P_2} = 20\log_{10}\frac{V_1}{V_2} $$

(The 20 vs 10 is because power ∝ voltage².) Logs turn the huge ranges into
manageable numbers and turn **multiplication into addition** — gains and losses
along a path simply **add** in dB.

**dB-referenced absolute units** (the EMC staples) fix a reference so an absolute
quantity becomes a single dB number:

- **dBµV** — voltage relative to 1 microvolt: `dBµV = 20·log10(V / 1µV)`. So
  1 mV = 60 dBµV, 1 V = 120 dBµV.
- **dBµV/m** — electric **field strength** relative to 1 µV/m (radiated-emission
  limits are in dBµV/m at a measured distance, e.g. 3 m or 10 m).
- **dBµA** — current relative to 1 µA. **dBm** — power relative to 1 mW.

**Why this is so convenient in EMC:**

- **Limits and measurements compare by subtraction.** Margin = limit − measured
  (in dB). A reading **6 dB under** the limit means **half** the allowed field;
  EMC sign-off targets a comfortable margin (often ≥ 6 dB).
- **Path effects add.** Source level − shielding (dB) − filter attenuation (dB) +
  antenna factor … all just add up.
- **Useful anchors:** **6 dB ≈ ×2** (voltage/field), **20 dB = ×10**,
  **−3 dB = half power**.

A subtlety unique to EMC: **detectors**. The same signal reads differently under a
**peak**, **quasi-peak (QP)**, or **average** detector — QP weights by repetition
rate to model how annoying interference is to radio reception, and most CISPR
limits are **quasi-peak**. So a measurement is "X dBµV/m, quasi-peak."

The practical upshot: comfortable EMC reasoning means **thinking in dB** — adding
path losses, reading margins by subtraction, and converting between µV and dBµV
without a second thought. You'll build that muscle in the next lab.
""",
        ),
        _code(
            "dB & EMC unit calculator",
            "12 min",
            r"""# EMC works in decibels: limits in dBuV/m, attenuations in dB, margins by
# subtraction. Build the conversions and a simple emissions margin check.
# Uses numpy for log10 (the math module is unavailable).

import numpy as np

def dbuv_to_v(dbuv):
    return 1e-6 * (10.0 ** (dbuv / 20.0))            # no numpy -> safe inside a function

# Conversions (log10 done at module level; numpy isn't visible inside functions)
for v in [1e-6, 1e-3, 0.1, 1.0]:
    dbuv = 20.0 * float(np.log10(v / 1e-6))          # ref = 1 microvolt
    print("%g V = %.1f dBuV" % (v, dbuv))
print("60 dBuV =", round(dbuv_to_v(60.0) * 1e3, 3), "mV")
print()

# dB anchors
print("a voltage ratio of 2x is %.2f dB; 10x is %.1f dB" % (20 * float(np.log10(2)), 20 * float(np.log10(10))))
print()

# Emissions margin: measured field vs a limit, after some shielding+filter.
source_dbuv_m = 58.0     # raw radiated field at 3 m (dBuV/m)
shield_db = 12.0         # shielding effectiveness
filter_db = 8.0          # filter attenuation on the offending harmonic
limit_dbuv_m = 40.0      # e.g. CISPR class B limit at this frequency

emitted = source_dbuv_m - shield_db - filter_db    # path effects ADD (subtract dB)
margin = limit_dbuv_m - emitted
print("raw source: %.0f dBuV/m" % source_dbuv_m)
print("after shielding (%.0f dB) + filter (%.0f dB): %.0f dBuV/m" % (shield_db, filter_db, emitted))
print("limit: %.0f dBuV/m -> margin: %+.0f dB %s" % (limit_dbuv_m, margin, "PASS" if margin >= 6 else "TIGHT/FAIL"))
print("EMC sign-off usually wants >= 6 dB margin (a factor of 2 in field).")
""",
        ),
        _t(
            "Sources & coupling paths",
            "11 min",
            r"""# Sources & coupling paths

Every EMC problem is a chain: **source → coupling path → victim**. Remove or weaken
**any link** and the interference goes away. Diagnosing EMC is largely identifying
which is which.

**Sources** of EMI are anything with **fast-changing voltage or current** (high
**dV/dt** or **dI/dt**):

- **Switching regulators / SMPS** — sharp switching edges, a top offender.
- **Clocks & digital edges** — produce energy at the clock frequency **and its
  harmonics** (a 100 MHz clock radiates at 100, 200, 300 MHz …). Fast edges spread
  energy to high harmonics (the rise-time/bandwidth link from the SI track).
- **Motors, relays, ignition, ESD** — broadband impulsive noise.

**Coupling paths** — how energy gets from source to victim — come in four flavours:

- **Conducted** — noise travels along **wires** (power, signal, ground). Dominant
  below ~30 MHz.
- **Radiated** — energy crosses **space** as electromagnetic fields. Dominant above
  ~30 MHz. (The ~30 MHz crossover is roughly where wavelengths shrink enough that
  structures radiate efficiently.)
- **Capacitive (electric-field) coupling** — through **dV/dt** between conductors
  at different potentials (a high-impedance, voltage-driven mechanism).
- **Inductive (magnetic-field) coupling** — through **dI/dt** between current
  loops (a low-impedance, current-driven mechanism). Same physics as crosstalk.

A distinction that runs through all EMC: **differential mode vs common mode**:

- **Differential-mode** noise flows **out one conductor and back the other**
  (the intended loop). Filtered with series/line elements.
- **Common-mode** noise flows the **same direction on all conductors**, returning
  through ground/earth/parasitics. It's the **main radiated-emissions culprit**
  (especially on cables, which act as antennas) and the hardest to control —
  tackled with **common-mode chokes** and good grounding.

The strategy follows the chain directly:

```
attack the SOURCE:  slow edges, spread spectrum, snubbers
break the PATH:     shield (radiated), filter (conducted), separate, twist/route
harden the VICTIM:  input filtering, immunity design, robust thresholds
```

Knowing **which mechanism** (conducted vs radiated, common vs differential,
electric vs magnetic) is dominant tells you which fix will work — applying a
shield to a conducted problem, or a line filter to a radiated one, wastes effort.
This source-path-victim discipline is the backbone of EMC troubleshooting.
""",
        ),
        _t(
            "Grounding & return current",
            "11 min",
            r"""# Grounding & return current

More EMC problems trace to **grounding and return current** than to anything else,
and the single most important idea in the whole field is this: **current flows in
loops.** Every signal or power current that goes *out* must return; **where it
returns, and how big the loop is, determines emissions, susceptibility, and
crosstalk.**

**"Ground" is a misleading word.** It is **not** a magic sink at 0 V everywhere —
it's just a conductor carrying **return current**, with real impedance. At high
frequency, return current doesn't take the path of least *resistance*; it takes the
path of least **inductance**, which is **directly under the signal trace** (the
smallest loop). This gives the cardinal rules:

- **Provide a continuous return path** directly adjacent to every signal (a solid
  reference plane). Break it — a **split plane**, a slot, a connector gap — and the
  return current must **detour**, creating a **large loop** that radiates (emits)
  and picks up noise (susceptibility). This is the #1 cause of both emission and
  immunity failures.
- **Minimise loop area.** Radiated emission from a loop scales with its **area** (and
  with frequency² and current). Tight signal-return loops radiate far less and are
  far less susceptible. Twisted pairs and adjacent power/ground planes shrink loops.

**Grounding topologies** — chosen by frequency:

- **Single-point ground** — everything returns to one node; avoids **ground loops**.
  Best at **low frequency** (audio, precision analog).
- **Multi-point ground** — many short connections to a ground plane; lowest
  inductance. Best at **high frequency** (digital, RF).
- **Hybrid** — single-point for low-frequency, multi-point (via caps) for high.

**Ground loops** — when two points connect to ground by **different paths**, the
loop can pick up magnetic fields and develop a voltage between "grounds," injecting
noise. Cures: single-point grounding, breaking the loop (isolation transformers,
opto/digital isolators), or common-mode chokes.

The mental upgrade for the rest of EMC (and SI/PI): **stop thinking "this connects
to ground" and start thinking "where does this current return, and how big is the
loop?"** Control the return paths and loop areas and most EMC problems never appear
— which is why grounding/return-path design is the foundation that shielding and
filtering merely *supplement*.
""",
        ),
        _code(
            "Shielding effectiveness",
            "12 min",
            r"""# A shield blocks fields by REFLECTING and ABSORBING them. Shielding
# effectiveness SE(dB) = R (reflection) + A (absorption). Absorption grows with
# thickness/frequency; reflection is huge for E-fields, weak for low-freq
# H-fields. Estimate SE vs frequency for a copper shield. Uses numpy.

import numpy as np

# Copper, simplified engineering model (relative to copper reference).
thickness_mm = 0.5

print("copper shield, %.2f mm thick" % thickness_mm)
print("freq(MHz)   skin_depth(um)   A(absorption dB)   R(reflection dB)   SE(dB)")
for f_mhz in [0.1, 1.0, 10.0, 100.0, 1000.0]:
    f = f_mhz * 1e6
    # Skin depth of copper ~ 66/sqrt(f) mm  (f in Hz) -> in um:
    skin_um = (66.0 / float(np.sqrt(f))) * 1000.0
    # Absorption loss A ~ 8.69 * thickness / skin_depth (dB).
    a_db = 8.69 * (thickness_mm * 1000.0) / skin_um
    # Reflection loss for a plane wave (E-field) rises as freq falls; toy model:
    r_db = 168.0 - 10.0 * float(np.log10(f_mhz)) - 10.0   # decreases ~ with log(f)
    if r_db < 0:
        r_db = 0.0
    se = a_db + r_db
    print("  %-8g   %-14.2f   %-16.2f   %-16.1f   %.1f" % (f_mhz, skin_um, a_db, r_db, se))

print()
print("Absorption dominates at HIGH frequency (thin skin depth); a continuous,")
print("thick conductor with few apertures shields best. Holes/seams ruin it (next course).")
""",
        ),
        _t(
            "Standards & testing",
            "10 min",
            r"""# Standards & testing

EMC is **certified against standards**, and you can't ship without it — so knowing
the landscape and how tests are run shapes how you design.

**The major regulatory regimes:**

- **FCC Part 15** (USA) — **Class A** (industrial/commercial) and the stricter
  **Class B** (residential — tighter limits because consumer gear sits next to TVs
  and radios).
- **CE / EMC Directive** (Europe) — conformity via **harmonised standards** (the
  **CISPR** / EN family). CISPR 32 (multimedia emissions), CISPR 35 (immunity),
  CISPR 11 (industrial/medical), CISPR 25 (automotive).
- **Sector-specific:** automotive (CISPR 25, OEM specs), medical (IEC 60601-1-2),
  military (**MIL-STD-461**), aerospace (DO-160) — generally far stricter.

**What gets tested — emissions:**

- **Radiated emissions** — measured in a **(semi-)anechoic chamber** or **OATS**
  (open-area test site) with a calibrated **antenna** at a set distance (3 m or
  10 m); the EUT sits on a turntable rotated for the worst-case angle, antenna
  height scanned, both polarisations. Result in **dBµV/m vs frequency** against the
  class limit line.
- **Conducted emissions** — measured on the **power leads** via a **LISN** (Line
  Impedance Stabilisation Network), which presents a defined impedance and taps the
  noise; result in **dBµV** (typically 150 kHz–30 MHz).

**What gets tested — immunity:** **radiated immunity** (blast the EUT with fields
from an antenna), **ESD** (zap it per IEC 61000-4-2), **EFT/burst**, **surge**,
**conducted immunity**, **dips/interruptions** — the EUT must keep functioning (or
recover) to a defined performance criterion.

**Detectors & the limit line** — emissions are usually evaluated with the
**quasi-peak** detector against the published limit; **peak** is a faster pre-scan
(if peak passes, you're safe). The measured spectrum is overlaid on the **limit
line** and every peak must sit below it (with margin).

The practical workflow: **pre-compliance** testing in-house (near-field probes, a
spectrum analyzer + LISN, a small chamber) to catch problems early and cheaply,
then a **full compliance** run at an **accredited lab** for certification. Knowing
**which standard, class, and limits** apply to your product from day one lets you
budget margins and design-in fixes — instead of discovering a 15 dB overshoot the
week before launch.
""",
        ),
        quiz_lesson(
            "Quiz: EMC Foundations",
            (
                q(
                    "What are the two halves of EMC?",
                    (
                        opt(
                            "Emissions (interference you produce) and immunity/susceptibility (withstanding interference)",
                            correct=True,
                        ),
                        opt("Voltage and current"),
                        opt("Analog and digital"),
                        opt("AC and DC"),
                    ),
                    "EMC = being electromagnetically polite (emissions under limits) AND robust (immune), each in conducted and radiated forms.",
                ),
                q(
                    "1 mV expressed in dBµV is…",
                    (
                        opt("60 dBµV (20·log10(1mV/1µV) = 20·log10(1000))", correct=True),
                        opt("3 dBµV"),
                        opt("120 dBµV"),
                        opt("1000 dBµV"),
                    ),
                    "dBµV = 20·log10(V/1µV); 1mV/1µV = 1000, and 20·log10(1000) = 60 dBµV. Path effects then add/subtract in dB.",
                ),
                q(
                    "What are the three links every EMC problem requires?",
                    (
                        opt(
                            "Source, coupling path, and victim — break any one to fix it",
                            correct=True,
                        ),
                        opt("Resistor, capacitor, inductor"),
                        opt("Power, ground, signal"),
                        opt("Peak, average, quasi-peak"),
                    ),
                    "Interference needs a source, a path (conducted/radiated, common/differential), and a victim; reduce the source, break the path, or harden the victim.",
                ),
                q(
                    "At high frequency, where does a signal's return current actually flow?",
                    (
                        opt(
                            "Along the path of least inductance — directly under the signal trace in the reference plane",
                            correct=True,
                        ),
                        opt("Through the path of least DC resistance, anywhere on the plane"),
                        opt("It does not return"),
                        opt("Only through the power supply"),
                    ),
                    "HF return current hugs the trace to minimise loop inductance/area; breaking that path (split plane) creates a large radiating/susceptible loop.",
                ),
                q(
                    "Which noise mode is the main culprit for radiated emissions, especially on cables?",
                    (
                        opt(
                            "Common-mode — current flowing the same direction on all conductors, returning through ground/parasitics",
                            correct=True,
                        ),
                        opt("Differential-mode only"),
                        opt("DC current"),
                        opt("There is no difference"),
                    ),
                    "Common-mode currents turn cables into antennas; they're hardest to control and usually dominate radiated emissions (cured with CM chokes/grounding).",
                ),
                q(
                    "What does a LISN do in conducted-emissions testing?",
                    (
                        opt(
                            "Presents a defined, stable impedance on the power leads and taps off the noise for measurement",
                            correct=True,
                        ),
                        opt("Radiates a test field"),
                        opt("Measures temperature"),
                        opt("Generates the clock"),
                    ),
                    "The Line Impedance Stabilisation Network standardises the supply impedance and couples conducted noise (≈150kHz–30MHz) to the analyzer in dBµV.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# emc-intermediate
# ──────────────────────────────────────────────────────────────────────

_EMC_INTERMEDIATE = SeedCourse(
    slug="emc-intermediate",
    title="EMC / EMI — Intermediate",
    description=(
        "Controlling emissions and surviving disturbances: how PCBs radiate "
        "(loops, harmonics), conducted-emissions filtering, shielding with real "
        "apertures, grounding/partitioning, and ESD protection. With runnable "
        "loop-emission and LC-filter labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "How PCBs radiate",
            "11 min",
            r"""# How PCBs radiate

To pass radiated emissions you must understand **how a circuit board becomes an
antenna**. The energy comes from the **fast-changing currents** in your design, and
two unintended antennas dominate.

**1. Loops radiate (magnetic / differential-mode emission).** Any current loop is a
small **loop antenna**. The radiated field from a small loop scales as:

```
E  ∝  f² · A · I        (frequency², loop area, current)
```

The brutal **f²** means **high-frequency harmonics radiate far more efficiently**
than the fundamental — so a clock's 5th/7th harmonic often fails even though the
fundamental is fine. The fixes follow the formula: **shrink loop area** (tight
signal-return loops, adjacent reference plane) and **reduce high-frequency current**
(slower edges, series resistors, decoupling so transient current loops stay local).

**2. Cables radiate (common-mode / "dipole" emission).** A cable driven by
**common-mode voltage** acts as a **dipole/monopole antenna** — and because cables
are long (tens of cm), they radiate efficiently at surprisingly low frequencies and
usually dominate radiated emissions above ~30 MHz. Even a tiny common-mode voltage
(millivolts) on a cable can blow the limit. Cures: **common-mode chokes**, filtering
at the connector, shielded cables bonded 360° to the chassis, and — at the root —
**not generating common-mode voltage** (good return paths, no ground noise driving
the cable).

**Clock harmonics — the usual suspects.** A clock (or any periodic digital signal)
produces a **comb** of emission spikes at the fundamental and its harmonics; a
square wave's harmonics roll off, but fast edges keep them strong far up the
spectrum (rise-time/bandwidth again). On an emissions scan you literally see the
clock's harmonic comb, and the failing peaks are almost always **clock harmonics**
or **SMPS switching harmonics**.

The diagnostic mindset: a radiated-emissions failure is asking **"what current, in
what loop or cable, is radiating at this frequency?"** Trace the failing frequency
back to a clock/switcher harmonic, find the **loop** (area) or **cable**
(common-mode) carrying it, and attack the area or the common-mode current. You'll
estimate a loop's emission against a limit next.
""",
        ),
        _code(
            "Estimate radiated emission from a loop",
            "12 min",
            r"""# A current loop is a small antenna; its radiated E-field grows with frequency^2,
# loop area, and current. Estimate the field at 3 m for clock harmonics and check
# each against a CISPR-style limit. Engineering estimate; uses numpy.

import numpy as np

# Simplified small-loop far-field estimate at distance r (m):
#   E(uV/m) ~ K * f_MHz^2 * area_cm2 * I_mA / r
# K is a lumped constant for this teaching model.
K = 0.012
area_cm2 = 4.0       # signal-return loop area
i_ma = 2.0           # harmonic current amplitude
r_m = 3.0            # measurement distance
limit = 40.0         # dBuV/m (e.g. class B around 100-200 MHz, simplified)
clock = 100.0        # MHz fundamental

# E(uV/m) ~ K * f_MHz^2 * area_cm2 * I_mA / r ; dB conversion at module level.
print("loop area %.1f cm^2, harmonic current %.1f mA, distance %.0f m, limit %.0f dBuV/m" % (area_cm2, i_ma, r_m, limit))
print("harmonic   freq(MHz)   E(dBuV/m)   margin   verdict")
for n in [1, 3, 5, 7, 9]:
    f = clock * n
    e_uv = K * (f ** 2) * area_cm2 * i_ma / r_m
    e = 20.0 * float(np.log10(e_uv))
    margin = limit - e
    print("   %dx        %-8.0f    %6.1f     %+5.1f   %s" % (n, f, e, margin, "ok" if margin >= 0 else "FAIL"))

# Halving the loop area drops the field by 6 dB (factor of 2):
e_big = 20.0 * float(np.log10(K * (700.0 ** 2) * area_cm2 * i_ma / r_m))
e_small = 20.0 * float(np.log10(K * (700.0 ** 2) * (area_cm2 / 2.0) * i_ma / r_m))
print()
print("7th harmonic with half the loop area: %.1f -> %.1f dBuV/m (%.1f dB better)" % (e_big, e_small, e_big - e_small))
print("the f^2 law makes high harmonics fail first; shrinking loop area is the cure.")
""",
        ),
        _t(
            "Conducted emissions & filtering",
            "11 min",
            r"""# Conducted emissions & filtering

Below ~30 MHz, interference mostly escapes by **conduction** — riding out on the
**power and signal cables**. The cure is **filtering**: insert components that
present a high impedance to noise (or shunt it back to its source) while passing the
wanted signal/power.

**The two noise modes set the filter design** (grounding lesson, applied):

- **Differential-mode (DM)** noise — between line and neutral (the normal current
  loop). Filtered by a **series inductor** and an **X-capacitor** (line-to-line).
- **Common-mode (CM)** noise — line and neutral together, returning via earth.
  Filtered by a **common-mode choke** (both lines wound on one core so DM current's
  fields cancel but CM current sees high impedance) and **Y-capacitors**
  (line-to-earth).

A typical **mains EMI filter** combines these:

```
line  ──[CM choke]──┬──[X-cap]──┬── load
neut  ──[CM choke]──┘   |  |     └──
                    [Y]      [Y]
                     └── earth ──┘
```

**How a filter attenuates** — it's an **impedance mismatch** deliberately placed in
the noise path. A simple **LC low-pass** gives **−40 dB/decade** above its corner
frequency `f_c = 1/(2π√(LC))`: pick f_c **below** the noise band and **above** the
wanted band. More stages → steeper roll-off. The **insertion loss** vs frequency is
the filter's figure of merit.

**Practical filtering realities (where beginners go wrong):**

- **Filter at the boundary.** Place the filter right where the cable **enters/exits
  the enclosure**, bonded to the chassis — otherwise noise couples around it.
- **Components aren't ideal.** A capacitor has series inductance (**ESL**) and a
  **self-resonant frequency** above which it becomes inductive and stops filtering;
  an inductor has parallel capacitance. Real filters are chosen for the **actual
  noise frequency**.
- **Ferrites / ferrite beads** add frequency-dependent **resistance** that
  **dissipates** high-frequency noise as heat — cheap, common, great on cables and
  power lines (a clip-on ferrite is the classic "lump" on a cable).
- **Match the filter to the impedance:** a series element (inductor/ferrite) works
  best facing a low-impedance source; a shunt element (cap) facing a high-impedance
  source.

The takeaway: **conducted EMI is solved by filtering at the port**, with the filter
topology (DM vs CM elements) matched to the dominant noise mode and tuned to the
offending frequency. You'll compute an LC filter's attenuation next.
""",
        ),
        _code(
            "LC filter attenuation",
            "12 min",
            r"""# A low-pass LC filter blocks high-frequency conducted noise. Its corner is
# f_c = 1/(2*pi*sqrt(L*C)); above it, attenuation rolls off ~ -40 dB/decade.
# Compute the insertion loss vs frequency and find where it meets a target. numpy.

import numpy as np

L = 10e-6      # 10 uH
C = 100e-9     # 100 nF
pi = 3.141592653589793

fc = 1.0 / (2.0 * pi * float(np.sqrt(L * C)))
print("L = %.0f uH, C = %.0f nF -> corner f_c = %.3f MHz" % (L * 1e6, C * 1e9, fc / 1e6))
print()
print("freq(MHz)   |H| atten(dB)")
for f_mhz in [0.1, 0.5, fc / 1e6, 1.0, 5.0, 10.0, 30.0]:
    f = f_mhz * 1e6
    ratio = f / fc
    # 2nd-order low-pass magnitude (ideal, undamped-ish): |H| = 1/|1 - (f/fc)^2|
    denom = abs(1.0 - ratio * ratio)
    if denom < 1e-6:
        denom = 1e-6
    atten_db = -20.0 * float(np.log10(1.0 / denom))   # negative = attenuation
    print("  %-8.3f   %7.1f" % (f_mhz, atten_db))

# Where does it reach -40 dB (100x suppression)?
# -40 dB -> (f/fc)^2 ~ 100 -> f ~ 10 * fc
print()
print("approx -40 dB (100x) attenuation near f = 10 * f_c = %.2f MHz" % (10 * fc / 1e6))
print("place f_c BELOW the noise band, ABOVE the wanted band; more stages = steeper.")
""",
        ),
        _t(
            "Shielding in depth",
            "10 min",
            r"""# Shielding in depth

The Basics course showed an ideal shield reflects and absorbs fields
(SE = R + A). In reality, **a shield is only as good as its worst hole** — and real
enclosures are full of holes. Intermediate shielding is mostly about **apertures and
seams**.

**Why holes matter so much.** A slot in a shield acts like a **slot antenna**. Its
leakage depends on the slot's **longest dimension** relative to wavelength: leakage
becomes severe when the slot length approaches **λ/2**, and a shield is effectively
transparent at frequencies where the largest opening is a half-wavelength. The
counter-intuitive rule:

```
Many SMALL holes leak far LESS than one LARGE hole of the same total area.
```

So a ventilation grille of many little holes shields better than one big slot — and
a **long thin seam** (a poorly-bonded lid) is worse than a round hole, because it's
the **longest dimension** that radiates. This is why a 1 mm gap along a seam can
wreck an otherwise excellent enclosure.

**Practical aperture/seam control:**

- **Keep the maximum slot dimension small** relative to the highest frequency of
  concern (keep it ≪ λ/2; a common target is < λ/20).
- **Bond seams frequently** — many short fasteners/contacts, **EMI gaskets**
  (conductive elastomer/fingerstock), and conductive coatings, so lid-to-box
  current flows without gaps.
- **Treat every penetration**: ventilation → **honeycomb** waveguide vents or many
  small holes; displays → **conductive mesh/coating**; connectors → bonded,
  filtered; shafts/buttons → conductive bushings.

**Cables are the biggest "hole."** An unshielded (or poorly-bonded) cable
penetrating the enclosure carries shield-internal noise straight outside, defeating
the shield entirely. **Shielded cables must be bonded 360° to the chassis at
entry** (a "pigtail" ground wire is a classic mistake — it adds inductance and ruins
high-frequency shielding).

**Material choice** depends on the field: **magnetic (H) fields at low frequency**
are hardest to shield and need **high-permeability** material (mu-metal) for
absorption; **electric (E) fields and plane waves** are easy to reflect with any
**good conductor**.

The discipline: **think of the enclosure as a Faraday cage whose performance is set
by its leaks** — apertures, seams, and cable penetrations — not by the nominal SE of
the metal. A theoretically 100 dB shield with one bad seam might deliver 20 dB.
Shielding is **detailing**, and it works with — never instead of — controlling the
source and the return currents.
""",
        ),
        _t(
            "ESD: electrostatic discharge",
            "10 min",
            r"""# ESD: electrostatic discharge

**Electrostatic discharge** is a sudden transfer of charge — the spark when you
touch a doorknob — and it's both a **reliability killer** (it destroys components)
and a mandatory **immunity test** (IEC 61000-4-2). An ESD event is brutally fast and
high-voltage: **kilovolts**, rising in **under a nanosecond**, with peak currents of
**amperes**. That sub-nanosecond edge is enormously broadband (rise-time/bandwidth
again), so ESD couples everywhere.

**Two faces of ESD:**

- **Component damage (manufacturing/handling)** — a human or machine discharges into
  a sensitive part, punching through thin gate oxides or fusing tiny traces. Modeled
  by the **Human Body Model (HBM)**, **Charged Device Model (CDM)**, and Machine
  Model — chips are rated to withstand a certain HBM/CDM voltage. Controlled with
  **ESD-safe handling**: wrist straps, mats, ionizers, grounded workstations.
- **System immunity (in the field)** — a user zaps the product (a connector, a
  button, a seam). The product must **survive and keep working** to pass. Tested by
  zapping with an **ESD gun** at specified kV via **contact** and **air** discharge.

**Designing for ESD immunity** — give the energy a **safe path** to chassis/ground
that **bypasses** sensitive circuitry:

- **TVS diodes / ESD-protection devices** at every exposed port (USB, buttons,
  connectors) — they clamp the voltage and **shunt the surge** to ground in
  picoseconds, before it reaches the chip. Place them **right at the connector**,
  with a **short, low-inductance** path to a solid ground.
- **Spark gaps / creepage & clearance** — physical layout so the discharge arcs to
  a safe point (e.g. a guard ring near a connector) rather than into the circuit.
- **Ground/chassis strategy** — a low-impedance chassis path to carry the surge
  away; keep sensitive traces away from exposed metal.
- **Series resistance/ferrites** on exposed lines to limit the surge current that
  reaches the IC.

The key insight echoes the whole track: ESD is a **fast transient seeking a return
path** — if you don't *provide* a safe, low-inductance path to ground at the entry
point, it will find its own destructive path **through your circuit**. Robust
products **route the discharge** to chassis at the boundary (TVS + grounding) and
keep its broadband energy out of the sensitive electronics. ESD design is immunity
design at its most demanding — and a frequent cause of field failures when
neglected.
""",
        ),
        quiz_lesson(
            "Quiz: Emissions, Filtering & ESD",
            (
                q(
                    "Why do a clock's high harmonics often fail radiated emissions before the fundamental?",
                    (
                        opt(
                            "Loop radiation scales with frequency² (E ∝ f²·A·I), so higher-frequency harmonics radiate far more efficiently",
                            correct=True,
                        ),
                        opt("Harmonics carry more current than the fundamental"),
                        opt("Low frequencies always fail first"),
                        opt("Harmonics don't exist"),
                    ),
                    "The f² law means the 5th/7th harmonic radiates much more than the fundamental for the same loop; shrink loop area and slow edges.",
                ),
                q(
                    "What is a common-mode choke used for?",
                    (
                        opt(
                            "Presenting high impedance to common-mode noise (both lines together) while passing differential signal/power",
                            correct=True,
                        ),
                        opt("Blocking all current"),
                        opt("Increasing emissions"),
                        opt("Shielding light"),
                    ),
                    "Wound so DM fields cancel (low impedance to wanted current) but CM current sees high impedance — key for cable/common-mode emissions.",
                ),
                q(
                    "Above an LC low-pass filter's corner frequency, attenuation rolls off at roughly…",
                    (
                        opt("−40 dB/decade (a 2nd-order filter)", correct=True),
                        opt("0 dB/decade"),
                        opt("+20 dB/decade"),
                        opt("−6 dB/octave only, forever flat after"),
                    ),
                    "A 2nd-order LC gives ~−40 dB/decade above f_c=1/(2π√(LC)); place f_c below the noise band and above the wanted band.",
                ),
                q(
                    "Why do many small holes in a shield leak less than one large hole of the same total area?",
                    (
                        opt(
                            "Aperture leakage depends on the longest dimension (slot-antenna effect), not total area — small holes have small max dimension",
                            correct=True,
                        ),
                        opt("Small holes have more total area"),
                        opt("Large holes reflect more"),
                        opt("Area is all that matters"),
                    ),
                    "A slot radiates based on its longest dimension vs wavelength; keep the max opening ≪ λ/2. A long seam is worse than a round hole.",
                ),
                q(
                    "What is the best way to bond a shielded cable to an enclosure for high-frequency shielding?",
                    (
                        opt(
                            "A 360° bond of the shield to the chassis at the entry point",
                            correct=True,
                        ),
                        opt("A long pigtail ground wire"),
                        opt("Leave it floating"),
                        opt("Connect only the center conductor"),
                    ),
                    "A pigtail adds inductance and ruins HF shielding; a 360° bond carries shield current cleanly so the cable doesn't defeat the enclosure.",
                ),
                q(
                    "What's the core strategy for ESD immunity at an exposed port?",
                    (
                        opt(
                            "Provide a safe, low-inductance path (TVS to ground at the connector) that shunts the surge before it reaches sensitive circuitry",
                            correct=True,
                        ),
                        opt("Make traces as thin as possible"),
                        opt("Remove all grounding"),
                        opt("Slow the system clock"),
                    ),
                    "ESD is a fast transient seeking a return path; TVS/clamps at the boundary with short ground paths route it away from the ICs.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# emc-advanced
# ──────────────────────────────────────────────────────────────────────

_EMC_ADVANCED = SeedCourse(
    slug="emc-advanced",
    title="EMC / EMI — Advanced",
    description=(
        "Designing for compliance and debugging failures: EMC-driven PCB/stackup "
        "design, spread-spectrum clocking, cable and connector EMC with "
        "common-mode chokes, pre-compliance debugging technique, and the "
        "regulatory landscape. With runnable spread-spectrum and emissions-budget "
        "labs."
    ),
    level="Advanced",
    lessons=(
        _t(
            "EMC by design: layout & stackup",
            "11 min",
            r"""# EMC by design: layout & stackup

The cheapest EMC fix costs nothing because it's **designed in** before the first
prototype. By the time you're in the chamber, options are limited to shields,
ferrites, and gaskets bolted on; the real wins are in **PCB layout and stackup** —
where EMC, signal integrity, and power integrity are the **same problem** (control
the return current and the loops).

**The stackup is the foundation.** A good multilayer stackup puts **signal layers
adjacent to solid reference planes**, giving every signal a tight, continuous return
path directly beneath it. A bad stackup (signals with no nearby plane, or planes
split under signals) guarantees large loops → emissions and susceptibility.
Power-ground plane pairs close together also add high-frequency decoupling
capacitance.

**The highest-impact layout rules (roughly in order):**

- **Continuous reference planes / control return paths.** Never route a high-speed
  signal across a **plane split** or gap — its return current detours into a large
  radiating loop. This single rule prevents most failures.
- **Minimise loop areas.** Keep signal and its return adjacent; keep decoupling caps
  tight to power pins so transient current loops stay small and local.
- **Partition the board.** Group by function/noise — keep **noisy** sections
  (SMPS, clocks, motor drivers, digital) **away from quiet** ones (analog, RF,
  sensors); control where currents cross between regions.
- **Control clock/edge routing.** Route clocks and fast signals over solid planes,
  away from board edges and connectors; **slow edges** that don't need to be fast.
- **Treat the board edge & connectors.** Keep high-speed signals and noisy planes
  **away from the edge** (edges radiate); filter/ground at connectors where cables
  attach (the dominant radiators).
- **Stitch grounds.** Sew ground planes together with **vias** (especially near
  layer transitions and the board perimeter — "via fencing") so return current has a
  low-inductance path and planes don't resonate.

**Component & power choices** matter too: low-EMI SMPS (or spread spectrum, next
lesson), edge-rate-controlled drivers, on-board filtering at I/O.

The professional mindset: **EMC is a layout discipline first**, a shielding/filtering
discipline second. A board designed with continuous return paths, small loops,
sensible partitioning, and treated connectors often passes with margin and **no**
shield — while a poorly-laid-out board can't be rescued by any amount of bolted-on
metal. Design it in; don't bolt it on.
""",
        ),
        _t(
            "Spread-spectrum clocking",
            "9 min",
            r"""# Spread-spectrum clocking

EMC limits are measured **per frequency** (in a defined resolution bandwidth), so a
clock's energy concentrated at exact harmonic frequencies produces tall, narrow
**spikes** that poke above the limit. **Spread-spectrum clocking (SSC)** is a clever
trick: instead of reducing the *total* emitted energy, it **spreads** that energy
over a small frequency band so no single frequency bin is as tall.

**How it works.** The clock is **frequency-modulated** by a small amount (typically
**0.5–2%**, often only downward — "down-spread" — to not exceed timing limits), at a
low rate (tens of kHz). A nominally 100 MHz clock instead sweeps over, say,
99–100 MHz continuously. The harmonic that used to sit entirely in one measurement
bin is now **smeared across many bins**, lowering the **peak** reading.

```
without SSC:  ▌            one tall spike at f
with SSC:    ▁▂▃▃▂▁         same energy, spread over a band -> lower peak
```

The peak reduction grows with how widely the energy is spread relative to the
measurement bandwidth — typically **7–15 dB** of attenuation at higher harmonics
(more at higher frequencies, where a fixed % spread covers more absolute Hz). That
can be the difference between failing and passing.

**The honest caveats:**

- **It doesn't reduce total energy** — it just redistributes it. A victim with a
  *wide* bandwidth (e.g. another wideband receiver) sees the same total
  interference; SSC mainly helps against **narrowband** measurement/victims. Some
  regard it as "gaming the measurement," but it's standard and effective for passing
  CISPR-style limits.
- **It adds jitter.** The frequency modulation **is** timing jitter, which can hurt
  high-speed links, audio, or anything clock-sensitive — so SSC is often **disabled**
  on critical clocks (e.g. some SerDes reference clocks) and used on the noisy,
  non-critical ones.
- **Down-spread vs center-spread** — down-spread keeps the max frequency at nominal
  (safe for timing); center-spread gives more reduction but raises the top
  frequency.

SSC is built into most modern clock generators and SMPS controllers as a one-bit
"EMI reduction" feature. The advanced engineer knows **what it really does** (trades
peak emission for jitter, redistributes rather than removes energy), so they enable
it where it helps and avoid it where the jitter would hurt. You'll quantify the peak
reduction next.
""",
        ),
        _code(
            "Spread-spectrum peak reduction",
            "12 min",
            r"""# Spread-spectrum clocking keeps the SAME total energy but spreads it over a
# band, so the PEAK in any measurement bin drops. Model the peak reduction vs how
# many measurement bins the energy is spread across. Uses numpy.

import numpy as np

# Total harmonic 'energy' (arbitrary linear units) concentrated, then spread.
total_energy = 1.0

print("spreading the same energy over more measurement bins lowers the PEAK:")
print("spread bins   peak(linear)   peak reduction(dB)")
peak_concentrated = total_energy            # all energy in one bin
for bins in [1, 2, 4, 8, 16, 32]:
    peak = total_energy / bins              # energy spread evenly across 'bins'
    reduction_db = -20.0 * float(np.log10(peak / peak_concentrated))
    print("   %-10d   %.4f         %.1f" % (bins, peak, reduction_db))

print()
# A typical 1% down-spread on a 200 MHz harmonic at 120 kHz RBW:
spread_hz = 0.01 * 200e6        # 1% of 200 MHz = 2 MHz spread
rbw = 120e3                     # CISPR resolution bandwidth
bins = spread_hz / rbw
reduction = 10.0 * float(np.log10(bins))   # ~ power spread over bins
print("1%% down-spread @200MHz, RBW=120kHz -> ~%.0f bins -> ~%.1f dB peak reduction" % (bins, reduction))
print("note: TOTAL energy is unchanged (it just moves); SSC also ADDS jitter.")
""",
        ),
        _t(
            "Cables, connectors & common-mode chokes",
            "10 min",
            r"""# Cables, connectors & common-mode chokes

By the time you reach advanced EMC, one lesson dominates real products: **the
cables are the antennas.** A PCB by itself is electrically small and often radiates
poorly; attach a cable and you've bolted on a **highly efficient antenna** tens of
centimetres long. The overwhelming majority of radiated-emissions failures (and many
immunity failures) involve **common-mode current on cables**.

**Why cables radiate.** Any **common-mode voltage** between the PCB ground and the
"outside world" drives a **common-mode current** down the cable, which radiates like
a monopole/dipole. Even **millivolts** of common-mode noise on a 1 m cable can
exceed limits at VHF. The common-mode voltage comes from **ground noise**, imperfect
return paths, and the very SI/PI problems of the other tracks — which is why
**cables expose your internal EMC sins**.

**The control toolkit, at the cable boundary:**

- **Common-mode choke (CMC)** — the workhorse. All conductors of the cable pass
  through one ferrite core; **differential** (wanted) current's fields cancel (it
  passes freely), while **common-mode** current sees a high impedance and is choked.
  A clip-on **ferrite** is a one-turn CMC; a wound CMC gives more impedance. Pick the
  ferrite material for the **offending frequency band**.
- **Filter at the connector** — Y-caps to chassis, pi-filters, filtered connectors —
  shunt common-mode noise to chassis **before** it reaches the cable.
- **Shielded cable, bonded 360°** — the shield carries common-mode current on its
  *outside* and keeps it off the inner conductors — **but only if bonded properly at
  both ends** (the 360° vs pigtail rule). A shield grounded at one end only does
  little for radiated emissions.
- **Reduce the source** — fix the ground noise / return path so there's little
  common-mode voltage to begin with (the real cure).

**The chassis is the reference.** At the system level, the **metal chassis** (not
the PCB ground) is the high-frequency reference that cables and shields bond to;
getting **PCB ground → chassis** bonding right (low inductance, at the I/O area) is
what stops internal noise from driving the cables.

The advanced view: **manage every cable penetration as an EMC port** — choke and/or
filter common-mode current, bond shields 360° to chassis, and above all **minimise
the common-mode voltage** that drives them. Control the cables and you've controlled
most of your radiated emissions; ignore them and no internal fix will save you.
""",
        ),
        _t(
            "Pre-compliance testing & debugging",
            "10 min",
            r"""# Pre-compliance testing & debugging

Full compliance testing at an accredited lab is **expensive and slow**, and a
failure there is a costly schedule hit. **Pre-compliance** testing — done in-house,
early and often — catches problems when they're cheap to fix and turns EMC from a
gamble into engineering.

**The pre-compliance toolkit (affordable, in-house):**

- **Spectrum analyzer / EMI receiver** — see the emission spectrum vs frequency and
  compare to the limit line. The core instrument.
- **Near-field probes** — small **H-field (loop)** and **E-field (stub)** probes you
  hold over the board to **localise the source**: sweep over the PCB and watch which
  trace, IC, cable, or seam lights up at the failing frequency. This is the key
  debugging move — **find *where* the energy comes from**.
- **LISN** for conducted emissions; a **current probe** to measure common-mode
  current on cables (often correlates directly with radiated failures).
- A **small (semi-)anechoic tent or chamber**, or even a careful open-area setup, for
  rough radiated scans.

**The debugging methodology:**

```
1. Scan -> find the failing frequencies (which peaks exceed the limit?)
2. Identify the source: trace each peak to a clock/SMPS harmonic (frequency math)
3. Localise: near-field probe to find WHERE that frequency radiates (loop? cable?)
4. Determine the mechanism: loop area (differential) or cable common-mode?
5. Apply the matched fix (source / path / victim) and RE-MEASURE
6. Iterate -> confirm margin
```

**Practical debugging tactics:**

- **Frequency is a fingerprint** — a peak at exactly a clock harmonic points
  straight to that clock; a broad hump points to an SMPS or a resonance.
- **Wiggle test** — touching/adding a ferrite to a cable, or temporarily shielding a
  section with copper tape, and watching the peak drop **confirms** the source/path
  before you commit to a layout fix.
- **One change at a time, always re-measure** — EMC fixes interact; verify each.

The mindset that separates pros: **EMC is debuggable, not mystical.** Every failing
peak has a **source**, a **path**, and a **mechanism** you can find with a spectrum
analyzer and near-field probes. Pre-compliance lets you do that iteration in your own
lab — so the accredited-lab visit is a **confirmation**, not a discovery. You'll
track an emissions margin budget across multiple sources next.
""",
        ),
        _code(
            "Emissions margin budget",
            "12 min",
            r"""# Like a noise budget, EMC sign-off tracks each emission source against the limit
# and sums correlated contributions. Combine several harmonic sources at a
# frequency and check margin after planned mitigations. Uses numpy.

import numpy as np

limit_dbuv_m = 40.0     # class B limit at the frequency of interest

# Each source: raw emission (dBuV/m) and the mitigation (dB) you plan to apply.
sources = [
    ("clock 7th harmonic", 46.0, 10.0),    # add ferrite + shrink loop
    ("SMPS harmonic",      42.0, 8.0),     # add input filter
    ("cable common-mode",  44.0, 12.0),    # common-mode choke
]

def dbuv_to_lin(dbuv):
    return 10.0 ** (dbuv / 20.0)           # to linear field (uV/m); no numpy -> safe

print("limit = %.0f dBuV/m" % limit_dbuv_m)
print("source                 raw     mitig   after")
total_lin = 0.0
for name, raw, mitig in sources:
    after = raw - mitig
    total_lin = total_lin + dbuv_to_lin(after)     # sum fields (worst-case, in-phase)
    print("  %-20s  %.0f    -%.0f     %.1f" % (name, raw, mitig, after))

combined = 20.0 * float(np.log10(total_lin))       # back to dB at module level
margin = limit_dbuv_m - combined
print()
print("combined (sum of fields): %.1f dBuV/m" % combined)
print("margin vs limit: %+.1f dB -> %s" % (margin, "PASS with margin" if margin >= 6 else ("PASS (tight)" if margin >= 0 else "FAIL")))
print("note: summing in LINEAR field units (not dB) is the correct worst-case combine.")
""",
        ),
        _t(
            "The regulatory landscape & systems EMC",
            "9 min",
            r"""# The regulatory landscape & systems EMC

EMC engineering ultimately serves **certification** and **system-level
reliability**, and the requirements vary enormously by industry — knowing the
landscape lets you scope a project correctly from day one.

**The major regimes and how strict they are:**

- **Commercial/consumer** — **FCC Part 15** (USA), **CE / EMC Directive** with
  **CISPR/EN** standards (Europe), VCCI (Japan), and others. Class B (residential)
  is tighter than Class A (industrial). The baseline most products face.
- **Automotive** — **CISPR 25** (component emissions), **CISPR 12**, ISO 11452
  (immunity), plus stringent **OEM-specific** specs. Vehicles are dense, harsh
  EM environments with safety-critical electronics, so limits and immunity levels
  are demanding (and **conducted transients** on the 12/48 V bus, per ISO 7637,
  matter hugely).
- **Medical** — **IEC 60601-1-2**: strict **immunity** (a device must not malfunction
  near phones, surgical equipment, transmitters) because failures risk lives.
- **Military / Aerospace** — **MIL-STD-461** (very broad frequency range, tight
  limits, lightning/EMP considerations) and **DO-160** (airborne). The strictest,
  reflecting harsh environments and mission-critical functions.
- **Industrial / Information technology** — CISPR 11, CISPR 32/35, IEC 61000 series
  (the immunity test methods: ESD, EFT, surge, dips, conducted/radiated immunity).

**Systems EMC** adds concerns beyond a single PCB:

- **Inter-system compatibility** — your device coexisting with others (and with
  intentional radios — coexistence with Wi-Fi/cellular/GPS on the same platform).
- **Installation & cabling** — system-level emissions/immunity depend on how units
  are cabled, grounded, and bonded in the final installation (a compliant box can
  fail as installed).
- **Intentional radiators** — products with radios face **additional** spectrum
  regulations (FCC Part 15 Subpart C, RED in Europe) on top of unintentional-emission
  rules.
- **Safety overlap** — Y-capacitors and isolation interact with **electrical safety**
  (leakage current, creepage/clearance), so EMC and safety must be designed
  together.

The professional takeaway: **identify the applicable standards, classes, and limits
at the start** — they set your emission limits, immunity levels, and test plan, and
therefore your margins and design effort. EMC is not a single hurdle but a **regime**
that depends on where and how the product will be sold and used. Combined with the
design-it-in discipline of this track — controlled return paths, small loops,
treated cables, filtering and shielding where needed, and pre-compliance debugging —
it turns EMC from a feared last-minute gate into a managed, predictable part of
engineering.
""",
        ),
        quiz_lesson(
            "Quiz: Design, Spread Spectrum & Compliance",
            (
                q(
                    "What is the single highest-impact EMC layout rule?",
                    (
                        opt(
                            "Keep reference planes continuous / control return paths — never route high-speed signals across a plane split",
                            correct=True,
                        ),
                        opt("Use the thickest possible traces"),
                        opt("Add a shield over everything"),
                        opt("Maximise loop areas"),
                    ),
                    "A break in the return path forces a large radiating/susceptible loop; continuous planes and small loops prevent most EMC failures.",
                ),
                q(
                    "What does spread-spectrum clocking actually do to emissions?",
                    (
                        opt(
                            "Spreads the same energy over a frequency band, lowering the peak in any measurement bin (it doesn't reduce total energy) — and adds jitter",
                            correct=True,
                        ),
                        opt("Eliminates all emitted energy"),
                        opt("Increases the clock frequency"),
                        opt("Removes the need for filtering"),
                    ),
                    "SSC redistributes harmonic energy to lower the measured peak (7–15 dB), helping narrowband limits — but it adds timing jitter, so avoid it on critical clocks.",
                ),
                q(
                    "Why are cables usually the dominant source of radiated emissions?",
                    (
                        opt(
                            "Common-mode current driven onto a long cable makes it an efficient antenna — even millivolts of CM voltage can exceed limits",
                            correct=True,
                        ),
                        opt("Cables carry the most differential signal"),
                        opt("PCBs cannot radiate at all"),
                        opt("Cables are always shielded"),
                    ),
                    "A bare PCB is electrically small; an attached cable is a long antenna driven by common-mode voltage from ground noise — hence chokes/filters/360° bonds.",
                ),
                q(
                    "In EMC debugging, what is a near-field probe used for?",
                    (
                        opt(
                            "Localising WHERE a failing frequency radiates (which trace, IC, cable, or seam)",
                            correct=True,
                        ),
                        opt("Measuring the final certified limit"),
                        opt("Generating ESD"),
                        opt("Cooling the board"),
                    ),
                    "H-field/E-field probes swept over the board pinpoint the source of a failing peak so you can apply a matched fix and re-measure.",
                ),
                q(
                    "When combining multiple emission sources for a margin budget, how should their fields be summed?",
                    (
                        opt(
                            "In linear field units (worst case), not by adding dB values directly",
                            correct=True,
                        ),
                        opt("By adding the dB numbers together"),
                        opt("By taking the maximum only"),
                        opt("They never combine"),
                    ),
                    "dB are logarithmic ratios; to combine contributions you convert to linear field, sum, then convert back — adding dB would be wrong.",
                ),
                q(
                    "Which regulatory regime is generally the strictest?",
                    (
                        opt(
                            "Military/aerospace (MIL-STD-461, DO-160) — broad frequency range, tight limits, harsh/mission-critical environments",
                            correct=True,
                        ),
                        opt("Consumer FCC Class B"),
                        opt("There are no differences between regimes"),
                        opt("Industrial only"),
                    ),
                    "Requirements scale with environment and criticality; military/aerospace and medical immunity are far stricter than consumer Class A/B.",
                ),
            ),
        ),
    ),
)


EMC_COURSES = (_EMC_BASICS, _EMC_INTERMEDIATE, _EMC_ADVANCED)
