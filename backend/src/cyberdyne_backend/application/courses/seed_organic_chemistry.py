"""Organic Chemistry track: Basics -> Intermediate -> Advanced.

A three-level chemistry track on the structure and reactivity of carbon
compounds. It moves from hybridization, functional groups and IUPAC
nomenclature, through reaction mechanisms (arrow pushing, substitution and
elimination, addition, carbonyl chemistry) and stereochemistry, to retrosynthetic
strategy, pericyclic and organometallic chemistry, and the chemistry of
biomolecules — with a closing lesson on computational and AI methods. Lessons are
`text` with LaTeX, interactive ```plot blocks (kinetics, energy profiles,
titration, dose response) and ```mermaid diagrams for mechanisms and pathways.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Organic Chemistry — Basics ───────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="organic-chemistry-basics",
    title="Organic Chemistry — Basics",
    description=(
        "The foundations of carbon chemistry: why carbon catenates, atomic and "
        "molecular orbitals and hybridization, drawing structures and "
        "resonance, the major functional groups, IUPAC nomenclature, and the "
        "intermolecular forces that set boiling points and solubility. "
        "Interactive plots and structure/classification diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Carbon, bonding and hybridization",
            "12 min",
            r"""
# Carbon, bonding and hybridization

Organic chemistry is the chemistry of carbon. Carbon's ground-state
configuration is $1s^2\,2s^2\,2p^2$, giving it four valence electrons and an
electronegativity ($\chi \approx 2.55$) midway in the periodic table, so it forms
strong **covalent** bonds and chains of almost unlimited length (*catenation*).

To explain molecular shape we mix atomic orbitals into equivalent **hybrid**
orbitals:

- **sp³** — four hybrids, tetrahedral, $\approx 109.5^\circ$ (methane, alkanes).
- **sp²** — three hybrids in a plane, $\approx 120^\circ$, with an unhybridized
  $p$ orbital forming a $\pi$ bond (ethene, carbonyls, aromatics).
- **sp** — two hybrids, linear, $180^\circ$, with two $\pi$ bonds (alkynes,
  nitriles).

A single bond is one head-on **$\sigma$** overlap; a double bond is one $\sigma$
plus one side-on **$\pi$**; a triple bond is one $\sigma$ plus two $\pi$. More $s$
character pulls electrons closer to the nucleus, so bonds shorten and strengthen
from sp³ to sp:

```plot
{"title": "Bond strength rises with s-character", "xLabel": "% s-character", "yLabel": "relative C-H bond energy", "xRange": [20, 55], "yRange": [0.9, 1.2], "grid": true, "functions": [{"expr": "0.9 + 0.006*x", "label": "trend", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  C["Carbon 2s,2p"] --> SP3["sp3 tetrahedral 109.5°"]
  C --> SP2["sp2 trigonal 120° + 1 pi"]
  C --> SP["sp linear 180° + 2 pi"]
```

**Next:** turning these atoms into pictures — Lewis structures and resonance.
""",
        ),
        _t(
            "Lewis structures, formal charge and resonance",
            "12 min",
            r"""
# Lewis structures, formal charge and resonance

A **Lewis structure** tracks valence electrons as bonds (shared pairs) and lone
pairs. Build one by counting valence electrons, connecting atoms, completing
octets, and assigning the **formal charge** of each atom:

$$\text{FC} = (\text{valence } e^-) - (\text{nonbonding } e^-) - \tfrac{1}{2}(\text{bonding } e^-).$$

The best structure minimizes formal charges and places any negative charge on
the most electronegative atom.

When one Lewis structure cannot capture the bonding, the real molecule is a
**resonance hybrid** — a weighted average of contributing structures that differ
only in electron placement. Curved arrows move electron *pairs*, never atoms. The
carboxylate ion is the classic case: its two C–O bonds are identical because the
negative charge is delocalized over both oxygens. Delocalization lowers energy,
so the more (and more equivalent) the resonance contributors, the more stable the
species:

