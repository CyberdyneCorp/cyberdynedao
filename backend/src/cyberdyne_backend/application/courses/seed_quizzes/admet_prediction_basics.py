"""Quiz questions for the ADMET & Toxicity Prediction - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is ADMET and why molecules fail": (
            q(
                "What do the letters ADMET stand for?",
                (
                    opt(
                        "Absorption, Distribution, Metabolism, Excretion, Toxicity",
                        correct=True,
                    ),
                    opt("Activity, Dosing, Metabolism, Efficacy, Targeting"),
                    opt("Affinity, Delivery, Molarity, Elimination, Tolerance"),
                    opt("Absorption, Diffusion, Mutation, Excretion, Transport"),
                ),
                "ADMET = Absorption, Distribution, Metabolism, Excretion and Toxicity.",
            ),
            q(
                "Why is predicting ADMET problems early so valuable?",
                (
                    opt("Late-stage clinical failures are extremely expensive", correct=True),
                    opt("It guarantees the molecule will be approved"),
                    opt("It removes the need for any biological target"),
                    opt("It makes the molecule more potent at its target"),
                ),
                "Catching ADMET liabilities early avoids costly late failures.",
            ),
            q(
                "What is the central tension in ADMET optimization?",
                (
                    opt("Improving one property often worsens another", correct=True),
                    opt("All ADMET properties improve together"),
                    opt("Potency and ADMET are unrelated"),
                    opt("Solubility has no effect on absorption"),
                ),
                "A greasy molecule absorbs well but is less soluble and more metabolized.",
            ),
        ),
        "The ADME journey through the body": (
            q(
                "Which organ performs most drug metabolism?",
                (
                    opt("The liver", correct=True),
                    opt("The spleen"),
                    opt("The lungs"),
                    opt("The pancreas"),
                ),
                "The liver, mainly via cytochrome P450 enzymes, dominates metabolism.",
            ),
            q(
                "What is first-pass metabolism?",
                (
                    opt(
                        "Loss of orally absorbed drug in the liver before reaching circulation",
                        correct=True,
                    ),
                    opt("Drug binding to plasma proteins"),
                    opt("The first dose given to a patient"),
                    opt("Filtration of drug by the kidneys"),
                ),
                "Gut-absorbed drug passes through the liver first, where much can be metabolized.",
            ),
            q(
                "Only what portion of a distributed drug is pharmacologically active?",
                (
                    opt("The free (unbound) fraction", correct=True),
                    opt("The protein-bound fraction"),
                    opt("The fraction stored in fat"),
                    opt("The fraction already excreted"),
                ),
                "Only unbound drug can leave blood and act at the target.",
            ),
        ),
        "The concentration-time curve and key PK parameters": (
            q(
                "What does AUC represent?",
                (
                    opt("Total drug exposure over time", correct=True),
                    opt("The peak concentration only"),
                    opt("The time to peak concentration"),
                    opt("The volume of distribution"),
                ),
                "AUC is the area under the concentration-time curve, total exposure.",
            ),
            q(
                "Half-life relates to elimination rate constant k how?",
                (
                    opt("t_1/2 = ln(2)/k", correct=True),
                    opt("t_1/2 = k/ln(2)"),
                    opt("t_1/2 = k * ln(2)"),
                    opt("t_1/2 = 1/k^2"),
                ),
                "For first-order elimination, half-life equals ln(2) divided by k.",
            ),
            q(
                "What does clearance (CL) measure?",
                (
                    opt("Volume of blood cleared of drug per unit time", correct=True),
                    opt("The total mass of drug in the body"),
                    opt("The fraction of drug bound to protein"),
                    opt("The time of peak concentration"),
                ),
                "Clearance is the volume cleared per unit time; CL = k * Vd.",
            ),
        ),
        "Drug-likeness and Lipinski's Rule of Five": (
            q(
                "Which is NOT one of Lipinski's Rule of Five limits?",
                (
                    opt("Melting point <= 200 C", correct=True),
                    opt("Molecular weight <= 500 Da"),
                    opt("logP <= 5"),
                    opt("Hydrogen-bond donors <= 5"),
                ),
                "The rule covers MW, logP, H-bond donors and acceptors, not melting point.",
            ),
            q(
                "How many rule violations flag likely poor absorption?",
                (
                    opt("Two or more", correct=True),
                    opt("Any single violation"),
                    opt("Five or more"),
                    opt("Only all four together"),
                ),
                "Poor absorption is more likely with two or more violations.",
            ),
            q(
                "How should the Rule of Five be treated?",
                (
                    opt("As a cheap early filter, not an absolute law", correct=True),
                    opt("As a strict requirement no drug may break"),
                    opt("As a measure of target potency"),
                    opt("As a rule that applies only to biologics"),
                ),
                "Many successful drugs break it; it is a guideline for early triage.",
            ),
        ),
        "Solubility, logP and the absorption gatekeeper": (
            q(
                "Why is aqueous solubility called the gatekeeper of absorption?",
                (
                    opt("A drug must dissolve before it can be absorbed", correct=True),
                    opt("Solubility determines target potency"),
                    opt("Solubility sets the half-life directly"),
                    opt("Insoluble drugs are absorbed faster"),
                ),
                "If a drug cannot dissolve it cannot cross the gut wall.",
            ),
            q(
                "What does logP measure?",
                (
                    opt("Octanol-water partition (lipophilicity)", correct=True),
                    opt("The acid dissociation constant"),
                    opt("Molecular weight"),
                    opt("Plasma half-life"),
                ),
                "logP is the octanol-water partition coefficient, a lipophilicity measure.",
            ),
            q(
                "As logP increases, what is the typical trade-off?",
                (
                    opt("Permeability rises but solubility tends to fall", correct=True),
                    opt("Both solubility and permeability rise"),
                    opt("Both solubility and permeability fall"),
                    opt("Neither property changes"),
                ),
                "Higher lipophilicity aids membrane crossing but hurts solubility.",
            ),
        ),
    },
    final=(
        q(
            "Which ADMET dimension concerns chemical modification of the drug?",
            (
                opt("Metabolism", correct=True),
                opt("Absorption"),
                opt("Distribution"),
                opt("Excretion"),
            ),
            "Metabolism is the chemical transformation, mostly by liver enzymes.",
        ),
        q(
            "What does a large volume of distribution typically indicate?",
            (
                opt("Extensive partitioning into tissues", correct=True),
                opt("The drug stays only in plasma"),
                opt("Very rapid renal excretion"),
                opt("High aqueous solubility"),
            ),
            "Lipophilic drugs distribute widely into tissues, giving a large Vd.",
        ),
        q(
            "After an IV bolus, first-order elimination gives a concentration curve that is roughly:",
            (
                opt("Exponentially decaying", correct=True),
                opt("Linearly increasing"),
                opt("Constant over time"),
                opt("A step function"),
            ),
            "First-order clearance produces an exponential decline in concentration.",
        ),
        q(
            "Veber's rules add which extra descriptors for oral bioavailability?",
            (
                opt("Rotatable bonds and polar surface area", correct=True),
                opt("Melting point and density"),
                opt("Charge and spin state"),
                opt("Boiling point and viscosity"),
            ),
            "Veber added rotatable bonds <= 10 and PSA <= 140 sq angstrom.",
        ),
        q(
            "Which classification system groups drugs by solubility and permeability?",
            (
                opt("BCS (Biopharmaceutics Classification System)", correct=True),
                opt("ATC therapeutic classes"),
                opt("The periodic table"),
                opt("ICH stability classes"),
            ),
            "The BCS sorts drugs into four classes by solubility and permeability.",
        ),
        q(
            "Why did poor pharmacokinetics drive fewer clinical failures after the 1990s?",
            (
                opt("ADMET began to be screened early in discovery", correct=True),
                opt("Drugs became inherently more soluble"),
                opt("Clinical trials were abolished"),
                opt("Targets stopped mattering"),
            ),
            "Early ADMET screening reduced PK-driven failures; toxicity and efficacy now dominate.",
        ),
    ),
)
