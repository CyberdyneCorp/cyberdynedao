"""Quiz questions for the Physics for Life Sciences - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Thermodynamics and free energy in cells": (
            q(
                "A chemical process is spontaneous (proceeds forward) when:",
                (
                    opt("delta G < 0", correct=True),
                    opt("delta G > 0"),
                    opt("delta H = 0"),
                    opt("delta S = 0"),
                ),
                "Spontaneity is governed by the sign of the Gibbs free energy change.",
            ),
            q(
                "How do cells drive an endergonic reaction forward?",
                (
                    opt(
                        "By coupling it to ATP hydrolysis so the total delta G is negative",
                        correct=True,
                    ),
                    opt("By violating the second law of thermodynamics"),
                    opt("By lowering the temperature to zero"),
                    opt("By removing all enzymes"),
                ),
                "Coupling an unfavorable reaction to ATP hydrolysis makes the combined delta G negative.",
            ),
            q(
                "At equilibrium, the standard free energy relates to K_eq by:",
                (
                    opt("delta G-standard = -R*T*ln(K_eq)", correct=True),
                    opt("delta G-standard = R*T*K_eq"),
                    opt("delta G-standard = K_eq / RT"),
                    opt("delta G-standard = 0 always"),
                ),
                "At equilibrium delta G = 0, giving delta G-standard = -RT ln K_eq.",
            ),
        ),
        "Diffusion and random walks": (
            q(
                "Fick's first law states the diffusive flux is proportional to:",
                (
                    opt("The negative concentration gradient", correct=True),
                    opt("The concentration itself"),
                    opt("Time"),
                    opt("The square of concentration"),
                ),
                "J = -D dC/dx: flux flows down the concentration gradient.",
            ),
            q(
                "In a random walk, the mean-square displacement grows with time as:",
                (
                    opt("Linearly: <x^2> = 2*D*t", correct=True),
                    opt("Quadratically with time"),
                    opt("Independently of time"),
                    opt("Exponentially with time"),
                ),
                "RMS displacement grows as sqrt(t), so mean-square displacement is linear in t.",
            ),
            q(
                "The Stokes-Einstein relation says the diffusion coefficient D is:",
                (
                    opt("Larger for smaller molecules in less viscous fluid", correct=True),
                    opt("Independent of molecule size"),
                    opt("Larger for larger molecules"),
                    opt("Zero at body temperature"),
                ),
                "D = kB*T/(6*pi*eta*r): smaller radius and lower viscosity give faster diffusion.",
            ),
        ),
        "Membranes, osmosis and transport": (
            q(
                "Osmotic pressure of a dilute solution is given (van 't Hoff) by:",
                (
                    opt("Pi = i*c*R*T", correct=True),
                    opt("Pi = c/RT"),
                    opt("Pi = R*T/c"),
                    opt("Pi = i + c + RT"),
                ),
                "Osmotic pressure rises with the concentration of dissolved particles.",
            ),
            q(
                "The Na+/K+-ATPase is an example of which type of transport?",
                (
                    opt("Active transport (ATP-driven, uphill)", correct=True),
                    opt("Simple diffusion"),
                    opt("Facilitated diffusion"),
                    opt("Osmosis"),
                ),
                "It pumps ions against their gradients at the cost of ATP: 3 Na+ out, 2 K+ in.",
            ),
            q(
                "A cell placed in a hypotonic solution will:",
                (
                    opt("Swell as water enters", correct=True),
                    opt("Shrink as water leaves"),
                    opt("Stay exactly the same"),
                    opt("Lose all its ions instantly"),
                ),
                "Water moves into the cell down its chemical potential, swelling it.",
            ),
        ),
        "Enzyme kinetics: Michaelis-Menten": (
            q(
                "In the Michaelis-Menten equation, K_m is:",
                (
                    opt("The substrate concentration giving half-maximal rate", correct=True),
                    opt("The maximum reaction velocity"),
                    opt("The total enzyme concentration"),
                    opt("The catalytic turnover number"),
                ),
                "K_m is [S] at which v = Vmax/2, an apparent affinity measure.",
            ),
            q(
                "At very high substrate concentration, the reaction rate:",
                (
                    opt("Plateaus at Vmax because enzymes are saturated", correct=True),
                    opt("Increases without bound"),
                    opt("Drops to zero"),
                    opt("Becomes negative"),
                ),
                "When all enzyme is occupied, rate saturates at Vmax = k_cat*[E]0.",
            ),
            q(
                "The specificity constant gauging catalytic efficiency is:",
                (
                    opt("k_cat / K_m", correct=True),
                    opt("K_m / k_cat"),
                    opt("Vmax * K_m"),
                    opt("k_cat * Vmax"),
                ),
                "k_cat/K_m measures how efficiently an enzyme converts substrate at low [S].",
            ),
        ),
        "Bioelectricity: Nernst and membrane potentials": (
            q(
                "The Nernst equation gives the equilibrium potential of an ion from:",
                (
                    opt("The log of its outside/inside concentration ratio", correct=True),
                    opt("The membrane thickness only"),
                    opt("The total ATP concentration"),
                    opt("The cell volume"),
                ),
                "E = (RT/zF) ln([out]/[in]) sets the equilibrium voltage for that ion.",
            ),
            q(
                "When several ions are permeant, the resting potential is best given by:",
                (
                    opt("The Goldman-Hodgkin-Katz equation weighting permeabilities", correct=True),
                    opt("The Nernst equation for Na+ alone"),
                    opt("Ohm's law"),
                    opt("The ideal gas law"),
                ),
                "GHK weights each ion by its permeability, dominated by the most permeant ion.",
            ),
            q(
                "The membrane time constant tau = R_m*C_m for a typical cell is about:",
                (
                    opt("A few milliseconds", correct=True),
                    opt("A few seconds"),
                    opt("A few microseconds"),
                    opt("A few minutes"),
                ),
                "The RC product of the membrane is on the order of milliseconds.",
            ),
        ),
        "The action potential and Hodgkin-Huxley": (
            q(
                "In the Hodgkin-Huxley model, the upstroke of the action potential is driven by:",
                (
                    opt("Regenerative Na+ influx through voltage-gated channels", correct=True),
                    opt("K+ efflux"),
                    opt("Cl- influx"),
                    opt("ATP synthesis"),
                ),
                "Voltage-gated Na+ channels open, depolarizing the membrane in a positive-feedback upstroke.",
            ),
            q(
                "The action potential is described as 'all-or-none' because:",
                (
                    opt(
                        "Above threshold a full spike fires regardless of stimulus size",
                        correct=True,
                    ),
                    opt("It happens only once per cell"),
                    opt("It requires no ions"),
                    opt("It is purely passive"),
                ),
                "The neuron is excitable: subthreshold does nothing, suprathreshold gives a full spike.",
            ),
            q(
                "Repolarization in the Hodgkin-Huxley model results from:",
                (
                    opt("Delayed K+ efflux plus Na+ channel inactivation", correct=True),
                    opt("More Na+ entering"),
                    opt("The pump alone"),
                    opt("Capacitor breakdown"),
                ),
                "K+ channels open with delay while Na+ channels inactivate, restoring rest.",
            ),
        ),
    },
    final=(
        q(
            "Cells make unfavorable reactions proceed by:",
            (
                opt("Coupling them to ATP hydrolysis", correct=True),
                opt("Cooling the cytoplasm"),
                opt("Raising the activation barrier"),
                opt("Removing all substrate"),
            ),
            "Energetic coupling makes the combined delta G negative.",
        ),
        q(
            "Diffusion is effective over cellular distances but not whole organisms because:",
            (
                opt("Time to diffuse scales as distance squared over D", correct=True),
                opt("Diffusion needs sunlight"),
                opt("Diffusion only moves charged particles"),
                opt("Diffusion stops above 37 C"),
            ),
            "L^2/D grows fast, so large organisms need bulk transport.",
        ),
        q(
            "K_m in Michaelis-Menten kinetics corresponds to:",
            (
                opt("[S] at half-maximal velocity", correct=True),
                opt("The maximum velocity"),
                opt("Enzyme concentration"),
                opt("The turnover number"),
            ),
            "K_m is the substrate level giving v = Vmax/2.",
        ),
        q(
            "The Nernst potential depends on ion concentrations through a:",
            (
                opt("Logarithmic function of the concentration ratio", correct=True),
                opt("Linear function"),
                opt("Quadratic function"),
                opt("Constant independent of ratio"),
            ),
            "E = (RT/zF) ln([out]/[in]).",
        ),
        q(
            "Active transport differs from facilitated diffusion in that it:",
            (
                opt("Moves solutes uphill using energy such as ATP", correct=True),
                opt("Never saturates"),
                opt("Requires no proteins"),
                opt("Only moves water"),
            ),
            "Active transport pumps against the gradient at energetic cost.",
        ),
        q(
            "The all-or-none action potential upstroke is caused by:",
            (
                opt("Voltage-gated Na+ channel opening (positive feedback)", correct=True),
                opt("K+ leaving the cell"),
                opt("The Na+/K+ pump"),
                opt("Membrane capacitance discharging passively"),
            ),
            "Regenerative Na+ influx produces the rapid depolarizing spike.",
        ),
    ),
)
