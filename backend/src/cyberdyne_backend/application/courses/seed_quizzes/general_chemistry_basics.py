"""Quiz questions for the General & Inorganic Chemistry - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Atoms and the quantum model": (
            q(
                "What does the atomic number Z define?",
                (
                    opt("The number of protons, which identifies the element", correct=True),
                    opt("The number of neutrons"),
                    opt("The total number of electron shells"),
                    opt("The mass of the atom in grams"),
                ),
                "Z is the proton count; it uniquely identifies the element.",
            ),
            q(
                "Two atoms of the same element with different neutron counts are called what?",
                (
                    opt("Ions"),
                    opt("Isotopes", correct=True),
                    opt("Isomers"),
                    opt("Allotropes"),
                ),
                "Isotopes share Z but differ in neutron number, hence mass number A.",
            ),
            q(
                "According to the Pauli exclusion principle, one orbital holds at most how many electrons?",
                (
                    opt("One"),
                    opt("Two, with opposite spins", correct=True),
                    opt("Three"),
                    opt("Eight"),
                ),
                "An orbital holds two electrons with opposite spin quantum numbers.",
            ),
        ),
        "The periodic table and trends": (
            q(
                "How does atomic radius change across a period (left to right)?",
                (
                    opt("It decreases as nuclear charge pulls electrons in", correct=True),
                    opt("It increases"),
                    opt("It stays constant"),
                    opt("It first increases then disappears"),
                ),
                "Rising effective nuclear charge across a period contracts the radius.",
            ),
            q(
                "Which element has the highest electronegativity on the Pauling scale?",
                (
                    opt("Oxygen"),
                    opt("Chlorine"),
                    opt("Fluorine", correct=True),
                    opt("Francium"),
                ),
                "Fluorine is the most electronegative element at about 3.98.",
            ),
            q(
                "Why are noble gases chemically inert?",
                (
                    opt("They have very large atomic radii"),
                    opt("They have full valence shells, a stable configuration", correct=True),
                    opt("They have the highest ionisation energy possible"),
                    opt("They are all radioactive"),
                ),
                "Full valence shells give noble gases little tendency to react.",
            ),
        ),
        "Chemical bonding basics": (
            q(
                "A large electronegativity difference between two atoms tends to produce which bond?",
                (
                    opt("Nonpolar covalent"),
                    opt("Ionic", correct=True),
                    opt("Metallic"),
                    opt("Hydrogen bond"),
                ),
                "A large difference favours electron transfer and an ionic bond.",
            ),
            q(
                "VSEPR theory predicts the geometry of a molecule with four electron domains as what?",
                (
                    opt("Linear"),
                    opt("Trigonal planar"),
                    opt("Tetrahedral, about 109.5 degrees", correct=True),
                    opt("Octahedral"),
                ),
                "Four domains spread to a tetrahedron at about 109.5 degrees.",
            ),
            q(
                "As bond order increases from single to triple, the bond becomes what?",
                (
                    opt("Longer and weaker"),
                    opt("Shorter and stronger", correct=True),
                    opt("Longer and stronger"),
                    opt("Unchanged in length and strength"),
                ),
                "Higher bond order means shorter, stronger bonds.",
            ),
        ),
        "The mole and stoichiometry": (
            q(
                "How many particles are in one mole?",
                (
                    opt("About 6.022 x 10^23", correct=True),
                    opt("About 3.14 x 10^10"),
                    opt("Exactly 1000"),
                    opt("About 9.81 x 10^5"),
                ),
                "Avogadro's number is 6.022 x 10^23 per mole.",
            ),
            q(
                "In N2 + 3 H2 -> 2 NH3, how many moles of H2 react per mole of N2?",
                (
                    opt("One"),
                    opt("Two"),
                    opt("Three", correct=True),
                    opt("Six"),
                ),
                "The balanced ratio requires 3 moles of H2 per mole of N2.",
            ),
            q(
                "The limiting reagent in a reaction is the one that does what?",
                (
                    opt("Is present in the largest amount"),
                    opt("Runs out first and caps the product yield", correct=True),
                    opt("Acts as a catalyst"),
                    opt("Has the highest molar mass"),
                ),
                "The limiting reagent is consumed first and limits how much product forms.",
            ),
        ),
        "Reactions and balancing equations": (
            q(
                "When balancing an equation you may adjust which of the following?",
                (
                    opt("Coefficients in front of formulas", correct=True),
                    opt("Subscripts within formulas"),
                    opt("The identity of the elements"),
                    opt("The atomic masses"),
                ),
                "Only coefficients are changed; changing subscripts would change the substances.",
            ),
            q(
                "In a redox reaction, oxidation is defined as what?",
                (
                    opt("Gain of electrons"),
                    opt("Loss of electrons", correct=True),
                    opt("Loss of protons"),
                    opt("Gain of neutrons"),
                ),
                "Oxidation is loss of electrons (LEO), reduction is gain (GER).",
            ),
            q(
                "Balancing equations is required by which conservation law?",
                (
                    opt("Conservation of momentum"),
                    opt("Conservation of mass", correct=True),
                    opt("Conservation of charge only"),
                    opt("Conservation of volume"),
                ),
                "Equal atoms on both sides reflect conservation of mass.",
            ),
        ),
        "States of matter and gas laws": (
            q(
                "The ideal gas law is written as which expression?",
                (
                    opt("PV = nRT", correct=True),
                    opt("P = mRT"),
                    opt("PV = nR/T"),
                    opt("V = PnT"),
                ),
                "PV = nRT relates pressure, volume, moles and absolute temperature.",
            ),
            q(
                "Boyle's law states that at fixed temperature and amount, pressure and volume are related how?",
                (
                    opt("Directly proportional"),
                    opt("Inversely proportional", correct=True),
                    opt("Unrelated"),
                    opt("Equal in magnitude"),
                ),
                "At fixed n and T, P is inversely proportional to V.",
            ),
            q(
                "Which intermolecular force is strongest and explains water's high boiling point?",
                (
                    opt("London dispersion only"),
                    opt("Hydrogen bonding", correct=True),
                    opt("Ionic bonding between molecules"),
                    opt("Covalent bonding between molecules"),
                ),
                "Hydrogen bonding between water molecules raises its boiling point.",
            ),
        ),
    },
    final=(
        q(
            "Which quantum number sets the shell and primary energy of an electron?",
            (
                opt("The principal quantum number n", correct=True),
                opt("The spin quantum number m_s"),
                opt("The magnetic quantum number m_l"),
                opt("The azimuthal number l alone"),
            ),
            "n sets the shell and the dominant energy level.",
        ),
        q(
            "Ionisation energy generally does what across a period?",
            (
                opt("Increases", correct=True),
                opt("Decreases"),
                opt("Stays constant"),
                opt("Drops to zero"),
            ),
            "Greater effective nuclear charge across a period raises ionisation energy.",
        ),
        q(
            "Water is a bent molecule with a bond angle near what value?",
            (
                opt("180 degrees"),
                opt("120 degrees"),
                opt("104.5 degrees", correct=True),
                opt("90 degrees"),
            ),
            "Lone-pair repulsion compresses water's angle to about 104.5 degrees.",
        ),
        q(
            "Molarity is defined as which ratio?",
            (
                opt("Moles of solute per litre of solution", correct=True),
                opt("Grams of solute per litre"),
                opt("Moles per kilogram of solvent"),
                opt("Litres per mole"),
            ),
            "Molarity c = n / V in mol per litre.",
        ),
        q(
            "Percent yield compares which two quantities?",
            (
                opt("Actual yield to theoretical yield", correct=True),
                opt("Theoretical yield to actual yield"),
                opt("Reactant mass to product mass"),
                opt("Moles to grams"),
            ),
            "Percent yield = actual / theoretical times 100 percent.",
        ),
        q(
            "Kinetic molecular theory connects temperature most directly to what?",
            (
                opt("The average kinetic energy of the particles", correct=True),
                opt("The total mass of the gas"),
                opt("The colour of the gas"),
                opt("The number of moles only"),
            ),
            "Absolute temperature is proportional to the average kinetic energy.",
        ),
    ),
)
