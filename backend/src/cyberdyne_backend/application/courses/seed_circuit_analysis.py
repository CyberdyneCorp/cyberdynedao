"""Circuit Analysis track: Basics -> Intermediate -> Advanced.

A three-level electrical-engineering track on analysing linear circuits. Starts
from Ohm's and Kirchhoff's laws and systematic DC analysis (nodal, mesh,
Thevenin/Norton), moves through energy-storage elements, transients and AC
steady-state with phasors, and ends with frequency response, the Laplace
transform, transfer functions, two-port networks and transformers. Lessons are
`text` with LaTeX, interactive ```plot blocks (transients, sinusoids, frequency
response) and ```mermaid circuit/block diagrams.
"""

# Lesson prose uses typographic characters (×, →, ≈, Ω, μ, ∠, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# ── Circuit Analysis — Basics ────────────────────────────────────────────────

_CA_BASICS = SeedCourse(
    slug="circuit-analysis-basics",
    title="Circuit Analysis — Basics",
    description=(
        "The foundations of analysing DC resistive circuits: Ohm's law and the "
        "power/sign conventions, Kirchhoff's voltage and current laws, "
        "series/parallel combinations and dividers, and the two systematic "
        "methods — nodal and mesh analysis — plus Thevenin and Norton "
        "equivalents. Interactive plots and circuit diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Ohm's law, power & sign conventions",
            "11 min",
            r"""\
# Ohm's law, power & sign conventions

Three quantities run through every circuit: **voltage** $v$ (volts, the energy
per charge between two points), **current** $i$ (amperes, the rate of charge
flow) and **resistance** $R$ (ohms, $\Omega$). For an ideal resistor they obey
**Ohm's law**:

$$v = R\,i, \qquad i = \frac{v}{R}, \qquad R = \frac{v}{i}.$$

The relationship is linear — double the voltage across a fixed resistor and the
current doubles. Slide the resistance and watch the $i$–$v$ line tilt (a steeper
line means a smaller resistor passing more current per volt):

```plot
{"title": "Ohm's law: current vs voltage for a resistor", "xLabel": "voltage v (V)", "yLabel": "current i (A)", "xRange": [0, 10], "yRange": [0, 5], "controls": [{"name": "R", "range": [2, 20], "value": 4, "label": "resistance R (Ω)"}], "functions": [{"expr": "x/R", "label": "i = v/R", "color": "#2563eb"}], "points": [{"x": 8, "yExpr": "8/R", "label": "operating point", "color": "#dc2626", "size": 7}]}
```

**Power** delivered to (or by) an element is $p = v\,i$. For a resistor this is
always *dissipated* as heat:

$$p = v\,i = i^2 R = \frac{v^2}{R} \;\ge\; 0.$$

**Sign / passive convention.** Define current entering the **+** terminal of an
element. Then $p = vi > 0$ means the element **absorbs** power (a resistor,
always), and $p < 0$ means it **delivers** power (a source). Getting the
reference arrows and polarities consistent is what makes the algebra come out
right.

```mermaid
flowchart LR
  SRC["Voltage source +v-"] -->|"i (into + terminal)"| R["Resistor R absorbs p = i^2 R"]
  R -->|"return path"| SRC
```

**Next:** how voltages and currents combine around a circuit — Kirchhoff's laws.
""",
        ),
        _t(
            "Kirchhoff's laws (KVL & KCL)",
            "11 min",
            r"""\
# Kirchhoff's laws (KVL & KCL)

Ohm's law describes one element; **Kirchhoff's laws** connect the whole circuit.
They follow from conservation of energy and charge.

**Kirchhoff's Current Law (KCL).** The algebraic sum of currents entering any
**node** is zero — charge does not pile up:

$$\sum_{\text{into node}} i = 0.$$

**Kirchhoff's Voltage Law (KVL).** The algebraic sum of voltages around any
closed **loop** is zero — energy returns to where it started:

$$\sum_{\text{around loop}} v = 0.$$

Consider a source $V_s$ driving two resistors in a single loop. KVL around the
loop gives $V_s = v_1 + v_2 = i(R_1 + R_2)$, so the loop current is
$i = V_s/(R_1+R_2)$. KCL at every node here just says the same current flows
through the series elements:

```mermaid
flowchart LR
  A(("node A")) -->|"v1 = i R1"| B(("node B"))
  B -->|"v2 = i R2"| C(("node C / ground"))
  C -->|"Vs (source)"| A
```

These two laws plus Ohm's law are *complete*: any linear resistive circuit can
be solved with them. The systematic recipes (nodal and mesh analysis) are just
organised bookkeeping of KCL and KVL.

**Next:** the most common patterns — series, parallel and dividers.
""",
        ),
        _t(
            "Series, parallel & dividers",
            "10 min",
            r"""\
# Series, parallel & dividers

Most everyday combinations reduce to two patterns.

**Series** (same current through each): resistances add.

$$R_\text{series} = R_1 + R_2 + \dots$$

**Parallel** (same voltage across each): conductances add, so

$$\frac{1}{R_\text{par}} = \frac{1}{R_1} + \frac{1}{R_2} + \dots,
\qquad R_1 \parallel R_2 = \frac{R_1 R_2}{R_1 + R_2}.$$

Two equal resistors in parallel give half the resistance; the parallel
combination is always *smaller* than the smallest branch.

**Voltage divider** (series). The source voltage splits in proportion to
resistance:

$$v_2 = V_s\,\frac{R_2}{R_1 + R_2}.$$

Sweep $R_2$ and watch the output of a 10 V divider rise from 0 toward the full
source as $R_2$ grows relative to a fixed $R_1 = 5\,\Omega$:

```plot
{"title": "Voltage divider output vs R2 (Vs = 10 V, R1 = 5 Ω)", "xLabel": "R2 (Ω)", "yLabel": "v2 (V)", "xRange": [0, 50], "yRange": [0, 10], "functions": [{"expr": "10*x/(5 + x)", "label": "v2 = Vs·R2/(R1+R2)", "color": "#2563eb"}], "points": [{"x": 5, "y": 5, "label": "R2 = R1 → half", "color": "#dc2626", "size": 6}]}
```

**Current divider** (parallel). Current splits *inversely* to resistance — more
current takes the easier (smaller-$R$) branch:

$$i_1 = i_\text{tot}\,\frac{R_2}{R_1 + R_2}.$$

**Next:** a method that handles any circuit — nodal analysis.
""",
        ),
        _t(
            "Nodal analysis",
            "12 min",
            r"""\
# Nodal analysis

**Nodal analysis** solves a circuit by finding the **node voltages** (each
measured against a chosen **reference / ground** node). It is KCL applied
systematically.

**Recipe**
1. Pick a reference node (call its voltage 0).
2. Label the remaining node voltages $V_1, V_2, \dots$
3. Write **KCL** at each unknown node, expressing every branch current via Ohm's
   law as a difference of node voltages over a resistance.
4. Solve the resulting linear system.

For a single unknown node $V_1$ fed by a source $V_s$ through $R_1$ and tied to
ground through $R_2$, KCL says the current in equals the current out:

$$\frac{V_s - V_1}{R_1} = \frac{V_1}{R_2}
\;\Longrightarrow\;
V_1 = V_s\,\frac{R_2}{R_1 + R_2}.$$

(Reassuringly, that is exactly the voltage divider.) The conductance form

$$\frac{V_1}{R_1} + \frac{V_1}{R_2} = \frac{V_s}{R_1}$$

generalises directly to the matrix equation $\mathbf{G}\,\mathbf{v} = \mathbf{i}$,
where $\mathbf{G}$ is the symmetric **conductance matrix**: diagonal = sum of
conductances at a node, off-diagonal = minus the shared conductance.

```mermaid
flowchart TD
  S["Pick reference (ground)"] --> L["Label node voltages V1, V2, ..."]
  L --> K["Write KCL at each node (Ohm's law for each branch)"]
  K --> M["Assemble G v = i"]
  M --> R["Solve the linear system"]
```

Nodal analysis is the method most circuit simulators (SPICE) use internally,
because it scales cleanly to large networks.

**Next:** the dual method built on loops — mesh analysis.
""",
        ),
        _t(
            "Mesh analysis",
            "11 min",
            r"""\
# Mesh analysis

**Mesh analysis** is the dual of nodal analysis: instead of node voltages it
solves for **mesh (loop) currents**, applying KVL systematically. A *mesh* is a
loop with no other loop inside it (think of the open "window panes" of a planar
circuit).

**Recipe**
1. Assign a circulating current ($I_1, I_2, \dots$) to each mesh, all in the same
   direction (say clockwise).
2. Write **KVL** around each mesh. The current through a resistor *shared* by two
   meshes is the **difference** of the two mesh currents.
3. Solve for the mesh currents; branch currents follow.

For two meshes sharing a middle resistor $R_2$, driven by source $V_s$ in mesh 1,
KVL gives:

$$V_s = I_1 R_1 + (I_1 - I_2)R_2, \qquad 0 = (I_2 - I_1)R_2 + I_2 R_3.$$

In matrix form this is $\mathbf{R}\,\mathbf{i} = \mathbf{v}$, with $\mathbf{R}$
the symmetric **resistance matrix**: diagonal = sum of resistances in a mesh,
off-diagonal = minus the shared resistance.

```mermaid
flowchart LR
  M1["Mesh 1: I1 (Vs, R1)"] -->|"shared R2 carries I1 - I2"| M2["Mesh 2: I2 (R3)"]
```

**Which to choose?** Nodal scales with the number of nodes; mesh with the number
of meshes. Pick whichever yields fewer equations. Both are exact and rest only
on Kirchhoff's laws.

**Next:** replacing a whole network with one source and one resistor.
""",
        ),
        _t(
            "Thevenin & Norton equivalents",
            "12 min",
            r"""\
# Thevenin & Norton equivalents

Any linear two-terminal network — however many sources and resistors — looks,
from the outside, like a single source and a single resistor. That is
**Thevenin's** (and dually **Norton's**) theorem.

- **Thevenin equivalent:** a voltage source $V_{th}$ in **series** with a
  resistance $R_{th}$.
- **Norton equivalent:** a current source $I_N$ in **parallel** with the same
  $R_{th}$.

**How to find them**
- $V_{th}$ = the **open-circuit voltage** at the terminals.
- $I_N$ = the **short-circuit current** at the terminals.
- $R_{th}$ = resistance looking back in with all *independent* sources zeroed
  (voltage sources shorted, current sources opened). Equivalently
  $R_{th} = V_{th}/I_N$.

```mermaid
flowchart LR
  NET["Messy linear network"] --> TH["Thevenin: Vth in series with Rth"]
  TH --> NO["Norton: IN = Vth/Rth in parallel with Rth"]
```

**Why it matters — maximum power transfer.** Connect a load $R_L$ to a Thevenin
source. The power delivered to the load is

$$P_L = \left(\frac{V_{th}}{R_{th}+R_L}\right)^2 R_L.$$

Plot it against $R_L$ (here $V_{th}=10\,\text{V}$, $R_{th}=4\,\Omega$): the curve
peaks exactly at **$R_L = R_{th}$** — the matched-load condition behind antennas,
amplifiers and power supplies:

```plot
{"title": "Power to the load peaks at R_L = R_th = 4 Ω", "xLabel": "load R_L (Ω)", "yLabel": "power P_L (W)", "xRange": [0, 20], "yRange": [0, 7], "functions": [{"expr": "100*x/(4 + x)^2", "label": "P_L(R_L)", "color": "#2563eb"}], "points": [{"x": 4, "y": 6.25, "label": "match: R_L = R_th", "color": "#dc2626", "size": 7}]}
```

Thevenin/Norton turn an intimidating network into something you can reason about
in one line.

**Next:** test what you've learned.
""",
        ),
    ),
)

