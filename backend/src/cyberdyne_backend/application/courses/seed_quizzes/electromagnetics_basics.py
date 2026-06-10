from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Electric charge & fields": (
            q(
                "How does the Coulomb force between two point charges change with their separation r?",
                (
                    opt("It is constant, independent of r"),
                    opt("It falls off as 1/r"),
                    opt("It falls off as the inverse square, 1/r^2", correct=True),
                    opt("It grows linearly with r"),
                ),
                "Coulomb's law has the force proportional to q1 q2 / r^2, an inverse-square fall-off.",
            ),
            q(
                "By Gauss's law, the electric flux through a closed surface depends on what?",
                (
                    opt("The total charge enclosed inside the surface", correct=True),
                    opt("Only charges outside the surface"),
                    opt("The surface area alone"),
                    opt("The distance to the nearest charge"),
                ),
                "Gauss's law states the closed-surface flux equals Q_enc divided by epsilon_0.",
            ),
            q(
                "How does the electric field fall off with distance for an infinite sheet of charge?",
                (
                    opt("As 1/r^2, like a point charge"),
                    opt("As 1/r, like a line charge"),
                    opt("It stays constant with distance", correct=True),
                    opt("It increases with distance"),
                ),
                "An infinite sheet gives a field that is constant with distance, unlike point (1/r^2) or line (1/r).",
            ),
        ),
        "Electric potential & capacitance": (
            q(
                "What is the relationship between the electric field and the potential?",
                (
                    opt(
                        "E is the negative gradient of V, the downhill slope of potential",
                        correct=True,
                    ),
                    opt("E is the integral of V over all space"),
                    opt("E equals V divided by the charge"),
                    opt("E is the time derivative of V"),
                ),
                "The field is the negative gradient of potential, E = -grad V, so it points downhill in V.",
            ),
            q(
                "For a parallel-plate capacitor, how does capacitance change as the gap d shrinks?",
                (
                    opt("Capacitance decreases"),
                    opt("Capacitance increases", correct=True),
                    opt("Capacitance stays the same"),
                    opt("Capacitance becomes negative"),
                ),
                "C = epsilon_0 A / d, so a thinner gap (smaller d) gives larger capacitance.",
            ),
            q(
                "How much energy is stored in a capacitor of capacitance C charged to voltage V?",
                (
                    opt("C V"),
                    opt("Q / V"),
                    opt("One half C V squared", correct=True),
                    opt("epsilon_0 A / d"),
                ),
                "The stored energy is U = (1/2) C V^2 = (1/2) Q V = Q^2 / (2C).",
            ),
        ),
        "Magnetic fields: Biot-Savart, Ampere & forces": (
            q(
                "Why do magnetic field lines form closed loops?",
                (
                    opt("Because there are no magnetic monopoles", correct=True),
                    opt("Because magnetic charge is quantized"),
                    opt("Because current always flows in circles"),
                    opt("Because the field is electrostatic"),
                ),
                "Unlike electric field lines, B lines close on themselves since no magnetic monopoles exist.",
            ),
            q(
                "How does the magnetic field of a long straight wire vary with distance r from the wire?",
                (
                    opt("As 1/r^2"),
                    opt("As 1/r", correct=True),
                    opt("Constant with r"),
                    opt("Proportional to r"),
                ),
                "A long straight wire gives B = mu_0 I / (2 pi r), which falls off as 1/r.",
            ),
            q(
                "What is a key property of the magnetic force on a moving charge?",
                (
                    opt("It is parallel to the velocity"),
                    opt("It does no work and only steers the charge", correct=True),
                    opt("It always speeds the charge up"),
                    opt("It is independent of the field B"),
                ),
                "The Lorentz force q v x B is perpendicular to v, so it does no work and only changes direction.",
            ),
        ),
        "Electromagnetic induction: Faraday, Lenz & inductance": (
            q(
                "According to Faraday's law, what induces a voltage in a loop?",
                (
                    opt("A constant magnetic field through the loop"),
                    opt("A changing magnetic flux through the loop", correct=True),
                    opt("A static charge near the loop"),
                    opt("A steady current in the loop"),
                ),
                "Faraday's law gives EMF = -d(Phi_B)/dt, so a changing flux induces a voltage.",
            ),
            q(
                "What does the minus sign in Faraday's law, known as Lenz's law, mean?",
                (
                    opt("The induced current opposes the change that made it", correct=True),
                    opt("The induced current reinforces the change"),
                    opt("The flux is always negative"),
                    opt("Voltage is measured backwards"),
                ),
                "Lenz's law: the induced current flows to oppose the change in flux, enforcing energy conservation.",
            ),
            q(
                "For a transformer, how do secondary and primary voltages relate to the turns?",
                (
                    opt("Vs/Vp equals Ns/Np, the turns ratio", correct=True),
                    opt("Vs/Vp equals Np/Ns"),
                    opt("Vs/Vp equals the current ratio Is/Ip"),
                    opt("Vs equals Vp regardless of turns"),
                ),
                "The voltage ratio equals the turns ratio: Vs/Vp = Ns/Np, while currents scale inversely.",
            ),
        ),
        "Materials: dielectrics, conductors & boundaries": (
            q(
                "What happens when a dielectric of relative permittivity eps_r fills a capacitor gap?",
                (
                    opt("Capacitance is divided by eps_r"),
                    opt("Capacitance is multiplied by eps_r", correct=True),
                    opt("Capacitance is unchanged"),
                    opt("The capacitor stops storing charge"),
                ),
                "A dielectric polarizes and partly cancels the field, multiplying capacitance by eps_r.",
            ),
            q(
                "Inside a conductor in electrostatic equilibrium, what is true of the field and charge?",
                (
                    opt(
                        "The internal field is zero and excess charge sits on the surface",
                        correct=True,
                    ),
                    opt("The field is strongest at the center"),
                    opt("Charge spreads uniformly through the volume"),
                    opt("The field equals the external field everywhere"),
                ),
                "Charges rearrange until the internal field is zero, leaving excess charge on the surface (Faraday cage).",
            ),
            q(
                "Which class of magnetic material has a relative permeability that is huge, in the hundreds to thousands?",
                (
                    opt("Diamagnetic, such as copper"),
                    opt("Paramagnetic, such as aluminum"),
                    opt("Ferromagnetic, such as iron or ferrite", correct=True),
                    opt("Vacuum"),
                ),
                "Ferromagnets like iron and ferrite have huge mu_r and concentrate flux in motor and transformer cores.",
            ),
        ),
        "Lab: field & potential of point charges": (
            q(
                "In the lab, what two charges are placed to model a dipole?",
                (
                    opt("Two equal positive charges"),
                    opt("A +Q on the left and a -Q on the right", correct=True),
                    opt("A single point charge at the origin"),
                    opt("Two negative charges of different size"),
                ),
                "The lab sets charges (+1e-9 at x=-1) and (-1e-9 at x=+1), a classic dipole.",
            ),
            q(
                "Why does the lab add a tiny term like 1e-9 to the distance r in the denominator?",
                (
                    opt("To avoid divide-by-zero at the charge locations", correct=True),
                    opt("To convert to SI units"),
                    opt("To scale the plot axes"),
                    opt("To normalize the field arrows"),
                ),
                "Adding 1e-9 to r prevents division by zero when a grid point lands on a charge.",
            ),
            q(
                "What does the lab do to the field components before drawing the quiver arrows?",
                (
                    opt("It normalizes them so the direction is visible everywhere", correct=True),
                    opt("It squares them"),
                    opt("It sets them all to zero"),
                    opt("It integrates them over the grid"),
                ),
                "The field is divided by its magnitude (Ux = Ex/mag) so arrow direction shows even where E is weak.",
            ),
        ),
    },
    final=(
        q(
            "Which fall-off law correctly pairs a source with its electric field?",
            (
                opt("Point charge field goes as 1/r"),
                opt("Infinite sheet field goes as 1/r^2"),
                opt(
                    "Point charge field goes as 1/r^2 and an infinite sheet field is constant",
                    correct=True,
                ),
                opt("Line charge field is constant with distance"),
            ),
            "A point charge gives 1/r^2, a line gives 1/r, and an infinite sheet gives a constant field.",
        ),
        q(
            "Which statement about magnetism and induction is correct?",
            (
                opt("A steady current induces a voltage in a nearby loop"),
                opt(
                    "The magnetic force q v x B does no work and only steers the charge",
                    correct=True,
                ),
                opt("Magnetic field lines start and end on magnetic monopoles"),
                opt("A long wire's field grows as r increases"),
            ),
            "The Lorentz magnetic force is perpendicular to velocity so it does no work; B lines close on themselves.",
        ),
        q(
            "What distinguishes the electric potential V from the electric field E?",
            (
                opt("V is the energy per unit charge and E is its negative gradient", correct=True),
                opt("V is the force per unit charge and E is the energy"),
                opt("V falls off as 1/r^2 while E falls off as 1/r"),
                opt("V and E are the same quantity"),
            ),
            "Potential is potential energy per unit charge; the field is the negative gradient of V.",
        ),
        q(
            "A dielectric with eps_r and a step-down transformer respectively do what?",
            (
                opt("The dielectric divides capacitance; the transformer raises voltage"),
                opt(
                    "The dielectric multiplies capacitance by eps_r; the transformer lowers voltage when Ns is less than Np",
                    correct=True,
                ),
                opt("Both leave their quantities unchanged"),
                opt(
                    "The dielectric removes stored charge; the transformer doubles current and voltage"
                ),
            ),
            "A dielectric multiplies C by eps_r; a transformer with fewer secondary turns (Ns < Np) steps voltage down.",
        ),
        q(
            "Why is the inside of a metal box (a Faraday cage) shielded from external electric fields?",
            (
                opt("Because the metal stores all charge in its volume"),
                opt("Because charges rearrange so the internal field is zero", correct=True),
                opt("Because metals have a huge permittivity"),
                opt("Because the box reflects all field lines outward by magnetism"),
            ),
            "In electrostatic equilibrium free charge moves to the surface, making the interior field zero.",
        ),
    ),
)
