"""Quiz questions for the Drug Development, Clinical Trials & Regulatory - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "From target to clinic: the drug development pipeline": (
            q(
                "About how long does it typically take to bring a new drug to market?",
                (
                    opt("10 to 15 years", correct=True),
                    opt("a few months"),
                    opt("about 2 years"),
                    opt("30 to 40 years"),
                ),
                "The full pipeline from target to approval spans roughly 10 to 15 years.",
            ),
            q(
                "Roughly what fraction of compounds entering human trials get approved?",
                (
                    opt("about 1 in 10", correct=True),
                    opt("about 9 in 10"),
                    opt("all of them"),
                    opt("about half"),
                ),
                "Attrition is steep: only around 10% of clinical entrants reach approval.",
            ),
            q(
                "Which step comes first in the pipeline?",
                (
                    opt("target identification", correct=True),
                    opt("Phase III"),
                    opt("regulatory review"),
                    opt("post-marketing surveillance"),
                ),
                "The funnel begins by identifying the biological target.",
            ),
        ),
        "Drug targets, mechanisms and modalities": (
            q(
                "Which is the largest single class of drug targets?",
                (
                    opt("G-protein-coupled receptors (GPCRs)", correct=True),
                    opt("ribosomal RNA"),
                    opt("cell membranes"),
                    opt("mitochondria"),
                ),
                "GPCRs are the most heavily drugged target family, alongside enzymes.",
            ),
            q(
                "A drug that blocks a receptor's activity is called what?",
                (
                    opt("an antagonist", correct=True),
                    opt("an agonist"),
                    opt("a substrate"),
                    opt("a cofactor"),
                ),
                "An antagonist blocks the target; an agonist activates it.",
            ),
            q(
                "Which is a key feature of a small-molecule modality versus a biologic?",
                (
                    opt("it is usually oral and can cross cell membranes", correct=True),
                    opt("it is always injected and very large"),
                    opt("it is made of mRNA"),
                    opt("it cannot be patented"),
                ),
                "Small molecules are typically oral and membrane-permeable; biologics are large and injected.",
            ),
        ),
        "Dose, response and the therapeutic window": (
            q(
                "Plotted against log concentration, a dose-response curve is typically what shape?",
                (
                    opt("sigmoidal", correct=True),
                    opt("a straight line"),
                    opt("a parabola"),
                    opt("a flat line"),
                ),
                "Effect versus log concentration produces a characteristic sigmoid that saturates.",
            ),
            q(
                "What does EC50 (or IC50) represent?",
                (
                    opt("the concentration giving half the maximal effect", correct=True),
                    opt("the molecular weight"),
                    opt("the patent term"),
                    opt("the number of trial sites"),
                ),
                "EC50/IC50 is the half-maximal effective/inhibitory concentration.",
            ),
            q(
                "A wide therapeutic window (large therapeutic index) means the drug is:",
                (
                    opt(
                        "relatively safe, with a big gap between effective and toxic doses",
                        correct=True,
                    ),
                    opt("dangerous, with toxic and effective doses nearly equal"),
                    opt("ineffective at any dose"),
                    opt("only usable intravenously"),
                ),
                "TI = TD50/ED50; a large ratio means a forgiving, safe margin.",
            ),
        ),
        "Preclinical studies: efficacy, safety and toxicology": (
            q(
                "What quality standard governs safety-critical preclinical studies?",
                (
                    opt("Good Laboratory Practice (GLP)", correct=True),
                    opt("Good Clinical Practice (GCP)"),
                    opt("Good Manufacturing Practice (GMP)"),
                    opt("ISO 9001 only"),
                ),
                "GLP governs non-clinical safety studies; GCP is for clinical and GMP for manufacturing.",
            ),
            q(
                "Pharmacokinetics describes what?",
                (
                    opt(
                        "what the body does to the drug (absorption, distribution, metabolism, excretion)",
                        correct=True,
                    ),
                    opt("what the drug does to the body"),
                    opt("the patent strategy"),
                    opt("the trial randomization scheme"),
                ),
                "PK is the body's handling of the drug: ADME.",
            ),
            q(
                "The human starting dose is usually derived from which animal value?",
                (
                    opt("the NOAEL, with a safety margin", correct=True),
                    opt("the maximum tolerated human dose"),
                    opt("the molecular weight"),
                    opt("the patent filing date"),
                ),
                "The No Observed Adverse Effect Level in the most sensitive species, scaled down, sets the first human dose.",
            ),
        ),
        "Clinical trial phases I, II and III": (
            q(
                "What is the primary aim of Phase I?",
                (
                    opt("assess safety and find the tolerable dose range", correct=True),
                    opt("prove the drug is better than standard of care"),
                    opt("market the drug"),
                    opt("file the patent"),
                ),
                "Phase I, often in healthy volunteers, establishes safety, tolerability and human PK.",
            ),
            q(
                "Which phase provides the pivotal, large confirmatory evidence for approval?",
                (
                    opt("Phase III", correct=True),
                    opt("Phase I"),
                    opt("preclinical"),
                    opt("Phase 0 only"),
                ),
                "Phase III runs large randomized controlled trials that regulators rely on.",
            ),
            q(
                "Why do later phases enroll more patients?",
                (
                    opt(
                        "to gain statistical power to detect rarer effects and modest benefits",
                        correct=True,
                    ),
                    opt("because the drug is cheaper to make then"),
                    opt("to reduce the cost per trial"),
                    opt("because regulators forbid small Phase III trials of any drug"),
                ),
                "Detecting small effects and rare harms requires larger samples for power.",
            ),
        ),
        "Regulators and the approval decision": (
            q(
                "Which agency regulates drugs in the United States?",
                (
                    opt("the FDA", correct=True),
                    opt("the EMA"),
                    opt("ANVISA"),
                    opt("the PMDA"),
                ),
                "The FDA is the US authority; EMA (EU), PMDA (Japan), ANVISA (Brazil).",
            ),
            q(
                "On what basis does a regulator approve a drug?",
                (
                    opt("its benefits outweigh its risks for a defined use", correct=True),
                    opt("it is the cheapest option available"),
                    opt("it has the most patents"),
                    opt("it was developed fastest"),
                ),
                "Approval rests on a favourable benefit-risk balance for the proposed label.",
            ),
            q(
                "What body harmonizes technical requirements across regions?",
                (
                    opt("ICH", correct=True),
                    opt("the WHO General Assembly"),
                    opt("the patent office"),
                    opt("the ethics committee"),
                ),
                "ICH harmonizes guidelines so one programme can serve many markets.",
            ),
        ),
    },
    final=(
        q(
            "Which sequence correctly orders the pipeline?",
            (
                opt("target ID, discovery, preclinical, Phase I-III, approval", correct=True),
                opt("Phase III, approval, preclinical, discovery"),
                opt("approval, Phase I, target ID, discovery"),
                opt("discovery, approval, Phase II, preclinical"),
            ),
            "The funnel runs target ID through discovery and preclinical to the three phases and approval.",
        ),
        q(
            "A more potent drug has which property?",
            (
                opt("a smaller EC50/IC50", correct=True),
                opt("a larger EC50/IC50"),
                opt("a higher molecular weight"),
                opt("more trial sites"),
            ),
            "Lower half-maximal concentration means greater potency.",
        ),
        q(
            "Which quality standard applies to manufacturing?",
            (
                opt("GMP", correct=True),
                opt("GLP"),
                opt("GCP"),
                opt("ICH E6"),
            ),
            "GMP governs how the drug is made; GLP preclinical and GCP clinical.",
        ),
        q(
            "The submission justifying first human dosing in the US is called what?",
            (
                opt("an IND", correct=True),
                opt("an NDA"),
                opt("an MAA"),
                opt("a REMS"),
            ),
            "The Investigational New Drug application precedes clinical trials.",
        ),
        q(
            "Which modality is typically a large, injected, highly specific molecule?",
            (
                opt("a monoclonal antibody (biologic)", correct=True),
                opt("an oral small molecule"),
                opt("a placebo tablet"),
                opt("a surrogate endpoint"),
            ),
            "Biologics like antibodies are large and injected, unlike oral small molecules.",
        ),
        q(
            "Regulatory approval is best described as:",
            (
                opt("an ongoing relationship with continued safety obligations", correct=True),
                opt("a permanent guarantee that can never be revisited"),
                opt("a marketing slogan"),
                opt("a patent grant"),
            ),
            "Labels can be restricted, Phase IV required, and drugs withdrawn if safety worsens.",
        ),
    ),
)
