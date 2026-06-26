"""Quiz questions for the QSAR & Pharmacophore Modeling - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "3D-QSAR: CoMFA and CoMSIA": (
            q(
                "In CoMFA, what is computed at each grid point?",
                (
                    opt("steric and electrostatic interaction energies with a probe", correct=True),
                    opt("the molecular weight"),
                    opt("the assay IC50"),
                    opt("the patent number"),
                ),
                "CoMFA grids hold Lennard-Jones and Coulombic probe energies, regressed by PLS.",
            ),
            q(
                "How does CoMSIA differ from CoMFA?",
                (
                    opt(
                        "it uses smooth Gaussian similarity fields and adds hydrophobic/HB fields",
                        correct=True,
                    ),
                    opt("it ignores all electrostatics"),
                    opt("it requires no alignment"),
                    opt("it uses only 2D descriptors"),
                ),
                "Gaussian functions avoid CoMFA's steep singularities near atoms.",
            ),
            q(
                "The biggest practical weakness of 3D-QSAR is:",
                (
                    opt("dependence on correct molecular alignment", correct=True),
                    opt("inability to use PLS"),
                    opt("requiring no conformations"),
                    opt("producing no contour maps"),
                ),
                "Poor alignment yields meaningless fields; bioactive conformation matters.",
            ),
        ),
        "Pharmacophore modeling": (
            q(
                "A pharmacophore describes:",
                (
                    opt(
                        "the spatial arrangement of features required for target interaction",
                        correct=True,
                    ),
                    opt("the exact atoms of one specific molecule"),
                    opt("the synthesis route"),
                    opt("the assay concentration"),
                ),
                "It is an abstract pattern of features, not specific atoms.",
            ),
            q(
                "A ligand-based pharmacophore is built by:",
                (
                    opt(
                        "aligning several known actives and extracting common features",
                        correct=True,
                    ),
                    opt("reading features from a protein structure only"),
                    opt("randomly placing spheres"),
                    opt("measuring melting points"),
                ),
                "Structure-based models instead read features from a complex or binding site.",
            ),
            q(
                "What do exclusion volumes in a pharmacophore represent?",
                (
                    opt("forbidden regions of space the ligand must avoid", correct=True),
                    opt("preferred hydrogen-bond donors"),
                    opt("the optimum logP"),
                    opt("the assay temperature"),
                ),
                "Exclusion volumes mark sterically forbidden space, improving selectivity.",
            ),
        ),
        "Pharmacophore-based virtual screening": (
            q(
                "Before matching a flexible molecule to a 3D pharmacophore, you must:",
                (
                    opt("generate plausible conformers", correct=True),
                    opt("crystallize it"),
                    opt("measure its IC50"),
                    opt("compute its price"),
                ),
                "Each molecule is expanded into conformers, then tested against the query spheres.",
            ),
            q(
                "What does the enrichment factor measure?",
                (
                    opt(
                        "how much the screen concentrates known actives near the top of the ranking",
                        correct=True,
                    ),
                    opt("the molecular weight of hits"),
                    opt("the number of atoms"),
                    opt("the solvent polarity"),
                ),
                "EF compares actives found in the top fraction to random expectation.",
            ),
            q(
                "Pharmacophore screening is often used as:",
                (
                    opt("a fast prefilter before slower molecular docking", correct=True),
                    opt("a replacement for synthesizing every molecule by hand"),
                    opt("a method to set assay pH"),
                    opt("a way to compute melting points"),
                ),
                "It shrinks the library that needs expensive docking and scoring.",
            ),
        ),
        "The applicability domain": (
            q(
                "The applicability domain of a QSAR model is:",
                (
                    opt(
                        "the region of descriptor space where predictions are reliable",
                        correct=True,
                    ),
                    opt("the list of authors"),
                    opt("the assay vendor"),
                    opt("the maximum molecular weight allowed by law"),
                ),
                "Predictions outside the AD are extrapolations and untrustworthy.",
            ),
            q(
                "The leverage approach to the applicability domain uses:",
                (
                    opt(
                        "the diagonal of the hat matrix with a warning value h* = 3p/n",
                        correct=True,
                    ),
                    opt("the molecular formula"),
                    opt("the synthesis yield"),
                    opt("the assay duration"),
                ),
                "Williams plots flag high-leverage compounds beyond h*.",
            ),
            q(
                "As a compound moves farther from the training data, prediction reliability:",
                (
                    opt("decreases", correct=True),
                    opt("increases"),
                    opt("stays perfectly constant"),
                    opt("becomes exactly 1"),
                ),
                "Reliability decays with distance from the training centroid.",
            ),
        ),
        "Deep learning and generative QSAR": (
            q(
                "What does transfer learning / pretraining provide for QSAR?",
                (
                    opt(
                        "a representation learned from large unlabeled data before fine-tuning on a small activity set",
                        correct=True,
                    ),
                    opt("a guarantee of zero error"),
                    opt("elimination of all descriptors"),
                    opt("a way to skip validation"),
                ),
                "Pretraining lifts the data-efficiency curve when labeled data are scarce.",
            ),
            q(
                "Multitask learning improves models by:",
                (
                    opt(
                        "training one network on many endpoints to borrow statistical strength",
                        correct=True,
                    ),
                    opt("using one descriptor only"),
                    opt("training a separate model per molecule"),
                    opt("ignoring all but one assay"),
                ),
                "Related endpoints share representation, helping data-poor tasks.",
            ),
            q(
                "Generative QSAR models (VAEs, RL agents) are used to:",
                (
                    opt("design new molecules optimized for predicted activity", correct=True),
                    opt("only fit existing data"),
                    opt("measure assay pH"),
                    opt("compute molecular weight faster"),
                ),
                "They invert QSAR to propose novel candidates in a design-make-test-analyze loop.",
            ),
        ),
        "Interpretability and regulatory QSAR": (
            q(
                "SHAP values are used in QSAR to:",
                (
                    opt("attribute a prediction to individual descriptors", correct=True),
                    opt("synthesize the molecule"),
                    opt("measure solubility"),
                    opt("set the assay temperature"),
                ),
                "SHAP and feature importance explain which inputs drive a prediction.",
            ),
            q(
                "How many OECD principles must a regulatory QSAR satisfy?",
                (
                    opt("five", correct=True),
                    opt("two"),
                    opt("ten"),
                    opt("zero"),
                ),
                "Defined endpoint, unambiguous algorithm, defined AD, statistics, and mechanism.",
            ),
            q(
                "Conformal prediction provides:",
                (
                    opt("calibrated prediction intervals quantifying confidence", correct=True),
                    opt("the exact synthesis cost"),
                    opt("the molecule's color"),
                    opt("a guarantee of zero uncertainty"),
                ),
                "Higher required coverage widens the interval, exposing the accuracy-confidence trade-off.",
            ),
        ),
    },
    final=(
        q(
            "CoMFA descriptors come from:",
            (
                opt("steric and electrostatic field energies on a 3D grid", correct=True),
                opt("a single logP value"),
                opt("the assay vendor"),
                opt("patent text"),
            ),
            "Grid probe energies are regressed against activity by PLS.",
        ),
        q(
            "A pharmacophore is an abstraction of:",
            (
                opt("the features and geometry required for target binding", correct=True),
                opt("the exact atoms of one molecule"),
                opt("the synthesis route"),
                opt("the price"),
            ),
            "Features like HBD/HBA, aromatic and hydrophobic groups in defined geometry.",
        ),
        q(
            "Virtual screening quality is commonly summarized by:",
            (
                opt("enrichment factor and ROC/AUC", correct=True),
                opt("molecular weight only"),
                opt("the number of authors"),
                opt("solvent boiling point"),
            ),
            "These quantify how well actives are ranked near the top.",
        ),
        q(
            "The applicability domain answers the question:",
            (
                opt(
                    "is this new compound similar enough to the training data to trust the prediction",
                    correct=True,
                ),
                opt("what is the molecule's price"),
                opt("who synthesized it"),
                opt("what is the assay pH"),
            ),
            "Outside the AD, predictions are unreliable extrapolations.",
        ),
        q(
            "A key advantage of graph neural networks over fixed fingerprints is:",
            (
                opt(
                    "they learn task-specific representations end to end from the graph",
                    correct=True,
                ),
                opt("they need no data"),
                opt("they ignore molecular structure"),
                opt("they cannot overfit"),
            ),
            "Learned representations can outperform fixed descriptors when data are abundant.",
        ),
        q(
            "The five OECD principles include all of the following EXCEPT:",
            (
                opt("a minimum acceptable retail price", correct=True),
                opt("a defined endpoint"),
                opt("a defined applicability domain"),
                opt("appropriate statistics for fit and predictivity"),
            ),
            "Price is not an OECD principle; endpoint, algorithm, AD, statistics and mechanism are.",
        ),
    ),
)
