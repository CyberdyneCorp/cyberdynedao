"""Academy seed content - Bioprocess Engineering.

Engineering with living systems: how cells and enzymes are put to work at
industrial scale. The course walks from industrial microbiology and enzyme
catalysis through cell growth kinetics, bioreactor design, oxygen transfer,
sterilization and aseptic operation, and downstream purification, closing on
scale-up and the pharma, food and biofuel processes that depend on all of it.
Every lesson is a direct explanation with a worked equation or calculation and
a mermaid diagram, followed by a checkpoint quiz; a comprehensive final quiz
closes the course.
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


_BIOPROCESS_ENGINEERING = SeedCourse(
    slug="bioprocess-engineering",
    title="Bioprocess Engineering",
    description=(
        "Engineering with living systems - cell growth kinetics, bioreactor "
        "design, oxygen transfer, sterile operation and downstream "
        "purification for pharma, food and biofuels. Every lesson pairs a "
        "worked design equation or calculation with a process diagram, from "
        "Monod kinetics and oxygen mass transfer to scale-up and product "
        "recovery."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Bioprocess Engineering

A **bioprocess** uses living cells or their enzymes to make a product:
antibiotics and vaccines, beer and yoghurt, ethanol and biodiesel,
enzymes and organic acids. Bioprocess engineering is chemical engineering
applied to biology - you still care about mass and energy balances,
reaction kinetics, heat and mass transfer, and unit operations, but the
catalyst is alive, so it grows, mutates, respires, and dies if you treat
it badly.

The approach here is **concrete**: each lesson explains one idea directly,
works a real design equation or calculation (Monod kinetics, oxygen
transfer, sterilization, a mass balance), and draws the process as a
diagram. After each lesson there is a short quiz; a final quiz covers the
whole course.

What you will build understanding for, in order:

1. **Industrial microbiology and enzymes** - the biocatalysts
2. **Cell growth kinetics (Monod)** - how fast a culture grows
3. **Bioreactor design and operation** - batch, fed-batch, continuous
4. **Aeration, agitation and oxygen transfer** - feeding the culture air
5. **Sterilization and aseptic processing** - keeping only your organism
6. **Downstream processing** - separating and purifying the product
7. **Fermentation scale-up** - from shake flask to production tank
8. **Bioprocesses for pharma, food and biofuels** - putting it together

This is the map from a vial of cells to a purified product. Keep a
calculator handy - the equations are the point.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is a bioprocess?",
                    (
                        opt("A purely chemical reaction with no catalyst"),
                        opt(
                            "A process that uses living cells or their enzymes to make a product",
                            correct=True,
                        ),
                        opt("A way to model climate systems"),
                        opt("A type of distillation column"),
                    ),
                    "Bioprocesses use a biological catalyst - whole cells or isolated "
                    "enzymes - to convert raw materials into a product.",
                ),
                q(
                    "Why is bioprocess engineering different from ordinary chemical "
                    "reaction engineering?",
                    (
                        opt("It ignores mass and energy balances"),
                        opt(
                            "The catalyst is alive - it grows, respires and dies, so "
                            "the process must keep it healthy",
                            correct=True,
                        ),
                        opt("It never uses heat or mass transfer"),
                        opt("It only works at very high temperature"),
                    ),
                    "The same transport and balance principles apply, but a living "
                    "catalyst adds growth, respiration and contamination concerns.",
                ),
            ),
        ),
        # -- 1. Industrial microbiology and enzymes --------------------
        _t(
            "Industrial microbiology and enzymes",
            "10 min",
            """# Industrial microbiology and enzymes

Industrial bioprocesses run on a handful of well-characterized
**biocatalysts**. The workhorses are microbes - *Escherichia coli* and
*Bacillus* for proteins and enzymes, *Saccharomyces cerevisiae* (baker's
yeast) for ethanol, *Aspergillus* moulds for citric acid and enzymes,
*Penicillium* for antibiotics - plus mammalian **CHO cells** for complex
therapeutic proteins. The organism is selected, and often genetically
engineered, to overproduce one target.

The catalyst may be the **whole cell** (fermentation) or an **isolated
enzyme** (biocatalysis). Enzymes are proteins that accelerate one
reaction with high **specificity** under mild conditions - near neutral
pH, moderate temperature. They are classified by the reaction they run
(oxidoreductases, transferases, hydrolases, lyases, isomerases, ligases).

Enzyme rate is usually described by **Michaelis-Menten** kinetics: rate
rises with substrate until the enzyme saturates at a maximum, `Vmax`.
`Km` is the substrate concentration giving half of `Vmax` - a measure of
affinity.

```text
Michaelis-Menten rate:

        Vmax * [S]
  v  =  -----------
         Km + [S]

  v     = reaction rate
  Vmax  = maximum rate (all enzyme saturated)
  Km    = substrate at which v = Vmax/2 (affinity)
  [S]   = substrate concentration

Worked example: Vmax = 2.0 mmol/(L.min), Km = 5.0 mmol/L, [S] = 10 mmol/L
  v = 2.0 * 10 / (5.0 + 10) = 20 / 15 = 1.33 mmol/(L.min)
```

