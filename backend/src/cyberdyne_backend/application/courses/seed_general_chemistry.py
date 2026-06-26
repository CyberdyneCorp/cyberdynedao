"""General & Inorganic Chemistry track: Basics -> Intermediate -> Advanced.

A university-level arc from atoms, bonding and stoichiometry, through chemical
equilibria, acids/bases and reaction kinetics, to coordination chemistry, the
solid state and metals in biology. Lessons embed interactive ```plot blocks for
quantitative relationships (titration curves, Arrhenius behaviour, decay,
binding) and ```mermaid diagrams for classifications and pipelines, with LaTeX
formulas throughout. Quizzes are attached from the central registry at assembly.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- General & Inorganic Chemistry -- Basics -----------------------------------

_BASICS = SeedCourse(
    slug="general-chemistry-basics",
    title="General & Inorganic Chemistry — Basics",
    description=(
        "The foundations of chemistry: atomic structure and the quantum model, "
        "the periodic table and periodic trends, the major types of chemical "
        "bonding, the mole concept and stoichiometry, balancing reactions and "
        "the states of matter. Built for first-year university students with "
        "interactive plots, Mermaid classifications and worked numerical examples."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Atoms and the quantum model",
            "12 min",
            r"""
# Atoms and the quantum model

All matter is built from **atoms**: a tiny, dense **nucleus** of positively
charged **protons** and neutral **neutrons**, surrounded by **electrons**. The
number of protons is the **atomic number** $Z$ and defines the element; protons
plus neutrons give the **mass number** $A$. Atoms of one element with different
neutron counts are **isotopes** (e.g. $^{12}$C and $^{14}$C).

Electrons do not orbit like planets. The **quantum model** describes them by
**orbitals** — regions of space where an electron is likely to be found,
governed by four quantum numbers $(n, \ell, m_\ell, m_s)$. The principal number
$n$ sets the shell and energy; $\ell$ sets the subshell shape (s, p, d, f).

The energy of a hydrogen level falls off as $1/n^2$:

$$E_n = -\frac{13.6\ \text{eV}}{n^2}$$

so levels crowd together as $n$ grows — the basis of atomic spectra.

```plot
{"title": "Hydrogen energy levels E_n = -13.6/n^2", "xLabel": "principal quantum number n", "yLabel": "energy (eV)", "xRange": [1, 6], "yRange": [-15, 1], "grid": true, "functions": [{"expr": "-13.6/(x*x)", "label": "E_n", "color": "#2563eb"}]}
```

Electrons fill orbitals following the **Aufbau** order, the **Pauli exclusion
principle** (two electrons per orbital, opposite spin) and **Hund's rule**. This
electron configuration drives everything chemical.

**Next:** how the periodic table organises these configurations.
""",
        ),
        _t(
            "The periodic table and trends",
            "12 min",
            r"""
# The periodic table and trends

Arranged by increasing $Z$, the periodic table groups elements with similar
**valence electron configurations** into vertical **groups** and horizontal
**periods**. The structure mirrors orbital filling: s-block (groups 1–2),
p-block (13–18), d-block (transition metals) and f-block (lanthanides/actinides).

```mermaid
flowchart LR
  PT["Periodic table"] --> S["s-block: alkali, alkaline earth"]
  PT --> P["p-block: nonmetals, halogens, noble gases"]
  PT --> D["d-block: transition metals"]
  PT --> F["f-block: lanthanides, actinides"]
```

Three trends explain most reactivity:

- **Atomic radius** *decreases* across a period (rising nuclear charge pulls
  electrons in) and *increases* down a group (more shells).
- **Ionisation energy** — the energy to remove an electron — *increases*
  across, *decreases* down.
- **Electronegativity** (Pauling scale) measures pull on bonding electrons:
  fluorine is highest (3.98), francium lowest.

Effective nuclear charge $Z_{eff} = Z - S$ (with screening $S$) drives the
across-period rise:

