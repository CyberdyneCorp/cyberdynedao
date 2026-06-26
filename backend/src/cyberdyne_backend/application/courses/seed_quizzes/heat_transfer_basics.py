"""Quiz questions for the Heat Transfer - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The three modes of heat transfer": (
            q(
                "Which mode of heat transfer does NOT require a material medium?",
                (
                    opt("Radiation", correct=True),
                    opt("Conduction"),
                    opt("Convection"),
                    opt("All three need a medium"),
                ),
                "Radiation travels as electromagnetic waves and works across a vacuum.",
            ),
            q(
                "Convection differs from conduction primarily because it involves:",
                (
                    opt("bulk motion of a fluid", correct=True),
                    opt("electromagnetic waves"),
                    opt("only solids"),
                    opt("no temperature difference"),
                ),
                "Convection combines conduction at the wall with advection by a moving fluid.",
            ),
            q(
                "Heat always flows spontaneously from:",
                (
                    opt("hot to cold", correct=True),
                    opt("cold to hot"),
                    opt("high pressure to low pressure"),
                    opt("large to small bodies"),
                ),
                "The second law of thermodynamics drives heat from high to low temperature.",
            ),
        ),
        "Conduction and Fourier's law": (
            q(
                "Fourier's law states the conduction heat flux is proportional to the:",
                (
                    opt("temperature gradient", correct=True),
                    opt("absolute temperature"),
                    opt("fourth power of temperature"),
                    opt("flow velocity"),
                ),
                "q'' = -k dT/dx; flux is proportional to the temperature gradient.",
            ),
            q(
                "Why does Fourier's law carry a minus sign?",
                (
                    opt("Heat flows down the temperature gradient, toward lower T", correct=True),
                    opt("Thermal conductivity is negative"),
                    opt("Area is measured backward"),
                    opt("It corrects for radiation"),
                ),
                "The minus sign encodes that heat flows toward lower temperature.",
            ),
            q(
                "Which material has the highest thermal conductivity?",
                (
                    opt("Copper"),
                    opt("Air"),
                    opt("Water"),
                    opt("Copper among these (~400 W/m-K)", correct=True),
                ),
                "Copper conducts via free electrons at ~400 W/m-K, far above water or air.",
            ),
        ),
        "Convection and Newton's law of cooling": (
            q(
                "Newton's law of cooling is written as:",
                (
                    opt("q = h A (T_s - T_inf)", correct=True),
                    opt("q = k A dT/dx"),
                    opt("q = sigma A T^4"),
                    opt("q = m cp dT"),
                ),
                "Newton's law of cooling: q = h A (T_s - T_inf).",
            ),
            q(
                "The convection coefficient h is best described as:",
                (
                    opt("a quantity lumping fluid, flow and geometry effects", correct=True),
                    opt("a pure material property like k"),
                    opt("always constant for a given fluid"),
                    opt("independent of flow speed"),
                ),
                "Unlike k, h depends on fluid properties, flow speed and geometry.",
            ),
            q(
                "Which situation gives the largest convection coefficient?",
                (
                    opt("Boiling (phase change)", correct=True),
                    opt("Natural convection in air"),
                    opt("Still air"),
                    opt("Forced convection of a gas"),
                ),
                "Phase-change processes like boiling have the highest h values.",
            ),
        ),
        "Radiation and the Stefan-Boltzmann law": (
            q(
                "Blackbody emissive power scales with temperature as:",
                (
                    opt("T^4", correct=True),
                    opt("T"),
                    opt("T^2"),
                    opt("ln T"),
                ),
                "The Stefan-Boltzmann law gives E_b = sigma T^4.",
            ),
            q(
                "In radiation formulas the temperature must be expressed in:",
                (
                    opt("kelvin (absolute)", correct=True),
                    opt("degrees Celsius"),
                    opt("degrees Fahrenheit"),
                    opt("any unit"),
                ),
                "T^4 requires absolute temperature in kelvin.",
            ),
            q(
                "A polished metal surface stays cooler by radiation because it has:",
                (
                    opt("low emissivity", correct=True),
                    opt("high emissivity"),
                    opt("high conductivity only"),
                    opt("a large area"),
                ),
                "Low emissivity (~0.05) means it emits little radiation.",
            ),
        ),
        "Energy balance and steady-state": (
            q(
                "The general energy balance for a control volume is:",
                (
                    opt("E_in - E_out + E_gen = E_st", correct=True),
                    opt("E_in + E_out = E_gen"),
                    opt("E_st = E_gen only"),
                    opt("E_in = E_out always"),
                ),
                "Conservation of energy: inflow minus outflow plus generation equals storage rate.",
            ),
            q(
                "At steady state, the storage term E_st is:",
                (
                    opt("zero", correct=True),
                    opt("maximum"),
                    opt("equal to E_gen"),
                    opt("negative"),
                ),
                "Steady state means nothing accumulates, so E_st = 0.",
            ),
            q(
                "A surface energy balance has no:",
                (
                    opt("storage or generation term", correct=True),
                    opt("conduction term"),
                    opt("convection term"),
                    opt("temperature"),
                ),
                "A surface has no volume, so storage and generation vanish: heat in equals heat out.",
            ),
        ),
        "The plane wall and composite walls": (
            q(
                "Conduction resistance of a plane wall is:",
                (
                    opt("L/(k A)", correct=True),
                    opt("k A / L"),
                    opt("1/(h A)"),
                    opt("h A"),
                ),
                "R_cond = L/(kA); thicker or lower-k walls have higher resistance.",
            ),
            q(
                "In a series thermal circuit, the resistances:",
                (
                    opt("add", correct=True),
                    opt("combine reciprocally"),
                    opt("cancel"),
                    opt("multiply"),
                ),
                "Series resistances add, just like electrical resistors.",
            ),
            q(
                "Across layers in series, the temperature drop on each layer is proportional to its:",
                (
                    opt("thermal resistance", correct=True),
                    opt("thickness only"),
                    opt("area"),
                    opt("conductivity"),
                ),
                "The same heat rate flows through each layer, so dT is proportional to R.",
            ),
        ),
    },
    final=(
        q(
            "Which rate law governs conduction?",
            (
                opt("q'' = -k dT/dx (Fourier)", correct=True),
                opt("q = h A dT (Newton)"),
                opt("E_b = sigma T^4 (Stefan-Boltzmann)"),
                opt("pv = nRT (ideal gas)"),
            ),
            "Fourier's law is the conduction rate law.",
        ),
        q(
            "The convection coefficient h has SI units of:",
            (
                opt("W/m^2-K", correct=True),
                opt("W/m-K"),
                opt("W/m^2-K^4"),
                opt("J/kg-K"),
            ),
            "h is in W/m^2-K; k is in W/m-K; sigma is in W/m^2-K^4.",
        ),
        q(
            "Net radiation between a surface and large surroundings is proportional to:",
            (
                opt("T_s^4 - T_sur^4", correct=True),
                opt("T_s - T_sur"),
                opt("T_s^2 - T_sur^2"),
                opt("ln(T_s/T_sur)"),
            ),
            "Net radiative exchange goes as the difference of fourth powers of absolute T.",
        ),
        q(
            "Trapped air is a good insulator because gases have:",
            (
                opt("low thermal conductivity", correct=True),
                opt("high thermal conductivity"),
                opt("high emissivity"),
                opt("zero specific heat"),
            ),
            "Air conducts at ~0.026 W/m-K, far below solids, so trapped air insulates well.",
        ),
        q(
            "For a plane wall with constant k at steady state, the temperature profile is:",
            (
                opt("linear", correct=True),
                opt("parabolic"),
                opt("exponential"),
                opt("sinusoidal"),
            ),
            "Constant k and no generation give a linear steady temperature profile.",
        ),
        q(
            "In a composite wall, a thin layer of insulating foam often carries most of the temperature drop because it has the:",
            (
                opt("largest thermal resistance", correct=True),
                opt("largest area"),
                opt("highest conductivity"),
                opt("smallest thickness"),
            ),
            "Low-k foam has the highest L/(kA), so the largest dT appears across it.",
        ),
    ),
)
