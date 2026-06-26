"""Quiz questions for the Biochemistry - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Water: the matrix of life": (
            q(
                "Why is water such an effective solvent for ions and polar molecules?",
                (
                    opt("It is a polar molecule that forms hydrogen bonds", correct=True),
                    opt("It is a nonpolar molecule with no net dipole"),
                    opt("It carries a permanent full negative charge"),
                    opt("It is chemically inert and never reacts"),
                ),
                "Water's polarity and hydrogen bonding let it surround and dissolve charged and polar solutes.",
            ),
            q(
                "The hydrophobic effect is best described as:",
                (
                    opt("nonpolar groups clustering so water minimises its ordering", correct=True),
                    opt("covalent bonds forming between water and oils"),
                    opt("ionic attraction between nonpolar molecules"),
                    opt("hydrogen bonds between nonpolar tails"),
                ),
                "Water orders around nonpolar groups; clustering them reduces that ordering, an entropy-driven force.",
            ),
            q(
                "Which property of water comes directly from its hydrogen-bond network?",
                (
                    opt("Low boiling point"),
                    opt("High heat capacity", correct=True),
                    opt("Inability to dissolve salts"),
                    opt("Lack of any dipole moment"),
                ),
                "Extensive hydrogen bonding gives water a high heat capacity and high boiling point.",
            ),
        ),
        "pH, pKa and buffers": (
            q(
                "The pH of a solution is defined as:",
                (
                    opt("-log10[H+]", correct=True),
                    opt("log10[H+]"),
                    opt("[H+] x [OH-]"),
                    opt("-log10[OH-]"),
                ),
                "pH is the negative base-10 logarithm of the hydrogen-ion concentration.",
            ),
            q(
                "A buffer resists pH change most effectively when the pH is:",
                (
                    opt("near the pKa of the buffering acid", correct=True),
                    opt("far above the pKa"),
                    opt("far below the pKa"),
                    opt("exactly 7 regardless of pKa"),
                ),
                "Buffering is strongest within about one pH unit of the pKa, where the titration curve is flattest.",
            ),
            q(
                "At a pH equal to the pKa of a weak acid HA, the ratio [A-]/[HA] is:",
                (
                    opt("1 (equal amounts)", correct=True),
                    opt("10"),
                    opt("0"),
                    opt("100"),
                ),
                "Henderson-Hasselbalch: pH = pKa when log([A-]/[HA]) = 0, i.e. the ratio equals 1.",
            ),
        ),
        "Carbohydrates and glycosidic bonds": (
            q(
                "Starch and cellulose are both glucose polymers but differ because:",
                (
                    opt(
                        "starch uses alpha(1->4) links and cellulose uses beta(1->4)", correct=True
                    ),
                    opt("starch is made of fructose and cellulose of glucose"),
                    opt("cellulose has ester bonds and starch has amide bonds"),
                    opt("they are built from different elements"),
                ),
                "Linkage geometry differs: digestible alpha(1->4) in starch versus structural beta(1->4) in cellulose.",
            ),
            q(
                "A glycosidic bond forms by:",
                (
                    opt("a condensation reaction that releases water", correct=True),
                    opt("hydrolysis that consumes water"),
                    opt("oxidation of the anomeric carbon"),
                    opt("formation of a phosphate ester"),
                ),
                "Two sugars join by condensation, releasing a molecule of water.",
            ),
            q(
                "Storing glucose as a large polysaccharide rather than free glucose helps the cell by:",
                (
                    opt("avoiding a large increase in osmotic pressure", correct=True),
                    opt("increasing the number of solute particles"),
                    opt("making the glucose impossible to recover"),
                    opt("raising the freezing point of the cytosol"),
                ),
                "One polymer counts as a single osmotic particle, so storage avoids osmotic stress.",
            ),
        ),
        "Lipids and membranes": (
            q(
                "Phospholipids form bilayers in water because they are:",
                (
                    opt("amphipathic, with a polar head and nonpolar tails", correct=True),
                    opt("entirely hydrophobic"),
                    opt("entirely hydrophilic"),
                    opt("positively charged on both ends"),
                ),
                "Their dual nature drives self-assembly into a bilayer via the hydrophobic effect.",
            ),
            q(
                "A cis double bond in a fatty-acid tail tends to:",
                (
                    opt("kink the chain and lower the melting point", correct=True),
                    opt("straighten the chain and raise the melting point"),
                    opt("make the lipid water-soluble"),
                    opt("add a phosphate group"),
                ),
                "Unsaturation kinks the chain, loosens packing, and lowers the melting point (oils vs fats).",
            ),
            q(
                "The fluid-mosaic model describes a membrane as:",
                (
                    opt(
                        "a two-dimensional fluid in which lipids and proteins diffuse", correct=True
                    ),
                    opt("a rigid crystalline sheet"),
                    opt("a solid wall impermeable to everything"),
                    opt("a single layer of fatty acids"),
                ),
                "The bilayer behaves as a 2D fluid with laterally diffusing components.",
            ),
        ),
        "Nucleic acids and the central dogma": (
            q(
                "In DNA, the base pairing rule is:",
                (
                    opt("A pairs with T, and G pairs with C", correct=True),
                    opt("A pairs with G, and C pairs with T"),
                    opt("A pairs with C, and G pairs with T"),
                    opt("every base pairs with uracil"),
                ),
                "A-T (two H-bonds) and G-C (three H-bonds) are the complementary pairs.",
            ),
            q(
                "The central dogma describes information flow as:",
                (
                    opt("DNA -> RNA -> protein", correct=True),
                    opt("protein -> RNA -> DNA"),
                    opt("RNA -> DNA -> protein"),
                    opt("protein -> DNA -> RNA"),
                ),
                "DNA is transcribed to mRNA, which is translated into protein.",
            ),
            q(
                "GC-rich DNA requires a higher temperature to melt because:",
                (
                    opt("G-C pairs have three hydrogen bonds versus two for A-T", correct=True),
                    opt("G-C pairs have fewer hydrogen bonds than A-T"),
                    opt("guanine is heavier than adenine"),
                    opt("GC regions contain no phosphate backbone"),
                ),
                "Three hydrogen bonds per G-C pair make GC-rich duplexes more stable.",
            ),
        ),
        "Amino acids and the peptide bond": (
            q(
                "How many amino acids are genetically encoded in proteins?",
                (
                    opt("20", correct=True),
                    opt("4"),
                    opt("64"),
                    opt("8"),
                ),
                "Twenty standard amino acids are specified by the genetic code.",
            ),
            q(
                "The peptide bond is:",
                (
                    opt("a planar, partially double-bonded amide", correct=True),
                    opt("a freely rotating single bond"),
                    opt("an ionic interaction"),
                    opt("a disulfide bridge"),
                ),
                "Resonance gives the peptide bond partial double-bond character and planarity.",
            ),
            q(
                "At physiological pH a free amino acid typically exists as a:",
                (
                    opt("zwitterion with -NH3+ and -COO-", correct=True),
                    opt("fully neutral molecule"),
                    opt("doubly positive cation"),
                    opt("doubly negative anion"),
                ),
                "The amino group is protonated and the carboxyl deprotonated, giving a zwitterion.",
            ),
        ),
    },
    final=(
        q(
            "Which force is the primary driver of protein folding and membrane assembly?",
            (
                opt("The hydrophobic effect", correct=True),
                opt("Covalent peptide bonds"),
                opt("Electrostatic repulsion"),
                opt("Gravity"),
            ),
            "Burying nonpolar groups away from water (the hydrophobic effect) drives both processes.",
        ),
        q(
            "Blood is held near pH 7.4 mainly by:",
            (
                opt("physiological buffer systems such as bicarbonate", correct=True),
                opt("the absence of any acids"),
                opt("constant addition of strong base"),
                opt("freezing of the plasma"),
            ),
            "Buffer pairs resist pH change to keep cellular pH in the range enzymes need.",
        ),
        q(
            "Which linkage makes cellulose indigestible to humans?",
            (
                opt("beta(1->4) glycosidic bonds", correct=True),
                opt("alpha(1->4) glycosidic bonds"),
                opt("phosphodiester bonds"),
                opt("peptide bonds"),
            ),
            "Humans lack enzymes to cleave the beta(1->4) links of cellulose.",
        ),
        q(
            "The monomers of nucleic acids are:",
            (
                opt("nucleotides (sugar + phosphate + base)", correct=True),
                opt("amino acids"),
                opt("fatty acids"),
                opt("monosaccharides"),
            ),
            "Nucleotides polymerise through phosphodiester bonds into DNA and RNA.",
        ),
        q(
            "Which pairing of biomolecule class and role is correct?",
            (
                opt("Proteins -> enzymes and structure", correct=True),
                opt("Lipids -> genetic information storage"),
                opt("Carbohydrates -> catalysis of all reactions"),
                opt("Nucleic acids -> membrane barriers"),
            ),
            "Proteins serve as enzymes and structural elements; the other roles are mismatched.",
        ),
        q(
            "Enzymes are most often made of which biomolecule?",
            (
                opt("Proteins", correct=True),
                opt("Triacylglycerols"),
                opt("Polysaccharides"),
                opt("Phospholipids"),
            ),
            "Most enzymes are proteins (a few are catalytic RNAs called ribozymes).",
        ),
    ),
)
