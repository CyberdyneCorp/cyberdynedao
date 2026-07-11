"""Academy seed content - Pharmaceutical Engineering.

Manufacturing medicines at quality and scale. The course walks the drug
product lifecycle, then goes deep on the unit operations and quality
systems that turn a molecule into a released dose: active pharmaceutical
ingredient synthesis, crystallization and particle engineering, solid
dosage form manufacturing, GMP and ICH, Quality by Design and process
analytical technology, continuous manufacturing, and sterile and
biologics production. Every lesson is a direct explanation with a mermaid
diagram and a worked example - a process, a spec table, or a calculation -
followed by a checkpoint quiz, closing with a comprehensive final quiz.
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


_PHARMACEUTICAL_ENGINEERING = SeedCourse(
    slug="pharmaceutical-engineering",
    title="Pharmaceutical Engineering",
    description=(
        "Manufacturing medicines at quality and scale: API synthesis and "
        "crystallization, solid dosage forms, GMP and ICH, Quality by Design "
        "and PAT, and continuous and biologics manufacturing - with worked "
        "mass balances, spec tables, calculations and a diagram in every "
        "lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Pharmaceutical Engineering

Making a medicine is not one process - it is a chain of them, each held to
a standard far stricter than ordinary chemical manufacturing, because the
product ends up inside a patient. A tablet that is 5 percent off target
potency, or contaminated with the wrong particle, is not a quality defect;
it is a safety event. Pharmaceutical engineering is the discipline of
turning a molecule into a safe, effective, reproducible dose - at scale,
under a quality system, provably.

The approach here is **concrete**: every lesson explains one part of the
chain directly, shows it in a short real example (a process flow, a
specification table, or a worked calculation), and draws it as a diagram.
After each lesson there is a short quiz; at the end, a final quiz covers
the whole course.

What you will build understanding for, in order:

1. **The drug product lifecycle** - discovery to commercial supply
2. **API manufacturing** - synthesizing the active molecule
3. **Crystallization and particle engineering** - isolating a pure solid
4. **Solid dosage form manufacturing** - making tablets and capsules
5. **GMP and ICH** - the quality system and its global standards
6. **Quality by Design and PAT** - building quality in, measuring in line
7. **Continuous manufacturing** - end to end, without stopping
8. **Sterile and biologics manufacturing** - injectables and living systems

The thread through all of it: **quality is designed and built in, not
tested in at the end**. Keep that in mind and each lesson connects to the
last.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What makes pharmaceutical manufacturing stricter than ordinary "
                    "chemical manufacturing?",
                    (
                        opt("The reactions are always more exothermic"),
                        opt(
                            "The product ends up inside a patient, so a quality defect is "
                            "a potential safety event and must be provably controlled",
                            correct=True,
                        ),
                        opt("Pharmaceutical plants are always larger"),
                        opt("It uses only continuous processes"),
                    ),
                    "The patient-safety consequence is why a quality system and standards "
                    "sit over every step.",
                ),
                q(
                    "What is the central theme the course keeps returning to?",
                    (
                        opt("Quality is tested into the product at final release"),
                        opt("The cheapest route always wins"),
                        opt(
                            "Quality is designed and built into the process, not tested "
                            "in at the end",
                            correct=True,
                        ),
                        opt("Manual operation is preferred for flexibility"),
                    ),
                    "Build quality in - this is the idea behind GMP, QbD and PAT alike.",
                ),
            ),
        ),
        # -- 1. Drug product lifecycle ---------------------------------
        _t(
            "The drug product lifecycle",
            "9 min",
            """# The drug product lifecycle

A medicine passes through a long, regulated lifecycle before it reaches a
pharmacy shelf, and engineering shows up at every stage. Understanding the
whole arc tells you *why* a manufacturing decision made in early
development constrains commercial supply years later.

The major stages:

- **Discovery** - a candidate molecule is identified and shown to hit a
  biological target. Chemists make milligrams.
- **Preclinical** - safety and pharmacology in cells and animals; the
  first real synthesis route is developed.
- **Clinical (Phase 1/2/3)** - dosing in humans, from a few volunteers to
  thousands of patients. Manufacturing must scale from grams to kilograms,
  under GMP, while the process is still changing.
- **Registration** - the dossier (in the **ICH Common Technical Document**
  format) is filed. Module 3 describes the whole manufacturing process and
  controls; this is where the **regulatory filing locks the process**.
- **Commercial manufacturing** - routine production, release testing,
  batch after batch, held to the filed process for the product's life.
- **Lifecycle management** - post-approval changes, tech transfer to new
  sites, and eventual withdrawal.

The engineering tension is **scale-up**: a route that works in a 1 L
round-bottom flask may be unsafe or impossible in a 6000 L reactor
(heat removal, mixing, filtration times all change with scale). Decisions
must anticipate the commercial scale early.

```mermaid
graph LR
    DISC["Discovery"] --> PRE["Preclinical"]
    PRE --> CLIN["Clinical trials"]
    CLIN --> REG["Registration filing"]
    REG --> COMM["Commercial manufacturing"]
    COMM --> LCM["Lifecycle management"]
```

A tablet has two halves that run in parallel and converge: the **drug
substance** (the API - the active molecule) and the **drug product** (the
final dosage form - tablet, capsule, injection) that carries it.

