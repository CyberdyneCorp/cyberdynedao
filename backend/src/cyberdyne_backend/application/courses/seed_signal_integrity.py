"""Academy seed content — the Signal Integrity & High-Speed Digital Design track.

* ``signal-integrity-basics``        — when wires become transmission lines, reflections, termination
* ``signal-integrity-intermediate``  — crosstalk, eye diagrams & jitter, PDN, differential signaling
* ``signal-integrity-advanced``      — SerDes & equalization, S-parameters, power integrity, measurement

Runnable ``code`` lessons use numpy + builtins to compute reflection coefficients,
simulate a lattice (bounce) diagram, estimate crosstalk, build an eye diagram and
BER curve, and model interconnect delay and pre-emphasis. SPICE/IBIS appear as
read-only blocks. Part of the Electronic Engineering curriculum.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, Ω, ², ×, Γ, λ) in diagrams.
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
# signal-integrity-basics
# ──────────────────────────────────────────────────────────────────────

_SI_BASICS = SeedCourse(
    slug="signal-integrity-basics",
    title="Signal Integrity — Basics",
    description=(
        "Why fast digital signals misbehave on real boards: when a wire becomes a "
        "transmission line, characteristic impedance, reflections from impedance "
        "mismatches, termination schemes, and the link between rise time and "
        "bandwidth. With runnable reflection and bounce-diagram labs."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is signal integrity?",
            "10 min",
            r"""# What is signal integrity?

In a slow circuit a wire is just a wire — connect A to B and the voltage at B
equals the voltage at A. **Signal integrity (SI)** is the engineering of keeping
that true when signals get **fast**: at high edge rates, a copper trace stops
behaving like an ideal wire and starts behaving like a **transmission line**, and
the clean square wave you sent can arrive ringing, rounded, or corrupted.

**The key question: lumped or distributed?** A wire can be treated as a simple
**lumped** node (one voltage everywhere) only if a signal crosses it almost
instantly compared to how fast the signal changes. Once the **propagation delay**
along the wire is a meaningful fraction of the signal's **rise time**, different
points on the wire are at different voltages *at the same instant* — it's
**distributed**, and transmission-line effects appear.

The practical rule of thumb: treat an interconnect as a transmission line when

```
length  >  (rise_time × propagation_speed) / 6     (roughly)
```

— equivalently, when the line's one-way delay exceeds ~⅙ of the signal's rise
time. Note what matters is **rise time, not clock frequency**: a 10 MHz clock with
100 ps edges has the same SI problems as a multi-GHz signal, because SI is driven
by **how fast the edge changes**, not how often.

Why this matters more every year: edge rates keep getting faster (DDR, PCIe, USB,
HDMI, SerDes all run at multi-Gbps), so traces that were "just wires" a generation
ago now ring, reflect, and crosstalk. The symptoms SI fights:

- **Reflections / ringing** from impedance mismatches (this course).
- **Crosstalk** between neighbouring traces (next course).
- **Attenuation & jitter** that close the **eye** (next course).
- **Power-supply noise** through the delivery network.

SI is where **digital design meets electromagnetics**: the logic is 1s and 0s, but
whether those 1s and 0s arrive intact is an analog, high-frequency problem. This
track teaches you to keep fast edges clean — starting with the transmission line.
""",
        ),
        _t(
            "Transmission lines & characteristic impedance",
            "11 min",
            r"""# Transmission lines & characteristic impedance

A **transmission line** is any interconnect long enough to show distributed
behaviour: a PCB trace over a ground plane, a cable, a connector. Its defining
property is **characteristic impedance, Z₀** — the ratio of voltage to current of
a wave travelling down the line, set purely by the line's **geometry and
materials** (not its length):

$$ Z_0 = \sqrt{\frac{L}{C}} $$

where L and C are the inductance and capacitance **per unit length**. For PCB
traces, Z₀ depends on trace width, dielectric height, and the dielectric constant
(εr). Common controlled impedances: **50 Ω** (single-ended RF/digital), **100 Ω**
(differential pairs like USB/Ethernet).

A signal launched onto the line travels at the **propagation velocity**:

$$ v = \frac{c}{\sqrt{\varepsilon_r}} $$

In typical PCB dielectric (εr ≈ 4), that's roughly **half the speed of light** —
about **6 inches/ns** (15 cm/ns), or a delay of ~**170 ps/inch**. This finite
delay is the whole reason distributed effects exist.

Two common PCB geometries:

- **Microstrip** — a trace on an outer layer over one reference plane (faster, but
  fields are partly in air).
- **Stripline** — a trace buried between two planes (slower, but better shielded
  and lower emissions).

The crucial mental shift: **Z₀ is not a resistance you can measure with an
ohmmeter** — a lossless line draws no DC current. It's the **dynamic** impedance a
fast edge "sees" as it propagates, before any reflection returns. As long as the
source impedance, the line Z₀, and the load impedance all **match**, the edge
travels down and is absorbed cleanly. The instant they **don't** match, you get
reflections — the subject of the next lesson, and the central SI problem.

Controlling Z₀ — "**impedance-controlled routing**" — is therefore the foundation
of high-speed PCB design: the board house manufactures traces to a specified Z₀
(±10%), and your job is to keep the signal's environment uniform so that
impedance stays constant end to end.
""",
        ),
        _t(
            "Reflections & the reflection coefficient",
            "11 min",
            r"""# Reflections & the reflection coefficient

When a travelling wave reaches a point where the impedance **changes** — the end
of the line, a connector, a via, a stub — part of its energy **reflects back**
toward the source, like an echo. Reflections are *the* classic SI problem: they
cause **ringing**, overshoot/undershoot, and false logic transitions.

The fraction reflected at a boundary between impedance Z₀ and a load Z_L is the
**reflection coefficient Γ** (gamma):

$$ \Gamma = \frac{Z_L - Z_0}{Z_L + Z_0} $$

Read off the three cases that tell you everything:

- **Matched (Z_L = Z₀):** Γ = 0 → **no reflection**. All energy absorbed. The goal.
- **Open circuit (Z_L = ∞):** Γ = +1 → **full reflection, same polarity** (voltage
  doubles at the open end).
- **Short circuit (Z_L = 0):** Γ = −1 → **full reflection, inverted**.

Anything between gives a partial reflection; the **sign** tells you whether the
reflected wave adds to (overshoot) or subtracts from (undershoot) the signal.

Reflections happen at **both ends**: the load reflects a wave back, the source
(if mismatched) re-reflects it forward, and so on — the wave **bounces** until it
decays, producing the **ringing** you see on a scope. The settling pattern depends
on both the load and source reflection coefficients.

A related figure of merit, especially in RF, is **VSWR** (Voltage Standing Wave
Ratio):

$$ \text{VSWR} = \frac{1 + |\Gamma|}{1 - |\Gamma|} $$

