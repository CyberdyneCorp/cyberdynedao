"""Quiz questions for the Parametric & Simulation-Driven Design - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is parametric design?": (
            q(
                "In parametric design, the geometry is:",
                (
                    opt(
                        "defined by parameters so it regenerates when a value changes", correct=True
                    ),
                    opt("drawn once and frozen forever"),
                    opt("stored only as a flat image"),
                    opt("limited to two dimensions"),
                ),
                "Parametric models regenerate from named dimensions and relations, capturing design intent.",
            ),
            q(
                "Compared with parametric modelling, direct (explicit) modelling:",
                (
                    opt(
                        "edits geometry that has no history, fast for one-off tweaks", correct=True
                    ),
                    opt("always keeps a full feature history"),
                    opt("cannot edit geometry at all"),
                    opt("requires a spreadsheet for every change"),
                ),
                "Direct modelling pushes/pulls geometry without history; parametric pays off across many revisions.",
            ),
            q(
                "Parametric modelling pays off most when a design is:",
                (
                    opt("revised many times or reused as a family of variants", correct=True),
                    opt("never going to change"),
                    opt("a single static picture"),
                    opt("only ever exported to STL"),
                ),
                "Build-once-edit-many makes parametric cheaper as the number of revisions grows.",
            ),
        ),
        "Sketch constraints and degrees of freedom": (
            q(
                "A sketch of N points starts with how many degrees of freedom?",
                (
                    opt("2N", correct=True),
                    opt("N"),
                    opt("N/2"),
                    opt("3N"),
                ),
                "Each point has two coordinates (x, y), so N points have 2N degrees of freedom.",
            ),
            q(
                "A sketch is fully defined when its degrees of freedom equal:",
                (
                    opt("zero", correct=True),
                    opt("one"),
                    opt("the number of points"),
                    opt("a negative number"),
                ),
                "Fully defined means DOF = 0: the sketch cannot be dragged into a different shape.",
            ),
            q(
                "Which of these is a geometric (not dimensional) constraint?",
                (
                    opt("tangent", correct=True),
                    opt("a 30 mm length"),
                    opt("a 45 degree angle value"),
                    opt("a 10 mm radius value"),
                ),
                "Tangent, parallel, coincident relate entities; lengths, radii and angles are dimensional.",
            ),
        ),
        "Features and the design tree": (
            q(
                "The feature (history) tree primarily records:",
                (
                    opt(
                        "the ordered features and their references that build the solid",
                        correct=True,
                    ),
                    opt("only the final mesh"),
                    opt("the printer settings"),
                    opt("the title block text"),
                ),
                "The tree replays features in order on regenerate, capturing how the solid is built.",
            ),
            q(
                "Why does feature order matter in the tree?",
                (
                    opt(
                        "a fillet before a pattern is repeated by it; after, it is not",
                        correct=True,
                    ),
                    opt("order never affects the result"),
                    opt("features are always alphabetical"),
                    opt("only the last feature is computed"),
                ),
                "Each feature references earlier geometry, so order changes what the result is.",
            ),
            q(
                "Referencing fragile edges instead of stable geometry tends to cause:",
                (
                    opt("rebuild errors when an upstream feature changes", correct=True),
                    opt("faster regeneration"),
                    opt("smaller file sizes"),
                    opt("automatic meshing"),
                ),
                "Edges can disappear when upstream features change; stable references avoid rebuild errors.",
            ),
        ),
        "Design intent and robust models": (
            q(
                "Design intent is:",
                (
                    opt("the rules you want the model to obey as parameters change", correct=True),
                    opt("the color of the part"),
                    opt("the file name"),
                    opt("the number of views on a drawing"),
                ),
                "Intent encodes what should move and what should stay put when the model changes.",
            ),
            q(
                "A quick test that design intent is captured is to:",
                (
                    opt(
                        "change a key dimension and confirm it regenerates as expected",
                        correct=True,
                    ),
                    opt("delete the feature tree"),
                    opt("export to STL"),
                    opt("rename the file"),
                ),
                "If the model updates correctly with no errors, the dependencies are robust.",
            ),
            q(
                "Which practice makes a model robust to change?",
                (
                    opt("fully defined sketches and stable references", correct=True),
                    opt("leaving sketches under-defined"),
                    opt("referencing temporary edges"),
                    opt("creating circular dependencies"),
                ),
                "Robust models are fully defined, reference stable geometry and use sensible feature order.",
            ),
        ),
        "Relations, equations and units": (
            q(
                "An equation like pocket_depth = thickness - wall lets you:",
                (
                    opt(
                        "compute one dimension from others so it tracks automatically", correct=True
                    ),
                    opt("disable all dimensions"),
                    opt("convert the file to an image"),
                    opt("delete the feature tree"),
                ),
                "Relations link dimensions so derived values update when their inputs change.",
            ),
            q(
                "Mixing millimetres and inches in equations without care leads to:",
                (
                    opt("dimensionally inconsistent, silently wrong results", correct=True),
                    opt("faster solves"),
                    opt("automatic conversion that is always correct"),
                    opt("a better mesh"),
                ),
                "Keep a single consistent unit system; mixed units are a classic source of error.",
            ),
            q(
                "Encoding an engineering rule (e.g. fillet = 0.3 * thickness) as a relation:",
                (
                    opt(
                        "keeps the rule satisfied automatically as the model changes", correct=True
                    ),
                    opt("removes the need for any parameters"),
                    opt("only works in 2D sketches"),
                    opt("prevents the model from regenerating"),
                ),
                "Relations enforce design rules so derived dimensions stay valid across edits.",
            ),
        ),
        "Documenting and exchanging models": (
            q(
                "Which neutral format is the workhorse for CAD-to-CAD and CAD-to-CAE exchange?",
                (
                    opt("STEP (ISO 10303, AP242)", correct=True),
                    opt("STL"),
                    opt("JPEG"),
                    opt("CSV"),
                ),
                "STEP AP242 carries solid B-rep and optional semantic PMI between tools.",
            ),
            q(
                "Exporting a model to STL:",
                (
                    opt("discards parametrics and approximates curves with facets", correct=True),
                    opt("preserves the full feature history"),
                    opt("keeps exact NURBS geometry"),
                    opt("adds new design parameters"),
                ),
                "STL is a tessellated mesh for 3D printing; it loses exact geometry and history.",
            ),
            q(
                "Finer STL tessellation lowers chordal deviation but:",
                (
                    opt("increases file size", correct=True),
                    opt("restores the parametric history"),
                    opt("makes the geometry exact"),
                    opt("reduces file size"),
                ),
                "More facets mean lower faceting error but a larger file - an accuracy/size trade-off.",
            ),
        ),
    },
    final=(
        q(
            "The defining feature of a parametric model is that it:",
            (
                opt("regenerates from driving parameters and relations", correct=True),
                opt("is a single frozen image"),
                opt("cannot be edited"),
                opt("stores only a mesh"),
            ),
            "Parameters drive the geometry; editing a value regenerates the model.",
        ),
        q(
            "A fully defined sketch has degrees of freedom equal to:",
            (
                opt("zero", correct=True),
                opt("2N"),
                opt("the number of constraints"),
                opt("one per point"),
            ),
            "Constraints remove DOF until none remain; the sketch is then stable.",
        ),
        q(
            "An under-defined sketch (DOF greater than zero):",
            (
                opt("can shift unpredictably when neighbouring geometry changes", correct=True),
                opt("throws a conflict error"),
                opt("is the ideal target state"),
                opt("has too many constraints"),
            ),
            "Under-defined geometry drags freely; over-defined geometry conflicts. Aim for exactly zero DOF.",
        ),
        q(
            "Feature order in the design tree matters because:",
            (
                opt(
                    "each feature references earlier geometry, so order changes the result",
                    correct=True,
                ),
                opt("features are computed in random order"),
                opt("only the first feature is used"),
                opt("order is purely cosmetic"),
            ),
            "A fillet before vs after a pattern gives different results; the tree replays in order.",
        ),
        q(
            "Equations and relations in a model are used to:",
            (
                opt("compute dimensions from others and enforce engineering rules", correct=True),
                opt("convert the model to an image"),
                opt("remove all design intent"),
                opt("disable regeneration"),
            ),
            "Relations turn the model into a small program where derived values track inputs.",
        ),
        q(
            "For an engineering hand-off that must keep exact solid geometry, prefer:",
            (
                opt("STEP over a mesh format like STL", correct=True),
                opt("STL over STEP"),
                opt("a screenshot"),
                opt("a CSV of dimensions"),
            ),
            "STEP preserves exact B-rep geometry; mesh formats approximate it for fabrication.",
        ),
    ),
)
