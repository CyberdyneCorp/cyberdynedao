"""Quiz questions for the Mechanics of Materials - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Axial deformation and indeterminate bars": (
            q(
                "A bar is statically indeterminate when:",
                (
                    opt("equilibrium alone cannot determine all the reactions", correct=True),
                    opt("it carries no load"),
                    opt("its area is constant"),
                    opt("it is made of a single material"),
                ),
                "Indeterminacy means more unknown reactions than equilibrium equations.",
            ),
            q(
                "To solve an indeterminate axial problem you add which equation type to equilibrium?",
                (
                    opt("a compatibility (deformation) condition", correct=True),
                    opt("a second equilibrium equation only"),
                    opt("a power-balance equation"),
                    opt("a fatigue criterion"),
                ),
                "Compatibility (geometry of deformation) plus the force-deformation law closes the system.",
            ),
            q(
                "The thermal stress in a fully restrained bar heated by delta_T is:",
                (
                    opt("sigma = E times alpha times delta_T", correct=True),
                    opt("sigma = alpha times delta_T"),
                    opt("sigma = E divided by (alpha delta_T)"),
                    opt("sigma = zero, always"),
                ),
                "A restrained bar cannot expand, so sigma = E*alpha*delta_T develops.",
            ),
        ),
        "Torsion of circular shafts": (
            q(
                "In the torsion formula, shear stress across a circular shaft:",
                (
                    opt(
                        "increases linearly from zero at the centre to a maximum at the surface",
                        correct=True,
                    ),
                    opt("is uniform across the section"),
                    opt("is maximum at the centre"),
                    opt("is zero at the surface"),
                ),
                "tau = T rho / J grows linearly with radial position rho.",
            ),
            q(
                "The angle of twist of a circular shaft is:",
                (
                    opt("phi = T L / (G J)", correct=True),
                    opt("phi = G J / (T L)"),
                    opt("phi = T J / (G L)"),
                    opt("phi = L / (T G J)"),
                ),
                "phi = TL/(GJ), with J the polar moment of inertia.",
            ),
            q(
                "A hollow circular shaft is more efficient than a solid one because:",
                (
                    opt(
                        "material near the axis carries little stress, so removing it saves weight",
                        correct=True,
                    ),
                    opt("the centre carries the most stress"),
                    opt("it has zero polar moment of inertia"),
                    opt("shear stress is highest at the centre"),
                ),
                "Stress is lowest near the axis, so a tube gives similar J at much lower weight.",
            ),
        ),
        "Shear force and bending moment diagrams": (
            q(
                "The relationship between bending moment and shear force is:",
                (
                    opt("dM/dx = V", correct=True),
                    opt("dV/dx = M"),
                    opt("M = V squared"),
                    opt("M and V are unrelated"),
                ),
                "Shear is the slope of the moment diagram: dM/dx = V.",
            ),
            q(
                "The bending moment is extreme at the section where:",
                (
                    opt("the shear force is zero", correct=True),
                    opt("the shear force is maximum"),
                    opt("the load is zero"),
                    opt("the deflection is zero"),
                ),
                "Since dM/dx = V, M is extreme where V crosses zero.",
            ),
            q(
                "For a simply supported beam of span L with a central point load P, the maximum moment is:",
                (
                    opt("P L / 4", correct=True),
                    opt("P L / 2"),
                    opt("P L / 8"),
                    opt("P L"),
                ),
                "Reactions are P/2 each, giving M_max = (P/2)(L/2) = PL/4 at midspan.",
            ),
        ),
        "Bending stress and the flexure formula": (
            q(
                "The flexure formula gives bending stress as:",
                (
                    opt("sigma = M y / I (linear in distance from the neutral axis)", correct=True),
                    opt("sigma = M I / y"),
                    opt("sigma = V Q / (I t)"),
                    opt("sigma = T r / J"),
                ),
                "Bending stress varies linearly with y: sigma = -M y / I.",
            ),
            q(
                "Bending stress is zero at the:",
                (
                    opt("neutral axis (centroid)", correct=True),
                    opt("top fibre"),
                    opt("bottom fibre"),
                    opt("supports"),
                ),
                "Strain and stress are zero on the neutral axis and largest at the extreme fibres.",
            ),
            q(
                "For a rectangular section b x h, the second moment of area is:",
                (
                    opt("I = b h^3 / 12", correct=True),
                    opt("I = b h / 12"),
                    opt("I = b^3 h / 12"),
                    opt("I = h / (12 b)"),
                ),
                "I = bh^3/12, so depth h dominates bending stiffness.",
            ),
        ),
        "Transverse shear stress in beams": (
            q(
                "The transverse shear stress in a beam is given by:",
                (
                    opt("tau = V Q / (I t)", correct=True),
                    opt("tau = M y / I"),
                    opt("tau = T r / J"),
                    opt("tau = N / A"),
                ),
                "The shear formula is tau = VQ/(It), with Q the first moment of area.",
            ),
            q(
                "Across a rectangular section, transverse shear stress is maximum at the:",
                (
                    opt("neutral axis", correct=True),
                    opt("top and bottom fibres"),
                    opt("supports only"),
                    opt("corners"),
                ),
                "Shear stress is parabolic, zero at the top/bottom and peak at the neutral axis.",
            ),
            q(
                "For a rectangular section the maximum shear stress equals:",
                (
                    opt("1.5 times the average V/A", correct=True),
                    opt("the average V/A"),
                    opt("0.5 times V/A"),
                    opt("3 times V/A"),
                ),
                "tau_max = (3/2) V/A for a rectangular cross-section.",
            ),
        ),
    },
    final=(
        q(
            "Axial deformation of a uniform bar is:",
            (
                opt("delta = N L / (A E)", correct=True),
                opt("delta = A E / (N L)"),
                opt("delta = N A / (E L)"),
                opt("delta = E / (N L A)"),
            ),
            "delta = NL/(AE).",
        ),
        q(
            "The polar moment of inertia J appears in the formula for:",
            (
                opt("torsional shear stress and angle of twist", correct=True),
                opt("bending stress"),
                opt("axial deformation"),
                opt("buckling load"),
            ),
            "J governs torsion: tau = T rho / J and phi = TL/(GJ).",
        ),
        q(
            "Distributed load w(x) relates to shear by:",
            (
                opt("dV/dx = -w", correct=True),
                opt("dV/dx = +M"),
                opt("V = w squared"),
                opt("w = V times M"),
            ),
            "The load is the negative slope of the shear diagram.",
        ),
        q(
            "The section modulus S is defined as:",
            (
                opt("I / c", correct=True),
                opt("I times c"),
                opt("c / I"),
                opt("M / I"),
            ),
            "S = I/c; maximum bending stress is M/S.",
        ),
        q(
            "An I-beam concentrates area in its flanges to:",
            (
                opt("maximize the second moment of area I for a given weight", correct=True),
                opt("reduce the second moment of area"),
                opt("eliminate shear stress"),
                opt("increase Poisson's ratio"),
            ),
            "Pushing area far from the neutral axis raises I efficiently.",
        ),
        q(
            "Power transmitted by a rotating shaft relates to torque and speed by:",
            (
                opt("P = T times omega", correct=True),
                opt("P = T divided by omega"),
                opt("P = omega divided by T"),
                opt("P = T plus omega"),
            ),
            "P = T*omega, so T = P/omega for a given angular speed.",
        ),
    ),
)
