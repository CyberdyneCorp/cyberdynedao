"""Quiz questions for the Cheminformatics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Molecular descriptors and drug-likeness": (
            q(
                "What is a molecular descriptor?",
                (
                    opt(
                        "A number computed from structure that summarises a property", correct=True
                    ),
                    opt("A 3D rendering of the molecule"),
                    opt("A reaction mechanism"),
                    opt("The price of a reagent"),
                ),
                "Descriptors are numeric features derived from structure.",
            ),
            q(
                "Lipinski's Rule of Five flags poor oral absorption when MW exceeds:",
                (
                    opt("500", correct=True),
                    opt("50"),
                    opt("5000"),
                    opt("100000"),
                ),
                "One of the rules is molecular weight <= 500.",
            ),
            q(
                "What does logP measure?",
                (
                    opt("Octanol-water partition coefficient (lipophilicity)", correct=True),
                    opt("Molecular weight"),
                    opt("Number of rings"),
                    opt("Melting point"),
                ),
                "logP is the octanol-water partition coefficient.",
            ),
        ),
        "Molecular fingerprints": (
            q(
                "What is a molecular fingerprint?",
                (
                    opt("A fixed bit-vector encoding a molecule's features", correct=True),
                    opt("A 3D coordinate file"),
                    opt("A reaction yield"),
                    opt("A protein sequence"),
                ),
                "Fingerprints are bit-vectors enabling fast bitwise comparison.",
            ),
            q(
                "Which fingerprint family encodes circular atom neighbourhoods?",
                (
                    opt("ECFP / Morgan", correct=True),
                    opt("MACCS structural keys"),
                    opt("Daylight path-based only"),
                    opt("InChIKey"),
                ),
                "ECFP/Morgan hash circular environments out to a given radius.",
            ),
            q(
                "What does ECFP4 mean by the '4'?",
                (
                    opt("Diameter 4, i.e. radius 2", correct=True),
                    opt("Four bits total"),
                    opt("Four molecules compared"),
                    opt("Four rings required"),
                ),
                "ECFP4 uses a diameter of 4 (radius 2) around each atom.",
            ),
        ),
        "Molecular similarity and the Tanimoto coefficient": (
            q(
                "The Tanimoto coefficient for bit-vectors equals:",
                (
                    opt("c / (a + b - c)", correct=True),
                    opt("a + b + c"),
                    opt("c / (a * b)"),
                    opt("(a - b) / c"),
                ),
                "Tanimoto = shared bits / union of set bits.",
            ),
            q(
                "What is the range of the Tanimoto coefficient?",
                (
                    opt("0 to 1", correct=True),
                    opt("-1 to 1"),
                    opt("0 to 100"),
                    opt("1 to infinity"),
                ),
                "0 means no shared features, 1 means identical fingerprints.",
            ),
            q(
                "The similarity principle states that:",
                (
                    opt(
                        "Structurally similar molecules tend to have similar bioactivity",
                        correct=True,
                    ),
                    opt("All molecules have identical activity"),
                    opt("Similarity guarantees identical activity"),
                    opt("Larger molecules are always more active"),
                ),
                "It is an empirical tendency, broken by activity cliffs.",
            ),
        ),
        "Substructure search and SMARTS": (
            q(
                "Substructure search is formally which problem?",
                (
                    opt("Subgraph isomorphism", correct=True),
                    opt("Sorting"),
                    opt("Matrix inversion"),
                    opt("Shortest path"),
                ),
                "Matching a pattern inside a molecule is subgraph isomorphism.",
            ),
            q(
                "SMARTS is best described as:",
                (
                    opt("A query language extending SMILES with wildcards and logic", correct=True),
                    opt("A 3D file format"),
                    opt("A clustering algorithm"),
                    opt("A database schema"),
                ),
                "SMARTS expresses atom and bond constraints for matching.",
            ),
            q(
                "Why do databases run a fingerprint screen before subgraph matching?",
                (
                    opt(
                        "A query can match only if its bits are a subset of the molecule's bits, cheaply discarding non-matches",
                        correct=True,
                    ),
                    opt("To compute molecular weight"),
                    opt("To draw 2D structures"),
                    opt("Because VF2 is impossible to run"),
                ),
                "The screen is a cheap necessary condition that shrinks the candidate set.",
            ),
        ),
        "Foundations of QSAR modelling": (
            q(
                "QSAR models predict what from structure-derived features?",
                (
                    opt("A property such as potency, solubility or toxicity", correct=True),
                    opt("The exact 3D crystal structure"),
                    opt("The name of the chemist"),
                    opt("The reagent supplier"),
                ),
                "QSAR maps features to a measured property.",
            ),
            q(
                "The Hansch equation relates activity primarily to:",
                (
                    opt("Lipophilicity (logP) and electronic terms", correct=True),
                    opt("Only molecular weight"),
                    opt("Only the melting point"),
                    opt("The number of atoms only"),
                ),
                "Hansch analysis uses logP and substituent constants like sigma.",
            ),
            q(
                "A QSAR model should only be trusted within its:",
                (
                    opt("Applicability domain", correct=True),
                    opt("Country of origin"),
                    opt("File format"),
                    opt("Color scheme"),
                ),
                "Predictions are reliable only in the descriptor region the training set covers.",
            ),
        ),
    },
    final=(
        q(
            "Which is a Lipinski Rule-of-Five criterion?",
            (
                opt("Hydrogen-bond donors <= 5", correct=True),
                opt("Molecular weight >= 5000"),
                opt("logP <= 50"),
                opt("Ring count exactly 1"),
            ),
            "Rule of Five: MW<=500, logP<=5, HBD<=5, HBA<=10.",
        ),
        q(
            "ECFP/Morgan fingerprints are the de-facto standard for:",
            (
                opt("Similarity search and ML features", correct=True),
                opt("Storing 3D coordinates"),
                opt("Measuring melting points"),
                opt("Naming molecules"),
            ),
            "Circular fingerprints capture local environments well.",
        ),
        q(
            "If a=12, b=10 and c=6 shared bits, the Tanimoto coefficient is:",
            (
                opt("6 / 16 = 0.375", correct=True),
                opt("6 / 22"),
                opt("6 / 120"),
                opt("12 / 10"),
            ),
            "T = c/(a+b-c) = 6/(12+10-6) = 6/16.",
        ),
        q(
            "The Dice coefficient is defined as:",
            (
                opt("2c / (a + b)", correct=True),
                opt("c / (a + b - c)"),
                opt("c / (a * b)"),
                opt("(a + b) / c"),
            ),
            "Dice weights the intersection more heavily than Tanimoto.",
        ),
        q(
            "A fingerprint screen before VF2 matching works because it is:",
            (
                opt("A necessary condition that cheaply rules out non-matches", correct=True),
                opt("A sufficient condition that confirms all matches"),
                opt("A way to compute logP"),
                opt("A 3D alignment method"),
            ),
            "Every query bit must be set in a true match, so the screen filters cheaply.",
        ),
        q(
            "Overfitting in QSAR shows up as:",
            (
                opt("Training error falling while test error eventually rises", correct=True),
                opt("Both errors always falling forever"),
                opt("Test error always lower than training error"),
                opt("No relationship between complexity and error"),
            ),
            "The U-shaped generalisation curve signals overfitting at high complexity.",
        ),
    ),
)
