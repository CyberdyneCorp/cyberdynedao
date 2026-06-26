"""Quiz questions for the AI-Driven Organic & Biomimetic Shapes - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Generative models for 3D form": (
            q(
                "A variational autoencoder (VAE) generates a new shape by:",
                (
                    opt("sampling a latent code from the prior and decoding it", correct=True),
                    opt("running a finite-element solve"),
                    opt("subtracting two meshes"),
                    opt("rotating an existing part"),
                ),
                "After training, sampling z ~ N(0, I) and decoding produces new shapes.",
            ),
            q(
                "The VAE loss balances reconstruction error against a:",
                (
                    opt("KL-divergence regularisation toward the prior", correct=True),
                    opt("support-volume penalty"),
                    opt("print-time term"),
                    opt("colour-matching term"),
                ),
                "The KL term pulls the encoder posterior toward the Gaussian prior so the latent space is sampleable.",
            ),
            q(
                "A common failure mode of GANs is:",
                (
                    opt("mode collapse (limited diversity of outputs)", correct=True),
                    opt("infinite resolution"),
                    opt("guaranteed convergence"),
                    opt("zero training cost"),
                ),
                "GANs can collapse to producing few distinct shapes despite a diverse dataset.",
            ),
        ),
        "Diffusion models for shape synthesis": (
            q(
                "A diffusion model generates shapes by:",
                (
                    opt(
                        "learning to reverse a noising process, denoising from pure noise",
                        correct=True,
                    ),
                    opt("encoding to a single latent and decoding once"),
                    opt("solving Murray's law"),
                    opt("applying marching cubes to a photo"),
                ),
                "A network learns to denoise step by step, so sampling walks noise back to a clean shape.",
            ),
            q(
                "The diffusion training objective typically has the network predict:",
                (
                    opt("the noise added at each step", correct=True),
                    opt("the final triangle count"),
                    opt("the build orientation"),
                    opt("the material cost"),
                ),
                "eps_theta(x_t, t) is trained to predict the added noise via an MSE loss.",
            ),
            q(
                "Increasing the number of denoising steps generally:",
                (
                    opt("improves sample quality with diminishing returns", correct=True),
                    opt("always lowers quality"),
                    opt("has no effect"),
                    opt("removes the need for a network"),
                ),
                "More steps refine quality but with diminishing returns, trading quality against speed.",
            ),
        ),
        "Topology optimisation and generative design": (
            q(
                "The objective minimised in classic stiffness topology optimisation is:",
                (
                    opt("compliance (to maximise stiffness) under a mass budget", correct=True),
                    opt("colour uniformity"),
                    opt("the number of triangles"),
                    opt("print temperature"),
                ),
                "TO minimises compliance c = U^T K U subject to a volume-fraction constraint.",
            ),
            q(
                "In the SIMP method, intermediate densities are discouraged by:",
                (
                    opt("a penalisation exponent p (about 3) on element stiffness", correct=True),
                    opt("adding random noise"),
                    opt("increasing the mass budget"),
                    opt("removing the FE solve"),
                ),
                "E_e = E_min + x_e^p (E0 - E_min) penalises gray values, pushing densities toward 0 or 1.",
            ),
            q(
                "A density filter is applied in topology optimisation mainly to:",
                (
                    opt("avoid checkerboard patterns and impose a length scale", correct=True),
                    opt("increase compliance"),
                    opt("change the load"),
                    opt("colour the part"),
                ),
                "Filtering removes numerical checkerboarding and enforces a minimum member size.",
            ),
        ),
        "Manufacturability and print-readiness": (
            q(
                "The overhang rule of thumb says surfaces are self-supporting when steeper than:",
                (
                    opt("the critical angle, often about 45 degrees from horizontal", correct=True),
                    opt("90 degrees only"),
                    opt("any angle at all"),
                    opt("0 degrees"),
                ),
                "Below the critical overhang angle, down-facing surfaces sag and need support.",
            ),
            q(
                "Internal lattices need escape holes primarily to:",
                (
                    opt("let trapped powder or resin drain out", correct=True),
                    opt("increase weight"),
                    opt("add colour"),
                    opt("raise the melting point"),
                ),
                "Without escape holes, unfused powder or uncured resin is trapped inside the part.",
            ),
            q(
                "Choosing build orientation is an optimisation because it trades:",
                (
                    opt(
                        "support volume against strength anisotropy and surface finish",
                        correct=True,
                    ),
                    opt("colour against weight"),
                    opt("latent dimension against epochs"),
                    opt("nothing - any orientation is equal"),
                ),
                "Orientation changes supported area, anisotropic strength and finish, so it is optimised.",
            ),
        ),
        "End-to-end pipeline: prompt to printed part": (
            q(
                "In the prompt-to-part pipeline, what happens when a candidate fails the manufacturability check?",
                (
                    opt("the loop returns to generate or refine new candidates", correct=True),
                    opt("the part is printed anyway"),
                    opt("the pipeline stops permanently"),
                    opt("the loads are deleted"),
                ),
                "A failed check feeds back to generation/optimisation until a print-ready candidate passes.",
            ),
            q(
                "Why is graded TPMS infill convenient at the end of the pipeline?",
                (
                    opt(
                        "it is self-supporting and self-draining, often needing no internal supports",
                        correct=True,
                    ),
                    opt("it requires dense internal supports"),
                    opt("it cannot be printed"),
                    opt("it removes the need for a mesh"),
                ),
                "TPMS lattices print without internal supports and drain powder/resin readily.",
            ),
            q(
                "The pipeline's best-design score over iterations typically:",
                (
                    opt("rises and saturates as it nears a print-ready optimum", correct=True),
                    opt("falls to zero"),
                    opt("oscillates forever without improving"),
                    opt("is constant"),
                ),
                "Keeping the best candidate yields a rising, saturating convergence curve.",
            ),
        ),
    },
    final=(
        q(
            "Which generative family is currently state of the art for high-quality 3D shape synthesis?",
            (
                opt("diffusion models", correct=True),
                opt("rule-based CAD macros"),
                opt("linear regression"),
                opt("k-means clustering"),
            ),
            "Diffusion models (often latent diffusion) lead modern generative 3D form synthesis.",
        ),
        q(
            "Topology optimisation produces organic, bone-like geometry because it:",
            (
                opt("places material along the load paths to minimise compliance", correct=True),
                opt("copies a fixed template"),
                opt("randomly removes material"),
                opt("maximises mass"),
            ),
            "Minimising compliance under a mass budget routes material along stress paths.",
        ),
        q(
            "A generated organic shape is made print-ready by, among other steps:",
            (
                opt(
                    "repairing the mesh and enforcing overhang and min-wall constraints",
                    correct=True,
                ),
                opt("only recolouring it"),
                opt("ignoring all process limits"),
                opt("doubling its mass"),
            ),
            "Print-readiness requires watertight repair plus DfAM constraint checks.",
        ),
        q(
            "Conditioning a diffusion model on a text or image embedding enables:",
            (
                opt("prompt-driven generation of shapes", correct=True),
                opt("faster finite-element solves"),
                opt("removal of the denoising steps"),
                opt("automatic slicing only"),
            ),
            "Conditioning lets the reverse process produce shapes matching a text/image prompt.",
        ),
        q(
            "In SIMP topology optimisation, the typical stiffness penalisation exponent p is about:",
            (
                opt("3", correct=True),
                opt("0"),
                opt("1"),
                opt("10"),
            ),
            "p ~ 3 strongly penalises intermediate densities, driving a clear 0/1 layout.",
        ),
        q(
            "A frontier direction for AI-driven organic design pipelines is:",
            (
                opt(
                    "differentiable pipelines that backprop manufacturing cost into the generator",
                    correct=True,
                ),
                opt("removing all physics from the loop"),
                opt("printing without any validation"),
                opt("using only 2D drawings"),
            ),
            "Differentiable, multi-physics, agentic pipelines are the active frontier - with humans owning sign-off.",
        ),
    ),
)
