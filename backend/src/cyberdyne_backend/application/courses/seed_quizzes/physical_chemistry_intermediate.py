"""Quiz questions for the Physical Chemistry & Thermodynamics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Chemical potential & the equilibrium constant": (
            q(
                "The relation between standard reaction Gibbs energy and the equilibrium constant is:",
                (
                    opt("dG0 = -RT ln K", correct=True),
                    opt("dG0 = RT ln K"),
                    opt("dG0 = -RT K"),
                    opt("dG0 = K / RT"),
                ),
                "At equilibrium dG = 0 and Q = K, giving dG0 = -RT ln K.",
            ),
            q(
                "A reaction is product-favoured (K > 1) when:",
                (
                    opt("the standard reaction Gibbs energy is negative", correct=True),
                    opt("the standard reaction Gibbs energy is positive"),
                    opt("the enthalpy is zero"),
                    opt("the temperature is zero"),
                ),
                "K > 1 corresponds to dG0 < 0.",
            ),
            q(
                "The reaction quotient Q at equilibrium:",
                (
                    opt("equals the equilibrium constant K", correct=True),
                    opt("is always greater than K"),
                    opt("is always zero"),
                    opt("equals 1 always"),
                ),
                "At equilibrium Q = K and the driving force vanishes.",
            ),
        ),
        "Le Chatelier & the van 't Hoff equation": (
            q(
                "Le Chatelier's principle predicts that a disturbed equilibrium shifts to:",
                (
                    opt("partly oppose the disturbance", correct=True),
                    opt("amplify the disturbance"),
                    opt("stop reacting entirely"),
                    opt("change the value of K at constant T"),
                ),
                "The system responds to counteract the imposed change.",
            ),
            q(
                "A van 't Hoff plot graphs:",
                (
                    opt("ln K against 1/T, with slope -dH0/R", correct=True),
                    opt("K against T linearly"),
                    opt("ln K against T squared"),
                    opt("1/K against T"),
                ),
                "ln K vs 1/T is linear with slope -dH0/R.",
            ),
            q(
                "For an exothermic reaction, raising the temperature:",
                (
                    opt("decreases K, disfavouring products", correct=True),
                    opt("increases K"),
                    opt("leaves K unchanged"),
                    opt("makes the reaction first order"),
                ),
                "Heating an exothermic reaction lowers K (Le Chatelier and van 't Hoff agree).",
            ),
        ),
        "Rate laws & reaction order": (
            q(
                "Reaction orders in a rate law are determined by:",
                (
                    opt("experiment, not the balanced stoichiometry", correct=True),
                    opt("the coefficients of the overall equation"),
                    opt("the sign of dG"),
                    opt("the equilibrium constant"),
                ),
                "Orders are found experimentally and need not match stoichiometry.",
            ),
            q(
                "A first-order reaction has a half-life that is:",
                (
                    opt("independent of the starting concentration", correct=True),
                    opt("proportional to the starting concentration"),
                    opt("inversely proportional to the rate constant squared"),
                    opt("zero"),
                ),
                "For first order, t_half = ln 2 / k, independent of [A]0.",
            ),
            q(
                "Which plot is linear for a first-order reaction?",
                (
                    opt("ln[A] versus time", correct=True),
                    opt("[A] versus time"),
                    opt("1/[A] versus time"),
                    opt("[A] squared versus time"),
                ),
                "First-order integrated law makes ln[A] linear in time.",
            ),
        ),
        "Arrhenius equation & transition state theory": (
            q(
                "The Arrhenius equation expresses the rate constant as:",
                (
                    opt("k = A exp(-Ea/RT)", correct=True),
                    opt("k = A exp(Ea/RT)"),
                    opt("k = A / (Ea RT)"),
                    opt("k = Ea exp(-A/RT)"),
                ),
                "k = A exp(-Ea/RT); ln k vs 1/T has slope -Ea/R.",
            ),
            q(
                "A catalyst speeds a reaction by:",
                (
                    opt("lowering the activation energy via a new pathway", correct=True),
                    opt("increasing the equilibrium constant"),
                    opt("making the reaction more exothermic"),
                    opt("raising the activation energy"),
                ),
                "Catalysts lower Ea but do not change dG or K.",
            ),
            q(
                "Transition state theory describes reactants passing through:",
                (
                    opt("an activated complex at a saddle point of the PES", correct=True),
                    opt("a stable intermediate minimum"),
                    opt("a vacuum with no interactions"),
                    opt("the product geometry directly"),
                ),
                "The transition state is the saddle point on the potential energy surface.",
            ),
        ),
        "Reaction mechanisms & rate-determining steps": (
            q(
                "The rate-determining step of a mechanism is:",
                (
                    opt("the slowest elementary step", correct=True),
                    opt("the fastest elementary step"),
                    opt("always the first step"),
                    opt("the step with the largest dG0"),
                ),
                "The slowest step is the bottleneck controlling the overall rate.",
            ),
            q(
                "The steady-state approximation assumes that:",
                (
                    opt(
                        "the net rate of change of a reactive intermediate is about zero",
                        correct=True,
                    ),
                    opt("all concentrations are constant"),
                    opt("the reaction never reaches equilibrium"),
                    opt("the rate constant is zero"),
                ),
                "Reactive intermediates are consumed about as fast as they form.",
            ),
            q(
                "The Michaelis-Menten rate law produces a curve that:",
                (
                    opt("saturates toward Vmax at high substrate", correct=True),
                    opt("grows without limit"),
                    opt("decreases with substrate"),
                    opt("is a straight line through the origin"),
                ),
                "v = Vmax[S]/(Km+[S]) saturates as [S] grows large.",
            ),
        ),
        "Electrochemistry & the Nernst equation": (
            q(
                "Cell potential and Gibbs energy are related by:",
                (
                    opt("dG = -n F E", correct=True),
                    opt("dG = n F E"),
                    opt("dG = -E / (n F)"),
                    opt("dG = n F / E"),
                ),
                "dG = -nFE; a spontaneous galvanic cell has E > 0.",
            ),
            q(
                "The Nernst equation gives the cell potential as:",
                (
                    opt("E = E0 - (RT/nF) ln Q", correct=True),
                    opt("E = E0 + (RT/nF) ln Q always increasing"),
                    opt("E = E0 ln Q"),
                    opt("E = nF / Q"),
                ),
                "E = E0 - (RT/nF) ln Q describes potential away from standard conditions.",
            ),
            q(
                "As a battery discharges toward equilibrium, the cell potential:",
                (
                    opt("falls toward zero as Q approaches K", correct=True),
                    opt("rises without limit"),
                    opt("stays at E0 forever"),
                    opt("becomes infinite"),
                ),
                "When Q reaches K, E = 0 (a dead battery).",
            ),
        ),
    },
    final=(
        q(
            "The cornerstone link between thermodynamics and equilibrium is:",
            (
                opt("dG0 = -RT ln K", correct=True),
                opt("dG0 = RT K"),
                opt("dG0 = -nFE only"),
                opt("dG0 = dH0 always"),
            ),
            "dG0 = -RT ln K connects standard Gibbs energy to the equilibrium constant.",
        ),
        q(
            "For an exothermic reaction, the van 't Hoff plot of ln K vs 1/T has:",
            (
                opt("positive slope, so K falls as T rises", correct=True),
                opt("negative slope, so K rises as T rises"),
                opt("zero slope"),
                opt("a vertical asymptote"),
            ),
            "Slope is -dH0/R, positive for exothermic, so K decreases with T.",
        ),
        q(
            "Which statement about kinetics is correct?",
            (
                opt("reaction orders are measured experimentally", correct=True),
                opt("orders always equal the stoichiometric coefficients"),
                opt("a catalyst increases K"),
                opt("the fastest step is rate-determining"),
            ),
            "Orders are experimental; catalysts lower Ea; the slowest step limits the rate.",
        ),
        q(
            "The Arrhenius activation energy can be obtained from:",
            (
                opt("the slope of ln k versus 1/T", correct=True),
                opt("the intercept of [A] versus t"),
                opt("the value of K at one temperature"),
                opt("the cell potential"),
            ),
            "ln k = ln A - Ea/RT, so slope of ln k vs 1/T is -Ea/R.",
        ),
        q(
            "A reactive intermediate treated with the steady-state approximation has:",
            (
                opt("a net rate of change of about zero", correct=True),
                opt("a constant large concentration"),
                opt("zero rate of formation"),
                opt("an order of two"),
            ),
            "Its formation and consumption rates nearly balance.",
        ),
        q(
            "In an electrochemical cell, a positive standard cell potential means:",
            (
                opt("the reaction is spontaneous as written, dG0 < 0", correct=True),
                opt("the reaction is non-spontaneous"),
                opt("Q must equal K"),
                opt("n equals zero"),
            ),
            "dG0 = -nFE0; positive E0 gives negative dG0, a spontaneous galvanic cell.",
        ),
    ),
)