```plot
{"title": "Ionisation energy rising with effective nuclear charge", "xLabel": "Z_eff", "yLabel": "relative ionisation energy", "xRange": [1, 8], "yRange": [0, 9], "grid": true, "functions": [{"expr": "x", "label": "~ Z_eff", "color": "#dc2626"}]}
```

Noble gases sit at the right with full shells — chemically inert — explaining why
other atoms react to reach such stable configurations.

**Next:** the bonds atoms form to gain stability.
""",
        ),
        _t(
            "Chemical bonding basics",
            "13 min",
            r"""
# Chemical bonding basics

Atoms bond to lower their energy, often approaching a full **octet** of valence
electrons. Three idealised bond types span a continuum set by the
**electronegativity difference** $\Delta\chi$:

| Bond | Mechanism | $\Delta\chi$ | Example |
|------|-----------|--------------|---------|
| **Ionic** | electron transfer, electrostatic attraction | large (> ~1.7) | NaCl |
| **Polar covalent** | unequal sharing | intermediate | H$_2$O |
| **Nonpolar covalent** | equal sharing | ~0 | N$_2$ |

```mermaid
flowchart LR
  A["Two atoms"] --> B{"electronegativity difference?"}
  B -->|large| C["Ionic: transfer e-"]
  B -->|intermediate| D["Polar covalent"]
  B -->|small| E["Nonpolar covalent"]
```

**Lewis structures** track valence electrons as bonding pairs and lone pairs.
**VSEPR theory** then predicts geometry: electron domains repel and spread out,
so 2 domains give linear ($180°$), 3 trigonal planar ($120°$), 4 tetrahedral
($109.5°$). Lone pairs compress angles — water is bent at about $104.5°$.

Bond strength rises and bond length shrinks as bond order increases (single <
double < triple). A Morse-like potential captures the energy well of a bond:

```plot
{"title": "Bond energy well (Morse-like potential)", "xLabel": "internuclear distance (arb.)", "yLabel": "potential energy", "xRange": [0.5, 5], "yRange": [-5, 5], "grid": true, "functions": [{"expr": "5*(exp(-2*(x-1))-2*exp(-(x-1)))", "label": "V(r)", "color": "#16a34a"}]}
```

**Next:** counting atoms with the mole and stoichiometry.
""",
        ),
        _t(
            "The mole and stoichiometry",
            "12 min",
            r"""
# The mole and stoichiometry

Chemistry is quantitative, and the bridge between the atomic and lab scales is
the **mole**. One mole contains **Avogadro's number** of particles:

$$N_A = 6.022 \times 10^{23}\ \text{mol}^{-1}$$

The **molar mass** $M$ (g/mol) numerically equals the atomic/molecular mass in
unified atomic mass units, so moles $n = m / M$. Concentration in solution is
**molarity** $c = n / V$ (mol/L).

A balanced equation gives the **mole ratios** that link reactants to products.
For ammonia synthesis:

$$\text{N}_2 + 3\,\text{H}_2 \rightarrow 2\,\text{NH}_3$$

one mole of N$_2$ needs three of H$_2$ and yields two of NH$_3$. Stoichiometry
is just unit conversion through these ratios.

```mermaid
flowchart LR
  M["mass (g)"] -->|/ M| MOL1["moles reactant"]
  MOL1 -->|mole ratio| MOL2["moles product"]
  MOL2 -->|x M| MASS2["mass product (g)"]
```

The **limiting reagent** runs out first and caps the yield. Product formed grows
linearly with the limiting reagent until it is exhausted:

```plot
{"title": "Product yield limited by reagent supply", "xLabel": "moles of limiting reagent", "yLabel": "moles of product", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "ideal yield", "color": "#2563eb"}]}
```

**Percent yield** = (actual / theoretical) $\times 100\%$ reports real-world loss.

**Next:** writing and balancing the reactions themselves.
""",
        ),
        _t(
            "Reactions and balancing equations",
            "11 min",
            r"""
# Reactions and balancing equations

A chemical equation is balanced when each element has equal atoms on both sides —
demanded by **conservation of mass**. You adjust **coefficients** (never
subscripts, which would change the substance).

