"""Quiz questions for the Proteomics & Metabolomics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Post-translational modifications & phosphoproteomics": (
            q(
                "Phosphorylation adds approximately what mass to a residue?",
                (
                    opt("+79.966 Da (HPO3)", correct=True),
                    opt("+42.011 Da"),
                    opt("-18 Da"),
                    opt("+6 Da"),
                ),
                "Phospho adds HPO3, ~79.966 Da; acetyl adds ~42.011 Da.",
            ),
            q(
                "Why is enrichment (e.g. IMAC or TiO2) used before phosphoproteomics?",
                (
                    opt("modified peptides are rare and would otherwise be swamped", correct=True),
                    opt("to remove all peptides"),
                    opt("to reverse the database"),
                    opt("to lower the resolution"),
                ),
                "Phosphopeptides are low abundance; IMAC/TiO2 selectively enrich them.",
            ),
            q(
                "Site localization tools rely on:",
                (
                    opt(
                        "site-determining fragment ions that distinguish modification isoforms",
                        correct=True,
                    ),
                    opt("the precursor charge alone"),
                    opt("retention time only"),
                    opt("the decoy database"),
                ),
                "Ascore/PTM-Score weigh fragment ions that pinpoint which residue carries the mod.",
            ),
        ),
        "Untargeted metabolomics & the annotation problem": (
            q(
                "Untargeted metabolomics aims to:",
                (
                    opt("profile everything and discover unexpected metabolites", correct=True),
                    opt("quantify only a fixed known panel"),
                    opt("measure only proteins"),
                    opt("sequence DNA"),
                ),
                "Untargeted profiling captures broad coverage rather than a predefined panel.",
            ),
            q(
                "Why is annotating an unknown metabolite harder than identifying a peptide?",
                (
                    opt(
                        "metabolites have no simple polymer alphabet, and isomers share formulas",
                        correct=True,
                    ),
                    opt("metabolites have no mass"),
                    opt("metabolites cannot be ionized"),
                    opt("peptides are never identifiable"),
                ),
                "Without a residue alphabet, formula and structure are ambiguous among isomers.",
            ),
            q(
                "The Schymanski confidence levels rank annotations where level 1 means:",
                (
                    opt("confirmed structure with a reference standard", correct=True),
                    opt("exact mass only"),
                    opt("a guessed name"),
                    opt("an unannotated feature"),
                ),
                "Level 1 is the highest confidence, validated by a reference standard.",
            ),
        ),
        "Deep learning for spectra & retention time": (
            q(
                "Models like Prosit predict, from a peptide sequence and charge:",
                (
                    opt("fragment ion intensities and retention time", correct=True),
                    opt("the DNA sequence"),
                    opt("the sample pH"),
                    opt("the chromatography column type"),
                ),
                "Deep models predict MS2 intensity patterns and retention time accurately.",
            ),
            q(
                "Predicted spectral libraries are especially useful for:",
                (
                    opt("library-free DIA analysis", correct=True),
                    opt("eliminating the mass analyzer"),
                    opt("removing all peptides"),
                    opt("DNA sequencing"),
                ),
                "In-silico libraries (e.g. DIA-NN) remove the need for experimental libraries.",
            ),
            q(
                "Rescoring with the spectral angle between observed and predicted intensities:",
                (
                    opt("recovers more true PSMs above the 1% FDR threshold", correct=True),
                    opt("lowers the resolution"),
                    opt("randomizes identifications"),
                    opt("removes the decoy database"),
                ),
                "The spectral-angle feature separates true from false matches, boosting IDs.",
            ),
        ),
        "Single-cell proteomics": (
            q(
                "Roughly how much protein is in a single mammalian cell?",
                (
                    opt("about 250 picograms", correct=True),
                    opt("about 1 gram"),
                    opt("about 1 milligram"),
                    opt("about 1 kilogram"),
                ),
                "A single cell holds ~250 pg of protein, a million-fold less than bulk samples.",
            ),
            q(
                "In SCoPE-MS, the carrier/booster channel serves to:",
                (
                    opt(
                        "drive ion statistics while reporter ions quantify single cells",
                        correct=True,
                    ),
                    opt("remove all single cells"),
                    opt("act as the decoy database"),
                    opt("replace the chromatography"),
                ),
                "A high-abundance carrier improves ion counts; reporters quantify each single cell.",
            ),
            q(
                "Counting (Poisson) noise means signal-to-noise scales approximately as:",
                (
                    opt("the square root of the number of ions sampled", correct=True),
                    opt("the square of the number of ions"),
                    opt("the inverse of the number of ions"),
                    opt("independently of ion count"),
                ),
                "S/N grows as sqrt(N), the fundamental limit of counting ions.",
            ),
        ),
        "Multi-omics integration": (
            q(
                "What is the goal of multi-omics integration?",
                (
                    opt("combine layers to model a system across the central dogma", correct=True),
                    opt("measure only the genome"),
                    opt("discard proteomics data"),
                    opt("avoid statistics entirely"),
                ),
                "Integration jointly models genome, transcriptome, proteome and metabolome.",
            ),
            q(
                "MOFA and DIABLO are examples of:",
                (
                    opt(
                        "intermediate integration methods that learn a shared latent space",
                        correct=True,
                    ),
                    opt("DNA sequencing chemistries"),
                    opt("ionization sources"),
                    opt("chromatography columns"),
                ),
                "Both find joint latent factors explaining variance across omics layers.",
            ),
            q(
                "A central challenge in multi-omics is:",
                (
                    opt("the curse of dimensionality: many features, few samples", correct=True),
                    opt("having too many samples and no features"),
                    opt("the absence of any data"),
                    opt("identical noise in all layers"),
                ),
                "Thousands of features with scarce samples demand regularization and reduction.",
            ),
        ),
    },
    final=(
        q(
            "Acetylation adds approximately what mass shift?",
            (
                opt("+42.011 Da", correct=True),
                opt("+79.966 Da"),
                opt("-18 Da"),
                opt("+128 Da"),
            ),
            "Acetyl adds ~42.011 Da; phospho adds ~79.966 Da.",
        ),
        q(
            "A 'feature' in untargeted metabolomics is:",
            (
                opt("a unique m/z-retention-time pair", correct=True),
                opt("a confirmed protein"),
                opt("a DNA variant"),
                opt("a reporter ion only"),
            ),
            "Features are detected m/z-RT pairs; many remain unannotated (the dark metabolome).",
        ),
        q(
            "De novo sequencing models such as Casanovo:",
            (
                opt("read spectra directly into sequence without a database", correct=True),
                opt("require a complete protein FASTA"),
                opt("only predict retention time"),
                opt("sequence genomic DNA"),
            ),
            "Transformer de novo tools are useful when no database exists.",
        ),
        q(
            "nanoPOTS-style miniaturized prep helps single-cell proteomics by:",
            (
                opt("reducing sample losses on surfaces in nanoliter volumes", correct=True),
                opt("increasing the sample to bulk levels"),
                opt("replacing the mass analyzer"),
                opt("removing the need for digestion"),
            ),
            "Working in nanoliter volumes minimizes adsorptive losses of scarce protein.",
        ),
        q(
            "In a scree of latent factors, most shared signal typically sits in:",
            (
                opt("a few top factors, with variance explained decaying quickly", correct=True),
                opt("every factor equally"),
                opt("the last factor only"),
                opt("no factors at all"),
            ),
            "Variance explained falls off fast, so a few factors capture the joint signal.",
        ),
        q(
            "Pathway/network methods (KEGG, Reactome) aid integration by:",
            (
                opt(
                    "mapping features onto known biology to interpret the joint signal",
                    correct=True,
                ),
                opt("removing all biological context"),
                opt("randomizing the data"),
                opt("converting proteins to DNA"),
            ),
            "Mapping onto curated pathways turns statistical factors into mechanism.",
        ),
    ),
)