VSWR = 1 is a perfect match; larger means worse. (VSWR 2:1 ≈ 11% reflected
voltage.)

```plot
{"title": "Reflection magnitude vs load (normalised to Z₀)", "xLabel": "Z_L / Z₀", "yLabel": "|Γ|", "xRange": [0, 5], "yRange": [0, 1], "functions": [{"expr": "abs((x - 1) / (x + 1))", "label": "|Γ| = |(Z_L−Z₀)/(Z_L+Z₀)|", "color": "#dc2626"}]}
```

The cure is **impedance matching** — make Z_L (and/or the source) equal Z₀ so Γ →
0 — which is exactly what **termination** does (next lesson). The takeaway: every
**impedance discontinuity** along a high-speed path is a reflection source, so SI
design is largely about keeping impedance **continuous** and **terminating**
properly. You'll compute Γ and VSWR for real loads next.
""",
        ),
        _code(
            "Reflection coefficient & VSWR",
            "12 min",
            r"""# At every impedance change a fast edge partly reflects. The reflection
# coefficient Gamma = (ZL - Z0) / (ZL + Z0) quantifies it; VSWR summarises the
# match. Compute them for several loads on a 50-ohm line. Uses numpy + builtins.

import numpy as np

z0 = 50.0
loads = [50.0, 75.0, 100.0, 25.0, 0.0, 1e9]   # matched, mild, 2x, half, short, open

print("Z0 =", z0, "ohms")
print("  ZL        Gamma     |Gamma|   %refl   VSWR")
for zl in loads:
    gamma = (zl - z0) / (zl + z0)
    mag = abs(gamma)
    pct = 100.0 * mag
    if mag < 1.0:
        vswr = (1.0 + mag) / (1.0 - mag)
    else:
        vswr = float("inf")
    name = "open" if zl > 1e6 else ("%.0f" % zl)
    print("  %-8s  %+.3f    %.3f    %5.1f   %s" % (name, gamma, mag, pct, ("inf" if vswr == float("inf") else "%.2f" % vswr)))

# A partial reflection adds ringing. At an OPEN end (Gamma=+1) the incident step
# doubles; reflected voltage = Gamma * incident.
incident = 1.0       # a 1 V step travelling down the line
for zl in [50.0, 100.0, 1e9]:
    gamma = (zl - z0) / (zl + z0)
    reflected = gamma * incident
    at_load = incident + reflected
    print("ZL=%-6s -> reflected %.2f V, voltage at load %.2f V" % (("open" if zl > 1e6 else "%.0f" % zl), reflected, at_load))
print("matched load (50) -> no reflection, clean edge. mismatches -> ringing.")
""",
        ),
        _t(
            "Termination schemes",
            "10 min",
            r"""# Termination schemes

**Termination** kills reflections by adding a resistor (or network) so the line
"sees" an impedance equal to Z₀ at one or both ends, driving Γ → 0. Choosing the
scheme trades off power, signal quality, and component count.

**Series (source) termination** — a resistor **at the driver**, sized so
`R_series + R_driver = Z₀`. The edge launches at half amplitude, travels to the
(unterminated) load where it **doubles** (Γ ≈ +1) to full amplitude, and the
reflection returns and is **absorbed** at the source. Cheap, **low power** (no DC
path), and excellent for **point-to-point** nets — but only correct at the
*single* far end (the line is at half-voltage during the round trip).

```
driver --[Rs]---------------- load (high-Z)
        Rs + Rdrv = Z0
```

**Parallel termination** — a resistor **at the load** to ground (or VCC), equal to
Z₀. The line is matched at the far end, so the edge is absorbed on first arrival —
great for **multi-drop** buses and best signal fidelity — but it draws **constant
DC current** (power) and loads the driver.

**Thévenin termination** — two resistors at the load (to VCC and GND) that parallel
to Z₀ while setting a bias level. Common on buses (e.g. older DDR), but burns power
in both resistors.

**AC termination** — a resistor **in series with a capacitor** to ground at the
load: looks like Z₀ to fast edges but blocks DC, **saving static power**. The cap
value is a tuning compromise.

**Differential termination** — a single resistor across the pair (≈100 Ω) for
differential signaling (next course).

Choosing:

```
Point-to-point, low power?   -> series (source) termination
Multi-drop bus, best SI?     -> parallel termination
Need DC bias level?          -> Thévenin
Save static power on a bus?  -> AC termination
```

The unifying idea: **present Z₀ where reflections would otherwise occur.**
Termination is the single most important reflection cure in high-speed design —
and where you place it (source vs load) follows directly from the topology.
""",
        ),
        _code(
            "Bounce (lattice) diagram",
            "13 min",
            r"""# When BOTH ends are mismatched, a step bounces back and forth, each round trip
# adding a smaller reflection -> the 'ringing' on a scope. A lattice diagram tracks
# the accumulating voltage at the load. Simulate it. Uses builtins.

z0 = 50.0
zs = 25.0       # source impedance (mismatched -> re-reflects)
zl = 1e9        # load: open circuit (Gamma_L ~ +1)
vsource = 2.0   # source step (before the source divider)

gamma_s = (zs - z0) / (zs + z0)
gamma_l = (zl - z0) / (zl + z0)
print("Gamma_source =", round(gamma_s, 3), " Gamma_load =", round(gamma_l, 3))

# Initial launched wave: source divider z0/(zs+z0).
launched = vsource * z0 / (zs + z0)
print("initially launched onto the line:", round(launched, 3), "V")
print()

# Track the wave bouncing; accumulate the voltage seen at the load.
wave = launched
v_load = 0.0
print("round   incident    reflect@load   V at load")
for rnd in range(1, 7):
    arrived = wave                      # wave arrives at load
    reflected_l = arrived * gamma_l     # reflects off the load
    v_load = v_load + arrived + reflected_l
    print("  %d     %+.4f      %+.4f       %.4f" % (rnd, arrived, reflected_l, v_load))
    # reflected wave travels back, re-reflects off the source, returns to load
    wave = reflected_l * gamma_s

print()
print("final settled V at load ->", round(v_load, 3), "V (settles to the full step)")
print("each bounce is smaller (|Gamma_s|<1) so the ringing decays. Matching ends removes it.")
""",
        ),
        _t(
            "Rise time, bandwidth & edges",
            "9 min",
            r"""# Rise time, bandwidth & edges

A recurring SI surprise: **what matters is the edge, not the clock**. A digital
signal's sharp transitions contain **high-frequency** content, and the faster the
edge, the higher the frequencies — which is what excites transmission-line
effects, crosstalk, and emissions.

The link between a signal's **rise time (t_r)** and its effective **bandwidth
(BW)** — the highest frequency that matters — is:

$$ \text{BW} \approx \frac{0.35}{t_r} $$

So a **1 ns** edge has ~**350 MHz** of bandwidth; a **100 ps** edge reaches
~**3.5 GHz** — regardless of whether the clock is 10 MHz or 1 GHz.

