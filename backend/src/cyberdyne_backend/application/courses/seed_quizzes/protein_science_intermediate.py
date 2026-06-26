"""Quiz questions for the Protein Science & Enzymology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Folding thermodynamics and stability": (
            q(
                "The net stability of a typical small protein is:",
                (
                    opt(
                        "a small margin (about 20-60 kJ/mol) from large opposing terms",
                        correct=True,
                    ),
                    opt("hundreds of kJ/mol, very large"),
                    opt("exactly zero"),
                    opt("negative, so the unfolded state is favoured"),
                ),
                "Folding stability is a small difference between large favourable and unfavourable terms.",
            ),
            q(
                "Which term opposes folding?",
                (
                    opt("loss of chain conformational entropy", correct=True),
                    opt("the hydrophobic effect"),
                    opt("backbone hydrogen bonding"),
                    opt("van der Waals packing"),
                ),
                "Folding restricts the chain, costing conformational entropy.",
            ),
            q(
                "The melting temperature Tm of a protein is where:",
                (
                    opt("half the molecules are unfolded", correct=True),
                    opt("all molecules are folded"),
                    opt("the enzyme has maximal activity"),
                    opt("Km equals Vmax"),
                ),
                "Tm is the midpoint of the thermal unfolding transition.",
            ),
        ),
        "Folding kinetics and the energy landscape": (
            q(
                "Levinthal's paradox is resolved by:",
                (
                    opt("a biased folding funnel landscape", correct=True),
                    opt("random conformational search"),
                    opt("covalent locking of every intermediate"),
                    opt("the absence of any transition state"),
                ),
                "The energy landscape funnels the chain downhill toward the native state.",
            ),
            q(
                "Phi-value analysis probes:",
                (
                    opt("which contacts are formed at the folding transition state", correct=True),
                    opt("the substrate specificity of an enzyme"),
                    opt("the melting temperature"),
                    opt("quaternary subunit count"),
                ),
                "Phi values report contact formation at the transition state via mutation effects.",
            ),
            q(
                "Molecular chaperones such as GroEL/GroES function to:",
                (
                    opt("prevent misfolding and aggregation", correct=True),
                    opt("cleave peptide bonds"),
                    opt("speed only the chemical catalytic step"),
                    opt("synthesise amino acids"),
                ),
                "Chaperones assist folding and suppress aggregation in the cell.",
            ),
        ),
        "Protein dynamics and allostery": (
            q(
                "Allostery is best defined as:",
                (
                    opt(
                        "regulation where binding at one site changes activity at a distinct site",
                        correct=True,
                    ),
                    opt("competition at the same active site"),
                    opt("irreversible denaturation"),
                    opt("formation of a disulfide bond"),
                ),
                "An allosteric effector acts at a site distinct from the functional site.",
            ),
            q(
                "The MWC model of allostery assumes:",
                (
                    opt(
                        "a concerted switch of the whole oligomer between T and R states",
                        correct=True,
                    ),
                    opt("subunits change strictly one at a time"),
                    opt("no conformational change at all"),
                    opt("covalent modification of every subunit"),
                ),
                "MWC is the concerted model; KNF is the sequential model.",
            ),
            q(
                "Cooperative ligand binding produces a saturation curve that is:",
                (
                    opt("sigmoidal", correct=True),
                    opt("a straight line"),
                    opt("a simple hyperbola"),
                    opt("exponentially decaying"),
                ),
                "Positive cooperativity gives a sigmoidal (S-shaped) binding curve.",
            ),
        ),
        "Enzyme kinetics: Michaelis-Menten": (
            q(
                "In the Michaelis-Menten equation, Km is:",
                (
                    opt("the substrate concentration giving half-maximal velocity", correct=True),
                    opt("the maximum velocity"),
                    opt("the turnover number"),
                    opt("the total enzyme concentration"),
                ),
                "v = Vmax[S]/(Km+[S]); v = Vmax/2 when [S] = Km.",
            ),
            q(
                "The specificity constant kcat/Km measures:",
                (
                    opt("catalytic efficiency, bounded by the diffusion limit", correct=True),
                    opt("the melting temperature"),
                    opt("the dissociation constant of an inhibitor"),
                    opt("the number of subunits"),
                ),
                "kcat/Km is efficiency, capped near 10^8 to 10^9 per M per s.",
            ),
            q(
                "The steady-state assumption sets:",
                (
                    opt("the rate of change of [ES] to approximately zero", correct=True),
                    opt("[S] to zero"),
                    opt("Vmax to zero"),
                    opt("the enzyme concentration to infinity"),
                ),
                "Steady state assumes d[ES]/dt is about zero during initial velocity.",
            ),
        ),
        "Linearisations and enzyme inhibition": (
            q(
                "A competitive inhibitor:",
                (
                    opt("raises apparent Km while leaving Vmax unchanged", correct=True),
                    opt("lowers Vmax while leaving Km unchanged"),
                    opt("lowers both Km and Vmax"),
                    opt("has no effect on kinetics"),
                ),
                "Competing for the active site raises apparent Km; Vmax is reached at high [S].",
            ),
            q(
                "Which linearisation plots 1/v against 1/[S]?",
                (
                    opt("Lineweaver-Burk", correct=True),
                    opt("Eadie-Hofstee"),
                    opt("Hanes-Woolf"),
                    opt("Ramachandran"),
                ),
                "The double-reciprocal Lineweaver-Burk plot uses 1/v vs 1/[S].",
            ),
            q(
                "An uncompetitive inhibitor binds:",
                (
                    opt("only the ES complex, lowering both Km and Vmax", correct=True),
                    opt("only free enzyme at the active site"),
                    opt("nowhere on the enzyme"),
                    opt("the substrate covalently"),
                ),
                "Uncompetitive inhibitors bind ES and reduce both Km and Vmax.",
            ),
        ),
    },
    final=(
        q(
            "Folding stability is the free-energy difference between which states?",
            (
                opt("native and unfolded", correct=True),
                opt("substrate and product"),
                opt("enzyme and inhibitor"),
                opt("T and R quaternary states"),
            ),
            "dG_fold = G_native - G_unfolded.",
        ),
        q(
            "Many small single-domain proteins unfold in a transition that is:",
            (
                opt("two-state and cooperative", correct=True),
                opt("multi-state with many intermediates"),
                opt("never reversible"),
                opt("instantaneous and barrierless"),
            ),
            "Two-state, cooperative unfolding shows no populated intermediates.",
        ),
        q(
            "A two-state folding reaction approaches equilibrium with an observed rate equal to:",
            (
                opt("kf + ku", correct=True),
                opt("kf - ku"),
                opt("kf times ku"),
                opt("kcat/Km"),
            ),
            "For two-state kinetics, kobs = kf + ku.",
        ),
        q(
            "The turnover number of an enzyme is:",
            (
                opt("kcat, reactions per active site per second", correct=True),
                opt("Km"),
                opt("the dissociation constant"),
                opt("the melting temperature"),
            ),
            "kcat is the turnover number, with Vmax = kcat times total enzyme.",
        ),
        q(
            "Haemoglobin's sigmoidal oxygen binding is an example of:",
            (
                opt("positive cooperativity / allostery", correct=True),
                opt("competitive inhibition"),
                opt("two-state folding"),
                opt("covalent catalysis"),
            ),
            "Cooperative binding among subunits gives the sigmoidal curve.",
        ),
        q(
            "Which technique reports protein conformational dynamics?",
            (
                opt("NMR relaxation dispersion", correct=True),
                opt("Lineweaver-Burk plotting"),
                opt("the Henderson-Hasselbalch equation"),
                opt("gel staining only"),
            ),
            "NMR relaxation dispersion, HDX-MS and smFRET probe dynamics.",
        ),
    ),
)
