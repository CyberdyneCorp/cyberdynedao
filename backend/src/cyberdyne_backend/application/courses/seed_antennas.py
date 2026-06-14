"""Academy seed content — the Antennas & Propagation track (Beginner → Advanced).

* ``antennas-basics``        — antenna parameters, patterns, gain, the dipole, Friis & path loss
* ``antennas-intermediate``  — antenna types, arrays & the array factor, beamforming, propagation, fading, link budget
* ``antennas-advanced``      — channel models, MIMO, mmWave & massive MIMO, measurement, numerical methods, smart antennas

Runnable ``code`` lessons use Python + numpy (validated inline) to compute
directivity/beamwidth, dipole patterns, Friis link budgets, array factors with
beam steering, the two-ray model, log-distance path loss, and massive-MIMO gain.
The **equivalent MATLAB** appears as read-only blocks (validated to run in the
MATLAB REPL). Interactive plots include a slider-driven array factor. Part of the
Electronic Engineering curriculum.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, λ, θ, ψ, °, ², ×, Ω) in diagrams.
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
# antennas-basics
# ──────────────────────────────────────────────────────────────────────

_ANT_BASICS = SeedCourse(
    slug="antennas-basics",
    title="Antennas & Propagation — Basics",
    description=(
        "How antennas turn signals into radio waves and back: radiation patterns, "
        "beamwidth, directivity and gain, impedance and polarization, the dipole, "
        "and free-space propagation via the Friis equation. With runnable Python "
        "labs, MATLAB equivalents, and an interactive dipole pattern."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is an antenna?",
            "10 min",
            r"""# What is an antenna?

An **antenna** is a **transducer** between guided waves and free space: it converts
the currents and voltages travelling on a transmission line into **electromagnetic
waves** radiating through space (transmit), and vice-versa (receive). Without it,
the energy your transmitter generates would never leave the wire.

**The physics in one idea:** radiation comes from **accelerating charges**. A
steady DC current doesn't radiate; a **time-varying** current (especially where it
changes direction, like the ends of a wire) launches EM waves. So an antenna is
shaped to make currents oscillate over a structure comparable in size to the
**wavelength** λ = c/f — which is why antenna size scales with wavelength (a
half-wave dipole at 100 MHz is 1.5 m; at 6 GHz it's 2.5 cm).

**Reciprocity** is a beautiful and practical theorem: an antenna's properties
(pattern, gain, impedance) are **identical** whether it transmits or receives. So
you can analyze whichever is easier, and a good transmit antenna is an equally good
receive antenna. (This is why we draw one radiation pattern and use it both ways.)

**Near field vs far field.** Close to the antenna (the **reactive near field**) the
fields are complex and store energy; what we usually care about is the **far field**
(the **Fraunhofer region**), beyond roughly `2D²/λ` (D = antenna size), where the
wave looks like a clean outgoing spherical wave, the pattern shape is fixed, and
power falls off as **1/r²**. Antenna specs (gain, pattern) are far-field quantities.

```
  transmission line          antenna           free space
  ───────────────────►   [ oscillating ]   ~~~~~► EM wave (far field, ∝ 1/r)
   guided wave             current
```

**Key intuition for the whole track:** an antenna doesn't *amplify* — it **shapes
and directs** the energy it's given. A "high-gain" antenna isn't louder overall;
it **concentrates** radiation into a narrower beam (more in one direction, less in
others), exactly like a flashlight reflector focuses the same bulb. Everything that
follows — patterns, directivity, arrays, beamforming — is about **controlling where
the energy goes** and understanding **how it propagates** once it leaves. We start
by quantifying the radiation pattern.
""",
        ),
        _t(
            "Radiation pattern, beamwidth, directivity & gain",
            "11 min",
            r"""# Radiation pattern, beamwidth, directivity & gain

The **radiation pattern** is the antenna's signature: how radiated power varies
with **direction**. Plotted (often in polar form) it shows a **main lobe** (the
beam), **side lobes**, and **nulls** (directions of (near-)zero radiation).

**Beamwidth** measures how focused the main lobe is:

- **HPBW (Half-Power Beamwidth)** — the angular width between the points where power
  drops to **half** its peak (**−3 dB**). The headline "how narrow is the beam"
  number.
- **FNBW** — first-null beamwidth (between the nulls bounding the main lobe).

**Directivity (D)** quantifies focusing: how much more power the antenna radiates in
its best direction than an **isotropic** radiator (a hypothetical point that
radiates equally everywhere) would, for the **same total power**:

$$ D = \frac{4\pi \cdot U_{\max}}{P_{\text{rad}}} = \frac{4\pi}{\Omega_A} $$

where Ω_A is the **beam solid angle**. Narrower beam → smaller Ω_A → **higher
directivity**. A handy estimate for a pencil beam: `D ≈ 41253 / (HPBW_E · HPBW_H)`
(beamwidths in degrees). Directivity is **dimensionless**; in dB it's **dBi**
("dB relative to isotropic").

**Gain (G)** is directivity **including losses**: `G = e · D`, where **e** is the
**radiation efficiency** (fraction of input power actually radiated, not lost to
conductor/dielectric heating). Gain is what a link budget uses. So:

```
Directivity  = pure focusing (ideal, lossless)
Gain         = focusing × efficiency  (what you actually get)  → dBi
```

Two reference units you'll see: **dBi** (vs isotropic) and **dBd** (vs a half-wave
dipole); `dBi = dBd + 2.15` (a dipole has 2.15 dBi gain).

**The conservation principle:** an antenna can't create energy, so **higher gain
means a narrower beam** — you buy directivity in one direction by giving it up
elsewhere. A satellite dish (huge gain, pencil beam) must be aimed precisely; a
phone antenna (low gain, near-omnidirectional) works in any orientation but reaches
less far. Choosing the pattern/gain is a fundamental antenna design trade-off.

You'll compute directivity and HPBW from a pattern next — and the relationship
"narrower beam ⇒ higher directivity" is the thread running through arrays and
beamforming later.
""",
        ),
        _code(
            "Directivity & beamwidth from a pattern",
            "13 min",
            r"""# From a radiation pattern you can extract the two headline numbers: HPBW (the
# -3 dB beamwidth) and directivity D = 4*pi*Umax / Prad. Compute them for a simple
# directional pattern by sampling and integrating. Uses numpy.

import numpy as np

# A directional power pattern with rotational symmetry about the axis:
# P(theta) = cos(theta)^(2n) for theta in [0, 90deg], zero beyond -> a 'cosine' beam.
n = 3
theta = np.linspace(0.0, np.pi, 1801)            # 0..180 deg, fine grid
power = np.where(theta <= np.pi / 2, np.cos(theta) ** (2 * n), 0.0)
power = power / power.max()                       # normalise peak to 1

# HPBW: angular width where power >= 0.5 (the -3 dB points).
above_half = theta[power >= 0.5]
hpbw_deg = float(np.degrees(above_half.max() - above_half.min()))

# Directivity: D = 4*pi*Pmax / integral(P dOmega), with dOmega = sin(theta) dtheta dphi.
# Phi-symmetric, so integral = 2*pi * integral(P*sin(theta) dtheta).
integrand = power * np.sin(theta)
area = float(np.sum((integrand[:-1] + integrand[1:]) * 0.5 * np.diff(theta)))  # trapezoid
beam_solid_angle = 2.0 * np.pi * area
directivity = 4.0 * np.pi / beam_solid_angle

print("cosine^%d pattern:" % (2 * n))
print("  HPBW       = %.1f deg" % hpbw_deg)
print("  directivity = %.2f = %.2f dBi" % (directivity, 10.0 * float(np.log10(directivity))))
print()
print("  rule-of-thumb D ~= 41253 / (HPBW_E * HPBW_H) =", round(41253.0 / (hpbw_deg * hpbw_deg), 2))
print("a narrower beam (bigger n) -> smaller beam solid angle -> higher directivity.")
""",
        ),
        _t(
            "Impedance, VSWR, bandwidth & polarization",
            "11 min",
            r"""# Impedance, VSWR, bandwidth & polarization

Pattern and gain describe *where* energy goes; these parameters describe how
**efficiently** the antenna accepts energy from the line and the **orientation** of
the wave it launches.