```plot
{"title": "Signal bandwidth vs rise time (BW ≈ 0.35 / t_r)", "xLabel": "rise time (ns)", "yLabel": "bandwidth (GHz)", "xRange": [0.05, 2], "yRange": [0, 8], "functions": [{"expr": "0.35 / x", "label": "0.35 / t_r", "color": "#2563eb"}]}
``` This is why a
slow-clocked bus with very fast buffers can still have severe SI problems: the
*edges* are fast.

Consequences that shape design:

- **Faster edges = more SI grief.** They reflect, couple, and radiate more. When a
  net doesn't need a fast edge, **slow it down** (edge-rate control / series
  resistor) — often the cheapest SI fix.
- **Your measurement gear must out-bandwidth the signal.** To see a 100 ps edge
  faithfully you need a scope/probe with several GHz of bandwidth, or you'll
  measure the *instrument's* rise time, not the signal's. (Rise times combine
  roughly as `t_measured ≈ √(t_signal² + t_scope²)`.)
- **The "knee frequency"** (~0.5/t_r) is where you focus impedance control: above
  it, the trace is firmly a transmission line.

The takeaway to carry into the rest of the track: **bandwidth is set by rise
time.** Every high-speed effect scales with edge rate, so the first questions in
any SI analysis are "how fast is the edge?" and "does this net actually need to be
that fast?" Managing edge rates — fast enough for timing, no faster — is a core SI
discipline.
""",
        ),
        quiz_lesson(
            "Quiz: Transmission Lines & Reflections",
            (
                q(
                    "When must an interconnect be treated as a transmission line rather than a simple wire?",
                    (
                        opt(
                            "When its propagation delay is a significant fraction of the signal's rise time",
                            correct=True,
                        ),
                        opt("Only above 1 GHz clock frequency"),
                        opt("Only for power traces"),
                        opt("Never, for digital signals"),
                    ),
                    "SI is driven by rise time, not clock rate: once one-way delay approaches ~⅙ of the edge's rise time, distributed effects appear.",
                ),
                q(
                    "What does the characteristic impedance Z₀ of a line depend on?",
                    (
                        opt(
                            "The line's geometry and dielectric (L and C per unit length) — not its length",
                            correct=True,
                        ),
                        opt("The line's total length"),
                        opt("The DC resistance measured with an ohmmeter"),
                        opt("The clock frequency"),
                    ),
                    "Z₀ = √(L/C) per unit length, set by trace/dielectric geometry; it's the dynamic impedance a fast edge sees, not a DC resistance.",
                ),
                q(
                    "For a load Z_L on a line of impedance Z₀, when is the reflection coefficient Γ zero?",
                    (
                        opt(
                            "When Z_L = Z₀ (matched) — all energy absorbed, no reflection",
                            correct=True,
                        ),
                        opt("When Z_L = 0 (short)"),
                        opt("When Z_L = ∞ (open)"),
                        opt("Never"),
                    ),
                    "Γ = (Z_L−Z₀)/(Z_L+Z₀); a matched load gives Γ=0. Open gives +1, short gives −1 (full reflections).",
                ),
                q(
                    "What does series (source) termination do?",
                    (
                        opt(
                            "Adds a resistor at the driver so R_series+R_driver=Z₀, absorbing the reflection on its return — low power, point-to-point",
                            correct=True,
                        ),
                        opt("Adds a resistor at the load drawing constant DC current"),
                        opt("Removes the ground plane"),
                        opt("Increases the clock speed"),
                    ),
                    "Series termination launches a half-amplitude edge that doubles at the far end; the return reflection is absorbed at the matched source. No DC path.",
                ),
                q(
                    "A signal has a 100 ps rise time. Its approximate bandwidth is…",
                    (
                        opt("~3.5 GHz (BW ≈ 0.35 / t_r)", correct=True),
                        opt("~100 MHz"),
                        opt("~35 MHz"),
                        opt("Exactly the clock frequency"),
                    ),
                    "BW ≈ 0.35/t_r → 0.35/100ps ≈ 3.5 GHz; faster edges carry higher frequencies and cause more SI effects regardless of clock rate.",
                ),
                q(
                    "Why does a slow 10 MHz clock sometimes still have serious signal-integrity problems?",
                    (
                        opt(
                            "SI is driven by edge rate (rise time), not clock frequency — fast buffers make fast edges with high bandwidth",
                            correct=True,
                        ),
                        opt("10 MHz is actually very high frequency"),
                        opt("Slow clocks always reflect more"),
                        opt("It cannot have SI problems"),
                    ),
                    "Fast edges contain high-frequency content (BW≈0.35/t_r) that excites reflections/crosstalk even when the clock is slow.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# signal-integrity-intermediate
# ──────────────────────────────────────────────────────────────────────

_SI_INTERMEDIATE = SeedCourse(
    slug="signal-integrity-intermediate",
    title="Signal Integrity — Intermediate",
    description=(
        "The effects that close the eye: line loss and dispersion, near- and "
        "far-end crosstalk, the eye diagram and jitter, the power delivery network "
        "and decoupling, and differential signaling. With runnable crosstalk and "
        "eye-diagram/BER labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Loss, attenuation & dispersion",
            "10 min",
            r"""# Loss, attenuation & dispersion

The ideal transmission line of the Basics course is **lossless**. Real lines lose
energy, and at multi-Gbps that loss is often the dominant problem — it rounds
edges, smears bits together, and **closes the eye**.

Two physical loss mechanisms grow with frequency:

- **Conductor loss (skin effect)** — at high frequency, current crowds into the
  surface of the conductor, shrinking the effective cross-section and raising
  resistance. It rises with **√f**.
- **Dielectric loss** — the insulating material (FR-4, etc.) absorbs energy as the
  field flips, characterised by the **loss tangent (tan δ)**. It rises roughly
  **linearly with f**, and dominates at the highest rates.

Because loss is **frequency-dependent**, a fast edge (which is made of many
frequencies) is distorted: the high-frequency components — the ones that make the
edge sharp — are attenuated **more** than the low ones. The result is
**dispersion**: the edge slows and spreads in time, so a bit's energy **smears
into the next bit** — **inter-symbol interference (ISI)**, the central enemy of
high-speed links.

```
sharp edge in  ──►  [lossy, dispersive channel]  ──►  rounded, spread edge out
```

Consequences and cures:

- **ISI closes the eye** (next lessons): adjacent bits interfere, making 1s and 0s
  harder to distinguish.
- **Lower-loss materials** (Megtron, Rogers vs FR-4) for long, fast channels.
- **Equalization** — deliberately boost the high frequencies to undo the channel's
  low-pass shaping (Advanced course): pre-emphasis/FFE at the transmitter, CTLE/DFE
  at the receiver.

