"""Quiz questions for the Engineering Statics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Dry friction & its applications": (
            q(
                "The maximum static friction force is:",
                (
                    opt("mu_s times the normal force N", correct=True),
                    opt("mu_s times the applied force"),
                    opt("equal to the weight always"),
                    opt("independent of the normal force"),
                ),
                "F_max = mu_s N caps the static friction available.",
            ),
            q(
                "The angle of repose for a block on an incline equals:",
                (
                    opt("arctan(mu_s)", correct=True),
                    opt("arcsin(mu_s)"),
                    opt("mu_s in radians"),
                    opt("90 degrees minus mu_s"),
                ),
                "The block slides when tan(theta) reaches mu_s.",
            ),
            q(
                "The capstan equation T2 = T1 exp(mu beta) shows the tension ratio grows:",
                (
                    opt("exponentially with wrap angle", correct=True),
                    opt("linearly with wrap angle"),
                    opt("inversely with wrap angle"),
                    opt("independently of wrap angle"),
                ),
                "Belt friction amplifies the holding force exponentially with beta.",
            ),
        ),
        "Centroids & centers of mass": (
            q(
                "In composite-area centroid calculations, a hole is treated as:",
                (
                    opt("a negative area", correct=True),
                    opt("a zero area"),
                    opt("a positive area"),
                    opt("ignored entirely"),
                ),
                "Holes subtract: they enter the sums with negative area.",
            ),
            q(
                "The centroid x-coordinate of a composite area is:",
                (
                    opt("sum(A_i x_i) / sum(A_i)", correct=True),
                    opt("sum(A_i) / sum(x_i)"),
                    opt("average of the x_i"),
                    opt("sum(x_i) / number of parts"),
                ),
                "It is the area-weighted average of the part centroids.",
            ),
            q(
                "The centroid of a right triangle lies at what fraction of the base from the vertical edge?",
                (
                    opt("one third (b/3)", correct=True),
                    opt("one half (b/2)"),
                    opt("two thirds (2b/3)"),
                    opt("one quarter (b/4)"),
                ),
                "A triangle's centroid sits at b/3 from the base edge.",
            ),
        ),
        "Distributed loads & hydrostatic pressure": (
            q(
                "The resultant of a distributed load equals:",
                (
                    opt("the area under the load curve", correct=True),
                    opt("the peak load intensity"),
                    opt("the load times the centroid distance"),
                    opt("half the load length"),
                ),
                "R = integral of w(x) dx is the area under w(x).",
            ),
            q(
                "Hydrostatic pressure on a wall varies with depth as:",
                (
                    opt("p = rho g h (linear in depth)", correct=True),
                    opt("constant with depth"),
                    opt("proportional to depth squared"),
                    opt("inversely with depth"),
                ),
                "Pressure increases linearly with depth h.",
            ),
            q(
                "The resultant of a triangular hydrostatic load on a wall of depth H acts at:",
                (
                    opt("2H/3 below the surface", correct=True),
                    opt("H/2 below the surface"),
                    opt("H/3 below the surface"),
                    opt("at the surface"),
                ),
                "The centroid of the triangular pressure prism is at 2H/3.",
            ),
        ),
        "Second moment of area & the parallel-axis theorem": (
            q(
                "The second moment of area of a rectangle about its centroid is:",
                (
                    opt("b h^3 / 12", correct=True),
                    opt("b h / 12"),
                    opt("b h^2 / 6"),
                    opt("b^3 h / 3"),
                ),
                "I = b h^3 / 12 about the centroidal axis.",
            ),
            q(
                "The parallel-axis theorem states I about a parallel axis is:",
                (
                    opt("I_centroid + A d^2", correct=True),
                    opt("I_centroid - A d^2"),
                    opt("I_centroid + A d"),
                    opt("I_centroid * d^2"),
                ),
                "Shift adds A d^2, the area times the distance squared.",
            ),
            q(
                "Doubling a beam's depth increases its bending stiffness (I) by a factor of:",
                (
                    opt("eight", correct=True),
                    opt("two"),
                    opt("four"),
                    opt("sixteen"),
                ),
                "I scales with h^3, so 2^3 = 8.",
            ),
        ),
        "Computational statics: matrix methods & optimization": (
            q(
                "The direct stiffness method solves a structure from:",
                (
                    opt("K u = f", correct=True),
                    opt("u = K f"),
                    opt("f = K + u"),
                    opt("K = u f"),
                ),
                "Global stiffness times displacement equals load: K u = f.",
            ),
            q(
                "A single truss bar contributes an element stiffness matrix of size:",
                (
                    opt("4 by 4 (2 DOF per node)", correct=True),
                    opt("2 by 2"),
                    opt("6 by 6"),
                    opt("3 by 3"),
                ),
                "Two planar DOF at each of two nodes gives a 4x4 matrix.",
            ),
            q(
                "A typical truss mass-minimization is constrained by:",
                (
                    opt("stress and displacement limits", correct=True),
                    opt("the number of iterations"),
                    opt("the color of the members"),
                    opt("nothing - it is unconstrained"),
                ),
                "Optimizers minimize mass subject to allowable stress/displacement.",
            ),
        ),
    },
    final=(
        q(
            "Kinetic friction compares to static friction as:",
            (
                opt("mu_k is usually less than mu_s", correct=True),
                opt("mu_k is always greater than mu_s"),
                opt("they are always equal"),
                opt("mu_k is zero"),
            ),
            "Once sliding starts, kinetic friction is lower than the static limit.",
        ),
        q(
            "The first moment of area is used to locate the:",
            (
                opt("centroid", correct=True),
                opt("second moment of area"),
                opt("shear center"),
                opt("modulus of elasticity"),
            ),
            "Centroid = first moment divided by total area.",
        ),
        q(
            "A uniform distributed load w0 over length L has a resultant of:",
            (
                opt("w0 L at midspan", correct=True),
                opt("w0 L / 2 at midspan"),
                opt("w0 L at one third"),
                opt("w0 at the centroid"),
            ),
            "Area of the rectangle is w0 L, acting at its center.",
        ),
        q(
            "The product of inertia and axis rotation lead to the concept of:",
            (
                opt("principal axes and Mohr's circle", correct=True),
                opt("the centroid"),
                opt("the angle of repose"),
                opt("the capstan equation"),
            ),
            "Rotating axes to zero I_xy gives the principal axes (Mohr's circle).",
        ),
        q(
            "After solving K u = f, member forces are recovered from:",
            (
                opt("the element displacements and element stiffness", correct=True),
                opt("the global load vector alone"),
                opt("the support reactions only"),
                opt("the number of DOFs"),
            ),
            "Element forces follow from the computed nodal displacements.",
        ),
        q(
            "Gradient-based structural optimization typically shows convergence that is:",
            (
                opt("geometric (roughly exponential decay of the objective)", correct=True),
                opt("linear growth"),
                opt("oscillating without settling"),
                opt("instantaneous in one step"),
            ),
            "Well-behaved optimizers reduce the objective geometrically per iteration.",
        ),
    ),
)
