"""Quiz questions for the Protein Science & Enzymology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Amino acids: the building blocks": (
            q(
                "What distinguishes one standard amino acid from another?",
                (
                    opt("The side chain (R group)", correct=True),
                    opt("The alpha-carbon"),
                    opt("The amino group"),
                    opt("The carboxyl group"),
                ),
                "All twenty share the same backbone; only the variable side chain differs.",
            ),
            q(
                "Which amino acid can form a disulfide bond?",
                (
                    opt("Cysteine", correct=True),
                    opt("Glycine"),
                    opt("Alanine"),
                    opt("Leucine"),
                ),
                "Two cysteine thiol groups oxidise to form a covalent disulfide bond.",
            ),
            q(
                "Aspartate and glutamate are classified as:",
                (
                    opt("acidic side chains", correct=True),
                    opt("basic side chains"),
                    opt("nonpolar side chains"),
                    opt("polar uncharged side chains"),
                ),
                "Asp and Glu carry carboxylate side chains, making them acidic.",
            ),
        ),
        "The peptide bond and primary structure": (
            q(
                "How is a peptide bond formed?",
                (
                    opt("By condensation, releasing a water molecule", correct=True),
                    opt("By hydrolysis, consuming water"),
                    opt("By forming a disulfide between cysteines"),
                    opt("By a hydrogen bond between backbones"),
                ),
                "The carboxyl of one residue and amino of the next condense, releasing water.",
            ),
            q(
                "Why is the peptide bond planar?",
                (
                    opt("It has partial double-bond character from resonance", correct=True),
                    opt("It is a full triple bond"),
                    opt("It is ionic"),
                    opt("Steric bulk forces it flat"),
                ),
                "Resonance gives the C-N amide bond partial double-bond character, restricting rotation.",
            ),
            q(
                "Primary structure refers to:",
                (
                    opt("the ordered sequence of amino acid residues", correct=True),
                    opt("the three-dimensional fold"),
                    opt("the arrangement of subunits"),
                    opt("local helices and sheets"),
                ),
                "Primary structure is the residue sequence read N- to C-terminus.",
            ),
        ),
        "Secondary structure: helices and sheets": (
            q(
                "In an alpha-helix, each carbonyl oxygen hydrogen-bonds to the amide N-H:",
                (
                    opt("four residues ahead (i to i+4)", correct=True),
                    opt("on the adjacent strand"),
                    opt("one residue ahead (i to i+1)"),
                    opt("of a different chain only"),
                ),
                "The alpha-helix is defined by i to i+4 backbone hydrogen bonds.",
            ),
            q(
                "Beta-sheets are stabilised by:",
                (
                    opt("hydrogen bonds between adjacent strands", correct=True),
                    opt("disulfide bonds only"),
                    opt("ionic bonds between side chains"),
                    opt("covalent peptide bonds across strands"),
                ),
                "Extended strands hydrogen-bond to neighbours, parallel or antiparallel.",
            ),
            q(
                "Which residue most strongly disrupts an alpha-helix?",
                (
                    opt("Proline", correct=True),
                    opt("Alanine"),
                    opt("Leucine"),
                    opt("Glutamate"),
                ),
                "Proline's ring kinks the backbone and lacks an amide H, breaking helices.",
            ),
        ),
        "Tertiary and quaternary structure": (
            q(
                "The dominant driving force for tertiary folding is:",
                (
                    opt("the hydrophobic effect burying nonpolar residues", correct=True),
                    opt("covalent peptide bonds"),
                    opt("the planarity of the peptide bond"),
                    opt("repulsion between charged residues"),
                ),
                "Nonpolar side chains bury into a water-excluded core, driving the fold.",
            ),
            q(
                "Quaternary structure describes:",
                (
                    opt("the assembly of multiple polypeptide subunits", correct=True),
                    opt("the sequence of one chain"),
                    opt("a single alpha-helix"),
                    opt("the fold of one chain"),
                ),
                "Quaternary structure is how separate subunits associate, as in haemoglobin.",
            ),
            q(
                "A recurring tertiary arrangement like a TIM barrel is called a:",
                (
                    opt("fold", correct=True),
                    opt("primary motif"),
                    opt("subunit"),
                    opt("disulfide"),
                ),
                "Common 3D arrangements such as TIM barrels and Rossmann folds are named folds.",
            ),
        ),
        "From structure to function": (
            q(
                "A smaller dissociation constant (Kd) means:",
                (
                    opt("tighter binding", correct=True),
                    opt("weaker binding"),
                    opt("no binding"),
                    opt("covalent bonding"),
                ),
                "Kd = [E][L]/[EL]; a smaller value means the complex is favoured (tighter binding).",
            ),
            q(
                "At what free ligand concentration is a protein half-saturated?",
                (
                    opt("[L] equal to Kd", correct=True),
                    opt("[L] equal to zero"),
                    opt("[L] much greater than Kd"),
                    opt("[L] equal to twice Kd"),
                ),
                "Fractional saturation reaches 0.5 when free ligand equals Kd.",
            ),
            q(
                "The structure-function principle states that:",
                (
                    opt(
                        "a protein's three-dimensional shape determines its function", correct=True
                    ),
                    opt("function is independent of shape"),
                    opt("only primary sequence matters for function"),
                    opt("all proteins share one function"),
                ),
                "The precise fold positions atoms to bind partners and do work.",
            ),
        ),
    },
    final=(
        q(
            "How many standard amino acids are encoded in proteins?",
            (
                opt("20", correct=True),
                opt("4"),
                opt("64"),
                opt("8"),
            ),
            "There are twenty standard amino acids differing in their side chains.",
        ),
        q(
            "Which two backbone dihedral angles define a residue's conformation?",
            (
                opt("phi and psi", correct=True),
                opt("alpha and beta"),
                opt("Km and Vmax"),
                opt("pH and pKa"),
            ),
            "Rotation is confined to phi and psi; the Ramachandran plot maps allowed pairs.",
        ),
        q(
            "Which is a secondary structure element?",
            (
                opt("Alpha-helix", correct=True),
                opt("Disulfide bond"),
                opt("Subunit interface"),
                opt("Active site"),
            ),
            "Alpha-helices and beta-sheets are the main secondary structures.",
        ),
        q(
            "The hydrophobic core of a folded protein is enriched in:",
            (
                opt("nonpolar side chains", correct=True),
                opt("charged side chains"),
                opt("phosphate groups"),
                opt("water molecules"),
            ),
            "Nonpolar residues bury inward, away from water.",
        ),
        q(
            "Haemoglobin's tetramer is an example of:",
            (
                opt("quaternary structure", correct=True),
                opt("primary structure"),
                opt("secondary structure"),
                opt("a single domain"),
            ),
            "Four subunits assembling is quaternary structure.",
        ),
        q(
            "Ligand binding to a specific site is described by which equilibrium constant?",
            (
                opt("Dissociation constant Kd", correct=True),
                opt("Boltzmann constant"),
                opt("Avogadro's number"),
                opt("Gas constant R"),
            ),
            "Binding affinity is characterised by the dissociation constant Kd.",
        ),
    ),
)
