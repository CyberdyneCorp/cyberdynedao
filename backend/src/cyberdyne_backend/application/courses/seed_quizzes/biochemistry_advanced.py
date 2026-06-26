"""Quiz questions for the Biochemistry - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Oxidative phosphorylation and chemiosmosis": (
            q(
                "According to the chemiosmotic theory, the immediate energy store used to make ATP is:",
                (
                    opt("the proton-motive force across the inner membrane", correct=True),
                    opt("a covalent high-energy intermediate"),
                    opt("stored glycogen"),
                    opt("the membrane lipid itself"),
                ),
                "Electron transport pumps protons, and the resulting gradient (PMF) drives ATP synthase.",
            ),
            q(
                "The terminal electron acceptor of the mitochondrial electron transport chain is:",
                (
                    opt("molecular oxygen, reduced to water", correct=True),
                    opt("carbon dioxide"),
                    opt("NAD+"),
                    opt("pyruvate"),
                ),
                "Oxygen accepts the electrons at Complex IV and is reduced to water.",
            ),
            q(
                "An uncoupler such as 2,4-dinitrophenol acts by:",
                (
                    opt("dissipating the proton gradient as heat", correct=True),
                    opt("blocking electron flow at Complex I"),
                    opt("inhibiting ATP synthase directly"),
                    opt("increasing the proton-motive force"),
                ),
                "Uncouplers carry protons across the membrane, collapsing the gradient so energy is lost as heat.",
            ),
        ),
        "Metabolic integration: fed and fasted states": (
            q(
                "Insulin is released in the fed state and promotes:",
                (
                    opt("glucose uptake and glycogen/fat synthesis", correct=True),
                    opt("gluconeogenesis and lipolysis"),
                    opt("ketone-body production"),
                    opt("glycogen breakdown"),
                ),
                "Insulin drives the anabolic, fuel-storing fed state.",
            ),
            q(
                "During prolonged fasting, the brain increasingly relies on:",
                (
                    opt("ketone bodies", correct=True),
                    opt("dietary glucose"),
                    opt("free fatty acids directly"),
                    opt("muscle glycogen"),
                ),
                "Ketone bodies fuel the brain during prolonged starvation, sparing muscle protein.",
            ),
            q(
                "Gluconeogenesis is the process of:",
                (
                    opt(
                        "synthesising glucose de novo from non-carbohydrate precursors",
                        correct=True,
                    ),
                    opt("breaking glucose down to pyruvate"),
                    opt("storing glucose as glycogen"),
                    opt("oxidising fatty acids"),
                ),
                "Gluconeogenesis makes new glucose, chiefly in the liver during fasting.",
            ),
        ),
        "Allostery, signalling and regulation": (
            q(
                "Allosteric enzymes typically show kinetics that are:",
                (
                    opt("sigmoidal (cooperative)", correct=True),
                    opt("strictly hyperbolic"),
                    opt("linear at all substrate levels"),
                    opt("independent of substrate"),
                ),
                "Cooperative binding gives a sigmoidal curve, well described by the Hill equation.",
            ),
            q(
                "Reversible covalent control of enzyme activity is most commonly achieved by:",
                (
                    opt("phosphorylation by kinases and removal by phosphatases", correct=True),
                    opt("permanent proteolytic cleavage"),
                    opt("changing the amino-acid sequence"),
                    opt("altering the membrane potential"),
                ),
                "Phosphorylation/dephosphorylation rapidly switches enzymes on or off.",
            ),
            q(
                "In a GPCR-cAMP-PKA cascade, the role of cAMP is to act as a:",
                (
                    opt("second messenger that amplifies the signal", correct=True),
                    opt("structural membrane lipid"),
                    opt("genetic template"),
                    opt("terminal electron acceptor"),
                ),
                "cAMP is a second messenger; cascades amplify a small hormone signal into a large response.",
            ),
        ),
        "Molecular basis of metabolic disease": (
            q(
                "Type 2 diabetes is fundamentally characterised by:",
                (
                    opt("insulin resistance with a blunted glucose-uptake response", correct=True),
                    opt("complete absence of insulin receptors from birth"),
                    opt("overproduction of glucagon only"),
                    opt("excessive ketone clearance"),
                ),
                "Tissues respond poorly to insulin, requiring higher levels until beta-cells fail.",
            ),
            q(
                "Phenylketonuria results from a defect in the enzyme:",
                (
                    opt("phenylalanine hydroxylase", correct=True),
                    opt("hexokinase"),
                    opt("ATP synthase"),
                    opt("pyruvate dehydrogenase"),
                ),
                "Loss of phenylalanine hydroxylase lets phenylalanine accumulate to neurotoxic levels.",
            ),
            q(
                "Inborn errors of metabolism generally arise from:",
                (
                    opt("a single defective enzyme blocking a pathway step", correct=True),
                    opt("infection by a virus"),
                    opt("dietary excess alone"),
                    opt("lack of any genetic cause"),
                ),
                "A single-enzyme defect backs up substrate and starves downstream products.",
            ),
        ),
        "Structural biology and AlphaFold": (
            q(
                "Which experimental method resolves large complexes near-atomically without crystals?",
                (
                    opt("cryo-electron microscopy", correct=True),
                    opt("X-ray crystallography"),
                    opt("gel electrophoresis"),
                    opt("mass spectrometry"),
                ),
                "Cryo-EM images frozen samples and now reaches near-atomic resolution without crystallisation.",
            ),
            q(
                "AlphaFold2 predicts protein structure primarily by exploiting:",
                (
                    opt("co-evolution signals from multiple-sequence alignments", correct=True),
                    opt("the molecular weight alone"),
                    opt("random guessing of coordinates"),
                    opt("direct measurement of the protein"),
                ),
                "Correlated mutations across homologues imply spatial contacts, learned by the Evoformer.",
            ),
            q(
                "The pLDDT score reported by AlphaFold represents:",
                (
                    opt("per-residue confidence in the predicted structure", correct=True),
                    opt("the protein's melting temperature"),
                    opt("the binding free energy"),
                    opt("the number of subunits"),
                ),
                "pLDDT is a per-residue confidence estimate for the prediction.",
            ),
        ),
        "Computational methods: MD and flux analysis": (
            q(
                "Molecular dynamics simulation works by:",
                (
                    opt(
                        "integrating Newton's equations for all atoms under a force field",
                        correct=True,
                    ),
                    opt("solving the Schrodinger equation exactly for the whole protein"),
                    opt("aligning protein sequences"),
                    opt("crystallising the protein"),
                ),
                "MD numerically integrates atomic motion using a classical force field.",
            ),
            q(
                "Flux balance analysis (FBA) assumes that at steady state:",
                (
                    opt("S v = 0, no metabolite accumulates", correct=True),
                    opt("all fluxes are zero"),
                    opt("kinetic constants are known for every reaction"),
                    opt("the network has no constraints"),
                ),
                "FBA imposes mass balance (S v = 0) and optimises an objective by linear programming.",
            ),
            q(
                "A key advantage of FBA over kinetic modelling is that it:",
                (
                    opt("predicts genome-scale fluxes without kinetic parameters", correct=True),
                    opt("requires every enzyme's kcat and Km"),
                    opt("simulates atomic motion in detail"),
                    opt("needs the full 3D structure of each enzyme"),
                ),
                "FBA uses only stoichiometry and bounds, sidestepping hard-to-measure kinetic parameters.",
            ),
        ),
    },
    final=(
        q(
            "Peter Mitchell's chemiosmotic theory explains ATP synthesis through:",
            (
                opt("a proton gradient driving ATP synthase", correct=True),
                opt("direct phosphate transfer from NADH"),
                opt("substrate-level phosphorylation in the cytosol"),
                opt("hydrolysis of glycogen"),
            ),
            "Electron transport builds a proton gradient that powers the ATP synthase motor.",
        ),
        q(
            "Which hormone dominates the fasted, fuel-mobilising state?",
            (
                opt("glucagon", correct=True),
                opt("insulin"),
                opt("amylase"),
                opt("pepsin"),
            ),
            "Glucagon triggers glycogenolysis, gluconeogenesis and lipolysis during fasting.",
        ),
        q(
            "Cooperative, sigmoidal enzyme kinetics are a hallmark of:",
            (
                opt("allosteric regulation", correct=True),
                opt("simple Michaelis-Menten enzymes"),
                opt("irreversible inhibition"),
                opt("denatured proteins"),
            ),
            "Allosteric, multi-subunit enzymes show cooperative sigmoidal behaviour.",
        ),
        q(
            "HbA1c is used clinically to monitor diabetes because it reflects:",
            (
                opt("non-enzymatic glycation from chronic high glucose", correct=True),
                opt("the number of red blood cells"),
                opt("insulin gene mutations"),
                opt("ketone-body concentration"),
            ),
            "Glycated haemoglobin reports average glucose exposure over weeks.",
        ),
        q(
            "AlphaFold largely solved which long-standing problem?",
            (
                opt("predicting 3D structure from amino-acid sequence", correct=True),
                opt("sequencing entire genomes"),
                opt("measuring enzyme kinetics"),
                opt("synthesising proteins chemically"),
            ),
            "It predicts structure from sequence at near-experimental accuracy.",
        ),
        q(
            "Flux balance analysis predicts metabolic phenotypes using:",
            (
                opt(
                    "stoichiometry, steady-state constraints and an objective function",
                    correct=True,
                ),
                opt("molecular dynamics trajectories"),
                opt("multiple-sequence alignments"),
                opt("cryo-EM density maps"),
            ),
            "FBA solves S v = 0 within bounds to optimise an objective such as biomass.",
        ),
    ),
)
