"""Quiz questions for the Manufacturing Processes - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Solidification, feeding and riser design": (
            q(
                "A common riser-design criterion using the modulus M = V/A is:",
                (
                    opt("M_riser >= about 1.2 times M_casting", correct=True),
                    opt("M_riser <= M_casting"),
                    opt("M_riser equal to zero"),
                    opt("M_riser independent of M_casting"),
                ),
                "The riser must freeze later, so its modulus exceeds the casting's (about 1.2x).",
            ),
            q(
                "A compact cylindrical riser (h = d) is preferred because it:",
                (
                    opt("has a low surface-area-to-volume ratio, freezing slowly", correct=True),
                    opt("has the highest surface area"),
                    opt("uses the least metal regardless of freezing"),
                    opt("cools faster than the casting"),
                ),
                "Low A/V (compact shape) keeps the riser molten longer to feed shrinkage.",
            ),
            q(
                "Besides freezing later, a riser must also satisfy a:",
                (
                    opt("volume criterion to supply enough feed metal", correct=True),
                    opt("color criterion"),
                    opt("hardness criterion"),
                    opt("spindle-speed criterion"),
                ),
                "Both the freezing-time and volume criteria must pass.",
            ),
        ),
        "Forming forces and energy": (
            q(
                "The 'friction hill' in open-die upsetting means average pressure:",
                (
                    opt("exceeds the flow stress and grows with d/h", correct=True),
                    opt("equals the flow stress everywhere"),
                    opt("falls below the flow stress"),
                    opt("is independent of friction"),
                ),
                "Friction at the die faces raises p_avg above flow stress, rising with d/h.",
            ),
            q(
                "To reduce both forming force and energy you can:",
                (
                    opt("lubricate (lower mu) and/or hot work (lower flow stress)", correct=True),
                    opt("increase friction at the dies"),
                    opt("cool the billet below room temperature"),
                    opt("raise the strain-hardening exponent"),
                ),
                "Lower mu and lower flow stress both cut force and energy.",
            ),
            q(
                "Ideal plastic work per unit volume for sigma = K epsilon^n is:",
                (
                    opt("K epsilon^(n+1) / (n+1)", correct=True),
                    opt("K epsilon^n"),
                    opt("K / epsilon"),
                    opt("n K epsilon"),
                ),
                "Integrating sigma d-epsilon gives K epsilon^(n+1)/(n+1).",
            ),
        ),
        "Metal cutting mechanics": (
            q(
                "In orthogonal cutting, a chip thickness ratio r = t_o/t_c is:",
                (
                    opt("less than or equal to 1", correct=True),
                    opt("always greater than 1"),
                    opt("always exactly 2"),
                    opt("negative"),
                ),
                "The chip is thicker than the uncut layer, so r = t_o/t_c <= 1.",
            ),
            q(
                "Increasing the rake angle (more positive) tends to:",
                (
                    opt("raise the shear angle and lower cutting force", correct=True),
                    opt("lower the shear angle and raise force"),
                    opt("have no effect on the chip"),
                    opt("eliminate all cutting heat"),
                ),
                "A larger rake increases phi and thins the chip, reducing force (but weakens the edge).",
            ),
            q(
                "Cutting power can be estimated from specific cutting energy u_s as:",
                (
                    opt("P = u_s times MRR", correct=True),
                    opt("P = u_s / MRR"),
                    opt("P = MRR / u_s"),
                    opt("P = u_s times tool life"),
                ),
                "Power equals energy per unit volume times volume removed per time (MRR).",
            ),
        ),
        "Tool life and Taylor's equation": (
            q(
                "Taylor's tool-life equation is:",
                (
                    opt("v_c T^n = C", correct=True),
                    opt("v_c + T = C"),
                    opt("v_c / T = n"),
                    opt("T = C v_c"),
                ),
                "v_c T^n = C with n the Taylor exponent and C a constant.",
            ),
            q(
                "A larger Taylor exponent n (e.g. ceramic vs HSS) means tool life is:",
                (
                    opt("less sensitive to cutting speed", correct=True),
                    opt("more sensitive to cutting speed"),
                    opt("independent of the tool material"),
                    opt("always one minute"),
                ),
                "Higher n flattens the speed-life relation, so life drops less with speed.",
            ),
            q(
                "Fitting n and C from two (speed, life) tests is done by:",
                (
                    opt("linear regression in log-log space", correct=True),
                    opt("guessing randomly"),
                    opt("measuring surface roughness"),
                    opt("counting chips"),
                ),
                "Taking logs makes v T^n = C linear in ln v and ln T.",
            ),
        ),
        "Weld thermal cycle and heat input": (
            q(
                "Net heat input per unit length in arc welding is:",
                (
                    opt("H = eta V I / v", correct=True),
                    opt("H = v / (V I)"),
                    opt("H = V I v"),
                    opt("H = eta / (V I)"),
                ),
                "H = eta V I / v: arc efficiency times power over travel speed.",
            ),
            q(
                "Higher travel speed (lower heat input) generally causes:",
                (
                    opt("faster cooling and a harder HAZ", correct=True),
                    opt("slower cooling and a softer HAZ"),
                    opt("no change in cooling rate"),
                    opt("complete elimination of the HAZ"),
                ),
                "Less heat input cools faster, hardening steel HAZs and risking cracking.",
            ),
            q(
                "Preheating the workpiece before welding mainly:",
                (
                    opt("slows cooling and reduces cracking in hardenable steels", correct=True),
                    opt("speeds cooling and increases hardness"),
                    opt("removes the need for filler metal"),
                    opt("lowers the arc voltage"),
                ),
                "Higher T0 slows cooling, reducing HAZ hardness and cracking risk.",
            ),
        ),
        "Tolerances and process capability": (
            q(
                "The capability index C_p is defined as:",
                (
                    opt("(USL - LSL) / (6 sigma)", correct=True),
                    opt("(USL - LSL) / mu"),
                    opt("6 sigma / (USL - LSL)"),
                    opt("mu / sigma"),
                ),
                "C_p compares tolerance width to six standard deviations.",
            ),
            q(
                "C_pk differs from C_p because C_pk also accounts for:",
                (
                    opt("a process mean shifted off center", correct=True),
                    opt("the cutting speed"),
                    opt("the tooling cost"),
                    opt("the heat input"),
                ),
                "C_pk penalizes a mean that is not centered between the limits.",
            ),
            q(
                "A common capability target for an acceptable process is:",
                (
                    opt("C_pk >= 1.33", correct=True),
                    opt("C_pk = 0"),
                    opt("C_pk <= 0.5"),
                    opt("C_pk = -1"),
                ),
                "C_pk >= 1.33 corresponds to roughly 30 ppm defects.",
            ),
        ),
    },
    final=(
        q(
            "The riser-design freezing criterion requires the riser modulus to be:",
            (
                opt("larger than the casting modulus", correct=True),
                opt("smaller than the casting modulus"),
                opt("zero"),
                opt("equal to the pouring temperature"),
            ),
            "The riser must freeze after the section it feeds (about 1.2x modulus).",
        ),
        q(
            "The friction hill makes forging pressure:",
            (
                opt("rise above flow stress as d/h increases", correct=True),
                opt("fall below flow stress"),
                opt("constant regardless of geometry"),
                opt("zero at the die center"),
            ),
            "Die friction raises average pressure, growing with the d/h ratio.",
        ),
        q(
            "Cutting power equals specific cutting energy times:",
            (
                opt("material removal rate (MRR)", correct=True),
                opt("tool life"),
                opt("rake angle"),
                opt("heat input"),
            ),
            "P = u_s * MRR.",
        ),
        q(
            "In v_c T^n = C, increasing cutting speed v_c:",
            (
                opt("reduces tool life T", correct=True),
                opt("increases tool life T"),
                opt("leaves tool life unchanged"),
                opt("changes the constant C"),
            ),
            "Higher speed shortens life along the Taylor curve.",
        ),
        q(
            "Net welding heat input H = eta V I / v increases when:",
            (
                opt("travel speed v decreases", correct=True),
                opt("travel speed v increases"),
                opt("current I decreases"),
                opt("voltage V decreases"),
            ),
            "Slower travel concentrates more energy per unit length.",
        ),
        q(
            "A process with C_pk = 1.5 and centered mean is:",
            (
                opt("very capable, well inside the tolerance band", correct=True),
                opt("incapable, producing many defects"),
                opt("exactly at the spec limit"),
                opt("outside the tolerance on both sides"),
            ),
            "C_pk of 1.5 indicates a highly capable, low-defect process.",
        ),
    ),
)
