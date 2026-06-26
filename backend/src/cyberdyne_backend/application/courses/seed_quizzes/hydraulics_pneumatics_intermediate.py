"""Quiz questions for the Hydraulics & Pneumatics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Pumps: types, displacement and sizing": (
            q(
                "Hydraulic systems use positive-displacement pumps because:",
                (
                    opt("they can build the high pressures required", correct=True),
                    opt("they are quieter than all alternatives"),
                    opt("they need no prime mover"),
                    opt("centrifugal pumps deliver more flow"),
                ),
                "Centrifugal pumps cannot reach the pressures hydraulics needs; positive-displacement can.",
            ),
            q(
                "A pump's ideal flow is given by:",
                (
                    opt("displacement times speed times volumetric efficiency", correct=True),
                    opt("pressure times displacement"),
                    opt("displacement divided by speed"),
                    opt("speed divided by pressure"),
                ),
                "Q = D n eta_v.",
            ),
            q(
                "Which pump type generally reaches the highest pressure and efficiency?",
                (
                    opt("piston (axial/radial) pumps", correct=True),
                    opt("gear pumps"),
                    opt("centrifugal pumps"),
                    opt("diaphragm pumps"),
                ),
                "Piston pumps reach ~400 bar with the best efficiency and offer variable displacement.",
            ),
        ),
        "Directional control valves": (
            q(
                "A directional control valve is classified by:",
                (
                    opt("its number of ports and positions", correct=True),
                    opt("its rated temperature only"),
                    opt("the fluid colour"),
                    opt("its reservoir size"),
                ),
                "DCVs are named ports/positions, e.g. 4/3.",
            ),
            q(
                "A tandem-centre 4/3 valve is useful because in centre it:",
                (
                    opt("holds the actuator while unloading the pump to tank", correct=True),
                    opt("connects all ports to the actuator"),
                    opt("forces the pump over the relief valve"),
                    opt("vents the actuator to atmosphere"),
                ),
                "Tandem centre links P to T (unload pump) while blocking A and B (hold load).",
            ),
            q(
                "Spool overlap in a directional valve produces:",
                (
                    opt("a deadband with leak-free hold at centre", correct=True),
                    opt("continuous flow at centre"),
                    opt("higher rated flow"),
                    opt("zero hysteresis"),
                ),
                "Overlap gives a deadband and leak-free centre; underlap leaks but responds faster.",
            ),
        ),
        "Pressure control and the orifice equation": (
            q(
                "The orifice equation says flow through a restriction varies with:",
                (
                    opt("the square root of the pressure drop", correct=True),
                    opt("the square of the pressure drop"),
                    opt("the pressure drop directly (linear)"),
                    opt("the inverse of the pressure drop"),
                ),
                "Q = Cd Ao sqrt(2 dp / rho): flow scales with sqrt(dp).",
            ),
            q(
                "To double the flow through a fixed orifice you must increase the pressure drop by a factor of:",
                (
                    opt("4", correct=True),
                    opt("2"),
                    opt("1.4"),
                    opt("8"),
                ),
                "Because Q ~ sqrt(dp), doubling Q needs 4x dp.",
            ),
            q(
                "Which valve sets a constant lower pressure for a sub-circuit?",
                (
                    opt("a pressure-reducing valve", correct=True),
                    opt("a relief valve"),
                    opt("a directional valve"),
                    opt("a check valve"),
                ),
                "A reducing valve holds a lower secondary pressure; a relief valve caps the maximum.",
            ),
        ),
        "Cylinders: force, speed and the differential effect": (
            q(
                "A double-acting cylinder extends with more force than it retracts because:",
                (
                    opt("the full bore area is larger than the rod-side annulus", correct=True),
                    opt("pressure is higher on extension"),
                    opt("the rod adds weight"),
                    opt("retraction uses more flow"),
                ),
                "F_ext = p A_bore > F_ret = p A_annulus since the rod reduces the annulus area.",
            ),
            q(
                "For a given flow, the rod retracts faster than it extends because:",
                (
                    opt("the rod-side annulus has a smaller volume to fill", correct=True),
                    opt("pressure rises during retraction"),
                    opt("the bore area is smaller on retraction"),
                    opt("the fluid is less viscous"),
                ),
                "v = Q/A; the smaller annulus area gives higher retraction speed.",
            ),
            q(
                "In a regenerative circuit the effective extend area becomes:",
                (
                    opt("the rod cross-section only", correct=True),
                    opt("the full bore area"),
                    opt("twice the bore area"),
                    opt("zero"),
                ),
                "Feeding rod-side oil back to the cap side leaves the rod cross-section as the net area: fast, lower force.",
            ),
        ),
        "Circuit design: meter-in, meter-out and losses": (
            q(
                "Meter-out flow control is preferred for overrunning (aiding) loads because it:",
                (
                    opt("creates back-pressure that stops the load running away", correct=True),
                    opt("uses the least energy"),
                    opt("removes all pressure drop"),
                    opt("eliminates heat generation"),
                ),
                "A meter-out restrictor on the outlet builds back-pressure to control aiding loads.",
            ),
            q(
                "A simple throttle controls speed by:",
                (
                    opt("turning the dropped pressure times flow into heat", correct=True),
                    opt("storing energy in the fluid"),
                    opt("increasing the pump efficiency"),
                    opt("reducing the system pressure to zero"),
                ),
                "The throttled dp*Q is dissipated as heat - the source of throttling loss.",
            ),
            q(
                "Which approach most reduces metering losses at partial load?",
                (
                    opt("load sensing with a variable pump", correct=True),
                    opt("a larger fixed-displacement pump"),
                    opt("a higher relief setting"),
                    opt("a smaller reservoir"),
                ),
                "Load sensing matches pump output to demand, slashing throttling loss.",
            ),
        ),
    },
    final=(
        q(
            "Pump input torque is proportional to:",
            (
                opt("displacement times pressure drop", correct=True),
                opt("flow times speed"),
                opt("pressure divided by displacement"),
                opt("volumetric efficiency only"),
            ),
            "T = D dp / (2 pi eta_m).",
        ),
        q(
            "The centre condition of a 4/3 valve that unloads the pump while holding the load is:",
            (
                opt("tandem centre", correct=True),
                opt("closed centre"),
                opt("open centre"),
                opt("float centre"),
            ),
            "Tandem connects P-T to unload the pump but blocks A and B to hold the actuator.",
        ),
        q(
            "Flow through an orifice scales with the pressure drop as:",
            (
                opt("the square root", correct=True),
                opt("the square"),
                opt("linearly"),
                opt("the cube"),
            ),
            "Q ~ sqrt(dp) from the orifice equation.",
        ),
        q(
            "On a double-acting cylinder, the extend force is greater than the retract force because:",
            (
                opt("the bore area exceeds the rod-side annular area", correct=True),
                opt("extension uses higher pressure"),
                opt("the rod increases the area"),
                opt("retraction wastes flow"),
            ),
            "The rod reduces the annulus area, so A_bore > A_annulus.",
        ),
        q(
            "Meter-in flow control is unsuitable for an overrunning load because it:",
            (
                opt("cannot stop the load running ahead of the supply", correct=True),
                opt("creates too much back-pressure"),
                opt("wastes no energy"),
                opt("only works on rotary actuators"),
            ),
            "Meter-in controls only resisting loads; an aiding load can run away.",
        ),
        q(
            "The dominant cause of efficiency loss in valve-controlled circuits is:",
            (
                opt("throttling pressure drop dissipated as heat", correct=True),
                opt("seal friction only"),
                opt("reservoir evaporation"),
                opt("pump inertia"),
            ),
            "Throttled dp*Q becomes heat; load sensing and variable pumps reduce it.",
        ),
    ),
)
