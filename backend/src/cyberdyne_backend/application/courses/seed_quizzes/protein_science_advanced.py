"""Quiz questions for the Protein Science & Enzymology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Catalytic mechanism and transition-state theory": (
            q(
                "Enzymes accelerate reactions primarily by:",
                (
                    opt(
                        "stabilising the transition state relative to the ground state",
                        correct=True,
                    ),
                    opt("raising the activation barrier"),
                    opt("being consumed in the reaction"),
                    opt("increasing the substrate concentration"),
                ),
                "Preferential transition-state binding lowers the activation free energy.",
            ),
            q(
                "The serine protease catalytic triad consists of:",
                (
                    opt("Ser, His, Asp", correct=True),
                    opt("Lys, Arg, Glu"),
                    opt("Cys, Gly, Ala"),
                    opt("Phe, Tyr, Trp"),
                ),
                "Serine proteases use a Ser-His-Asp triad for covalent catalysis.",
            ),
            q(
                "According to transition-state theory, the rate depends on the activation free energy as:",
                (
                    opt("k proportional to exp(-dG_double_dagger/RT)", correct=True),
                    opt("k proportional to dG_double_dagger"),
                    opt("k proportional to 1/dG_double_dagger"),
                    opt("k independent of dG_double_dagger"),
                ),
                "Rate falls exponentially with the activation free energy barrier.",
            ),
        ),
        "Structure determination and AlphaFold": (
            q(
                "Which method requires no crystals and excels at large complexes?",
                (
                    opt("Cryo-electron microscopy", correct=True),
                    opt("X-ray crystallography"),
                    opt("Lineweaver-Burk plotting"),
                    opt("Edman degradation"),
                ),
                "Cryo-EM resolves large assemblies without crystallisation.",
            ),
            q(
                "AlphaFold2's per-residue confidence metric is called:",
                (
                    opt("pLDDT", correct=True),
                    opt("Km"),
                    opt("RMSD only"),
                    opt("pKa"),
                ),
                "pLDDT scores per-residue confidence; PAE scores inter-domain confidence.",
            ),
            q(
                "A key input that lets AlphaFold2 detect contacting residues is:",
                (
                    opt("the multiple sequence alignment (coevolution signal)", correct=True),
                    opt("the melting temperature"),
                    opt("the inhibitor IC50"),
                    opt("the gel migration distance"),
                ),
                "Coevolving residues in the MSA flag spatial contacts.",
            ),
        ),
        "Protein engineering and de novo design": (
            q(
                "Directed evolution requires:",
                (
                    opt("diversification plus a good screen or selection", correct=True),
                    opt("a complete atomic mechanism"),
                    opt("a solved crystal structure"),
                    opt("no genetic variation at all"),
                ),
                "It iterates mutate-and-select using an assay, no mechanistic model needed.",
            ),
            q(
                "RFdiffusion is used to:",
                (
                    opt("generate new protein backbones by denoising diffusion", correct=True),
                    opt("measure enzyme Km"),
                    opt("crystallise proteins"),
                    opt("sequence DNA"),
                ),
                "RFdiffusion designs de novo backbones; ProteinMPNN then designs sequences.",
            ),
            q(
                "Frances Arnold received a Nobel Prize for:",
                (
                    opt("the directed evolution of enzymes", correct=True),
                    opt("X-ray crystallography"),
                    opt("discovering the peptide bond"),
                    opt("inventing PROTACs"),
                ),
                "Arnold shared the 2018 Chemistry Nobel for directed evolution.",
            ),
        ),
        "Inhibitor design and computational methods": (
            q(
                "The IC50 of an inhibitor is the concentration that gives:",
                (
                    opt("half-maximal inhibition", correct=True),
                    opt("complete inhibition"),
                    opt("no inhibition"),
                    opt("maximal enzyme activity"),
                ),
                "IC50 is the inflection point of the dose-response curve.",
            ),
            q(
                "Free-energy perturbation (FEP) is used to predict:",
                (
                    opt("relative binding affinities of congeneric ligands", correct=True),
                    opt("protein melting temperature"),
                    opt("the genetic code"),
                    opt("crystal space groups"),
                ),
                "FEP estimates relative binding free energies, often within about 1 kcal/mol.",
            ),
            q(
                "Virtual screening primarily serves to:",
                (
                    opt("rank large compound libraries computationally", correct=True),
                    opt("synthesise compounds automatically"),
                    opt("determine a crystal structure"),
                    opt("measure kcat experimentally"),
                ),
                "Docking-based virtual screening ranks millions of candidates in silico.",
            ),
        ),
        "Disorder, condensates and the frontier": (
            q(
                "Intrinsically disordered proteins:",
                (
                    opt("lack a single stable structure yet are functional", correct=True),
                    opt("always fold into rigid TIM barrels"),
                    opt("cannot bind any partner"),
                    opt("are never found in signalling"),
                ),
                "IDPs function as flexible ensembles, often folding upon binding.",
            ),
            q(
                "Biomolecular condensates form mainly via:",
                (
                    opt(
                        "liquid-liquid phase separation driven by multivalent weak interactions",
                        correct=True,
                    ),
                    opt("disulfide cross-linking only"),
                    opt("covalent peptide bond formation"),
                    opt("X-ray irradiation"),
                ),
                "Multivalent weak contacts drive LLPS into membraneless condensates.",
            ),
            q(
                "Aberrant maturation of condensates to solid aggregates is linked to:",
                (
                    opt("neurodegeneration (e.g. FUS, TDP-43 in ALS)", correct=True),
                    opt("faster enzyme catalysis"),
                    opt("improved protein stability"),
                    opt("higher AlphaFold confidence"),
                ),
                "Liquid-to-solid transitions of FUS and TDP-43 are implicated in ALS.",
            ),
        ),
    },
    final=(
        q(
            "Enzymes lower which quantity to speed a reaction?",
            (
                opt("the activation free energy of the transition state", correct=True),
                opt("the equilibrium constant of the overall reaction"),
                opt("the temperature"),
                opt("the substrate concentration"),
            ),
            "Catalysis lowers the activation barrier without changing equilibrium.",
        ),
        q(
            "AlphaFold2's core network that processes the MSA is the:",
            (
                opt("Evoformer", correct=True),
                opt("Transformer decoder for text"),
                opt("Lineweaver-Burk module"),
                opt("Rosetta scorer"),
            ),
            "The Evoformer attention stack feeds the structure module.",
        ),
        q(
            "Which tool designs a sequence for a given target backbone?",
            (
                opt("ProteinMPNN", correct=True),
                opt("Cryo-EM"),
                opt("FEP"),
                opt("Edman degradation"),
            ),
            "ProteinMPNN is a deep-learning sequence designer for fixed backbones.",
        ),
        q(
            "Binding free energy relates to the dissociation constant by:",
            (
                opt("dG = RT ln Kd", correct=True),
                opt("dG = Kd squared"),
                opt("dG = Km/Vmax"),
                opt("dG = -log[H+]"),
            ),
            "Tighter binding (smaller Kd) corresponds to more negative dG.",
        ),
        q(
            "A PROTAC is an example of a strategy that:",
            (
                opt("extends beyond classical reversible inhibition", correct=True),
                opt("measures melting temperature"),
                opt("is a type of crystallography"),
                opt("is a folding intermediate"),
            ),
            "PROTACs induce targeted degradation, beyond reversible active-site blocking.",
        ),
        q(
            "Intrinsic disorder challenges which classic paradigm?",
            (
                opt("structure determines function", correct=True),
                opt("the Michaelis-Menten equation"),
                opt("transition-state theory"),
                opt("the second law of thermodynamics"),
            ),
            "IDPs are functional without a single fixed structure.",
        ),
    ),
)
