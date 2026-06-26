"""Quiz questions for the ADMET & Toxicity Prediction - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "hERG and cardiotoxicity prediction": (
            q(
                "Blocking the hERG channel can lead to which dangerous outcome?",
                (
                    opt("QT prolongation and torsades de pointes", correct=True),
                    opt("Increased solubility"),
                    opt("Faster renal excretion"),
                    opt("Stronger target binding"),
                ),
                "hERG block prolongs cardiac repolarization, risking arrhythmia.",
            ),
            q(
                "How is the hERG safety margin usually expressed?",
                (
                    opt("Ratio of hERG IC50 to free therapeutic concentration", correct=True),
                    opt("Molecular weight over logP"),
                    opt("Half-life times clearance"),
                    opt("Number of rotatable bonds"),
                ),
                "Margins below about 30-fold raise cardiotoxicity concern.",
            ),
            q(
                "Which property change commonly reduces hERG liability?",
                (
                    opt("Lowering basicity (pKa) or lipophilicity", correct=True),
                    opt("Increasing molecular weight"),
                    opt("Adding more aromatic rings"),
                    opt("Raising the number of H-bond donors only"),
                ),
                "hERG binds basic, lipophilic drugs; reducing these mitigates block.",
            ),
        ),
        "Hepatotoxicity, mutagenicity and structural alerts": (
            q(
                "What is a key mechanism of drug-induced liver injury?",
                (
                    opt("Bioactivation to a reactive metabolite", correct=True),
                    opt("Excess aqueous solubility"),
                    opt("Strong target potency"),
                    opt("Low molecular weight"),
                ),
                "Reactive metabolites covalently bind proteins/DNA, causing injury.",
            ),
            q(
                "What is the regulatory standard test for mutagenicity?",
                (
                    opt("The Ames bacterial reverse-mutation test", correct=True),
                    opt("The Caco-2 assay"),
                    opt("Equilibrium dialysis"),
                    opt("PAMPA"),
                ),
                "The Ames test is the standard for bacterial mutagenicity.",
            ),
            q(
                "How should structural alerts be interpreted?",
                (
                    opt("Sensitive but not specific; they prioritize follow-up", correct=True),
                    opt("As definitive proof a drug is toxic"),
                    opt("As a measure of solubility"),
                    opt("As irrelevant to safety"),
                ),
                "Many safe drugs contain alerting groups that are detoxified.",
            ),
        ),
        "Deep learning for ADMET: graph nets, multitask, uncertainty": (
            q(
                "How does a graph neural network represent a molecule?",
                (
                    opt("Atoms as nodes and bonds as edges with message passing", correct=True),
                    opt("As a single scalar descriptor"),
                    opt("As a fixed SMILES character count"),
                    opt("As a 3D crystal lattice only"),
                ),
                "GNNs pass messages between neighbouring atoms to learn features.",
            ),
            q(
                "Why can multitask learning help data-poor ADMET endpoints?",
                (
                    opt("Correlated tasks share a learned representation", correct=True),
                    opt("It removes the need for any data"),
                    opt("It guarantees zero error"),
                    opt("It only works for one endpoint"),
                ),
                "Sharing representations transfers signal from data-rich to data-poor tasks.",
            ),
            q(
                "Which method gives calibrated prediction intervals with coverage guarantees?",
                (
                    opt("Conformal prediction", correct=True),
                    opt("Random splitting"),
                    opt("One-hot encoding"),
                    opt("Gradient descent alone"),
                ),
                "Conformal prediction provides intervals with formal coverage.",
            ),
        ),
        "PBPK modelling: mechanistic whole-body simulation": (
            q(
                "How does a PBPK model represent the body?",
                (
                    opt("Physiological compartments linked by blood flow", correct=True),
                    opt("A single empirical regression line"),
                    opt("A fixed lookup table of doses"),
                    opt("Only the gut"),
                ),
                "PBPK uses organ compartments with mass-balance equations.",
            ),
            q(
                "A major advantage of PBPK is predicting:",
                (
                    opt("Dosing for special populations and DDIs without new trials", correct=True),
                    opt("The synthetic route to a molecule"),
                    opt("The crystal structure of the target"),
                    opt("The Tanimoto similarity of two drugs"),
                ),
                "PBPK extrapolates to pediatric, impaired or interacting scenarios.",
            ),
            q(
                "What inputs does a PBPK model combine?",
                (
                    opt("Physiology plus drug-specific ADMET parameters", correct=True),
                    opt("Only the molecular weight"),
                    opt("Only the SMILES string"),
                    opt("Only clinical trial outcomes"),
                ),
                "Physiology data plus f_u, CL_int, P_app, logP drive the simulation.",
            ),
        ),
        "In-silico ADMET pipelines and design triage": (
            q(
                "What is multi-parameter optimization (MPO) in ADMET design?",
                (
                    opt(
                        "Combining endpoints into a single desirability that respects trade-offs",
                        correct=True,
                    ),
                    opt("Optimizing only potency"),
                    opt("Removing all filters"),
                    opt("Ignoring toxicity endpoints"),
                ),
                "MPO scores balance many endpoints rather than pass/fail per axis.",
            ),
            q(
                "What makes an in-silico ADMET pipeline trustworthy over time?",
                (
                    opt("Tracking prospective accuracy as new assay data arrives", correct=True),
                    opt("Never updating the models"),
                    opt("Hiding the uncertainty"),
                    opt("Using only one molecule for training"),
                ),
                "Closing the loop with prospective validation keeps models honest.",
            ),
            q(
                "In the DMTA loop, when is ADMET prediction now applied?",
                (
                    opt("Before synthesis, to triage designed molecules", correct=True),
                    opt("Only after clinical trials"),
                    opt("Only during manufacturing"),
                    opt("Never, it is purely experimental"),
                ),
                "Predictions prioritize which molecules to make and test.",
            ),
        ),
    },
    final=(
        q(
            "The hERG channel carries which cardiac current?",
            (
                opt("The repolarizing potassium current I_Kr", correct=True),
                opt("The fast sodium current"),
                opt("The L-type calcium current"),
                opt("The pacemaker funny current"),
            ),
            "hERG conducts I_Kr, key to ventricular repolarization.",
        ),
        q(
            "Under ICH M7, impurity mutagenicity can be assessed by:",
            (
                opt("Two complementary (Q)SAR systems", correct=True),
                opt("A single PBPK simulation"),
                opt("The Caco-2 assay"),
                opt("logP calculation alone"),
            ),
            "M7 allows an expert-rule plus a statistical QSAR in place of testing.",
        ),
        q(
            "Which is a widely used directed message-passing model for ADMET?",
            (
                opt("Chemprop", correct=True),
                opt("BLAST"),
                opt("AlphaFold"),
                opt("Clustal"),
            ),
            "Chemprop is a strong D-MPNN baseline for molecular property prediction.",
        ),
        q(
            "Which platform is an open-source PBPK tool?",
            (
                opt("PK-Sim / OSP", correct=True),
                opt("PyMOL"),
                opt("Excel only"),
                opt("ImageJ"),
            ),
            "PK-Sim (Open Systems Pharmacology) is open-source PBPK software.",
        ),
        q(
            "Why must ADMET predictions carry uncertainty estimates?",
            (
                opt("To flag molecules outside the applicability domain", correct=True),
                opt("To increase model size"),
                opt("To slow down inference"),
                opt("To avoid using any data"),
            ),
            "Uncertainty tells chemists when to distrust a prediction.",
        ),
        q(
            "Benchmarks such as TDC and MoleculeNet provide:",
            (
                opt("Standardized ADMET datasets and splits for fair comparison", correct=True),
                opt("Patient clinical records"),
                opt("Synthetic chemistry recipes"),
                opt("Regulatory approval"),
            ),
            "They standardize data and scaffold splits so methods compare fairly.",
        ),
    ),
)
