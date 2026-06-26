"""Quiz questions for the Molecular Dynamics Simulations - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What molecular dynamics computes": (
            q(
                "Molecular dynamics advances atoms by numerically solving:",
                (
                    opt("Newton's second law, F = m a, for every atom", correct=True),
                    opt("the Schrodinger equation for all electrons each step"),
                    opt("Maxwell's equations"),
                    opt("the Navier-Stokes equations"),
                ),
                "Classical MD integrates Newton's equations of motion for the nuclei.",
            ),
            q(
                "The force on an atom in MD is obtained from the potential energy by:",
                (
                    opt("taking minus the gradient of U", correct=True),
                    opt("integrating U over time"),
                    opt("squaring U"),
                    opt("taking the time derivative of velocity"),
                ),
                "F_i = -grad_i U, the negative gradient of the potential energy.",
            ),
            q(
                "A typical MD integration time step is on the order of:",
                (
                    opt("1 to 2 femtoseconds", correct=True),
                    opt("1 to 2 nanoseconds"),
                    opt("1 to 2 seconds"),
                    opt("1 to 2 microseconds"),
                ),
                "Steps are ~1-2 fs, set by the fastest bond vibrations.",
            ),
        ),
        "The potential energy surface & force fields": (
            q(
                "Which term is NOT a bonded interaction in a classical force field?",
                (
                    opt("van der Waals (Lennard-Jones)", correct=True),
                    opt("bond stretching"),
                    opt("angle bending"),
                    opt("dihedral torsion"),
                ),
                "Van der Waals is non-bonded; bonds, angles and dihedrals are bonded.",
            ),
            q(
                "Bond stretching in common force fields is usually modelled as:",
                (
                    opt("a harmonic spring, (1/2) k (r - r0)^2", correct=True),
                    opt("a linear function of r"),
                    opt("a constant"),
                    opt("an exponential of r"),
                ),
                "Bonds are stiff harmonic springs about an equilibrium length r0.",
            ),
            q(
                "Examples of widely used biomolecular force fields include:",
                (
                    opt("AMBER, CHARMM, OPLS, GROMOS", correct=True),
                    opt("FFT, PME, WHAM"),
                    opt("TCP, UDP, HTTP"),
                    opt("RMSD, RMSF, PCA"),
                ),
                "AMBER, CHARMM, OPLS and GROMOS are standard force-field families.",
            ),
        ),
        "Lennard-Jones & electrostatic interactions": (
            q(
                "In the Lennard-Jones potential, the r^-12 term represents:",
                (
                    opt("short-range Pauli repulsion", correct=True),
                    opt("long-range attraction"),
                    opt("electrostatic attraction"),
                    opt("the harmonic bond"),
                ),
                "The steep r^-12 term is repulsion; r^-6 is attractive dispersion.",
            ),
            q(
                "Why can't Coulomb interactions simply be truncated at a short cutoff?",
                (
                    opt("they decay slowly as 1/r (long range)", correct=True),
                    opt("they decay as 1/r^12"),
                    opt("they are always zero"),
                    opt("they only act on bonded atoms"),
                ),
                "Coulomb decays as 1/r, so long-range methods like PME are needed.",
            ),
            q(
                "Compared with electrostatics, Lennard-Jones interactions:",
                (
                    opt("decay fast, so a ~1 nm cutoff is acceptable", correct=True),
                    opt("decay even more slowly than Coulomb"),
                    opt("never need a cutoff"),
                    opt("act only between bonded atoms"),
                ),
                "LJ falls off as r^-6, fast enough to cut at about 1 nm.",
            ),
        ),
        "Time integration & the Verlet algorithm": (
            q(
                "A key advantage of the velocity Verlet integrator is that it is:",
                (
                    opt(
                        "symplectic and time-reversible with no long-term energy drift",
                        correct=True,
                    ),
                    opt("exact for any time step size"),
                    opt("free of any time step limit"),
                    opt("able to skip force evaluations entirely"),
                ),
                "Verlet is symplectic and reversible, giving stable energy.",
            ),
            q(
                "What primarily limits how large the MD time step can be?",
                (
                    opt("the fastest motions, such as hydrogen bond vibrations", correct=True),
                    opt("the size of the hard disk"),
                    opt("the number of CPU cores"),
                    opt("the color of the molecule"),
                ),
                "The step must resolve the fastest vibrations (~10 fs H bonds).",
            ),
            q(
                "Constraint algorithms like SHAKE or LINCS allow larger time steps by:",
                (
                    opt("freezing fast bond vibrations (e.g. X-H bonds)", correct=True),
                    opt("removing all non-bonded forces"),
                    opt("doubling the number of atoms"),
                    opt("turning off the thermostat"),
                ),
                "Constraining the stiff X-H bonds removes the fastest motion.",
            ),
        ),
        "Temperature, kinetic energy & equipartition": (
            q(
                "In MD, temperature is:",
                (
                    opt("computed from the kinetic energy of the atoms", correct=True),
                    opt("a fixed input that never changes"),
                    opt("read from the potential energy only"),
                    opt("unrelated to atomic motion"),
                ),
                "T is measured from E_K via T = 2 E_K / (N_f k_B).",
            ),
            q(
                "The equipartition theorem assigns how much energy per quadratic degree of freedom?",
                (
                    opt("(1/2) k_B T", correct=True),
                    opt("k_B T^2"),
                    opt("3 k_B T"),
                    opt("zero"),
                ),
                "Each quadratic degree of freedom carries (1/2) k_B T on average.",
            ),
            q(
                "At equilibrium, atomic speeds follow which distribution?",
                (
                    opt("the Maxwell-Boltzmann distribution", correct=True),
                    opt("a uniform distribution"),
                    opt("a Poisson distribution"),
                    opt("a delta function at one speed"),
                ),
                "Equilibrium speeds are Maxwell-Boltzmann distributed.",
            ),
        ),
    },
    final=(
        q(
            "What does a molecular dynamics simulation fundamentally produce?",
            (
                opt("a trajectory of atomic positions and velocities over time", correct=True),
                opt("a single static crystal structure"),
                opt("only the total energy, no positions"),
                opt("a list of gene sequences"),
            ),
            "MD outputs a time trajectory from which properties are averaged.",
        ),
        q(
            "The Born-Oppenheimer approximation in classical MD lets us:",
            (
                opt(
                    "move nuclei on a single potential surface, separating fast electrons",
                    correct=True,
                ),
                opt("ignore all forces"),
                opt("treat electrons as heavier than nuclei"),
                opt("avoid integrating in time"),
            ),
            "It separates slow nuclei from fast electrons, giving a PES for the nuclei.",
        ),
        q(
            "Which interaction requires special long-range treatment such as PME?",
            (
                opt("electrostatics (Coulomb)", correct=True),
                opt("harmonic bonds"),
                opt("angle bending"),
                opt("Lennard-Jones repulsion"),
            ),
            "Coulomb's 1/r tail needs Ewald/PME; short-range terms can use cutoffs.",
        ),
        q(
            "The velocity Verlet integrator needs how many force evaluations per step?",
            (
                opt("one", correct=True),
                opt("zero"),
                opt("ten"),
                opt("one per atom pair"),
            ),
            "Verlet uses a single force evaluation per step, which is efficient.",
        ),
        q(
            "Heavy and light atoms at the same temperature differ in that:",
            (
                opt("heavy atoms move slower, light atoms faster", correct=True),
                opt("they all move at exactly the same speed"),
                opt("heavy atoms move faster"),
                opt("light atoms do not move"),
            ),
            "Equal (1/2)k_B T per DOF means heavier atoms have lower speeds.",
        ),
        q(
            "Which software packages are commonly used to run MD?",
            (
                opt("GROMACS, NAMD, LAMMPS, OpenMM, AMBER", correct=True),
                opt("Photoshop, Illustrator, InDesign"),
                opt("Excel, Word, PowerPoint"),
                opt("TCP, UDP, HTTP"),
            ),
            "These are standard MD engines used across chemistry and biophysics.",
        ),
    ),
)
