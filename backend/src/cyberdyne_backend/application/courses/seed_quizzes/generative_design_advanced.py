"""Quiz questions for the Generative Design & AI for CAD - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Deep generative models of geometry": (
            q(
                "Unlike classical topology optimization, a deep generative model:",
                (
                    opt("learns a distribution over geometry and samples new shapes", correct=True),
                    opt("solves one PDE exactly"),
                    opt("requires no data"),
                    opt("only produces 2D drawings"),
                ),
                "Trained on a corpus, it maps a latent vector to plausible new shapes.",
            ),
            q(
                "Which model family is currently state of the art for fidelity and diversity, underpinning text-to-3D?",
                (
                    opt("diffusion models", correct=True),
                    opt("linear regression"),
                    opt("k-means clustering"),
                    opt("decision stumps"),
                ),
                "Diffusion models learn to denoise and lead in generative fidelity.",
            ),
            q(
                "As the latent dimension grows, reconstruction error tends to fall but:",
                (
                    opt("the latent space becomes harder to search", correct=True),
                    opt("the model needs no training"),
                    opt("shapes become impossible"),
                    opt("error grows instead"),
                ),
                "Higher capacity lowers reconstruction error but complicates the search.",
            ),
        ),
        "Neural surrogates and physics-informed networks": (
            q(
                "A neural surrogate inside a design loop replaces the:",
                (
                    opt("expensive FEA/CFD solver with a fast learned predictor", correct=True),
                    opt("CAD kernel with pixels"),
                    opt("optimizer with a constant"),
                    opt("mesh with a drawing"),
                ),
                "Once trained, the network predicts simulation outputs in milliseconds.",
            ),
            q(
                "A physics-informed neural network (PINN) adds to its loss the:",
                (
                    opt("residual of the governing PDE", correct=True),
                    opt("file size of the mesh"),
                    opt("number of training epochs"),
                    opt("colour histogram"),
                ),
                "The PDE-residual term forces predictions to obey the physics.",
            ),
            q(
                "Adding the physics term in a PINN typically:",
                (
                    opt(
                        "reduces the amount of training data needed for a target accuracy",
                        correct=True,
                    ),
                    opt("requires far more data"),
                    opt("removes the need for any network"),
                    opt("guarantees zero error always"),
                ),
                "Physics constraints let the model generalize with less data.",
            ),
        ),
        "Bayesian optimization for expensive designs": (
            q(
                "Bayesian optimization is most appropriate when each evaluation is:",
                (
                    opt("very expensive, so the evaluation budget is tiny", correct=True),
                    opt("free and instant"),
                    opt("purely random"),
                    opt("impossible to measure"),
                ),
                "BO is built for costly black-box objectives with few allowed trials.",
            ),
            q(
                "The acquisition function in Bayesian optimization balances:",
                (
                    opt("exploiting good regions against exploring uncertain ones", correct=True),
                    opt("mesh size against colour"),
                    opt("file format against units"),
                    opt("CPU against GPU only"),
                ),
                "Expected Improvement trades off mean (exploit) and variance (explore).",
            ),
            q(
                "The probabilistic surrogate most often used in Bayesian optimization is a:",
                (
                    opt("Gaussian process", correct=True),
                    opt("hash table"),
                    opt("linked list"),
                    opt("finite-state machine"),
                ),
                "A GP gives a posterior mean and variance that drive the acquisition.",
            ),
        ),
        "Reinforcement learning for sequential CAD": (
            q(
                "Why is reinforcement learning a natural fit for CAD construction?",
                (
                    opt(
                        "a model is built as a sequence of operations - a sequential decision problem",
                        correct=True,
                    ),
                    opt("CAD has no operations"),
                    opt("geometry never changes"),
                    opt("there are no rewards possible"),
                ),
                "Sketch-extrude-fillet-pattern is a sequence of actions an agent can learn.",
            ),
            q(
                "In RL the policy pi_theta(a|s) is trained to maximize:",
                (
                    opt("expected discounted return (sum of gamma^t r_t)", correct=True),
                    opt("the mesh element count"),
                    opt("the file size"),
                    opt("the number of colours"),
                ),
                "The objective is expected cumulative discounted reward.",
            ),
            q(
                "The discount factor gamma (0 < gamma < 1) makes the agent:",
                (
                    opt("weight near-term rewards more than distant ones", correct=True),
                    opt("ignore all rewards"),
                    opt("only consider the final reward"),
                    opt("maximize file size"),
                ),
                "Discounting future rewards keeps the return finite and favours sooner gains.",
            ),
        ),
        "LLM and multimodal copilots for CAD": (
            q(
                "The most reliable LLM-for-CAD pattern today is to have the model:",
                (
                    opt("generate CAD-API code that a deterministic kernel executes", correct=True),
                    opt("paint the final geometry pixel by pixel"),
                    opt("guess dimensions without any kernel"),
                    opt("skip verification entirely"),
                ),
                "Deterministic CAD kernels build exact geometry from generated code.",
            ),
            q(
                "Retrieval-augmented generation in a CAD copilot is used to:",
                (
                    opt("ground output in company standards and the parts library", correct=True),
                    opt("increase the latent dimension"),
                    opt("delete the constraints"),
                    opt("replace the CAD kernel"),
                ),
                "Retrieval keeps generated designs consistent with valid, approved data.",
            ),
            q(
                "Even with a capable copilot, generated designs still require:",
                (
                    opt("FEA and manufacturing verification", correct=True),
                    opt("no checks at all"),
                    opt("removal of all constraints"),
                    opt("a colour change only"),
                ),
                "Capability is rising, but verification against physics and process remains essential.",
            ),
        ),
        "Automated evaluation and candidate selection": (
            q(
                "In a high-throughput pipeline, the bottleneck shifts to:",
                (
                    opt("evaluating and selecting among many candidates", correct=True),
                    opt("drawing each part by hand"),
                    opt("choosing a font"),
                    opt("printing the manual"),
                ),
                "When generation is cheap, consistent scoring and selection dominate.",
            ),
            q(
                "Why normalize each metric to [0, 1] before a weighted score?",
                (
                    opt("to put incomparable units (kg, MPa, cost) on equal footing", correct=True),
                    opt("to delete the worst candidate"),
                    opt("to increase the mass"),
                    opt("to skip the Pareto step"),
                ),
                "Normalization lets a weighted sum combine metrics with different units.",
            ),
            q(
                "A robust selection scheme first screens candidates on:",
                (
                    opt(
                        "hard constraints such as safety factor and manufacturability", correct=True
                    ),
                    opt("alphabetical order of names"),
                    opt("generation timestamp"),
                    opt("colour preference"),
                ),
                "Screen out infeasible designs, then rank survivors on the Pareto front.",
            ),
        ),
    },
    final=(
        q(
            "A deep generative model produces geometry by:",
            (
                opt("sampling a learned latent space of shapes", correct=True),
                opt("solving one fixed PDE"),
                opt("using no training data"),
                opt("editing a spreadsheet"),
            ),
            "VAEs, GANs and diffusion models map latent vectors to shapes.",
        ),
        q(
            "A physics-informed neural network differs from a plain data-driven net by:",
            (
                opt("including the PDE residual in its training loss", correct=True),
                opt("never using data"),
                opt("ignoring the governing equations"),
                opt("running only on CPUs"),
            ),
            "The PDE-residual term enforces physical consistency and cuts data needs.",
        ),
        q(
            "Bayesian optimization chooses the next design using an acquisition function over a:",
            (
                opt("Gaussian-process surrogate of the objective", correct=True),
                opt("random number alone"),
                opt("fixed lookup table"),
                opt("CAD drawing"),
            ),
            "The GP posterior drives Expected Improvement to balance explore/exploit.",
        ),
        q(
            "Reinforcement learning suits CAD because design is a:",
            (
                opt("sequence of operations - a sequential decision problem", correct=True),
                opt("single static image"),
                opt("problem with no actions"),
                opt("purely random process"),
            ),
            "The agent learns a policy over CAD actions to maximize discounted return.",
        ),
        q(
            "The most dependable way to use an LLM copilot for CAD is to have it:",
            (
                opt("emit code executed by a deterministic CAD kernel, then verify", correct=True),
                opt("hand-draw the final part"),
                opt("skip all simulation"),
                opt("ignore company standards"),
            ),
            "Deterministic kernels build exact geometry; verification stays essential.",
        ),
        q(
            "An automated selection pipeline should ultimately:",
            (
                opt(
                    "screen, build a Pareto front, score, and hand a short list to the engineer",
                    correct=True,
                ),
                opt("auto-ship the first candidate"),
                opt("hide all metrics"),
                opt("pick the heaviest design"),
            ),
            "Automate the grind; reserve the final judgment for the human.",
        ),
    ),
)
