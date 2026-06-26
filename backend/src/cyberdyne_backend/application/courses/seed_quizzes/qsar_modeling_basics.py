"""Quiz questions for the QSAR & Pharmacophore Modeling - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is QSAR?": (
            q(
                "What does a QSAR model relate?",
                (
                    opt("numerical structural descriptors to biological activity", correct=True),
                    opt("price to molecular weight"),
                    opt("color to melting point"),
                    opt("synthesis cost to patent age"),
                ),
                "QSAR maps descriptors (structure encoded as numbers) to a measured activity.",
            ),
            q(
                "Who pioneered the modern QSAR approach in the 1960s?",
                (
                    opt("Corwin Hansch", correct=True),
                    opt("Linus Pauling"),
                    opt("Dmitri Mendeleev"),
                    opt("Christopher Lipinski"),
                ),
                "Hansch introduced linear free-energy QSAR using physicochemical descriptors.",
            ),
            q(
                "What practical benefit does a QSAR model give a medicinal chemist?",
                (
                    opt(
                        "it prioritizes which analogues to synthesize before bench work",
                        correct=True,
                    ),
                    opt("it eliminates the need for any assays ever"),
                    opt("it guarantees clinical approval"),
                    opt("it determines the price of the drug"),
                ),
                "QSAR enables virtual screening and prioritization, saving time and reagents.",
            ),
        ),
        "Measuring biological activity": (
            q(
                "What does IC50 measure?",
                (
                    opt("the concentration that inhibits 50% of a target's activity", correct=True),
                    opt("the molecular weight at 50 percent purity"),
                    opt("the time to reach 50 percent absorption"),
                    opt("the temperature at half-maximal solubility"),
                ),
                "IC50 is the half-maximal inhibitory concentration.",
            ),
            q(
                "Why does QSAR use pIC50 rather than IC50 directly?",
                (
                    opt(
                        "the log scale spreads potencies evenly and is additive in free-energy terms",
                        correct=True,
                    ),
                    opt("IC50 is impossible to measure"),
                    opt("pIC50 has larger numbers that look more impressive"),
                    opt("IC50 is always negative"),
                ),
                "pIC50 = -log10(IC50) linearizes a multiplicative scale spanning orders of magnitude.",
            ),
            q(
                "A dose-response curve plotted against log concentration is typically:",
                (
                    opt("sigmoidal, described by the Hill equation", correct=True),
                    opt("a straight horizontal line"),
                    opt("a perfect circle"),
                    opt("exponentially diverging"),
                ),
                "The Hill equation gives the classic S-shaped curve with the midpoint at EC50/IC50.",
            ),
        ),
        "Molecular descriptors": (
            q(
                "Which of these is a lipophilic descriptor in the Hansch scheme?",
                (
                    opt("logP", correct=True),
                    opt("Hammett sigma"),
                    opt("Taft Es"),
                    opt("dipole moment"),
                ),
                "logP (and the pi constant) are lipophilic; sigma is electronic, Es is steric.",
            ),
            q(
                "The Hammett sigma constant belongs to which descriptor family?",
                (
                    opt("electronic", correct=True),
                    opt("lipophilic"),
                    opt("steric"),
                    opt("topological"),
                ),
                "Sigma quantifies electronic effects of substituents.",
            ),
            q(
                "What are ECFP and MACCS examples of?",
                (
                    opt("molecular fingerprints / structural keys", correct=True),
                    opt("assay instruments"),
                    opt("regression algorithms"),
                    opt("solvents"),
                ),
                "They are substructure fingerprints that encode the presence of features.",
            ),
        ),
        "The SAR concept and activity cliffs": (
            q(
                "What is the similar property principle?",
                (
                    opt(
                        "structurally similar molecules tend to have similar activities",
                        correct=True,
                    ),
                    opt("all molecules have identical activity"),
                    opt("larger molecules are always more active"),
                    opt("similarity has no relation to activity"),
                ),
                "This assumption underpins SAR and QSAR.",
            ),
            q(
                "What is an activity cliff?",
                (
                    opt("two very similar molecules with very different activities", correct=True),
                    opt("a molecule with zero activity"),
                    opt("a plateau in a dose-response curve"),
                    opt("the maximum logP a drug can have"),
                ),
                "Activity cliffs are exceptions to the similar property principle and break QSAR smoothness.",
            ),
            q(
                "Why are activity cliffs important to medicinal chemists?",
                (
                    opt("they pinpoint a critical structural interaction", correct=True),
                    opt("they prove the assay was wrong"),
                    opt("they indicate the molecule is insoluble"),
                    opt("they have no informational value"),
                ),
                "A large activity swing from a tiny change reveals a key binding interaction.",
            ),
        ),
        "Matched molecular pairs": (
            q(
                "What defines a matched molecular pair?",
                (
                    opt("two molecules differing by a single defined transformation", correct=True),
                    opt("two molecules with identical activity"),
                    opt("two molecules with the same molecular weight"),
                    opt("two molecules from different organisms"),
                ),
                "An MMP differs by one edit while the rest of the molecule (context) stays fixed.",
            ),
            q(
                "What does aggregating many pairs sharing the same transformation reveal?",
                (
                    opt(
                        "the average property change attributable to that transformation",
                        correct=True,
                    ),
                    opt("the synthesis cost of the molecule"),
                    opt("the boiling point of the solvent"),
                    opt("the assay temperature"),
                ),
                "Pooling pairs separates the transformation's signal from molecule-to-molecule noise.",
            ),
            q(
                "A transformation with a wide, bimodal delta-activity distribution often signals:",
                (
                    opt("activity cliffs", correct=True),
                    opt("a perfect linear model"),
                    opt("an inert substituent"),
                    opt("a measurement with no variance"),
                ),
                "Bimodal/wide spreads indicate context-dependent, cliff-like behaviour.",
            ),
        ),
        "A first linear QSAR model": (
            q(
                "Multiple linear regression models activity as:",
                (
                    opt("a weighted sum of descriptors", correct=True),
                    opt("the product of all descriptors"),
                    opt("a random constant"),
                    opt("the maximum descriptor only"),
                ),
                "MLR fits pIC50 = c0 + c1*D1 + ... by least squares.",
            ),
            q(
                "What does R^2 measure?",
                (
                    opt("how well the model fits the data it was trained on", correct=True),
                    opt("the molecular weight"),
                    opt("the number of descriptors"),
                    opt("the assay duration"),
                ),
                "R^2 is the coefficient of determination for the fit, between 0 and 1.",
            ),
            q(
                "Why is a high R^2 alone not enough?",
                (
                    opt(
                        "it can reflect overfitting and says nothing about predicting new compounds",
                        correct=True,
                    ),
                    opt("R^2 is always exactly 1"),
                    opt("R^2 measures toxicity"),
                    opt("a high R^2 guarantees external prediction"),
                ),
                "With many descriptors and few compounds you can fit noise; validation is required.",
            ),
        ),
    },
    final=(
        q(
            "QSAR fundamentally connects molecular structure to:",
            (
                opt("measured activity via numerical descriptors", correct=True),
                opt("the cost of synthesis"),
                opt("the color of the compound"),
                opt("the year of discovery"),
            ),
            "QSAR is a model A = f(descriptors).",
        ),
        q(
            "The standard QSAR response variable derived from IC50 is:",
            (
                opt("pIC50 = -log10(IC50)", correct=True),
                opt("IC50 squared"),
                opt("1/MW"),
                opt("the Hill slope"),
            ),
            "The negative log molar potency linearizes the scale.",
        ),
        q(
            "Which trio matches the classical Hansch descriptor families?",
            (
                opt("lipophilic, electronic, steric", correct=True),
                opt("acidic, basic, neutral"),
                opt("solid, liquid, gas"),
                opt("red, green, blue"),
            ),
            "Hansch grouped descriptors into hydrophobic, electronic and steric.",
        ),
        q(
            "An activity cliff is best described as:",
            (
                opt("similar structures with very different activities", correct=True),
                opt("a smooth linear trend"),
                opt("the optimum logP value"),
                opt("a fully validated model"),
            ),
            "Cliffs violate the similar property principle.",
        ),
        q(
            "A matched molecular pair differs by:",
            (
                opt("a single defined structural transformation", correct=True),
                opt("their entire scaffold"),
                opt("the assay used"),
                opt("nothing at all"),
            ),
            "One edit, fixed context.",
        ),
        q(
            "The simplest QSAR fitting method covered is:",
            (
                opt("multiple linear regression by least squares", correct=True),
                opt("a graph neural network"),
                opt("partial least squares with 3D fields"),
                opt("conformal prediction"),
            ),
            "MLR is the first model; advanced methods come later.",
        ),
    ),
)
