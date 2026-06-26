"""Quiz questions for the Medicinal Chemistry - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Structure-activity relationships (SAR)": (
            q(
                "An SAR study reveals:",
                (
                    opt("how structural changes alter biological activity", correct=True),
                    opt("the boiling point of a solvent"),
                    opt("the cost of synthesis only"),
                    opt("the color of a crystal"),
                ),
                "SAR maps which structural features the target requires or tolerates.",
            ),
            q(
                "A pharmacophore is best described as:",
                (
                    opt("the minimal 3D arrangement of features needed for activity", correct=True),
                    opt("the full molecular weight of the drug"),
                    opt("a single carbon atom"),
                    opt("the manufacturing batch record"),
                ),
                "The pharmacophore is the essential set of features (donors, hydrophobes, charges) for binding.",
            ),
            q(
                "An 'activity cliff' is:",
                (
                    opt("a small structural change causing a large activity jump", correct=True),
                    opt("a gradual loss of activity over time"),
                    opt("a measurement error"),
                    opt("a synthesis failure"),
                ),
                "Cliffs signal a specific, high-leverage interaction with the target.",
            ),
        ),
        "Bioisosterism": (
            q(
                "A bioisostere is a group that replaces another while:",
                (
                    opt("retaining similar biological activity", correct=True),
                    opt("always doubling potency"),
                    opt("removing all functional groups"),
                    opt("making the molecule radioactive"),
                ),
                "Bioisosteres share key physical/electronic properties, preserving activity.",
            ),
            q(
                "A common non-classical bioisostere for a carboxylic acid is:",
                (
                    opt("a tetrazole", correct=True),
                    opt("a methyl group"),
                    opt("a chlorine atom"),
                    opt("a benzene ring"),
                ),
                "Tetrazoles mimic carboxylic-acid acidity and H-bonding with better permeability.",
            ),
            q(
                "Replacing a metabolically labile C-H with C-F often:",
                (
                    opt("extends metabolic half-life", correct=True),
                    opt("makes the drug instantly toxic"),
                    opt("removes the need for a target"),
                    opt("eliminates all hydrogen bonds"),
                ),
                "Fluorine blocks oxidative metabolism at that site, slowing clearance.",
            ),
        ),
        "Enzyme inhibition and kinetics": (
            q(
                "In Michaelis-Menten kinetics, Km is the substrate concentration that gives:",
                (
                    opt("half of Vmax", correct=True),
                    opt("zero velocity"),
                    opt("maximum velocity"),
                    opt("twice Vmax"),
                ),
                "Km is the [S] at which v equals half of Vmax.",
            ),
            q(
                "A competitive inhibitor changes the apparent kinetics how?",
                (
                    opt("raises apparent Km, Vmax unchanged", correct=True),
                    opt("lowers Vmax, Km unchanged"),
                    opt("lowers both Km and Vmax"),
                    opt("has no effect on either"),
                ),
                "It competes at the active site and can be outcompeted by excess substrate.",
            ),
            q(
                "Irreversible (covalent) inhibitor potency is best described by:",
                (
                    opt("kinact / KI", correct=True),
                    opt("a simple Kd alone"),
                    opt("the molecular weight"),
                    opt("the boiling point"),
                ),
                "Covalent inhibition combines reversible recognition (KI) and inactivation rate (kinact).",
            ),
        ),
        "ADME and pharmacokinetics": (
            q(
                "What does ADME stand for?",
                (
                    opt("Absorption, Distribution, Metabolism, Excretion", correct=True),
                    opt("Activity, Dose, Mass, Energy"),
                    opt("Affinity, Density, Mobility, Entropy"),
                    opt("Acid, Base, Metal, Electron"),
                ),
                "ADME describes the body's handling of a drug.",
            ),
            q(
                "Which enzyme family is the main site of Phase I hepatic metabolism?",
                (
                    opt("cytochrome P450 (CYP)", correct=True),
                    opt("DNA polymerase"),
                    opt("ATP synthase"),
                    opt("ribosomes"),
                ),
                "CYP3A4, CYP2D6 and others perform oxidative Phase I metabolism.",
            ),
            q(
                "After an IV dose, first-order elimination gives a plasma curve that:",
                (
                    opt("decays exponentially", correct=True),
                    opt("rises linearly forever"),
                    opt("stays perfectly flat"),
                    opt("oscillates sinusoidally"),
                ),
                "C(t) = C0 exp(-ke t), with half-life ln2/ke.",
            ),
        ),
        "Ligand efficiency and optimization metrics": (
            q(
                "Ligand efficiency (LE) normalizes binding energy by:",
                (
                    opt("the number of heavy atoms", correct=True),
                    opt("the boiling point"),
                    opt("the number of synthetic steps"),
                    opt("the price per gram"),
                ),
                "LE = dG / heavy-atom count, rewarding potency per atom.",
            ),
            q(
                "Lipophilic efficiency (LLE) is calculated as:",
                (
                    opt("pIC50 minus logP", correct=True),
                    opt("pIC50 plus molecular weight"),
                    opt("logP minus pKa"),
                    opt("Vmax over Km"),
                ),
                "LLE = pIC50 - logP rewards potency not driven by lipophilicity.",
            ),
            q(
                "Efficiency metrics help avoid which problem during optimization?",
                (
                    opt("molecular obesity (rising MW and logP)", correct=True),
                    opt("low molecular weight"),
                    opt("excess aqueous solubility"),
                    opt("too few synthetic steps"),
                ),
                "They keep molecules lean by penalizing potency bought with bulk and grease.",
            ),
        ),
        "Lead optimization strategy": (
            q(
                "The iterative engine of lead optimization is the:",
                (
                    opt("design-make-test-analyze (DMTA) cycle", correct=True),
                    opt("Carnot cycle"),
                    opt("citric acid cycle"),
                    opt("nitrogen cycle"),
                ),
                "DMTA loops design, synthesis, assay and analysis to refine the lead.",
            ),
            q(
                "Avoiding hERG-channel activity during optimization aims to reduce:",
                (
                    opt("cardiotoxicity risk", correct=True),
                    opt("aqueous solubility"),
                    opt("synthetic yield"),
                    opt("molecular weight"),
                ),
                "hERG blockade can cause dangerous cardiac arrhythmias.",
            ),
            q(
                "Multi-parameter optimization (MPO) means balancing:",
                (
                    opt(
                        "potency, selectivity, ADME, safety and developability together",
                        correct=True,
                    ),
                    opt("only potency"),
                    opt("only molecular weight"),
                    opt("only synthetic cost"),
                ),
                "No single property wins; MPO seeks a balanced sweet spot.",
            ),
        ),
    },
    final=(
        q(
            "Hansch analysis often shows activity tracking lipophilicity in what way?",
            (
                opt("parabolically, peaking at an optimum logP", correct=True),
                opt("as a flat line"),
                opt("increasing without bound"),
                opt("as a sharp step at logP zero"),
            ),
            "Activity rises to an optimum logP then falls, a parabolic Hansch relationship.",
        ),
        q(
            "A classical bioisostere pair would be:",
            (
                opt("-CH2- replaced by -O-", correct=True),
                opt("a carboxylic acid replaced by a tetrazole"),
                opt("benzene replaced by a metal atom"),
                opt("an amide replaced by a chloride salt"),
            ),
            "Classical isosteres share valence and size, such as CH2/O/NH/S swaps.",
        ),
        q(
            "A non-competitive inhibitor typically:",
            (
                opt("lowers Vmax by binding an allosteric site", correct=True),
                opt("raises Km only"),
                opt("has no effect on the enzyme"),
                opt("makes the substrate covalent"),
            ),
            "Binding away from the active site reduces Vmax regardless of substrate.",
        ),
        q(
            "Bioavailability (F) is the fraction of an oral dose that:",
            (
                opt("reaches the systemic circulation", correct=True),
                opt("is excreted unchanged"),
                opt("binds the target irreversibly"),
                opt("is converted to heat"),
            ),
            "F accounts for incomplete absorption and first-pass metabolism.",
        ),
        q(
            "A healthy lead typically has lipophilic efficiency (LLE) of roughly:",
            (
                opt("5 or more", correct=True),
                opt("less than zero"),
                opt("exactly 1"),
                opt("at least 100"),
            ),
            "LLE >= 5 indicates potency that is not merely bought with lipophilicity.",
        ),
        q(
            "Drug-drug interactions frequently arise from a compound that:",
            (
                opt("inhibits or induces cytochrome P450 enzymes", correct=True),
                opt("has high aqueous solubility"),
                opt("has low molecular weight"),
                opt("contains a single fluorine"),
            ),
            "CYP inhibition or induction alters the metabolism of co-administered drugs.",
        ),
    ),
)