```text
Cost and risk grow through the lifecycle (illustrative):

Stage           Typical scale        Attrition risk    GMP required
Discovery       milligrams           very high         no
Preclinical     grams                high              no
Phase 1         100s of grams        high              yes
Phase 3         kilograms            moderate           yes
Commercial      100s of kilograms    low               yes
```

Remember: manufacturing decisions are cheap to change early and expensive
to change once the process is filed - design for the commercial scale from
the start.
""",
        ),
        quiz_lesson(
            "Quiz: The drug product lifecycle",
            (
                q(
                    "At which stage is the manufacturing process effectively locked by "
                    "the regulatory dossier?",
                    (
                        opt("Discovery"),
                        opt("Preclinical"),
                        opt(
                            "Registration filing - Module 3 of the ICH CTD describes the "
                            "process and controls the product is then held to",
                            correct=True,
                        ),
                        opt("It is never locked"),
                    ),
                    "Post-approval changes to a filed process require regulatory work, so "
                    "the filing is a commitment.",
                ),
                q(
                    "What is the difference between the drug substance and the drug product?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "The drug substance is the active molecule (API); the drug "
                            "product is the final dosage form that delivers it",
                            correct=True,
                        ),
                        opt("The drug substance is the tablet; the drug product is the box"),
                        opt("The drug product contains no active ingredient"),
                    ),
                    "API (substance) is made, then formulated into a tablet or injection "
                    "(product).",
                ),
                q(
                    "Why must commercial scale be anticipated early in development?",
                    (
                        opt("Regulators forbid small-scale work"),
                        opt(
                            "Heat removal, mixing and filtration behave differently at "
                            "large scale, so a route that works in a flask may fail or be "
                            "unsafe in a large reactor",
                            correct=True,
                        ),
                        opt("Large reactors are cheaper to run at any scale"),
                        opt("Small scale always gives lower yield"),
                    ),
                    "Scale-up changes the physics; designing for the final scale avoids "
                    "expensive late redesign.",
                ),
            ),
        ),
        # -- 2. API manufacturing --------------------------------------
        _t(
            "Active pharmaceutical ingredient (API) manufacturing",
            "11 min",
            """# Active pharmaceutical ingredient (API) manufacturing

The **active pharmaceutical ingredient (API)**, or **drug substance**, is
the molecule that produces the therapeutic effect. Making it - **primary
manufacturing** - is essentially applied synthetic organic chemistry run
under GMP: a sequence of reaction, work-up, and isolation steps that build
the molecule and then purify it to a defined quality.

A synthesis **route** is a series of steps from cheap starting materials
to the API. Each step typically has:

- **Reaction** - combine reagents in a solvent under controlled
  temperature, often in a jacketed **batch reactor**.
- **Work-up** - quench, extract, wash to remove reagents and by-products.
- **Isolation** - usually **crystallization** (next lesson) to get a pure
  solid, then filtration and drying.

The stakes are **impurity control**. Regulators (ICH Q3A for the drug
substance, and especially ICH M7 for **mutagenic impurities**) require
that impurities be identified and controlled to tiny limits. A late step
that generates a genotoxic impurity can sink a route.

```mermaid
graph LR
    SM["Starting material"] --> RXN["Reaction step"]
    RXN --> WORK["Work-up and extraction"]
    WORK --> CRYST["Crystallization"]
    CRYST --> ISO["Filter and dry"]
    ISO --> NEXT["Next step or final API"]
```

Two engineering ideas dominate route design:

- **Convergent over linear** - build two fragments in parallel and join
  them late, rather than one long chain. A linear route loses yield
  multiplicatively; a convergent one protects your most valuable
  intermediates.
- **Process safety** - many reactions are highly exothermic. Reaction
  calorimetry and **runaway** analysis are mandatory before scale-up.

Yield compounds step by step. For a linear route, overall yield is the
product of the step yields:

```text
Overall yield = y1 x y2 x y3 x ... x yn

Example: a 5-step linear route, each step 85 percent yield
  Overall = 0.85^5 = 0.4437 -> about 44 percent

Same 5 steps but convergent (two 2-step arms + 1 coupling), each 85 percent:
  Longest path is 3 steps -> 0.85^3 = 0.614 -> about 61 percent
  More of the expensive late-stage material survives.
```

