"""Quiz questions for the Single-Cell & Spatial Omics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why single cell? The limits of bulk": (
            q(
                "What key information does bulk RNA-seq lose that single-cell recovers?",
                (
                    opt("The cell-to-cell distribution of expression", correct=True),
                    opt("The total RNA mass of the sample"),
                    opt("The DNA sequence of each gene"),
                    opt("The pH of the tissue"),
                ),
                "Bulk reports only the average; single-cell recovers the full distribution.",
            ),
            q(
                "Two samples can have the same bulk mean for a gene but differ how?",
                (
                    opt("In the fraction of cells expressing it and at what level", correct=True),
                    opt("Only in their total sequencing cost"),
                    opt("Only in the gene's exon count"),
                    opt("They cannot differ at all if the mean matches"),
                ),
                "Identical means can hide very different per-cell distributions.",
            ),
            q(
                "Why is single-cell especially useful for rare populations?",
                (
                    opt("Rare cells are averaged away in bulk but resolved per cell", correct=True),
                    opt("Rare cells have more RNA than common cells"),
                    opt("Bulk sequencing only reads rare cells"),
                    opt("Rare cells cannot be sequenced in bulk at all"),
                ),
                "A 10% population is diluted in a bulk average but visible per cell.",
            ),
        ),
        "What scRNA-seq measures": (
            q(
                "What molecule does scRNA-seq directly count per gene per cell?",
                (
                    opt("mRNA transcripts", correct=True),
                    opt("Genomic DNA copies"),
                    opt("Proteins"),
                    opt("Lipids"),
                ),
                "scRNA-seq quantifies mRNA, a proxy for gene activity.",
            ),
            q(
                "What distinguishes full-length (Smart-seq) from tag-based droplet methods?",
                (
                    opt(
                        "Full-length covers the whole transcript; tag-based reads one end",
                        correct=True,
                    ),
                    opt("Full-length needs no reverse transcription"),
                    opt("Tag-based methods sequence DNA, not RNA"),
                    opt("Full-length methods process more cells per run"),
                ),
                "Smart-seq is high-sensitivity/low-throughput; droplet is the reverse.",
            ),
            q(
                "Why does the number of detected genes saturate with sequencing depth?",
                (
                    opt(
                        "Extra reads increasingly re-sequence already-seen molecules", correct=True
                    ),
                    opt("Genes are deleted at high depth"),
                    opt("The sequencer stops at a fixed gene count"),
                    opt("Deeper reads create new genes"),
                ),
                "Capture is finite, so detection plateaus as depth rises.",
            ),
        ),
        "Droplets, barcodes and UMIs": (
            q(
                "What does a cell barcode identify?",
                (
                    opt("Which droplet/cell a transcript came from", correct=True),
                    opt("Which individual mRNA molecule it is"),
                    opt("The gene's chromosome"),
                    opt("The sequencing machine used"),
                ),
                "All transcripts from one bead share its cell barcode.",
            ),
            q(
                "What is the purpose of a unique molecular identifier (UMI)?",
                (
                    opt(
                        "To tag each original mRNA so PCR duplicates can be collapsed", correct=True
                    ),
                    opt("To label which cell type a cell is"),
                    opt("To store the gene's protein sequence"),
                    opt("To increase sequencing depth"),
                ),
                "Identical cell+gene+UMI reads collapse to one molecule, removing PCR bias.",
            ),
            q(
                "How does the doublet rate change as more cells are loaded?",
                (
                    opt("It rises (roughly linearly) with cells loaded", correct=True),
                    opt("It falls with more cells"),
                    opt("It is independent of loading"),
                    opt("It drops to zero above a threshold"),
                ),
                "More cells per droplet volume increases the chance of two cells per droplet.",
            ),
        ),
        "The count matrix": (
            q(
                "What do the rows and columns of a standard count matrix represent?",
                (
                    opt("Rows are cells, columns are genes", correct=True),
                    opt("Rows are chromosomes, columns are samples"),
                    opt("Rows are reads, columns are barcodes"),
                    opt("Rows are proteins, columns are pathways"),
                ),
                "Each entry is the UMI count of a gene in a cell.",
            ),
            q(
                "Why is the single-cell count matrix mostly zeros?",
                (
                    opt(
                        "Limited capture and biological off-states leave most entries empty",
                        correct=True,
                    ),
                    opt("All genes are silent in every cell"),
                    opt("Zeros are added artificially for storage"),
                    opt("The sequencer rounds all counts to zero"),
                ),
                "Sparsity arises from true off-genes plus technical dropouts.",
            ),
            q(
                "A technical zero (dropout) means what?",
                (
                    opt("A transcript was present but not captured", correct=True),
                    opt("The gene does not exist in the genome"),
                    opt("The cell is dead"),
                    opt("The gene is always off"),
                ),
                "Dropouts are missed-capture zeros, distinct from true biological zeros.",
            ),
        ),
        "From droplets to real cells: basic QC": (
            q(
                "Why does a high mitochondrial fraction flag a low-quality cell?",
                (
                    opt(
                        "Membrane rupture leaks cytoplasmic mRNA but retains mitochondria",
                        correct=True,
                    ),
                    opt("Mitochondrial genes are always artifacts"),
                    opt("Healthy cells have no mitochondrial RNA"),
                    opt("High mito % means the cell is a doublet"),
                ),
                "Dying cells lose cytoplasmic RNA, raising the mito proportion.",
            ),
            q(
                "What does the 'knee' in a barcode rank plot separate?",
                (
                    opt("Real cells from empty/ambient droplets", correct=True),
                    opt("T cells from B cells"),
                    opt("Spliced from unspliced RNA"),
                    opt("Genes from chromosomes"),
                ),
                "Left of the knee are cell-containing barcodes; right is background.",
            ),
            q(
                "Which is NOT a standard per-cell QC metric?",
                (
                    opt("The GC content of the reference genome", correct=True),
                    opt("Total counts (library size)"),
                    opt("Number of detected genes"),
                    opt("Mitochondrial fraction"),
                ),
                "QC uses counts, gene count and mito %; genome GC is not per-cell.",
            ),
        ),
    },
    final=(
        q(
            "The main advantage of scRNA-seq over bulk RNA-seq is that it:",
            (
                opt("Resolves heterogeneity and cell-type composition", correct=True),
                opt("Sequences DNA instead of RNA"),
                opt("Avoids any need for amplification"),
                opt("Is always cheaper per sample"),
            ),
            "Single-cell recovers per-cell distributions and cell types hidden in bulk.",
        ),
        q(
            "In a droplet experiment, the ideal droplet contains:",
            (
                opt("One cell and one barcoded bead", correct=True),
                opt("Two cells and two beads"),
                opt("Only oil"),
                opt("One bead and no cell"),
            ),
            "One cell plus one bead enables correct barcoding of that cell's RNA.",
        ),
        q(
            "Collapsing reads by UMI converts read counts into:",
            (
                opt("Original molecule counts, removing PCR bias", correct=True),
                opt("Protein abundances"),
                opt("Genome coverage depth"),
                opt("Cell-type labels"),
            ),
            "Deduplicating by UMI yields true molecule counts.",
        ),
        q(
            "The single-cell count matrix is best described as:",
            (
                opt("A large, sparse cells-by-genes table of UMI counts", correct=True),
                opt("A dense genes-by-chromosomes table"),
                opt("A list of protein sequences"),
                opt("A phylogenetic tree"),
            ),
            "Cells x genes, mostly zeros, stored as AnnData or Seurat objects.",
        ),
        q(
            "A cell with very low total counts and few detected genes is likely:",
            (
                opt("An empty droplet or low-quality barcode to be filtered", correct=True),
                opt("The highest-quality cell in the run"),
                opt("A doublet that should be kept"),
                opt("A reference genome entry"),
            ),
            "Low library size and gene count signal empty/poor barcodes.",
        ),
        q(
            "Which tool produces a count matrix from raw single-cell reads?",
            (
                opt("Cell Ranger / STARsolo / alevin-fry", correct=True),
                opt("BLAST"),
                opt("PyMOL"),
                opt("ImageJ"),
            ),
            "These pipelines align reads, assign barcodes and collapse UMIs.",
        ),
    ),
)
