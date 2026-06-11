from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Power system stability & the swing equation": (
            q(
                "In the swing equation, what does the inertia constant H represent?",
                (
                    opt("the mechanical input power Pm"),
                    opt("the stored kinetic energy per MVA", correct=True),
                    opt("the electrical output power Pe"),
                    opt("the line reactance X"),
                ),
                "H is the inertia constant, the stored kinetic energy of the rotating mass per MVA of rating.",
            ),
            q(
                "According to the swing equation, when does a generator rotor accelerate or decelerate?",
                (
                    opt("only when the line reactance X changes"),
                    opt("when frequency equals exactly 50 Hz"),
                    opt(
                        "when the mechanical power Pm differs from the electrical power Pe",
                        correct=True,
                    ),
                    opt("only during normal steady-state operation"),
                ),
                "When Pm is not equal to Pe the rotor accelerates or decelerates, which is the swing.",
            ),
            q(
                "Why is falling system inertia a concern as inverter-based renewables are added?",
                (
                    opt("inverters add too much spinning mass to the grid"),
                    opt(
                        "inverters have no spinning inertia, so total H falls and frequency moves faster after a disturbance",
                        correct=True,
                    ),
                    opt("inverters force the grid frequency above 60 Hz permanently"),
                    opt("inverters eliminate the need for protection entirely"),
                ),
                "Inverter-based renewables have no spinning inertia, lowering total H so frequency changes faster after a disturbance.",
            ),
        ),
        "The equal-area criterion": (
            q(
                "What is the stability condition stated by the equal-area criterion?",
                (
                    opt("the machine is stable if A2 is greater than or equal to A1", correct=True),
                    opt("the machine is stable if A1 is always greater than A2"),
                    opt("the machine is stable only if A1 equals zero"),
                    opt("the machine is stable if rotor angle stays below 30 degrees"),
                ),
                "Stability holds when the decelerating area A2 is at least as large as the accelerating area A1.",
            ),
            q(
                "What happens to the rotor during the fault, before the breaker clears it?",
                (
                    opt("it decelerates and gives back energy"),
                    opt(
                        "it accelerates and stores kinetic energy as the accelerating area A1",
                        correct=True,
                    ),
                    opt("it stays exactly at the steady angle delta0"),
                    opt("it instantly reaches the unstable equilibrium angle"),
                ),
                "When Pe drops below Pm the rotor accelerates and delta grows, building the accelerating area A1.",
            ),
            q(
                "The critical clearing angle directly sets which practical requirement?",
                (
                    opt("the nominal grid frequency of 50 or 60 Hz"),
                    opt("the per-unit base for line impedance"),
                    opt(
                        "the relay and breaker speed, e.g. clearing faults in 3-5 cycles",
                        correct=True,
                    ),
                    opt("the inertia constant H of every generator"),
                ),
                "The critical clearing time corresponding to the critical clearing angle sets relay and breaker speed, hence 3-5 cycle clearing.",
            ),
        ),
        "Frequency & load-frequency control": (
            q(
                "If generation exceeds load on a synchronous grid, what happens to frequency?",
                (
                    opt("frequency rises as machines speed up", correct=True),
                    opt("frequency falls as machines slow down"),
                    opt("frequency stays fixed regardless of balance"),
                    opt("frequency drops to zero immediately"),
                ),
                "Excess generation speeds the machines up, so frequency rises; frequency is a direct readout of power balance.",
            ),
            q(
                "What does a 5 percent governor droop R mean?",
                (
                    opt(
                        "a 5 percent frequency drop calls for 100 percent more output", correct=True
                    ),
                    opt("the generator output never changes with frequency"),
                    opt("a 100 percent frequency drop calls for 5 percent more output"),
                    opt("frequency must stay within 5 Hz of nominal"),
                ),
                "Droop R is the percent frequency change for a 100 percent power change, so 5 percent droop means a 5 percent frequency drop calls for 100 percent more output.",
            ),
            q(
                "What is the job of secondary control (AGC) compared to primary governor droop?",
                (
                    opt("it arrests the frequency drop within seconds"),
                    opt(
                        "it restores frequency to exactly 50/60 Hz and returns interchange to schedule over minutes",
                        correct=True,
                    ),
                    opt("it physically opens breakers during a fault"),
                    opt("it replaces the need for spinning reserve"),
                ),
                "AGC is the slow secondary layer that restores nominal frequency and returns scheduled interchange over minutes.",
            ),
        ),
        "Renewable integration: inverters, the duck curve & grid codes": (
            q(
                "Why does a standard grid-tied inverter provide no natural inertia?",
                (
                    opt("it runs at a different frequency than the grid"),
                    opt("it has no rotating mass unless programmed to mimic it", correct=True),
                    opt("it converts AC to DC only"),
                    opt("it always trips during voltage dips"),
                ),
                "An inverter has no rotating mass, so it provides no natural inertia unless made grid-forming with synthetic inertia.",
            ),
            q(
                "What is the duck curve?",
                (
                    opt(
                        "net load (demand minus solar) that dips at midday then ramps steeply at sunset",
                        correct=True,
                    ),
                    opt("the rotor-angle swing after a fault"),
                    opt("the power-angle curve of a synchronous machine"),
                    opt("the cost of HVDC versus AC over distance"),
                ),
                "The duck curve is net load shaped like a duck: a deep midday belly from solar and a steep evening ramp.",
            ),
            q(
                "Which behavior does a grid-code fault ride-through requirement enforce?",
                (
                    opt("renewables must trip off instantly at any voltage dip"),
                    opt(
                        "renewables must stay connected through brief voltage dips instead of all tripping at once",
                        correct=True,
                    ),
                    opt("renewables must always run at maximum output"),
                    opt("renewables must convert their output to DC"),
                ),
                "Fault ride-through requires plants to stay connected through brief voltage dips so they do not all trip and crash frequency.",
            ),
        ),
        "HVDC & FACTS: power-electronic grid control": (
            q(
                "Which capability is unique to HVDC and impossible for AC?",
                (
                    opt("transforming voltage up and down"),
                    opt("an asynchronous tie linking grids at different frequencies", correct=True),
                    opt("carrying reactive power across a transformer"),
                    opt("providing spinning inertia to the grid"),
                ),
                "HVDC can form an asynchronous tie between grids at different frequencies or out of phase, which AC cannot do.",
            ),
            q(
                "Why is HVDC preferred for long undersea cables?",
                (
                    opt("DC cables are cheaper to manufacture than any AC cable"),
                    opt(
                        "AC cable charging current would consume all the capacity, while DC has no charging current",
                        correct=True,
                    ),
                    opt("undersea cables require no converters at all"),
                    opt("DC eliminates the need for grid codes"),
                ),
                "AC cable capacitance draws charging current that consumes capacity over distance; HVDC has no charging current, making it the choice for long undersea cables.",
            ),
            q(
                "What does a FACTS device such as a STATCOM do?",
                (
                    opt("converts bulk power from AC to DC for long-haul transport"),
                    opt(
                        "injects controllable reactive power or voltage to steer flow and stabilize voltage",
                        correct=True,
                    ),
                    opt("provides mechanical inertia from a spinning rotor"),
                    opt("sets the nominal system frequency"),
                ),
                "FACTS devices inject controllable reactive power or voltage into an AC line to steer flow and stabilize voltage faster than mechanical switches.",
            ),
        ),
        "The smart grid: metering, demand response & microgrids": (
            q(
                "What do PMUs (phasor measurement units) provide to grid operators?",
                (
                    opt("monthly meter readings for billing"),
                    opt(
                        "GPS-synchronized voltage/current phasor samples 30-60 times a second for a wide-area picture",
                        correct=True,
                    ),
                    opt("automatic conversion of AC to DC"),
                    opt("governor droop response within seconds"),
                ),
                "PMUs sample phasors GPS-synchronized 30-60 times a second, giving operators a live wide-area picture (a WAMS).",
            ),
            q(
                "What does demand response do in the smart grid?",
                (
                    opt("it only matches generation to a fixed demand"),
                    opt(
                        "it flexes demand to match supply by shifting consumption to cheap/abundant hours",
                        correct=True,
                    ),
                    opt("it disconnects all renewables during peaks"),
                    opt("it replaces transmission lines with HVDC"),
                ),
                "Demand response flexes demand to match supply, shifting loads like thermostats and EV chargers to cheap or abundant hours.",
            ),
            q(
                "What defines a microgrid?",
                (
                    opt("a single large central power plant feeding passive consumers"),
                    opt(
                        "a local cluster of generation, storage, and load that can island during an outage",
                        correct=True,
                    ),
                    opt("a long-distance HVDC transmission corridor"),
                    opt("a phasor measurement unit on the transmission system"),
                ),
                "A microgrid is a local cluster of generation, storage, and load that can run grid-connected or disconnect and run as an island.",
            ),
        ),
        "Lab: swing equation, equal-area & governor droop": (
            q(
                "In the lab, what change to the fault clearing time makes the rotor swing past recovery (unstable)?",
                (
                    opt("pushing fault_off to 0.4 s", correct=True),
                    opt("setting Pmax to 2.0"),
                    opt("setting H to 4.0"),
                    opt("setting ws to 2 pi 60"),
                ),
                "The lab notes that pushing fault_off to 0.4 s makes the rotor swing past recovery and go unstable.",
            ),
            q(
                "How is the steady rotor angle delta0 computed in the lab?",
                (
                    opt("np.arcsin(Pm/Pmax)", correct=True),
                    opt("np.arccos(Pm/Pmax)"),
                    opt("np.pi minus Pm"),
                    opt("ws divided by 2H"),
                ),
                "delta0 = np.arcsin(Pm/Pmax) gives the steady rotor angle where Pm meets Pe.",
            ),
            q(
                "When two units with different droop share a load increase, what do they share in common?",
                (
                    opt("the same mechanical power Pm"),
                    opt("the same common frequency deviation df", correct=True),
                    opt("the same inertia constant H"),
                    opt("the same critical clearing angle"),
                ),
                "Both units settle to one common frequency deviation df, and each picks up power as -df/R according to its droop.",
            ),
        ),
        "Applications, use cases & the throughline": (
            q(
                "In the worked thread of surviving a generator trip, what acts first after frequency falls?",
                (
                    opt(
                        "governor droop on every machine picks up the deficit within seconds",
                        correct=True,
                    ),
                    opt("microgrids island the entire grid immediately"),
                    opt("HVDC converters shut down all renewables"),
                    opt("smart meters send monthly bills"),
                ),
                "Governor droop on every machine picks up the deficit within seconds to arrest the dip, then AGC restores nominal over minutes.",
            ),
            q(
                "According to the lesson, what is the grand challenge reshaping the grid?",
                (
                    opt(
                        "decarbonization, rebuilding the grid around inverter-based renewables",
                        correct=True,
                    ),
                    opt("eliminating all transmission lines"),
                    opt("returning to one-way power flow from big plants"),
                    opt("removing protection from the grid"),
                ),
                "The grand challenge is decarbonization: rebuilding the grid around inverter-based renewables with falling inertia, the duck curve, storage, HVDC, and a smart grid.",
            ),
            q(
                "Which tool is used to flag an overloaded line during contingency analysis?",
                (
                    opt("the swing equation integrated in real time"),
                    opt("power-flow / contingency tools run on the Ybus", correct=True),
                    opt("smart meters reporting consumption"),
                    opt("governor droop curves"),
                ),
                "Power-flow and contingency tools run on the Ybus flag overloaded lines so operators can reroute, helped by FACTS flow control.",
            ),
        ),
    },
    final=(
        q(
            "Which quantity is the shared, system-wide readout of power balance on a synchronous grid?",
            (
                opt("the rotor angle delta of one machine"),
                opt("the grid frequency", correct=True),
                opt("the line reactance X"),
                opt("the inertia constant H"),
            ),
            "Frequency is shared by every connected machine and is a direct readout of generation-versus-load balance.",
        ),
        q(
            "The equal-area criterion judges transient stability by comparing what?",
            (
                opt(
                    "the accelerating area A1 against the decelerating area A2 under the power-angle curve",
                    correct=True,
                ),
                opt("the mechanical power against the inertia constant"),
                opt("the droop of two competing governors"),
                opt("the cost of HVDC against AC over distance"),
            ),
            "It compares the accelerating area A1 to the decelerating area A2; the machine stays in step if A2 is at least A1.",
        ),
        q(
            "Why does adding inverter-based renewables make grid frequency move faster after a disturbance?",
            (
                opt("inverters increase the line reactance"),
                opt("inverters lack spinning inertia, lowering total system H", correct=True),
                opt("inverters raise the nominal frequency above 60 Hz"),
                opt("inverters force AGC to act within seconds"),
            ),
            "Inverters have no rotating mass, so total system inertia H falls and frequency changes faster after a disturbance.",
        ),
        q(
            "Which technology can tie together two grids running at different frequencies?",
            (
                opt("a FACTS SVC"),
                opt("a tap-changing transformer"),
                opt("an HVDC link as an asynchronous tie", correct=True),
                opt("governor droop control"),
            ),
            "HVDC forms an asynchronous tie linking grids at different frequencies or out of phase, which AC cannot do.",
        ),
        q(
            "In the smart grid, demand response improves reliability by doing what?",
            (
                opt("shifting consumption to cheap/abundant hours to shave peaks", correct=True),
                opt("permanently disconnecting all consumers from the grid"),
                opt("converting all generation to DC"),
                opt("removing the need for spinning reserve and AGC"),
            ),
            "Demand response flexes load to match supply, shifting consumption to cheap or abundant hours and shaving peaks, deferring new plant construction.",
        ),
    ),
)
