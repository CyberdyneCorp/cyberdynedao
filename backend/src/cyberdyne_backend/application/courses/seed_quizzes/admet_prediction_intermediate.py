"""Quiz questions for the ADMET & Toxicity Prediction - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Permeability: Caco-2, PAMPA and predictive models": (
            q(
                "What does the PAMPA assay primarily measure?",
                (
                    opt("Passive membrane permeability only", correct=True),
                    opt("Active transporter-mediated uptake"),
                    opt("Metabolic clearance"),
                    opt("Plasma protein binding"),
                ),
                "PAMPA is a cell-free lipid membrane measuring passive permeability.",
            ),
            q(
                "An efflux ratio greater than 2 in Caco-2 typically flags:",
                (
                    opt("P-glycoprotein efflux", correct=True),
                    opt("High aqueous solubility"),
                    opt("Rapid metabolism"),
                    opt("Strong protein binding"),
                ),
                "A high efflux ratio indicates active efflux, commonly by P-gp.",
            ),
            q(
                "What does the apparent permeability P_app describe?",
                (
                    opt(
                        "The rate of transport across the membrane per area and donor concentration",
                        correct=True,
                    ),
                    opt("The fraction of drug metabolized"),
                    opt("The volume of distribution"),
                    opt("The drug's half-life"),
                ),
                "P_app = (1/(A*C0)) * dQ/dt, the normalized transport rate.",
            ),
        ),
        "Metabolism kinetics: Michaelis-Menten and clearance": (
            q(
                "In the Michaelis-Menten equation, what is K_m?",
                (
                    opt("The substrate concentration giving half of Vmax", correct=True),
                    opt("The maximum reaction rate"),
                    opt("The enzyme concentration"),
                    opt("The half-life of the drug"),
                ),
                "K_m is the [S] at which v equals half of Vmax.",
            ),
            q(
                "In the linear (low [S]) regime, intrinsic clearance equals:",
                (
                    opt("Vmax / Km", correct=True),
                    opt("Km / Vmax"),
                    opt("Vmax * Km"),
                    opt("Km - Vmax"),
                ),
                "At low substrate, CL_int = Vmax/Km.",
            ),
            q(
                "For a high-extraction drug, hepatic clearance is mainly limited by:",
                (
                    opt("Hepatic blood flow Q_H", correct=True),
                    opt("Intrinsic clearance"),
                    opt("Renal filtration"),
                    opt("Gut absorption"),
                ),
                "High-extraction drugs are flow-limited; low-extraction are CL_int-limited.",
            ),
        ),
        "Cytochrome P450 and drug-drug interactions": (
            q(
                "Which CYP isoform metabolizes the largest share of drugs?",
                (
                    opt("CYP3A4", correct=True),
                    opt("CYP2D6"),
                    opt("CYP1A2"),
                    opt("CYP2C19"),
                ),
                "CYP3A4 handles roughly half of metabolized drugs.",
            ),
            q(
                "A CYP inhibitor co-dosed with a substrate tends to:",
                (
                    opt("Raise the substrate's plasma levels", correct=True),
                    opt("Lower the substrate's plasma levels"),
                    opt("Have no effect on the substrate"),
                    opt("Permanently destroy the enzyme gene"),
                ),
                "Inhibition slows metabolism, raising substrate concentration.",
            ),
            q(
                "What does CYP2D6 genotype variation cause?",
                (
                    opt("Differing metabolizer phenotypes among patients", correct=True),
                    opt("Identical drug response in all patients"),
                    opt("Loss of all P450 activity"),
                    opt("Changes only in absorption"),
                ),
                "Poor to ultrarapid metabolizer genotypes change drug handling between patients.",
            ),
        ),
        "Plasma protein binding and the free drug hypothesis": (
            q(
                "What does the free drug hypothesis state?",
                (
                    opt("Only unbound drug drives efficacy and clearance", correct=True),
                    opt("Total concentration alone determines effect"),
                    opt("Bound drug is the active species"),
                    opt("Binding has no effect on pharmacology"),
                ),
                "At steady state, free plasma concentration equals that at the target.",
            ),
            q(
                "Which plasma protein chiefly binds acidic drugs?",
                (
                    opt("Albumin", correct=True),
                    opt("Hemoglobin"),
                    opt("Insulin"),
                    opt("Fibrinogen"),
                ),
                "Albumin is the main carrier for acidic, lipophilic drugs.",
            ),
            q(
                "Does very high protein binding automatically mean low efficacy?",
                (
                    opt("No, absolute free concentration is what matters", correct=True),
                    opt("Yes, bound drug is always wasted"),
                    opt("Yes, it always blocks the target"),
                    opt("Only if the drug is acidic"),
                ),
                "High f_bound alone is not a problem; the free level drives effect.",
            ),
        ),
        "Building and validating QSAR/QSPR models": (
            q(
                "Why are random train/test splits problematic for ADMET QSAR?",
                (
                    opt("They leak similar molecules and inflate performance", correct=True),
                    opt("They make training too slow"),
                    opt("They require deep learning only"),
                    opt("They cannot use fingerprints"),
                ),
                "Scaffold or time splits better mimic prospective use.",
            ),
            q(
                "What is the applicability domain of a model?",
                (
                    opt("The chemical space where predictions are reliable", correct=True),
                    opt("The list of authors who built it"),
                    opt("The runtime of the model"),
                    opt("The number of training epochs"),
                ),
                "Predictions for molecules unlike the training set are untrustworthy.",
            ),
            q(
                "For ADMET datasets, what often matters more than raw data quantity?",
                (
                    opt("Data quality and chemical diversity", correct=True),
                    opt("Using the largest possible neural net"),
                    opt("Always using random splits"),
                    opt("Ignoring uncertainty"),
                ),
                "Clean, diverse data frequently beats more noisy data.",
            ),
        ),
    },
    final=(
        q(
            "Which assay captures both passive diffusion and active transport?",
            (
                opt("Caco-2 cell monolayer", correct=True),
                opt("PAMPA"),
                opt("Equilibrium dialysis"),
                opt("Ames test"),
            ),
            "Caco-2 cells express transporters and tight junctions.",
        ),
        q(
            "The well-stirred model relates CL_H to Q_H, f_u and CL_int. When f_u*CL_int << Q_H, CL_H approaches:",
            (
                opt("f_u * CL_int", correct=True),
                opt("Q_H"),
                opt("Vmax * Km"),
                opt("Zero"),
            ),
            "Low-extraction drugs are limited by intrinsic clearance and unbound fraction.",
        ),
        q(
            "DDI risk from CYP inhibition scales approximately with:",
            (
                opt("[I]/Ki", correct=True),
                opt("Ki/[I]"),
                opt("[I]*Ki"),
                opt("Ki - [I]"),
            ),
            "Interaction magnitude grows with inhibitor concentration over Ki.",
        ),
        q(
            "Which equation describes saturable enzyme metabolism?",
            (
                opt("v = Vmax[S]/(Km+[S])", correct=True),
                opt("v = k[S]^2"),
                opt("v = Vmax + Km[S]"),
                opt("v = [S]/Vmax"),
            ),
            "Michaelis-Menten kinetics describe enzyme-catalysed metabolism.",
        ),
        q(
            "Which split best simulates prospective ADMET prediction?",
            (
                opt("Scaffold or time split", correct=True),
                opt("Pure random split"),
                opt("Alphabetical split"),
                opt("No split at all"),
            ),
            "Scaffold/time splits avoid leaking near-identical molecules.",
        ),
        q(
            "What is IVIVE used for?",
            (
                opt("Scaling in-vitro clearance to in-vivo hepatic clearance", correct=True),
                opt("Measuring protein binding directly"),
                opt("Predicting toxicity structural alerts"),
                opt("Calculating molecular weight"),
            ),
            "In-vitro-to-in-vivo extrapolation scales CL_int to whole-liver clearance.",
        ),
    ),
)
