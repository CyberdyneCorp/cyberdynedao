"""Quiz questions for the Electric Drives & Motor Control - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Field-oriented (vector) control": (
            q(
                "Field-oriented control decouples:",
                (
                    opt("torque and flux (like a DC motor)", correct=True),
                    opt("voltage and current names"),
                    opt("two encoders"),
                    opt("nothing"),
                ),
                "FOC independently controls torque and flux currents.",
            ),
            q(
                "FOC transforms currents into the:",
                (
                    opt("rotating dq reference frame", correct=True),
                    opt("time-of-day frame"),
                    opt("frequency bins"),
                    opt("binary domain"),
                ),
                "Park/Clarke transforms to dq.",
            ),
            q(
                "Accurate FOC requires knowledge of the:",
                (
                    opt("rotor flux angle/position", correct=True),
                    opt("ambient temperature only"),
                    opt("cable length"),
                    opt("paint color"),
                ),
                "Rotor angle aligns the dq frame.",
            ),
        ),
        "Space-vector PWM": (
            q(
                "Space-vector PWM (SVPWM) improves on sinusoidal PWM by:",
                (
                    opt("better DC-bus utilization", correct=True),
                    opt("using fewer phases"),
                    opt("removing the inverter"),
                    opt("needing no switching"),
                ),
                "SVPWM extends linear modulation range ~15%.",
            ),
            q(
                "SVPWM represents the three-phase output as:",
                (
                    opt("a rotating space vector", correct=True),
                    opt("a single scalar"),
                    opt("a DC level"),
                    opt("a truth table"),
                ),
                "Voltages are a rotating vector synthesized by switching states.",
            ),
            q(
                "SVPWM selects among:",
                (
                    opt("active and zero switching vectors", correct=True),
                    opt("analog dials"),
                    opt("resistor taps"),
                    opt("encoder counts"),
                ),
                "Combines inverter switching states.",
            ),
        ),
        "Direct torque control (DTC)": (
            q(
                "DTC directly controls torque and flux using:",
                (
                    opt("hysteresis comparators and a switching table", correct=True),
                    opt("a slow PI only"),
                    opt("an encoder always"),
                    opt("no feedback"),
                ),
                "DTC uses bang-bang control on torque/flux.",
            ),
            q(
                "Compared with FOC, DTC offers:",
                (
                    opt("fast torque response, simpler transforms", correct=True),
                    opt("slower response"),
                    opt("more coordinate transforms"),
                    opt("no flux control"),
                ),
                "DTC is fast but has variable switching frequency.",
            ),
            q(
                "A drawback of basic DTC is:",
                (
                    opt("torque/flux ripple and variable switching frequency", correct=True),
                    opt("needing many transforms"),
                    opt("zero dynamics"),
                    opt("no torque control"),
                ),
                "Hysteresis causes ripple.",
            ),
        ),
        "Sensorless control & observers": (
            q(
                "Sensorless drives estimate rotor position from:",
                (
                    opt("voltages and currents via a model/observer", correct=True),
                    opt("a mechanical encoder"),
                    opt("GPS"),
                    opt("the bus temperature"),
                ),
                "Back-EMF/observer-based estimation.",
            ),
            q(
                "Sensorless control is hardest at:",
                (
                    opt("very low / zero speed", correct=True),
                    opt("high speed"),
                    opt("steady state"),
                    opt("rated load"),
                ),
                "Back-EMF vanishes near zero speed.",
            ),
            q(
                "A benefit of sensorless control is:",
                (
                    opt("lower cost and fewer failure points", correct=True),
                    opt("higher cost"),
                    opt("mandatory encoder"),
                    opt("no control"),
                ),
                "Removes the position sensor.",
            ),
        ),
        "Servo drives & motion profiles": (
            q(
                "A servo drive typically closes loops on:",
                (
                    opt("position, speed and current", correct=True),
                    opt("only voltage"),
                    opt("only temperature"),
                    opt("nothing"),
                ),
                "Cascaded position/speed/current control.",
            ),
            q(
                "A trapezoidal motion profile limits:",
                (
                    opt("acceleration (and thus jerk steps)", correct=True),
                    opt("only position"),
                    opt("the bus voltage"),
                    opt("the encoder count"),
                ),
                "Profiles bound velocity/acceleration.",
            ),
            q(
                "S-curve profiles further limit:",
                (
                    opt("jerk (rate of acceleration)", correct=True),
                    opt("voltage"),
                    opt("current names"),
                    opt("pole count"),
                ),
                "Smoother motion, less mechanical stress.",
            ),
        ),
        "Drive design case study: sizing & loop tuning": (
            q(
                "Motor sizing must cover:",
                (
                    opt("peak and continuous (RMS) torque", correct=True),
                    opt("only average speed"),
                    opt("only the encoder"),
                    opt("the paint"),
                ),
                "Size for thermal RMS and peak torque.",
            ),
            q(
                "Loop tuning typically proceeds:",
                (
                    opt("inner current loop first, then speed, then position", correct=True),
                    opt("position first"),
                    opt("all at once randomly"),
                    opt("never"),
                ),
                "Tune fastest inner loop outward.",
            ),
            q(
                "Thermal limits are set by:",
                (
                    opt("continuous RMS current/torque", correct=True),
                    opt("peak torque only"),
                    opt("bus color"),
                    opt("switching table"),
                ),
                "RMS heating governs continuous rating.",
            ),
        ),
    },
    final=(
        q(
            "FOC decouples:",
            (
                opt("torque and flux", correct=True),
                opt("two encoders"),
                opt("voltage names"),
                opt("nothing"),
            ),
            "Like a DC motor.",
        ),
        q(
            "SVPWM improves:",
            (
                opt("DC-bus utilization", correct=True),
                opt("phase count"),
                opt("switching need"),
                opt("nothing"),
            ),
            "~15% more range.",
        ),
        q(
            "DTC uses:",
            (
                opt("hysteresis + switching table", correct=True),
                opt("slow PI only"),
                opt("encoder always"),
                opt("no feedback"),
            ),
            "Fast torque control.",
        ),
        q(
            "Sensorless control struggles at:",
            (
                opt("zero/low speed", correct=True),
                opt("high speed"),
                opt("steady state"),
                opt("rated load"),
            ),
            "Back-EMF vanishes.",
        ),
        q(
            "A servo drive closes loops on:",
            (
                opt("position/speed/current", correct=True),
                opt("voltage only"),
                opt("temperature"),
                opt("none"),
            ),
            "Cascaded.",
        ),
        q(
            "Motor sizing covers:",
            (
                opt("peak and RMS torque", correct=True),
                opt("average speed only"),
                opt("encoder"),
                opt("paint"),
            ),
            "Thermal + peak.",
        ),
    ),
)
