"""Quiz questions for the Genetics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Genome-wide association studies (GWAS)": (
            q(
                "What is the conventional genome-wide significance threshold in a GWAS?",
                (
                    opt("p < 5 x 10^-8", correct=True),
                    opt("p < 0.05"),
                    opt("p < 0.01"),
                    opt("p < 0.5"),
                ),
                "The stringent threshold corrects for roughly a million independent tests.",
            ),
            q(
                "Population stratification in a GWAS is typically corrected by what?",
                (
                    opt(
                        "Including principal components or using linear mixed models", correct=True
                    ),
                    opt("Removing all common variants"),
                    opt("Ignoring it"),
                    opt("Using a lower sample size"),
                ),
                "PCs and mixed models account for ancestry structure that would cause false positives.",
            ),
            q(
                "Most variants found by GWAS for common diseases are what?",
                (
                    opt("Non-coding and of small effect", correct=True),
                    opt("Protein-truncating and large effect"),
                    opt("Located only on the Y chromosome"),
                    opt("Always the direct causal variant"),
                ),
                "Common-disease GWAS hits are largely regulatory variants with small individual effects.",
            ),
        ),
        "Linkage disequilibrium and fine-mapping": (
            q(
                "Linkage disequilibrium refers to what?",
                (
                    opt("Non-random association of alleles at nearby loci", correct=True),
                    opt("The rate of new mutations"),
                    opt("Random mating in a population"),
                    opt("The number of genes on a chromosome"),
                ),
                "LD is correlation between alleles at linked sites, often measured by r^2.",
            ),
            q(
                "Over many generations, LD between two loci tends to do what?",
                (
                    opt("Decay as recombination breaks up haplotypes", correct=True),
                    opt("Increase without limit"),
                    opt("Stay perfectly constant"),
                    opt("Disappear in a single generation"),
                ),
                "Recombination erodes LD with distance and time.",
            ),
            q(
                "What does fine-mapping aim to produce?",
                (
                    opt("A credible set of likely causal variants", correct=True),
                    opt("A complete protein structure"),
                    opt("A new reference genome"),
                    opt("A list of all genes in the body"),
                ),
                "Methods like SuSiE/FINEMAP give posterior probabilities and a credible set.",
            ),
        ),
        "Polygenic risk scores and genomic prediction": (
            q(
                "A polygenic risk score is computed as what?",
                (
                    opt("A weighted sum of genotypes using per-variant effect sizes", correct=True),
                    opt("The count of chromosomes"),
                    opt("The single largest-effect variant only"),
                    opt("The mutation rate of the genome"),
                ),
                "PRS_i = sum of beta_j times genotype_ij across variants.",
            ),
            q(
                "Why must PRS methods adjust for linkage disequilibrium?",
                (
                    opt("Correlated SNPs would otherwise be double-counted", correct=True),
                    opt("LD increases the mutation rate"),
                    opt("LD removes all signal"),
                    opt("Genotypes cannot be measured otherwise"),
                ),
                "Clumping or Bayesian shrinkage (LDpred2, PRS-CS) handle correlated effects.",
            ),
            q(
                "A major limitation of current polygenic scores is that they do what?",
                (
                    opt("Transfer poorly across ancestries", correct=True),
                    opt("Work equally well in all populations"),
                    opt("Require no training data"),
                    opt("Predict only Mendelian diseases"),
                ),
                "Differing LD and allele frequencies degrade cross-ancestry portability, an equity concern.",
            ),
        ),
        "Medical genetics and pharmacogenomics": (
            q(
                "Which disorder is monogenic (single-gene)?",
                (
                    opt("Cystic fibrosis (CFTR)", correct=True),
                    opt("Type 2 diabetes"),
                    opt("Coronary artery disease"),
                    opt("Common obesity"),
                ),
                "Cystic fibrosis follows clear single-gene inheritance; the others are complex/polygenic.",
            ),
            q(
                "What does the ACMG framework provide?",
                (
                    opt("Criteria to classify variants from benign to pathogenic", correct=True),
                    opt("A method to synthesize proteins"),
                    opt("A way to grow cells in culture"),
                    opt("Rules for naming chromosomes"),
                ),
                "ACMG criteria standardize clinical variant interpretation.",
            ),
            q(
                "Pharmacogenomics matching CYP2D6 metaboliser status to drug dosing is an example of what?",
                (
                    opt("Using genotype to guide drug response and dosing", correct=True),
                    opt("Editing the genome to cure disease"),
                    opt("Predicting eye color"),
                    opt("Sequencing the whole microbiome"),
                ),
                "Pharmacogenomics tailors therapy to a patient's metaboliser genotype.",
            ),
        ),
        "CRISPR genome editing and gene therapy": (
            q(
                "What directs Cas9 to a specific genomic site?",
                (
                    opt("A guide RNA", correct=True),
                    opt("A ribosome"),
                    opt("A restriction enzyme"),
                    opt("A histone"),
                ),
                "The guide RNA base-pairs with the target DNA, positioning Cas9 to cut.",
            ),
            q(
                "Repair of a Cas9 double-strand break by non-homologous end joining typically produces what?",
                (
                    opt("Indels that knock out the gene", correct=True),
                    opt("A precise designed sequence"),
                    opt("No change at all"),
                    opt("A new chromosome"),
                ),
                "NHEJ is error-prone, creating insertions/deletions; HDR with a template gives precise edits.",
            ),
            q(
                "Which technology edits DNA without creating a double-strand break?",
                (
                    opt("Base or prime editing", correct=True),
                    opt("Standard NHEJ knockout"),
                    opt("PCR amplification"),
                    opt("Gel electrophoresis"),
                ),
                "Base and prime editors chemically convert or rewrite bases via a nicking Cas9.",
            ),
        ),
        "Deep learning for variant effect and gene regulation": (
            q(
                "How does a sequence-to-function model like Enformer score a variant's effect?",
                (
                    opt(
                        "By comparing predictions for the reference and alternate alleles",
                        correct=True,
                    ),
                    opt("By counting the variant's chromosome number"),
                    opt("By measuring the patient's blood pressure"),
                    opt("By sequencing the protein directly"),
                ),
                "The effect is the predicted change in molecular readout between ref and alt sequences.",
            ),
            q(
                "AlphaMissense and ESM are used primarily to do what?",
                (
                    opt("Classify missense variants as benign or pathogenic", correct=True),
                    opt("Assemble a genome from reads"),
                    opt("Measure recombination frequency"),
                    opt("Synthesize DNA in the lab"),
                ),
                "These models predict the functional impact of amino-acid-changing variants.",
            ),
            q(
                "A key caveat of deep-learning variant-effect models is what?",
                (
                    opt(
                        "Distribution shift and the gap between molecular prediction and causal disease relevance",
                        correct=True,
                    ),
                    opt("They require no data to train"),
                    opt("They cannot run on a computer"),
                    opt("They only work on prokaryotes"),
                ),
                "Predicting a molecular readout is not the same as proving clinical causality; validation is needed.",
            ),
        ),
    },
    final=(
        q(
            "GWAS uses a very stringent significance threshold mainly because of what?",
            (
                opt("Multiple testing across millions of variants", correct=True),
                opt("Small sample sizes"),
                opt("Low-quality genotyping only"),
                opt("The use of mixed models"),
            ),
            "Testing ~1 million independent variants demands a Bonferroni-style 5 x 10^-8 cutoff.",
        ),
        q(
            "Why is the lead SNP from a GWAS often not the causal variant?",
            (
                opt("Many correlated SNPs in the same LD block all show association", correct=True),
                opt("GWAS never finds real signals"),
                opt("Causal variants are always coding"),
                opt("The lead SNP is chosen at random"),
            ),
            "LD makes whole blocks of variants significant, so fine-mapping is needed to localize cause.",
        ),
        q(
            "Polygenic risk score accuracy as a function of training sample size shows what behavior?",
            (
                opt(
                    "Rising accuracy with diminishing returns toward a heritability ceiling",
                    correct=True,
                ),
                opt("Unlimited linear growth"),
                opt("No relationship at all"),
                opt("Accuracy decreasing with more data"),
            ),
            "Accuracy improves with N but plateaus at a limit set by trait heritability and the SNP panel.",
        ),
        q(
            "Which pairing of variant and clinical action is a pharmacogenomic example?",
            (
                opt("HLA-B*57:01 and abacavir hypersensitivity risk", correct=True),
                opt("CFTR and eye color"),
                opt("BRCA1 and blood type"),
                opt("SRY and lactose tolerance"),
            ),
            "HLA-B*57:01 testing predicts abacavir hypersensitivity, a classic pharmacogenomic use.",
        ),
        q(
            "Prime editing differs from classic CRISPR knockout because it does what?",
            (
                opt("Rewrites sequence without a double-strand break", correct=True),
                opt("Always requires a full double-strand break"),
                opt("Cannot target specific sites"),
                opt("Only deletes whole chromosomes"),
            ),
            "Prime editing uses a nicking Cas9 fused to reverse transcriptase to write new sequence.",
        ),
        q(
            "A recurring equity concern across modern genomic methods (PRS, deep models) is what?",
            (
                opt("Poor transfer across ancestries due to data and LD differences", correct=True),
                opt("That they are too cheap to run"),
                opt("That they ignore the genome entirely"),
                opt("That they work only on Mendelian traits"),
            ),
            "Models trained mostly in one ancestry generalize poorly to others, a major fairness problem.",
        ),
    ),
)