Cells are held in a working stock - a **cell bank** (a master bank and a
working bank of frozen vials) - so every production run starts from the
same genetic material. A run begins by reviving one vial and growing it
up through a **seed train** of ever-larger flasks and seed reactors.

```mermaid
graph LR
    BANK["Frozen cell bank"] --> VIAL["Revive one vial"]
    VIAL --> FLASK["Shake flask"]
    FLASK --> SEED["Seed reactor"]
    SEED --> PROD["Production reactor"]
    PROD --> PRODUCT["Product enzyme or cells"]
```

Remember: pick the right organism or enzyme, keep it consistent through a
cell bank, and describe enzyme rate with Michaelis-Menten kinetics.
""",
        ),
        quiz_lesson(
            "Quiz: Industrial microbiology and enzymes",
            (
                q(
                    "In Michaelis-Menten kinetics, what does Km represent?",
                    (
                        opt("The maximum possible reaction rate"),
                        opt(
                            "The substrate concentration at which the rate is half "
                            "of Vmax - a measure of affinity",
                            correct=True,
                        ),
                        opt("The total amount of enzyme present"),
                        opt("The temperature of the reaction"),
                    ),
                    "Km is the substrate concentration giving v = Vmax/2; a lower Km "
                    "means higher affinity for the substrate.",
                ),
                q(
                    "Why do industrial processes keep a master and working cell bank?",
                    (
                        opt("To make the culture grow faster"),
                        opt(
                            "So every production run starts from the same, "
                            "consistent genetic material",
                            correct=True,
                        ),
                        opt("To avoid needing a bioreactor"),
                        opt("Because banks replace sterilization"),
                    ),
                    "A frozen cell bank preserves a consistent strain, so runs are "
                    "reproducible over the life of the product.",
                ),
                q(
                    "What is an advantage of enzymes as catalysts?",
                    (
                        opt("They work only at very high temperature and pressure"),
                        opt(
                            "High specificity for one reaction under mild conditions "
                            "of pH and temperature",
                            correct=True,
                        ),
                        opt("They never saturate with substrate"),
                        opt("They require no substrate at all"),
                    ),
                    "Enzymes catalyze one reaction with high specificity under mild, "
                    "near-ambient conditions.",
                ),
            ),
        ),
        # -- 2. Cell growth kinetics (Monod) ---------------------------
        _t(
            "Cell growth kinetics (Monod)",
            "11 min",
            """# Cell growth kinetics (Monod)

A growing culture behaves like an **autocatalytic** reaction: cells make
more cells. In the exponential phase, biomass concentration `X` grows in
proportion to how much biomass is already there:

```text
Exponential growth:

  dX/dt = mu * X        ->      X(t) = X0 * exp(mu * t)

  mu = specific growth rate (per hour)

Doubling time:
  td = ln(2) / mu

Example: mu = 0.5 /h  ->  td = 0.693 / 0.5 = 1.39 h
```

The specific growth rate `mu` is not constant - it depends on how much
**limiting substrate** (often the carbon source) is available. The
**Monod equation** captures this, and looks exactly like Michaelis-Menten:

```text
Monod equation:

           mu_max * S
  mu  =  --------------
            Ks + S

  mu_max = maximum specific growth rate
  Ks     = substrate at which mu = mu_max/2 (saturation constant)
  S      = limiting substrate concentration

At high S, mu -> mu_max (growth is saturated).
At low  S, mu ~ (mu_max/Ks) * S (growth is substrate limited).
```

A batch culture passes through recognizable **phases**: **lag** (cells
adapt), **exponential/log** (`mu` near `mu_max`), **stationary** (substrate
exhausted or inhibitor built up, growth = death), and **death**. Two more
useful numbers: the **yield coefficient** `Yxs` (biomass formed per gram
of substrate consumed) and the specific rates of substrate uptake and
product formation.

```mermaid
graph LR
    LAG["Lag phase adapt"] --> LOG["Exponential phase"]
    LOG --> STAT["Stationary phase"]
    STAT --> DEATH["Death phase"]
    SUB["Substrate S"] --> MU["Monod sets mu"]
    MU --> LOG
```

Worked example: `Yxs` = 0.5 g cells per g glucose, and you consume 40 g/L
of glucose. Biomass produced = 0.5 * 40 = 20 g/L (above the inoculum).

