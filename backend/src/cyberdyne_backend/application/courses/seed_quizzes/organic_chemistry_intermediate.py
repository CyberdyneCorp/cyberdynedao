"""Quiz questions for the Organic Chemistry - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Acids, bases and pKa": (
            q(
                "A lower pKa value means the acid is:",
                (opt("stronger", correct=True), opt("weaker"), opt("more basic"), opt("neutral")),
                "pKa = -log Ka; a smaller pKa means a larger Ka and a stronger acid.",
            ),
            q(
                "An acid-base equilibrium favors the side with the:",
                (
                    opt("weaker acid (higher pKa)", correct=True),
                    opt("stronger acid"),
                    opt("smaller molecule"),
                    opt("more polar solvent"),
                ),
                "Equilibrium lies toward the weaker acid / weaker base.",
            ),
            q(
                "Why is a carboxylic acid much more acidic than an alcohol?",
                (
                    opt("its conjugate base (carboxylate) is resonance-stabilized", correct=True),
                    opt("it has more carbon atoms"),
                    opt("alcohols cannot lose a proton"),
                    opt("it is a stronger base"),
                ),
                "Carboxylate spreads the negative charge over two oxygens by resonance.",
            ),
        ),
        "Reaction mechanisms and arrow pushing": (
            q(
                "A full-headed curved arrow represents the movement of:",
                (
                    opt("an electron pair", correct=True),
                    opt("a single electron"),
                    opt("a proton"),
                    opt("an atom"),
                ),
                "Double-barbed arrows move pairs; single-barbed arrows move single electrons (radicals).",
            ),
            q(
                "Order of carbocation stability is:",
                (
                    opt("3 degree > 2 degree > 1 degree", correct=True),
                    opt("1 degree > 2 degree > 3 degree"),
                    opt("all equal"),
                    opt("2 degree > 3 degree > 1 degree"),
                ),
                "More alkyl groups stabilize the cation via hyperconjugation and induction.",
            ),
            q(
                "In the Arrhenius equation, increasing the activation energy Ea does what to the rate?",
                (
                    opt("decreases it", correct=True),
                    opt("increases it"),
                    opt("has no effect"),
                    opt("reverses the reaction"),
                ),
                "k = A exp(-Ea/RT); higher Ea means a smaller rate constant.",
            ),
        ),
        "Substitution and elimination (SN1, SN2, E1, E2)": (
            q(
                "The SN2 reaction proceeds with:",
                (
                    opt("inversion of configuration (backside attack)", correct=True),
                    opt("retention of configuration"),
                    opt("racemization"),
                    opt("no stereochemical change ever"),
                ),
                "Backside attack in the single concerted step inverts the stereocenter.",
            ),
            q(
                "SN1 reactions are favored by which substrate?",
                (
                    opt("tertiary (3 degree)", correct=True),
                    opt("methyl"),
                    opt("primary (1 degree)"),
                    opt("none"),
                ),
                "SN1 needs a stable carbocation, best at tertiary carbons.",
            ),
            q(
                "A bulky, strong base in an elimination tends to give the:",
                (
                    opt("less substituted Hofmann alkene", correct=True),
                    opt("more substituted Zaitsev alkene"),
                    opt("substitution product"),
                    opt("carbocation only"),
                ),
                "Steric bulk steers E2 toward the less hindered (Hofmann) alkene.",
            ),
        ),
        "Addition reactions of alkenes": (
            q(
                "Markovnikov's rule predicts that in HX addition the proton adds to the carbon that:",
                (
                    opt("already has more hydrogens", correct=True),
                    opt("has more alkyl groups"),
                    opt("is more electronegative"),
                    opt("bears the halogen"),
                ),
                "H adds to give the more stable carbocation, so it goes to the more-H carbon.",
            ),
            q(
                "Hydroboration-oxidation (BH3 then H2O2/OH-) gives:",
                (
                    opt("anti-Markovnikov, syn addition of -OH", correct=True),
                    opt("Markovnikov -OH"),
                    opt("anti addition of Br"),
                    opt("a carbocation rearrangement"),
                ),
                "Boron adds to the less hindered carbon; oxidation places OH there (anti-Markovnikov, syn).",
            ),
            q(
                "Bromine (Br2) adds across an alkene with what stereochemistry?",
                (
                    opt("anti addition via a bromonium ion", correct=True),
                    opt("syn addition"),
                    opt("Markovnikov only"),
                    opt("radical-only"),
                ),
                "The cyclic bromonium ion forces anti (trans) addition.",
            ),
        ),
        "Carbonyl and aromatic chemistry": (
            q(
                "The carbonyl carbon is electrophilic because:",
                (
                    opt("the C=O bond is polarized, leaving C partially positive", correct=True),
                    opt("carbon is electron-rich"),
                    opt("oxygen donates electrons to carbon"),
                    opt("it carries a full negative charge"),
                ),
                "Oxygen is more electronegative, so carbon bears a partial positive charge.",
            ),
            q(
                "Hueckel's rule for aromaticity requires a planar conjugated ring with how many pi electrons?",
                (opt("4n+2", correct=True), opt("4n"), opt("any even number"), opt("exactly 4")),
                "Aromatic rings have 4n+2 pi electrons (e.g. benzene with 6).",
            ),
            q(
                "An -NO2 group on a benzene ring is best described as a:",
                (
                    opt("deactivating, meta-directing substituent", correct=True),
                    opt("activating, ortho/para-director"),
                    opt("non-directing group"),
                    opt("electron donor"),
                ),
                "Nitro is strongly electron-withdrawing: it deactivates and directs meta.",
            ),
        ),
        "Stereochemistry: chirality and configuration": (
            q(
                "A carbon stereocenter is a carbon bonded to:",
                (
                    opt("four different groups", correct=True),
                    opt("two identical groups"),
                    opt("only hydrogens"),
                    opt("a double bond"),
                ),
                "Four different substituents make the carbon a stereocenter.",
            ),
            q(
                "Enantiomers are stereoisomers that are:",
                (
                    opt("non-superimposable mirror images", correct=True),
                    opt("identical molecules"),
                    opt("not mirror images"),
                    opt("always achiral"),
                ),
                "Enantiomers are mirror images that cannot be superimposed.",
            ),
            q(
                "A meso compound:",
                (
                    opt(
                        "has stereocenters but an internal mirror plane, so it is achiral",
                        correct=True,
                    ),
                    opt("has no stereocenters"),
                    opt("is always optically active"),
                    opt("is a constitutional isomer"),
                ),
                "An internal mirror plane makes a stereocenter-bearing molecule achiral overall.",
            ),
        ),
    },
    final=(
        q(
            "For HA + B- giving A- + HB, the position of equilibrium is governed by comparing:",
            (
                opt("the pKa values of HA and HB", correct=True),
                opt("only the temperature"),
                opt("the molecular weights"),
                opt("the boiling points"),
            ),
            "The equilibrium favors formation of the weaker acid (higher pKa).",
        ),
        q(
            "A transition state on a reaction-energy diagram corresponds to:",
            (
                opt("an energy maximum along the path", correct=True),
                opt("a local energy minimum"),
                opt("the most stable species"),
                opt("an isolable intermediate"),
            ),
            "Transition states are maxima; intermediates sit in local minima.",
        ),
        q(
            "SN2 rate has what dependence on substrate steric bulk?",
            (
                opt("it falls sharply as bulk increases", correct=True),
                opt("it rises with bulk"),
                opt("it is independent of bulk"),
                opt("it depends only on temperature"),
            ),
            "Backside attack is blocked by bulk, so SN2 slows from methyl to tertiary.",
        ),
        q(
            "Markovnikov selectivity in electrophilic addition is controlled by:",
            (
                opt("carbocation stability", correct=True),
                opt("solvent boiling point"),
                opt("the color of the reagent"),
                opt("aromaticity"),
            ),
            "The electrophile adds to give the most stable carbocation intermediate.",
        ),
        q(
            "Electron-donating ortho/para-directors on benzene do what to the EAS rate?",
            (
                opt("increase it (activate)", correct=True),
                opt("decrease it"),
                opt("have no effect"),
                opt("prevent any reaction"),
            ),
            "Donors raise ring electron density and accelerate electrophilic aromatic substitution.",
        ),
        q(
            "Observed optical rotation of a sample is proportional to its:",
            (
                opt("enantiomeric excess", correct=True),
                opt("molecular weight"),
                opt("boiling point"),
                opt("number of carbons"),
            ),
            "A racemate (0% ee) is inactive; rotation scales linearly with ee.",
        ),
    ),
)