Common reaction classes:

```mermaid
flowchart TB
  R["Reaction types"] --> COMB["Combination A + B -> AB"]
  R --> DECOMP["Decomposition AB -> A + B"]
  R --> DISP["Single displacement"]
  R --> META["Double displacement / precipitation"]
  R --> COMBUST["Combustion (with O2)"]
  R --> REDOX["Redox (electron transfer)"]
```

**Redox** reactions exchange electrons; **oxidation** is loss, **reduction** is
gain (LEO–GER). Track **oxidation states** to identify what is oxidised and
reduced, then balance electrons (often via half-reactions in acid or base).

For combustion of methane:

$$\text{CH}_4 + 2\,\text{O}_2 \rightarrow \text{CO}_2 + 2\,\text{H}_2\text{O}$$

Oxygen demand scales with fuel burned; for a general hydrocarbon the required
O$_2$ rises steeply with carbon number:

```plot
{"title": "O2 needed to burn a saturated hydrocarbon CnH(2n+2)", "xLabel": "carbon number n", "yLabel": "moles O2 per mole fuel", "xRange": [1, 8], "yRange": [0, 14], "grid": true, "functions": [{"expr": "(3*x+1)/2", "label": "(3n+1)/2", "color": "#dc2626"}]}
```

**Next:** how matter is held together in its physical states.
""",
        ),
        _t(
            "States of matter and gas laws",
            "12 min",
            r"""
# States of matter and gas laws

Matter exists as **solid**, **liquid** or **gas**, set by the balance between
**kinetic energy** (temperature) and **intermolecular forces** (dispersion,
dipole–dipole, hydrogen bonding). Phase changes — melting, vaporisation,
sublimation — absorb or release energy without changing temperature.

```mermaid
flowchart LR
  S["Solid"] -->|melt| L["Liquid"]
  L -->|vaporise| G["Gas"]
  S -->|sublime| G
  G -->|condense| L
  L -->|freeze| S
```

Gases are the simplest to model. The **ideal gas law** ties together the state
variables:

$$PV = nRT, \qquad R = 8.314\ \text{J mol}^{-1}\text{K}^{-1}$$

At fixed $n$ and $T$, **Boyle's law** gives the inverse pressure–volume curve;
at fixed $n$ and $P$, **Charles's law** makes volume rise linearly with absolute
temperature.

```plot
{"title": "Boyle's law: P inversely proportional to V", "xLabel": "volume V (L)", "yLabel": "pressure P (atm)", "xRange": [0.5, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "10/x", "label": "P = nRT/V", "color": "#16a34a"}]}
```

Real gases deviate at high pressure and low temperature, where molecular size
and attractions matter — captured by the **van der Waals equation**. Kinetic
molecular theory connects $T$ to the average kinetic energy of the particles.

**Next:** test your grasp of the foundations.
""",
        ),
        _quiz(),
    ),
)


# -- General & Inorganic Chemistry -- Intermediate -----------------------------

_INTERMEDIATE = SeedCourse(
    slug="general-chemistry-intermediate",
    title="General & Inorganic Chemistry — Intermediate",
    description=(
        "The quantitative core of general chemistry: chemical equilibrium and "
        "Le Chatelier's principle, acids and bases with pH and buffers, "
        "thermochemistry and enthalpy, chemical kinetics and rate laws, "
        "electrochemistry and cell potentials, and solubility/precipitation "
        "equilibria. Worked equations, titration curves and Arrhenius plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Chemical equilibrium",
            "13 min",
            r"""
# Chemical equilibrium

Most reactions are **reversible** and settle to a **dynamic equilibrium** where
forward and reverse rates are equal — concentrations stop changing but reactions
continue. For $a\,A + b\,B \rightleftharpoons c\,C + d\,D$:

$$K_c = \frac{[C]^c [D]^d}{[A]^a [B]^b}$$

A large $K$ favours products; a small $K$ favours reactants. The **reaction
quotient** $Q$ uses current (non-equilibrium) concentrations: if $Q < K$ the
reaction proceeds forward, if $Q > K$ it reverses.