Remember: exponential growth is set by `mu`, and Monod ties `mu` to the
limiting substrate - the master relationship for sizing a fermentation.
""",
        ),
        quiz_lesson(
            "Quiz: Cell growth kinetics (Monod)",
            (
                q(
                    "The Monod equation relates the specific growth rate mu to what?",
                    (
                        opt("The temperature of the reactor only"),
                        opt(
                            "The concentration of the limiting substrate, saturating at mu_max",
                            correct=True,
                        ),
                        opt("The color of the culture broth"),
                        opt("The stirrer speed alone"),
                    ),
                    "Monod: mu = mu_max * S / (Ks + S) - growth rate rises with "
                    "substrate and saturates at mu_max.",
                ),
                q(
                    "If mu = 0.35 /h during exponential growth, the doubling time is about:",
                    (
                        opt("About 0.35 h"),
                        opt("About 2.0 h", correct=True),
                        opt("About 10 h"),
                        opt("It cannot be calculated"),
                    ),
                    "td = ln(2)/mu = 0.693/0.35 = 1.98 h, about 2 hours.",
                ),
                q(
                    "In a batch culture, why does growth slow into the stationary phase?",
                    (
                        opt("The cells run out of stirring"),
                        opt(
                            "The limiting substrate is exhausted or inhibitory "
                            "products accumulate, so growth equals death",
                            correct=True,
                        ),
                        opt("The reactor gets too cold to measure"),
                        opt("The Monod constant Ks becomes negative"),
                    ),
                    "Stationary phase is reached when substrate runs low or "
                    "inhibitors build up; net growth stops.",
                ),
            ),
        ),
        # -- 3. Bioreactor design and operation ------------------------
        _t(
            "Bioreactor design and operation",
            "11 min",
            """# Bioreactor design and operation

A **bioreactor** (fermenter) is the vessel that holds the culture under
controlled conditions. The classic industrial design is the **stirred-tank
reactor (STR)**: a cylindrical, jacketed vessel with an impeller, a
**sparger** to bubble in air, **baffles** to prevent swirl, and probes for
**temperature, pH, dissolved oxygen (DO)** and foam. Control loops hold
each variable at setpoint - cooling water in the jacket removes metabolic
heat, acid/base pumps hold pH, an antifoam pump breaks foam.

There are three ways to **operate** it:

- **Batch** - load medium and inoculum, run to completion, harvest. Simple
  and easy to keep sterile, but productivity is limited and substrate can
  be inhibitory at high starting concentration.
- **Fed-batch** - start with a small charge and **feed** substrate slowly
  during the run. This keeps the sugar low, avoids overflow metabolism
  (e.g. acetate in *E. coli*, the Crabtree effect in yeast), and reaches
  high cell densities. It is the workhorse of industry.
- **Continuous (chemostat)** - feed fresh medium and withdraw broth at the
  same rate. At steady state the **dilution rate** `D = F/V` sets the
  growth rate: `mu = D`. Great for study and some bulk products, but harder
  to keep sterile and stable for long runs.

```text
Chemostat steady state:

  D = F / V         (dilution rate, per hour)
  At steady state:  mu = D

  Washout when D > mu_max (cells leave faster than they grow).

Example: F = 2 L/h into V = 10 L  ->  D = 0.2 /h, so mu = 0.2 /h
         If mu_max = 0.5 /h, D = 0.2 is safely below washout.
```

```mermaid
graph TD
    FEED["Sterile medium feed"] --> TANK["Stirred tank reactor"]
    AIR["Air via sparger"] --> TANK
    TANK --> IMP["Impeller mixes"]
    JACKET["Cooling jacket"] --> TANK
    PROBE["pH DO temperature probes"] --> CTRL["Control loops"]
    CTRL --> TANK
    TANK --> HARVEST["Harvest broth"]
```

Remember: the stirred tank is the standard vessel; batch, fed-batch and
continuous are the three operating modes, and fed-batch dominates industry
because it controls substrate and reaches high cell density.
""",
        ),
        quiz_lesson(
            "Quiz: Bioreactor design and operation",
            (
                q(
                    "In a chemostat at steady state, the specific growth rate equals:",
                    (
                        opt("The impeller tip speed"),
                        opt("The dilution rate D = F/V", correct=True),
                        opt("The maximum growth rate mu_max always"),
                        opt("Zero"),
                    ),
                    "At chemostat steady state mu = D; if D exceeds mu_max the culture washes out.",
                ),
                q(
                    "Why is fed-batch the workhorse of industrial fermentation?",
                    (
                        opt("It removes the need for any sterilization"),
                        opt(
                            "Feeding substrate slowly keeps sugar low, avoids "
                            "overflow metabolism, and reaches high cell density",
                            correct=True,
                        ),
                        opt("It requires no impeller or aeration"),
                        opt("It is the only mode that can be sterile"),
                    ),
                    "Controlled feeding avoids substrate inhibition and overflow "
                    "byproducts while pushing cell density high.",
                ),
                q(
                    "What is the role of baffles in a stirred-tank bioreactor?",
                    (
                        opt("To heat the broth"),
                        opt(
                            "To break up swirling flow and improve mixing and gas dispersion",
                            correct=True,
                        ),
                        opt("To measure pH"),
                        opt("To store the product"),
                    ),
                    "Baffles convert bulk rotation into turbulent mixing, improving "
                    "oxygen dispersion and homogeneity.",
                ),
            ),
        ),
        # -- 4. Aeration, agitation and oxygen transfer ----------------
        _t(
            "Aeration, agitation and oxygen transfer",
            "12 min",
            """# Aeration, agitation and oxygen transfer

For aerobic cultures, **oxygen is usually the limiting reactant**, and it
is hard to supply: oxygen is only sparingly soluble in water (about
7 mg/L in equilibrium with air at 30 C). A dense culture can consume the
dissolved oxygen in seconds, so you must transfer it from bubbles into the
liquid continuously.

