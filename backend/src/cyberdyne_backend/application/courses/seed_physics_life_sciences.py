"""Physics for Life Sciences track: Basics -> Intermediate -> Advanced.

An arc from the mechanics, energy and fluids of organisms, through
thermodynamics, diffusion and bioelectricity, to optics, spectroscopy and the
biophysics of macromolecules. Lessons embed interactive ```plot blocks for
quantitative curves (Michaelis-Menten, dose-response, decay) and ```mermaid
diagrams for pathways, instrument pipelines and method classifications.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Physics for Life Sciences — Basics ───────────────────────────────────────

_BASICS = SeedCourse(
    slug="physics-life-sciences-basics",
    title="Physics for Life Sciences — Basics",
    description=(
        "Physical intuition for biology: how forces and torques act on muscles "
        "and bones, why energy bookkeeping governs metabolism, and how fluids "
        "move through vessels. The qualitative and order-of-magnitude foundation "
        "for everything quantitative that follows."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why physics for living systems",
            "10 min",
            r"""
# Why physics for living systems

Living organisms are not exempt from physics — they are exquisite physical
machines operating under the same conservation laws as everything else. What
makes biophysics distinctive is **scale** and **noise**: a bacterium swims in a
world dominated by viscosity, a protein folds while being kicked by thermal
collisions, and your eye can detect a handful of photons.

A first tool is the **order-of-magnitude estimate**. Before any equation, ask:
how big, how fast, how much energy? The thermal energy scale $k_B T \approx
4.1 \times 10^{-21}$ J at body temperature sets the "currency" against which
molecular events are measured — a bond worth a few $k_B T$ is fragile, one worth
$20\,k_B T$ is stable.

