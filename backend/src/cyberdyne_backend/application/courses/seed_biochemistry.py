"""Biochemistry track: Basics -> Intermediate -> Advanced.

A three-level life-sciences track on the chemistry of living systems. It starts
from water, pH/buffers and the four classes of biomolecules; advances through
protein structure, enzyme kinetics, bioenergetics and the core metabolic
pathways; and ends with metabolic integration, regulation, signalling and the
computational/AI methods (AlphaFold, flux balance analysis, molecular dynamics)
used in modern research. Lessons are `text` with LaTeX, interactive ```plot
blocks (kinetics, titration, dose-response) and ```mermaid pathway diagrams.
"""

# Lesson prose uses typographic characters and LaTeX — exempt this content file
# from the ambiguous-character lints.
# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Biochemistry — Basics ────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="biochemistry-basics",
    title="Biochemistry — Basics",
    description=(
        "The molecular foundations of life: why water and its hydrogen-bond "
        "network make biochemistry possible, the pH scale and buffers, and a "
        "tour of the four great classes of biomolecules — carbohydrates, "
        "lipids, nucleic acids and proteins — plus the central dogma that "
        "links genes to enzymes. Interactive titration and binding plots and "
        "pathway diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Water: the matrix of life",
            "10 min",
            r"""
# Water: the matrix of life

Almost every biochemical reaction happens in water, and water is not a passive
backdrop — its structure shapes biology. Each H₂O molecule is **polar**: oxygen
pulls electron density away from the two hydrogens, leaving a partial negative
charge ($\delta^-$) on O and partial positive ($\delta^+$) on each H. Polar
molecules attract one another through **hydrogen bonds**, weak (~20 kJ/mol) but
collectively powerful links between an O–H or N–H donor and an electronegative
acceptor.

This cohesive network gives water its high boiling point, high heat capacity and
its role as a near-universal solvent for ions and polar (**hydrophilic**)
compounds. Nonpolar (**hydrophobic**) molecules cannot hydrogen-bond, so water
orders around them and the system minimises that ordering by clustering them
together — the **hydrophobic effect**. This entropy-driven force folds proteins
and assembles lipid membranes.

```mermaid
flowchart LR
  W["Polar water molecule"] --> HB["Hydrogen-bond network"]
  HB --> SOL["Dissolves ions and polar solutes"]
  HB --> HE["Hydrophobic effect orders nonpolar groups"]
  HE --> FOLD["Drives protein folding and membrane assembly"]
```

The strength of the hydrophobic effect grows with the buried nonpolar surface
area, roughly linearly — bury more greasy surface, gain more stabilisation:

```plot
{"title": "Hydrophobic stabilisation vs buried surface", "xLabel": "buried nonpolar area (nm^2)", "yLabel": "free-energy gain |ΔG| (kJ/mol)", "xRange": [0, 6], "yRange": [0, 30], "grid": true, "functions": [{"expr": "5*x", "label": "ΔG ≈ 5·area", "color": "#2563eb"}]}
```

**Next:** how water's self-ionisation sets the pH scale.
""",
        ),
        _t(
            "pH, pKa and buffers",
            "11 min",
            r"""
# pH, pKa and buffers

Water self-ionises slightly: $2\,\mathrm{H_2O} \rightleftharpoons \mathrm{H_3O^+}
+ \mathrm{OH^-}$, with $K_w = [\mathrm{H^+}][\mathrm{OH^-}] = 10^{-14}$ at 25 °C.
We measure acidity on the logarithmic **pH** scale, $\mathrm{pH} = -\log_{10}
[\mathrm{H^+}]$, so pure water is pH 7 and blood is tightly held near pH 7.4.

A weak acid HA dissociates with constant $K_a$, and its $\mathrm{p}K_a =
-\log_{10} K_a$ is the pH at which it is half-dissociated. The
**Henderson–Hasselbalch** equation links pH to the ratio of conjugate base to
acid:

$$\mathrm{pH} = \mathrm{p}K_a + \log_{10}\frac{[\mathrm{A^-}]}{[\mathrm{HA}]}.$$

A **buffer** resists pH change because both HA and A⁻ are present to neutralise
added acid or base. Buffering is strongest within ±1 pH unit of the pKa, where a
titration curve is flattest. The sigmoidal titration curve below shows the
fraction deprotonated rising through the pKa (here at pH 5):

```plot
{"title": "Titration curve: fraction deprotonated vs pH", "xLabel": "pH", "yLabel": "fraction as A^-", "xRange": [1, 9], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "A^- / total (pKa = 5)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  HA["Weak acid HA"] -->|"loses H+"| A["Conjugate base A-"]
  A -->|"gains H+"| HA
  ADD["Add strong acid/base"] --> BUF["Buffer pair absorbs change → small ΔpH"]
```

Physiological buffers — bicarbonate, phosphate and proteins — keep cellular pH
in the narrow window enzymes require.

**Next:** carbohydrates, the cell's quick energy and recognition molecules.
""",
        ),
        _t(
            "Carbohydrates and glycosidic bonds",
            "10 min",
            r"""
# Carbohydrates and glycosidic bonds

Carbohydrates have the empirical formula $(\mathrm{CH_2O})_n$. The simplest are
**monosaccharides** — glucose, fructose and galactose are all $\mathrm{C_6H_{12}
O_6}$ isomers. In water glucose cyclises into a six-membered pyranose ring,
existing as interconverting $\alpha$ and $\beta$ **anomers** that differ only at
the anomeric carbon.

Two sugars join by a **glycosidic bond**, a condensation that releases water.
Linkage geometry matters enormously: $\alpha(1\!\to\!4)$ links give digestible,
helical **starch** and **glycogen**, while $\beta(1\!\to\!4)$ links give the
straight, hydrogen-bonded chains of **cellulose** that humans cannot digest. The
same monomer, opposite biology.

```mermaid
flowchart LR
  G["Glucose monomers"] -->|"α(1→4)"| ST["Starch / glycogen — energy store"]
  G -->|"β(1→4)"| CE["Cellulose — structural fibre"]
  G -->|"oxidation"| ATP["Catabolism → ATP"]
```

Polysaccharide length lets cells store glucose without raising osmotic pressure,
since one large polymer counts as a single solute particle. The energy released
per gram on full oxidation is roughly constant (~17 kJ/g) across simple
carbohydrates, scaling with mass:

```plot
{"title": "Energy released by carbohydrate oxidation", "xLabel": "mass oxidised (g)", "yLabel": "energy (kJ)", "xRange": [0, 10], "yRange": [0, 180], "grid": true, "functions": [{"expr": "17*x", "label": "≈ 17 kJ/g", "color": "#16a34a"}]}
```

Sugars also decorate proteins and lipids (**glycosylation**), tagging them for
recognition, trafficking and immune identity (the ABO blood groups).

**Next:** lipids and the membranes that compartmentalise the cell.
""",
        ),
        _t(
            "Lipids and membranes",
            "10 min",
            r"""
# Lipids and membranes

**Lipids** are defined by solubility, not structure: they are hydrophobic or
amphipathic molecules that dissolve in organic solvents. **Fatty acids** are
long hydrocarbon tails ending in a carboxyl group; **saturated** chains pack
tightly and are solid (butter), while a *cis* double bond kinks the chain
(**unsaturated**, oils) and lowers the melting point.

The key membrane lipid is the **phospholipid**: a polar phosphate head plus two
fatty-acid tails. Being **amphipathic**, in water phospholipids spontaneously
self-assemble — driven by the hydrophobic effect — into a **bilayer**, the
foundation of every biological membrane.

```mermaid
flowchart LR
  FA["Fatty acids + phosphate head"] --> PL["Amphipathic phospholipid"]
  PL -->|"hydrophobic effect in water"| BL["Lipid bilayer"]
  BL --> MEM["Selectively permeable membrane"]
  MEM --> COMP["Compartments + electrochemical gradients"]
```

The bilayer is a two-dimensional fluid: lipids and proteins diffuse laterally
(the **fluid-mosaic model**), with fluidity tuned by chain saturation and
cholesterol. A membrane is selectively permeable — small nonpolar gases cross
freely while ions need transporters — letting cells maintain the gradients that
power transport and signalling. Passive flux across the membrane follows a
saturating relationship as carrier transporters become occupied:

```plot
{"title": "Carrier-mediated transport rate vs concentration", "xLabel": "external concentration (mM)", "yLabel": "transport rate (a.u.)", "xRange": [0, 12], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturable carrier", "color": "#2563eb"}]}
```

**Next:** nucleic acids and the central dogma of molecular biology.
""",
        ),
        _t(
            "Nucleic acids and the central dogma",
            "11 min",
            r"""
# Nucleic acids and the central dogma

**Nucleotides** are the monomers of nucleic acids: a five-carbon sugar (ribose
in RNA, deoxyribose in DNA), a phosphate, and a nitrogenous base — the purines
**adenine (A)** and **guanine (G)** and the pyrimidines **cytosine (C)**,
**thymine (T)** in DNA, and **uracil (U)** in RNA. Phosphodiester bonds link them
into a directional 5′→3′ backbone.

**DNA** is a right-handed double helix held by complementary base pairing: A–T
(two hydrogen bonds) and G–C (three). The two strands are **antiparallel**, so
one strand's sequence dictates the other's — the chemical basis of faithful
replication.

The **central dogma** describes information flow: DNA is **transcribed** into
messenger RNA, which is **translated** by ribosomes into protein. The genetic
code reads mRNA in non-overlapping triplet **codons**, with 64 codons specifying
20 amino acids plus stop signals (it is redundant, or degenerate).

```mermaid
flowchart LR
  DNA["DNA (genome)"] -->|"replication"| DNA
  DNA -->|"transcription"| RNA["messenger RNA"]
  RNA -->|"translation"| PROT["Protein"]
  PROT --> FUNC["Enzymes & structure"]
```

Because GC pairs have three hydrogen bonds, GC-rich DNA needs a higher
temperature to melt. Melting (denaturation) follows a sharp sigmoidal transition
in absorbance with temperature:

```plot
{"title": "DNA melting curve (fraction of strands separated)", "xLabel": "temperature (°C, shifted)", "yLabel": "fraction denatured", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "denatured fraction", "color": "#dc2626"}]}
```

**Next:** amino acids and how they build proteins.
""",
        ),
        _t(
            "Amino acids and the peptide bond",
            "10 min",
            r"""
# Amino acids and the peptide bond

Proteins are polymers of **amino acids**, of which 20 are genetically encoded.
Each has a central $\alpha$-carbon bonded to an amino group, a carboxyl group, a
hydrogen, and a distinctive **side chain (R group)**. The side chains sort amino
acids into families — nonpolar, polar, acidic and basic — and those chemistries
determine how a protein folds and functions.

At physiological pH amino acids are **zwitterions**: the amino group is
protonated ($\mathrm{-NH_3^+}$) and the carboxyl deprotonated
($\mathrm{-COO^-}$). The pH at which net charge is zero is the **isoelectric
point (pI)**, the basis of separation by isoelectric focusing.

Amino acids link through the **peptide bond**, an amide formed by condensation
between one carboxyl and the next amino group. The peptide bond is **planar and
partially double-bonded** (resonance), restricting backbone rotation to the
$\phi$ and $\psi$ dihedral angles — the degrees of freedom mapped by a
Ramachandran plot.

```mermaid
flowchart LR
  AA1["Amino acid (–COOH)"] -->|"condensation, –H2O"| PB["Peptide bond (planar amide)"]
  AA2["Amino acid (–NH2)"] --> PB
  PB --> POLY["Polypeptide chain"]
  POLY --> FOLD["Folds into functional protein"]
```

Side-chain titration shapes a protein's charge across pH; a single ionisable
group follows the familiar sigmoidal curve around its pKa:

```plot
{"title": "Side-chain ionisation vs pH", "xLabel": "pH", "yLabel": "fraction charged", "xRange": [1, 9], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "fraction ionised", "color": "#16a34a"}]}
```

**Next:** test your grasp of the molecular foundations.
""",
        ),
        _quiz(),
    ),
)


