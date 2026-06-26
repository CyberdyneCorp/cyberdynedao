"""Quiz questions for the Physics for Life Sciences - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why physics for living systems": (
            q(
                "What does the thermal energy scale kB*T represent in biophysics?",
                (
                    opt("The reference energy currency for molecular events", correct=True),
                    opt("The total energy stored in a cell"),
                    opt("The activation energy of every enzyme"),
                    opt("The electrical potential of a neuron"),
                ),
                "kB*T (~4.1e-21 J at body temperature) is the scale against which molecular energies are judged.",
            ),
            q(
                "Roughly how does metabolic rate scale with body mass (Kleiber's law)?",
                (
                    opt("As mass to the 3/4 power", correct=True),
                    opt("Linearly with mass"),
                    opt("As mass squared"),
                    opt("Independently of mass"),
                ),
                "Kleiber's law: metabolic rate scales as mass^(3/4) across many orders of magnitude.",
            ),
            q(
                "Why is dimensional analysis useful before solving a biophysics problem?",
                (
                    opt("It checks unit consistency and reveals scaling laws", correct=True),
                    opt("It gives the exact numerical answer"),
                    opt("It replaces the need for experiments"),
                    opt("It proves causation"),
                ),
                "Checking units catches errors and often exposes how quantities scale with each other.",
            ),
        ),
        "Forces, torques and the body as a lever": (
            q(
                "The torque produced by a force is given by:",
                (
                    opt("tau = r*F*sin(theta)", correct=True),
                    opt("tau = F/r"),
                    opt("tau = r + F"),
                    opt("tau = m*a"),
                ),
                "Torque is the product of the force, its distance from the pivot, and sin of the angle.",
            ),
            q(
                "Most skeletal joints (e.g. the elbow holding a weight) act as which class of lever?",
                (
                    opt("Third-class lever", correct=True),
                    opt("First-class lever"),
                    opt("A frictionless pulley"),
                    opt("A hydraulic press"),
                ),
                "In a third-class lever the effort (muscle) sits between the fulcrum and the load.",
            ),
            q(
                "Why must the biceps exert a force much larger than the weight held in the hand?",
                (
                    opt(
                        "Its short moment arm trades force for speed and range of motion",
                        correct=True,
                    ),
                    opt("Muscle force is always 10x the load by definition"),
                    opt("Bones absorb most of the load"),
                    opt("Gravity is amplified at the elbow"),
                ),
                "The muscle's short lever arm is a mechanical disadvantage in force but an advantage in motion.",
            ),
        ),
        "Energy, work and metabolic power": (
            q(
                "What is the approximate basal metabolic power of a resting human?",
                (
                    opt("About 100 W", correct=True),
                    opt("About 1 W"),
                    opt("About 10 kW"),
                    opt("About 0.1 W"),
                ),
                "A resting human dissipates roughly 100 W, comparable to a bright incandescent bulb.",
            ),
            q(
                "Approximately how efficient is skeletal muscle at converting metabolic energy to work?",
                (
                    opt("About 20-25%", correct=True),
                    opt("About 90%"),
                    opt("About 100%"),
                    opt("About 1%"),
                ),
                "Muscle efficiency is only ~20-25%; the rest becomes heat, warming you during exercise.",
            ),
            q(
                "What is the immediate chemical energy currency hydrolyzed to power cellular work?",
                (
                    opt("ATP", correct=True),
                    opt("Glucose only"),
                    opt("Oxygen"),
                    opt("DNA"),
                ),
                "ATP hydrolysis releases roughly 50-60 kJ/mol under cellular conditions.",
            ),
        ),
        "Fluids at rest: pressure and buoyancy": (
            q(
                "Hydrostatic pressure in a fluid at rest varies with depth as:",
                (
                    opt("P = P0 + rho*g*h", correct=True),
                    opt("P = P0 - rho/h"),
                    opt("P = rho*g/h"),
                    opt("P is constant with depth"),
                ),
                "Pressure rises linearly with depth: each unit of depth adds rho*g*h.",
            ),
            q(
                "Archimedes' principle states the buoyant force equals:",
                (
                    opt("The weight of the fluid displaced", correct=True),
                    opt("The weight of the object"),
                    opt("The object's surface area times pressure"),
                    opt("Zero for any submerged object"),
                ),
                "Buoyant force = rho_fluid * V * g, the weight of displaced fluid.",
            ),
            q(
                "Why does standing blood pressure differ between your feet and your head?",
                (
                    opt("The hydrostatic column of blood adds pressure with depth", correct=True),
                    opt("Blood is denser in the feet"),
                    opt("The heart pumps only downward"),
                    opt("Gravity does not affect fluids"),
                ),
                "A ~1.3 m column of blood adds roughly 100 mmHg at the feet versus the head.",
            ),
        ),
        "Fluids in motion: flow and circulation": (
            q(
                "In Poiseuille's law, flow rate Q depends on vessel radius as:",
                (
                    opt("Q proportional to r^4", correct=True),
                    opt("Q proportional to r"),
                    opt("Q proportional to r^2"),
                    opt("Q independent of r"),
                ),
                "Q = pi*r^4*deltaP/(8*eta*L): the fourth power of radius makes vascular tone powerful.",
            ),
            q(
                "The continuity equation A1*v1 = A2*v2 implies a fluid does what through a constriction?",
                (
                    opt("Speeds up", correct=True),
                    opt("Slows down"),
                    opt("Stops"),
                    opt("Changes density"),
                ),
                "Conserving volume flow, smaller area means higher velocity.",
            ),
            q(
                "Bernoulli's principle relates, along a streamline, a rise in speed to:",
                (
                    opt("A drop in pressure", correct=True),
                    opt("A rise in pressure"),
                    opt("A rise in density"),
                    opt("No change at all"),
                ),
                "P + 0.5*rho*v^2 + rho*g*h is constant, so faster flow means lower pressure.",
            ),
        ),
        "Thermal energy and the scale of molecular life": (
            q(
                "The Boltzmann factor giving the relative population of a state at energy E is:",
                (
                    opt("exp(-E/kB*T)", correct=True),
                    opt("E/kB*T"),
                    opt("kB*T/E"),
                    opt("exp(+E/kB*T)"),
                ),
                "Higher-energy states are exponentially less populated, by exp(-E/kB*T).",
            ),
            q(
                "Roughly what is kB*T at body temperature (310 K)?",
                (
                    opt("About 4e-21 J (~0.6 kcal/mol)", correct=True),
                    opt("About 4 J"),
                    opt("About 1 eV"),
                    opt("About 100 kJ/mol"),
                ),
                "kB*T is approximately 4.1e-21 J, the yardstick for molecular energies.",
            ),
            q(
                "The equipartition theorem assigns how much energy to each quadratic degree of freedom?",
                (
                    opt("(1/2) kB*T", correct=True),
                    opt("kB*T"),
                    opt("2 kB*T"),
                    opt("Zero"),
                ),
                "Each quadratic degree of freedom carries (1/2) kB*T of thermal energy.",
            ),
        ),
    },
    final=(
        q(
            "Which single quantity is the reference 'currency' for molecular biophysics?",
            (
                opt("kB*T, the thermal energy", correct=True),
                opt("The speed of light"),
                opt("Avogadro's number"),
                opt("The gas constant alone"),
            ),
            "kB*T sets the scale against which binding energies and barriers are compared.",
        ),
        q(
            "A skeletal joint acting as a third-class lever provides:",
            (
                opt("Mechanical disadvantage in force but advantage in speed/range", correct=True),
                opt("Mechanical advantage in force"),
                opt("Perfect efficiency"),
                opt("No torque at all"),
            ),
            "Short muscle moment arms cost force to gain hand speed and range of motion.",
        ),
        q(
            "Skeletal muscle converts metabolic energy to mechanical work at roughly:",
            (
                opt("20-25% efficiency", correct=True),
                opt("0% efficiency"),
                opt("50% efficiency"),
                opt("99% efficiency"),
            ),
            "The remaining ~75% is dissipated as heat.",
        ),
        q(
            "Halving the radius of a blood vessel changes Poiseuille flow by a factor of:",
            (
                opt("1/16", correct=True),
                opt("1/2"),
                opt("1/4"),
                opt("1/8"),
            ),
            "Flow scales as r^4, so halving radius gives (1/2)^4 = 1/16.",
        ),
        q(
            "Hydrostatic pressure increases by about one atmosphere for every:",
            (
                opt("10 m of water depth", correct=True),
                opt("1 m of water depth"),
                opt("100 m of water depth"),
                opt("1 cm of water depth"),
            ),
            "rho*g*h gives roughly 100 kPa (~1 atm) per 10 m of water.",
        ),
        q(
            "Why must large organisms rely on bulk transport rather than diffusion over long distances?",
            (
                opt("Diffusion time scales as distance squared, becoming too slow", correct=True),
                opt("Diffusion violates conservation of mass"),
                opt("Diffusion only works for gases"),
                opt("Diffusion needs ATP at every step"),
            ),
            "Since <x^2> ~ 2Dt, diffusing a metre would take impractically long; hence circulation.",
        ),
    ),
)
