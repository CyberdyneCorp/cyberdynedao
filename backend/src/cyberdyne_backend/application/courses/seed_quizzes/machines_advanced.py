from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The motor-drive power stage: inverter, machine & PWM": (
            q(
                "What is the heart of a modern motor drive that synthesizes AC from a DC bus?",
                (
                    opt("a single full-bridge with two switches"),
                    opt(
                        "a three-phase voltage-source inverter with six switches in three legs",
                        correct=True,
                    ),
                    opt("a passive diode rectifier"),
                    opt("a linear class-AB amplifier"),
                ),
                "The drive uses a three-phase voltage-source inverter: six transistors in three half-bridge legs.",
            ),
            q(
                "In sinusoidal PWM, when is a leg switched on?",
                (
                    opt(
                        "while the sine reference is greater than the triangle carrier",
                        correct=True,
                    ),
                    opt("only at the peak of the sine reference"),
                    opt("whenever the carrier crosses zero"),
                    opt("at a fixed 50 percent duty cycle always"),
                ),
                "Sine PWM compares a sine reference to a triangle carrier; the switch is on while reference exceeds carrier.",
            ),
            q(
                "What is the central trade-off when choosing a higher switching frequency?",
                (
                    opt("smoother current but more switching losses", correct=True),
                    opt("lower current ripple and lower losses with no downside"),
                    opt("higher torque but lower bus voltage"),
                    opt("more harmonics but cooler devices"),
                ),
                "Higher switching frequency gives smoother current but increases switching losses, which is why SiC/GaN devices help.",
            ),
        ),
        "Scalar V/f control": (
            q(
                "In scalar V/f control, why must voltage track frequency?",
                (
                    opt(
                        "to keep the stator flux roughly constant since flux is proportional to V over f",
                        correct=True,
                    ),
                    opt("to keep the switching frequency constant"),
                    opt("to increase the slip at high speed"),
                    opt("to reduce the number of inverter switches needed"),
                ),
                "Stator flux is roughly proportional to V/f, so holding V/f constant keeps flux constant and avoids saturation.",
            ),
            q(
                "Why does practical V/f control add a small voltage boost at low frequency?",
                (
                    opt(
                        "because the stator resistance drop becomes significant and flux collapses",
                        correct=True,
                    ),
                    opt("to raise the switching frequency at low speed"),
                    opt("to weaken the field above base speed"),
                    opt("to eliminate the need for a position sensor"),
                ),
                "At very low frequency the stator resistance drop is significant and flux collapses, so a voltage boost keeps low-speed torque.",
            ),
            q(
                "For which loads is open-loop V/f control especially well suited?",
                (
                    opt(
                        "pumps and fans, where slowing the motor cuts power dramatically",
                        correct=True,
                    ),
                    opt("robot joints needing precise torque at zero speed"),
                    opt("EV traction drives needing instant torque"),
                    opt("servos requiring fast dynamic response"),
                ),
                "V/f is open-loop on torque and ideal for pumps and fans where the cube law makes modest speed cuts save large energy.",
            ),
        ),
        "Field-oriented control (FOC) in depth": (
            q(
                "What does field-oriented control make an AC machine behave like?",
                (
                    opt("the ideal DC motor with independent flux and torque knobs", correct=True),
                    opt("a fixed-speed synchronous generator"),
                    opt("a passive transformer"),
                    opt("an uncontrolled induction motor"),
                ),
                "FOC gives two independent knobs, one for flux and one for torque, just like the ideal DC motor.",
            ),
            q(
                "In the d-q frame for a PMSM below base speed, what is the role of i_d and i_q?",
                (
                    opt("i_d controls flux and is set to zero; i_q controls torque", correct=True),
                    opt("i_d controls torque; i_q controls flux"),
                    opt("both control torque equally"),
                    opt("i_q is always set to zero below base speed"),
                ),
                "i_d controls flux and is set to zero below base speed for a PMSM, while i_q controls torque with T about k times i_q.",
            ),
            q(
                "Why does FOC add decoupling feedforward terms?",
                (
                    opt(
                        "because the d and q axes cross-couple through the speed EMF terms omega L i",
                        correct=True,
                    ),
                    opt("to increase the switching frequency"),
                    opt("to remove the need for Clarke and Park transforms"),
                    opt("to add slip compensation for induction motors only"),
                ),
                "A rotating motor cross-couples d and q through speed EMF terms, so decoupling feedforward lets the two PI loops act independently.",
            ),
        ),
        "Sensorless control & observers": (
            q(
                "What does sensorless control estimate instead of measuring directly?",
                (
                    opt(
                        "the rotor position and speed from currents and voltages already measured",
                        correct=True,
                    ),
                    opt("the DC bus voltage from the switching frequency"),
                    opt("the stator resistance from the torque command"),
                    opt("the load inertia from the encoder count"),
                ),
                "Sensorless control estimates rotor position and speed from the currents and voltages the drive already measures.",
            ),
            q(
                "Which method is used at low or zero speed where back-EMF vanishes?",
                (
                    opt(
                        "high-frequency signal injection that detects rotor saliency", correct=True
                    ),
                    opt("back-EMF phase detection"),
                    opt("an encoder reading"),
                    opt("V/f open-loop control"),
                ),
                "Near standstill the back-EMF vanishes, so a high-frequency probe is injected to detect the rotor saliency.",
            ),
            q(
                "What is an observer in this context?",
                (
                    opt(
                        "a real-time motor model that continuously corrects itself with the measurement error",
                        correct=True,
                    ),
                    opt("a hardware encoder mounted on the shaft"),
                    opt("a fixed lookup table of rotor angles"),
                    opt("a passive low-pass filter on the bus voltage"),
                ),
                "An observer runs a real-time model of the motor and corrects it with the measurement error, a feedback loop on the estimate.",
            ),
        ),
        "Regenerative braking & four-quadrant operation": (
            q(
                "In which quadrants is the machine acting as a generator?",
                (
                    opt("quadrants II and IV, where braking torque opposes motion", correct=True),
                    opt("quadrants I and III, where power flows to the motor"),
                    opt("only quadrant I"),
                    opt("only quadrant III"),
                ),
                "In quadrants II and IV the machine is a generator: braking torque opposes motion and power flows back to the DC bus.",
            ),
            q(
                "How does the controller command the machine to brake regeneratively?",
                (
                    opt(
                        "it commands negative i_q so the machine generates negative torque",
                        correct=True,
                    ),
                    opt("it raises the switching frequency"),
                    opt("it commands maximum positive i_d"),
                    opt("it disconnects the inverter from the bus"),
                ),
                "To brake, the controller commands negative i_q (negative torque); the machine generates and charges the DC bus.",
            ),
            q(
                "What is used when a simple diode-rectifier drive cannot send power back to the source?",
                (
                    opt(
                        "a braking chopper plus resistor that dumps the excess energy as heat",
                        correct=True,
                    ),
                    opt("an active front end that feeds the grid"),
                    opt("a larger DC bus capacitor only"),
                    opt("a second inverter in parallel"),
                ),
                "A diode-rectifier drive cannot send power back, so a braking chopper and resistor dump the excess as heat to limit bus voltage.",
            ),
        ),
        "Lab: d-q (FOC) current control": (
            q(
                "In the lab, what does the iq* reference do during the simulation?",
                (
                    opt("it steps from 0 to 30 A at t = 2 ms", correct=True),
                    opt("it ramps linearly from 0 to 100 A"),
                    opt("it stays at 30 A the whole time"),
                    opt("it follows a sine wave at 50 Hz"),
                ),
                "The references set id* = 0 and iq* steps from 0 to 30 A at t = 2 ms so the loop tracks a torque step.",
            ),
            q(
                "What is the purpose of the decoupling feedforward terms in the lab code?",
                (
                    opt(
                        "to cancel the speed cross-coupling so id stays near zero when iq steps",
                        correct=True,
                    ),
                    opt("to increase the magnet flux psi"),
                    opt("to raise the sample rate above 50 kHz"),
                    opt("to convert from the d-q frame to three phases"),
                ),
                "The decoupling feedforward cancels the speed cross-coupling terms; removing them lets id get disturbed by iq steps.",
            ),
            q(
                "According to the Try it yourself notes, what happens if you raise Kp and Ki?",
                (
                    opt("faster tracking but risk of overshoot or oscillation", correct=True),
                    opt("slower tracking with no overshoot"),
                    opt("the id loop is removed entirely"),
                    opt("the simulation step dt automatically shrinks"),
                ),
                "Raising Kp/Ki gives faster tracking but you must watch for overshoot and oscillation.",
            ),
        ),
        "Applications & the throughline: EV, robotics, industrial & HVAC": (
            q(
                "What is the classic EV traction torque-speed envelope?",
                (
                    opt(
                        "flat torque to base speed, then torque falls as 1/speed to hold constant power",
                        correct=True,
                    ),
                    opt("torque rises linearly with speed without limit"),
                    opt("constant power from zero speed upward"),
                    opt("zero torque until base speed, then constant torque"),
                ),
                "Below base speed torque is flat (current-limited); above it torque falls as 1/speed to hold constant power (voltage-limited).",
            ),
            q(
                "Which drive type increasingly powers modern inverter HVAC and appliance compressors?",
                (
                    opt(
                        "sensorless FOC PMSM drives for quiet, efficient variable-capacity operation",
                        correct=True,
                    ),
                    opt("fixed-speed on/off induction motors"),
                    opt("open-loop stepper drives"),
                    opt("brushed DC motors with mechanical commutators"),
                ),
                "HVAC and appliance compressors increasingly use sensorless FOC PMSM drives for quiet, efficient, variable-capacity operation.",
            ),
            q(
                "Roughly what share of the world's electricity do electric machines and their drives consume?",
                (
                    opt("about 45 percent", correct=True),
                    opt("about 5 percent"),
                    opt("about 90 percent"),
                    opt("about 20 percent"),
                ),
                "Electric machines and their drives consume roughly 45 percent of the world's electricity, so efficiency gains scale globally.",
            ),
        ),
    },
    final=(
        q(
            "What sets the line voltage limit advantage of space-vector PWM over plain sine PWM?",
            (
                opt(
                    "SVPWM and third-harmonic injection reach about 15 percent more line voltage",
                    correct=True,
                ),
                opt("SVPWM halves the DC bus requirement"),
                opt("sine PWM always reaches a higher line voltage"),
                opt("both reach exactly the same line voltage"),
            ),
            "SVPWM and third-harmonic injection squeeze out about 15 percent more, reaching V_line_max = Vdc / sqrt(2).",
        ),
        q(
            "Compared with V/f, what is the key advantage of FOC?",
            (
                opt(
                    "fast, precise dynamic torque control including excellent torque at zero speed",
                    correct=True,
                ),
                opt("it needs no DSP or MCU and has tiny compute cost"),
                opt("it works open-loop on torque for pumps and fans"),
                opt("it never requires rotor angle information"),
            ),
            "FOC gives fast, precise response and excellent torque at zero speed, at the cost of needing position and a DSP/MCU.",
        ),
        q(
            "In FOC, how is high speed beyond base speed reached when there is no voltage headroom left?",
            (
                opt("by driving negative i_d to weaken the magnet flux", correct=True),
                opt("by driving negative i_q to add torque"),
                opt("by raising the DC bus to infinity"),
                opt("by switching to V/f control"),
            ),
            "Above base speed there is no voltage headroom, so negative i_d weakens the magnet flux to extend speed at constant power.",
        ),
        q(
            "Which estimation regime relies on back-EMF for the rotor angle?",
            (
                opt("medium to high speed, where back-EMF is strong", correct=True),
                opt("low or zero speed, where back-EMF vanishes"),
                opt("only when an encoder is present"),
                opt("only during regenerative braking"),
            ),
            "At medium and high speed the back-EMF is strong and its phase reveals the rotor angle; low/zero speed uses saliency injection.",
        ),
        q(
            "What common chain underlies EV, robotics, industrial, and HVAC drives?",
            (
                opt(
                    "machine plus inverter plus control, changing only machine type, ratings, and tuning",
                    correct=True,
                ),
                opt("a different control algorithm unique to each application"),
                opt("a passive rectifier with no control"),
                opt("a mechanical gearbox replacing electronic control"),
            ),
            "The same chain of machine, inverter, and control powers all of them by changing only the machine type, ratings, and control tuning.",
        ),
    ),
)
