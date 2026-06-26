"""Quiz questions for the Computational Target Identification - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is a drug target?": (
            q(
                "What is a drug target?",
                (
                    opt(
                        "A biomolecule whose modulation changes the course of a disease",
                        correct=True,
                    ),
                    opt("The disease symptom itself"),
                    opt("The patient population in a trial"),
                    opt("A laboratory reagent used for staining"),
                ),
                "A target is usually a protein whose activity a drug modulates therapeutically.",
            ),
            q(
                "Which two axes run through all of target identification?",
                (
                    opt("Disease relevance and druggability", correct=True),
                    opt("Cost and marketing"),
                    opt("Color and solubility"),
                    opt("Patent length and branding"),
                ),
                "A useful target must be biologically relevant and pharmacologically tractable.",
            ),
            q(
                "Why is a good target usually upstream in disease causation?",
                (
                    opt("Perturbing it can shift the phenotype toward health", correct=True),
                    opt("Upstream molecules are always cheaper to make"),
                    opt("It guarantees zero side effects"),
                    opt("Downstream molecules cannot be measured"),
                ),
                "Causality upstream means modulation propagates a therapeutic change.",
            ),
        ),
        "Disease biology as perturbed networks": (
            q(
                "How is disease best described in systems terms?",
                (
                    opt(
                        "A perturbation of a biological network, not one isolated broken gene",
                        correct=True,
                    ),
                    opt("Always a single point mutation acting alone"),
                    opt("A purely random measurement"),
                    opt("Only an environmental effect with no molecular basis"),
                ),
                "The phenotype emerges from many altered genes and proteins.",
            ),
            q(
                "Which intervention level matches an antisense or siRNA modality?",
                (
                    opt("The mRNA (transcript) level", correct=True),
                    opt("The DNA replication origin"),
                    opt("The protein active site directly"),
                    opt("The cell membrane lipid"),
                ),
                "Antisense and siRNA silence the transcript before translation.",
            ),
            q(
                "What does the midpoint (EC50/IC50) of a dose-response curve tell you?",
                (
                    opt(
                        "The potency: the intervention strength giving half-maximal effect",
                        correct=True,
                    ),
                    opt("The maximum possible effect"),
                    opt("The number of genes mutated"),
                    opt("The molecular weight of the drug"),
                ),
                "The midpoint marks half-maximal response; steepness marks switch-like behaviour.",
            ),
        ),
        "Target classes and modalities": (
            q(
                "Which target class is the single largest for small-molecule drugs?",
                (
                    opt("G-protein-coupled receptors (GPCRs)", correct=True),
                    opt("Histones"),
                    opt("Ribosomal RNAs"),
                    opt("Lipid droplets"),
                ),
                "GPCRs are the largest small-molecule drug target class.",
            ),
            q(
                "Which modality is the natural choice for a secreted cytokine?",
                (
                    opt("An antibody / biologic", correct=True),
                    opt("A competitive active-site inhibitor"),
                    opt("An ion-channel blocker"),
                    opt("A DNA intercalator"),
                ),
                "Secreted and surface proteins are well suited to antibody neutralisation.",
            ),
            q(
                "In Michaelis-Menten kinetics, what does a competitive inhibitor do?",
                (
                    opt(
                        "Raises the apparent Km so more substrate is needed for the same velocity",
                        correct=True,
                    ),
                    opt("Lowers Vmax to zero permanently"),
                    opt("Changes the substrate's molecular formula"),
                    opt("Has no effect on enzyme velocity"),
                ),
                "Competitive inhibition increases apparent Km, shifting the saturation curve right.",
            ),
        ),
        "Differential expression as a first signal": (
            q(
                "What does log2 fold-change measure?",
                (
                    opt(
                        "The ratio of disease to control mean expression on a log2 scale",
                        correct=True,
                    ),
                    opt("The absolute number of cells sequenced"),
                    opt("The p-value of a test"),
                    opt("The length of the gene in base pairs"),
                ),
                "log2FC summarises how much a gene's expression changes between groups.",
            ),
            q(
                "Why must we control the false discovery rate in differential expression?",
                (
                    opt(
                        "Thousands of genes are tested, so some look extreme by chance",
                        correct=True,
                    ),
                    opt("Genes never change by chance"),
                    opt("FDR makes fold-changes larger"),
                    opt("It removes the need for normalisation"),
                ),
                "Multiple testing inflates false positives; BH FDR controls them.",
            ),
            q(
                "Why is differential expression only correlative evidence?",
                (
                    opt(
                        "A gene may change because it drives disease or merely responds to it",
                        correct=True,
                    ),
                    opt("Because expression cannot be measured accurately"),
                    opt("Because fold-changes are always wrong"),
                    opt("Because it proves causation directly"),
                ),
                "DE cannot distinguish driver from passenger on its own.",
            ),
        ),
        "Pathways and biological context": (
            q(
                "Why is a coordinated pathway change more convincing than one gene?",
                (
                    opt(
                        "It points to a coherent mechanism rather than an isolated signal",
                        correct=True,
                    ),
                    opt("Single genes can never be measured"),
                    opt("Pathways ignore statistics"),
                    opt("It guarantees the gene is druggable"),
                ),
                "Concordant changes across a pathway implicate a mechanism.",
            ),
            q(
                "Which resources curate biological pathways and gene sets?",
                (
                    opt("KEGG, Reactome and the Gene Ontology", correct=True),
                    opt("PubMed and arXiv only"),
                    opt("BLAST and Bowtie"),
                    opt("Excel and PowerPoint"),
                ),
                "KEGG, Reactome and GO encode pathway and functional annotations.",
            ),
            q(
                "What statistical test underlies over-representation (enrichment) analysis?",
                (
                    opt("A hypergeometric / Fisher's exact test on the overlap", correct=True),
                    opt("A simple average of expression"),
                    opt("A Fourier transform"),
                    opt("A linear regression of sample order"),
                ),
                "Enrichment compares observed overlap to chance via the hypergeometric test.",
            ),
        ),
        "Binding, affinity and the dose-response idea": (
            q(
                "What does the dissociation constant Kd represent?",
                (
                    opt(
                        "The drug concentration at which half the target is occupied", correct=True
                    ),
                    opt("The molecular weight of the target"),
                    opt("The number of binding sites total"),
                    opt("The speed of diffusion in water"),
                ),
                "Kd is the half-occupancy concentration; smaller Kd means tighter binding.",
            ),
            q(
                "A smaller Kd corresponds to what?",
                (
                    opt("Higher affinity (tighter binding)", correct=True),
                    opt("Lower affinity (weaker binding)"),
                    opt("A larger protein"),
                    opt("No binding at all"),
                ),
                "Affinity is inversely related to Kd.",
            ),
            q(
                "What does a Hill coefficient greater than 1 indicate?",
                (
                    opt("Cooperative, switch-like dose-response behaviour", correct=True),
                    opt("No binding occurs"),
                    opt("The drug is insoluble"),
                    opt("A purely linear response"),
                ),
                "Hill coefficients above 1 reflect positive cooperativity and steeper curves.",
            ),
        ),
    },
    final=(
        q(
            "Which best defines target identification?",
            (
                opt(
                    "Proposing a biomolecule and assembling evidence it is disease-relevant and tractable",
                    correct=True,
                ),
                opt("Choosing a clinical trial endpoint"),
                opt("Naming a marketed drug"),
                opt("Selecting a cell-staining dye"),
            ),
            "It pairs disease relevance with druggability.",
        ),
        q(
            "Which sequence describes the central dogma as interventable steps?",
            (
                opt("DNA -> mRNA -> protein, each blockable by a different modality", correct=True),
                opt("Protein -> DNA -> mRNA"),
                opt("mRNA -> DNA -> lipid"),
                opt("Protein -> lipid -> DNA"),
            ),
            "Different modalities act at the transcript or protein level.",
        ),
        q(
            "Which pairing of target class and modality is correct?",
            (
                opt("Secreted cytokine -> antibody", correct=True),
                opt("Cytosolic enzyme -> antibody"),
                opt("GPCR -> DNA intercalator"),
                opt("Ion channel -> antisense to a lipid"),
            ),
            "Secreted proteins are classic antibody targets.",
        ),
        q(
            "On a volcano plot, where do the most compelling genes sit?",
            (
                opt("Upper corners: large fold-change and high significance", correct=True),
                opt("Exactly at the origin"),
                opt("Along the bottom edge"),
                opt("Only on the left axis"),
            ),
            "Large, confident changes appear in the upper corners.",
        ),
        q(
            "What does enrichment analysis add to a flat gene list?",
            (
                opt("Biological mechanism by finding over-represented pathways", correct=True),
                opt("A higher sequencing depth"),
                opt("A lower molecular weight"),
                opt("A guaranteed causal proof"),
            ),
            "Enrichment maps genes onto coherent pathways and mechanisms.",
        ),
        q(
            "The fraction of target bound versus drug concentration has what shape?",
            (
                opt("A saturating hyperbola approaching full occupancy", correct=True),
                opt("A straight line with no limit"),
                opt("A decaying exponential to zero"),
                opt("A flat horizontal line"),
            ),
            "Occupancy saturates as concentration rises, like enzyme and receptor curves.",
        ),
    ),
)
