from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Electromechanical energy conversion & magnetic circuits": (
            q(
                "In the magnetic-circuit analogy, which electrical quantity does magnetic flux correspond to?",
                (
                    opt("voltage"),
                    opt("current", correct=True),
                    opt("resistance"),
                    opt("power"),
                ),
                "MMF is like voltage, flux is like current, and reluctance is like resistance.",
            ),
            q(
                "What does Faraday's law e = -N dPhi/dt tell us about induced voltage?",
                (
                    opt("It is produced only by a steady, unchanging flux"),
                    opt("It is produced by a changing flux and opposes the change", correct=True),
                    opt("It depends on the wire resistance, not the flux"),
                    opt("It is always zero in an iron core"),
                ),
                "A changing flux induces a voltage and Lenz's law fixes the sign so the effect opposes the change.",
            ),
            q(
                "Why are motor cores made of iron?",
                (
                    opt(
                        "Iron has high permeability and low reluctance, so it guides flux",
                        correct=True,
                    ),
                    opt("Iron has the highest electrical conductivity of any metal"),
                    opt("Iron cannot saturate at any flux level"),
                    opt("Iron produces magnetomotive force on its own without current"),
                ),
                "Iron has high permeability (low reluctance), so it guides flux the way a wire guides current.",
            ),
        ),
        "DC machines: construction, back-EMF & torque-speed": (
            q(
                "What is the function of the commutator and brushes in a DC machine?",
                (
                    opt("They generate the field flux without any magnets"),
                    opt("They reverse the armature current so torque never reverses", correct=True),
                    opt("They store energy to smooth the supply voltage"),
                    opt("They measure the rotor speed for feedback"),
                ),
                "The commutator plus brushes mechanically reverse the armature current twice per revolution so torque never reverses.",
            ),
            q(
                "Using V = E + Ia*Ra, why is the stall (inrush) current so large at the instant of switch-on?",
                (
                    opt("The armature resistance Ra spikes to a high value at standstill"),
                    opt("Speed is zero so back-EMF E is zero, leaving current V/Ra", correct=True),
                    opt("The back-EMF E equals the supply V at standstill"),
                    opt("The field flux collapses to zero at standstill"),
                ),
                "At standstill omega = 0 so there is no back-EMF, and the stall current is V/Ra.",
            ),
            q(
                "What shape is the ideal DC-motor torque-speed characteristic?",
                (
                    opt("A straight line from stall torque down to no-load speed", correct=True),
                    opt("A parabola peaking at half speed"),
                    opt("A flat horizontal line at constant torque"),
                    opt("An exponential decay"),
                ),
                "Combining T = kPhi*Ia with V = E + Ia*Ra gives a straight line: max torque at stall, zero torque at no-load speed.",
            ),
        ),
        "Transformers: ideal, real & the equivalent circuit": (
            q(
                "For an ideal transformer with turns ratio a = N1/N2, how do the currents relate?",
                (
                    opt("I1/I2 = a"),
                    opt("I1/I2 = 1/a", correct=True),
                    opt("I1/I2 = a squared"),
                    opt("I1 = I2 always"),
                ),
                "Because power in equals power out, currents scale inversely: I1/I2 = N2/N1 = 1/a.",
            ),
            q(
                "Which non-ideality is modelled by the shunt resistance Rc in the equivalent circuit?",
                (
                    opt("winding copper I^2R loss"),
                    opt("leakage flux that misses the other coil"),
                    opt("core loss from hysteresis and eddy currents", correct=True),
                    opt("finite core permeability"),
                ),
                "Rc models core loss (hysteresis plus eddy currents); Xm models the magnetizing current.",
            ),
            q(
                "Why does the grid transmit power at high voltage and low current?",
                (
                    opt("Transformers cannot operate at low voltage"),
                    opt("It slashes line losses because P_loss = I^2*R", correct=True),
                    opt("High voltage eliminates copper losses entirely"),
                    opt("Low current increases the turns ratio automatically"),
                ),
                "High voltage and low current cut line losses, since P_loss = I^2*R; that is why the grid is AC with transformers.",
            ),
        ),
        "Three-phase fundamentals: phasors, line vs phase & power": (
            q(
                "By how many degrees are the three voltages of a balanced three-phase system shifted from each other?",
                (
                    opt("90 degrees"),
                    opt("120 degrees", correct=True),
                    opt("60 degrees"),
                    opt("180 degrees"),
                ),
                "The three sinusoidal voltages have equal amplitude and are each shifted by 120 degrees.",
            ),
            q(
                "In a wye (Y) connection, how do line and phase quantities relate?",
                (
                    opt("Vline = sqrt(3)*Vphase and Iline = Iphase", correct=True),
                    opt("Vline = Vphase and Iline = sqrt(3)*Iphase"),
                    opt("Vline = Vphase and Iline = Iphase"),
                    opt("Vline = sqrt(3)*Vphase and Iline = sqrt(3)*Iphase"),
                ),
                "In wye, Vline = sqrt(3)*Vphase while Iline = Iphase; delta is the reverse.",
            ),
            q(
                "Why do large three-phase motors run more smoothly than single-phase ones?",
                (
                    opt("Three-phase uses thicker copper wires"),
                    opt(
                        "Instantaneous three-phase power is constant with no pulsation",
                        correct=True,
                    ),
                    opt("The neutral carries the full motor current"),
                    opt("Single-phase has a higher power factor"),
                ),
                "Unlike single phase, instantaneous balanced three-phase power is constant, so big motors run smoothly.",
            ),
        ),
        "AC machines & the rotating magnetic field": (
            q(
                "What produces a rotating magnetic field in an AC machine?",
                (
                    opt(
                        "Three coils 120 deg apart in space fed by currents 120 deg apart in time",
                        correct=True,
                    ),
                    opt("A single coil fed with DC current"),
                    opt("A commutator switching a DC supply"),
                    opt("Permanent magnets spinning on the stator"),
                ),
                "Feeding three coils placed 120 deg apart in space with currents 120 deg apart in time gives a rotating field of constant magnitude.",
            ),
            q(
                "For a 4-pole motor on a 50 Hz supply, what is the synchronous speed ns = 120 f / P?",
                (
                    opt("3000 rpm"),
                    opt("1500 rpm", correct=True),
                    opt("750 rpm"),
                    opt("1000 rpm"),
                ),
                "ns = 120*50/4 = 1500 rpm; a 2-pole motor would spin at 3000 rpm.",
            ),
            q(
                "What is the key difference between an induction motor and a synchronous motor?",
                (
                    opt(
                        "The induction rotor lags the field by slip; the synchronous rotor locks to it",
                        correct=True,
                    ),
                    opt(
                        "The induction rotor is a permanent magnet; the synchronous rotor is a cage"
                    ),
                    opt("The synchronous motor has brushes; the induction motor does not"),
                    opt("The induction motor runs faster than synchronous speed"),
                ),
                "The induction rotor chases the field and lags by slip; the synchronous rotor is a magnet that locks to the field at ns.",
            ),
        ),
        "Lab: DC motor torque-speed curve": (
            q(
                "In the lab, how is the no-load speed w0 computed?",
                (
                    opt("w0 = V/kPhi", correct=True),
                    opt("w0 = kPhi/V"),
                    opt("w0 = V/Ra"),
                    opt("w0 = kPhi*V/Ra"),
                ),
                "Torque is zero when back-EMF equals the supply, giving w0 = V/kPhi.",
            ),
            q(
                "The lab computes T_stall = kPhi*V/Ra. What does this represent?",
                (
                    opt("the torque at zero speed (standstill)", correct=True),
                    opt("the torque at no-load speed"),
                    opt("the mechanical output power"),
                    opt("the peak mechanical power point"),
                ),
                "T_stall = kPhi*V/Ra is the torque at zero speed, the highest point on the torque-speed line.",
            ),
            q(
                "According to the lab note, at what speed does peak mechanical power occur?",
                (
                    opt("at half the no-load speed", correct=True),
                    opt("at the no-load speed"),
                    opt("at standstill"),
                    opt("at twice the no-load speed"),
                ),
                "The lab prints that peak power occurs at half the no-load speed, the middle of the torque-speed line.",
            ),
        ),
    },
    final=(
        q(
            "Which law explains the back-EMF of a motor, transformer action, and generator voltage alike?",
            (
                opt("Ohm's law"),
                opt("Faraday's law of induction", correct=True),
                opt("Kirchhoff's current law"),
                opt("the turns-ratio rule"),
            ),
            "A changing flux inducing a voltage (Faraday, with Lenz's sign) underlies transformers, generators, and motor back-EMF.",
        ),
        q(
            "A DC motor and a transformer differ most in that:",
            (
                opt(
                    "the transformer has no moving parts and trades voltage for current",
                    correct=True,
                ),
                opt("the transformer produces mechanical torque on a shaft"),
                opt("the DC motor has no back-EMF"),
                opt("the transformer uses a commutator and brushes"),
            ),
            "A transformer has no moving parts and trades voltage for current at constant power; the DC motor converts electrical energy to torque.",
        ),
        q(
            "For a three-phase wye system with Vline = 400 V, what is the approximate phase voltage?",
            (
                opt("400 V"),
                opt("231 V", correct=True),
                opt("693 V"),
                opt("133 V"),
            ),
            "In wye Vphase = Vline/sqrt(3) = 400/1.732 ~ 231 V, which is why 400 V three-phase feeds 230 V single-phase sockets.",
        ),
        q(
            "Why did Tesla's induction motor beat the brushed DC motor for industrial use?",
            (
                opt("It runs at exactly synchronous speed with no slip"),
                opt(
                    "It has no brushes or commutator to wear, and the rotor needs no electrical contact",
                    correct=True,
                ),
                opt("It requires a permanent magnet rotor that never demagnetizes"),
                opt("It produces a larger stall current at switch-on"),
            ),
            "The rotating-field induction motor has no brushes or commutator to wear; its rotor needs no electrical connection.",
        ),
        q(
            "Which statement about the synchronous speed ns = 120 f / P is correct?",
            (
                opt("It depends only on supply frequency and pole count", correct=True),
                opt("It increases as the number of poles increases"),
                opt("It depends on the rotor slip"),
                opt("It is set by the armature voltage"),
            ),
            "Synchronous speed is set only by supply frequency f and pole number P; more poles gives a lower ns.",
        ),
    ),
)
