"""Quiz questions for the Fluid Mechanics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Conservation of mass and the continuity equation": (
            q(
                "For steady incompressible flow in a duct, continuity gives:",
                (
                    opt("A1 V1 = A2 V2", correct=True),
                    opt("A1 V1 = A2 / V2"),
                    opt("A1 / V1 = A2 V2"),
                    opt("V1 + V2 = constant"),
                ),
                "Constant volumetric flow Q = A V means A1 V1 = A2 V2.",
            ),
            q(
                "The Reynolds transport theorem converts a system law into:",
                (
                    opt("a control-volume statement", correct=True),
                    opt("a molecular dynamics model"),
                    opt("a dimensionless group"),
                    opt("a turbulence closure"),
                ),
                "RTT relates the rate of change for the system to storage plus net flux in a control volume.",
            ),
            q(
                "When the area of a duct decreases at fixed Q, the velocity:",
                (
                    opt("increases", correct=True),
                    opt("decreases"),
                    opt("stays the same"),
                    opt("drops to zero"),
                ),
                "V = Q/A, so smaller area means higher velocity.",
            ),
        ),
        "Bernoulli's equation and its assumptions": (
            q(
                "Bernoulli's equation requires the flow to be:",
                (
                    opt("steady, incompressible, frictionless along a streamline", correct=True),
                    opt("unsteady and viscous"),
                    opt("compressible with shaft work"),
                    opt("turbulent with heat addition"),
                ),
                "Bernoulli holds for steady, incompressible, inviscid flow with no shaft work.",
            ),
            q(
                "In Bernoulli's equation, the term (1/2) rho V^2 represents:",
                (
                    opt("dynamic pressure", correct=True),
                    opt("static pressure"),
                    opt("hydrostatic pressure"),
                    opt("shaft work"),
                ),
                "The three terms are static p, dynamic (1/2) rho V^2, and hydrostatic rho g z.",
            ),
            q(
                "A Pitot tube infers speed from:",
                (
                    opt("the difference between stagnation and static pressure", correct=True),
                    opt("the absolute temperature"),
                    opt("the pipe roughness"),
                    opt("the fluid density alone"),
                ),
                "V = sqrt(2 (p0 - p)/rho) from the measured pressure difference.",
            ),
        ),
        "The momentum equation on a control volume": (
            q(
                "For steady flow with one inlet and one outlet, the net force equals:",
                (
                    opt("mdot (V_out - V_in)", correct=True),
                    opt("mdot (V_out + V_in)"),
                    opt("rho g h"),
                    opt("zero always"),
                ),
                "Sum F = mdot (V_out - V_in), the momentum flux difference.",
            ),
            q(
                "The momentum equation is most directly used to size:",
                (
                    opt("anchoring forces on pipe bends and nozzles", correct=True),
                    opt("the fluid viscosity"),
                    opt("the Reynolds number"),
                    opt("surface tension"),
                ),
                "Reaction/anchoring forces on bends, reducers, nozzles and jets come from momentum balance.",
            ),
            q(
                "A jet of speed V hitting a fixed plate normally exerts a force of:",
                (
                    opt("rho A V^2", correct=True),
                    opt("rho A V"),
                    opt("(1/2) rho A V"),
                    opt("rho A / V"),
                ),
                "F = mdot V = (rho A V) V = rho A V^2.",
            ),
        ),
        "The energy equation and head losses": (
            q(
                "Compared with Bernoulli, the engineering energy equation adds:",
                (
                    opt("pump head, turbine head and head loss", correct=True),
                    opt("only the elevation term"),
                    opt("the Reynolds number"),
                    opt("surface tension"),
                ),
                "It restores machines (h_p, h_t) and losses (h_L) that Bernoulli omits.",
            ),
            q(
                "Major head loss in a pipe is given by the Darcy-Weisbach equation as:",
                (
                    opt("f (L/D) V^2 / (2g)", correct=True),
                    opt("f (D/L) V / (2g)"),
                    opt("f L D V^2"),
                    opt("V^2 / (f L D)"),
                ),
                "h_L,major = f (L/D) V^2/(2g); fittings add sum K V^2/(2g).",
            ),
            q(
                "The operating point of a pumped system is where:",
                (
                    opt("the pump curve intersects the system curve", correct=True),
                    opt("the head loss is zero"),
                    opt("the flow is zero"),
                    opt("the Reynolds number equals 2300"),
                ),
                "The intersection of pump head and required system head sets the delivered flow.",
            ),
        ),
        "The Navier-Stokes equations and exact solutions": (
            q(
                "The term that makes the Navier-Stokes equations nonlinear is:",
                (
                    opt("the convective term (u . grad) u", correct=True),
                    opt("the pressure gradient"),
                    opt("the viscous diffusion term"),
                    opt("the gravity body force"),
                ),
                "The convective inertia (u . grad)u is nonlinear and underlies turbulence.",
            ),
            q(
                "Fully developed laminar pipe flow has a velocity profile that is:",
                (
                    opt("parabolic with u_max = 2 times the mean", correct=True),
                    opt("uniform (plug) across the pipe"),
                    opt("linear from wall to centre"),
                    opt("zero everywhere"),
                ),
                "Hagen-Poiseuille flow is parabolic; the centreline speed is twice the mean.",
            ),
            q(
                "The viscous term in the incompressible Navier-Stokes equations is:",
                (
                    opt("mu times the Laplacian of velocity", correct=True),
                    opt("rho times velocity"),
                    opt("the gradient of pressure"),
                    opt("rho g"),
                ),
                "Viscous diffusion is mu (grad^2 u).",
            ),
        ),
        "Laminar vs turbulent flow and the Reynolds number": (
            q(
                "The Reynolds number is the ratio of:",
                (
                    opt("inertial to viscous forces", correct=True),
                    opt("pressure to gravity forces"),
                    opt("surface tension to inertia"),
                    opt("density to viscosity only"),
                ),
                "Re = rho V D / mu compares inertial and viscous forces.",
            ),
            q(
                "Pipe flow is generally laminar for Reynolds numbers below about:",
                (
                    opt("2300", correct=True),
                    opt("100"),
                    opt("50000"),
                    opt("1000000"),
                ),
                "Transition begins near Re ~ 2300; flow is turbulent above ~4000.",
            ),
            q(
                "For laminar pipe flow the friction factor is:",
                (
                    opt("f = 64/Re", correct=True),
                    opt("f = Re/64"),
                    opt("f = 0.316 Re"),
                    opt("f = constant"),
                ),
                "Laminar pipe flow has the exact closed form f = 64/Re.",
            ),
        ),
    },
    final=(
        q(
            "Continuity for steady incompressible duct flow states that:",
            (
                opt("the volumetric flow Q = A V is constant", correct=True),
                opt("the velocity is constant"),
                opt("the pressure is constant"),
                opt("the area is constant"),
            ),
            "Q = A V is conserved, so velocity rises where area falls.",
        ),
        q(
            "Which assumption is NOT required for Bernoulli's equation?",
            (
                opt("The flow must be turbulent", correct=True),
                opt("The flow is steady"),
                opt("The flow is incompressible"),
                opt("The flow is frictionless along a streamline"),
            ),
            "Bernoulli requires steady, incompressible, inviscid flow; it does not require turbulence.",
        ),
        q(
            "The steady control-volume momentum equation gives the net force as:",
            (
                opt("mdot (V_out - V_in)", correct=True),
                opt("rho g h"),
                opt("f (L/D) V^2/(2g)"),
                opt("zero"),
            ),
            "Net force equals the momentum-flux difference, mdot (V_out - V_in).",
        ),
        q(
            "Pump shaft power for a head h_p and efficiency eta is:",
            (
                opt("rho g Q h_p / eta", correct=True),
                opt("rho g Q h_p * eta"),
                opt("rho g Q / (h_p eta)"),
                opt("Q h_p / (rho g)"),
            ),
            "Useful power is rho g Q h_p; dividing by eta gives the shaft power.",
        ),
        q(
            "The nonlinearity of the Navier-Stokes equations comes from:",
            (
                opt("the convective inertia term", correct=True),
                opt("the body-force term"),
                opt("the pressure term"),
                opt("the continuity constraint"),
            ),
            "The (u . grad)u convective term is the nonlinear source of turbulence.",
        ),
        q(
            "A pipe-flow Reynolds number of 8000 indicates:",
            (
                opt("turbulent flow", correct=True),
                opt("laminar flow"),
                opt("static fluid"),
                opt("supersonic flow"),
            ),
            "Re = 8000 is well above ~4000, so the flow is turbulent.",
        ),
    ),
)
