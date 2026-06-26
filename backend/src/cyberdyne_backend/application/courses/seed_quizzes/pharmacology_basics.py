"""Quiz questions for the Pharmacology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is a drug and what does it do": (
            q(
                "Which branch of pharmacology asks what the body does to the drug?",
                (
                    opt("Pharmacokinetics", correct=True),
                    opt("Pharmacodynamics"),
                    opt("Pharmacognosy"),
                    opt("Toxicodynamics"),
                ),
                "Pharmacokinetics covers ADME: absorption, distribution, metabolism, excretion.",
            ),
            q(
                "What does ADME stand for?",
                (
                    opt("Absorption, distribution, metabolism, excretion", correct=True),
                    opt("Affinity, dose, metabolism, effect"),
                    opt("Agonist, drug, membrane, enzyme"),
                    opt("Absorption, dilution, mixing, elimination"),
                ),
                "ADME is the pharmacokinetic journey of a drug through the body.",
            ),
            q(
                "Which is NOT one of the four major drug target classes?",
                (
                    opt("Ribosomal RNA caps", correct=True),
                    opt("Receptors"),
                    opt("Enzymes"),
                    opt("Ion channels"),
                ),
                "The four classes are receptors, enzymes, ion channels and transporters.",
            ),
        ),
        "Receptors and drug binding": (
            q(
                "What does a smaller dissociation constant Kd indicate?",
                (
                    opt("Higher affinity (tighter binding)", correct=True),
                    opt("Lower affinity"),
                    opt("Higher efficacy"),
                    opt("Faster metabolism"),
                ),
                "Kd is the concentration occupying half the receptors; smaller Kd means tighter binding.",
            ),
            q(
                "Fractional receptor occupancy versus concentration follows what shape?",
                (
                    opt("A saturating rectangular hyperbola", correct=True),
                    opt("A straight line with no limit"),
                    opt("An exponential that grows without bound"),
                    opt("A parabola"),
                ),
                "Receptors are finite, so occupancy saturates as a hyperbola toward 1.",
            ),
            q(
                "Which is a major receptor superfamily?",
                (
                    opt("G-protein-coupled receptors", correct=True),
                    opt("Phospholipid bilayers"),
                    opt("Mitochondrial cristae"),
                    opt("Glycogen granules"),
                ),
                "GPCRs are one of the four major receptor superfamilies.",
            ),
        ),
        "Agonists and antagonists": (
            q(
                "What distinguishes a full agonist from a partial agonist?",
                (
                    opt(
                        "The partial agonist has submaximal efficacy even at full occupancy",
                        correct=True,
                    ),
                    opt("The partial agonist binds with no affinity"),
                    opt("The full agonist never activates the receptor"),
                    opt("The partial agonist is always irreversible"),
                ),
                "A partial agonist plateaus below the maximal response due to lower efficacy.",
            ),
            q(
                "A competitive antagonist shifts the agonist dose-response curve how?",
                (
                    opt("Rightward, surmountable by more agonist", correct=True),
                    opt("Leftward and irreversibly"),
                    opt("Downward, lowering the maximum permanently"),
                    opt("It has no effect on the curve"),
                ),
                "Competitive antagonists are surmountable: more agonist overcomes the block.",
            ),
            q(
                "What does an inverse agonist do?",
                (
                    opt("Suppresses constitutive activity below baseline", correct=True),
                    opt("Produces the maximal response"),
                    opt("Binds with zero affinity"),
                    opt("Acts only as a competitive blocker"),
                ),
                "An inverse agonist stabilises the resting state, reducing baseline activity.",
            ),
        ),
        "The dose-response curve": (
            q(
                "Why is effect plotted against the logarithm of concentration?",
                (
                    opt(
                        "It spreads the wide concentration range and linearises the informative middle",
                        correct=True,
                    ),
                    opt("It removes the need for an Emax"),
                    opt("It converts the curve into a parabola"),
                    opt("It eliminates the Hill coefficient"),
                ),
                "The log axis turns the hyperbola into a readable sigmoid.",
            ),
            q(
                "In the Hill-Langmuir equation, what does EC50 represent?",
                (
                    opt("The concentration producing half-maximal effect", correct=True),
                    opt("The maximal achievable effect"),
                    opt("The Hill coefficient"),
                    opt("The toxic dose"),
                ),
                "EC50 is the concentration giving 50% of Emax.",
            ),
            q(
                "A Hill coefficient n greater than 1 does what to the curve?",
                (
                    opt("Steepens it, reflecting positive cooperativity", correct=True),
                    opt("Flattens it completely"),
                    opt("Lowers the maximal effect"),
                    opt("Shifts it without changing slope"),
                ),
                "n>1 makes the sigmoid steeper, indicating cooperativity.",
            ),
        ),
        "Potency, efficacy and the therapeutic window": (
            q(
                "Potency is best described by which parameter?",
                (
                    opt("EC50 or ED50 (lower means more potent)", correct=True),
                    opt("Emax"),
                    opt("The Hill coefficient"),
                    opt("The volume of distribution"),
                ),
                "Potency reflects how much drug is needed; a lower EC50 means higher potency.",
            ),
            q(
                "How is the therapeutic index defined?",
                (
                    opt("TD50 divided by ED50", correct=True),
                    opt("ED50 divided by TD50"),
                    opt("Emax divided by EC50"),
                    opt("Kd divided by EC50"),
                ),
                "TI = TD50/ED50; a larger value means a wider safety margin.",
            ),
            q(
                "Which drug typically has a NARROW therapeutic index?",
                (
                    opt("Warfarin", correct=True),
                    opt("Penicillin"),
                    opt("Ibuprofen"),
                    opt("Loratadine"),
                ),
                "Warfarin, digoxin and lithium have narrow indices needing monitoring.",
            ),
        ),
    },
    final=(
        q(
            "Pharmacodynamics describes:",
            (
                opt("What the drug does to the body", correct=True),
                opt("What the body does to the drug"),
                opt("How a drug is manufactured"),
                opt("How a drug is named"),
            ),
            "Pharmacodynamics is the drug's molecular action and resulting response.",
        ),
        q(
            "Half-maximal receptor occupancy occurs when free concentration equals:",
            (
                opt("Kd", correct=True),
                opt("Emax"),
                opt("EC50 times n"),
                opt("Zero"),
            ),
            "By definition Kd is the concentration occupying half the receptors.",
        ),
        q(
            "An antagonist is characterised by:",
            (
                opt("Affinity but zero efficacy", correct=True),
                opt("Efficacy but zero affinity"),
                opt("Both maximal affinity and efficacy"),
                opt("Neither affinity nor binding"),
            ),
            "Antagonists bind without activating, blocking agonist action.",
        ),
        q(
            "The horizontal position of a log dose-response curve reports:",
            (
                opt("Potency", correct=True),
                opt("Efficacy"),
                opt("Toxicity"),
                opt("Bioavailability"),
            ),
            "Position reports potency; the ceiling reports efficacy.",
        ),
        q(
            "Two drugs with the same target can differ independently in:",
            (
                opt("Potency and efficacy", correct=True),
                opt("Only their molecular weight"),
                opt("Only their colour"),
                opt("Nothing measurable"),
            ),
            "Potency (dose needed) and efficacy (ceiling) are independent properties.",
        ),
        q(
            "The therapeutic window is the concentration range:",
            (
                opt(
                    "Above the minimum effective level but below the toxic threshold", correct=True
                ),
                opt("Below all effective levels"),
                opt("Above the toxic threshold"),
                opt("Where the drug is not absorbed"),
            ),
            "The window spans effective but non-toxic concentrations.",
        ),
    ),
)
