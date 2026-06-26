"""Quiz questions for the General & Inorganic Chemistry - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Coordination chemistry": (
            q(
                "In a coordination compound, a ligand acts as which species?",
                (
                    opt("A Lewis base donating an electron pair", correct=True),
                    opt("A Lewis acid accepting electrons"),
                    opt("A proton donor"),
                    opt("A neutral spectator only"),
                ),
                "Ligands are Lewis bases donating lone pairs to the metal centre.",
            ),
            q(
                "The chelate effect, which stabilises polydentate complexes, is driven mainly by what?",
                (
                    opt("A large favourable entropy change", correct=True),
                    opt("A large unfavourable enthalpy"),
                    opt("Decreasing temperature"),
                    opt("Loss of all ligand bonds"),
                ),
                "Chelation releases several small ligands, raising entropy.",
            ),
            q(
                "An octahedral complex has which coordination number?",
                (
                    opt("Two"),
                    opt("Four"),
                    opt("Six", correct=True),
                    opt("Eight"),
                ),
                "Octahedral geometry corresponds to coordination number six.",
            ),
        ),
        "Crystal field and ligand field theory": (
            q(
                "In an octahedral field, which set of d-orbitals is raised in energy?",
                (
                    opt("The e_g set", correct=True),
                    opt("The t_2g set"),
                    opt("The s-orbitals"),
                    opt("None of them"),
                ),
                "The e_g orbitals point at ligands and rise; t_2g fall.",
            ),
            q(
                "A strong-field ligand with large splitting tends to produce which configuration?",
                (
                    opt("Low-spin", correct=True),
                    opt("High-spin"),
                    opt("Always paramagnetic with maximum unpaired electrons"),
                    opt("No electron occupancy"),
                ),
                "Large delta_o exceeds pairing energy, giving a low-spin complex.",
            ),
            q(
                "The colour of a transition-metal complex is set primarily by what?",
                (
                    opt("The crystal-field splitting delta_o", correct=True),
                    opt("The molar mass of the metal"),
                    opt("The number of neutrons"),
                    opt("The temperature only"),
                ),
                "Light of energy equal to delta_o is absorbed, setting the colour.",
            ),
        ),
        "Organometallics and catalysis": (
            q(
                "The 18-electron rule predicts special stability when the valence shell has what?",
                (
                    opt("18 electrons (a filled valence shell)", correct=True),
                    opt("8 electrons"),
                    opt("2 electrons"),
                    opt("32 electrons"),
                ),
                "Many organometallics are most stable at an 18-electron count.",
            ),
            q(
                "Which step forms a new metal-substrate bond by adding across the metal centre?",
                (
                    opt("Oxidative addition", correct=True),
                    opt("Reductive elimination"),
                    opt("Beta-hydride loss only"),
                    opt("Ligand dissociation only"),
                ),
                "Oxidative addition adds a substrate and raises the metal oxidation state.",
            ),
            q(
                "Pd-catalysed Suzuki and Heck reactions are prized for forming which bonds?",
                (
                    opt("Carbon-carbon bonds", correct=True),
                    opt("Nitrogen-nitrogen bonds"),
                    opt("Metal-metal bonds"),
                    opt("Ionic bonds only"),
                ),
                "These cross-couplings build C-C bonds, key in pharma synthesis.",
            ),
        ),
        "Solid-state and materials chemistry": (
            q(
                "Crystalline solids are distinguished by what feature?",
                (
                    opt("A periodic, long-range ordered lattice", correct=True),
                    opt("No order at any scale"),
                    opt("Being always electrically conductive"),
                    opt("Being liquids at room temperature"),
                ),
                "Crystals have long-range periodic order; amorphous solids do not.",
            ),
            q(
                "In band theory, a semiconductor is characterised by which band gap?",
                (
                    opt("A small band gap", correct=True),
                    opt("No band gap at all"),
                    opt("An extremely large band gap"),
                    opt("A negative band gap"),
                ),
                "Semiconductors have a small gap; metals have none, insulators a large one.",
            ),
            q(
                "Bragg's law (n lambda = 2 d sin theta) is the basis of which technique?",
                (
                    opt("X-ray diffraction", correct=True),
                    opt("Nuclear magnetic resonance"),
                    opt("Mass spectrometry"),
                    opt("Calorimetry"),
                ),
                "Bragg's law underlies X-ray diffraction structure determination.",
            ),
        ),
        "Bioinorganic chemistry: metals in biology": (
            q(
                "Which metal at the heme centre of hemoglobin reversibly binds oxygen?",
                (
                    opt("Iron", correct=True),
                    opt("Zinc"),
                    opt("Magnesium"),
                    opt("Sodium"),
                ),
                "Heme iron binds O2 reversibly for transport.",
            ),
            q(
                "Hemoglobin's sigmoidal oxygen-binding curve reflects what behaviour?",
                (
                    opt("Cooperative binding (Hill n > 1)", correct=True),
                    opt("No binding at all"),
                    opt("Simple linear binding"),
                    opt("Irreversible binding"),
                ),
                "Cooperativity across subunits produces the sigmoidal Hill curve.",
            ),
            q(
                "Nitrogenase, which fixes N2 to ammonia, relies on which metals?",
                (
                    opt("Molybdenum and iron", correct=True),
                    opt("Sodium and potassium"),
                    opt("Silver and gold"),
                    opt("Aluminium only"),
                ),
                "The nitrogenase active site uses a Mo-Fe cofactor.",
            ),
        ),
        "Spectroscopy and computational chemistry": (
            q(
                "The Beer-Lambert law makes UV-Vis quantitative by relating absorbance to what?",
                (
                    opt("Concentration (A = epsilon c l)", correct=True),
                    opt("Temperature only"),
                    opt("Magnetic field"),
                    opt("Nuclear spin"),
                ),
                "Absorbance is proportional to concentration and path length.",
            ),
            q(
                "Which computational method is now standard for predicting electronic structure?",
                (
                    opt("Density functional theory (DFT)", correct=True),
                    opt("Newtonian mechanics by hand"),
                    opt("Linear regression on bond lengths"),
                    opt("Bragg's law"),
                ),
                "DFT approximately solves the electronic structure and is widely used.",
            ),
            q(
                "Machine-learning interatomic potentials are valued in materials discovery because they do what?",
                (
                    opt("Approach DFT accuracy at far lower computational cost", correct=True),
                    opt("Replace the need for any chemistry knowledge"),
                    opt("Are always exact and never approximate"),
                    opt("Only work for noble gases"),
                ),
                "ML potentials enable high-throughput screening near DFT accuracy, much faster.",
            ),
        ),
    },
    final=(
        q(
            "EDTA is an example of what kind of ligand?",
            (
                opt("A polydentate chelator", correct=True),
                opt("A monodentate ligand"),
                opt("A pure Lewis acid"),
                opt("A noble gas"),
            ),
            "EDTA wraps a metal with several donor atoms, a polydentate chelator.",
        ),
        q(
            "Whether a complex is high-spin or low-spin depends on comparing delta_o to what?",
            (
                opt("The electron pairing energy P", correct=True),
                opt("The atomic mass"),
                opt("The pH"),
                opt("Avogadro's number"),
            ),
            "If delta_o exceeds the pairing energy, the complex is low-spin.",
        ),
        q(
            "Reductive elimination in a catalytic cycle accomplishes what?",
            (
                opt("Releases product and regenerates the metal catalyst", correct=True),
                opt("Adds a substrate to the metal"),
                opt("Permanently destroys the catalyst"),
                opt("Raises the metal oxidation state"),
            ),
            "Reductive elimination expels the product and lowers the metal oxidation state.",
        ),
        q(
            "A material with no band gap is best classified as what?",
            (
                opt("A metal (conductor)", correct=True),
                opt("An insulator"),
                opt("A wide-gap semiconductor"),
                opt("A molecular gas"),
            ),
            "No band gap means overlapping bands and metallic conduction.",
        ),
        q(
            "Zinc in carbonic anhydrase functions primarily as what?",
            (
                opt("A Lewis-acid catalytic centre", correct=True),
                opt("An oxygen carrier"),
                opt("A magnetic probe"),
                opt("A structural defect"),
            ),
            "Zinc acts as a Lewis acid to catalyse CO2 hydration.",
        ),
        q(
            "Autonomous, robot-run laboratories combined with ML models aim to do what?",
            (
                opt("Close the design-make-test loop for new materials", correct=True),
                opt("Eliminate the periodic table"),
                opt("Replace all spectroscopy with guesswork"),
                opt("Make DFT unnecessary for any purpose"),
            ),
            "Generative models and self-driving labs accelerate materials discovery end to end.",
        ),
    ),
)
