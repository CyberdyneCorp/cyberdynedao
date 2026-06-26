"""Quiz questions for the Materials Science & Engineering - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What materials science is": (
            q(
                "The central paradigm of materials science links which factors?",
                (
                    opt("structure, properties, processing and performance", correct=True),
                    opt("price, weight, colour and brand"),
                    opt("voltage, current and resistance"),
                    opt("only chemical composition"),
                ),
                "The structure-property-processing-performance tetrahedron is the field's core idea.",
            ),
            q(
                "Which of these is a ceramic?",
                (
                    opt("alumina (Al2O3)", correct=True),
                    opt("copper"),
                    opt("nylon"),
                    opt("carbon-fibre-reinforced polymer"),
                ),
                "Alumina is an oxide ceramic; copper is a metal, nylon a polymer, CFRP a composite.",
            ),
            q(
                "Why can slow-cooled and quenched steel of the same chemistry differ so much?",
                (
                    opt("different processing changes the internal structure", correct=True),
                    opt("their atomic numbers differ"),
                    opt("Young's modulus is changed by cooling rate"),
                    opt("they are actually different elements"),
                ),
                "Processing (cooling rate) alters the structure, which alters properties like hardness.",
            ),
        ),
        "Atomic bonding": (
            q(
                "Which primary bond involves a shared sea of delocalised electrons?",
                (
                    opt("metallic", correct=True),
                    opt("ionic"),
                    opt("covalent"),
                    opt("van der Waals"),
                ),
                "Metallic bonding has delocalised electrons, giving ductility and conductivity.",
            ),
            q(
                "In an interatomic potential U(r), the equilibrium spacing r0 is where:",
                (
                    opt("U(r) is a minimum (net force is zero)", correct=True),
                    opt("U(r) is maximum"),
                    opt("the repulsion is largest"),
                    opt("r is infinite"),
                ),
                "At r0 the potential is minimum and the net force F = -dU/dr is zero.",
            ),
            q(
                "A deeper, narrower potential well generally means the material is:",
                (
                    opt("stiffer with a higher melting point", correct=True),
                    opt("softer and lower melting"),
                    opt("electrically insulating only"),
                    opt("always ductile"),
                ),
                "Greater curvature at r0 gives higher stiffness (Young's modulus) and melting point.",
            ),
        ),
        "Crystal structures & the unit cell": (
            q(
                "Which structures are close-packed with an atomic packing factor of 0.74?",
                (
                    opt("FCC and HCP", correct=True),
                    opt("BCC and FCC"),
                    opt("BCC only"),
                    opt("simple cubic and BCC"),
                ),
                "FCC and HCP are close-packed at APF 0.74; BCC is 0.68.",
            ),
            q(
                "How many atoms belong to a BCC unit cell?",
                (
                    opt("2", correct=True),
                    opt("1"),
                    opt("4"),
                    opt("6"),
                ),
                "BCC has 8 corner atoms (1/8 each) plus 1 body-centre atom = 2 atoms per cell.",
            ),
            q(
                "Iron transforming from BCC ferrite to FCC austenite on heating is an example of:",
                (
                    opt("polymorphism (allotropy)", correct=True),
                    opt("diffusion-less melting"),
                    opt("a change in atomic number"),
                    opt("corrosion"),
                ),
                "The same element adopting different crystal structures is polymorphism/allotropy.",
            ),
        ),
        "Stress, strain & elasticity": (
            q(
                "Engineering stress is defined as:",
                (
                    opt("force divided by original cross-sectional area, F/A0", correct=True),
                    opt("change in length divided by original length"),
                    opt("force times length"),
                    opt("area divided by force"),
                ),
                "Engineering stress sigma = F/A0; strain is the dimensionless dL/L0.",
            ),
            q(
                "Hooke's law in the elastic regime states:",
                (
                    opt("sigma = E * epsilon", correct=True),
                    opt("sigma = epsilon / E"),
                    opt("epsilon = E * sigma"),
                    opt("E = sigma * epsilon"),
                ),
                "In the linear elastic region stress is proportional to strain: sigma = E*epsilon.",
            ),
            q(
                "Poisson's ratio describes:",
                (
                    opt("transverse contraction relative to axial extension", correct=True),
                    opt("the slope of the elastic line"),
                    opt("the area under the stress-strain curve"),
                    opt("the energy absorbed before fracture"),
                ),
                "Poisson's ratio nu = -lateral strain / axial strain, about 0.3 for metals.",
            ),
        ),
        "The tensile test & mechanical properties": (
            q(
                "Yield strength is conventionally measured using the:",
                (
                    opt("0.2 percent offset method", correct=True),
                    opt("peak of the curve"),
                    opt("fracture point"),
                    opt("initial slope"),
                ),
                "Yield strength is taken at the 0.2 percent plastic-strain offset.",
            ),
            q(
                "Toughness on a stress-strain curve corresponds to:",
                (
                    opt("the area under the whole curve (energy absorbed)", correct=True),
                    opt("the slope of the elastic region"),
                    opt("the maximum stress only"),
                    opt("the strain at yield"),
                ),
                "Toughness is the total energy absorbed before fracture, the area under the curve.",
            ),
            q(
                "Compared with engineering stress, true stress during necking:",
                (
                    opt(
                        "keeps rising because it uses the shrinking instantaneous area",
                        correct=True,
                    ),
                    opt("is always equal to engineering stress"),
                    opt("drops to zero immediately"),
                    opt("is independent of cross-section"),
                ),
                "True stress F/A_instantaneous keeps rising as the neck reduces the area.",
            ),
        ),
    },
    final=(
        q(
            "Which class is bonded by long covalent chains held together by weak secondary bonds?",
            (
                opt("polymers", correct=True),
                opt("metals"),
                opt("ceramics"),
                opt("intermetallics"),
            ),
            "Polymers are long covalent chains with weak van der Waals / hydrogen bonds between them.",
        ),
        q(
            "Young's modulus E is primarily determined by:",
            (
                opt("the stiffness of the atomic bonds (curvature of U(r))", correct=True),
                opt("the grain size"),
                opt("the amount of cold work"),
                opt("the safety factor chosen by the designer"),
            ),
            "E reflects bond stiffness and is barely changed by processing, unlike strength.",
        ),
        q(
            "Which structure typically gives the greatest ductility?",
            (
                opt("FCC, with many slip systems", correct=True),
                opt("HCP, with few slip systems"),
                opt("amorphous glass"),
                opt("simple cubic"),
            ),
            "FCC metals (Al, Cu) have many close-packed slip systems and are very ductile.",
        ),
        q(
            "A material that fractures near its elastic limit with almost no plastic strain is:",
            (
                opt("brittle", correct=True),
                opt("ductile"),
                opt("viscoelastic"),
                opt("superplastic"),
            ),
            "Little or no plastic strain before fracture defines brittle behaviour (e.g. ceramics).",
        ),
        q(
            "The atomic packing factor (APF) measures:",
            (
                opt("the fraction of unit-cell volume filled by atoms", correct=True),
                opt("the number of grains per unit area"),
                opt("the stress at yield"),
                opt("the diffusion coefficient"),
            ),
            "APF = (atoms per cell * atomic volume) / unit-cell volume.",
        ),
        q(
            "Reading a tensile curve, the ultimate tensile strength (UTS) is:",
            (
                opt("the peak stress on the curve", correct=True),
                opt("the stress at 0.2 percent offset"),
                opt("the slope of the elastic region"),
                opt("the strain at fracture"),
            ),
            "UTS is the maximum (peak) engineering stress reached during the test.",
        ),
    ),
)
