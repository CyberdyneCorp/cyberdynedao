"""Academy seed content - Environmental Chemistry.

The chemistry of the natural environment across its three compartments -
water, air, and soil - and how contaminants move and transform between
them. It covers aquatic chemistry (the carbonate system, alkalinity,
dissolved oxygen and redox), chemical equilibria and solubility, sorption
and partitioning, atmospheric photochemistry (ozone and acid rain), soil
and sediment chemistry, the fate and transport of pollutants, and the
emerging contaminants (PFAS, microplastics, pharmaceuticals) now
reshaping the field. Every lesson is a direct explanation with a mermaid
diagram and a worked formula or calculation, followed by a checkpoint
quiz; the course closes with a comprehensive final quiz.
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


_ENVIRONMENTAL_CHEMISTRY = SeedCourse(
    slug="environmental-chemistry",
    title="Environmental Chemistry",
    description=(
        "The chemistry of the environment - aquatic, atmospheric and soil "
        "chemistry and the fate and transport of contaminants, including "
        "emerging pollutants. Every lesson pairs a direct explanation with a "
        "mermaid diagram and a worked formula (carbonate equilibria, "
        "Streeter-Phelps, partition coefficients, Gaussian plumes) grounded "
        "in real standards from WHO, US EPA, CONAMA and ISO."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Environmental Chemistry

The environment is one giant, slow chemical reactor. Rain dissolves
carbon dioxide and weathers rock; rivers carry the products to the sea;
oxygen and sunlight drive reactions in water and air; soils sorb and
release metals and organics. **Environmental chemistry** is the study of
these reactions - and of the contaminants we add to them: where they go,
how they transform, and how long they last.

This course is organised around the three environmental compartments -
**water, air, and soil** - plus the theme that ties them together: the
**fate and transport** of pollutants as they move between phases.

The approach is **concrete**: every lesson explains one idea directly,
draws it as a diagram, and works through a real formula or calculation
(an equilibrium, a mass balance, a partition coefficient, a dispersion
estimate). After each lesson there is a short quiz; a final quiz covers
the whole course.

What you will build understanding for, in order:

1. **Aquatic chemistry and the carbonate system** - pH and alkalinity
2. **Dissolved oxygen and redox reactions** - the health of water
3. **Chemical equilibria and solubility** - what dissolves and what does not
4. **Sorption and partitioning** - how compounds split between phases
5. **Atmospheric chemistry** - photochemistry, ozone, and acid rain
6. **Soil and sediment chemistry** - the reactive solid surfaces
7. **Fate and transport of contaminants** - advection, dispersion, decay
8. **Emerging pollutants** - PFAS, microplastics, pharmaceuticals

Throughout we anchor the chemistry to real standards and models - WHO and
US EPA drinking-water limits, Brazil's CONAMA resolutions, ABNT NBR, and
tools such as QUAL2K, AERMOD and MODFLOW - while keeping every idea
teachable from first principles.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "How is this course organised?",
                    (
                        opt("Around programming languages"),
                        opt(
                            "Around the three environmental compartments (water, air, "
                            "soil) plus the fate and transport of contaminants between them",
                            correct=True,
                        ),
                        opt("Only around laboratory glassware technique"),
                        opt("Around a single pollutant"),
                    ),
                    "Water, air, and soil chemistry, tied together by how pollutants "
                    "move and transform between phases.",
                ),
                q(
                    "What does each content lesson include?",
                    (
                        opt("Only a block of prose"),
                        opt(
                            "A direct explanation, a mermaid diagram, and a worked "
                            "formula or calculation grounded in real practice",
                            correct=True,
                        ),
                        opt("A video and nothing else"),
                        opt("Only a quiz"),
                    ),
                    "Explanation + diagram + a concrete formula or calculation, then a "
                    "short checkpoint quiz.",
                ),
            ),
        ),
        # -- 1. Carbonate system --------------------------------------
        _t(
            "Aquatic chemistry and the carbonate system",
            "11 min",
            """# Aquatic chemistry and the carbonate system

Almost every question about natural water comes back to the **carbonate
system** - the coupled equilibria of carbon dioxide, carbonic acid,
bicarbonate and carbonate. It sets the **pH** of most fresh and marine
waters and gives them the capacity to resist change.

Carbon dioxide from the air (and from respiration) dissolves and hydrates:

```text
CO2(g)  +  H2O  <->  H2CO3        (dissolution and hydration)
H2CO3        <->  H+  +  HCO3-     pKa1 = 6.35  (25 C)
HCO3-        <->  H+  +  CO3^2-    pKa2 = 10.33 (25 C)
```

Because pKa1 is 6.35 and pKa2 is 10.33, in the typical natural-water
range of pH 6.5 to 8.5 the dominant species is **bicarbonate (HCO3-)**.
Below pH 6.35 dissolved CO2 dominates; above pH 10.33 carbonate does.

**Alkalinity** is the water's acid-neutralising capacity - the amount of
strong acid needed to bring it to the carbonic-acid endpoint. In most
waters it is carbonate alkalinity:

```text
Alkalinity ~= [HCO3-] + 2*[CO3^2-] + [OH-] - [H+]   (equivalents per litre)

Worked example - a river at pH 8.0:
  measured alkalinity = 2.0 meq/L (about 100 mg/L as CaCO3)
  at pH 8.0, [CO3^2-] and [OH-] are tiny, so:
      [HCO3-] ~= 2.0 mmol/L
  A dose of 1.0 meq/L of strong acid consumes half the bicarbonate,
  and because the water is buffered the pH barely moves - that is the
  practical meaning of alkalinity as buffering.
```

