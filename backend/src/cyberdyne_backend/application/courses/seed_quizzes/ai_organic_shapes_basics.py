"""Quiz questions for the AI-Driven Organic & Biomimetic Shapes - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why nature builds organic shapes": (
            q(
                "Why do natural structures tend to look organic and porous?",
                (
                    opt(
                        "They are shaped by selection toward efficient use of material and energy",
                        correct=True,
                    ),
                    opt("Random growth with no constraints"),
                    opt("Organisms prefer complex shapes for appearance"),
                    opt("Porous shapes are always the strongest possible"),
                ),
                "Natural form is near-optimal for its loads under material, energy and growth constraints.",
            ),
            q(
                "Biomimicry differs from bio-inspired optimisation in that biomimicry:",
                (
                    opt("copies a working principle observed in nature", correct=True),
                    opt("ignores nature entirely"),
                    opt("only uses neural networks"),
                    opt("always produces lighter parts"),
                ),
                "Biomimicry transfers a natural principle; bio-inspired optimisation lets an algorithm rediscover form.",
            ),
            q(
                "Removing under-stressed material from a solid part initially:",
                (
                    opt("cuts mass sharply while barely lowering stiffness", correct=True),
                    opt("destroys stiffness immediately"),
                    opt("increases mass"),
                    opt("has no effect on either mass or stiffness"),
                ),
                "Material only carries load where stress flows, so removing idle material is nearly free in stiffness.",
            ),
        ),
        "Biomimicry: levels and examples": (
            q(
                "The three levels of biomimicry are form, process, and:",
                (
                    opt("system", correct=True),
                    opt("colour"),
                    opt("material cost"),
                    opt("temperature"),
                ),
                "Biomimicry works at the level of form, process or whole-system organisation.",
            ),
            q(
                "Shark-skin riblets are a biomimetic example used to:",
                (
                    opt("reduce turbulent drag", correct=True),
                    opt("increase weight"),
                    opt("generate electricity"),
                    opt("store heat"),
                ),
                "Riblets reduce turbulent skin-friction drag, a classic form-level biomimicry case.",
            ),
            q(
                "A sandwich panel's bending stiffness scales with core thickness as:",
                (
                    opt("thickness cubed, while mass grows only linearly", correct=True),
                    opt("thickness squared, mass cubed"),
                    opt("linearly, same as mass"),
                    opt("inversely with thickness"),
                ),
                "Bending stiffness goes as t^3 but mass as t, so thicker cores give stiffness per weight cheaply.",
            ),
        ),
        "Scaling laws and allometry": (
            q(
                "Under the square-cube law, scaling a shape up by a factor L grows weight as:",
                (
                    opt("L cubed, while strength grows as L squared", correct=True),
                    opt("L squared, strength as L cubed"),
                    opt("L, strength as L cubed"),
                    opt("both grow as L"),
                ),
                "Volume (weight) ~ L^3 but cross-section (strength) ~ L^2, so big things are relatively weaker.",
            ),
            q(
                "Allometry describes a trait Y versus body mass M using:",
                (
                    opt("a power law Y = a * M^b", correct=True),
                    opt("a straight line Y = a + b*M"),
                    opt("an exponential Y = a*e^M"),
                    opt("a constant"),
                ),
                "Allometric relations are power laws, straight lines on log-log axes with slope b.",
            ),
            q(
                "Doubling the linear scale of a part changes its self-weight stress by roughly:",
                (
                    opt("a factor of 2 (stress grows linearly with size)", correct=True),
                    opt("no change"),
                    opt("a factor of 4"),
                    opt("a factor of 8"),
                ),
                "Self-weight stress ~ weight/area ~ L^3/L^2 = L, so doubling size doubles the stress.",
            ),
        ),
        "Cellular materials, lattices and foams": (
            q(
                "The key descriptor of a cellular material in Gibson-Ashby scaling is:",
                (
                    opt("relative density (solid fraction)", correct=True),
                    opt("absolute temperature"),
                    opt("colour"),
                    opt("print speed"),
                ),
                "Relative density rho*/rhos drives the modulus and strength scaling laws.",
            ),
            q(
                "Compared with a bending-dominated foam, a stretching-dominated octet-truss at the same density is:",
                (
                    opt("stiffer (exponent n closer to 1 instead of 2)", correct=True),
                    opt("always weaker"),
                    opt("identical in stiffness"),
                    opt("only useful for heat exchange"),
                ),
                "Stretching-dominated lattices scale with n~1 versus n~2 for bending, so they are stiffer per weight.",
            ),
            q(
                "Which is a periodic surface-based cellular structure rather than a strut lattice?",
                (
                    opt("Gyroid (a TPMS)", correct=True),
                    opt("BCC strut cell"),
                    opt("Octet-truss"),
                    opt("Random stochastic foam"),
                ),
                "Gyroid and Schwarz-P are triply periodic minimal surfaces; BCC and octet-truss are strut lattices.",
            ),
        ),
        "Curvature and minimal surfaces": (
            q(
                "Gaussian curvature K is defined as:",
                (
                    opt("the product of the two principal curvatures k1*k2", correct=True),
                    opt("the average of the principal curvatures"),
                    opt("the larger principal curvature"),
                    opt("always zero"),
                ),
                "K = k1*k2; mean curvature H = (k1+k2)/2 is the average instead.",
            ),
            q(
                "A minimal surface (like a gyroid wall) is characterised by:",
                (
                    opt("zero mean curvature everywhere", correct=True),
                    opt("zero Gaussian curvature everywhere"),
                    opt("infinite curvature"),
                    opt("being perfectly flat"),
                ),
                "Minimal surfaces have H = 0 at every point, locally minimising area.",
            ),
            q(
                "Sharp internal corners are avoided in organic forms because high curvature there:",
                (
                    opt("concentrates stress", correct=True),
                    opt("reduces weight"),
                    opt("improves print speed"),
                    opt("has no mechanical effect"),
                ),
                "Sharp corners are stress raisers; smooth fillets spread stress, which is why organic forms are rounded.",
            ),
        ),
        "How computers represent organic shape": (
            q(
                "A signed distance field (SDF) stores at each point:",
                (
                    opt("the signed distance to the surface (negative inside)", correct=True),
                    opt("an RGB colour"),
                    opt("a triangle index"),
                    opt("the print temperature"),
                ),
                "An SDF is negative inside, zero on the surface, positive outside.",
            ),
            q(
                "Which representation makes smooth blending and booleans easiest for organic geometry?",
                (
                    opt("Implicit / signed distance fields", correct=True),
                    opt("Triangle meshes"),
                    opt("NURBS B-rep"),
                    opt("2D drawings"),
                ),
                "Implicit fields turn booleans and smooth blends into simple algebra on the field.",
            ),
            q(
                "Doubling the resolution of a dense voxel grid multiplies memory by about:",
                (
                    opt("8 (memory ~ n^3)", correct=True),
                    opt("2"),
                    opt("4"),
                    opt("no change"),
                ),
                "A voxel grid stores n^3 cells, so doubling n along each axis multiplies memory eightfold.",
            ),
        ),
    },
    final=(
        q(
            "Natural organic forms are efficient mainly because they:",
            (
                opt("place material where stress flows, minimising waste", correct=True),
                opt("are grown randomly"),
                opt("always use the densest possible material"),
                opt("ignore mechanical loads"),
            ),
            "Selection drives natural form toward material-efficient, near-optimal structures.",
        ),
        q(
            "Under the square-cube law, larger organisms must be relatively stockier because:",
            (
                opt("weight grows faster (L^3) than strength (L^2)", correct=True),
                opt("strength grows faster than weight"),
                opt("both grow at the same rate"),
                opt("weight is independent of size"),
            ),
            "Stress ~ weight/area ~ L rises with size, forcing thicker proportions at scale.",
        ),
        q(
            "In Gibson-Ashby scaling, a stretching-dominated lattice has a modulus exponent n of about:",
            (
                opt("1", correct=True),
                opt("2"),
                opt("3"),
                opt("0"),
            ),
            "Stretching-dominated lattices scale with n~1; bending-dominated foams with n~2.",
        ),
        q(
            "A gyroid is an example of a:",
            (
                opt("triply periodic minimal surface (TPMS)", correct=True),
                opt("strut-based BCC lattice"),
                opt("solid block"),
                opt("2D pattern only"),
            ),
            "The gyroid is a TPMS with near-zero mean curvature, smooth and self-supporting.",
        ),
        q(
            "Which shape representation is resolution-free and best for smooth booleans?",
            (
                opt("Implicit signed distance field", correct=True),
                opt("Fixed triangle mesh"),
                opt("Bitmap image stack"),
                opt("G-code"),
            ),
            "SDFs can be queried at any point and make blending and booleans trivial.",
        ),
        q(
            "Biomimicry is best applied by:",
            (
                opt("abstracting the working principle, not just copying the animal", correct=True),
                opt("copying the organism's exact appearance only"),
                opt("avoiding any natural inspiration"),
                opt("scaling a design up without re-tuning"),
            ),
            "Good biomimicry abstracts the principle and re-tunes it for the engineering scale and material.",
        ),
    ),
)
