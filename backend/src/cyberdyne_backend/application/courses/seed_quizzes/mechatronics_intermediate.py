"""Quiz questions for the Mechatronics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Signal conditioning and the ADC chain": (
            q(
                "The canonical signal-conditioning chain before an ADC is?",
                (
                    opt("Amplify, filter, level-shift, then sample", correct=True),
                    opt("Sample first, then amplify"),
                    opt("Filter only, never amplify"),
                    opt("Quantise before filtering"),
                ),
                "Conditioning prepares the signal: gain, anti-aliasing filter, level shift, then ADC.",
            ),
            q(
                "An instrumentation amplifier is preferred for a bridge sensor because it?",
                (
                    opt("Rejects common-mode noise with high CMRR", correct=True),
                    opt("Has no gain"),
                    opt("Only works at DC"),
                    opt("Removes the need for an ADC"),
                ),
                "High CMRR rejects the common-mode voltage the bridge sits on while amplifying the small difference.",
            ),
            q(
                "A first-order RC low-pass filter has cutoff frequency fc equal to?",
                (
                    opt("1 / (2 pi R C)", correct=True),
                    opt("2 pi R C"),
                    opt("R C"),
                    opt("1 / (R + C)"),
                ),
                "fc = 1/(2 pi R C); it rolls off at 20 dB/decade above fc.",
            ),
        ),
        "Microcontrollers: timers, PWM and interrupts": (
            q(
                "PWM produces an effective analog level by?",
                (
                    opt("Varying the duty cycle so average voltage is D*Vcc", correct=True),
                    opt("Changing the supply voltage continuously"),
                    opt("Using a true DAC only"),
                    opt("Switching the pin at random"),
                ),
                "Average delivered voltage equals duty cycle times supply.",
            ),
            q(
                "Why run a control loop from a timer interrupt rather than polling?",
                (
                    opt("It gives a fixed, jitter-free sample period Ts", correct=True),
                    opt("It makes the loop slower on purpose"),
                    opt("Polling is always more accurate"),
                    opt("Interrupts cannot read sensors"),
                ),
                "A timer ISR fires at an exact rate, giving deterministic sampling for control.",
            ),
            q(
                "A good rule for interrupt service routines is?",
                (
                    opt("Keep them short and never block", correct=True),
                    opt("Do all heavy computation inside them"),
                    opt("Add long delays for stability"),
                    opt("Disable all other interrupts forever"),
                ),
                "ISRs must be fast and non-blocking to preserve real-time behaviour.",
            ),
        ),
        "Digital communication: I2C, SPI, UART, CAN": (
            q(
                "Which bus is asynchronous and uses no shared clock line?",
                (
                    opt("UART", correct=True),
                    opt("SPI"),
                    opt("I2C"),
                    opt("CAN"),
                ),
                "UART is asynchronous; both ends agree on a baud rate instead of sharing a clock.",
            ),
            q(
                "I2C's main advantage over SPI is?",
                (
                    opt("Only two wires shared by many addressed devices", correct=True),
                    opt("It is always faster than SPI"),
                    opt("It needs one chip-select per device"),
                    opt("It is full-duplex"),
                ),
                "I2C is wire-thrifty (SDA/SCL) with addressing; SPI is faster but pin-hungry.",
            ),
            q(
                "Which bus is the robust, multi-master backbone of automotive networks?",
                (
                    opt("CAN", correct=True),
                    opt("UART"),
                    opt("SPI"),
                    opt("I2C"),
                ),
                "CAN is differential, multi-master, with arbitration and error checking.",
            ),
        ),
        "DC motor modelling and PWM drive": (
            q(
                "In the DC motor electrical equation V = R i + L di/dt + ke*omega, the term ke*omega is?",
                (
                    opt("The back-EMF that grows with speed", correct=True),
                    opt("The resistive voltage drop"),
                    opt("The inductive transient"),
                    opt("The load torque"),
                ),
                "Back-EMF ke*omega opposes the applied voltage as speed rises.",
            ),
            q(
                "Neglecting inductance, a DC motor's speed response to a voltage step is?",
                (
                    opt("First order with time constant tau_m = R J / (kt ke + R b)", correct=True),
                    opt("An undamped oscillation"),
                    opt("Instantaneous with no dynamics"),
                    opt("A pure integrator forever"),
                ),
                "With L neglected the mechanical pole dominates, giving a first-order rise.",
            ),
            q(
                "An H-bridge driven by PWM provides?",
                (
                    opt(
                        "Average voltage control via duty cycle plus direction control",
                        correct=True,
                    ),
                    opt("Only on/off with no speed control"),
                    opt("A constant voltage regardless of duty"),
                    opt("Sensing but no driving"),
                ),
                "Duty sets average voltage (D*Vcc); the bridge sets direction and braking.",
            ),
        ),
        "The digital PID loop": (
            q(
                "Which PID term removes steady-state error?",
                (
                    opt("The integral term", correct=True),
                    opt("The proportional term"),
                    opt("The derivative term"),
                    opt("None of them"),
                ),
                "Integral action accumulates past error until the offset is driven to zero.",
            ),
            q(
                "Integrator anti-windup is needed because?",
                (
                    opt(
                        "A saturated actuator lets the integral grow unboundedly, causing overshoot",
                        correct=True,
                    ),
                    opt("The derivative term is too small"),
                    opt("Proportional gain must be zero"),
                    opt("The sample period is too long only"),
                ),
                "When the output saturates, unchecked integration winds up and degrades response.",
            ),
            q(
                "In a discrete PID, the derivative term is commonly approximated by?",
                (
                    opt(
                        "A backward difference (e_k - e_(k-1)) / Ts, usually filtered", correct=True
                    ),
                    opt("A running sum of error"),
                    opt("The reference value alone"),
                    opt("A constant offset"),
                ),
                "Backward difference estimates de/dt; filtering tames measurement noise.",
            ),
        ),
    },
    final=(
        q(
            "The anti-aliasing filter in an ADC chain should be placed?",
            (
                opt("Before the ADC, with cutoff below fs/2", correct=True),
                opt("After the ADC in software only"),
                opt("Anywhere; placement does not matter"),
                opt("After quantisation"),
            ),
            "Aliasing must be removed in the analog domain before sampling.",
        ),
        q(
            "A 30 percent duty cycle PWM on a 12 V supply delivers an average of about?",
            (
                opt("3.6 V", correct=True),
                opt("12 V"),
                opt("0.3 V"),
                opt("9 V"),
            ),
            "Average = D*Vcc = 0.30*12 = 3.6 V.",
        ),
        q(
            "Which bus is best when many low-rate sensors must share just two wires?",
            (
                opt("I2C", correct=True),
                opt("SPI"),
                opt("CAN"),
                opt("Parallel bus"),
            ),
            "I2C addresses many devices over SDA/SCL with minimal wiring.",
        ),
        q(
            "The torque constant kt of a DC motor relates torque to?",
            (
                opt("Armature current", correct=True),
                opt("Supply frequency"),
                opt("Ambient temperature"),
                opt("Rotor inertia"),
            ),
            "tau = kt * i.",
        ),
        q(
            "Running the control loop in a timer ISR primarily ensures?",
            (
                opt("A fixed sample period with low jitter", correct=True),
                opt("The lowest possible CPU usage"),
                opt("That no sensors are read"),
                opt("That PWM is disabled"),
            ),
            "Deterministic timing is essential for correct discrete control.",
        ),
        q(
            "Which statement about discrete PID tuning is true?",
            (
                opt(
                    "Derivative action should be filtered to reduce noise amplification",
                    correct=True,
                ),
                opt("Integral gain has no effect on steady-state error"),
                opt("Anti-windup is never necessary"),
                opt("Sample period Ts can be ignored in the difference equations"),
            ),
            "The derivative term amplifies noise; filtering it is standard practice.",
        ),
    ),
)
