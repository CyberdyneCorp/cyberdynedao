"""Quiz questions for the Protein-Ligand Binding & Free-Energy Methods - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The binding equilibrium and Kd": (
            q(
                "What does a smaller dissociation constant Kd indicate?",
                (
                    opt("Tighter binding between ligand and receptor", correct=True),
                    opt("Weaker binding"),
                    opt("No binding at all"),
                    opt("A covalent bond has formed"),
                ),
                "Kd is the free-ligand concentration for half-occupancy; lower Kd means higher affinity.",
            ),
            q(
                "Kd can be written as the ratio of which two rate constants?",
                (
                    opt("koff / kon", correct=True),
                    opt("kon / koff"),
                    opt("kon * koff"),
                    opt("kon + koff"),
                ),
                "Kd = koff/kon, the balance of dissociation over association rates.",
            ),
            q(
                "At what free-ligand concentration is the receptor half-occupied?",
                (
                    opt("When [L] equals Kd", correct=True),
                    opt("When [L] equals zero"),
                    opt("When [L] is twice Kd"),
                    opt("Never; occupancy is always full"),
                ),
                "The Langmuir isotherm gives 50% occupancy exactly at [L] = Kd.",
            ),
        ),
        "From affinity to free energy": (
            q(
                "How is binding free energy related to the dissociation constant?",
                (
                    opt("ΔG° = RT ln Kd", correct=True),
                    opt("ΔG° = RT * Kd"),
                    opt("ΔG° = Kd / RT"),
                    opt("ΔG° is independent of Kd"),
                ),
                "ΔG° = -RT ln Ka = RT ln Kd; more negative ΔG° means tighter binding.",
            ),
            q(
                "Roughly how much binding free energy does each 10-fold gain in affinity buy at room temperature?",
                (
                    opt("About 1.36 kcal/mol", correct=True),
                    opt("About 10 kcal/mol"),
                    opt("About 100 kcal/mol"),
                    opt("Zero, affinity and energy are unrelated"),
                ),
                "RT ln 10 is about 1.36 kcal/mol at 298 K, so the relationship is logarithmic.",
            ),
            q(
                "Why is roughly 1 kcal/mol accuracy ('chemical accuracy') the target for binding prediction?",
                (
                    opt(
                        "Affinity differences of interest are tiny on the molecular energy scale",
                        correct=True,
                    ),
                    opt("Because proteins have exactly 1 kcal/mol of energy"),
                    opt("Because solvents always add 1 kcal/mol"),
                    opt("Because experiments cannot measure better than that"),
                ),
                "A 1000-fold affinity span is only about 4 kcal/mol, so methods must resolve ~1 kcal/mol.",
            ),
        ),
        "Enthalpy, entropy and the binding signature": (
            q(
                "How does binding free energy decompose?",
                (
                    opt("ΔG = ΔH - TΔS", correct=True),
                    opt("ΔG = ΔH + TΔS squared"),
                    opt("ΔG = TΔS - ΔH always positive"),
                    opt("ΔG depends only on temperature"),
                ),
                "Gibbs free energy combines enthalpic and entropic contributions.",
            ),
            q(
                "Which experimental method directly yields the full thermodynamic signature (Kd, ΔH, stoichiometry)?",
                (
                    opt("Isothermal titration calorimetry (ITC)", correct=True),
                    opt("X-ray crystallography"),
                    opt("Mass spectrometry"),
                    opt("Circular dichroism"),
                ),
                "ITC measures heat of binding, giving Kd, ΔH and stoichiometry in one experiment.",
            ),
            q(
                "What is enthalpy-entropy compensation?",
                (
                    opt(
                        "Gains in ΔH are partly offset by losses in entropy, so ΔG moves less",
                        correct=True,
                    ),
                    opt("Enthalpy and entropy are always equal"),
                    opt("Entropy always dominates over enthalpy"),
                    opt("Compensation only occurs at zero temperature"),
                ),
                "Tightening a contact often rigidifies the complex, paying back entropy.",
            ),
        ),
        "Molecular forces in recognition": (
            q(
                "Which interaction is the dominant driver of binding for many drugs?",
                (
                    opt("The hydrophobic effect (releasing ordered water)", correct=True),
                    opt("Covalent bond formation"),
                    opt("Gravitational attraction"),
                    opt("Nuclear forces"),
                ),
                "Burying nonpolar surface releases structured water, a strongly favourable contribution.",
            ),
            q(
                "What does the Lennard-Jones potential describe?",
                (
                    opt(
                        "The balance of van der Waals attraction and short-range repulsion",
                        correct=True,
                    ),
                    opt("Only covalent bonding"),
                    opt("Only electrostatic salt bridges"),
                    opt("The entropy of solvent"),
                ),
                "Its 12-6 form captures steric repulsion and dispersion attraction.",
            ),
            q(
                "Hydrogen bonds are especially important for which property of binding?",
                (
                    opt("Specificity, because they are directional", correct=True),
                    opt("Color of the complex"),
                    opt("Molecular weight"),
                    opt("Boiling point"),
                ),
                "Directional donor-acceptor geometry makes H-bonds key to selective recognition.",
            ),
        ),
        "Induced fit and conformational selection": (
            q(
                "In the induced-fit model, what happens after the ligand binds?",
                (
                    opt("The protein reshapes its pocket to optimise contacts", correct=True),
                    opt("The ligand immediately dissociates"),
                    opt("The protein unfolds completely"),
                    opt("Nothing changes in the protein"),
                ),
                "Induced fit means binding triggers a conformational adjustment of the receptor.",
            ),
            q(
                "In conformational selection, the ligand binds to:",
                (
                    opt("A pre-existing, often rare, binding-competent conformation", correct=True),
                    opt("A conformation that does not exist before binding"),
                    opt("The fully unfolded state only"),
                    opt("Any random conformation with equal probability"),
                ),
                "The protein already samples the competent state; the ligand selects and stabilises it.",
            ),
            q(
                "What is a cryptic pocket?",
                (
                    opt(
                        "A binding site invisible in the apo structure that opens transiently",
                        correct=True,
                    ),
                    opt("A site that is always wide open"),
                    opt("A covalent warhead"),
                    opt("A type of crystallisation buffer"),
                ),
                "Cryptic pockets appear only in certain conformations, explaining why static structures miss them.",
            ),
        ),
        "Measuring affinity experimentally": (
            q(
                "Which method measures kon and koff in real time to give binding kinetics?",
                (
                    opt("Surface plasmon resonance (SPR)", correct=True),
                    opt("Isothermal titration calorimetry"),
                    opt("X-ray diffraction"),
                    opt("Gel electrophoresis"),
                ),
                "SPR tracks association and dissociation, yielding rate constants and thus Kd.",
            ),
            q(
                "The Cheng-Prusoff relation converts which measured quantity to Ki?",
                (
                    opt("IC50", correct=True),
                    opt("Molecular weight"),
                    opt("Melting temperature"),
                    opt("logP"),
                ),
                "Ki = IC50 / (1 + [S]/Km) corrects IC50 for substrate competition.",
            ),
            q(
                "Why can residence time matter beyond equilibrium Kd?",
                (
                    opt(
                        "A long residence time (1/koff) can sustain efficacy even with modest Kd",
                        correct=True,
                    ),
                    opt("Residence time changes the molecular weight"),
                    opt("It only affects the color of the assay"),
                    opt("It is identical to Kd in all cases"),
                ),
                "Slow dissociation can prolong target engagement independent of equilibrium affinity.",
            ),
        ),
    },
    final=(
        q(
            "The dissociation constant Kd equals the ligand concentration at which:",
            (
                opt("The receptor is half-occupied", correct=True),
                opt("The receptor is fully saturated"),
                opt("No ligand is bound"),
                opt("The ligand is fully metabolised"),
            ),
            "Half-maximal occupancy occurs at [L] = Kd in the Langmuir isotherm.",
        ),
        q(
            "Binding free energy relates to affinity by:",
            (
                opt("ΔG° = -RT ln Ka", correct=True),
                opt("ΔG° = Ka * RT"),
                opt("ΔG° = RT / Ka"),
                opt("ΔG° is constant for all ligands"),
            ),
            "Tighter binding (larger Ka, smaller Kd) gives a more negative ΔG°.",
        ),
        q(
            "Two ligands with the same ΔG can differ in:",
            (
                opt(
                    "Their balance of enthalpy and entropy (thermodynamic signature)", correct=True
                ),
                opt("Nothing; ΔG fixes everything"),
                opt("Only their molecular formula"),
                opt("Only their color"),
            ),
            "Equal ΔG can arise from enthalpy-driven or entropy-driven binding.",
        ),
        q(
            "Which force is most often the dominant driver of small-molecule binding?",
            (
                opt("The hydrophobic effect", correct=True),
                opt("Covalent bonding"),
                opt("Magnetic attraction"),
                opt("Radioactive decay"),
            ),
            "Releasing ordered water from a nonpolar surface is strongly favourable.",
        ),
        q(
            "Induced fit and conformational selection both describe:",
            (
                opt("How protein flexibility participates in complex formation", correct=True),
                opt("How ligands are synthesised"),
                opt("How crystals are grown"),
                opt("How DNA is replicated"),
            ),
            "Both models address the role of receptor conformational change in binding.",
        ),
        q(
            "Which technique gives Kd, ΔH and stoichiometry in a single experiment?",
            (
                opt("Isothermal titration calorimetry (ITC)", correct=True),
                opt("Surface plasmon resonance"),
                opt("Mass spectrometry"),
                opt("NMR chemical shift only"),
            ),
            "ITC measures heat of titration to deliver the full thermodynamic signature.",
        ),
    ),
)
