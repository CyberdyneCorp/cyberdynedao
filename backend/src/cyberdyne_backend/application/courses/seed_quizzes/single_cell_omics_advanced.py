"""Quiz questions for the Single-Cell & Spatial Omics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Trajectory inference and pseudotime": (
            q(
                "What does pseudotime estimate?",
                (
                    opt("How far a cell has progressed along a continuous process", correct=True),
                    opt("The literal age of the cell in hours"),
                    opt("The cell's chromosome count"),
                    opt("The sequencing depth"),
                ),
                "Pseudotime is a similarity-based ordering, not a real clock.",
            ),
            q(
                "Which tool abstracts clusters into a coarse connectivity graph?",
                (
                    opt("PAGA", correct=True),
                    opt("Cell Ranger"),
                    opt("BLAST"),
                    opt("FastQC"),
                ),
                "PAGA preserves global topology as a cluster-level graph.",
            ),
            q(
                "Trajectory inference is appropriate when the biology is:",
                (
                    opt("Continuous, like differentiation", correct=True),
                    opt("A set of fully discrete, unrelated types"),
                    opt("Purely about DNA mutations"),
                    opt("Independent of expression"),
                ),
                "Continua such as differentiation suit pseudotime ordering.",
            ),
        ),
        "RNA velocity": (
            q(
                "RNA velocity infers direction of change by comparing:",
                (
                    opt("Unspliced (intronic) vs spliced (mature) mRNA", correct=True),
                    opt("DNA vs RNA"),
                    opt("Protein vs lipid"),
                    opt("Two different cells' totals"),
                ),
                "Excess unspliced signals up-regulation; the ratio gives direction.",
            ),
            q(
                "In the kinetic model, gamma represents:",
                (
                    opt("The degradation rate of spliced mRNA", correct=True),
                    opt("The transcription rate"),
                    opt("The splicing rate"),
                    opt("The sequencing depth"),
                ),
                "alpha=transcription, beta=splicing, gamma=degradation.",
            ),
            q(
                "A gene point lying below the steady-state line indicates:",
                (
                    opt("Excess unspliced RNA, i.e. up-regulation", correct=True),
                    opt("The gene is being degraded"),
                    opt("The cell is dead"),
                    opt("No transcription at all"),
                ),
                "Below the line = more unspliced than steady state = increasing.",
            ),
        ),
        "Batch effects and data integration": (
            q(
                "A failure mode of unintegrated multi-batch data is that cells:",
                (
                    opt("Cluster by batch instead of by cell type", correct=True),
                    opt("Lose their barcodes"),
                    opt("All become doublets"),
                    opt("Cannot be sequenced"),
                ),
                "Technical batch variation can dominate biological signal.",
            ),
            q(
                "How does Harmony perform integration?",
                (
                    opt(
                        "Iterative clustering with soft cluster-specific linear corrections",
                        correct=True,
                    ),
                    opt("By deleting one batch entirely"),
                    opt("By folding proteins"),
                    opt("By aligning DNA reads"),
                ),
                "Harmony corrects PCA coordinates iteratively per soft cluster.",
            ),
            q(
                "The central trade-off in integration is between:",
                (
                    opt("Batch mixing and conservation of biological signal", correct=True),
                    opt("Read length and depth"),
                    opt("GC content and gene length"),
                    opt("Speed and color"),
                ),
                "Over-correction erases biology; under-correction leaves batch effects.",
            ),
        ),
        "Deep generative and foundation models": (
            q(
                "scVI models single-cell counts using which likelihood?",
                (
                    opt("Zero-inflated or standard negative binomial", correct=True),
                    opt("Gaussian on raw counts"),
                    opt("Uniform distribution"),
                    opt("Binomial on DNA bases"),
                ),
                "scVI is a VAE with an (ZI)NB count likelihood.",
            ),
            q(
                "What is a single-cell foundation model (e.g. scGPT, Geneformer)?",
                (
                    opt(
                        "A transformer pretrained on millions of cells, then fine-tuned",
                        correct=True,
                    ),
                    opt("A read aligner"),
                    opt("A microfluidic device"),
                    opt("A staining protocol"),
                ),
                "They learn general gene co-expression grammar for transfer tasks.",
            ),
            q(
                "A benefit of scVI's latent space is that it:",
                (
                    opt("Provides a batch-corrected low-dimensional representation", correct=True),
                    opt("Returns the raw FASTQ"),
                    opt("Outputs protein crystal structures"),
                    opt("Removes the need for any sequencing"),
                ),
                "The encoder yields an integrated latent z for downstream use.",
            ),
        ),
        "Spatial transcriptomics": (
            q(
                "What does spatial transcriptomics preserve that scRNA-seq discards?",
                (
                    opt("The tissue coordinates of each measurement", correct=True),
                    opt("The DNA sequence"),
                    opt("The UMI tags"),
                    opt("The sequencing depth"),
                ),
                "ST retains where expression occurs in the tissue.",
            ),
            q(
                "Which is an imaging-based, subcellular-resolution spatial method?",
                (
                    opt("MERFISH / Xenium", correct=True),
                    opt("Visium"),
                    opt("Bulk RNA-seq"),
                    opt("Sanger sequencing"),
                ),
                "MERFISH/Xenium use combinatorial smFISH at subcellular resolution.",
            ),
            q(
                "The key trade-off between spatial technology families is:",
                (
                    opt(
                        "Resolution (imaging) vs transcriptome-wide coverage (sequencing)",
                        correct=True,
                    ),
                    opt("Price vs color"),
                    opt("DNA vs protein"),
                    opt("Speed vs barcode length"),
                ),
                "Imaging is targeted/high-res; sequencing is whole-tx/coarser.",
            ),
        ),
    },
    final=(
        q(
            "Pseudotime provides an ordering; RNA velocity adds:",
            (
                opt("The direction (arrow of time) of the process", correct=True),
                opt("The exact cell age"),
                opt("The DNA mutation rate"),
                opt("The library size"),
            ),
            "Velocity uses spliced/unspliced ratios to orient the trajectory.",
        ),
        q(
            "A correctly integrated dataset should show high batch mixing while:",
            (
                opt("Preserving cell-type (biological) structure", correct=True),
                opt("Merging all cell types into one"),
                opt("Removing all cells"),
                opt("Maximizing the mitochondrial fraction"),
            ),
            "Good integration balances mixing against biology conservation.",
        ),
        q(
            "scVI is best described as a:",
            (
                opt("Variational autoencoder with a negative-binomial count model", correct=True),
                opt("Read aligner"),
                opt("Phylogenetics tool"),
                opt("Microscope"),
            ),
            "scVI learns a batch-conditioned latent space from counts.",
        ),
        q(
            "Single-cell foundation models gain capability primarily by:",
            (
                opt("Pretraining on tens of millions of cells, then fine-tuning", correct=True),
                opt("Using only one labelled sample"),
                opt("Avoiding any neural network"),
                opt("Sequencing deeper per cell"),
            ),
            "Scale of pretraining drives transferable performance.",
        ),
        q(
            "Visium (sequencing-based ST) differs from Xenium (imaging-based) in that Visium:",
            (
                opt("Covers the whole transcriptome but at coarser spot resolution", correct=True),
                opt("Has subcellular resolution and a tiny gene panel"),
                opt("Cannot retain spatial coordinates"),
                opt("Sequences DNA only"),
            ),
            "Sequencing ST trades resolution for transcriptome-wide coverage.",
        ),
        q(
            "Deconvolving a multi-cell Visium spot into cell-type proportions uses tools like:",
            (
                opt("cell2location / RCTD", correct=True),
                opt("BLAST / Bowtie"),
                opt("PyMOL / Chimera"),
                opt("ImageJ / Fiji only"),
            ),
            "These methods estimate cell-type composition within spots.",
        ),
    ),
)