```plot
{"title": "Delocalization stabilizes: energy drops with contributors", "xLabel": "equivalent resonance contributors", "yLabel": "relative energy", "xRange": [1, 5], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*(x-1))", "label": "stabilization", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  A["Carboxylate: C=O / C-O(-)"] -->|"push pi + lone pair"| B["C-O(-) / C=O"]
  A --> H["Hybrid: two equal C–O bonds, charge shared"]
  B --> H
```

**Next:** the language of functional groups.
""",
        ),
        _t(
            "Functional groups",
            "13 min",
            r"""
# Functional groups

A **functional group** is a specific atom or arrangement that dominates a
molecule's reactivity. Recognizing them lets you predict behaviour without
memorizing every compound. The major families, roughly by oxidation level of
carbon:

- **Hydrocarbons:** alkanes (C–C), alkenes (C=C), alkynes (C≡C), arenes (benzene
  ring).
- **Single-bond heteroatoms:** alcohols (–OH), ethers (C–O–C), amines (C–N),
  halides (C–X).
- **Carbonyl (C=O) family:** aldehydes (–CHO), ketones (C=O), and the
  *carboxylic acid derivatives* — carboxylic acids (–COOH), esters (–COOR),
  amides (–CONR₂), acyl halides, anhydrides, plus nitriles (C≡N).

Within the acyl family, reactivity toward nucleophilic acyl substitution falls
as the leaving group gets worse: acyl halide > anhydride > ester ≈ acid > amide.
A clean indicator is the carbonyl C=O stretch in the infrared spectrum, which
shifts with the attached group:

```plot
{"title": "Carbonyl C=O IR stretch by group", "xLabel": "group index (amide→acyl halide)", "yLabel": "wavenumber (cm^-1)", "xRange": [1, 5], "yRange": [1620, 1830], "grid": true, "functions": [{"expr": "1640 + 38*x", "label": "C=O stretch", "color": "#dc2626"}]}
```

```mermaid
flowchart TB
  FG["Functional groups"] --> HC["Hydrocarbons: alkane/ene/yne/arene"]
  FG --> SB["Single bond: -OH, -O-, -N, -X"]
  FG --> CO["Carbonyl: aldehyde/ketone/acid/ester/amide/nitrile"]
```

**Next:** naming compounds systematically with IUPAC rules.
""",
        ),
        _t(
            "IUPAC nomenclature",
            "13 min",
            r"""
# IUPAC nomenclature

A systematic name is a recipe for the structure. The IUPAC algorithm:

1. **Find the principal chain** — the longest carbon chain that contains the
   highest-priority functional group (the *principal characteristic group*,
   which becomes the suffix).
2. **Number** to give the lowest locants to that group, then to multiple bonds,
   then to substituents.
3. **Name and locate substituents** as prefixes, in alphabetical order
   (di-, tri- do not count for alphabetizing).
4. **Assemble:** locants-prefixes-parent-unsaturation-suffix, e.g.
   *4-methylpent-3-en-2-ol*.

Priority of the suffix group, high to low: carboxylic acid > ester > amide >
nitrile > aldehyde > ketone > alcohol > amine > alkene/alkyne. Everything below
the chosen principal group is cited as a prefix (e.g. hydroxy-, oxo-, amino-).

Stems encode chain length: meth- (1), eth- (2), prop- (3), but- (4), pent- (5),
hex- (6), and so on. Because the parent stem grows linearly with carbon count,
naming is fully algorithmic:

```plot
{"title": "Parent stem index vs carbon count", "xLabel": "carbons in principal chain", "yLabel": "stem index", "xRange": [1, 10], "yRange": [0, 11], "grid": true, "functions": [{"expr": "x", "label": "meth..dec", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  S["Structure"] --> P["1. Principal chain + top group"]
  P --> N["2. Number for lowest locants"]
  N --> SUB["3. Substituent prefixes A→Z"]
  SUB --> NAME["4. Assemble IUPAC name"]
```

**Next:** how shape and forces between molecules set physical properties.
""",
        ),
        _t(
            "Isomers and intermolecular forces",
            "12 min",
            r"""
# Isomers and intermolecular forces

