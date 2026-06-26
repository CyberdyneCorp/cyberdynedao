"""Quiz questions for the Capstone: End-to-End AI Drug Design Project - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Building the QSAR activity model": (
            q(
                "What does a QSAR model predict?",
                (
                    opt("activity (e.g. pIC50) from molecular structure", correct=True),
                    opt("the price of a compound"),
                    opt("the protein's amino-acid sequence"),
                    opt("the country a drug is sold in"),
                ),
                "QSAR learns activity as a function of structure-derived features.",
            ),
            q(
                "What is a strong, fast baseline model for small-to-medium chemical datasets?",
                (
                    opt("a random forest or gradient boosting on ECFP", correct=True),
                    opt("a billion-parameter language model from scratch"),
                    opt("a hand-written if-else rule per molecule"),
                    opt("a spreadsheet sort"),
                ),
                "Tree ensembles on fingerprints are hard to beat without far more data.",
            ),
            q(
                "QSAR predictive skill as data grows tends to:",
                (
                    opt("rise then saturate, bounded by assay noise", correct=True),
                    opt("rise without limit forever"),
                    opt("fall as data is added"),
                    opt("stay exactly constant"),
                ),
                "Skill saturates and is capped by experimental noise in the assay.",
            ),
        ),
        "Validating the model honestly": (
            q(
                "Why prefer a scaffold split over a random split?",
                (
                    opt("it forces the model to generalize to novel chemical series", correct=True),
                    opt("it always gives higher scores"),
                    opt("it is faster to compute"),
                    opt("it removes the need for a test set"),
                ),
                "Real use requires predicting novel scaffolds, which random splits hide.",
            ),
            q(
                "What is data leakage in this context?",
                (
                    opt(
                        "test information (e.g. near-duplicates or test-set scaling) influencing training",
                        correct=True,
                    ),
                    opt("a molecule dissolving in water"),
                    opt("a slow database query"),
                    opt("a missing license file"),
                ),
                "Leakage inflates scores; near-duplicates across the split are a common cause.",
            ),
            q(
                "A prediction is most trustworthy when the molecule is:",
                (
                    opt("inside the applicability domain (near training data)", correct=True),
                    opt("far from any training example"),
                    opt("the heaviest in the library"),
                    opt("randomly generated"),
                ),
                "Low-similarity, out-of-domain molecules should be flagged as uncertain.",
            ),
        ),
        "Running the virtual screen": (
            q(
                "Why is enrichment, not accuracy, the right screen metric?",
                (
                    opt(
                        "actives are rare (often under 1%), so accuracy is misleading", correct=True
                    ),
                    opt("accuracy cannot be computed for molecules"),
                    opt("enrichment is easier to spell"),
                    opt("regulators forbid accuracy"),
                ),
                "With extreme class imbalance, a high accuracy can be achieved by predicting all inactive.",
            ),
            q(
                "Ligand-based virtual screening scores library molecules by:",
                (
                    opt("a QSAR model or similarity to known actives", correct=True),
                    opt("their melting point only"),
                    opt("alphabetical order of SMILES"),
                    opt("the protein's pLDDT"),
                ),
                "Ligand-based VS uses learned activity or similarity to knowns.",
            ),
            q(
                "BEDROC improves on plain ROC-AUC by:",
                (
                    opt(
                        "up-weighting actives ranked near the top (early recognition)", correct=True
                    ),
                    opt("ignoring the actives entirely"),
                    opt("counting only the bottom of the list"),
                    opt("requiring a 3D structure"),
                ),
                "BEDROC rewards finding actives early, which matters when you test only the top fraction.",
            ),
        ),
        "Docking the shortlist": (
            q(
                "Molecular docking consists of which two parts?",
                (
                    opt("a pose search and a scoring function", correct=True),
                    opt("a training loop and a test set"),
                    opt("synthesis and assay"),
                    opt("encoder and decoder"),
                ),
                "Docking searches over poses and scores them.",
            ),
            q(
                "Binding free energy relates to the dissociation constant by:",
                (
                    opt(
                        "deltaG = RT ln Kd, so tighter binders have more negative deltaG",
                        correct=True,
                    ),
                    opt("deltaG = Kd squared"),
                    opt("deltaG is independent of Kd"),
                    opt("deltaG = molecular weight times Kd"),
                ),
                "Smaller Kd (tighter binding) corresponds to more negative deltaG.",
            ),
            q(
                "Why inspect the docked pose, not just the score?",
                (
                    opt(
                        "classical scores are noisy; a good score can still be an artifact",
                        correct=True,
                    ),
                    opt("inspection changes the score automatically"),
                    opt("the score is always wrong"),
                    opt("poses cannot be visualized"),
                ),
                "Check that key interactions are present rather than trusting the number blindly.",
            ),
        ),
        "Generating new candidate molecules": (
            q(
                "What advantage does SELFIES have over plain SMILES for generation?",
                (
                    opt("every SELFIES string decodes to a valid molecule", correct=True),
                    opt("SELFIES strings are always shorter"),
                    opt("SELFIES encodes 3D coordinates"),
                    opt("SELFIES requires no training"),
                ),
                "SELFIES guarantees validity, avoiding invalid generated structures.",
            ),
            q(
                "Generation should be constrained by which guard, among others?",
                (
                    opt("synthetic accessibility (SA score)", correct=True),
                    opt("the alphabetical order of atoms"),
                    opt("the protein's molecular weight"),
                    opt("the assay vendor name"),
                ),
                "Validity, novelty and SA score keep generated molecules makeable and meaningful.",
            ),
            q(
                "What is reward hacking in generative design?",
                (
                    opt(
                        "the model exploits the oracle, proposing unrealistic high-scoring molecules",
                        correct=True,
                    ),
                    opt("the model refuses to generate anything"),
                    opt("the assay produces too many hits"),
                    opt("the GPU overheats"),
                ),
                "An over-trusted oracle gets gamed into adversarial, unsynthesizable structures.",
            ),
        ),
        "Reading the metrics that gate each stage": (
            q(
                "Which metric set is appropriate for the QSAR regression model?",
                (
                    opt("R-squared and RMSE on a scaffold split", correct=True),
                    opt("enrichment factor only"),
                    opt("SA score and novelty"),
                    opt("plain accuracy on a random split"),
                ),
                "Regression quality is read from R^2/RMSE under an honest split.",
            ),
            q(
                "For a rare-active classification, the F1 score balances:",
                (
                    opt("precision and recall", correct=True),
                    opt("speed and memory"),
                    opt("logP and TPSA"),
                    opt("training and test loss"),
                ),
                "F1 = 2PR/(P+R) trades off precision against recall.",
            ),
            q(
                "A common mistake when evaluating a virtual screen is:",
                (
                    opt("reporting plain accuracy instead of enrichment / ROC-AUC", correct=True),
                    opt("computing the enrichment factor"),
                    opt("using a scaffold split"),
                    opt("flagging out-of-domain molecules"),
                ),
                "Accuracy is meaningless at 1% actives; use enrichment-based metrics.",
            ),
        ),
    },
    final=(
        q(
            "What does the QSAR model in the project predict?",
            (
                opt("activity such as pIC50 from molecular structure", correct=True),
                opt("the protein 3D fold"),
                opt("the synthesis cost"),
                opt("the clinical trial outcome"),
            ),
            "QSAR maps structure-derived features to activity.",
        ),
        q(
            "Which validation choice best reflects real-world generalization?",
            (
                opt("a scaffold split", correct=True),
                opt("a random split"),
                opt("training and testing on the same set"),
                opt("no validation"),
            ),
            "Scaffold splits force generalization across chemical series.",
        ),
        q(
            "The enrichment factor measures:",
            (
                opt(
                    "how many actives appear in the top fraction vs random expectation",
                    correct=True,
                ),
                opt("the molecular weight of the library"),
                opt("the number of training epochs"),
                opt("the protein's pLDDT"),
            ),
            "EF compares actives found early against random chance.",
        ),
        q(
            "Docking estimates binding by combining a pose search with:",
            (
                opt("a scoring function", correct=True),
                opt("a random forest only"),
                opt("a SMILES tokenizer"),
                opt("an assay protocol"),
            ),
            "The scoring function ranks the poses found by the search.",
        ),
        q(
            "A key guard on generative design is:",
            (
                opt("synthetic accessibility, validity and novelty", correct=True),
                opt("maximizing molecular weight"),
                opt("ignoring the QSAR oracle"),
                opt("alphabetizing the output"),
            ),
            "These guards keep generated molecules makeable and genuinely new.",
        ),
        q(
            "Matching metric to stage, virtual screening should be judged by:",
            (
                opt("enrichment factor, ROC-AUC or BEDROC", correct=True),
                opt("plain accuracy"),
                opt("RMSE of pIC50"),
                opt("the SA score alone"),
            ),
            "Rare actives demand enrichment-based metrics, not accuracy.",
        ),
    ),
)
