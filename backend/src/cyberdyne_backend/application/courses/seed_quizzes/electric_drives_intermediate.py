"""Quiz questions for the Electric Drives & Motor Control - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "DC motor drives & closed-loop speed control": (
            q(
                "DC motor speed is commonly controlled by varying:",
                (
                    opt("the armature voltage", correct=True),
                    opt("the number of poles"),
                    opt("the frame size"),
                    opt("the paint"),
                ),
                "Armature voltage control sets speed below base speed.",
            ),
            q(
                "A closed-loop speed drive uses:",
                (
                    opt("speed feedback to correct error", correct=True),
                    opt("no feedback"),
                    opt("only open-loop voltage"),
                    opt("a fixed duty cycle"),
                ),
                "Feedback corrects load disturbances.",
            ),
            q(
                "Above base speed, DC motors use:",
                (
                    opt("field weakening", correct=True),
                    opt("voltage boost beyond rated"),
                    opt("more poles"),
                    opt("larger brushes"),
                ),
                "Field weakening extends the speed range at constant power.",
            ),
        ),
        "PWM & the voltage-source inverter": (
            q(
                "A voltage-source inverter converts:",
                (
                    opt("DC to variable-frequency AC", correct=True),
                    opt("AC to DC only"),
                    opt("DC to fixed DC"),
                    opt("AC to AC directly"),
                ),
                "VSI synthesizes AC from a DC bus.",
            ),
            q(
                "PWM controls the inverter output by varying:",
                (
                    opt("the switch duty cycle", correct=True),
                    opt("the DC bus color"),
                    opt("the number of phases"),
                    opt("the heatsink"),
                ),
                "Duty cycle sets the average output voltage.",
            ),
            q(
                "A higher PWM switching frequency tends to:",
                (
                    opt("reduce current ripple but raise switching losses", correct=True),
                    opt("eliminate all losses"),
                    opt("reduce bandwidth"),
                    opt("increase ripple"),
                ),
                "Trade-off: ripple vs switching loss.",
            ),
        ),
        "Scalar V/f control of induction motors": (
            q(
                "V/f control keeps which ratio roughly constant?",
                (
                    opt("voltage-to-frequency", correct=True),
                    opt("current-to-torque"),
                    opt("power-to-speed"),
                    opt("flux-to-current"),
                ),
                "Constant V/f keeps flux roughly constant.",
            ),
            q(
                "V/f control is popular because it is:",
                (
                    opt("simple and sensorless", correct=True),
                    opt("the most precise dynamic control"),
                    opt("only for DC motors"),
                    opt("exact at zero speed"),
                ),
                "Simple open-loop-ish speed control.",
            ),
            q(
                "A limitation of basic V/f control is:",
                (
                    opt("poor torque/dynamics at very low speed", correct=True),
                    opt("too much precision"),
                    opt("needing an encoder"),
                    opt("working only above base speed"),
                ),
                "Low-speed torque is weak without compensation.",
            ),
        ),
        "Current control loops & cascaded control": (
            q(
                "In a cascaded drive, the inner loop usually controls:",
                (
                    opt("current (torque)", correct=True),
                    opt("position"),
                    opt("temperature"),
                    opt("voltage bus"),
                ),
                "Inner current loop is fastest; outer loops are speed/position.",
            ),
            q(
                "Cascaded loops require the inner loop to be:",
                (
                    opt("faster than the outer loop", correct=True),
                    opt("slower than the outer"),
                    opt("the same speed"),
                    opt("disabled"),
                ),
                "Bandwidth separation ensures stability.",
            ),
            q(
                "Current control matters because motor torque is set by:",
                (
                    opt("current", correct=True),
                    opt("the frame color"),
                    opt("the PWM carrier only"),
                    opt("the supply frequency only"),
                ),
                "Torque is proportional to current.",
            ),
        ),
        "Feedback devices: encoders, resolvers & Hall sensors": (
            q(
                "An incremental encoder provides:",
                (
                    opt("relative position via pulse counting", correct=True),
                    opt("absolute position always"),
                    opt("temperature"),
                    opt("bus voltage"),
                ),
                "Counts pulses for relative position/speed.",
            ),
            q(
                "A resolver is valued for:",
                (
                    opt("robustness in harsh environments", correct=True),
                    opt("being the cheapest"),
                    opt("needing no excitation"),
                    opt("digital-only output"),
                ),
                "Rugged analog position sensor.",
            ),
            q(
                "Hall sensors in BLDC motors give:",
                (
                    opt("coarse rotor position for commutation", correct=True),
                    opt("high-resolution position"),
                    opt("torque directly"),
                    opt("bus current"),
                ),
                "Six-step commutation uses Hall position.",
            ),
        ),
        "Regenerative braking & energy recovery": (
            q(
                "During regenerative braking the motor acts as a:",
                (
                    opt("generator returning energy", correct=True),
                    opt("short circuit"),
                    opt("fixed resistor"),
                    opt("capacitor"),
                ),
                "Kinetic energy is converted back to electrical.",
            ),
            q(
                "Recovered energy can be:",
                (
                    opt("returned to the supply or stored", correct=True),
                    opt("only dissipated as heat"),
                    opt("ignored"),
                    opt("sent to ground"),
                ),
                "Fed back or stored (battery/cap).",
            ),
            q(
                "If the supply cannot absorb regen energy, drives use a:",
                (
                    opt("braking resistor (dynamic braking)", correct=True),
                    opt("larger motor"),
                    opt("bigger encoder"),
                    opt("smaller bus"),
                ),
                "A chopper+resistor dumps excess energy.",
            ),
        ),
    },
    final=(
        q(
            "DC motor speed below base speed is set by:",
            (
                opt("armature voltage", correct=True),
                opt("pole count"),
                opt("frame size"),
                opt("paint"),
            ),
            "Armature voltage control.",
        ),
        q(
            "A VSI converts:",
            (
                opt("DC to variable AC", correct=True),
                opt("AC to DC"),
                opt("DC to DC"),
                opt("AC to AC"),
            ),
            "DC-bus to AC.",
        ),
        q(
            "V/f control holds constant:",
            (
                opt("voltage/frequency", correct=True),
                opt("current/torque"),
                opt("power/speed"),
                opt("flux/current"),
            ),
            "Constant flux.",
        ),
        q(
            "Inner cascaded loop controls:",
            (
                opt("current/torque", correct=True),
                opt("position"),
                opt("temperature"),
                opt("bus"),
            ),
            "Fastest inner loop.",
        ),
        q(
            "A resolver is chosen for:",
            (
                opt("ruggedness", correct=True),
                opt("lowest cost"),
                opt("digital output"),
                opt("no excitation"),
            ),
            "Harsh-environment position.",
        ),
        q(
            "Regen braking makes the motor a:",
            (
                opt("generator", correct=True),
                opt("resistor"),
                opt("capacitor"),
                opt("short"),
            ),
            "Returns energy.",
        ),
    ),
)