**Isomers** share a molecular formula but differ in structure. *Constitutional*
(structural) isomers differ in connectivity — butane vs isobutane both are
C₄H₁₀. *Stereoisomers* share connectivity but differ in spatial arrangement
(covered in depth in the Intermediate course). The number of constitutional
isomers explodes with carbon count, which is why nomenclature matters.

Physical properties are governed by **intermolecular forces (IMFs)**, in order of
typical strength:

- **London dispersion** — induced-dipole, present in all molecules; grows with
  surface area and polarizability (so boiling point rises with chain length).
- **Dipole–dipole** — between permanent dipoles (e.g. ketones, halides).
- **Hydrogen bonding** — a strong dipole interaction when H is bonded to N, O or
  F; it makes alcohols and acids boil far higher than alkanes of similar mass.

Boiling point climbs roughly linearly with the number of carbons in a homologous
series, as dispersion forces accumulate:

```plot
{"title": "Boiling point of n-alkanes vs chain length", "xLabel": "number of carbons", "yLabel": "boiling point (°C)", "xRange": [1, 10], "yRange": [-180, 180], "grid": true, "functions": [{"expr": "-180 + 35*x", "label": "n-alkane trend", "color": "#dc2626"}]}
```

```mermaid
flowchart TB
  IMF["Intermolecular forces"] --> D["London dispersion (all; grows with size)"]
  IMF --> DD["Dipole-dipole (polar groups)"]
  IMF --> HB["Hydrogen bonding (N/O/F-H): highest bp & solubility"]
```

**Next:** check your understanding of structure and bonding.
""",
        ),
        _quiz(),
    ),
)


# ── Organic Chemistry — Intermediate ─────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="organic-chemistry-intermediate",
    title="Organic Chemistry — Intermediate",
    description=(
        "The quantitative core of reactivity: acid–base chemistry and pKa, "
        "arrow-pushing and reaction-energy diagrams, nucleophilic substitution "
        "and elimination (SN1/SN2/E1/E2) with their kinetics, addition to "
        "alkenes and Markovnikov selectivity, carbonyl and aromatic "
        "(electrophilic substitution) chemistry, and a full treatment of "
        "stereochemistry. Kinetics plots, energy profiles and mechanism diagrams "
        "throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Acids, bases and pKa",
            "13 min",
            r"""
# Acids, bases and pKa

Most organic reactions are, at heart, electrons flowing from a base/nucleophile
to an acid/electrophile. The **Brønsted–Lowry** view (proton donor/acceptor) is
quantified by the acid dissociation constant $K_a$ and its log scale
$\mathrm{p}K_a = -\log_{10} K_a$. A *lower* pKa means a *stronger* acid. For a
reaction $\mathrm{HA} + \mathrm{B}^- \rightleftharpoons \mathrm{A}^- + \mathrm{HB}$,
equilibrium favours formation of the **weaker** acid (higher pKa).

Acidity reflects the stability of the conjugate base $\mathrm{A}^-$. Stabilizing
factors: electronegative atom bearing the charge, larger atom (size), resonance
delocalization, and electron-withdrawing inductive groups. Carboxylic acids
(pKa ≈ 4–5) are far more acidic than alcohols (pKa ≈ 16) because the carboxylate
is resonance-stabilized.

The fraction of a weak acid that is deprotonated follows the
**Henderson–Hasselbalch** relationship; plotting it against pH gives the familiar
sigmoidal titration curve centred on the pKa:

```plot
{"title": "Fraction deprotonated vs pH (pKa = 5)", "xLabel": "pH", "yLabel": "fraction A- (deprotonated)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "[A-]/[HA]+[A-]", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  HA["HA (acid)"] -->|"lose H+"| A["A- (conjugate base)"]
  A -->|"stabilized by: EN, size, resonance, induction"| S["lower pKa = stronger acid"]
```

**Next:** representing electron flow with curved arrows.
""",
        ),
        _t(
            "Reaction mechanisms and arrow pushing",
            "13 min",
            r"""
# Reaction mechanisms and arrow pushing

