"""Quiz questions for the AI-Driven Drug Discovery - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The drug discovery pipeline and where AI fits": (
            q(
                "Roughly how long does it take to bring a drug to market?",
                (
                    opt("about 10 to 15 years", correct=True),
                    opt("a few weeks"),
                    opt("about 6 months"),
                    opt("about 2 years"),
                ),
                "The full pipeline from target to approval typically spans 10 to 15 years.",
            ),
            q(
                "Which stage comes first in the discovery funnel?",
                (
                    opt("target identification", correct=True),
                    opt("clinical phase III"),
                    opt("regulatory approval"),
                    opt("lead optimization"),
                ),
                "The funnel begins with identifying the biological target.",
            ),
            q(
                "Why is AI's economic value concentrated in the early stages?",
                (
                    opt(
                        "Catching a doomed compound early avoids the large cost of late failures",
                        correct=True,
                    ),
                    opt("Early experiments are the most expensive"),
                    opt("Regulators only accept AI in early phases"),
                    opt("Late stages have no data"),
                ),
                "Most clinical entrants fail, so cheap early triage compounds into big savings.",
            ),
        ),
        "How molecules become data: SMILES, fingerprints, descriptors": (
            q(
                "What is a SMILES string?",
                (
                    opt("A text encoding of a molecule's structure", correct=True),
                    opt("A 3D protein structure file"),
                    opt("A clinical trial identifier"),
                    opt("A measure of toxicity"),
                ),
                "SMILES encodes a molecule as a compact text string, e.g. CCO for ethanol.",
            ),
            q(
                "What does an ECFP / Morgan fingerprint encode?",
                (
                    opt("Circular atom neighborhoods hashed into bits", correct=True),
                    opt("The exact 3D coordinates of every atom"),
                    opt("The melting point only"),
                    opt("The patent number of the compound"),
                ),
                "Morgan fingerprints hash circular substructures into a fixed-length bit vector.",
            ),
            q(
                "Tanimoto similarity between two fingerprints measures what?",
                (
                    opt("Overlap of set bits relative to their union", correct=True),
                    opt("Difference in molecular weight"),
                    opt("Number of clinical trials"),
                    opt("Boiling point ratio"),
                ),
                "Tanimoto is the intersection over union of the two bit sets.",
            ),
        ),
        "Activity, potency and dose-response": (
            q(
                "A dose-response curve plotted against log concentration is typically what shape?",
                (
                    opt("sigmoidal", correct=True),
                    opt("a straight line"),
                    opt("a parabola"),
                    opt("a step that never changes"),
                ),
                "Response versus log concentration produces a characteristic sigmoid.",
            ),
            q(
                "What does IC50 represent?",
                (
                    opt("The concentration that inhibits a process by 50%", correct=True),
                    opt("The molecular weight at half mass"),
                    opt("The time to reach the liver"),
                    opt("The number of hydrogen bonds"),
                ),
                "IC50 is the half-maximal inhibitory concentration.",
            ),
            q(
                "If pIC50 = -log10(IC50), what does a larger pIC50 mean?",
                (
                    opt("more potent compound", correct=True),
                    opt("less potent compound"),
                    opt("higher molecular weight"),
                    opt("lower solubility"),
                ),
                "A smaller IC50 (more potent) gives a larger pIC50.",
            ),
        ),
        "Drug-likeness and the Rule of Five": (
            q(
                "Lipinski's Rule of Five flags poor oral absorption when how many limits are broken?",
                (
                    opt("two or more", correct=True),
                    opt("any single one"),
                    opt("all five"),
                    opt("exactly three"),
                ),
                "Two or more violations flag likely poor oral absorption.",
            ),
            q(
                "Which is one of the Rule of Five limits?",
                (
                    opt("molecular weight at most 500 Da", correct=True),
                    opt("at least 20 rotatable bonds"),
                    opt("logP at least 12"),
                    opt("more than 50 hydrogen-bond donors"),
                ),
                "MW <= 500, logP <= 5, HBD <= 5, HBA <= 10.",
            ),
            q(
                "Are the rules absolute laws?",
                (
                    opt("No, many approved drugs break them", correct=True),
                    opt("Yes, no approved drug violates them"),
                    opt("Yes, they are enforced by regulators"),
                    opt("They apply only to injectable drugs"),
                ),
                "They are coarse heuristics; natural products and antibiotics often break them.",
            ),
        ),
        "ADMET: what happens to a drug in the body": (
            q(
                "What does ADMET stand for?",
                (
                    opt(
                        "Absorption, Distribution, Metabolism, Excretion, Toxicity",
                        correct=True,
                    ),
                    opt("Activity, Dose, Mass, Energy, Time"),
                    opt("Affinity, Diffusion, Mixing, Entropy, Temperature"),
                    opt("Assay, Database, Model, Endpoint, Test"),
                ),
                "ADMET captures what the body does to a drug plus toxicity.",
            ),
            q(
                "hERG channel block is a concern for which ADMET property?",
                (
                    opt("toxicity (cardiac risk)", correct=True),
                    opt("absorption"),
                    opt("excretion"),
                    opt("distribution"),
                ),
                "hERG inhibition is associated with dangerous cardiac arrhythmia.",
            ),
            q(
                "Which enzymes are central to drug metabolism?",
                (
                    opt("cytochrome P450 enzymes such as CYP3A4", correct=True),
                    opt("DNA polymerases"),
                    opt("ribosomes"),
                    opt("ATP synthase"),
                ),
                "Liver CYP enzymes like CYP3A4 and CYP2D6 clear many drugs.",
            ),
        ),
        "Families of AI models in discovery": (
            q(
                "A graph neural network operates directly on what?",
                (
                    opt("the molecular graph of atoms and bonds", correct=True),
                    opt("a single scalar molecular weight"),
                    opt("the patent text"),
                    opt("the clinical outcome only"),
                ),
                "GNNs treat atoms as nodes and bonds as edges and learn end-to-end.",
            ),
            q(
                "With only a few hundred measured compounds, what usually performs best?",
                (
                    opt("a random forest on ECFP fingerprints", correct=True),
                    opt("a giant deep transformer"),
                    opt("a diffusion model"),
                    opt("no model can work at all"),
                ),
                "Classical ML on fingerprints is a strong baseline in low-data regimes.",
            ),
            q(
                "Which model family reads SMILES sequences?",
                (
                    opt("RNNs and transformers", correct=True),
                    opt("random forests on descriptors"),
                    opt("support vector machines on fingerprints"),
                    opt("docking scoring functions"),
                ),
                "Sequence models read SMILES for prediction and generation.",
            ),
        ),
    },
    final=(
        q(
            "Where does AI add the most value in the discovery funnel?",
            (
                opt("the early, data-rich stages where decisions are cheap", correct=True),
                opt("only after regulatory approval"),
                opt("during manufacturing scale-up only"),
                opt("nowhere; it is not used"),
            ),
            "AI accelerates early triage where the search space is huge and tests are cheap.",
        ),
        q(
            "Which representation is a text encoding of a molecule?",
            (
                opt("SMILES", correct=True),
                opt("ECFP fingerprint"),
                opt("pLDDT"),
                opt("IC50"),
            ),
            "SMILES is the line-notation string representation.",
        ),
        q(
            "A more potent compound has which of these?",
            (
                opt("a higher pIC50", correct=True),
                opt("a higher IC50"),
                opt("a higher molecular weight"),
                opt("more rotatable bonds"),
            ),
            "pIC50 = -log10(IC50), so potency rises with pIC50.",
        ),
        q(
            "Two violations of Lipinski's rules suggest what?",
            (
                opt("likely poor oral absorption", correct=True),
                opt("guaranteed approval"),
                opt("high binding affinity"),
                opt("low toxicity"),
            ),
            "Two or more violations flag poor oral bioavailability.",
        ),
        q(
            "The 'T' in ADMET refers to what?",
            (
                opt("toxicity", correct=True),
                opt("temperature"),
                opt("time"),
                opt("titration"),
            ),
            "ADMET ends with Toxicity.",
        ),
        q(
            "Which is the safest first model choice for a small QSAR dataset?",
            (
                opt("random forest or gradient boosting on fingerprints", correct=True),
                opt("a large generative diffusion model"),
                opt("a billion-parameter language model"),
                opt("no features at all"),
            ),
            "Classical ML on fingerprints is the robust default for small data.",
        ),
    ),
)
