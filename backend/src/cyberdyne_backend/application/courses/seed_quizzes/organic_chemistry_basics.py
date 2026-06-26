"""Quiz questions for the Organic Chemistry - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Carbon, bonding and hybridization": (
            q(
                "How many valence electrons does a carbon atom have?",
                (opt("4", correct=True), opt("2"), opt("6"), opt("8")),
                "Carbon is 1s2 2s2 2p2, giving four valence electrons.",
            ),
            q(
                "What is the approximate bond angle around an sp3-hybridized carbon?",
                (
                    opt("109.5 degrees", correct=True),
                    opt("90 degrees"),
                    opt("120 degrees"),
                    opt("180 degrees"),
                ),
                "Four sp3 hybrids point to the corners of a tetrahedron, about 109.5 degrees.",
            ),
            q(
                "A carbon-carbon triple bond consists of:",
                (
                    opt("one sigma bond and two pi bonds", correct=True),
                    opt("three sigma bonds"),
                    opt("one sigma bond and one pi bond"),
                    opt("two sigma bonds and one pi bond"),
                ),
                "A triple bond is one head-on sigma plus two side-on pi bonds (sp carbon).",
            ),
        ),
        "Lewis structures, formal charge and resonance": (
            q(
                "Formal charge equals valence electrons minus nonbonding electrons minus:",
                (
                    opt("half the bonding electrons", correct=True),
                    opt("all the bonding electrons"),
                    opt("the number of lone pairs"),
                    opt("the atomic number"),
                ),
                "FC = valence - nonbonding - (1/2)(bonding electrons).",
            ),
            q(
                "Curved arrows in resonance structures show the movement of:",
                (
                    opt("electron pairs", correct=True),
                    opt("atoms"),
                    opt("protons only"),
                    opt("whole molecules"),
                ),
                "Resonance arrows move electron pairs; atoms stay put.",
            ),
            q(
                "Why are the two C-O bonds in carboxylate identical?",
                (
                    opt(
                        "the negative charge is delocalized over both oxygens by resonance",
                        correct=True,
                    ),
                    opt("carbon forms two double bonds at once"),
                    opt("oxygen atoms repel equally"),
                    opt("the molecule is not really an ion"),
                ),
                "Resonance delocalizes the charge, making both C-O bonds equivalent.",
            ),
        ),
        "Functional groups": (
            q(
                "Which functional group contains a -COOH unit?",
                (opt("carboxylic acid", correct=True), opt("alcohol"), opt("ketone"), opt("amine")),
                "A carboxylic acid has the -COOH (carboxyl) group.",
            ),
            q(
                "Which carboxylic acid derivative is the LEAST reactive toward nucleophilic acyl substitution?",
                (opt("amide", correct=True), opt("acyl halide"), opt("anhydride"), opt("ester")),
                "Reactivity order: acyl halide > anhydride > ester ~ acid > amide.",
            ),
            q(
                "An aldehyde is characterized by which group?",
                (
                    opt("-CHO (terminal carbonyl)", correct=True),
                    opt("-OH"),
                    opt("-NH2"),
                    opt("C-O-C"),
                ),
                "Aldehydes carry a -CHO group at the end of a chain.",
            ),
        ),
        "IUPAC nomenclature": (
            q(
                "In choosing the principal chain, you select the longest chain that contains:",
                (
                    opt("the highest-priority functional group", correct=True),
                    opt("the most branches"),
                    opt("the fewest carbons"),
                    opt("only single bonds"),
                ),
                "The principal chain must contain the principal characteristic group.",
            ),
            q(
                "Which group has the highest suffix priority?",
                (opt("carboxylic acid", correct=True), opt("ketone"), opt("alcohol"), opt("amine")),
                "Carboxylic acid outranks ester, amide, aldehyde, ketone, alcohol and amine.",
            ),
            q(
                "The stem 'pent-' denotes how many carbons in the parent chain?",
                (opt("5", correct=True), opt("3"), opt("4"), opt("6")),
                "meth(1), eth(2), prop(3), but(4), pent(5), hex(6).",
            ),
        ),
        "Isomers and intermolecular forces": (
            q(
                "Butane and isobutane (both C4H10) are examples of:",
                (
                    opt("constitutional (structural) isomers", correct=True),
                    opt("enantiomers"),
                    opt("the same compound"),
                    opt("diastereomers"),
                ),
                "They share a formula but differ in connectivity.",
            ),
            q(
                "Which intermolecular force is the strongest and raises boiling points the most?",
                (
                    opt("hydrogen bonding", correct=True),
                    opt("London dispersion"),
                    opt("dipole-dipole"),
                    opt("ion-induced dipole in alkanes"),
                ),
                "Hydrogen bonding (H to N, O, F) is the strongest of these.",
            ),
            q(
                "Why does boiling point rise along a series of n-alkanes?",
                (
                    opt(
                        "London dispersion forces grow with chain length/surface area", correct=True
                    ),
                    opt("hydrogen bonding increases"),
                    opt("the molecules become ionic"),
                    opt("dipole moments grow"),
                ),
                "Longer alkanes have more surface area and stronger cumulative dispersion.",
            ),
        ),
    },
    final=(
        q(
            "An sp-hybridized carbon has what geometry and bond angle?",
            (
                opt("linear, 180 degrees", correct=True),
                opt("trigonal, 120 degrees"),
                opt("tetrahedral, 109.5 degrees"),
                opt("bent, 104.5 degrees"),
            ),
            "Two sp hybrids point opposite, giving a linear 180-degree arrangement.",
        ),
        q(
            "Resonance delocalization generally does what to a molecule's energy?",
            (
                opt("lowers it (stabilizes)", correct=True),
                opt("raises it"),
                opt("has no effect"),
                opt("makes it ionic"),
            ),
            "Spreading electrons over more atoms lowers energy and stabilizes the species.",
        ),
        q(
            "Which is a hydrocarbon functional group?",
            (
                opt("alkene (C=C)", correct=True),
                opt("alcohol (-OH)"),
                opt("amine (C-N)"),
                opt("ester (-COOR)"),
            ),
            "Alkenes contain only carbon and hydrogen with a C=C double bond.",
        ),
        q(
            "When numbering an IUPAC chain, locants are assigned to give:",
            (
                opt("the lowest set to the principal group first", correct=True),
                opt("the highest possible numbers"),
                opt("numbers only to substituents"),
                opt("locants alphabetically"),
            ),
            "Lowest locants go to the principal group, then unsaturation, then substituents.",
        ),
        q(
            "A C=O stretch near 1700 cm-1 in an IR spectrum indicates a:",
            (
                opt("carbonyl group", correct=True),
                opt("hydroxyl group"),
                opt("C-H bond"),
                opt("C-C single bond"),
            ),
            "The carbonyl C=O stretch appears strongly around 1700 cm-1.",
        ),
        q(
            "Alcohols boil much higher than alkanes of similar mass mainly because they:",
            (
                opt("can hydrogen bond", correct=True),
                opt("are heavier"),
                opt("are ionic"),
                opt("have weaker dispersion forces"),
            ),
            "The -OH group enables hydrogen bonding, sharply raising boiling point.",
        ),
    ),
)