A **mechanism** is the step-by-step account of bond making and breaking. The
universal grammar is the **curved arrow**: a full-headed arrow moves an electron
*pair* from a source of high electron density (lone pair or bond) to an electron
sink. Nucleophiles (Nu, electron-rich) attack electrophiles (E⁺, electron-poor).

Bonds break **heterolytically** (both electrons to one atom → ions) or
**homolytically** (one electron each → radicals, shown with single-barbed
arrows). Reactive intermediates include carbocations (stabilized by
hyperconjugation/resonance: 3° > 2° > 1°), carbanions, and radicals.

Energy diagrams summarize the path. A **transition state** sits at each energy
maximum; an **intermediate** sits in a local minimum. The activation energy
$E_a$ controls rate via Arrhenius, $k = A\,e^{-E_a/RT}$, so rate falls steeply as
$E_a$ rises:

```plot
{"title": "Arrhenius: rate constant vs activation energy", "xLabel": "Ea (relative)", "yLabel": "relative rate k", "xRange": [0, 8], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "k ∝ exp(-Ea/RT)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  R["Reactants"] --> TS1["Transition state 1"]
  TS1 --> I["Intermediate (carbocation)"]
  I --> TS2["Transition state 2"]
  TS2 --> P["Products"]
```

**Next:** the substitution/elimination battleground.
""",
        ),
        _t(
            "Substitution and elimination (SN1, SN2, E1, E2)",
            "14 min",
            r"""
# Substitution and elimination (SN1, SN2, E1, E2)

At an sp³ carbon bearing a leaving group, a nucleophile/base has four competing
pathways:

- **SN2** — one concerted step, backside attack, **inversion** of configuration;
  rate $= k[\text{substrate}][\text{Nu}]$ (second order). Favoured by methyl/1°
  substrates and strong, unhindered nucleophiles in polar aprotic solvents.
- **SN1** — two steps via a carbocation; rate $= k[\text{substrate}]$ (first
  order), racemization. Favoured by 3° substrates, weak nucleophiles, polar
  protic solvents.
- **E2** — concerted anti-periplanar elimination, second order; favoured by
  strong bulky bases. Gives the more substituted (**Zaitsev**) alkene unless a
  bulky base steers to the **Hofmann** product.
- **E1** — stepwise via the same carbocation as SN1.

The trade-off is dramatic: SN2 rate collapses with steric bulk, while SN1 rate
climbs with carbocation stability. Sketching relative SN2 rate against
substitution makes the steric penalty obvious:

```plot
{"title": "Relative SN2 rate falls with substrate substitution", "xLabel": "degree of substitution (methyl→3°)", "yLabel": "relative SN2 rate", "xRange": [0, 4], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-1.4*x)", "label": "SN2 rate", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  S["R-LG + Nu/Base"] --> SN2["SN2: 1°, strong Nu, aprotic — inversion"]
  S --> SN1["SN1: 3°, weak Nu, protic — racemization"]
  S --> E2["E2: strong bulky base — Zaitsev/Hofmann"]
  S --> E1["E1: 3°, heat — via carbocation"]
```

**Next:** building C–C and C–X bonds by adding across pi bonds.
""",
        ),
        _t(
            "Addition reactions of alkenes",
            "12 min",
            r"""
# Addition reactions of alkenes

The electron-rich $\pi$ bond of an alkene is a nucleophile that adds
electrophiles. In **electrophilic addition** (e.g. HX, H₂O/H⁺), the
electrophile adds first to give the *more stable carbocation*, so the nucleophile
ends up on the more substituted carbon — **Markovnikov's rule** ("the rich get
richer," H goes to the carbon with more H's).

Key additions:

- **Hydrohalogenation (HX):** Markovnikov; with peroxides, HBr adds
  *anti*-Markovnikov by a radical chain.
- **Acid-catalysed hydration / oxymercuration:** Markovnikov –OH, no
  rearrangement for oxymercuration.
- **Hydroboration–oxidation (BH₃ then H₂O₂/OH⁻):** *anti*-Markovnikov, *syn*
  addition.
