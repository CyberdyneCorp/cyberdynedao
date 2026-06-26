"""Quiz questions for the Cell Biology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The cell and the cell theory": (
            q(
                "Which statement is part of the cell theory?",
                (
                    opt("Every cell arises from a pre-existing cell", correct=True),
                    opt("Cells form spontaneously from non-living matter"),
                    opt("Only plants are made of cells"),
                    opt("Organelles are the basic unit of life"),
                ),
                "Virchow's 'omnis cellula e cellula' states that cells come from pre-existing cells.",
            ),
            q(
                "What is the key structural difference between prokaryotes and eukaryotes?",
                (
                    opt(
                        "Eukaryotes have a membrane-bound nucleus, prokaryotes do not", correct=True
                    ),
                    opt("Prokaryotes are always larger than eukaryotes"),
                    opt("Only prokaryotes have DNA"),
                    opt("Eukaryotes have no plasma membrane"),
                ),
                "Eukaryotes compartmentalize DNA in a membrane-bound nucleus; prokaryotes keep it in a nucleoid.",
            ),
            q(
                "Why does the surface-to-volume ratio limit cell size?",
                (
                    opt(
                        "Volume (demand) grows faster than surface (supply) as radius increases",
                        correct=True,
                    ),
                    opt("Surface area grows faster than volume"),
                    opt("Both grow at exactly the same rate"),
                    opt("Larger cells always have more membrane than they need"),
                ),
                "S/V = 3/r falls as r grows, so large cells cannot supply their volume across their membrane.",
            ),
        ),
        "The plasma membrane: the fluid mosaic": (
            q(
                "Why do phospholipids spontaneously form a bilayer in water?",
                (
                    opt(
                        "They are amphipathic: hydrophilic heads face water, hydrophobic tails hide inward",
                        correct=True,
                    ),
                    opt("They are entirely hydrophobic"),
                    opt("They are entirely hydrophilic"),
                    opt("They are pumped into shape by ATP"),
                ),
                "Amphipathic lipids bury their tails away from water, the lowest free-energy arrangement.",
            ),
            q(
                "What role does cholesterol play in the membrane?",
                (
                    opt(
                        "It buffers fluidity, stiffening at warm and fluidizing at cold temperatures",
                        correct=True,
                    ),
                    opt("It carries the genetic code"),
                    opt("It is the main transporter of glucose"),
                    opt("It blocks all proteins from moving"),
                ),
                "Cholesterol broadens the transition, moderating membrane fluidity across temperatures.",
            ),
            q(
                "The fluid mosaic model describes the membrane as what?",
                (
                    opt("A two-dimensional fluid with proteins that drift laterally", correct=True),
                    opt("A rigid crystalline solid"),
                    opt("A single layer of protein"),
                    opt("A static wall of cellulose"),
                ),
                "Singer-Nicolson modeled the bilayer as a fluid studded with mobile proteins.",
            ),
        ),
        "Organelles and the endomembrane system": (
            q(
                "Which organelle folds and glycosylates proteins entering the secretory pathway?",
                (
                    opt("Rough endoplasmic reticulum", correct=True),
                    opt("Peroxisome"),
                    opt("Mitochondrion"),
                    opt("Nucleolus"),
                ),
                "The rough ER, studded with ribosomes, folds and glycosylates secretory and membrane proteins.",
            ),
            q(
                "What maintains the acidic pH inside lysosomes?",
                (
                    opt("A V-ATPase proton pump", correct=True),
                    opt("The Na/K-ATPase"),
                    opt("Passive diffusion of glucose"),
                    opt("The nuclear pore complex"),
                ),
                "The vacuolar V-ATPase pumps protons in to keep the lysosome near pH 4.5.",
            ),
            q(
                "Which vesicle coat carries cargo outward from the ER toward the Golgi?",
                (
                    opt("COPII", correct=True),
                    opt("COPI"),
                    opt("Clathrin only"),
                    opt("Lamin"),
                ),
                "COPII buds anterograde from the ER; COPI is retrograde and clathrin acts at the PM/Golgi.",
            ),
        ),
        "The nucleus and the central dogma": (
            q(
                "What is a nucleosome?",
                (
                    opt("DNA wound around a histone octamer", correct=True),
                    opt("A ribosome bound to mRNA"),
                    opt("A type of mitochondrion"),
                    opt("A pore in the nuclear envelope"),
                ),
                "Nucleosomes are the beads-on-a-string units of DNA wrapped around histones.",
            ),
            q(
                "In the central dogma, what is the normal direction of information flow?",
                (
                    opt("DNA -> RNA -> protein", correct=True),
                    opt("Protein -> RNA -> DNA"),
                    opt("RNA -> protein -> DNA"),
                    opt("DNA -> protein directly, skipping RNA"),
                ),
                "Transcription makes RNA from DNA; translation makes protein from RNA.",
            ),
            q(
                "Which processing step removes introns from pre-mRNA?",
                (
                    opt("Splicing", correct=True),
                    opt("Capping"),
                    opt("Polyadenylation"),
                    opt("Translation"),
                ),
                "Splicing excises introns and joins exons before export.",
            ),
        ),
        "Mitochondria, chloroplasts and cellular energy": (
            q(
                "According to the endosymbiotic theory, mitochondria descend from what?",
                (
                    opt("Engulfed free-living bacteria", correct=True),
                    opt("Fragments of the nucleus"),
                    opt("Pieces of the Golgi apparatus"),
                    opt("Viral particles"),
                ),
                "Their own circular DNA and 70S-type ribosomes support a bacterial endosymbiont origin.",
            ),
            q(
                "What directly powers ATP synthase during oxidative phosphorylation?",
                (
                    opt(
                        "A proton gradient across the inner membrane (proton-motive force)",
                        correct=True,
                    ),
                    opt("Direct sunlight"),
                    opt("Glucose binding to the enzyme"),
                    opt("The Na/K gradient"),
                ),
                "Chemiosmosis: protons flow back through ATP synthase, driving phosphorylation of ADP.",
            ),
            q(
                "Where does glycolysis occur?",
                (
                    opt("In the cytosol", correct=True),
                    opt("In the mitochondrial matrix"),
                    opt("Inside the nucleus"),
                    opt("In the thylakoid membrane"),
                ),
                "Glycolysis runs in the cytosol, producing pyruvate and a small ATP yield before the Krebs cycle.",
            ),
        ),
    },
    final=(
        q(
            "Which is the smallest unit considered alive?",
            (
                opt("The cell", correct=True),
                opt("The organelle"),
                opt("The protein"),
                opt("The chromosome"),
            ),
            "The cell is the basic unit of life capable of metabolism and reproduction.",
        ),
        q(
            "The hydrophobic core of the plasma membrane is formed by what?",
            (
                opt("The fatty-acid tails of phospholipids", correct=True),
                opt("The phosphate head groups"),
                opt("Cholesterol crystals only"),
                opt("Membrane carbohydrates"),
            ),
            "Fatty-acid tails point inward to form the hydrophobic interior of the bilayer.",
        ),
        q(
            "Which sequence correctly orders the secretory pathway?",
            (
                opt("Rough ER -> Golgi -> secretory vesicle -> plasma membrane", correct=True),
                opt("Golgi -> rough ER -> lysosome -> nucleus"),
                opt("Plasma membrane -> Golgi -> rough ER"),
                opt("Mitochondrion -> Golgi -> ER"),
            ),
            "Cargo flows from the ER through the Golgi to vesicles and the cell surface.",
        ),
        q(
            "Nuclear pore complexes primarily do what?",
            (
                opt("Gate macromolecular traffic across the nuclear envelope", correct=True),
                opt("Synthesize ATP"),
                opt("Replicate mitochondrial DNA"),
                opt("Pump protons into lysosomes"),
            ),
            "NPCs control passage of RNA and proteins between nucleus and cytoplasm.",
        ),
        q(
            "ATP synthase produces ATP by harnessing what?",
            (
                opt("The flow of protons down their electrochemical gradient", correct=True),
                opt("The breakdown of DNA"),
                opt("Direct absorption of light by every cell"),
                opt("Lateral diffusion of membrane proteins"),
            ),
            "Protons returning through ATP synthase drive its rotation and ATP synthesis.",
        ),
        q(
            "Why must cells stay small or have high surface-to-volume ratios?",
            (
                opt(
                    "To exchange enough material across their membrane to supply their volume",
                    correct=True,
                ),
                opt("To store more DNA"),
                opt("To avoid making any proteins"),
                opt("Because large cells cannot contain water"),
            ),
            "Exchange across the membrane scales with surface area, which lags volume as size grows.",
        ),
    ),
)