The mental model upgrade: a real channel is a **frequency-dependent low-pass
filter**. SI at multi-Gbps becomes a question of **how much loss the channel has
at the signal's key frequencies**, and whether equalization can recover the eye.
You'll see the eye and ISI directly in a lab shortly.
""",
        ),
        _t(
            "Crosstalk: NEXT & FEXT",
            "11 min",
            r"""# Crosstalk: near-end & far-end

**Crosstalk** is unwanted coupling of a signal from one trace (the **aggressor**)
onto a neighbour (the **victim**) through the **mutual capacitance** and **mutual
inductance** between them. As traces get closer and edges get faster, crosstalk
grows — it causes noise, false switching, and timing push-out.

Coupling has two parts that combine differently at each end of the victim:

- **Capacitive coupling** injects current proportional to **dV/dt** (the
  aggressor's voltage edge), flowing **both ways** on the victim.
- **Inductive coupling** injects voltage proportional to **dI/dt** (the
  aggressor's current edge), with a **direction**.

Because of how these add, crosstalk appears as two distinct phenomena:

- **NEXT (Near-End Crosstalk)** — noise at the victim end **closest to the
  aggressor's driver**. Capacitive and inductive contributions **add**; NEXT is
  a relatively wide, same-polarity pulse and saturates for long lines. Dominant
  for signals travelling **opposite** directions.
- **FEXT (Far-End Crosstalk)** — noise at the **far** end. The two contributions
  **subtract**, leaving a **narrow spike** whose amplitude **grows with coupled
  length and edge speed**. Often the more damaging for co-propagating high-speed
  signals.

Crosstalk scales with:

```
↑ coupling  with  ↑ edge speed (dV/dt, dI/dt),  ↑ parallel length,  ↓ spacing,
            and  ↑ distance from the reference plane
```

The cures follow directly:

- **Spacing** — the "3W rule": keep trace-to-trace spacing ≥ 3× trace width to cut
  coupling sharply.
- **A close, continuous reference plane** — tight field confinement reduces mutual
  inductance/capacitance (and is the #1 SI rule generally).
- **Guard traces / ground** between sensitive lines (grounded at both ends).
- **Minimise parallel run length**; cross signals at 90° on adjacent layers.
- **Slower edges** where speed isn't needed.

Crosstalk is a **budget**: each aggressor contributes noise to a victim, and many
aggressors (a bus) sum. SI sign-off allocates a portion of the noise margin to
crosstalk and checks the total stays within it — which you'll estimate next.
""",
        ),
        _code(
            "Estimate crosstalk coupling",
            "12 min",
            r"""# Crosstalk grows with edge speed, coupling, and parallel length, and shrinks
# with spacing. A simple model: coupled noise ~ (coupling factor) * swing, where
# the coupling factor falls with spacing and rises with coupled length. Estimate
# victim noise and check it against a noise budget. Uses numpy + builtins.

import numpy as np

swing = 1.0           # aggressor voltage swing (V)
noise_budget = 0.15   # allowed crosstalk noise (V), e.g. 15% of swing

# Backward (NEXT) coupling coefficient ~ saturates; forward (FEXT) ~ grows with length.
# Toy model: k_b depends on spacing; FEXT grows with coupled length / rise time.
def next_noise(swing, kb):
    return swing * kb

def fext_noise(swing, length_in, tr_ns, kf):
    # narrow spike amplitude grows with coupled length and edge speed (1/tr)
    return swing * kf * length_in / tr_ns

print("aggressor swing = %.1f V, crosstalk budget = %.2f V" % (swing, noise_budget))
print("spacing   kb(NEXT)   NEXT(V)   FEXT(V, 4in,0.3ns)   total   verdict")
for spacing_w, kb, kf in [(1.0, 0.06, 0.010), (2.0, 0.03, 0.006), (3.0, 0.015, 0.003)]:
    nxt = next_noise(swing, kb)
    fxt = fext_noise(swing, 4.0, 0.3, kf)
    total = nxt + fxt
    verdict = "OK" if total <= noise_budget else "FAIL (too close)"
    print("  %.0fW      %.3f      %.3f       %.3f              %.3f   %s" % (spacing_w, kb, nxt, fxt, total, verdict))

print()
print("wider spacing (the 3W rule) sharply cuts coupling -> noise drops under budget.")
""",
        ),
        _t(
            "The eye diagram & jitter",
            "11 min",
            r"""# The eye diagram & jitter

The **eye diagram** is *the* picture of high-speed link health. You take a long
stream of bits and **overlay** every unit interval (UI) on top of each other,
triggered on the clock. The overlapping 1→0, 0→1, 1→1, 0→0 transitions trace out
an **"eye"** shape — and the size of the eye opening tells you, at a glance,
whether the receiver can reliably tell 1s from 0s.

```
voltage
   1 ─ \   ___   /      ← traces overlap; the open region in the
        \ /   \ /         middle is the "eye"
   0 ─  / \___/ \
        └── one unit interval (UI) ──┘
```

Two dimensions of the opening matter:

- **Vertical (voltage) eye opening** — the noise margin: how much amplitude
  separates a 1 from a 0 at the sampling instant. Closed by **loss/ISI**,
  crosstalk, and reflections.
- **Horizontal (timing) eye opening** — the timing margin: how much of the UI is
  "safe" to sample in. Closed by **jitter**.

**Jitter** is the deviation of edges from their ideal times — timing noise. It
decomposes into:

- **Random jitter (RJ)** — Gaussian, unbounded, from thermal noise; quoted as an
  RMS value and extrapolated to a **bit error rate** (e.g. ×14 for BER 1e-12).
- **Deterministic jitter (DJ)** — bounded, with a cause: **ISI** (data-dependent),
  **duty-cycle distortion**, periodic jitter (coupling from a clock/supply).

The receiver samples near the **centre** of the eye; an error occurs when noise +
jitter pushes a bit across the decision boundary at the sampling point. So the eye
opening **is** the margin, and SI sign-off is largely about **keeping the eye open
enough** for the target **BER** (often 1e-12 or 1e-15) — using a **bathtub curve**
(BER vs sampling position) to quantify the horizontal margin.

The eye unifies everything in this track: reflections, loss/ISI, crosstalk, and
jitter **all close the eye**, and equalization (next course) **opens it back up**.
You'll generate an eye diagram and a BER estimate from a noisy bit stream next.
""",
        ),
        _code(
            "Eye diagram & BER",
            "13 min",
            r"""# An eye diagram overlays many bit periods; noise/ISI close the 'eye' and cause
# errors. We build a noisy 2-level (NRZ) signal, measure the eye opening, and
# estimate the bit error rate (BER) at the decision threshold. Uses numpy.

import numpy as np

# A run of bits at two levels (0 V and 1 V), each held for some samples, with
# additive noise and slight ISI (a bit leaks into the next).
bits = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1])
samples_per_bit = 8
clean = np.repeat(bits.astype(float), samples_per_bit)

# Add ISI (low-pass smear) by a simple moving average, then noise.
kernel = np.ones(3) / 3.0
smeared = np.convolve(clean, kernel, mode="same")
noise_sigma = 0.12
noise = noise_sigma * np.sin(np.arange(len(smeared)) * 1.7)   # deterministic 'noise' (no RNG)
rx = smeared + noise

# Sample at the centre of each bit and decide against threshold 0.5.
threshold = 0.5
centers = np.arange(samples_per_bit // 2, len(rx), samples_per_bit)
sampled = rx[centers]
decided = (sampled > threshold).astype(int)
errors = int((decided != bits[: len(decided)]).sum())

# Eye opening: smallest margin between a sampled '1' and a sampled '0'.
ones = sampled[bits[: len(sampled)] == 1]
zeros = sampled[bits[: len(sampled)] == 0]
eye_open = float(ones.min() - zeros.max())

print("bits sent    :", list(bits[: len(decided)]))
print("bits decided :", list(decided))
print("sampled 1s: min %.2f   sampled 0s: max %.2f" % (float(ones.min()), float(zeros.max())))
print("vertical eye opening:", round(eye_open, 3), "V", "(OPEN)" if eye_open > 0 else "(CLOSED!)")
print("bit errors:", errors, "of", len(decided), " -> BER ~", round(errors / len(decided), 3))
print("more loss/noise -> smaller eye -> higher BER. Equalization reopens the eye.")
""",
        ),
        _t(
            "Power delivery & decoupling",
            "10 min",
            r"""# Power delivery & decoupling

Signals are only as clean as the **power** behind them. Every time a gate
switches, it pulls a sharp **current transient** from the supply. The **Power
Delivery Network (PDN)** — the regulators, planes, vias, and capacitors feeding the
chips — must supply that current **without the voltage sagging or ringing**, across
a huge frequency range. Poor power integrity shows up as supply noise that
modulates signals, creates jitter, and radiates.

The core relationship is **Ohm's law for the PDN**: a current transient ΔI across
the PDN impedance Z produces a voltage ripple `ΔV = ΔI × Z`. To keep ripple under
budget (say 5% of VDD) while ΔI can be amperes in nanoseconds, the PDN must present
a **low impedance** over frequency:

$$ Z_{\text{target}} = \frac{\Delta V_{\text{allowed}}}{\Delta I_{\text{max}}} $$

No single component is low-impedance everywhere, so the PDN is a **team of sources**
covering different frequency bands:

```
DC–kHz:   the voltage regulator (VRM)
kHz–MHz:  bulk capacitors (large electrolytic/tantalum)
MHz–100s MHz: ceramic decoupling caps (many small 0.1µF/0.01µF near pins)
GHz:      the power/ground plane capacitance & on-die capacitance
```

Key practices for power integrity:

- **Decoupling capacitors** placed **close** to each power pin act as **local
  charge reservoirs**, supplying the fast transient before the distant regulator
  can react. Placement and the **mounting inductance** (via/pad loops) matter as
  much as the capacitance — a perfectly-valued cap with a long, inductive
  connection is useless at high frequency.
- **Solid power/ground planes** provide low-inductance distribution and
  high-frequency plane capacitance.
- **Avoid plane splits** under high-speed signals — a signal's **return current**
  flows in the reference plane right beneath it; a gap forces a detour that adds
  inductance, noise, and EMI (a major, often-missed SI/PI/EMC issue).

The unifying idea — **return current**: every signal current loops back through the
nearest plane, so **signal integrity and power integrity are inseparable**. A clean
PDN and continuous reference planes are prerequisites for clean signals, which is
why PI is a core part of high-speed design, not a separate afterthought.
""",
        ),
        _t(
            "Differential signaling",
            "10 min",
            r"""# Differential signaling

Almost every fast interface — USB, PCIe, HDMI, Ethernet, SATA, LVDS, DDR strobes —
uses **differential signaling**: the data is carried on a **pair** of traces as the
**difference** between them (one goes high as the other goes low), and the receiver
looks only at **V+ − V−**.

Why this wins at high speed:

- **Noise immunity (common-mode rejection).** Noise and crosstalk couple **almost
  equally** onto both closely-routed traces (**common mode**); subtracting them at
  the receiver **cancels** that common noise, leaving the clean differential
  signal. This is the headline benefit.
- **Tighter return path / lower EMI.** The pair's currents are equal and opposite,
  so their fields largely cancel — radiating less and being less sensitive to a
  perfect reference plane.
- **Lower swing, faster edges.** Because the *difference* is what counts, you can
  use a smaller voltage swing (less power, faster) while keeping margin.

Differential lines have **two impedances**:

- **Differential impedance (Z_diff)** — seen by the difference signal (commonly
  **100 Ω**); set by trace geometry **and** the coupling between the two traces.
- **Common-mode impedance** — seen by signals common to both.

(For tightly-coupled pairs, Z_diff ≈ 2 × the odd-mode impedance of one trace.)

The routing rules that make it work:

- **Match length** within the pair tightly — a length mismatch becomes **skew**,
  converting good differential signal into harmful **common mode** (and closing the
  eye). Designers add tiny serpentine "**bumps**" to length-match.
- **Maintain constant spacing** end-to-end to hold Z_diff constant (keep the
  coupling uniform; route them as a couple).
- **Terminate differentially** (≈100 Ω across the pair at the receiver).
- **Symmetry everywhere** — vias, bends, and connectors should treat both traces
  identically, or you generate **mode conversion** (diff → common), which radiates
  and adds noise.

The big idea: differential signaling buys **robustness against the very effects
this track studies** — crosstalk, supply noise, and reference-plane imperfections —
by rejecting whatever is **common** to the pair. That's why it dominates modern
high-speed I/O, and why **symmetry and length-matching** are the differential
designer's obsessions.
""",
        ),
        quiz_lesson(
            "Quiz: Crosstalk, Eyes & Power",
            (
                q(
                    "Why does a lossy channel cause inter-symbol interference (ISI)?",
                    (
                        opt(
                            "Loss rises with frequency, attenuating the high-frequency edge content more, so bits spread in time into their neighbours",
                            correct=True,
                        ),
                        opt("It speeds up the edges"),
                        opt("It adds DC offset only"),
                        opt("Loss has no effect on digital signals"),
                    ),
                    "A real channel is a frequency-dependent low-pass filter; attenuating highs rounds/spreads edges so energy smears into adjacent bits (ISI).",
                ),
                q(
                    "What is the '3W rule' a remedy for?",
                    (
                        opt(
                            "Crosstalk — spacing traces ≥3× their width sharply reduces coupling between them",
                            correct=True,
                        ),
                        opt("Power supply ripple"),
                        opt("Clock jitter"),
                        opt("Via inductance"),
                    ),
                    "Crosstalk falls quickly with spacing; the 3W guideline (plus a close reference plane) keeps aggressor-to-victim coupling low.",
                ),
                q(
                    "What does the vertical opening of an eye diagram represent?",
                    (
                        opt(
                            "The voltage/noise margin separating a 1 from a 0 at the sampling instant",
                            correct=True,
                        ),
                        opt("The clock frequency"),
                        opt("The supply voltage"),
                        opt("The trace length"),
                    ),
                    "Vertical opening = amplitude margin (closed by loss/crosstalk/reflections); horizontal opening = timing margin (closed by jitter).",
                ),
                q(
                    "What sets the PDN target impedance?",
                    (
                        opt(
                            "Allowed voltage ripple divided by maximum transient current (Z_target = ΔV/ΔI)",
                            correct=True,
                        ),
                        opt("The clock frequency times capacitance"),
                        opt("The trace width"),
                        opt("The number of layers"),
                    ),
                    "Since ΔV = ΔI×Z, keeping ripple under budget for large fast ΔI requires a low PDN impedance across frequency, met by a team of caps + planes.",
                ),
                q(
                    "Why does a signal's reference plane need to be continuous (no splits) beneath it?",
                    (
                        opt(
                            "Return current flows in the plane right under the trace; a gap forces a detour that adds inductance, noise, and EMI",
                            correct=True,
                        ),
                        opt("Planes are only for mechanical support"),
                        opt("It changes the clock frequency"),
                        opt("Splits make signals faster"),
                    ),
                    "Every signal's return current loops through the nearest plane; a plane gap breaks that path — a major SI/PI/EMC problem.",
                ),
                q(
                    "What is the headline benefit of differential signaling?",
                    (
                        opt(
                            "Common-mode rejection: noise/crosstalk coupling equally onto both traces cancels when the receiver takes the difference",
                            correct=True,
                        ),
                        opt("It uses only one wire"),
                        opt("It eliminates the need for a clock"),
                        opt("It requires no termination"),
                    ),
                    "Subtracting the pair cancels common noise; it also lowers EMI and allows smaller, faster swings — hence its dominance in fast I/O.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# signal-integrity-advanced
# ──────────────────────────────────────────────────────────────────────

_SI_ADVANCED = SeedCourse(
    slug="signal-integrity-advanced",
    title="Signal Integrity — Advanced",
    description=(
        "Multi-gigabit links and sign-off: SerDes and equalization (FFE/CTLE/DFE), "
        "interconnect delay modeling, S-parameters and insertion loss, channel "
        "modeling, simultaneous switching noise, and the measurement/simulation "
        "toolchain. With runnable Elmore-delay and pre-emphasis labs."
    ),
    level="Advanced",
    lessons=(
        _t(
            "High-speed serial links & SerDes",
            "11 min",
            r"""# High-speed serial links & SerDes

Modern interfaces abandoned wide parallel buses (skew between many bits became
unmanageable) for **high-speed serial links**: a few **differential lanes** each
running at multi-Gbps, with the clock **embedded** in the data. The block that
does this is the **SerDes** (Serializer/Deserializer) — the heart of PCIe, USB,
Ethernet, SATA, HDMI, and chip-to-chip links.

The serial link pipeline:

```
parallel data → [serialize] → [TX equalizer] → channel (lossy!) → [RX equalizer]
              → [CDR: clock-data recovery] → [deserialize] → parallel data
```

The defining challenge: at 10–100+ Gbps, the channel (the very traces, vias, and
connectors of this track) has **severe loss** — often **20–40 dB** at the Nyquist
frequency — so the eye at the receiver is **completely closed** before any
processing. The link works only because of aggressive **equalization** (next
lessons) that undoes the channel's filtering.

Key SerDes concepts:

- **Embedded clock & CDR** — there's no separate clock line; the receiver's
  **Clock-Data Recovery** extracts timing from the data edges, so the data must be
  **DC-balanced** with enough transitions (via **line coding**: 8b/10b, 64b/66b, or
  **scrambling**) — long runs of identical bits would starve the CDR.
- **Lanes & bonding** — bandwidth scales by adding lanes (PCIe ×1, ×4, ×16).
- **Modulation** — beyond 2-level **NRZ**, modern links use **PAM4** (4 levels, 2
  bits/symbol) to double data rate within the same bandwidth — at the cost of
  smaller eyes and tighter noise margins (three eyes, ⅓ the spacing).

The mindset shift for advanced SI: you no longer aim for a "clean" signal at the
pins — the channel **will** close the eye. Instead you **co-design the channel and
the equalization** so that, after the receiver's processing, the **recovered** eye
meets the BER target. SI sign-off becomes **statistical link analysis** (millions
of bits, BER bathtub curves) rather than looking at a single waveform. Equalization
is what makes it possible — starting next.
""",
        ),
        _code(
            "Interconnect delay (Elmore)",
            "12 min",
            r"""# Before a signal even reflects, the RC of an interconnect adds DELAY. The Elmore
# delay model estimates the delay of an RC tree as a sum of (resistance to a node)
# x (downstream capacitance). Compute it for a simple RC line split into segments.
# Uses builtins.

# Model a wire as N segments, each with resistance r and capacitance c, driving a
# load cap at the end. Elmore delay to the end node = sum over segments of
# R_upstream_through_segment * C_downstream.
segments = 5
r_seg = 10.0      # ohms per segment
c_seg = 0.2       # pF per segment
c_load = 1.0      # pF load at the far end

# Node k (1..segments) sees resistance = k*r_seg from the source.
# Downstream cap at node k = remaining segment caps + load.
elmore = 0.0
for k in range(1, segments + 1):
    r_to_node = k * r_seg
    downstream_c = (segments - k) * c_seg + c_load + c_seg
    elmore = elmore + r_seg * (((segments - k) * c_seg) + c_load)  # contribution of this seg's R
print("RC line: %d segments, r=%.0f ohm, c=%.1f pF each, load=%.1f pF" % (segments, r_seg, c_seg, c_load))

# Cleaner formulation: delay = sum_i R_i * (sum of caps downstream of i)
total = 0.0
caps = [c_seg] * segments
caps[segments - 1] = caps[segments - 1] + c_load     # add load at the end
for i in range(segments):
    downstream = 0.0
    for j in range(i, segments):
        downstream = downstream + caps[j]
    total = total + r_seg * downstream
print("Elmore delay (R in ohm, C in pF) =", round(total, 2), "ohm*pF =", round(total, 2), "ps")

# Delay grows ~ quadratically with length (more R AND more downstream C) -> why
# long on-chip wires are buffered into segments to break the RC^2 growth.
print("doubling the segments roughly QUADRUPLES delay -> insert buffers/repeaters.")
""",
        ),
        _t(
            "S-parameters & insertion loss",
            "10 min",
            r"""# S-parameters & insertion loss

At gigahertz frequencies you can't probe voltages and currents directly inside a
network, so high-speed channels are characterised by **S-parameters** (scattering
parameters) — measured with a **Vector Network Analyzer (VNA)**. S-parameters
describe a network entirely in terms of **incident and reflected waves** at its
**ports**, which is exactly the language of the reflections you studied.

For a 2-port (e.g. a channel from TX to RX), the four S-parameters are:

- **S11 — return loss / input reflection.** How much of an incident wave bounces
  back from port 1. This is the **reflection coefficient Γ** vs frequency; you want
  it **low** (very negative in dB → little reflection → good match).
- **S21 — insertion loss / forward transmission.** How much signal gets **through**
  from port 1 to port 2. For a channel you want it **close to 0 dB** (low loss); at
  multi-Gbps it droops badly at high frequency (the loss/dispersion of earlier
  lessons).
- **S22** — output reflection (like S11, the other side).
- **S12** — reverse transmission (isolation).

S-parameters are quoted in **dB** vs frequency:

```
dB = 20 · log10(|S|)
S21 = 0 dB  -> lossless pass-through
S21 = -20 dB -> only 10% of the voltage gets through (big loss)
S11 = -20 dB -> good match (only 10% reflected)
```

The **insertion-loss profile S21(f)** *is* the channel's frequency response — read
off the loss at the **Nyquist frequency** (half the bit rate) to know how much
equalization you'll need. For differential channels there are **mixed-mode**
S-parameters (SDD21 = differential insertion loss, SCD21 = mode conversion, etc.)
that separately quantify the differential signal and the harmful diff↔common
conversion.

Why this matters: S-parameters are the **common currency** between measurement
(VNA), simulation (field solvers export S-parameter "Touchstone" files), and
link analysis. You hand an S-parameter channel model to a SerDes simulator, it
applies the equalization, and predicts the eye/BER. Mastering "read the S21 loss
and the S11 match vs frequency" is the core skill of advanced channel work.
""",
        ),
        _t(
            "Equalization: FFE, CTLE & DFE",
            "11 min",
            r"""# Equalization: FFE, CTLE & DFE

If the channel is a low-pass filter that closes the eye, **equalization** is the
inverse filter that opens it back up — boosting the high frequencies the channel
attenuated (or cancelling the resulting ISI). It's what makes multi-gigabit links
possible over lossy copper. Three workhorses, used together:

- **FFE — Feed-Forward Equalizer (TX, also called pre-emphasis/de-emphasis).** A
  short digital FIR filter at the **transmitter** that **pre-distorts** the signal:
  it **boosts the edges** (or de-emphasizes steady bits) so that, after the channel
  flattens them, the received signal is correct. Simple and effective, but it
  **can't add power** — boosting highs effectively cuts the lows, and it amplifies
  nothing the channel already killed entirely.

- **CTLE — Continuous-Time Linear Equalizer (RX).** An **analog** filter at the
  **receiver** with a high-frequency peaking response that **mirrors the inverse**
  of the channel's loss — flattening the overall response. Low-power and handles a
  lot of loss, but, being linear, it **also boosts high-frequency noise and
  crosstalk**.

- **DFE — Decision-Feedback Equalizer (RX).** A **non-linear** equalizer: it uses
  the **already-decided previous bits** to subtract their known ISI contribution
  from the current bit. Because it feeds back *decisions* (not the noisy signal),
  it cancels ISI **without amplifying noise** — its key advantage — but it can
  **propagate errors** (a wrong decision corrupts the next) and can't fix
  **pre-cursor** ISI (only post-cursor).

A real link **stacks** them: **TX FFE + RX CTLE + RX DFE**, often **adaptive**
(coefficients auto-tuned to the specific channel during link training, e.g. PCIe
equalization negotiation).

```
TX:  data → FFE (pre-emphasis) → channel (loss) → RX: CTLE (analog boost) → DFE (ISI cancel) → CDR
```

The conceptual takeaway: the channel and the equalizer are **co-designed** so their
**combined** response is flat enough to meet the BER target. Equalization trades
silicon complexity and power for the ability to push more bits through cheap, lossy
copper — which is why every modern SerDes is mostly equalization. You'll see TX
pre-emphasis sharpen a smeared pulse next.
""",
        ),
        _code(
            "TX pre-emphasis (FFE)",
            "13 min",
            r"""# A feed-forward equalizer (FFE) at the transmitter pre-distorts the signal so
# the lossy channel's output is correct. Here a 2-tap FFE boosts edges; we pass a
# bit pattern through a smearing channel with and without FFE and compare the eye.
# Uses numpy.

import numpy as np

bits = np.array([0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0], dtype=float)
spb = 8
signal = np.repeat(bits, spb)

# Channel: low-pass smear (loss/ISI) via a moving average.
chan = np.ones(5) / 5.0

# --- No equalization ---
out_plain = np.convolve(signal, chan, mode="same")

# --- 2-tap FFE pre-emphasis: y[n] = (1+a)*x[n] - a*x[n-1] boosts transitions ---
a = 0.6
pre = np.zeros(len(signal))
pre[0] = (1.0 + a) * signal[0]
for n in range(1, len(signal)):
    pre[n] = (1.0 + a) * signal[n] - a * signal[n - 1]
out_ffe = np.convolve(pre, chan, mode="same")

# Measure eye opening: min(sampled 1s) - max(sampled 0s) at bit centres.
centers = np.arange(spb // 2, len(signal), spb)
def eye(sig, centers, bits):
    s = sig[centers]
    ones = s[bits[: len(s)] == 1]
    zeros = s[bits[: len(s)] == 0]
    return float(ones.min() - zeros.max())

eye_plain = eye(out_plain, centers, bits)
eye_ffe = eye(out_ffe, centers, bits)
print("eye opening WITHOUT FFE: %.3f" % eye_plain)
print("eye opening WITH 2-tap FFE (a=%.1f): %.3f" % (a, eye_ffe))
print("improvement: %.1f%%" % (100.0 * (eye_ffe - eye_plain) / abs(eye_plain)))
print("pre-emphasis boosts the edges the channel attenuates -> the eye opens.")
""",
        ),
        _t(
            "Power integrity & simultaneous switching noise",
            "10 min",
            r"""# Power integrity & simultaneous switching noise

The Intermediate course introduced the PDN; at advanced data rates, **power
integrity (PI)** becomes one of the hardest sign-off problems, and its sharpest
form is **Simultaneous Switching Noise (SSN)**, also called **ground bounce**.

**SSN / ground bounce.** When **many** output drivers switch **at the same instant**
(e.g. a whole bus toggling), they pull a large, fast current spike `ΔI` through the
**inductance** of the shared power/ground path (package leads, vias, bond wires).
By `V = L·dI/dt`, that creates a **voltage glitch** on the chip's internal power and
ground references:

```
many drivers switch → big dI/dt → V = L·(dI/dt) across package/plane inductance
→ the chip's "ground" momentarily bounces → quiet signals glitch, timing shifts
```

Consequences: a "quiet" output can show a false glitch, input thresholds shift,
and timing margins erode — all worsening as buses get wider and edges faster.

Mitigations attack the **L·dI/dt** terms:

- **Reduce inductance L** — more power/ground pins and vias in parallel, on-package
  and on-die decoupling **close** to the switching circuits, low-inductance cap
  mounting. (On-die capacitance is the last line of defense at GHz.)
- **Reduce dI/dt** — **edge-rate control** (slew-limited drivers), and **stagger**
  switching so not everything toggles on the same clock edge.
- **Solid, low-impedance planes** and short return paths.

Advanced PI analysis treats the **PDN impedance vs frequency** profile (the Z_target
curve from before) and hunts for **anti-resonances** — frequency peaks where a
capacitor's inductance resonates with plane/other-cap capacitance, creating an
impedance spike. If a switching harmonic lands on an anti-resonance, ripple
explodes. The cure is a **spread of capacitor values** and good placement to keep
the impedance below target across the whole band.

The advanced view ties PI and SI together through the same physics: **inductance
and return paths**. Clean power needs low-inductance distribution and decoupling;
clean signals need continuous return paths — and SSN is what happens when fast,
correlated currents meet path inductance. Designing the PDN impedance profile is
now as much a part of high-speed sign-off as the channel itself.
""",
        ),
        _t(
            "Measurement & simulation",
            "10 min",
            r"""# Measurement & simulation

Advanced SI is verified with a **toolchain** that spans simulation (before the
board exists) and measurement (after), all speaking the common language of waves,
eyes, and S-parameters.

**Simulation — predict before you build:**

- **2D/3D field solvers** extract the **impedance and S-parameters** of traces,
  vias, and connectors from the physical geometry and material properties — the
  bridge from layout to electrical model.
- **IBIS models** describe a driver/receiver's behaviour (I/V and switching
  characteristics) **without revealing the vendor's transistor netlist** — the
  standard way to simulate chip I/O in SI tools. **IBIS-AMI** adds the SerDes
  **equalization algorithms** so simulators can run millions of bits for
  **statistical link/BER analysis**.
- **SPICE** for detailed transistor/analog behaviour where needed.
- The flow: field solver → channel S-parameters → IBIS/AMI driver+RX → eye/BER
  prediction.

**Measurement — verify the real thing:**

- **TDR (Time-Domain Reflectometry)** — launches a fast step and watches the
  reflections in time to **locate and quantify impedance discontinuities** along a
  trace (a bump at a connector, an impedance dip at a via) — a "radar" for the
  board.
- **VNA (Vector Network Analyzer)** — measures **S-parameters** vs frequency
  (insertion loss S21, return loss S11) — the frequency-domain truth of the
  channel.
- **High-bandwidth real-time / sampling scopes** with SI software capture the
  **eye diagram**, **jitter** decomposition, and **BER bathtub** on the live link.
- **BERT (Bit Error Rate Tester)** drives a known pattern and counts errors
  directly, mapping the **bathtub curve**.

The professional reality: you **simulate to design** (catch problems when fixes are
free — choosing stackup, impedance, termination, equalization) and **measure to
verify** (TDR/VNA/scope/BERT to confirm the hardware matches prediction and to
debug surprises). Mastery of SI is ultimately about **closing the loop** between a
geometry, its electrical model, and the measured eye — so that a multi-gigabit link
hits its BER target with margin, on real, manufacturable, affordable boards.
""",
        ),
        quiz_lesson(
            "Quiz: SerDes, S-parameters & Equalization",
            (
                q(
                    "Why do high-speed serial links rely so heavily on equalization?",
                    (
                        opt(
                            "At multi-Gbps the channel loss is so high the eye is closed at the receiver; equalization undoes the channel's filtering to recover it",
                            correct=True,
                        ),
                        opt("Because the clock is too slow"),
                        opt("To save board space"),
                        opt("Equalization is optional and rarely used"),
                    ),
                    "Channels can lose 20–40 dB at Nyquist, closing the eye; TX FFE + RX CTLE/DFE reopen it so the recovered signal meets the BER target.",
                ),
                q(
                    "What does the S-parameter S21 tell you about a channel?",
                    (
                        opt(
                            "Insertion loss — how much signal gets through vs frequency (you want it near 0 dB)",
                            correct=True,
                        ),
                        opt("The DC resistance"),
                        opt("The clock frequency"),
                        opt("The number of vias"),
                    ),
                    "S21 is forward transmission/insertion loss; S11 is return loss (match). The S21(f) droop at Nyquist sets how much EQ you need.",
                ),
                q(
                    "What is the key advantage of a Decision-Feedback Equalizer (DFE)?",
                    (
                        opt(
                            "It cancels ISI using already-decided bits, so it doesn't amplify noise (unlike a linear equalizer)",
                            correct=True,
                        ),
                        opt("It adds power to the signal"),
                        opt("It fixes pre-cursor ISI perfectly"),
                        opt("It needs no decisions"),
                    ),
                    "DFE subtracts known ISI from prior decisions (no noise boost), though it risks error propagation and only handles post-cursor ISI.",
                ),
                q(
                    "Why does Elmore/RC delay of a wire grow roughly quadratically with length?",
                    (
                        opt(
                            "A longer wire has both more series resistance and more downstream capacitance, and delay ~ R×C of the tree",
                            correct=True,
                        ),
                        opt("Because resistance decreases with length"),
                        opt("Because of reflections only"),
                        opt("It actually grows linearly"),
                    ),
                    "Both R and downstream C scale with length, so RC delay ~ length²; long on-chip wires are buffered into segments to linearise it.",
                ),
                q(
                    "What causes simultaneous switching noise (ground bounce)?",
                    (
                        opt(
                            "Many drivers switching at once create a large dI/dt across power/ground path inductance: V = L·dI/dt glitches the references",
                            correct=True,
                        ),
                        opt("Too little switching activity"),
                        opt("A perfectly continuous ground plane"),
                        opt("Low clock frequency"),
                    ),
                    "Correlated fast currents through package/plane inductance bounce the chip's power/ground; cures reduce L (more pins/decoupling) and dI/dt (slew control, staggering).",
                ),
                q(
                    "What does a TDR (Time-Domain Reflectometer) measure?",
                    (
                        opt(
                            "Impedance discontinuities located along a trace, by sending a step and timing its reflections",
                            correct=True,
                        ),
                        opt("The frequency-domain insertion loss"),
                        opt("The bit error rate"),
                        opt("The power consumption"),
                    ),
                    "TDR is a 'radar' for interconnect: reflections in time reveal where and how much the impedance deviates (connector bumps, via dips). VNA gives the frequency-domain S-parameters.",
                ),
            ),
        ),
    ),
)


SIGNAL_INTEGRITY_COURSES = (_SI_BASICS, _SI_INTERMEDIATE, _SI_ADVANCED)