```mermaid
flowchart LR
  Q{"compare Q to K"}
  Q -->|Q < K| F["shift forward (make products)"]
  Q -->|Q = K| E["at equilibrium"]
  Q -->|Q > K| R["shift reverse (make reactants)"]
```

**Le Chatelier's principle**: a system at equilibrium responds to a stress
(concentration, pressure, temperature) by shifting to partially offset it. Adding
reactant pushes forward; compressing a gas mixture favours the side with fewer
moles; heating shifts an endothermic reaction forward.

As you add reactant, the equilibrium amount of product climbs toward a plateau —
a saturating response:

```plot
{"title": "Product at equilibrium vs added reactant", "xLabel": "added reactant (arb.)", "yLabel": "product at equilibrium", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "equilibrium product", "color": "#2563eb"}]}
```

$K$ links to thermodynamics via $\Delta G° = -RT \ln K$.

**Next:** the most important equilibrium in water — acids and bases.
""",
        ),
        _t(
            "Acids, bases and pH",
            "14 min",
            r"""
# Acids, bases and pH

The **Bronsted–Lowry** model defines an **acid** as a proton ($\text{H}^+$)
donor and a **base** as a proton acceptor; every acid has a **conjugate base**.
Water self-ionises with $K_w = [\text{H}^+][\text{OH}^-] = 10^{-14}$ at 25 °C.

The **pH** scale compresses concentration logarithmically:

$$\text{pH} = -\log_{10}[\text{H}^+], \qquad \text{pH} + \text{pOH} = 14$$

Strong acids dissociate fully; **weak acids** only partly, with acid dissociation
constant $K_a$ (and $\text{p}K_a = -\log K_a$). The **Henderson–Hasselbalch**
equation governs buffers:

$$\text{pH} = \text{p}K_a + \log\frac{[\text{A}^-]}{[\text{HA}]}$$

A **buffer** resists pH change near pH $= \text{p}K_a$, where the ratio of
conjugate base to acid is balanced.

```mermaid
flowchart LR
  HA["weak acid HA"] -->|donate H+| AP["conjugate base A-"]
  AP -->|accept H+| HA
  W["add acid/base"] -->|buffer absorbs| HA
```

A titration of a weak acid with strong base produces the classic sigmoidal
curve, steepest at the equivalence point:

```plot
{"title": "Weak-acid titration curve (sigmoidal)", "xLabel": "volume of base added (mL)", "yLabel": "pH", "xRange": [0, 10], "yRange": [0, 14], "grid": true, "functions": [{"expr": "2+12/(1+exp(-(x-5)))", "label": "pH vs added base", "color": "#dc2626"}]}
```

**Next:** the heat that accompanies reactions.
""",
        ),
        _t(
            "Thermochemistry and enthalpy",
            "12 min",
            r"""
# Thermochemistry and enthalpy

Thermochemistry tracks **heat** in chemical change. At constant pressure the heat
flow equals the **enthalpy change** $\Delta H$. Reactions that release heat are
**exothermic** ($\Delta H < 0$); those that absorb it are **endothermic**
($\Delta H > 0$).

**Hess's law**: enthalpy is a **state function**, so $\Delta H$ for an overall
reaction is the sum of any sequence of steps that add to it. We tabulate
**standard enthalpies of formation** $\Delta H_f°$ and compute:

$$\Delta H°_{rxn} = \sum n\,\Delta H_f°(\text{products}) - \sum n\,\Delta H_f°(\text{reactants})$$

```mermaid
flowchart LR
  REAC["reactants"] -->|path 1| PROD["products"]
  REAC -->|intermediate A| INT["intermediate"]
  INT -->|intermediate B| PROD
  PROD -.->|same total Delta H| REAC
```

Calorimetry measures heat from temperature change: $q = m\,c\,\Delta T$, with
$c$ the specific heat. The heat delivered to a sample rises linearly with the
temperature change you drive:

