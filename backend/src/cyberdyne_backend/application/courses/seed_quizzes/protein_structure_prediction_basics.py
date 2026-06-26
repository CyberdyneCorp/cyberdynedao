"""Quiz questions for the Protein Structure Prediction - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "From sequence to structure: the folding problem": (
            q(
                "What did Anfinsen's ribonuclease experiment support?",
                (
                    opt(
                        "The native fold is encoded in the sequence and is the free-energy minimum",
                        correct=True,
                    ),
                    opt("Proteins need other proteins to fold at all"),
                    opt("DNA determines structure without translation"),
                    opt("Folding is purely random"),
                ),
                "It supported the thermodynamic hypothesis.",
            ),
            q(
                "What does Levinthal's paradox highlight?",
                (
                    opt(
                        "Random conformational search would take impossibly long, yet folding is fast",
                        correct=True,
                    ),
                    opt("Proteins cannot fold without enzymes"),
                    opt("Sequences are unrelated to structure"),
                    opt("Folding always fails in the test tube"),
                ),
                "Folding is fast because the landscape is a funnel.",
            ),
            q(
                "The folding energy landscape is best described as what shape?",
                (
                    opt("Funnel-shaped toward a native basin", correct=True),
                    opt("A flat plateau"),
                    opt("A single tall spike"),
                    opt("A perfect sphere"),
                ),
                "A funnel guides many unfolded states to the native minimum.",
            ),
        ),
        "The four levels of protein structure": (
            q(
                "Which is the correct order of structural levels?",
                (
                    opt("Primary, secondary, tertiary, quaternary", correct=True),
                    opt("Tertiary, primary, quaternary, secondary"),
                    opt("Quaternary, tertiary, secondary, primary"),
                    opt("Secondary, primary, tertiary, quaternary"),
                ),
                "Sequence, local H-bonding, 3D chain, then multi-chain assembly.",
            ),
            q(
                "The Ramachandran plot maps which backbone angles?",
                (
                    opt("phi and psi dihedral angles", correct=True),
                    opt("Bond lengths and masses"),
                    opt("Temperature and pressure"),
                    opt("Charge and hydrophobicity"),
                ),
                "Allowed phi/psi regions correspond to helices and strands.",
            ),
            q(
                "Alpha-helices and beta-sheets are examples of which level?",
                (
                    opt("Secondary structure", correct=True),
                    opt("Primary structure"),
                    opt("Quaternary structure"),
                    opt("Genetic structure"),
                ),
                "They are local backbone hydrogen-bonded motifs.",
            ),
        ),
        "Forces that stabilise the fold": (
            q(
                "What is usually the dominant driving force of folding in water?",
                (
                    opt("The hydrophobic effect", correct=True),
                    opt("Covalent disulfide bonds only"),
                    opt("Gravity"),
                    opt("Magnetic interactions"),
                ),
                "Burying nonpolar side chains minimises water ordering.",
            ),
            q(
                "Typical net folding stability of a protein is about what?",
                (
                    opt("5-15 kcal/mol (marginally stable)", correct=True),
                    opt("Several thousand kcal/mol"),
                    opt("Exactly zero always"),
                    opt("Negative infinity"),
                ),
                "Stability is a small difference between large terms.",
            ),
            q(
                "A two-state thermal denaturation curve is characterised by what?",
                (
                    opt("A sigmoidal transition with a melting temperature Tm", correct=True),
                    opt("A straight horizontal line"),
                    opt("A curve that never changes"),
                    opt("A random scatter"),
                ),
                "Folded fraction drops sharply around Tm.",
            ),
        ),
        "How experimental structures are determined": (
            q(
                "Where are most experimentally solved structures deposited?",
                (
                    opt("The Protein Data Bank (PDB)", correct=True),
                    opt("GenBank"),
                    opt("UniProt"),
                    opt("PubMed"),
                ),
                "The PDB is the central structure repository.",
            ),
            q(
                "Which technique images frozen single particles?",
                (
                    opt("Cryo-electron microscopy", correct=True),
                    opt("X-ray crystallography"),
                    opt("Mass spectrometry"),
                    opt("PCR"),
                ),
                "Cryo-EM freezes particles and reconstructs density.",
            ),
            q(
                "Lower resolution numbers (in angstrom) generally mean what?",
                (
                    opt("Sharper, more detailed maps", correct=True),
                    opt("Worse, blurrier maps"),
                    opt("No structural information"),
                    opt("A larger protein"),
                ),
                "Smaller resolution values give finer detail.",
            ),
        ),
        "Homology modeling: structure follows sequence": (
            q(
                "Homology modeling relies on which key biological fact?",
                (
                    opt("Structure is more conserved than sequence among homologs", correct=True),
                    opt("Sequence is more conserved than structure"),
                    opt("Homologs never share folds"),
                    opt("Structure is random"),
                ),
                "Conserved folds let us copy a template's structure.",
            ),
            q(
                "What is the 'twilight zone' in homology modeling?",
                (
                    opt(
                        "Sequence identity below ~25-30% where models are unreliable", correct=True
                    ),
                    opt("Identity above 90%"),
                    opt("The region of perfect models"),
                    opt("A type of X-ray detector"),
                ),
                "Low identity makes alignment and modeling unreliable.",
            ),
            q(
                "Which tool is a classic homology-modeling program?",
                (
                    opt("MODELLER", correct=True),
                    opt("BLAST"),
                    opt("DSSP"),
                    opt("Excel"),
                ),
                "MODELLER (and SWISS-MODEL) build comparative models.",
            ),
        ),
        "When homology fails: the de novo problem": (
            q(
                "When is template-free (de novo) prediction needed?",
                (
                    opt("When no reliable template is detectable", correct=True),
                    opt("When identity is above 90%"),
                    opt("Whenever a template exists"),
                    opt("Only for DNA"),
                ),
                "Novel folds and twilight-zone sequences lack templates.",
            ),
            q(
                "How does classic Rosetta build de novo models?",
                (
                    opt(
                        "Assembling PDB fragments with Monte Carlo and an energy function",
                        correct=True,
                    ),
                    opt("Copying a single known template exactly"),
                    opt("Reading the structure from a database"),
                    opt("Translating DNA directly to coordinates"),
                ),
                "Fragment assembly plus scoring searches conformations.",
            ),
            q(
                "Why is de novo prediction historically limited to small proteins?",
                (
                    opt(
                        "Conformational search is very expensive and grows with size", correct=True
                    ),
                    opt("Large proteins have no sequence"),
                    opt("Small proteins have no structure"),
                    opt("It is forbidden by Anfinsen"),
                ),
                "Sampling cost explodes with chain length.",
            ),
        ),
    },
    final=(
        q(
            "The thermodynamic hypothesis states that the native fold is what?",
            (
                opt("The global free-energy minimum encoded by the sequence", correct=True),
                opt("A random accident"),
                opt("Determined only by chaperones"),
                opt("Independent of the amino-acid sequence"),
            ),
            "Anfinsen showed structure follows from sequence.",
        ),
        q(
            "Which level of structure is the amino-acid sequence itself?",
            (
                opt("Primary", correct=True),
                opt("Secondary"),
                opt("Tertiary"),
                opt("Quaternary"),
            ),
            "Primary structure is the linear sequence.",
        ),
        q(
            "The main entropic driving force of folding in water is the:",
            (
                opt("Hydrophobic effect", correct=True),
                opt("Disulfide bond"),
                opt("Peptide bond"),
                opt("Ionic radius"),
            ),
            "Burying nonpolar residues frees ordered water.",
        ),
        q(
            "Which method determines structures from a crystal's diffraction?",
            (
                opt("X-ray crystallography", correct=True),
                opt("NMR"),
                opt("Cryo-EM"),
                opt("Sanger sequencing"),
            ),
            "Crystallography uses X-ray diffraction.",
        ),
        q(
            "Homology-model accuracy depends most strongly on what?",
            (
                opt("Sequence identity to the template", correct=True),
                opt("The day of the week"),
                opt("Protein color"),
                opt("Number of authors"),
            ),
            "Higher identity yields lower-RMSD models.",
        ),
        q(
            "Template-free prediction is required when:",
            (
                opt("No usable template can be found for the query", correct=True),
                opt("A high-identity template exists"),
                opt("The protein is already in the PDB"),
                opt("The sequence is unknown"),
            ),
            "De novo methods handle novel or twilight-zone folds.",
        ),
    ),
)
