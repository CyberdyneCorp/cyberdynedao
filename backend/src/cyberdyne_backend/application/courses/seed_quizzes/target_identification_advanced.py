"""Quiz questions for the Computational Target Identification - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "CRISPR dependency screens": (
            q(
                "What does a strongly negative gene dependency score (e.g. CERES/Chronos) mean?",
                (
                    opt(
                        "Knocking out the gene impairs cell survival, i.e. it is essential",
                        correct=True,
                    ),
                    opt("The gene is not expressed"),
                    opt("The gene is on a sex chromosome"),
                    opt("The gene has no orthologs"),
                ),
                "Negative dependency scores reflect dropout of essential-gene knockouts.",
            ),
            q(
                "What is a selective dependency?",
                (
                    opt("A gene essential in disease cells but not in normal cells", correct=True),
                    opt("A gene essential in every cell type"),
                    opt("A gene never essential anywhere"),
                    opt("A gene with no guides in the library"),
                ),
                "Selective dependencies define a therapeutic window.",
            ),
            q(
                "Synthetic lethality (e.g. PARP in BRCA-mutant tumours) is found how?",
                (
                    opt("By contrasting dependency across genetic backgrounds", correct=True),
                    opt("By measuring protein melting temperature"),
                    opt("By sequencing a single gene"),
                    opt("By averaging expression over all tissues"),
                ),
                "Synthetic lethality is a dependency present only in a specific mutant context.",
            ),
        ),
        "Single-cell and spatial target discovery": (
            q(
                "What advantage does single-cell RNA-seq give over bulk for target finding?",
                (
                    opt(
                        "It pinpoints which cell type or state expresses a candidate target",
                        correct=True,
                    ),
                    opt("It measures only the average across all cells"),
                    opt("It sequences DNA, not RNA"),
                    opt("It removes the need for clustering"),
                ),
                "scRNA-seq resolves cell-type-specific expression hidden by bulk averaging.",
            ),
            q(
                "What does spatial transcriptomics add to single-cell data?",
                (
                    opt(
                        "Tissue location of expression, e.g. tumour core versus margin",
                        correct=True,
                    ),
                    opt("Higher sequencing error"),
                    opt("The protein crystal structure"),
                    opt("The patient's age"),
                ),
                "Spatial methods restore the coordinates lost in dissociated single-cell assays.",
            ),
            q(
                "Why is cell-type-restricted expression desirable for a target?",
                (
                    opt(
                        "It improves selectivity and lowers on-target toxicity in vital tissues",
                        correct=True,
                    ),
                    opt("It guarantees a deep binding pocket"),
                    opt("It increases sequencing depth"),
                    opt("It removes the need for validation"),
                ),
                "Restricted expression maps onto therapeutic selectivity.",
            ),
        ),
        "Machine-learning target prediction": (
            q(
                "Why is target prediction often a positive-unlabelled problem?",
                (
                    opt(
                        "Known targets are positives, but unlabelled genes mix true negatives and unknown targets",
                        correct=True,
                    ),
                    opt("Every gene is a confirmed negative"),
                    opt("There are no known targets at all"),
                    opt("All genes are positives"),
                ),
                "Unlabelled genes cannot be assumed negative, complicating training and evaluation.",
            ),
            q(
                "What do graph neural networks learn over a biological knowledge graph?",
                (
                    opt(
                        "A vector embedding per gene from topology, enabling gene-disease link prediction",
                        correct=True,
                    ),
                    opt("The raw DNA sequence only"),
                    opt("The melting temperature of proteins"),
                    opt("The cost of each experiment"),
                ),
                "GNNs/KG embeddings frame target discovery as link prediction.",
            ),
            q(
                "Why use temporal (time-split) validation for target prediction models?",
                (
                    opt(
                        "To prevent leakage by testing on targets discovered after the training cutoff",
                        correct=True,
                    ),
                    opt("To make training faster"),
                    opt("To increase the read length"),
                    opt("To avoid using any features"),
                ),
                "Temporal holdout mimics prospective discovery and guards against leakage.",
            ),
        ),
        "Structure-based and AI druggability": (
            q(
                "How did AlphaFold change structure-based target assessment?",
                (
                    opt(
                        "It provided high-quality predicted structures for nearly the whole proteome",
                        correct=True,
                    ),
                    opt("It eliminated the need for any pocket detection"),
                    opt("It replaced all genetic evidence"),
                    opt("It only works on RNA"),
                ),
                "Proteome-wide models expanded structure-based analysis beyond solved structures.",
            ),
            q(
                "What does a diffusion model like DiffDock predict?",
                (
                    opt("Ligand binding poses in the target", correct=True),
                    opt("The GWAS p-value of a locus"),
                    opt("The mRNA half-life"),
                    opt("The patient's prognosis"),
                ),
                "DiffDock is a generative model for protein-ligand docking poses.",
            ),
            q(
                "Why must predicted-structure confidence (pLDDT/PAE) gate downstream use?",
                (
                    opt(
                        "Low-confidence or disordered regions mislead pocket detection",
                        correct=True,
                    ),
                    opt("Confidence has no bearing on reliability"),
                    opt("High confidence always means undruggable"),
                    opt("Confidence only affects file size"),
                ),
                "Only high-confidence regions give trustworthy structural signal.",
            ),
        ),
        "Expanding the druggable space: new modalities": (
            q(
                "How does a PROTAC act on its target?",
                (
                    opt(
                        "It recruits an E3 ligase to ubiquitinate and degrade the target",
                        correct=True,
                    ),
                    opt("It permanently blocks the active site only"),
                    opt("It edits the target's DNA"),
                    opt("It increases the target's transcription"),
                ),
                "PROTACs are bifunctional degraders bridging target and E3 ligase.",
            ),
            q(
                "Why can targeted degradation reach undruggable proteins lacking active sites?",
                (
                    opt(
                        "It needs only a binding handle, not a functional active-site inhibitor",
                        correct=True,
                    ),
                    opt("It requires a deep catalytic pocket"),
                    opt("It only works on enzymes"),
                    opt("It needs no binding at all"),
                ),
                "Event-driven degradation needs ligandability, not occupancy of a catalytic site.",
            ),
            q(
                "What does it mean that degraders are catalytic (event-driven)?",
                (
                    opt(
                        "One degrader can destroy many target copies, enabling deep knockdown at low dose",
                        correct=True,
                    ),
                    opt("Each degrader binds one target permanently and is consumed"),
                    opt("Degraders require stoichiometric saturation like inhibitors"),
                    opt("Degradation only happens once per cell"),
                ),
                "Recycled degraders give sub-stoichiometric, durable target loss.",
            ),
        ),
        "Target validation, safety and reverse translation": (
            q(
                "What distinguishes pharmacological from genetic validation?",
                (
                    opt(
                        "It uses tool compounds and confirms effects track target engagement",
                        correct=True,
                    ),
                    opt("It only knocks out the gene with CRISPR"),
                    opt("It avoids any perturbation"),
                    opt("It measures only mRNA levels"),
                ),
                "Pharmacological validation ties phenotype to measured engagement of the target.",
            ),
            q(
                "Why are human loss-of-function variants in gnomAD reassuring for safety?",
                (
                    opt(
                        "Healthy LoF carriers suggest the target can be inhibited without harm",
                        correct=True,
                    ),
                    opt("They prove the target is undruggable"),
                    opt("They increase off-target binding"),
                    opt("They raise the molecular weight"),
                ),
                "Tolerated human LoF is evidence of an acceptable safety profile.",
            ),
            q(
                "What does reverse translation contribute?",
                (
                    opt(
                        "Feeding clinical and human data back to refine which evidence predicts success",
                        correct=True,
                    ),
                    opt("Translating proteins into RNA"),
                    opt("Reversing the DNA sequence"),
                    opt("Removing all validation steps"),
                ),
                "Reverse translation closes the loop from clinic back to discovery.",
            ),
        ),
    },
    final=(
        q(
            "A selective CRISPR dependency is most useful because it indicates what?",
            (
                opt(
                    "A therapeutic window: essential in disease cells, dispensable in normal cells",
                    correct=True,
                ),
                opt("The gene is essential everywhere"),
                opt("The gene is never essential"),
                opt("The gene is on the Y chromosome"),
            ),
            "Selective dependencies separate disease cells from normal cells.",
        ),
        q(
            "What is the chief advantage of single-cell over bulk profiling for targets?",
            (
                opt(
                    "Resolving the specific cell type/state expressing a candidate target",
                    correct=True,
                ),
                opt("Lower cost per sample only"),
                opt("Reading DNA instead of RNA"),
                opt("Avoiding any normalisation"),
            ),
            "Single-cell resolution exposes the disease-driving cell type.",
        ),
        q(
            "Why is AUPRC preferred over accuracy for target-prediction models?",
            (
                opt(
                    "Positives are rare, so accuracy is misleading on imbalanced data", correct=True
                ),
                opt("AUPRC ignores the predictions"),
                opt("Accuracy is impossible to compute"),
                opt("AUPRC requires no labels"),
            ),
            "With few positives, precision-recall metrics are the honest choice.",
        ),
        q(
            "AlphaFold's main impact on target assessment was to provide what?",
            (
                opt(
                    "Proteome-wide predicted structures for previously structure-less targets",
                    correct=True,
                ),
                opt("A new sequencing chemistry"),
                opt("A replacement for genetic evidence"),
                opt("A clinical trial design"),
            ),
            "Predicted structures expanded structure-based druggability proteome-wide.",
        ),
        q(
            "Which property lets PROTACs target proteins lacking a deep active site?",
            (
                opt(
                    "They need only a binding handle and act catalytically via degradation",
                    correct=True,
                ),
                opt("They require a deep catalytic pocket"),
                opt("They edit the genome directly"),
                opt("They work only on GPCRs"),
            ),
            "Event-driven degradation needs ligandability, not occupancy of a functional site.",
        ),
        q(
            "What is the gold standard for target validation?",
            (
                opt(
                    "Convergent orthogonal evidence across systems plus a sound safety profile",
                    correct=True,
                ),
                opt("A single cell-line experiment"),
                opt("One literature mention"),
                opt("A single GWAS hit alone"),
            ),
            "Orthogonal validation and safety together de-risk a target.",
        ),
    ),
)
