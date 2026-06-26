"""Quiz questions for the Medicinal Chemistry - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Prodrugs and soft drugs": (
            q(
                "A prodrug is:",
                (
                    opt(
                        "an inactive derivative converted in vivo to the active drug", correct=True
                    ),
                    opt("a drug that never metabolizes"),
                    opt("a placebo"),
                    opt("a drug given only intravenously"),
                ),
                "Prodrugs are activated in the body to solve a delivery problem.",
            ),
            q(
                "Esterifying a polar carboxylic acid as a prodrug commonly improves:",
                (
                    opt("membrane permeability", correct=True),
                    opt("radioactivity"),
                    opt("molecular weight only"),
                    opt("color"),
                ),
                "The neutral ester crosses membranes, then esterases unmask the acid (e.g. enalapril).",
            ),
            q(
                "A soft drug is designed to be:",
                (
                    opt("rapidly deactivated after it acts", correct=True),
                    opt("permanently bound to its target"),
                    opt("impossible to metabolize"),
                    opt("active only after years"),
                ),
                "Soft drugs include a labile group for short, controllable duration (e.g. esmolol).",
            ),
        ),
        "Fragment-based and structure-based design": (
            q(
                "Structure-based drug design relies on:",
                (
                    opt("an experimental 3D structure of the target", correct=True),
                    opt("only the drug's price"),
                    opt("random number generation alone"),
                    opt("the boiling point of water"),
                ),
                "SBDD uses X-ray, cryo-EM or NMR structures to design complementary ligands.",
            ),
            q(
                "Fragment hits typically bind:",
                (
                    opt("weakly but with high ligand efficiency", correct=True),
                    opt("with nanomolar affinity immediately"),
                    opt("covalently in every case"),
                    opt("only to lipids"),
                ),
                "Fragments bind mM-uM but efficiently per atom, then are grown into leads.",
            ),
            q(
                "The fragment 'Rule of Three' includes approximately:",
                (
                    opt("MW <= 300 and cLogP <= 3", correct=True),
                    opt("MW <= 500 and cLogP <= 5"),
                    opt("MW <= 1000 and cLogP <= 10"),
                    opt("MW <= 50 and cLogP <= 1"),
                ),
                "Fragments stay small: MW <= 300, <= 3 donors/acceptors, cLogP <= 3.",
            ),
        ),
        "Scaffolds, privileged structures and macrocycles": (
            q(
                "A privileged structure is a scaffold that:",
                (
                    opt("recurs across many drug classes binding diverse targets", correct=True),
                    opt("can never be patented"),
                    opt("contains only carbon"),
                    opt("is always toxic"),
                ),
                "Examples include benzodiazepine, indole and biphenyl cores.",
            ),
            q(
                "Rigidifying a flexible ligand into a ring tends to improve affinity by:",
                (
                    opt("paying back the entropic cost of binding", correct=True),
                    opt("increasing molecular flexibility"),
                    opt("removing all functional groups"),
                    opt("lowering molecular complementarity"),
                ),
                "Conformational restriction reduces the entropy penalty on binding.",
            ),
            q(
                "Increasing fraction sp3 (Fsp3) generally helps with:",
                (
                    opt("solubility and three-dimensionality", correct=True),
                    opt("making molecules perfectly flat"),
                    opt("removing all stereochemistry"),
                    opt("eliminating hydrogen bonds"),
                ),
                "More sp3 character ('escape from flatland') improves solubility and success rates.",
            ),
        ),
        "Covalent inhibitors and targeted protein degradation": (
            q(
                "Covalent inhibitors typically react with which residue via a mild warhead?",
                (
                    opt("a pocket cysteine", correct=True),
                    opt("a backbone carbonyl only"),
                    opt("a phosphate group"),
                    opt("a metal ion exclusively"),
                ),
                "Acrylamide and chloroacetamide warheads commonly target active-site cysteines.",
            ),
            q(
                "A PROTAC works by:",
                (
                    opt(
                        "recruiting an E3 ligase to ubiquitinate and degrade the target",
                        correct=True,
                    ),
                    opt("permanently blocking the active site"),
                    opt("dissolving the cell membrane"),
                    opt("oxidizing the target irreversibly"),
                ),
                "PROTACs form a ternary complex tagging the target for proteasomal destruction.",
            ),
            q(
                "The PROTAC 'hook effect' means that at very high concentration:",
                (
                    opt("ternary complex formation and degradation decrease", correct=True),
                    opt("degradation increases without limit"),
                    opt("the target becomes covalently bound"),
                    opt("the E3 ligase is destroyed"),
                ),
                "Saturating each end separately blocks the productive ternary complex (bell-shaped curve).",
            ),
        ),
        "Beyond small molecules: peptides, oligonucleotides and conjugates": (
            q(
                "Which strategy helps therapeutic peptides resist protease degradation?",
                (
                    opt("D-amino acids, N-methylation and stapling/cyclization", correct=True),
                    opt("adding many free thiols"),
                    opt("maximizing molecular flexibility"),
                    opt("removing all amide bonds"),
                ),
                "These modifications stabilize peptides against proteases and aid conformation.",
            ),
            q(
                "siRNA and antisense oligonucleotides act by:",
                (
                    opt("silencing a target mRNA", correct=True),
                    opt("blocking an ion channel"),
                    opt("acetylating a cysteine"),
                    opt("partitioning into membranes"),
                ),
                "Oligonucleotides target the genetic message rather than a protein pocket.",
            ),
            q(
                "An antibody-drug conjugate (ADC) combines an antibody with:",
                (
                    opt("a potent cytotoxic payload via a linker", correct=True),
                    opt("a second antibody only"),
                    opt("a sugar coating only"),
                    opt("a radio antenna"),
                ),
                "ADCs use the antibody's targeting to deliver a cytotoxic payload through a linker.",
            ),
        ),
        "Computational and AI methods in drug design": (
            q(
                "Free-energy perturbation (FEP) is used to:",
                (
                    opt(
                        "predict relative binding affinities of analogues before synthesis",
                        correct=True,
                    ),
                    opt("measure the boiling point of a solvent"),
                    opt("count the atoms in a crystal"),
                    opt("set the price of a drug"),
                ),
                "FEP ranks designs by predicted relative binding free energy to ~1 kcal/mol.",
            ),
            q(
                "How are molecules commonly encoded for cheminformatics and ML?",
                (
                    opt("as SMILES strings or molecular graphs/fingerprints", correct=True),
                    opt("as audio waveforms"),
                    opt("as JPEG images only"),
                    opt("as spreadsheet rows of prices"),
                ),
                "SMILES, graphs and fingerprints feed descriptors and machine-learning models.",
            ),
            q(
                "Generative AI methods such as REINVENT are used to:",
                (
                    opt("invent novel molecules optimized for a scoring function", correct=True),
                    opt("only store existing molecules"),
                    opt("manufacture tablets physically"),
                    opt("replace all assays permanently"),
                ),
                "Reinforcement-learning generators design new, synthesizable candidates for MPO goals.",
            ),
        ),
    },
    final=(
        q(
            "Capecitabine, activated preferentially in tumour tissue, is an example of a:",
            (
                opt("targeting prodrug", correct=True),
                opt("soft drug"),
                opt("covalent inhibitor"),
                opt("macrocycle"),
            ),
            "It is converted to 5-FU more in tumour tissue, a targeting prodrug strategy.",
        ),
        q(
            "Fragment hits are advanced to leads chiefly by:",
            (
                opt("growing, linking or merging while defending ligand efficiency", correct=True),
                opt("immediately discarding them"),
                opt("adding maximum lipophilic bulk"),
                opt("converting them to peptides"),
            ),
            "Fragments are elaborated into potent leads without ruining LE.",
        ),
        q(
            "Macrocycles are notable because they can:",
            (
                opt(
                    "address flat protein-protein interfaces in beyond-Rule-of-Five space",
                    correct=True,
                ),
                opt("only bind small enzyme active sites"),
                opt("never be orally active"),
                opt("avoid all hydrogen bonding"),
            ),
            "Large rings can engage PPIs and shield polarity via intramolecular H-bonds.",
        ),
        q(
            "Targeted protein degradation is described as event-driven because the degrader:",
            (
                opt("acts catalytically, recycling after tagging each target", correct=True),
                opt("must occupy the target continuously"),
                opt("binds covalently forever"),
                opt("works only at one fixed concentration"),
            ),
            "PROTACs release and act again, so sub-stoichiometric molecules clear the protein.",
        ),
        q(
            "GalNAc conjugation of oligonucleotides is used mainly to:",
            (
                opt("deliver them to the liver", correct=True),
                opt("make them fluorescent"),
                opt("increase their molecular charge to zero"),
                opt("convert them to peptides"),
            ),
            "GalNAc targets hepatocyte receptors for efficient liver delivery.",
        ),
        q(
            "Why does ML prediction error fall with larger training sets?",
            (
                opt("error decays roughly as 1/sqrt(N), an empirical scaling law", correct=True),
                opt("error increases with more data"),
                opt("data has no effect on error"),
                opt("models stop working above 100 examples"),
            ),
            "More high-quality bioactivity data predictably lowers model error.",
        ),
    ),
)
