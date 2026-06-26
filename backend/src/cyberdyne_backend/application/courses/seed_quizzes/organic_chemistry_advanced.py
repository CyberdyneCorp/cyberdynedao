"""Quiz questions for the Organic Chemistry - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Retrosynthetic analysis and protecting groups": (
            q(
                "In retrosynthesis, the open arrow (double-line) denotes a:",
                (
                    opt("disconnection", correct=True),
                    opt("forward reaction"),
                    opt("resonance step"),
                    opt("oxidation"),
                ),
                "The open arrow indicates a retrosynthetic disconnection into synthons.",
            ),
            q(
                "A protecting group is used to:",
                (
                    opt(
                        "temporarily mask a functional group so a reaction can occur elsewhere",
                        correct=True,
                    ),
                    opt("permanently destroy a functional group"),
                    opt("increase the molecular weight"),
                    opt("act as a catalyst"),
                ),
                "Protect, react, then deprotect; e.g. TBS silyl ethers for alcohols.",
            ),
            q(
                "Compared with a long linear route, a convergent synthesis generally gives:",
                (
                    opt("higher overall yield", correct=True),
                    opt("lower overall yield"),
                    opt("the same yield always"),
                    opt("no product"),
                ),
                "Overall yield multiplies per step (y^n); convergence shortens the longest path.",
            ),
        ),
        "Organometallic catalysis and cross-coupling": (
            q(
                "The Suzuki-Miyaura coupling joins an organohalide with which partner?",
                (
                    opt("an organoboron compound", correct=True),
                    opt("an organozinc"),
                    opt("an organotin"),
                    opt("an alkene"),
                ),
                "Suzuki couples aryl/vinyl halides with boronic acids/boronates.",
            ),
            q(
                "Order the steps of a Pd cross-coupling cycle:",
                (
                    opt("oxidative addition, transmetalation, reductive elimination", correct=True),
                    opt("reductive elimination, transmetalation, oxidative addition"),
                    opt("transmetalation, oxidative addition, reductive elimination"),
                    opt("oxidative addition, reductive elimination, transmetalation"),
                ),
                "Pd(0) oxidatively adds Ar-X, transmetalates R, then reductively eliminates Ar-R.",
            ),
            q(
                "Olefin metathesis (Grubbs catalysts) is used to:",
                (
                    opt("reshuffle carbon-carbon double bonds", correct=True),
                    opt("form C-N bonds only"),
                    opt("reduce ketones"),
                    opt("hydrogenate aromatics"),
                ),
                "Metathesis swaps alkene fragments for ring closing and cross metathesis.",
            ),
        ),
        "Pericyclic reactions and frontier orbitals": (
            q(
                "The Diels-Alder reaction is a:",
                (
                    opt("[4+2] cycloaddition", correct=True),
                    opt("[2+2] cycloaddition"),
                    opt("radical chain reaction"),
                    opt("nucleophilic substitution"),
                ),
                "A diene (4 pi) plus a dienophile (2 pi) give a cyclohexene.",
            ),
            q(
                "Pericyclic selectivity is governed by orbital symmetry, codified in the:",
                (
                    opt("Woodward-Hoffmann rules", correct=True),
                    opt("Markovnikov rule"),
                    opt("Hund rule"),
                    opt("Zaitsev rule"),
                ),
                "Woodward-Hoffmann rules use orbital symmetry (FMO theory).",
            ),
            q(
                "Diels-Alder rate increases as the HOMO-LUMO energy gap:",
                (
                    opt("decreases", correct=True),
                    opt("increases"),
                    opt("stays fixed"),
                    opt("becomes infinite"),
                ),
                "A smaller gap means stronger frontier-orbital interaction and faster reaction.",
            ),
        ),
        "Chemistry of biomolecules": (
            q(
                "At physiological pH, an amino acid predominantly exists as a:",
                (
                    opt("zwitterion", correct=True),
                    opt("neutral molecule"),
                    opt("dication"),
                    opt("dianion"),
                ),
                "The amine is protonated and the carboxyl deprotonated, giving a zwitterion.",
            ),
            q(
                "In Michaelis-Menten kinetics, Km is the substrate concentration at which:",
                (
                    opt("the rate is half of Vmax", correct=True),
                    opt("the rate equals Vmax"),
                    opt("the enzyme denatures"),
                    opt("no reaction occurs"),
                ),
                "Km is the [S] giving v = Vmax/2.",
            ),
            q(
                "Which base pairing is correct in DNA?",
                (
                    opt("A with T, G with C", correct=True),
                    opt("A with G, T with C"),
                    opt("A with C, G with T"),
                    opt("A with A, G with G"),
                ),
                "Complementary pairing: adenine-thymine and guanine-cytosine.",
            ),
        ),
        "Spectroscopy and structure determination": (
            q(
                "Which technique most directly gives a compound's molecular mass and formula?",
                (
                    opt("mass spectrometry", correct=True),
                    opt("infrared"),
                    opt("UV-Vis"),
                    opt("polarimetry"),
                ),
                "MS gives the molecular ion; high-resolution MS gives the formula.",
            ),
            q(
                "In 1H NMR, the n+1 multiplicity rule reports the number of:",
                (
                    opt("neighboring equivalent protons", correct=True),
                    opt("carbon atoms in the molecule"),
                    opt("oxygen atoms"),
                    opt("rings"),
                ),
                "Splitting into n+1 lines reveals n equivalent neighboring protons.",
            ),
            q(
                "The Beer-Lambert law states that absorbance is proportional to:",
                (
                    opt("concentration (A = epsilon * l * c)", correct=True),
                    opt("the square of concentration"),
                    opt("temperature"),
                    opt("molecular weight"),
                ),
                "A = epsilon * path length * concentration, linear in c.",
            ),
        ),
        "Computational and AI methods in organic chemistry": (
            q(
                "DFT (Density Functional Theory) is most commonly used to predict:",
                (
                    opt("geometries, transition-state energies and spectra", correct=True),
                    opt("market prices"),
                    opt("boiling points only"),
                    opt("DNA sequences"),
                ),
                "DFT computes electronic-structure properties including TS energies.",
            ),
            q(
                "SMILES is a way to represent a molecule as a:",
                (
                    opt("text string", correct=True),
                    opt("3D printed model"),
                    opt("photograph"),
                    opt("mass spectrum"),
                ),
                "SMILES encodes molecular structure as a line of text.",
            ),
            q(
                "A transformer model like the Molecular Transformer is used in organic chemistry to:",
                (
                    opt("predict reaction products and plan retrosynthesis", correct=True),
                    opt("weigh reagents on a balance"),
                    opt("distill solvents"),
                    opt("measure pH"),
                ),
                "Sequence models predict products and propose retrosynthetic routes.",
            ),
        ),
    },
    final=(
        q(
            "A good retrosynthetic disconnection should:",
            (
                opt("correspond to a known, reliable forward reaction", correct=True),
                opt("always be at the center of the molecule"),
                opt("ignore functional groups"),
                opt("maximize the number of steps"),
            ),
            "Disconnections map onto real, dependable reactions and favor convergence.",
        ),
        q(
            "The 2010 Nobel Prize in Chemistry recognized which class of reactions?",
            (
                opt("palladium-catalyzed cross-couplings", correct=True),
                opt("aldol condensations"),
                opt("Grignard additions"),
                opt("Fischer esterifications"),
            ),
            "Heck, Negishi and Suzuki shared it for Pd cross-coupling.",
        ),
        q(
            "Frontier molecular orbital theory analyzes the interaction between the:",
            (
                opt("HOMO of one reactant and the LUMO of the other", correct=True),
                opt("two LUMOs"),
                opt("nucleus and the electrons"),
                opt("solvent and the catalyst"),
            ),
            "Bonding requires phase-matched HOMO-LUMO overlap.",
        ),
        q(
            "The isoelectric point (pI) of an amino acid is the pH at which it has:",
            (
                opt("zero net charge", correct=True),
                opt("maximum positive charge"),
                opt("maximum negative charge"),
                opt("no protons at all"),
            ),
            "At pI the positive and negative charges cancel to a net zero.",
        ),
        q(
            "A strong, sharp IR band near 1700 cm-1 most likely indicates a:",
            (
                opt("C=O (carbonyl) stretch", correct=True),
                opt("C-H bend"),
                opt("O-H stretch"),
                opt("aromatic ring breathing"),
            ),
            "Carbonyl C=O stretches appear strongly near 1700 cm-1.",
        ),
        q(
            "Empirically, machine-learning prediction error tends to decrease as training-set size:",
            (
                opt("increases (a power-law scaling)", correct=True),
                opt("decreases"),
                opt("stays constant"),
                opt("reaches exactly 10 examples"),
            ),
            "More data lowers error following an approximate power law, motivating large datasets.",
        ),
    ),
)
