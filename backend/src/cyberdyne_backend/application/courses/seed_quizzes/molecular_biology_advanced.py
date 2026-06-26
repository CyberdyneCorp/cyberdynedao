"""Quiz questions for the Molecular Biology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Gene regulation: operons and transcription factors": (
            q(
                "In the lac operon, what happens to the repressor when lactose is present?",
                (
                    opt(
                        "Allolactose inactivates the repressor, releasing it from the operator",
                        correct=True,
                    ),
                    opt("The repressor binds more tightly"),
                    opt("The repressor is permanently destroyed"),
                    opt("Lactose has no effect on the repressor"),
                ),
                "Lactose's isomer allolactose is the inducer that frees the operator.",
            ),
            q(
                "When glucose is scarce, high cAMP and CAP do what to the lac operon?",
                (
                    opt("Activate transcription (positive control)", correct=True),
                    opt("Repress transcription"),
                    opt("Delete the operon"),
                    opt("Convert it into RNA directly"),
                ),
                "CAP-cAMP boosts transcription when glucose (the preferred sugar) is low.",
            ),
            q(
                "Cooperative transcription-factor binding makes gene activation:",
                (
                    opt("Switch-like (a steep sigmoid with high Hill coefficient)", correct=True),
                    opt("Perfectly linear with activator"),
                    opt("Completely random"),
                    opt("Independent of activator concentration"),
                ),
                "Cooperativity sharpens the dose-response into an on/off switch.",
            ),
        ),
        "Epigenetics and chromatin regulation": (
            q(
                "DNA methylation at CpG islands generally has what effect?",
                (
                    opt("Gene silencing", correct=True),
                    opt("Gene activation"),
                    opt("DNA replication"),
                    opt("Codon reading"),
                ),
                "Methylated promoter CpG islands typically repress transcription.",
            ),
            q(
                "Which histone mark is associated with active (open) chromatin?",
                (
                    opt("H3K4me3 / H3K27ac", correct=True),
                    opt("H3K9me3"),
                    opt("H3K27me3"),
                    opt("CpG methylation"),
                ),
                "H3K4me3 and H3K27ac mark active promoters and enhancers.",
            ),
            q(
                "In the writer/eraser/reader model, what does a 'reader' do?",
                (
                    opt(
                        "Recognizes and interprets a histone mark via a binding domain",
                        correct=True,
                    ),
                    opt("Adds the mark"),
                    opt("Removes the mark"),
                    opt("Cuts the DNA"),
                ),
                "Readers (e.g. bromodomains) bind marks and recruit downstream machinery.",
            ),
        ),
        "RNA interference and non-coding RNA": (
            q(
                "Which enzyme processes pre-miRNA into the mature miRNA duplex in the cytoplasm?",
                (
                    opt("Dicer", correct=True),
                    opt("Drosha"),
                    opt("Taq polymerase"),
                    opt("Cas9"),
                ),
                "Drosha acts in the nucleus; Dicer cuts pre-miRNA in the cytoplasm.",
            ),
            q(
                "What is the role of the RISC complex (with Argonaute)?",
                (
                    opt(
                        "It uses the small RNA as a guide to silence complementary mRNAs",
                        correct=True,
                    ),
                    opt("It replicates DNA"),
                    opt("It transcribes promoters"),
                    opt("It splices introns"),
                ),
                "RISC carries the guide strand to target and repress or cleave mRNA.",
            ),
            q(
                "Which long non-coding RNA is central to X-chromosome inactivation?",
                (
                    opt("XIST", correct=True),
                    opt("tRNA-Met"),
                    opt("18S rRNA"),
                    opt("U6 snRNA"),
                ),
                "XIST coats the inactive X and recruits silencing machinery.",
            ),
        ),
        "CRISPR-Cas genome editing": (
            q(
                "What directs Cas9 to its target sequence?",
                (
                    opt("A guide RNA that base-pairs with the target", correct=True),
                    opt("A signal peptide"),
                    opt("A poly-A tail"),
                    opt("The ribosome"),
                ),
                "The gRNA programs Cas9 for a 20-nt target next to a PAM.",
            ),
            q(
                "Repairing a Cas9-induced break by NHEJ typically produces:",
                (
                    opt("Small insertions/deletions that knock out the gene", correct=True),
                    opt("A precise programmed substitution"),
                    opt("A perfect restoration every time"),
                    opt("A new chromosome"),
                ),
                "Error-prone NHEJ creates indels; HDR with a donor gives precise edits.",
            ),
            q(
                "Base editors differ from standard Cas9 because they:",
                (
                    opt(
                        "Convert one base to another without making a double-strand break",
                        correct=True,
                    ),
                    opt("Always cut both strands"),
                    opt("Require no guide RNA"),
                    opt("Edit only RNA"),
                ),
                "Base editors chemically convert a base, avoiding double-strand breaks.",
            ),
        ),
        "Next-generation sequencing": (
            q(
                "Illumina sequencing reads DNA by which principle?",
                (
                    opt(
                        "Sequencing by synthesis with reversible fluorescent terminators",
                        correct=True,
                    ),
                    opt("Edman degradation"),
                    opt("Mass spectrometry of peptides"),
                    opt("Restriction mapping only"),
                ),
                "Each cycle incorporates and images a labeled reversible terminator.",
            ),
            q(
                "A Phred quality score of Q30 corresponds to an error probability of:",
                (
                    opt("1 in 1000", correct=True),
                    opt("1 in 10"),
                    opt("1 in 100"),
                    opt("1 in 100000"),
                ),
                "Q = -10 log10(P_error), so Q30 means P = 10^-3.",
            ),
            q(
                "Which platforms are best suited to long single-molecule reads?",
                (
                    opt("PacBio SMRT and Oxford Nanopore", correct=True),
                    opt("Sanger capillary only"),
                    opt("Illumina short-read only"),
                    opt("qPCR machines"),
                ),
                "PacBio and Nanopore read tens of kilobases per molecule.",
            ),
        ),
        "AI and deep learning in genomics": (
            q(
                "What does a model like Enformer predict from DNA sequence?",
                (
                    opt("Gene expression using long-range attention", correct=True),
                    opt("The 3D structure of proteins only"),
                    opt("PCR cycle thresholds"),
                    opt("Restriction sites"),
                ),
                "Enformer uses transformer attention over ~100 kb to predict expression.",
            ),
            q(
                "AlphaFold is best known for predicting:",
                (
                    opt("Protein 3D structure from amino-acid sequence", correct=True),
                    opt("mRNA decay rates"),
                    opt("CRISPR PAM sites"),
                    opt("DNA melting temperature"),
                ),
                "AlphaFold predicts protein structure from sequence with high accuracy.",
            ),
            q(
                "Why is a held-out evaluation set important for genomic deep-learning models?",
                (
                    opt(
                        "To detect overfitting and distribution shift rather than overstate accuracy",
                        correct=True,
                    ),
                    opt("To increase training data size"),
                    opt("To make models run faster"),
                    opt("To remove the need for any labels"),
                ),
                "Proper held-out evaluation guards against overfitting and batch/domain effects.",
            ),
        ),
    },
    final=(
        q(
            "Eukaryotic enhancers can regulate promoters over long distances by:",
            (
                opt("DNA looping that brings transcription factors to the promoter", correct=True),
                opt("Being translated into protein"),
                opt("Reverse transcription"),
                opt("Cutting the chromosome"),
            ),
            "Looping and Mediator bridge distal enhancers to the promoter.",
        ),
        q(
            "Which epigenetic mark is generally repressive?",
            (
                opt("H3K27me3 and CpG methylation", correct=True),
                opt("H3K4me3"),
                opt("H3K27ac"),
                opt("None are repressive"),
            ),
            "H3K27me3 and promoter CpG methylation are silencing marks.",
        ),
        q(
            "RNA interference silences genes using:",
            (
                opt("Small RNAs that guide RISC to complementary mRNA", correct=True),
                opt("Large proteins that cut DNA"),
                opt("Reverse transcriptase"),
                opt("The poly-A polymerase"),
            ),
            "miRNA/siRNA loaded into RISC target mRNAs for repression or cleavage.",
        ),
        q(
            "CRISPR-Cas9 makes precise knock-ins when repair uses:",
            (
                opt("Homology-directed repair with a donor template", correct=True),
                opt("Non-homologous end joining"),
                opt("Random mutagenesis"),
                opt("Translation"),
            ),
            "HDR with a supplied donor templates an exact edit.",
        ),
        q(
            "Increasing guide-target mismatches affects Cas9 how?",
            (
                opt("Cleavage efficiency falls steeply, improving specificity", correct=True),
                opt("Cleavage rises with more mismatches"),
                opt("It has no effect"),
                opt("It changes the PAM sequence"),
            ),
            "Mismatches sharply reduce off-target cutting, the basis of specificity.",
        ),
        q(
            "Deep-learning genomic models typically show what as labeled data grows?",
            (
                opt("Improving accuracy with diminishing returns", correct=True),
                opt("Accuracy decreasing with more data"),
                opt("No relationship to data at all"),
                opt("Perfect accuracy from a single example"),
            ),
            "A saturating learning curve motivates self-supervised pretraining.",
        ),
    ),
)
