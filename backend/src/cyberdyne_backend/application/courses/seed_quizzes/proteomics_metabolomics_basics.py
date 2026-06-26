"""Quiz questions for the Proteomics & Metabolomics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Proteomes, metabolomes & the central dogma": (
            q(
                "What is the proteome?",
                (
                    opt("the full set of proteins expressed by a cell or organism", correct=True),
                    opt("the complete DNA sequence of an organism"),
                    opt("the set of all mRNA molecules"),
                    opt("the set of all lipids only"),
                ),
                "The proteome is the complete set of expressed proteins; it is dynamic.",
            ),
            q(
                "Why measure proteins directly rather than infer them from mRNA?",
                (
                    opt(
                        "mRNA abundance correlates only weakly with protein abundance", correct=True
                    ),
                    opt("mRNA cannot be measured at all"),
                    opt("proteins are always identical to their mRNA levels"),
                    opt("mRNA and protein levels are always equal"),
                ),
                "Translation rate, protein half-life and modification weaken the mRNA-protein correlation.",
            ),
            q(
                "Which layer sits closest to the phenotype?",
                (
                    opt("the metabolome", correct=True),
                    opt("the genome"),
                    opt("the transcriptome"),
                    opt("the exome"),
                ),
                "Metabolites are the downstream readout of enzyme activity, nearest to phenotype.",
            ),
        ),
        "What a mass spectrometer measures: m/z": (
            q(
                "What quantity does a mass spectrometer actually measure?",
                (
                    opt("the mass-to-charge ratio (m/z) of gas-phase ions", correct=True),
                    opt("the weight of neutral molecules"),
                    opt("the optical absorbance of the sample"),
                    opt("the pH of the solution"),
                ),
                "MS measures m/z of ions, not the mass of neutral molecules directly.",
            ),
            q(
                "What are the three stages of every mass spectrometer?",
                (
                    opt("ion source, mass analyzer, detector", correct=True),
                    opt("pump, column, lamp"),
                    opt("anode, cathode, membrane"),
                    opt("laser, prism, screen"),
                ),
                "Ionize, separate by m/z, then detect.",
            ),
            q(
                "Resolution R = m/dm describes:",
                (
                    opt("how well two close m/z peaks are separated", correct=True),
                    opt("how fast the chromatography runs"),
                    opt("the sample concentration"),
                    opt("the laser wavelength"),
                ),
                "Higher resolving power separates closer peaks and resolves isotopes.",
            ),
        ),
        "Bottom-up proteomics & tryptic digestion": (
            q(
                "In bottom-up proteomics, proteins are first:",
                (
                    opt("digested into peptides", correct=True),
                    opt("kept fully intact"),
                    opt("converted to DNA"),
                    opt("crystallized"),
                ),
                "Bottom-up digests proteins into peptides, identifies peptides, then infers proteins.",
            ),
            q(
                "Where does trypsin cleave?",
                (
                    opt(
                        "C-terminal to lysine (K) and arginine (R), not before proline",
                        correct=True,
                    ),
                    opt("N-terminal to glycine only"),
                    opt("at every peptide bond"),
                    opt("only at cysteine residues"),
                ),
                "Trypsin cuts after K and R (except when followed by P), giving well-behaved peptides.",
            ),
            q(
                "Why are cysteines reduced and alkylated before digestion?",
                (
                    opt("to break disulfide bonds and prevent them re-forming", correct=True),
                    opt("to add a positive charge for ionization"),
                    opt("to cleave the backbone"),
                    opt("to remove all peptides"),
                ),
                "Reduction (DTT) breaks disulfides; alkylation (iodoacetamide) blocks re-bridging.",
            ),
        ),
        "Soft ionization: ESI and MALDI": (
            q(
                "Which ionization method produces multiply-charged ions and pairs with LC?",
                (
                    opt("electrospray ionization (ESI)", correct=True),
                    opt("MALDI"),
                    opt("electron impact (EI)"),
                    opt("flame ionization"),
                ),
                "ESI yields multiply-charged ions from a liquid stream, ideal for LC coupling.",
            ),
            q(
                "MALDI typically produces:",
                (
                    opt("mostly singly-charged ions from a matrix crystal", correct=True),
                    opt("only neutral molecules"),
                    opt("highly multiply-charged ions"),
                    opt("no ions at all"),
                ),
                "A UV laser desorbs analyte from a matrix, giving predominantly singly-charged ions.",
            ),
            q(
                "Why is ESI/MALDI called 'soft' ionization?",
                (
                    opt("it transfers large molecules into the gas phase intact", correct=True),
                    opt("it uses very low temperatures only"),
                    opt("it always fragments molecules completely"),
                    opt("it requires no energy"),
                ),
                "Soft ionization preserves the intact molecule rather than shattering it.",
            ),
        ),
        "Separation first: LC-MS and the chromatogram": (
            q(
                "Why separate peptides by LC before the mass spectrometer?",
                (
                    opt("to reduce ion suppression and spectral overlap", correct=True),
                    opt("to increase the sample volume"),
                    opt("to remove all peptides"),
                    opt("to change their charge to zero"),
                ),
                "Spreading peptides in time lets the MS see a manageable subset at each moment.",
            ),
            q(
                "In reversed-phase C18 LC, peptides elute as the mobile phase becomes:",
                (
                    opt("more organic (e.g. increasing acetonitrile)", correct=True),
                    opt("more aqueous"),
                    opt("more acidic only"),
                    opt("colder"),
                ),
                "Hydrophobic peptides release from C18 as organic solvent rises along the gradient.",
            ),
            q(
                "LC-MS data are three-dimensional in:",
                (
                    opt("retention time, m/z, and intensity", correct=True),
                    opt("pH, temperature, and time"),
                    opt("voltage, current, and resistance"),
                    opt("mass, charge, and pH"),
                ),
                "Each point has a retention time, an m/z and an intensity.",
            ),
        ),
    },
    final=(
        q(
            "The metabolome consists of:",
            (
                opt(
                    "small-molecule metabolites such as sugars, lipids and amino acids",
                    correct=True,
                ),
                opt("only proteins"),
                opt("only DNA"),
                opt("only mRNA"),
            ),
            "The metabolome is the full set of small molecules in a system.",
        ),
        q(
            "A +10 charged 10,000 Da protein appears near which m/z?",
            (
                opt("about 1001", correct=True),
                opt("about 100"),
                opt("about 10,000"),
                opt("about 100,000"),
            ),
            "m/z = (M + z*mH)/z = (10000 + 10)/10 ~ 1001.",
        ),
        q(
            "Which protease is standard in bottom-up proteomics?",
            (
                opt("trypsin", correct=True),
                opt("DNA polymerase"),
                opt("lysozyme"),
                opt("reverse transcriptase"),
            ),
            "Trypsin cleaves after K/R, giving peptides that ionize and fragment well.",
        ),
        q(
            "Which technique is best suited to coupling with online liquid chromatography?",
            (
                opt("ESI", correct=True),
                opt("MALDI"),
                opt("electron impact"),
                opt("X-ray diffraction"),
            ),
            "ESI ionizes directly from the LC liquid stream.",
        ),
        q(
            "What does increasing chromatographic resolution achieve for the MS?",
            (
                opt("fewer peptides compete for ionization at any instant", correct=True),
                opt("higher sample salt content"),
                opt("complete loss of signal"),
                opt("conversion of peptides to DNA"),
            ),
            "Better separation reduces co-elution and ion suppression, improving coverage.",
        ),
        q(
            "Roughly how many orders of magnitude span human protein abundances?",
            (
                opt("about seven", correct=True),
                opt("about one"),
                opt("about two"),
                opt("about twenty"),
            ),
            "The dynamic range of the proteome spans about seven orders of magnitude.",
        ),
    ),
)
