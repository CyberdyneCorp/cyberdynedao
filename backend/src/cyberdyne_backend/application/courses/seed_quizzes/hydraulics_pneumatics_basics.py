"""Quiz questions for the Hydraulics & Pneumatics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is fluid power? Pascal's law": (
            q(
                "Pascal's law states that pressure applied to a confined fluid:",
                (
                    opt("acts equally in all directions and transmits undiminished", correct=True),
                    opt("acts only in the direction of the applied force"),
                    opt("decreases with distance from the piston"),
                    opt("is proportional to the fluid temperature"),
                ),
                "Pressure in a confined fluid is transmitted equally and undiminished in all directions.",
            ),
            q(
                "In a hydraulic press, a small input force gives a large output force because:",
                (
                    opt("the output piston has a larger area at the same pressure", correct=True),
                    opt("the fluid amplifies energy"),
                    opt("pressure is higher on the large piston"),
                    opt("the small piston moves slower"),
                ),
                "Equal pressure on a larger area means F2 = F1 * (A2/A1).",
            ),
            q(
                "The force multiplication of a hydraulic jack is paid for by:",
                (
                    opt("a shorter stroke at the large piston", correct=True),
                    opt("a loss of total pressure"),
                    opt("heating of the fluid"),
                    opt("an increase in fluid density"),
                ),
                "Volume is conserved, so the large piston moves less - work is conserved.",
            ),
        ),
        "Pressure and flow: the two currencies": (
            q(
                "In a fluid-power circuit, actuator force is set by pressure and speed by:",
                (
                    opt("flow rate", correct=True),
                    opt("fluid density"),
                    opt("pipe diameter only"),
                    opt("temperature"),
                ),
                "Force F = p A; speed v = Q / A, so flow sets speed.",
            ),
            q(
                "Which statement about pumps is correct?",
                (
                    opt(
                        "Pumps create flow; pressure rises only when flow meets resistance",
                        correct=True,
                    ),
                    opt("Pumps create pressure directly"),
                    opt("Pumps create both flow and pressure independently"),
                    opt("Pumps reduce the flow they receive"),
                ),
                "A pump delivers flow; pressure builds when that flow is resisted by a load.",
            ),
            q(
                "Hydraulic power delivered to a load equals:",
                (
                    opt("pressure times flow rate", correct=True),
                    opt("pressure divided by flow rate"),
                    opt("pressure plus flow rate"),
                    opt("flow rate squared"),
                ),
                "P = p Q (watts in SI).",
            ),
        ),
        "Components of a hydraulic system": (
            q(
                "Which component is the essential safety device in a hydraulic system?",
                (
                    opt("the relief valve", correct=True),
                    opt("the reservoir"),
                    opt("the cooler"),
                    opt("the directional valve"),
                ),
                "The relief valve caps system pressure so a dead-headed pump cannot spike to failure.",
            ),
            q(
                "Besides storing oil, the reservoir also:",
                (
                    opt("de-aerates, settles contaminants and dissipates heat", correct=True),
                    opt("generates the system pressure"),
                    opt("meters the actuator flow"),
                    opt("multiplies the pump torque"),
                ),
                "The tank de-aerates, lets dirt settle and rejects heat.",
            ),
            q(
                "The energy chain of a hydraulic system converts power as:",
                (
                    opt("mechanical -> fluid (pump) -> mechanical (actuator)", correct=True),
                    opt("electrical -> chemical -> mechanical"),
                    opt("fluid -> electrical -> fluid"),
                    opt("thermal -> fluid -> thermal"),
                ),
                "A pump turns shaft power into fluid power; the actuator turns it back to motion.",
            ),
        ),
        "Pneumatics fundamentals: compressed air": (
            q(
                "The defining difference of pneumatics versus hydraulics is that air is:",
                (
                    opt("highly compressible, giving a springy response", correct=True),
                    opt("incompressible and very stiff"),
                    opt("denser than oil"),
                    opt("unable to transmit pressure"),
                ),
                "Air compressibility makes pneumatic actuators behave like stiff springs.",
            ),
            q(
                "What does an FRL unit do in a pneumatic system?",
                (
                    opt("filters, regulates and lubricates the air", correct=True),
                    opt("flushes, refills and levels the reservoir"),
                    opt("rectifies and limits the current"),
                    opt("filters, recovers and liquefies the air"),
                ),
                "FRL = Filter, Regulator, Lubricator - the air preparation unit.",
            ),
            q(
                "Typical pneumatic working pressure is around:",
                (
                    opt("6 to 8 bar", correct=True),
                    opt("60 to 80 bar"),
                    opt("200 to 350 bar"),
                    opt("0.5 to 1 bar"),
                ),
                "Pneumatics works at roughly 6-8 bar, far below hydraulics.",
            ),
        ),
        "Reading ISO 1219 circuit diagrams": (
            q(
                "In ISO 1219 symbols, a dashed line represents:",
                (
                    opt("a pilot or control line", correct=True),
                    opt("a working pressure line"),
                    opt("the reservoir return"),
                    opt("an electrical wire"),
                ),
                "Solid lines are working lines; dashed lines are pilot/control lines.",
            ),
            q(
                "A valve described as 4/3 has:",
                (
                    opt("4 ports and 3 positions", correct=True),
                    opt("3 ports and 4 positions"),
                    opt("4 spools and 3 springs"),
                    opt("4 bar at 3 L/min"),
                ),
                "The naming is ports/positions: 4 ports, 3 switching positions.",
            ),
            q(
                "In a pump symbol, a triangle pointing out of the circle indicates:",
                (
                    opt("a pump (flow leaving)", correct=True),
                    opt("a motor (flow entering)"),
                    opt("a relief valve"),
                    opt("a filter"),
                ),
                "Triangle out = pump; triangle in = motor.",
            ),
        ),
    },
    final=(
        q(
            "Pascal's law is the basis of which device?",
            (
                opt("the hydraulic press / jack force multiplier", correct=True),
                opt("the centrifugal compressor"),
                opt("the heat exchanger"),
                opt("the electric motor"),
            ),
            "Equal pressure over a larger area multiplies force in a hydraulic press.",
        ),
        q(
            "In a fluid-power system, flow rate primarily controls:",
            (
                opt("actuator speed", correct=True),
                opt("actuator force"),
                opt("fluid density"),
                opt("oil cleanliness"),
            ),
            "Speed v = Q/A; pressure sets force.",
        ),
        q(
            "Which device protects a hydraulic system from overpressure?",
            (
                opt("the relief valve", correct=True),
                opt("the lubricator"),
                opt("the accumulator only"),
                opt("the rod seal"),
            ),
            "The relief valve dumps excess flow to tank above its cracking pressure.",
        ),
        q(
            "Compared with hydraulics, pneumatics is best described as:",
            (
                opt("clean and fast but springy and lower force", correct=True),
                opt("higher force and perfectly stiff"),
                opt("incompressible and oil-based"),
                opt("only suitable for very high pressure"),
            ),
            "Air is compressible: clean, fast, compliant, moderate force.",
        ),
        q(
            "Hydraulic power equals:",
            (
                opt("pressure times flow", correct=True),
                opt("pressure minus flow"),
                opt("flow divided by pressure"),
                opt("pressure squared"),
            ),
            "P = p Q.",
        ),
        q(
            "A 3/2 directional valve has:",
            (
                opt("3 ports and 2 positions", correct=True),
                opt("2 ports and 3 positions"),
                opt("3 spools and 2 lands"),
                opt("3 bar and 2 L/min rating"),
            ),
            "Valve naming is ports/positions.",
        ),
    ),
)
