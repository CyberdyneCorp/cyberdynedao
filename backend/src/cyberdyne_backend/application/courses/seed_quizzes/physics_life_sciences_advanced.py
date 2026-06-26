"""Quiz questions for the Physics for Life Sciences - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Light and matter: optics for the life sciences": (
            q(
                "The Beer-Lambert law relates absorbance to concentration as:",
                (
                    opt("A = epsilon * c * l", correct=True),
                    opt("A = c / l"),
                    opt("A = epsilon / c"),
                    opt("A is independent of concentration"),
                ),
                "Absorbance is proportional to molar absorptivity, concentration and path length.",
            ),
            q(
                "The diffraction (Abbe) limit of conventional light microscopy is about:",
                (
                    opt("200 nm for visible light", correct=True),
                    opt("2 nm"),
                    opt("2 micrometers"),
                    opt("2 mm"),
                ),
                "d ~ lambda/(2*NA) is roughly 200 nm, the wall super-resolution methods break.",
            ),
            q(
                "Why is absorbance, rather than transmittance, the convenient linear quantity?",
                (
                    opt(
                        "Transmittance falls exponentially; absorbance is its logarithm and is linear in c",
                        correct=True,
                    ),
                    opt("Transmittance is always zero"),
                    opt("Absorbance does not depend on concentration"),
                    opt("Transmittance is linear and absorbance is not"),
                ),
                "I/I0 decays exponentially with concentration, so its log (absorbance) is linear.",
            ),
        ),
        "Fluorescence, FRET and spectroscopy": (
            q(
                "The Stokes shift in fluorescence refers to:",
                (
                    opt("Emission at a longer wavelength than absorption", correct=True),
                    opt("Emission at a shorter wavelength"),
                    opt("Identical absorption and emission wavelengths"),
                    opt("The absence of any emission"),
                ),
                "Vibrational energy loss in the excited state shifts emission to longer wavelengths.",
            ),
            q(
                "FRET efficiency depends on donor-acceptor distance as:",
                (
                    opt("1/(1 + (r/R0)^6)", correct=True),
                    opt("1/(1 + r/R0)"),
                    opt("Linear in r"),
                    opt("Independent of r"),
                ),
                "The sixth-power dependence makes FRET a sensitive nanometre ruler.",
            ),
            q(
                "FRET is most sensitive as a molecular ruler over distances around:",
                (
                    opt("2-8 nm (near R0 ~ 5 nm)", correct=True),
                    opt("2-8 micrometers"),
                    opt("2-8 mm"),
                    opt("0.01-0.1 nm"),
                ),
                "FRET reports best near the Forster radius R0, typically a few nanometres.",
            ),
        ),
        "Single-molecule biophysics and force spectroscopy": (
            q(
                "Optical tweezers and AFM apply forces on single molecules in the range of:",
                (
                    opt("Piconewtons", correct=True),
                    opt("Newtons"),
                    opt("Kilonewtons"),
                    opt("Megajoules"),
                ),
                "Single-molecule force tools operate at piconewton forces and nanometre displacements.",
            ),
            q(
                "In Bell's model, an applied force F changes the unfolding off-rate by:",
                (
                    opt("Increasing it exponentially with force", correct=True),
                    opt("Decreasing it exponentially"),
                    opt("Leaving it unchanged"),
                    opt("Making it independent of temperature"),
                ),
                "k(F) = k0 * exp(F*x-dagger/kB*T): force lowers the barrier, raising the off-rate.",
            ),
            q(
                "What advantage do single-molecule methods have over bulk measurements?",
                (
                    opt(
                        "They reveal rare states and stochastic dynamics hidden in averages",
                        correct=True,
                    ),
                    opt("They are always cheaper"),
                    opt("They require no instrumentation"),
                    opt("They eliminate thermal noise"),
                ),
                "Bulk reports ensemble averages; single-molecule reveals heterogeneity and dynamics.",
            ),
        ),
        "Structure determination: X-ray, NMR and cryo-EM": (
            q(
                "The 'phase problem' is characteristic of which technique?",
                (
                    opt("X-ray crystallography", correct=True),
                    opt("Solution NMR"),
                    opt("Mass spectrometry"),
                    opt("Light microscopy"),
                ),
                "Diffraction gives amplitudes but not phases, solved by molecular replacement or anomalous scattering.",
            ),
            q(
                "Cryo-EM resolution improves with the number N of averaged particles roughly as:",
                (
                    opt("SNR proportional to sqrt(N)", correct=True),
                    opt("SNR proportional to N^2"),
                    opt("SNR independent of N"),
                    opt("SNR proportional to 1/N"),
                ),
                "Averaging noisy single-particle images raises SNR as sqrt(N).",
            ),
            q(
                "Which method uniquely reports protein dynamics in solution but is limited to smaller proteins?",
                (
                    opt("NMR spectroscopy", correct=True),
                    opt("X-ray crystallography"),
                    opt("Cryo-EM"),
                    opt("Electron tomography"),
                ),
                "Solution NMR captures dynamics but is size-limited compared with crystallography and cryo-EM.",
            ),
        ),
        "Statistical physics of macromolecules": (
            q(
                "An ideal (random-coil) polymer chain has its size scale with N segments as:",
                (
                    opt("R ~ b * N^(1/2)", correct=True),
                    opt("R ~ b * N"),
                    opt("R ~ b * N^2"),
                    opt("R independent of N"),
                ),
                "An ideal chain has exponent nu = 1/2; a self-avoiding chain ~ 3/5.",
            ),
            q(
                "Levinthal's paradox is resolved by:",
                (
                    opt("A funnelled free-energy landscape that channels folding", correct=True),
                    opt("Folding being instantaneous and barrier-free"),
                    opt("Proteins never folding"),
                    opt("An exhaustive random search of all conformations"),
                ),
                "A biased, funnel-shaped landscape guides the chain to the native state quickly.",
            ),
            q(
                "Cooperative two-state folding appears as which kind of transition?",
                (
                    opt("A sharp sigmoidal switch with temperature or denaturant", correct=True),
                    opt("A perfectly linear ramp"),
                    opt("No transition at all"),
                    opt("A discontinuous jump to zero"),
                ),
                "Aggregating many small interactions makes folding nearly all-or-none.",
            ),
        ),
        "Computational and AI biophysics": (
            q(
                "Molecular dynamics simulations integrate which equations with femtosecond timesteps?",
                (
                    opt("Newton's equations of motion under a force field", correct=True),
                    opt("Maxwell's equations"),
                    opt("The Schrodinger equation for every electron"),
                    opt("The Navier-Stokes equations"),
                ),
                "Classical MD integrates Newton's equations using force fields like AMBER or CHARMM.",
            ),
            q(
                "AlphaFold2 is notable for:",
                (
                    opt(
                        "Predicting protein structure from sequence at near-experimental accuracy",
                        correct=True,
                    ),
                    opt("Sequencing genomes faster"),
                    opt("Replacing all wet-lab experiments"),
                    opt("Measuring membrane potentials"),
                ),
                "AlphaFold2 solved a decades-old grand challenge in structure prediction.",
            ),
            q(
                "Machine-learned interatomic potentials aim to:",
                (
                    opt("Approach quantum accuracy at classical computational cost", correct=True),
                    opt("Eliminate the need for any force field concept"),
                    opt("Replace experimental crystallography"),
                    opt("Slow down simulations for accuracy"),
                ),
                "ML potentials trained on quantum data give accurate forces at far lower cost.",
            ),
        ),
    },
    final=(
        q(
            "The Beer-Lambert law makes which quantity linear in concentration?",
            (
                opt("Absorbance", correct=True),
                opt("Transmittance"),
                opt("Reflected intensity"),
                opt("Wavelength"),
            ),
            "A = epsilon*c*l; transmittance itself decays exponentially.",
        ),
        q(
            "FRET works as a molecular ruler because efficiency varies with distance as:",
            (
                opt("1/(1 + (r/R0)^6)", correct=True),
                opt("Linearly in r"),
                opt("As 1/r^2"),
                opt("Independently of r"),
            ),
            "The steep sixth-power law gives nanometre sensitivity near R0.",
        ),
        q(
            "Bell's model predicts that mechanical force on a molecule:",
            (
                opt("Exponentially accelerates unfolding by lowering the barrier", correct=True),
                opt("Has no effect on kinetics"),
                opt("Always stabilizes the folded state"),
                opt("Only matters at zero temperature"),
            ),
            "k(F) = k0 exp(F*x-dagger/kB*T).",
        ),
        q(
            "Cryo-EM achieves near-atomic resolution largely by:",
            (
                opt("Averaging many noisy single-particle images (SNR ~ sqrt(N))", correct=True),
                opt("Growing perfect crystals"),
                opt("Using radio waves"),
                opt("Measuring NMR chemical shifts"),
            ),
            "Direct detectors plus particle averaging drove the resolution revolution.",
        ),
        q(
            "Levinthal's paradox is resolved by recognizing that the folding landscape is:",
            (
                opt("Funnelled toward the native state", correct=True),
                opt("Perfectly flat"),
                opt("Infinitely high everywhere"),
                opt("Searched exhaustively at random"),
            ),
            "A funnel channels the chain downhill quickly to the native minimum.",
        ),
        q(
            "Which AI advance solved the protein structure prediction grand challenge?",
            (
                opt("AlphaFold2 / AlphaFold3", correct=True),
                opt("Classical molecular dynamics alone"),
                opt("X-ray crystallography software"),
                opt("Faster DNA sequencers"),
            ),
            "Deep-learning models predict structure from sequence at near-experimental accuracy.",
        ),
    ),
)
