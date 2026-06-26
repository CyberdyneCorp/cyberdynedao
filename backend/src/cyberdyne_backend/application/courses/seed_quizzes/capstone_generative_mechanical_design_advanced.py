"""Quiz questions for the Capstone: AI-Optimised Organic Part - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Multi-load-case and stress-constrained optimization": (
            q(
                "How are multiple load cases handled in stiffness optimization?",
                (
                    opt("a weighted sum of each case's compliance", correct=True),
                    opt("optimize only the lightest case"),
                    opt("ignore all but one case"),
                    opt("average the geometries"),
                ),
                "Weighted compliance with sum of weights = 1 balances the cases.",
            ),
            q(
                "Why is stress-constrained topology optimization hard?",
                (
                    opt(
                        "stress is local, singular at low density, and highly non-linear",
                        correct=True,
                    ),
                    opt("stress is trivial to compute"),
                    opt("there is only one constraint"),
                    opt("it needs no FEA"),
                ),
                "Local, singular, non-linear stress makes the problem ill-behaved.",
            ),
            q(
                "What is the purpose of a p-norm or KS aggregation of stresses?",
                (
                    opt("collapse many local constraints into a smooth global one", correct=True),
                    opt("increase the number of constraints"),
                    opt("remove the volume constraint"),
                    opt("speed up printing"),
                ),
                "Aggregation approximates the max stress for tractable gradients.",
            ),
        ),
        "Machine-learning surrogates for the design loop": (
            q(
                "What does a surrogate model learn?",
                (
                    opt("the map from design parameters to performance responses", correct=True),
                    opt("the printer firmware"),
                    opt("the invoice total"),
                    opt("the room temperature"),
                ),
                "It predicts compliance/stress/mass fast, replacing slow FEA.",
            ),
            q(
                "Why are Gaussian-process surrogates useful in Bayesian optimization?",
                (
                    opt("they provide uncertainty used by the acquisition function", correct=True),
                    opt("they need no data"),
                    opt("they only work in 1D"),
                    opt("they require no validation"),
                ),
                "Predicted mean plus uncertainty guides where to sample next.",
            ),
            q(
                "A confident-but-wrong surrogate is avoided by?",
                (
                    opt("validating and confirming the chosen design on real FEA", correct=True),
                    opt("trusting it without checks"),
                    opt("training on a single point"),
                    opt("removing the test set"),
                ),
                "Hold-out validation plus a final high-fidelity check guards against it.",
            ),
        ),
        "Generative neural methods for geometry": (
            q(
                "What do deep-generative models output in this context?",
                (
                    opt("candidate geometry conditioned on loads and constraints", correct=True),
                    opt("the final G-code only"),
                    opt("a bill of materials"),
                    opt("a printer driver"),
                ),
                "They propose density fields/shapes from conditioning inputs.",
            ),
            q(
                "Optimizing inside a VAE latent space turns shape search into?",
                (
                    opt("low-dimensional continuous search", correct=True),
                    opt("a discrete combinatorial explosion"),
                    opt("a manual sketching task"),
                    opt("a slicing problem"),
                ),
                "A smooth latent space lets you optimize a few continuous variables.",
            ),
            q(
                "Why must every generative candidate still be checked by FEA?",
                (
                    opt("the output is a prior, not a guarantee of feasibility", correct=True),
                    opt("FEA is faster than the model"),
                    opt("the model is always wrong"),
                    opt("printers require it"),
                ),
                "Generated geometry can violate equilibrium or stress limits.",
            ),
        ),
        "Lattice infill and multiscale design": (
            q(
                "Lattice cell stiffness vs relative density follows which law?",
                (
                    opt("a Gibson-Ashby power law E*/Es = C*(rho)^n", correct=True),
                    opt("a linear law independent of density"),
                    opt("Hooke's law for water"),
                    opt("the ideal gas law"),
                ),
                "Cellular-solid scaling: modulus scales as a power of relative density.",
            ),
            q(
                "Which cell type is stiffer per gram?",
                (
                    opt("stretch-dominated (n ~ 1)", correct=True),
                    opt("bending-dominated (n ~ 2)"),
                    opt("they are identical"),
                    opt("neither carries load"),
                ),
                "Stretch-dominated cells (octet truss) give stiffness ~ linear in density.",
            ),
            q(
                "Why are TPMS (gyroid) lattices attractive for additive manufacturing?",
                (
                    opt("smooth, self-supporting, no stress-concentrating nodes", correct=True),
                    opt("they need maximum supports"),
                    opt("they trap powder by design"),
                    opt("they can only be machined"),
                ),
                "Minimal surfaces are smooth, self-supporting and easy to grade.",
            ),
        ),
        "Design for additive manufacturing constraints": (
            q(
                "Surfaces shallower than the self-support angle (~45 deg) need?",
                (
                    opt("support structures or a redesign", correct=True),
                    opt("no action"),
                    opt("a larger keep-out only"),
                    opt("a colour change"),
                ),
                "Steep overhangs cannot self-support in powder-bed fusion.",
            ),
            q(
                "Layer-by-layer building makes the build (Z) direction?",
                (
                    opt("weaker, so FEA should use orthotropic properties", correct=True),
                    opt("stronger than all others"),
                    opt("perfectly isotropic"),
                    opt("irrelevant to strength"),
                ),
                "Inter-layer bonding causes anisotropy; the Z direction is weakest.",
            ),
            q(
                "Closed internal voids in a printed part require?",
                (
                    opt("drain holes to remove trapped powder or resin", correct=True),
                    opt("extra paint"),
                    opt("a thicker box"),
                    opt("no consideration"),
                ),
                "Trapped powder/resin must escape, hence drain holes or lattices.",
            ),
        ),
        "Verification of the final printed part": (
            q(
                "Why use a CT scan during verification?",
                (
                    opt("to detect internal porosity that lowers fatigue life", correct=True),
                    opt("to choose the colour"),
                    opt("to slice the model"),
                    opt("to set the bolt torque"),
                ),
                "CT reveals lack-of-fusion voids that hurt fatigue performance.",
            ),
            q(
                "Comparing measured stiffness to FEA serves to?",
                (
                    opt("validate the simulation model, not only the part", correct=True),
                    opt("set the print speed"),
                    opt("pick the supplier"),
                    opt("decide the colour"),
                ),
                "A stiffness gap exposes wrong material data or modelling error.",
            ),
            q(
                "As-built additive surfaces affect fatigue how?",
                (
                    opt("rough surfaces lower the S-N curve unless finished/HIP'd", correct=True),
                    opt("they always improve fatigue"),
                    opt("they have no effect"),
                    opt("they eliminate cyclic loads"),
                ),
                "Surface roughness reduces fatigue strength versus machined surfaces.",
            ),
        ),
    },
    final=(
        q(
            "Multiple load cases are typically combined into the objective via?",
            (
                opt("a weighted sum of compliances", correct=True),
                opt("the single heaviest geometry"),
                opt("ignoring the worst case"),
                opt("a random pick"),
            ),
            "Weighted compliance balances stiffness across all scenarios.",
        ),
        q(
            "The main benefit of an ML surrogate in the design loop is?",
            (
                opt("millisecond predictions that replace slow FEA for exploration", correct=True),
                opt("guaranteed exact stresses"),
                opt("no need for any data"),
                opt("eliminating the need to print"),
            ),
            "Surrogates accelerate search; the best design is confirmed on real FEA.",
        ),
        q(
            "Generative neural geometry should be regarded as?",
            (
                opt("a fast, diverse prior that still needs FEA verification", correct=True),
                opt("a final guaranteed-feasible part"),
                opt("useless output"),
                opt("a replacement for the brief"),
            ),
            "Its value is speed and diversity, not correctness.",
        ),
        q(
            "To get the most stiffness per gram from a lattice you choose?",
            (
                opt("stretch-dominated cells graded by the macro density field", correct=True),
                opt("bending-dominated cells at uniform density"),
                opt("solid bulk everywhere"),
                opt("random struts"),
            ),
            "Stretch-dominated, density-graded lattices put stiffness on the load path.",
        ),
        q(
            "Which DfAM concern is unique to layer-based metal printing?",
            (
                opt("residual stress and distortion from thermal gradients", correct=True),
                opt("excessive part colour saturation"),
                opt("too few bolt holes"),
                opt("oversized packaging"),
            ),
            "Fast thermal cycling builds residual stress, managed by orientation/supports.",
        ),
        q(
            "Final sign-off of the printed part requires?",
            (
                opt(
                    "dimensional, internal (CT) and mechanical checks against the brief",
                    correct=True,
                ),
                opt("only a visual glance"),
                opt("trusting the FEA alone"),
                opt("matching the render colour"),
            ),
            "Physical verification closes the loop; simulation alone is insufficient.",
        ),
    ),
)
