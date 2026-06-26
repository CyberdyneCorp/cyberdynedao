"""Quiz questions for the Robot Manipulators & Industrial Robotics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Anatomy of a robot manipulator": (
            q(
                "What are the two most common industrial joint types?",
                (
                    opt("Revolute and prismatic", correct=True),
                    opt("Spherical and planar"),
                    opt("Magnetic and hydraulic"),
                    opt("Fixed and floating"),
                ),
                "Almost every industrial joint is revolute (rotates) or prismatic (slides).",
            ),
            q(
                "How many degrees of freedom are needed to reach an arbitrary position and orientation in 3-D space?",
                (
                    opt("Three"),
                    opt("Four"),
                    opt("Six", correct=True),
                    opt("Nine"),
                ),
                "Six DoF span all of position (3) and orientation (3) in space.",
            ),
            q(
                "What is the robot's configuration?",
                (
                    opt("The set of joint variables q", correct=True),
                    opt("The tool position only"),
                    opt("The base mounting bolts"),
                    opt("The motor voltages"),
                ),
                "The configuration is the vector of joint variables; the pose is the tool position/orientation.",
            ),
        ),
        "Industrial robot morphologies": (
            q(
                "Which morphology is the classic anthropomorphic 6R arm?",
                (
                    opt("SCARA"),
                    opt("Articulated", correct=True),
                    opt("Cartesian gantry"),
                    opt("Delta"),
                ),
                "An articulated arm uses six revolute joints for a large, dexterous workspace.",
            ),
            q(
                "What is the SCARA robot especially good at?",
                (
                    opt("Six-axis welding in any orientation"),
                    opt("Fast horizontal pick-and-place and assembly", correct=True),
                    opt("Heavy machining over large flat areas"),
                    opt("Tilting the tool to arbitrary angles"),
                ),
                "SCARA is stiff vertically and compliant horizontally, ideal for fast assembly.",
            ),
            q(
                "Why are delta robots fast?",
                (
                    opt("They have the longest links"),
                    opt("Parallel closed-chain arms move a very light platform", correct=True),
                    opt("They use hydraulic actuators"),
                    opt("They have only one motor"),
                ),
                "A delta's parallel arms drive a light platform, enabling very high speed and acceleration.",
            ),
        ),
        "Workspace and degrees of freedom": (
            q(
                "What is the dexterous workspace?",
                (
                    opt("Positions reachable in every orientation", correct=True),
                    opt("All positions reachable in some orientation"),
                    opt("The space behind the robot base"),
                    opt("The set of joint limits"),
                ),
                "The dexterous workspace is the (smaller) set of positions reachable in any orientation.",
            ),
            q(
                "For a planar 2-link arm with lengths l1 and l2, the reachable distance from the base ranges between:",
                (
                    opt("0 and l1"),
                    opt("|l1 - l2| and l1 + l2", correct=True),
                    opt("l1 and l2"),
                    opt("l1*l2 and l1 + l2"),
                ),
                "The reach is an annulus from |l1 - l2| (folded) to l1 + l2 (stretched).",
            ),
            q(
                "A robot with more DoF than the task requires is called:",
                (
                    opt("Under-actuated"),
                    opt("Redundant", correct=True),
                    opt("Singular"),
                    opt("Decoupled"),
                ),
                "Extra DoF beyond the task make the robot redundant, with many configurations per pose.",
            ),
        ),
        "Rigid-body pose and homogeneous transforms": (
            q(
                "What two parts make up a rigid-body pose?",
                (
                    opt("A rotation R and a translation p", correct=True),
                    opt("A mass and an inertia"),
                    opt("A velocity and an acceleration"),
                    opt("Two angles only"),
                ),
                "A pose is a rotation matrix R plus a translation vector p, packed in a 4x4 transform.",
            ),
            q(
                "How do you compose two homogeneous transforms?",
                (
                    opt("Add them"),
                    opt("Multiply the 4x4 matrices", correct=True),
                    opt("Take their average"),
                    opt("Subtract translations only"),
                ),
                "Transforms compose by matrix multiplication: frame 2 in base = T1 @ T2.",
            ),
            q(
                "The inverse of a homogeneous transform with rotation R and translation p has:",
                (
                    opt("Rotation R^T and translation -R^T p", correct=True),
                    opt("Rotation R and translation -p"),
                    opt("Rotation -R and translation p"),
                    opt("The same R and p"),
                ),
                "The inverse uses R transpose and translation -R^T p, cheap to compute.",
            ),
        ),
        "Rotations and orientation": (
            q(
                "Which orientation representation suffers from gimbal lock?",
                (
                    opt("Rotation matrix"),
                    opt("Unit quaternion"),
                    opt("Euler / roll-pitch-yaw angles", correct=True),
                    opt("Axis-angle"),
                ),
                "Euler angles lose a degree of freedom (gimbal lock) when two axes align.",
            ),
            q(
                "Why are unit quaternions preferred for storing and interpolating orientation?",
                (
                    opt("They use only two numbers"),
                    opt("No gimbal lock and numerically stable, with smooth slerp", correct=True),
                    opt("They are easier for humans to read"),
                    opt("They cannot represent rotation"),
                ),
                "Quaternions avoid gimbal lock, stay stable, and interpolate smoothly via slerp.",
            ),
            q(
                "Which formula builds a rotation matrix from an axis and angle?",
                (
                    opt("The law of cosines"),
                    opt("Rodrigues' formula", correct=True),
                    opt("Bayes' rule"),
                    opt("The chain rule"),
                ),
                "Rodrigues' formula constructs R from a unit axis and rotation angle.",
            ),
        ),
        "From joint angles to tool position": (
            q(
                "Mapping joint angles to the tool pose is called:",
                (
                    opt("Forward kinematics", correct=True),
                    opt("Inverse kinematics"),
                    opt("Inverse dynamics"),
                    opt("Trajectory planning"),
                ),
                "Forward kinematics maps configuration to pose; it is always unique.",
            ),
            q(
                "For a planar 2-link arm, the tool x is l1*cos(t1) + l2*cos(t1+t2). This shows forward kinematics is:",
                (
                    opt("Always ambiguous"),
                    opt("A unique, well-defined map", correct=True),
                    opt("Impossible to compute"),
                    opt("Independent of the angles"),
                ),
                "Each configuration maps to exactly one pose, so forward kinematics is unique.",
            ),
            q(
                "Compared with forward kinematics, inverse kinematics is harder because it:",
                (
                    opt("Always has exactly one solution"),
                    opt("Can have multiple solutions, none, or infinitely many", correct=True),
                    opt("Requires no trigonometry"),
                    opt("Does not depend on link lengths"),
                ),
                "Inverse kinematics may have several solutions, no solution, or infinitely many.",
            ),
        ),
    },
    final=(
        q(
            "Which joint type has an angle as its variable?",
            (
                opt("Prismatic"),
                opt("Revolute", correct=True),
                opt("Spherical"),
                opt("Fixed"),
            ),
            "A revolute joint rotates and its variable is an angle; a prismatic joint slides.",
        ),
        q(
            "How many degrees of freedom give full position and orientation control in space?",
            (
                opt("Three"),
                opt("Five"),
                opt("Six", correct=True),
                opt("Twelve"),
            ),
            "Six DoF cover three for position and three for orientation.",
        ),
        q(
            "Which robot morphology uses three orthogonal linear axes?",
            (
                opt("Articulated"),
                opt("Cartesian / gantry", correct=True),
                opt("Delta"),
                opt("SCARA"),
            ),
            "A Cartesian gantry uses three orthogonal prismatic axes (PPP).",
        ),
        q(
            "Homogeneous transforms are powerful because they:",
            (
                opt("Compose by matrix multiplication", correct=True),
                opt("Require no rotation part"),
                opt("Only work in 2-D"),
                opt("Cannot be inverted"),
            ),
            "Chaining link transforms by multiplication builds the whole arm geometry.",
        ),
        q(
            "Which representation is best to talk to humans but worst for computation near singular orientations?",
            (
                opt("Quaternion"),
                opt("Rotation matrix"),
                opt("Euler angles", correct=True),
                opt("Axis-angle"),
            ),
            "Euler angles are intuitive but suffer gimbal lock; use matrices/quaternions to compute.",
        ),
        q(
            "Forward kinematics maps configuration to pose and is:",
            (
                opt("Unique", correct=True),
                opt("Always multi-valued"),
                opt("Undefined inside the workspace"),
                opt("The same as inverse dynamics"),
            ),
            "Forward kinematics is a unique map from joint angles to the tool pose.",
        ),
    ),
)
