"""Quiz questions for the Engineering Thermodynamics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Gas-power cycles: Otto and Diesel": (
            q(
                "The air-standard Otto cycle efficiency depends only on:",
                (
                    opt("Compression ratio r and gamma", correct=True),
                    opt("Cutoff ratio only"),
                    opt("Heat added per cycle"),
                    opt("Pressure ratio"),
                ),
                "eta_Otto = 1 - 1/r^(gamma-1).",
            ),
            q(
                "In the Diesel cycle, heat is added at constant:",
                (
                    opt("Pressure", correct=True),
                    opt("Volume"),
                    opt("Temperature"),
                    opt("Entropy"),
                ),
                "Diesel adds heat at constant pressure; Otto at constant volume.",
            ),
            q(
                "Why do diesel engines typically out-efficiency gasoline engines?",
                (
                    opt("They run at higher compression ratios", correct=True),
                    opt("They have lower compression ratios"),
                    opt("They add heat at constant volume"),
                    opt("They have no cutoff ratio"),
                ),
                "Higher r (14-22) overcomes the constant-pressure cutoff penalty.",
            ),
        ),
        "The Brayton cycle and gas turbines": (
            q(
                "Ideal Brayton thermal efficiency depends only on:",
                (
                    opt("Pressure ratio rp and gamma", correct=True),
                    opt("Compression ratio r"),
                    opt("Cutoff ratio"),
                    opt("Turbine inlet temperature alone"),
                ),
                "eta = 1 - rp^(-(gamma-1)/gamma).",
            ),
            q(
                "The back-work ratio of a gas turbine is significant because:",
                (
                    opt("The compressor consumes a large fraction of turbine work", correct=True),
                    opt("The turbine produces no work"),
                    opt("There is no compressor"),
                    opt("Heat addition is at constant volume"),
                ),
                "Gas turbines have high back-work ratios (~40-60%), so component efficiencies matter greatly.",
            ),
            q(
                "Combined-cycle plants reach the highest heat-engine efficiencies by:",
                (
                    opt("Using a Rankine bottoming cycle on the Brayton exhaust", correct=True),
                    opt("Removing the compressor"),
                    opt("Lowering turbine inlet temperature"),
                    opt("Using constant-volume combustion"),
                ),
                "A Rankine bottoming cycle recovers exhaust heat, pushing efficiency past 60%.",
            ),
        ),
        "Refrigeration and heat pump cycles": (
            q(
                "In vapour-compression refrigeration, the expansion device is modelled as:",
                (
                    opt("An isenthalpic throttle", correct=True),
                    opt("An isentropic turbine"),
                    opt("An isobaric heater"),
                    opt("A constant-volume process"),
                ),
                "The expansion valve is isenthalpic: h3 = h4.",
            ),
            q(
                "How are the refrigeration and heat-pump COPs related?",
                (
                    opt("COP_hp = COP_ref + 1", correct=True),
                    opt("COP_hp = COP_ref - 1"),
                    opt("COP_hp = COP_ref"),
                    opt("COP_hp = 1/COP_ref"),
                ),
                "The heat pump delivers QH = QL + Win, so its COP is one higher.",
            ),
            q(
                "What happens to COP as the temperature lift (TH - TL) increases?",
                (
                    opt("COP decreases", correct=True),
                    opt("COP increases"),
                    opt("COP stays constant"),
                    opt("COP becomes negative"),
                ),
                "Larger lift means more work per unit heat moved, so COP falls.",
            ),
        ),
        "Exergy analysis and the dead state": (
            q(
                "The dead state used in exergy analysis is:",
                (
                    opt("Equilibrium with the environment at T0, p0", correct=True),
                    opt("Absolute zero"),
                    opt("The critical point"),
                    opt("The triple point"),
                ),
                "Exergy is work available as a system reaches the environmental dead state (T0, p0).",
            ),
            q(
                "The Gouy-Stodola relation links exergy destruction to:",
                (
                    opt("Entropy generation: Xdest = T0 * Sgen", correct=True),
                    opt("Heat added: Xdest = Qin"),
                    opt("Work output: Xdest = Wnet"),
                    opt("Pressure ratio"),
                ),
                "Destroyed exergy equals T0 times entropy generation.",
            ),
            q(
                "Second-law (exergetic) efficiency compares performance against:",
                (
                    opt("The reversible (ideal) process", correct=True),
                    opt("Energy input only"),
                    opt("The dead state pressure"),
                    opt("The compression ratio"),
                ),
                "Exergetic efficiency benchmarks against the reversible ideal, exposing real losses.",
            ),
        ),
        "Computational cycle optimization": (
            q(
                "What does a property library like CoolProp provide in a cycle optimizer?",
                (
                    opt("Accurate fluid state properties (h, s, T, p)", correct=True),
                    opt("The optimization algorithm itself"),
                    opt("The mechanical drawings"),
                    opt("The financial model"),
                ),
                "CoolProp/REFPROP supply thermophysical properties evaluated each iteration.",
            ),
            q(
                "Why are genetic algorithms or Bayesian optimization used instead of gradient methods for some cycle designs?",
                (
                    opt("They handle non-convex, multi-objective trade-offs", correct=True),
                    opt("They are always faster"),
                    opt("They need no objective function"),
                    opt("They ignore constraints"),
                ),
                "Non-convex, multi-objective design spaces suit GA / Bayesian methods.",
            ),
            q(
                "A common role for ML surrogate models inside an optimization loop is to:",
                (
                    opt(
                        "Replace slow property or simulation calls to speed evaluation",
                        correct=True,
                    ),
                    opt("Eliminate the need for design variables"),
                    opt("Guarantee a global optimum"),
                    opt("Remove all constraints"),
                ),
                "Surrogates approximate expensive evaluations, accelerating the search.",
            ),
        ),
    },
    final=(
        q(
            "Otto efficiency at compression ratio r = 10 with gamma = 1.4 is about:",
            (
                opt("0.60", correct=True),
                opt("0.40"),
                opt("0.25"),
                opt("0.90"),
            ),
            "1 - 1/10^0.4 ~ 0.60.",
        ),
        q(
            "Spark-ignition (gasoline) compression ratio is limited mainly by:",
            (
                opt("Knock / autoignition", correct=True),
                opt("Turbine blade stress"),
                opt("Condenser pressure"),
                opt("Refrigerant GWP"),
            ),
            "Knock limits gasoline engines to roughly r = 8-11.",
        ),
        q(
            "Increasing Brayton pressure ratio beyond the optimum:",
            (
                opt("Can reduce net specific work as compressor work grows", correct=True),
                opt("Always increases net work"),
                opt("Has no effect on net work"),
                opt("Eliminates the combustor"),
            ),
            "Net specific work peaks at an optimum rp; beyond it the compressor erodes net output.",
        ),
        q(
            "Refrigerant selection (R-134a, R-1234yf, CO2) trades off COP against:",
            (
                opt("Global warming potential, flammability and pressures", correct=True),
                opt("Compression ratio only"),
                opt("The dead state temperature"),
                opt("Turbine inlet temperature"),
            ),
            "Modern refrigerant choice balances COP with GWP, safety and operating pressures.",
        ),
        q(
            "Exergy destruction in an adiabatic throttle of an ideal gas arises from:",
            (
                opt("Entropy generation due to the pressure drop", correct=True),
                opt("Heat rejection to the environment"),
                opt("Shaft work extraction"),
                opt("A temperature rise"),
            ),
            "The irreversible pressure drop generates entropy, destroying exergy (T0 Sgen).",
        ),
        q(
            "In a well-posed gradient-based cycle optimization, convergence typically looks like:",
            (
                opt("A fast, monotone decrease of the objective gap", correct=True),
                opt("Random oscillation forever"),
                opt("A linear increase"),
                opt("No change between iterations"),
            ),
            "Gradient methods on well-posed problems converge quickly and monotonically.",
        ),
    ),
)
