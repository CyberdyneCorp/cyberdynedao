"""Quiz questions for the Engineering Graphics, GD&T & CAD - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The graphic language: views and projection": (
            q(
                "In orthographic projection the projection rays are:",
                (
                    opt("parallel and perpendicular to the projection plane", correct=True),
                    opt("converging to a single station point"),
                    opt("diverging from the object"),
                    opt("at 45 degrees to the plane"),
                ),
                "Orthographic uses parallel rays normal to the plane, giving true size with no perspective distortion.",
            ),
            q(
                "In third-angle (ASME) projection, the top view is placed:",
                (
                    opt("above the front view", correct=True),
                    opt("below the front view"),
                    opt("to the left of the front view"),
                    opt("overlapping the front view"),
                ),
                "In third-angle each view sits on the side seen from, so the top view goes above the front; first-angle puts it below.",
            ),
            q(
                "How is first-angle vs third-angle projection communicated on a drawing?",
                (
                    opt("by a standard symbol in the title block", correct=True),
                    opt("by the color of the border"),
                    opt("by the sheet size only"),
                    opt("it is never indicated"),
                ),
                "A truncated-cone symbol in the title block declares the projection convention.",
            ),
        ),
        "The alphabet of lines": (
            q(
                "A visible (object) edge is drawn as a:",
                (
                    opt("thick continuous line", correct=True),
                    opt("thin dashed line"),
                    opt("thin long-short-long line"),
                    opt("thin line with arrowheads"),
                ),
                "Visible edges use a thick continuous line; hidden edges are thin and dashed.",
            ),
            q(
                "A thin long-short-long line typically represents a:",
                (
                    opt("center line or axis of symmetry", correct=True),
                    opt("visible edge"),
                    opt("cutting plane"),
                    opt("dimension line"),
                ),
                "Center lines (long-short-long) mark axes of symmetry and hole centers.",
            ),
            q(
                "When a visible line and a hidden line coincide, which takes precedence?",
                (
                    opt("the visible line", correct=True),
                    opt("the hidden line"),
                    opt("the center line"),
                    opt("neither - both are omitted"),
                ),
                "Line precedence: visible over hidden over center.",
            ),
        ),
        "Multiview drawings and view selection": (
            q(
                "The front view should generally be chosen as the one that:",
                (
                    opt(
                        "shows the most characteristic shape with the fewest hidden lines",
                        correct=True,
                    ),
                    opt("is the largest face of the part"),
                    opt("contains the part number"),
                    opt("requires the most dimensions"),
                ),
                "The front view shows the most descriptive contour with minimal hidden detail.",
            ),
            q(
                "Depth is transferred from the top view to the side view using:",
                (
                    opt("a 45 degree miter line", correct=True),
                    opt("a center line"),
                    opt("the cutting-plane line"),
                    opt("a phantom line"),
                ),
                "A 45 degree miter line transfers depth between top and side views, keeping alignment.",
            ),
            q(
                "How many principal views does a simple cylinder require to be fully defined?",
                (
                    opt("two", correct=True),
                    opt("six"),
                    opt("four"),
                    opt("five"),
                ),
                "A cylinder needs only two views (a rectangle and a circle); include only enough views to remove ambiguity.",
            ),
        ),
        "Sectional and auxiliary views": (
            q(
                "Section lining (hatching) on a section view indicates:",
                (
                    opt("solid material cut by the cutting plane", correct=True),
                    opt("hidden features behind the cut"),
                    opt("the title block region"),
                    opt("an inclined surface in true size"),
                ),
                "Hatching fills the solid faces exposed where the cutting plane passes through material.",
            ),
            q(
                "An auxiliary view is used to show:",
                (
                    opt("the true size and shape of an inclined surface", correct=True),
                    opt("the interior of a hollow part"),
                    opt("the title block"),
                    opt("an exploded assembly"),
                ),
                "An auxiliary view projects onto a plane parallel to a slanted face so it appears in true size.",
            ),
            q(
                "When a cutting plane passes lengthwise along a rib or web, the rib is:",
                (
                    opt("not hatched, to avoid implying a solid disk", correct=True),
                    opt("hatched with doubled line spacing"),
                    opt("removed entirely from the view"),
                    opt("shown only with hidden lines"),
                ),
                "Ribs and webs are conventionally left unhatched when the plane runs along them.",
            ),
        ),
        "Dimensioning fundamentals": (
            q(
                "Good practice is to dimension to:",
                (
                    opt("visible outlines rather than hidden lines", correct=True),
                    opt("hidden lines whenever convenient"),
                    opt("center lines only"),
                    opt("the drawing border"),
                ),
                "ASME Y14.5 directs dimensioning to visible features, placed between and off the views.",
            ),
            q(
                "Compared with baseline dimensioning, chain (incremental) dimensioning:",
                (
                    opt("causes tolerances to accumulate along the chain", correct=True),
                    opt("eliminates all tolerance buildup"),
                    opt("requires no tolerances"),
                    opt("can only be used on circles"),
                ),
                "Each chained dimension adds its tolerance, so error accumulates; baseline references one datum and avoids stacking.",
            ),
            q(
                "How many size dimensions should each feature receive?",
                (
                    opt("exactly one", correct=True),
                    opt("at least two for redundancy"),
                    opt("none - only location dimensions"),
                    opt("one per view it appears in"),
                ),
                "Each feature gets exactly one size dimension; duplicating dimensions creates conflicting requirements.",
            ),
        ),
        "Scale, title blocks and drawing standards": (
            q(
                "On a drawing at 1:2 scale, dimensions written on the part state the:",
                (
                    opt("true (full) size of the feature", correct=True),
                    opt("measured size on the printed sheet"),
                    opt("size divided by two"),
                    opt("size multiplied by two"),
                ),
                "Always dimension the true size; scale only affects how large it is drawn.",
            ),
            q(
                "Which information is found in the title block?",
                (
                    opt("part number, material, scale and units", correct=True),
                    opt("the section hatching pattern"),
                    opt("the auxiliary view"),
                    opt("the miter line"),
                ),
                "The title block records part name/number, material, scale, sheet size, units, revision and approvals.",
            ),
            q(
                "A scale of 2:1 means the drawing shows the object:",
                (
                    opt("twice its real size (enlarged)", correct=True),
                    opt("half its real size"),
                    opt("at real size"),
                    opt("rotated 90 degrees"),
                ),
                "2:1 is an enlargement - drawn length is twice the true length.",
            ),
        ),
    },
    final=(
        q(
            "Orthographic projection differs from perspective because it:",
            (
                opt("uses parallel rays and preserves true size", correct=True),
                opt("uses converging rays and foreshortens depth"),
                opt("can only show one view"),
                opt("requires a 45 degree miter line"),
            ),
            "Parallel, perpendicular rays give undistorted true-size views.",
        ),
        q(
            "Which line is thick and continuous?",
            (
                opt("the visible (object) line", correct=True),
                opt("the hidden line"),
                opt("the dimension line"),
                opt("the center line"),
            ),
            "Visible edges are thick continuous lines.",
        ),
        q(
            "The three most common views for a prismatic part are:",
            (
                opt("front, top and right-side", correct=True),
                opt("front, rear and bottom"),
                opt("top, bottom and rear"),
                opt("left, right and rear"),
            ),
            "Front, top and right usually fully describe a part.",
        ),
        q(
            "A full section view is created by:",
            (
                opt(
                    "passing a cutting plane entirely through the part and hatching the cut",
                    correct=True,
                ),
                opt("projecting onto a plane parallel to an inclined face"),
                opt("removing one quarter of the part"),
                opt("drawing only hidden lines"),
            ),
            "A full section cuts completely through; the exposed solid is hatched.",
        ),
        q(
            "Baseline dimensioning is preferred over chain dimensioning when you want to:",
            (
                opt("prevent tolerance accumulation", correct=True),
                opt("use the fewest extension lines"),
                opt("avoid using any datum"),
                opt("double every tolerance"),
            ),
            "Locating every feature from one datum stops tolerances from stacking.",
        ),
        q(
            "If a part is drawn at 1:2 scale, a feature whose true length is 60 mm appears on the sheet as:",
            (
                opt("30 mm, but is dimensioned 60 mm", correct=True),
                opt("120 mm, dimensioned 120 mm"),
                opt("60 mm, dimensioned 30 mm"),
                opt("15 mm, dimensioned 15 mm"),
            ),
            "At 1:2 it is drawn half size (30 mm) but always dimensioned at true size (60 mm).",
        ),
    ),
)
