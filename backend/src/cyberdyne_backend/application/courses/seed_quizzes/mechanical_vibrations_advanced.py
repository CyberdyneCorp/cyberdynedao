"""Quiz questions for the Mechanical Vibrations - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Multi-DOF systems in matrix form": (
            q(
                "The matrix equation of motion for an n-DOF system is?",
                (
                    opt("M x'' + C x' + K x = f(t)", correct=True),
                    opt("K x'' + C x' + M x = f(t)"),
                    opt("M x'' + K x' + C x = f(t)"),
                    opt("C x'' + M x' + K x = f(t)"),
                ),
                "Mass, damping, and stiffness matrices multiply the acceleration, velocity, and displacement vectors.",
            ),
            q(
                "Off-diagonal terms in the stiffness matrix K represent?",
                (
                    opt("Coupling between coordinates through shared springs", correct=True),
                    opt("The total mass of the system"),
                    opt("Pure damping effects"),
                    opt("External forcing"),
                ),
                "Shared elements create off-diagonal -k terms that couple the masses.",
            ),
            q(
                "How are global stiffness matrices typically built in practice?",
                (
                    opt("By assembling element contributions into the global matrix", correct=True),
                    opt("By inverting the mass matrix"),
                    opt("By measuring damping ratios"),
                    opt("By solving the wave equation analytically"),
                ),
                "Each element contributes a local stiffness pattern summed into the global K, as in FEA.",
            ),
        ),
        "The eigenvalue problem and mode shapes": (
            q(
                "Natural frequencies of an undamped MDOF system come from?",
                (
                    opt("det(K - omega^2 M) = 0", correct=True),
                    opt("det(K + C) = 0"),
                    opt("trace(M) = 0"),
                    opt("det(M) = 0"),
                ),
                "The generalized eigenvalue problem (K - omega^2 M) phi = 0 yields the natural frequencies.",
            ),
            q(
                "A mode shape (eigenvector) represents?",
                (
                    opt(
                        "The relative deformation pattern when the structure rings at that frequency",
                        correct=True,
                    ),
                    opt("The total applied force"),
                    opt("The damping ratio"),
                    opt("The static deflection under gravity"),
                ),
                "Each eigenvector is the spatial pattern of motion at its natural frequency.",
            ),
            q(
                "Mode shapes are orthogonal with respect to?",
                (
                    opt("Both the mass and stiffness matrices", correct=True),
                    opt("The damping matrix only"),
                    opt("The identity matrix only"),
                    opt("No matrix at all"),
                ),
                "phi_i^T M phi_j = 0 and phi_i^T K phi_j = 0 for i != j, which decouples the system.",
            ),
        ),
        "Modal analysis and modal superposition": (
            q(
                "Transforming to modal coordinates x = Phi q does what to the equations?",
                (
                    opt("Decouples them into independent SDOF equations", correct=True),
                    opt("Couples them more strongly"),
                    opt("Removes all damping"),
                    opt("Makes them nonlinear"),
                ),
                "Orthogonality diagonalizes M and K, giving one independent SDOF equation per mode.",
            ),
            q(
                "Modal truncation is useful because?",
                (
                    opt("Only the first few modes usually dominate the response", correct=True),
                    opt("Higher modes are always the most important"),
                    opt("It eliminates the need for mode shapes"),
                    opt("It increases the number of DOFs"),
                ),
                "Keeping a handful of low modes makes huge models tractable.",
            ),
            q(
                "Rayleigh (proportional) damping C = alpha M + beta K is convenient because?",
                (
                    opt("It keeps the modes uncoupled", correct=True),
                    opt("It removes the stiffness matrix"),
                    opt("It forces all modes to the same frequency"),
                    opt("It makes the system undamped"),
                ),
                "Proportional damping preserves modal orthogonality so the decoupled equations stay valid.",
            ),
        ),
        "Continuous systems: strings and beams": (
            q(
                "A vibrating string has natural frequencies that are?",
                (
                    opt("A harmonic series, integer multiples of the fundamental", correct=True),
                    opt("Non-harmonic and irregular"),
                    opt("Always a single frequency"),
                    opt("Independent of tension"),
                ),
                "String modes follow omega_n = (n pi / L) sqrt(T/rho), a harmonic series.",
            ),
            q(
                "The Euler-Bernoulli beam equation involves which spatial derivative of w?",
                (
                    opt("The fourth derivative (EI w_xxxx)", correct=True),
                    opt("The first derivative"),
                    opt("The second derivative only"),
                    opt("No spatial derivative"),
                ),
                "Flexural rigidity multiplies the fourth spatial derivative in the beam PDE.",
            ),
            q(
                "Compared with a string, beam overtones are?",
                (
                    opt("Not harmonic (not integer multiples)", correct=True),
                    opt("Exactly harmonic"),
                    opt("Always identical to string overtones"),
                    opt("Independent of boundary conditions"),
                ),
                "Beam frequencies scale with (beta_n L)^2, which are not integer-related.",
            ),
        ),
        "Computational modal analysis with FEA": (
            q(
                "FEA modal analysis ultimately solves which problem?",
                (
                    opt("The generalized eigenproblem (K - omega^2 M) phi = 0", correct=True),
                    opt("A linear static equation only"),
                    opt("A heat-conduction equation"),
                    opt("A pure optimization problem"),
                ),
                "FEA assembles M and K, then solves the same eigenproblem with many DOFs.",
            ),
            q(
                "Why solve only the lowest k modes with shift-invert in large models?",
                (
                    opt(
                        "The lowest modes are the engineering-relevant ones and full solves are costly",
                        correct=True,
                    ),
                    opt("Higher modes are easier to compute"),
                    opt("Shift-invert only works on the highest modes"),
                    opt("It removes the need for boundary conditions"),
                ),
                "Sparse shift-invert efficiently extracts the few low modes that dominate the dynamics.",
            ),
            q(
                "The modal assurance criterion (MAC) is used to?",
                (
                    opt("Compare computed mode shapes against measured ones", correct=True),
                    opt("Apply boundary conditions"),
                    opt("Mesh the geometry"),
                    opt("Compute the damping matrix"),
                ),
                "MAC quantifies correlation between FE and test mode shapes for validation.",
            ),
        ),
        "Experimental FRF identification and damping optimization": (
            q(
                "A frequency-response function (FRF) is estimated as?",
                (
                    opt("The ratio of measured output to measured input", correct=True),
                    opt("The mass divided by stiffness"),
                    opt("The static deflection"),
                    opt("The product of all natural frequencies"),
                ),
                "H(omega) = output/input; curve-fitting its peaks recovers modal parameters.",
            ),
            q(
                "The H1 estimator S_fx/S_ff is preferred when?",
                (
                    opt("Output (response) noise dominates", correct=True),
                    opt("There is no measurement noise"),
                    opt("Input (force) noise dominates"),
                    opt("The system is perfectly linear and noise-free"),
                ),
                "H1 from cross/auto spectra is robust to output noise; coherence flags bad bands.",
            ),
            q(
                "Optimizing a damping treatment typically means?",
                (
                    opt(
                        "Choosing parameters to minimize a vibration objective under constraints",
                        correct=True,
                    ),
                    opt("Maximizing the peak response"),
                    opt("Removing all sensors"),
                    opt("Ignoring mass and cost limits"),
                ),
                "Optimizers tune TMD/layer/mount parameters to minimize peak or RMS response.",
            ),
        ),
    },
    final=(
        q(
            "Natural frequencies of an MDOF system are found from?",
            (
                opt("det(K - omega^2 M) = 0", correct=True),
                opt("det(M) = 0"),
                opt("trace(C) = 0"),
                opt("Inverting K only"),
            ),
            "The generalized eigenvalue problem gives the n natural frequencies.",
        ),
        q(
            "Mode shapes are orthogonal with respect to?",
            (
                opt("The mass and stiffness matrices", correct=True),
                opt("The damping matrix alone"),
                opt("No matrices"),
                opt("Only the forcing vector"),
            ),
            "This orthogonality decouples the equations in modal coordinates.",
        ),
        q(
            "Modal superposition lets you?",
            (
                opt(
                    "Solve an n-DOF problem as n independent SDOF problems and sum them",
                    correct=True,
                ),
                opt("Avoid finding any natural frequencies"),
                opt("Eliminate the mass matrix"),
                opt("Make the response nonlinear"),
            ),
            "After decoupling, each modal coordinate is a familiar SDOF system.",
        ),
        q(
            "Euler-Bernoulli beam frequencies scale with?",
            (
                opt("(beta_n L)^2 times sqrt(EI/(rho A L^4))", correct=True),
                opt("Integer multiples of a fundamental"),
                opt("The damping ratio only"),
                opt("The applied force amplitude"),
            ),
            "Beam overtones are non-harmonic, set by transcendental roots beta_n L.",
        ),
        q(
            "FEA modal analysis differs from analytic MDOF analysis mainly in that it?",
            (
                opt(
                    "Discretizes complex geometry into many elements and solves a sparse eigenproblem",
                    correct=True,
                ),
                opt("Avoids solving any eigenvalue problem"),
                opt("Ignores boundary conditions"),
                opt("Works only for single-DOF systems"),
            ),
            "FEA assembles M and K from elements, then solves the same eigenproblem at scale.",
        ),
        q(
            "Experimental modal analysis recovers modal parameters by?",
            (
                opt("Curve-fitting measured frequency-response functions", correct=True),
                opt("Measuring static deflection only"),
                opt("Computing the determinant of M"),
                opt("Assuming zero damping"),
            ),
            "Peaks in the FRF yield natural frequencies, damping, and mode shapes.",
        ),
    ),
)