Remember: an API route is judged not just on whether it works, but on
yield, purity, safety, cost, and whether every impurity can be controlled
to a proven limit.
""",
        ),
        quiz_lesson(
            "Quiz: Active pharmaceutical ingredient (API) manufacturing",
            (
                q(
                    "What is an API (drug substance)?",
                    (
                        opt("The coating on a tablet"),
                        opt(
                            "The molecule that produces the therapeutic effect, made by "
                            "synthesis under GMP",
                            correct=True,
                        ),
                        opt("The container the medicine ships in"),
                        opt("A filler added to bulk out a tablet"),
                    ),
                    "API = the active molecule; primary manufacturing is applied "
                    "synthetic chemistry under GMP.",
                ),
                q(
                    "Why is a convergent synthesis route usually preferred over a long linear one?",
                    (
                        opt("It uses more steps, which regulators prefer"),
                        opt(
                            "Yield multiplies across steps, so joining fragments late "
                            "protects the most valuable intermediates and gives higher "
                            "overall yield",
                            correct=True,
                        ),
                        opt("Linear routes cannot be run under GMP"),
                        opt("Convergent routes never produce impurities"),
                    ),
                    "Overall yield is the product of step yields; a shorter longest-path "
                    "keeps expensive late material.",
                ),
                q(
                    "Which ICH guideline specifically governs mutagenic (genotoxic) "
                    "impurities in a drug substance?",
                    (
                        opt("ICH Q10"),
                        opt("ICH M7", correct=True),
                        opt("ICH E6"),
                        opt("ICH Q1A"),
                    ),
                    "ICH M7 addresses assessment and control of DNA-reactive (mutagenic) "
                    "impurities; Q3A covers impurities in new drug substances generally.",
                ),
            ),
        ),
        # -- 3. Crystallization and particle engineering ---------------
        _t(
            "Crystallization and particle engineering",
            "11 min",
            """# Crystallization and particle engineering

**Crystallization** is how most APIs are purified and isolated as a solid.
It is the single most important unit operation in drug substance
manufacturing, because it sets not only purity but the **solid-state
properties** that control how the final medicine behaves: particle size,
shape, and **polymorphic form**.

The driving force is **supersaturation** - a solution holding more solute
than its equilibrium solubility. You create it by cooling, by evaporating
solvent, or by adding an **antisolvent** in which the API is poorly
soluble. Supersaturated solution then does two things:

- **Nucleation** - new crystals form (spontaneously, or seeded).
- **Growth** - existing crystals get larger.

The balance between them sets the particle size distribution. Too much
uncontrolled nucleation gives fine, hard-to-filter powder; controlled
growth from **seed** crystals gives larger, uniform particles.

```mermaid
graph TD
    SOL["Solution at equilibrium"] --> SS["Create supersaturation"]
    SS --> NUC["Nucleation new crystals"]
    SS --> GRO["Growth of crystals"]
    NUC --> PSD["Particle size distribution"]
    GRO --> PSD
    PSD --> FILT["Filter and dry"]
```

**Polymorphism** is the ability of the same molecule to pack into
different crystal lattices. Different polymorphs can have different
solubility, dissolution rate, stability, and bioavailability - so the
**wrong form can change how the drug works**. The infamous case is
ritonavir, where a more stable, less soluble form appeared and disrupted
supply. You must identify and reliably produce the intended form.

**Particle engineering** matters downstream: particle size affects
dissolution (and therefore bioavailability), flow, and content uniformity
in a tablet. If crystallization cannot deliver the target size, **milling**
(reducing size) or **granulation** (building it up) follows.

A simple crystallization yield from a solubility curve:

```text
Cool crystallization mass balance (single component, ideal):

  Solute in solution initially:  C_hot  x  V   (g)
  Solute remaining dissolved:    C_cold x  V   (g)
  Crystal yield  =  (C_hot - C_cold) x V

Example:
  V = 100 L, solubility at 60 C = 250 g/L, at 5 C = 40 g/L
  Yield = (250 - 40) g/L x 100 L = 21000 g = 21.0 kg of crystals
  Recovery = (250 - 40) / 250 = 84 percent
```

Remember: crystallization is not just purification - it is where you
engineer purity, particle size, and the polymorphic form that determines
whether the medicine performs as designed.
""",
        ),
        quiz_lesson(
            "Quiz: Crystallization and particle engineering",
            (
                q(
                    "What is the driving force for crystallization?",
                    (
                        opt("High temperature alone"),
                        opt(
                            "Supersaturation - a solution holding more solute than its "
                            "equilibrium solubility",
                            correct=True,
                        ),
                        opt("Mechanical stirring alone"),
                        opt("Adding more of the same solvent"),
                    ),
                    "Supersaturation (from cooling, evaporation or antisolvent) drives "
                    "nucleation and growth.",
                ),
                q(
                    "Why does polymorphism matter for a drug product?",
                    (
                        opt("It only changes the crystal color"),
                        opt(
                            "Different crystal forms can have different solubility, "
                            "dissolution and stability, which can change bioavailability "
                            "and how the drug performs",
                            correct=True,
                        ),
                        opt("It has no effect once the tablet is made"),
                        opt("It changes the molecular formula of the API"),
                    ),
                    "Same molecule, different lattice - the ritonavir case showed how a "
                    "new, less soluble form can disrupt a product.",
                ),
                q(
                    "In a cooling crystallization, 100 L of solution goes from 250 g/L "
                    "solubility (hot) to 50 g/L (cold). Roughly how much crystal is "
                    "recovered?",
                    (
                        opt("5 kg"),
                        opt("20 kg", correct=True),
                        opt("25 kg"),
                        opt("50 kg"),
                    ),
                    "Yield = (250 - 50) g/L x 100 L = 20000 g = 20 kg.",
                ),
            ),
        ),
        # -- 4. Solid dosage form manufacturing ------------------------
        _t(
            "Solid dosage form manufacturing",
            "11 min",
            """# Solid dosage form manufacturing

