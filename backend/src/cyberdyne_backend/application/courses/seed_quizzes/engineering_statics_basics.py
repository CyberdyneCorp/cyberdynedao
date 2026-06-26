"""Quiz questions for the Engineering Statics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What statics is: forces, units & Newton's laws": (
            q(
                "In statics, the acceleration of every body is taken to be:",
                (
                    opt("zero, so the net force is zero", correct=True),
                    opt("equal to g downward"),
                    opt("constant but nonzero"),
                    opt("whatever Newton's second law gives"),
                ),
                "Statics studies equilibrium: acceleration is zero, so sum F = 0.",
            ),
            q(
                "One newton is equivalent to:",
                (
                    opt("1 kg*m/s^2", correct=True),
                    opt("1 kg*m/s"),
                    opt("1 kg/m^2"),
                    opt("1 kg*m^2/s^2"),
                ),
                "Force = mass times acceleration, so 1 N = 1 kg*m/s^2.",
            ),
            q(
                "The weight of a 10 kg object near Earth's surface is about:",
                (
                    opt("98 N", correct=True),
                    opt("10 N"),
                    opt("9.81 N"),
                    opt("981 N"),
                ),
                "W = m g = 10 * 9.81 = 98.1 N.",
            ),
        ),
        "Vectors & resolving forces into components": (
            q(
                "The x-component of a force F at angle theta from the x-axis is:",
                (
                    opt("F cos(theta)", correct=True),
                    opt("F sin(theta)"),
                    opt("F tan(theta)"),
                    opt("F / cos(theta)"),
                ),
                "Fx = F cos(theta), Fy = F sin(theta).",
            ),
            q(
                "Given components Fx and Fy, the magnitude of the force is:",
                (
                    opt("sqrt(Fx^2 + Fy^2)", correct=True),
                    opt("Fx + Fy"),
                    opt("Fx * Fy"),
                    opt("(Fx + Fy)/2"),
                ),
                "Magnitude is the Pythagorean sum of the components.",
            ),
            q(
                "To add several forces, the most systematic approach is to:",
                (
                    opt("sum their x-components and y-components separately", correct=True),
                    opt("add their magnitudes directly"),
                    opt("average their angles"),
                    opt("multiply the magnitudes"),
                ),
                "Component-wise addition turns vector sums into simple arithmetic.",
            ),
        ),
        "Moment of a force & couples": (
            q(
                "The moment of a force about a point equals force times:",
                (
                    opt("the perpendicular distance to its line of action", correct=True),
                    opt("the total length of the force vector"),
                    opt("the distance along the line of action"),
                    opt("the angle of the force"),
                ),
                "M = F times the perpendicular (moment arm) distance d.",
            ),
            q(
                "A couple consists of:",
                (
                    opt("two equal, opposite, non-collinear forces", correct=True),
                    opt("a single force through the centroid"),
                    opt("two equal forces in the same direction"),
                    opt("a force and an equal reaction at the same point"),
                ),
                "A couple is two equal opposite parallel forces a distance apart.",
            ),
            q(
                "The moment produced by a couple is:",
                (
                    opt("the same about every point (a free vector)", correct=True),
                    opt("zero everywhere"),
                    opt("largest at the midpoint between the forces"),
                    opt("dependent on the chosen reference point"),
                ),
                "A couple's net force is zero and its moment is independent of the point.",
            ),
        ),
        "Free-body diagrams & support reactions": (
            q(
                "On a free-body diagram a pin (hinge) support is replaced by:",
                (
                    opt("two force components", correct=True),
                    opt("a single normal force"),
                    opt("a force and a moment"),
                    opt("a tension only"),
                ),
                "A pin resists translation in two directions: Rx and Ry.",
            ),
            q(
                "A roller support supplies:",
                (
                    opt("one force normal to its surface", correct=True),
                    opt("two perpendicular forces"),
                    opt("a force plus a moment"),
                    opt("nothing"),
                ),
                "A roller resists motion only normal to the surface: one reaction.",
            ),
            q(
                "A simply supported beam (one pin, one roller) is statically:",
                (
                    opt("determinate - 3 reactions, 3 equations", correct=True),
                    opt("indeterminate - too many reactions"),
                    opt("unstable - too few reactions"),
                    opt("determinate only in 3-D"),
                ),
                "Three reaction unknowns match the three planar equations.",
            ),
        ),
        "Equilibrium of a particle": (
            q(
                "How many independent equilibrium equations apply to a particle in 2-D?",
                (
                    opt("two", correct=True),
                    opt("one"),
                    opt("three"),
                    opt("six"),
                ),
                "A particle has no moment equation: only sum Fx = 0 and sum Fy = 0.",
            ),
            q(
                "As two symmetric support cables become nearly horizontal, the tension:",
                (
                    opt("increases sharply toward infinity", correct=True),
                    opt("decreases toward zero"),
                    opt("stays constant"),
                    opt("equals exactly half the weight"),
                ),
                "T = W/(2 sin theta) grows without bound as theta -> 0.",
            ),
            q(
                "A particle equilibrium problem can solve for at most how many unknowns in 2-D?",
                (
                    opt("two", correct=True),
                    opt("three"),
                    opt("one"),
                    opt("four"),
                ),
                "Two scalar equations solve for at most two unknowns.",
            ),
        ),
    },
    final=(
        q(
            "Statics deals with bodies that are:",
            (
                opt("in equilibrium (net force and net moment zero)", correct=True),
                opt("always accelerating"),
                opt("rotating at increasing speed"),
                opt("free of any forces"),
            ),
            "Equilibrium means sum F = 0 and sum M = 0.",
        ),
        q(
            "The y-component of a 200 N force at 30 degrees above horizontal is:",
            (
                opt("100 N", correct=True),
                opt("173 N"),
                opt("200 N"),
                opt("50 N"),
            ),
            "Fy = 200 sin(30) = 100 N.",
        ),
        q(
            "Moving a wrench grip farther from the bolt, for the same applied force:",
            (
                opt("increases the moment linearly", correct=True),
                opt("decreases the moment"),
                opt("leaves the moment unchanged"),
                opt("reverses the moment direction"),
            ),
            "M = F d grows linearly with the moment arm d.",
        ),
        q(
            "Which support provides both horizontal and vertical reaction but no moment?",
            (
                opt("a pin / hinge", correct=True),
                opt("a roller"),
                opt("a fixed (built-in) support"),
                opt("a cable"),
            ),
            "A pin gives Rx and Ry; a fixed support also gives a moment.",
        ),
        q(
            "A negative result for an assumed-tension cable force means:",
            (
                opt(
                    "the assumption was wrong; the value is still a magnitude with reversed sense",
                    correct=True,
                ),
                opt("the calculation is invalid"),
                opt("the cable carries no force"),
                opt("the cable is in tension twice as large"),
            ),
            "A negative sign flips the assumed direction of the force.",
        ),
        q(
            "Drawing a correct free-body diagram requires replacing each support with:",
            (
                opt("the reactions that support physically provides", correct=True),
                opt("the applied loads only"),
                opt("the weight of the support"),
                opt("nothing - supports are ignored"),
            ),
            "Each support type contributes its specific reaction forces/moments.",
        ),
    ),
)
