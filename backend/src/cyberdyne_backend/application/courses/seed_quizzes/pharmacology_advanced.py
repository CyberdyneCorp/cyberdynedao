"""Quiz questions for the Pharmacology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "ADME: the full journey of a drug": (
            q(
                "Phase II metabolism mainly involves:",
                (
                    opt("Conjugation reactions such as glucuronidation", correct=True),
                    opt("Oxidation by cytochrome P450"),
                    opt("Glomerular filtration"),
                    opt("Protein binding to albumin"),
                ),
                "Phase II attaches polar groups (glucuronide, sulfate, glutathione) to ease excretion.",
            ),
            q(
                "Which barrier uses P-glycoprotein efflux to keep drugs out of the CNS?",
                (
                    opt("The blood-brain barrier", correct=True),
                    opt("The glomerular membrane"),
                    opt("The gut lumen"),
                    opt("The alveolar wall"),
                ),
                "The blood-brain barrier's P-gp pumps exclude many drugs from the CNS.",
            ),
            q(
                "Drug ionisation across membranes is governed by:",
                (
                    opt("The Henderson-Hasselbalch balance of pKa and local pH", correct=True),
                    opt("The Hill coefficient"),
                    opt("The volume of distribution alone"),
                    opt("The Michaelis constant"),
                ),
                "Henderson-Hasselbalch relates pKa and pH to the ionised fraction.",
            ),
        ),
        "Toxicology and dose-response thresholds": (
            q(
                "The NOAEL is:",
                (
                    opt("The highest dose with no observed adverse effect", correct=True),
                    opt("The dose that kills half the population"),
                    opt("The half-maximal effective dose"),
                    opt("The maximal achievable effect"),
                ),
                "NOAEL anchors safe-exposure estimates via uncertainty factors.",
            ),
            q(
                "Acetaminophen overdose toxicity is caused by:",
                (
                    opt("The reactive metabolite NAPQI depleting glutathione", correct=True),
                    opt("The parent drug binding hERG"),
                    opt("Excess Phase II conjugation"),
                    opt("Renal P-glycoprotein"),
                ),
                "In overdose, CYP2E1 generates NAPQI; N-acetylcysteine replenishes glutathione.",
            ),
            q(
                "Screening for hERG channel block during development predicts:",
                (
                    opt("QT prolongation / cardiac risk", correct=True),
                    opt("Improved bioavailability"),
                    opt("Faster absorption"),
                    opt("Higher potency"),
                ),
                "hERG block is associated with QT prolongation and arrhythmia risk.",
            ),
        ),
        "Pharmacogenomics and personalised dosing": (
            q(
                "A CYP2D6 ultra-rapid metaboliser given codeine risks:",
                (
                    opt("Excess morphine and toxicity", correct=True),
                    opt("No conversion and total toxicity from codeine"),
                    opt("Complete lack of any metabolism"),
                    opt("Reduced renal excretion only"),
                ),
                "Ultra-rapid metabolisers convert too much prodrug codeine to morphine.",
            ),
            q(
                "Genotyping HLA-B*57:01 before prescribing helps avoid:",
                (
                    opt("Abacavir hypersensitivity", correct=True),
                    opt("Warfarin overdose"),
                    opt("Clopidogrel failure"),
                    opt("Thiopurine toxicity"),
                ),
                "HLA-B*57:01 predicts abacavir hypersensitivity and is screened beforehand.",
            ),
            q(
                "Consortia like CPIC provide:",
                (
                    opt("Gene-drug dosing guidelines", correct=True),
                    opt("Manufacturing standards"),
                    opt("Patent filings"),
                    opt("Marketing approvals"),
                ),
                "CPIC translates genotype into actionable dosing recommendations.",
            ),
        ),
        "PK/PD modelling and simulation": (
            q(
                "Beta-lactam antibiotics are best dosed to maximise:",
                (
                    opt("Time the concentration stays above the MIC", correct=True),
                    opt("Peak concentration only"),
                    opt("The Hill coefficient"),
                    opt("The volume of distribution"),
                ),
                "Beta-lactams are time-dependent: time above MIC drives efficacy.",
            ),
            q(
                "Hysteresis between concentration and effect is modelled with:",
                (
                    opt("An effect-compartment or indirect-response model", correct=True),
                    opt("A simple linear regression"),
                    opt("A zero-order absorption model"),
                    opt("The therapeutic index"),
                ),
                "These models capture the lag between plasma level and biological effect.",
            ),
            q(
                "Population PK (e.g. NONMEM) separates which two effect types?",
                (
                    opt(
                        "Fixed effects (covariates) and random effects (variability)", correct=True
                    ),
                    opt("Agonist and antagonist effects"),
                    opt("Phase I and Phase II effects"),
                    opt("Absorption and excretion effects"),
                ),
                "Nonlinear mixed-effects models split covariate fixed effects from between-patient variability.",
            ),
        ),
        "AI and computational drug discovery": (
            q(
                "AlphaFold contributes to drug discovery mainly by:",
                (
                    opt("Predicting target protein structures for docking", correct=True),
                    opt("Synthesising compounds in the lab"),
                    opt("Running clinical trials"),
                    opt("Measuring half-lives"),
                ),
                "Predicted structures enable structure-based design and docking.",
            ),
            q(
                "Graph neural networks treat molecules as:",
                (
                    opt("Graphs of atoms and bonds", correct=True),
                    opt("Time-series signals"),
                    opt("Pixel images only"),
                    opt("Audio waveforms"),
                ),
                "GNNs model molecules as graphs to predict activity and ADMET properties.",
            ),
            q(
                "The antibiotic halicin is notable because it was:",
                (
                    opt(
                        "Discovered by screening with a trained machine-learning model",
                        correct=True,
                    ),
                    opt("Designed entirely by hand without computation"),
                    opt("A repurposed beta-lactam"),
                    opt("Found by random animal testing"),
                ),
                "Halicin was identified using a deep-learning (GNN) screen.",
            ),
        ),
    },
    final=(
        q(
            "Enterohepatic recycling affects which ADME step?",
            (
                opt("Excretion (biliary, with reabsorption)", correct=True),
                opt("Absorption only at the lung"),
                opt("Phase I oxidation"),
                opt("Receptor binding"),
            ),
            "Biliary excretion can be followed by intestinal reabsorption, prolonging exposure.",
        ),
        q(
            "Paracelsus' principle states that:",
            (
                opt("The dose makes the poison", correct=True),
                opt("All chemicals are harmless"),
                opt("Genetics never affect toxicity"),
                opt("Toxicity is always off-target"),
            ),
            "Toxicity depends on dose; even useful drugs harm above a threshold.",
        ),
        q(
            "CYP2C19 genotype is most relevant to which drug's activation?",
            (
                opt("Clopidogrel", correct=True),
                opt("Penicillin"),
                opt("Acetaminophen"),
                opt("Insulin"),
            ),
            "Clopidogrel is a prodrug activated by CYP2C19; poor metabolisers respond less.",
        ),
        q(
            "Concentration-dependent antibiotics are best dosed to maximise:",
            (
                opt("Cmax/MIC or AUC/MIC", correct=True),
                opt("Time above MIC"),
                opt("The Hill coefficient"),
                opt("Bioavailability of zero"),
            ),
            "Aminoglycosides and fluoroquinolones are concentration-dependent.",
        ),
        q(
            "Generative models in drug discovery are used to:",
            (
                opt("Design novel molecules with desired properties", correct=True),
                opt("Only measure plasma concentrations"),
                opt("Replace all experimental validation"),
                opt("Compute the therapeutic index directly in patients"),
            ),
            "VAEs, diffusion models and RL generate candidate molecules.",
        ),
        q(
            "Why do AI predictions still require experimental validation?",
            (
                opt("PK/PD and safety remain the gatekeepers of real candidates", correct=True),
                opt("Computers cannot store molecular data"),
                opt("Predictions are always exactly correct"),
                opt("Regulators ignore computational evidence entirely"),
            ),
            "Models accelerate but do not replace pharmacology; predictions need lab and PBPK validation.",
        ),
    ),
)