The rate of **oxygen transfer (OTR)** from gas to liquid is:

```text
Oxygen transfer rate:

  OTR = kLa * (C_star - C_L)

  kLa     = volumetric mass-transfer coefficient (per hour)
  C_star  = dissolved O2 in equilibrium with the gas (saturation)
  C_L     = actual dissolved O2 in the broth

The oxygen uptake rate by cells:  OUR = qO2 * X

At steady state you need:  OTR >= OUR
```

The engineer's job is to make **kLa** big enough. kLa rises with **gas
flow rate**, with **agitation power per unit volume** (smaller bubbles,
more interfacial area, thinner films), and it drops in viscous or
coalescing broths. Faster/bigger impellers raise kLa but also raise
**shear** (which can damage fragile mammalian or mycelial cells) and heat
input - a real design trade-off.

Worked example: a culture needs `OUR` = 80 mmol O2/(L.h). With
`C_star` = 0.24 mmol/L and holding `C_L` = 0.04 mmol/L, the required
coefficient is

```text
  kLa = OUR / (C_star - C_L)
      = 80 / (0.24 - 0.04)
      = 80 / 0.20
      = 400 per hour
```

so the aeration and agitation must be set to deliver kLa of at least
400/h. Dissolved oxygen is measured with a **DO probe** and often held at
setpoint by a control loop that ramps stirrer speed or air flow.

```mermaid
graph LR
    AIR["Air sparged as bubbles"] --> FILM["Gas liquid film"]
    STIR["Agitation raises kLa"] --> FILM
    FILM --> DO["Dissolved oxygen C_L"]
    DO --> CELLS["Cells consume OUR"]
    DO --> PROBE["DO probe"]
    PROBE --> LOOP["Control stirrer and air"]
    LOOP --> STIR
```

Remember: oxygen transfer is often the bottleneck of aerobic culture -
size the system so OTR = kLa times the driving force meets or exceeds the
cells' oxygen uptake.
""",
        ),
        quiz_lesson(
            "Quiz: Aeration, agitation and oxygen transfer",
            (
                q(
                    "Why is oxygen supply often the limiting factor in aerobic fermentation?",
                    (
                        opt("Oxygen dissolves extremely well in water"),
                        opt(
                            "Oxygen is only sparingly soluble, yet dense cultures "
                            "consume it in seconds, so it must be transferred "
                            "continuously",
                            correct=True,
                        ),
                        opt("Cells do not need oxygen"),
                        opt("Oxygen reacts with the impeller"),
                    ),
                    "Low solubility plus high demand makes gas-to-liquid oxygen "
                    "transfer the usual bottleneck.",
                ),
                q(
                    "In OTR = kLa * (C_star - C_L), what does kLa represent?",
                    (
                        opt("The oxygen uptake rate of the cells"),
                        opt(
                            "The volumetric mass-transfer coefficient - how well the "
                            "system moves oxygen from gas to liquid",
                            correct=True,
                        ),
                        opt("The saturation concentration of oxygen"),
                        opt("The reactor temperature"),
                    ),
                    "kLa lumps the transfer coefficient and interfacial area; raising "
                    "agitation and aeration raises it.",
                ),
                q(
                    "A culture has OUR = 60 mmol/(L.h), C_star = 0.25 mmol/L and you "
                    "hold C_L = 0.05 mmol/L. The minimum kLa is:",
                    (
                        opt("About 12 per hour"),
                        opt("About 300 per hour", correct=True),
                        opt("About 60 per hour"),
                        opt("About 1200 per hour"),
                    ),
                    "kLa = OUR/(C_star - C_L) = 60/0.20 = 300 per hour.",
                ),
                q(
                    "What is a downside of raising agitation to increase kLa?",
                    (
                        opt("It lowers the oxygen demand of the cells"),
                        opt(
                            "It raises shear (which can damage fragile cells) and "
                            "adds heat that must be removed",
                            correct=True,
                        ),
                        opt("It always sterilizes the broth"),
                        opt("It has no effect on kLa"),
                    ),
                    "More power gives higher kLa but more shear and heat - a design "
                    "trade-off, especially for shear-sensitive cells.",
                ),
            ),
        ),
        # -- 5. Sterilization and aseptic processing -------------------
        _t(
            "Sterilization and aseptic processing",
            "11 min",
            """# Sterilization and aseptic processing

A fermentation must contain **only your organism**. A single contaminant
that grows faster, or makes a toxin, ruins the batch - and in pharma can
be dangerous. So the medium, the vessel, the air and every addition must
be **sterile**, and the process must stay **aseptic** (contamination-free)
throughout the run.

**Heat sterilization** of liquid medium follows first-order **thermal
death kinetics** of spores:

```text
Thermal death of spores (first order):

  dN/dt = -k_d * N        ->      N = N0 * exp(-k_d * t)

  k_d follows Arrhenius:  k_d = A * exp(-Ea / (R * T))

Sterilization criterion - the Del factor:

  Del = ln(N0 / N) = integral of k_d dt over the cycle

A common target reduces viable spores from N0 to a probability
of survival of 1e-3 in the whole batch.
```

