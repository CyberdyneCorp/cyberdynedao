"""Quiz questions for the Multibody Dynamics & Simulation - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is a multibody system?": (
            q(
                "What is a multibody system?",
                (
                    opt("A set of bodies connected by joints and acted on by forces", correct=True),
                    opt("A single particle moving in a straight line"),
                    opt("A static structure that never moves"),
                    opt("A purely thermal system with no motion"),
                ),
                "A multibody system is a collection of rigid or flexible bodies linked by joints under applied forces.",
            ),
            q(
                "How many degrees of freedom does one free rigid body have in 3D?",
                (
                    opt("6", correct=True),
                    opt("3"),
                    opt("1"),
                    opt("12"),
                ),
                "Three translations plus three rotations give 6 DOF in space.",
            ),
            q(
                "Besides motion, what important output does a multibody simulation provide?",
                (
                    opt("Reaction forces in each joint", correct=True),
                    opt("The chemical composition of the bodies"),
                    opt("The electrical resistance of the links"),
                    opt("Nothing beyond the input geometry"),
                ),
                "Joint reaction forces let engineers size bearings and check loads.",
            ),
        ),
        "Rigid bodies, pose and degrees of freedom": (
            q(
                "How many DOF does a single rigid body have in the plane?",
                (
                    opt("3 (x, y, theta)", correct=True),
                    opt("2 (x, y)"),
                    opt("6"),
                    opt("1"),
                ),
                "Planar pose is position (x, y) plus one rotation theta.",
            ),
            q(
                "Why are quaternions often preferred over Euler angles for orientation?",
                (
                    opt("They avoid the gimbal-lock singularity", correct=True),
                    opt("They use fewer numbers than Euler angles"),
                    opt("They eliminate the need for a mass matrix"),
                    opt("They make every body rigid automatically"),
                ),
                "A unit quaternion has no orientation singularity, unlike Euler angles.",
            ),
            q(
                "What does the inertia tensor describe?",
                (
                    opt("How mass is distributed about the rotation axes", correct=True),
                    opt("The total mass only"),
                    opt("The color of the body"),
                    opt("The number of joints attached"),
                ),
                "The inertia tensor generalizes the moment of inertia to 3D rotation.",
            ),
        ),
        "Joints and the constraints they impose": (
            q(
                "How many DOF does a revolute (pin) joint permit between two spatial bodies?",
                (
                    opt("1", correct=True),
                    opt("3"),
                    opt("0"),
                    opt("6"),
                ),
                "A revolute joint allows rotation about one axis only.",
            ),
            q(
                "A spherical (ball) joint permits how many DOF?",
                (
                    opt("3 rotations", correct=True),
                    opt("1 rotation"),
                    opt("2 translations"),
                    opt("0"),
                ),
                "A ball joint allows pure rotation in three directions.",
            ),
            q(
                "Where can a joint carry a reaction force or torque?",
                (
                    opt("In the directions of motion it forbids", correct=True),
                    opt("Only in the directions it permits"),
                    opt("Nowhere - ideal joints carry no reactions"),
                    opt("Only along gravity"),
                ),
                "Reactions act exactly where the joint constrains relative motion.",
            ),
        ),
        "Mobility and the Gruebler-Kutzbach criterion": (
            q(
                "What is the planar mobility of a standard four-bar linkage?",
                (
                    opt("1", correct=True),
                    opt("0"),
                    opt("2"),
                    opt("3"),
                ),
                "M = 3(4-1) - 2(4) = 1, so a single input crank drives it.",
            ),
            q(
                "In the planar Gruebler formula M = 3(n-1) - 2j, what does n include?",
                (
                    opt("All links, including the fixed ground", correct=True),
                    opt("Only the moving links"),
                    opt("Only the joints"),
                    opt("Only the input crank"),
                ),
                "n counts every link, with the ground counted as one link.",
            ),
            q(
                "What does a computed mobility of M = 0 indicate?",
                (
                    opt("A structure with no net motion", correct=True),
                    opt("A mechanism with one input"),
                    opt("An over-constrained frame"),
                    opt("A system with infinite motion"),
                ),
                "M = 0 means the assembly is a rigid structure.",
            ),
        ),
        "Forces, torques and free-body thinking": (
            q(
                "How do joint reactions appear across two connected bodies?",
                (
                    opt("As equal and opposite third-law pairs", correct=True),
                    opt("As identical forces on both bodies"),
                    opt("Only on the heavier body"),
                    opt("They are ignored in free-body diagrams"),
                ),
                "Newton's third law makes joint reactions equal and opposite.",
            ),
            q(
                "A linear spring between two points contributes what force?",
                (
                    opt("F = -k times the change in length", correct=True),
                    opt("A constant force independent of stretch"),
                    opt("A force proportional to velocity only"),
                    opt("No force at all"),
                ),
                "Spring force is -k(l - l0) along its line of action.",
            ),
            q(
                "In a multibody free-body diagram, joint reactions are treated as",
                (
                    opt("unknowns the simulation solves for", correct=True),
                    opt("known applied loads given in advance"),
                    opt("always zero"),
                    opt("equal to gravity"),
                ),
                "Reactions are unknowns determined together with the motion.",
            ),
        ),
        "What a multibody simulation computes": (
            q(
                "What is the main output of a multibody simulation?",
                (
                    opt("A time history of positions, velocities and reactions", correct=True),
                    opt("A single static equilibrium position"),
                    opt("Only the total system mass"),
                    opt("A list of material costs"),
                ),
                "The simulator marches the equations of motion to produce trajectories.",
            ),
            q(
                "Each simulation time step conceptually does which sequence?",
                (
                    opt("Evaluate forces, solve for accelerations, integrate", correct=True),
                    opt("Integrate first, then add the bodies"),
                    opt("Only evaluate forces, never integrate"),
                    opt("Randomly perturb positions"),
                ),
                "Forces -> constrained accelerations -> integration updates the state.",
            ),
            q(
                "Which is a general-purpose or robotics multibody simulation tool?",
                (
                    opt("MSC Adams, Simscape Multibody, Pinocchio or MuJoCo", correct=True),
                    opt("A spreadsheet word processor"),
                    opt("A relational database engine"),
                    opt("An image editor"),
                ),
                "These packages formulate and integrate multibody equations of motion.",
            ),
        ),
    },
    final=(
        q(
            "Which best defines a joint in multibody dynamics?",
            (
                opt(
                    "An idealized connection that permits some motion and forbids the rest",
                    correct=True,
                ),
                opt("A rigid body with mass and inertia"),
                opt("An external applied force"),
                opt("A numerical integration method"),
            ),
            "Joints allow certain relative DOF and impose constraints on the rest.",
        ),
        q(
            "A prismatic (slider) joint between two spatial bodies permits how many DOF?",
            (
                opt("1 translation", correct=True),
                opt("3 rotations"),
                opt("6"),
                opt("0"),
            ),
            "A slider allows translation along one axis only.",
        ),
        q(
            "Using M = 3(n-1) - 2j, the mobility of a slider-crank (n=4, j=4) is",
            (
                opt("1", correct=True),
                opt("0"),
                opt("2"),
                opt("-1"),
            ),
            "3(3) - 2(4) = 1, a single-DOF mechanism.",
        ),
        q(
            "Which orientation representation can suffer gimbal lock?",
            (
                opt("Euler angles", correct=True),
                opt("Unit quaternions"),
                opt("Rotation matrices used with quaternions"),
                opt("Cartesian positions"),
            ),
            "Euler angles lose a DOF at certain orientations; quaternions avoid this.",
        ),
        q(
            "What relation gives a linear damper's force between two points?",
            (
                opt("Proportional to the rate of change of length", correct=True),
                opt("Proportional to the length itself"),
                opt("Constant regardless of motion"),
                opt("Zero unless the bodies touch"),
            ),
            "A linear damper contributes -c times the relative speed along its axis.",
        ),
        q(
            "What does a multibody simulator solve for at each step besides motion?",
            (
                opt("The joint reaction forces", correct=True),
                opt("The ambient temperature"),
                opt("The manufacturing cost"),
                opt("The body colors"),
            ),
            "Reactions are produced alongside the accelerations and trajectories.",
        ),
    ),
)