```plot
{"title": "Calorimetry: heat absorbed vs temperature rise", "xLabel": "temperature change Delta T (K)", "yLabel": "heat q (kJ)", "xRange": [0, 20], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.42*x", "label": "q = m c Delta T", "color": "#16a34a"}]}
```

Spontaneity also needs **entropy** $S$: the **Gibbs free energy**
$\Delta G = \Delta H - T\,\Delta S$ is negative for spontaneous processes.

**Next:** how fast reactions actually go.
""",
        ),
        _t(
            "Chemical kinetics",
            "14 min",
            r"""
# Chemical kinetics

Kinetics studies **reaction rate** and **mechanism** — distinct from
thermodynamics, which only says whether a reaction *can* happen. The **rate law**
relates rate to concentrations:

$$\text{rate} = k\,[A]^m[B]^n$$

where $m, n$ are the **reaction orders** (found experimentally, not from
coefficients) and $k$ is the **rate constant**. A first-order reaction decays
exponentially with a constant **half-life** $t_{1/2} = \ln 2 / k$:

$$[A]_t = [A]_0\,e^{-kt}$$

```plot
{"title": "First-order decay of reactant concentration", "xLabel": "time (s)", "yLabel": "[A] / [A]_0", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "first-order decay", "color": "#2563eb"}]}
```

Rate constants rise with temperature via the **Arrhenius equation**:

$$k = A\,e^{-E_a / RT}$$

where $E_a$ is the **activation energy** — the barrier of the transition state.
A **catalyst** lowers $E_a$ by providing an alternative pathway, speeding both
directions without being consumed.

```mermaid
flowchart LR
  R["reactants"] -->|climb E_a| TS["transition state"]
  TS -->|release| P["products"]
  CAT["catalyst"] -.->|lowers E_a| TS
```

The exponential dependence means a modest temperature increase can multiply the
rate — the rule of thumb that rate roughly doubles per 10 K.

**Next:** reactions that move electrons through a wire.
""",
        ),
        _t(
            "Electrochemistry",
            "13 min",
            r"""
# Electrochemistry

Electrochemistry harnesses **redox** reactions to drive or extract electrical
work. A **galvanic (voltaic) cell** spontaneously converts chemical energy to
electricity; an **electrolytic cell** uses electricity to force a nonspontaneous
reaction.

```mermaid
flowchart LR
  ANODE["anode (oxidation, -)"] -->|electrons via wire| CATHODE["cathode (reduction, +)"]
  ANODE -->|ions via salt bridge| CATHODE
```

Each half-reaction has a **standard reduction potential** $E°$ (vs the standard
hydrogen electrode). The overall cell potential is:

$$E°_{cell} = E°_{cathode} - E°_{anode}$$

A positive $E°_{cell}$ means spontaneous, tied to free energy by
$\Delta G° = -nFE°_{cell}$ with Faraday's constant $F = 96485\ \text{C/mol}$.

Away from standard conditions the **Nernst equation** corrects for
concentrations:

$$E = E° - \frac{RT}{nF}\ln Q$$

so cell voltage falls logarithmically as products accumulate (as $Q$ rises):

```plot
{"title": "Nernst: cell potential falls as ln Q rises", "xLabel": "reaction quotient Q", "yLabel": "cell potential E (V)", "xRange": [0.1, 10], "yRange": [0.5, 1.5], "grid": true, "functions": [{"expr": "1.1-0.0257*log(x)", "label": "E vs Q (n=1)", "color": "#dc2626"}]}
```

This underlies batteries, fuel cells, corrosion and electroplating.

**Next:** when ionic solids dissolve — solubility equilibria.
""",
        ),
        _t(
            "Solubility and precipitation",
            "11 min",
            r"""
# Solubility and precipitation

A sparingly soluble salt in water sits at equilibrium with its dissolved ions,
described by the **solubility product** $K_{sp}$. For
$\text{M}_a\text{X}_b(s) \rightleftharpoons a\,\text{M}^{n+} + b\,\text{X}^{m-}$:

$$K_{sp} = [\text{M}^{n+}]^a[\text{X}^{m-}]^b$$

Comparing the **ion product** $Q$ to $K_{sp}$ predicts precipitation: $Q > K_{sp}$
means a solid forms, $Q < K_{sp}$ means it keeps dissolving.

```mermaid
flowchart LR
  S["ionic solid"] -->|dissolve| IONS["dissolved ions"]
  IONS -->|Q > Ksp| PPT["precipitate forms"]
  IONS -->|Q < Ksp| DISS["stays dissolved"]
```

The **common-ion effect** suppresses solubility: adding an ion already in the
equilibrium shifts it back toward the solid. As the added common-ion
concentration grows, molar solubility falls sharply:

```plot
{"title": "Common-ion effect: solubility vs added common ion", "xLabel": "added common-ion concentration (arb.)", "yLabel": "molar solubility", "xRange": [0.1, 5], "yRange": [0, 5], "grid": true, "functions": [{"expr": "1/x", "label": "solubility ~ 1/[ion]", "color": "#16a34a"}]}
```

Selective precipitation, complex-ion formation and pH all tune solubility —
central to qualitative analysis and to keeping metals in or out of solution.

**Next:** test the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# -- General & Inorganic Chemistry -- Advanced ---------------------------------

