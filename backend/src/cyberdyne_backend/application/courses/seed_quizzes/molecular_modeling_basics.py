"""Quiz questions for the Molecular Modeling & Visualization - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Atomic coordinates and molecular representations": (
            q(
                "Cartesian molecular coordinates are usually expressed in which unit?",
                (
                    opt("Angstrom (1e-10 m)", correct=True),
                    opt("Meters"),
                    opt("Nanometers only"),
                    opt("Degrees"),
                ),
                "Atomic positions are conventionally given in angstrom.",
            ),
            q(
                "Which file format adds explicit bonds and bond orders?",
                (
                    opt("SDF / MOL2", correct=True),
                    opt("XYZ"),
                    opt("Plain text only"),
                    opt("A screenshot"),
                ),
                "SDF/MOL/MOL2 encode connectivity and bond orders; XYZ has coordinates only.",
            ),
            q(
                "In a Z-matrix, an atom is placed using:",
                (
                    opt("a bond length, bond angle and dihedral", correct=True),
                    opt("only its absolute (x,y,z)"),
                    opt("its mass and charge"),
                    opt("its color in the viewer"),
                ),
                "Z-matrices use internal coordinates: bond, angle and dihedral relative to placed atoms.",
            ),
        ),
        "The potential energy surface": (
            q(
                "On the potential energy surface, a local minimum represents:",
                (
                    opt("a stable conformer", correct=True),
                    opt("a transition state"),
                    opt("a broken bond"),
                    opt("the highest-energy structure"),
                ),
                "Minima are stable geometries where the gradient is zero and curvature is positive.",
            ),
            q(
                "A saddle point linking two minima corresponds to:",
                (
                    opt("a transition state", correct=True),
                    opt("the global minimum"),
                    opt("an isolated atom"),
                    opt("a solvent molecule"),
                ),
                "A first-order saddle point is a transition state between two minima.",
            ),
            q(
                "Treating energy as a function of nuclear positions is justified by:",
                (
                    opt("the Born-Oppenheimer approximation", correct=True),
                    opt("Hooke's law"),
                    opt("the Henderson-Hasselbalch equation"),
                    opt("Coulomb's law"),
                ),
                "Born-Oppenheimer separates fast electronic motion from slow nuclear motion.",
            ),
        ),
        "Force fields and bonded terms": (
            q(
                "Bond stretching in a typical force field is modeled as:",
                (
                    opt("a harmonic (spring) potential", correct=True),
                    opt("a Coulomb term"),
                    opt("a Lennard-Jones term"),
                    opt("a constant"),
                ),
                "Bonds use a harmonic term, 0.5 k (r - r0)^2.",
            ),
            q(
                "Torsion (dihedral) terms are represented by:",
                (
                    opt("a periodic cosine series", correct=True),
                    opt("a single harmonic well"),
                    opt("an inverse-square law"),
                    opt("a step function"),
                ),
                "Torsions use a cosine series to capture multiple rotational minima.",
            ),
            q(
                "Which of these is a biomolecular force field?",
                (
                    opt("AMBER", correct=True),
                    opt("PyMOL"),
                    opt("BLAST"),
                    opt("PDB"),
                ),
                "AMBER, CHARMM, OPLS and GROMOS are force fields; the others are tools/formats/databases.",
            ),
        ),
        "Non-bonded interactions: van der Waals and electrostatics": (
            q(
                "The Lennard-Jones potential combines repulsion and attraction as:",
                (
                    opt("r^-12 repulsion and r^-6 dispersion", correct=True),
                    opt("r^-1 and r^-2"),
                    opt("only attraction"),
                    opt("a harmonic spring"),
                ),
                "LJ uses an r^-12 repulsive and r^-6 attractive (dispersion) term.",
            ),
            q(
                "Electrostatic interactions between partial charges decay as:",
                (
                    opt("1/r (Coulomb)", correct=True),
                    opt("1/r^12"),
                    opt("exponentially to zero immediately"),
                    opt("they do not depend on distance"),
                ),
                "Coulomb's law gives a slow 1/r decay, requiring long-range treatment.",
            ),
            q(
                "Particle Mesh Ewald (PME) is used to handle:",
                (
                    opt("long-range electrostatics in periodic systems", correct=True),
                    opt("bond stretching"),
                    opt("adding hydrogens"),
                    opt("rendering surfaces"),
                ),
                "PME efficiently sums the slowly decaying 1/r electrostatics under periodic boundaries.",
            ),
        ),
        "Molecular mechanics vs quantum methods": (
            q(
                "Compared with quantum methods, molecular mechanics is:",
                (
                    opt("faster but cannot break bonds", correct=True),
                    opt("slower and more accurate for electronic states"),
                    opt("able to model charge transfer explicitly"),
                    opt("identical in cost"),
                ),
                "MM is fast and treats atoms classically, so it cannot model bond breaking or electrons.",
            ),
            q(
                "Which quantum method is described as the common workhorse?",
                (
                    opt("Density functional theory (DFT)", correct=True),
                    opt("Steepest descent"),
                    opt("Gasteiger charges"),
                    opt("Distance geometry"),
                ),
                "DFT is the widely used quantum workhorse between semi-empirical and post-Hartree-Fock.",
            ),
            q(
                "A QM/MM scheme is useful because it:",
                (
                    opt(
                        "treats a small reactive region with QM and the rest with MM", correct=True
                    ),
                    opt("uses QM for the entire system"),
                    opt("ignores the solvent entirely"),
                    opt("only renders pictures"),
                ),
                "QM/MM combines quantum accuracy locally with cheap MM for the surroundings.",
            ),
        ),
        "Visualizing molecules": (
            q(
                "A cartoon (ribbon) representation is best for showing:",
                (
                    opt("the secondary-structure fold of a protein", correct=True),
                    opt("exact partial charges"),
                    opt("individual hydrogen positions"),
                    opt("the file format"),
                ),
                "Cartoon views abstract the backbone into helices and sheets to show the fold.",
            ),
            q(
                "Space-filling (CPK) representation draws atoms using:",
                (
                    opt("van der Waals radii", correct=True),
                    opt("bond orders only"),
                    opt("residue numbers"),
                    opt("partial charges"),
                ),
                "CPK/space-filling spheres use van der Waals radii to show shape and packing.",
            ),
            q(
                "Which is a molecular visualization tool?",
                (
                    opt("PyMOL", correct=True),
                    opt("AMBER"),
                    opt("RESP"),
                    opt("TIP3P"),
                ),
                "PyMOL, VMD and ChimeraX are viewers; the others are force fields/charge/water models.",
            ),
        ),
    },
    final=(
        q(
            "The potential energy surface maps energy as a function of:",
            (
                opt("atomic positions", correct=True),
                opt("time only"),
                opt("temperature only"),
                opt("pH"),
            ),
            "The PES is E as a function of the atomic coordinates.",
        ),
        q(
            "Which term is NOT a bonded force-field term?",
            (
                opt("Van der Waals", correct=True),
                opt("Bond stretch"),
                opt("Angle bend"),
                opt("Torsion"),
            ),
            "Van der Waals is a non-bonded term; the others are bonded.",
        ),
        q(
            "The Lennard-Jones potential has its minimum where:",
            (
                opt("attraction and repulsion balance", correct=True),
                opt("the distance is zero"),
                opt("the distance is infinite"),
                opt("the charge is zero"),
            ),
            "The LJ well sits where the r^-12 repulsion and r^-6 attraction balance.",
        ),
        q(
            "Quantum methods are needed (over MM) mainly to model:",
            (
                opt("bond breaking and electronic effects", correct=True),
                opt("large systems quickly"),
                opt("simple geometry rendering"),
                opt("file conversion"),
            ),
            "QM captures electrons explicitly, enabling bond breaking and charge transfer.",
        ),
        q(
            "An XYZ file contains:",
            (
                opt("element symbols and coordinates", correct=True),
                opt("explicit bond orders"),
                opt("secondary-structure annotation"),
                opt("partial charges and pKa values"),
            ),
            "XYZ is a bare list of elements and (x,y,z) positions.",
        ),
        q(
            "A surface representation in a viewer is most useful for:",
            (
                opt("revealing binding pockets and shape", correct=True),
                opt("listing atom indices"),
                opt("showing the force-field name"),
                opt("counting iterations"),
            ),
            "Molecular/solvent-accessible surfaces expose pockets and overall shape.",
        ),
    ),
)
