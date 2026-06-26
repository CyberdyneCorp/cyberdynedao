"""Quiz questions for the AI-Driven Drug Discovery - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Generative molecular design": (
            q(
                "What advantage does SELFIES have over raw SMILES for generation?",
                (
                    opt("every SELFIES string decodes to a valid molecule", correct=True),
                    opt("it is shorter than SMILES always"),
                    opt("it encodes the 3D structure exactly"),
                    opt("it stores the patent number"),
                ),
                "SELFIES is constructed so all strings are valid molecules.",
            ),
            q(
                "Why must generators be constrained by synthetic accessibility?",
                (
                    opt("to avoid proposing molecules no one can make", correct=True),
                    opt("to make training slower"),
                    opt("to lower molecular weight always"),
                    opt("to remove all rings"),
                ),
                "Without SA constraints, optimizers find unsynthesizable molecules.",
            ),
            q(
                "What is reward hacking in generative design?",
                (
                    opt(
                        "the model exploits flaws in the property oracle off-distribution",
                        correct=True,
                    ),
                    opt("the model trains too slowly"),
                    opt("the assay measures the wrong target"),
                    opt("the scaffold is too small"),
                ),
                "Generators can find adversarial molecules that fool a weak oracle.",
            ),
        ),
        "Foundation models and self-supervised pretraining": (
            q(
                "What does self-supervised pretraining exploit?",
                (
                    opt("vast unlabeled molecular data", correct=True),
                    opt("only labeled clinical outcomes"),
                    opt("a single curated assay"),
                    opt("the patent database alone"),
                ),
                "Pretraining uses hundreds of millions of unlabeled molecules.",
            ),
            q(
                "Where does pretraining help most?",
                (
                    opt("in the low-data labeled regime", correct=True),
                    opt("only when millions of labels exist"),
                    opt("never; it always hurts"),
                    opt("only for protein folding"),
                ),
                "Transfer learning matters most where labeled data is scarce.",
            ),
            q(
                "A pretext task like masked-atom prediction is an example of what?",
                (
                    opt("self-supervised learning", correct=True),
                    opt("supervised regression on IC50"),
                    opt("reinforcement learning on assays"),
                    opt("docking"),
                ),
                "Masking and predicting parts of the input is self-supervision.",
            ),
        ),
        "Structure prediction and structure-based AI": (
            q(
                "What does AlphaFold predict?",
                (
                    opt("protein 3D structure from sequence", correct=True),
                    opt("the IC50 of a ligand"),
                    opt("the patent expiry date"),
                    opt("the clinical trial result"),
                ),
                "AlphaFold predicts 3D protein structure from amino-acid sequence.",
            ),
            q(
                "What does the pLDDT score report?",
                (
                    opt("per-residue confidence of the predicted structure", correct=True),
                    opt("the binding affinity"),
                    opt("the molecular weight"),
                    opt("the assay noise"),
                ),
                "pLDDT (0-100) is a per-residue confidence measure.",
            ),
            q(
                "Why treat a predicted protein-ligand complex cautiously?",
                (
                    opt(
                        "a high-confidence backbone can still have a misplaced side chain",
                        correct=True,
                    ),
                    opt("predictions are always perfect"),
                    opt("structures are irrelevant to docking"),
                    opt("ligands never bind proteins"),
                ),
                "Predicted structures are hypotheses needing experimental validation.",
            ),
        ),
        "Active learning and Bayesian optimization": (
            q(
                "What does an active learning loop do?",
                (
                    opt("proposes the next experiments, then retrains on results", correct=True),
                    opt("trains once and never updates"),
                    opt("ignores model uncertainty"),
                    opt("only runs after approval"),
                ),
                "It iterates predict-propose-test-retrain to learn from few experiments.",
            ),
            q(
                "An acquisition function balances which two goals?",
                (
                    opt("exploitation and exploration", correct=True),
                    opt("synthesis and excretion"),
                    opt("absorption and toxicity"),
                    opt("price and weight"),
                ),
                "It trades testing the predicted-best against testing uncertain regions.",
            ),
            q(
                "In the UCB acquisition mu(x) + k*sigma(x), what does sigma represent?",
                (
                    opt("model uncertainty at x", correct=True),
                    opt("the molecular weight"),
                    opt("the assay temperature"),
                    opt("the number of atoms"),
                ),
                "sigma is the predictive uncertainty driving exploration.",
            ),
        ),
        "Multi-objective optimization and the design funnel": (
            q(
                "Why is there no single best molecule across many objectives?",
                (
                    opt("objectives conflict, yielding a set of trade-offs", correct=True),
                    opt("all objectives are identical"),
                    opt("objectives never matter"),
                    opt("only potency is ever measured"),
                ),
                "Conflicting goals produce a Pareto front of non-dominated options.",
            ),
            q(
                "A molecule is Pareto-optimal when what holds?",
                (
                    opt("no other molecule is better on every objective", correct=True),
                    opt("it is the heaviest molecule"),
                    opt("it has the most rings"),
                    opt("it is cheapest to make"),
                ),
                "Pareto-optimal means non-dominated across all objectives.",
            ),
            q(
                "Why use a geometric-mean desirability function?",
                (
                    opt("any single zero kills the candidate, enforcing balance", correct=True),
                    opt("it ignores poor properties"),
                    opt("it maximizes one property only"),
                    opt("it removes the need for models"),
                ),
                "The product form penalizes any property scoring zero.",
            ),
        ),
        "The modern stack: self-driving labs and the AI loop": (
            q(
                "What does the DMTA loop stand for?",
                (
                    opt("Design, Make, Test, Analyze", correct=True),
                    opt("Dock, Model, Train, Approve"),
                    opt("Data, Metric, Test, Average"),
                    opt("Dose, Measure, Titrate, Adjust"),
                ),
                "The closed loop is Design-Make-Test-Analyze.",
            ),
            q(
                "What becomes the binding constraint as a DMTA loop matures?",
                (
                    opt("the cost per cycle as gains diminish", correct=True),
                    opt("the number of letters in SMILES"),
                    opt("the color of the compounds"),
                    opt("the patent font"),
                ),
                "Gains shrink each cycle, so cost per cycle dominates.",
            ),
            q(
                "Which remains a hard, unsolved challenge for AI in discovery?",
                (
                    opt("causality, generalization and trust", correct=True),
                    opt("converting SMILES to text"),
                    opt("computing molecular weight"),
                    opt("counting rings"),
                ),
                "Whether a target drives disease, off-distribution skill, and calibrated trust remain hard.",
            ),
        ),
    },
    final=(
        q(
            "What is a key risk of optimizing molecules against a learned property oracle?",
            (
                opt("reward hacking into unsynthesizable molecules", correct=True),
                opt("the oracle becomes too accurate"),
                opt("molecules become too easy to make"),
                opt("no molecules are produced"),
            ),
            "Generators exploit oracle weaknesses; constrain by SA and validity.",
        ),
        q(
            "Self-supervised pretraining is most valuable when what is true?",
            (
                opt("labeled data is scarce", correct=True),
                opt("labeled data is unlimited"),
                opt("no molecules exist"),
                opt("the target is unknown"),
            ),
            "Transfer learning shines in the low-label regime.",
        ),
        q(
            "AlphaFold's pLDDT tells you what?",
            (
                opt("how confident the structure prediction is per residue", correct=True),
                opt("the binding affinity"),
                opt("the clinical phase"),
                opt("the synthetic accessibility"),
            ),
            "pLDDT is per-residue prediction confidence.",
        ),
        q(
            "Active learning aims to do what?",
            (
                opt("reach a good candidate in fewer experiments", correct=True),
                opt("avoid building any model"),
                opt("test every molecule exhaustively"),
                opt("ignore uncertainty"),
            ),
            "It selects the most informative experiments each round.",
        ),
        q(
            "The Pareto front represents what?",
            (
                opt("the set of non-dominated trade-offs across objectives", correct=True),
                opt("the single optimal molecule"),
                opt("the cheapest synthesis route"),
                opt("the largest molecule"),
            ),
            "No point on it is beaten on every objective at once.",
        ),
        q(
            "The modern self-driving lab closes which loop?",
            (
                opt("Design-Make-Test-Analyze", correct=True),
                opt("only Design"),
                opt("only Test"),
                opt("approval and marketing"),
            ),
            "It automates the full DMTA cycle, retraining each turn.",
        ),
    ),
)
