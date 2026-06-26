"""Quiz questions for the Capstone: End-to-End AI Drug Design Project - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Framing the project: the DMTA loop end to end": (
            q(
                "What does the DMTA loop stand for?",
                (
                    opt("Design, Make, Test, Analyze", correct=True),
                    opt("Discover, Model, Train, Apply"),
                    opt("Dock, Measure, Tune, Assess"),
                    opt("Design, Measure, Test, Approve"),
                ),
                "DMTA is the Design-Make-Test-Analyze cycle that organizes discovery.",
            ),
            q(
                "Which two arms of the DMTA loop does AI most accelerate?",
                (
                    opt("Design and Analyze", correct=True),
                    opt("Make and Test"),
                    opt("Make and Analyze"),
                    opt("Test and Design"),
                ),
                "AI speeds up proposing molecules (Design) and learning from data (Analyze).",
            ),
            q(
                "What should be fixed before any model is built?",
                (
                    opt("the target, the objective, and the success criteria", correct=True),
                    opt("the cloud GPU budget only"),
                    opt("the final clinical dose"),
                    opt("the marketing name"),
                ),
                "A capstone defines target, objective and measurable success criteria up front.",
            ),
        ),
        "Choosing and validating a target": (
            q(
                "Target validation asks about causality and which other property?",
                (
                    opt("druggability of the binding pocket", correct=True),
                    opt("the color of the protein"),
                    opt("the molecular weight of water"),
                    opt("the price of reagents"),
                ),
                "You need both a causal disease link and a druggable pocket.",
            ),
            q(
                "Which targets are classically easier to drug with small molecules?",
                (
                    opt("enzymes and receptors with enclosed pockets", correct=True),
                    opt("flat protein-protein interfaces"),
                    opt("disordered regions with no structure"),
                    opt("any protein equally"),
                ),
                "Well-defined enclosed pockets (kinases, proteases, receptors) are tractable.",
            ),
            q(
                "Where would you look for known ligands of a target?",
                (
                    opt("ChEMBL", correct=True),
                    opt("a weather database"),
                    opt("a stock-price feed"),
                    opt("a music catalog"),
                ),
                "ChEMBL holds curated bioactivities for many targets.",
            ),
        ),
        "Assembling the dataset: ChEMBL, PDB and beyond": (
            q(
                "What does the PDB primarily provide?",
                (
                    opt("3D protein and complex structures", correct=True),
                    opt("retail drug prices"),
                    opt("clinical trial schedules"),
                    opt("SMILES generation models"),
                ),
                "The Protein Data Bank stores experimentally determined 3D structures.",
            ),
            q(
                "Why convert IC50 to pIC50 = -log10(IC50)?",
                (
                    opt(
                        "activity spans orders of magnitude; the log gives a well-behaved label",
                        correct=True,
                    ),
                    opt("it makes the numbers larger for marketing"),
                    opt("it removes the need for any data cleaning"),
                    opt("it converts mass to moles"),
                ),
                "The log transform tames a huge dynamic range into a symmetric continuous label.",
            ),
            q(
                "On the pIC50 scale, a larger value means a compound is:",
                (
                    opt("more potent", correct=True),
                    opt("less potent"),
                    opt("more toxic"),
                    opt("heavier"),
                ),
                "pIC50 = -log10(IC50), so higher pIC50 means a smaller IC50 and more potency.",
            ),
        ),
        "Cleaning and curating chemical data": (
            q(
                "Standardizing structures includes which step?",
                (
                    opt("removing salts and picking a canonical tautomer", correct=True),
                    opt("deleting all hydrogen atoms permanently"),
                    opt("randomizing the atom order"),
                    opt("converting to a JPEG image"),
                ),
                "Standardization neutralizes charges, strips salts/solvents, and canonicalizes tautomers.",
            ),
            q(
                "What are PAINS?",
                (
                    opt(
                        "pan-assay interference compounds that cause false positives", correct=True
                    ),
                    opt("a class of approved painkillers"),
                    opt("protein assembly index numbers"),
                    opt("a docking scoring function"),
                ),
                "PAINS frequently give spurious assay hits and should be flagged.",
            ),
            q(
                "Why deduplicate compounds before modeling?",
                (
                    opt(
                        "repeated or conflicting measurements bias and leak into the model",
                        correct=True,
                    ),
                    opt("duplicates make files smaller"),
                    opt("duplicates improve accuracy automatically"),
                    opt("models require exactly one copy of water"),
                ),
                "Duplicate records must be merged; wildly disagreeing values are unreliable.",
            ),
        ),
        "Representing molecules for modeling": (
            q(
                "What is a SMILES string?",
                (
                    opt("a text encoding of a molecule, e.g. CCO for ethanol", correct=True),
                    opt("a 3D crystal coordinate file"),
                    opt("a protein sequence"),
                    opt("an assay protocol"),
                ),
                "SMILES is a compact line notation read directly by sequence models.",
            ),
            q(
                "An ECFP / Morgan fingerprint encodes what?",
                (
                    opt("circular atom neighborhoods hashed into a bit vector", correct=True),
                    opt("the exact 3D coordinates of every atom"),
                    opt("the assay IC50 value"),
                    opt("the protein folding energy"),
                ),
                "Morgan fingerprints hash circular substructures into fixed-length bits.",
            ),
            q(
                "Tanimoto similarity between two fingerprints measures:",
                (
                    opt("overlap of set bits (shared substructure)", correct=True),
                    opt("the difference in molecular weight"),
                    opt("the docking score"),
                    opt("the number of carbon atoms only"),
                ),
                "Tanimoto = |A intersect B| / |A union B| over fingerprint bits.",
            ),
        ),
        "Scoping the project plan and success criteria": (
            q(
                "A good capstone objective should be:",
                (
                    opt(
                        "specific and measurable, like a mini target product profile", correct=True
                    ),
                    opt("intentionally vague to allow flexibility"),
                    opt("defined only after the final results"),
                    opt("about model architecture, not outcomes"),
                ),
                "Vague goals are unfalsifiable; state concrete, measurable criteria.",
            ),
            q(
                "What is the purpose of go/no-go gates in the plan?",
                (
                    opt("kill weak candidates cheaply and early", correct=True),
                    opt("delay all decisions to the end"),
                    opt("ensure every compound advances"),
                    opt("avoid measuring anything"),
                ),
                "Gates apply explicit thresholds so weak candidates fail before costly stages.",
            ),
            q(
                "When should you decide the validation strategy?",
                (
                    opt("up front, in the plan", correct=True),
                    opt("after seeing the test scores"),
                    opt("never; it is optional"),
                    opt("only if the model fails"),
                ),
                "Choosing the scaffold split, held-out set and baseline early prevents self-deception.",
            ),
        ),
    },
    final=(
        q(
            "The capstone is best described as running which cycle end to end?",
            (
                opt("the Design-Make-Test-Analyze loop", correct=True),
                opt("a single one-shot prediction"),
                opt("a clinical trial"),
                opt("a literature review only"),
            ),
            "The project is a DMTA loop, not a single model.",
        ),
        q(
            "Which database is the primary source of curated bioactivity data?",
            (
                opt("ChEMBL", correct=True),
                opt("the PDB"),
                opt("UniProt only"),
                opt("a news API"),
            ),
            "ChEMBL provides curated IC50/Ki/EC50 measurements with assay context.",
        ),
        q(
            "Why is data curation so important?",
            (
                opt(
                    "every downstream model inherits the quality of the assembled data",
                    correct=True,
                ),
                opt("it makes training faster only"),
                opt("regulators require exactly 1000 compounds"),
                opt("it has no real effect on results"),
            ),
            "A sloppy dataset poisons every model trained on it.",
        ),
        q(
            "Which is NOT one of the three core molecular representations covered?",
            (
                opt("the assay vendor catalog number", correct=True),
                opt("SMILES strings"),
                opt("ECFP fingerprints"),
                opt("computed descriptors"),
            ),
            "SMILES, fingerprints and descriptors are the three; a catalog number is not a representation.",
        ),
        q(
            "Target validation requires evidence of:",
            (
                opt("disease causality and a druggable pocket", correct=True),
                opt("low molecular weight only"),
                opt("a catchy compound name"),
                opt("a large marketing budget"),
            ),
            "You need both causality and druggability before committing.",
        ),
        q(
            "What role do go/no-go gates play in the project plan?",
            (
                opt("they apply explicit thresholds to advance or kill candidates", correct=True),
                opt("they replace the need for data"),
                opt("they guarantee a drug is found"),
                opt("they are decorative only"),
            ),
            "Gates make each stage a measurable decision aligned to success criteria.",
        ),
    ),
)