# ── Circuit Analysis — Intermediate ──────────────────────────────────────────

_CA_INTERMEDIATE = SeedCourse(
    slug="circuit-analysis-intermediate",
    title="Circuit Analysis — Intermediate",
    description=(
        "Circuits that store energy and change in time: the i–v laws and energy of "
        "capacitors and inductors, first-order RC/RL transients and the time "
        "constant, second-order RLC damping, and AC steady-state via phasors, "
        "impedance/admittance and AC power (real, reactive, apparent and power "
        "factor). Interactive transient and sinusoid plots throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Capacitors & inductors",
            "11 min",
            r"""\
# Capacitors & inductors

Resistors dissipate energy; **capacitors** and **inductors** *store* it, and
their laws involve the *rate of change* of a signal.

**Capacitor** — stores energy in an electric field. Its charge is $q = Cv$, so

$$i_C = C\,\frac{dv}{dt}, \qquad w_C = \tfrac12 C v^2.$$

A capacitor's voltage **cannot jump** (that would need infinite current). At DC
(nothing changing) $i_C = 0$ — it looks like an **open circuit**.

**Inductor** — stores energy in a magnetic field:

$$v_L = L\,\frac{di}{dt}, \qquad w_L = \tfrac12 L i^2.$$

Dually, an inductor's current cannot jump, and at DC ($di/dt = 0$) it looks like
a **short circuit**.

These are *duals*: swap $v \leftrightarrow i$ and $C \leftrightarrow L$ and one
law becomes the other. The stored-energy curves are both quadratic — doubling the
capacitor voltage (or inductor current) **quadruples** the stored energy:

```plot
{"title": "Stored energy is quadratic (½Cv² and ½Li²)", "xLabel": "v (V) or i (A)", "yLabel": "energy (J)", "xRange": [0, 5], "yRange": [0, 12], "functions": [{"expr": "0.5*1*x^2", "label": "capacitor ½Cv² (C = 1 F)", "color": "#2563eb"}, {"expr": "0.5*0.8*x^2", "label": "inductor ½Li² (L = 0.8 H)", "color": "#dc2626"}]}
```

Because their laws are derivatives, putting capacitors or inductors in a circuit
turns the algebraic equations of resistive circuits into **differential
equations** — that is what the next lessons solve.

**Next:** the simplest dynamics — first-order RC/RL transients.
""",
        ),
        _t(
            "First-order RC/RL transients",
            "12 min",
            r"""\
# First-order RC/RL transients

A single capacitor (or inductor) with resistance gives a **first-order** circuit
whose response is a single decaying exponential set by the **time constant**
$\tau$.

- **RC circuit:** $\tau = RC$.
- **RL circuit:** $\tau = L/R$.

```mermaid
flowchart LR
  SW["Switch closes (t = 0)"] --> SRC["DC source Vs"]
  SRC -->|"charges through R"| CAP["Capacitor C: v rises to Vs as 1 - e^(-t/RC)"]
  CAP -->|"source removed"| DIS["Discharge: v decays as e^(-t/RC)"]
```

**Step response.** Switch a DC source $V_s$ onto an initially uncharged RC
circuit. The capacitor voltage rises exponentially toward $V_s$:

$$v_C(t) = V_s\left(1 - e^{-t/\tau}\right).$$

After one $\tau$ it reaches $\approx 63\%$ of the final value; after about
$5\tau$ it is essentially settled ($>99\%$). Here $V_s = 1$, $\tau = 1\,\text{s}$
— the red marker is the one-time-constant point:

```plot
{"title": "RC step response: charging toward Vs (τ = 1 s)", "xLabel": "t (s)", "yLabel": "v_C(t) (V)", "xRange": [0, 5], "yRange": [0, 1.2], "functions": [{"expr": "1 - exp(-x)", "label": "v_C(t) = Vs(1 − e^{−t/τ})", "color": "#2563eb"}], "points": [{"x": 1, "y": 0.632, "label": "1τ → 63%", "color": "#dc2626", "size": 7}]}
```

**Natural (discharge) response.** With the source removed, a charged capacitor
decays: $v_C(t) = V_0\,e^{-t/\tau}$. The general first-order solution combines
both:

$$x(t) = x(\infty) + \big(x(0) - x(\infty)\big)\,e^{-t/\tau}.$$

The time constant sets the speed of every relay debounce, RC filter and logic
edge. Smaller $\tau$ = faster response (at the cost of bandwidth/noise).

**Next:** add a second storage element — RLC and damping.
""",
        ),
        _t(
            "Second-order RLC transients",
            "12 min",
            r"""\
# Second-order RLC transients

Put a resistor, inductor **and** capacitor together and you get a **second-order**
circuit, governed by a second-order differential equation. Its character is set
by the **damping ratio** $\zeta$, comparing dissipation to the natural
oscillation $\omega_0 = 1/\sqrt{LC}$.

Three regimes:

- **Overdamped** ($\zeta > 1$): two real roots, a slow non-oscillatory crawl to
  the final value.
- **Critically damped** ($\zeta = 1$): the fastest approach with **no** overshoot.
- **Underdamped** ($\zeta < 1$): complex roots — the response **rings**,
  oscillating at the damped frequency $\omega_d = \omega_0\sqrt{1-\zeta^2}$ while
  decaying.

Compare a smooth (near-critical) approach with a ringing underdamped step
response settling to the same final value of 1:

```plot
{"title": "RLC step: critically damped vs underdamped (ringing)", "xLabel": "t (s)", "yLabel": "output", "xRange": [0, 12], "yRange": [0, 1.8], "functions": [{"expr": "1 - (1 + x)*exp(-x)", "label": "critically damped (no overshoot)", "color": "#2563eb"}, {"expr": "1 - exp(-0.4*x)*cos(2*x)", "label": "underdamped (rings, ζ < 1)", "color": "#dc2626"}]}
```

The underdamped curve overshoots and oscillates before settling; the critically
damped one is the fastest response that never overshoots. Designers trade
**speed against overshoot** — fast logic and control loops are tuned just shy of
critical damping.

**Next:** steady sinusoids — AC analysis with phasors.
""",
        ),
        _t(
            "AC steady-state & phasors",
            "11 min",
            r"""\
# AC steady-state & phasors

When a linear circuit is driven by a sinusoid for a long time, every voltage and
current settles into a sinusoid at the **same frequency** $\omega$ — only the
**amplitude** and **phase** differ. This is the **AC steady state**, and the
trick that tames it is the **phasor**.

A sinusoid

$$v(t) = V_m\cos(\omega t + \phi)$$

is represented by the complex **phasor** $\mathbf{V} = V_m\,e^{j\phi} = V_m\angle\phi$,
which strips away the common $\cos\omega t$ and keeps only amplitude and phase. A
**leading** or **lagging** phase shows up as a horizontal shift of the waveform.
Slide the phase and watch the red wave slide relative to the reference:

```plot
{"title": "Same frequency, shifted phase: v(t) = cos(ωt + φ)", "xLabel": "ωt (rad)", "yLabel": "amplitude", "xRange": [0, 12.6], "yRange": [-1.5, 1.5], "controls": [{"name": "phi", "range": [-3.14, 3.14], "value": 1, "label": "phase φ (rad)"}], "functions": [{"expr": "cos(x)", "label": "reference cos(ωt)", "color": "#2563eb"}, {"expr": "cos(x + phi)", "label": "cos(ωt + φ)", "color": "#dc2626"}]}
```

The payoff: with phasors, the calculus of $d/dt$ becomes **algebra**. A
derivative $d/dt$ turns into multiplication by $j\omega$, so the differential
equations of AC circuits collapse into ordinary complex algebra — exactly like
the DC resistive case, but with complex numbers.

**Next:** the AC version of resistance — impedance and admittance.
""",
        ),
        _t(
            "Impedance & admittance",
            "11 min",
            r"""\
# Impedance & admittance

In the phasor domain, every element obeys a generalised Ohm's law
$\mathbf{V} = \mathbf{Z}\,\mathbf{I}$, where $\mathbf{Z}$ is the complex
**impedance** (ohms). Its reciprocal is the **admittance** $\mathbf{Y} = 1/\mathbf{Z}$.

The three elements:

$$\mathbf{Z}_R = R, \qquad \mathbf{Z}_L = j\omega L, \qquad
\mathbf{Z}_C = \frac{1}{j\omega C} = -\frac{j}{\omega C}.$$

Writing $\mathbf{Z} = R + jX$, the **reactance** $X$ is positive for inductors
(voltage *leads* current) and negative for capacitors (voltage *lags*). Crucially,
**series and parallel combine exactly as for resistors** — series impedances add,
parallel admittances add — so all your DC tricks (dividers, nodal, mesh,
Thevenin) carry straight over, now with complex numbers.

Reactance is frequency-dependent. An inductor's magnitude $|Z_L| = \omega L$ rises
with frequency (blocks high frequencies); a capacitor's $|Z_C| = 1/(\omega C)$
falls (passes high frequencies). They cross at the resonant frequency:

```plot
{"title": "Reactance magnitude vs frequency (L = 0.1 H, C = 0.1 F)", "xLabel": "ω (rad/s)", "yLabel": "|reactance| (Ω)", "xRange": [0.5, 20], "yRange": [0, 12], "functions": [{"expr": "0.1*x", "label": "|Z_L| = ωL (rises)", "color": "#dc2626"}, {"expr": "1/(0.1*x)", "label": "|Z_C| = 1/(ωC) (falls)", "color": "#2563eb"}], "points": [{"x": 10, "y": 1, "label": "ω₀ = 1/√(LC)", "color": "#16a34a", "size": 6}]}
```

**Next:** what all this means for power delivered by an AC source.
""",
        ),
        _t(
            "AC power & power factor",
            "12 min",
            r"""\
# AC power & power factor

In AC, the phase between voltage and current splits power into useful work and
sloshing energy. Let $\theta$ be the angle of the load impedance (the angle by
which current lags voltage).

- **Real (average) power** $P = V_\text{rms} I_\text{rms}\cos\theta$ — watts (W).
  The energy actually consumed.
- **Reactive power** $Q = V_\text{rms} I_\text{rms}\sin\theta$ — VAR. Energy that
  flows back and forth into reactances; nets to zero work.
- **Apparent power** $S = V_\text{rms} I_\text{rms}$ — VA. The hypotenuse:
  $S^2 = P^2 + Q^2$.

The **power factor** is

$$\text{pf} = \cos\theta = \frac{P}{S}.$$

The three powers form a right triangle, the **power triangle**:

```mermaid
flowchart LR
  S["Apparent power S (VA) = Vrms·Irms"] --> P["Real power P (W) = S·cos θ"]
  S --> Q["Reactive power Q (VAR) = S·sin θ"]
  P --> REL["S² = P² + Q², pf = cos θ = P/S"]
  Q --> REL
```

A purely resistive load has $\text{pf}=1$ (all power is real). As the load becomes
more reactive, $\theta$ grows, the real power $P=S\cos\theta$ drops, and the
utility carries extra current for no useful work. Sweep $\theta$ — pf is highest
at $\theta = 0$ and collapses toward $90°$:

```plot
{"title": "Power factor cos θ falls as the load gets more reactive", "xLabel": "phase angle θ (rad)", "yLabel": "power factor cos θ", "xRange": [0, 1.57], "yRange": [0, 1.1], "functions": [{"expr": "cos(x)", "label": "pf = cos θ", "color": "#2563eb"}], "points": [{"x": 0, "y": 1, "label": "resistive: pf = 1", "color": "#dc2626", "size": 6}]}
```

Because a low power factor means wasted current and bigger conductors, industrial
plants add **power-factor-correction** capacitors to cancel inductive $Q$ and push
pf back toward 1.

**Next:** test what you've learned.
""",
        ),
    ),
)

