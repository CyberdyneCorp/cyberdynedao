"""Quiz questions for the Capstone: End-to-End AI Drug Design Project - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Molecular dynamics: validating the binding pose": (
            q(
                "What does molecular dynamics add over a static docking pose?",
                (
                    opt(
                        "it simulates motion over time to test whether the pose is stable",
                        correct=True,
                    ),
                    opt("it predicts the compound price"),
                    opt("it generates new SMILES"),
                    opt("it replaces the need for any assay"),
                ),
                "MD integrates Newton's equations under a force field to test pose stability.",
            ),
            q(
                "Which readout indicates a stable binding pose during MD?",
                (
                    opt("ligand RMSD that settles to a low plateau", correct=True),
                    opt("RMSD that grows without bound"),
                    opt("a higher molecular weight"),
                    opt("a shorter SMILES string"),
                ),
                "A pose that drifts away (rising RMSD) was likely a docking artifact.",
            ),
            q(
                "Why is MD reserved for only the top candidates?",
                (
                    opt("it is computationally expensive", correct=True),
                    opt("it is forbidden for large libraries"),
                    opt("it requires no force field"),
                    opt("it is less accurate than docking"),
                ),
                "MD is costly, so it filters the handful of best poses, not the whole library.",
            ),
        ),
        "Free-energy calculations and binding affinity": (
            q(
                "What does free-energy perturbation (FEP) compute?",
                (
                    opt("the relative binding free energy between similar ligands", correct=True),
                    opt("the absolute price of synthesis"),
                    opt("the protein sequence"),
                    opt("the assay vendor"),
                ),
                "FEP alchemically transforms one ligand into another to get deltadeltaG.",
            ),
            q(
                "MM-GBSA / MM-PBSA is best described as:",
                (
                    opt(
                        "a cheaper end-point estimate of binding energy from MD snapshots",
                        correct=True,
                    ),
                    opt("a generative model"),
                    opt("a fingerprint type"),
                    opt("a database of structures"),
                ),
                "It is a faster middle ground between docking scores and rigorous FEP.",
            ),
            q(
                "Why is FEP applied only to closely related (congeneric) candidates?",
                (
                    opt(
                        "it is accurate but costly, best for relative ranking of similar ligands",
                        correct=True,
                    ),
                    opt("it cannot handle any small molecule"),
                    opt("it is faster than docking on huge libraries"),
                    opt("it ignores the protein entirely"),
                ),
                "FEP gives ~1 kcal/mol accuracy on congeneric series but is expensive.",
            ),
        ),
        "ADMET and off-target risk prediction": (
            q(
                "What does ADMET stand for?",
                (
                    opt("Absorption, Distribution, Metabolism, Excretion, Toxicity", correct=True),
                    opt("Activity, Docking, Modeling, Energy, Training"),
                    opt("Affinity, Dose, Mass, Excretion, Time"),
                    opt("Assay, Data, Model, Evaluate, Test"),
                ),
                "ADMET captures what the body does to a drug and how it harms.",
            ),
            q(
                "Which toxicity endpoint is a major cardiac liability to predict?",
                (
                    opt("hERG channel block", correct=True),
                    opt("high logP only"),
                    opt("low molecular weight"),
                    opt("a long SMILES string"),
                ),
                "hERG block can cause dangerous cardiac arrhythmia.",
            ),
            q(
                "Why predict ADMET early in the project?",
                (
                    opt(
                        "poor ADMET drives most late-stage failures, so early triage protects the project",
                        correct=True,
                    ),
                    opt("ADMET is irrelevant to drugs"),
                    opt("it sets the marketing name"),
                    opt("it replaces docking"),
                ),
                "Catching ADMET problems early avoids expensive late failures.",
            ),
        ),
        "Closing the loop with active learning": (
            q(
                "Active learning proposes the next experiments by balancing:",
                (
                    opt("exploitation (predicted-best) and exploration (uncertain)", correct=True),
                    opt("file size and memory"),
                    opt("color and shape"),
                    opt("training and inference speed"),
                ),
                "The acquisition function trades off mean and uncertainty.",
            ),
            q(
                "The UCB acquisition function alpha = mu(x) + kappa*sigma(x) rewards:",
                (
                    opt("high predicted value and high uncertainty", correct=True),
                    opt("low value and low uncertainty"),
                    opt("only molecular weight"),
                    opt("only the training-set mean"),
                ),
                "UCB favors candidates that are promising or informative (uncertain).",
            ),
            q(
                "In active learning, what becomes the binding constraint?",
                (
                    opt("cost per experimental cycle", correct=True),
                    opt("the number of SMILES characters"),
                    opt("the screen color"),
                    opt("the file format"),
                ),
                "Each cycle improves the best candidate with diminishing returns, so cost dominates.",
            ),
        ),
        "Uncertainty quantification and decision risk": (
            q(
                "Aleatoric uncertainty refers to:",
                (
                    opt("irreducible noise in the measurements/assay", correct=True),
                    opt("the model not having seen similar chemistry"),
                    opt("a bug in the code"),
                    opt("the GPU temperature"),
                ),
                "Aleatoric is data noise; epistemic is model ignorance.",
            ),
            q(
                "Which method gives calibrated prediction intervals with guaranteed coverage?",
                (
                    opt("conformal prediction", correct=True),
                    opt("a single random forest point estimate"),
                    opt("alphabetical sorting"),
                    opt("docking score alone"),
                ),
                "Conformal prediction provides intervals with a guaranteed coverage rate.",
            ),
            q(
                "Epistemic uncertainty typically behaves how relative to the training data?",
                (
                    opt("it grows for molecules far from training data", correct=True),
                    opt("it is constant everywhere"),
                    opt("it shrinks far from training data"),
                    opt("it depends only on molecular weight"),
                ),
                "Well-calibrated epistemic uncertainty rises away from seen chemistry.",
            ),
        ),
        "Assembling the decision dossier": (
            q(
                "What is the final deliverable of the project?",
                (
                    opt("a decision dossier justifying ranked recommendations", correct=True),
                    opt("a single trained model file"),
                    opt("a raw SMILES dump"),
                    opt("the GPU logs"),
                ),
                "The project ends with a defensible decision, documented in a dossier.",
            ),
            q(
                "A desirability function D = (product of d_i)^(1/n) enforces balance because:",
                (
                    opt("any single zero desirability kills the candidate", correct=True),
                    opt("it ignores all but one property"),
                    opt("it always equals 1"),
                    opt("it maximizes molecular weight"),
                ),
                "The geometric mean is zero if any property is unacceptable, enforcing trade-offs.",
            ),
            q(
                "Why reason over a Pareto front of candidates?",
                (
                    opt(
                        "no candidate wins on every objective; you want non-dominated trade-offs",
                        correct=True,
                    ),
                    opt("there is always one perfect molecule"),
                    opt("objectives never conflict"),
                    opt("the front removes the need for data"),
                ),
                "Conflicting objectives yield a set of non-dominated, Pareto-optimal candidates.",
            ),
        ),
    },
    final=(
        q(
            "Why run molecular dynamics on top docked candidates?",
            (
                opt("to test whether the binding pose stays stable under motion", correct=True),
                opt("to generate new molecules"),
                opt("to compute the compound price"),
                opt("to replace the assay entirely"),
            ),
            "MD checks pose stability that static docking cannot reveal.",
        ),
        q(
            "FEP is best suited to:",
            (
                opt("ranking the relative affinity of closely related ligands", correct=True),
                opt("screening a billion-compound library quickly"),
                opt("predicting protein sequence"),
                opt("generating SMILES"),
            ),
            "FEP is accurate but costly, ideal for congeneric relative ranking.",
        ),
        q(
            "Which ADMET endpoint is the classic cardiac toxicity flag?",
            (
                opt("hERG channel block", correct=True),
                opt("blood-brain barrier penetration"),
                opt("aqueous solubility"),
                opt("metabolic clearance"),
            ),
            "hERG block is a major cardiac liability to predict early.",
        ),
        q(
            "Active learning improves the project by:",
            (
                opt("choosing the most informative or promising next experiments", correct=True),
                opt("testing every compound at random"),
                opt("removing the need to retrain"),
                opt("ignoring uncertainty"),
            ),
            "It closes the DMTA loop by balancing exploitation and exploration.",
        ),
        q(
            "Which uncertainty grows for molecules far from the training data?",
            (
                opt("epistemic uncertainty", correct=True),
                opt("aleatoric uncertainty"),
                opt("molecular weight"),
                opt("the docking score"),
            ),
            "Epistemic (model) uncertainty rises out of the applicability domain.",
        ),
        q(
            "A good decision dossier is honest by stating:",
            (
                opt(
                    "the applicability domain, uncertainty and assumptions behind each recommendation",
                    correct=True,
                ),
                opt("only the single best benchmark score"),
                opt("nothing about uncertainty"),
                opt("just the model architecture"),
            ),
            "It hands a defensible, caveated decision to the next team.",
        ),
    ),
)
