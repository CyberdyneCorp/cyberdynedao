from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Advanced state estimation: EKF & observers": (
            q(
                "Why is the extended Kalman filter (rather than a plain linear Kalman filter) the tool for model-based SoC estimation?",
                (
                    opt("Because terminal voltage is never measured directly"),
                    opt(
                        "Because OCV(SoC) is nonlinear and must be linearized at the current estimate",
                        correct=True,
                    ),
                    opt("Because the RC model has no hidden states"),
                    opt("Because coulomb counting is exact and needs no correction"),
                ),
                "OCV(SoC) is nonlinear, so the EKF linearizes it at the current estimate; its slope enters the measurement Jacobian.",
            ),
            q(
                "In the predict-correct loop, what is the innovation that drives the correction step?",
                (
                    opt(
                        "The difference between measured and predicted terminal voltage",
                        correct=True,
                    ),
                    opt("The product of the Kalman gain and the process noise"),
                    opt("The integral of current over the timestep"),
                    opt("The slope of OCV with respect to temperature"),
                ),
                "The innovation is measured minus predicted voltage; the state is nudged by the Kalman gain times this innovation.",
            ),
            q(
                "Why do LFP fuel gauges lean harder on coulomb counting and rest-OCV re-anchoring than the EKF?",
                (
                    opt("LFP cells have no equivalent-circuit model"),
                    opt(
                        "The OCV slope is nearly zero on the flat LFP plateau, so voltage tells the filter almost nothing about SoC",
                        correct=True,
                    ),
                    opt("LFP cells cannot be measured for terminal voltage"),
                    opt("The Kalman gain is always zero for LFP chemistry"),
                ),
                "On a flat LFP plateau the OCV slope is near zero, so the EKF gets little SoC information from voltage.",
            ),
        ),
        "Thermal modeling & management": (
            q(
                "A serious BMS runs a thermal model alongside the electrical one because the two are coupled. How?",
                (
                    opt("Heat raises resistance and resistance generates heat", correct=True),
                    opt("Cooling increases the cell capacity directly"),
                    opt("Voltage measurement requires a temperature sensor"),
                    opt("The entropic term always cancels the Joule term"),
                ),
                "They form an electro-thermal model: heat raises resistance and resistance generates heat, so each feeds the other.",
            ),
            q(
                "Of the two heat-generation sources, which dominates at high current?",
                (
                    opt("The reversible entropic term I*T*dU/dT"),
                    opt("The irreversible Joule term I^2*R0", correct=True),
                    opt("The Newton cooling term h*A*(T - Tcoolant)"),
                    opt("The thermal mass term m*cp"),
                ),
                "The irreversible I^2*R0 term dominates at high current; the entropic term can heat or cool depending on direction.",
            ),
            q(
                "What is the primary control target for thermal management across a pack, beyond average temperature?",
                (
                    opt("Maximizing the steady-state temperature"),
                    opt("Cell-to-cell temperature uniformity within a few degrees", correct=True),
                    opt("Eliminating all coolant flow"),
                    opt("Keeping the pack below freezing at all times"),
                ),
                "The control target is uniformity, keeping cell-to-cell spread within a few degrees so the pack ages evenly.",
            ),
        ),
        "Fast charging & charging strategies": (
            q(
                "In the standard CC-CV profile, what happens during the CV phase?",
                (
                    opt("Voltage climbs while current is held fixed"),
                    opt(
                        "Voltage is held at the limit while current tapers exponentially",
                        correct=True,
                    ),
                    opt("Both voltage and current are held constant"),
                    opt("Current is increased to speed up the last 20 percent"),
                ),
                "In CV the voltage is held at the limit and the current tapers exponentially as the cell fills.",
            ),
            q(
                "What physically happens above the lithium-plating threshold, and why does it matter?",
                (
                    opt("Lithium intercalates safely with no consequence"),
                    opt(
                        "Metallic lithium plates on the anode, causing irreversible capacity loss and a safety hazard",
                        correct=True,
                    ),
                    opt("The cell voltage rises above 4.2 V harmlessly"),
                    opt("Round-trip efficiency improves"),
                ),
                "Above the plating threshold metallic lithium plates on the anode, which is irreversible capacity loss and a safety hazard.",
            ),
            q(
                "Why is the last 20 percent of an EV charge deliberately slow compared with the 10-80 percent region?",
                (
                    opt("The chemistry hits an absolute C-rate ceiling at 80 percent"),
                    opt("The CV tail tapers current to protect the cell as it fills", correct=True),
                    opt("The charger runs out of power above 80 percent"),
                    opt("The BMS shuts off cooling near full charge"),
                ),
                "The 10-80 percent is the fast CC region; the last 20 percent is the slow CV taper deliberately shaped to protect the cell.",
            ),
        ),
        "Grid & stationary storage": (
            q(
                "Which grid service operates on a seconds time scale to hold frequency at 50/60 Hz?",
                (
                    opt("Peak shaving"),
                    opt("Frequency regulation", correct=True),
                    opt("Renewable firming"),
                    opt("Black start"),
                ),
                "Frequency regulation acts on a seconds time scale, injecting or absorbing power to hold grid frequency at nominal.",
            ),
            q(
                "How does a BESS perform peak shaving?",
                (
                    opt("It charges during the daily peak and discharges off-peak"),
                    opt(
                        "It charges during cheap off-peak hours and discharges to cover the daily peak",
                        correct=True,
                    ),
                    opt("It only injects power during outages"),
                    opt("It runs at constant power all day to flatten frequency"),
                ),
                "Peak shaving charges during cheap off-peak hours and discharges to cover the costly daily peak.",
            ),
            q(
                "Why does LFP dominate grid and stationary storage rather than high-energy-density chemistries?",
                (
                    opt("Because energy density matters most when the battery sits in a field"),
                    opt(
                        "Because cost per kWh, cycle life, round-trip efficiency, and safety matter more than density",
                        correct=True,
                    ),
                    opt("Because LFP has the highest specific energy of all chemistries"),
                    opt("Because grid storage must be carried by hand"),
                ),
                "Nobody carries grid storage, so density barely matters; cost per kWh, cycle life, RTE, and safety dominate, which favors LFP.",
            ),
        ),
        "Second life, recycling & alternatives": (
            q(
                "Why can an 80 percent-SoH EV pack still serve a useful second life?",
                (
                    opt(
                        "It is suited to less demanding jobs like stationary storage where weight and peak power matter less",
                        correct=True,
                    ),
                    opt("It regains capacity once removed from the vehicle"),
                    opt("It can only be used for high-power racing applications"),
                    opt("It is immediately recycled with no further use"),
                ),
                "An 80 percent-SoH pack still holds most of its energy and fits less demanding jobs like stationary storage and backup.",
            ),
            q(
                "What is the key advantage of a flow battery for multi-hour grid storage?",
                (
                    opt("It has the highest energy density of any technology"),
                    opt(
                        "Power (stack) and energy (tank volume) can be sized independently",
                        correct=True,
                    ),
                    opt("It charges and discharges in seconds like a supercapacitor"),
                    opt("It requires no electrolyte"),
                ),
                "Flow batteries pump electrolyte from tanks through a cell stack, so power and energy are sized independently by stack and tank volume.",
            ),
            q(
                "What distinguishes a supercapacitor from a battery in the power-energy tradeoff?",
                (
                    opt("It stores far more energy per kilogram than a battery"),
                    opt(
                        "It stores charge physically, giving huge power and about a million cycles but little energy",
                        correct=True,
                    ),
                    opt("It relies on slow chemistry to deliver bulk energy"),
                    opt("It cannot be paired with a battery"),
                ),
                "A supercapacitor stores charge physically, so it has huge power and roughly a million cycles but holds little energy.",
            ),
        ),
        "Lab: EKF SoC estimator with a thermal check": (
            q(
                "In the lab, what is special about the EKF's initial state x = [0.60, 0.0]?",
                (
                    opt("It is the exact true SoC of 0.80"),
                    opt(
                        "It is a deliberately wrong initial SoC guess that the filter must converge from",
                        correct=True,
                    ),
                    opt("It disables the thermal trace"),
                    opt("It sets the measurement noise to zero"),
                ),
                "The EKF starts from a wrong SoC of 0.60 while the true SoC is 0.80, demonstrating convergence to the truth.",
            ),
            q(
                "How does the lab compute the OCV slope (dOCV) used in the measurement Jacobian H?",
                (
                    opt("Analytically from a closed-form OCV equation"),
                    opt(
                        "Numerically, by interpolating OCV at x[0] plus and minus 1e-3 and dividing by 2e-3",
                        correct=True,
                    ),
                    opt("By assuming a constant slope of 1.0"),
                    opt("From the thermal trace temperature"),
                ),
                "The lab takes a numeric central difference of the interpolated OCV around x[0] over 2e-3 to get dOCV.",
            ),
            q(
                "What does raising Rn (the measurement noise) do in the suggested experiment?",
                (
                    opt("It makes the EKF distrust the model and converge instantly"),
                    opt(
                        "It makes the filter trust the model more, so convergence slows and rides through noise",
                        correct=True,
                    ),
                    opt("It increases the cell capacity Q_Ah"),
                    opt("It removes the thermal trace from the plot"),
                ),
                "Raising Rn trusts the model more relative to the sensor, so convergence slows and the estimate rides through measurement noise.",
            ),
        ),
        "Applications & the throughline": (
            q(
                "For an EV pack, which set of priorities does the application balance?",
                (
                    opt(
                        "Energy, power, safety, and life in a weight- and volume-constrained box",
                        correct=True,
                    ),
                    opt("Cost and cycle life only, with weight being free"),
                    opt("Energy density per gram alone, ignoring safety"),
                    opt("Round-trip efficiency only, ignoring power"),
                ),
                "An EV pack balances energy (range), power, safety, and life within a weight- and volume-constrained box.",
            ),
            q(
                "What single number is described as the cost-per-cycle throughline tying the field together?",
                (
                    opt("The peak terminal voltage of a single cell"),
                    opt(
                        "The effective cost of stored energy over the life of the pack",
                        correct=True,
                    ),
                    opt("The maximum charge C-rate"),
                    opt("The cell-to-cell temperature spread"),
                ),
                "The throughline is the effective cost of stored energy over the pack's life: capital cost spread across all energy delivered.",
            ),
            q(
                "According to the lesson, what drives the lifetime cost per delivered kWh down?",
                (
                    opt("Shorter cycle life and lower round-trip efficiency"),
                    opt("Longer cycle life and higher round-trip efficiency", correct=True),
                    opt("Higher pack price and more frequent charging"),
                    opt("Lower energy density and more weight"),
                ),
                "Longer cycle life and higher round-trip efficiency both lower the cost per delivered kWh, which is why EV and grid makers obsess over them.",
            ),
        ),
    },
    final=(
        q(
            "Across the track, what is the EKF's core mechanism for correcting an SoC estimate?",
            (
                opt(
                    "It linearizes nonlinear OCV(SoC) and corrects via Kalman gain times the voltage innovation",
                    correct=True,
                ),
                opt("It integrates current only, ignoring terminal voltage"),
                opt("It averages OCV and coulomb counting with fixed weights"),
                opt("It uses the thermal model to set the SoC directly"),
            ),
            "The EKF linearizes OCV(SoC), forms an innovation from measured minus predicted voltage, and corrects by the Kalman gain.",
        ),
        q(
            "Why is fast charging described as fundamentally a thermal problem?",
            (
                opt("Because the entropic term is the only heat source"),
                opt(
                    "Because the I^2*R0 heat is large at high current and the sustainable charge rate is set by how fast heat can be removed",
                    correct=True,
                ),
                opt("Because cooling raises the plating threshold to infinity"),
                opt("Because the CV phase generates the most heat"),
            ),
            "Fast charging draws huge current, so I^2*R0 heat is large; the sustainable rate is usually limited by heat removal, not chemistry.",
        ),
        q(
            "Which technology lets you size power and energy independently, making it ideal for long-duration grid storage?",
            (
                opt("Supercapacitor"),
                opt("Flow battery", correct=True),
                opt("Solid-state lithium"),
                opt("High-energy NMC cell"),
            ),
            "Flow batteries decouple power (stack) and energy (tank volume), so scaling energy is just bigger tanks.",
        ),
        q(
            "What set of priorities dominates grid and stationary storage decisions?",
            (
                opt("Energy density per gram and pocket safety"),
                opt("Cost per kWh, cycle life, round-trip efficiency, and safety", correct=True),
                opt("Acceleration power and fast-charge speed"),
                opt("Minimizing pack volume above all else"),
            ),
            "Grid storage flips consumer priorities: weight is free, so cost per kWh, cycle life, RTE, and safety dominate, favoring LFP.",
        ),
        q(
            "What is the stated throughline of the whole track?",
            (
                opt("Only chemistry choice matters; the engineering changes completely with scale"),
                opt(
                    "Model it, estimate it, protect it, cool it, and account for its life; the engineering does not change with chemistry or scale",
                    correct=True,
                ),
                opt("Coulomb counting alone suffices for every application"),
                opt("Energy density is the single metric that governs all batteries"),
            ),
            "The chemistry and scale change, but the engineering -- model it, estimate it, protect it, cool it, and account for its life -- does not.",
        ),
    ),
)
