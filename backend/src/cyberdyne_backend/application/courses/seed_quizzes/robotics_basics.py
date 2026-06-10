"""Curated quiz questions for the Robotics - Basics course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each lesson."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Robots, joints & degrees of freedom": (
            q(
                "What does a revolute (R) joint contribute to a manipulator?",
                (
                    opt("A sliding length d along a linear actuator"),
                    opt(
                        "A rotation described by one angle, like an elbow or shoulder", correct=True
                    ),
                    opt("A fixed rigid connection with no motion"),
                    opt("Two independent angles at once"),
                ),
                "A revolute joint rotates and is parameterized by a single angle theta, such as an elbow or shoulder.",
            ),
            q(
                "How many numbers (DOF) does a 6-DOF industrial arm need to fully fix its pose?",
                (
                    opt("3 numbers, all for position"),
                    opt("6 numbers: 3 to position the hand and 3 to orient it", correct=True),
                    opt("2 numbers, one per joint type"),
                    opt("1 number for the whole configuration"),
                ),
                "A 6-DOF arm needs 6 numbers: 3 to position the hand and 3 to orient it.",
            ),
            q(
                "What is the configuration q of a manipulator?",
                (
                    opt(
                        "The list of all joint values, a point in configuration space", correct=True
                    ),
                    opt("The Cartesian position of the end-effector only"),
                    opt("The total mass of all the links"),
                    opt("The number of links minus the number of joints"),
                ),
                "The configuration q is the list of all joint values, which is a single point in configuration space.",
            ),
        ),
        "Rotations & rigid-body transforms": (
            q(
                "What is the 2D rotation matrix R(theta)?",
                (
                    opt("[[cos, sin], [sin, cos]]"),
                    opt("[[cos, -sin], [sin, cos]]", correct=True),
                    opt("[[sin, cos], [-cos, sin]]"),
                    opt("[[1, theta], [0, 1]]"),
                ),
                "R(theta) is [[cos theta, -sin theta], [sin theta, cos theta]], whose columns are the rotated axes.",
            ),
            q(
                "What does a homogeneous transform T in SE(2) or SE(3) carry in one object?",
                (
                    opt("Only the translation vector"),
                    opt("Only the rotation matrix"),
                    opt("Both rotation R and translation p together", correct=True),
                    opt("The joint velocities of the arm"),
                ),
                "A homogeneous transform packs both the rotation R and the translation p into a single matrix.",
            ),
            q(
                "In 3D, why is a quaternion often used to store the rotation?",
                (
                    opt("To make the matrix larger and slower"),
                    opt("To avoid gimbal lock", correct=True),
                    opt("Because SO(3) cannot be represented as a matrix"),
                    opt("To add an extra translation component"),
                ),
                "In 3D the rotation R in SO(3) is often stored as a quaternion to avoid gimbal lock.",
            ),
        ),
        "Forward kinematics: where is the hand?": (
            q(
                "What question does forward kinematics (FK) answer?",
                (
                    opt("Given the joint angles, where is the end-effector?", correct=True),
                    opt("Given the hand position, what joint angles reach it?"),
                    opt("What torques move the arm against gravity?"),
                    opt("Which configurations are singular?"),
                ),
                "FK takes the joint angles and computes where the end-effector is.",
            ),
            q(
                "For the planar 2-link arm, what is the x coordinate of the hand?",
                (
                    opt("l1*cos(theta1) + l2*cos(theta1+theta2)", correct=True),
                    opt("l1*sin(theta1) + l2*sin(theta1+theta2)"),
                    opt("l1*cos(theta1) - l2*sin(theta2)"),
                    opt("(l1+l2)*cos(theta1+theta2)"),
                ),
                "The lesson gives x = l1*cos(theta1) + l2*cos(theta1+theta2) for the 2-link arm.",
            ),
            q(
                "A defining property of forward kinematics is that it is:",
                (
                    opt("Always ambiguous with up to 8 answers"),
                    opt("A unique, well-defined answer", correct=True),
                    opt("Undefined whenever the arm is folded"),
                    opt("Only solvable numerically"),
                ),
                "FK is always a unique, well-defined answer for a given set of joint angles.",
            ),
        ),
        "The workspace & joint limits": (
            q(
                "What shape is the workspace of the 2-link arm with no joint limits?",
                (
                    opt("A full disk centered at the base"),
                    opt("An annulus between an inner and outer radius", correct=True),
                    opt("A single straight line segment"),
                    opt("A square region around the base"),
                ),
                "Without joint limits the 2-link arm reaches an annulus bounded by an inner and an outer radius.",
            ),
            q(
                "What is the outer radius of the 2-link arm workspace?",
                (
                    opt("l1 + l2, with the arm stretched straight", correct=True),
                    opt("|l1 - l2|, with the arm folded back"),
                    opt("l1 * l2"),
                    opt("Half of l1 + l2"),
                ),
                "The outer radius is l1 + l2, reached when the arm is stretched straight.",
            ),
            q(
                "Besides joint limits, what else carves down a real robot workspace?",
                (
                    opt("Self-collision and obstacles the arm must avoid", correct=True),
                    opt("The color of the links"),
                    opt("The order in which joints were assembled"),
                    opt("The choice of programming language"),
                ),
                "Real arms must avoid self-collision and obstacles, which further reduces the reachable region.",
            ),
        ),
        "Lab: forward kinematics in NumPy": (
            q(
                "In the lab, what library provides the trig and array math?",
                (
                    opt("NumPy", correct=True),
                    opt("pandas"),
                    opt("matplotlib"),
                    opt("SciPy"),
                ),
                "The lab imports numpy as np and uses it for the trig and array math.",
            ),
            q(
                "With theta2 = 0 (arm straight) and l1=1.2, l2=1.0, what reach should the lab show?",
                (
                    opt("2.2, equal to l1 + l2", correct=True),
                    opt("0.2, equal to |l1 - l2|"),
                    opt("1.0, equal to l2"),
                    opt("1.2, equal to l1"),
                ),
                "With the arm straight the reach equals l1 + l2 = 2.2.",
            ),
            q(
                "How are the joint angle configs given to the lab before converting them?",
                (
                    opt("In radians directly"),
                    opt("In degrees, then converted with np.deg2rad", correct=True),
                    opt("As Cartesian x,y points"),
                    opt("As quaternions"),
                ),
                "The configs are listed in degrees and converted to radians with np.deg2rad.",
            ),
        ),
    },
    final=(
        q(
            "Which two joint types do almost everything in a manipulator?",
            (
                opt("Revolute and prismatic", correct=True),
                opt("Spherical and planar"),
                opt("Fixed and floating"),
                opt("Helical and cylindrical"),
            ),
            "The course states that revolute (rotating) and prismatic (sliding) joints do almost everything.",
        ),
        q(
            "How do you chain two frames given their transforms T_0^1 and T_1^2?",
            (
                opt("By adding the matrices"),
                opt("By matrix multiplication, T_0^2 = T_0^1 * T_1^2", correct=True),
                opt("By inverting the second transform"),
                opt("By taking the determinant of each"),
            ),
            "Chaining frames is matrix multiplication: T_0^2 = T_0^1 * T_1^2.",
        ),
        q(
            "For the 2-link arm, what is the y coordinate of the end-effector?",
            (
                opt("l1*sin(theta1) + l2*sin(theta1+theta2)", correct=True),
                opt("l1*cos(theta1) + l2*cos(theta1+theta2)"),
                opt("l1*sin(theta1) - l2*cos(theta2)"),
                opt("(l1+l2)*sin(theta2)"),
            ),
            "FK gives y = l1*sin(theta1) + l2*sin(theta1+theta2).",
        ),
        q(
            "What is the inner radius of the 2-link arm reachable annulus?",
            (
                opt("l1 + l2"),
                opt("|l1 - l2|, with the arm folded back", correct=True),
                opt("0, the base point"),
                opt("l1 * l2"),
            ),
            "The inner radius is |l1 - l2|, reached when the arm is folded back.",
        ),
        q(
            "Why is staying away from the workspace boundary desirable for a robot cell?",
            (
                opt("The arm moves faster only at the boundary"),
                opt(
                    "Near the boundary the arm loses dexterity, approaching singularities",
                    correct=True,
                ),
                opt("The boundary is where gravity is strongest"),
                opt("Joint limits do not apply inside the boundary"),
            ),
            "Near the boundary the arm loses dexterity, which is where the singularities of a later lesson occur.",
        ),
    ),
)
