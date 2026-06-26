"""Quiz questions for the Proteomics & Metabolomics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Tandem MS (MS/MS) & peptide fragmentation": (
            q(
                "Why is the precursor mass alone usually insufficient to identify a peptide?",
                (
                    opt("many different sequences can share the same mass", correct=True),
                    opt("mass cannot be measured for peptides"),
                    opt("peptides have no mass"),
                    opt("the detector ignores precursors"),
                ),
                "MS/MS adds sequence information that mass alone cannot provide.",
            ),
            q(
                "CID/HCD of a peptide backbone primarily produces:",
                (
                    opt("b-ions and y-ions", correct=True),
                    opt("only neutral fragments"),
                    opt("DNA fragments"),
                    opt("c-ions and z-ions only"),
                ),
                "Collision-induced dissociation cleaves the amide bond giving b/y ions.",
            ),
            q(
                "The mass difference between consecutive y-ions equals:",
                (
                    opt("the mass of one amino acid residue", correct=True),
                    opt("the mass of a water molecule only"),
                    opt("always 79.966 Da"),
                    opt("the precursor mass"),
                ),
                "Spacing between adjacent y-ions spells the sequence one residue at a time.",
            ),
        ),
        "Database search & peptide-spectrum matches": (
            q(
                "What does a database search engine do with a protein FASTA file?",
                (
                    opt(
                        "performs an in silico digest and predicts fragment ions to match spectra",
                        correct=True,
                    ),
                    opt("translates it into DNA"),
                    opt("runs the chromatography"),
                    opt("ionizes the sample"),
                ),
                "It digests in silico, predicts b/y ions, and scores against observed spectra.",
            ),
            q(
                "A PSM is a:",
                (
                    opt("peptide-spectrum match with a confidence score", correct=True),
                    opt("protein structure model"),
                    opt("plasmid sequence map"),
                    opt("phosphate site marker"),
                ),
                "A PSM links one spectrum to one candidate peptide with a score.",
            ),
            q(
                "Carbamidomethylation of cysteine is typically set as a:",
                (
                    opt("fixed modification", correct=True),
                    opt("decoy sequence"),
                    opt("variable modification only"),
                    opt("precursor charge"),
                ),
                "Alkylation puts carbamidomethyl on nearly all Cys, so it is a fixed mod.",
            ),
        ),
        "False discovery rate & target-decoy": (
            q(
                "What does the false discovery rate (FDR) estimate?",
                (
                    opt(
                        "the expected fraction of accepted identifications that are incorrect",
                        correct=True,
                    ),
                    opt("the total number of spectra acquired"),
                    opt("the chromatographic run time"),
                    opt("the sample concentration"),
                ),
                "FDR is the expected proportion of false positives among accepted hits.",
            ),
            q(
                "How are decoy sequences typically generated?",
                (
                    opt("by reversing or shuffling the target sequences", correct=True),
                    opt("by adding random PTMs"),
                    opt("by translating mRNA"),
                    opt("by using only real proteins"),
                ),
                "Reversed/shuffled sequences cannot be correct, so they estimate false hits.",
            ),
            q(
                "The community-standard FDR threshold in proteomics is:",
                (
                    opt("1%", correct=True),
                    opt("50%"),
                    opt("0%"),
                    opt("25%"),
                ),
                "1% FDR is standard at PSM, peptide and protein levels.",
            ),
        ),
        "Acquisition strategies: DDA vs DIA": (
            q(
                "In DDA, which precursors are selected for MS2?",
                (
                    opt("the top-N most intense precursors per cycle", correct=True),
                    opt("all precursors in every window"),
                    opt("a random one per minute"),
                    opt("only decoy ions"),
                ),
                "Data-dependent acquisition fragments the most intense precursors.",
            ),
            q(
                "A key drawback of DDA is:",
                (
                    opt("stochastic sampling causes missing values across runs", correct=True),
                    opt("it cannot measure any peptides"),
                    opt("it requires no mass analyzer"),
                    opt("it only works for DNA"),
                ),
                "Top-N selection misses low-abundance peptides, producing missing values.",
            ),
            q(
                "In DIA, the analyzer:",
                (
                    opt("fragments all precursors within fixed isolation windows", correct=True),
                    opt("fragments only the single most intense ion"),
                    opt("never fragments anything"),
                    opt("measures only retention time"),
                ),
                "DIA co-fragments everything in each window, sampling comprehensively.",
            ),
        ),
        "Quantification: label-free, SILAC & TMT": (
            q(
                "Label-free quantification (LFQ) compares:",
                (
                    opt("MS1 peak areas or spectral counts across separate runs", correct=True),
                    opt("reporter ion intensities only"),
                    opt("DNA copy number"),
                    opt("only retention times"),
                ),
                "LFQ runs samples separately and compares intensity or spectral counts.",
            ),
            q(
                "SILAC achieves quantification by:",
                (
                    opt(
                        "metabolically incorporating heavy isotopes so peptides appear as light/heavy doublets",
                        correct=True,
                    ),
                    opt("adding isobaric reporter tags"),
                    opt("reversing the protein database"),
                    opt("changing the chromatography column"),
                ),
                "Heavy labels (e.g. 13C6-Lys) create MS1 doublets whose ratio gives abundance.",
            ),
            q(
                "TMT/iTRAQ tags are isobaric, meaning they:",
                (
                    opt(
                        "have identical mass at MS1 but release distinct reporter ions on fragmentation",
                        correct=True,
                    ),
                    opt("differ in MS1 mass by 6 Da"),
                    opt("cannot be fragmented"),
                    opt("change the peptide sequence"),
                ),
                "Isobaric tags co-elute at MS1; reporter ions quantify each channel after fragmentation.",
            ),
        ),
    },
    final=(
        q(
            "ETD/ECD fragmentation is especially useful because it:",
            (
                opt("preserves labile PTMs and gives c/z ions", correct=True),
                opt("destroys all PTMs"),
                opt("only works on DNA"),
                opt("measures retention time"),
            ),
            "Electron-based dissociation keeps labile modifications and complements CID.",
        ),
        q(
            "A precursor tolerance of 10 ppm on a high-resolution instrument is:",
            (
                opt("a tight mass window that reduces false candidate peptides", correct=True),
                opt("a very loose tolerance"),
                opt("a measure of retention time"),
                opt("the FDR threshold"),
            ),
            "Tight precursor tolerance shrinks the candidate list and false matches.",
        ),
        q(
            "Target-decoy estimates FDR(t) approximately as:",
            (
                opt("N_decoy(t) / N_target(t)", correct=True),
                opt("N_target(t) / N_decoy(t)"),
                opt("N_decoy(t) * N_target(t)"),
                opt("1 - N_target(t)"),
            ),
            "Decoy hits above threshold approximate the false target hits.",
        ),
        q(
            "Compared with DDA, DIA primarily improves:",
            (
                opt("reproducibility and reduced missing values", correct=True),
                opt("spectral simplicity"),
                opt("the need for a mass analyzer"),
                opt("sample weight"),
            ),
            "DIA samples comprehensively and reproducibly, at the cost of harder deconvolution.",
        ),
        q(
            "Ratio compression in TMT is caused by:",
            (
                opt("co-isolation of interfering precursors with the target", correct=True),
                opt("too few samples"),
                opt("reversed databases"),
                opt("low chromatographic resolution alone"),
            ),
            "Interfering ions co-isolated in the window dampen measured reporter ratios.",
        ),
        q(
            "The posterior error probability (PEP) describes:",
            (
                opt("the probability that one specific match is wrong", correct=True),
                opt("the global fraction of false hits"),
                opt("the precursor charge state"),
                opt("the gradient length"),
            ),
            "PEP is a per-hit measure, complementing the global FDR.",
        ),
    ),
)
