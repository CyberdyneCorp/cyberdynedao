"""Quiz questions for the Machine Design & Elements - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Endurance limit and Marin factors": (
            q(
                "The uncorrected endurance limit is commonly estimated as:",
                (
                    opt("about half the ultimate tensile strength", correct=True),
                    opt("twice the ultimate strength"),
                    opt("equal to the yield strength"),
                    opt("zero"),
                ),
                "Se' is roughly 0.5 Sut for steels up to about 1400 MPa.",
            ),
            q(
                "Marin factors are used to:",
                (
                    opt("derate the lab endurance limit for real-part conditions", correct=True),
                    opt("increase the endurance limit above the lab value"),
                    opt("compute the static factor of safety"),
                    opt("find the bearing life"),
                ),
                "ka..ke account for surface, size, load, temperature and reliability.",
            ),
            q(
                "Each Marin factor is generally:",
                (
                    opt("less than or equal to 1, reducing Se", correct=True),
                    opt("greater than 1, raising Se"),
                    opt("always exactly 1"),
                    opt("negative"),
                ),
                "Real conditions only lower the endurance limit, so factors are <= 1.",
            ),
        ),
        "Mean stress: Goodman, Gerber, Soderberg": (
            q(
                "A positive (tensile) mean stress generally:",
                (
                    opt("reduces fatigue life", correct=True),
                    opt("increases fatigue life"),
                    opt("has no effect on fatigue"),
                    opt("eliminates the alternating stress"),
                ),
                "Tensile mean stress shifts the operating point toward failure.",
            ),
            q(
                "The Goodman criterion draws a straight line between:",
                (
                    opt("Se on the alternating axis and Sut on the mean axis", correct=True),
                    opt("Se and Sy"),
                    opt("Sut and zero"),
                    opt("two yield points"),
                ),
                "Goodman connects Se (sigma_a axis) to Sut (sigma_m axis).",
            ),
            q(
                "Among the three criteria, the most conservative is usually:",
                (
                    opt("Soderberg (uses Sy on the mean axis)", correct=True),
                    opt("Gerber"),
                    opt("Goodman"),
                    opt("none are conservative"),
                ),
                "Soderberg goes to the yield strength, giving the smallest safe region.",
            ),
        ),
        "Shaft design under combined loading": (
            q(
                "A rotating shaft with a steady transverse load experiences:",
                (
                    opt("fully reversed bending plus steady torsion", correct=True),
                    opt("steady bending only"),
                    opt("no fatigue loading"),
                    opt("pure axial load"),
                ),
                "Rotation turns a constant bending moment into reversed bending.",
            ),
            q(
                "The DE-Goodman shaft equation solves directly for the:",
                (
                    opt("required shaft diameter d", correct=True),
                    opt("bearing L10 life"),
                    opt("gear module"),
                    opt("weld FAT class"),
                ),
                "It combines distortion-energy stresses with Goodman and is solved for d.",
            ),
            q(
                "After sizing a shaft for strength, the next checks are typically:",
                (
                    opt("deflection and critical speed (whirl)", correct=True),
                    opt("paint thickness"),
                    opt("bolt preload only"),
                    opt("none are needed"),
                ),
                "Shafts often fail serviceability before fatigue, so check stiffness and whirl.",
            ),
        ),
        "Rolling-element bearing life": (
            q(
                "The L10 life of a rolling-element bearing follows:",
                (
                    opt("(C/P) raised to a power a (3 for balls)", correct=True),
                    opt("C times P"),
                    opt("P divided by C only"),
                    opt("the square root of C"),
                ),
                "L10 = (C/P)^a, with a = 3 for ball bearings.",
            ),
            q(
                "The basic dynamic load rating C corresponds to a life of:",
                (
                    opt("one million revolutions for 90 percent of bearings", correct=True),
                    opt("one revolution"),
                    opt("infinite life for all bearings"),
                    opt("one hour at any speed"),
                ),
                "C is the load giving 1e6 revolutions at 90 percent reliability.",
            ),
            q(
                "Doubling the load on a ball bearing reduces its L10 life by about:",
                (
                    opt("a factor of eight", correct=True),
                    opt("a factor of two"),
                    opt("no change"),
                    opt("a factor of sixteen"),
                ),
                "Life scales as (C/P)^3, so 2x load cuts life by 2^3 = 8.",
            ),
        ),
        "Spur gear bending and contact stress": (
            q(
                "Spur gear teeth are designed against:",
                (
                    opt("root bending stress and surface contact stress", correct=True),
                    opt("hoop stress and longitudinal stress"),
                    opt("buckling and torsion only"),
                    opt("preload and surge"),
                ),
                "The Lewis/AGMA bending check and the Hertzian contact check both apply.",
            ),
            q(
                "The tangential tooth load Wt is obtained from:",
                (
                    opt("transmitted power divided by pitch-line velocity", correct=True),
                    opt("the module times the face width"),
                    opt("the Lewis form factor"),
                    opt("the bearing rating C"),
                ),
                "Wt = P / V, where V is the pitch-line velocity.",
            ),
            q(
                "Surface (contact) fatigue in gears manifests as:",
                (
                    opt("pitting of the tooth flank", correct=True),
                    opt("buckling of the rim"),
                    opt("thread stripping"),
                    opt("weld toe cracking"),
                ),
                "Hertzian contact stress causes pitting, often governing hardened gears.",
            ),
        ),
        "Bolted joints and preload": (
            q(
                "The joint stiffness constant C is defined as:",
                (
                    opt("kb / (kb + km)", correct=True),
                    opt("km / (kb + km)"),
                    opt("kb times km"),
                    opt("kb - km"),
                ),
                "C is the fraction of external load taken by the bolt.",
            ),
            q(
                "Because members are much stiffer than the bolt, C is typically:",
                (
                    opt("about 0.2 to 0.3", correct=True),
                    opt("about 0.9"),
                    opt("exactly 1"),
                    opt("negative"),
                ),
                "A small C means the bolt sees only a fraction of the external load.",
            ),
            q(
                "Recommended preload for a reusable connection is about:",
                (
                    opt("0.75 of the proof load", correct=True),
                    opt("0.10 of the proof load"),
                    opt("zero"),
                    opt("twice the proof load"),
                ),
                "Fi = 0.75 Fp for reusable, 0.90 Fp for permanent joints.",
            ),
        ),
    },
    final=(
        q(
            "The corrected endurance limit Se is the lab value multiplied by:",
            (
                opt("the Marin factors (each <= 1)", correct=True),
                opt("the factor of safety"),
                opt("the bearing rating C"),
                opt("the gear module"),
            ),
            "Se = ka kb kc kd ke times Se', each Marin factor reducing it.",
        ),
        q(
            "On the mean-stress diagram, a point inside the Goodman line is:",
            (
                opt("safe against fatigue (n greater than 1)", correct=True),
                opt("at the point of failure"),
                opt("always yielding"),
                opt("impossible"),
            ),
            "Inside the line n > 1; on the line n = 1.",
        ),
        q(
            "A rotating shaft converts a constant bending moment into:",
            (
                opt("fully reversed (alternating) bending stress", correct=True),
                opt("steady stress"),
                opt("pure torsion"),
                opt("zero stress"),
            ),
            "Rotation makes each fibre alternate between tension and compression.",
        ),
        q(
            "Ball-bearing L10 life varies with load as:",
            (
                opt("(C/P) cubed", correct=True),
                opt("C/P linear"),
                opt("(C/P) squared"),
                opt("the log of C/P"),
            ),
            "For ball bearings a = 3, so life = (C/P)^3.",
        ),
        q(
            "Gear tooth bending stress (Lewis/AGMA) decreases when you:",
            (
                opt("increase the face width F", correct=True),
                opt("decrease the module"),
                opt("increase the transmitted load"),
                opt("reduce the face width"),
            ),
            "sigma_b ~ Wt/(F m Y), so wider face reduces bending stress.",
        ),
        q(
            "In a preloaded bolted joint, separation occurs when the external load reaches:",
            (
                opt("Fi / (1 - C)", correct=True),
                opt("Fi times C"),
                opt("zero"),
                opt("the proof load times 10"),
            ),
            "Separation load P0 = Fi/(1-C); keep working load well below it.",
        ),
    ),
)
