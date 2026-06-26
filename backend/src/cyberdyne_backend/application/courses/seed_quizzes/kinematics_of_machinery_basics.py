"""Quiz questions for the Kinematics & Dynamics of Machinery - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Machines, mechanisms, links and joints": (
            q(
                "What distinguishes a machine from a bare mechanism?",
                (
                    opt("It also transmits significant force and power to do work", correct=True),
                    opt("It has no moving parts"),
                    opt("It always uses gears"),
                    opt("It has exactly two links"),
                ),
                "A machine is a mechanism that transmits meaningful force/power to do useful work.",
            ),
            q(
                "A revolute (pin) joint is a lower pair that allows:",
                (
                    opt("pure rotation, removing two degrees of freedom", correct=True),
                    opt("pure translation only"),
                    opt("both rotation and translation freely"),
                    opt("no relative motion at all"),
                ),
                "A revolute permits one rotational DOF and removes two in the plane (it is a lower pair).",
            ),
            q(
                "A cam-and-follower contact is an example of a:",
                (
                    opt("higher pair with line or point contact", correct=True),
                    opt("lower pair with surface contact"),
                    opt("rigid weld"),
                    opt("ternary link"),
                ),
                "Cam/follower and gear teeth touch along a line or point, making them higher pairs.",
            ),
        ),
        "Mobility and the Gruebler-Kutzbach equation": (
            q(
                "The planar Gruebler-Kutzbach mobility equation is:",
                (
                    opt("M = 3(n-1) - 2 j1 - j2", correct=True),
                    opt("M = 6(n-1) - 2 j1 - j2"),
                    opt("M = 3n - j1 - 2 j2"),
                    opt("M = 2(n-1) - 3 j1"),
                ),
                "Each planar body has 3 DOF; each lower pair removes 2 and each higher pair removes 1.",
            ),
            q(
                "For a standard planar four-bar linkage, the mobility M equals:",
                (
                    opt("1", correct=True),
                    opt("0"),
                    opt("2"),
                    opt("3"),
                ),
                "With n=4, j1=4, j2=0: M = 3(3) - 8 = 1, a single-input constrained mechanism.",
            ),
            q(
                "A mechanism computed to have M = 0 is best described as a:",
                (
                    opt("structure with no motion", correct=True),
                    opt("mechanism needing two inputs"),
                    opt("Grashof crank-rocker"),
                    opt("higher-pair cam"),
                ),
                "M = 0 means no degrees of freedom remain, so it is a (statically determinate) structure.",
            ),
        ),
        "The four-bar linkage and Grashof's criterion": (
            q(
                "Grashof's law states a four-bar has a fully rotating link when:",
                (
                    opt("S + L <= P + Q", correct=True),
                    opt("S + L > P + Q"),
                    opt("S * L = P * Q"),
                    opt("S = L"),
                ),
                "With S, L the shortest and longest links, S + L <= P + Q guarantees a full revolution.",
            ),
            q(
                "In a Grashof linkage where the shortest link is a side link, you get a:",
                (
                    opt("crank-rocker", correct=True),
                    opt("triple-rocker"),
                    opt("double-crank only"),
                    opt("rigid structure"),
                ),
                "Shortest as a side -> crank-rocker; as ground -> double-crank; as coupler -> double-rocker.",
            ),
            q(
                "When S + L = P + Q exactly, the linkage is at a:",
                (
                    opt("change point, able to switch branches", correct=True),
                    opt("permanent dead lock"),
                    opt("non-Grashof triple-rocker"),
                    opt("zero-mobility structure"),
                ),
                "Equality is the change-point case (e.g. parallelogram) where branches can interchange.",
            ),
        ),
        "Transmission angle and mechanical advantage": (
            q(
                "The transmission angle is best kept within roughly:",
                (
                    opt("40 to 140 degrees", correct=True),
                    opt("0 to 10 degrees"),
                    opt("170 to 180 degrees"),
                    opt("exactly 0 degrees"),
                ),
                "Keeping mu between about 40 and 140 deg keeps force transmission efficient.",
            ),
            q(
                "The useful, motion-driving component of the coupler force scales with:",
                (
                    opt("sin(mu)", correct=True),
                    opt("cos(mu)"),
                    opt("tan(mu) squared"),
                    opt("1/mu"),
                ),
                "Useful component ~ sin(mu); the wasted bearing-loading part ~ cos(mu).",
            ),
            q(
                "Mechanical advantage of a linkage becomes very large near a:",
                (
                    opt("toggle (dead-center) position", correct=True),
                    opt("transmission angle of 90 degrees"),
                    opt("change point only"),
                    opt("maximum output velocity"),
                ),
                "Near toggle the output velocity ratio approaches zero, so MA = w_in/w_out grows large.",
            ),
        ),
        "Kinematics versus kinetics": (
            q(
                "Kinematics studies motion by considering:",
                (
                    opt(
                        "position, velocity and acceleration without the causing forces",
                        correct=True,
                    ),
                    opt("only the forces and torques"),
                    opt("material stress and strain"),
                    opt("thermal expansion"),
                ),
                "Kinematics is purely geometric motion; kinetics adds the forces and inertia.",
            ),
            q(
                "The d'Alembert inertia force on an accelerating link of mass m is:",
                (
                    opt("F = -m a", correct=True),
                    opt("F = m / a"),
                    opt("F = m a squared"),
                    opt("F = a / m"),
                ),
                "An accelerating mass exerts an effective inertia force -m*a that the joints must react.",
            ),
            q(
                "Piston inertia forces in a slider-crank grow with engine speed as:",
                (
                    opt("omega squared", correct=True),
                    opt("omega"),
                    opt("the square root of omega"),
                    opt("they are independent of omega"),
                ),
                "Inertia force ~ m r omega^2, so it rises with the square of crank speed.",
            ),
        ),
    },
    final=(
        q(
            "A kinematic pair (joint) is classified by:",
            (
                opt("the relative motion it permits and DOF it removes", correct=True),
                opt("the color of the link"),
                opt("the mass of the link"),
                opt("the material it is made from"),
            ),
            "Joints are classified as lower/higher pairs by permitted motion and removed DOF.",
        ),
        q(
            "Using M = 3(n-1) - 2 j1 - j2, a six-bar with seven revolute joints has mobility:",
            (
                opt("1", correct=True),
                opt("0"),
                opt("2"),
                opt("3"),
            ),
            "M = 3(6-1) - 2(7) - 0 = 15 - 14 = 1, matching a Watt or Stephenson six-bar.",
        ),
        q(
            "A crank-rocker mechanism converts:",
            (
                opt("continuous rotation into oscillation", correct=True),
                opt("oscillation into nothing"),
                opt("translation into translation"),
                opt("rotation into faster rotation only"),
            ),
            "The crank rotates fully while the rocker oscillates back and forth.",
        ),
        q(
            "A negative mobility (M < 0) indicates a structure that is:",
            (
                opt("over-constrained / statically indeterminate", correct=True),
                opt("a normal one-input mechanism"),
                opt("a robot needing many motors"),
                opt("frictionless"),
            ),
            "M < 0 means redundant constraints (over-constrained structure).",
        ),
        q(
            "Force transmission is poor when the transmission angle is near:",
            (
                opt("0 or 180 degrees", correct=True),
                opt("90 degrees"),
                opt("45 degrees"),
                opt("60 degrees"),
            ),
            "Near 0 or 180 deg the useful component sin(mu) vanishes and bearing loads spike.",
        ),
        q(
            "High-speed machinery must be balanced mainly because:",
            (
                opt("unbalanced inertia forces grow with omega squared", correct=True),
                opt("static weight increases with speed"),
                opt("friction disappears at speed"),
                opt("gears stop meshing"),
            ),
            "Inertia (centrifugal) forces ~ omega^2 dominate bearing loads and vibration at speed.",
        ),
    ),
)
