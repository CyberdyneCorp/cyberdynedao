"""Quiz questions for the Medicinal Chemistry - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is medicinal chemistry?": (
            q(
                "Medicinal chemistry sits at the intersection of organic chemistry with which fields?",
                (
                    opt("pharmacology and structural biology", correct=True),
                    opt("astronomy and geology"),
                    opt("economics and law"),
                    opt("civil engineering and acoustics"),
                ),
                "It blends synthesis, pharmacology and structural insight to design drugs.",
            ),
            q(
                "Roughly how long does it take to bring a drug from idea to approval?",
                (
                    opt("about 10 to 15 years", correct=True),
                    opt("a few weeks"),
                    opt("about 6 months"),
                    opt("about 2 years"),
                ),
                "The full discovery and development pipeline typically spans 10 to 15 years.",
            ),
            q(
                "Which step comes first in the typical discovery pipeline?",
                (
                    opt("target identification", correct=True),
                    opt("clinical phase III"),
                    opt("regulatory approval"),
                    opt("lead optimization"),
                ),
                "The funnel runs target ID, hit discovery, hit-to-lead, lead optimization, then development.",
            ),
        ),
        "Drug-likeness and the Rule of Five": (
            q(
                "Lipinski's Rule of Five flags poor oral absorption when how many limits are violated?",
                (
                    opt("two or more", correct=True),
                    opt("any single one"),
                    opt("all four"),
                    opt("at least three"),
                ),
                "Two or more violations predict likely absorption/permeability problems.",
            ),
            q(
                "Which is NOT one of Lipinski's four parameters?",
                (
                    opt("number of stereocenters", correct=True),
                    opt("molecular weight <= 500"),
                    opt("cLogP <= 5"),
                    opt("hydrogen-bond donors <= 5"),
                ),
                "The four are MW, cLogP, H-bond donors and acceptors; stereocenters are not counted.",
            ),
            q(
                "How does membrane permeability typically vary with lipophilicity (logP)?",
                (
                    opt("it rises to an optimum then falls (parabolic)", correct=True),
                    opt("it increases without limit"),
                    opt("it is independent of logP"),
                    opt("it always decreases"),
                ),
                "Too low logP cannot cross membranes; too high is insoluble, so there is an optimum.",
            ),
        ),
        "Functional groups in drug molecules": (
            q(
                "A basic amine in a drug commonly improves binding by forming what with acidic residues?",
                (
                    opt("salt bridges", correct=True),
                    opt("covalent C-C bonds"),
                    opt("metallic bonds"),
                    opt("disulfide bonds"),
                ),
                "Protonated amines form ionic salt bridges with Asp/Glu carboxylates.",
            ),
            q(
                "Why is fluorine so widely used in drug molecules?",
                (
                    opt("it tunes lipophilicity and blocks metabolism at that site", correct=True),
                    opt("it always increases molecular weight dramatically"),
                    opt("it makes molecules radioactive"),
                    opt("it removes all hydrogen bonding"),
                ),
                "Small electron-withdrawing fluorine adjusts logP, lowers nearby pKa and blocks oxidation.",
            ),
            q(
                "Which group lowers passive permeability when it ionizes to its anion?",
                (
                    opt("carboxylic acid", correct=True),
                    opt("aromatic ring"),
                    opt("methyl group"),
                    opt("ether"),
                ),
                "An ionized carboxylate carries charge, hindering passive membrane crossing.",
            ),
        ),
        "Physicochemical properties: pKa, logP and solubility": (
            q(
                "The pKa of a drug determines its:",
                (
                    opt("ionization state at a given pH", correct=True),
                    opt("molecular weight"),
                    opt("number of rings"),
                    opt("color"),
                ),
                "pKa with Henderson-Hasselbalch fixes the ratio of ionized to neutral species.",
            ),
            q(
                "What does logD account for that logP does not?",
                (
                    opt("ionization of the drug at a specified pH", correct=True),
                    opt("molecular weight"),
                    opt("the number of chiral centers"),
                    opt("the melting point"),
                ),
                "logD is the distribution of all species at a given pH; logP is only the neutral form.",
            ),
            q(
                "Aqueous solubility generally does what as lipophilicity rises?",
                (
                    opt("falls", correct=True),
                    opt("rises sharply"),
                    opt("stays constant"),
                    opt("becomes infinite"),
                ),
                "Higher lipophilicity usually lowers aqueous solubility, the central optimization tension.",
            ),
        ),
        "How drugs bind their targets": (
            q(
                "A lower dissociation constant Kd means:",
                (
                    opt("tighter binding to the target", correct=True),
                    opt("weaker binding"),
                    opt("no binding at all"),
                    opt("faster metabolism"),
                ),
                "Kd is inverse to affinity: lower Kd, tighter the complex.",
            ),
            q(
                "Which force is directional and decisive for binding specificity?",
                (
                    opt("hydrogen bonds", correct=True),
                    opt("gravitational attraction"),
                    opt("nuclear forces"),
                    opt("magnetic dipole coupling"),
                ),
                "Directional hydrogen bonds confer specificity in molecular recognition.",
            ),
            q(
                "Receptor occupancy versus ligand concentration follows what shape?",
                (
                    opt("a saturable (hyperbolic) binding isotherm", correct=True),
                    opt("a straight line through the origin"),
                    opt("a parabola opening downward"),
                    opt("a step function"),
                ),
                "Occupancy = L/(L+Kd) saturates as concentration rises.",
            ),
        ),
        "Dose, potency and the therapeutic window": (
            q(
                "EC50 (or IC50) measures a drug's:",
                (
                    opt("potency", correct=True),
                    opt("maximal efficacy"),
                    opt("molecular weight"),
                    opt("solubility"),
                ),
                "EC50 is the concentration giving half-maximal effect, i.e. potency.",
            ),
            q(
                "The therapeutic index is defined as:",
                (
                    opt("TD50 / ED50", correct=True),
                    opt("ED50 / TD50"),
                    opt("EC50 times Emax"),
                    opt("logP minus pKa"),
                ),
                "TI = toxic dose 50 / effective dose 50; larger is safer.",
            ),
            q(
                "A partial agonist differs from a full agonist in that it:",
                (
                    opt("plateaus below the maximal effect (lower Emax)", correct=True),
                    opt("produces no effect at all"),
                    opt("always has lower EC50"),
                    opt("binds covalently"),
                ),
                "A partial agonist cannot reach full Emax even at saturating dose.",
            ),
        ),
    },
    final=(
        q(
            "What is the goal of medicinal chemistry?",
            (
                opt(
                    "design and optimize molecules that modulate a biological target", correct=True
                ),
                opt("study only the geology of minerals"),
                opt("build mechanical engines"),
                opt("forecast the weather"),
            ),
            "It designs drug molecules balancing synthesis, potency and drug-likeness.",
        ),
        q(
            "Which is part of Veber's rules for good oral bioavailability?",
            (
                opt("rotatable bonds <= 10 and PSA <= 140", correct=True),
                opt("molecular weight >= 1000"),
                opt("at least five stereocenters"),
                opt("logP exactly equal to 7"),
            ),
            "Veber adds rotatable-bond and polar-surface-area limits to drug-likeness.",
        ),
        q(
            "Henderson-Hasselbalch relates pH, pKa and the ratio of:",
            (
                opt("ionized to neutral species", correct=True),
                opt("solvent to solute mass"),
                opt("donors to acceptors"),
                opt("potency to efficacy"),
            ),
            "It predicts the ionization ratio of a weak acid or base at a given pH.",
        ),
        q(
            "The hydrophobic effect contributes to binding mainly by:",
            (
                opt("releasing ordered water when greasy surfaces are buried", correct=True),
                opt("forming covalent bonds"),
                opt("ionizing the ligand"),
                opt("increasing molecular weight"),
            ),
            "Burying nonpolar surface releases structured water, a favorable entropy gain.",
        ),
        q(
            "About how much affinity gain corresponds to ~1.4 kcal/mol at room temperature?",
            (
                opt("roughly tenfold tighter binding", correct=True),
                opt("no change in binding"),
                opt("a hundredfold weaker binding"),
                opt("exactly double the molecular weight"),
            ),
            "dG = RT ln Kd, so ~1.4 kcal/mol changes Kd about tenfold.",
        ),
        q(
            "A drug with a larger therapeutic index is generally:",
            (
                opt("safer, with a wider window between effective and toxic doses", correct=True),
                opt("more toxic"),
                opt("less potent by definition"),
                opt("impossible to formulate"),
            ),
            "A larger TI means a wider gap between effective and toxic doses.",
        ),
    ),
)