# ── Biochemistry — Intermediate ──────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="biochemistry-intermediate",
    title="Biochemistry — Intermediate",
    description=(
        "The quantitative core of biochemistry: how proteins fold into "
        "functional shapes, how enzymes accelerate reactions and how we measure "
        "them with Michaelis–Menten kinetics and inhibition analysis, the "
        "thermodynamics of ATP and redox coupling, and the central catabolic "
        "pathways — glycolysis, the citric acid cycle and oxidative "
        "phosphorylation. Interactive kinetics and energetics plots throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Protein structure: four levels",
            "11 min",
            r"""
# Protein structure: four levels

A protein's function follows from its three-dimensional shape, organised in four
hierarchical levels. **Primary structure** is the amino-acid sequence — the
covalent order set by the gene. **Secondary structure** is local backbone
folding stabilised by hydrogen bonds: the $\alpha$-helix (3.6 residues per turn)
and the $\beta$-sheet of extended strands. **Tertiary structure** is the full
three-dimensional fold of one chain, driven mainly by the hydrophobic effect
burying nonpolar side chains, with help from disulfide bonds, salt bridges and
hydrogen bonds. **Quaternary structure** is the assembly of multiple subunits,
as in haemoglobin's four chains.

```mermaid
flowchart LR
  P["Primary: sequence"] --> S["Secondary: α-helix / β-sheet"]
  S --> T["Tertiary: 3D fold of one chain"]
  T --> Q["Quaternary: multi-subunit assembly"]
  Q --> FN["Biological function"]
```

Folding is a thermodynamic search for the lowest free-energy state, but the
native fold is only marginally stable (often 20–60 kJ/mol). **Denaturation** by
heat, pH or chaotropes unfolds proteins cooperatively: stability drops sharply
once a melting temperature is passed, giving a sigmoidal unfolding transition:

```plot
{"title": "Two-state protein unfolding vs denaturant", "xLabel": "denaturant (M, shifted)", "yLabel": "fraction unfolded", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "fraction unfolded", "color": "#dc2626"}]}
```

The same sequence-to-structure logic underlies cooperativity, allostery and the
prediction problem that AI now tackles.

**Next:** how enzymes turn structure into catalytic power.
""",
        ),
        _t(
            "Enzymes and catalysis",
            "11 min",
            r"""
# Enzymes and catalysis

**Enzymes** are biological catalysts — mostly proteins, some RNAs (ribozymes) —
that accelerate reactions by factors of $10^6$–$10^{17}$ without being consumed.
They do this by **lowering the activation energy** $E_a$: they stabilise the
high-energy **transition state** more than the substrate, providing a lower
energy path between reactants and products. They do not change the equilibrium,
only the rate at which it is reached.

```mermaid
flowchart LR
  S["Substrate"] -->|"binds active site"| ES["Enzyme–substrate complex"]
  ES -->|"transition state stabilised"| EP["Enzyme–product"]
  EP --> P["Product + free enzyme"]
```

Catalysis exploits **specificity**: the active site is shaped to bind a
particular substrate (**induced fit**, not a rigid lock and key) and positions
catalytic residues, metal ions or coenzymes (NAD⁺, FAD, coenzyme A, vitamins)
precisely. Mechanisms include acid–base catalysis, covalent catalysis and
metal-ion catalysis.

Because $E_a$ sits in the exponent of the Arrhenius law $k = A\,e^{-E_a/RT}$,
lowering it multiplies the rate dramatically. The rate's exponential rise with
temperature (before denaturation) illustrates this sensitivity:

```plot
{"title": "Arrhenius: relative rate vs temperature", "xLabel": "temperature (a.u.)", "yLabel": "relative rate k", "xRange": [0, 10], "yRange": [0, 25], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "k ∝ exp(–Ea/RT)", "color": "#2563eb"}]}
```

**Next:** quantifying enzyme behaviour with Michaelis–Menten kinetics.
""",
        ),
        _t(
            "Michaelis-Menten kinetics",
            "12 min",
            r"""
# Michaelis-Menten kinetics

The standard model of single-substrate enzymes assumes
$\mathrm{E} + \mathrm{S} \rightleftharpoons \mathrm{ES} \to \mathrm{E} +
\mathrm{P}$. Applying the steady-state approximation to [ES] gives the
**Michaelis–Menten equation** relating initial velocity $v_0$ to substrate
concentration $[\mathrm{S}]$:

$$v_0 = \frac{V_{max}\,[\mathrm{S}]}{K_m + [\mathrm{S}]}.$$

Here $V_{max} = k_{cat}[\mathrm{E}]_{\text{total}}$ is the saturating rate and
$K_m$ is the substrate concentration giving half-maximal velocity. A small $K_m$
signals tight substrate binding. The curve is a rectangular hyperbola — linear
at low $[\mathrm{S}]$, saturating at high $[\mathrm{S}]$:

```plot
{"title": "Michaelis–Menten saturation curve", "xLabel": "substrate [S] (mM)", "yLabel": "initial velocity v0", "xRange": [0, 20], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v0 = Vmax[S]/(Km+[S])", "color": "#2563eb"}]}
```

The ratio $k_{cat}/K_m$ is the **specificity constant**, a measure of catalytic
efficiency that is bounded above by the diffusion limit (~$10^8$–$10^9\,
\mathrm{M^{-1}s^{-1}}$). To extract parameters historically one linearised the
data — the **Lineweaver–Burk** double-reciprocal plot $1/v_0$ versus
$1/[\mathrm{S}]$ gives a straight line of slope $K_m/V_{max}$ — though nonlinear
regression is now preferred because the reciprocal distorts error.

```mermaid
flowchart LR
  DATA["v0 vs [S] data"] --> FIT["Nonlinear fit"]
  FIT --> KM["Km (affinity)"]
  FIT --> VM["Vmax → kcat"]
  KM --> EFF["kcat/Km efficiency"]
  VM --> EFF
```

**Next:** how inhibitors reshape these kinetics — the basis of pharmacology.
""",
        ),
        _t(
            "Enzyme inhibition",
            "11 min",
            r"""
# Enzyme inhibition

Most drugs work by **inhibiting enzymes**, and the inhibition mechanism is read
directly from how $K_m$ and $V_{max}$ change.

A **competitive** inhibitor binds the active site and competes with substrate. It
raises the apparent $K_m$ (more substrate needed to reach half-$V_{max}$) but
leaves $V_{max}$ unchanged, because saturating substrate outcompetes the
inhibitor. A **noncompetitive** inhibitor binds elsewhere and lowers $V_{max}$
while $K_m$ is unchanged. An **uncompetitive** inhibitor binds only the ES
complex, lowering both $K_m$ and $V_{max}$.

```mermaid
flowchart LR
  C["Competitive"] --> CK["Km ↑, Vmax —"]
  N["Noncompetitive"] --> NK["Km —, Vmax ↓"]
  U["Uncompetitive"] --> UK["Km ↓, Vmax ↓"]
```

The diagnostic signature appears on the velocity curve. A competitive inhibitor
shifts the hyperbola to the right (larger effective $K_m$) — the same $V_{max}$
is reached, but only at higher substrate. Compare uninhibited (left, $K_m=2$)
with competitively inhibited (right, $K_m=6$):

```plot
{"title": "Competitive inhibition raises apparent Km", "xLabel": "substrate [S] (mM)", "yLabel": "initial velocity v0", "xRange": [0, 20], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "no inhibitor (Km=2)", "color": "#2563eb"}, {"expr": "8*x/(6+x)", "label": "competitive (Km=6)", "color": "#dc2626"}]}
```

**Irreversible** inhibitors (e.g. aspirin acetylating cyclooxygenase) form
covalent bonds and permanently disable the enzyme.

**Next:** the energy currency that all this catalysis serves — ATP and redox.
""",
        ),
        _t(
            "Bioenergetics: ATP and redox",
            "11 min",
            r"""
# Bioenergetics: ATP and redox

Whether a reaction proceeds depends on the **Gibbs free-energy change**: $\Delta
G = \Delta H - T\Delta S$. A reaction is spontaneous (**exergonic**) when
$\Delta G < 0$ and requires input (**endergonic**) when $\Delta G > 0$. Cells run
unfavourable reactions by **coupling** them to favourable ones.

The universal coupling agent is **ATP**. Hydrolysing its terminal phosphoanhydride
bond releases $\Delta G'^{\circ} \approx -30.5\,\mathrm{kJ/mol}$; in the cell,
where the ATP/ADP ratio is far from equilibrium, the actual release is closer to
$-50\,\mathrm{kJ/mol}$. ATP is not long-term storage but a high-turnover currency
— a human regenerates roughly their body mass in ATP each day.

```mermaid
flowchart LR
  CAT["Catabolism (exergonic)"] -->|"ΔG < 0"| ADP["ADP + Pi → ATP"]
  ATP["ATP"] -->|"hydrolysis ΔG < 0"| WORK["Drives endergonic work"]
  WORK --> ADP
```

The other currency is **redox**: electron carriers **NAD⁺/NADH** and **FAD/FADH₂**
shuttle reducing power. A carrier's tendency to accept electrons is its standard
**reduction potential** $E^{\circ\prime}$, and the energy available from
transferring electrons is $\Delta G^{\circ\prime} = -nF\,\Delta E^{\circ\prime}$.
Electrons flow spontaneously from low to high potential, releasing energy that
the cell captures.

```plot
{"title": "Free energy stored vs ATP equivalents made", "xLabel": "ATP synthesised (mol)", "yLabel": "energy captured (kJ)", "xRange": [0, 10], "yRange": [0, 320], "grid": true, "functions": [{"expr": "30.5*x", "label": "≈ 30.5 kJ per ATP", "color": "#16a34a"}]}
```

**Next:** the pathway that begins glucose catabolism — glycolysis.
""",
        ),
        _t(
            "Glycolysis and the citric acid cycle",
            "12 min",
            r"""
# Glycolysis and the citric acid cycle

**Glycolysis** is the universal, oxygen-independent pathway that splits one
glucose into two pyruvate through ten cytosolic steps. An initial **investment
phase** spends 2 ATP to phosphorylate and cleave glucose; the **payoff phase**
then harvests 4 ATP (by substrate-level phosphorylation) and 2 NADH, for a net
gain of **2 ATP and 2 NADH** per glucose. The committed, rate-limiting step is
phosphofructokinase-1, the pathway's key regulatory valve.

Under aerobic conditions pyruvate enters mitochondria, is oxidatively
decarboxylated by **pyruvate dehydrogenase** to acetyl-CoA, and feeds the
**citric acid cycle** (Krebs / TCA cycle). Each acetyl-CoA turn releases 2 CO₂
and stores energy as **3 NADH, 1 FADH₂ and 1 GTP**, regenerating oxaloacetate to
continue.

```mermaid
flowchart LR
  GLU["Glucose"] -->|"glycolysis"| PYR["2 Pyruvate (+2 ATP, +2 NADH)"]
  PYR -->|"PDH"| ACA["Acetyl-CoA + CO2 + NADH"]
  ACA -->|"citric acid cycle"| RED["per turn: 3 NADH, FADH2, GTP, 2 CO2"]
  RED --> ETC["Electron transport chain"]
```

The cycle is amphibolic: its intermediates also feed biosynthesis of amino
acids, haem and other building blocks, so they must be replenished by
**anaplerotic** reactions. The reducing equivalents (NADH, FADH₂) are the real
prize — their energy is cashed in next. The cumulative ATP yield rises with the
glucose processed:

```plot
{"title": "Cumulative ATP yield from glucose (aerobic)", "xLabel": "glucose molecules", "yLabel": "ATP equivalents", "xRange": [0, 10], "yRange": [0, 320], "grid": true, "functions": [{"expr": "30*x", "label": "≈ 30–32 ATP per glucose", "color": "#2563eb"}]}
```

**Next:** test your grasp of structure, kinetics and energetics.
""",
        ),
        _quiz(),
    ),
)


