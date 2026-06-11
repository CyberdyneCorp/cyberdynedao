from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Induction motors: slip, torque-speed & starting": (
            q(
                "What is the slip s of an induction motor at standstill?",
                (
                    opt("s = 0"),
                    opt("s = 1", correct=True),
                    opt("s = 0.5"),
                    opt("s is negative"),
                ),
                "At standstill the rotor does not turn, so n = 0 and s = (ns - n)/ns = 1.",
            ),
            q(
                "How does increasing rotor resistance R2 affect the torque-speed curve?",
                (
                    opt("It raises the magnitude of the breakdown torque"),
                    opt(
                        "It moves the breakdown point toward standstill (higher starting torque)",
                        correct=True,
                    ),
                    opt("It moves the breakdown point toward synchronous speed"),
                    opt("It eliminates slip entirely"),
                ),
                "Peak torque magnitude is fixed but its location is s approx R2/X2, so more R2 shifts the peak toward starting.",
            ),
            q(
                "Roughly how much current does an induction motor draw at start (s = 1) on direct line voltage?",
                (
                    opt("About the same as rated current"),
                    opt("About half rated current"),
                    opt("About 5-7x its rated current", correct=True),
                    opt("Zero until it reaches synchronous speed"),
                ),
                "At s = 1 a motor on direct line voltage pulls 5-7x its rated current, which starting methods aim to limit.",
            ),
        ),
        "Synchronous machines & PMSM: excitation, generators & V-curves": (
            q(
                "At what load angle delta does a synchronous machine develop maximum power?",
                (
                    opt("0 degrees"),
                    opt("45 degrees"),
                    opt("90 degrees", correct=True),
                    opt("180 degrees"),
                ),
                "P = (V*E/Xs) sin(delta) peaks at delta = 90 degrees; pushing past it causes loss of synchronism (pole slip).",
            ),
            q(
                "What does adjusting field excitation let a synchronous machine control independently of its mechanical load?",
                (
                    opt("Its synchronous speed"),
                    opt("Its power factor", correct=True),
                    opt("Its number of poles"),
                    opt("The grid frequency"),
                ),
                "By adjusting field excitation you control power factor: under-excited draws lagging current, over-excited supplies leading current.",
            ),
            q(
                "Why is the grid frequency held tightly at 50/60 Hz?",
                (
                    opt("Because induction motor slip forces it there"),
                    opt(
                        "Because synchronous generator frequency is locked to shaft speed",
                        correct=True,
                    ),
                    opt("Because transformers only work at those frequencies"),
                    opt("Because rotor resistance fixes it"),
                ),
                "Nearly all electricity comes from synchronous generators whose frequency is locked to shaft speed, holding the grid at 50/60 Hz.",
            ),
        ),
        "The rotating field & space vectors: Clarke & Park transforms": (
            q(
                "What does the Clarke transform produce from the three phase quantities?",
                (
                    opt("A rotating d-q frame"),
                    opt("A two-axis stationary alpha-beta frame", correct=True),
                    opt("A single DC value"),
                    opt("The rotor slip"),
                ),
                "The Clarke transform collapses the three 120-degree phase quantities into a two-axis stationary (alpha, beta) frame.",
            ),
            q(
                "In the d-q frame, which current is the torque-producing component?",
                (
                    opt("id, aligned with rotor flux"),
                    opt("iq, the quadrature-axis current", correct=True),
                    opt("ialpha"),
                    opt("ibeta"),
                ),
                "iq is 90 degrees ahead of the flux and is the torque-producing current; id is the magnetizing flux-producing current.",
            ),
            q(
                "What happens to the AC space vector when viewed in the rotating d-q (Park) frame in steady state?",
                (
                    opt("It traces a larger circle"),
                    opt("It becomes DC (stops moving)", correct=True),
                    opt("It doubles in frequency"),
                    opt("It disappears entirely"),
                ),
                "Rotating the axes at the rotor angle makes the space vector stop moving, so the AC quantities become DC and are easier to regulate.",
            ),
        ),
        "BLDC & stepper motors: commutation & drive schemes": (
            q(
                "How does a BLDC motor commutate instead of using brushes?",
                (
                    opt("With slip rings fed DC"),
                    opt("The inverter energizes phases in a six-step sequence", correct=True),
                    opt("With a mechanical commutator on the rotor"),
                    opt("By varying rotor resistance"),
                ),
                "A BLDC has magnets on the rotor and the inverter does commutation, energizing two of three phases in a six-step sequence every 60 electrical degrees.",
            ),
            q(
                "What is a defining feature of a stepper motor used for positioning?",
                (
                    opt("It always needs encoder feedback"),
                    opt(
                        "It moves a fixed angle per step and holds position open-loop", correct=True
                    ),
                    opt("It cannot hold a position when stopped"),
                    opt("It runs only at synchronous speed"),
                ),
                "A stepper moves a fixed angle per electrical step (commonly 1.8 deg = 200 steps/rev) and holds position open-loop with no feedback.",
            ),
            q(
                "What does microstepping drive into the two phases to settle the rotor between full-step positions?",
                (
                    opt("Constant DC current in one phase"),
                    opt("Sine and cosine currents", correct=True),
                    opt("Trapezoidal back-EMF"),
                    opt("Random PWM pulses"),
                ),
                "Microstepping drives the two phases with sine and cosine currents, a slow open-loop version of the space-vector idea.",
            ),
        ),
        "Machine losses, efficiency & thermal limits": (
            q(
                "How do copper (I^2R) losses scale with load?",
                (
                    opt("Linearly with load"),
                    opt("With the square of the load (current squared)", correct=True),
                    opt("They stay fixed regardless of load"),
                    opt("Inversely with load"),
                ),
                "Copper losses scale with current squared, hence load squared, so they dominate at heavy load.",
            ),
            q(
                "Why does motor efficiency rise, peak, then fall as load increases?",
                (
                    opt("Because iron loss grows with load squared"),
                    opt(
                        "Because copper loss grows as load squared while fixed losses stay put",
                        correct=True,
                    ),
                    opt("Because slip increases with load"),
                    opt("Because the synchronous speed changes"),
                ),
                "Efficiency peaks where fixed losses equal copper loss; below that fixed losses dominate, above it copper loss grows as load squared.",
            ),
            q(
                "What ultimately sets a machine's continuous power rating?",
                (
                    opt("The magnetic flux density"),
                    opt(
                        "Heat, set by the insulation class winding-temperature limit", correct=True
                    ),
                    opt("The number of poles"),
                    opt("The supply frequency"),
                ),
                "Heat, not magnetics, sets continuous power: the insulation class sets the maximum winding temperature, and life halves for every ~10 C over rating.",
            ),
        ),
        "Lab: induction motor torque-speed & slip": (
            q(
                "In the lab, how is torque computed from the per-phase equivalent circuit?",
                (
                    opt("T = (3/ws) * V1^2 * (R2/s) / ((R1 + R2/s)^2 + (X1 + X2)^2)", correct=True),
                    opt("T = V1 * R2 * s"),
                    opt("T = (R1 + R2)/X2"),
                    opt("T = ws / (V1 * s)"),
                ),
                "The lab uses the Thevenin-free per-phase form T = (3/ws) * V1^2 * (R2/s) / ((R1 + R2/s)^2 + (X1 + X2)^2).",
            ),
            q(
                "With f = 50 Hz and poles = 4, what synchronous speed does the lab compute (ns = 120*f/poles)?",
                (
                    opt("3000 rpm"),
                    opt("1500 rpm", correct=True),
                    opt("1000 rpm"),
                    opt("750 rpm"),
                ),
                "ns = 120*f/poles = 120*50/4 = 1500 rpm.",
            ),
            q(
                "The lab suggests raising R2 to 0.8. What does that do to the breakdown torque location?",
                (
                    opt("Moves it toward synchronous speed"),
                    opt("Moves it toward standstill, giving more starting torque", correct=True),
                    opt("Removes the breakdown torque"),
                    opt("Has no effect on the curve"),
                ),
                "Raising R2 moves the breakdown point toward standstill (s = 1), increasing starting torque.",
            ),
        ),
    },
    final=(
        q(
            "Which statement correctly distinguishes an induction motor from a synchronous machine?",
            (
                opt("The induction rotor locks to the field with no slip"),
                opt(
                    "The synchronous rotor is a magnet and turns at exactly synchronous speed, while the induction rotor must slip",
                    correct=True,
                ),
                opt("Both run at exactly synchronous speed"),
                opt("The synchronous machine needs slip to produce torque"),
            ),
            "A synchronous machine has a magnet rotor that locks to the field at synchronous speed; an induction rotor must lag (slip) for the field to induce current.",
        ),
        q(
            "What is the combined role of the Clarke and Park transforms in motor control?",
            (
                opt("They increase the supply frequency"),
                opt(
                    "They repackage three AC phases into id/iq DC components to regulate flux and torque cleanly",
                    correct=True,
                ),
                opt("They eliminate copper losses"),
                opt("They convert DC to AC in the inverter"),
            ),
            "Clarke + Park turn three AC phase currents into DC d-q components (id for flux, iq for torque), letting an inverter regulate them like a DC motor's two knobs.",
        ),
        q(
            "Why can an EV motor deliver huge peak torque but a much lower continuous rating?",
            (
                opt("Because slip increases at high torque"),
                opt(
                    "Because the continuous rating is limited by how fast cooling pulls heat out of the copper",
                    correct=True,
                ),
                opt("Because the magnets demagnetize at low torque"),
                opt("Because the grid frequency drops under load"),
            ),
            "Peak torque is allowed for short bursts, but continuous power is set by thermal limits: how fast cooling removes heat from the windings.",
        ),
        q(
            "Which pair correctly matches a motor type to a typical application from the course?",
            (
                opt("Stepper motors spin EV traction drives"),
                opt(
                    "BLDC motors spin drones, fans, and power tools; steppers run 3D printer and CNC axes",
                    correct=True,
                ),
                opt("PMSM motors are used only as synchronous condensers"),
                opt("Induction motors are used only for open-loop positioning"),
            ),
            "BLDC motors drive drones, fans, hard drives, e-bikes and power tools; steppers give cheap open-loop precision for 3D printers and CNC axes.",
        ),
        q(
            "At what load angle does the synchronous power-angle curve P = (V*E/Xs) sin(delta) reach maximum, and what happens beyond it?",
            (
                opt("At 0 degrees; the machine speeds up"),
                opt(
                    "At 90 degrees; beyond it the machine loses synchronism (pole slip)",
                    correct=True,
                ),
                opt("At 180 degrees; beyond it efficiency peaks"),
                opt("At 45 degrees; beyond it slip becomes zero"),
            ),
            "P peaks at delta = 90 degrees; pushing past that causes loss of synchronism, known as pole slip.",
        ),
    ),
)