- **Halogenation (Br₂):** *anti* addition via a bromonium ion.

Regioselectivity is set by carbocation stability, which rises with substitution
(hyperconjugation and induction). The Markovnikov preference for the more
substituted cation can be read straight off a stability curve:

```plot
{"title": "Carbocation stability vs substitution drives Markovnikov", "xLabel": "alkyl substituents on C+", "yLabel": "relative cation stability", "xRange": [0, 3], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "x/(x+0.5)", "label": "stability", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  AL["Alkene (pi nucleophile)"] -->|"E+ adds"| CC["More stable carbocation"]
  CC -->|"Nu- traps"| MK["Markovnikov product"]
  AL -->|"BH3 / radical HBr"| AM["anti-Markovnikov product"]
```

**Next:** the carbonyl group and aromatic reactivity.
""",
        ),
        _t(
            "Carbonyl and aromatic chemistry",
            "14 min",
            r"""
# Carbonyl and aromatic chemistry

The **carbonyl** (C=O) is polarized $\delta^+$ at carbon, $\delta^-$ at oxygen,
making the carbon electrophilic. Two master patterns:

- **Nucleophilic addition** (aldehydes/ketones): Nu attacks C, O picks up the
  electrons. Gives alcohols (with hydride/Grignard), hemiacetals/acetals (with
  alcohols), imines (with amines).
- **Nucleophilic acyl substitution** (acid derivatives): addition then expulsion
  of a leaving group, interconverting acyl halides → anhydrides → esters →
  amides (downhill only). The **α-carbon** is also acidic (enol/enolate
  chemistry: aldol, Claisen).

**Aromatic** rings satisfy **Hückel's rule** — planar, cyclic, fully conjugated,
with $4n+2$ $\pi$ electrons (benzene: 6). They react not by addition but by
**electrophilic aromatic substitution (EAS)**, preserving aromaticity.
Substituents already on the ring direct the incoming electrophile: activating
o/p-directors (–OH, –NH₂, alkyl) speed it up; deactivating m-directors (–NO₂,
–C=O) slow it. Reaction rate tracks the substituent's electron donation:

```plot
{"title": "EAS rate vs ring electron density (donor→acceptor)", "xLabel": "substituent donating power", "yLabel": "relative EAS rate", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "EAS rate", "color": "#dc2626"}]}
```

```mermaid
flowchart TB
  CO["Carbonyl C=O"] --> ADD["Aldehyde/ketone: nucleophilic addition"]
  CO --> ACYL["Acid derivative: acyl substitution"]
  AR["Aromatic ring (4n+2 pi)"] --> EAS["Electrophilic aromatic substitution"]
  EAS --> DIR["o/p-director activates; m-director deactivates"]
```

**Next:** the three-dimensional world — stereochemistry.
""",
        ),
        _t(
            "Stereochemistry: chirality and configuration",
            "13 min",
            r"""
# Stereochemistry: chirality and configuration

Molecules are 3D, and shape controls biology. A carbon with four different groups
is a **stereocenter**; a molecule non-superimposable on its mirror image is
**chiral**. The mirror-image pair are **enantiomers** — identical in ordinary
properties but opposite in optical rotation and often in biological activity (one
thalidomide enantiomer is sedative, the other teratogenic).

Configuration is named with **R/S** by the Cahn–Ingold–Prelog (CIP) priority
rules: rank the four groups by atomic number, view with the lowest priority away,
and read 1→2→3 clockwise (**R**) or counterclockwise (**S**).

Other relationships:

- **Diastereomers** — stereoisomers that are *not* mirror images (e.g. cis/trans,
  or molecules differing at one of several stereocenters); they have different
  physical properties.
- **Meso** compounds — have stereocenters but an internal mirror plane, so they
  are achiral overall.

A pure enantiomer rotates plane-polarized light by an amount proportional to
**enantiomeric excess**; a racemate (50:50) is optically inactive. Observed
rotation scales linearly with ee:

```plot
{"title": "Observed optical rotation vs enantiomeric excess", "xLabel": "enantiomeric excess (%)", "yLabel": "observed rotation (relative)", "xRange": [0, 100], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "x/100", "label": "rotation ∝ ee", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  SC["Stereocenter: 4 different groups"] --> CH["Chiral molecule"]
  CH --> EN["Enantiomers (mirror images, R vs S)"]
  CH --> DI["Diastereomers (not mirror images)"]
  CH --> ME["Meso: stereocenters but internal mirror → achiral"]
```

**Next:** check your understanding of mechanisms and stereochemistry.
""",
        ),
        _quiz(),
    ),
)


# ── Organic Chemistry — Advanced ─────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="organic-chemistry-advanced",
    title="Organic Chemistry — Advanced",
    description=(
        "Strategy and frontier methods: retrosynthetic analysis and protecting "
        "groups, modern C–C bond formation by organometallic catalysis "
        "(cross-coupling, metathesis), pericyclic reactions through frontier "
        "molecular orbital theory, the chemistry of biomolecules (amino acids, "
        "carbohydrates, nucleic acids and enzyme catalysis), spectroscopic "
        "structure determination, and computational/AI methods for prediction and "
        "design. Energy profiles, kinetics and pathway diagrams throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Retrosynthetic analysis and protecting groups",
            "14 min",
            r"""
# Retrosynthetic analysis and protecting groups

Designing a synthesis means working **backward** from the target. E. J. Corey's
**retrosynthetic analysis** breaks a molecule at strategic bonds with the open
arrow ⇒ (a *disconnection*), revealing simpler **synthons** (idealized
fragments) that correspond to real **synthetic equivalents** (reagents). A good
disconnection cuts near functional groups, maximizes convergence, and exploits
known reliable reactions.

Two complementary ideas:

- **Polarity (umpolung):** a carbonyl carbon is naturally electrophilic
  ($a^1$); reversing its polarity (e.g. with a dithiane) gives an acyl anion
  equivalent ($d^1$) for new disconnections.
- **Protecting groups:** when a reagent would attack the wrong functional group,
  mask it temporarily (e.g. acetals for ketones, silyl ethers like TBS for
  alcohols, Boc/Fmoc for amines), do the chemistry, then deprotect.

Synthesis efficiency favours **convergent** routes: assembling fragments in
parallel and joining them late gives far higher overall yield than a long linear
sequence, because yield multiplies per step ($Y_{\text{overall}} = y^n$):

```plot
{"title": "Overall yield decays with step count (per-step y = 0.8)", "xLabel": "number of linear steps", "yLabel": "overall yield (fraction)", "xRange": [1, 12], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "0.8^x", "label": "0.8^n", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  T["Target molecule"] -->|"disconnect (⇒)"| S["Synthons"]
  S --> E["Synthetic equivalents (reagents)"]
  E --> PG["Protect → react → deprotect"]
  PG --> R["Forward synthesis"]
```

**Next:** the catalytic toolbox that makes those disconnections real.
""",
        ),
        _t(
            "Organometallic catalysis and cross-coupling",
            "14 min",
            r"""
# Organometallic catalysis and cross-coupling

Transition-metal catalysis transformed how C–C and C–heteroatom bonds are made.
The **palladium cross-couplings** — Suzuki–Miyaura (boronic acids), Negishi
(organozincs), Stille (stannanes), Heck (alkenes), Sonogashira (alkynes) and
Buchwald–Hartwig (C–N) — earned the 2010 Nobel Prize and dominate
pharmaceutical synthesis.

Their shared catalytic cycle is:

1. **Oxidative addition** of an aryl/vinyl halide to Pd(0) → Pd(II).
2. **Transmetalation** transferring the organic group from the partner (e.g.
   boronate) to Pd.
3. **Reductive elimination** forming the new C–C bond and regenerating Pd(0).

Other pillars: **olefin metathesis** (Grubbs/Schrock catalysts) reshuffles C=C
bonds for ring closure and cross metathesis; **asymmetric hydrogenation** (Knowles,
Noyori) sets stereocenters catalytically.

