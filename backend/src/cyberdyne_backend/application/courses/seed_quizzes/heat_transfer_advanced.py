"""Quiz questions for the Heat Transfer - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Heat exchangers and the LMTD method": (
            q(
                "The LMTD design equation for a heat exchanger is:",
                (
                    opt("q = U A dT_lm", correct=True),
                    opt("q = U A (T_h - T_c) average arithmetic"),
                    opt("q = sigma A T^4"),
                    opt("q = m cp"),
                ),
                "The log-mean temperature difference method gives q = U A dT_lm.",
            ),
            q(
                "For the same area and conditions, counterflow versus parallel flow extracts:",
                (
                    opt("more heat", correct=True),
                    opt("less heat"),
                    opt("exactly the same heat"),
                    opt("no heat"),
                ),
                "Counterflow maintains a more uniform dT and outperforms parallel flow.",
            ),
            q(
                "The overall coefficient U accounts for fouling through a:",
                (
                    opt("fouling resistance added in series", correct=True),
                    opt("multiplier on the area"),
                    opt("change in fluid density"),
                    opt("correction to the LMTD only"),
                ),
                "1/(UA) includes a fouling resistance term in series with the films and wall.",
            ),
        ),
        "Effectiveness-NTU design method": (
            q(
                "The number of transfer units NTU is defined as:",
                (
                    opt("UA / C_min", correct=True),
                    opt("C_min / UA"),
                    opt("U A dT"),
                    opt("C_min / C_max"),
                ),
                "NTU = UA / C_min, where C = m cp is the heat-capacity rate.",
            ),
            q(
                "Effectiveness is the ratio of actual heat transfer to:",
                (
                    opt("the maximum possible heat transfer q_max", correct=True),
                    opt("the wall conduction"),
                    opt("the radiation exchange"),
                    opt("the pumping power"),
                ),
                "eps = q / q_max with q_max = C_min (T_h,i - T_c,i).",
            ),
            q(
                "As NTU grows large, effectiveness:",
                (
                    opt("rises with diminishing returns", correct=True),
                    opt("falls toward zero"),
                    opt("grows without bound"),
                    opt("stays exactly constant"),
                ),
                "Past NTU ~ 3-4 added area buys little extra effectiveness.",
            ),
        ),
        "Boiling and condensation": (
            q(
                "The high coefficients of boiling and condensation come from:",
                (
                    opt("latent heat exchanged at nearly constant temperature", correct=True),
                    opt("very large temperature differences"),
                    opt("radiation"),
                    opt("low fluid conductivity"),
                ),
                "Phase change absorbs/releases latent heat with little temperature change, giving huge h.",
            ),
            q(
                "Exceeding the critical heat flux in boiling leads to:",
                (
                    opt("film boiling and a sharp wall-temperature rise (burnout)", correct=True),
                    opt("nucleate boiling"),
                    opt("free-convection boiling"),
                    opt("condensation"),
                ),
                "Past CHF a vapor blanket forms, flux drops and wall temperature can spike to burnout.",
            ),
            q(
                "Which boiling regime is the high-flux workhorse used in design?",
                (
                    opt("nucleate boiling", correct=True),
                    opt("film boiling"),
                    opt("free-convection boiling"),
                    opt("transition boiling above CHF"),
                ),
                "Nucleate boiling gives very high flux and is the desired operating regime.",
            ),
        ),
        "Numerical conduction and CFD": (
            q(
                "The five-point finite-difference stencil for 2-D steady conduction sets each interior node to the:",
                (
                    opt("average of its four neighbours", correct=True),
                    opt("sum of all boundary nodes"),
                    opt("product of two neighbours"),
                    opt("fourth power of a neighbour"),
                ),
                "Central differencing gives T_ij = (sum of 4 neighbours)/4 with no generation.",
            ),
            q(
                "An explicit transient conduction scheme is stable in 1-D only if the Fourier number per step satisfies:",
                (
                    opt("Fo <= 1/2", correct=True),
                    opt("Fo >= 1"),
                    opt("Fo = 1 exactly"),
                    opt("any value"),
                ),
                "Explicit schemes have a stability limit (Fo <= 1/2 in 1-D); implicit schemes do not.",
            ),
            q(
                "Crank-Nicolson and other implicit schemes are attractive because they are:",
                (
                    opt("unconditionally stable", correct=True),
                    opt("always explicit"),
                    opt("free of any matrix solve"),
                    opt("limited to steady state"),
                ),
                "Implicit time stepping is unconditionally stable, allowing larger time steps.",
            ),
        ),
        "Radiation exchange and view factors": (
            q(
                "The view factor F_ij is the fraction of radiation that leaves surface i and:",
                (
                    opt("strikes surface j", correct=True),
                    opt("is absorbed by surface i itself"),
                    opt("is converted to conduction"),
                    opt("escapes to space only"),
                ),
                "F_ij is the geometric fraction of i's radiation reaching j.",
            ),
            q(
                "The reciprocity relation for view factors states:",
                (
                    opt("A_i F_ij = A_j F_ji", correct=True),
                    opt("F_ij = F_ji always"),
                    opt("F_ij + F_ji = 1"),
                    opt("A_i = A_j"),
                ),
                "Reciprocity: A_i F_ij = A_j F_ji.",
            ),
            q(
                "A radiation shield reduces net exchange by:",
                (
                    opt("adding low-emissivity resistances in series", correct=True),
                    opt("increasing both surface emissivities"),
                    opt("raising the temperatures"),
                    opt("removing the vacuum"),
                ),
                "A low-emissivity shield inserts extra resistances in series, cutting net radiation.",
            ),
        ),
        "Thermal design optimization and ML": (
            q(
                "A typical thermal-design optimization minimizes mass or pumping power subject to a:",
                (
                    opt("junction-temperature constraint", correct=True),
                    opt("fixed view factor"),
                    opt("constant Reynolds number"),
                    opt("zero Biot number"),
                ),
                "The constraint is usually keeping the junction below a temperature limit.",
            ),
            q(
                "A surrogate model is used in optimization because each high-fidelity CFD run is:",
                (
                    opt("computationally expensive", correct=True),
                    opt("perfectly accurate and free"),
                    opt("unnecessary"),
                    opt("only valid at steady state"),
                ),
                "Cheap surrogates approximate the expensive CFD so many designs can be searched.",
            ),
            q(
                "Physics-informed neural networks (PINNs) can be used to:",
                (
                    opt("learn temperature fields that satisfy the heat equation", correct=True),
                    opt("replace thermodynamics entirely"),
                    opt("eliminate the need for boundary conditions"),
                    opt("only post-process plots"),
                ),
                "PINNs embed the governing PDE in the loss to learn physically consistent fields.",
            ),
        ),
    },
    final=(
        q(
            "Use the effectiveness-NTU method rather than LMTD when:",
            (
                opt("outlet temperatures are unknown (a rating problem)", correct=True),
                opt("both outlet temperatures are already known"),
                opt("there is no fluid flow"),
                opt("the exchanger is a single resistor"),
            ),
            "Effectiveness-NTU is convenient for rating when outlet temperatures are unknown.",
        ),
        q(
            "The dominant reason boiling achieves very high heat fluxes is:",
            (
                opt("latent heat transfer at nearly constant temperature", correct=True),
                opt("strong radiation"),
                opt("very large wall superheats"),
                opt("low fluid conductivity"),
            ),
            "Phase change moves latent heat with minimal temperature change.",
        ),
        q(
            "For two large parallel gray plates, the net radiative exchange denominator is:",
            (
                opt("1/eps1 + 1/eps2 - 1", correct=True),
                opt("eps1 + eps2"),
                opt("eps1 eps2"),
                opt("1 - eps1 - eps2"),
            ),
            "q = sigma A (T1^4 - T2^4) / (1/eps1 + 1/eps2 - 1).",
        ),
        q(
            "An explicit transient finite-difference scheme can become unstable if the:",
            (
                opt("time step is too large (Fo exceeds the stability limit)", correct=True),
                opt("grid is too fine"),
                opt("conductivity is constant"),
                opt("boundary is adiabatic"),
            ),
            "Explicit schemes require the time step to keep Fo within the stability limit.",
        ),
        q(
            "In an enclosure, the view-factor summation rule states that for each surface:",
            (
                opt("the sum of F_ij over all surfaces equals 1", correct=True),
                opt("the sum equals zero"),
                opt("F_ij is the same for every j"),
                opt("only F_ii matters"),
            ),
            "Summation rule: sum_j F_ij = 1 over an enclosure.",
        ),
        q(
            "Bayesian / surrogate-based optimization of a heat sink works by:",
            (
                opt("optimizing a cheap surrogate then verifying with CFD", correct=True),
                opt("running CFD at every candidate without any model"),
                opt("ignoring the temperature constraint"),
                opt("using only hand calculation"),
            ),
            "A surrogate is fit to sampled designs, optimized cheaply, and the optimum is verified with CFD.",
        ),
    ),
)
