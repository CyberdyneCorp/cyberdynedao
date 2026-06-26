"""Quiz questions for the Additive Manufacturing - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Design for additive manufacturing (DfAM)": (
            q(
                "A core goal of DfAM part consolidation is to:",
                (
                    opt("replace an assembly with a single printed part", correct=True),
                    opt("add more fasteners for strength"),
                    opt("split parts into many subcomponents"),
                    opt("maximize raw material usage"),
                ),
                "Consolidation removes joints, fasteners and inspection steps by printing one part.",
            ),
            q(
                "The buy-to-fly ratio measures:",
                (
                    opt("raw material input per finished part", correct=True),
                    opt("flight hours per aircraft"),
                    opt("layers per millimeter"),
                    opt("laser power per scan"),
                ),
                "A high buy-to-fly ratio (e.g. 20:1 in machining) means lots of wasted material; AM lowers it.",
            ),
            q(
                "A common self-supporting overhang guideline is surfaces steeper than about:",
                (
                    opt("45 degrees from horizontal", correct=True),
                    opt("5 degrees from horizontal"),
                    opt("85 degrees from horizontal"),
                    opt("0 degrees (fully horizontal)"),
                ),
                "Surfaces above ~45 deg from horizontal are usually self-supporting.",
            ),
        ),
        "Lattices and TPMS structures": (
            q(
                "Gibson-Ashby scaling relates a lattice's relative modulus to:",
                (
                    opt("relative density raised to a power n", correct=True),
                    opt("absolute build temperature"),
                    opt("the laser wavelength"),
                    opt("the number of layers"),
                ),
                "E*/Es = C (rho*/rhos)^n, with n depending on the deformation mode.",
            ),
            q(
                "Stretching-dominated lattices (e.g. octet-truss) versus bending-dominated ones are:",
                (
                    opt("stiffer at the same relative density (n closer to 1)", correct=True),
                    opt("always heavier"),
                    opt("less stiff at the same density"),
                    opt("impossible to print"),
                ),
                "Stretching-dominated topologies have n ~ 1, far stiffer per unit mass than bending (n ~ 2).",
            ),
            q(
                "A gyroid is an example of a:",
                (
                    opt("triply periodic minimal surface (TPMS)", correct=True),
                    opt("strut-based BCC lattice"),
                    opt("solid infill pattern"),
                    opt("support structure type"),
                ),
                "Gyroid, Schwarz-P and diamond are TPMS, defined by implicit fields.",
            ),
        ),
        "Topology optimization for AM": (
            q(
                "In the SIMP method, element stiffness is interpolated as:",
                (
                    opt("E = Emin + x^p (E0 - Emin) with penalty p ~ 3", correct=True),
                    opt("E = x / p"),
                    opt("E = E0 * sin(x)"),
                    opt("E = constant regardless of density"),
                ),
                "SIMP penalizes intermediate densities with the exponent p (typically 3).",
            ),
            q(
                "Classic topology optimization typically minimizes which objective?",
                (
                    opt(
                        "compliance (maximizing stiffness) under a volume constraint", correct=True
                    ),
                    opt("the number of triangles in the STL"),
                    opt("the print time only"),
                    opt("the laser power"),
                ),
                "Minimizing compliance c = U^T K U for a mass budget maximizes stiffness.",
            ),
            q(
                "A density filter is applied in topology optimization to:",
                (
                    opt("avoid checkerboarding and enforce a minimum length scale", correct=True),
                    opt("increase the volume fraction"),
                    opt("remove all supports"),
                    opt("speed up the FE solve only"),
                ),
                "Filtering prevents numerical checkerboard patterns and imposes a minimum member size.",
            ),
        ),
        "Supports, overhangs and slicing": (
            q(
                "Surfaces shallower than the critical overhang angle tend to:",
                (
                    opt("sag or curl and require supports", correct=True),
                    opt("print perfectly without supports"),
                    opt("become stronger"),
                    opt("cure faster"),
                ),
                "Below the critical angle the overhang is not self-supporting and needs support.",
            ),
            q(
                "Besides anchoring, support structures in metal PBF also serve to:",
                (
                    opt("conduct heat and resist recoater forces", correct=True),
                    opt("add color to the part"),
                    opt("reduce the part's mass"),
                    opt("replace post-curing"),
                ),
                "Supports act as heat sinks and stabilize the part against recoater loads.",
            ),
            q(
                "Choosing build orientation to minimize supported area is:",
                (
                    opt("an optimization trade-off affecting cost and finish", correct=True),
                    opt("irrelevant to print success"),
                    opt("fixed by the slicer automatically with no trade-offs"),
                    opt("only about part color"),
                ),
                "Orientation changes supported area, surface finish, accuracy and post-processing labor.",
            ),
        ),
        "Simulation, ML and in-situ monitoring": (
            q(
                "The inherent-strain method is used to:",
                (
                    opt("predict build distortion and residual stress quickly", correct=True),
                    opt("generate G-code"),
                    opt("measure powder humidity"),
                    opt("color the part"),
                ),
                "Inherent-strain build simulation predicts distortion so geometry can be pre-compensated.",
            ),
            q(
                "Geometry pre-compensation means:",
                (
                    opt("warping the CAD by the negative of predicted distortion", correct=True),
                    opt("printing the part twice"),
                    opt("increasing infill density"),
                    opt("adding more supports everywhere"),
                ),
                "Morphing the model opposite to predicted distortion makes it spring back to nominal.",
            ),
            q(
                "Typical in-situ monitoring sensors for laser PBF include:",
                (
                    opt("melt-pool cameras, pyrometers and photodiodes", correct=True),
                    opt("strain gauges on the operator"),
                    opt("only a thermometer on the powder bin"),
                    opt("a microphone for room noise"),
                ),
                "Coaxial melt-pool imaging, photodiode intensity and pyrometry feed ML defect detection.",
            ),
        ),
    },
    final=(
        q(
            "A primary DfAM strategy enabled by AM's geometric freedom is:",
            (
                opt("part consolidation and lightweighting", correct=True),
                opt("adding more bolted joints"),
                opt("maximizing material waste"),
                opt("avoiding internal channels"),
            ),
            "AM lets engineers consolidate assemblies and lightweight with lattices and TO.",
        ),
        q(
            "Gibson-Ashby relative modulus scales as (rho*/rhos)^n; n near 2 indicates:",
            (
                opt("a bending-dominated lattice", correct=True),
                opt("a stretching-dominated lattice"),
                opt("a fully solid part"),
                opt("a support structure"),
            ),
            "n ~ 2 is bending-dominated; n ~ 1 is the stiffer stretching-dominated case.",
        ),
        q(
            "SIMP topology optimization minimizes compliance subject to:",
            (
                opt("a volume (mass) constraint", correct=True),
                opt("a fixed number of layers"),
                opt("a maximum laser power"),
                opt("a color budget"),
            ),
            "The volume fraction caps material while compliance is minimized for stiffness.",
        ),
        q(
            "Required support area increases sharply as a surface becomes:",
            (
                opt("more horizontal (overhang angle decreases)", correct=True),
                opt("more vertical"),
                opt("thicker"),
                opt("hotter"),
            ),
            "Support area scales roughly with 1/sin(theta); flatter overhangs need much more support.",
        ),
        q(
            "Build simulation feeds back into design mainly by:",
            (
                opt("pre-compensating geometry for predicted distortion", correct=True),
                opt("choosing the part color"),
                opt("setting the spool weight"),
                opt("eliminating slicing"),
            ),
            "Predicted distortion is used to warp the CAD so the part prints to nominal.",
        ),
        q(
            "In-situ ML monitoring in AM is mainly used to:",
            (
                opt("detect porosity and process anomalies during the build", correct=True),
                opt("replace the CAD model"),
                opt("increase room temperature"),
                opt("color the finished part"),
            ),
            "ML on melt-pool and layer-wise sensor data flags defects to cut qualification cost.",
        ),
    ),
)
