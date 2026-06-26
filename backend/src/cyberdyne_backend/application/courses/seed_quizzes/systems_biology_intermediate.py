"""Quiz questions for the Systems & Network Biology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "ODE models and mass action": (
            q(
                "What does the law of mass action state about reaction rate?",
                (
                    opt(
                        "It is proportional to the product of reactant concentrations", correct=True
                    ),
                    opt("It is independent of concentration"),
                    opt("It depends only on temperature"),
                    opt("It is proportional to the product concentration only"),
                ),
                "For A + B -> C the rate is k[A][B].",
            ),
            q(
                "What is the analytical solution of first-order decay dA/dt = -kA?",
                (
                    opt("A(t) = A0 * exp(-kt)", correct=True),
                    opt("A(t) = A0 + kt"),
                    opt("A(t) = A0 * kt"),
                    opt("A(t) = A0 * exp(+kt)"),
                ),
                "First-order decay is exponential.",
            ),
            q(
                "Which tools numerically integrate biochemical ODE models?",
                (
                    opt("SciPy solve_ivp, COPASI and Tellurium", correct=True),
                    opt("A word processor"),
                    opt("A genome browser only"),
                    opt("A sequence aligner only"),
                ),
                "These integrate the stacked balance equations over time.",
            ),
        ),
        "Steady states and stability analysis": (
            q(
                "How is a steady state (fixed point) defined?",
                (
                    opt("All time derivatives equal zero", correct=True),
                    opt("All concentrations equal zero"),
                    opt("The system is oscillating fastest"),
                    opt("The Jacobian is the identity matrix"),
                ),
                "At a fixed point dx/dt = 0 for every species.",
            ),
            q(
                "What determines the local stability of a fixed point?",
                (
                    opt("The signs of the real parts of the Jacobian's eigenvalues", correct=True),
                    opt("The total number of species"),
                    opt("The color of the plot"),
                    opt("The size of the genome"),
                ),
                "Negative real parts mean perturbations decay; the state is stable.",
            ),
            q(
                "Complex eigenvalues at a fixed point indicate what?",
                (
                    opt("Oscillatory approach to or from the state", correct=True),
                    opt("That the model is invalid"),
                    opt("Exact adaptation guaranteed"),
                    opt("That there are no fixed points"),
                ),
                "Imaginary parts produce spiralling (oscillatory) dynamics.",
            ),
        ),
        "Bifurcations, switches and oscillators": (
            q(
                "What is a bifurcation?",
                (
                    opt(
                        "A qualitative change in the number or stability of fixed points as a parameter varies",
                        correct=True,
                    ),
                    opt("A type of DNA mutation"),
                    opt("The splitting of a chromosome"),
                    opt("A measurement unit for flux"),
                ),
                "Bifurcations reorganise the system's qualitative behaviour.",
            ),
            q(
                "A Hopf bifurcation gives birth to what?",
                (
                    opt("A stable limit cycle (sustained oscillation)", correct=True),
                    opt("A single stable fixed point only"),
                    opt("A permanent shutdown"),
                    opt("A scale-free network"),
                ),
                "Hopf bifurcations create limit-cycle oscillations like circadian clocks.",
            ),
            q(
                "What does bistability with hysteresis require structurally?",
                (
                    opt("Cooperative positive feedback giving two stable states", correct=True),
                    opt("Only first-order linear kinetics"),
                    opt("Negative feedback with no nonlinearity"),
                    opt("No feedback at all"),
                ),
                "Sharp positive feedback creates two stable states and memory.",
            ),
        ),
        "Stochastic gene expression": (
            q(
                "When are stochastic models necessary instead of ODEs?",
                (
                    opt(
                        "When molecule numbers are small, making reactions inherently random",
                        correct=True,
                    ),
                    opt("When concentrations are extremely high"),
                    opt("Whenever the model is linear"),
                    opt("Only at steady state"),
                ),
                "Low copy numbers make discreteness and noise important.",
            ),
            q(
                "Which algorithm exactly simulates the chemical master equation?",
                (
                    opt("The Gillespie stochastic simulation algorithm (SSA)", correct=True),
                    opt("Linear programming"),
                    opt("The Smith-Waterman algorithm"),
                    opt("Principal component analysis"),
                ),
                "Gillespie's SSA draws random reaction times and identities.",
            ),
            q(
                "For a Poisson copy-number distribution, what is the Fano factor?",
                (
                    opt("1 (variance equals mean)", correct=True),
                    opt("0 always"),
                    opt("Negative"),
                    opt("Equal to the genome size"),
                ),
                "Poisson statistics give variance/mean = 1; bursting raises it.",
            ),
        ),
        "Constraint-based modelling and FBA": (
            q(
                "What steady-state constraint underlies constraint-based modelling?",
                (
                    opt("S*v = 0, where S is the stoichiometric matrix", correct=True),
                    opt("v = Vmax always"),
                    opt("Every flux equals zero"),
                    opt("S equals the identity matrix"),
                ),
                "At metabolic steady state internal metabolites are balanced.",
            ),
            q(
                "What optimisation method does FBA use, and what does it usually maximise?",
                (
                    opt("Linear programming, maximising biomass production", correct=True),
                    opt("Random sampling, maximising entropy"),
                    opt("Gradient descent on a neural net"),
                    opt("Sorting, maximising read length"),
                ),
                "FBA solves an LP for the biomass-maximising flux distribution.",
            ),
            q(
                "Why is constraint-based modelling preferred for genome-scale metabolism?",
                (
                    opt(
                        "It avoids needing the mostly-unknown kinetic rate constants", correct=True
                    ),
                    opt("It requires measuring every rate constant"),
                    opt("It ignores stoichiometry"),
                    opt("It only works for two reactions"),
                ),
                "Steady-state and stoichiometry constraints replace detailed kinetics.",
            ),
        ),
    },
    final=(
        q(
            "What is the rate expression for A + B -> C under mass action?",
            (
                opt("k[A][B]", correct=True),
                opt("k[A] + k[B]"),
                opt("k[C]"),
                opt("k only"),
            ),
            "Rate is proportional to the product of reactant concentrations.",
        ),
        q(
            "Stability of a fixed point is read from which quantities?",
            (
                opt("The eigenvalues of the Jacobian", correct=True),
                opt("The determinant of the stoichiometric matrix"),
                opt("The number of reactions"),
                opt("The plot color"),
            ),
            "Eigenvalue real parts decide whether perturbations decay or grow.",
        ),
        q(
            "Which bifurcation produces sustained oscillations?",
            (
                opt("Hopf bifurcation", correct=True),
                opt("Saddle-node only"),
                opt("No bifurcation"),
                opt("A power-law bifurcation"),
            ),
            "A Hopf bifurcation creates a stable limit cycle.",
        ),
        q(
            "What does the Gillespie algorithm compute?",
            (
                opt("Exact stochastic trajectories of reacting molecules", correct=True),
                opt("The optimal metabolic flux"),
                opt("A protein structure"),
                opt("A multiple sequence alignment"),
            ),
            "It simulates the chemical master equation exactly.",
        ),
        q(
            "In FBA, what is the role of the stoichiometric matrix S?",
            (
                opt("It encodes reaction stoichiometry and enforces S*v = 0", correct=True),
                opt("It stores kinetic rate constants"),
                opt("It lists gene sequences"),
                opt("It is the Jacobian of the ODEs"),
            ),
            "Rows are metabolites, columns reactions; S*v = 0 at steady state.",
        ),
        q(
            "What is the repressilator?",
            (
                opt("A synthetic three-gene ring of repressors that oscillates", correct=True),
                opt("A metabolic database"),
                opt("A type of stochastic noise"),
                opt("A linear-programming solver"),
            ),
            "Three mutually repressing genes generate oscillations.",
        ),
    ),
)