Because `k_d` climbs steeply with temperature (high `Ea`) while nutrient
destruction climbs more slowly, **higher temperature for shorter time**
(HTST) kills spores while sparing the medium - the basis of **continuous**
sterilization for large volumes. Small batches use in-situ steam
sterilization of the whole vessel (typically 121 C).

Other streams need their own methods:

- **Inlet and outlet air** - sterilized by **depth or membrane filtration**
  (0.2 micron), not heat.
- **Heat-labile media** (some sugars, vitamins, proteins) - **filter
  sterilized** through 0.2 micron membranes.
- **The running process** - kept aseptic by positive pressure, steam-locked
  valves, sterile sampling, and sterile feed and antifoam additions.

```mermaid
graph TD
    MEDIA["Liquid medium"] --> HEAT["Heat sterilize HTST"]
    AIR["Inlet air"] --> FILT["0.2 micron filter"]
    LABILE["Heat labile additives"] --> MEMB["Membrane filter"]
    HEAT --> REACTOR["Sterile bioreactor"]
    FILT --> REACTOR
    MEMB --> REACTOR
    REACTOR --> ASEPTIC["Aseptic operation"]
```

Worked idea: to raise `Del` you can either hold longer at the same
temperature or, far more efficiently, raise the temperature - because
`k_d` depends exponentially on `T` through the Arrhenius term.

Remember: sterilize medium with heat (HTST spares nutrients), sterilize
air and heat-labile streams by filtration, and hold the whole process
aseptic for the entire run.
""",
        ),
        quiz_lesson(
            "Quiz: Sterilization and aseptic processing",
            (
                q(
                    "Thermal death of microbial spores is usually modeled as:",
                    (
                        opt("Zero-order (constant rate)"),
                        opt(
                            "First-order decay, N = N0 * exp(-k_d * t)",
                            correct=True,
                        ),
                        opt("Instantaneous at any temperature"),
                        opt("Independent of temperature"),
                    ),
                    "Spore death follows first-order kinetics; k_d rises with "
                    "temperature via the Arrhenius relation.",
                ),
                q(
                    "Why is high-temperature short-time (HTST) sterilization preferred for medium?",
                    (
                        opt("It uses no energy at all"),
                        opt(
                            "Spore death rate climbs with temperature faster than "
                            "nutrient destruction, so hot-and-fast kills spores while "
                            "sparing the medium",
                            correct=True,
                        ),
                        opt("It avoids the need for a bioreactor"),
                        opt("It works only below room temperature"),
                    ),
                    "The high activation energy of spore death makes higher "
                    "temperature far more selective for killing than for nutrient loss.",
                ),
                q(
                    "How is the inlet air to a bioreactor usually sterilized?",
                    (
                        opt("By boiling it"),
                        opt("By 0.2 micron depth or membrane filtration", correct=True),
                        opt("By adding antibiotics to the air"),
                        opt("It does not need sterilizing"),
                    ),
                    "Air and heat-labile streams are sterilized by 0.2 micron "
                    "filtration rather than heat.",
                ),
            ),
        ),
        # -- 6. Downstream processing ----------------------------------
        _t(
            "Downstream processing (separation and purification)",
            "12 min",
            """# Downstream processing (separation and purification)

When fermentation ends you have a dilute, complex **broth**: the target
product mixed with cells, unused medium, and many other molecules.
**Downstream processing (DSP)** recovers and purifies it. DSP often
dominates the cost of a product - especially for a high-purity
therapeutic protein - so it is engineered as carefully as the
fermentation.

A typical DSP train has four stages:

1. **Removal of insolubles** - separate cells from liquid by
   **centrifugation** or **microfiltration**. If the product is *inside*
   the cells (intracellular), first **lyse** them (homogenizer, bead mill)
   to release it, then clarify.
2. **Isolation / concentration** - crude concentration and buffer
   exchange: **ultrafiltration**, **precipitation** (e.g. ammonium
   sulfate), or **extraction**.
3. **Purification** - high-resolution separation, usually
   **chromatography** exploiting a molecular property: **ion-exchange**
   (charge), **hydrophobic-interaction**, **size-exclusion**, and highly
   specific **affinity** (e.g. Protein A for antibodies).
4. **Polishing / formulation** - a final chromatography step, then
   **sterile filtration**, concentration and formulation into the final
   dosage form; often **lyophilization** (freeze-drying) for storage.

A quick way to reason about overall recovery is that step yields
**multiply**:

```text
Overall yield = product of the step yields.

Example: four steps at 90 percent each
  Y = 0.90 * 0.90 * 0.90 * 0.90 = 0.656  (about 66 percent)

Lesson: every extra step costs yield, so use as few, high-yield steps as
possible. Ten steps at 90 percent each keep only 0.9^10 = 35 percent.
```

```mermaid
graph LR
    BROTH["Harvest broth"] --> SEP["Cell separation"]
    SEP --> CONC["Concentration UF"]
    CONC --> CHROM["Chromatography purify"]
    CHROM --> POLISH["Polishing and formulation"]
    POLISH --> DRY["Sterile fill or freeze dry"]
    DRY --> PRODUCT["Purified product"]
```