A catalyst lowers $E_a$ without being consumed, so it raises rate enormously and
lets one metal centre turn over many times (high TON). The Arrhenius gap between
catalysed and uncatalysed paths is the whole game:

```plot
{"title": "Catalysis lowers Ea — rate enhancement", "xLabel": "Ea reduction (relative)", "yLabel": "rate enhancement factor", "xRange": [0, 8], "yRange": [0, 60], "grid": true, "functions": [{"expr": "exp(0.5*x)", "label": "exp(ΔEa/RT)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  Pd0["Pd(0)"] -->|"oxidative addition Ar-X"| PdII["Ar-Pd(II)-X"]
  PdII -->|"transmetalation R-[B]"| PdR["Ar-Pd(II)-R"]
  PdR -->|"reductive elimination"| Prod["Ar-R + Pd(0)"]
  Prod --> Pd0
```

**Next:** reactions with no intermediates at all — pericyclic chemistry.
""",
        ),
        _t(
            "Pericyclic reactions and frontier orbitals",
            "13 min",
            r"""
# Pericyclic reactions and frontier orbitals

**Pericyclic** reactions proceed through a single cyclic, concerted transition
state with no intermediates: **cycloadditions** (the Diels–Alder [4+2]),
**electrocyclizations**, and **sigmatropic rearrangements** (Cope, Claisen).
Their stereochemistry is governed by orbital symmetry — the
**Woodward–Hoffmann rules** — best understood through **frontier molecular
orbital (FMO)** theory.

The key interaction is between the **HOMO** of one component and the **LUMO** of
the other; bonding requires their lobes to overlap with matching phase. For the
Diels–Alder, the diene's HOMO and the dienophile's LUMO combine suprafacially on
both partners — thermally allowed for $4n+2$ electrons. Photochemical excitation
promotes an electron, swapping HOMO/LUMO symmetry and reversing the selection
rules ($4n$ allowed thermally / forbidden photochemically and vice versa).

Reactivity rises as the HOMO–LUMO energy gap shrinks: electron-poor dienophiles
(lower LUMO) react faster with electron-rich dienes. Rate scales inversely with
that gap:

```plot
{"title": "Diels-Alder rate vs HOMO-LUMO gap", "xLabel": "HOMO-LUMO energy gap (relative)", "yLabel": "relative rate", "xRange": [1, 8], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/x", "label": "rate ∝ 1/ΔE", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  D["Diene HOMO"] -->|"phase-matched overlap"| TS["Cyclic transition state"]
  P["Dienophile LUMO"] --> TS
  TS --> C["Cyclohexene ([4+2])"]
```

**Next:** the molecules of life.
""",
        ),
        _t(
            "Chemistry of biomolecules",
            "14 min",
            r"""
# Chemistry of biomolecules

Life runs on organic chemistry. The four classes:

- **Amino acids & proteins:** 20 α-amino acids, each chiral (L) and amphoteric
  (the **zwitterion** at physiological pH). Their side-chain pKa values set the
  net charge; the **isoelectric point** pI is where net charge is zero. Peptide
  (amide) bonds link them; folding is driven by H-bonds and the hydrophobic
  effect.
- **Carbohydrates:** polyhydroxy aldehydes/ketones that cyclize to hemiacetals,
  creating the **anomeric** center (α/β); glycosidic bonds build di- and
  polysaccharides (starch, cellulose).
- **Nucleic acids:** nucleotides (base + sugar + phosphate) whose
  complementary base pairing (A–T, G–C) encodes information.
- **Lipids:** fatty acids and membrane phospholipids.

Enzymes are protein catalysts. Most obey **Michaelis–Menten** kinetics: the
initial rate rises with substrate then saturates as active sites fill, defined by
$V_{max}$ and the Michaelis constant $K_m$ (the [S] giving half $V_{max}$):

$$v = \frac{V_{max}\,[S]}{K_m + [S]}.$$

