"""Quiz questions for the Engineering Statics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Rigid-body equilibrium in 2-D": (
            q(
                "How many independent equilibrium equations apply to a rigid body in 2-D?",
                (
                    opt("three", correct=True),
                    opt("two"),
                    opt("six"),
                    opt("one"),
                ),
                "sum Fx = 0, sum Fy = 0, sum M = 0 - three equations.",
            ),
            q(
                "A smart choice of moment point is one that:",
                (
                    opt(
                        "lies on the intersection of unknown forces to eliminate them", correct=True
                    ),
                    opt("is far from all forces"),
                    opt("is the centroid of the body"),
                    opt("maximizes the moment arm"),
                ),
                "Taking moments through unknowns removes them from that equation.",
            ),
            q(
                "For a simply supported beam, a central point load P gives each reaction:",
                (
                    opt("P/2", correct=True),
                    opt("P"),
                    opt("P/4"),
                    opt("2P"),
                ),
                "By symmetry each support carries half the central load.",
            ),
        ),
        "Equilibrium in 3-D": (
            q(
                "A rigid body in 3-D has how many equilibrium equations?",
                (
                    opt("six", correct=True),
                    opt("three"),
                    opt("four"),
                    opt("nine"),
                ),
                "Three force and three moment equations: six total.",
            ),
            q(
                "A force along a member is written as magnitude times:",
                (
                    opt("the unit vector along the member's line of action", correct=True),
                    opt("the member length"),
                    opt("the position of one endpoint"),
                    opt("the cross product of the endpoints"),
                ),
                "F vector = F * (d/|d|), the unit direction vector.",
            ),
            q(
                "In 3-D the moment of a force is computed as:",
                (
                    opt("r cross F", correct=True),
                    opt("r dot F"),
                    opt("r + F"),
                    opt("|r| |F|"),
                ),
                "The moment vector is the cross product r x F.",
            ),
        ),
        "Trusses: the method of joints": (
            q(
                "Each member of an ideal truss carries:",
                (
                    opt("axial force only (tension or compression)", correct=True),
                    opt("bending moment only"),
                    opt("shear force only"),
                    opt("torsion only"),
                ),
                "Two-force members carry pure axial force along their length.",
            ),
            q(
                "The method of joints works best by starting at a joint with:",
                (
                    opt("at most two unknown member forces", correct=True),
                    opt("the most members"),
                    opt("the applied load"),
                    opt("three unknown members"),
                ),
                "Two scalar equations per joint solve at most two unknowns.",
            ),
            q(
                "If a member force comes out negative under a tension assumption, the member is:",
                (
                    opt("in compression", correct=True),
                    opt("in tension"),
                    opt("a zero-force member"),
                    opt("overstressed"),
                ),
                "Negative means the actual force opposes the assumed tension - compression.",
            ),
        ),
        "Trusses: the method of sections": (
            q(
                "The method of sections cuts through at most how many unknown members?",
                (
                    opt("three", correct=True),
                    opt("two"),
                    opt("one"),
                    opt("four"),
                ),
                "Three rigid-body equations solve up to three cut-member unknowns.",
            ),
            q(
                "To find one cut member directly, take moments about:",
                (
                    opt("the intersection of the other two cut members", correct=True),
                    opt("the loaded joint"),
                    opt("the centroid of the truss"),
                    opt("a support reaction"),
                ),
                "That point removes the other two unknowns from the moment equation.",
            ),
            q(
                "For a fixed bending moment, increasing truss depth makes the chord force:",
                (
                    opt("smaller (F = M/h)", correct=True),
                    opt("larger"),
                    opt("unchanged"),
                    opt("zero"),
                ),
                "Chord force varies inversely with depth: F = M/h.",
            ),
        ),
        "Frames, machines & internal forces": (
            q(
                "Frames and machines differ from trusses because they contain:",
                (
                    opt("multi-force members carrying shear and bending", correct=True),
                    opt("only two-force members"),
                    opt("no internal forces"),
                    opt("only cables"),
                ),
                "Multi-force members are loaded at more than two points.",
            ),
            q(
                "The relationship between shear V and bending moment M along a beam is:",
                (
                    opt("dM/dx = V", correct=True),
                    opt("dV/dx = M"),
                    opt("M = V"),
                    opt("dM/dx = -M"),
                ),
                "The slope of the bending-moment diagram equals the shear force.",
            ),
            q(
                "When dismembering a frame, forces at a shared pin obey:",
                (
                    opt("Newton's third law: equal and opposite on the two members", correct=True),
                    opt("they are zero by definition"),
                    opt("they double at the pin"),
                    opt("they act only on the heavier member"),
                ),
                "Action-reaction links the pin forces between connected members.",
            ),
        ),
    },
    final=(
        q(
            "A properly constrained 2-D rigid body needs how many reactions for determinacy?",
            (
                opt("three", correct=True),
                opt("two"),
                opt("four"),
                opt("six"),
            ),
            "Three reactions match the three planar equilibrium equations.",
        ),
        q(
            "In 3-D, the unit vector along a member from A to B is:",
            (
                opt("(B - A) / |B - A|", correct=True),
                opt("B - A"),
                opt("A - B"),
                opt("|B - A|"),
            ),
            "Divide the position difference by its magnitude.",
        ),
        q(
            "A zero-force member in a truss carries:",
            (
                opt("no axial force under the given loading", correct=True),
                opt("the largest force"),
                opt("only compression"),
                opt("half the applied load"),
            ),
            "Certain geometries force a member to carry zero force.",
        ),
        q(
            "The method of sections is preferred over joints when you need:",
            (
                opt("a few specific member forces quickly", correct=True),
                opt("the force in every member"),
                opt("support reactions only"),
                opt("displacements"),
            ),
            "Sections targets selected members without solving the whole truss.",
        ),
        q(
            "The peak bending moment in a simply supported beam with a central point load occurs:",
            (
                opt("at midspan under the load", correct=True),
                opt("at the supports"),
                opt("at the quarter points"),
                opt("nowhere - it is constant"),
            ),
            "Moment rises linearly to a maximum under the central load.",
        ),
        q(
            "Assembling all joint equilibrium equations of a truss yields:",
            (
                opt("a linear system A f = b solvable at once", correct=True),
                opt("a nonlinear system"),
                opt("a differential equation"),
                opt("an underdetermined system always"),
            ),
            "Joint equations are linear in the member forces.",
        ),
    ),
)