The **buffer** works because adding acid converts HCO3- to CO2 and adding
base converts it to CO3^2-, soaking up the change. This is why a river
with 100 mg/L alkalinity as CaCO3 shrugs off an acid input that would
crash the pH of pure water. WHO and CONAMA both use pH and alkalinity as
core water-quality indicators for exactly this reason.

```mermaid
graph LR
    CO2["Dissolved CO2"] --> H2CO3["Carbonic acid"]
    H2CO3 --> HCO3["Bicarbonate dominant pH 6.5 to 8.5"]
    HCO3 --> CO3["Carbonate above pH 10.3"]
    HCO3 --> BUFFER["Buffers against acid and base"]
    BUFFER --> ALK["Alkalinity acid neutralising capacity"]
```

Remember: the carbonate system sets pH and supplies alkalinity; know
which species dominates at a given pH and you can predict how a water will
respond to an acid or base load.
""",
        ),
        quiz_lesson(
            "Quiz: Aquatic chemistry and the carbonate system",
            (
                q(
                    "In the typical natural-water range of pH 6.5 to 8.5, which "
                    "carbonate species dominates?",
                    (
                        opt("Dissolved CO2"),
                        opt("Bicarbonate HCO3-", correct=True),
                        opt("Carbonate CO3^2-"),
                        opt("Hydroxide OH-"),
                    ),
                    "With pKa1 = 6.35 and pKa2 = 10.33, bicarbonate dominates between "
                    "them; CO2 below 6.35, carbonate above 10.33.",
                ),
                q(
                    "What does alkalinity measure?",
                    (
                        opt("How basic the water smells"),
                        opt(
                            "The water's acid-neutralising capacity - how much strong "
                            "acid it can absorb before the pH drops sharply",
                            correct=True,
                        ),
                        opt("The total dissolved oxygen"),
                        opt("The temperature of the water"),
                    ),
                    "Alkalinity is acid-neutralising capacity, in most waters supplied "
                    "by bicarbonate and carbonate.",
                ),
                q(
                    "Why does a river with high alkalinity resist pH change when acid is added?",
                    (
                        opt("The acid evaporates"),
                        opt(
                            "Bicarbonate converts the added acid to CO2 (and base to "
                            "carbonate), soaking up the change - the buffering action",
                            correct=True,
                        ),
                        opt("Water cannot change pH"),
                        opt("The acid freezes"),
                    ),
                    "The coupled equilibria consume added acid or base, so pH moves "
                    "only slightly - that is buffering.",
                ),
            ),
        ),
        # -- 2. Dissolved oxygen & redox ------------------------------
        _t(
            "Dissolved oxygen and redox reactions",
            "11 min",
            """# Dissolved oxygen and redox reactions

**Dissolved oxygen (DO)** is the single best indicator of a water body's
health. Fish need roughly 5 mg/L; below about 2 mg/L water is **hypoxic**
and most aquatic life suffers. DO is controlled by a balance: **aeration**
and photosynthesis add oxygen, while **microbial decomposition** of
organic matter consumes it.

The oxygen demand of organic pollution is measured as **BOD** (biochemical
oxygen demand - what microbes consume) and **COD** (chemical oxygen demand
- a stronger chemical oxidation). When sewage enters a river, microbes
oxidise the organic load and draw DO down, forming an **oxygen sag** that
recovers downstream as reaeration catches up.

The classic **Streeter-Phelps** model captures the sag as a competition
between deoxygenation (rate kd) and reaeration (rate kr):

```text
dD/dt = kd*L - kr*D

  D = dissolved-oxygen deficit (saturation minus actual DO), mg/L
  L = remaining BOD in the water, mg/L
  kd = deoxygenation rate constant, per day
  kr = reaeration rate constant, per day

Critical point - where DO is lowest (deficit greatest):
  t_c = 1/(kr - kd) * ln[ (kr/kd) * (1 - D0*(kr - kd)/(kd*L0)) ]

Read it simply: strong BOD (large L, large kd) deepens the sag; fast
reaeration (large kr, e.g. a turbulent shallow reach) fills it back in.
```

Below the surface, once oxygen is exhausted, microbes turn to other
**electron acceptors** in a fixed thermodynamic order - the **redox
ladder**. Each step yields less energy, so the most favourable acceptor is
used first:

```mermaid
graph TD
    O2["Aerobic oxygen respiration"] --> NO3["Nitrate reduction"]
    NO3 --> MN["Manganese reduction"]
    MN --> FE["Iron reduction"]
    FE --> SO4["Sulfate reduction"]
    SO4 --> CH4["Methanogenesis"]
    CH4 --> ANOX["Deep anoxic sediment"]
```

This ladder explains a lot of environmental chemistry: nitrate disappears
before iron does, sulfate reduction produces the rotten-egg smell of
anoxic sediment, and methane forms only when everything else is gone.
CONAMA 357 and US EPA both set minimum DO limits (commonly 5 to 6 mg/L for
healthy freshwater) precisely because DO integrates all of this.