Most medicines are **oral solid dosage forms** - tablets and capsules -
because they are stable, cheap, precise, and easy for patients to take.
Turning a fine API powder into a robust tablet is **secondary
manufacturing**, and it is a materials-handling problem as much as a
chemical one.

A tablet is mostly **excipients** - inactive ingredients that each do a
job:

- **Filler / diluent** (e.g. lactose, microcrystalline cellulose) - bulk
  the tablet to a usable size.
- **Binder** - hold the granule together.
- **Disintegrant** - make the tablet break apart in the gut so the API
  can dissolve.
- **Lubricant** (e.g. magnesium stearate) - stop powder sticking to the
  press.
- **Glidant** - improve powder flow.

The core challenge is **blend uniformity and flow**: every tablet must
contain the right dose (**content uniformity**), which means the API must
be evenly distributed in a powder that flows consistently into the tablet
press. Fine, cohesive API powders flow badly and segregate - so we often
**granulate** first, building small particles into larger, free-flowing,
uniform granules.

The two main routes:

```mermaid
graph TD
    API["API plus excipients"] --> ROUTE{"Powder flows and compresses well"}
    ROUTE -->|"yes"| DC["Direct compression"]
    ROUTE -->|"no"| GRAN["Granulate"]
    GRAN --> WET["Wet granulation add liquid"]
    GRAN --> DRY["Dry granulation roller compaction"]
    WET --> BLEND["Blend with lubricant"]
    DRY --> BLEND
    DC --> BLEND
    BLEND --> PRESS["Tablet press compression"]
    PRESS --> COAT["Film coating optional"]
```

- **Direct compression** - blend the powders and press. Simplest, but
  needs materials that already flow and compress well.
- **Wet granulation** - add a binder liquid, form granules, dry, mill.
  Robust for poorly-flowing or low-dose APIs.
- **Dry granulation (roller compaction)** - compact into ribbons, mill
  into granules. For moisture- or heat-sensitive materials.

Then **compression** on a rotary press, and optional **film coating**.

Dose and content uniformity are the acceptance gate. A worked dose check:

```text
Tablet potency and uniformity:

  Target dose             = 200 mg API per tablet
  Blend assay             = 40.0 mg API per 100 mg blend  (40.0 percent w/w)
  Tablet target weight    = 200 / 0.40 = 500 mg

  Content uniformity (USP): sample 10 tablets, each 85 to 115 percent of
  label claim, and acceptance value (AV) <= 15.0.
  A tablet assaying 180 mg = 180/200 = 90 percent -> within 85 to 115.
```

Remember: a tablet is engineered particles and excipients pressed into a
dose - flow, blend uniformity, and disintegration decide whether it
delivers the API correctly.
""",
        ),
        quiz_lesson(
            "Quiz: Solid dosage form manufacturing",
            (
                q(
                    "What is the role of a disintegrant in a tablet?",
                    (
                        opt("To lubricate the tablet press"),
                        opt(
                            "To make the tablet break apart in the gut so the API can dissolve",
                            correct=True,
                        ),
                        opt("To add therapeutic effect"),
                        opt("To color the tablet"),
                    ),
                    "Disintegrants swell or wick water to break the tablet up; lubricants "
                    "(e.g. magnesium stearate) prevent sticking.",
                ),
                q(
                    "Why is a poorly-flowing, low-dose API often granulated before compression?",
                    (
                        opt("Granulation removes the API"),
                        opt(
                            "Granulation builds fine cohesive powder into larger, "
                            "free-flowing, uniform granules, improving flow and content "
                            "uniformity",
                            correct=True,
                        ),
                        opt("It is required for every tablet by law"),
                        opt("It makes the tablet dissolve more slowly"),
                    ),
                    "Good flow and even API distribution are what let every tablet carry "
                    "the correct dose.",
                ),
                q(
                    "A blend assays 25 percent API by weight and the target dose is "
                    "100 mg. What tablet weight delivers the dose?",
                    (
                        opt("125 mg"),
                        opt("250 mg"),
                        opt("400 mg", correct=True),
                        opt("100 mg"),
                    ),
                    "Weight = dose / fraction = 100 mg / 0.25 = 400 mg.",
                ),
            ),
        ),
        # -- 5. GMP and ICH --------------------------------------------
        _t(
            "Good Manufacturing Practice (GMP) and ICH",
            "10 min",
            """# Good Manufacturing Practice (GMP) and ICH

Making the right molecule is not enough - you must **prove** you made it
correctly, every time. **Good Manufacturing Practice (GMP)** is the body
of regulation that ensures medicines are consistently produced and
controlled to quality standards. It is enforced by agencies (FDA, EMA and
others) and is the legal condition for selling a medicine.

GMP is often summarized by principles - the essence:

- **Written procedures** - everything is done to an approved procedure
  (an SOP or batch record).
- **Records prove it happened** - "if it is not documented, it did not
  happen." A **batch record** captures who did what, when, with which
  materials and equipment.
- **Validation** - processes, equipment and cleaning are validated to show
  they reliably do what they should before routine use.
- **Traceability** - every material is identified and traceable; every
  batch can be traced forward and back.
- **Quality unit independence** - an independent quality function releases
  (or rejects) each batch; the people who make it do not sign off on it
  alone.
- **Data integrity** - records must be **ALCOA**: Attributable, Legible,
  Contemporaneous, Original, Accurate.

