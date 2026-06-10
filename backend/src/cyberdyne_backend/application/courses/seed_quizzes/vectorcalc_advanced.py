"""Curated quiz questions for the Vector Calculus - Advanced course. Keys are
the EXACT content-lesson titles from ``seed_vectorcalc`` so the seed can
interleave a checkpoint quiz after each content lesson, plus a final
comprehensive quiz. Every question is answerable from the lesson body."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Multiple integrals, surfaces & flux": (
            q(
                "What does a double integral of a scalar field over a 2D region compute?",
                (
                    opt("The curl of a vector field around the region"),
                    opt("The volume under a surface, total mass, or total charge", correct=True),
                    opt("The length of the boundary curve of the region"),
                    opt("The unit normal vector to the region"),
                ),
                "The lesson defines the double integral as adding a scalar field over a 2D region, giving volume under a surface, total mass, or total charge.",
            ),
            q(
                "How is the flux of a vector field through a surface defined in the lesson?",
                (
                    opt("As the integral of the field's magnitude over the region"),
                    opt(
                        "As the surface integral of F dotted with the unit normal n over the surface",
                        correct=True,
                    ),
                    opt("As the divergence of the field at a single point"),
                    opt("As the line integral of F around the surface boundary"),
                ),
                "Flux is given as the surface integral of F dot n dA, where n is the surface's unit normal.",
            ),
            q(
                "According to the lesson, which component of the field contributes to the flux through a surface?",
                (
                    opt("Only the component of F that runs parallel to the surface"),
                    opt("Only the component of F passing through the surface", correct=True),
                    opt("The full magnitude of F regardless of direction"),
                    opt("Only the component of F along the boundary curve"),
                ),
                "The lesson states only the component of F through the surface counts toward the flux.",
            ),
        ),
        "Green's theorem": (
            q(
                "What does Green's theorem equate the circulation of F around a closed curve C to?",
                (
                    opt("The flux of F out through C"),
                    opt("The total curl of F over the region R enclosed by C", correct=True),
                    opt("The total divergence of F over the region R"),
                    opt("The arc length of the curve C"),
                ),
                "Green's theorem says the circulation around C equals the double integral of the curl over the enclosed region R.",
            ),
            q(
                "For the swirl field with curl equal to 2, what is the circulation around a loop equal to?",
                (
                    opt("The perimeter of the loop"),
                    opt("Twice the enclosed area", correct=True),
                    opt("Zero, because the field is conservative"),
                    opt("Half the enclosed area"),
                ),
                "With curl 2, the integral of the curl over the region is 2 times the enclosed area.",
            ),
            q(
                "Which device does the lesson cite as measuring land area by tracing its outline, illustrating area from a boundary walk?",
                (
                    opt("A paddlewheel"),
                    opt("A planimeter", correct=True),
                    opt("A barometer"),
                    opt("A pendulum"),
                ),
                "The lesson notes a planimeter measures land area by tracing its outline, a consequence of Green's theorem.",
            ),
        ),
        "The Divergence (Gauss) theorem": (
            q(
                "What does the Divergence theorem equate the net flux of F out through a closed surface S to?",
                (
                    opt("The total curl of F over the surface"),
                    opt("The total divergence of F inside the enclosed volume V", correct=True),
                    opt("The circulation of F around the surface boundary"),
                    opt("The gradient of F at the center of V"),
                ),
                "The Divergence theorem states the net outward flux through S equals the triple integral of the divergence over the enclosed volume V.",
            ),
            q(
                "In the lesson, what role do sources and sinks play with respect to flux?",
                (
                    opt("Sources pull flux in and sinks push flux out"),
                    opt("Sources inside push flux out and sinks pull it in", correct=True),
                    opt("Both sources and sinks leave the net flux at zero"),
                    opt("Sources and sinks only affect curl, not flux"),
                ),
                "The lesson says sources inside push flux out while sinks pull it in.",
            ),
            q(
                "Which physical law does the lesson say the Divergence theorem is in electromagnetism?",
                (
                    opt("Faraday's law of induction"),
                    opt(
                        "Gauss's law relating flux of E to enclosed charge over epsilon zero",
                        correct=True,
                    ),
                    opt("Ampere's law for magnetic circulation"),
                    opt("Ohm's law for current and voltage"),
                ),
                "The lesson identifies the Divergence theorem as Gauss's law: flux of E out of a surface equals enclosed charge over epsilon zero.",
            ),
        ),
        "Stokes' theorem & Maxwell": (
            q(
                "What does Stokes' theorem equate the circulation of F around the boundary curve of a surface to?",
                (
                    opt("The total divergence of F inside the surface"),
                    opt("The flux of the curl of F through that surface", correct=True),
                    opt("The arc length of the boundary curve"),
                    opt("The gradient of F along the boundary"),
                ),
                "Stokes' theorem equates the circulation around the boundary curve to the flux of the curl through the surface.",
            ),
            q(
                "How does the lesson describe the relationship of Stokes' theorem to Green's theorem?",
                (
                    opt("It is Green's theorem lifted into 3D", correct=True),
                    opt("It is the 1D special case of Green's theorem"),
                    opt("It is unrelated to Green's theorem"),
                    opt("It replaces Green's theorem for conservative fields"),
                ),
                "The lesson calls Stokes' theorem Green's theorem lifted into 3D.",
            ),
            q(
                "According to the lesson, which laws form Maxwell's equations and predict light?",
                (
                    opt("Only Gauss's law and Ohm's law"),
                    opt("Gauss's law, Faraday's law and Ampere's law", correct=True),
                    opt("Only Faraday's law and Newton's laws"),
                    opt("The continuity equation and Hooke's law"),
                ),
                "The lesson states Gauss's law, Faraday's law and Ampere's law are Maxwell's equations that predict light.",
            ),
        ),
        "Lab: check Green's theorem numerically": (
            q(
                "In the lab, what is the curl of the swirl field F = (-y, x)?",
                (
                    opt("0"),
                    opt("2", correct=True),
                    opt("1"),
                    opt("-2"),
                ),
                "The lab computes curl F = dFy/dx - dFx/dy = 1 - (-1) = 2.",
            ),
            q(
                "On the unit square, what value should the loop integral equal according to the lab's use of Green's theorem?",
                (
                    opt("curl times area = 2", correct=True),
                    opt("curl plus area = 3"),
                    opt("area divided by curl = 0.5"),
                    opt("zero, since the field is conservative"),
                ),
                "The lab notes curl is 2 and the area is 1, so the loop integral should equal curl times area = 2.",
            ),
            q(
                "How does the lab compute the divergence of the source field G = (x, y) at the point (1,1)?",
                (
                    opt("By integrating G around the boundary loop"),
                    opt("By central differences of the components", correct=True),
                    opt("By taking the curl with a paddlewheel"),
                    opt("By summing the field magnitudes on a grid"),
                ),
                "The lab estimates the divergence of (x,y) at (1,1) using central differences and expects 2.",
            ),
        ),
    },
    final=(
        q(
            "Which statement captures the unifying idea behind Green's, the Divergence, and Stokes' theorems?",
            (
                opt("An integral over a region equals an integral over its boundary", correct=True),
                opt("Every vector field is conservative"),
                opt("Curl and divergence are always equal"),
                opt("Flux through any surface is always zero"),
            ),
            "The lesson states the next three theorems each say an integral over a region equals an integral over its boundary.",
        ),
        q(
            "What does flux measure for a vector field?",
            (
                opt("How fast a paddlewheel spins in the field"),
                opt("How much of the field passes through a surface", correct=True),
                opt("The steepest direction of increase of a scalar field"),
                opt("The arc length of a path through the field"),
            ),
            "Flux measures how much of a vector field passes through a surface, the flow rate across it.",
        ),
        q(
            "Green's theorem relates a loop's circulation to which interior quantity?",
            (
                opt("The total divergence enclosed"),
                opt("The total curl enclosed", correct=True),
                opt("The total flux out of the region"),
                opt("The gradient at the loop's center"),
            ),
            "Green's theorem equates the circulation around C to the total curl over the enclosed region.",
        ),
        q(
            "The Divergence (Gauss) theorem relates net flux out of a closed surface to which interior quantity?",
            (
                opt("The total curl inside the volume"),
                opt("The total divergence inside the enclosed volume", correct=True),
                opt("The circulation around the boundary curve"),
                opt("The surface area of the boundary"),
            ),
            "The Divergence theorem equates the net flux out through S to the total divergence inside the volume V.",
        ),
        q(
            "Which trio of physical laws does the course identify as Maxwell's equations grounded in these theorems?",
            (
                opt("Gauss's law, Faraday's law, and Ampere's law", correct=True),
                opt("Newton's three laws of motion"),
                opt("Ohm's law, Hooke's law, and the continuity equation"),
                opt("The first, second, and third laws of thermodynamics"),
            ),
            "The course ties Gauss's law (divergence theorem) and Faraday's and Ampere's laws (Stokes' theorem) to Maxwell's equations.",
        ),
    ),
)
