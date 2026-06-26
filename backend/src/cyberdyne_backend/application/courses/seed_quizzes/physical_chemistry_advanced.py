"""Quiz questions for the Physical Chemistry & Thermodynamics - Advanced course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The Schrödinger equation & quantization": (
            q(
                "The time-independent Schrodinger equation is written as:",
                (
                    opt("H psi = E psi", correct=True),
                    opt("H psi = 0"),
                    opt("E psi = 0"),
                    opt("H = E psi"),
                ),
                "It is an eigenvalue equation: the Hamiltonian acting on psi gives E psi.",
            ),
            q(
                "For a particle in a 1D box, the energy levels scale with quantum number n as:",
                (
                    opt("n squared", correct=True),
                    opt("n"),
                    opt("1/n"),
                    opt("the square root of n"),
                ),
                "E_n is proportional to n^2, so level spacing widens with n.",
            ),
            q(
                "The physical meaning of the squared wavefunction is:",
                (
                    opt("the probability density of finding the particle", correct=True),
                    opt("the energy of the particle"),
                    opt("the momentum directly"),
                    opt("the temperature"),
                ),
                "|psi|^2 is the probability density.",
            ),
        ),
        "Molecular Hamiltonian & Born–Oppenheimer": (
            q(
                "The Born-Oppenheimer approximation is justified because:",
                (
                    opt(
                        "nuclei are much heavier and move much slower than electrons", correct=True
                    ),
                    opt("electrons are heavier than nuclei"),
                    opt("Coulomb forces can be ignored"),
                    opt("temperature is zero"),
                ),
                "Heavy, slow nuclei can be frozen while solving the electronic problem.",
            ),
            q(
                "The electronic energy as a function of nuclear coordinates defines:",
                (
                    opt("the potential energy surface", correct=True),
                    opt("the partition function"),
                    opt("the entropy"),
                    opt("the rate constant"),
                ),
                "E_elec(R) is the potential energy surface (PES).",
            ),
            q(
                "On a potential energy surface, a transition state is:",
                (
                    opt("a first-order saddle point", correct=True),
                    opt("a deep minimum"),
                    opt("a maximum in every direction"),
                    opt("any point at high energy"),
                ),
                "Transition states are first-order saddle points connecting minima.",
            ),
        ),
        "Electronic structure: Hartree–Fock to DFT": (
            q(
                "Hartree-Fock treats electron-electron repulsion as:",
                (
                    opt("an averaged mean field", correct=True),
                    opt("exactly, with full correlation"),
                    opt("zero"),
                    opt("a random perturbation"),
                ),
                "HF uses a mean-field SCF treatment and misses electron correlation.",
            ),
            q(
                "Density functional theory expresses the energy as a functional of:",
                (
                    opt("the electron density", correct=True),
                    opt("the full many-electron wavefunction"),
                    opt("the nuclear masses"),
                    opt("the temperature"),
                ),
                "DFT works with the electron density n(r) via Kohn-Sham equations.",
            ),
            q(
                "Which method is often called the gold standard but scales very steeply with size?",
                (
                    opt("CCSD(T)", correct=True),
                    opt("Hartree-Fock"),
                    opt("simple molecular mechanics"),
                    opt("the particle in a box"),
                ),
                "CCSD(T) is highly accurate but scales roughly as N^7.",
            ),
        ),
        "Statistical thermodynamics & partition functions": (
            q(
                "The partition function counts:",
                (
                    opt(
                        "the thermally accessible states weighted by Boltzmann factors",
                        correct=True,
                    ),
                    opt("the number of atoms"),
                    opt("the number of bonds"),
                    opt("the reaction order"),
                ),
                "Q sums g_i exp(-energy/kT) over accessible states.",
            ),
            q(
                "Thermodynamic properties such as U, S and A can be derived from:",
                (
                    opt("the partition function and its temperature derivatives", correct=True),
                    opt("the equilibrium constant alone"),
                    opt("the cell potential only"),
                    opt("the rate law"),
                ),
                "Statistical thermodynamics gets all properties from ln Q.",
            ),
            q(
                "The molecular partition function is typically factored into contributions from:",
                (
                    opt("translation, rotation, vibration and electronic states", correct=True),
                    opt("only translation"),
                    opt("only electronic states"),
                    opt("pressure and volume"),
                ),
                "q = q_trans q_rot q_vib q_elec.",
            ),
        ),
        "Molecular spectroscopy": (
            q(
                "The resonance condition for a spectroscopic transition is:",
                (
                    opt("the photon energy equals the level spacing, dE = h nu", correct=True),
                    opt("the photon energy is zero"),
                    opt("dE = kT"),
                    opt("dE = -RT ln K"),
                ),
                "Absorption or emission occurs when h nu matches dE.",
            ),
            q(
                "Infrared spectroscopy primarily probes:",
                (
                    opt("vibrational transitions", correct=True),
                    opt("nuclear spin transitions"),
                    opt("rotational transitions only"),
                    opt("electronic transitions"),
                ),
                "IR excites molecular vibrations; UV-Vis probes electronic states.",
            ),
            q(
                "A harmonic-oscillator vibrational transition requires:",
                (
                    opt("a change in dipole moment, with dv = +/- 1", correct=True),
                    opt("no change in dipole moment"),
                    opt("dv = +/- 2 only"),
                    opt("a magnetic field"),
                ),
                "IR-active fundamentals need a changing dipole and obey dv = +/-1.",
            ),
        ),
        "Machine-learning interatomic potentials": (
            q(
                "Machine-learning interatomic potentials are trained to reproduce:",
                (
                    opt("energies and forces from quantum calculations", correct=True),
                    opt("experimental spectra only"),
                    opt("equilibrium constants only"),
                    opt("random noise"),
                ),
                "MLIPs learn the PES from quantum-computed energies and forces.",
            ),
            q(
                "The main advantage of an MLIP over direct DFT is:",
                (
                    opt("near-quantum accuracy at far lower computational cost", correct=True),
                    opt("it requires no training data"),
                    opt("it ignores the potential energy surface"),
                    opt("it is always exact"),
                ),
                "MLIPs run orders of magnitude faster while retaining accuracy.",
            ),
            q(
                "Active learning in an MLIP workflow flags configurations that are:",
                (
                    opt("high-uncertainty, sending them for new quantum labels", correct=True),
                    opt("already well predicted"),
                    opt("at zero temperature"),
                    opt("chemically identical"),
                ),
                "Active learning targets uncertain structures to improve the model.",
            ),
        ),
    },
    final=(
        q(
            "The Schrodinger equation H psi = E psi is an example of:",
            (
                opt("an eigenvalue problem", correct=True),
                opt("a rate law"),
                opt("a thermodynamic state function"),
                opt("a spectroscopic selection rule"),
            ),
            "psi are eigenfunctions of H with eigenvalues E.",
        ),
        q(
            "The Born-Oppenheimer approximation produces:",
            (
                opt("a potential energy surface for nuclear motion", correct=True),
                opt("the partition function directly"),
                opt("the Nernst equation"),
                opt("the Arrhenius prefactor"),
            ),
            "Freezing nuclei gives E_elec(R), the PES.",
        ),
        q(
            "Which ordering reflects increasing treatment of electron correlation?",
            (
                opt("Hartree-Fock, then DFT or MP2, then CCSD(T)", correct=True),
                opt("CCSD(T), then DFT, then Hartree-Fock"),
                opt("DFT has no role in correlation"),
                opt("all methods are equivalent"),
            ),
            "HF lacks correlation; post-HF and DFT recover it, with CCSD(T) most accurate.",
        ),
        q(
            "Statistical thermodynamics connects molecular energy levels to bulk properties via:",
            (
                opt("the partition function", correct=True),
                opt("the equilibrium constant only"),
                opt("the rate-determining step"),
                opt("the cell potential"),
            ),
            "All macroscopic thermodynamics follows from the partition function.",
        ),
        q(
            "Microwave, infrared and UV-visible spectroscopy probe, respectively:",
            (
                opt("rotational, vibrational and electronic transitions", correct=True),
                opt("electronic, rotational and vibrational transitions"),
                opt("nuclear spin, vibrational and rotational transitions"),
                opt("all probe the same transitions"),
            ),
            "Energy scale increases from rotational to vibrational to electronic.",
        ),
        q(
            "Machine-learning interatomic potentials are valuable because they:",
            (
                opt("approximate the quantum PES at greatly reduced cost", correct=True),
                opt("eliminate the need for any quantum data"),
                opt("replace the Schrodinger equation with thermodynamics"),
                opt("only work at zero temperature"),
            ),
            "MLIPs enable large, long simulations at near-quantum accuracy.",
        ),
    ),
)