```mermaid
graph TD
    SOP["Approved procedures SOPs"] --> MFG["Manufacture to the procedure"]
    MFG --> REC["Batch record captures everything"]
    REC --> QC["QC testing against specifications"]
    QC --> QA["Independent quality review"]
    QA --> REL{"Meets all specifications"}
    REL -->|"yes"| SHIP["Release batch"]
    REL -->|"no"| REJ["Reject or investigate"]
```

Above national GMP sits **ICH** - the International Council for
Harmonisation - which writes harmonized technical guidelines so a common
standard applies across regions. The quality (Q) series is core:

```text
Key ICH quality guidelines:

  Q1A/Q1B    Stability testing (shelf life, conditions)
  Q2         Analytical procedure validation
  Q3A/Q3B    Impurities in drug substance / drug product
  Q6A        Specifications - tests and acceptance criteria
  Q7         GMP for active pharmaceutical ingredients
  Q8         Pharmaceutical development (Quality by Design)
  Q9         Quality risk management
  Q10        Pharmaceutical quality system
  Q13        Continuous manufacturing
```

Remember: GMP turns "we made a good batch" into "we can prove every batch
is good" - through procedures, records, validation, and an independent
quality unit; ICH harmonizes the standard globally.
""",
        ),
        quiz_lesson(
            "Quiz: Good Manufacturing Practice (GMP) and ICH",
            (
                q(
                    "What is the core idea captured by 'if it is not documented, it did "
                    "not happen'?",
                    (
                        opt("Documentation is optional if the batch passes testing"),
                        opt(
                            "GMP requires records that prove each step was performed "
                            "correctly - the batch record is the evidence",
                            correct=True,
                        ),
                        opt("Only the final result needs recording"),
                        opt("Operators may reconstruct records later from memory"),
                    ),
                    "Contemporaneous records are the proof of control; data integrity "
                    "(ALCOA) underpins the whole system.",
                ),
                q(
                    "Why must an independent quality unit release each batch?",
                    (
                        opt("To slow down production"),
                        opt(
                            "So the decision to release is separated from the people "
                            "under pressure to produce - an independent check that all "
                            "specifications are met",
                            correct=True,
                        ),
                        opt("Because operators cannot read the specifications"),
                        opt("It is only a formality with no real effect"),
                    ),
                    "Independence of the quality unit is a foundational GMP principle.",
                ),
                q(
                    "Which ICH guideline covers GMP for active pharmaceutical ingredients?",
                    (
                        opt("ICH Q1A"),
                        opt("ICH Q7", correct=True),
                        opt("ICH Q9"),
                        opt("ICH Q13"),
                    ),
                    "Q7 is GMP for APIs; Q9 is quality risk management, Q13 is continuous "
                    "manufacturing.",
                ),
            ),
        ),
        # -- 6. QbD and PAT --------------------------------------------
        _t(
            "Quality by Design and process analytical technology (PAT)",
            "11 min",
            """# Quality by Design and process analytical technology (PAT)

Traditionally, quality was checked by testing finished batches and
rejecting failures. **Quality by Design (QbD)** - formalized in ICH Q8 -
flips this: you **design quality into the process** by understanding how
material and process variables affect the product, then control them.
Testing then confirms what the design already assures.

The QbD vocabulary:

- **Quality Target Product Profile (QTPP)** - what the product must be
  (dose, dissolution, stability) from the patient's view.
- **Critical Quality Attributes (CQAs)** - the properties that must stay
  in range to be safe and effective (e.g. assay, dissolution, impurities).
- **Critical Process Parameters (CPPs)** - the process knobs that affect
  CQAs (e.g. granulation water amount, compression force, drying time).
- **Design Space** - the multidimensional region of CPP settings proven to
  deliver acceptable CQAs. Moving within it is not considered a change.
- **Control Strategy** - how you keep the process in the design space.

```mermaid
graph LR
    QTPP["QTPP patient needs"] --> CQA["Critical quality attributes"]
    CQA --> CPP["Critical process parameters"]
    CPP --> DS["Design space"]
    DS --> CS["Control strategy"]
    CS --> RTR["Real time release option"]
```

**Process Analytical Technology (PAT)** is the toolkit that makes this
real: **measure quality attributes in line, in real time**, rather than
sending samples to a lab hours later. Common PAT sensors are spectroscopic
- **near-infrared (NIR)** and **Raman** - reading blend uniformity,
moisture, or crystal form continuously as the process runs. Feed those
readings to control and you can correct in real time, and ultimately do
**real time release testing (RTRT)** - releasing on in-process data
instead of waiting for end-product lab tests.

A worked design-space acceptance check:

```python
# Predict a critical quality attribute (tablet dissolution, percent at 30 min)
# from two critical process parameters, and test a design-space corner.
def dissolution(compression_kN, granule_water_pct):
    # Illustrative empirical model from designed experiments (DoE):
    return 95.0 - 1.8 * (compression_kN - 10.0) - 2.5 * (granule_water_pct - 30.0)

# CQA acceptance: dissolution must be at least 80 percent at 30 min.
proposed = dissolution(compression_kN=14.0, granule_water_pct=33.0)
print(round(proposed, 1))       # -> 80.3  (just inside the design space)
print(proposed >= 80.0)         # -> True  (acceptable)
```

