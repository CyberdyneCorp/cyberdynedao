"""Quiz questions for the Fluid Mechanics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Turbulent pipe flow and the Moody chart": (
            q(
                "The turbulent friction factor depends on:",
                (
                    opt("Reynolds number and relative roughness", correct=True),
                    opt("Reynolds number only"),
                    opt("relative roughness only"),
                    opt("pipe length only"),
                ),
                "In turbulent flow f = f(Re, eps/D), as plotted on the Moody chart.",
            ),
            q(
                "The Colebrook-White equation is:",
                (
                    opt("implicit in the friction factor f", correct=True),
                    opt("an explicit formula for f"),
                    opt("valid only for laminar flow"),
                    opt("independent of roughness"),
                ),
                "Colebrook is implicit (f appears on both sides) and is solved iteratively.",
            ),
            q(
                "In the fully rough regime at high Reynolds number, f:",
                (
                    opt("becomes nearly constant, independent of Re", correct=True),
                    opt("keeps falling as Re grows"),
                    opt("equals 64/Re"),
                    opt("becomes zero"),
                ),
                "At high Re viscosity stops mattering and f depends only on roughness.",
            ),
        ),
        "Boundary layers and flow separation": (
            q(
                "Prandtl's boundary-layer idea is that viscosity matters mainly:",
                (
                    opt("in a thin layer near the surface", correct=True),
                    opt("throughout the entire flow equally"),
                    opt("only far from the wall"),
                    opt("only in the wake"),
                ),
                "Viscous effects concentrate in a thin near-wall boundary layer.",
            ),
            q(
                "For a laminar flat plate the boundary-layer thickness grows as:",
                (
                    opt("delta/x ~ 5 / sqrt(Re_x)", correct=True),
                    opt("delta/x ~ Re_x"),
                    opt("delta/x ~ Re_x^2"),
                    opt("delta is constant"),
                ),
                "Blasius gives delta/x ~ 5/sqrt(Re_x).",
            ),
            q(
                "Boundary-layer separation is triggered by:",
                (
                    opt("an adverse pressure gradient (dp/dx > 0)", correct=True),
                    opt("a favourable pressure gradient"),
                    opt("constant pressure"),
                    opt("high viscosity alone"),
                ),
                "An adverse gradient reverses near-wall flow and detaches the layer.",
            ),
        ),
        "Drag, lift and bluff-body aerodynamics": (
            q(
                "Drag force scales with speed as:",
                (
                    opt("V squared", correct=True),
                    opt("V"),
                    opt("the square root of V"),
                    opt("1/V"),
                ),
                "F_D = C_D (1/2) rho V^2 A, so drag grows with V^2.",
            ),
            q(
                "Form (pressure) drag dominates for:",
                (
                    opt("bluff bodies with large separated wakes", correct=True),
                    opt("thin streamlined airfoils"),
                    opt("a flat plate aligned with the flow"),
                    opt("any body at zero speed"),
                ),
                "Bluff bodies separate and produce large wakes, dominated by form drag.",
            ),
            q(
                "The Strouhal number characterises:",
                (
                    opt("the vortex-shedding frequency behind a bluff body", correct=True),
                    opt("the compressibility of the flow"),
                    opt("the surface-tension force"),
                    opt("the pump head"),
                ),
                "St = f D / V ~ 0.2 sets the von Karman vortex-shedding frequency.",
            ),
        ),
        "Dimensional analysis and similitude": (
            q(
                "The Buckingham Pi theorem states that n variables in k dimensions yield:",
                (
                    opt("n - k independent dimensionless groups", correct=True),
                    opt("n + k groups"),
                    opt("n times k groups"),
                    opt("exactly one group"),
                ),
                "The number of independent Pi groups is n - k.",
            ),
            q(
                "The Froude number is most relevant to flows with:",
                (
                    opt("a free surface and gravity effects", correct=True),
                    opt("strong compressibility"),
                    opt("dominant surface tension"),
                    opt("only viscous effects"),
                ),
                "Fr = V/sqrt(gL) governs free-surface (ship, open-channel) flows.",
            ),
            q(
                "Dynamic similarity between a model and prototype requires:",
                (
                    opt("matching the governing dimensionless groups", correct=True),
                    opt("identical absolute velocities"),
                    opt("identical absolute sizes"),
                    opt("the same color of fluid"),
                ),
                "Matching the relevant Pi groups (e.g. Re, Fr) ensures similitude.",
            ),
        ),
        "Turbulence modelling and CFD": (
            q(
                "RANS turbulence models work by:",
                (
                    opt("solving the mean flow and modelling the Reynolds stresses", correct=True),
                    opt("resolving every turbulent eddy"),
                    opt("ignoring turbulence entirely"),
                    opt("assuming laminar flow"),
                ),
                "RANS solves the time-averaged equations with a closure like k-epsilon or k-omega SST.",
            ),
            q(
                "DNS (direct numerical simulation) is limited because cost scales roughly as:",
                (
                    opt("Re^(9/4)", correct=True),
                    opt("Re^(1/2)"),
                    opt("log Re"),
                    opt("independent of Re"),
                ),
                "Resolving all scales costs ~Re^(9/4) grid points, infeasible at high Re.",
            ),
            q(
                "In a finite-volume CFD workflow, verification refers to:",
                (
                    opt("checking mesh independence of the numerical solution", correct=True),
                    opt("comparing against experimental data"),
                    opt("choosing the geometry"),
                    opt("selecting a turbulence model"),
                ),
                "Verification = solving the equations right (mesh independence); validation = comparing to data.",
            ),
        ),
        "Shape optimisation: adjoint and ML methods": (
            q(
                "The key advantage of the adjoint method is that the gradient cost is:",
                (
                    opt("nearly independent of the number of design variables", correct=True),
                    opt("proportional to the number of design variables"),
                    opt("proportional to the square of the design variables"),
                    opt("always higher than finite differences"),
                ),
                "One adjoint solve per objective yields the full gradient regardless of variable count.",
            ),
            q(
                "A physics-informed neural network (PINN) incorporates:",
                (
                    opt("the governing PDE residual into its loss function", correct=True),
                    opt("only labelled experimental data"),
                    opt("no physics at all"),
                    opt("a fixed mesh of finite volumes"),
                ),
                "PINNs embed the Navier-Stokes residual in the training loss.",
            ),
            q(
                "Bayesian optimisation with a Gaussian-process surrogate is useful because it:",
                (
                    opt("reduces the number of expensive CFD evaluations needed", correct=True),
                    opt("eliminates the need for an objective function"),
                    opt("requires gradients of the true CFD solver"),
                    opt("only works for laminar flow"),
                ),
                "The surrogate replaces costly CFD runs, sampling efficiently toward the optimum.",
            ),
        ),
    },
    final=(
        q(
            "The Moody chart gives the friction factor as a function of:",
            (
                opt("Reynolds number and relative roughness", correct=True),
                opt("only the pipe diameter"),
                opt("only the flow rate"),
                opt("the fluid color"),
            ),
            "Moody plots f = f(Re, eps/D) for laminar through fully rough turbulent flow.",
        ),
        q(
            "Flow separation on an airfoil leads to:",
            (
                opt("stall and a large increase in form drag", correct=True),
                opt("reduced drag"),
                opt("increased lift indefinitely"),
                opt("laminar reattachment always"),
            ),
            "Separation under an adverse gradient causes stall and a wake-dominated drag rise.",
        ),
        q(
            "The drag crisis on a sphere is when C_D drops sharply because:",
            (
                opt("the boundary layer turns turbulent and delays separation", correct=True),
                opt("the sphere shrinks"),
                opt("viscosity vanishes"),
                opt("the flow becomes laminar"),
            ),
            "Near Re ~ 3e5 a turbulent layer separates later, shrinking the wake and C_D.",
        ),
        q(
            "Matching the Reynolds number for a 1:10 scale model in the same fluid requires:",
            (
                opt("ten times the prototype velocity", correct=True),
                opt("one tenth the prototype velocity"),
                opt("the same velocity"),
                opt("no velocity constraint"),
            ),
            "Re match with L reduced 10x and same fluid means V must increase 10x.",
        ),
        q(
            "Among RANS, LES and DNS, the cheapest industry workhorse is:",
            (
                opt("RANS", correct=True),
                opt("LES"),
                opt("DNS"),
                opt("all cost the same"),
            ),
            "RANS solves only the mean flow and is the standard low-cost industrial choice.",
        ),
        q(
            "The adjoint method enables large-scale aerodynamic shape optimisation because it:",
            (
                opt(
                    "computes the full gradient at a cost independent of variable count",
                    correct=True,
                ),
                opt("avoids solving the flow equations"),
                opt("requires one CFD run per design variable"),
                opt("only works for two design variables"),
            ),
            "Adjoint gradients make thousand-variable optimisation tractable.",
        ),
    ),
)