Remember: DSP goes solids-out, then concentrate, then purify (usually by
chromatography), then polish and formulate - and because step yields
multiply, fewer high-yield steps beat many mediocre ones.
""",
        ),
        quiz_lesson(
            "Quiz: Downstream processing (separation and purification)",
            (
                q(
                    "What is the first job of a typical downstream processing train?",
                    (
                        opt("Freeze-drying the final product"),
                        opt(
                            "Removing insolubles - separating cells from liquid by "
                            "centrifugation or microfiltration",
                            correct=True,
                        ),
                        opt("Running the fermentation"),
                        opt("Selling the product"),
                    ),
                    "DSP starts by clarifying the broth - removing cells and debris - "
                    "before concentration and purification.",
                ),
                q(
                    "Four purification steps each recover 90 percent of the product. "
                    "The overall yield is about:",
                    (
                        opt("About 90 percent"),
                        opt("About 66 percent", correct=True),
                        opt("About 100 percent"),
                        opt("About 10 percent"),
                    ),
                    "Step yields multiply: 0.9^4 = 0.656, roughly 66 percent - so "
                    "each extra step costs yield.",
                ),
                q(
                    "Which technique gives the highest-resolution, most specific "
                    "purification, e.g. Protein A for antibodies?",
                    (
                        opt("Centrifugation"),
                        opt("Affinity chromatography", correct=True),
                        opt("Sparging"),
                        opt("Sterilization"),
                    ),
                    "Affinity chromatography exploits a highly specific interaction "
                    "(like Protein A binding antibodies) for high selectivity.",
                ),
            ),
        ),
        # -- 7. Fermentation scale-up ----------------------------------
        _t(
            "Fermentation scale-up",
            "11 min",
            """# Fermentation scale-up

A process that works in a 1 L bench reactor must eventually run in a
10,000 L (or larger) production tank. **Scale-up** is hard because you
**cannot keep every variable constant at once** - the geometry and physics
change with size. As a tank gets bigger, its volume grows with the cube of
diameter but its surface area only with the square, so heat removal,
mixing time and oxygen transfer all get relatively harder.

The core problem: you have several candidate **scale-up criteria** and
they conflict.

- **Constant power per unit volume (P/V)** - the most common criterion for
  aerobic cultures, because it roughly preserves **kLa** and oxygen
  transfer.
- **Constant impeller tip speed** - preserves the maximum **shear**;
  chosen for fragile mammalian or mycelial cells.
- **Constant mixing time** - keeps the broth homogeneous, but is usually
  impossible to hold at large scale (mixing time grows with size).
- **Constant Reynolds number** - rarely practical.

You pick the criterion that matters most for your organism and accept that
the others drift. Keeping **geometric similarity** (same shape ratios)
makes the translation more predictable.

```text
Impeller power and tip speed:

  Ungassed power:   P = Np * rho * N^3 * D^5
      Np = power number, rho = density,
      N  = impeller speed (rev/s), D = impeller diameter

  Tip speed:        v_tip = pi * N * D

Constant P/V scale-up (geometrically similar, subscript 1 = small,
2 = large):

  N2 = N1 * (D1 / D2)^(2/3)

Example: N1 = 400 rpm, D1 = 0.1 m, scaling to D2 = 1.0 m
  N2 = 400 * (0.1/1.0)^(2/3) = 400 * 0.215 = 86 rpm
  The big tank turns much slower, yet keeps similar P/V.
```

```mermaid
graph LR
    LAB["Bench 1 L"] --> PILOT["Pilot 100 L"]
    PILOT --> PROD["Production 10000 L"]
    CRIT["Pick scale-up criterion"] --> PV["Constant P per V"]
    CRIT --> TIP["Constant tip speed"]
    PV --> PROD
    TIP --> PROD
```

Remember: you cannot hold everything constant when you scale up - choose
the criterion that governs your process (usually constant P/V to preserve
oxygen transfer) and keep geometric similarity so the translation is
predictable.
""",
        ),
        quiz_lesson(
            "Quiz: Fermentation scale-up",
            (
                q(
                    "Why can you not hold every variable constant when scaling up a fermenter?",
                    (
                        opt("Because larger tanks use no power"),
                        opt(
                            "Geometry and physics change with size - volume grows "
                            "faster than area - so the scale-up criteria conflict",
                            correct=True,
                        ),
                        opt("Because the organism changes species"),
                        opt("Because sterilization becomes unnecessary"),
                    ),
                    "As size grows, heat transfer, mixing and oxygen transfer scale "
                    "differently, so criteria like P/V, tip speed and mixing time "
                    "cannot all be held.",
                ),
                q(
                    "Which scale-up criterion is most common for aerobic cultures, "
                    "because it roughly preserves oxygen transfer?",
                    (
                        opt("Constant mixing time"),
                        opt("Constant power per unit volume (P/V)", correct=True),
                        opt("Constant tank color"),
                        opt("Constant number of baffles"),
                    ),
                    "Constant P/V roughly preserves kLa and thus oxygen transfer, "
                    "the usual limiting factor.",
                ),
                q(
                    "Which criterion is chosen to protect shear-sensitive cells?",
                    (
                        opt("Constant impeller tip speed", correct=True),
                        opt("Constant Reynolds number"),
                        opt("Maximum possible stirrer speed"),
                        opt("Constant medium cost"),
                    ),
                    "Tip speed sets the maximum shear, so holding it constant "
                    "protects fragile mammalian or mycelial cells.",
                ),
            ),
        ),
        # -- 8. Bioprocesses for pharma, food and biofuels -------------
        _t(
            "Bioprocesses for pharma, food and biofuels",
            "12 min",
            """# Bioprocesses for pharma, food and biofuels