Remember: QbD understands and controls *why* quality happens; PAT measures
it in line so you can steer the process and, ultimately, release on real
time data.
""",
        ),
        quiz_lesson(
            "Quiz: Quality by Design and process analytical technology (PAT)",
            (
                q(
                    "What is the core shift that Quality by Design represents?",
                    (
                        opt("Testing more finished batches"),
                        opt(
                            "Designing quality into the process by understanding and "
                            "controlling the variables that drive it, rather than testing "
                            "quality in at the end",
                            correct=True,
                        ),
                        opt("Removing all in-process controls"),
                        opt("Filing fewer documents with regulators"),
                    ),
                    "QbD (ICH Q8): build quality in; end testing confirms what the design "
                    "already assures.",
                ),
                q(
                    "In QbD terms, what is a Critical Process Parameter (CPP)?",
                    (
                        opt("A property the patient experiences directly"),
                        opt(
                            "A process variable (e.g. compression force, drying time) "
                            "whose variation affects a Critical Quality Attribute",
                            correct=True,
                        ),
                        opt("The final price of the product"),
                        opt("A regulatory filing deadline"),
                    ),
                    "CPPs are the knobs; CQAs are the product properties they affect; the "
                    "design space links them.",
                ),
                q(
                    "What does Process Analytical Technology (PAT) enable?",
                    (
                        opt("Slower, lab-only end-product testing"),
                        opt(
                            "In-line, real-time measurement of quality attributes (e.g. "
                            "NIR or Raman), enabling real-time control and real time "
                            "release testing",
                            correct=True,
                        ),
                        opt("Elimination of the quality unit"),
                        opt("Manufacturing without any measurement"),
                    ),
                    "PAT sensors read attributes as the process runs, so you steer in "
                    "real time instead of waiting for the lab.",
                ),
            ),
        ),
        # -- 7. Continuous manufacturing -------------------------------
        _t(
            "Continuous manufacturing",
            "10 min",
            """# Continuous manufacturing

Most pharmaceutical manufacturing is **batch**: make a discrete lot, stop,
test, clean, make the next lot. **Continuous manufacturing (CM)** instead
runs material through an integrated line without stopping - powders feed in
one end and tablets come out the other, steadily. ICH **Q13** provides the
regulatory framework, and regulators actively encourage it.

Why it is attractive:

- **Smaller footprint** - a compact line replaces large batch equipment.
- **No scale-up** - you run the *same* line longer to make more; you do
  not redesign for a bigger reactor. This removes the classic scale-up
  risk.
- **Built-in PAT and real-time release** - CM lines are instrumented with
  NIR/Raman throughout, so quality is measured continuously and bad
  material can be **diverted** in real time.
- **Faster and more consistent** - less hold time, fewer manual steps.

A continuous direct-compression tablet line:

```mermaid
graph LR
    FEED["Loss in weight feeders"] --> BLEND["Continuous blender"]
    BLEND --> PAT["In line NIR blend check"]
    PAT --> PRESS["Tablet press"]
    PRESS --> DIV{"In spec"}
    DIV -->|"yes"| GOOD["Collect good tablets"]
    DIV -->|"no"| REJECT["Divert to waste"]
```

Two concepts are central to CM:

- **State of control** - the line runs at a steady state where CQAs stay
  in range; you monitor continuously to confirm it.
- **Residence time distribution (RTD)** - because material flows, a
  disturbance (a bad feeder pulse) spreads over time as it travels down
  the line. The RTD tells you *which* downstream tablets are affected, so
  you can divert exactly those and no more. This is what makes
  material traceability possible without discrete batches.

A simple throughput and diversion calculation:

```text
Continuous line throughput and traceability:

  Line rate            = 25 kg/h of blend
  Tablet weight        = 500 mg = 0.0005 kg
  Tablet output        = 25 / 0.0005 = 50000 tablets/h

  Feeder disturbance lasts 12 s. Mean residence time = 90 s,
  RTD spread means affected material exits over ~60 s.
  Tablets to divert = 50000/h x (60/3600) h = ~833 tablets
  Only those are rejected - the rest of the run continues.
```

Remember: continuous manufacturing removes scale-up, shrinks the plant,
and - through PAT and residence time understanding - lets you monitor and
correct quality in real time, diverting only the affected material.
""",
        ),
        quiz_lesson(
            "Quiz: Continuous manufacturing",
            (
                q(
                    "How does continuous manufacturing largely remove scale-up risk?",
                    (
                        opt("By using much larger reactors"),
                        opt(
                            "You make more by running the same line longer, rather than "
                            "redesigning the process for bigger equipment",
                            correct=True,
                        ),
                        opt("By skipping quality testing"),
                        opt("By using only manual operations"),
                    ),
                    "Same equipment, longer run time - no re-development for a bigger "
                    "scale, which is the classic batch scale-up problem.",
                ),
                q(
                    "What is the role of residence time distribution (RTD) in a continuous line?",
                    (
                        opt("It sets the color of the tablets"),
                        opt(
                            "It describes how a disturbance spreads over time as material "
                            "flows, so you can identify and divert exactly the affected "
                            "downstream material",
                            correct=True,
                        ),
                        opt("It measures the price per tablet"),
                        opt("It has no effect on traceability"),
                    ),
                    "RTD is what makes traceability and precise diversion possible without "
                    "discrete batches.",
                ),
                q(
                    "A continuous line runs at 30 kg/h of blend and each tablet weighs "
                    "600 mg. What is the tablet output per hour?",
                    (
                        opt("18000 tablets/h"),
                        opt("50000 tablets/h", correct=True),
                        opt("30000 tablets/h"),
                        opt("6000 tablets/h"),
                    ),
                    "30 kg/h / 0.0006 kg = 50000 tablets/h.",
                ),
            ),
        ),
        # -- 8. Sterile and biologics manufacturing --------------------
        _t(
            "Sterile and biologics manufacturing",
            "11 min",
            """# Sterile and biologics manufacturing

