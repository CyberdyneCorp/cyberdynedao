"""Quiz questions for the Molecular Dynamics Simulations - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Statistical ensembles in MD": (
            q(
                "Plain Newtonian MD that conserves total energy samples which ensemble?",
                (
                    opt("microcanonical (NVE)", correct=True),
                    opt("canonical (NVT)"),
                    opt("isothermal-isobaric (NPT)"),
                    opt("grand canonical (muVT)"),
                ),
                "Energy-conserving Newtonian dynamics gives the NVE ensemble.",
            ),
            q(
                "The ergodic hypothesis allows us to replace an ensemble average with:",
                (
                    opt("a time average over one long trajectory", correct=True),
                    opt("a single instantaneous snapshot"),
                    opt("the potential energy alone"),
                    opt("a random number"),
                ),
                "Ergodicity equates the long-time average with the ensemble average.",
            ),
            q(
                "To simulate at fixed N, P and T you use the:",
                (
                    opt("NPT ensemble with a thermostat and a barostat", correct=True),
                    opt("NVE ensemble with no coupling"),
                    opt("microcanonical ensemble"),
                    opt("muVT ensemble only"),
                ),
                "NPT fixes N, P, T using both a thermostat and a barostat.",
            ),
        ),
        "Thermostats: controlling temperature": (
            q(
                "Why is the Berendsen thermostat unsuitable for production sampling?",
                (
                    opt(
                        "it suppresses fluctuations and does not give a true canonical ensemble",
                        correct=True,
                    ),
                    opt("it makes the system explode immediately"),
                    opt("it cannot reach the target temperature"),
                    opt("it requires quantum mechanics"),
                ),
                "Berendsen damps fluctuations, so it is not a correct NVT generator.",
            ),
            q(
                "Which thermostats DO generate a correct canonical (NVT) ensemble?",
                (
                    opt("Nose-Hoover and velocity-rescale (v-rescale/CSVR)", correct=True),
                    opt("only simple Berendsen coupling"),
                    opt("no thermostat can"),
                    opt("only velocity zeroing"),
                ),
                "Nose-Hoover and v-rescale reproduce the canonical distribution.",
            ),
            q(
                "Langevin dynamics controls temperature by coupling each atom to:",
                (
                    opt("a friction term plus a random force (a stochastic bath)", correct=True),
                    opt("a fixed external magnetic field"),
                    opt("the box volume only"),
                    opt("the electronic wavefunction"),
                ),
                "Langevin adds friction and random forces representing a heat bath.",
            ),
        ),
        "Barostats & periodic boundary conditions": (
            q(
                "Pressure in MD is computed from the temperature term plus the:",
                (
                    opt("virial of the interatomic forces", correct=True),
                    opt("total mass of the system"),
                    opt("number of time steps"),
                    opt("disk usage"),
                ),
                "P combines the ideal-gas (kinetic) term with the force virial.",
            ),
            q(
                "Periodic boundary conditions are used in MD primarily to:",
                (
                    opt("eliminate artificial surfaces by tiling the box", correct=True),
                    opt("make the simulation run slower"),
                    opt("remove all electrostatics"),
                    opt("fix the temperature"),
                ),
                "PBC tiles the box infinitely, avoiding edge/surface artifacts.",
            ),
            q(
                "The minimum-image convention requires the cutoff to be:",
                (
                    opt("less than half the box length", correct=True),
                    opt("greater than the box length"),
                    opt("exactly equal to the box length"),
                    opt("zero"),
                ),
                "Cutoff < L/2 ensures an atom sees only one image of each neighbour.",
            ),
        ),
        "Long-range electrostatics: Particle-Mesh Ewald": (
            q(
                "Ewald summation splits the Coulomb energy into:",
                (
                    opt(
                        "a short-range real-space part and a long-range reciprocal-space part",
                        correct=True,
                    ),
                    opt("a bonded part and an angle part"),
                    opt("kinetic and potential energy"),
                    opt("two identical halves"),
                ),
                "Ewald separates real-space (screened) and reciprocal-space sums.",
            ),
            q(
                "Particle-Mesh Ewald reduces the cost of electrostatics from O(N^2) to:",
                (
                    opt("O(N log N) using an FFT on a charge grid", correct=True),
                    opt("O(N^3)"),
                    opt("O(2^N)"),
                    opt("O(1) regardless of N"),
                ),
                "PME interpolates charges onto a grid and uses the FFT for O(N log N).",
            ),
            q(
                "The complementary error function erfc(alpha r) in Ewald serves to:",
                (
                    opt("damp the real-space term so a cutoff can be used", correct=True),
                    opt("amplify long-range forces"),
                    opt("remove all charges"),
                    opt("set the temperature"),
                ),
                "erfc damps the short-range part so it converges within a cutoff.",
            ),
        ),
        "Solvation: explicit & implicit water": (
            q(
                "TIP3P, TIP4P and SPC/E are examples of:",
                (
                    opt("explicit water models", correct=True),
                    opt("implicit solvent theories"),
                    opt("thermostats"),
                    opt("integrators"),
                ),
                "These are rigid point-charge explicit water models.",
            ),
            q(
                "Implicit solvation (e.g. Generalized Born) represents water as:",
                (
                    opt("a continuum dielectric, no explicit molecules", correct=True),
                    opt("thousands of explicit molecules"),
                    opt("a vacuum with no effect"),
                    opt("a crystalline solid"),
                ),
                "Implicit models use a dielectric continuum plus a surface term.",
            ),
            q(
                "A drawback of implicit solvation compared with explicit water is that it:",
                (
                    opt("loses specific water-mediated contacts and hydrodynamics", correct=True),
                    opt("is far slower"),
                    opt("requires more atoms"),
                    opt("cannot reach equilibrium ever"),
                ),
                "Implicit water is cheap but misses specific waters and viscosity.",
            ),
        ),
        "Equilibration & the production workflow": (
            q(
                "What is the purpose of energy minimisation before dynamics?",
                (
                    opt("to remove bad steric contacts before integrating", correct=True),
                    opt("to set the final production temperature"),
                    opt("to compute the free energy"),
                    opt("to delete water molecules"),
                ),
                "Minimisation relaxes clashes so dynamics does not blow up.",
            ),
            q(
                "Why are position restraints applied during the heating stage?",
                (
                    opt("to keep the solute structure intact while solvent relaxes", correct=True),
                    opt("to freeze the entire system permanently"),
                    opt("to increase the temperature faster"),
                    opt("to remove electrostatics"),
                ),
                "Restraints hold the solute while velocities and solvent equilibrate.",
            ),
            q(
                "Observables for analysis should be averaged over which segment?",
                (
                    opt("the production run, after equilibration", correct=True),
                    opt("the minimisation steps"),
                    opt("the heating phase only"),
                    opt("the first picosecond before equilibration"),
                ),
                "Only the equilibrated production segment gives valid averages.",
            ),
        ),
    },
    final=(
        q(
            "Which ensemble fixes the chemical potential and exchanges particles?",
            (
                opt("grand canonical (muVT)", correct=True),
                opt("microcanonical (NVE)"),
                opt("canonical (NVT)"),
                opt("isothermal-isobaric (NPT)"),
            ),
            "The grand canonical ensemble holds muVT and allows particle exchange.",
        ),
        q(
            "Which combination correctly produces the NVT ensemble?",
            (
                opt("Nose-Hoover or v-rescale thermostat at fixed volume", correct=True),
                opt("Berendsen thermostat (true canonical)"),
                opt("no thermostat at all"),
                opt("a barostat alone"),
            ),
            "Correct NVT needs a canonical thermostat such as Nose-Hoover/v-rescale.",
        ),
        q(
            "Parrinello-Rahman and Monte Carlo barostats are preferred over Berendsen because they:",
            (
                opt("give correct NPT volume fluctuations", correct=True),
                opt("are simpler with no parameters"),
                opt("remove the need for a thermostat"),
                opt("eliminate periodic boundaries"),
            ),
            "They reproduce proper NPT fluctuations; Berendsen damps them.",
        ),
        q(
            "Particle-Mesh Ewald is the standard method for handling:",
            (
                opt("long-range electrostatics under periodic boundaries", correct=True),
                opt("bond constraints"),
                opt("temperature control"),
                opt("trajectory storage"),
            ),
            "PME efficiently evaluates periodic Coulomb interactions.",
        ),
        q(
            "Counter-ions such as Na+ and Cl- are added to an explicit-solvent box to:",
            (
                opt("neutralise net charge and set ionic strength", correct=True),
                opt("increase the temperature"),
                opt("remove water molecules"),
                opt("speed up the integrator"),
            ),
            "Ions neutralise charge and reproduce physiological ionic strength.",
        ),
        q(
            "Which is a valid convergence check during equilibration?",
            (
                opt(
                    "temperature, energy and density stabilising and RMSD plateauing", correct=True
                ),
                opt("the file name length"),
                opt("the number of CPU cores"),
                opt("the color of the rendering"),
            ),
            "Stable T, energy, density and a plateaued RMSD indicate equilibration.",
        ),
    ),
)
