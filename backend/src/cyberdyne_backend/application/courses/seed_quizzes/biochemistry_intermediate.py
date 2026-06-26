"""Quiz questions for the Biochemistry - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Protein structure: four levels": (
            q(
                "The primary structure of a protein is its:",
                (
                    opt("amino-acid sequence", correct=True),
                    opt("alpha-helices and beta-sheets"),
                    opt("overall 3D fold"),
                    opt("multi-subunit assembly"),
                ),
                "Primary structure is the covalent order of amino acids set by the gene.",
            ),
            q(
                "An alpha-helix and a beta-sheet are examples of:",
                (
                    opt("secondary structure", correct=True),
                    opt("primary structure"),
                    opt("quaternary structure"),
                    opt("denatured states"),
                ),
                "Secondary structure is local backbone folding stabilised by hydrogen bonds.",
            ),
            q(
                "Quaternary structure refers to:",
                (
                    opt("the assembly of multiple polypeptide subunits", correct=True),
                    opt("the linear sequence of residues"),
                    opt("a single alpha-helix"),
                    opt("the peptide bond geometry"),
                ),
                "Quaternary structure is how multiple folded chains assemble, as in haemoglobin.",
            ),
        ),
        "Enzymes and catalysis": (
            q(
                "Enzymes speed up reactions by:",
                (
                    opt("lowering the activation energy", correct=True),
                    opt("changing the equilibrium constant"),
                    opt("increasing the free-energy difference"),
                    opt("being consumed in the reaction"),
                ),
                "Enzymes stabilise the transition state, lowering Ea without altering equilibrium.",
            ),
            q(
                "The modern view of substrate binding is best described as:",
                (
                    opt(
                        "induced fit, with the active site adjusting to the substrate", correct=True
                    ),
                    opt("a rigid lock and key that never changes shape"),
                    opt("random collision with no specificity"),
                    opt("permanent covalent attachment to the substrate"),
                ),
                "Induced fit captures the conformational adjustment of the active site on binding.",
            ),
            q(
                "An enzyme changes which of the following?",
                (
                    opt("the rate at which equilibrium is reached", correct=True),
                    opt("the position of equilibrium"),
                    opt("the overall free-energy change of the reaction"),
                    opt("the thermodynamic favourability of the reaction"),
                ),
                "Catalysts accelerate the approach to equilibrium but do not shift it.",
            ),
        ),
        "Michaelis-Menten kinetics": (
            q(
                "In the Michaelis-Menten equation, Km is:",
                (
                    opt("the substrate concentration giving half-maximal velocity", correct=True),
                    opt("the maximum reaction velocity"),
                    opt("the turnover number kcat"),
                    opt("the total enzyme concentration"),
                ),
                "Km is [S] at which v0 = Vmax/2; a low Km indicates tight binding.",
            ),
            q(
                "Vmax is reached when:",
                (
                    opt("the enzyme is saturated with substrate", correct=True),
                    opt("substrate concentration is zero"),
                    opt("the inhibitor concentration is maximal"),
                    opt("temperature is at absolute zero"),
                ),
                "At saturating [S] essentially all enzyme is in the ES form, giving Vmax.",
            ),
            q(
                "The specificity constant kcat/Km measures:",
                (
                    opt("catalytic efficiency, bounded by the diffusion limit", correct=True),
                    opt("the molecular weight of the enzyme"),
                    opt("the pH optimum"),
                    opt("the number of subunits"),
                ),
                "kcat/Km gauges efficiency and cannot exceed the diffusion-controlled limit.",
            ),
        ),
        "Enzyme inhibition": (
            q(
                "A competitive inhibitor affects the kinetics by:",
                (
                    opt("raising the apparent Km while Vmax is unchanged", correct=True),
                    opt("lowering Vmax while Km is unchanged"),
                    opt("lowering both Km and Vmax"),
                    opt("raising both Km and Vmax"),
                ),
                "It competes for the active site; saturating substrate still reaches the same Vmax.",
            ),
            q(
                "A noncompetitive inhibitor typically:",
                (
                    opt("lowers Vmax while leaving Km unchanged", correct=True),
                    opt("raises Km while leaving Vmax unchanged"),
                    opt("has no effect on the enzyme"),
                    opt("only binds the free substrate"),
                ),
                "Binding away from the active site reduces Vmax without changing apparent affinity.",
            ),
            q(
                "Aspirin acetylating cyclooxygenase is an example of:",
                (
                    opt("irreversible (covalent) inhibition", correct=True),
                    opt("competitive inhibition"),
                    opt("uncompetitive inhibition"),
                    opt("allosteric activation"),
                ),
                "A covalent modification permanently disables the enzyme.",
            ),
        ),
        "Bioenergetics: ATP and redox": (
            q(
                "A reaction is spontaneous (exergonic) when:",
                (
                    opt("delta G is negative", correct=True),
                    opt("delta G is positive"),
                    opt("delta G is zero"),
                    opt("enthalpy is positive"),
                ),
                "Negative Gibbs free-energy change indicates a spontaneous reaction.",
            ),
            q(
                "Cells run endergonic reactions by:",
                (
                    opt("coupling them to exergonic reactions like ATP hydrolysis", correct=True),
                    opt("lowering the temperature to zero"),
                    opt("removing all enzymes"),
                    opt("increasing the pH indefinitely"),
                ),
                "Energetic coupling, often to ATP hydrolysis, drives unfavourable reactions.",
            ),
            q(
                "NAD+ and FAD function in metabolism as:",
                (
                    opt("electron (reducing-power) carriers", correct=True),
                    opt("structural membrane lipids"),
                    opt("genetic information carriers"),
                    opt("primary osmotic solutes"),
                ),
                "They shuttle electrons as NADH and FADH2 in redox reactions.",
            ),
        ),
        "Glycolysis and the citric acid cycle": (
            q(
                "The net ATP yield of glycolysis per glucose is:",
                (
                    opt("2 ATP (and 2 NADH)", correct=True),
                    opt("36 ATP"),
                    opt("0 ATP"),
                    opt("4 ATP with no NADH"),
                ),
                "Investment costs 2 ATP and payoff makes 4, for a net of 2 ATP plus 2 NADH.",
            ),
            q(
                "Pyruvate is converted to acetyl-CoA by:",
                (
                    opt("pyruvate dehydrogenase", correct=True),
                    opt("phosphofructokinase-1"),
                    opt("ATP synthase"),
                    opt("hexokinase"),
                ),
                "The pyruvate dehydrogenase complex oxidatively decarboxylates pyruvate to acetyl-CoA.",
            ),
            q(
                "The main energy products harvested per turn of the citric acid cycle are:",
                (
                    opt("3 NADH, 1 FADH2 and 1 GTP", correct=True),
                    opt("4 ATP directly"),
                    opt("only CO2"),
                    opt("2 NADH and nothing else"),
                ),
                "Each acetyl-CoA turn yields 3 NADH, 1 FADH2, 1 GTP and 2 CO2.",
            ),
        ),
    },
    final=(
        q(
            "Which level of structure is set directly by the gene sequence?",
            (
                opt("Primary structure", correct=True),
                opt("Secondary structure"),
                opt("Tertiary structure"),
                opt("Quaternary structure"),
            ),
            "The gene specifies the amino-acid sequence, i.e. primary structure.",
        ),
        q(
            "Catalytic efficiency of an enzyme is best captured by:",
            (
                opt("kcat/Km", correct=True),
                opt("Km alone"),
                opt("Vmax alone"),
                opt("the molecular weight"),
            ),
            "The specificity constant kcat/Km combines turnover and affinity.",
        ),
        q(
            "A competitive inhibitor can be overcome by:",
            (
                opt("increasing substrate concentration", correct=True),
                opt("lowering substrate concentration"),
                opt("removing the enzyme"),
                opt("decreasing temperature only"),
            ),
            "High substrate outcompetes a competitive inhibitor, restoring Vmax.",
        ),
        q(
            "The approximate free energy released by ATP hydrolysis under standard conditions is:",
            (
                opt("about -30.5 kJ/mol", correct=True),
                opt("about +30.5 kJ/mol"),
                opt("about -300 kJ/mol"),
                opt("zero"),
            ),
            "Standard ATP hydrolysis releases roughly -30.5 kJ/mol (more in the cell).",
        ),
        q(
            "Glycolysis occurs in the cytosol and produces which final product?",
            (
                opt("pyruvate", correct=True),
                opt("acetyl-CoA"),
                opt("citrate"),
                opt("oxaloacetate"),
            ),
            "Glycolysis splits glucose into two pyruvate in the cytosol.",
        ),
        q(
            "The reducing equivalents (NADH, FADH2) from glycolysis and the TCA cycle are used to:",
            (
                opt("drive oxidative phosphorylation to make ATP", correct=True),
                opt("store genetic information"),
                opt("build the plasma membrane"),
                opt("lower the cell's pH directly"),
            ),
            "Their electrons feed the electron transport chain to power ATP synthesis.",
        ),
    ),
)