Some medicines are injected, and some are made by living cells. Both raise
the stakes beyond solid dose: an injectable that bypasses the gut must be
**sterile** and free of pyrogens, and a **biologic** (a protein, antibody,
or vaccine) is a large, fragile molecule made by biology rather than
chemistry.

**Sterile manufacturing** aims for the absence of viable microorganisms.
Two philosophies:

- **Terminal sterilization** - fill the product, then sterilize the sealed
  container (e.g. steam autoclave). Preferred when the product survives it,
  because you sterilize the final unit.
- **Aseptic processing** - sterilize components separately and assemble
  under conditions that keep microbes out, because the product (a protein)
  cannot survive terminal heat. Riskier - it relies on maintaining
  sterility, verified by **media fills** and monitored **cleanroom grades**
  (ISO 14644 / EU GMP Annex 1 Grades A to D).

```text
EU GMP Annex 1 cleanroom grades (particle and activity):

  Grade A   Critical zone - filling, aseptic connections (laminar flow)
  Grade B   Background to Grade A during aseptic processing
  Grade C   Less critical preparation steps
  Grade D   Clean support areas

  Rule: the most critical operation (open product) is in Grade A.
```

**Biologics** are made by **bioprocessing**, split into upstream and
downstream:

- **Upstream** - engineer cells (often CHO mammalian cells) to express the
  protein, grow them in a **bioreactor** (fed with media, controlled for
  pH, dissolved oxygen, temperature) until they secrete the product.
- **Downstream** - **purify** the protein from the messy broth, typically
  by a train of **chromatography** steps (Protein A affinity capture, then
  polishing) plus **viral clearance** and filtration.

```mermaid
graph LR
    CELL["Engineered cell line"] --> BIO["Bioreactor upstream"]
    BIO --> HARV["Harvest and clarify"]
    HARV --> CAP["Protein A capture"]
    CAP --> POL["Polishing chromatography"]
    POL --> VIRAL["Viral clearance and filtration"]
    VIRAL --> FILL["Sterile fill finish"]
```

Because a biologic's identity is inseparable from *how it is made*, the
process defines the product - small changes can alter the molecule's
folding, glycosylation, or activity. This is why a copy is a
**biosimilar**, not a generic: you cannot make an identical copy without
the originator's exact process.

A quick sterility-assurance idea:

```text
Sterility Assurance Level (SAL):

  SAL = probability that a unit is non-sterile after processing.
  Standard target for terminal sterilization: SAL = 1e-6
  i.e. no more than 1 non-sterile unit per 1,000,000 units.

  You cannot test this in by sampling - it is assured by validating
  the sterilization or aseptic process, not by end-product testing.
```

