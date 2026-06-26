"""Quiz questions for the Computational Fluid Dynamics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Scale-resolving simulation: LES, DES and DNS": (
            q(
                "DNS resolves:",
                (
                    opt("every turbulent scale down to the Kolmogorov microscale", correct=True),
                    opt("only the mean flow"),
                    opt("nothing below the mesh"),
                    opt("only the large eddies"),
                ),
                "DNS resolves all scales; its grid count scales as roughly Re^(9/4).",
            ),
            q(
                "LES works by:",
                (
                    opt("resolving large eddies and modelling subgrid scales", correct=True),
                    opt("modelling all turbulence like RANS"),
                    opt("ignoring turbulence"),
                    opt("solving only the energy equation"),
                ),
                "LES filters the field; an SGS model represents scales below the filter width.",
            ),
            q(
                "DES / hybrid RANS-LES is attractive for high-Re external flows because it:",
                (
                    opt(
                        "uses RANS in attached boundary layers and LES in separated regions",
                        correct=True,
                    ),
                    opt("uses DNS everywhere"),
                    opt("removes the need for a mesh"),
                    opt("ignores the boundary layer"),
                ),
                "Hybrid methods get LES fidelity in the wake at a fraction of wall-resolved cost.",
            ),
        ),
        "Verification, validation and the grid-convergence index": (
            q(
                "Verification answers the question:",
                (
                    opt("are we solving the equations right?", correct=True),
                    opt("are we solving the right equations?"),
                    opt("is the experiment correct?"),
                    opt("is the mesh pretty?"),
                ),
                "Verification = numerical correctness; validation = comparison to physical reality.",
            ),
            q(
                "Validation requires comparison against:",
                (
                    opt("trusted experimental data with its own uncertainty", correct=True),
                    opt("a finer CFD mesh only"),
                    opt("the initial guess"),
                    opt("the CAD file"),
                ),
                "Validation judges the model physics against measured data.",
            ),
            q(
                "The Grid Convergence Index (GCI) estimates:",
                (
                    opt(
                        "discretisation uncertainty from systematically refined meshes",
                        correct=True,
                    ),
                    opt("the turbulence intensity"),
                    opt("the wall temperature"),
                    opt("the parallel speedup"),
                ),
                "GCI uses three grids, the observed order and a safety factor to bound mesh error.",
            ),
        ),
        "The practical CFD workflow end to end": (
            q(
                "A common practical failure in CFD is:",
                (
                    opt("skipping mesh independence and trusting the first run", correct=True),
                    opt("checking quantities of interest"),
                    opt("cleaning up the CAD geometry"),
                    opt("validating against data"),
                ),
                "Without a mesh-independence study the result's accuracy is unknown.",
            ),
            q(
                "The first stage of a disciplined CFD workflow is to:",
                (
                    opt("define the question and the quantity of interest", correct=True),
                    opt("run the solver immediately"),
                    opt("buy a bigger cluster"),
                    opt("post-process contours"),
                ),
                "Knowing the target QoI and accuracy drives every later choice.",
            ),
            q(
                "During the solve it is best practice to monitor:",
                (
                    opt("a quantity of interest live, not just residuals", correct=True),
                    opt("only the wall-clock time"),
                    opt("the CAD file size"),
                    opt("the number of colours in the plot"),
                ),
                "A steady drag/heat-load value is a stronger convergence signal than residuals alone.",
            ),
        ),
        "High-performance computing and parallel scaling": (
            q(
                "CFD is parallelised mainly through:",
                (
                    opt("domain decomposition with halo exchange between ranks", correct=True),
                    opt("running the same mesh on every core"),
                    opt("removing the boundary conditions"),
                    opt("using a single thread"),
                ),
                "The mesh is partitioned; ranks exchange ghost-cell data via MPI each iteration.",
            ),
            q(
                "Amdahl's law implies that for a fixed problem, speedup is:",
                (
                    opt("capped by the serial fraction of the work", correct=True),
                    opt("unlimited with more cores"),
                    opt("always equal to the core count"),
                    opt("independent of parallel fraction"),
                ),
                "S(N) = 1/((1-P)+P/N); even 95% parallel caps speedup near 20x.",
            ),
            q(
                "Weak scaling (Gustafson) for CFD aims to:",
                (
                    opt("keep cells-per-core roughly constant as the problem grows", correct=True),
                    opt("shrink the problem as cores increase"),
                    opt("use one core only"),
                    opt("eliminate communication"),
                ),
                "Holding ~50k-200k cells/core keeps communication overhead bounded.",
            ),
        ),
        "Adjoint-based shape optimisation": (
            q(
                "A finite-difference gradient over design variables costs:",
                (
                    opt("about one CFD solve per design variable", correct=True),
                    opt("one solve regardless of variables"),
                    opt("zero solves"),
                    opt("one adjoint solve total"),
                ),
                "That scaling is why FD is hopeless for thousands of parameters.",
            ),
            q(
                "The key advantage of the adjoint method is that its gradient cost is:",
                (
                    opt("nearly independent of the number of design variables", correct=True),
                    opt("proportional to the number of variables"),
                    opt("proportional to the mesh size squared"),
                    opt("always larger than finite differences"),
                ),
                "One extra adjoint solve per objective yields the full gradient.",
            ),
            q(
                "Discrete vs continuous adjoints trade off:",
                (
                    opt("gradient consistency against derivation effort", correct=True),
                    opt("mesh size against time step"),
                    opt("density against viscosity"),
                    opt("inlet against outlet"),
                ),
                "Discrete adjoints match the discrete primal exactly; continuous ones are easier to derive.",
            ),
        ),
        "Machine-learning-accelerated CFD": (
            q(
                "A surrogate (reduced-order) model is used to:",
                (
                    opt(
                        "predict outputs quickly from a few CFD runs for many-query design",
                        correct=True,
                    ),
                    opt("replace the mesh"),
                    opt("eliminate boundary conditions"),
                    opt("increase the Reynolds number"),
                ),
                "Surrogates enable fast Bayesian optimisation and design sweeps.",
            ),
            q(
                "A Physics-Informed Neural Network (PINN) embeds in its loss:",
                (
                    opt("the Navier-Stokes residual", correct=True),
                    opt("the mesh skewness"),
                    opt("the CFL number"),
                    opt("the CAD geometry"),
                ),
                "PINNs penalise the PDE residual so the network respects the governing equations.",
            ),
            q(
                "The central risk of ML-accelerated CFD is:",
                (
                    opt("poor generalisation outside the training envelope", correct=True),
                    opt("being conservative by construction"),
                    opt("guaranteeing exact results"),
                    opt("never needing validation"),
                ),
                "ML models can fail outside their training data, so V&V remains essential.",
            ),
        ),
    },
    final=(
        q(
            "Ranked by cost from cheapest to most expensive, the methods are:",
            (
                opt("RANS, LES, DNS", correct=True),
                opt("DNS, LES, RANS"),
                opt("LES, DNS, RANS"),
                opt("DNS, RANS, LES"),
            ),
            "RANS models all scales (cheapest); DNS resolves everything (most costly).",
        ),
        q(
            "The GCI is computed from:",
            (
                opt("three systematically refined meshes and the observed order", correct=True),
                opt("a single mesh"),
                opt("the inlet velocity"),
                opt("the number of cores"),
            ),
            "Roache's GCI estimates discretisation uncertainty from a refinement study.",
        ),
        q(
            "A trustworthy CFD result must include:",
            (
                opt("quantified uncertainty via verification and validation", correct=True),
                opt("only a colourful contour plot"),
                opt("the fastest possible run time"),
                opt("a single un-refined mesh"),
            ),
            "V&V (e.g. ASME V&V 20) underpins credible CFD.",
        ),
        q(
            "Amdahl's law limits strong-scaling speedup because of:",
            (
                opt("the non-parallel (serial) fraction of the work", correct=True),
                opt("too many cells per core"),
                opt("the turbulence model"),
                opt("the outlet pressure"),
            ),
            "S(N) = 1/((1-P)+P/N) saturates as N grows.",
        ),
        q(
            "The adjoint method makes large-scale shape optimisation tractable by:",
            (
                opt(
                    "delivering the full gradient at near-constant cost in design variables",
                    correct=True,
                ),
                opt("requiring one solve per variable"),
                opt("avoiding any flow solve"),
                opt("refining the mesh automatically"),
            ),
            "One adjoint solve per objective gives dJ/dalpha for all parameters.",
        ),
        q(
            "Machine learning is reshaping CFD mainly as:",
            (
                opt("surrogates, learned closures and PINNs that augment the solver", correct=True),
                opt("a complete replacement that needs no validation"),
                opt("a meshing-only tool"),
                opt("a way to remove conservation laws"),
            ),
            "ML accelerates the pipeline but still demands V&V rigour.",
        ),
    ),
)