_ADVANCED = SeedCourse(
    slug="general-chemistry-advanced",
    title="General & Inorganic Chemistry — Advanced",
    description=(
        "State-of-the-art inorganic chemistry: coordination compounds and "
        "crystal field theory, organometallics and catalysis, solid-state and "
        "materials chemistry, bioinorganic chemistry and metals in biology, "
        "spectroscopic and computational methods including DFT and machine "
        "learning for materials discovery. Applied, research-grade material."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Coordination chemistry",
            "14 min",
            r"""
# Coordination chemistry

A **coordination compound** is a central **metal** ion bonded to surrounding
**ligands** — Lewis bases donating electron pairs into the metal's empty
orbitals. The number of donor atoms is the **coordination number** (commonly 4
or 6), setting the geometry (tetrahedral, square planar, octahedral).

```mermaid
flowchart LR
  M["metal centre (Lewis acid)"] --> L1["ligand 1 (Lewis base)"]
  M --> L2["ligand 2"]
  M --> L3["ligand n"]
  L1 -.->|donate lone pair| M
```

**Ligands** range from monodentate (NH$_3$, Cl$^-$) to **polydentate chelators**
(ethylenediamine, EDTA) that wrap the metal. Chelation gives a large stability
boost — the **chelate effect**, driven mostly by entropy as one big ligand
releases several small ones.

Nomenclature, isomerism (geometric *cis/trans*, optical $\Delta/\Lambda$) and
**18-electron counting** organise the field. The stepwise formation constants
$K_1, K_2, \dots$ multiply to an overall $\beta_n$; the fraction of metal bound
rises sigmoidally with ligand concentration:

```plot
{"title": "Fraction of metal complexed vs ligand concentration", "xLabel": "ligand concentration (arb.)", "yLabel": "fraction bound", "xRange": [0.1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating binding", "color": "#2563eb"}]}
```

Coordination chemistry underpins catalysis, pigments, MRI contrast agents and
metalloenzymes.

**Next:** how d-orbitals split — crystal field theory.
""",
        ),
        _t(
            "Crystal field and ligand field theory",
            "14 min",
            r"""
# Crystal field and ligand field theory

**Crystal field theory (CFT)** explains the colour, magnetism and stability of
transition-metal complexes by how ligands split the five degenerate **d-orbitals**.
In an **octahedral** field the orbitals pointing at ligands ($e_g$:
$d_{z^2}, d_{x^2-y^2}$) rise in energy while the others ($t_{2g}$) fall, separated
by the **splitting parameter** $\Delta_o$.

```mermaid
flowchart LR
  D["5 degenerate d-orbitals"] --> EG["e_g (higher) d(z2), d(x2-y2)"]
  D --> T2G["t_2g (lower) d(xy), d(xz), d(yz)"]
  EG -.->|gap = Delta_o| T2G
```

The **spectrochemical series** ranks ligands by $\Delta_o$ they induce (I$^-$ <
... < CN$^-$, CO). A large $\Delta_o$ (strong field) forces a **low-spin**
configuration (electrons pair before occupying $e_g$); a small $\Delta_o$ gives
**high-spin**, set by whether $\Delta_o$ exceeds the pairing energy $P$.

Absorbed light of energy $\Delta_o$ sets the complex colour; the absorbed
wavelength is inversely related to the splitting:

```plot
{"title": "Absorption wavelength vs crystal-field splitting", "xLabel": "splitting Delta_o (arb.)", "yLabel": "absorbed wavelength (arb.)", "xRange": [1, 6], "yRange": [0, 6], "grid": true, "functions": [{"expr": "5/x", "label": "lambda ~ 1/Delta_o", "color": "#dc2626"}]}
```

**Ligand field theory** refines CFT with molecular-orbital covalency,
explaining $\pi$-donor/acceptor effects and the full spectrochemical ordering.

**Next:** metals bonded to carbon — organometallics and catalysis.
""",
        ),
        _t(
            "Organometallics and catalysis",
            "13 min",
            r"""
# Organometallics and catalysis

**Organometallic** chemistry studies metal–carbon bonds and the catalytic cycles
they enable. Stability often tracks the **18-electron rule**: a filled valence
shell (counting metal d-electrons plus ligand donations) is especially robust.

Elementary steps assemble into catalytic cycles:

```mermaid
flowchart LR
  M["active metal complex"] -->|oxidative addition| A["M(substrate)"]
  A -->|migratory insertion| B["M(intermediate)"]
  B -->|reductive elimination| P["product + regenerated M"]
  P --> M
```

Key steps are **oxidative addition**, **migratory insertion**, **transmetalation**
and **reductive elimination**. They power industrial and Nobel-winning chemistry:
**hydroformylation** (Rh/Co), Ziegler–Natta and metallocene **olefin
polymerisation**, and Pd cross-couplings (**Suzuki, Heck, Negishi**) for C–C bond
formation in pharma.

Catalysts increase **turnover frequency (TOF)** and total **turnover number
(TON)**. Like enzymes, many show Michaelis–Menten–type saturation as substrate
rises, since the active sites become rate-limited:

```plot
{"title": "Catalytic rate saturating with substrate (TOF)", "xLabel": "substrate concentration (arb.)", "yLabel": "turnover frequency", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturation kinetics", "color": "#16a34a"}]}
```

Homogeneous catalysts offer selectivity; heterogeneous ones offer easy
separation. Computational screening now guides ligand design.

**Next:** chemistry of extended solids and materials.
""",
        ),
        _t(
            "Solid-state and materials chemistry",
            "13 min",
            r"""
# Solid-state and materials chemistry

In the **solid state**, properties emerge from extended structure rather than
discrete molecules. **Crystalline** solids have periodic lattices (described by
**unit cells** and the 14 Bravais lattices); **amorphous** solids lack long-range
order. Close-packing (FCC, HCP) and **Bragg's law** ($n\lambda = 2d\sin\theta$)
underpin X-ray diffraction structure determination.

```mermaid
flowchart LR
  SOLID["solid"] --> CRYS["crystalline (periodic lattice)"]
  SOLID --> AMOR["amorphous (no long-range order)"]
  CRYS --> METAL["metallic"]
  CRYS --> IONIC["ionic"]
  CRYS --> COV["covalent network"]
  CRYS --> MOL["molecular"]
```

**Band theory** explains electrical behaviour: overlapping atomic orbitals form
continuous **bands**, and the **band gap** $E_g$ between valence and conduction
bands sorts materials into **metals** (no gap), **semiconductors** (small gap)
and **insulators** (large gap). Conductivity in a semiconductor follows a
thermally activated, Arrhenius-like rise:

```plot
{"title": "Semiconductor carrier population vs temperature factor", "xLabel": "temperature factor (arb.)", "yLabel": "relative conductivity", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "thermally activated", "color": "#2563eb"}]}
```

Defects, doping and nonstoichiometry tune properties — enabling LEDs,
perovskite solar cells, zeolite catalysts, superconductors and battery cathodes.

**Next:** the metals that run living cells.
""",
        ),
        _t(
            "Bioinorganic chemistry: metals in biology",
            "14 min",
            r"""
# Bioinorganic chemistry: metals in biology

Roughly a third of all proteins use **metal ions** for structure, electron
transfer or catalysis. **Bioinorganic chemistry** explains how nature tunes metal
centres with protein-supplied ligands.

```mermaid
flowchart LR
  M["metal cofactor"] --> O2["O2 transport: Fe in hemoglobin/myoglobin"]
  M --> ET["electron transfer: Fe-S clusters, cytochromes (Cu, Fe)"]
  M --> CAT["catalysis: Zn in carbonic anhydrase, Mo in nitrogenase"]
  M --> STR["structure: Zn fingers, Ca signalling"]
```

**Iron** in the **heme** of hemoglobin reversibly binds O$_2$; cooperative
binding across four subunits gives the famous **sigmoidal** oxygen-binding curve,
modelled by the **Hill equation** $\theta = p^n / (K + p^n)$ with $n > 1$:

```plot
{"title": "Cooperative O2 binding (Hill, n>1)", "xLabel": "oxygen partial pressure (arb.)", "yLabel": "fraction saturated", "xRange": [0.1, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "Hill (n=2)", "color": "#dc2626"}]}
```

Other highlights: **zinc** as a Lewis-acid catalyst in carbonic anhydrase;
**molybdenum/iron** in **nitrogenase** fixing N$_2$ to ammonia under ambient
conditions; **manganese** in photosystem II splitting water; **copper** and
**iron** clusters shuttling electrons in respiration. Metal toxicity and
chelation therapy (EDTA, deferoxamine) are the clinical flip side.

**Next:** the methods used to see and predict all of this.
""",
        ),
        _t(
            "Spectroscopy and computational chemistry",
            "14 min",
            r"""
# Spectroscopy and computational chemistry

Modern inorganic chemistry is driven by **spectroscopy** and **computation**.
Spectroscopic methods probe structure across the electromagnetic spectrum:

```mermaid
flowchart LR
  EM["electromagnetic probe"] --> UV["UV-Vis: d-d, charge-transfer"]
  EM --> IR["IR/Raman: vibrations, ligand modes"]
  EM --> NMR["NMR: nuclei environment"]
  EM --> EPR["EPR: unpaired electrons"]
  EM --> XAS["X-ray (XAS, XRD): oxidation state, geometry"]
```

The **Beer–Lambert law** $A = \varepsilon\,c\,\ell$ makes UV-Vis quantitative:
absorbance rises linearly with concentration, the basis of analytical assays:

```plot
{"title": "Beer-Lambert law: absorbance vs concentration", "xLabel": "concentration c (mM)", "yLabel": "absorbance A", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.9*x", "label": "A = epsilon c l", "color": "#16a34a"}]}
```

**Computational chemistry** predicts structure, energetics and spectra from first
principles. **Density functional theory (DFT)** solves the electronic structure
approximately, now standard for reaction mechanisms, $\Delta_o$ splittings and
redox potentials. Tools include Gaussian, ORCA, VASP and Quantum ESPRESSO.

**AI/machine learning** has transformed materials discovery: **machine-learning
interatomic potentials** (e.g. graph neural networks such as those behind
GNoME/MACE) approach DFT accuracy at orders-of-magnitude lower cost, enabling
high-throughput screening of catalysts and battery materials. Inverse-design and
generative models propose novel stable compounds, closing the loop with
autonomous, robot-run experimental laboratories.

**Next:** test the research-grade material.
""",
        ),
        _quiz(),
    ),
)


GENERAL_CHEMISTRY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["GENERAL_CHEMISTRY_COURSES"]
