"""Quiz questions for the Mechatronics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is mechatronics?": (
            q(
                "Mechatronics is best described as the integration of which disciplines?",
                (
                    opt("Mechanical, electronic, control and computer engineering", correct=True),
                    opt("Only mechanical and electrical engineering"),
                    opt("Chemistry, biology and physics"),
                    opt("Software engineering alone"),
                ),
                "Mechatronics is the synergistic integration of mechanics, electronics, control and computing.",
            ),
            q(
                "What is the defining structure of a mechatronic system?",
                (
                    opt("A closed feedback loop: sense, decide, actuate", correct=True),
                    opt("A one-way open chain with no measurement"),
                    opt("A purely mechanical linkage"),
                    opt("A database with no moving parts"),
                ),
                "Sensor -> controller -> actuator -> plant -> back to sensor is the core closed loop.",
            ),
            q(
                "A key advantage of the mechatronic approach over a purely mechanical one is?",
                (
                    opt(
                        "Complexity moves into software, lowering cost and adding flexibility",
                        correct=True,
                    ),
                    opt("It removes the need for any sensors"),
                    opt("It always uses less software"),
                    opt("It requires no control theory"),
                ),
                "Software can compensate for imperfect hardware and be updated without new parts.",
            ),
        ),
        "The four domains and the V-model": (
            q(
                "The V-model (VDI 2206) organises mechatronic development how?",
                (
                    opt(
                        "Decompose requirements down the left arm, integrate and verify up the right arm",
                        correct=True,
                    ),
                    opt("Build all hardware first, then add software"),
                    opt("Skip system design and start coding"),
                    opt("Test only at the very end with no plan"),
                ),
                "The left arm decomposes to domain design, the bottom implements, the right arm integrates and verifies.",
            ),
            q(
                "Why is a motor mount considered a cross-domain concern?",
                (
                    opt(
                        "Its mechanical stiffness sets a resonance the controller must handle",
                        correct=True,
                    ),
                    opt("It is purely an electrical component"),
                    opt("It has nothing to do with control"),
                    opt("It is only relevant to software"),
                ),
                "Mechanical design choices directly constrain the control design - they intersect.",
            ),
            q(
                "The main lesson of the V-model is that integration should be?",
                (
                    opt(
                        "Designed in from the start via agreed interfaces and budgets", correct=True
                    ),
                    opt("Bolted on at the end"),
                    opt("Avoided entirely"),
                    opt("Handled only by the mechanical team"),
                ),
                "Interfaces, signal ranges and timing are agreed in system design so domains integrate cleanly.",
            ),
        ),
        "Signals: analog, digital and sampling": (
            q(
                "The Nyquist-Shannon theorem requires a sampling rate fs that is?",
                (
                    opt("Greater than twice the highest frequency in the signal", correct=True),
                    opt("Exactly equal to the signal frequency"),
                    opt("Half the highest frequency"),
                    opt("Independent of signal bandwidth"),
                ),
                "You must sample faster than 2*f_max to reconstruct the signal.",
            ),
            q(
                "Aliasing occurs when?",
                (
                    opt(
                        "A signal is sampled too slowly and high frequencies appear as low ones",
                        correct=True,
                    ),
                    opt("The ADC has too many bits"),
                    opt("The signal is perfectly band-limited"),
                    opt("An anti-aliasing filter is used"),
                ),
                "Under-sampling folds high frequencies into low ones; an anti-aliasing filter prevents it.",
            ),
            q(
                "For an N-bit ADC over full-scale range Vfs, the quantisation step q is?",
                (
                    opt("Vfs / 2^N", correct=True),
                    opt("Vfs * 2^N"),
                    opt("2^N / Vfs"),
                    opt("N / Vfs"),
                ),
                "Each LSB spans q = Vfs / 2^N volts.",
            ),
        ),
        "Sensors: turning physics into voltage": (
            q(
                "A sensor's sensitivity is?",
                (
                    opt(
                        "The output change per unit input - the slope of its response", correct=True
                    ),
                    opt("The largest input it can measure"),
                    opt("Its smallest detectable change"),
                    opt("The time it takes to respond"),
                ),
                "Sensitivity S is output per unit measurand; range and resolution are separate specs.",
            ),
            q(
                "A strain gauge produces a signal because?",
                (
                    opt("Its resistance changes with strain, dR/R = GF * strain", correct=True),
                    opt("It generates a voltage from temperature only"),
                    opt("It emits light under load"),
                    opt("Its capacitance is fixed"),
                ),
                "Gauge factor GF (about 2) relates fractional resistance change to strain.",
            ),
            q(
                "A linear calibration y = S x + b is found by?",
                (
                    opt("Least-squares fitting measured output-versus-input points", correct=True),
                    opt("Guessing the offset"),
                    opt("Ignoring the offset entirely"),
                    opt("Measuring a single point only"),
                ),
                "Fitting a line to calibration data gives sensitivity S and offset b.",
            ),
        ),
        "Actuators: moving the world": (
            q(
                "In a DC motor, the produced torque is?",
                (
                    opt("Proportional to armature current, tau = kt * i", correct=True),
                    opt("Proportional to voltage squared"),
                    opt("Independent of current"),
                    opt("Proportional to temperature"),
                ),
                "Torque is kt times current; back-EMF e = ke * omega opposes motion.",
            ),
            q(
                "A stepper motor's main advantage is?",
                (
                    opt("Open-loop positioning in fixed steps without an encoder", correct=True),
                    opt("Highest possible top speed of any motor"),
                    opt("It never loses steps under any load"),
                    opt("It requires no driver"),
                ),
                "Steppers move in discrete steps, enabling open-loop position control.",
            ),
            q(
                "A gearbox of ratio n changes output torque and speed how?",
                (
                    opt("Torque multiplied by n, speed divided by n", correct=True),
                    opt("Both torque and speed multiplied by n"),
                    opt("Torque divided by n, speed multiplied by n"),
                    opt("Neither changes"),
                ),
                "A reduction trades speed for torque: tau_out = n*tau_in, omega_out = omega_in/n.",
            ),
        ),
    },
    final=(
        q(
            "Which best captures the core idea of mechatronics?",
            (
                opt(
                    "Closed-loop integration of mechanics, electronics, control and computing",
                    correct=True,
                ),
                opt("Building bigger mechanical gears"),
                opt("Writing software with no hardware"),
                opt("Eliminating all sensors"),
            ),
            "It is the synergistic, feedback-driven integration of the four domains.",
        ),
        q(
            "To sample a signal with content up to 1 kHz without aliasing, fs must be?",
            (
                opt("More than 2 kHz", correct=True),
                opt("Exactly 1 kHz"),
                opt("500 Hz"),
                opt("Any value works"),
            ),
            "Nyquist requires fs > 2*f_max = 2 kHz.",
        ),
        q(
            "Which component converts a control signal into physical motion?",
            (
                opt("An actuator", correct=True),
                opt("A sensor"),
                opt("An ADC"),
                opt("A resistor divider"),
            ),
            "Actuators (motors, solenoids) act on the world; sensors measure it.",
        ),
        q(
            "A 12-bit ADC over 3.3 V has an LSB of approximately?",
            (
                opt("About 0.8 mV", correct=True),
                opt("About 80 mV"),
                opt("About 3.3 V"),
                opt("About 12 mV"),
            ),
            "q = 3.3 / 4096 ~= 0.806 mV.",
        ),
        q(
            "The V-model emphasises that integration and verification should be?",
            (
                opt(
                    "Planned at system design and verified against each requirement level",
                    correct=True,
                ),
                opt("Done only after everything is built"),
                opt("Skipped to save time"),
                opt("The job of one domain alone"),
            ),
            "Each right-arm step verifies a corresponding left-arm design level.",
        ),
        q(
            "Back-EMF in a DC motor does what?",
            (
                opt(
                    "Opposes the applied voltage and rises with speed (e = ke*omega)", correct=True
                ),
                opt("Adds to the applied voltage"),
                opt("Is independent of speed"),
                opt("Only appears at standstill"),
            ),
            "Back-EMF grows with speed and limits the no-load speed.",
        ),
    ),
)
