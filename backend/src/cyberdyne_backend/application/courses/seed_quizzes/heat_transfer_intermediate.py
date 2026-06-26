"""Quiz questions for the Heat Transfer - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Thermal resistance networks": (
            q(
                "The conduction resistance of a cylindrical pipe wall is:",
                (
                    opt("ln(r2/r1) / (2 pi k L)", correct=True),
                    opt("L/(k A)"),
                    opt("(r2 - r1)/(k A)"),
                    opt("1/(h A)"),
                ),
                "Radial conduction gives R_cyl = ln(r2/r1)/(2 pi k L).",
            ),
            q(
                "Below the critical radius of insulation, adding insulation to a small tube:",
                (
                    opt("can increase the heat loss", correct=True),
                    opt("always decreases heat loss"),
                    opt("has no effect"),
                    opt("freezes the fluid"),
                ),
                "Below r_c = k/h the rising outer area lowers convection resistance faster than conduction rises.",
            ),
            q(
                "Two heat paths side by side (a stud and the insulation beside it) are treated as resistances in:",
                (
                    opt("parallel", correct=True),
                    opt("series"),
                    opt("a single lumped resistor of zero value"),
                    opt("opposition that cancels"),
                ),
                "Alternate heat paths combine as parallel resistances.",
            ),
        ),
        "Fins and extended surfaces": (
            q(
                "The fin parameter m equals:",
                (
                    opt("sqrt(h P / (k A_c))", correct=True),
                    opt("h P k A_c"),
                    opt("k A_c / (h P)"),
                    opt("h A / (k L)"),
                ),
                "m = sqrt(hP/(kA_c)); larger m means faster temperature decay along the fin.",
            ),
            q(
                "Fin efficiency compares the actual fin heat rate to that of a fin which is:",
                (
                    opt("entirely at the base temperature (isothermal)", correct=True),
                    opt("at ambient temperature"),
                    opt("infinitely long"),
                    opt("made of insulation"),
                ),
                "Efficiency = q_fin / (h A_fin theta_b), the ideal isothermal fin.",
            ),
            q(
                "Which change makes a fin more effective?",
                (
                    opt("Higher thermal conductivity material", correct=True),
                    opt("Lower thermal conductivity material"),
                    opt("A higher convection coefficient at the base"),
                    opt("A thicker, stubbier profile"),
                ),
                "High-k, thin profiles and low h favor effective fins.",
            ),
        ),
        "Dimensionless numbers in convection": (
            q(
                "The Reynolds number represents the ratio of:",
                (
                    opt("inertial to viscous forces", correct=True),
                    opt("buoyancy to viscous forces"),
                    opt("conduction to convection"),
                    opt("thermal to momentum diffusivity"),
                ),
                "Re = uL/nu, inertial vs viscous forces; it sets laminar vs turbulent flow.",
            ),
            q(
                "The Nusselt number is essentially the dimensionless:",
                (
                    opt("convection coefficient, Nu = hL/k", correct=True),
                    opt("thermal conductivity"),
                    opt("viscosity"),
                    opt("density"),
                ),
                "Nu = hL/k; we solve for Nu then recover h = Nu k / L.",
            ),
            q(
                "The Prandtl number of air is approximately:",
                (
                    opt("0.7", correct=True),
                    opt("7"),
                    opt("100"),
                    opt("0.001"),
                ),
                "Pr ~ 0.7 for air, ~7 for water, much larger for oils.",
            ),
        ),
        "Forced convection correlations": (
            q(
                "The Dittus-Boelter correlation for turbulent pipe flow is:",
                (
                    opt("Nu = 0.023 Re^0.8 Pr^n", correct=True),
                    opt("Nu = 0.664 Re^0.5 Pr^(1/3)"),
                    opt("Nu = 0.59 Ra^0.25"),
                    opt("Nu = constant"),
                ),
                "Dittus-Boelter: Nu = 0.023 Re^0.8 Pr^n (n=0.4 heating, 0.3 cooling).",
            ),
            q(
                "In Dittus-Boelter, the exponent n on Pr is 0.4 when the fluid is being:",
                (
                    opt("heated", correct=True),
                    opt("cooled"),
                    opt("kept isothermal"),
                    opt("boiled"),
                ),
                "n = 0.4 for heating the fluid, n = 0.3 for cooling.",
            ),
            q(
                "For the laminar flat-plate correlation Nu = 0.664 Re^0.5 Pr^(1/3), the length scale is the:",
                (
                    opt("plate length from the leading edge", correct=True),
                    opt("plate thickness"),
                    opt("boundary-layer thickness"),
                    opt("pipe diameter"),
                ),
                "External flat-plate flow uses the streamwise length L from the leading edge.",
            ),
        ),
        "Natural convection": (
            q(
                "Natural convection is driven by:",
                (
                    opt("buoyancy from density differences", correct=True),
                    opt("an external fan or pump"),
                    opt("electromagnetic waves"),
                    opt("pressure gradients from a compressor"),
                ),
                "Heating creates density differences; buoyancy drives the flow.",
            ),
            q(
                "The Rayleigh number is the product of:",
                (
                    opt("Grashof and Prandtl numbers", correct=True),
                    opt("Reynolds and Prandtl numbers"),
                    opt("Nusselt and Reynolds numbers"),
                    opt("Biot and Fourier numbers"),
                ),
                "Ra = Gr Pr governs natural-convection regimes.",
            ),
            q(
                "Compared with forced convection, natural-convection coefficients in air are:",
                (
                    opt("much smaller", correct=True),
                    opt("much larger"),
                    opt("identical"),
                    opt("always zero"),
                ),
                "Natural convection in air gives only a few W/m^2-K, limiting passive cooling.",
            ),
        ),
        "Transient conduction and lumped capacitance": (
            q(
                "The lumped-capacitance model is valid when the Biot number is:",
                (
                    opt("less than about 0.1", correct=True),
                    opt("greater than 1"),
                    opt("exactly equal to the Fourier number"),
                    opt("negative"),
                ),
                "Bi < 0.1 means internal gradients are negligible, so lumped capacitance applies.",
            ),
            q(
                "The time constant for lumped-capacitance cooling is:",
                (
                    opt("rho V cp / (h A_s)", correct=True),
                    opt("h A_s / (rho V cp)"),
                    opt("k / (rho cp)"),
                    opt("alpha t / L^2"),
                ),
                "tau = rho V cp / (h A_s); the temperature decays as exp(-t/tau).",
            ),
            q(
                "The Biot number compares:",
                (
                    opt(
                        "internal conduction resistance to surface convection resistance",
                        correct=True,
                    ),
                    opt("inertial to viscous forces"),
                    opt("buoyancy to viscosity"),
                    opt("two radiation resistances"),
                ),
                "Bi = h L_c / k is the ratio of internal conduction to surface convection resistance.",
            ),
        ),
    },
    final=(
        q(
            "The overall heat-transfer coefficient combines:",
            (
                opt("both convection films and the wall conduction resistance", correct=True),
                opt("only the wall conduction"),
                opt("only radiation"),
                opt("only the inside film"),
            ),
            "1/(UA) sums inside film, wall, fouling and outside film resistances.",
        ),
        q(
            "To recover the convection coefficient from a correlation you compute Nu, then use:",
            (
                opt("h = Nu k / L", correct=True),
                opt("h = Nu L / k"),
                opt("h = k / (Nu L)"),
                opt("h = Re Pr"),
            ),
            "From Nu = hL/k, h = Nu k / L.",
        ),
        q(
            "A fin is generally worthwhile only when its effectiveness exceeds about:",
            (
                opt("2", correct=True),
                opt("0.1"),
                opt("0.5"),
                opt("100"),
            ),
            "Effectiveness above ~2 means the fin meaningfully beats the bare base.",
        ),
        q(
            "Pipe flow is typically laminar when the Reynolds number is below about:",
            (
                opt("2300", correct=True),
                opt("23"),
                opt("500000"),
                opt("1000000"),
            ),
            "Internal pipe flow transitions to turbulence near Re ~ 2300.",
        ),
        q(
            "When the Biot number exceeds 0.1 you should:",
            (
                opt("use the 1-D transient solution (series / Heisler charts)", correct=True),
                opt("still use lumped capacitance"),
                opt("ignore conduction"),
                opt("assume steady state"),
            ),
            "Large Bi means internal gradients matter; the spatial transient solution is needed.",
        ),
        q(
            "Adding insulation to a thin wire below the critical radius will:",
            (
                opt("increase its heat loss", correct=True),
                opt("always decrease its heat loss"),
                opt("have no effect on heat loss"),
                opt("stop convection entirely"),
            ),
            "Below r_c = k_ins/h, the increase in outer area lowers convection resistance, raising heat loss.",
        ),
    ),
)
