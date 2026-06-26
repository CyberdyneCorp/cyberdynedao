"""Quiz questions for the Engineering Thermodynamics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Systems, surroundings and control volumes": (
            q(
                "What distinguishes an open system (control volume) from a closed system?",
                (
                    opt("Mass crosses the boundary in an open system", correct=True),
                    opt("Only an open system can exchange heat"),
                    opt("A closed system has no boundary"),
                    opt("An open system is always adiabatic"),
                ),
                "In an open system (control volume) both mass and energy cross the boundary; a closed system exchanges energy only.",
            ),
            q(
                "A boundary that blocks heat transfer is called what?",
                (
                    opt("Diathermal"),
                    opt("Adiabatic", correct=True),
                    opt("Isobaric"),
                    opt("Isolated"),
                ),
                "An adiabatic boundary blocks heat; a diathermal one allows it.",
            ),
            q(
                "Which best describes an isolated system?",
                (
                    opt("Exchanges neither mass nor energy with surroundings", correct=True),
                    opt("Exchanges energy but not mass"),
                    opt("Exchanges mass but not energy"),
                    opt("Has a moving boundary only"),
                ),
                "An isolated system exchanges neither mass nor energy across its boundary.",
            ),
        ),
        "Properties, state and the ideal gas": (
            q(
                "According to the state postulate, how many independent intensive properties fix the state of a simple compressible substance?",
                (
                    opt("One"),
                    opt("Two", correct=True),
                    opt("Three"),
                    opt("It depends on the mass"),
                ),
                "The state postulate fixes the state with two independent intensive properties.",
            ),
            q(
                "Which is an intensive property?",
                (
                    opt("Total volume V"),
                    opt("Total internal energy U"),
                    opt("Pressure p", correct=True),
                    opt("Total entropy S"),
                ),
                "Intensive properties (p, T, v) do not depend on system size; V, U, S are extensive.",
            ),
            q(
                "The specific gas constant R in pv = RT is obtained how?",
                (
                    opt("R = Ru / M, universal constant divided by molar mass", correct=True),
                    opt("R = Ru times M"),
                    opt("R is the same 8.314 for every gas"),
                    opt("R = cp + cv"),
                ),
                "R = Ru/M; for air this gives about 287 J/kg.K.",
            ),
        ),
        "Temperature and the zeroth law": (
            q(
                "What does the zeroth law of thermodynamics establish?",
                (
                    opt("Energy is conserved"),
                    opt(
                        "Two bodies each in thermal equilibrium with a third are in equilibrium with each other",
                        correct=True,
                    ),
                    opt("Entropy of an isolated system never decreases"),
                    opt("Absolute zero cannot be reached"),
                ),
                "The zeroth law underpins thermometry: equilibrium is transitive through a third body.",
            ),
            q(
                "Why must thermodynamic relations use the Kelvin scale?",
                (
                    opt("It is an absolute scale starting at absolute zero", correct=True),
                    opt("It uses smaller degree increments than Celsius"),
                    opt("It is the SI unit only by convention"),
                    opt("Celsius cannot measure cold temperatures"),
                ),
                "Relations like the ideal gas law and Carnot efficiency require absolute (Kelvin) temperature.",
            ),
            q(
                "A constant-volume gas thermometer extrapolates pressure to zero to define what?",
                (
                    opt("The triple point of water"),
                    opt("Absolute zero (0 K)", correct=True),
                    opt("The boiling point of the gas"),
                    opt("The critical temperature"),
                ),
                "Pressure extrapolated to zero defines absolute zero, about -273.15 C.",
            ),
        ),
        "Work: the boundary integral": (
            q(
                "On a p-V diagram, the boundary work of a process equals what?",
                (
                    opt("The area under the process curve", correct=True),
                    opt("The slope of the curve"),
                    opt("The vertical distance between endpoints"),
                    opt("Zero for any closed path"),
                ),
                "Boundary work W = integral of p dV is the area under the path on a p-V diagram.",
            ),
            q(
                "Why is work written as an inexact differential (delta W) rather than dW?",
                (
                    opt("Work is a path function, not a property", correct=True),
                    opt("Work has no units"),
                    opt("Work is always negative"),
                    opt("Work equals heat"),
                ),
                "Work depends on the path between states, so it is not an exact differential of a property.",
            ),
            q(
                "For an isothermal ideal-gas expansion, the boundary work is:",
                (
                    opt("W = mRT ln(V2/V1)", correct=True),
                    opt("W = p(V2 - V1)"),
                    opt("W = m cv (T2 - T1)"),
                    opt("W = 0"),
                ),
                "Isothermal ideal-gas work is W = mRT ln(V2/V1).",
            ),
        ),
        "Heat and the first law for closed systems": (
            q(
                "The first law for a closed system is written as:",
                (
                    opt("Q - W = dU", correct=True),
                    opt("Q + W = 0"),
                    opt("Q = W always"),
                    opt("dU = 0 for every process"),
                ),
                "Heat in minus work out equals the change in internal energy: Q - W = dU.",
            ),
            q(
                "Mayer's relation for an ideal gas states that:",
                (
                    opt("cp - cv = R", correct=True),
                    opt("cp + cv = R"),
                    opt("cp = cv"),
                    opt("cp / cv = R"),
                ),
                "Mayer's relation: cp - cv = R; their ratio is gamma.",
            ),
            q(
                "For an ideal gas, internal energy U depends on which property alone?",
                (
                    opt("Temperature", correct=True),
                    opt("Pressure"),
                    opt("Specific volume"),
                    opt("Entropy"),
                ),
                "For an ideal gas, U (and H) are functions of temperature only.",
            ),
        ),
    },
    final=(
        q(
            "Which framing tracks mass flow rate (m-dot) crossing the boundary?",
            (
                opt("Control volume (open system)", correct=True),
                opt("Control mass (closed system)"),
                opt("Isolated system"),
                opt("Adiabatic system"),
            ),
            "Open systems / control volumes have mass flow across the boundary.",
        ),
        q(
            "For air, the specific gas constant R is approximately:",
            (
                opt("287 J/kg.K", correct=True),
                opt("8.314 J/kg.K"),
                opt("1005 J/kg.K"),
                opt("1.4 J/kg.K"),
            ),
            "R_air = Ru/M = 8.314/0.029 ~ 287 J/kg.K.",
        ),
        q(
            "Both heat and work are classified as:",
            (
                opt("Path functions", correct=True),
                opt("Point (state) functions"),
                opt("Intensive properties"),
                opt("Extensive properties"),
            ),
            "Heat and work depend on the path, so they are path functions, not properties.",
        ),
        q(
            "At constant pressure, the heat added to an ideal gas equals:",
            (
                opt("The change in enthalpy, m cp dT", correct=True),
                opt("The change in internal energy, m cv dT"),
                opt("Zero"),
                opt("m R dT"),
            ),
            "Q_p = dH = m cp dT at constant pressure.",
        ),
        q(
            "The zeroth law is the basis for which instrument or concept?",
            (
                opt("The thermometer", correct=True),
                opt("The heat engine"),
                opt("The Carnot cycle"),
                opt("The entropy balance"),
            ),
            "The zeroth law licenses temperature measurement by a thermometer.",
        ),
        q(
            "The ratio of specific heats gamma = cp/cv for air is about:",
            (
                opt("1.4", correct=True),
                opt("0.7"),
                opt("287"),
                opt("1.0"),
            ),
            "For diatomic air, gamma is about 1.4.",
        ),
    ),
)
