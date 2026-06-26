"""Quiz questions for the Fluid Mechanics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is a fluid? The continuum hypothesis": (
            q(
                "What distinguishes a fluid from a solid?",
                (
                    opt("A fluid deforms continuously under any shear stress", correct=True),
                    opt("A fluid cannot transmit pressure"),
                    opt("A fluid has no mass"),
                    opt("A fluid always has higher density than a solid"),
                ),
                "A fluid cannot resist shear at rest; it keeps deforming as long as shear is applied.",
            ),
            q(
                "The continuum hypothesis is valid when the Knudsen number is:",
                (
                    opt("much less than 1", correct=True),
                    opt("much greater than 1"),
                    opt("exactly equal to 1"),
                    opt("negative"),
                ),
                "Kn = lambda/L << 1 means the molecular mean free path is tiny compared to the scale of interest.",
            ),
            q(
                "Which statement about liquids and gases is correct?",
                (
                    opt(
                        "Both are fluids; gases are far more compressible than liquids",
                        correct=True,
                    ),
                    opt("Only liquids are fluids"),
                    opt("Only gases are fluids"),
                    opt("Liquids are more compressible than gases"),
                ),
                "Liquids and gases are both fluids; the main difference is compressibility.",
            ),
        ),
        "Fluid properties: density, viscosity, surface tension": (
            q(
                "Newton's law of viscosity relates shear stress to:",
                (
                    opt("the velocity gradient du/dy", correct=True),
                    opt("the absolute velocity u"),
                    opt("the pressure"),
                    opt("the density only"),
                ),
                "tau = mu (du/dy): shear stress is proportional to the strain rate.",
            ),
            q(
                "Kinematic viscosity nu is defined as:",
                (
                    opt("mu / rho", correct=True),
                    opt("mu * rho"),
                    opt("rho / mu"),
                    opt("mu * g"),
                ),
                "Kinematic viscosity is dynamic viscosity divided by density, nu = mu/rho.",
            ),
            q(
                "The pressure jump across a spherical droplet of radius R is:",
                (
                    opt("2 sigma / R", correct=True),
                    opt("sigma / R"),
                    opt("sigma R"),
                    opt("4 sigma R"),
                ),
                "Young-Laplace for a sphere gives delta p = 2 sigma / R.",
            ),
        ),
        "Hydrostatic pressure and manometry": (
            q(
                "In a constant-density liquid, gauge pressure with depth h is:",
                (
                    opt("rho g h", correct=True),
                    opt("rho g / h"),
                    opt("h / (rho g)"),
                    opt("rho / (g h)"),
                ),
                "Integrating dp/dz = -rho g gives p = p0 + rho g h.",
            ),
            q(
                "The hydrostatic paradox states that pressure at a given depth:",
                (
                    opt("is independent of the container shape", correct=True),
                    opt("depends on the total weight of liquid"),
                    opt("is larger in a wider tank"),
                    opt("depends on the surface area"),
                ),
                "Pressure depends only on depth and density, not on the vessel shape.",
            ),
            q(
                "Gauge pressure is related to absolute pressure by:",
                (
                    opt("p_gauge = p_abs - p_atm", correct=True),
                    opt("p_gauge = p_abs + p_atm"),
                    opt("p_gauge = p_atm - p_abs"),
                    opt("p_gauge = p_abs * p_atm"),
                ),
                "Gauge pressure is measured relative to atmospheric pressure.",
            ),
        ),
        "Forces on submerged surfaces and buoyancy": (
            q(
                "The resultant hydrostatic force on a flat submerged plate is:",
                (
                    opt("rho g h_c A, using the centroid depth", correct=True),
                    opt("rho g h_max A"),
                    opt("zero"),
                    opt("rho g A only"),
                ),
                "F_R = p_c A = rho g h_c A, with h_c the depth of the centroid.",
            ),
            q(
                "The centre of pressure on a vertical surface lies:",
                (
                    opt("below the centroid", correct=True),
                    opt("above the centroid"),
                    opt("exactly at the centroid"),
                    opt("at the free surface"),
                ),
                "Because pressure grows with depth, the resultant acts below the centroid.",
            ),
            q(
                "Archimedes' principle says the buoyant force equals:",
                (
                    opt("the weight of the displaced fluid", correct=True),
                    opt("the weight of the body"),
                    opt("the volume of the body"),
                    opt("the surface area times pressure"),
                ),
                "F_B = rho_fluid g V_disp, the weight of the fluid displaced.",
            ),
        ),
        "Flow kinematics: streamlines, steady vs unsteady": (
            q(
                "A flow is steady when:",
                (
                    opt("the partial time derivative is zero everywhere", correct=True),
                    opt("the velocity is zero"),
                    opt("the density is constant"),
                    opt("streamlines are straight"),
                ),
                "Steady means d/dt = 0 at every fixed point in the field.",
            ),
            q(
                "Streamlines, pathlines and streaklines coincide:",
                (
                    opt("only in steady flow", correct=True),
                    opt("only in unsteady flow"),
                    opt("never"),
                    opt("only for compressible flow"),
                ),
                "In steady flow the three families of curves are identical.",
            ),
            q(
                "The convective acceleration term lets a particle accelerate when:",
                (
                    opt(
                        "it moves into a region of different velocity, even in steady flow",
                        correct=True,
                    ),
                    opt("only the flow is unsteady"),
                    opt("the density changes"),
                    opt("the pressure is zero"),
                ),
                "The (u . grad)u term gives acceleration through a nozzle even when the flow is steady.",
            ),
        ),
    },
    final=(
        q(
            "A Newtonian fluid is one whose shear stress is:",
            (
                opt("linearly proportional to the strain rate", correct=True),
                opt("independent of the strain rate"),
                opt("proportional to the square of the strain rate"),
                opt("proportional to pressure"),
            ),
            "Newtonian: tau = mu (du/dy), a linear stress-strain-rate relation.",
        ),
        q(
            "Pressure in a static fluid increases with depth as:",
            (
                opt("p = p0 + rho g h", correct=True),
                opt("p = p0 - rho g h"),
                opt("p = p0 / (rho g h)"),
                opt("p = p0 rho g h"),
            ),
            "Hydrostatics gives p = p0 + rho g h below the surface.",
        ),
        q(
            "A body floats when:",
            (
                opt("the buoyant force equals its weight", correct=True),
                opt("its density equals atmospheric pressure"),
                opt("it displaces no fluid"),
                opt("the buoyant force is zero"),
            ),
            "Floating equilibrium: F_B = weight, with F_B = rho_fluid g V_disp.",
        ),
        q(
            "Kinematic viscosity has units of:",
            (
                opt("m^2/s", correct=True),
                opt("Pa.s"),
                opt("kg/m^3"),
                opt("N/m"),
            ),
            "nu = mu/rho has units of m^2/s; dynamic viscosity mu is in Pa.s.",
        ),
        q(
            "Surface tension is responsible for:",
            (
                opt("capillary rise and the pressure jump across a curved interface", correct=True),
                opt("the linear pressure-depth relation"),
                opt("turbulent mixing"),
                opt("buoyancy"),
            ),
            "Surface tension drives capillary rise and the Young-Laplace pressure jump.",
        ),
        q(
            "The Eulerian description of a flow records:",
            (
                opt("the velocity field at fixed points in space", correct=True),
                opt("the trajectory of each labelled particle"),
                opt("only the average speed"),
                opt("the molecular positions"),
            ),
            "Eulerian uses u(x,y,z,t) at fixed points; Lagrangian follows particles.",
        ),
    ),
)
