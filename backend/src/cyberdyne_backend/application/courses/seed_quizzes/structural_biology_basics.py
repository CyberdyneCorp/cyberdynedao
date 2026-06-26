"""Quiz questions for the Structural Biology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Amino acids and the peptide bond": (
            q(
                "What distinguishes the 20 standard amino acids from one another?",
                (
                    opt("Their side chains (R groups)", correct=True),
                    opt("Their backbone amino group"),
                    opt("Their backbone carboxyl group"),
                    opt("Their alpha-carbon hydrogen"),
                ),
                "All share the same backbone; only the side chain differs.",
            ),
            q(
                "The peptide bond is usually planar because:",
                (
                    opt("the amide C-N bond has partial double-bond character", correct=True),
                    opt("it is a true carbon-carbon double bond"),
                    opt("the side chains lock it in place"),
                    opt("it contains a disulfide linkage"),
                ),
                "Resonance gives the amide bond partial double-bond character, restricting rotation.",
            ),
            q(
                "Which torsion angles set a residue's backbone conformation?",
                (
                    opt("phi and psi", correct=True),
                    opt("alpha and beta"),
                    opt("the peptide-bond omega angle only"),
                    opt("the chi side-chain angles only"),
                ),
                "Because the peptide unit is planar, conformation is captured by phi and psi.",
            ),
        ),
        "Secondary structure: helices and sheets": (
            q(
                "Secondary structure is stabilised mainly by:",
                (
                    opt("backbone hydrogen bonds (C=O to N-H)", correct=True),
                    opt("disulfide bonds"),
                    opt("side-chain salt bridges"),
                    opt("covalent peptide bonds"),
                ),
                "Helices and sheets form via backbone C=O to N-H hydrogen bonds.",
            ),
            q(
                "In a right-handed alpha-helix, each C=O hydrogen-bonds to the N-H of the residue:",
                (
                    opt("four residues ahead (i to i+4)", correct=True),
                    opt("in the adjacent strand"),
                    opt("one residue ahead (i to i+1)"),
                    opt("at the opposite terminus"),
                ),
                "The alpha-helix uses an i to i+4 hydrogen-bond pattern, 3.6 residues per turn.",
            ),
            q(
                "Which beta-sheet arrangement gives straighter, stronger hydrogen bonds?",
                (
                    opt("Antiparallel", correct=True),
                    opt("Parallel"),
                    opt("Left-handed"),
                    opt("Coiled-coil"),
                ),
                "Antiparallel strands form straighter, stronger hydrogen bonds than parallel ones.",
            ),
        ),
        "The Ramachandran plot": (
            q(
                "The Ramachandran plot maps which two variables?",
                (
                    opt("phi versus psi", correct=True),
                    opt("temperature versus stability"),
                    opt("resolution versus R-factor"),
                    opt("ligand concentration versus saturation"),
                ),
                "It plots the two backbone torsion angles, phi and psi.",
            ),
            q(
                "Which residue can occupy normally disallowed regions because it lacks a side chain?",
                (
                    opt("Glycine", correct=True),
                    opt("Tryptophan"),
                    opt("Phenylalanine"),
                    opt("Arginine"),
                ),
                "Glycine has only a hydrogen side chain, so it tolerates conformations others cannot.",
            ),
            q(
                "Most (phi, psi) combinations are forbidden because of:",
                (
                    opt("steric clashes between atoms", correct=True),
                    opt("lack of hydrogen bonding"),
                    opt("the loss of disulfide bonds"),
                    opt("electrostatic repulsion of phosphates"),
                ),
                "Disallowed regions correspond to conformations that cause atomic overlap.",
            ),
        ),
        "Tertiary and quaternary structure": (
            q(
                "Tertiary structure refers to:",
                (
                    opt("the full 3D fold of a single polypeptide chain", correct=True),
                    opt("the local helices and sheets only"),
                    opt("the assembly of multiple subunits"),
                    opt("the linear amino-acid sequence"),
                ),
                "Tertiary structure is the complete 3D fold of one chain.",
            ),
            q(
                "Which covalent bond can staple distant parts of a folded chain together?",
                (
                    opt("Disulfide bond between cysteines", correct=True),
                    opt("Hydrogen bond"),
                    opt("Van der Waals contact"),
                    opt("Salt bridge"),
                ),
                "Disulfide bonds are covalent cross-links formed between two cysteine side chains.",
            ),
            q(
                "Quaternary structure describes:",
                (
                    opt("the assembly of multiple folded subunits into a complex", correct=True),
                    opt("the hydrophobic core of one domain"),
                    opt("a single alpha-helix"),
                    opt("the sugar-phosphate backbone"),
                ),
                "Quaternary structure is how separate subunits associate, as in haemoglobin.",
            ),
        ),
        "Nucleic-acid structure and the double helix": (
            q(
                "In DNA, adenine pairs with which base?",
                (
                    opt("Thymine", correct=True),
                    opt("Guanine"),
                    opt("Cytosine"),
                    opt("Uracil"),
                ),
                "A pairs with T (two hydrogen bonds); G pairs with C.",
            ),
            q(
                "A G-C base pair is held by how many hydrogen bonds?",
                (
                    opt("Three", correct=True),
                    opt("Two"),
                    opt("One"),
                    opt("Four"),
                ),
                "G-C pairs have three hydrogen bonds; A-T pairs have two.",
            ),
            q(
                "The two strands of the DNA double helix are:",
                (
                    opt("antiparallel", correct=True),
                    opt("parallel"),
                    opt("identical in sequence"),
                    opt("joined by covalent bonds between bases"),
                ),
                "The strands run antiparallel (one 5'->3', the other 3'->5').",
            ),
        ),
        "Forces that fold and stabilise molecules": (
            q(
                "The dominant driving force of protein folding is:",
                (
                    opt("the hydrophobic effect", correct=True),
                    opt("covalent peptide-bond formation"),
                    opt("magnetic attraction"),
                    opt("gravitational settling"),
                ),
                "Burying nonpolar side chains away from water (the hydrophobic effect) drives folding.",
            ),
            q(
                "Typical net stability of a small folded protein is about:",
                (
                    opt("20-60 kJ/mol (marginally stable)", correct=True),
                    opt("several thousand kJ/mol"),
                    opt("exactly zero"),
                    opt("negative infinity"),
                ),
                "Proteins are only marginally stable, by roughly 20-60 kJ/mol.",
            ),
            q(
                "Which is NOT a noncovalent force stabilising a fold?",
                (
                    opt("Peptide bond", correct=True),
                    opt("Hydrogen bond"),
                    opt("Van der Waals contact"),
                    opt("Salt bridge"),
                ),
                "The peptide bond is covalent; folding stability comes from weak noncovalent forces.",
            ),
        ),
    },
    final=(
        q(
            "Which group makes amino acids chemically distinct from each other?",
            (
                opt("The side chain", correct=True),
                opt("The amino group"),
                opt("The carboxyl group"),
                opt("The alpha-carbon"),
            ),
            "Only the side chain varies among the 20 standard amino acids.",
        ),
        q(
            "An alpha-helix has roughly how many residues per turn?",
            (
                opt("3.6", correct=True),
                opt("2.0"),
                opt("10.5"),
                opt("7.2"),
            ),
            "The alpha-helix has about 3.6 residues per turn.",
        ),
        q(
            "The Ramachandran plot is primarily used to:",
            (
                opt("check whether backbone conformations are sterically allowed", correct=True),
                opt("measure X-ray wavelength"),
                opt("count subunits in a complex"),
                opt("determine GC content"),
            ),
            "It shows allowed phi/psi combinations and flags improbable conformations.",
        ),
        q(
            "Hemoglobin's four-subunit assembly is an example of:",
            (
                opt("quaternary structure", correct=True),
                opt("secondary structure"),
                opt("primary structure"),
                opt("a disulfide bond"),
            ),
            "Multiple subunits assembling into one complex is quaternary structure.",
        ),
        q(
            "Which base pair is more stable per pair in DNA?",
            (
                opt("G-C (three hydrogen bonds)", correct=True),
                opt("A-T (two hydrogen bonds)"),
                opt("A-G"),
                opt("C-T"),
            ),
            "G-C pairs have three hydrogen bonds, so higher GC content raises melting temperature.",
        ),
        q(
            "Why are proteins described as marginally stable?",
            (
                opt("stabilising and destabilising contributions nearly cancel", correct=True),
                opt("they are held together by one strong covalent bond"),
                opt("they never unfold under any condition"),
                opt("they have no hydrophobic core"),
            ),
            "Net stability is a small difference between large opposing terms, around 20-60 kJ/mol.",
        ),
    ),
)