```plot
{"title": "Michaelis-Menten enzyme kinetics", "xLabel": "[S] (substrate)", "yLabel": "initial rate v", "xRange": [0, 20], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  BIO["Biomolecules"] --> AA["Amino acids → proteins (zwitterion, pI)"]
  BIO --> CB["Carbohydrates (anomeric C, glycosidic bond)"]
  BIO --> NA["Nucleic acids (base pairing A-T, G-C)"]
  BIO --> LP["Lipids (membranes)"]
```

**Next:** how we determine structure and design molecules computationally.
""",
        ),
        _t(
            "Spectroscopy and structure determination",
            "13 min",
            r"""
# Spectroscopy and structure determination

You rarely *see* a molecule; you infer it from how it interacts with radiation.
The four workhorses:

- **NMR (nuclear magnetic resonance):** the most powerful. ¹H and ¹³C nuclei
  resonate at frequencies (chemical shifts, in ppm) set by their electronic
  environment; **integration** counts protons, **multiplicity** (n+1 rule)
  reveals neighbours, and 2D methods (COSY, HSQC, HMBC) map connectivity.
- **Infrared (IR):** vibrational frequencies fingerprint functional groups — a
  sharp O–H near 3300, a strong C=O near 1700 cm⁻¹.
- **Mass spectrometry (MS):** the molecular ion gives the mass; high-resolution
  MS gives the molecular formula, and fragmentation patterns map the skeleton.
- **UV–Vis:** electronic transitions probe conjugation.

NMR chemical shift increases with deshielding (nearby electronegative atoms);
more conjugation in UV–Vis shifts absorption to longer wavelength
(bathochromic). Absorbance itself follows the **Beer–Lambert law**, linear in
concentration, $A = \varepsilon\,\ell\,c$:

```plot
{"title": "Beer-Lambert law: absorbance vs concentration", "xLabel": "concentration c (relative)", "yLabel": "absorbance A", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "0.1*x", "label": "A = εℓc", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  X["Unknown compound"] --> MS["MS: mass + formula"]
  X --> IR["IR: functional groups"]
  X --> NMR["NMR: connectivity (1D + 2D)"]
  MS --> STR["Assembled structure"]
  IR --> STR
  NMR --> STR
```

**Next:** computation and machine learning in modern organic chemistry.
""",
        ),
        _t(
            "Computational and AI methods in organic chemistry",
            "14 min",
            r"""
# Computational and AI methods in organic chemistry

Modern organic chemistry is increasingly *in silico*. Three layers:

- **Quantum chemistry:** **Density Functional Theory (DFT)**, e.g. the B3LYP
  and ωB97X-D functionals, predicts geometries, transition-state energies and
  spectra; locating a TS and confirming a single imaginary frequency lets you
  compute $E_a$ and rationalize selectivity before touching a flask.
- **Cheminformatics:** molecules are encoded as **SMILES** strings or
  fingerprints; tools like RDKit compute descriptors and enable similarity
  search across millions of structures.
- **Machine learning & AI:** **graph neural networks** (e.g. Chemprop, message-
  passing networks) predict properties and reactivity directly from molecular
  graphs; transformer models (RXNMapper, IBM RXN, the Molecular Transformer)
  predict products and do **computer-aided retrosynthesis**; generative and
  diffusion models design novel molecules; and AlphaFold-class models predict the
  protein structures that drugs must bind.

ML accuracy improves predictably with training-set size — error decays as a
power law, the empirical "scaling law" that justifies building large reaction
datasets:

```plot
{"title": "ML prediction error vs training-set size", "xLabel": "training examples (relative)", "yLabel": "prediction error (relative)", "xRange": [1, 20], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "error ∝ 1/sqrt(N)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  M["Molecule (SMILES / graph)"] --> DFT["DFT: energies, TS, spectra"]
  M --> GNN["GNN: property & reactivity prediction"]
  M --> RXN["Transformer: forward & retrosynthesis"]
  RXN --> PLAN["AI synthesis planning"]
  GNN --> PLAN
```

**Next:** check your understanding of strategy, catalysis and modern methods.
""",
        ),
        _quiz(),
    ),
)


ORGANIC_CHEMISTRY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ORGANIC_CHEMISTRY_COURSES"]
