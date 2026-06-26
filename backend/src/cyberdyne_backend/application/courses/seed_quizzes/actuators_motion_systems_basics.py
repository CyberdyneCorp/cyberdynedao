"""Quiz questions for the Actuators & Motion Systems - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is an actuator?": (
            q(
                "What does an electric actuator convert?",
                (
                    opt("A control signal and power source into motion or force", correct=True),
                    opt("Motion into a control signal only"),
                    opt("Heat into electrical energy"),
                    opt("Light into sound"),
                ),
                "An actuator turns a command plus power into controlled mechanical motion or force.",
            ),
            q(
                "In an ideal motor, how do the torque constant kt and back-EMF constant ke compare in SI units?",
                (
                    opt("kt is always 1000 times larger"),
                    opt("They are numerically equal", correct=True),
                    opt("ke is zero"),
                    opt("They have no relationship"),
                ),
                "For an ideal machine in SI units kt (N*m/A) and ke (V*s/rad) are numerically equal.",
            ),
            q(
                "Which is NOT a standard electric actuator class?",
                (
                    opt("Brushed DC"),
                    opt("Stepper"),
                    opt("Brushless BLDC/PMSM"),
                    opt("Hydraulic ram", correct=True),
                ),
                "A hydraulic ram is a fluid-power actuator, not an electric one.",
            ),
        ),
        "The brushed DC motor": (
            q(
                "What component automatically switches current in a brushed DC motor's windings?",
                (
                    opt("An external inverter"),
                    opt("The mechanical commutator and brushes", correct=True),
                    opt("A Hall sensor"),
                    opt("The encoder"),
                ),
                "Brushes on a segmented commutator switch current so torque always pushes the rotor forward.",
            ),
            q(
                "On the torque-speed line, where does maximum torque occur?",
                (
                    opt("At no-load speed"),
                    opt("At zero speed (stall)", correct=True),
                    opt("At half of no-load speed"),
                    opt("Torque is constant at all speeds"),
                ),
                "Stall torque is the maximum and occurs at zero speed; speed is maximum at zero torque.",
            ),
            q(
                "Roughly where does a DC motor deliver maximum mechanical power?",
                (
                    opt("At stall"),
                    opt("At no-load speed"),
                    opt("At about half the no-load speed and half the stall torque", correct=True),
                    opt("Power is constant everywhere"),
                ),
                "Mechanical power peaks near half no-load speed and half stall torque on the linear curve.",
            ),
        ),
        "Servo motors and closed-loop control": (
            q(
                "What defines a servo motor?",
                (
                    opt("A unique motor winding material"),
                    opt(
                        "A feedback sensor and controller forcing the shaft to track a command",
                        correct=True,
                    ),
                    opt("That it has no controller"),
                    opt("That it can only spin one direction"),
                ),
                "A servo is any motor wrapped in a feedback loop with a sensor that closes position/velocity/torque.",
            ),
            q(
                "How are servo control loops usually organized?",
                (
                    opt("A single position loop only"),
                    opt("Cascaded position -> velocity -> current loops", correct=True),
                    opt("Current loop outside the position loop"),
                    opt("No loops at all"),
                ),
                "Cascaded loops nest a fast inner current loop inside velocity inside position.",
            ),
            q(
                "For the cascade to be stable, the inner loops must be:",
                (
                    opt("Much faster than the outer loops", correct=True),
                    opt("Much slower than the outer loops"),
                    opt("Exactly the same speed"),
                    opt("Disabled during motion"),
                ),
                "Inner loops must be markedly faster so the outer loop sees them as ideal.",
            ),
        ),
        "Stepper motors and open-loop indexing": (
            q(
                "How many full steps per revolution does a common 1.8-degree hybrid stepper have?",
                (
                    opt("50"),
                    opt("100"),
                    opt("200", correct=True),
                    opt("400"),
                ),
                "360 / 1.8 = 200 full steps per revolution.",
            ),
            q(
                "What is the dangerous failure mode of an open-loop stepper?",
                (
                    opt("Overspeeding past no-load"),
                    opt("Losing steps silently with no way to detect it", correct=True),
                    opt("Producing too much back-EMF"),
                    opt("Drawing zero current"),
                ),
                "If torque is exceeded the stepper loses steps; open loop cannot detect the position error.",
            ),
            q(
                "What does microstepping primarily improve?",
                (
                    opt("Static positioning accuracy proportionally"),
                    opt("Smoothness of motion and apparent resolution", correct=True),
                    opt("Holding torque at standstill"),
                    opt("Peak torque at high speed"),
                ),
                "Microstepping smooths motion and adds resolution but does not proportionally raise accuracy or torque.",
            ),
        ),
        "BLDC and PMSM machines": (
            q(
                "Where are the permanent magnets in a brushless motor?",
                (
                    opt("On the stator"),
                    opt("On the rotor", correct=True),
                    opt("In the inverter"),
                    opt("In the encoder"),
                ),
                "Brushless machines put magnets on the rotor and windings on the stator, commutating electronically.",
            ),
            q(
                "Which drive method gives smooth, ripple-free torque for servo-grade PMSM?",
                (
                    opt("Six-step trapezoidal commutation"),
                    opt("Sinusoidal currents with field-oriented control", correct=True),
                    opt("On/off relay switching"),
                    opt("Brushed commutation"),
                ),
                "Sinusoidal FOC produces smooth torque; trapezoidal BLDC ripples at commutation transitions.",
            ),
            q(
                "By how many electrical degrees are the three phase currents separated?",
                (
                    opt("90 degrees"),
                    opt("120 degrees", correct=True),
                    opt("180 degrees"),
                    opt("60 degrees"),
                ),
                "A balanced three-phase set is spaced 120 electrical degrees apart.",
            ),
        ),
        "Gears, lead screws and motion conversion": (
            q(
                "A gearbox of ratio N (ideal) multiplies torque by N and does what to speed?",
                (
                    opt("Multiplies speed by N"),
                    opt("Divides speed by N", correct=True),
                    opt("Leaves speed unchanged"),
                    opt("Divides speed by N squared"),
                ),
                "Torque is multiplied by N and output speed is divided by N.",
            ),
            q(
                "How does a gearbox reflect load inertia back to the motor?",
                (
                    opt("Reduced by N"),
                    opt("Reduced by N squared", correct=True),
                    opt("Increased by N squared"),
                    opt("Unchanged"),
                ),
                "Reflected load inertia scales by 1/N^2, the basis of inertia matching.",
            ),
            q(
                "For a lead screw with lead L, the linear speed for shaft speed omega is:",
                (
                    opt("v = L * omega / (2*pi)", correct=True),
                    opt("v = 2*pi*L*omega"),
                    opt("v = omega / L"),
                    opt("v = L / omega"),
                ),
                "Lead L is travel per revolution, so v = L * omega / (2*pi).",
            ),
        ),
    },
    final=(
        q(
            "Which constants relate motor torque to current and back-EMF to speed?",
            (
                opt("kt and ke", correct=True),
                opt("R and L"),
                opt("J and b"),
                opt("N and L"),
            ),
            "Torque = kt*i and back-EMF = ke*omega; these are the torque and back-EMF constants.",
        ),
        q(
            "Why does stall represent a thermal limit for a brushed DC motor?",
            (
                opt("Because back-EMF is maximum at stall"),
                opt("Because current V/R is largest and heats the windings", correct=True),
                opt("Because speed is maximum"),
                opt("Because torque is zero"),
            ),
            "At stall there is no back-EMF, so current is V/R - large enough to overheat the windings.",
        ),
        q(
            "Which actuator can be driven open-loop by counting pulses?",
            (
                opt("Brushed DC"),
                opt("Stepper", correct=True),
                opt("Sensorless induction motor"),
                opt("Hydraulic cylinder"),
            ),
            "A stepper snaps to known positions, so counting step pulses gives position without an encoder.",
        ),
        q(
            "What is the main advantage of brushless over brushed motors?",
            (
                opt("Lower cost always"),
                opt("No wearing brushes, higher efficiency and power density", correct=True),
                opt("They need no controller"),
                opt("They produce no torque ripple ever"),
            ),
            "Removing brushes improves life, efficiency and power density, which is why modern servos are brushless.",
        ),
        q(
            "A ball screw is preferred over a sliding lead screw mainly because it:",
            (
                opt("Is always self-locking"),
                opt("Reaches much higher efficiency (90%+)", correct=True),
                opt("Has zero cost"),
                opt("Cannot back-drive"),
            ),
            "Ball screws roll instead of slide, reaching 90%+ efficiency versus low-efficiency sliding screws.",
        ),
        q(
            "A servo differs from simply switching a motor on because it:",
            (
                opt("Uses a bigger motor"),
                opt("Closes a feedback loop to track a command", correct=True),
                opt("Runs straight from mains with no electronics"),
                opt("Has no sensor"),
            ),
            "The defining feature of a servo is the feedback loop driving the tracking error to zero.",
        ),
    ),
)
