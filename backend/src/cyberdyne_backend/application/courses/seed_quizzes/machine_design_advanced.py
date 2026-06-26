"""Quiz questions for the Machine Design & Elements - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Helical compression spring design": (
            q(
                "The rate (stiffness) of a helical spring depends most strongly on:",
                (
                    opt("the wire diameter to the fourth power", correct=True),
                    opt("the wire diameter to the first power"),
                    opt("the number of coils squared"),
                    opt("the free length only"),
                ),
                "k = G d^4 / (8 D^3 Na), so k scales with d^4.",
            ),
            q(
                "The Wahl factor corrects the spring shear stress for:",
                (
                    opt("coil curvature and direct shear at the inner coil", correct=True),
                    opt("temperature effects"),
                    opt("the number of active coils"),
                    opt("surface finish"),
                ),
                "Kw accounts for curvature and transverse shear, peaking at the inner fibre.",
            ),
            q(
                "Spring surge refers to:",
                (
                    opt("resonance of the coil treated as a wave medium", correct=True),
                    opt("buckling under axial load"),
                    opt("corrosion of the wire"),
                    opt("loss of preload in a bolt"),
                ),
                "Surge is dynamic resonance; the natural frequency is kept above forcing.",
            ),
        ),
        "Fatigue of welded joints": (
            q(
                "Fatigue cracks in welded joints usually start at the:",
                (
                    opt("weld toe, a sharp notch with residual tensile stress", correct=True),
                    opt("center of the base metal"),
                    opt("bolt head"),
                    opt("painted surface"),
                ),
                "The weld toe combines a notch, defects and residual tension.",
            ),
            q(
                "A FAT class in weld fatigue codes is the:",
                (
                    opt("stress range giving 2e6 cycles for that detail", correct=True),
                    opt("yield strength of the filler metal"),
                    opt("preload of the joint"),
                    opt("bearing dynamic rating"),
                ),
                "The FAT number is the detail's stress range at 2 million cycles.",
            ),
            q(
                "Post-weld treatments such as toe grinding or HFMI peening improve life by:",
                (
                    opt("blunting the notch and adding compressive residual stress", correct=True),
                    opt("increasing the residual tensile stress"),
                    opt("sharpening the weld toe"),
                    opt("removing all base metal"),
                ),
                "They reduce the local stress concentration and introduce compression.",
            ),
        ),
        "Fracture mechanics and damage tolerance": (
            q(
                "The stress intensity factor K is given by:",
                (
                    opt("Y sigma sqrt(pi a)", correct=True),
                    opt("sigma / a"),
                    opt("E times strain"),
                    opt("M c / I"),
                ),
                "K = Y sigma sqrt(pi a); fracture occurs when K reaches KIc.",
            ),
            q(
                "Unstable fracture occurs when K reaches the material's:",
                (
                    opt("fracture toughness KIc", correct=True),
                    opt("yield strength"),
                    opt("endurance limit"),
                    opt("Young's modulus"),
                ),
                "When K = KIc the crack runs unstably, defining the critical crack size.",
            ),
            q(
                "Paris' law describes:",
                (
                    opt("sub-critical fatigue crack growth rate da/dN vs delta-K", correct=True),
                    opt("static yield under load"),
                    opt("bearing life vs load"),
                    opt("spring rate vs coils"),
                ),
                "da/dN = C (delta K)^m governs stable crack growth per cycle.",
            ),
        ),
        "Reliability-based design": (
            q(
                "In reliability-based design, failure is defined as the event:",
                (
                    opt("strength is less than the load stress", correct=True),
                    opt("strength equals the modulus"),
                    opt("the factor of safety is exactly 3"),
                    opt("deflection equals zero"),
                ),
                "Failure occurs in the stress-strength interference region where Sigma < S.",
            ),
            q(
                "The reliability index beta is largest when:",
                (
                    opt("the means are far apart and the scatter is small", correct=True),
                    opt("the distributions overlap completely"),
                    opt("the standard deviations are very large"),
                    opt("the mean strength equals the mean load"),
                ),
                "beta = (mu_str - mu_load)/sqrt(var sum); larger margin and less scatter raise it.",
            ),
            q(
                "Reducing scatter (tighter tolerances, better material control):",
                (
                    opt("can raise reliability without adding mass", correct=True),
                    opt("always requires a heavier part"),
                    opt("has no effect on reliability"),
                    opt("lowers the reliability index"),
                ),
                "Shrinking the distributions reduces overlap, often more cheaply than mass.",
            ),
        ),
        "Design optimization": (
            q(
                "A machine design optimization problem minimizes an objective subject to:",
                (
                    opt("constraints such as stress, deflection and geometry", correct=True),
                    opt("no constraints at all"),
                    opt("only the color of the part"),
                    opt("a fixed number of iterations"),
                ),
                "min f(x) s.t. g_i(x) <= 0 and variable bounds.",
            ),
            q(
                "For smooth, single-mode minimum-mass problems, a good solver is:",
                (
                    opt("a gradient-based method such as SQP", correct=True),
                    opt("random guessing only"),
                    opt("no method works"),
                    opt("a fixed lookup table"),
                ),
                "SQP converges quickly; multimodal/discrete problems use GA or PSO.",
            ),
            q(
                "Topology optimization (SIMP) is used to:",
                (
                    opt(
                        "grow material only where load flows, enabling generative designs",
                        correct=True,
                    ),
                    opt("remove all constraints"),
                    opt("fix the geometry permanently"),
                    opt("increase the part mass"),
                ),
                "SIMP distributes material by element density, ideal for additive manufacturing.",
            ),
        ),
        "Digital twins and ML for predictive maintenance": (
            q(
                "A digital twin is best described as:",
                (
                    opt(
                        "a calibrated model fed live sensor data to estimate the part's state",
                        correct=True,
                    ),
                    opt("a second physical copy of the machine"),
                    opt("a paper drawing"),
                    opt("a static catalogue table"),
                ),
                "It couples physics/surrogate models with real-time data for state and RUL.",
            ),
            q(
                "Palmgren-Miner's rule accumulates fatigue damage as:",
                (
                    opt("the sum of n_i / N_i over load blocks, failing at 1", correct=True),
                    opt("the product of all stresses"),
                    opt("the square root of cycles"),
                    opt("the ratio C/P"),
                ),
                "D = sum(n_i/N_i); failure is predicted when D reaches 1.",
            ),
            q(
                "An ML surrogate is used in this workflow to:",
                (
                    opt("predict stress in real time faster than full FEA", correct=True),
                    opt("replace all sensors"),
                    opt("eliminate the damage model"),
                    opt("increase the load on the part"),
                ),
                "A surrogate trained on FEA/test data gives fast stress estimates for monitoring.",
            ),
        ),
    },
    final=(
        q(
            "A helical spring's rate scales with the wire diameter as:",
            (
                opt("d to the fourth power", correct=True),
                opt("d to the first power"),
                opt("d squared"),
                opt("1/d"),
            ),
            "k = G d^4 / (8 D^3 Na).",
        ),
        q(
            "Welded-joint fatigue is governed primarily by the:",
            (
                opt("stress range at the weld toe and the detail's FAT class", correct=True),
                opt("base-metal ultimate strength alone"),
                opt("bolt preload"),
                opt("spring surge frequency"),
            ),
            "The toe notch and FAT-class S-N curve control weld fatigue life.",
        ),
        q(
            "The critical crack size is reached when the stress intensity factor equals:",
            (
                opt("the fracture toughness KIc", correct=True),
                opt("the endurance limit"),
                opt("the yield strength"),
                opt("zero"),
            ),
            "a_c follows from K = Y sigma sqrt(pi a) = KIc.",
        ),
        q(
            "The reliability index beta increases when:",
            (
                opt("the safety margin grows and the scatter shrinks", correct=True),
                opt("the distributions overlap more"),
                opt("the standard deviations increase"),
                opt("the mean load exceeds the mean strength"),
            ),
            "beta = (mu_str - mu_load)/sqrt(variance sum).",
        ),
        q(
            "A constrained design optimization is written as:",
            (
                opt("minimize f(x) subject to g_i(x) <= 0 and bounds", correct=True),
                opt("maximize the mass with no constraints"),
                opt("minimize iterations only"),
                opt("ignore all constraints"),
            ),
            "Objective minimization under inequality constraints and variable bounds.",
        ),
        q(
            "In predictive maintenance, remaining useful life is estimated by combining sensor data with a:",
            (
                opt("damage model such as Miner's rule or Paris' law", correct=True),
                opt("paper drawing"),
                opt("fixed factor of safety only"),
                opt("bearing color chart"),
            ),
            "Measured load history feeds a damage model to compute accumulated damage and RUL.",
        ),
    ),
)