A second tool is **dimensional analysis**: checking that units balance catches
most errors and often reveals scaling laws. Metabolic rate, for instance, scales
roughly as body mass to the $3/4$ power (Kleiber's law) across many orders of
magnitude.

```mermaid
flowchart LR
  A[Physical law] --> B[Scale & units]
  B --> C[Order-of-magnitude estimate]
  C --> D[Biological prediction]
  D --> E[Compare to data]
  E --> A
```

We will return to $k_B T$, scaling and estimation constantly.

**Next:** forces, torques and the lever mechanics of the body.
""",
        ),
        _t(
            "Forces, torques and the body as a lever",
            "11 min",
            r"""
# Forces, torques and the body as a lever

Muscles, bones and joints form systems of **levers**. A torque is
$\tau = r\,F\sin\theta$, the product of force, the distance from the pivot, and
the angle. Static equilibrium requires both the net force and the net torque to
vanish: $\sum F = 0$ and $\sum \tau = 0$.

Most skeletal joints are **third-class levers**: the muscle (effort) attaches
between the joint (fulcrum) and the load. Holding a mass in your hand, the biceps
inserts only a few centimetres from the elbow while the load sits ~30 cm away.
Balancing torques means the biceps must pull with a force many times the weight
held — the body trades force for **speed and range of motion**.

This is why a 5 kg weight can demand a 200 N muscle force: the short moment arm
of the muscle is its price for a large, fast hand displacement.

```plot
{"title": "Required muscle force vs load (third-class lever)", "xLabel": "load (kg)", "yLabel": "muscle force (N)", "xRange": [0, 10], "yRange": [0, 600], "grid": true, "functions": [{"expr": "58*x", "label": "F_muscle (arm ratio 6:1)", "color": "#2563eb"}]}
```

The line's steep slope is the mechanical *disadvantage* in force that buys
mechanical *advantage* in motion.

**Next:** energy, work and the power of metabolism.
""",
        ),
        _t(
            "Energy, work and metabolic power",
            "11 min",
            r"""
# Energy, work and metabolic power

Energy is conserved, and organisms are open systems that take in chemical energy
and dissipate it as work and heat. **Work** is $W = \int F\,dx$; **power** is the
rate of doing work, $P = dW/dt$, in watts.

A resting human dissipates about 100 W — comparable to a bright incandescent
bulb — the **basal metabolic rate**. During hard exercise, sustained power output
can reach several hundred watts, with peaks above 1 kW for seconds. The chemical
fuel is ultimately **ATP**, whose hydrolysis releases roughly $50$–$60$ kJ/mol
under cellular conditions.

Muscle efficiency — useful mechanical work divided by metabolic energy consumed —
is only about **20–25%**; the rest becomes heat, which is why exercise warms you.

```plot
{"title": "Mechanical work delivered vs metabolic energy used", "xLabel": "metabolic energy in (kJ)", "yLabel": "mechanical work out (kJ)", "xRange": [0, 100], "yRange": [0, 30], "grid": true, "functions": [{"expr": "0.25*x", "label": "25% efficient muscle", "color": "#16a34a"}]}
```

The shallow slope is the efficiency: most of the input energy never becomes
motion.

**Next:** pressure, buoyancy and fluids at rest.
""",
        ),
        _t(
            "Fluids at rest: pressure and buoyancy",
            "11 min",
            r"""
# Fluids at rest: pressure and buoyancy

Pressure is force per unit area, $P = F/A$, measured in pascals (1 mmHg ≈ 133
Pa). In a fluid at rest, pressure rises with depth: $P = P_0 + \rho g h$. This
**hydrostatic** term explains why blood pressure in your feet exceeds that in
your head when standing — a column of blood ~1.3 m tall adds roughly 100 mmHg.

**Archimedes' principle** states the buoyant force equals the weight of displaced
fluid, $F_B = \rho_{fluid}\,V\,g$. A fish tunes its density toward that of water
with a gas-filled swim bladder to hover effortlessly; humans float more easily in
dense seawater than in fresh water.

Surface tension, another rest property, lets water striders stand on ponds and
shapes the alveolar films in your lungs.

```plot
{"title": "Hydrostatic pressure vs depth in water", "xLabel": "depth (m)", "yLabel": "gauge pressure (kPa)", "xRange": [0, 10], "yRange": [0, 100], "grid": true, "functions": [{"expr": "9.81*x", "label": "rho*g*h", "color": "#2563eb"}]}
```

Each 10 m of water adds about one atmosphere — a fact every diver lives by.

**Next:** fluids in motion and blood flow.
""",
        ),
        _t(
            "Fluids in motion: flow and circulation",
            "11 min",
            r"""
# Fluids in motion: flow and circulation

When fluids move, two ideas dominate. **Continuity** conserves volume flow:
$A_1 v_1 = A_2 v_2$, so a fluid speeds up through a constriction. **Bernoulli's
principle** trades pressure for speed along a streamline,
$P + \tfrac{1}{2}\rho v^2 + \rho g h = \text{const}$, the basis for a partially
blocked artery showing a local pressure drop.

For the small, slow vessels of the body, viscosity rules. **Poiseuille's law**
gives the flow through a tube,
$$Q = \frac{\pi r^4 \Delta P}{8 \eta L},$$
where the **fourth power of radius** is decisive: halving a vessel's radius cuts
flow 16-fold. This is why arterioles, by slightly dilating or constricting,
control the body's blood distribution so powerfully.

```plot
{"title": "Poiseuille flow vs vessel radius (radius^4 law)", "xLabel": "radius (relative)", "yLabel": "flow Q (relative)", "xRange": [0, 2], "yRange": [0, 16], "grid": true, "functions": [{"expr": "x^4", "label": "Q ∝ r^4", "color": "#dc2626"}]}
```

The explosive rise with radius is what makes vascular tone such an effective
control knob.

**Next:** the master concept of thermal energy, $k_B T$.
""",
        ),
        _t(
            "Thermal energy and the scale of molecular life",
            "11 min",
            r"""
# Thermal energy and the scale of molecular life

At the molecular scale, everything jiggles. The **equipartition theorem** assigns
$\tfrac{1}{2} k_B T$ of energy to each quadratic degree of freedom, so a molecule
in solution carries thermal energy of order $k_B T \approx 4.1 \times 10^{-21}$ J
($\approx 0.6$ kcal/mol) at 310 K.

This single number is the reference for molecular biophysics. Whether a structure
holds together depends on the ratio of its binding energy to $k_B T$. The
probability of occupying a state of energy $E$ follows the **Boltzmann factor**
$e^{-E/k_B T}$: states only a few $k_B T$ above the ground state are still
visibly populated, while a barrier of $20\,k_B T$ makes a transition rare.

Thermal motion is also the engine of **diffusion** and the source of the random
kicks that fold proteins and let enzymes find substrates.

```plot
{"title": "Boltzmann occupancy vs energy (units of kT)", "xLabel": "energy E / kT", "yLabel": "relative population", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-x)", "label": "e^(-E/kT)", "color": "#16a34a"}]}
```

Memorise $k_B T$: it is the yardstick for every molecular argument to come.

**Next:** check your understanding with a short quiz.
""",
        ),
        _quiz(),
    ),
)


# ── Physics for Life Sciences — Intermediate ─────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="physics-life-sciences-intermediate",
    title="Physics for Life Sciences — Intermediate",
    description=(
        "The quantitative core: thermodynamics and free energy of biomolecules, "
        "the diffusion equation and transport across membranes, enzyme kinetics, "
        "and the electrical physics of nerve and muscle from Nernst to "
        "Hodgkin-Huxley."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Thermodynamics and free energy in cells",
            "12 min",
            r"""
# Thermodynamics and free energy in cells

Biology runs on **free energy**, not raw energy. The Gibbs free energy
$G = H - TS$ combines enthalpy and entropy; a process is spontaneous when
$\Delta G < 0$. For a reaction, $\Delta G = \Delta G^\circ + RT \ln Q$, where $Q$
is the reaction quotient, so even an unfavourable $\Delta G^\circ$ can be driven
forward by keeping products low and reactants high.

Cells exploit this with **coupling**: an endergonic reaction is paired with ATP
hydrolysis ($\Delta G^\circ \approx -30$ kJ/mol, but $\approx -50$ kJ/mol in vivo)
so the sum is negative. The second law still holds — local order is paid for by
exporting entropy as heat to the surroundings.

At equilibrium $\Delta G = 0$, which links the standard free energy to the
equilibrium constant: $\Delta G^\circ = -RT \ln K_{eq}$.

```plot
{"title": "Free energy vs equilibrium constant", "xLabel": "K_eq", "yLabel": "-ΔG° / RT", "xRange": [0.2, 20], "yRange": [-2, 3], "grid": true, "functions": [{"expr": "log(x)", "label": "ln K_eq", "color": "#2563eb"}]}
```

A tenfold shift in $K_{eq}$ costs only $\sim 5.9$ kJ/mol — free energy is a
logarithmic ledger.

**Next:** how molecules spread by diffusion.
""",
        ),
        _t(
            "Diffusion and random walks",
            "12 min",
            r"""
# Diffusion and random walks

Diffusion is the macroscopic face of molecular random walks. **Fick's first law**
relates flux to a concentration gradient, $J = -D\,\dfrac{dC}{dx}$, and combined
with conservation gives **Fick's second law**, the diffusion equation
$$\frac{\partial C}{\partial t} = D\,\frac{\partial^2 C}{\partial x^2}.$$

The key result is that mean-square displacement grows **linearly with time**:
$\langle x^2 \rangle = 2Dt$ in one dimension. So the time to diffuse a distance
$L$ scales as $L^2/D$ — fine for a micron-sized cell (milliseconds) but hopeless
across a metre, which is why large organisms need circulatory and respiratory
**bulk transport**, not diffusion alone.

The diffusion coefficient itself follows the **Stokes-Einstein** relation
$D = k_B T / 6\pi\eta r$: smaller molecules in less viscous fluid diffuse faster.

```plot
{"title": "Diffusion spreading: width vs time", "xLabel": "time (relative)", "yLabel": "RMS displacement", "xRange": [0, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "sqrt(2*x)", "label": "sqrt(2 D t)", "color": "#16a34a"}]}
```

The square-root growth is the signature of a random walk — and the reason
diffusion is slow over long distances.

**Next:** moving solutes across membranes.
""",
        ),
        _t(
            "Membranes, osmosis and transport",
            "12 min",
            r"""
# Membranes, osmosis and transport

The cell membrane is a selectively permeable lipid bilayer. Water moves across it
by **osmosis** down its own chemical potential, generating osmotic pressure
$\Pi = i\,c\,R\,T$ (van 't Hoff). A cell in hypotonic medium swells; in hypertonic
medium it shrinks — tonicity is a matter of pressures and balances.

Solutes cross by several routes. **Passive** transport (simple or facilitated
diffusion) runs downhill and saturates when carriers are full, looking just like
enzyme kinetics. **Active** transport runs uphill at the cost of ATP — the
Na$^+$/K$^+$-ATPase pumps 3 Na$^+$ out and 2 K$^+$ in per ATP, building the
gradients that power nerves and secondary transporters.

```mermaid
flowchart LR
  A[Solute outside] --> B{Gradient?}
  B -->|downhill| C[Passive: channels / carriers]
  B -->|uphill| D[Active: ATP-driven pump]
  C --> E[Cytoplasm]
  D --> E
  D --> F[Gradient stored as potential energy]
```

Facilitated transport saturates like a Michaelis-Menten curve — carriers are a
finite, shared resource.

**Next:** the quantitative laws of enzyme kinetics.
""",
        ),
        _t(
            "Enzyme kinetics: Michaelis-Menten",
            "12 min",
            r"""
# Enzyme kinetics: Michaelis-Menten

Enzymes accelerate reactions by lowering the activation barrier. The canonical
model treats binding then catalysis, $E + S \rightleftharpoons ES \to E + P$,
and under the steady-state assumption yields the **Michaelis-Menten** rate law
$$v = \frac{V_{max}[S]}{K_m + [S]}.$$

Here $V_{max} = k_{cat}[E]_0$ is the saturating velocity and $K_m$ is the
substrate concentration giving half-maximal rate — a measure of apparent affinity.
At low $[S]$ the rate is first-order in substrate; at high $[S]$ it plateaus
because every enzyme is occupied. The ratio $k_{cat}/K_m$ is the **specificity
constant**, gauging catalytic efficiency.

```plot
{"title": "Michaelis-Menten rate vs substrate", "xLabel": "[S] (units of K_m)", "yLabel": "v / V_max", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#2563eb"}]}
```

The hyperbola flattens as enzymes saturate — the visual heart of kinetics.
Inhibitors shift $K_m$ (competitive) or $V_{max}$ (non-competitive), the basis of
much drug design.

**Next:** the electrical physics of cells.
""",
        ),
        _t(
            "Bioelectricity: Nernst and membrane potentials",
            "12 min",
            r"""
# Bioelectricity: Nernst and membrane potentials

A resting cell holds a voltage across its membrane, typically about $-70$ mV
inside. It arises because ion gradients (set by pumps) act through selectively
permeable channels. For a single permeant ion, the equilibrium voltage is the
**Nernst potential**
$$E_{ion} = \frac{RT}{zF}\ln\frac{[\text{ion}]_{out}}{[\text{ion}]_{in}}.$$

For K$^+$ this is near $-90$ mV; for Na$^+$, near $+60$ mV. With several ions
permeant, the **Goldman-Hodgkin-Katz** equation weights each by its permeability,
giving the actual resting potential dominated by whichever ion the membrane lets
through most.

The membrane behaves electrically as a capacitor in parallel with conductances,
with time constant $\tau = R_m C_m$ — typically a few milliseconds.

```plot
{"title": "Nernst potential vs concentration ratio", "xLabel": "[out]/[in]", "yLabel": "E (mV, monovalent)", "xRange": [0.1, 20], "yRange": [-80, 80], "grid": true, "functions": [{"expr": "26.7*log(x)", "label": "(RT/F) ln(ratio)", "color": "#dc2626"}]}
```

The logarithmic law means large gradients give only modest voltages — yet enough
to fire a neuron.

**Next:** the action potential and Hodgkin-Huxley.
""",
        ),
        _t(
            "The action potential and Hodgkin-Huxley",
            "12 min",
            r"""
# The action potential and Hodgkin-Huxley

A neuron fires by briefly, dramatically changing its ion permeabilities. The
**Hodgkin-Huxley** model (Nobel 1963) describes the squid axon with
voltage-gated Na$^+$ and K$^+$ conductances whose gating variables ($m$, $h$,
$n$) follow first-order kinetics. The membrane equation is
$$C_m \frac{dV}{dt} = -g_{Na}m^3h(V-E_{Na}) - g_K n^4(V-E_K) - g_L(V-E_L) + I.$$

A suprathreshold stimulus triggers regenerative Na$^+$ influx (depolarisation),
then delayed K$^+$ efflux and Na$^+$ inactivation (repolarisation), producing the
all-or-none spike. The model is **excitable**: below threshold nothing happens;
above it, a full ~100 mV spike fires regardless of stimulus size.

```mermaid
flowchart LR
  A[Stimulus depolarizes V] --> B{V > threshold?}
  B -->|no| C[Decay back to rest]
  B -->|yes| D[Na+ channels open: upstroke]
  D --> E[K+ open, Na+ inactivate: downstroke]
  E --> F[Refractory period]
  F --> A
```

```plot
{"title": "Channel open-probability vs voltage (sigmoid gating)", "xLabel": "depolarization (mV above rest)", "yLabel": "open probability", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "voltage-gated activation", "color": "#2563eb"}]}
```

The sigmoid gating curve is what makes neurons threshold devices.

**Next:** test your grasp of the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# ── Physics for Life Sciences — Advanced ─────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="physics-life-sciences-advanced",
    title="Physics for Life Sciences — Advanced",
    description=(
        "State-of-the-art biophysics: light-matter interaction and fluorescence, "
        "spectroscopy and single-molecule methods, structure determination from "
        "cryo-EM to AlphaFold, the statistical physics of macromolecules, and "
        "molecular-dynamics and AI-driven computational biophysics."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Light and matter: optics for the life sciences",
            "13 min",
            r"""
# Light and matter: optics for the life sciences

Light interacts with biological matter through absorption, scattering and
emission. Absorption follows the **Beer-Lambert law**, $A = \varepsilon c \ell$,
where the molar absorptivity $\varepsilon$, concentration $c$ and path length
$\ell$ set how much light a sample removes — the basis of every spectrophotometer
and the $A_{260}/A_{280}$ ratio used to assess nucleic-acid purity.

Resolution in light microscopy is bounded by **diffraction**: the Abbe limit is
$d \approx \lambda / (2\,\text{NA})$, about 200 nm for visible light. This wall
motivated **super-resolution** methods (STED, PALM/STORM; Nobel 2014) that beat
it by controlling which molecules emit at a time.

```plot
{"title": "Beer-Lambert: transmitted light vs concentration", "xLabel": "concentration × path (a.u.)", "yLabel": "transmittance I/I0", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "I/I0 = 10^(-εcl)", "color": "#dc2626"}]}
```

Transmittance falls exponentially with concentration, so absorbance (its log) is
the linear, useful quantity.

**Next:** fluorescence and the methods built on it.
""",
        ),
        _t(
            "Fluorescence, FRET and spectroscopy",
            "13 min",
            r"""
# Fluorescence, FRET and spectroscopy

Fluorescence is the workhorse of modern biology. A fluorophore absorbs a photon,
loses some energy to vibrations (the **Stokes shift**), then re-emits at a longer
wavelength — the basis of GFP imaging and flow cytometry. Excited-state lifetimes
of nanoseconds are read by **FLIM**, and bleaching/blinking statistics underpin
single-molecule counting.

**FRET** (Förster resonance energy transfer) turns a donor-acceptor pair into a
molecular ruler. Transfer efficiency depends steeply on separation,
$$E = \frac{1}{1 + (r/R_0)^6},$$
where $R_0$ (~5 nm) is the Förster radius. The sixth-power dependence makes FRET
exquisitely sensitive over the 2–8 nm range — perfect for reporting protein
conformational changes and binding.

```plot
{"title": "FRET efficiency vs donor-acceptor distance", "xLabel": "distance r (units of R0)", "yLabel": "transfer efficiency E", "xRange": [0.3, 3], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+x^6)", "label": "E = 1/(1+(r/R0)^6)", "color": "#16a34a"}]}
```

The sharp drop near $r = R_0$ is what makes FRET a precise nanometre ruler.

**Next:** watching one molecule at a time.
""",
        ),
        _t(
            "Single-molecule biophysics and force spectroscopy",
            "13 min",
            r"""
# Single-molecule biophysics and force spectroscopy

Bulk experiments report averages; single-molecule methods reveal the **rare
states and stochastic dynamics** hidden underneath. **Optical and magnetic
tweezers** and the **AFM** apply piconewton forces to a single DNA strand,
protein or motor, while reading nanometre displacements — enough to watch a
kinesin step 8 nm along a microtubule, ATP by ATP.

Pulling on a folded molecule biases its energy landscape. Bell's model predicts
that an applied force $F$ lowers an unfolding barrier, so the off-rate grows
exponentially, $k(F) = k_0\,e^{F x^\ddagger / k_B T}$, where $x^\ddagger$ is the
distance to the transition state. Force spectroscopy thus maps the **energy
landscape** of folding and binding directly.

```plot
{"title": "Bell model: unfolding rate vs applied force", "xLabel": "force (pN)", "yLabel": "off-rate (relative)", "xRange": [0, 10], "yRange": [0, 20], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "k(F) = k0 e^(F x‡/kT)", "color": "#dc2626"}]}
```

Force is exponentially powerful — modest piconewtons can accelerate unfolding
millionfold.

**Next:** how molecular structures are actually solved.
""",
        ),
        _t(
            "Structure determination: X-ray, NMR and cryo-EM",
            "13 min",
            r"""
# Structure determination: X-ray, NMR and cryo-EM

Knowing a macromolecule's atomic structure is half of understanding its function.
Three experimental pillars dominate, complemented by computation.

```mermaid
flowchart LR
  A[Purified macromolecule] --> B[X-ray crystallography]
  A --> C[Solution NMR]
  A --> D[Cryo-EM]
  B --> E[Atomic coordinates / PDB]
  C --> E
  D --> E
  E --> F[Mechanism, drug design, validation]
```

**X-ray crystallography** reads the diffraction of a crystal; the intensities
give amplitudes but not phases — the famous *phase problem*, solved by molecular
replacement or anomalous scattering. **NMR** works in solution and uniquely
reports dynamics, but is limited to smaller proteins. **Cryo-EM** (Nobel 2017)
flash-freezes single particles and averages tens of thousands of noisy images;
the **resolution revolution** from direct electron detectors now reaches near
atomic resolution for large complexes that never crystallise.

Resolution improves as roughly $1/\sqrt{N}$ with the number $N$ of averaged
particles — the statistical engine behind cryo-EM.

```plot
{"title": "Cryo-EM: resolution gain from particle averaging", "xLabel": "particles averaged (×10k)", "yLabel": "relative SNR", "xRange": [0, 10], "yRange": [0, 4], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "SNR ∝ sqrt(N)", "color": "#2563eb"}]}
```

**Next:** the statistical physics of how chains fold.
""",
        ),
        _t(
            "Statistical physics of macromolecules",
            "13 min",
            r"""
# Statistical physics of macromolecules

A protein or DNA molecule is a polymer buffeted by thermal noise, so its
behaviour is statistical. An unfolded chain behaves like a **random coil** whose
size scales as $R \sim b\,N^\nu$ with the number of segments $N$; an ideal chain
has $\nu = 1/2$, a swollen self-avoiding one $\nu \approx 3/5$.

**Folding** is the search across a rugged free-energy landscape for the native
minimum — Levinthal's paradox (too many conformations to search blindly) is
resolved by a **funnelled** landscape that channels the chain downhill. Cooperative
folding often looks **two-state**, switching sharply with temperature or
denaturant like a sigmoidal transition, with stability set by the balance of
chain entropy against favourable contacts.

The fraction folded follows a Boltzmann competition, $f = 1/(1 + e^{\Delta G/k_B T})$,
sharp because $\Delta G$ aggregates many small interactions.

```plot
{"title": "Two-state folding transition", "xLabel": "denaturant / temperature (a.u.)", "yLabel": "fraction unfolded", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "cooperative unfolding", "color": "#16a34a"}]}
```

The steep sigmoid is cooperativity made visible — folding is nearly all-or-none.

**Next:** simulating and predicting structure with computation and AI.
""",
        ),
        _t(
            "Computational and AI biophysics",
            "13 min",
            r"""
# Computational and AI biophysics

Computation now sits beside experiment as a first-class tool. **Molecular
dynamics** (MD) integrates Newton's equations for every atom under a force field
(AMBER, CHARMM), with femtosecond timesteps; specialised hardware (Anton) and
GPU codes (GROMACS, OpenMM) reach microseconds to milliseconds, long enough to
watch folding and ligand binding. Free-energy methods (umbrella sampling,
metadynamics, FEP) extract $\Delta G$ for binding, central to drug design.

The deep-learning era reshaped the field. **AlphaFold2** (and AlphaFold3,
RoseTTAFold) predict protein structure from sequence at near-experimental
accuracy, solving a 50-year grand challenge; diffusion models like **RFdiffusion**
now *design* novel proteins. AI also accelerates MD via **machine-learned
potentials** that approach quantum accuracy at classical cost.

```mermaid
flowchart LR
  A[Sequence] --> B[AlphaFold / RoseTTAFold]
  B --> C[Predicted structure]
  C --> D[MD refinement & dynamics]
  D --> E[Free-energy / binding ΔG]
  E --> F[Drug & protein design]
  F --> G[Experimental validation]
  G --> B
```

```plot
{"title": "Accessible MD timescale over the years", "xLabel": "years (since 2005)", "yLabel": "log10 sim length (s)", "xRange": [0, 15], "yRange": [-9, -3], "grid": true, "functions": [{"expr": "-9+0.4*x", "label": "Moore-like growth in MD reach", "color": "#2563eb"}]}
```

Exponential growth in compute keeps pushing simulation toward biological
timescales.

**Next:** the final comprehensive quiz.
""",
        ),
        _quiz(),
    ),
)


PHYSICS_LIFE_SCIENCES_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PHYSICS_LIFE_SCIENCES_COURSES"]
