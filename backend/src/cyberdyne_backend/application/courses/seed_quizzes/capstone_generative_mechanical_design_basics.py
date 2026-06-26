"""Quiz questions for the Capstone: AI-Optimised Organic Part - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is generative mechanical design?": (
            q(
                "In generative design, what does the engineer mainly specify?",
                (
                    opt("loads, supports, design space and what to minimise", correct=True),
                    opt("the exact final shape feature by feature"),
                    opt("only the material colour"),
                    opt("the printer firmware"),
                ),
                "You provide goals and constraints; the optimizer proposes geometry.",
            ),
            q(
                "What does topology optimization decide?",
                (
                    opt("the best material layout inside a fixed design space", correct=True),
                    opt("the bolt torque sequence"),
                    opt("the print bed temperature"),
                    opt("the supplier of the raw stock"),
                ),
                "Topology optimization finds where material should and should not be.",
            ),
            q(
                "What metric does an optimized part typically improve most?",
                (
                    opt("specific stiffness (stiffness per unit mass)", correct=True),
                    opt("surface gloss"),
                    opt("part colour"),
                    opt("packaging volume"),
                ),
                "Material sits only on load paths, raising stiffness per gram.",
            ),
        ),
        "From brief to requirements and load cases": (
            q(
                "What makes a requirement verifiable?",
                (
                    opt("a number, a unit and a direction (min or max)", correct=True),
                    opt("a vague adjective like 'strong'"),
                    opt("the designer's opinion"),
                    opt("the brand name"),
                ),
                "Verifiable requirements have measurable values you can test against.",
            ),
            q(
                "A load case specifies what?",
                (
                    opt("a combination of forces, moments and supports to survive", correct=True),
                    opt("the colour of the part"),
                    opt("the CAD file format"),
                    opt("the invoice total"),
                ),
                "A load case is a specific load-plus-support scenario the part must meet.",
            ),
            q(
                "For a simple tensile member at constant stress, doubling the force does what to required area?",
                (
                    opt("doubles it, since sigma = F/A", correct=True),
                    opt("halves it"),
                    opt("leaves it unchanged"),
                    opt("quadruples it"),
                ),
                "Stress sigma = F/A, so area scales linearly with force at fixed stress.",
            ),
        ),
        "Stiffness, strength and factor of safety": (
            q(
                "What does stiffness resist?",
                (
                    opt("deformation under load", correct=True),
                    opt("permanent failure only"),
                    opt("corrosion"),
                    opt("heat"),
                ),
                "Stiffness limits deflection; strength resists yielding or fracture.",
            ),
            q(
                "Hooke's law in the elastic region is written as?",
                (
                    opt("sigma = E * eps", correct=True),
                    opt("sigma = F * L"),
                    opt("eps = m * a"),
                    opt("sigma = rho * g"),
                ),
                "Stress equals Young's modulus times strain in the linear-elastic range.",
            ),
            q(
                "Factor of safety against yield is defined as?",
                (
                    opt("yield stress divided by maximum stress", correct=True),
                    opt("maximum stress divided by yield stress"),
                    opt("mass divided by volume"),
                    opt("load divided by area"),
                ),
                "FoS = sigma_y / sigma_max; a value of 2 means half the yield stress is used.",
            ),
        ),
        "Design space, keep-out zones and boundary conditions": (
            q(
                "Which region must the optimizer leave empty?",
                (
                    opt("a keep-out / obstacle region", correct=True),
                    opt("the design space"),
                    opt("a keep-in bolt boss"),
                    opt("the load application point"),
                ),
                "Keep-out zones reserve clearance and must stay void.",
            ),
            q(
                "Boundary conditions define which two things?",
                (
                    opt("where the part is fixed and where loads are applied", correct=True),
                    opt("the colour and the cost"),
                    opt("the slicer and the firmware"),
                    opt("the supplier and the lead time"),
                ),
                "Supports and applied loads anchor the physics of the problem.",
            ),
            q(
                "A common beginner mistake with the design space is?",
                (
                    opt("making it too small, forcing inefficient layouts", correct=True),
                    opt("making it perfectly cubic"),
                    opt("painting it blue"),
                    opt("naming it incorrectly"),
                ),
                "Too little freedom prevents the optimizer from finding light load paths.",
            ),
        ),
        "Why optimized parts look organic": (
            q(
                "Why do optimized parts look bone-like?",
                (
                    opt("material follows principal stress paths to minimise mass", correct=True),
                    opt("designers prefer the aesthetic"),
                    opt("printers can only make curves"),
                    opt("it is a software bug"),
                ),
                "Material is kept only along load paths, matching how nature builds bone.",
            ),
            q(
                "The Michell truss describes what?",
                (
                    opt(
                        "the theoretically lightest structure carrying a load to a support",
                        correct=True,
                    ),
                    opt("a type of welded joint"),
                    opt("a printer calibration pattern"),
                    opt("a fatigue test rig"),
                ),
                "Michell trusses follow principal stress trajectories, like topology results.",
            ),
            q(
                "Why do optimized organic shapes pair well with additive manufacturing?",
                (
                    opt(
                        "hollow, branched geometry is hard to machine but natural to print",
                        correct=True,
                    ),
                    opt("they are always flat plates"),
                    opt("they require no support at all"),
                    opt("they only use metal"),
                ),
                "AM builds complex internal/branched geometry that machining cannot.",
            ),
        ),
        "The capstone arc: brief to printed part": (
            q(
                "What comes immediately after topology optimization in the arc?",
                (
                    opt("generative refinement and smoothing", correct=True),
                    opt("printing the part"),
                    opt("writing the brief"),
                    opt("billing the customer"),
                ),
                "Raw optimized geometry is refined and smoothed before FEA.",
            ),
            q(
                "If FEA validation fails, what happens?",
                (
                    opt(
                        "you loop back to adjust the optimization or problem statement",
                        correct=True,
                    ),
                    opt("you print it anyway"),
                    opt("you delete the project"),
                    opt("you change the part colour"),
                ),
                "Failure sends you back to re-optimize or revise requirements.",
            ),
            q(
                "Optimization output should be treated as?",
                (
                    opt("a candidate that still needs validation and DfAM", correct=True),
                    opt("a finished, ready-to-ship part"),
                    opt("a marketing render only"),
                    opt("an unusable result"),
                ),
                "Candidates almost always need FEA and manufacturability work.",
            ),
        ),
    },
    final=(
        q(
            "What is the core idea of generative / topology optimization?",
            (
                opt("place material only where the load path needs it", correct=True),
                opt("fill the whole design space solid"),
                opt("randomly remove material"),
                opt("copy an existing part"),
            ),
            "It minimises mass while meeting stiffness and strength requirements.",
        ),
        q(
            "Which is a properly framed requirement?",
            (
                opt("max mass <= 180 g", correct=True),
                opt("should be lightweight"),
                opt("looks modern"),
                opt("feels strong"),
            ),
            "Good requirements are measurable with a value, unit and direction.",
        ),
        q(
            "Stiffness and strength differ how?",
            (
                opt("stiffness resists deflection; strength resists failure", correct=True),
                opt("they are identical"),
                opt("stiffness resists corrosion"),
                opt("strength resists deflection only"),
            ),
            "A part can be stiff but weak, or strong but flexible.",
        ),
        q(
            "A factor of safety of 2.0 means?",
            (
                opt("the worst load uses half the yield stress", correct=True),
                opt("the part is twice as heavy"),
                opt("there are two load cases"),
                opt("the cost doubled"),
            ),
            "FoS = sigma_y / sigma_max = 2 implies sigma_max is half of yield.",
        ),
        q(
            "Keep-in (preserve) regions are?",
            (
                opt("geometry that must stay, like bolt bosses and seats", correct=True),
                opt("volumes that must be empty"),
                opt("the optimizer's scratch space"),
                opt("printer support material"),
            ),
            "Preserve regions are frozen and not removed by the optimizer.",
        ),
        q(
            "Why does the optimized-part workflow include a loop back from FEA?",
            (
                opt("validation often reveals the problem statement must be revised", correct=True),
                opt("FEA always passes first time"),
                opt("printers require it"),
                opt("to slow the project down"),
            ),
            "Iterating the brief, loads and design space is the real engineering.",
        ),
    ),
)
