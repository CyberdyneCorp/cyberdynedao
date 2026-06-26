"""Quiz questions for the Mechanics of Materials - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Beam deflection: integration and energy methods": (
            q(
                "The Euler-Bernoulli beam equation relates curvature to moment by:",
                (
                    opt("E I times the second derivative of v equals M(x)", correct=True),
                    opt("E I times v equals M(x)"),
                    opt("E I times the first derivative of v equals M(x)"),
                    opt("v equals M(x) divided by E I"),
                ),
                "EI d2v/dx2 = M(x); integrate twice with boundary conditions.",
            ),
            q(
                "The tip deflection of a cantilever with end load P is:",
                (
                    opt("P L^3 / (3 E I)", correct=True),
                    opt("P L / (3 E I)"),
                    opt("P L^2 / (2 E I)"),
                    opt("P L^4 / (8 E I)"),
                ),
                "delta_tip = PL^3/(3EI); the cubic dependence on L dominates.",
            ),
            q(
                "Castigliano's second theorem gives a deflection as:",
                (
                    opt(
                        "the partial derivative of strain energy with respect to the load",
                        correct=True,
                    ),
                    opt("the integral of stress over area"),
                    opt("the product of force and length"),
                    opt("the second derivative of the moment"),
                ),
                "delta_i = dU/dP_i, with U the strain energy.",
            ),
        ),
        "Stress transformation and Mohr's circle": (
            q(
                "Principal stresses are the normal stresses on the plane where:",
                (
                    opt("the shear stress is zero", correct=True),
                    opt("the shear stress is maximum"),
                    opt("the normal stress is zero"),
                    opt("the area is largest"),
                ),
                "Principal planes carry no shear; they give the extreme normal stresses.",
            ),
            q(
                "On Mohr's circle, the centre is located at:",
                (
                    opt("the average normal stress (sigma_x + sigma_y)/2", correct=True),
                    opt("the maximum shear stress"),
                    opt("the origin always"),
                    opt("sigma_x only"),
                ),
                "The circle is centred at the average normal stress, with radius equal to tau_max.",
            ),
            q(
                "The radius of Mohr's circle equals:",
                (
                    opt("the maximum in-plane shear stress", correct=True),
                    opt("the average normal stress"),
                    opt("the larger principal stress"),
                    opt("zero for plane stress"),
                ),
                "The radius is sqrt(((sx-sy)/2)^2 + txy^2) = tau_max in-plane.",
            ),
        ),
        "Combined loading and pressure vessels": (
            q(
                "Within linear elasticity, stresses from several loads at a point are combined by:",
                (
                    opt("superposition (adding the individual contributions)", correct=True),
                    opt("multiplying them"),
                    opt("taking only the largest one"),
                    opt("averaging them"),
                ),
                "Linear elasticity allows superposition of axial, bending and torsion stresses.",
            ),
            q(
                "In a thin-walled cylindrical pressure vessel, the hoop stress is:",
                (
                    opt("twice the longitudinal stress", correct=True),
                    opt("half the longitudinal stress"),
                    opt("equal to the longitudinal stress"),
                    opt("zero"),
                ),
                "sigma_hoop = pr/t is twice sigma_long = pr/2t.",
            ),
            q(
                "For a thin-walled sphere under internal pressure, the wall stress is:",
                (
                    opt("p r / (2 t) in all directions", correct=True),
                    opt("p r / t in all directions"),
                    opt("2 p r / t"),
                    opt("zero"),
                ),
                "A sphere has sigma = pr/2t uniformly, lower than a cylinder's hoop stress.",
            ),
        ),
        "Column buckling and stability": (
            q(
                "The Euler critical buckling load for a pin-ended column is:",
                (
                    opt("pi^2 E I / (K L)^2", correct=True),
                    opt("E I / (K L)"),
                    opt("pi E I / (K L)"),
                    opt("E A / L"),
                ),
                "P_cr = pi^2 E I / (KL)^2.",
            ),
            q(
                "Euler buckling depends primarily on:",
                (
                    opt("stiffness E I and geometry, not material strength", correct=True),
                    opt("the yield strength only"),
                    opt("the ultimate tensile strength only"),
                    opt("Poisson's ratio only"),
                ),
                "Buckling is a stability phenomenon governed by EI and effective length.",
            ),
            q(
                "As a column's length increases, the Euler critical load:",
                (
                    opt("decreases with the inverse square of length", correct=True),
                    opt("increases linearly"),
                    opt("stays constant"),
                    opt("increases with the square of length"),
                ),
                "P_cr is proportional to 1/(KL)^2, so longer columns are much weaker.",
            ),
        ),
        "Failure theories and fatigue": (
            q(
                "The von Mises criterion is most appropriate for:",
                (
                    opt("yielding of ductile metals", correct=True),
                    opt("brittle fracture"),
                    opt("buckling"),
                    opt("thermal expansion"),
                ),
                "Von Mises (distortion energy) predicts yield in ductile metals.",
            ),
            q(
                "An S-N (Wohler) curve plots:",
                (
                    opt("stress amplitude versus cycles to failure", correct=True),
                    opt("stress versus strain"),
                    opt("load versus deflection"),
                    opt("temperature versus time"),
                ),
                "The S-N curve shows fatigue life: stress amplitude vs number of cycles.",
            ),
            q(
                "An endurance limit (in steels) is:",
                (
                    opt(
                        "a stress amplitude below which fatigue life is effectively infinite",
                        correct=True,
                    ),
                    opt("the static yield strength"),
                    opt("the ultimate tensile strength"),
                    opt("the buckling stress"),
                ),
                "Below the endurance limit, many steels do not fail by fatigue.",
            ),
        ),
        "Finite element method and structural optimization": (
            q(
                "The core linear system solved in static FEM is:",
                (
                    opt("K u = F (stiffness times displacement equals force)", correct=True),
                    opt("u = K F"),
                    opt("F = u / K"),
                    opt("K = u F"),
                ),
                "Assemble the global stiffness K and solve K u = F for displacements.",
            ),
            q(
                "Element stiffness matrices are combined into the global system by:",
                (
                    opt(
                        "assembly (adding contributions at shared degrees of freedom)", correct=True
                    ),
                    opt("multiplying all element matrices"),
                    opt("taking the inverse of each element"),
                    opt("averaging the matrices"),
                ),
                "Global K is assembled by summing element matrices at shared DOFs.",
            ),
            q(
                "Topology optimization (e.g. the SIMP method) aims to:",
                (
                    opt("place material only where it carries load, minimizing mass", correct=True),
                    opt("maximize the part's weight"),
                    opt("remove all boundary conditions"),
                    opt("increase the factor of safety to infinity"),
                ),
                "SIMP-based topology optimization grows material where it is structurally useful.",
            ),
        ),
    },
    final=(
        q(
            "The cantilever tip deflection PL^3/(3EI) shows deflection scales with length as:",
            (
                opt("the cube of the length", correct=True),
                opt("the square of the length"),
                opt("linearly"),
                opt("the inverse of the length"),
            ),
            "Tip deflection is proportional to L^3.",
        ),
        q(
            "Principal stresses occur on planes with:",
            (
                opt("zero shear stress", correct=True),
                opt("maximum shear stress"),
                opt("zero normal stress"),
                opt("maximum area"),
            ),
            "Principal planes are shear-free.",
        ),
        q(
            "Hoop stress in a thin cylindrical vessel relative to longitudinal stress is:",
            (
                opt("twice as large", correct=True),
                opt("half as large"),
                opt("equal"),
                opt("zero"),
            ),
            "sigma_hoop = 2 * sigma_long.",
        ),
        q(
            "The Euler critical buckling load varies with length as:",
            (
                opt("1 / L^2", correct=True),
                opt("L^2"),
                opt("L"),
                opt("constant"),
            ),
            "P_cr proportional to 1/(KL)^2.",
        ),
        q(
            "Which theory is best suited to brittle materials?",
            (
                opt("maximum normal stress (Rankine)", correct=True),
                opt("von Mises distortion energy"),
                opt("Tresca maximum shear"),
                opt("Euler buckling"),
            ),
            "The maximum normal stress theory suits brittle fracture.",
        ),
        q(
            "In static FEM, after solving K u = F the next step is to:",
            (
                opt("recover element strains and stresses from the displacements", correct=True),
                opt("re-mesh from scratch every time"),
                opt("discard the displacements"),
                opt("set all forces to zero"),
            ),
            "Element strains and stresses are computed from the nodal displacements.",
        ),
    ),
)
