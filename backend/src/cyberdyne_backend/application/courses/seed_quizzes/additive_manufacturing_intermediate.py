"""Quiz questions for the Additive Manufacturing - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Powder bed fusion: SLS, SLM, DMLS, EBM": (
            q(
                "Which powder bed fusion variant uses an electron beam in vacuum?",
                (
                    opt("EBM", correct=True),
                    opt("SLS"),
                    opt("SLM"),
                    opt("DMLS"),
                ),
                "EBM melts metal with an electron beam in vacuum and uses high preheat.",
            ),
            q(
                "Why does polymer SLS generally not need support structures?",
                (
                    opt("the surrounding powder cake holds the part", correct=True),
                    opt("nylon does not warp"),
                    opt("the laser cures resin instantly"),
                    opt("the build chamber is pressurized"),
                ),
                "In SLS the un-sintered powder bed supports overhangs, so no added supports are needed.",
            ),
            q(
                "A typical particle size range for laser metal powder bed fusion is:",
                (
                    opt("15-45 micrometers", correct=True),
                    opt("0.1-1 micrometer"),
                    opt("150-450 micrometers"),
                    opt("1-5 millimeters"),
                ),
                "Metal AM powders are usually 15-45 um for good spreadability and resolution.",
            ),
        ),
        "Laser melting physics and energy density": (
            q(
                "Volumetric energy density in laser PBF is defined as:",
                (
                    opt("P / (v * h * t)", correct=True),
                    opt("P * v * h * t"),
                    opt("v / (P * h * t)"),
                    opt("P / (v + h + t)"),
                ),
                "EV = P/(v h t) with units J/mm^3; P power, v scan speed, h hatch, t layer.",
            ),
            q(
                "Excessively high energy density tends to cause:",
                (
                    opt("keyholing porosity from entrapped vapor", correct=True),
                    opt("lack-of-fusion porosity"),
                    opt("perfectly dense parts always"),
                    opt("no melting at all"),
                ),
                "Too much energy destabilizes the melt pool into a keyhole, trapping vapor pores.",
            ),
            q(
                "The Rosenthal solution describes the temperature field of:",
                (
                    opt("a moving point heat source", correct=True),
                    opt("a static uniform furnace"),
                    opt("radiative cooling only"),
                    opt("a vibrating beam"),
                ),
                "Rosenthal gives the quasi-steady thermal field of a moving point source.",
            ),
        ),
        "Materials and microstructure in AM": (
            q(
                "Fusion AM is characterized by which thermal condition?",
                (
                    opt("very high cooling rates (10^3-10^6 K/s)", correct=True),
                    opt("extremely slow furnace cooling"),
                    opt("constant uniform temperature"),
                    opt("no temperature change"),
                ),
                "Rapid melting and solidification give cooling rates of 10^3-10^6 K/s.",
            ),
            q(
                "High thermal gradient G with high G/R ratio favors which grain morphology?",
                (
                    opt("columnar grains along the build direction", correct=True),
                    opt("fully equiaxed grains"),
                    opt("amorphous glass"),
                    opt("single perfect crystal of arbitrary size"),
                ),
                "High G/R favors planar/columnar growth aligned with the steep gradient.",
            ),
            q(
                "Which post-process is used to close internal porosity in metal AM parts?",
                (
                    opt("hot isostatic pressing (HIP)", correct=True),
                    opt("electropolishing"),
                    opt("anodizing"),
                    opt("shot peening"),
                ),
                "HIP applies high temperature and isostatic pressure to collapse internal pores.",
            ),
        ),
        "Residual stress and distortion": (
            q(
                "Residual stress in PBF arises mainly from:",
                (
                    opt("constrained thermal contraction of each new layer", correct=True),
                    opt("chemical etching"),
                    opt("magnetic fields"),
                    opt("powder humidity"),
                ),
                "The thermal gradient mechanism: hot layers contract while restrained below.",
            ),
            q(
                "The thermal strain from a temperature change is estimated by:",
                (
                    opt("eps = alpha * dT", correct=True),
                    opt("eps = dT / alpha"),
                    opt("eps = alpha / dT"),
                    opt("eps = alpha * dT^2"),
                ),
                "Thermal strain equals the CTE times the temperature change.",
            ),
            q(
                "Which is an effective mitigation for residual stress and distortion?",
                (
                    opt("scan-vector rotation and base-plate preheat", correct=True),
                    opt("removing all supports before printing"),
                    opt("increasing layer height to maximum"),
                    opt("printing in open air with no shielding"),
                ),
                "Rotating scan vectors, preheating, robust supports and stress relief reduce distortion.",
            ),
        ),
        "Dimensional accuracy and tolerances": (
            q(
                "Stair-stepping roughness on an inclined surface scales roughly with:",
                (
                    opt("layer thickness times cosine of the surface angle", correct=True),
                    opt("layer thickness times sine of the surface angle"),
                    opt("nozzle diameter divided by speed"),
                    opt("laser power times hatch spacing"),
                ),
                "Cusp height ~ (t/4) cos(theta); near-vertical walls are smoothest.",
            ),
            q(
                "To hit nominal size despite shrinkage, the model should be:",
                (
                    opt("pre-scaled larger by a compensation factor", correct=True),
                    opt("printed exactly at nominal"),
                    opt("scaled smaller"),
                    opt("rotated 90 degrees"),
                ),
                "Pre-scale by 1/(1 - shrink) so the part lands on nominal after shrinkage.",
            ),
            q(
                "Critical toleranced features on a metal AM part are usually:",
                (
                    opt("printed oversize and finish-machined", correct=True),
                    opt("left as-built without finishing"),
                    opt("printed with zero supports"),
                    opt("etched chemically to size"),
                ),
                "As-built tolerances are coarse, so critical faces get machining stock and CNC finishing.",
            ),
        ),
    },
    final=(
        q(
            "Which PBF process fully melts metal powder with a laser under inert gas?",
            (
                opt("SLM / DMLS", correct=True),
                opt("SLS"),
                opt("binder jetting"),
                opt("FFF"),
            ),
            "SLM/DMLS fully melt metal with a laser under an argon or nitrogen atmosphere.",
        ),
        q(
            "Volumetric energy density EV equals:",
            (
                opt("P / (v * h * t)", correct=True),
                opt("P * v * h * t"),
                opt("h * t / (P * v)"),
                opt("v * t / P"),
            ),
            "EV = P/(v h t), J/mm^3.",
        ),
        q(
            "Low energy density most often produces which defect?",
            (
                opt("lack-of-fusion porosity", correct=True),
                opt("keyholing porosity"),
                opt("over-melting"),
                opt("excessive density"),
            ),
            "Too little energy under-melts the powder, leaving lack-of-fusion voids.",
        ),
        q(
            "Rapid AM solidification typically produces:",
            (
                opt("fine, often columnar grains and metastable phases", correct=True),
                opt("coarse equiaxed grains only"),
                opt("a fully amorphous metal"),
                opt("a defect-free single crystal automatically"),
            ),
            "High gradients and fast cooling give fine columnar grains and phases like alpha-prime.",
        ),
        q(
            "Distortion in metal PBF is best reduced by:",
            (
                opt("scan rotation, preheat, supports and stress relief", correct=True),
                opt("maximizing energy density"),
                opt("skipping supports"),
                opt("printing flat horizontal surfaces only"),
            ),
            "These control or relax the residual stress that drives warping.",
        ),
        q(
            "Stair-step roughness is minimized on surfaces that are:",
            (
                opt("near-vertical (steep from horizontal)", correct=True),
                opt("near-horizontal up-facing"),
                opt("oriented at exactly 45 degrees"),
                opt("printed with the thickest layers"),
            ),
            "Ra ~ cos(theta), so vertical walls (theta near 90 deg) are smoothest.",
        ),
    ),
)
