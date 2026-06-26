"""Quiz questions for the Machine Design & Elements - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The machine design process": (
            q(
                "The machine design process is best described as:",
                (
                    opt(
                        "iterative, cycling between synthesis, analysis and evaluation",
                        correct=True,
                    ),
                    opt("a single forward pass from concept to drawing"),
                    opt("purely analytical with no concept stage"),
                    opt("only about minimizing material cost"),
                ),
                "Design loops repeatedly: synthesise, analyse, evaluate, then iterate.",
            ),
            q(
                "Two threads run through every design loop. They are:",
                (
                    opt("failure prevention and economics", correct=True),
                    opt("painting and packaging"),
                    opt("marketing and branding"),
                    opt("welding and machining only"),
                ),
                "Designers balance whether the part will fail against its mass and cost.",
            ),
            q(
                "Engineering standards (ISO, ASME, AGMA) are used to:",
                (
                    opt(
                        "encode proven practice so safe proportions are not reinvented",
                        correct=True,
                    ),
                    opt("forbid any analysis"),
                    opt("increase the part weight on purpose"),
                    opt("replace the need for a specification"),
                ),
                "Standards capture hard-won practice for bolts, gears, shafts and more.",
            ),
        ),
        "Loads and static stress": (
            q(
                "Bending of a beam produces a stress given by:",
                (
                    opt("sigma = M c / I", correct=True),
                    opt("sigma = F / A only"),
                    opt("tau = T r / J"),
                    opt("sigma = E times strain squared"),
                ),
                "Bending stress is M c / I, largest at the extreme fibre.",
            ),
            q(
                "When several loads act together within linear elasticity, the stresses are:",
                (
                    opt(
                        "superposed at a point, then combined into an equivalent stress",
                        correct=True,
                    ),
                    opt("ignored except the largest one"),
                    opt("multiplied together"),
                    opt("always equal to the yield strength"),
                ),
                "Superposition then a von Mises equivalent stress handles combined loading.",
            ),
            q(
                "The key design insight about loads is that:",
                (
                    opt("stress, not force, is what the material feels", correct=True),
                    opt("force alone determines failure regardless of area"),
                    opt("area never matters"),
                    opt("torsion produces no stress"),
                ),
                "The same force is dangerous in a thin section and safe in a stout one.",
            ),
        ),
        "Factor of safety and the design equation": (
            q(
                "The factor of safety is defined as:",
                (
                    opt("strength divided by the actual stress", correct=True),
                    opt("actual stress divided by strength"),
                    opt("load divided by deflection"),
                    opt("strain divided by stress"),
                ),
                "n = S / sigma, so the allowable stress is S / n.",
            ),
            q(
                "A larger factor of safety generally results in a part that is:",
                (
                    opt("bigger, heavier and more costly", correct=True),
                    opt("smaller and lighter"),
                    opt("identical in size"),
                    opt("guaranteed to be cheaper"),
                ),
                "Higher n lowers allowable stress, demanding more material.",
            ),
            q(
                "Modern codes refine a single lumped factor of safety by:",
                (
                    opt("using separate partial factors on loads and on resistance", correct=True),
                    opt("setting n exactly to 1"),
                    opt("ignoring material scatter"),
                    opt("using only the ultimate strength"),
                ),
                "LRFD applies distinct load and resistance factors.",
            ),
        ),
        "Stress concentration and notches": (
            q(
                "The stress concentration factor Kt relates:",
                (
                    opt("maximum local stress to nominal stress at a discontinuity", correct=True),
                    opt("strength to stress"),
                    opt("strain to stress"),
                    opt("load to deflection"),
                ),
                "sigma_max = Kt * sigma_nom; Kt depends only on geometry.",
            ),
            q(
                "A small hole in a wide plate gives a Kt of about:",
                (
                    opt("3", correct=True),
                    opt("0.3"),
                    opt("1"),
                    opt("100"),
                ),
                "The classic small-hole-in-wide-plate result is Kt close to 3.",
            ),
            q(
                "For a ductile material under static load, the stress concentration is often:",
                (
                    opt("ignored because local yielding redistributes the peak", correct=True),
                    opt("the only thing that matters"),
                    opt("multiplied by 10"),
                    opt("larger for bigger fillet radii"),
                ),
                "Static ductile yielding relieves the peak; fatigue and brittle cases do not.",
            ),
        ),
        "Fluctuating loads and fatigue intuition": (
            q(
                "The stress amplitude of a fluctuating load is:",
                (
                    opt("half the difference between max and min stress", correct=True),
                    opt("the sum of max and min stress"),
                    opt("the mean stress"),
                    opt("the yield strength"),
                ),
                "sigma_a = (sigma_max - sigma_min)/2; sigma_m is the mean.",
            ),
            q(
                "On an S-N curve for steel, the endurance limit is:",
                (
                    opt(
                        "a stress amplitude below which life is effectively infinite", correct=True
                    ),
                    opt("the static yield strength"),
                    opt("the stress at one cycle"),
                    opt("always zero"),
                ),
                "Steels show a flat endurance limit (about half Sut); aluminium does not.",
            ),
            q(
                "The leading cause of in-service mechanical failure is:",
                (
                    opt("fatigue from fluctuating loads", correct=True),
                    opt("a single static overload"),
                    opt("painting defects"),
                    opt("excess stiffness"),
                ),
                "Most failures accumulate fatigue damage below the static strength.",
            ),
        ),
        "Machine elements: shafts, bearings, gears, fasteners": (
            q(
                "Rolling-element bearings are typically selected by their:",
                (
                    opt("rated life such as L10", correct=True),
                    opt("color"),
                    opt("Poisson ratio"),
                    opt("melting point"),
                ),
                "Bearings are chosen from catalogue dynamic ratings and L10 life.",
            ),
            q(
                "Gears are designed against which two failure modes?",
                (
                    opt("tooth bending and surface contact (pitting)", correct=True),
                    opt("buckling and corrosion only"),
                    opt("preload and surge"),
                    opt("hoop and longitudinal stress"),
                ),
                "Spur gears are checked for root bending and Hertzian contact stress.",
            ),
            q(
                "For a solid shaft transmitting torque, the required diameter scales roughly as the:",
                (
                    opt("cube root of the torque", correct=True),
                    opt("square of the torque"),
                    opt("torque to the first power"),
                    opt("inverse of the torque"),
                ),
                "Since tau ~ T/d^3, diameter grows as the cube root of torque.",
            ),
        ),
    },
    final=(
        q(
            "The factor of safety n equals:",
            (
                opt("strength S divided by stress sigma", correct=True),
                opt("stress divided by strength"),
                opt("load times area"),
                opt("strain times modulus"),
            ),
            "n = S / sigma; the allowable stress is S / n.",
        ),
        q(
            "A stress concentration factor Kt of 3 at a hole means the local stress is:",
            (
                opt("three times the nominal stress", correct=True),
                opt("one third of the nominal stress"),
                opt("equal to the nominal stress"),
                opt("zero"),
            ),
            "sigma_max = Kt * sigma_nom, so a tripling at the hole edge.",
        ),
        q(
            "Fatigue failure is driven mainly by the load's:",
            (
                opt("repeated fluctuation over many cycles", correct=True),
                opt("single peak value only"),
                opt("color"),
                opt("static mean with no cycling"),
            ),
            "Cyclic loading accumulates damage even below the static strength.",
        ),
        q(
            "Bending stress in a beam is given by:",
            (
                opt("M c / I", correct=True),
                opt("F / A"),
                opt("T r / J"),
                opt("p r / t"),
            ),
            "Bending stress is M c / I; torsion uses T r / J.",
        ),
        q(
            "Bolted joints carry external load reliably because of:",
            (
                opt("preload that keeps the joint clamped", correct=True),
                opt("the weight of the bolt"),
                opt("painting the threads"),
                opt("removing all clamp force"),
            ),
            "Preload makes the much-stiffer members carry most of the external load.",
        ),
        q(
            "The machine design process is fundamentally:",
            (
                opt("iterative", correct=True),
                opt("a single non-repeating step"),
                opt("free of any analysis"),
                opt("independent of cost"),
            ),
            "Designs loop through synthesis, analysis and evaluation until they meet specs.",
        ),
    ),
)
