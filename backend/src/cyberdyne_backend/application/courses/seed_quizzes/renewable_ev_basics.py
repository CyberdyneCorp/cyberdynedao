"""Quiz questions for the Renewable Energy & EV Powertrains - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The energy transition & renewable overview": (
            q(
                "The energy transition refers to:",
                (
                    opt("the shift from fossil fuels to low-carbon sources", correct=True),
                    opt("using more coal"),
                    opt("removing the grid"),
                    opt("banning electricity"),
                ),
                "Decarbonizing energy supply.",
            ),
            q(
                "Variable renewables include:",
                (
                    opt("solar PV and wind", correct=True),
                    opt("coal and gas"),
                    opt("nuclear baseload only"),
                    opt("diesel"),
                ),
                "Their output depends on weather.",
            ),
            q(
                "A key challenge of variable renewables is:",
                (
                    opt("intermittency / matching supply to demand", correct=True),
                    opt("too much constancy"),
                    opt("zero output always"),
                    opt("no cost"),
                ),
                "Output varies, needing storage/flexibility.",
            ),
        ),
        "Solar PV fundamentals: the I-V & P-V curves": (
            q(
                "A PV cell's output power is maximized at the:",
                (
                    opt("maximum power point (MPP) on the I-V curve", correct=True),
                    opt("short-circuit point"),
                    opt("open-circuit point"),
                    opt("origin"),
                ),
                "MPP is the knee of the I-V curve.",
            ),
            q(
                "PV cell current is roughly proportional to:",
                (
                    opt("irradiance (sunlight intensity)", correct=True),
                    opt("wire color"),
                    opt("ambient sound"),
                    opt("grid frequency"),
                ),
                "More light -> more current.",
            ),
            q(
                "Rising cell temperature mainly:",
                (
                    opt("reduces the output voltage/efficiency", correct=True),
                    opt("increases efficiency"),
                    opt("has no effect"),
                    opt("increases current hugely"),
                ),
                "PV efficiency drops as it heats.",
            ),
        ),
        "Wind energy fundamentals: power curve & Betz limit": (
            q(
                "Wind turbine power scales with wind speed approximately as:",
                (
                    opt("the cube of wind speed", correct=True),
                    opt("linearly"),
                    opt("the square root"),
                    opt("inversely"),
                ),
                "P ~ v^3 below rated.",
            ),
            q(
                "The Betz limit caps the fraction of wind power captured at about:",
                (
                    opt("59%", correct=True),
                    opt("100%"),
                    opt("10%"),
                    opt("0%"),
                ),
                "Theoretical max ~16/27 ~ 59.3%.",
            ),
            q(
                "Above rated wind speed, turbines:",
                (
                    opt("limit/regulate power (e.g. pitch control)", correct=True),
                    opt("increase power indefinitely"),
                    opt("shut off always"),
                    opt("ignore the wind"),
                ),
                "Power is capped to protect the machine.",
            ),
        ),
        "Energy storage for renewables": (
            q(
                "Energy storage helps renewables by:",
                (
                    opt("storing surplus and supplying when output is low", correct=True),
                    opt("adding load only"),
                    opt("removing the grid"),
                    opt("fixing frequency at zero"),
                ),
                "Time-shifts intermittent generation.",
            ),
            q(
                "A battery's C-rate describes:",
                (
                    opt("charge/discharge rate relative to capacity", correct=True),
                    opt("its color"),
                    opt("its weight"),
                    opt("its voltage only"),
                ),
                "1C discharges the capacity in one hour.",
            ),
            q(
                "Round-trip efficiency is:",
                (
                    opt("energy out divided by energy in", correct=True),
                    opt("always 100%"),
                    opt("the C-rate"),
                    opt("the voltage"),
                ),
                "Accounts for storage losses.",
            ),
        ),
        "Grid connection of renewables: inverters": (
            q(
                "A grid-tied PV inverter converts:",
                (
                    opt("DC from panels to grid-synchronized AC", correct=True),
                    opt("AC to DC"),
                    opt("DC to DC only"),
                    opt("AC to AC"),
                ),
                "Inverter feeds AC to the grid.",
            ),
            q(
                "Maximum power point tracking (MPPT) is performed by:",
                (
                    opt("the inverter / charge controller", correct=True),
                    opt("the breaker"),
                    opt("the meter"),
                    opt("the paint"),
                ),
                "It keeps the array at its MPP.",
            ),
            q(
                "Grid-tied inverters must provide:",
                (
                    opt("anti-islanding protection", correct=True),
                    opt("more harmonics"),
                    opt("no protection"),
                    opt("DC to loads"),
                ),
                "Disconnect safely on grid loss.",
            ),
        ),
        "Capacity factor & LCOE intuition": (
            q(
                "Capacity factor is:",
                (
                    opt("actual energy divided by max possible energy", correct=True),
                    opt("the peak power"),
                    opt("the voltage"),
                    opt("the cost"),
                ),
                "Average output relative to nameplate.",
            ),
            q(
                "LCOE stands for:",
                (
                    opt("Levelized Cost of Energy", correct=True),
                    opt("Low Carbon Output Estimate"),
                    opt("Load Curve Of Energy"),
                    opt("Line Continuity Of Equipment"),
                ),
                "Lifetime cost per unit energy.",
            ),
            q(
                "Solar PV typically has a capacity factor of roughly:",
                (
                    opt("10-25%", correct=True),
                    opt("90-100%"),
                    opt("exactly 50% always"),
                    opt("0%"),
                ),
                "Limited by day/night and weather.",
            ),
        ),
    },
    final=(
        q(
            "The energy transition is:",
            (
                opt("shift to low-carbon sources", correct=True),
                opt("more coal"),
                opt("removing the grid"),
                opt("banning power"),
            ),
            "Decarbonization.",
        ),
        q(
            "PV power is maximized at the:",
            (
                opt("maximum power point", correct=True),
                opt("short circuit"),
                opt("open circuit"),
                opt("origin"),
            ),
            "MPP.",
        ),
        q(
            "Wind power scales as:",
            (
                opt("v^3", correct=True),
                opt("v"),
                opt("sqrt(v)"),
                opt("1/v"),
            ),
            "Cube of wind speed.",
        ),
        q(
            "Battery C-rate is:",
            (
                opt("rate relative to capacity", correct=True),
                opt("color"),
                opt("weight"),
                opt("voltage"),
            ),
            "Charge/discharge rate.",
        ),
        q(
            "A grid-tied inverter converts:",
            (
                opt("panel DC to grid AC", correct=True),
                opt("AC to DC"),
                opt("DC to DC"),
                opt("AC to AC"),
            ),
            "DC to AC.",
        ),
        q(
            "LCOE means:",
            (
                opt("Levelized Cost of Energy", correct=True),
                opt("Low Carbon Output"),
                opt("Load Curve"),
                opt("Line Continuity"),
            ),
            "Cost per unit energy.",
        ),
    ),
)