The same toolkit - a healthy organism, a controlled reactor, oxygen
transfer, sterility and downstream purification - serves very different
industries, each with its own priorities.

**Pharmaceutical bioprocessing** makes antibiotics, vaccines, and
**biologics** (therapeutic proteins and monoclonal antibodies, often from
CHO cells). Here **purity, safety and consistency** dominate. Production
runs under **GMP** (Good Manufacturing Practice) with validated steps,
extensive documentation, and quality built in by design - the modern
**QbD (Quality by Design)** and **PAT (Process Analytical Technology)**
approaches follow **ICH** guidelines. Value per gram is high, so complex
multi-step DSP is justified.

**Food and beverage bioprocessing** is the oldest: **brewing and wine**
(yeast fermenting sugar to ethanol and CO2), **baking**, **dairy** (lactic
acid bacteria for yoghurt and cheese), and food ingredients (citric acid,
amino acids like glutamate, enzymes, single-cell protein). Priorities are
**flavor, safety, food-grade materials and cost**.

**Biofuels** turn biomass into energy carriers: **bioethanol** (yeast
fermenting sugars from corn or sugarcane; **cellulosic** ethanol from
pretreated and enzyme-hydrolyzed plant fibre), **biodiesel**
(transesterification of oils, sometimes enzyme-catalyzed), and **biogas**
(anaerobic digestion to methane). Here the product is cheap, so
**feedstock cost, yield and energy balance** decide viability.

The **stoichiometry** of ethanol fermentation is a useful anchor:

```text
Alcoholic fermentation (Gay-Lussac):

  C6H12O6  ->  2 C2H5OH  +  2 CO2
  glucose      ethanol       carbon dioxide

Mass basis (molar masses g/mol):
  glucose 180,  ethanol 2 x 46 = 92,  CO2 2 x 44 = 88

Theoretical yield of ethanol:
  92 / 180 = 0.511 g ethanol per g glucose

Real yields reach about 90 to 93 percent of this because some sugar goes
to yeast biomass and byproducts. From 1000 kg glucose:
  ideal  = 511 kg ethanol;  at 92 percent = 470 kg ethanol.
```

```mermaid
graph TD
    ORG["Organism and reactor"] --> PHARMA["Pharma GMP biologics"]
    ORG --> FOOD["Food brewing dairy"]
    ORG --> FUEL["Biofuels ethanol biogas"]
    PHARMA --> PURITY["Purity and safety"]
    FOOD --> FLAVOR["Flavor and cost"]
    FUEL --> ENERGY["Feedstock and energy balance"]
```