# ── Circuit Analysis — Advanced ──────────────────────────────────────────────

_CA_ADVANCED = SeedCourse(
    slug="circuit-analysis-advanced",
    title="Circuit Analysis — Advanced",
    description=(
        "Frequency-domain and systems view of circuits: sinusoidal frequency "
        "response and resonance (Q, bandwidth), the Laplace transform and "
        "s-domain impedances, transfer functions with poles and zeros, two-port "
        "network parameters (z, y, h, ABCD), coupled inductors and transformers, "
        "and an applied analysis tying it all together. Interactive response "
        "plots and block diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Frequency response & resonance",
            "12 min",
            r"""\
# Frequency response & resonance

Sweep the driving frequency and a circuit's response — gain and phase — traces
out its **frequency response**. The dramatic case is **resonance**, where a series
RLC circuit's inductive and capacitive reactances cancel.

At the **resonant frequency**

$$\omega_0 = \frac{1}{\sqrt{LC}},$$

the reactances cancel ($\omega_0 L = 1/\omega_0 C$), the impedance is purely
resistive and *minimum*, and the current **peaks**. The sharpness of that peak is
the **quality factor**

$$Q = \frac{\omega_0 L}{R} = \frac{1}{R}\sqrt{\frac{L}{C}},$$

and the **bandwidth** (the width between the half-power points) is
$\text{BW} = \omega_0/Q$. High $Q$ = a tall, narrow peak (a selective filter);
low $Q$ = a broad, gentle one. The curve below peaks at $\omega_0 = 10$:

```plot
{"title": "Series-RLC resonance: response peaks at ω₀ = 10", "xLabel": "ω (rad/s)", "yLabel": "normalised current", "xRange": [2, 25], "yRange": [0, 1.2], "functions": [{"expr": "1/sqrt(1 + (4*(x/10 - 10/x))^2)", "label": "|I(ω)| (high Q, narrow)", "color": "#dc2626"}, {"expr": "1/sqrt(1 + (1*(x/10 - 10/x))^2)", "label": "|I(ω)| (low Q, broad)", "color": "#2563eb"}], "points": [{"x": 10, "y": 1, "label": "ω₀ resonance", "color": "#16a34a", "size": 6}]}
```

A **parallel** RLC resonator is the dual: impedance is *maximum* at $\omega_0$ and
current is minimum. Resonance is the basis of radio tuning, oscillators and
filters.

**Next:** a general tool for any input — the Laplace transform.
""",
        ),
        _t(
            "The Laplace transform for circuits",
            "13 min",
            r"""\
# The Laplace transform for circuits

Phasors handle one steady sinusoid; the **Laplace transform** handles *any* input
(steps, pulses, decaying sinusoids) **and** the initial conditions, in one
framework. It maps a time function to a function of the complex variable
$s = \sigma + j\omega$:

$$F(s) = \int_0^\infty f(t)\,e^{-st}\,dt.$$

The magic is that differentiation becomes multiplication by $s$:

$$\mathcal{L}\!\left\{\frac{df}{dt}\right\} = sF(s) - f(0^-).$$

So the differential equations of a circuit turn into **algebra** in $s$. Each
element gets an **s-domain impedance**, a generalisation of the phasor impedance
with $j\omega \to s$:

$$Z_R = R, \qquad Z_L = sL, \qquad Z_C = \frac{1}{sC}.$$

```mermaid
flowchart LR
  T["Circuit ODE in t (with initial conditions)"] --> L["Laplace: replace d/dt by s"]
  L --> A["Algebraic network in s (Z_R=R, Z_L=sL, Z_C=1/sC)"]
  A --> S["Solve for V(s) / I(s)"]
  S --> I["Inverse-Laplace → response v(t), i(t)"]
```

Note that setting $s = j\omega$ recovers the phasor/AC result, and $s = 0$ (DC)
recovers the resistive case — Laplace contains both as special cases. Solve in
$s$ with ordinary algebra, then inverse-transform (usually by partial fractions)
to get $v(t)$.

**Next:** the ratio that characterises a circuit — the transfer function.
""",
        ),
        _t(
            "Transfer functions, poles & zeros",
            "12 min",
            r"""\
# Transfer functions, poles & zeros

With everything in the $s$-domain, a linear circuit is summarised by its
**transfer function** — output over input, with initial conditions zero:

$$H(s) = \frac{Y(s)}{X(s)} = \frac{N(s)}{D(s)}.$$

It is a ratio of polynomials in $s$. Two sets of numbers tell you almost
everything:

- **Zeros:** roots of $N(s)$ — frequencies where the output is *nulled*.
- **Poles:** roots of $D(s)$ — the circuit's natural frequencies, which set
  stability and transient shape.

**Pole location decides behaviour** (recall $s = \sigma + j\omega$):

- Poles in the **left half-plane** ($\sigma < 0$) → decaying, **stable**.
- Poles on the **imaginary axis** → sustained oscillation.
- Poles in the **right half-plane** ($\sigma > 0$) → growing, **unstable**.

A first-order low-pass $H(s) = 1/(1 + s/\omega_c)$ has a single pole at
$s = -\omega_c$. Its magnitude response is flat in the passband and rolls off
past the **cutoff** $\omega_c$ (here $\omega_c = 5$, the $-3\text{dB}$ point):

```plot
{"title": "First-order low-pass: |H(ω)| with one pole at ω_c = 5", "xLabel": "ω (rad/s)", "yLabel": "|H(ω)|", "xRange": [0, 30], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1 + (x/5)^2)", "label": "|H(ω)| = 1/√(1+(ω/ω_c)²)", "color": "#2563eb"}], "points": [{"x": 5, "y": 0.707, "label": "ω_c → 0.707 (−3 dB)", "color": "#dc2626", "size": 7}]}
```

Reading off poles and zeros lets you sketch the **Bode plot** and judge stability
without solving any differential equation.

**Next:** describing a circuit by its ports — two-port networks.
""",
        ),
        _t(
            "Two-port networks",
            "12 min",
            r"""\
# Two-port networks

Amplifiers, filters and transmission lines are often treated as black boxes with
an **input port** and an **output port**. A **two-port network** characterises the
box purely by how its two port voltages and currents relate — no need to know the
internal topology.

Several equivalent parameter sets exist, each convenient for different work:

- **z-parameters** (impedance): $\mathbf{V} = \mathbf{z}\,\mathbf{I}$ — open-circuit
  tests.
- **y-parameters** (admittance): $\mathbf{I} = \mathbf{y}\,\mathbf{V}$ —
  short-circuit tests.
- **h-parameters** (hybrid): mix voltage and current — the classic for transistor
  models ($h_{fe}$ is the current gain $\beta$).
- **ABCD (transmission) parameters:** relate input to output as
  $\begin{bmatrix}V_1\\I_1\end{bmatrix} = \begin{bmatrix}A & B\\C & D\end{bmatrix}\begin{bmatrix}V_2\\-I_2\end{bmatrix}$.

The ABCD form has a superpower: **cascading** two-ports (output of one into the
input of the next) is just **matrix multiplication** of their ABCD matrices —
ideal for chained stages and transmission lines.

```mermaid
flowchart LR
  IN["Port 1: V1, I1"] --> N1["Two-port A (matrix M₁)"]
  N1 --> N2["Two-port B (matrix M₂)"]
  N2 --> OUT["Port 2: V2, I2 (overall = M₁·M₂)"]
```

Any one set converts to any other by algebra, so you measure in whatever way is
easiest and convert as needed.

**Next:** the magnetically coupled two-port — the transformer.
""",
        ),
        _t(
            "Coupled inductors & transformers",
            "12 min",
            r"""\
# Coupled inductors & transformers

When two inductors share magnetic flux, current in one induces voltage in the
other — they are **magnetically coupled**. The coupled equations are:

$$v_1 = L_1\frac{di_1}{dt} + M\frac{di_2}{dt}, \qquad
v_2 = M\frac{di_1}{dt} + L_2\frac{di_2}{dt},$$

where $M$ is the **mutual inductance**. The **coupling coefficient**

$$k = \frac{M}{\sqrt{L_1 L_2}}, \qquad 0 \le k \le 1$$

measures how much flux is shared ($k \to 1$ is tight coupling). **Dot
convention** marks the winding ends with matching flux polarity and fixes the
sign of $M$.

An **ideal transformer** ($k = 1$, no losses) scales voltage and current by the
**turns ratio** $n = N_1/N_2$:

$$\frac{V_1}{V_2} = n, \qquad \frac{I_1}{I_2} = \frac{1}{n},$$

so power in equals power out. A key consequence is **impedance reflection**: a
load $Z_L$ on the secondary appears from the primary as

$$Z_\text{in} = n^2 Z_L.$$

Step the turns ratio and watch a fixed $8\,\Omega$ secondary load reflect to the
primary as $n^2 \times 8$:

```plot
{"title": "Reflected impedance Z_in = n²·Z_L (Z_L = 8 Ω)", "xLabel": "turns ratio n = N1/N2", "yLabel": "Z_in (Ω)", "xRange": [0.5, 5], "yRange": [0, 100], "functions": [{"expr": "x^2*8", "label": "Z_in = n²·8", "color": "#2563eb"}], "points": [{"x": 2, "y": 32, "label": "n = 2 → 32 Ω", "color": "#dc2626", "size": 7}]}
```

This is how transformers match a loudspeaker to an amplifier, step grid voltages
up and down, and isolate circuits.

**Next:** put the whole toolkit to work.
""",
        ),
        _t(
            "Applied circuit analysis",
            "12 min",
            r"""\
# Applied circuit analysis

This capstone ties the track together by analysing one circuit several ways and
choosing the right tool for the question asked.

**Case study — a second-order RLC filter driving a load.**

1. **DC bias (resistive).** Open the capacitors, short the inductors, and use
   **nodal/mesh analysis** with **Thevenin** reduction to find the operating
   point — the Basics toolkit.
2. **Frequency response.** Replace elements with phasor impedances
   ($j\omega L$, $1/j\omega C$) and compute the transfer function $H(j\omega)$ to
   find the passband, cutoff and any **resonant** peak — the Intermediate/Advanced
   frequency view.
3. **Transient / stability.** Move to the **Laplace** $s$-domain, read the
   **poles** of $H(s)$, and predict whether the step response is over-,
   critically, or under-damped before simulating.

```mermaid
flowchart TD
  Q["What do I need to know?"] --> DC["Operating point? → nodal/mesh + Thevenin (s=0)"]
  Q --> FR["Filtering / gain vs frequency? → phasors, H(jω), resonance"]
  Q --> TR["Transient / stability? → Laplace H(s), poles & damping"]
```

A worked sanity check: a low-pass output that rolls off past its cutoff. Confirm
the $-3\text{dB}$ point matches the pole you computed (here $\omega_c = 8$):

```plot
{"title": "Applied check: low-pass magnitude, cutoff at ω_c = 8", "xLabel": "ω (rad/s)", "yLabel": "|H(ω)|", "xRange": [0, 40], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(1 + (x/8)^2)", "label": "|H(ω)|", "color": "#2563eb"}], "points": [{"x": 8, "y": 0.707, "label": "−3 dB at ω_c = 8", "color": "#dc2626", "size": 7}]}
```

**The throughline:** DC, AC and transient analysis are the *same* linear circuit
seen at $s = 0$, $s = j\omega$, and general $s$. Master the laws once and you read
a circuit in every regime.

**Next:** test what you've learned.
""",
        ),
    ),
)


CIRCUIT_ANALYSIS_COURSES: tuple[SeedCourse, ...] = (
    _CA_BASICS,
    _CA_INTERMEDIATE,
    _CA_ADVANCED,
)

__all__ = ["CIRCUIT_ANALYSIS_COURSES"]
