"""Quiz questions for the General & Inorganic Chemistry - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Chemical equilibrium": (
            q(
                "At dynamic equilibrium, what is true of the forward and reverse rates?",
                (
                    opt("They are equal", correct=True),
                    opt("The forward rate is zero"),
                    opt("Both rates are zero"),
                    opt("The reverse rate is always larger"),
                ),
                "Equilibrium is dynamic: forward and reverse rates are equal.",
            ),
            q(
                "If the reaction quotient Q is less than K, the reaction will do what?",
                (
                    opt("Shift forward to make more products", correct=True),
                    opt("Shift reverse"),
                    opt("Stay exactly as is"),
                    opt("Stop completely"),
                ),
                "Q < K means too few products, so the reaction proceeds forward.",
            ),
            q(
                "By Le Chatelier's principle, compressing a gas-phase equilibrium favours which side?",
                (
                    opt("The side with more moles of gas"),
                    opt("The side with fewer moles of gas", correct=True),
                    opt("Neither side"),
                    opt("The side with heavier molecules"),
                ),
                "Higher pressure shifts toward fewer gas moles to relieve the stress.",
            ),
        ),
        "Acids, bases and pH": (
            q(
                "In the Bronsted-Lowry model, an acid is defined as what?",
                (
                    opt("A proton donor", correct=True),
                    opt("A proton acceptor"),
                    opt("An electron-pair donor"),
                    opt("A hydroxide producer only"),
                ),
                "A Bronsted-Lowry acid donates a proton (H+).",
            ),
            q(
                "A solution with pH 3 compared to pH 5 has how much higher H+ concentration?",
                (
                    opt("2 times"),
                    opt("10 times"),
                    opt("100 times", correct=True),
                    opt("1000 times"),
                ),
                "Each pH unit is a factor of 10; two units is 100 times.",
            ),
            q(
                "A buffer resists pH change most effectively near which condition?",
                (
                    opt("pH = pKa", correct=True),
                    opt("pH = 0"),
                    opt("pH = 14"),
                    opt("Where all acid is dissociated"),
                ),
                "Buffering is strongest when pH equals pKa and the conjugate ratio is balanced.",
            ),
        ),
        "Thermochemistry and enthalpy": (
            q(
                "A reaction with a negative enthalpy change is described as what?",
                (
                    opt("Endothermic"),
                    opt("Exothermic", correct=True),
                    opt("Athermic"),
                    opt("Catalytic"),
                ),
                "Negative delta H means heat is released, an exothermic reaction.",
            ),
            q(
                "Hess's law works because enthalpy is which kind of quantity?",
                (
                    opt("A path-dependent quantity"),
                    opt("A state function", correct=True),
                    opt("A rate constant"),
                    opt("An entropy term"),
                ),
                "Enthalpy is a state function, so step enthalpies sum to the overall value.",
            ),
            q(
                "Which equation determines whether a process is spontaneous?",
                (
                    opt("Delta G = Delta H - T Delta S", correct=True),
                    opt("Delta G = Delta H + T Delta S"),
                    opt("Delta G = q m c"),
                    opt("Delta G = PV"),
                ),
                "A negative Gibbs free energy delta G = delta H - T delta S means spontaneous.",
            ),
        ),
        "Chemical kinetics": (
            q(
                "Reaction orders in a rate law are determined how?",
                (
                    opt("From the balanced equation's coefficients"),
                    opt("Experimentally", correct=True),
                    opt("From the molar masses"),
                    opt("From the equilibrium constant"),
                ),
                "Orders must be found experimentally, not read off coefficients.",
            ),
            q(
                "A first-order reaction has a half-life that does what?",
                (
                    opt("Stays constant regardless of concentration", correct=True),
                    opt("Doubles each cycle"),
                    opt("Depends strongly on initial concentration"),
                    opt("Is always one second"),
                ),
                "For first order, t_1/2 = ln2 / k is independent of concentration.",
            ),
            q(
                "A catalyst speeds a reaction by doing what?",
                (
                    opt("Lowering the activation energy via a new pathway", correct=True),
                    opt("Raising the activation energy"),
                    opt("Shifting the equilibrium toward products"),
                    opt("Being consumed in the reaction"),
                ),
                "A catalyst provides a lower-Ea path and is not consumed.",
            ),
        ),
        "Electrochemistry": (
            q(
                "In an electrochemical cell, oxidation occurs at which electrode?",
                (
                    opt("The anode", correct=True),
                    opt("The cathode"),
                    opt("The salt bridge"),
                    opt("Both electrodes equally"),
                ),
                "Oxidation always occurs at the anode.",
            ),
            q(
                "A galvanic cell is characterised by a cell potential that is what?",
                (
                    opt("Positive and spontaneous", correct=True),
                    opt("Negative and nonspontaneous"),
                    opt("Always exactly zero"),
                    opt("Independent of the reaction"),
                ),
                "A positive E_cell indicates a spontaneous galvanic cell.",
            ),
            q(
                "The Nernst equation corrects cell potential for what?",
                (
                    opt("Non-standard concentrations (the quotient Q)", correct=True),
                    opt("The colour of the electrodes"),
                    opt("The mass of the wire"),
                    opt("Atmospheric pressure only"),
                ),
                "The Nernst equation adjusts E for concentrations via ln Q.",
            ),
        ),
        "Solubility and precipitation": (
            q(
                "The solubility product Ksp describes equilibrium for what?",
                (
                    opt("A sparingly soluble salt with its dissolved ions", correct=True),
                    opt("A gas dissolving in a liquid only"),
                    opt("A weak acid dissociation"),
                    opt("A catalysed reaction"),
                ),
                "Ksp is the equilibrium constant for a slightly soluble ionic solid.",
            ),
            q(
                "A precipitate forms when the ion product Q satisfies which condition?",
                (
                    opt("Q > Ksp", correct=True),
                    opt("Q < Ksp"),
                    opt("Q = 0"),
                    opt("Q equals the pH"),
                ),
                "When Q exceeds Ksp the solution is supersaturated and a solid precipitates.",
            ),
            q(
                "The common-ion effect does what to a salt's solubility?",
                (
                    opt("Decreases it", correct=True),
                    opt("Increases it"),
                    opt("Leaves it unchanged"),
                    opt("Makes it infinite"),
                ),
                "Adding a shared ion shifts equilibrium back toward the solid, lowering solubility.",
            ),
        ),
    },
    final=(
        q(
            "A large equilibrium constant K indicates a mixture that favours what?",
            (
                opt("Products", correct=True),
                opt("Reactants"),
                opt("Neither side"),
                opt("Only the solvent"),
            ),
            "A large K means products dominate at equilibrium.",
        ),
        q(
            "The Henderson-Hasselbalch equation relates pH to which ratio?",
            (
                opt("Conjugate base to acid, [A-]/[HA]", correct=True),
                opt("Acid to water"),
                opt("Hydroxide to chloride"),
                opt("Moles to volume"),
            ),
            "pH = pKa + log([A-]/[HA]).",
        ),
        q(
            "Calorimetry computes heat using which relation?",
            (
                opt("q = m c delta T", correct=True),
                opt("q = nRT"),
                opt("q = k [A]"),
                opt("q = -nFE"),
            ),
            "Heat absorbed is mass times specific heat times temperature change.",
        ),
        q(
            "The Arrhenius equation shows that rate constant k depends on temperature how?",
            (
                opt("Exponentially through exp(-Ea/RT)", correct=True),
                opt("Linearly with T"),
                opt("Inversely with T squared"),
                opt("Not at all"),
            ),
            "k = A exp(-Ea/RT) gives an exponential temperature dependence.",
        ),
        q(
            "Standard cell potential relates to free energy by which expression?",
            (
                opt("Delta G = -nFE", correct=True),
                opt("Delta G = nFE"),
                opt("Delta G = E/nF"),
                opt("Delta G = nF/E"),
            ),
            "Delta G = -nFE_cell links electrochemistry to thermodynamics.",
        ),
        q(
            "Comparing Q to Ksp lets you predict what?",
            (
                opt("Whether a precipitate will form", correct=True),
                opt("The reaction rate"),
                opt("The activation energy"),
                opt("The molar mass"),
            ),
            "Q > Ksp predicts precipitation; Q < Ksp means more can dissolve.",
        ),
    ),
)
