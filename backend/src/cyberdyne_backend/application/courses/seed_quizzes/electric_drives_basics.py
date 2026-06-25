"""Curated quiz questions for the Electric Drives & Motor Control - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is an electric drive?": (
            q(
                "Which feature most distinguishes an electric drive from simply switching a motor on?",
                (
                    opt("It uses a larger motor"),
                    opt(
                        "A feedback loop where the controller measures the motor and corrects the converter output",
                        correct=True,
                    ),
                    opt("It runs directly from the AC mains with no electronics"),
                    opt("It has no sensors"),
                ),
                "A drive continuously measures the motor and corrects the converter via feedback; that loop is the defining feature.",
            ),
            q(
                "Which block is the 'brain' that compares command to feedback and commands the converter?",
                (
                    opt("The motor"),
                    opt("The power converter"),
                    opt("The controller", correct=True),
                    opt("The mechanical load"),
                ),
                "The controller compares the command to the feedback and drives the converter so the error goes to zero.",
            ),
            q(
                "What does the power converter block do in a drive?",
                (
                    opt("It measures shaft position"),
                    opt("It shapes the voltage and current fed to the motor", correct=True),
                    opt("It stores the mechanical energy of the load"),
                    opt("It generates the speed command"),
                ),
                "The power converter (rectifier plus inverter) shapes the voltage and current delivered to the motor.",
            ),
        ),
        "Motor types for drives": (
            q(
                "Which motor type uses a mechanical commutator and brushes that wear out?",
                (
                    opt("DC motor", correct=True),
                    opt("Induction motor"),
                    opt("PMSM"),
                    opt("BLDC motor"),
                ),
                "The DC motor sets torque by armature current but relies on a commutator and brushes that wear.",
            ),
            q(
                "What characterises induction-motor operation?",
                (
                    opt("The rotor turns exactly in step with the stator field"),
                    opt(
                        "The rotor runs at a slip below synchronous speed, dragged by the rotating stator field",
                        correct=True,
                    ),
                    opt("It needs magnets on the rotor"),
                    opt("It requires brushes for commutation"),
                ),
                "An induction motor's rotor runs at a slip below the synchronous speed of the rotating stator field.",
            ),
            q(
                "Which motor type gives the highest torque density and dominates servos and EV traction?",
                (
                    opt("DC motor"),
                    opt("Induction motor"),
                    opt("PMSM / BLDC", correct=True),
                    opt("Universal motor"),
                ),
                "Permanent-magnet synchronous / BLDC motors offer the highest torque density and dominate servos, robotics and EV traction.",
            ),
        ),
        "Torque-speed characteristics & load matching": (
            q(
                "Where does the steady operating point of a drive occur?",
                (
                    opt("Where motor torque is maximum"),
                    opt(
                        "Where the motor torque-speed curve crosses the load torque curve",
                        correct=True,
                    ),
                    opt("At zero speed always"),
                    opt("Where the load torque is zero"),
                ),
                "The operating point is where motor torque equals load torque, so the two curves cross and speed stops changing.",
            ),
            q(
                "How does a fan or pump load's torque vary with speed?",
                (
                    opt("It is constant with speed"),
                    opt("It rises with the square of speed", correct=True),
                    opt("It falls inversely with speed"),
                    opt("It is independent of the motor"),
                ),
                "Fan and pump loads follow a square law, with torque proportional to the square of speed.",
            ),
            q(
                "What determines the acceleration of the drive's shaft?",
                (
                    opt("The supply voltage alone"),
                    opt(
                        "The gap between motor torque and load torque, divided by inertia",
                        correct=True,
                    ),
                    opt("Only the load torque"),
                    opt("The number of poles"),
                ),
                "Acceleration follows J dω/dt = τ_motor − τ_load, so it comes from the torque gap divided by inertia.",
            ),
        ),
        "Power-electronic converters for drives": (
            q(
                "What is the role of the rectifier stage in an AC drive?",
                (
                    opt("It synthesises variable-frequency AC for the motor"),
                    opt(
                        "It converts fixed AC mains into a roughly constant DC-link voltage",
                        correct=True,
                    ),
                    opt("It measures rotor position"),
                    opt("It stores mechanical energy"),
                ),
                "The rectifier converts the fixed AC mains into a roughly constant DC-link voltage.",
            ),
            q(
                "How does the inverter control the average voltage applied to the motor?",
                (
                    opt("By adding more diodes"),
                    opt(
                        "By varying the fraction of time each switch is on (duty cycle)",
                        correct=True,
                    ),
                    opt("By changing the DC-link capacitor size in real time"),
                    opt("By rotating the rectifier"),
                ),
                "The inverter switches thousands of times per second and varies each switch's duty cycle to set the average voltage.",
            ),
            q(
                "What is the purpose of the DC-link capacitor?",
                (
                    opt("To measure current"),
                    opt(
                        "To stiffen the DC voltage and buffer energy between the two stages",
                        correct=True,
                    ),
                    opt("To commutate the motor"),
                    opt("To generate the speed reference"),
                ),
                "The DC link stiffens the DC voltage and buffers energy between the rectifier and inverter stages.",
            ),
        ),
        "Four-quadrant operation": (
            q(
                "In which quadrant does forward motoring occur?",
                (
                    opt("Speed positive, torque positive (Quadrant I)", correct=True),
                    opt("Speed positive, torque negative"),
                    opt("Speed negative, torque negative"),
                    opt("Speed negative, torque positive"),
                ),
                "Forward motoring is Quadrant I: speed and torque both positive, so power flows into the load.",
            ),
            q(
                "When torque and speed have opposite signs, what is the machine doing?",
                (
                    opt("Motoring with positive power"),
                    opt(
                        "Acting as a generator, with power flowing back toward the converter",
                        correct=True,
                    ),
                    opt("Sitting at standstill"),
                    opt("Drawing maximum current from the mains"),
                ),
                "With opposite signs power P = τω is negative, so the machine generates and energy flows back to the converter.",
            ),
            q(
                "Why can a simple diode-rectifier drive normally only motor?",
                (
                    opt("Its motor cannot reverse"),
                    opt(
                        "The diode rectifier cannot return braking energy to the mains, so there is nowhere for it to go",
                        correct=True,
                    ),
                    opt("It has no DC link"),
                    opt("It lacks a controller"),
                ),
                "A diode bridge is one-directional, so braking energy cannot return to the mains without a brake resistor or active front-end.",
            ),
        ),
        "Basic speed & torque control concepts": (
            q(
                "What is the error signal in a closed-loop speed controller?",
                (
                    opt("The measured speed times the reference"),
                    opt("Reference speed minus measured speed", correct=True),
                    opt("The DC-link voltage minus the reference"),
                    opt("The torque minus the current"),
                ),
                "The error is reference minus measured speed; the controller acts to drive it to zero.",
            ),
            q(
                "Why is the torque (current) loop placed inside the speed loop?",
                (
                    opt("Because torque responds faster than speed"),
                    opt("Because torque is slower than speed"),
                    opt("Because the speed loop protects the switches"),
                    opt("Because the inverter requires it physically"),
                ),
                "Torque responds faster than speed, so the fast torque/current loop is nested inside the slower speed loop.",
                # keep order: correct is first option
            ),
            q(
                "What does increasing the PI controller gain too far tend to cause?",
                (
                    opt("A perfectly smooth, infinitely fast response"),
                    opt("Ringing, overshoot or even instability", correct=True),
                    opt("Lower current draw"),
                    opt("Reduced torque density"),
                ),
                "Too much gain makes the loop ring or go unstable; too little makes it sluggish.",
            ),
        ),
    },
    final=(
        q(
            "Which four blocks make up an electric drive?",
            (
                opt("Battery, gearbox, clutch and brake"),
                opt("Power converter, motor, sensors/feedback and controller", correct=True),
                opt("Rectifier, capacitor, resistor and inductor"),
                opt("Encoder, resolver, Hall sensor and shunt"),
            ),
            "A drive comprises the power converter, the motor, the sensors/feedback and the controller.",
        ),
        q(
            "Which motor type is brushless, rugged and runs at a slip below synchronous speed?",
            (
                opt("DC motor"),
                opt("Induction motor", correct=True),
                opt("PMSM"),
                opt("Stepper motor"),
            ),
            "The induction motor is brushless and rugged and runs at a slip below the synchronous speed of the stator field.",
        ),
        q(
            "At the steady operating point of a drive, what is true?",
            (
                opt("Motor torque is zero"),
                opt("Motor torque equals load torque and the speed stops changing", correct=True),
                opt("Speed is always maximum"),
                opt("The inverter is switched off"),
            ),
            "At the operating point motor torque equals load torque, so the net torque is zero and speed is steady.",
        ),
        q(
            "What two stages of an AC drive surround the DC link?",
            (
                opt("Two inverters"),
                opt("A rectifier (AC to DC) and an inverter (DC to variable AC)", correct=True),
                opt("Two rectifiers"),
                opt("A gearbox and a clutch"),
            ),
            "An AC drive uses a rectifier to make the DC link and an inverter to synthesise variable AC for the motor.",
        ),
        q(
            "How is electrical power related to torque and speed?",
            (
                opt("P = τ / ω"),
                opt(
                    "P = τ ω, so opposite signs mean negative power (braking/regeneration)",
                    correct=True,
                ),
                opt("P = τ + ω"),
                opt("Power is independent of torque"),
            ),
            "Power is the product P = τω; opposite signs of torque and speed give negative power, i.e. braking or regeneration.",
        ),
        q(
            "Why do high-performance drives nest a torque (current) loop inside a speed loop?",
            (
                opt("Because speed responds faster than torque"),
                opt(
                    "Because torque responds faster than speed, so the fast loop goes inside the slow one",
                    correct=True,
                ),
                opt("Because the inverter cannot measure speed"),
                opt("To eliminate the need for a controller"),
            ),
            "Torque responds faster than speed, so the cascaded structure puts the fast current/torque loop inside the slower speed loop.",
        ),
    ),
)
