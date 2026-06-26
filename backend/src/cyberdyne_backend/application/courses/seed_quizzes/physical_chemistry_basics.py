"""Quiz questions for the Physical Chemistry & Thermodynamics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Systems, state functions & the first law": (
            q(
                "The first law of thermodynamics states that the change in internal energy equals:",
                (
                    opt("heat plus work, q + w", correct=True),
                    opt("heat minus work, q - w, always"),
                    opt("work alone"),
                    opt("temperature times entropy"),
                ),
                "The first law is conservation of energy: dU = q + w.",
            ),
            q(
                "Which is a state function?",
                (
                    opt("internal energy U", correct=True),
                    opt("heat q"),
                    opt("work w"),
                    opt("the path taken"),
                ),
                "U depends only on the state; heat and work are path quantities.",
            ),
            q(
                "For an ideal gas, internal energy depends only on:",
                (
                    opt("temperature", correct=True),
                    opt("pressure"),
                    opt("volume"),
                    opt("the container shape"),
                ),
                "Ideal-gas internal energy is a function of temperature alone.",
            ),
        ),
        "Enthalpy & thermochemistry": (
            q(
                "Enthalpy is defined as:",
                (
                    opt("H = U + pV", correct=True),
                    opt("H = U - TS"),
                    opt("H = q - w"),
                    opt("H = TS"),
                ),
                "Enthalpy H = U + pV accounts for expansion work at constant pressure.",
            ),
            q(
                "A reaction with a negative enthalpy change is:",
                (
                    opt("exothermic, releasing heat", correct=True),
                    opt("endothermic, absorbing heat"),
                    opt("always non-spontaneous"),
                    opt("at equilibrium by definition"),
                ),
                "Negative dH means heat is released: exothermic.",
            ),
            q(
                "Hess's law works because enthalpy is:",
                (
                    opt("a state function, so dH is path independent", correct=True),
                    opt("always negative"),
                    opt("equal to the work done"),
                    opt("proportional to entropy"),
                ),
                "Since H is a state function, reaction enthalpies add along any route.",
            ),
        ),
        "Entropy & the second law": (
            q(
                "Boltzmann's equation relates entropy to the number of microstates as:",
                (
                    opt("S = k ln W", correct=True),
                    opt("S = k W"),
                    opt("S = W / k"),
                    opt("S = k / ln W"),
                ),
                "Entropy S = k_B ln W increases with the number of accessible microstates.",
            ),
            q(
                "The second law states that for an isolated system the total entropy:",
                (
                    opt("never decreases", correct=True),
                    opt("always decreases"),
                    opt("stays exactly constant"),
                    opt("equals the enthalpy"),
                ),
                "Total entropy of the universe never decreases for a spontaneous process.",
            ),
            q(
                "Higher entropy corresponds to:",
                (
                    opt("more accessible microstates", correct=True),
                    opt("fewer microstates"),
                    opt("lower temperature always"),
                    opt("zero heat exchange"),
                ),
                "More microstates W means higher entropy.",
            ),
        ),
        "Gibbs free energy & spontaneity": (
            q(
                "The Gibbs free energy is defined as:",
                (
                    opt("G = H - TS", correct=True),
                    opt("G = U + pV"),
                    opt("G = q + w"),
                    opt("G = TS - H"),
                ),
                "G = H - TS, so dG = dH - T dS at constant T.",
            ),
            q(
                "At constant temperature and pressure, a process is spontaneous when:",
                (
                    opt("dG < 0", correct=True),
                    opt("dG > 0"),
                    opt("dG = 0"),
                    opt("dH > 0"),
                ),
                "Negative Gibbs energy change means spontaneous at constant T, p.",
            ),
            q(
                "An endothermic reaction with positive dS becomes spontaneous:",
                (
                    opt("above the temperature dH/dS", correct=True),
                    opt("only at absolute zero"),
                    opt("at any temperature"),
                    opt("never"),
                ),
                "The -T dS term wins above T = dH/dS, making dG negative.",
            ),
        ),
        "Temperature, heat capacity & the Boltzmann distribution": (
            q(
                "Temperature is best understood as a measure of:",
                (
                    opt("the average thermal energy per molecule", correct=True),
                    opt("the total amount of heat stored"),
                    opt("the entropy of the system"),
                    opt("the number of molecules"),
                ),
                "Temperature reflects average molecular energy, not total heat content.",
            ),
            q(
                "In the Boltzmann distribution, the population of a level at fixed T:",
                (
                    opt("decreases exponentially with its energy", correct=True),
                    opt("increases with its energy"),
                    opt("is independent of its energy"),
                    opt("is zero for all excited levels"),
                ),
                "Population scales as exp(-energy/kT), decaying with level energy.",
            ),
            q(
                "Larger, more complex molecules tend to have:",
                (
                    opt("larger heat capacities, with more modes to store energy", correct=True),
                    opt("zero heat capacity"),
                    opt("smaller heat capacities"),
                    opt("heat capacity independent of structure"),
                ),
                "More vibrational and rotational modes store more energy per kelvin.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about the first law is correct?",
            (
                opt("dU = q + w, energy is conserved", correct=True),
                opt("heat is always converted entirely to work"),
                opt("internal energy depends on the path"),
                opt("work is a state function"),
            ),
            "dU = q + w; U is a state function while q and w are path quantities.",
        ),
        q(
            "At constant pressure, the heat exchanged equals:",
            (
                opt("the enthalpy change dH", correct=True),
                opt("the entropy change"),
                opt("the Gibbs energy change"),
                opt("zero"),
            ),
            "q_p = dH at constant pressure.",
        ),
        q(
            "Which combination guarantees a spontaneous reaction at all temperatures?",
            (
                opt("dH < 0 and dS > 0", correct=True),
                opt("dH > 0 and dS < 0"),
                opt("dH > 0 and dS > 0"),
                opt("dH < 0 and dS < 0"),
            ),
            "With dH negative and dS positive, dG = dH - T dS is negative for all T.",
        ),
        q(
            "Entropy increases when a system moves toward a state with:",
            (
                opt("more accessible microstates", correct=True),
                opt("fewer microstates"),
                opt("lower temperature only"),
                opt("no heat exchange"),
            ),
            "S = k ln W rises with the number of microstates.",
        ),
        q(
            "Which is the correct definition of Gibbs free energy?",
            (
                opt("G = H - TS", correct=True),
                opt("G = U + pV"),
                opt("G = H + TS"),
                opt("G = TS - U"),
            ),
            "G = H - TS combines enthalpy and entropy into one spontaneity criterion.",
        ),
        q(
            "The Boltzmann factor exp(-energy/kT) describes:",
            (
                opt("the relative population of an energy level at temperature T", correct=True),
                opt("the total internal energy"),
                opt("the reaction rate constant directly"),
                opt("the heat capacity"),
            ),
            "It gives the relative population of a level in thermal equilibrium.",
        ),
    ),
)
