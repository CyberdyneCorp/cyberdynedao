"""Quiz questions for the Mathematics for Life Sciences - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Nonlinear dynamics, equilibria and stability": (
            q(
                "At an equilibrium of a dynamical system, what is true?",
                (
                    opt("All the rates of change are zero", correct=True),
                    opt("All variables are maximal"),
                    opt("The system is always unstable"),
                    opt("Time stops"),
                ),
                "An equilibrium is a steady state where every rate of change vanishes.",
            ),
            q(
                "For a one-variable system dx/dt = f(x), an equilibrium x* is stable when?",
                (
                    opt("f'(x*) < 0", correct=True),
                    opt("f'(x*) > 0"),
                    opt("f(x*) > 0"),
                    opt("f'(x*) = 1"),
                ),
                "A negative slope of f at x* makes perturbations decay, so it is stable.",
            ),
            q(
                "A qualitative change in equilibria as a parameter varies is called what?",
                (
                    opt("A bifurcation", correct=True),
                    opt("A derivative"),
                    opt("An eigenvector"),
                    opt("A residual"),
                ),
                "A bifurcation is where equilibria appear, vanish or change stability.",
            ),
        ),
        "Predator-prey and interacting populations": (
            q(
                "In the Lotka-Volterra model, the predation term is proportional to what?",
                (
                    opt("The product of prey and predator densities, N times P", correct=True),
                    opt("Prey density alone"),
                    opt("Predator density alone"),
                    opt("Time"),
                ),
                "Encounters scale with N times P, the mass-action predation term.",
            ),
            q(
                "What is the hallmark behaviour of the classic Lotka-Volterra system?",
                (
                    opt("Sustained oscillations of prey and predator", correct=True),
                    opt("Monotone exponential growth of both"),
                    opt("Immediate extinction of both"),
                    opt("A constant steady state always"),
                ),
                "The basic model produces sustained predator-prey cycles.",
            ),
            q(
                "A saturating predator response at high prey density is called what?",
                (
                    opt("A Holling type-II functional response", correct=True),
                    opt("Linear growth"),
                    opt("A Poisson process"),
                    opt("A bifurcation"),
                ),
                "A Holling type-II response saturates, analogous to Michaelis-Menten.",
            ),
        ),
        "Epidemic modelling: the SIR system and R0": (
            q(
                "In the SIR model, what does R0 represent?",
                (
                    opt(
                        "Expected secondary cases from one infected in a fully susceptible population",
                        correct=True,
                    ),
                    opt("The recovery rate"),
                    opt("The total population size"),
                    opt("The number recovered at the end"),
                ),
                "R0 is the basic reproduction number, the average secondary infections.",
            ),
            q(
                "An epidemic takes off when which condition holds?",
                (
                    opt("R0 > 1", correct=True),
                    opt("R0 < 1"),
                    opt("R0 = 0"),
                    opt("R0 is negative"),
                ),
                "If R0 exceeds 1, cases grow and an epidemic occurs.",
            ),
            q(
                "The herd-immunity threshold for an epidemic is which fraction immune?",
                (
                    opt("1 - 1/R0", correct=True),
                    opt("1/R0"),
                    opt("R0"),
                    opt("R0 - 1"),
                ),
                "Once a fraction 1 - 1/R0 is immune, the epidemic cannot grow.",
            ),
        ),
        "Enzyme kinetics: parameter estimation": (
            q(
                "Why are linearised plots like Lineweaver-Burk discouraged for estimating Km and Vmax?",
                (
                    opt(
                        "The reciprocal transform biases estimates by distorting the error structure",
                        correct=True,
                    ),
                    opt("They require a supercomputer"),
                    opt("They cannot be plotted"),
                    opt("They give Vmax but never Km"),
                ),
                "Reciprocal transforms inflate low-substrate noise and bias the fit.",
            ),
            q(
                "Which optimiser is commonly used for nonlinear least-squares kinetic fitting?",
                (
                    opt("Levenberg-Marquardt (e.g. via curve_fit)", correct=True),
                    opt("Bubble sort"),
                    opt("The Gillespie algorithm"),
                    opt("Gaussian elimination only"),
                ),
                "Levenberg-Marquardt is the standard nonlinear least-squares optimiser.",
            ),
            q(
                "What can a global fit across inhibitor concentrations help distinguish?",
                (
                    opt("Competitive from non-competitive inhibition", correct=True),
                    opt("The molecular weight of the enzyme"),
                    opt("The pH of the buffer"),
                    opt("The color of the assay"),
                ),
                "Sharing parameters in a global fit distinguishes inhibition mechanisms.",
            ),
        ),
        "Pharmacokinetics: compartment models": (
            q(
                "In a one-compartment model, clearance CL relates to ke and Vd how?",
                (
                    opt("CL = ke times Vd", correct=True),
                    opt("CL = ke / Vd"),
                    opt("CL = Vd / ke"),
                    opt("CL = ke + Vd"),
                ),
                "Clearance equals the elimination rate constant times the volume of distribution.",
            ),
            q(
                "A two-compartment model produces what kind of plasma decay?",
                (
                    opt(
                        "Bi-exponential: a fast distribution phase then a slower elimination phase",
                        correct=True,
                    ),
                    opt("A single straight line"),
                    opt("Pure linear growth"),
                    opt("A constant level"),
                ),
                "Two compartments give a bi-exponential decline.",
            ),
            q(
                "What does population PK (nonlinear mixed-effects modelling) add?",
                (
                    opt(
                        "Variability across patients and covariate effects like weight and renal function",
                        correct=True,
                    ),
                    opt("Only a single patient's curve"),
                    opt("The enzyme Km"),
                    opt("The basic reproduction number"),
                ),
                "Population PK models between-subject variability and covariates.",
            ),
        ),
        "Stochastic models and computational methods": (
            q(
                "When is a stochastic model preferred over deterministic ODEs?",
                (
                    opt(
                        "When molecule numbers are small and randomness drives behaviour",
                        correct=True,
                    ),
                    opt("When concentrations are very large"),
                    opt("Always, ODEs are never useful"),
                    opt("Only for linear systems"),
                ),
                "At low copy number, discrete random events matter, so use stochastic models.",
            ),
            q(
                "What does the Gillespie algorithm (SSA) generate?",
                (
                    opt("Exact sample trajectories of a chemical reaction network", correct=True),
                    opt("The mean of a normal distribution"),
                    opt("An eigenvalue"),
                    opt("A least-squares fit"),
                ),
                "The SSA produces exact stochastic trajectories of reaction networks.",
            ),
            q(
                "Approximate Bayesian computation (ABC) is useful when what is intractable?",
                (
                    opt("The likelihood function", correct=True),
                    opt("The prior"),
                    opt("Addition of numbers"),
                    opt("The plotting library"),
                ),
                "ABC enables Bayesian inference when the likelihood cannot be evaluated.",
            ),
        ),
    },
    final=(
        q(
            "A system's equilibrium is stable when its Jacobian eigenvalues have what property?",
            (
                opt("All negative real parts", correct=True),
                opt("All positive real parts"),
                opt("They are all integers"),
                opt("They sum to zero"),
            ),
            "Negative real parts of all eigenvalues mean perturbations decay.",
        ),
        q(
            "The classic Lotka-Volterra predator-prey model exhibits what?",
            (
                opt("Sustained population oscillations", correct=True),
                opt("Monotone decay to zero"),
                opt("A fixed constant for both species"),
                opt("Unbounded growth of predators"),
            ),
            "Lotka-Volterra produces sustained cycles of prey and predator.",
        ),
        q(
            "In the SIR model, an epidemic is prevented once the immune fraction exceeds which threshold?",
            (
                opt("1 - 1/R0", correct=True),
                opt("1/R0"),
                opt("R0"),
                opt("0.5 always"),
            ),
            "Herd immunity is reached at a fraction 1 - 1/R0.",
        ),
        q(
            "The modern, unbiased way to estimate Km and Vmax from kinetic data is what?",
            (
                opt(
                    "Nonlinear least-squares fitting of the Michaelis-Menten equation", correct=True
                ),
                opt("A Lineweaver-Burk double-reciprocal plot"),
                opt("Reading values off by eye"),
                opt("Assuming Km = Vmax"),
            ),
            "Direct nonlinear least squares avoids the bias of reciprocal plots.",
        ),
        q(
            "In one-compartment PK, the area under the curve equals what?",
            (
                opt("Dose / clearance", correct=True),
                opt("Dose times clearance"),
                opt("Clearance / dose"),
                opt("Half-life times dose"),
            ),
            "AUC = dose/CL for a single dose with first-order elimination.",
        ),
        q(
            "Which method gives exact stochastic trajectories of a reaction network at low copy number?",
            (
                opt("The Gillespie stochastic simulation algorithm", correct=True),
                opt("Linear regression"),
                opt("Gaussian elimination"),
                opt("The Fundamental Theorem of Calculus"),
            ),
            "The Gillespie SSA simulates exact stochastic reaction trajectories.",
        ),
    ),
)
