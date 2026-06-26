"""Quiz questions for the Structural Biology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Folding thermodynamics and stability": (
            q(
                "In a two-state folding model, which states are appreciably populated?",
                (
                    opt("Only folded (N) and unfolded (U)", correct=True),
                    opt("Folded, unfolded and many intermediates equally"),
                    opt("Only the unfolded state"),
                    opt("Crystalline and amorphous states"),
                ),
                "Two-state means only N and U are significantly populated at equilibrium.",
            ),
            q(
                "The free energy of unfolding relates to the equilibrium constant by:",
                (
                    opt("delta-G = -RT ln K", correct=True),
                    opt("delta-G = RT / K"),
                    opt("delta-G = K / RT"),
                    opt("delta-G = R + T + K"),
                ),
                "The standard relation is delta-G = -RT ln K.",
            ),
            q(
                "The denaturant midpoint Cm is the concentration where:",
                (
                    opt("half the protein is unfolded (f_U = 0.5)", correct=True),
                    opt("the protein is fully folded"),
                    opt("no denaturant remains"),
                    opt("resolution reaches 2 angstroms"),
                ),
                "Cm is where the fraction unfolded equals 0.5.",
            ),
        ),
        "The folding landscape and kinetics": (
            q(
                "Levinthal's paradox is resolved by:",
                (
                    opt(
                        "a funnel-shaped energy landscape biasing the chain toward native contacts",
                        correct=True,
                    ),
                    opt("proteins folding by exhaustive random search"),
                    opt("the absence of any energy barrier"),
                    opt("a single rigid folding pathway with no alternatives"),
                ),
                "A funneled landscape lets folding proceed downhill along many routes, not random search.",
            ),
            q(
                "The folding rate is governed mainly by:",
                (
                    opt("the height of the transition-state barrier", correct=True),
                    opt("the molecular weight only"),
                    opt("the crystal symmetry"),
                    opt("the detector resolution"),
                ),
                "Rate depends on the highest barrier, the transition state.",
            ),
            q(
                "What is the role of chaperones such as GroEL/GroES?",
                (
                    opt(
                        "provide protected environments that prevent off-pathway aggregation",
                        correct=True,
                    ),
                    opt("covalently cross-link the native fold"),
                    opt("supply the X-ray phases"),
                    opt("increase the simulation time step"),
                ),
                "Chaperones help proteins fold and avoid aggregation, not change the native structure.",
            ),
        ),
        "X-ray crystallography: Bragg's law": (
            q(
                "Why is a crystal required for X-ray crystallography?",
                (
                    opt(
                        "the periodic lattice amplifies weak scattering into measurable reflections",
                        correct=True,
                    ),
                    opt("crystals emit their own X-rays"),
                    opt("only crystals are biologically active"),
                    opt("crystals remove the need for phases"),
                ),
                "A single molecule scatters too weakly; the lattice amplifies it into discrete spots.",
            ),
            q(
                "Bragg's law is written as:",
                (
                    opt("n*lambda = 2 d sin(theta)", correct=True),
                    opt("E = m c^2"),
                    opt("lambda = 2 d / theta"),
                    opt("n = lambda d sin(theta)"),
                ),
                "Bragg's law: n*lambda = 2 d sin(theta).",
            ),
            q(
                "The 'phase problem' in crystallography is that:",
                (
                    opt(
                        "intensities give amplitudes but the phase of each reflection is lost",
                        correct=True,
                    ),
                    opt("the crystal melts during data collection"),
                    opt("the wavelength is unknown"),
                    opt("electrons cannot be detected"),
                ),
                "Detectors record intensity (amplitude); phases must be recovered separately.",
            ),
        ),
        "Cryo-electron microscopy": (
            q(
                "In cryo-EM, samples are frozen into:",
                (
                    opt("vitreous (glassy) ice", correct=True),
                    opt("crystalline ice"),
                    opt("a protein crystal"),
                    opt("liquid water at room temperature"),
                ),
                "Rapid freezing forms vitreous ice, avoiding damaging crystalline ice.",
            ),
            q(
                "Single-particle reconstruction builds a 3D map by:",
                (
                    opt(
                        "aligning and averaging many 2D projections in different orientations",
                        correct=True,
                    ),
                    opt("growing a large single crystal"),
                    opt("measuring one molecule directly at atomic resolution"),
                    opt("solving Bragg's law for each spot"),
                ),
                "Software assigns orientations to many noisy images and back-projects them into 3D.",
            ),
            q(
                "Which advance drove the cryo-EM 'resolution revolution'?",
                (
                    opt("direct electron detectors enabling motion correction", correct=True),
                    opt("higher denaturant concentrations"),
                    opt("smaller crystals"),
                    opt("longer X-ray wavelengths"),
                ),
                "Fast, low-noise direct detectors plus improved software transformed achievable resolution.",
            ),
        ),
        "Resolution, refinement and validation": (
            q(
                "Lower resolution numbers (in angstroms) mean:",
                (
                    opt("finer detail and a better map", correct=True),
                    opt("coarser, lower-quality maps"),
                    opt("no atoms can be seen"),
                    opt("the crystal is larger"),
                ),
                "Resolution is a distance; smaller values mean finer detail.",
            ),
            q(
                "R-free is used to:",
                (
                    opt(
                        "cross-validate the model against held-out reflections and detect overfitting",
                        correct=True,
                    ),
                    opt("measure the X-ray wavelength"),
                    opt("count the number of subunits"),
                    opt("set the simulation time step"),
                ),
                "R-free is computed on reflections excluded from refinement, flagging overfitting.",
            ),
            q(
                "Cryo-EM resolution is commonly reported from:",
                (
                    opt(
                        "the Fourier Shell Correlation between half-maps at the 0.143 threshold",
                        correct=True,
                    ),
                    opt("Bragg's law applied to spots"),
                    opt("the denaturation midpoint"),
                    opt("the Hill coefficient"),
                ),
                "FSC between two independent half-maps at 0.143 gives the reported resolution.",
            ),
        ),
    },
    final=(
        q(
            "For a two-state protein, delta-G of unfolding equals:",
            (
                opt("-RT ln K", correct=True),
                opt("RT ln K"),
                opt("K/RT"),
                opt("RT/K"),
            ),
            "delta-G = -RT ln K for the N to U equilibrium.",
        ),
        q(
            "The funnel model of folding explains why:",
            (
                opt(
                    "proteins fold quickly despite astronomically many conformations", correct=True
                ),
                opt("proteins can never fold"),
                opt("folding requires a crystal"),
                opt("phases are always known"),
            ),
            "The funneled landscape resolves Levinthal's paradox.",
        ),
        q(
            "Bragg's law relates diffraction angle to:",
            (
                opt("the spacing between lattice planes", correct=True),
                opt("the protein's melting temperature"),
                opt("the Hill coefficient"),
                opt("the number of subunits"),
            ),
            "n*lambda = 2 d sin(theta) links angle to plane spacing d.",
        ),
        q(
            "A major advantage of cryo-EM over crystallography is that it:",
            (
                opt("needs no crystal and suits large, flexible assemblies", correct=True),
                opt("requires a perfect crystal"),
                opt("gives no 3D information"),
                opt("cannot resolve ribosomes"),
            ),
            "Cryo-EM images particles directly and excels at large flexible complexes.",
        ),
        q(
            "A well-refined structure keeps R-free:",
            (
                opt("low and close to R-work", correct=True),
                opt("far above R-work"),
                opt("exactly 1.0"),
                opt("undefined"),
            ),
            "A large gap between R-free and R-work signals overfitting.",
        ),
        q(
            "At about 2 angstrom resolution you can typically see:",
            (
                opt("individual atoms and ordered water molecules", correct=True),
                opt("only the overall molecular envelope"),
                opt("hydrogen atoms clearly"),
                opt("nothing usable"),
            ),
            "Around 2 A you resolve individual atoms and waters; hydrogens need sub-1.2 A.",
        ),
    ),
)
