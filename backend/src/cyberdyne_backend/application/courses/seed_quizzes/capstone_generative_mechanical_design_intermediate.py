"""Quiz questions for the Capstone: AI-Optimised Organic Part - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The compliance minimisation problem": (
            q(
                "Minimising compliance is equivalent to?",
                (
                    opt("maximising global stiffness", correct=True),
                    opt("maximising mass"),
                    opt("maximising deflection"),
                    opt("minimising the build envelope"),
                ),
                "Compliance is the work done by loads, the inverse of stiffness.",
            ),
            q(
                "In the SIMP setup, the design variables are?",
                (
                    opt("element densities x_e between 0 and 1", correct=True),
                    opt("nodal temperatures"),
                    opt("bolt torques"),
                    opt("layer heights"),
                ),
                "Each element carries a density from void (0) to solid (1).",
            ),
            q(
                "The constraint K*U = F in the problem represents?",
                (
                    opt("static equilibrium solved by FEA each iteration", correct=True),
                    opt("the volume constraint"),
                    opt("the move limit"),
                    opt("the filter radius"),
                ),
                "It is the equilibrium FEA solve linking densities to displacements.",
            ),
        ),
        "SIMP: penalising intermediate densities": (
            q(
                "What does the SIMP penalty exponent p (>= 3) achieve?",
                (
                    opt("makes intermediate (grey) densities stiffness-inefficient", correct=True),
                    opt("makes solid material heavier"),
                    opt("removes the volume constraint"),
                    opt("speeds up FEA solving"),
                ),
                "Penalising grey material pushes the design toward crisp 0/1 layouts.",
            ),
            q(
                "With p = 3, half-dense material gives roughly what fraction of solid stiffness?",
                (
                    opt("about 0.125 (0.5 cubed)", correct=True),
                    opt("about 0.5"),
                    opt("about 0.9"),
                    opt("exactly 1.0"),
                ),
                "E scales with x^p, so 0.5^3 = 0.125 of full stiffness.",
            ),
            q(
                "The compliance sensitivity dc/dx_e under SIMP is?",
                (
                    opt("always negative (adding material lowers compliance)", correct=True),
                    opt("always positive"),
                    opt("always zero"),
                    opt("undefined"),
                ),
                "Adding material can only reduce compliance, so the sensitivity is <= 0.",
            ),
        ),
        "Optimality criteria and density filtering": (
            q(
                "The optimality-criteria update is derived from?",
                (
                    opt("the KKT optimality conditions", correct=True),
                    opt("random sampling"),
                    opt("the slicer settings"),
                    opt("Newton's second law"),
                ),
                "OC is a fixed-point update from the problem's KKT conditions.",
            ),
            q(
                "How is the Lagrange multiplier lambda found in the OC update?",
                (
                    opt("bisection so the volume constraint is satisfied", correct=True),
                    opt("by training a neural net"),
                    opt("set to a fixed constant forever"),
                    opt("by random guessing"),
                ),
                "A bisection on lambda enforces the target volume fraction.",
            ),
            q(
                "What numerical pathologies does a filter with radius r_min cure?",
                (
                    opt("checkerboarding and mesh dependence", correct=True),
                    opt("rounding errors in printing"),
                    opt("slow disk access"),
                    opt("colour banding"),
                ),
                "Filtering imposes a minimum feature size, removing both artefacts.",
            ),
        ),
        "Linear static FEA for validation": (
            q(
                "Linear static FEA solves which system?",
                (
                    opt("K*U = F for nodal displacements", correct=True),
                    opt("M*a = F for accelerations"),
                    opt("dT/dt = alpha*lap(T)"),
                    opt("PV = nRT"),
                ),
                "The global stiffness times displacements equals the load vector.",
            ),
            q(
                "Which assumption must hold for linear static FEA to be valid?",
                (
                    opt("linear elasticity and small deflections", correct=True),
                    opt("large plastic deformation"),
                    opt("transient impact loading"),
                    opt("fluid turbulence"),
                ),
                "Linearity and small strains are core assumptions of the method.",
            ),
            q(
                "For a single axial bar, the hand check on tip deflection is?",
                (
                    opt("delta = P*L/(A*E)", correct=True),
                    opt("delta = E/(P*L)"),
                    opt("delta = A*E/(P*L)"),
                    opt("delta = P*A*E"),
                ),
                "Axial extension is delta = PL/(AE); it validates the FEA model.",
            ),
        ),
        "Mesh convergence and discretisation error": (
            q(
                "A coarse mesh tends to do what to stress predictions?",
                (
                    opt("under-predict peak stress (too stiff)", correct=True),
                    opt("over-predict peak stress wildly"),
                    opt("predict stress exactly"),
                    opt("ignore stress entirely"),
                ),
                "Coarse meshes are artificially stiff and miss steep gradients.",
            ),
            q(
                "A mesh convergence study refines the mesh until?",
                (
                    opt("the quantity of interest changes less than a tolerance", correct=True),
                    opt("the file size doubles"),
                    opt("the colour stabilises"),
                    opt("the part is printed"),
                ),
                "You stop when successive refinements change results below tolerance.",
            ),
            q(
                "At a sharp re-entrant corner the FEA stress will?",
                (
                    opt("not converge (a singularity); round the corner", correct=True),
                    opt("converge fastest"),
                    opt("equal zero"),
                    opt("equal the yield stress exactly"),
                ),
                "Sharp corners create stress singularities; fillet or interpret carefully.",
            ),
        ),
        "Stress criteria and factor of safety in FEA": (
            q(
                "Which scalar criterion predicts yielding of ductile metals?",
                (
                    opt("von Mises (distortion-energy) stress", correct=True),
                    opt("hydrostatic pressure only"),
                    opt("the trace of the strain tensor"),
                    opt("the mass density"),
                ),
                "Von Mises stress collapses the tensor into a yield indicator.",
            ),
            q(
                "Yielding is predicted when?",
                (
                    opt("von Mises stress reaches the yield stress", correct=True),
                    opt("density reaches zero"),
                    opt("displacement reaches zero"),
                    opt("temperature reaches melting"),
                ),
                "sigma_v >= sigma_y signals onset of plastic yielding.",
            ),
            q(
                "How do you report safety across multiple load cases?",
                (
                    opt("take the minimum factor of safety over all cases", correct=True),
                    opt("average all the stresses"),
                    opt("use only the first case"),
                    opt("ignore the worst case"),
                ),
                "The governing margin is the lowest FoS found anywhere, any case.",
            ),
        ),
    },
    final=(
        q(
            "The stiffness topology problem minimises compliance subject to?",
            (
                opt("equilibrium and a volume-fraction constraint", correct=True),
                opt("a fixed colour"),
                opt("maximum mass"),
                opt("a fixed print time"),
            ),
            "Minimise U^T K U with K*U = F and V/V0 <= f.",
        ),
        q(
            "SIMP makes the discrete topology problem tractable by?",
            (
                opt("relaxing to continuous densities with a penalty exponent", correct=True),
                opt("printing every candidate"),
                opt("removing all constraints"),
                opt("using random search"),
            ),
            "Continuous x_e with E ~ x^p yields a differentiable, near-0/1 problem.",
        ),
        q(
            "The optimality-criteria loop combines an OC update with?",
            (
                opt("a density/sensitivity filter for minimum feature size", correct=True),
                opt("a random shuffle"),
                opt("a neural network only"),
                opt("no FEA at all"),
            ),
            "Filtering prevents checkerboarding and mesh dependence.",
        ),
        q(
            "Before trusting a complex FEA result you should?",
            (
                opt("validate against a closed-form hand calculation", correct=True),
                opt("trust the first mesh always"),
                opt("skip boundary conditions"),
                opt("use the coarsest mesh"),
            ),
            "Hand checks like delta = PL/(AE) confirm the model setup.",
        ),
        q(
            "Quadratic elements are preferred because they?",
            (
                opt("converge faster and avoid shear locking", correct=True),
                opt("are always cheaper than linear"),
                opt("never need refinement"),
                opt("eliminate all error"),
            ),
            "Higher-order elements reach accuracy at fewer nodes.",
        ),
        q(
            "The governing safety result for a validated part is?",
            (
                opt("the minimum von Mises factor of safety across all load cases", correct=True),
                opt("the average deflection"),
                opt("the total mass"),
                opt("the maximum density"),
            ),
            "You require the worst-case min FoS to clear the brief.",
        ),
    ),
)
