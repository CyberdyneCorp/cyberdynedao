"""Quiz questions for the Engineering Thermodynamics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "First law for control volumes (SFEE)": (
            q(
                "Why does enthalpy h, not internal energy u, appear in the SFEE?",
                (
                    opt(
                        "It bundles in the flow work pv done pushing fluid across the boundary",
                        correct=True,
                    ),
                    opt("Internal energy is undefined for flowing fluids"),
                    opt("Enthalpy is always larger"),
                    opt("Flow work is ignored"),
                ),
                "For open systems, flow work pv combines with u to give h = u + pv.",
            ),
            q(
                "An ideal throttling valve (no shaft work, adiabatic) satisfies which relation?",
                (
                    opt("h1 = h2 (isenthalpic)", correct=True),
                    opt("s1 = s2 (isentropic)"),
                    opt("T1 = T2 (isothermal)"),
                    opt("p1 = p2 (isobaric)"),
                ),
                "A throttle is isenthalpic: h1 = h2.",
            ),
            q(
                "For an adiabatic turbine with negligible KE/PE, the specific shaft work is:",
                (
                    opt("w_s = h1 - h2", correct=True),
                    opt("w_s = h2 - h1"),
                    opt("w_s = u1 - u2"),
                    opt("w_s = 0"),
                ),
                "Steady adiabatic turbine: w_s = h1 - h2 (work out positive).",
            ),
        ),
        "The second law and the Carnot limit": (
            q(
                "The Kelvin-Planck statement of the second law says:",
                (
                    opt(
                        "No cycle can convert heat entirely into work from a single reservoir",
                        correct=True,
                    ),
                    opt("Heat flows spontaneously from cold to hot"),
                    opt("Energy is always conserved"),
                    opt("Entropy of the universe decreases"),
                ),
                "Kelvin-Planck: some heat must be rejected; 100% conversion from one reservoir is impossible.",
            ),
            q(
                "The Carnot efficiency between reservoirs at TH and TL is:",
                (
                    opt("1 - TL/TH", correct=True),
                    opt("1 - TH/TL"),
                    opt("TL/TH"),
                    opt("TH/(TH - TL)"),
                ),
                "Reversible (Carnot) efficiency is 1 - TL/TH with absolute temperatures.",
            ),
            q(
                "Raising the source temperature TH (fixed TL) does what to the Carnot ceiling?",
                (
                    opt("Raises it", correct=True),
                    opt("Lowers it"),
                    opt("Leaves it unchanged"),
                    opt("Drives it negative"),
                ),
                "Higher TH increases 1 - TL/TH, so the efficiency ceiling rises.",
            ),
        ),
        "Entropy and isentropic processes": (
            q(
                "Entropy generation S_gen for any real process obeys:",
                (
                    opt("S_gen >= 0", correct=True),
                    opt("S_gen <= 0"),
                    opt("S_gen = 0 always"),
                    opt("S_gen can be any sign"),
                ),
                "The second law requires S_gen >= 0; it is zero only for reversible processes.",
            ),
            q(
                "A reversible adiabatic process is:",
                (
                    opt("Isentropic (constant entropy)", correct=True),
                    opt("Isenthalpic"),
                    opt("Isobaric"),
                    opt("Isothermal"),
                ),
                "Reversible (S_gen=0) plus adiabatic (Q=0) gives constant entropy.",
            ),
            q(
                "For an isentropic ideal gas, T2/T1 equals:",
                (
                    opt("(p2/p1)^((gamma-1)/gamma)", correct=True),
                    opt("(p2/p1)^gamma"),
                    opt("p2/p1"),
                    opt("(p1/p2)^gamma"),
                ),
                "Isentropic ideal-gas relation: T2/T1 = (p2/p1)^((gamma-1)/gamma).",
            ),
        ),
        "The Rankine vapour power cycle": (
            q(
                "Why does Rankine use water that changes phase rather than a gas cycle?",
                (
                    opt("Pumping liquid costs far less than compressing vapour", correct=True),
                    opt("Water cannot be heated"),
                    opt("Gases cannot drive turbines"),
                    opt("Phase change violates the first law"),
                ),
                "Pumping incompressible liquid needs little work, unlike compressing a gas.",
            ),
            q(
                "In the ideal Rankine cycle, the boiler process is:",
                (
                    opt("Isobaric heat addition", correct=True),
                    opt("Isentropic expansion"),
                    opt("Isenthalpic throttling"),
                    opt("Constant-volume heating"),
                ),
                "Heat is added at constant pressure in the boiler (2->3).",
            ),
            q(
                "Thermal efficiency of the ideal Rankine cycle can be written as:",
                (
                    opt("1 - q_out/q_in", correct=True),
                    opt("1 - q_in/q_out"),
                    opt("w_p/w_t"),
                    opt("q_in/w_net"),
                ),
                "eta = (w_t - w_p)/q_in = 1 - q_out/q_in.",
            ),
        ),
        "Improving Rankine: reheat and regeneration": (
            q(
                "The main purpose of reheat in a Rankine cycle is to:",
                (
                    opt("Keep turbine-exit steam quality high and add work", correct=True),
                    opt("Reduce boiler pressure"),
                    opt("Eliminate the condenser"),
                    opt("Make the pump unnecessary"),
                ),
                "Reheat avoids excessive moisture at turbine exit while adding output.",
            ),
            q(
                "Regeneration improves efficiency primarily by:",
                (
                    opt(
                        "Preheating feedwater, raising the mean heat-addition temperature",
                        correct=True,
                    ),
                    opt("Lowering the condenser temperature"),
                    opt("Increasing turbine exit moisture"),
                    opt("Removing the boiler"),
                ),
                "Bled steam preheats feedwater, so less external heat is added at low temperature.",
            ),
            q(
                "Adding more feedwater heaters gives:",
                (
                    opt("Diminishing efficiency returns", correct=True),
                    opt("Linearly unlimited gains"),
                    opt("No change at all"),
                    opt("Decreasing efficiency"),
                ),
                "Each extra heater helps less than the previous one - diminishing returns.",
            ),
        ),
    },
    final=(
        q(
            "For a steady adiabatic nozzle (no shaft work), the exit velocity is found from:",
            (
                opt("V2 = sqrt(V1^2 + 2(h1 - h2))", correct=True),
                opt("V2 = h1 - h2"),
                opt("V2 = sqrt(2 q)"),
                opt("V2 = V1"),
            ),
            "A nozzle converts enthalpy drop into kinetic energy.",
        ),
        q(
            "A refrigerator's reversible coefficient of performance is:",
            (
                opt("TL/(TH - TL)", correct=True),
                opt("TH/(TH - TL)"),
                opt("1 - TL/TH"),
                opt("(TH - TL)/TL"),
            ),
            "COP_ref(Carnot) = TL/(TH - TL); the heat pump version adds 1.",
        ),
        q(
            "The Clausius inequality states that for a cycle:",
            (
                opt("The cyclic integral of dQ/T is <= 0", correct=True),
                opt("The cyclic integral of dQ/T is > 0"),
                opt("dU = 0 only if reversible"),
                opt("Q = W for every cycle"),
            ),
            "Clausius inequality: closed integral of dQ/T <= 0, equality for reversible cycles.",
        ),
        q(
            "Turbine isentropic efficiency is defined as:",
            (
                opt("(h1 - h2)/(h1 - h2s)", correct=True),
                opt("(h1 - h2s)/(h1 - h2)"),
                opt("(h2 - h1)/(h2s - h1)"),
                opt("h2/h1"),
            ),
            "Actual work over ideal (isentropic) work: (h1-h2)/(h1-h2s).",
        ),
        q(
            "Which change LOWERS Rankine thermal efficiency?",
            (
                opt("Raising the condenser pressure", correct=True),
                opt("Raising the boiler pressure"),
                opt("Superheating the steam"),
                opt("Adding regeneration"),
            ),
            "Higher condenser pressure raises the heat-rejection temperature, cutting efficiency.",
        ),
        q(
            "The pump work in a Rankine cycle is approximated by:",
            (
                opt("v1 (p2 - p1)", correct=True),
                opt("cp (T2 - T1)"),
                opt("R T ln(p2/p1)"),
                opt("h3 - h4"),
            ),
            "For nearly incompressible liquid, w_p = h2 - h1 ~ v1(p2 - p1).",
        ),
    ),
)