**Input impedance & matching.** An antenna presents an **input impedance**
`Z_A = R_A + jX_A` to the feed line. For maximum power transfer it must **match**
the line (usually 50 Ω): a mismatch reflects power back (the **reflection
coefficient Γ** and **VSWR** from the Signal Integrity track — same physics). The
resistance has two parts: **radiation resistance R_r** (the "useful" part —
represents radiated power) and **loss resistance R_L** (heat). Antenna design and
**matching networks** bring Z_A to 50 Ω at the operating frequency.

- **Return loss / VSWR** — how good the match is. **VSWR ≤ 2:1** (return loss
  ≥ ~10 dB, ~11% reflected) is a common "well-matched" bar.

**Bandwidth.** The range of frequencies over which the antenna performs acceptably
(match, gain, pattern all within spec). A **resonant** antenna (dipole, patch) is
inherently **narrowband**; **broadband** antennas (log-periodic, spiral, horn,
Vivaldi) trade size/complexity for wide bandwidth. Bandwidth is quoted as a percent
of center frequency, or an absolute range.

**Efficiency (e).** The fraction of input power actually radiated:
`e = R_r / (R_r + R_L)`. Electrically **small** antennas (much smaller than λ, like
a phone's) have **low radiation resistance**, so loss resistance dominates and
efficiency suffers — a fundamental limit (Chu's limit) on tiny antennas. This is
why miniaturization is hard and why efficiency, not just gain, matters.

**Polarization** — the orientation of the wave's **electric field**:

- **Linear** (vertical or horizontal) — most common; **transmit and receive
  antennas must match orientation** or you suffer **polarization loss** (cross-
  polarized = up to total loss in theory; that's why you align antennas).
- **Circular** (RHCP/LHCP) — the E-field rotates; robust to orientation (great for
  satellites/GPS where the link geometry changes), but pairing opposite senses
  loses ~3 dB or more.

**The complete antenna spec** therefore combines: **pattern/gain** (where + how
focused), **impedance/VSWR/bandwidth** (how well it accepts power, over what
frequencies), **efficiency** (how much is radiated vs lost), and **polarization**
(field orientation). A real antenna choice balances all of these against size and
cost — e.g. a phone antenna sacrifices gain and efficiency for tiny size and
broad pattern, while a dish maximizes gain at the cost of size and narrow beam.
Next: the workhorse antenna that makes these concrete — the dipole.
""",
        ),
        _t(
            "The dipole & monopole",
            "10 min",
            r"""# The dipole & monopole

The **half-wave dipole** is the canonical antenna — simple, efficient, and the
reference against which others are measured (dBd). It's a straight conductor about
**λ/2** long, fed at the center.

**Why λ/2?** At half a wavelength the current distribution forms a **standing wave**
with a current **maximum at the center** (the feed) and **zeros at the ends** —
an efficient, resonant radiator. At resonance its input impedance is conveniently
near **73 Ω** (mostly radiation resistance, small reactance) — close to common feed
lines, so it matches well with minimal effort.

Its **radiation pattern**:

```
        z (dipole axis)
        │
   ╭────┼────╮         doughnut-shaped pattern:
  (     ●     )        - max radiation BROADSIDE (perpendicular to the wire)
   ╰────┼────╯         - NULLS along the wire axis (off the ends)
        │              - omnidirectional in the plane perpendicular to the wire
```

So a vertical dipole radiates equally in all **horizontal** directions (great for
broadcast/base stations) and nothing straight up/down. Its key numbers:
**HPBW ≈ 78°**, **directivity ≈ 1.64 (2.15 dBi)** — modest focusing, because the
doughnut is broad.

**The monopole** is "half a dipole": a **λ/4** vertical element over a **ground
plane**, which acts as a mirror to create the missing half by **image theory**. A
quarter-wave monopole over a perfect ground behaves like a dipole's upper half:
~**36 Ω** input impedance, and it radiates into the **upper hemisphere** (with the
ground plane as the reference). Monopoles are everywhere — car whip antennas,
the classic "rubber duck," and ground-plane-backed PCB antennas — because they're
half the size of a dipole and use the chassis/ground as the other half.

**Shortening & loading.** When λ/4 is still too big (low frequencies, small
devices), antennas are physically shortened and **loaded** (helical/meander
"rubber duck," loading coils) — recovering resonance at the cost of **bandwidth and
efficiency** (the small-antenna trade-off).

The dipole/monopole teach the core relationships you'll reuse: **length ↔
resonance ↔ impedance**, **current distribution ↔ pattern**, and the **broadside
doughnut** shape. They're also the **elements** that arrays combine to build high
gain (next course). You'll compute the half-wave dipole's exact pattern, HPBW, and
directivity next — and see the famous 2.15 dBi fall out.
""",
        ),
        _code(
            "Half-wave dipole radiation pattern",
            "13 min",
            r"""# The half-wave dipole's far-field pattern has the classic closed form
# E(theta) = cos((pi/2)*cos theta) / sin theta. Compute it, find the HPBW (~78 deg)
# and directivity (~2.15 dBi) -- the textbook numbers. Uses numpy.

import numpy as np

# theta measured from the dipole axis; avoid the exact 0/pi endpoints (nulls).
theta = np.linspace(0.001, np.pi - 0.001, 1801)
e_field = np.abs(np.cos((np.pi / 2.0) * np.cos(theta)) / np.sin(theta))
power = e_field ** 2
power = power / power.max()                       # peak (broadside, 90 deg) -> 1

# HPBW: width of the region with power >= 0.5.
above_half = theta[power >= 0.5]
hpbw_deg = float(np.degrees(above_half.max() - above_half.min()))

# Directivity (phi-symmetric): D = 4*pi / [2*pi * integral(P sin theta dtheta)].
integrand = power * np.sin(theta)
area = float(np.sum((integrand[:-1] + integrand[1:]) * 0.5 * np.diff(theta)))  # trapezoid
beam_solid_angle = 2.0 * np.pi * area
directivity = 4.0 * np.pi / beam_solid_angle

print("half-wave dipole (E = cos((pi/2)cos T)/sin T):")
print("  peak radiation at theta = 90 deg (broadside), nulls along the axis")
print("  HPBW        = %.1f deg   (textbook ~ 78 deg)" % hpbw_deg)
print("  directivity = %.3f = %.2f dBi   (textbook ~ 2.15 dBi)"
      % (directivity, 10.0 * float(np.log10(directivity))))
print()
print("the broad 'doughnut' gives modest directivity; arrays of dipoles do far better.")
""",
        ),
        _t(
            "Free-space propagation & the Friis equation",
            "11 min",
            r"""# Free-space propagation & the Friis equation

Once a wave leaves the antenna, **how much power reaches the receiver?** In free
space (no obstacles, line-of-sight) the answer is the **Friis transmission
equation** — the foundation of every link budget.

The received power:

$$ P_r = P_t \, G_t \, G_r \left(\frac{\lambda}{4\pi d}\right)^2 $$

where P_t is transmit power, G_t/G_r the antenna gains, λ the wavelength, and d the
distance. In **dB** (how engineers actually use it) it becomes a simple sum:

$$ P_r[\text{dBm}] = P_t + G_t + G_r - \text{FSPL} $$

with the **Free-Space Path Loss**:

$$ \text{FSPL[dB]} = 20\log_{10}\!\left(\frac{4\pi d}{\lambda}\right) = 20\log_{10} d + 20\log_{10} f + 32.45 $$

(d in km, f in MHz, for the last form). Two consequences everyone must internalize:

- **Power falls as 1/d²** (inverse-square law) → FSPL rises **20 dB per decade** of
  distance. **Doubling the distance loses 6 dB**; 10× distance loses 20 dB.
- **Higher frequency = more path loss** (for fixed antenna *gains*): FSPL ∝ f²
  because λ shrinks (the **λ²** in Friis). This is a key reason mmWave/5G needs
  high-gain beamforming — the raw path loss at 28 GHz is brutal. (Note: a fixed-
  *aperture* antenna actually gains with frequency, which partly offsets this — but
  for fixed gain, higher f means more loss.)

```plot
{"title": "Free-space path loss vs distance (2.4 GHz)", "xLabel": "distance (m)", "yLabel": "FSPL (dB)", "xRange": [1, 1000], "yRange": [0, 110], "functions": [{"expr": "20*log10(4*pi*x/0.125)", "label": "FSPL = 20·log10(4πd/λ)", "color": "#2563eb"}]}
```

**Why the inverse-square law?** A transmitter spreads its power over the surface of
an expanding sphere (area ∝ d²); a receive antenna captures a fixed slice, so the
fraction caught ∝ 1/d². The **antenna gains** focus more of that power toward the
receiver (and the receive antenna's **effective aperture** `A_e = Gλ²/4π` captures
more), which is why **gain directly buys range**: every dB of antenna gain is a dB
of link margin.

Friis is the **ideal** (free space, far field, matched, polarization-aligned, no
obstacles). Real links add obstacles, reflections, and fading (next course), but
Friis sets the **baseline** and is the first calculation in any wireless design.

The same link budget in **MATLAB** (run it in the MATLAB REPL):

```matlab
Pt = 20; Gt = 6; Gr = 6;            % dBm, dBi, dBi
f = 2.4e9; c = 3e8; lam = c/f;      % wavelength (m)
d = [1 10 100 1000 10000];          % distances (m)
FSPL = 20*log10(4*pi*d/lam);        % free-space path loss (dB)
Pr = Pt + Gt + Gr - FSPL;           % received power (dBm)
disp('distances (m):');  disp(d)
disp('FSPL (dB):');      disp(FSPL)
disp('Pr (dBm):');       disp(Pr)
```

You'll build the same Friis link budget in Python — runnable inline — next.
""",
        ),
        _code(
            "Friis link budget (Python + MATLAB)",
            "13 min",
            r"""# The Friis equation predicts received power over a free-space link:
#   Pr[dBm] = Pt + Gt + Gr - FSPL,   FSPL = 20*log10(4*pi*d/lambda).
# Compute a link budget vs distance. (The MATLAB equivalent is shown read-only in
# the lesson text for the MATLAB REPL.) Uses numpy.

import numpy as np

pt_dbm = 20.0      # transmit power (dBm) = 100 mW
gt_dbi = 6.0       # transmit antenna gain
gr_dbi = 6.0       # receive antenna gain
f_hz = 2.4e9       # 2.4 GHz
c = 3.0e8
lam = c / f_hz
sensitivity = -90.0   # receiver sensitivity (dBm) -> minimum usable Pr

print("Pt=%.0f dBm, Gt=%.0f dBi, Gr=%.0f dBi, f=%.1f GHz, lambda=%.3f m" % (pt_dbm, gt_dbi, gr_dbi, f_hz / 1e9, lam))
print(" dist(m)   FSPL(dB)   Pr(dBm)   margin(dB)")
for d in [1, 10, 100, 1000, 10000]:
    fspl = 20.0 * float(np.log10(4.0 * np.pi * d / lam))
    pr = pt_dbm + gt_dbi + gr_dbi - fspl
    margin = pr - sensitivity
    flag = "" if margin >= 0 else "  <-- below sensitivity!"
    print("  %-7d  %7.1f   %7.1f   %+8.1f%s" % (d, fspl, pr, margin, flag))

print()
print("doubling distance adds ~6 dB loss; +1 dB of antenna gain = +1 dB of margin.")
print("(the same calculation in MATLAB is shown in the lesson, for the MATLAB REPL.)")
""",
        ),
        quiz_lesson(
            "Quiz: Antenna Fundamentals",
            (
                q(
                    "What does an antenna fundamentally do?",
                    (
                        opt(
                            "Transduce guided waves to/from free-space EM waves, shaping and directing (not amplifying) the energy",
                            correct=True,
                        ),
                        opt("Amplify the total radiated power"),
                        opt("Generate electrical energy"),
                        opt("Convert AC to DC"),
                    ),
                    "An antenna is a transducer; 'gain' is concentration of energy into a beam (like a flashlight reflector), not amplification. Reciprocity makes TX/RX behaviour identical.",
                ),
                q(
                    "What is the difference between directivity and gain?",
                    (
                        opt(
                            "Gain = directivity × radiation efficiency; directivity is the ideal (lossless) focusing",
                            correct=True,
                        ),
                        opt("They are identical"),
                        opt("Gain ignores direction"),
                        opt("Directivity includes losses, gain does not"),
                    ),
                    "D measures focusing vs isotropic; G = e·D folds in losses (heat). Gain (dBi) is what a link budget uses.",
                ),
                q(
                    "What are the key numbers for a half-wave dipole?",
                    (
                        opt(
                            "~73 Ω input impedance, ~2.15 dBi directivity, ~78° HPBW, doughnut pattern with nulls along the axis",
                            correct=True,
                        ),
                        opt("50 Ω, 30 dBi, 1° HPBW"),
                        opt("0 Ω, 0 dBi, isotropic"),
                        opt("100 Ω, 10 dBi, pencil beam"),
                    ),
                    "The λ/2 dipole resonates near 73 Ω with a broad doughnut pattern: 2.15 dBi, ~78° HPBW, max broadside, nulls off the ends.",
                ),
                q(
                    "Why does higher antenna gain imply a narrower beam?",
                    (
                        opt(
                            "An antenna can't create energy, so concentrating power in one direction means radiating less elsewhere (smaller beam solid angle)",
                            correct=True,
                        ),
                        opt("Gain adds power from the supply"),
                        opt("Narrow beams use less bandwidth"),
                        opt("It doesn't — gain and beamwidth are unrelated"),
                    ),
                    "D = 4π/Ω_A: higher gain = smaller beam solid angle = narrower beam. A dish has huge gain but must be aimed precisely.",
                ),
                q(
                    "In the Friis equation, how does free-space path loss change with distance?",
                    (
                        opt(
                            "Power falls as 1/d² → FSPL rises 20 dB/decade; doubling distance loses 6 dB",
                            correct=True,
                        ),
                        opt("Power falls as 1/d → 10 dB/decade"),
                        opt("Loss is constant with distance"),
                        opt("Power increases with distance"),
                    ),
                    "The inverse-square law (power spread over a sphere of area ∝ d²) gives 20log10(d); ×2 distance = +6 dB loss, ×10 = +20 dB.",
                ),
                q(
                    "Why must transmit and receive antenna polarizations match?",
                    (
                        opt(
                            "Cross-polarization causes polarization loss (a vertically-polarized wave barely couples to a horizontal antenna)",
                            correct=True,
                        ),
                        opt("Polarization has no effect on a link"),
                        opt("Matching polarization reduces gain"),
                        opt("Only circular polarization matters"),
                    ),
                    "Linear polarizations must align or you lose power (up to a total null when orthogonal); circular polarization is robust to orientation but costs ~3 dB when sense-mismatched.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# antennas-intermediate
# ──────────────────────────────────────────────────────────────────────

_ANT_INTERMEDIATE = SeedCourse(
    slug="antennas-intermediate",
    title="Antennas & Propagation — Intermediate",
    description=(
        "Building gain and surviving the real channel: common antenna types, "
        "antenna arrays and the array factor, beamforming and phased arrays, "
        "propagation mechanisms (reflection/diffraction/scattering/multipath), "
        "fading, and practical link budgets. With an interactive array-factor "
        "plot and runnable array-steering and two-ray labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Antenna types",
            "10 min",
            r"""# Antenna types

Beyond the dipole, a zoo of antenna types each suits a job — the choice trades
**gain, bandwidth, size, polarization, and cost**. A working tour:

- **Dipole / monopole** — simple, omnidirectional-in-a-plane, low gain (~2 dBi).
  Broadcast, base stations, whips. (Previous course.)
- **Yagi-Uda** — a driven dipole plus parasitic **reflector** and **directors** that
  shape a **directional** beam (~7–15 dBi). The classic rooftop **TV antenna**;
  cheap directional gain, narrowband.
- **Patch / microstrip** — a metal patch over a ground plane on a PCB. **Low-profile,
  cheap, planar**, easily arrayed; modest gain (~6–9 dBi), narrowband. Ubiquitous in
  phones, GPS, Wi-Fi, and **arrays**.
- **Horn** — a flared waveguide; **broadband**, moderate-high gain (10–25 dBi),
  clean pattern. The standard **gain reference** and feed for dishes; radar,
  measurement.
- **Parabolic reflector (dish)** — a feed at the focus of a parabola; **very high
  gain** (30–50+ dBi), pencil beam. Satellite, radio astronomy, point-to-point
  microwave. Gain ∝ aperture area / λ².
- **Helical** — a coil; naturally **circularly polarized**, good for satellite/space
  links (axial mode).
- **Loop** — small loops are **magnetic** antennas (RFID, direction finding, AM
  receive); large (≈λ) loops radiate efficiently.
- **Log-periodic** — many scaled dipoles; **very broadband** directional (the
  wide-band cousin of the Yagi).
- **Slot / aperture, Vivaldi, dielectric resonator, fractal** — specialized planar/
  wideband/miniature forms.

**How to choose** (the engineering questions):

```
Need omnidirectional coverage?   -> dipole/monopole
Cheap directional gain?          -> Yagi
Flat, cheap, arrayable (phones)? -> patch (microstrip)
Very high gain / long haul?      -> dish (or a big array)
Wide bandwidth?                  -> horn, log-periodic, spiral
Circular polarization?           -> helical (or crossed dipoles)
```

The single most important modern theme: **the patch**. Because patches are flat,
cheap, and printable, you can tile **many** of them and combine their signals — an
**array** — to synthesize **electronically steerable, high-gain** beams. That's the
foundation of phased arrays, 5G, and radar, and the subject of the rest of this
course. Most "antennas" in cutting-edge systems are really **arrays of simple
elements** — so understanding how elements **combine** is where the real power lies.
""",
        ),
        _t(
            "Antenna arrays & the array factor",
            "12 min",
            r"""# Antenna arrays & the array factor

A single small element has low gain. Put **many** elements together, feed them
**coherently**, and their waves **add constructively** in some directions and
**cancel** in others — synthesizing a **narrow, high-gain beam** from cheap parts.
This is an **array**, and it's how modern high-performance antennas (radar, 5G,
satellite) are built.

**Pattern multiplication** is the key simplification: the total pattern of an array
of identical elements is

$$ \text{Total pattern} = (\text{Element pattern}) \times (\text{Array Factor}) $$

The **element pattern** is one element's own pattern; the **Array Factor (AF)**
captures the **interference** from the elements' positions and feed phases —
*independent of what the element is*. So you analyze the AF to understand the beam.

For a **uniform linear array** of N equally-spaced (spacing d), equally-fed
elements, with progressive phase shift β between elements:

$$ \text{AF}(\psi) = \frac{\sin(N\psi/2)}{N \sin(\psi/2)}, \qquad \psi = kd\cos\theta + \beta $$

(normalized to 1 at the peak; k = 2π/λ.) Read off its behaviour:

- **Main lobe** where ψ = 0 → all elements in phase → maximum. Steered by **β**
  (next lesson).
- **N − 1 nulls** and **N − 2 side lobes** between main lobes — **more elements →
  more nulls → narrower main beam and higher gain** (gain ≈ N for a uniform array,
  i.e. **+3 dB per doubling**).
- **Grating lobes** — unwanted *extra* main lobes appear if spacing **d > λ/2** (the
  AF repeats). Keeping **d ≤ λ/2** avoids them (the array equivalent of the Nyquist
  rule).

Drag the slider to watch the beam sharpen and nulls multiply as N grows:

```plot
{"title": "Array factor — drag N: more elements ⇒ narrower beam, more nulls", "xLabel": "electrical angle ψ (rad)", "yLabel": "|AF| (normalised)", "xRange": [0.001, 6.2], "yRange": [0, 1.05], "controls": [{"name": "N", "label": "elements N", "range": [2, 12], "step": 1, "value": 4}], "functions": [{"expr": "abs(sin(N * x / 2) / (N * sin(x / 2)))", "label": "|AF(ψ)|", "color": "#2563eb"}]}
```

(The two peaks at ψ→0 and ψ→2π are the main lobe and the first grating lobe; real
arrays keep d ≤ λ/2 so only the main lobe falls in visible angle.)

The array factor and its beamwidth in **MATLAB** (for the MATLAB REPL):

```matlab
N = 8; d = 0.5; k = 2*pi;                 % 8 elements, half-wavelength spacing
theta = linspace(0.5, 179.5, 720)*pi/180;
psi = k*d*cos(theta);                      % broadside (no phase shift)
AF = abs(sin(N*psi/2) ./ (N*sin(psi/2) + 1e-12));
[~, idx] = max(AF);
above = theta(AF >= 0.707) * 180/pi;       % -3 dB points
fprintf('peak at %.1f deg, HPBW ~ %.1f deg\n', theta(idx)*180/pi, max(above)-min(above));
```

The profound idea: **you build a beam out of interference.** By choosing the number
of elements (gain/beamwidth), their spacing (grating lobes), their **phases** (beam
direction — next), and their **amplitudes** (side-lobe level — a *taper*), you
**synthesize** almost any pattern you want from identical cheap elements. You'll
compute and steer an array's pattern next.
""",
        ),
        _code(
            "Array factor & beam steering",
            "13 min",
            r"""# An N-element uniform linear array forms a beam by interference; a progressive
# phase shift STEERS that beam electronically (no moving parts). Compute the
# pattern and confirm the beam points where we steered it. Uses numpy.

import numpy as np

N = 8           # elements
d = 0.5         # spacing in wavelengths (<= 0.5 avoids grating lobes)
k = 2.0 * np.pi

theta_deg = np.linspace(0.5, 179.5, 720)
theta = np.radians(theta_deg)

steer_deg = 60.0                                   # desired beam direction (from array axis)
beta = -k * d * np.cos(np.radians(steer_deg))      # progressive phase to steer there
psi = k * d * np.cos(theta) + beta
af = np.abs(np.sin(N * psi / 2.0) / (N * np.sin(psi / 2.0) + 1e-12))

peak_idx = int(np.argmax(af))
above_half = theta_deg[af >= 0.707]                # -3 dB points
hpbw = float(above_half.max() - above_half.min())

print("uniform linear array: N=%d elements, spacing d=%.1f lambda" % (N, d))
print("  steered to %.0f deg -> AF peak at %.1f deg (electronic steering works)" % (steer_deg, theta_deg[peak_idx]))
print("  main-lobe HPBW ~ %.1f deg" % hpbw)

# Gain scales ~ N: compare broadside HPBW for N and 2N.
for nn in [8, 16, 32]:
    psi_b = k * d * np.cos(theta)                  # broadside (beta=0)
    afb = np.abs(np.sin(nn * psi_b / 2.0) / (nn * np.sin(psi_b / 2.0) + 1e-12))
    ah = theta_deg[afb >= 0.707]
    print("  N=%-3d broadside HPBW ~ %.1f deg, array gain ~ %.1f dB" % (nn, ah.max() - ah.min(), 10 * np.log10(nn)))
print("doubling N halves the beamwidth and adds ~3 dB gain; phase steers it instantly.")
""",
        ),
        _t(
            "Beamforming & phased arrays",
            "11 min",
            r"""# Beamforming & phased arrays

A **phased array** is an array whose element **phases (and amplitudes) are
controlled electronically**, so the beam can be **steered, shaped, and split**
**instantly, with no moving parts**. It's the technology behind modern radar, 5G
base stations, satellite terminals (Starlink), and Wi-Fi beamforming.

**Beam steering** (from the last lab): applying a **progressive phase shift β**
across the elements tilts the wavefront, pointing the main beam to any angle —
changed in **microseconds** by updating phase shifters, vs mechanically rotating a
dish. One array can **track** multiple targets by time-slicing or form **multiple
simultaneous beams**.

**Beam shaping with amplitude taper.** A *uniform* array has the narrowest beam but
relatively high **side lobes** (first side lobe only −13 dB). Tapering the element
**amplitudes** (more in the center, less at the edges — e.g. **Chebyshev, Taylor,
Hamming** weightings) **lowers the side lobes** (crucial for radar to reject
clutter/jamming) at the cost of a **slightly wider main beam** and a bit of gain.
The classic trade-off:

```
uniform:        narrowest beam, highest side lobes (-13 dB)
tapered (e.g.   wider beam, much lower side lobes (-20 to -40 dB)
 Chebyshev):    -> reject interference / clutter at the cost of resolution
```

**Key practical issues:**

- **Grating lobes** — keep element spacing **≤ λ/2** (especially when steering far
  off broadside, the effective spacing grows), or duplicate main lobes appear and
  waste power / cause ambiguity.
- **Scan loss** — steering far off broadside reduces the effective aperture
  (projected area shrinks as cosθ), so gain drops and the beam widens at wide scan
  angles.
- **Calibration** — every element's phase/amplitude must be accurate; real arrays
  need careful calibration, and element/feed errors raise side lobes.

**Analog vs digital beamforming:**

- **Analog** — phase shifters in RF; one beam (or a few), cheap, low power.
- **Digital** — each element has its own transceiver/ADC, so you form **many beams
  in software** and do advanced processing (**MIMO**, null-steering). Powerful but
  power-hungry; **hybrid** beamforming (analog sub-arrays + digital combining) is the
  5G mmWave compromise.

**Adaptive / smart beamforming** goes further: the array **measures the
environment** and adapts weights to **maximize signal** toward the user and place
**nulls toward interferers** (null-steering / MVDR/MUSIC) — the basis of smart
antennas (advanced course). The big idea: a phased array turns the antenna pattern
into a **software-controlled, real-time variable** — point it, shape it, null
interference, track users — which is exactly why 5G and modern radar are built on
arrays. Next: what the channel does to the beam once it leaves.
""",
        ),
        _t(
            "Propagation mechanisms",
            "11 min",
            r"""# Propagation mechanisms

Friis assumed empty space. Real environments — cities, buildings, terrain — bend,
bounce, and block radio waves through four mechanisms, and understanding them
explains why real coverage looks nothing like a clean 1/d² circle.

- **Reflection** — waves bounce off surfaces **large** compared to λ (ground,
  buildings, walls). The reflected wave's phase can **add to or cancel** the direct
  wave at the receiver. Reflection off the ground is so important it gets its own
  model (the two-ray, next lab).
- **Diffraction** — waves **bend around edges** and over obstacles (hilltops,
  rooftops, corners), via **Huygens' principle** — which is why you get (weak)
  signal in the **shadow** behind an obstacle, not a sharp black shadow. Modeled by
  **knife-edge diffraction** and **Fresnel zones** (keep the first Fresnel zone
  clear for a good link). Diffraction is what lets signals reach NLOS (non-line-of-
  sight) receivers, more effectively at **lower frequencies**.
- **Scattering** — waves hitting objects **small** or **rough** relative to λ
  (foliage, rain, street furniture, rough walls) **re-radiate in many directions**,
  spreading energy. Rain scattering is a serious impairment at high frequency
  (rain fade at Ku/Ka-band and mmWave).
- **Absorption** — materials (walls, foliage, the atmosphere — notably the **O₂ and
  H₂O absorption peaks**, e.g. ~60 GHz oxygen) **attenuate** the wave, converting RF
  to heat. Worse at higher frequency and through dense materials.

**The combined result: multipath.** A transmitted signal reaches the receiver via
**many paths** — direct, reflected, diffracted, scattered — each with a different
**delay, amplitude, and phase**. At the receiver they **sum vectorially**, and
depending on the phases they **constructively or destructively interfere**:

```
TX ──direct──────────────► RX
   ╲reflected (ground)╱        the RX sums all arriving copies:
    ╲   ╱diffracted            sometimes they reinforce (peak),
     ╲ ╱  (rooftop)            sometimes cancel (deep fade)
```

This produces **fading** (rapid signal variation over small distances/time) and
**delay spread** (the signal smears in time, causing inter-symbol interference) —
the defining challenges of mobile radio (next lesson). It's also why moving a phone
a few centimeters can change reception, and why **frequency** matters so much:
**lower frequencies** diffract and penetrate better (wide coverage, sub-GHz), while
**higher frequencies** are blocked easily and rely on reflections and LOS (mmWave).

The takeaway: real propagation is **reflection + diffraction + scattering +
absorption**, combining into **multipath** that both **extends** coverage (into
shadows, via bounces) and **degrades** it (fading, delay spread). You'll quantify
the most important reflection effect — the two-ray ground model — next.
""",
        ),
        _code(
            "Two-ray ground reflection model",
            "12 min",
            r"""# Near the ground, the receiver gets the DIRECT ray plus a GROUND-REFLECTED ray.
# Their interference makes path loss fall off faster than free space at long range:
# beyond a 'breakpoint', loss ~ d^4 (40 dB/decade) instead of d^2. Compare. numpy.

import numpy as np

ht = 30.0        # transmit antenna height (m)
hr = 2.0         # receive antenna height (m)
f = 900e6        # 900 MHz
c = 3.0e8
lam = c / f

# Breakpoint distance: beyond it the two-ray model -> d^4 behaviour.
d_break = 4.0 * ht * hr / lam

print("two-ray model: ht=%.0f m, hr=%.0f m, f=%.0f MHz" % (ht, hr, f / 1e6))
print("breakpoint distance ~ %.0f m" % d_break)
print(" dist(m)   free-space loss(dB)   two-ray loss(dB)")
for d in [10, 100, 500, 1000, 5000, 10000]:
    fspl = 20.0 * float(np.log10(4.0 * np.pi * d / lam))
    # Far-field two-ray approximation (d >> breakpoint): PL = 40log10(d) - 20log10(ht) - 20log10(hr)
    tworay = 40.0 * float(np.log10(d)) - 20.0 * float(np.log10(ht)) - 20.0 * float(np.log10(hr))
    note = "  (use free-space below breakpoint)" if d < d_break else ""
    print("  %-7d  %10.1f          %10.1f%s" % (d, fspl, tworay, note))

print()
print("beyond the breakpoint, doubling distance loses ~12 dB (d^4), not 6 dB (d^2)")
print("-> raising antenna height (ht, hr) directly reduces two-ray path loss.")
""",
        ),
        _t(
            "Fading & multipath",
            "10 min",
            r"""# Fading & multipath

Multipath makes the received signal **vary** — sometimes wildly — over small
changes in position, time, or frequency. This variation is **fading**, and managing
it is the central challenge of mobile/wireless communication. It comes in layers:

**Large-scale vs small-scale:**

- **Path loss** — the average power decay with distance (Friis / two-ray / models,
  next course). The deterministic trend.
- **Shadowing (slow fading)** — slower variation (tens of metres) from **blockage**
  by buildings/terrain. Modeled as **log-normal** (Gaussian in dB) about the
  path-loss mean — you budget a **fade margin** (e.g. ~2σ) to cover it.
- **Multipath (fast fading)** — rapid, deep fluctuations over **fractions of a
  wavelength** as multipath components shift in and out of phase. Moving λ/2 can
  swing the signal **20–30 dB**.

**Statistical models for fast fading:**

- **Rayleigh fading** — **no** dominant line-of-sight; the sum of many random
  multipath components gives a Rayleigh-distributed envelope. The classic urban
  NLOS model; deep fades are common.
- **Rician fading** — a **dominant LOS** component plus multipath; less severe.
  Characterized by the **K-factor** (LOS power / scattered power); large K → nearly
  LOS, K → 0 → Rayleigh.

**Time and frequency dispersion** — two more multipath effects that shape system
design:

- **Delay spread** — paths of different lengths arrive at different **delays**,
  smearing symbols → **inter-symbol interference (ISI)**. The **coherence
  bandwidth** (∝ 1/delay-spread) is the frequency width over which the channel is
  "flat"; signals **wider** than it suffer **frequency-selective** fading (different
  frequencies fade differently) — which is exactly why **OFDM** splits a wide signal
  into many narrow flat sub-carriers (digital-comms track).
- **Doppler spread** — motion shifts frequencies (**Doppler**), causing **time-
  selective** fading; the **coherence time** (∝ 1/Doppler) is how long the channel
  stays stable. Fast motion → rapidly changing channel.

**Combating fading — diversity** (the key weapon): send/receive the signal over
**independent** channels so they don't all fade at once:

- **Spatial** (multiple antennas — MIMO, advanced course), **frequency** (spread
  spectrum/OFDM), **time** (interleaving + coding), **polarization** diversity.
- Plus **equalization**, **error-correcting codes**, and **adaptive** rate/power.

The mindset shift from free-space: the wireless channel is **random and time-
varying**, not a fixed pipe. Designs don't fight every fade — they use **margins**
(for shadowing) and **diversity + coding** (for multipath) to keep reliability high
despite a channel that can drop 20 dB without warning. This statistical view of the
channel underpins the link budgets and MIMO techniques that follow.
""",
        ),
        quiz_lesson(
            "Quiz: Arrays, Beamforming & Propagation",
            (
                q(
                    "What does pattern multiplication state for an array of identical elements?",
                    (
                        opt(
                            "Total pattern = element pattern × array factor (the AF captures element positions and phases)",
                            correct=True,
                        ),
                        opt("Total pattern = element pattern + array factor"),
                        opt("The array factor is irrelevant"),
                        opt("Only the element pattern matters"),
                    ),
                    "The AF (interference from positions/phases) multiplies the single-element pattern; analyzing the AF reveals the beam.",
                ),
                q(
                    "In a uniform linear array, what happens as you add more elements (N)?",
                    (
                        opt(
                            "The main beam narrows and gain rises (~N, +3 dB per doubling), with more nulls/side lobes",
                            correct=True,
                        ),
                        opt("The beam widens"),
                        opt("Gain decreases"),
                        opt("Nothing changes"),
                    ),
                    "More elements = more interference nulls = narrower beam and higher gain (≈N). Spacing >λ/2 introduces grating lobes.",
                ),
                q(
                    "How does a phased array steer its beam?",
                    (
                        opt(
                            "By applying a progressive phase shift across elements — tilting the wavefront electronically, no moving parts",
                            correct=True,
                        ),
                        opt("By physically rotating the antenna"),
                        opt("By changing the frequency"),
                        opt("By turning elements off"),
                    ),
                    "Progressive phase β steers the main lobe in microseconds; amplitude taper shapes side lobes; spacing ≤λ/2 avoids grating lobes.",
                ),
                q(
                    "Which propagation mechanism lets signals reach into the shadow behind an obstacle?",
                    (
                        opt(
                            "Diffraction — waves bend around edges (Huygens' principle), more so at lower frequencies",
                            correct=True,
                        ),
                        opt("Absorption"),
                        opt("Polarization"),
                        opt("Impedance matching"),
                    ),
                    "Diffraction bends waves around edges/over hilltops (knife-edge, Fresnel zones), filling shadows; reflection/scattering/absorption are the other mechanisms.",
                ),
                q(
                    "Beyond the breakpoint, how does two-ray ground-reflection path loss behave?",
                    (
                        opt(
                            "Loss ∝ d⁴ (≈40 dB/decade) — doubling distance loses ~12 dB, faster than free space",
                            correct=True,
                        ),
                        opt("Loss ∝ d² like free space"),
                        opt("Loss is constant"),
                        opt("Signal increases with distance"),
                    ),
                    "The ground-reflected ray interferes with the direct ray; far out, PL ~ 40log10(d), and raising antenna heights reduces it.",
                ),
                q(
                    "What is Rayleigh fading?",
                    (
                        opt(
                            "Fast fading with NO dominant line-of-sight — many random multipath components sum to a Rayleigh-distributed envelope (deep fades common)",
                            correct=True,
                        ),
                        opt("Fading caused only by distance"),
                        opt("A type of antenna"),
                        opt("Fading with a strong LOS component"),
                    ),
                    "Rayleigh = NLOS multipath (deep fades); Rician adds a dominant LOS component (K-factor). Diversity combats both.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# antennas-advanced
# ──────────────────────────────────────────────────────────────────────

_ANT_ADVANCED = SeedCourse(
    slug="antennas-advanced",
    title="Antennas & Propagation — Advanced",
    description=(
        "Modern wireless and the cutting edge: empirical channel/path-loss models, "
        "MIMO and spatial multiplexing, mmWave and massive MIMO, antenna "
        "measurement, numerical EM methods, and smart antennas/RIS. With runnable "
        "path-loss and massive-MIMO labs and a beamwidth plot."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Radio channel & path-loss models",
            "11 min",
            r"""# Radio channel & path-loss models

Friis gives free-space loss, but real deployments need models that capture
**clutter, terrain, and environment**. Engineers use a hierarchy of **path-loss
models** — from simple and general to detailed and site-specific — to predict
coverage and plan networks.

**The log-distance model** — the workhorse generalization of Friis:

$$ PL(d) = PL(d_0) + 10\,n\,\log_{10}\!\left(\frac{d}{d_0}\right) + X_\sigma $$

- **n — the path-loss exponent** — captures the environment: **n = 2** free space,
  **2.7–3.5** urban, **3–5** shadowed/indoor, **4–6** dense obstruction, and even
  **< 2** in waveguide-like corridors/tunnels. This single number is the most
  important channel descriptor.
- **X_σ — log-normal shadowing** — a Gaussian (in dB) random term (σ ≈ 4–12 dB)
  modeling blockage variability; you add a **fade margin** (~σ to 2σ) for the
  desired coverage reliability.

**Empirical models** (fit to measurement campaigns) for specific scenarios:

- **Okumura-Hata** — classic cellular (150 MHz–1.5 GHz), urban/suburban/rural,
  using frequency, distance, antenna heights. **COST-231 Hata** extends it to
  2 GHz.
- **COST-231 Walfisch-Ikegami** — urban, using building heights/spacing/street
  width.
- **Indoor models** — log-distance plus **wall/floor penetration losses** (each wall
  adds a few dB; floors more).
- **3GPP / ITU models** — modern standardized models for cellular (UMa/UMi/RMa) and
  **mmWave**, including LOS/NLOS probabilities — used to design and simulate 5G.

**Ray-tracing** goes site-specific: given a 3D map, it computes reflections/
diffractions/scattering deterministically for accurate (but compute-heavy) coverage
prediction — increasingly used for mmWave and dense urban planning.

The engineering reality: **pick the model that matches your scenario and accuracy
need.** Quick coverage estimate → log-distance with a typical n. Cellular planning
→ Hata/COST/3GPP. mmWave or a specific building → ray-tracing or measurement.
Every model ultimately answers the link-budget question — **what's the path loss,
and what fade margin do I need?** — so the receiver gets enough signal at the
target reliability.

Log-distance path loss in **MATLAB** (for the MATLAB REPL):

```matlab
PL_d0 = 40; d0 = 1; n = 3.2; sigma = 8;   % urban exponent, shadowing std (dB)
d = [50 100 200 500];
PL = PL_d0 + 10*n*log10(d/d0);            % mean path loss (dB)
budget = PL + 2*sigma;                     % add ~2-sigma fade margin
disp('distances (m):');           disp(d)
disp('mean path loss (dB):');     disp(PL)
disp('with 2-sigma margin (dB):'); disp(budget)
```

You'll compute the same log-distance loss with shadowing in Python next.
""",
        ),
        _code(
            "Log-distance path loss with shadowing",
            "12 min",
            r"""# The log-distance model generalizes Friis: PL(d) = PL(d0) + 10n*log10(d/d0),
# plus log-normal shadowing X_sigma. Compute the mean path loss and the loss you
# must budget for (mean + fade margin) for a target reliability. Uses numpy.

import numpy as np

pl_d0 = 40.0     # reference path loss at d0 (dB)
d0 = 1.0         # reference distance (m)
sigma = 8.0      # shadowing std dev (dB)

print(" reference PL(d0)=%.0f dB at %.0f m, shadowing sigma=%.0f dB" % (pl_d0, d0, sigma))
print(" environment       n     dist(m)   mean PL(dB)   +2sigma margin(dB)")
for name, n in [("free space", 2.0), ("urban", 3.2), ("indoor/obstructed", 4.5)]:
    for d in [50.0, 200.0]:
        pl = pl_d0 + 10.0 * n * float(np.log10(d / d0))
        budgeted = pl + 2.0 * sigma           # cover shadowing to ~97.7% reliability
        print("  %-16s  %.1f   %-7.0f   %8.1f       %8.1f" % (name, n, d, pl, budgeted))

print()
print("the path-loss exponent n dominates: doubling distance adds 10n*log10(2) =")
print("  %.1f dB (n=2), %.1f dB (n=3.2), %.1f dB (n=4.5) per doubling."
      % (10 * 2.0 * np.log10(2), 10 * 3.2 * np.log10(2), 10 * 4.5 * np.log10(2)))
print("budget ~2sigma of fade margin so the cell edge still closes the link reliably.")
""",
        ),
        _t(
            "MIMO & spatial techniques",
            "11 min",
            r"""# MIMO & spatial techniques

**MIMO (Multiple-Input Multiple-Output)** uses **multiple antennas at both ends** of
a link and turns multipath — the enemy of the previous course — into an **asset**.
It's the single biggest reason modern Wi-Fi and cellular throughput has exploded.
Multipath provides **independent spatial channels**, and MIMO exploits them three
ways:

- **Spatial multiplexing (capacity).** With rich multipath, an M×N MIMO system can
  send **multiple independent data streams** simultaneously on the **same frequency**
  — the receiver separates them using the spatial signatures. Capacity scales with
  **min(M, N)** — e.g. 4×4 MIMO ≈ 4× the data rate, *for free* in spectrum. This is
  the headline 5G/Wi-Fi capacity gain.
- **Diversity (reliability).** Send the same data over multiple antennas/paths
  (e.g. **space-time codes** like Alamouti) so it's unlikely **all** fade at once,
  drastically cutting outage. Trades the capacity gain for robustness.
- **Beamforming / array gain (coverage).** Coherently combine antennas to focus
  energy (the array gain of the previous course), improving SNR and range.

The fundamental insight (Shannon meets antennas): in a scattering channel, capacity
grows **linearly with the number of antennas** (min of TX/RX), not just
logarithmically with power — so adding antennas beats adding power. Rich multipath
**increases** MIMO capacity (more independent channels); a pure LOS channel has
**rank 1** and gives multiplexing no benefit (only beamforming/diversity).

**Flavours and terms:**

- **SU-MIMO** (single user — multiple streams to one device) vs **MU-MIMO**
  (multi-user — simultaneous streams to *different* users via spatial separation;
  a base-station capacity multiplier).
- **Channel state information (CSI)** — the TX/RX must **estimate the channel**
  (via pilots) to separate/precode streams; MIMO lives or dies on good CSI.
- **Precoding** (e.g. zero-forcing, SVD-based) at the TX and **detection** (MMSE,
  ML) at the RX do the spatial math.

MIMO ties the whole track together: it's **antenna arrays + the random multipath
channel + signal processing**, combined to multiply capacity, reliability, **or**
coverage. Pushing the antenna count *way* up — **massive MIMO** — is the next leap,
and the foundation of 5G.
""",
        ),
        _t(
            "mmWave & massive MIMO",
            "11 min",
            r"""# mmWave & massive MIMO

5G and beyond chase huge bandwidth at **millimeter-wave** frequencies (~24–100 GHz),
where spectrum is plentiful. But mmWave propagation is **brutal**, and the cure is
**massive MIMO** — and the two are deeply linked.

**Why mmWave is hard:**

- **Severe path loss** — FSPL ∝ f², so 28 GHz starts ~20+ dB worse than sub-6 GHz
  for the same gains.
- **Blockage** — short wavelengths are easily blocked by walls, foliage, even a
  **hand or a body**; mmWave is largely **LOS or strong-reflection** only.
- **Atmospheric/rain absorption** — oxygen (~60 GHz) and rain add loss; range is
  short (often < a few hundred metres).

**Why mmWave is also an opportunity:** tiny wavelengths mean **tiny antennas**, so
you can pack **hundreds** of elements into a small array — and that array provides
the **beamforming gain** that *overcomes* the path loss. The physics conspires
nicely: the same small λ that causes high path loss also enables a large-element-
count array in a small area.

**Massive MIMO** = base stations with a **very large number of antennas**
(64, 128, 256+):

- **Huge beamforming gain** — gain ≈ **10·log10(N)** dB, so 256 elements add ~24 dB,
  directly buying back mmWave path loss; the beamwidth narrows ~**1/N**, a pencil
  beam aimed at each user.
- **Massive MU-MIMO** — with so many antennas, the base station serves **many users
  simultaneously** on the same time/frequency via spatially-separated beams,
  multiplying capacity.
- **Channel hardening & favorable propagation** — with many antennas, fast fading
  **averages out** and users' channels become nearly **orthogonal**, simplifying
  scheduling and making simple **linear precoding** (MRT/ZF) near-optimal — a
  surprising statistical gift of large arrays.

**The hard parts:** mmWave + massive MIMO needs **beam management** (discovering and
**tracking** the narrow beam as users/blockers move — a beam-search problem),
**hybrid beamforming** (full digital is too power-hungry at these counts/bandwidths,
so analog sub-arrays + digital combining), **accurate CSI** for hundreds of
antennas, and dense **small-cell** deployment for coverage.

The synthesis of the whole track: **massive MIMO arrays of tiny mmWave elements,
electronically beamformed and tracked, serving many users at once** — turning the
harsh mmWave channel into multi-gigabit 5G. You'll quantify the array gain and
pencil-beamwidth that make it work next.
""",
        ),
        _code(
            "Massive MIMO array gain & beamwidth",
            "12 min",
            r"""# Massive MIMO overcomes mmWave path loss with sheer antenna count: array gain
# grows ~10*log10(N) dB and the beam narrows ~ 1/N (a pencil beam per user).
# Quantify both, and check the gain against a mmWave path-loss penalty. Uses numpy.

import numpy as np

# Half-wave-spaced uniform array: HPBW ~ 0.886 * lambda / (N*d) rad ~ 102/N degrees.
print("massive MIMO (lambda/2 uniform linear array):")
print("  N        array gain(dB)   ~HPBW(deg)")
for n in [1, 4, 16, 64, 128, 256]:
    gain = 10.0 * float(np.log10(n))
    hpbw = 102.0 / n
    print("  %-5d    %8.1f         %8.2f" % (n, gain, hpbw))

print()
# mmWave penalty: extra path loss of 28 GHz vs 3 GHz for the SAME link (FSPL ~ f^2).
f_low = 3e9
f_mmw = 28e9
extra_loss = 20.0 * float(np.log10(f_mmw / f_low))
print("28 GHz vs 3 GHz extra free-space loss: %.1f dB" % extra_loss)
# How many antennas to recover it with array gain at BOTH ends?
# total beamforming gain with N at TX and N at RX ~ 2 * 10log10(N).
for n in [16, 64, 256]:
    recovered = 2.0 * 10.0 * float(np.log10(n))
    print("  N=%-3d at each end -> %.1f dB beamforming gain (%s the %.0f dB penalty)"
          % (n, recovered, "covers" if recovered >= extra_loss else "short of", extra_loss))
print("this is why mmWave NEEDS large arrays: beamforming gain buys back the path loss.")
""",
        ),
        _t(
            "Antenna measurement",
            "10 min",
            r"""# Antenna measurement

A designed antenna must be **measured** to confirm its pattern, gain, impedance, and
polarization — simulation and reality always differ. Antenna metrology ties to the
Test & Measurement and Signal Integrity tracks (it's all S-parameters and
calibrated RF).

**What's measured:**

- **Input match (S11 / VSWR)** vs frequency — with a **VNA** (T&M track). Quick,
  and tells you the bandwidth and resonance. The first bench test.
- **Radiation pattern** — received signal vs angle as the antenna rotates
  (azimuth/elevation cuts, co- and cross-polarization). Yields beamwidth, side
  lobes, nulls, front-to-back ratio.
- **Gain** — typically by **comparison** to a calibrated **standard gain horn**
  (gain-transfer method), or absolute (three-antenna method).
- **Polarization**, **efficiency**, **phase center**.

**Where it's measured — the far field is the catch.** Patterns are far-field
quantities, requiring distance **≥ 2D²/λ**, which for a large/high-frequency antenna
is **huge** (tens to hundreds of metres). The solutions:

- **Far-field range** — outdoor or a large **anechoic chamber** (walls lined with
  RF-absorbing foam to suppress reflections — a "quiet zone" mimicking free space).
  Conceptually simple but needs the full far-field distance.
- **Compact Antenna Test Range (CATR)** — a precision **reflector** collimates the
  wave to create a planar (far-field-like) wavefront in a **small** chamber.
- **Near-field scanning** — measure amplitude **and phase** on a surface (planar/
  cylindrical/spherical) **close** to the antenna, then **mathematically transform**
  (FFT-based near-field-to-far-field) to get the far-field pattern. Compact,
  accurate, gives the full 3D pattern — the modern workhorse for large arrays.

**Why anechoic chambers matter:** any reflection from walls/floor/ceiling corrupts
the pattern (it's multipath, the enemy of a clean measurement); the absorber
creates a reflection-free environment, and a **shielded** chamber also blocks
outside interference (ties to EMC testing — often the same facilities).

**Practical pitfalls** (echoing T&M): the **measurement system must out-perform** the
antenna (range reflections below the side-lobe level you want to measure; positioner
accuracy; cable flexing changing phase), and **calibration** (gain standard,
VNA cal) governs accuracy. Cross-polarization and mutual coupling in arrays are
easy to get wrong.

The takeaway: measuring an antenna is **calibrated, far-field (or transformed
near-field), reflection-controlled RF metrology**. It closes the loop between
design/simulation and reality — and, like all measurement, is only as trustworthy
as its calibration and its control of the (multipath) environment.
""",
        ),
        _t(
            "Numerical methods & smart antennas",
            "11 min",
            r"""# Numerical methods & smart antennas

Modern antenna engineering rests on two advanced pillars: **simulating**
electromagnetics numerically (you rarely have closed forms for real antennas), and
**adapting** antennas intelligently in real time.

**Computational electromagnetics (CEM)** — solving Maxwell's equations numerically
to predict an antenna's behaviour before building it. The major methods, each suited
to different problems:

- **Method of Moments (MoM)** — solves integral equations on the **conductor
  surfaces/wires**; extremely efficient for **wire antennas and metallic
  structures** (the engine behind **NEC**, the classic wire-antenna tool). Scales
  poorly for large dielectric volumes.
- **FEM (Finite Element Method)** — divides the volume into a mesh; great for
  **complex 3D geometries and dielectrics** (e.g. **HFSS**). Frequency-domain,
  handles intricate structures.
- **FDTD (Finite-Difference Time-Domain)** — steps Maxwell's equations on a grid in
  **time**; naturally **broadband** (one run gives a wide frequency response) and
  great for **transient/wideband** and large problems (e.g. **CST**, used widely for
  EMC too).

The workflow: model the geometry → mesh → solve → extract pattern, gain, impedance,
S-parameters → iterate the design. CEM is to antennas what SPICE is to circuits —
and like all simulation, it must be **validated against measurement** (previous
lesson). Trade-offs: MoM for wires/metal, FEM for complex 3D/dielectric, FDTD for
broadband/transient/large — and all face the **electrically-large** problem (huge
meshes at high frequency) that drives ongoing research (and GPU acceleration).

**Smart / adaptive antennas** — arrays that **sense and respond** to the
environment in real time (building on phased arrays + MIMO):

- **Adaptive beamforming** — continuously adjust element weights to **maximize SNR**
  toward the desired user **and steer nulls onto interferers** (algorithms: **MVDR/
  Capon**, LMS; **direction-of-arrival** estimation via **MUSIC/ESPRIT**). The basis
  of interference-resistant comms and radar.
- **Beam tracking** — follow moving users/beams (essential for mmWave's pencil
  beams).
- **Reconfigurable antennas** — electronically change pattern, frequency, or
  polarization (via switches/varactors/MEMS) to adapt to conditions.

**The frontier — Reconfigurable Intelligent Surfaces (RIS):** passive (or nearly
passive) surfaces of many tiny reconfigurable elements that **reflect/shape**
incident waves to **redirect** signals around blockages — turning the *environment
itself* into a controllable part of the link ("smart radio environments"), a hot
6G research direction.

**The throughline of the entire track:** antennas progressed from a **fixed wire**
that radiates a fixed pattern, to **arrays** that synthesize beams, to **phased/
MIMO** arrays steered and multiplexed electronically, to **massive MIMO/mmWave**
serving many users with pencil beams, toward **smart, adaptive, and reconfigurable**
systems — even shaping the environment with RIS. Throughout, the same fundamentals
rule: **radiation, patterns, gain, interference, and propagation**. Master those,
and from a dipole to a 256-element 5G array to a 6G RIS, it's all the same physics —
applied with ever more control over **where the energy goes**.
""",
        ),
        quiz_lesson(
            "Quiz: Channels, MIMO & the Modern RF Frontier",
            (
                q(
                    "In the log-distance path-loss model, what does the exponent n represent?",
                    (
                        opt(
                            "How fast power decays with distance in a given environment (2 free space, ~3-4 urban, 4-6 obstructed/indoor)",
                            correct=True,
                        ),
                        opt("The number of antennas"),
                        opt("The carrier frequency"),
                        opt("The transmit power"),
                    ),
                    "PL = PL(d0) + 10n·log10(d/d0) + shadowing; n is the most important channel descriptor, and you add ~2σ fade margin for shadowing.",
                ),
                q(
                    "How does spatial multiplexing in MIMO increase data rate?",
                    (
                        opt(
                            "Rich multipath provides independent spatial channels, so multiple streams send on the same frequency; capacity ~ min(M,N)",
                            correct=True,
                        ),
                        opt("By increasing transmit power only"),
                        opt("By using more bandwidth"),
                        opt("By reducing the number of antennas"),
                    ),
                    "MIMO turns multipath into independent channels; capacity scales with min(TX,RX) antennas. A rank-1 pure-LOS channel gives no multiplexing gain.",
                ),
                q(
                    "Why does mmWave (5G) depend on massive MIMO / large arrays?",
                    (
                        opt(
                            "mmWave has severe path loss and blockage; large arrays provide beamforming gain (~10·log10(N)) that buys it back",
                            correct=True,
                        ),
                        opt("mmWave has no path loss"),
                        opt("Arrays are only decorative at mmWave"),
                        opt("To reduce the data rate"),
                    ),
                    "Tiny mmWave wavelengths allow many elements in a small area; their beamforming gain and pencil beams overcome the high path loss and blockage.",
                ),
                q(
                    "Why are antenna patterns measured in an anechoic chamber?",
                    (
                        opt(
                            "RF absorber suppresses wall reflections (multipath) that would corrupt the pattern, creating a reflection-free 'quiet zone'",
                            correct=True,
                        ),
                        opt("To keep the antenna warm"),
                        opt("Because patterns are near-field quantities"),
                        opt("To increase the antenna's gain"),
                    ),
                    "Reflections are multipath that distorts the measured pattern; absorber mimics free space. Far-field distance (≥2D²/λ) or near-field scanning + transform is also needed.",
                ),
                q(
                    "Which numerical EM method is naturally broadband (one run → wide frequency response)?",
                    (
                        opt(
                            "FDTD (Finite-Difference Time-Domain) — it steps Maxwell's equations in time",
                            correct=True,
                        ),
                        opt("Method of Moments (MoM)"),
                        opt("Static analysis"),
                        opt("None can do broadband"),
                    ),
                    "FDTD is time-domain (broadband, good for transient/large problems); MoM suits wires/metal; FEM suits complex 3D dielectric geometries.",
                ),
                q(
                    "What does an adaptive (smart) antenna array do?",
                    (
                        opt(
                            "Adjusts element weights in real time to maximize SNR toward the user and steer nulls onto interferers",
                            correct=True,
                        ),
                        opt("Physically rotates to track the sun"),
                        opt("Only works at DC"),
                        opt("Disables beamforming"),
                    ),
                    "Adaptive beamforming (MVDR/LMS, with DOA estimation like MUSIC) maximizes desired signal and nulls interference; RIS extends control to the environment itself.",
                ),
            ),
        ),
    ),
)


ANTENNAS_COURSES = (_ANT_BASICS, _ANT_INTERMEDIATE, _ANT_ADVANCED)