Remember: one bioprocess toolkit, three worlds - pharma optimizes for
purity and GMP compliance, food for flavor, safety and cost, biofuels for
feedstock cost and energy balance.
""",
        ),
        quiz_lesson(
            "Quiz: Bioprocesses for pharma, food and biofuels",
            (
                q(
                    "The theoretical mass yield of ethanol from glucose "
                    "(C6H12O6 -> 2 C2H5OH + 2 CO2) is about:",
                    (
                        opt("About 0.25 g/g"),
                        opt("About 0.51 g/g", correct=True),
                        opt("About 1.0 g/g"),
                        opt("About 2.0 g/g"),
                    ),
                    "92 g ethanol per 180 g glucose = 0.511 g/g; real yields reach "
                    "about 90 to 93 percent of this.",
                ),
                q(
                    "What dominates the design of pharmaceutical bioprocessing?",
                    (
                        opt("Making the product as cheap as possible above all"),
                        opt(
                            "Purity, safety and consistency under GMP, with validated "
                            "steps and quality built in by design",
                            correct=True,
                        ),
                        opt("Maximizing CO2 output"),
                        opt("Avoiding any documentation"),
                    ),
                    "Pharma runs under GMP with QbD/PAT and ICH guidance; purity, "
                    "safety and consistency come first.",
                ),
                q(
                    "For biofuels, which factors most decide commercial viability?",
                    (
                        opt("The color and smell of the fuel"),
                        opt(
                            "Feedstock cost, yield and the overall energy balance, "
                            "because the product is cheap",
                            correct=True,
                        ),
                        opt("The brand name of the reactor"),
                        opt("The number of chromatography steps"),
                    ),
                    "Low-value products like fuels live or die on feedstock cost, "
                    "yield and net energy balance.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is bioprocess engineering?",
                    (
                        opt("Only the study of enzymes in test tubes"),
                        opt(
                            "Chemical engineering applied to living catalysts - "
                            "designing and operating processes that use cells or "
                            "enzymes to make products",
                            correct=True,
                        ),
                        opt("A branch of electrical engineering"),
                        opt("The design of distillation columns only"),
                    ),
                    "It applies balances, kinetics and transport to a living "
                    "catalyst that grows, respires and can be contaminated.",
                ),
                q(
                    "The Monod equation mu = mu_max * S / (Ks + S) describes:",
                    (
                        opt("Heat loss from the reactor jacket"),
                        opt(
                            "How the specific growth rate depends on the limiting "
                            "substrate, saturating at mu_max",
                            correct=True,
                        ),
                        opt("The freeze-drying rate"),
                        opt("The cost of chromatography"),
                    ),
                    "Monod links growth rate to substrate; it mirrors Michaelis-"
                    "Menten enzyme kinetics.",
                ),
                q(
                    "A chemostat reaches steady state when:",
                    (
                        opt("The stirrer stops"),
                        opt(
                            "The specific growth rate equals the dilution rate, "
                            "mu = D = F/V (below washout)",
                            correct=True,
                        ),
                        opt("All the cells die"),
                        opt("The temperature reaches 121 C"),
                    ),
                    "Continuous culture holds mu = D at steady state; if D exceeds "
                    "mu_max the culture washes out.",
                ),
                q(
                    "In OTR = kLa * (C_star - C_L), oxygen transfer is limited largely because:",
                    (
                        opt("Oxygen is too soluble in water"),
                        opt(
                            "Oxygen is only sparingly soluble, so the driving force "
                            "(C_star - C_L) is small and kLa must be made large",
                            correct=True,
                        ),
                        opt("Cells produce their own oxygen"),
                        opt("The probe cannot read oxygen"),
                    ),
                    "Low solubility keeps the driving force small; the engineer "
                    "raises kLa via aeration and agitation to meet demand.",
                ),
                q(
                    "A culture needs OUR = 100 mmol/(L.h) with C_star = 0.25 and "
                    "C_L held at 0.05 mmol/L. The required kLa is:",
                    (
                        opt("About 20 per hour"),
                        opt("About 500 per hour", correct=True),
                        opt("About 100 per hour"),
                        opt("About 2000 per hour"),
                    ),
                    "kLa = OUR/(C_star - C_L) = 100/0.20 = 500 per hour.",
                ),
                q(
                    "Why is high-temperature short-time (HTST) sterilization used for medium?",
                    (
                        opt("It is the only method that works"),
                        opt(
                            "Spore death rate rises with temperature faster than "
                            "nutrient destruction, so it kills spores while sparing "
                            "the medium",
                            correct=True,
                        ),
                        opt("It cools the medium below freezing"),
                        opt("It removes the need to inoculate"),
                    ),
                    "The high activation energy of spore death makes hot-and-fast "
                    "selective for killing over nutrient loss.",
                ),
                q(
                    "In downstream processing, why do fewer high-yield steps beat "
                    "many mediocre ones?",
                    (
                        opt("Because steps have no effect on yield"),
                        opt(
                            "Step yields multiply, so each extra step multiplies the "
                            "overall recovery down",
                            correct=True,
                        ),
                        opt("Because more steps are always sterile"),
                        opt("Because chromatography is free"),
                    ),
                    "Overall yield is the product of step yields; 0.9^10 keeps only "
                    "35 percent, so minimize the number of steps.",
                ),
                q(
                    "Which downstream technique offers the most specific "
                    "purification of an antibody?",
                    (
                        opt("Sparging"),
                        opt("Protein A affinity chromatography", correct=True),
                        opt("Sterilization"),
                        opt("Sedimentation by gravity alone"),
                    ),
                    "Affinity chromatography (Protein A binding antibodies) gives "
                    "very high, specific selectivity.",
                ),
                q(
                    "When scaling up an aerobic fermentation, the most common criterion is:",
                    (
                        opt("Constant mixing time"),
                        opt(
                            "Constant power per unit volume (P/V), to roughly "
                            "preserve oxygen transfer",
                            correct=True,
                        ),
                        opt("Constant Reynolds number"),
                        opt("Maximum shear at all costs"),
                    ),
                    "Constant P/V roughly preserves kLa; tip speed is chosen instead "
                    "when protecting shear-sensitive cells.",
                ),
                q(
                    "The theoretical ethanol yield from glucose is 0.51 g/g; real "
                    "fermentation reaches about 90 to 93 percent of it because:",
                    (
                        opt("The equation is wrong"),
                        opt(
                            "Some sugar is diverted to yeast biomass and byproducts "
                            "rather than ethanol",
                            correct=True,
                        ),
                        opt("The ethanol evaporates completely"),
                        opt("Glucose weighs more than ethanol per mole only"),
                    ),
                    "Not all substrate becomes product - biomass and byproducts take "
                    "a share, so real yield is below the 0.51 g/g theoretical.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

BIOPROCESS_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_BIOPROCESS_ENGINEERING,)
