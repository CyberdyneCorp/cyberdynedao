"""Quiz questions for the Computer-Aided Drug Design (CADD) - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The drug discovery pipeline": (
            q(
                "What is the main goal of computer-aided drug design (CADD) in the pipeline?",
                (
                    opt(
                        "Make early stages faster and more rational by predicting useful molecules",
                        correct=True,
                    ),
                    opt("Replace all clinical trials with simulations"),
                    opt("Eliminate the need for a biological target"),
                    opt("Guarantee that every candidate becomes a drug"),
                ),
                "CADD prioritises which molecules to synthesise and test, improving early-stage efficiency.",
            ),
            q(
                "Which stage comes immediately after target identification and validation?",
                (
                    opt("Hit discovery", correct=True),
                    opt("Clinical trials"),
                    opt("Regulatory approval"),
                    opt("Lead optimisation"),
                ),
                "After choosing a validated target, hit discovery finds molecules that bind it.",
            ),
            q(
                "Why is attrition important in drug discovery?",
                (
                    opt("Most screened molecules fail, so per-stage gains compound", correct=True),
                    opt("All molecules survive equally to market"),
                    opt("It only matters in the manufacturing step"),
                    opt("It means trials are unnecessary"),
                ),
                "Survival probability multiplies across stages, so small improvements have large cumulative effects.",
            ),
        ),
        "Drug targets and druggability": (
            q(
                "Which protein family is a common class of drug targets?",
                (
                    opt("G-protein-coupled receptors (GPCRs)", correct=True),
                    opt("Structural collagen fibres only"),
                    opt("Ribosomal RNA exclusively"),
                    opt("Storage proteins like ferritin only"),
                ),
                "Enzymes, GPCRs, ion channels and nuclear receptors dominate the druggable target space.",
            ),
            q(
                "What does 'druggability' primarily refer to?",
                (
                    opt(
                        "Whether the target has a pocket a small molecule can bind with high affinity",
                        correct=True,
                    ),
                    opt("Whether the target is expensive to purify"),
                    opt("Whether the target is found only in bacteria"),
                    opt("Whether the protein has been crystallised"),
                ),
                "Druggability concerns a well-defined, partly hydrophobic pocket suited to small-molecule binding.",
            ),
            q(
                "Why are flat protein-protein interfaces hard to drug?",
                (
                    opt(
                        "They lack a well-defined concave pocket for a small molecule", correct=True
                    ),
                    opt("They are always located outside the cell"),
                    opt("They cannot be expressed in the lab"),
                    opt("They are never disease-relevant"),
                ),
                "Small molecules need an enclosed pocket; flat surfaces give few high-affinity contacts.",
            ),
        ),
        "Ligand-receptor binding and affinity": (
            q(
                "A smaller dissociation constant Kd means:",
                (
                    opt("tighter binding between ligand and receptor", correct=True),
                    opt("weaker binding"),
                    opt("no binding at all"),
                    opt("a covalent bond has formed"),
                ),
                "Kd is the ligand concentration for half-occupancy; lower Kd means higher affinity.",
            ),
            q(
                "At what ligand concentration is the receptor half-occupied?",
                (
                    opt("when [L] equals Kd", correct=True),
                    opt("when [L] equals zero"),
                    opt("when [L] is twice Kd"),
                    opt("never, occupancy is always full"),
                ),
                "The Langmuir isotherm gives 50% occupancy exactly at [L] = Kd.",
            ),
            q(
                "Binding free energy is decomposed as:",
                (
                    opt("delta G = delta H - T delta S", correct=True),
                    opt("delta G = delta H + T delta S squared"),
                    opt("delta G = T delta S - delta H always positive"),
                    opt("delta G depends only on temperature"),
                ),
                "Gibbs free energy combines enthalpic and entropic contributions to affinity.",
            ),
        ),
        "Dose-response, potency and efficacy": (
            q(
                "What does EC50 measure?",
                (
                    opt("the concentration giving half-maximal effect (potency)", correct=True),
                    opt("the maximal possible response"),
                    opt("the molecular weight of the drug"),
                    opt("the number of hydrogen-bond donors"),
                ),
                "EC50 (or IC50 for inhibitors) is the standard potency measure.",
            ),
            q(
                "A partial agonist is best described as a drug that is:",
                (
                    opt("potent but with low maximal efficacy", correct=True),
                    opt("always more efficacious than a full agonist"),
                    opt("incapable of binding the receptor"),
                    opt("identical to an antagonist in every way"),
                ),
                "A partial agonist may bind well yet cannot reach the full Emax.",
            ),
            q(
                "What does the Hill coefficient n describe in a dose-response curve?",
                (
                    opt("the steepness / cooperativity of the curve", correct=True),
                    opt("the molecular weight of the ligand"),
                    opt("the half-life of the drug"),
                    opt("the absolute toxicity"),
                ),
                "The Hill coefficient governs how steeply response rises with dose.",
            ),
        ),
        "Drug-likeness and Lipinski's rules": (
            q(
                "Lipinski's Rule of Five flags poor absorption when a molecule violates two or more of which set?",
                (
                    opt("MW <= 500, logP <= 5, donors <= 5, acceptors <= 10", correct=True),
                    opt("MW <= 100, logP <= 1, donors <= 1, acceptors <= 1"),
                    opt("charge, colour, melting point, density"),
                    opt("number of rings, atoms, bonds and angles only"),
                ),
                "The Ro5 sets thresholds on weight, lipophilicity and hydrogen-bonding capacity.",
            ),
            q(
                "Veber's rules add limits on which two properties?",
                (
                    opt("rotatable bonds and polar surface area", correct=True),
                    opt("boiling point and density"),
                    opt("colour and odour"),
                    opt("price and shelf life"),
                ),
                "Veber added rotatable bonds (<=10) and PSA (<=140 square angstrom) for bioavailability.",
            ),
            q(
                "Why does too-high lipophilicity become a problem?",
                (
                    opt(
                        "it causes poor solubility and toxicity despite good permeation",
                        correct=True,
                    ),
                    opt("it makes the molecule too small to bind"),
                    opt("it always lowers binding affinity to zero"),
                    opt("it prevents any membrane crossing"),
                ),
                "Permeability saturates while excessive logP brings solubility and toxicity liabilities.",
            ),
        ),
        "ADMET: from molecule to medicine": (
            q(
                "What does ADMET stand for?",
                (
                    opt("Absorption, Distribution, Metabolism, Excretion, Toxicity", correct=True),
                    opt("Affinity, Docking, Modelling, Energy, Targeting"),
                    opt("Activity, Dose, Mass, Entropy, Temperature"),
                    opt("Assay, Database, Method, Enzyme, Test"),
                ),
                "ADMET summarises a drug's pharmacokinetic and safety fate in the body.",
            ),
            q(
                "Which enzyme family dominates drug metabolism in the liver?",
                (
                    opt("cytochrome P450 (e.g. CYP3A4)", correct=True),
                    opt("DNA polymerase"),
                    opt("ATP synthase"),
                    opt("ribosomal peptidyl transferase"),
                ),
                "CYP enzymes such as CYP3A4 and CYP2D6 metabolise most small-molecule drugs.",
            ),
            q(
                "First-order elimination implies plasma concentration over time follows:",
                (
                    opt("an exponential decay with constant half-life", correct=True),
                    opt("a linear increase forever"),
                    opt("a constant flat line"),
                    opt("a parabola opening upward"),
                ),
                "C(t) = C0 exp(-ke t), so half-life is constant regardless of starting dose.",
            ),
        ),
    },
    final=(
        q(
            "Roughly how long and costly is bringing a new drug to market?",
            (
                opt("10-15 years and often over a billion US dollars", correct=True),
                opt("a few months and under a thousand dollars"),
                opt("exactly one year, fixed cost"),
                opt("decades but essentially free"),
            ),
            "Development is famously long and expensive, motivating CADD efficiency gains.",
        ),
        q(
            "A validated drug target must be both:",
            (
                opt("disease-relevant and druggable", correct=True),
                opt("colourful and water-soluble"),
                opt("large and negatively charged"),
                opt("rare and structurally unknown"),
            ),
            "Modulating it must affect disease, and it must have a bindable pocket.",
        ),
        q(
            "The dissociation constant Kd equals the ligand concentration at which:",
            (
                opt("the receptor is half-occupied", correct=True),
                opt("the receptor is fully saturated"),
                opt("no ligand is bound"),
                opt("the drug is fully metabolised"),
            ),
            "Half-maximal occupancy occurs at [L] = Kd in the Langmuir isotherm.",
        ),
        q(
            "Potency and efficacy of a drug correspond respectively to:",
            (
                opt("EC50 and Emax", correct=True),
                opt("molecular weight and logP"),
                opt("half-life and clearance"),
                opt("donors and acceptors"),
            ),
            "Potency is the half-maximal concentration; efficacy is the maximal response.",
        ),
        q(
            "Which is a Lipinski Rule-of-Five threshold?",
            (
                opt("molecular weight <= 500 Da", correct=True),
                opt("molecular weight >= 2000 Da"),
                opt("logP >= 12"),
                opt("hydrogen-bond donors >= 50"),
            ),
            "Ro5 limits MW to 500, logP to 5, donors to 5 and acceptors to 10.",
        ),
        q(
            "Why did poor ADMET historically cause most clinical failures?",
            (
                opt(
                    "Molecules can be potent yet have poor absorption, metabolism or toxicity",
                    correct=True,
                ),
                opt("Because potency is the only thing that ever matters"),
                opt("Because targets were always wrong"),
                opt("Because trials never test safety"),
            ),
            "Affinity is necessary but not sufficient; pharmacokinetics and safety decide success.",
        ),
    ),
)
