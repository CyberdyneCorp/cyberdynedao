"""Quiz questions for the Mechanics of Materials - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Normal and shear stress": (
            q(
                "Normal stress on a cut face is defined as:",
                (
                    opt("force component perpendicular to the face divided by area", correct=True),
                    opt("force component tangent to the face divided by area"),
                    opt("force times area"),
                    opt("the change in length divided by original length"),
                ),
                "Normal stress sigma = N/A uses the force component perpendicular to the face.",
            ),
            q(
                "Shear stress on a face is the:",
                (
                    opt("tangential force component divided by area", correct=True),
                    opt("perpendicular force divided by area"),
                    opt("moment divided by area"),
                    opt("pressure times volume"),
                ),
                "Shear stress tau = V/A uses the in-plane (tangential) force component.",
            ),
            q(
                "For a bar of fixed area, increasing the axial force will:",
                (
                    opt("increase the normal stress proportionally", correct=True),
                    opt("decrease the normal stress"),
                    opt("leave the stress unchanged"),
                    opt("convert the stress entirely to shear"),
                ),
                "Since sigma = N/A and A is fixed, stress rises in proportion to N.",
            ),
        ),
        "Normal and shear strain": (
            q(
                "Normal strain is defined as:",
                (
                    opt("change in length divided by original length", correct=True),
                    opt("force divided by area"),
                    opt("change in angle between fibres"),
                    opt("stress times Young's modulus"),
                ),
                "Normal strain epsilon = delta / L0 is dimensionless.",
            ),
            q(
                "Shear strain measures:",
                (
                    opt("the change in an originally right angle, in radians", correct=True),
                    opt("the fractional change in length"),
                    opt("the force per unit area"),
                    opt("the volume change of the body"),
                ),
                "Shear strain gamma is the angular distortion of an initially right angle.",
            ),
            q(
                "True strain differs from engineering strain because it uses:",
                (
                    opt("the current length instead of the original length", correct=True),
                    opt("the original area instead of current area"),
                    opt("the applied force instead of the stress"),
                    opt("a logarithm of the stress"),
                ),
                "True strain epsilon_t = ln(L/L0) is based on the instantaneous length.",
            ),
        ),
        "The stress-strain curve": (
            q(
                "On a ductile metal's stress-strain curve, the ultimate tensile strength is:",
                (
                    opt("the peak stress reached before fracture", correct=True),
                    opt("the stress at first yield"),
                    opt("the stress at the proportional limit"),
                    opt("the stress at zero strain"),
                ),
                "The ultimate tensile strength sigma_u is the maximum stress on the curve.",
            ),
            q(
                "The 0.2 percent offset method is used to define the:",
                (
                    opt("yield strength when there is no sharp yield point", correct=True),
                    opt("ultimate strength"),
                    opt("Young's modulus"),
                    opt("Poisson's ratio"),
                ),
                "The 0.2% offset construction locates a practical yield strength for metals without a sharp knee.",
            ),
            q(
                "Compared with ductile materials, brittle materials typically:",
                (
                    opt(
                        "fracture near the elastic limit with little plastic deformation",
                        correct=True,
                    ),
                    opt("show a long strain-hardening region"),
                    opt("absorb more energy before fracture"),
                    opt("have a higher Poisson's ratio by definition"),
                ),
                "Brittle materials fracture with almost no plastic region and low toughness.",
            ),
        ),
        "Hooke's law and Young's modulus": (
            q(
                "Hooke's law for uniaxial loading states that:",
                (
                    opt("sigma = E times epsilon", correct=True),
                    opt("sigma = E divided by epsilon"),
                    opt("epsilon = E times sigma"),
                    opt("sigma = E times epsilon squared"),
                ),
                "In the linear-elastic region stress is proportional to strain: sigma = E*epsilon.",
            ),
            q(
                "Young's modulus E represents the material's:",
                (
                    opt("stiffness (slope of the elastic line)", correct=True),
                    opt("strength at fracture"),
                    opt("ductility"),
                    opt("density"),
                ),
                "E is the elastic stiffness, the slope of the stress-strain line.",
            ),
            q(
                "The axial deformation of a uniform bar is:",
                (
                    opt("delta = N L / (A E)", correct=True),
                    opt("delta = A E / (N L)"),
                    opt("delta = N A / (L E)"),
                    opt("delta = E L / (N A)"),
                ),
                "Combining Hooke's law with the definitions gives delta = NL/(AE).",
            ),
        ),
        "Poisson's ratio and elastic constants": (
            q(
                "Poisson's ratio is the ratio of:",
                (
                    opt("lateral contraction to axial extension (with a sign)", correct=True),
                    opt("stress to strain"),
                    opt("shear stress to shear strain"),
                    opt("axial force to area"),
                ),
                "nu = -epsilon_lateral / epsilon_axial; about 0.3 for many metals.",
            ),
            q(
                "For an isotropic material, how many independent elastic constants are there?",
                (
                    opt("two", correct=True),
                    opt("one"),
                    opt("three"),
                    opt("six"),
                ),
                "Knowing any two (e.g. E and nu) fixes G and K and the full response.",
            ),
            q(
                "The shear modulus is related to E and nu by:",
                (
                    opt("G = E / (2(1 + nu))", correct=True),
                    opt("G = E times (1 + nu)"),
                    opt("G = E / (3(1 - 2 nu))"),
                    opt("G = 2 E (1 + nu)"),
                ),
                "G = E / (2(1+nu)); the bulk modulus K = E / (3(1-2nu)).",
            ),
        ),
        "Factor of safety and allowable stress": (
            q(
                "The factor of safety is defined as:",
                (
                    opt("failure stress divided by allowable stress", correct=True),
                    opt("allowable stress divided by failure stress"),
                    opt("load divided by area"),
                    opt("strain divided by stress"),
                ),
                "n = sigma_fail / sigma_allow, so sigma_allow = sigma_fail / n.",
            ),
            q(
                "Increasing the factor of safety, for a fixed material, generally:",
                (
                    opt("lowers the allowable stress and increases member size", correct=True),
                    opt("raises the allowable stress"),
                    opt("has no effect on member size"),
                    opt("reduces the member weight"),
                ),
                "Higher n means lower allowable stress, requiring a larger, heavier member.",
            ),
            q(
                "Modern codes such as AISC LRFD and Eurocode refine the single safety factor by:",
                (
                    opt(
                        "applying separate partial factors to loads and to resistance", correct=True
                    ),
                    opt("ignoring material strength variability"),
                    opt("using only the ultimate strength"),
                    opt("setting the factor of safety to exactly 1"),
                ),
                "LRFD uses separate load and resistance factors rather than one lumped FoS.",
            ),
        ),
    },
    final=(
        q(
            "Stress has units of:",
            (
                opt("pascals (N/m^2)", correct=True),
                opt("newtons"),
                opt("metres"),
                opt("dimensionless"),
            ),
            "Stress is force per unit area, measured in pascals.",
        ),
        q(
            "Strain is:",
            (
                opt("dimensionless", correct=True),
                opt("measured in pascals"),
                opt("measured in newtons"),
                opt("measured in metres squared"),
            ),
            "Normal strain is a ratio of lengths and therefore dimensionless.",
        ),
        q(
            "Young's modulus is the slope of which part of the stress-strain curve?",
            (
                opt("the initial linear-elastic region", correct=True),
                opt("the necking region"),
                opt("the fracture point"),
                opt("the strain-hardening peak"),
            ),
            "E is the slope of the elastic (linear) portion.",
        ),
        q(
            "A material with Poisson's ratio near 0.5 is nearly:",
            (
                opt("incompressible", correct=True),
                opt("infinitely stiff"),
                opt("perfectly brittle"),
                opt("frictionless"),
            ),
            "nu near 0.5 (like rubber) implies almost no volume change.",
        ),
        q(
            "If sigma_y = 300 MPa and the factor of safety is 3, the allowable stress is:",
            (
                opt("100 MPa", correct=True),
                opt("900 MPa"),
                opt("300 MPa"),
                opt("3 MPa"),
            ),
            "sigma_allow = sigma_y / n = 300 / 3 = 100 MPa.",
        ),
        q(
            "The energy absorbed per unit volume up to fracture corresponds to:",
            (
                opt("the area under the stress-strain curve", correct=True),
                opt("the slope of the elastic line"),
                opt("Poisson's ratio"),
                opt("the factor of safety"),
            ),
            "Toughness is the total area under the stress-strain curve.",
        ),
    ),
)