# ── Biochemistry — Advanced ──────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="biochemistry-advanced",
    title="Biochemistry — Advanced",
    description=(
        "Integration, regulation and the computational frontier: oxidative "
        "phosphorylation and the chemiosmotic theory, how the body switches "
        "between fed and fasted states, allosteric and covalent regulation and "
        "signalling cascades, the molecular basis of metabolic disease, and the "
        "AI/computational toolkit — AlphaFold, molecular dynamics and genome-"
        "scale flux balance analysis — now central to research and drug design."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Oxidative phosphorylation and chemiosmosis",
            "12 min",
            r"""
# Oxidative phosphorylation and chemiosmosis

Most cellular ATP is made by **oxidative phosphorylation**, where the NADH and
FADH₂ from catabolism are oxidised and their energy used to phosphorylate ADP.
Electrons pass down the **electron transport chain** (Complexes I–IV) in the
inner mitochondrial membrane, flowing toward oxygen — the terminal acceptor —
which is reduced to water. Because electrons move from low to high reduction
potential, each transfer is exergonic.

The key insight is **Peter Mitchell's chemiosmotic theory**: that released
energy is not used directly but to **pump protons** out of the matrix, creating
an electrochemical gradient — the **proton-motive force (PMF)**. Protons then
flow back through **ATP synthase** (Complex V), a rotary molecular motor whose
turning drives ADP + Pᵢ → ATP.

```mermaid
flowchart LR
  NADH["NADH / FADH2"] -->|"e- through I–IV"| O2["O2 → H2O"]
  NADH -->|"energy pumps H+"| PMF["Proton-motive force across membrane"]
  PMF -->|"H+ back through ATP synthase"| ATP["ATP"]
```

The PMF combines a pH difference and a membrane potential:
$\Delta p = \Delta\psi - \frac{2.3RT}{F}\,\Delta\mathrm{pH}$. Yields are
approximately 2.5 ATP per NADH and 1.5 per FADH₂. **Uncouplers** (e.g.
2,4-dinitrophenol, or thermogenin in brown fat) carry protons across the
membrane, dissipating the gradient as heat. ATP output rises with the proton
gradient but saturates as ATP synthase reaches its maximal rate:

```plot
{"title": "ATP synthesis rate vs proton-motive force", "xLabel": "proton-motive force (a.u.)", "yLabel": "ATP synthesis rate", "xRange": [0, 12], "yRange": [0, 10], "grid": true, "functions": [{"expr": "9*x/(3+x)", "label": "saturating ATP synthase", "color": "#2563eb"}]}
```

**Next:** how the whole body integrates these pathways across feeding and
fasting.
""",
        ),
        _t(
            "Metabolic integration: fed and fasted states",
            "12 min",
            r"""
# Metabolic integration: fed and fasted states

Whole-body metabolism is orchestrated by hormones that switch tissues between
storing and mobilising fuel. After a meal, rising glucose triggers **insulin**
from pancreatic β-cells: it promotes glucose uptake (GLUT4), glycogen synthesis,
lipogenesis and protein synthesis — the **anabolic, fed state**. During fasting,
falling glucose triggers **glucagon** (and adrenaline in stress): glycogen is
broken down (**glycogenolysis**), then glucose is synthesised de novo
(**gluconeogenesis**), and fat is mobilised (**lipolysis**).

```mermaid
flowchart LR
  FED["Fed state (insulin)"] --> STORE["Glycogen + fat synthesis, glucose uptake"]
  FAST["Fasted state (glucagon)"] --> MOB["Glycogenolysis → gluconeogenesis → lipolysis"]
  MOB --> KET["Prolonged fast: ketone bodies fuel brain"]
```

Tissues specialise. Liver buffers blood glucose and is the gluconeogenic and
ketogenic hub; muscle hoards glycogen for its own use; adipose stores
triacylglycerol; the brain normally burns glucose but adapts to **ketone
bodies** during prolonged starvation, sparing muscle protein. Fatty-acid
**β-oxidation** feeds acetyl-CoA into the TCA cycle and yields far more ATP per
carbon than carbohydrate.

As fasting continues, hepatic glycogen depletes within ~24 h and the body
transitions to fat-derived fuels; plasma ketones rise roughly exponentially over
days:

```plot
{"title": "Plasma ketone bodies during fasting", "xLabel": "days of fasting", "yLabel": "ketone concentration (mM)", "xRange": [0, 10], "yRange": [0, 8], "grid": true, "functions": [{"expr": "0.5*exp(0.28*x)", "label": "rising ketogenesis", "color": "#dc2626"}]}
```

**Next:** the regulatory logic — allostery, covalent modification and cascades.
""",
        ),
        _t(
            "Allostery, signalling and regulation",
            "12 min",
            r"""
# Allostery, signalling and regulation

Metabolism is controlled on multiple timescales. The fastest is **allosteric
regulation**: a small effector binds a site distinct from the active site and
shifts the enzyme between low- and high-activity conformations. Allosteric and
multi-subunit enzymes show **cooperative**, sigmoidal kinetics rather than
hyperbolic — haemoglobin's oxygen binding and phosphofructokinase's response to
ATP and AMP are classic examples, well described by the **Hill equation**
$\theta = [\mathrm{L}]^n / (K + [\mathrm{L}]^n)$.

```plot
{"title": "Cooperative (sigmoidal) binding — Hill model", "xLabel": "ligand concentration (a.u.)", "yLabel": "fractional saturation θ", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "Hill coefficient n=2", "color": "#2563eb"}]}
```

A second layer is **covalent modification**, chiefly reversible
**phosphorylation** by kinases (countered by phosphatases), which flips enzyme
activity on or off within seconds. Hormone signals are amplified through
**second-messenger cascades**: a receptor activates a G-protein, which activates
adenylate cyclase to make cyclic AMP, which activates protein kinase A — each
step multiplying the signal so a few hormone molecules mobilise millions of
glucose units.

```mermaid
flowchart LR
  H["Hormone"] --> R["GPCR receptor"]
  R --> G["G-protein → adenylate cyclase"]
  G --> CAMP["cAMP (second messenger)"]
  CAMP --> PKA["Protein kinase A"]
  PKA --> EFF["Phosphorylates target enzymes — amplified response"]
```

Slowest is **transcriptional control**, changing enzyme amounts over hours.
Together these layers tune flux precisely to demand.

**Next:** what happens when this regulation fails — metabolic disease.
""",
        ),
        _t(
            "Molecular basis of metabolic disease",
            "12 min",
            r"""
# Molecular basis of metabolic disease

When regulation breaks, disease follows. In **type 2 diabetes**, tissues become
**insulin-resistant**: the same insulin produces a diminished glucose-uptake
response, so the pancreas compensates with more insulin until β-cells fail and
hyperglycaemia results. Chronic high glucose drives non-enzymatic glycation of
proteins (measured as **HbA1c**) and vascular damage.

```mermaid
flowchart LR
  IR["Insulin resistance"] --> COMP["β-cell hypersecretion compensates"]
  COMP --> FAIL["β-cell exhaustion"]
  FAIL --> HG["Hyperglycaemia → glycation, complications"]
```

Insulin resistance blunts the dose–response: the curve shifts right and its
maximum drops, so much higher insulin is needed for the same effect. Compare a
normal response with a resistant one:

```plot
{"title": "Insulin dose–response: normal vs resistant", "xLabel": "insulin (log dose, shifted)", "yLabel": "glucose uptake (fraction max)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-3)))", "label": "normal", "color": "#2563eb"}, {"expr": "0.6/(1+exp(-(x-6)))", "label": "insulin resistant", "color": "#dc2626"}]}
```

Many diseases are **inborn errors of metabolism** — single-enzyme defects.
Phenylketonuria (loss of phenylalanine hydroxylase) lets phenylalanine
accumulate to neurotoxic levels; Tay–Sachs, Gaucher and the glycogen-storage
diseases follow the same logic of a blocked step backing up substrate.
**Mitochondrial disorders** impair oxidative phosphorylation and strike
energy-hungry tissues hardest. Understanding the broken step pinpoints both
diagnosis and therapy (e.g. dietary phenylalanine restriction in PKU).

**Next:** the computational and AI methods reshaping biochemistry.
""",
        ),
        _t(
            "Structural biology and AlphaFold",
            "12 min",
            r"""
# Structural biology and AlphaFold

Function follows structure, so determining structures is central. The classical
experimental methods are **X-ray crystallography** (diffraction from a crystal,
historically dominant), **nuclear magnetic resonance (NMR)** for smaller
proteins in solution, and **cryo-electron microscopy (cryo-EM)**, whose
resolution revolution now resolves large complexes near-atomically without
crystals.

The long-standing **protein-folding problem** — predicting 3D structure from
sequence alone — was largely solved computationally by **AlphaFold2** (DeepMind,
2021). It is a deep neural network that reads a multiple-sequence alignment,
infers residue co-evolution (correlated mutations imply spatial contact), and a
transformer-based **Evoformer** plus a structure module outputs atomic
coordinates with a per-residue confidence score (**pLDDT**). It reached
experimental accuracy at CASP14 and now covers essentially every known protein
sequence.

```mermaid
flowchart LR
  SEQ["Amino-acid sequence"] --> MSA["Multiple-sequence alignment"]
  MSA --> EVO["Evoformer (co-evolution attention)"]
  EVO --> SM["Structure module"]
  SM --> STR["3D coordinates + pLDDT confidence"]
  STR --> USE["Function, docking, design"]
```

Prediction confidence rises with the depth of the alignment — more homologous
sequences give a richer co-evolution signal, with diminishing returns:

```plot
{"title": "Prediction confidence vs alignment depth", "xLabel": "homologous sequences (log)", "yLabel": "mean pLDDT (a.u.)", "xRange": [0, 12], "yRange": [0, 100], "grid": true, "functions": [{"expr": "95*x/(2+x)", "label": "saturating confidence", "color": "#16a34a"}]}
```

Newer tools (AlphaFold3, RoseTTAFold) extend prediction to complexes and
ligands, and generative models (RFdiffusion, ProteinMPNN) now **design** novel
proteins.

**Next:** simulating and modelling metabolism dynamically.
""",
        ),
        _t(
            "Computational methods: MD and flux analysis",
            "12 min",
            r"""
# Computational methods: MD and flux analysis

Static structures are only the start; biochemistry is dynamic. **Molecular
dynamics (MD)** simulation integrates Newton's equations for every atom under a
**force field** (AMBER, CHARMM, OpenMM) to watch proteins flex, ligands bind and
membranes fluctuate over nanoseconds to microseconds. MD reveals conformational
ensembles invisible to a single crystal structure and, with enhanced-sampling
methods (metadynamics, free-energy perturbation), estimates binding free
energies for **structure-based drug design**.

```mermaid
flowchart LR
  STR["Structure + force field"] --> INT["Integrate Newton's equations"]
  INT --> TRAJ["Trajectory (ns–μs)"]
  TRAJ --> ENS["Conformational ensemble"]
  ENS --> DG["Binding free energy → drug design"]
```

At the systems scale, **constraint-based modelling** treats metabolism as a
network. **Flux balance analysis (FBA)** assumes steady state (no metabolite
accumulates), so the stoichiometric matrix times the flux vector is zero,
$\mathbf{S}\,\mathbf{v} = 0$. Within that null space and reaction bounds, linear
programming finds the flux distribution that maximises an objective such as
biomass growth or ATP yield — predicting genome-scale phenotypes from
stoichiometry alone, without kinetic parameters.

The cost of MD scales steeply with system size (long-range interactions dominate),
roughly with the square of the atom count:

```plot
{"title": "MD compute cost vs system size", "xLabel": "atoms (thousands)", "yLabel": "relative cost", "xRange": [0, 10], "yRange": [0, 100], "grid": true, "functions": [{"expr": "x^2", "label": "≈ O(N^2) interactions", "color": "#dc2626"}]}
```

Coupled with machine learning — ML force fields, generative enzyme design and
omics-trained models — these methods make biochemistry increasingly predictive.

**Next:** test your grasp of integration, regulation and computation.
""",
        ),
        _quiz(),
    ),
)


BIOCHEMISTRY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["BIOCHEMISTRY_COURSES"]
