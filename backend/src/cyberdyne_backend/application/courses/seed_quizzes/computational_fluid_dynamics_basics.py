"""Quiz questions for the Computational Fluid Dynamics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What CFD is and the governing equations": (
            q(
                "Which three conservation laws form the basis of CFD?",
                (
                    opt("mass, momentum and energy", correct=True),
                    opt("charge, spin and energy"),
                    opt("force, torque and power"),
                    opt("pressure, temperature and density"),
                ),
                "CFD solves the conservation of mass, momentum (Navier-Stokes) and energy.",
            ),
            q(
                "Why are the Navier-Stokes equations hard to solve analytically?",
                (
                    opt("the convective term makes them nonlinear", correct=True),
                    opt("they are purely linear"),
                    opt("they have no pressure term"),
                    opt("they ignore viscosity entirely"),
                ),
                "The convective term (u . grad)u is nonlinear, which also makes turbulence possible.",
            ),
            q(
                "The continuity equation for incompressible flow states that:",
                (
                    opt("the divergence of velocity is zero", correct=True),
                    opt("pressure equals density"),
                    opt("velocity is constant in time"),
                    opt("viscosity is zero"),
                ),
                "Incompressible continuity is div(u) = 0.",
            ),
        ),
        "From PDEs to a grid: discretisation": (
            q(
                "Why must the PDEs be discretised?",
                (
                    opt("a computer cannot store a continuous field", correct=True),
                    opt("the equations are linear"),
                    opt("fluids have no viscosity"),
                    opt("to remove the pressure term"),
                ),
                "Derivatives are replaced by algebraic approximations at a finite set of cells/points.",
            ),
            q(
                "Which method is conservative by construction and dominates commercial CFD?",
                (
                    opt("finite volume (FVM)", correct=True),
                    opt("finite difference (FDM)"),
                    opt("spectral collocation"),
                    opt("Monte Carlo"),
                ),
                "FVM integrates the conservation law per cell, so flux leaving one cell enters its neighbour.",
            ),
            q(
                "A second-order scheme has a truncation error that scales as:",
                (
                    opt("dx^2", correct=True),
                    opt("dx"),
                    opt("1/dx"),
                    opt("constant"),
                ),
                "Second order means halving dx cuts the error roughly fourfold.",
            ),
        ),
        "The finite-volume method and fluxes": (
            q(
                "In FVM, a volume integral of a flux is converted into:",
                (
                    opt("a sum of fluxes through the cell faces", correct=True),
                    opt("a single value at the cell centre"),
                    opt("a time derivative"),
                    opt("a surface tension term"),
                ),
                "The divergence theorem turns the volume integral into face-flux sums.",
            ),
            q(
                "Why is FVM globally conservative?",
                (
                    opt("flux leaving one cell exactly enters its neighbour", correct=True),
                    opt("it ignores diffusion"),
                    opt("it uses only structured meshes"),
                    opt("it assumes inviscid flow"),
                ),
                "Shared-face fluxes cancel, so the global balance is exact regardless of mesh quality.",
            ),
            q(
                "The face value of the transported scalar is obtained by:",
                (
                    opt("interpolation from neighbouring cell centroids", correct=True),
                    opt("setting it to zero"),
                    opt("the global average"),
                    opt("the inlet value everywhere"),
                ),
                "The interpolation/scheme choice controls accuracy and stability.",
            ),
        ),
        "Meshes: structured, unstructured and quality": (
            q(
                "An unstructured mesh is preferred when:",
                (
                    opt("the geometry is complex and arbitrary", correct=True),
                    opt("the domain is a perfect box"),
                    opt("you need (i,j,k) ordering"),
                    opt("there are no walls"),
                ),
                "Unstructured tet/poly meshes handle industrial geometry flexibly.",
            ),
            q(
                "Which is a mesh quality metric to keep low?",
                (
                    opt("skewness", correct=True),
                    opt("Reynolds number"),
                    opt("Mach number"),
                    opt("density"),
                ),
                "High skewness distorts cells and causes numerical diffusion or divergence.",
            ),
            q(
                "Prism layers near a wall in a hybrid mesh are used to:",
                (
                    opt("resolve the boundary layer", correct=True),
                    opt("speed up the bulk flow"),
                    opt("remove the need for BCs"),
                    opt("make the mesh coarser"),
                ),
                "Thin prism layers capture the steep near-wall gradients.",
            ),
        ),
        "Boundary and initial conditions": (
            q(
                "A Dirichlet boundary condition fixes:",
                (
                    opt("the value of the variable", correct=True),
                    opt("the normal gradient"),
                    opt("the second derivative"),
                    opt("the time step"),
                ),
                "Dirichlet sets the value (e.g. inlet velocity); Neumann sets the gradient.",
            ),
            q(
                "A no-slip wall imposes:",
                (
                    opt("zero fluid velocity at the wall", correct=True),
                    opt("zero pressure"),
                    opt("maximum velocity"),
                    opt("zero temperature"),
                ),
                "Viscous fluids satisfy u = 0 at a solid wall (no-slip).",
            ),
            q(
                "Fixing both velocity and pressure at the same patch tends to make the problem:",
                (
                    opt("over-constrained / ill-posed", correct=True),
                    opt("more accurate"),
                    opt("conservative"),
                    opt("faster to converge"),
                ),
                "BCs must be physically consistent; over-specifying makes the problem ill-posed.",
            ),
        ),
        "Convergence and residuals": (
            q(
                "A residual measures:",
                (
                    opt(
                        "how far the fields are from satisfying the discretised equations",
                        correct=True,
                    ),
                    opt("the wall temperature"),
                    opt("the mesh skewness"),
                    opt("the Reynolds number"),
                ),
                "The residual is the per-cell imbalance b - A x of the discretised system.",
            ),
            q(
                "Besides low residuals, convergence should also be judged by:",
                (
                    opt("monitored quantities of interest flattening out", correct=True),
                    opt("the number of cells"),
                    opt("the colour of the contour plot"),
                    opt("the CAD file size"),
                ),
                "A steady drag/mass-flow value matters as much as a small residual.",
            ),
            q(
                "Under-relaxation factors are used to:",
                (
                    opt("stabilise the nonlinear iteration by damping updates", correct=True),
                    opt("increase the time step without limit"),
                    opt("remove boundary conditions"),
                    opt("refine the mesh automatically"),
                ),
                "phi_new = phi_old + alpha*delta; too large diverges, too small slows convergence.",
            ),
        ),
    },
    final=(
        q(
            "CFD primarily solves which set of governing equations?",
            (
                opt("the Navier-Stokes (conservation) equations", correct=True),
                opt("Maxwell's equations"),
                opt("Schrodinger's equation"),
                opt("the heat equation only"),
            ),
            "CFD discretises the conservation of mass, momentum and energy.",
        ),
        q(
            "The finite-volume method is favoured because it is:",
            (
                opt("conservative by construction", correct=True),
                opt("limited to 1-D problems"),
                opt("only valid for inviscid flow"),
                opt("independent of the mesh"),
            ),
            "FVM enforces conservation on every cell via face fluxes.",
        ),
        q(
            "Refining the mesh generally:",
            (
                opt("reduces discretisation error at higher cost", correct=True),
                opt("increases error"),
                opt("has no effect on accuracy"),
                opt("removes the need for boundary conditions"),
            ),
            "More cells lower truncation error but cost more memory and time.",
        ),
        q(
            "A pressure outlet boundary condition typically:",
            (
                opt("fixes pressure and lets velocity adjust", correct=True),
                opt("fixes velocity and lets pressure adjust"),
                opt("sets u = 0"),
                opt("imposes symmetry"),
            ),
            "Outlets commonly fix gauge pressure with zero-gradient velocity.",
        ),
        q(
            "Convergence of an iterative CFD solve is indicated by:",
            (
                opt("residuals dropping and monitors becoming steady", correct=True),
                opt("a single iteration"),
                opt("a larger mesh"),
                opt("a higher Reynolds number"),
            ),
            "Both falling residuals and flat quantities of interest are needed.",
        ),
        q(
            "The continuum hypothesis underlying CFD assumes:",
            (
                opt("fluid properties are smooth fields, not individual molecules", correct=True),
                opt("the fluid is a vacuum"),
                opt("molecules are tracked one by one"),
                opt("viscosity is always zero"),
            ),
            "CFD treats density, velocity and pressure as continuous fields.",
        ),
    ),
)
