"""Quiz questions for the Engineering Graphics, GD&T & CAD - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Limits, fits and tolerances": (
            q(
                "The tolerance of a dimension is defined as:",
                (
                    opt("the difference between the maximum and minimum limits", correct=True),
                    opt("the nominal size"),
                    opt("the sum of the limits"),
                    opt("the average of the limits"),
                ),
                "Tolerance T = D_max - D_min, the permissible range of size.",
            ),
            q(
                "A fit that always leaves a gap between hole and shaft is a:",
                (
                    opt("clearance fit", correct=True),
                    opt("interference fit"),
                    opt("transition fit"),
                    opt("press fit"),
                ),
                "Clearance fits always have a gap; interference always overlaps; transition may do either.",
            ),
            q(
                "In the hole-basis system, the reference whose size is held fixed at nominal is the:",
                (
                    opt("hole", correct=True),
                    opt("shaft"),
                    opt("keyway"),
                    opt("fillet"),
                ),
                "Hole-basis fixes the hole's lower limit at nominal and varies the shaft to set the fit.",
            ),
        ),
        "Why GD&T: from coordinate tolerancing to function": (
            q(
                "Plus/minus coordinate tolerancing of a hole's x and y position produces a tolerance zone that is:",
                (
                    opt("square, which mismatches the round functional requirement", correct=True),
                    opt("circular, matching function exactly"),
                    opt("triangular"),
                    opt("nonexistent"),
                ),
                "A +/- box is square; function depends on radial distance, so the diagonal over-permits and the sides under-permit.",
            ),
            q(
                "Switching from a square zone to a round true-position zone of the same side gains roughly:",
                (
                    opt("57% more usable area", correct=True),
                    opt("no additional area"),
                    opt("90% less area"),
                    opt("exactly double the area"),
                ),
                "The round zone area is pi/2 ~ 1.57 times the square, about 57% more good parts accepted.",
            ),
            q(
                "A primary advantage of GD&T over coordinate tolerancing is that it:",
                (
                    opt("references functional datums and captures design intent", correct=True),
                    opt("removes the need for any tolerances"),
                    opt("makes all features the same size"),
                    opt("eliminates the title block"),
                ),
                "GD&T controls geometry relative to datums, enabling functional gaging and bonus tolerance.",
            ),
        ),
        "Geometric characteristics and feature control frames": (
            q(
                "How many geometric characteristic symbols does ASME Y14.5 define?",
                (
                    opt("14", correct=True),
                    opt("5"),
                    opt("10"),
                    opt("20"),
                ),
                "There are 14 characteristics across form, orientation, location, profile and runout.",
            ),
            q(
                "Which family of controls requires NO datum reference?",
                (
                    opt("form (flatness, straightness, circularity, cylindricity)", correct=True),
                    opt("orientation"),
                    opt("location"),
                    opt("runout"),
                ),
                "Form controls are self-referencing and take no datum; orientation, location and runout require datums.",
            ),
            q(
                "Reading left to right, a feature control frame lists:",
                (
                    opt(
                        "symbol, then tolerance with modifiers, then datum references", correct=True
                    ),
                    opt("datums, then symbol, then nominal size"),
                    opt("material, then symbol, then scale"),
                    opt("title block info only"),
                ),
                "The FCF reads: characteristic symbol | tolerance (and modifiers) | datum references.",
            ),
        ),
        "Datums and the datum reference frame": (
            q(
                "A rigid part has how many degrees of freedom to be constrained by a datum reference frame?",
                (
                    opt("six (three translations, three rotations)", correct=True),
                    opt("three"),
                    opt("two"),
                    opt("twelve"),
                ),
                "Six DOF: three translations and three rotations, fully constrained by the 3-2-1 scheme.",
            ),
            q(
                "In the 3-2-1 rule, the primary datum is established with:",
                (
                    opt("three points of contact, removing 3 DOF", correct=True),
                    opt("one point, removing 1 DOF"),
                    opt("two points, removing 2 DOF"),
                    opt("six points"),
                ),
                "Primary uses 3 points (-3 DOF), secondary 2 points (-2), tertiary 1 point (-1): 3+2+1=6.",
            ),
            q(
                "Why does the order of datums (primary, secondary, tertiary) matter?",
                (
                    opt(
                        "it determines how the part seats and therefore the measured results",
                        correct=True,
                    ),
                    opt("it changes the part material"),
                    opt("it has no effect on measurement"),
                    opt("it sets the drawing scale"),
                ),
                "Datum precedence controls contact order and seating, so reversing it changes measurements.",
            ),
        ),
        "Material condition modifiers and bonus tolerance": (
            q(
                "Maximum material condition (MMC) of a hole corresponds to the:",
                (
                    opt("smallest hole (most material)", correct=True),
                    opt("largest hole"),
                    opt("nominal hole only"),
                    opt("hole at its mean size"),
                ),
                "MMC is the condition with the most material - for a hole that is the smallest diameter.",
            ),
            q(
                "Bonus tolerance is gained when a feature toleranced at MMC:",
                (
                    opt("departs from MMC toward LMC", correct=True),
                    opt("stays exactly at MMC"),
                    opt("is referenced regardless of feature size"),
                    opt("has no datum"),
                ),
                "Departing from MMC adds the size departure as extra (bonus) geometric tolerance.",
            ),
            q(
                "A hole with MMC = 10.00 mm and position tolerance 0.20 at MMC measures 10.30 mm actual. The total position tolerance is:",
                (
                    opt("0.50 mm", correct=True),
                    opt("0.20 mm"),
                    opt("0.30 mm"),
                    opt("0.10 mm"),
                ),
                "Bonus = |10.30 - 10.00| = 0.30; total = 0.20 + 0.30 = 0.50 mm.",
            ),
        ),
        "Tolerance stack-up analysis": (
            q(
                "Worst-case tolerance stack-up combines part tolerances by:",
                (
                    opt("summing them", correct=True),
                    opt("root-sum-square"),
                    opt("taking the maximum"),
                    opt("averaging them"),
                ),
                "Worst-case sums all tolerances, assuming every part is at its worst limit simultaneously.",
            ),
            q(
                "The statistical (RSS) stack-up of n equal tolerances t grows as:",
                (
                    opt("t times the square root of n", correct=True),
                    opt("n times t"),
                    opt("t divided by n"),
                    opt("t squared"),
                ),
                "RSS = sqrt(sum of t^2); for equal t it is t*sqrt(n), versus n*t for worst-case.",
            ),
            q(
                "RSS is appropriate primarily for:",
                (
                    opt(
                        "high-volume production with an acceptable defined reject rate",
                        correct=True,
                    ),
                    opt("safety-critical one-off assemblies needing 100% interchangeability"),
                    opt("parts with a single dimension"),
                    opt("drawings without tolerances"),
                ),
                "RSS allows looser, cheaper tolerances at a small statistical reject risk - good for volume; worst-case suits safety-critical.",
            ),
        ),
    },
    final=(
        q(
            "The ISO standard tolerance unit i used to size IT grades increases with:",
            (
                opt("nominal size", correct=True),
                opt("surface roughness"),
                opt("material density"),
                opt("drawing scale"),
            ),
            "i = 0.45 D^(1/3) + 0.001 D, so tolerance grows with nominal size.",
        ),
        q(
            "Compared to a square +/- zone, the round true-position zone is preferred because it:",
            (
                opt("matches the radial nature of the functional requirement", correct=True),
                opt("is easier to draw"),
                opt("needs no datum"),
                opt("ignores feature size"),
            ),
            "Function depends on radial distance, which the round zone represents correctly.",
        ),
        q(
            "Which is a FORM control requiring no datum?",
            (
                opt("flatness", correct=True),
                opt("position"),
                opt("perpendicularity"),
                opt("total runout"),
            ),
            "Flatness is a form control; position, perpendicularity and runout need datums.",
        ),
        q(
            "Applying datums in the 3-2-1 sequence constrains a total of how many degrees of freedom?",
            (
                opt("six", correct=True),
                opt("three"),
                opt("five"),
                opt("nine"),
            ),
            "3 + 2 + 1 = 6 degrees of freedom fully constrained.",
        ),
        q(
            "A shaft toleranced at MMC earns bonus tolerance when its actual size:",
            (
                opt("departs from MMC toward LMC", correct=True),
                opt("equals MMC exactly"),
                opt("equals nominal"),
                opt("is regardless of feature size"),
            ),
            "Bonus equals the departure from MMC, added to the geometric tolerance.",
        ),
        q(
            "For five parts each at +/-0.1 mm, the worst-case and RSS assembly tolerances are about:",
            (
                opt("0.50 mm and 0.22 mm", correct=True),
                opt("0.10 mm and 0.10 mm"),
                opt("0.50 mm and 0.50 mm"),
                opt("0.22 mm and 0.50 mm"),
            ),
            "Worst-case = 5*0.1 = 0.50; RSS = 0.1*sqrt(5) ~ 0.22 mm.",
        ),
    ),
)
