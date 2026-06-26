"""Quiz questions for the Genomics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Genome assembly: de Bruijn and overlap graphs": (
            q(
                "In a de Bruijn graph assembler, what are the nodes typically?",
                (
                    opt("Length-(k-1) words, with k-mers as edges", correct=True),
                    opt("Whole reads, with overlaps as edges"),
                    opt("Individual chromosomes"),
                    opt("Single nucleotides only"),
                ),
                "DBG nodes are (k-1)-mers; finding a genome path is an Eulerian problem.",
            ),
            q(
                "What does the N50 statistic measure?",
                (
                    opt(
                        "The contig length at which 50% of the assembly is in contigs that long or longer",
                        correct=True,
                    ),
                    opt("The total number of reads"),
                    opt("The average sequencing error rate"),
                    opt("The GC content of the assembly"),
                ),
                "N50 summarizes assembly contiguity.",
            ),
            q(
                "Which assembly paradigm is most associated with long-read data?",
                (
                    opt("Overlap-Layout-Consensus (OLC)", correct=True),
                    opt("De Bruijn graphs only"),
                    opt("Smith-Waterman alignment"),
                    opt("Bonferroni correction"),
                ),
                "OLC (Canu, hifiasm) suits long, noisier reads; DBG suits short reads.",
            ),
        ),
        "Genome annotation": (
            q(
                "What distinguishes structural from functional annotation?",
                (
                    opt(
                        "Structural locates features; functional assigns roles/identities",
                        correct=True,
                    ),
                    opt("They are the same thing"),
                    opt("Structural is only for proteins"),
                    opt("Functional only masks repeats"),
                ),
                "Structural = where features are; functional = what they do (GO, pathways).",
            ),
            q(
                "What statistical model underlies ab initio gene predictors like AUGUSTUS?",
                (
                    opt("Hidden Markov Models of splice sites and codons", correct=True),
                    opt("Linear regression on coverage"),
                    opt("k-means clustering of reads"),
                    opt("Bonferroni correction"),
                ),
                "HMMs model signal sequences and codon bias.",
            ),
            q(
                "Why are repeats masked before gene prediction?",
                (
                    opt("To avoid spurious gene calls in repetitive DNA", correct=True),
                    opt("To delete all genes"),
                    opt("To increase the error rate"),
                    opt("To translate them into proteins"),
                ),
                "RepeatMasker masks repeats so predictors do not call false genes.",
            ),
        ),
        "Sequence alignment algorithms": (
            q(
                "Which algorithm performs optimal local alignment?",
                (
                    opt("Smith-Waterman", correct=True),
                    opt("Needleman-Wunsch"),
                    opt("BWA-MEM indexing"),
                    opt("k-means"),
                ),
                "Smith-Waterman finds the best local subsequence; Needleman-Wunsch is global.",
            ),
            q(
                "What is the purpose of an affine gap penalty?",
                (
                    opt("Charge a larger opening cost and smaller extension cost", correct=True),
                    opt("Forbid all gaps"),
                    opt("Make every gap free"),
                    opt("Penalize matches"),
                ),
                "w(g) = o + e*g favours one long indel over many short ones.",
            ),
            q(
                "What is the time complexity of dynamic-programming alignment of two sequences?",
                (
                    opt("O(mn)", correct=True),
                    opt("O(1)"),
                    opt("O(log n)"),
                    opt("O(n!)"),
                ),
                "Filling the m-by-n scoring matrix is quadratic.",
            ),
        ),
        "Variant calling and filtering": (
            q(
                "What does GATK HaplotypeCaller do that simple pileup callers do not?",
                (
                    opt("Locally reassembles reads into candidate haplotypes", correct=True),
                    opt("Skips genotype likelihoods entirely"),
                    opt("Aligns to a graph genome only"),
                    opt("Performs RNA-seq quantification"),
                ),
                "Local reassembly improves indel and SNP calling near variants.",
            ),
            q(
                "Which file format stores called variants?",
                (
                    opt("VCF", correct=True),
                    opt("FASTQ"),
                    opt("BAM only"),
                    opt("FASTA"),
                ),
                "VCF holds variants with QUAL, DP and genotype fields.",
            ),
            q(
                "The genotype posterior P(G|D) is proportional to:",
                (
                    opt("P(D|G) * P(G), the likelihood times the prior", correct=True),
                    opt("P(G) only"),
                    opt("The read length"),
                    opt("The Bonferroni threshold"),
                ),
                "Bayes' rule combines the read likelihood with a genotype prior.",
            ),
        ),
        "Genome-wide association studies": (
            q(
                "What is the conventional genome-wide significance threshold?",
                (
                    opt("p < 5e-8", correct=True),
                    opt("p < 0.05"),
                    opt("p < 0.5"),
                    opt("p < 1"),
                ),
                "Bonferroni for ~1 million independent tests gives 5e-8.",
            ),
            q(
                "Why must GWAS adjust for population structure?",
                (
                    opt("To avoid spurious associations from ancestry differences", correct=True),
                    opt("To increase the number of SNPs"),
                    opt("To shorten the reads"),
                    opt("To remove the phenotype"),
                ),
                "PCs or mixed models control for confounding by structure.",
            ),
            q(
                "An associated SNP is often not causal because it:",
                (
                    opt("Tags a region through linkage disequilibrium", correct=True),
                    opt("Has no genomic position"),
                    opt("Is always in a repeat"),
                    opt("Cannot be genotyped"),
                ),
                "LD makes the lead SNP a marker for the true causal variant nearby.",
            ),
        ),
    },
    final=(
        q(
            "Which assemblers use de Bruijn graphs for short reads?",
            (
                opt("SPAdes and Velvet", correct=True),
                opt("Canu and hifiasm"),
                opt("BLAST and BWA"),
                opt("DESeq2 and edgeR"),
            ),
            "DBG assemblers (SPAdes, Velvet) target short reads; OLC targets long reads.",
        ),
        q(
            "Functional annotation typically assigns:",
            (
                opt("GO terms, gene names and pathway roles", correct=True),
                opt("Only the chromosome number"),
                opt("Only the read length"),
                opt("Only the Phred score"),
            ),
            "Functional annotation gives biological identity and roles.",
        ),
        q(
            "Needleman-Wunsch versus Smith-Waterman differ in that:",
            (
                opt("NW is global (end-to-end), SW is local", correct=True),
                opt("NW is local, SW is global"),
                opt("Both are heuristics like BLAST"),
                opt("Neither uses dynamic programming"),
            ),
            "NW aligns full sequences; SW finds the best local region.",
        ),
        q(
            "What is VQSR used for in GATK workflows?",
            (
                opt("Modelling true vs artifactual variants to filter calls", correct=True),
                opt("Aligning reads to the reference"),
                opt("Assembling contigs"),
                opt("Calling cell types in scRNA-seq"),
            ),
            "Variant Quality Score Recalibration filters raw calls.",
        ),
        q(
            "In GWAS, the effect of a SNP on a binary disease is usually reported as:",
            (
                opt("An odds ratio from logistic regression", correct=True),
                opt("An N50"),
                opt("A CIGAR string"),
                opt("A Phred score"),
            ),
            "Logistic regression yields odds ratios for case/control traits.",
        ),
        q(
            "Variant detection sensitivity as a function of depth tends to:",
            (
                opt("Rise and then saturate (diminishing returns)", correct=True),
                opt("Fall to zero with more depth"),
                opt("Stay perfectly flat"),
                opt("Oscillate forever"),
            ),
            "Past ~30x, extra depth adds little SNP sensitivity.",
        ),
    ),
)
