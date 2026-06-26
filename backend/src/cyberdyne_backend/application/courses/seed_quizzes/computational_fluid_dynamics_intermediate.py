"""Quiz questions for the Computational Fluid Dynamics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Convection-diffusion discretisation schemes": (
            q(
                "The local Peclet number compares:",
                (
                    opt("convection to diffusion", correct=True),
                    opt("pressure to velocity"),
                    opt("inertia to gravity"),
                    opt("time step to cell size"),
                ),
                "Pe = rho u dx / Gamma measures the strength of convection relative to diffusion.",
            ),
            q(
                "Central differencing for convection becomes unbounded (oscillates) when:",
                (
                    opt("the cell Peclet number exceeds 2", correct=True),
                    opt("the mesh is structured"),
                    opt("the flow is laminar"),
                    opt("the time step is small"),
                ),
                "CDS is second order but unstable for |Pe| > 2, producing wiggles.",
            ),
            q(
                "First-order upwind is stable but introduces:",
                (
                    opt("numerical (false) diffusion that smears gradients", correct=True),
                    opt("negative density"),
                    opt("perfect accuracy"),
                    opt("zero error"),
                ),
                "Upwind is bounded but smears steep gradients with artificial diffusion.",
            ),
        ),
        "Stability and the CFL condition": (
            q(
                "The CFL (Courant) number is defined as:",
                (
                    opt("u dt / dx", correct=True),
                    opt("dx / (u dt)"),
                    opt("rho u dx / mu"),
                    opt("u / sqrt(g dx)"),
                ),
                "CFL = u dt / dx; it measures cells crossed per time step.",
            ),
            q(
                "For an explicit advection scheme, stability requires:",
                (
                    opt("CFL <= 1", correct=True),
                    opt("CFL >= 10"),
                    opt("CFL = 0"),
                    opt("CFL < -1"),
                ),
                "Information must not cross more than one cell per step (CFL <= 1).",
            ),
            q(
                "Compared with explicit schemes, implicit schemes are:",
                (
                    opt("unconditionally stable but solve a system each step", correct=True),
                    opt("always cheaper per step"),
                    opt("limited to CFL < 1"),
                    opt("unable to handle diffusion"),
                ),
                "Implicit methods allow large dt at the cost of a linear solve per step.",
            ),
        ),
        "Pressure-velocity coupling and SIMPLE": (
            q(
                "In incompressible flow, continuity acts as:",
                (
                    opt("a constraint with no explicit pressure equation", correct=True),
                    opt("an evolution equation for pressure"),
                    opt("the energy equation"),
                    opt("a turbulence model"),
                ),
                "Pressure is the field that enforces div(u) = 0; there is no standalone pressure PDE.",
            ),
            q(
                "What does the SIMPLE algorithm compute and apply each outer iteration?",
                (
                    opt(
                        "a pressure correction that drives velocity toward continuity", correct=True
                    ),
                    opt("the mesh size"),
                    opt("the turbulence intensity"),
                    opt("the CFL number"),
                ),
                "SIMPLE: guess p*, solve momentum, derive p', correct u and p, repeat.",
            ),
            q(
                "PISO differs from SIMPLE mainly by:",
                (
                    opt("using extra pressure correctors, suiting transient runs", correct=True),
                    opt("ignoring continuity"),
                    opt("being explicit only"),
                    opt("requiring no momentum solve"),
                ),
                "PISO adds neighbour/skewness correctors and is common for transient simulation.",
            ),
        ),
        "Turbulence modelling: RANS and two-equation models": (
            q(
                "Reynolds-averaging the Navier-Stokes equations introduces:",
                (
                    opt("the Reynolds stress tensor (closure problem)", correct=True),
                    opt("an extra pressure equation"),
                    opt("zero new unknowns"),
                    opt("a gravitational term"),
                ),
                "Averaging the nonlinear term yields -rho <u'_i u'_j>, which must be modelled.",
            ),
            q(
                "The Boussinesq hypothesis models the Reynolds stress using:",
                (
                    opt("an eddy (turbulent) viscosity", correct=True),
                    opt("the speed of sound"),
                    opt("surface tension"),
                    opt("the CFL number"),
                ),
                "It relates Reynolds stress to the mean strain rate via mu_t.",
            ),
            q(
                "Which model blends near-wall and free-stream behaviour and is a default for aerodynamics?",
                (
                    opt("k-omega SST", correct=True),
                    opt("pure k-epsilon"),
                    opt("inviscid Euler"),
                    opt("potential flow"),
                ),
                "k-omega SST uses k-omega near walls and k-epsilon away, handling separation well.",
            ),
        ),
        "Near-wall treatment and the y-plus criterion": (
            q(
                "The dimensionless wall distance y+ is defined using:",
                (
                    opt("the friction velocity u_tau and first-cell distance", correct=True),
                    opt("the free-stream Mach number"),
                    opt("the domain length"),
                    opt("the time step"),
                ),
                "y+ = u_tau * y / nu, with u_tau = sqrt(tau_w/rho).",
            ),
            q(
                "For a wall-resolved approach, the first cell should sit at about:",
                (
                    opt("y+ ~ 1 (viscous sublayer)", correct=True),
                    opt("y+ ~ 1000"),
                    opt("y+ ~ 15 (buffer layer)"),
                    opt("y+ ~ 500"),
                ),
                "Wall-resolved meshing needs y+ around 1; wall functions target 30-300.",
            ),
            q(
                "Landing the first cell in the buffer layer (5 < y+ < 30) is undesirable because:",
                (
                    opt("neither the sublayer law nor the log law applies well", correct=True),
                    opt("it is the most accurate region"),
                    opt("it removes the boundary layer"),
                    opt("it guarantees convergence"),
                ),
                "The buffer layer is a transition zone poorly captured by either model.",
            ),
        ),
        "Transient simulation and time integration": (
            q(
                "Which time scheme is second order, stable, and a common production default?",
                (
                    opt("second-order backward (BDF2)", correct=True),
                    opt("explicit Euler"),
                    opt("implicit Euler (first order)"),
                    opt("no time scheme"),
                ),
                "BDF2 balances stability and second-order accuracy for transient CFD.",
            ),
            q(
                "Implicit Euler is unconditionally stable but:",
                (
                    opt("only first order and can over-damp oscillations", correct=True),
                    opt("third order accurate"),
                    opt("limited to CFL < 0.1"),
                    opt("cannot be used for unsteady flow"),
                ),
                "Backward Euler is robust but first order and numerically dissipative.",
            ),
            q(
                "The Strouhal number St = fD/U helps set the time step by:",
                (
                    opt(
                        "fixing the shedding frequency so you resolve enough steps per cycle",
                        correct=True,
                    ),
                    opt("giving the mesh size"),
                    opt("setting the pressure outlet"),
                    opt("defining the turbulence model"),
                ),
                "St ~ 0.2 gives the vortex-shedding frequency; aim for ~20-40 steps per cycle.",
            ),
        ),
    },
    final=(
        q(
            "First-order upwind differencing is chosen for its:",
            (
                opt("boundedness/stability, at the cost of numerical diffusion", correct=True),
                opt("second-order accuracy"),
                opt("zero truncation error"),
                opt("ability to ignore convection"),
            ),
            "Upwind is robust but smears gradients with false diffusion.",
        ),
        q(
            "An explicit solver diverges when:",
            (
                opt("the CFL number exceeds its stability limit", correct=True),
                opt("the mesh is too fine"),
                opt("residuals are too low"),
                opt("pressure is fixed at the outlet"),
            ),
            "Exceeding CFL ~ 1 makes an explicit advection scheme unstable.",
        ),
        q(
            "The SIMPLE algorithm exists to:",
            (
                opt("couple pressure and velocity to satisfy continuity", correct=True),
                opt("generate the mesh"),
                opt("model turbulence"),
                opt("set boundary conditions"),
            ),
            "It iterates momentum and a pressure correction until mass is conserved.",
        ),
        q(
            "RANS turbulence modelling solves for:",
            (
                opt("the mean flow with modelled Reynolds stresses", correct=True),
                opt("every turbulent eddy directly"),
                opt("only the pressure field"),
                opt("an inviscid flow"),
            ),
            "RANS resolves the averaged fields and closes the Reynolds stress.",
        ),
        q(
            "A y+ near 1 is required when you want to:",
            (
                opt("resolve the viscous sublayer (wall-resolved)", correct=True),
                opt("use wall functions"),
                opt("coarsen the mesh"),
                opt("ignore the boundary layer"),
            ),
            "Wall-resolved heat transfer and separation need first cells in the sublayer.",
        ),
        q(
            "For transient CFD, the time step is typically chosen to:",
            (
                opt("keep CFL near 1 and resolve the unsteady physics", correct=True),
                opt("be as large as possible regardless of physics"),
                opt("equal the mesh skewness"),
                opt("match the Reynolds number"),
            ),
            "Even with implicit schemes, CFL ~ 1 resolves the relevant time scales.",
        ),
    ),
)
