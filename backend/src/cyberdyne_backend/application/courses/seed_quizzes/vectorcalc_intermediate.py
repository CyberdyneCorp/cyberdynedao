"""Curated quiz questions for the Vector Calculus - Intermediate course
(per-lesson checkpoints keyed by exact content-lesson title, plus a final
comprehensive quiz). Grounded entirely in seed_vectorcalc's intermediate
lessons."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Divergence: sources & sinks": (
            q(
                "What does divergence of a vector field measure at a point?",
                (
                    opt("How fast a paddlewheel placed there would spin"),
                    opt(
                        "The net outflow per unit area, how much the field spreads out",
                        correct=True,
                    ),
                    opt("The work done moving a particle along a closed loop"),
                    opt("The slope of the field in the steepest direction"),
                ),
                "Divergence measures how much a field spreads out from a point, the net outflow per unit area.",
            ),
            q(
                "What sign of divergence corresponds to a sink, where the field flows inward like a drain?",
                (
                    opt("Negative divergence", correct=True),
                    opt("Positive divergence"),
                    opt("Zero divergence"),
                    opt("Infinite divergence"),
                ),
                "A sink has negative divergence; for example F = (-x, -y) has divergence -2.",
            ),
            q(
                "What is the divergence of the swirl field F = (-y, x)?",
                (
                    opt("2"),
                    opt("-2"),
                    opt("0, the field is incompressible", correct=True),
                    opt("1"),
                ),
                "The swirl (-y, x) has zero divergence, meaning it is incompressible: whatever flows in flows out.",
            ),
        ),
        "Curl: rotation & circulation": (
            q(
                "Using the paddlewheel picture, what does curl measure?",
                (
                    opt("How much the field rotates around a point", correct=True),
                    opt("How much the field spreads outward from a point"),
                    opt("The volume under a surface over a region"),
                    opt("The flux of the field through a closed surface"),
                ),
                "Curl measures how much a field rotates around a point, like how fast a tiny paddlewheel spins.",
            ),
            q(
                "What is the curl of the swirl field F = (-y, x)?",
                (
                    opt("0"),
                    opt("2", correct=True),
                    opt("-2"),
                    opt("It varies from point to point"),
                ),
                "The swirl (-y, x) rotates everywhere with curl equal to 2, spinning counter-clockwise.",
            ),
            q(
                "What is true of the purely radial field F = (x, y)?",
                (
                    opt("It has zero curl; it spreads but never spins", correct=True),
                    opt("It has large curl and strong rotation"),
                    opt("It has zero divergence"),
                    opt("It is a conservative loop with negative circulation"),
                ),
                "A radial field like (x, y) has zero curl: it spreads out but never spins.",
            ),
        ),
        "Line integrals & work": (
            q(
                "When F is a force, what does the line integral of F along a path represent?",
                (
                    opt("The work done moving along the path", correct=True),
                    opt("The divergence of the field inside the path"),
                    opt("The curl of the field at the start point"),
                    opt("The flux through a surface bounded by the path"),
                ),
                "When F is a force, the line integral along the path is the work done moving along it.",
            ),
            q(
                "What is the line integral around a closed loop called?",
                (
                    opt("The flux"),
                    opt("The circulation", correct=True),
                    opt("The potential"),
                    opt("The gradient"),
                ),
                "Going around a closed loop, the line integral is called the circulation.",
            ),
            q(
                "In the dot product F . dr, which part of the field actually contributes?",
                (
                    opt("Only the part of F along the direction of motion", correct=True),
                    opt("Only the part of F perpendicular to the motion"),
                    opt("The full magnitude of F regardless of direction"),
                    opt("Only the divergence of F"),
                ),
                "Because of the dot product, only the component of F along the direction of motion counts.",
            ),
        ),
        "Conservative fields & potential": (
            q(
                "What defines a conservative field?",
                (
                    opt("The work between two points is independent of the path", correct=True),
                    opt("The work depends strongly on which path you choose"),
                    opt("The divergence is always positive"),
                    opt("The field always points radially outward"),
                ),
                "A conservative field is one where the work between two points is independent of the path taken.",
            ),
            q(
                "For a conservative field, what is the circulation around every closed loop?",
                (
                    opt("Equal to twice the enclosed area"),
                    opt("Zero", correct=True),
                    opt("Equal to the divergence inside"),
                    opt("Always positive"),
                ),
                "Path-independence is equivalent to the circulation around every closed loop being zero.",
            ),
            q(
                "A conservative field can be written as which of the following?",
                (
                    opt("The curl of another field"),
                    opt("The gradient of a potential, F = grad phi", correct=True),
                    opt("The divergence of a surface integral"),
                    opt("The flux through a closed boundary"),
                ),
                "A conservative field is the gradient of a potential phi, which is why curl F = 0.",
            ),
        ),
    },
    final=(
        q(
            "Which operator measures spreading (net outflow) and which measures rotation?",
            (
                opt("Divergence measures rotation; curl measures spreading"),
                opt("Divergence measures spreading; curl measures rotation", correct=True),
                opt("Both measure rotation"),
                opt("Both measure spreading"),
            ),
            "Divergence measures how a field spreads out, while curl measures how it rotates.",
        ),
        q(
            "For the swirl field F = (-y, x), which pair of values is correct?",
            (
                opt("Divergence 0 and curl 2", correct=True),
                opt("Divergence 2 and curl 0"),
                opt("Divergence 2 and curl 2"),
                opt("Divergence -2 and curl -2"),
            ),
            "The swirl (-y, x) is incompressible with divergence 0 and rotates with curl 2.",
        ),
        q(
            "A line integral around a closed loop gives the circulation; what does it equal when F is a force over an open path?",
            (
                opt("The work done", correct=True),
                opt("The divergence enclosed"),
                opt("The potential energy lost to friction"),
                opt("The flux through the loop"),
            ),
            "For a force F, the line integral along a path is the work done moving along it.",
        ),
        q(
            "Which three statements all mean a field is conservative?",
            (
                opt(
                    "F = grad phi, curl F = 0, and circulation around every loop is 0", correct=True
                ),
                opt("divergence F = 0, curl F = 2, and flux is positive"),
                opt("F points outward, divergence is positive, and curl is large"),
                opt("F = curl phi, divergence F = 0, and work depends on the path"),
            ),
            "Being a gradient of a potential, having zero curl, and zero circulation around every loop are equivalent.",
        ),
        q(
            "Why is the radial source field F = (x, y) not conservative-looking the same as the swirl in terms of curl?",
            (
                opt("The source (x, y) has zero curl while the swirl has curl 2", correct=True),
                opt("The source has curl 2 while the swirl has zero curl"),
                opt("Both fields have the same nonzero curl"),
                opt("Both fields have zero divergence"),
            ),
            "The radial source (x, y) spreads but does not spin, so its curl is zero, unlike the swirl whose curl is 2.",
        ),
    ),
)