Remember: injectables demand sterility assured by process design, and
biologics are defined by their manufacturing process - upstream cell
culture, downstream purification, then sterile fill-finish.
""",
        ),
        quiz_lesson(
            "Quiz: Sterile and biologics manufacturing",
            (
                q(
                    "Why is aseptic processing used instead of terminal sterilization "
                    "for many biologics?",
                    (
                        opt("Aseptic processing is always cheaper"),
                        opt(
                            "The protein product cannot survive terminal sterilization "
                            "(e.g. heat), so components are sterilized separately and "
                            "assembled while keeping microbes out",
                            correct=True,
                        ),
                        opt("Terminal sterilization is illegal"),
                        opt("Biologics do not need to be sterile"),
                    ),
                    "Terminal sterilization is preferred when the product survives it; "
                    "fragile biologics require the riskier aseptic route.",
                ),
                q(
                    "In bioprocessing, what happens in the downstream stage?",
                    (
                        opt("Cells are grown in the bioreactor"),
                        opt(
                            "The protein is purified from the broth, typically by "
                            "chromatography steps plus viral clearance and filtration",
                            correct=True,
                        ),
                        opt("The cell line is genetically engineered"),
                        opt("The tablet is compressed"),
                    ),
                    "Upstream grows the cells and expresses the protein; downstream "
                    "purifies it (Protein A capture, polishing, viral clearance).",
                ),
                q(
                    "Why is a copy of a biologic called a biosimilar rather than a generic?",
                    (
                        opt("Because it is chemically identical to the original"),
                        opt(
                            "Because the process defines the product - without the "
                            "originator's exact process you cannot make an identical copy, "
                            "only a highly similar one",
                            correct=True,
                        ),
                        opt("Because it contains no active ingredient"),
                        opt("Because regulators do not review it"),
                    ),
                    "A biologic's folding and glycosylation depend on how it is made, so "
                    "an exact copy is not possible - hence 'similar'.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the central theme of pharmaceutical engineering emphasized "
                    "throughout this course?",
                    (
                        opt("Quality is tested into the product at the very end"),
                        opt(
                            "Quality is designed and built into the process, then "
                            "confirmed - not tested in afterwards",
                            correct=True,
                        ),
                        opt("The cheapest route is always the correct one"),
                        opt("Documentation is optional if the batch looks good"),
                    ),
                    "Build quality in - the shared idea behind GMP, QbD, PAT and CM.",
                ),
                q(
                    "What is the difference between a drug substance and a drug product?",
                    (
                        opt("They are identical"),
                        opt(
                            "The drug substance is the API (active molecule); the drug "
                            "product is the final dosage form that delivers it",
                            correct=True,
                        ),
                        opt("The drug substance is the packaging"),
                        opt("The drug product contains no API"),
                    ),
                    "Primary manufacturing makes the API; secondary manufacturing "
                    "formulates it into a tablet, capsule or injection.",
                ),
                q(
                    "Why is a convergent synthesis route generally preferred for an API?",
                    (
                        opt("It uses fewer reagents overall"),
                        opt(
                            "Yield multiplies across steps, so joining fragments late "
                            "gives a higher overall yield and protects valuable "
                            "intermediates",
                            correct=True,
                        ),
                        opt("Convergent routes cannot form impurities"),
                        opt("Regulators require the maximum number of steps"),
                    ),
                    "A shorter longest-path means more of the expensive late material survives.",
                ),
                q(
                    "In crystallization, what is supersaturation?",
                    (
                        opt("A solution at exactly its solubility limit"),
                        opt(
                            "A solution holding more solute than its equilibrium "
                            "solubility - the driving force for nucleation and growth",
                            correct=True,
                        ),
                        opt("A completely dry powder"),
                        opt("A solvent with no solute"),
                    ),
                    "Created by cooling, evaporation or antisolvent addition; it drives "
                    "crystals to form and grow.",
                ),
                q(
                    "Why does polymorphic form matter for a solid drug?",
                    (
                        opt("It only affects the crystal color"),
                        opt(
                            "Different forms can differ in solubility, dissolution and "
                            "stability, changing bioavailability and product performance",
                            correct=True,
                        ),
                        opt("It changes the molecular formula"),
                        opt("It has no downstream effect"),
                    ),
                    "The ritonavir case showed a new, less soluble form disrupting supply "
                    "- form must be identified and controlled.",
                ),
                q(
                    "What is the main function of a disintegrant in a tablet?",
                    (
                        opt("To provide the therapeutic effect"),
                        opt("To lubricate the tablet press"),
                        opt(
                            "To make the tablet break apart in the gut so the API can dissolve",
                            correct=True,
                        ),
                        opt("To color-code the dose"),
                    ),
                    "Excipients each have a job; the disintegrant drives break-up and release.",
                ),
                q(
                    "Which principle best captures GMP data integrity?",
                    (
                        opt("Only the final result must be recorded"),
                        opt(
                            "Records must be ALCOA - Attributable, Legible, "
                            "Contemporaneous, Original and Accurate",
                            correct=True,
                        ),
                        opt("Operators may reconstruct records from memory later"),
                        opt("Documentation is optional when testing passes"),
                    ),
                    "'If it is not documented, it did not happen' - contemporaneous, "
                    "attributable records are the proof of control.",
                ),
                q(
                    "In Quality by Design, what is the design space?",
                    (
                        opt("The physical floor area of the plant"),
                        opt(
                            "The multidimensional region of process-parameter settings "
                            "proven to deliver acceptable quality attributes; moving "
                            "within it is not a change",
                            correct=True,
                        ),
                        opt("The warehouse where product is stored"),
                        opt("The list of excipients in the formula"),
                    ),
                    "The design space links CPPs to CQAs; the control strategy keeps the "
                    "process inside it.",
                ),
                q(
                    "What does Process Analytical Technology (PAT) provide?",
                    (
                        opt("Slower, lab-only final testing"),
                        opt(
                            "In-line, real-time measurement of quality attributes, "
                            "enabling real-time control and real time release testing",
                            correct=True,
                        ),
                        opt("A way to skip the quality unit"),
                        opt("A packaging label design tool"),
                    ),
                    "NIR/Raman sensors read attributes as the process runs, so you steer "
                    "in real time.",
                ),
                q(
                    "Why is a copy of a biologic a biosimilar rather than a generic?",
                    (
                        opt("It contains a different active target"),
                        opt(
                            "The manufacturing process defines the product, so without "
                            "the originator's exact process only a highly similar - not "
                            "identical - copy is possible",
                            correct=True,
                        ),
                        opt("Biosimilars need no clinical or regulatory review"),
                        opt("It is chemically identical, just cheaper"),
                    ),
                    "Folding and glycosylation depend on how the protein is made; the "
                    "process is inseparable from the product.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PHARMACEUTICAL_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_PHARMACEUTICAL_ENGINEERING,)