Remember: DO is set by a tug-of-war between decomposition and reaeration;
model the sag with Streeter-Phelps, and remember that anoxic water works
its way down the redox ladder.
""",
        ),
        quiz_lesson(
            "Quiz: Dissolved oxygen and redox reactions",
            (
                q(
                    "What does the Streeter-Phelps model describe?",
                    (
                        opt("The colour of a river"),
                        opt(
                            "The dissolved-oxygen sag downstream of an organic load, as "
                            "a balance between deoxygenation and reaeration",
                            correct=True,
                        ),
                        opt("The speed of a river's current only"),
                        opt("The concentration of dissolved metals"),
                    ),
                    "It models the DO deficit D from competing rates kd "
                    "(deoxygenation) and kr (reaeration) - the oxygen sag.",
                ),
                q(
                    "As oxygen is exhausted, in what order do microbes use electron acceptors?",
                    (
                        opt("Randomly, with no pattern"),
                        opt(
                            "In a fixed thermodynamic order - oxygen, then nitrate, "
                            "manganese, iron, sulfate, and finally methanogenesis",
                            correct=True,
                        ),
                        opt("Sulfate first, then oxygen"),
                        opt("Only oxygen is ever used"),
                    ),
                    "The redox ladder: the most energy-yielding acceptor (oxygen) goes "
                    "first, methanogenesis last.",
                ),
                q(
                    "What do BOD and COD both measure?",
                    (
                        opt("The salt content of water"),
                        opt(
                            "The oxygen demand of the water - BOD what microbes consume, "
                            "COD by stronger chemical oxidation",
                            correct=True,
                        ),
                        opt("The pH of the water"),
                        opt("The turbidity only"),
                    ),
                    "Both quantify oxidisable load; COD is typically higher because it "
                    "oxidises material microbes will not. COD is at least BOD for the "
                    "same sample, since chemical oxidation reaches compounds biology cannot.",
                ),
            ),
        ),
        # -- 3. Equilibria & solubility -------------------------------
        _t(
            "Chemical equilibria and solubility",
            "11 min",
            """# Chemical equilibria and solubility

Whether a metal stays dissolved or drops out as a solid, whether a mineral
weathers or precipitates - these are questions of **chemical equilibrium**.
The key tool is the **solubility product**, Ksp, the equilibrium constant
for a solid dissolving into its ions.

For a salt that dissolves as MmXn:

```text
MmXn(s)  <->  m*M^n+  +  n*X^m-
Ksp = [M^n+]^m * [X^m-]^n     (activities, approximated as concentrations)

Worked example - will calcium carbonate precipitate?
  Ksp(CaCO3, calcite) = 3.3e-9 at 25 C
  A water has [Ca^2+] = 1.0e-3 M and [CO3^2-] = 5.0e-5 M
  Ion activity product IAP = [Ca^2+]*[CO3^2-] = 1.0e-3 * 5.0e-5 = 5.0e-8

  Saturation index  SI = log10(IAP / Ksp) = log10(5.0e-8 / 3.3e-9)
                       = log10(15.2) = +1.18

  SI > 0  -> supersaturated, CaCO3 tends to precipitate (scaling)
  SI = 0  -> at equilibrium
  SI < 0  -> undersaturated, the solid dissolves
```

The **saturation index (SI)** is how practitioners read solubility in the
field: it tells a water-treatment engineer whether a pipe will scale up
with calcium carbonate or corrode. The Langelier Index used in drinking
water is exactly this idea applied to calcite.

Several factors shift these equilibria:

- **pH** - controls speciation; carbonate rises with pH, so CaCO3 is far
  less soluble in alkaline water. Metal hydroxides precipitate as pH rises.
- **Common-ion effect** - adding a shared ion (more CO3^2-) pushes the
  equilibrium toward the solid, lowering solubility.
- **Complexation** - ligands (chloride, natural organic matter) can keep a
  metal in solution far above its simple Ksp would predict.
- **Temperature** - most salts dissolve more at higher T, but calcite is
  unusual and precipitates more when heated (hence kettle scale).

```mermaid
graph LR
    SOLID["Solid mineral"] --> IONS["Dissolved ions"]
    IONS --> IAP["Ion activity product"]
    IAP --> SI["Saturation index vs Ksp"]
    SI --> PPT["Above zero precipitates"]
    SI --> DISS["Below zero dissolves"]
    PH["pH and complexation"] --> IONS
```

Remember: compute the ion activity product, compare it to Ksp through the
saturation index, and you can predict whether a solid forms or dissolves -
the basis of scaling, corrosion, and mineral weathering.
""",
        ),
        quiz_lesson(
            "Quiz: Chemical equilibria and solubility",
            (
                q(
                    "What does the solubility product Ksp represent?",
                    (
                        opt("The speed at which a solid dissolves"),
                        opt(
                            "The equilibrium constant for a solid dissolving into its "
                            "ions - the product of ion concentrations at saturation",
                            correct=True,
                        ),
                        opt("The pH of the solution"),
                        opt("The temperature of dissolution"),
                    ),
                    "Ksp is the equilibrium ion activity product at saturation; compare "
                    "it to the actual IAP to judge saturation.",
                ),
                q(
                    "A water has a saturation index of +1.2 for calcite. What happens?",
                    (
                        opt("The calcite dissolves"),
                        opt(
                            "The water is supersaturated, so CaCO3 tends to precipitate (scaling)",
                            correct=True,
                        ),
                        opt("Nothing - the water is exactly at equilibrium"),
                        opt("The pH drops to zero"),
                    ),
                    "SI > 0 means the ion activity product exceeds Ksp: supersaturated, "
                    "the solid precipitates.",
                ),
                q(
                    "How can complexation keep a metal dissolved above its simple Ksp?",
                    (
                        opt("It heats the water"),
                        opt(
                            "Ligands bind the metal into soluble complexes, lowering the "
                            "free-ion concentration so the solid does not form",
                            correct=True,
                        ),
                        opt("It raises the temperature only"),
                        opt("It has no effect on solubility"),
                    ),
                    "Ligands (chloride, natural organic matter) tie up the free metal "
                    "ion, so the solubility limit on the free ion is not reached.",
                ),
            ),
        ),
        # -- 4. Sorption & partitioning -------------------------------
        _t(
            "Sorption and partitioning between phases",
            "11 min",
            """# Sorption and partitioning between phases

A contaminant released to the environment does not stay in one phase. It
distributes itself among **water, air, solids, and living tissue** according
to a set of **partition coefficients**. Predicting where a chemical ends up
- and therefore who is exposed - is largely a matter of these ratios.

The central quantities:

- **Kow (octanol-water partition coefficient)** - the ratio of a chemical's
  concentration in octanol to water. High Kow (reported as log Kow) means
  the chemical is **hydrophobic**: it prefers organic matter, sorbs to
  soils and sediments, and **bioaccumulates** in fat.
- **Koc (organic-carbon partition coefficient)** - how strongly a chemical
  sorbs to the organic carbon in soil or sediment. For neutral organics,
  Koc correlates closely with Kow.
- **KH (Henry's law constant)** - the ratio of a chemical's tendency to be
  in air versus water. High KH means it **volatilises** readily.

The soil-water distribution follows the **linear sorption isotherm** and
its **retardation** of transport:

```text
Kd = Koc * foc            (soil-water distribution coefficient, L/kg)
   foc = fraction of organic carbon in the soil (e.g. 0.01 = 1 percent)

Sorbed concentration:  Cs = Kd * Cw

Retardation factor (how much slower the plume moves than the water):
  R = 1 + (rho_b / theta) * Kd
    rho_b = soil bulk density (kg/L), theta = porosity

Worked example - atrazine, Koc = 100 L/kg, soil foc = 0.01:
  Kd = 100 * 0.01 = 1.0 L/kg
  with rho_b = 1.6 kg/L and theta = 0.4:
  R = 1 + (1.6/0.4)*1.0 = 1 + 4.0 = 5.0
  -> the contaminant front travels 5x slower than groundwater.
```

Henry's law links the water and air phases:

```text
C_air = KH * C_water        (KH dimensionless, air over water)
```

A high log Kow flags the compounds that biomagnify up the food chain (DDT,
PCBs, dioxins); a high KH flags the ones that escape to the atmosphere
(many solvents). US EPA fate models and tools like EPI Suite are built
directly on these partition coefficients.

```mermaid
graph TD
    RELEASE["Chemical released"] --> WATER["Dissolved in water"]
    WATER --> AIR["Volatilises high Henry constant"]
    WATER --> SOIL["Sorbs to organic carbon high Koc"]
    SOIL --> RETARD["Retards plume transport"]
    WATER --> BIO["Bioaccumulates high log Kow"]
    BIO --> FOOD["Biomagnifies up the food chain"]
```

Remember: Kow, Koc and Henry's constant decide the split between water,
solids, air and tissue - and the retardation factor turns Kd into how fast
a plume actually moves.
""",
        ),
        quiz_lesson(
            "Quiz: Sorption and partitioning between phases",
            (
                q(
                    "What does a high octanol-water partition coefficient (log Kow) "
                    "tell you about a chemical?",
                    (
                        opt("It is highly water-soluble and washes away quickly"),
                        opt(
                            "It is hydrophobic - it prefers organic matter, sorbs to "
                            "soils and bioaccumulates in fat",
                            correct=True,
                        ),
                        opt("It evaporates instantly"),
                        opt("It cannot exist in soil"),
                    ),
                    "High Kow means hydrophobic: strong sorption to organic carbon and "
                    "bioaccumulation up the food chain.",
                ),
                q(
                    "A contaminant has a retardation factor R = 5. What does that mean?",
                    (
                        opt("It degrades five times faster"),
                        opt(
                            "Its contaminant front travels about five times slower than "
                            "the groundwater, because of sorption",
                            correct=True,
                        ),
                        opt("It is five times more toxic"),
                        opt("It has five times the solubility"),
                    ),
                    "R = 1 + (rho_b/theta)*Kd; R = 5 means sorption slows the plume "
                    "fivefold relative to water flow.",
                ),
                q(
                    "Which partition coefficient governs whether a chemical volatilises "
                    "from water to air?",
                    (
                        opt("The Henry's law constant KH", correct=True),
                        opt("The solubility product Ksp"),
                        opt("The organic-carbon coefficient Koc"),
                        opt("The alkalinity"),
                    ),
                    "Henry's law constant is the air-over-water ratio; a high KH means "
                    "the chemical readily escapes to the atmosphere.",
                ),
            ),
        ),
        # -- 5. Atmospheric chemistry ---------------------------------
        _t(
            "Atmospheric chemistry - photochemistry, ozone, acid rain",
            "11 min",
            """# Atmospheric chemistry - photochemistry, ozone, acid rain

The atmosphere is a **photochemical reactor** driven by sunlight. The same
molecule, ozone, is protective high up and harmful at ground level - a
distinction worth getting straight.

**Stratospheric ozone** (the "good" ozone layer) forms and shields us from
ultraviolet light through the Chapman cycle:

```text
O2  +  UV  ->  O  +  O            (photolysis of oxygen)
O   +  O2  ->  O3                 (ozone formation)
O3  +  UV  ->  O2  +  O           (ozone absorbs UV - the shield)

Catalytic destruction by chlorine (from CFCs):
  Cl   +  O3  ->  ClO  +  O2
  ClO  +  O   ->  Cl   +  O2       (Cl regenerated - one atom kills many O3)
```

Because chlorine is regenerated, one CFC-derived chlorine atom can destroy
thousands of ozone molecules - the mechanism behind the ozone hole and the
reason the **Montreal Protocol** phased CFCs out.

**Tropospheric (ground-level) ozone** is the "bad" ozone - a component of
**photochemical smog**. It is not emitted directly; it forms when sunlight
drives reactions between nitrogen oxides (NOx) and volatile organic
compounds (VOCs) from traffic and industry:

```text
NO2  +  UV  ->  NO  +  O
O    +  O2  ->  O3               (ozone builds up in sunlit, VOC-rich air)
```

**Acid rain** is the third classic atmospheric problem. Sulfur and
nitrogen oxides from fossil-fuel combustion oxidise and dissolve in cloud
water:

```text
SO2  +  oxidation  +  H2O  ->  H2SO4   (sulfuric acid)
NOx  +  oxidation  +  H2O  ->  HNO3    (nitric acid)

Clean rain is naturally about pH 5.6 (from dissolved CO2);
acid rain drops well below - pH 4 has been recorded downwind of
coal regions, acidifying lakes and stripping nutrients from soil.
```

```mermaid
graph TD
    SUN["Sunlight UV"] --> STRAT["Stratosphere ozone shield"]
    CFC["CFC chlorine"] --> DESTROY["Catalytic ozone loss"]
    STRAT --> DESTROY
    SUN --> SMOG["Ground level ozone and smog"]
    NOX["NOx and VOCs from traffic"] --> SMOG
    SO2["SO2 and NOx from combustion"] --> ACID["Acid rain sulfuric and nitric"]
    ACID --> LAKES["Acidified lakes and soils"]
```

Remember: ozone is good in the stratosphere (a UV shield destroyed
catalytically by CFCs) and bad at ground level (smog from NOx and VOCs);
acid rain comes from SO2 and NOx oxidising to strong acids. AERMOD and
similar models translate these emissions into ground-level concentrations.
""",
        ),
        quiz_lesson(
            "Quiz: Atmospheric chemistry - photochemistry, ozone, acid rain",
            (
                q(
                    "Why is stratospheric ozone 'good' but ground-level ozone 'bad'?",
                    (
                        opt("They are different molecules"),
                        opt(
                            "High up it shields us from harmful UV; at ground level it "
                            "is a toxic component of photochemical smog",
                            correct=True,
                        ),
                        opt("Ground-level ozone blocks UV better"),
                        opt("Stratospheric ozone causes smog"),
                    ),
                    "Same molecule, different place: a protective UV shield in the "
                    "stratosphere, a harmful pollutant near the surface.",
                ),
                q(
                    "How can one CFC-derived chlorine atom destroy thousands of ozone molecules?",
                    (
                        opt("It is consumed after one reaction"),
                        opt(
                            "Chlorine acts catalytically - it is regenerated in the "
                            "cycle, so a single atom destroys ozone repeatedly",
                            correct=True,
                        ),
                        opt("It splits into thousands of atoms"),
                        opt("It does not actually destroy ozone"),
                    ),
                    "Cl reacts with O3 to ClO, then ClO reacts to regenerate Cl - a "
                    "catalytic loop, which is why the Montreal Protocol banned CFCs.",
                ),
                q(
                    "What causes acid rain?",
                    (
                        opt("Dissolved carbon dioxide alone"),
                        opt(
                            "SO2 and NOx from fossil-fuel combustion oxidising and "
                            "dissolving into sulfuric and nitric acids",
                            correct=True,
                        ),
                        opt("Ozone falling from the stratosphere"),
                        opt("Natural rain is already pH 4"),
                    ),
                    "Clean rain is about pH 5.6 from CO2; acid rain drops far lower as "
                    "SO2 and NOx form strong acids.",
                ),
            ),
        ),
        # -- 6. Soil & sediment chemistry -----------------------------
        _t(
            "Soil and sediment chemistry",
            "11 min",
            """# Soil and sediment chemistry

Soils and sediments are the environment's most **chemically reactive
solids**. Their surfaces - clays, iron and manganese oxides, and organic
matter - hold and release nutrients, metals, and pollutants, acting as
both a sink and a delayed source.

The dominant property is **cation exchange capacity (CEC)**: negatively
charged surface sites that hold exchangeable cations (Ca2+, Mg2+, K+,
Na+, and acidic Al3+ and H+). CEC governs fertility and how tightly metals
are retained:

```text
CEC = sum of exchangeable cation charges  (cmol_c per kg of soil)

Base saturation = (Ca + Mg + K + Na) / CEC  x 100 percent
  High base saturation -> fertile, near-neutral soil
  Low base saturation  -> acidic soil dominated by Al3+ and H+

Typical CEC:
  sandy soil        3 to 5   cmol_c/kg   (low retention)
  clay or organic   25 to 40 cmol_c/kg   (high retention)
```

**pH is the master variable** of soil chemistry. It controls metal
mobility through a simple rule of thumb: most metal cations are **more
soluble and mobile in acidic soil** and are immobilised as pH rises toward
neutral, where they precipitate as hydroxides or sorb strongly.

```text
Metal hydroxide solubility falls sharply with pH, e.g.:
  Pb^2+  +  2 OH-  <->  Pb(OH)2(s)

Rule of thumb: for a divalent metal hydroxide, free-metal solubility
falls roughly 100-fold per unit rise in pH (two OH- consumed per metal).
This is why liming (raising pH) is a standard remediation to lock down
lead and cadmium in contaminated soil.
```

Redox status matters too. In **waterlogged, anoxic sediment**, iron and
manganese oxides dissolve (reductive dissolution), releasing the metals
and arsenic they had sorbed - the mechanism behind arsenic contamination
of groundwater in reduced aquifers.

```mermaid
graph TD
    SURF["Reactive surfaces clays oxides organics"] --> CEC["Cation exchange capacity"]
    CEC --> HOLD["Holds Ca Mg K and metals"]
    PH["Soil pH master variable"] --> MOBILE["Acidic soil metals mobile"]
    PH --> LOCK["Neutral to alkaline metals locked"]
    REDOX["Anoxic waterlogging"] --> DISSOLVE["Oxides dissolve release metals and arsenic"]
```

Standards reflect this: CONAMA 420 and US EPA regional screening levels set
soil quality thresholds, and remediation often means adjusting pH or redox
to shift metals from mobile to immobile forms.

Remember: soil holds contaminants through CEC and surface sorption, pH is
the master switch on metal mobility, and changing redox in wet sediment can
suddenly release what was locked away.
""",
        ),
        quiz_lesson(
            "Quiz: Soil and sediment chemistry",
            (
                q(
                    "What does cation exchange capacity (CEC) describe?",
                    (
                        opt("The water-holding capacity of soil"),
                        opt(
                            "The amount of exchangeable cations the soil's negatively "
                            "charged surfaces can hold",
                            correct=True,
                        ),
                        opt("The soil temperature"),
                        opt("The soil's colour"),
                    ),
                    "CEC is the charge of exchangeable cations per kg; it governs "
                    "fertility and metal retention.",
                ),
                q(
                    "How does soil pH generally affect metal mobility?",
                    (
                        opt("Metals are more mobile as pH rises"),
                        opt(
                            "Most metal cations are more mobile in acidic soil and are "
                            "locked down (precipitated or sorbed) as pH rises toward neutral",
                            correct=True,
                        ),
                        opt("pH has no effect on metals"),
                        opt("Metals only move at exactly pH 7"),
                    ),
                    "Raising pH precipitates metal hydroxides and increases sorption - "
                    "why liming immobilises lead and cadmium.",
                ),
                q(
                    "Why can waterlogged, anoxic sediment suddenly release sorbed metals "
                    "and arsenic?",
                    (
                        opt("The water washes them out mechanically"),
                        opt(
                            "Reductive dissolution of iron and manganese oxides frees the "
                            "metals and arsenic that were sorbed to them",
                            correct=True,
                        ),
                        opt("Anoxia raises the pH to 14"),
                        opt("Metals evaporate under water"),
                    ),
                    "Under anoxia the Fe and Mn oxide hosts dissolve, releasing their "
                    "sorbed load - the classic arsenic-in-groundwater mechanism.",
                ),
            ),
        ),
        # -- 7. Fate & transport --------------------------------------
        _t(
            "Fate and transport of contaminants",
            "12 min",
            """# Fate and transport of contaminants

**Fate and transport** ties the whole course together: once a contaminant
is released, where does it go and what happens to it on the way?
**Transport** is the physical movement; **fate** is the chemical and
biological transformation. Three processes move a contaminant, and one
class of processes removes it.

The transport processes:

- **Advection** - bulk movement with the flowing water or air. The plume
  travels at the fluid velocity.
- **Dispersion and diffusion** - spreading that smears and dilutes the
  plume around the advective centre.
- **Sorption** - retardation (from the earlier lesson), slowing the
  reactive fraction relative to the fluid.

The removal processes - **degradation** - include biodegradation,
hydrolysis, and photolysis, often modelled as first-order decay.

In **groundwater**, advection follows **Darcy's law**, and the governing
equation is advection-dispersion with retardation and decay:

```text
Darcy flux:      q = -K * dh/dx        (K = hydraulic conductivity)
Seepage velocity: v = q / theta        (theta = porosity)

Advection-dispersion-reaction (1D):
  R * dC/dt = D * d2C/dx2  -  v * dC/dx  -  R * k * C
    R = retardation factor, D = dispersion coefficient, k = decay rate

First-order decay half-life:  t_half = ln(2) / k
```

In the **atmosphere**, a continuous release from a stack disperses as a
**Gaussian plume** - advected downwind, spreading in the crosswind and
vertical directions:

```text
Gaussian plume, ground-level centreline concentration:
  C(x) = Q / (pi * u * sy * sz) * exp( -H^2 / (2*sz^2) )

    Q  = emission rate (g/s)          u  = wind speed (m/s)
    H  = effective stack height (m)   sy, sz = dispersion coefficients
         that grow with downwind distance and atmospheric stability
```

Higher wind speed and a taller stack lower ground-level concentrations;
stable air (a temperature inversion) traps pollutants and raises them.

```mermaid
graph LR
    SOURCE["Contaminant source"] --> ADV["Advection moves with flow"]
    ADV --> DISP["Dispersion spreads and dilutes"]
    DISP --> SORB["Sorption retards reactive fraction"]
    SORB --> DEG["Degradation removes mass"]
    DEG --> RECEPTOR["Concentration at the receptor"]
```

These are the equations inside the standard models: MODFLOW and MT3D for
groundwater, AERMOD for air, QUAL2K for rivers. They all balance the same
four ideas - advection, dispersion, sorption, degradation.

Remember: transport is advection plus dispersion (with sorption slowing
the reactive part); fate is degradation removing mass. Darcy's law drives
groundwater, the Gaussian plume drives air, and the answer is always the
concentration that reaches a receptor.
""",
        ),
        quiz_lesson(
            "Quiz: Fate and transport of contaminants",
            (
                q(
                    "What is the difference between 'transport' and 'fate'?",
                    (
                        opt("They mean the same thing"),
                        opt(
                            "Transport is the physical movement of a contaminant; fate "
                            "is its chemical and biological transformation",
                            correct=True,
                        ),
                        opt("Transport is chemical, fate is physical"),
                        opt("Fate only applies to air"),
                    ),
                    "Transport moves the mass (advection, dispersion, sorption); fate "
                    "transforms or removes it (degradation).",
                ),
                q(
                    "In groundwater, what does Darcy's law give you?",
                    (
                        opt("The chemical decay rate"),
                        opt(
                            "The flux and hence velocity of groundwater flow from "
                            "hydraulic conductivity and the head gradient",
                            correct=True,
                        ),
                        opt("The sorption coefficient"),
                        opt("The atmospheric stability class"),
                    ),
                    "q = -K*dh/dx gives the Darcy flux; dividing by porosity gives the "
                    "seepage velocity that advects the plume.",
                ),
                q(
                    "In the Gaussian plume model, what lowers the ground-level "
                    "concentration downwind of a stack?",
                    (
                        opt("Lower wind speed and a shorter stack"),
                        opt(
                            "Higher wind speed and a taller effective stack height, which "
                            "dilute and lift the plume",
                            correct=True,
                        ),
                        opt("A temperature inversion"),
                        opt("Increasing the emission rate Q"),
                    ),
                    "C is inversely related to wind speed u and falls with stack height "
                    "H; stable inversions suppress vertical mixing and keep the plume "
                    "near the ground, raising concentrations.",
                ),
            ),
        ),
        # -- 8. Emerging pollutants -----------------------------------
        _t(
            "Emerging pollutants - PFAS, microplastics, pharmaceuticals",
            "12 min",
            """# Emerging pollutants - PFAS, microplastics, pharmaceuticals

**Emerging pollutants** (or contaminants of emerging concern) are chemicals
now detected widely in the environment that older regulations never
anticipated. They are hard to measure, hard to remove, and their long-term
effects are still being worked out. Three families dominate current
concern.

**PFAS** (per- and polyfluoroalkyl substances) are the "forever chemicals".

- The carbon-fluorine bond is one of the strongest in organic chemistry, so
  PFAS resist hydrolysis, photolysis, and biodegradation almost completely
  - they do not break down on any human timescale.
- They are both water-soluble and surface-active, so they travel far in
  groundwater yet also bioaccumulate in blood and liver (bound to protein,
  not fat - unusual among persistent pollutants).
- The US EPA 2024 drinking-water limits for PFOA and PFOS are just **4 parts
  per trillion** - among the lowest regulatory thresholds ever set, a sign
  of how potent and persistent they are.

```text
Unit intuition for trace contaminants:
  1 ng/L  =  1 part per trillion (ppt) in water
  EPA limit for PFOA = 4 ng/L
  = 4 grams dissolved in 1,000,000,000,000 litres
  = roughly four drops in a thousand Olympic swimming pools
Conventional treatment (coagulation, chlorination) barely touches PFAS;
removal needs activated carbon, ion exchange, or reverse osmosis.
```

**Microplastics** are plastic fragments smaller than 5 mm, from broken-down
litter and synthetic fibres. They persist for centuries, sorb hydrophobic
pollutants (high-Kow compounds concentrate on their surfaces, so they act
as pollutant shuttles), and are now found from deep ocean sediment to human
blood.

**Pharmaceuticals and personal-care products** - antibiotics, hormones,
painkillers, contraceptives - enter rivers through wastewater because
sewage plants were never designed to remove them. Even at nanogram-per-litre
levels they matter: synthetic estrogens feminise fish, and environmental
antibiotics drive **antimicrobial resistance**.

```mermaid
graph TD
    SOURCES["Consumer and industrial use"] --> WWTP["Wastewater plant not designed for them"]
    WWTP --> WATER["Rivers and groundwater trace levels"]
    WATER --> PFAS["PFAS forever chemicals persist"]
    WATER --> MICRO["Microplastics shuttle pollutants"]
    WATER --> PHARMA["Pharmaceuticals disrupt and resist"]
    PFAS --> ADV["Advanced treatment GAC ion exchange RO"]
    MICRO --> ADV
    PHARMA --> ADV
```

The common thread: these compounds slip through conventional treatment,
persist, and act at trace concentrations - so the response is **advanced
treatment** (granular activated carbon, ion exchange, reverse osmosis,
advanced oxidation) plus **source control** and better analytical detection.
The EU Water Framework watch list and US EPA UCMR programme track them as
regulation catches up.

Remember: emerging pollutants (PFAS, microplastics, pharmaceuticals) are
persistent, mobile, and active at trace levels - conventional treatment
misses them, so detection, source control, and advanced treatment are the
frontier of environmental chemistry.
""",
        ),
        quiz_lesson(
            "Quiz: Emerging pollutants - PFAS, microplastics, pharmaceuticals",
            (
                q(
                    "Why are PFAS called 'forever chemicals'?",
                    (
                        opt("They are used forever in every product"),
                        opt(
                            "The strong carbon-fluorine bond makes them resist "
                            "hydrolysis, photolysis and biodegradation - they do not "
                            "break down on human timescales",
                            correct=True,
                        ),
                        opt("They glow permanently"),
                        opt("They evaporate and never return"),
                    ),
                    "The C-F bond is exceptionally strong, so PFAS persist almost "
                    "indefinitely - hence EPA limits of just 4 ppt.",
                ),
                q(
                    "Why do microplastics act as pollutant 'shuttles'?",
                    (
                        opt("They dissolve pollutants into gas"),
                        opt(
                            "Their surfaces sorb hydrophobic (high-Kow) pollutants, "
                            "carrying a concentrated load through the environment and "
                            "into organisms",
                            correct=True,
                        ),
                        opt("They neutralise all pollutants they touch"),
                        opt("They only float and never sorb anything"),
                    ),
                    "High-Kow contaminants concentrate on plastic surfaces, so "
                    "microplastics transport and deliver them into food webs.",
                ),
                q(
                    "Why do pharmaceuticals reach rivers, and why does it matter at trace levels?",
                    (
                        opt("They are dumped directly and are harmless"),
                        opt(
                            "Conventional sewage plants were not designed to remove them, "
                            "and even at nanogram levels hormones disrupt wildlife and "
                            "antibiotics drive resistance",
                            correct=True,
                        ),
                        opt("They break down completely before any discharge"),
                        opt("They only affect the colour of water"),
                    ),
                    "They pass through treatment and are biologically active at trace "
                    "concentrations - endocrine disruption and antimicrobial resistance.",
                ),
                q(
                    "What treatment is generally needed to remove emerging pollutants like PFAS?",
                    (
                        opt("Simple chlorination is enough"),
                        opt(
                            "Advanced treatment such as activated carbon, ion exchange, "
                            "reverse osmosis or advanced oxidation",
                            correct=True,
                        ),
                        opt("Nothing - they remove themselves"),
                        opt("Only physical screening"),
                    ),
                    "Conventional coagulation and chlorination barely touch PFAS; "
                    "advanced processes plus source control are required.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In the natural-water pH range of 6.5 to 8.5, which carbonate "
                    "species dominates and what property does it give the water?",
                    (
                        opt("Carbonate, which makes water corrosive"),
                        opt(
                            "Bicarbonate, which buffers the water and provides its "
                            "alkalinity (acid-neutralising capacity)",
                            correct=True,
                        ),
                        opt("Dissolved CO2, which has no effect on pH"),
                        opt("Hydroxide, which lowers the pH"),
                    ),
                    "Between pKa1 (6.35) and pKa2 (10.33), bicarbonate dominates and "
                    "supplies the buffering and alkalinity.",
                ),
                q(
                    "What does the Streeter-Phelps oxygen sag balance?",
                    (
                        opt("Evaporation against rainfall"),
                        opt(
                            "Microbial deoxygenation of an organic load against "
                            "reaeration from the atmosphere",
                            correct=True,
                        ),
                        opt("Sorption against volatilisation"),
                        opt("Advection against dispersion"),
                    ),
                    "kd (deoxygenation) draws DO down, kr (reaeration) restores it - "
                    "the downstream sag and recovery.",
                ),
                q(
                    "As oxygen runs out, which electron acceptor do microbes use last?",
                    (
                        opt("Nitrate"),
                        opt("Sulfate"),
                        opt(
                            "Carbon dioxide, producing methane (methanogenesis) - the "
                            "lowest rung of the redox ladder",
                            correct=True,
                        ),
                        opt("Iron"),
                    ),
                    "Order: oxygen, nitrate, manganese, iron, sulfate, then "
                    "methanogenesis last - least energy-yielding.",
                ),
                q(
                    "A water's saturation index for calcite is negative. What does that imply?",
                    (
                        opt("The water is supersaturated and will scale"),
                        opt(
                            "The water is undersaturated, so calcite dissolves rather "
                            "than precipitates",
                            correct=True,
                        ),
                        opt("The water is exactly at equilibrium"),
                        opt("The pH must be above 14"),
                    ),
                    "SI = log10(IAP/Ksp); negative means IAP below Ksp - undersaturated, "
                    "the solid dissolves.",
                ),
                q(
                    "A high octanol-water partition coefficient (log Kow) predicts that "
                    "a chemical will…",
                    (
                        opt("stay dissolved and flush away quickly"),
                        opt(
                            "sorb to organic matter in soils and sediments and "
                            "bioaccumulate in tissue",
                            correct=True,
                        ),
                        opt("volatilise instantly to the air"),
                        opt("precipitate as a mineral"),
                    ),
                    "High Kow means hydrophobic: strong sorption and bioaccumulation, "
                    "e.g. DDT and PCBs.",
                ),
                q(
                    "Which single factor most controls metal mobility in soil?",
                    (
                        opt("Soil colour"),
                        opt(
                            "pH - metals are mobile in acidic soil and are immobilised as "
                            "pH rises toward neutral",
                            correct=True,
                        ),
                        opt("Soil temperature"),
                        opt("The time of day"),
                    ),
                    "pH is the master variable; raising it precipitates metal "
                    "hydroxides and boosts sorption, which is why liming works.",
                ),
                q(
                    "Ground-level ozone (smog) forms when…",
                    (
                        opt("ozone falls from the stratosphere"),
                        opt(
                            "sunlight drives reactions between NOx and volatile organic "
                            "compounds near the surface",
                            correct=True,
                        ),
                        opt("acid rain neutralises the air"),
                        opt("CFCs are released at ground level"),
                    ),
                    "Tropospheric ozone is a secondary pollutant from sunlit NOx and "
                    "VOCs - unlike the protective stratospheric ozone layer.",
                ),
                q(
                    "In groundwater transport, what does the retardation factor R quantify?",
                    (
                        opt("How fast the contaminant degrades"),
                        opt(
                            "How much slower the sorbing contaminant front moves compared "
                            "to the groundwater itself",
                            correct=True,
                        ),
                        opt("The emission rate from a stack"),
                        opt("The half-life of decay"),
                    ),
                    "R = 1 + (rho_b/theta)*Kd; sorption slows the reactive plume "
                    "relative to the water velocity.",
                ),
                q(
                    "Why are PFAS so difficult to remove from drinking water?",
                    (
                        opt("They are large and settle out on their own"),
                        opt(
                            "The strong carbon-fluorine bond makes them persistent, and "
                            "conventional treatment barely removes them - needing carbon, "
                            "ion exchange or reverse osmosis",
                            correct=True,
                        ),
                        opt("They break down under chlorination"),
                        opt("They evaporate during aeration"),
                    ),
                    "PFAS resist degradation and pass through conventional processes; "
                    "advanced treatment is required, at limits near 4 ppt.",
                ),
                q(
                    "What is the common thread linking PFAS, microplastics and "
                    "pharmaceuticals as emerging pollutants?",
                    (
                        opt("They are all metals"),
                        opt(
                            "They are persistent, mobile and biologically active at trace "
                            "levels, and slip through conventional treatment",
                            correct=True,
                        ),
                        opt("They all evaporate harmlessly"),
                        opt("They are removed by simple filtration"),
                    ),
                    "All three persist, act at trace concentrations, and evade "
                    "conventional treatment - the frontier of environmental chemistry.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

ENVIRONMENTAL_CHEMISTRY_COURSES: tuple[SeedCourse, ...] = (_ENVIRONMENTAL_CHEMISTRY,)
