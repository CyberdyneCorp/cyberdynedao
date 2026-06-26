"""Quiz questions for the Generative Design & AI for CAD - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is generative design?": (
            q(
                "What does the engineer specify in a generative-design workflow?",
                (
                    opt("the goals, loads, supports and constraints (the what)", correct=True),
                    opt("the exact final geometry by hand"),
                    opt("the toolpaths for the CNC machine"),
                    opt("only the colour and finish"),
                ),
                "The engineer states what must be true; the algorithm searches for a how.",
            ),
            q(
                "A defining feature of a generative-design run is that it produces:",
                (
                    opt("many candidate designs to compare", correct=True),
                    opt("exactly one final design"),
                    opt("a 2D drawing only"),
                    opt("a bill of materials only"),
                ),
                "One run returns a portfolio of candidates with different trade-offs.",
            ),
            q(
                "Generative design pays off most when the design problem is:",
                (
                    opt("complex and hard to intuit by hand", correct=True),
                    opt("trivially simple"),
                    opt("already fully solved"),
                    opt("purely aesthetic"),
                ),
                "For complex multi-load problems the search reaches places intuition cannot.",
            ),
        ),
        "Goals, constraints and the design space": (
            q(
                "Which three ingredients define a generative (optimization) problem?",
                (
                    opt("design variables, objectives and constraints", correct=True),
                    opt("colour, weight and price"),
                    opt("mesh, solver and post-processor"),
                    opt("sketch, extrude and fillet"),
                ),
                "Generative design is an optimization problem: variables, objectives, constraints.",
            ),
            q(
                "A preserve (keep) region is geometry that the algorithm:",
                (
                    opt("must not change - bolt bosses, bearing seats, mating faces", correct=True),
                    opt("is free to delete entirely"),
                    opt("must always fill with a lattice"),
                    opt("uses only for colour"),
                ),
                "Keep regions are mandatory geometry; keep-out regions forbid material.",
            ),
            q(
                "Adding more active constraints to a problem generally:",
                (
                    opt("shrinks the feasible fraction of the design space", correct=True),
                    opt("enlarges the feasible region"),
                    opt("has no effect on feasibility"),
                    opt("guarantees a lighter design"),
                ),
                "Each constraint removes designs that no longer qualify.",
            ),
        ),
        "Generative design vs topology optimization": (
            q(
                "How does generative design differ from topology optimization?",
                (
                    opt("it sweeps many materials/methods and returns a portfolio", correct=True),
                    opt("it ignores physics entirely"),
                    opt("it only works in 2D"),
                    opt("it returns exactly one layout for one load case"),
                ),
                "Topology optimization is the solver; generative design is the workflow around it.",
            ),
            q(
                "The compliance C = U^T K U that both methods minimize is a measure of:",
                (
                    opt("flexibility - lower compliance means stiffer", correct=True),
                    opt("mass density"),
                    opt("surface roughness"),
                    opt("electrical resistance"),
                ),
                "Minimizing compliance is equivalent to maximizing stiffness.",
            ),
            q(
                "As the allowed material volume fraction increases, achievable compliance:",
                (
                    opt("decreases - the part gets stiffer but heavier", correct=True),
                    opt("increases without limit"),
                    opt("stays exactly constant"),
                    opt("becomes negative"),
                ),
                "More material lowers compliance (raises stiffness) at the cost of mass.",
            ),
        ),
        "How the generative engine iterates": (
            q(
                "What does the engine do inside each iteration of its loop?",
                (
                    opt("simulate with FEA, score, then update the material field", correct=True),
                    opt("randomly recolour the part"),
                    opt("export a drawing"),
                    opt("ask the user to redraw"),
                ),
                "Propose, FEA-solve, score against goals/constraints, update, repeat.",
            ),
            q(
                "A typical objective-vs-iteration curve for a healthy run:",
                (
                    opt("falls quickly then flattens as it converges", correct=True),
                    opt("rises steadily forever"),
                    opt("oscillates with growing amplitude"),
                    opt("stays flat from the first iteration"),
                ),
                "Convergence shows fast early improvement that levels off near the optimum.",
            ),
            q(
                "A common stopping rule ends the run when:",
                (
                    opt(
                        "the relative change in the objective drops below a tolerance", correct=True
                    ),
                    opt("the part turns blue"),
                    opt("the mesh is deleted"),
                    opt("the user presses undo"),
                ),
                "Stop when successive objectives stop improving by more than the tolerance.",
            ),
        ),
        "Manufacturing constraints shape the result": (
            q(
                "Why fold the manufacturing method into the generative search?",
                (
                    opt("so every candidate is actually buildable", correct=True),
                    opt("to make the run faster only"),
                    opt("to change the material colour"),
                    opt("it has no effect on geometry"),
                ),
                "Different processes (additive, milling, casting) yield different buildable shapes.",
            ),
            q(
                "Die casting imposes which characteristic requirement on geometry?",
                (
                    opt("draft angles and fairly uniform wall thickness", correct=True),
                    opt("dense internal lattices"),
                    opt("zero-radius internal corners"),
                    opt("unsupported overhangs everywhere"),
                ),
                "Draft and uniform walls allow ejection and even cooling in casting.",
            ),
            q(
                "Relative to a freely optimized additive shape, a casting/milling-constrained part is usually:",
                (
                    opt("heavier for the same stiffness target", correct=True),
                    opt("always lighter"),
                    opt("identical in mass"),
                    opt("impossible to simulate"),
                ),
                "Process restrictions force extra material, raising mass for the same performance.",
            ),
        ),
        "Reading and comparing candidates": (
            q(
                "A candidate is Pareto-optimal (non-dominated) when:",
                (
                    opt(
                        "no other candidate is better in one objective without being worse in another",
                        correct=True,
                    ),
                    opt("it has the lowest mass only"),
                    opt("it was generated first"),
                    opt("it uses the most material"),
                ),
                "Non-dominated designs form the trade-off frontier of good choices.",
            ),
            q(
                "The safety factor is computed as:",
                (
                    opt("yield stress divided by peak stress", correct=True),
                    opt("peak stress divided by mass"),
                    opt("mass divided by volume"),
                    opt("displacement times stiffness"),
                ),
                "SF = yield / peak; a value above 1 (often >= 1.5) means it survives with margin.",
            ),
            q(
                "When comparing candidates, why is a single ranking number insufficient?",
                (
                    opt("objectives conflict, so trade-offs must be weighed", correct=True),
                    opt("all candidates are identical"),
                    opt("metrics are never measurable"),
                    opt("the engine forbids comparison"),
                ),
                "Mass, stiffness and cost compete; the Pareto view exposes the trade-offs.",
            ),
        ),
    },
    final=(
        q(
            "Generative design is best described as:",
            (
                opt(
                    "stating goals/constraints and letting an algorithm propose geometry",
                    correct=True,
                ),
                opt("drawing a shape then checking it"),
                opt("machining a billet by hand"),
                opt("choosing a colour scheme"),
            ),
            "You specify what must be true; the computer searches for how.",
        ),
        q(
            "Topology optimization, relative to generative design, is:",
            (
                opt("the underlying solver for one well-posed problem", correct=True),
                opt("a broader workflow over many materials and methods"),
                opt("unrelated to compliance"),
                opt("a drawing tool"),
            ),
            "Generative design wraps topology optimization in a multi-objective workflow.",
        ),
        q(
            "Compliance C = U^T K U is minimized in order to:",
            (
                opt("maximize stiffness", correct=True),
                opt("maximize mass"),
                opt("increase surface roughness"),
                opt("raise the temperature"),
            ),
            "Lower compliance means a stiffer structure.",
        ),
        q(
            "A keep-out (obstacle) region tells the engine that material is:",
            (
                opt("forbidden there - clearance must be kept", correct=True),
                opt("mandatory there"),
                opt("optional and ignored"),
                opt("doubled there"),
            ),
            "Keep-out regions reserve clearance; preserve regions are mandatory geometry.",
        ),
        q(
            "Choosing casting over additive manufacturing for the same problem tends to:",
            (
                opt("add mass because of draft and wall-thickness rules", correct=True),
                opt("always reduce mass"),
                opt("remove all constraints"),
                opt("make simulation unnecessary"),
            ),
            "Manufacturing constraints cost performance; casting forces extra material.",
        ),
        q(
            "The right way to pick a final candidate from a generative run is to:",
            (
                opt(
                    "screen on constraints, then choose from the Pareto front by priorities",
                    correct=True,
                ),
                opt("always pick the first one generated"),
                opt("pick the heaviest design"),
                opt("ignore the safety factor"),
            ),
            "Filter infeasible designs, then weigh trade-offs on the non-dominated set.",
        ),
    ),
)
