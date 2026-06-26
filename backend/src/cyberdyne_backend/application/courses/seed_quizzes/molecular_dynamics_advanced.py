"""Quiz questions for the Molecular Dynamics Simulations - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Free energy: thermodynamic integration & FEP": (
            q(
                "Thermodynamic integration obtains Delta G by:",
                (
                    opt(
                        "integrating <dH/dlambda> over the coupling parameter lambda from 0 to 1",
                        correct=True,
                    ),
                    opt("reading the potential energy of one frame"),
                    opt("averaging the temperature"),
                    opt("counting atoms"),
                ),
                "TI integrates the ensemble-averaged dH/dlambda along the path.",
            ),
            q(
                "Free energy perturbation (Zwanzig) computes Delta G from:",
                (
                    opt(
                        "an exponential average of the energy difference between states",
                        correct=True,
                    ),
                    opt("a linear average of positions"),
                    opt("the kinetic energy alone"),
                    opt("the box volume"),
                ),
                "FEP uses -k_B T ln <exp(-(H_B-H_A)/k_B T)>.",
            ),
            q(
                "BAR and MBAR are used to:",
                (
                    opt("combine information from all lambda windows optimally", correct=True),
                    opt("set the simulation temperature"),
                    opt("build the starting structure"),
                    opt("remove periodic boundaries"),
                ),
                "BAR/MBAR are statistically optimal free-energy estimators.",
            ),
        ),
        "Enhanced sampling: umbrella sampling & metadynamics": (
            q(
                "Enhanced-sampling methods add a bias along chosen:",
                (
                    opt("collective variables (CVs)", correct=True),
                    opt("random atoms only"),
                    opt("time steps"),
                    opt("force-field parameters"),
                ),
                "CVs (distances, dihedrals, etc.) are biased to flatten barriers.",
            ),
            q(
                "Umbrella sampling reconstructs the free-energy profile (PMF) using:",
                (
                    opt("WHAM or MBAR to combine the biased windows", correct=True),
                    opt("a single unbiased run"),
                    opt("the Verlet integrator"),
                    opt("Particle-Mesh Ewald"),
                ),
                "WHAM/MBAR unbias and stitch the windows into a PMF.",
            ),
            q(
                "Metadynamics escapes free-energy wells by:",
                (
                    opt("depositing Gaussian hills of bias into visited regions", correct=True),
                    opt("lowering the temperature to zero"),
                    opt("removing all atoms"),
                    opt("increasing the time step"),
                ),
                "Metadynamics fills wells with history-dependent Gaussian bias.",
            ),
        ),
        "Replica exchange molecular dynamics": (
            q(
                "In replica exchange MD, the multiple replicas typically differ in:",
                (
                    opt("temperature (a temperature ladder)", correct=True),
                    opt("the number of atoms"),
                    opt("the force-field type only"),
                    opt("the file format"),
                ),
                "Standard REMD runs replicas across a temperature ladder.",
            ),
            q(
                "Swaps between neighbouring replicas are accepted using a:",
                (
                    opt("Metropolis criterion that preserves each ensemble", correct=True),
                    opt("rule that always accepts every swap"),
                    opt("rule that never accepts any swap"),
                    opt("random coin flip with no energy dependence"),
                ),
                "A Metropolis acceptance keeps each replica in its correct ensemble.",
            ),
            q(
                "Efficient REMD requires neighbouring replicas to have:",
                (
                    opt("overlapping potential energy distributions", correct=True),
                    opt("identical temperatures"),
                    opt("zero energy"),
                    opt("no interactions at all"),
                ),
                "Energy-distribution overlap is needed for a reasonable swap rate.",
            ),
        ),
        "Trajectory analysis: RMSD, PCA & Markov models": (
            q(
                "RMSF (root-mean-square fluctuation) measures:",
                (
                    opt("per-residue flexibility around the average position", correct=True),
                    opt("the total simulation time"),
                    opt("the box pressure"),
                    opt("the number of water molecules"),
                ),
                "RMSF reports how much each residue fluctuates.",
            ),
            q(
                "Principal component analysis of a trajectory identifies:",
                (
                    opt("large-amplitude collective motions (essential dynamics)", correct=True),
                    opt("the exact bond lengths"),
                    opt("the simulation temperature"),
                    opt("the disk format"),
                ),
                "PCA diagonalises the covariance to find dominant collective motions.",
            ),
            q(
                "A Markov state model estimates kinetics by building a:",
                (
                    opt(
                        "transition matrix between discretised conformational states", correct=True
                    ),
                    opt("single average structure"),
                    opt("force field from scratch"),
                    opt("list of file names"),
                ),
                "MSMs estimate T(tau); its slow eigenvectors reveal kinetics.",
            ),
        ),
        "Machine-learned interatomic potentials": (
            q(
                "Machine-learned interatomic potentials are typically trained on:",
                (
                    opt("ab initio (DFT) energies and forces", correct=True),
                    opt("experimental photographs"),
                    opt("random labels"),
                    opt("only bond connectivity"),
                ),
                "MLIPs learn from quantum-chemistry energies and forces.",
            ),
            q(
                "Modern equivariant graph neural network potentials include:",
                (
                    opt("NequIP, Allegro and MACE", correct=True),
                    opt("GROMACS, NAMD and LAMMPS"),
                    opt("WHAM, MBAR and BAR"),
                    opt("TIP3P, TIP4P and SPC/E"),
                ),
                "NequIP, Allegro and MACE are equivariant GNN potentials.",
            ),
            q(
                "A major advantage of ML potentials over classical force fields is that they can:",
                (
                    opt(
                        "model reactive chemistry such as bond breaking at near-quantum accuracy",
                        correct=True,
                    ),
                    opt("run without any training data"),
                    opt("avoid all symmetry constraints"),
                    opt("eliminate the need for a time step"),
                ),
                "MLIPs reach near-DFT accuracy and can describe bond breaking.",
            ),
        ),
        "Ab initio & QM/MM molecular dynamics": (
            q(
                "Ab initio molecular dynamics differs from classical MD because it:",
                (
                    opt(
                        "computes forces directly from electronic structure each step", correct=True
                    ),
                    opt("uses a fixed empirical force field"),
                    opt("ignores the nuclei"),
                    opt("never integrates in time"),
                ),
                "AIMD evaluates forces from quantum electronic structure on the fly.",
            ),
            q(
                "In QM/MM, the quantum region is usually chosen to be:",
                (
                    opt("a small reactive area such as an enzyme active site", correct=True),
                    opt("the entire solvent box"),
                    opt("a region with no atoms"),
                    opt("randomly selected each step"),
                ),
                "QM treats a small reactive region; MM handles the surroundings.",
            ),
            q(
                "Car-Parrinello MD avoids a full SCF each step by:",
                (
                    opt(
                        "propagating fictitious electronic degrees of freedom with the nuclei",
                        correct=True,
                    ),
                    opt("ignoring the electrons completely"),
                    opt("freezing the nuclei"),
                    opt("using a classical force field"),
                ),
                "CPMD treats electronic variables dynamically to skip per-step SCF.",
            ),
        ),
    },
    final=(
        q(
            "The quantity that determines binding, folding and solubility is the:",
            (
                opt("free energy difference Delta G", correct=True),
                opt("instantaneous potential energy of one frame"),
                opt("number of atoms"),
                opt("integration time step"),
            ),
            "Delta G, which includes entropy, governs these thermodynamic outcomes.",
        ),
        q(
            "A potential of mean force (PMF) is the free energy as a function of:",
            (
                opt("a collective variable", correct=True),
                opt("simulation wall-clock time"),
                opt("the number of CPU cores"),
                opt("the file size"),
            ),
            "A PMF is the free energy profile along a chosen collective variable.",
        ),
        q(
            "Replica exchange improves sampling because high-temperature replicas:",
            (
                opt(
                    "cross barriers easily and pass moves down to cooler replicas via swaps",
                    correct=True,
                ),
                opt("freeze the system in place"),
                opt("remove all interactions"),
                opt("delete the trajectory"),
            ),
            "Hot replicas overcome barriers; accepted swaps share these moves.",
        ),
        q(
            "Markov state models let many short trajectories be combined into:",
            (
                opt("long-timescale kinetics and metastable states", correct=True),
                opt("a single energy-minimised structure"),
                opt("a new force field"),
                opt("a faster integrator"),
            ),
            "MSMs stitch short runs into long-timescale kinetics via T(tau).",
        ),
        q(
            "Active learning in ML interatomic potentials works by:",
            (
                opt("adding new DFT reference points where the model is uncertain", correct=True),
                opt("deleting the training data"),
                opt("lowering the temperature"),
                opt("removing symmetry constraints"),
            ),
            "Active learning queries DFT for high-uncertainty configurations.",
        ),
        q(
            "QM/MM combined with umbrella sampling is the standard approach for:",
            (
                opt("computing enzyme reaction free-energy barriers", correct=True),
                opt("storing trajectory files"),
                opt("rescaling the box volume"),
                opt("drawing molecular cartoons"),
            ),
            "QM/MM plus enhanced sampling yields reaction mechanisms and barriers.",
        ),
    ),
)
