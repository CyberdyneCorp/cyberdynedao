"""Quiz questions for the Robot Manipulators & Industrial Robotics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Denavit-Hartenberg parameters": (
            q(
                "How many DH parameters describe each joint?",
                (
                    opt("Two"),
                    opt("Three"),
                    opt("Four", correct=True),
                    opt("Six"),
                ),
                "The DH convention uses four parameters per joint: a, alpha, d, theta.",
            ),
            q(
                "For a revolute joint, which DH parameter is the variable?",
                (
                    opt("a (link length)"),
                    opt("alpha (link twist)"),
                    opt("theta (joint angle)", correct=True),
                    opt("d (link offset)"),
                ),
                "Theta varies for a revolute joint; d varies for a prismatic joint.",
            ),
            q(
                "What does a DH table provide?",
                (
                    opt("The full geometric specification of the arm", correct=True),
                    opt("The motor temperatures"),
                    opt("The control gains"),
                    opt("The payload mass only"),
                ),
                "One row per joint fully specifies the arm geometry, a standard interchange format.",
            ),
        ),
        "Forward kinematics by transform chains": (
            q(
                "Forward kinematics from a DH table is computed by:",
                (
                    opt("Adding the joint angles"),
                    opt("Multiplying the per-joint transforms base to tool", correct=True),
                    opt("Inverting the Jacobian"),
                    opt("Taking the SVD"),
                ),
                "FK is the product of per-joint homogeneous transforms from base to end-effector.",
            ),
            q(
                "In the resulting 4x4 transform, the tool position is found in:",
                (
                    opt("The top-left 3x3 block"),
                    opt("The last column (translation)", correct=True),
                    opt("The bottom row"),
                    opt("The diagonal"),
                ),
                "The last column holds the translation (tool position); the 3x3 block is orientation.",
            ),
            q(
                "Why does the same FK code handle 2-DoF and 7-DoF arms?",
                (
                    opt(
                        "Because matrix multiplication composes cleanly; only the DH table changes",
                        correct=True,
                    ),
                    opt("Because all arms have the same geometry"),
                    opt("Because DoF count does not matter"),
                    opt("Because it ignores the joints"),
                ),
                "The chain of transforms is general; changing the DH table adapts it to any serial arm.",
            ),
        ),
        "Inverse kinematics": (
            q(
                "Inverse kinematics solves for:",
                (
                    opt("The tool pose given joint angles"),
                    opt("The joint angles given a desired tool pose", correct=True),
                    opt("The joint torques given motion"),
                    opt("The mass matrix"),
                ),
                "IK is the reverse map: from a desired pose to the joint angles.",
            ),
            q(
                "For the planar 2R arm, the elbow angle is found from:",
                (
                    opt("The law of cosines", correct=True),
                    opt("The SVD of the Jacobian"),
                    opt("A Fourier transform"),
                    opt("Newton's second law"),
                ),
                "cos(theta2) comes from the law of cosines on the link triangle.",
            ),
            q(
                "Most 6-DoF arms with a spherical wrist admit a closed-form IK because of:",
                (
                    opt("Kinematic decoupling of position and orientation", correct=True),
                    opt("Having no joint limits"),
                    opt("Being parallel robots"),
                    opt("Using only prismatic joints"),
                ),
                "A spherical wrist decouples the wrist-centre position from the orientation solution.",
            ),
        ),
        "The manipulator Jacobian": (
            q(
                "The Jacobian J(q) maps:",
                (
                    opt("Joint velocities to end-effector velocity", correct=True),
                    opt("Joint angles to torques"),
                    opt("Forces to temperatures"),
                    opt("Positions to masses"),
                ),
                "J relates joint rates qdot to the Cartesian twist (v, omega).",
            ),
            q(
                "How does the Jacobian relate joint torques to an end-effector wrench F?",
                (
                    opt("tau = J F"),
                    opt("tau = J^T F", correct=True),
                    opt("tau = J^-1 F"),
                    opt("tau = F"),
                ),
                "Force-torque duality gives tau = J transpose times the wrench F.",
            ),
            q(
                "For the 2R arm, det(J) equals l1*l2*sin(theta2). It vanishes when:",
                (
                    opt("The arm is straight or folded (theta2 = 0 or pi)", correct=True),
                    opt("theta2 = 90 degrees"),
                    opt("The motors are off"),
                    opt("The payload is zero"),
                ),
                "sin(theta2) = 0 at the stretched and folded configurations - a singularity.",
            ),
        ),
        "Singularities and manipulability": (
            q(
                "At a singularity, the Jacobian:",
                (
                    opt("Loses rank, so the tool cannot move in some direction", correct=True),
                    opt("Becomes the identity"),
                    opt("Doubles in size"),
                    opt("Has infinite manipulability"),
                ),
                "A singularity is a rank loss; some Cartesian direction becomes unreachable.",
            ),
            q(
                "Which quantity signals proximity to a singularity?",
                (
                    opt("The largest singular value growing"),
                    opt("The smallest singular value going to zero", correct=True),
                    opt("The trace of M"),
                    opt("The number of joints"),
                ),
                "As sigma_min approaches zero from the SVD of J, the arm nears a singularity.",
            ),
            q(
                "Yoshikawa's manipulability w = sqrt(det(J J^T)) is:",
                (
                    opt("The volume of the velocity ellipsoid", correct=True),
                    opt("The robot mass"),
                    opt("The joint limit range"),
                    opt("The cycle time"),
                ),
                "Manipulability measures the velocity-ellipsoid volume; zero means singular.",
            ),
        ),
        "Joint-space trajectory generation": (
            q(
                "Why not command a joint to jump instantly to its target?",
                (
                    opt("It would demand infinite velocity", correct=True),
                    opt("It would use too little power"),
                    opt("The encoder cannot read it"),
                    opt("It violates DH convention"),
                ),
                "An instantaneous jump needs infinite velocity; a smooth trajectory respects limits.",
            ),
            q(
                "A cubic point-to-point trajectory has zero end velocities and a velocity profile that is:",
                (
                    opt("Constant"),
                    opt("A parabola peaking at mid-move", correct=True),
                    opt("A step"),
                    opt("Always zero"),
                ),
                "A cubic gives a parabolic velocity peaking at the midpoint, zero at the ends.",
            ),
            q(
                "What does a quintic (5th-order) polynomial add over a cubic?",
                (
                    opt("Zero end accelerations for smoother motion", correct=True),
                    opt("Faster infinite jerk"),
                    opt("Fewer waypoints"),
                    opt("Lower resolution"),
                ),
                "A quintic also zeroes end accelerations, giving continuous, jerk-friendlier motion.",
            ),
        ),
        "Resolved-rate velocity control": (
            q(
                "Resolved-rate control computes joint rates from a commanded tool velocity by:",
                (
                    opt("Inverting (or pseudo-inverting) the Jacobian", correct=True),
                    opt("Differentiating the mass matrix"),
                    opt("Integrating the gravity torque"),
                    opt("Ignoring the Jacobian"),
                ),
                "qdot = J^-1 xdot_des (or J^+ for non-square / damped least-squares).",
            ),
            q(
                "What problem does damped least-squares solve near a singularity?",
                (
                    opt("It bounds joint speeds at the cost of small tracking error", correct=True),
                    opt("It increases manipulability to infinity"),
                    opt("It removes all joint limits"),
                    opt("It eliminates the need for feedback"),
                ),
                "DLS adds a damping term so joint speeds stay finite near singularities.",
            ),
            q(
                "Integrating qdot = J^+ K e (pose error e) gives:",
                (
                    opt("A general numerical inverse-kinematics solver", correct=True),
                    opt("The mass matrix"),
                    opt("The DH table"),
                    opt("The workspace boundary"),
                ),
                "Driving the pose error to zero with the pseudoinverse is numerical IK.",
            ),
        ),
    },
    final=(
        q(
            "How many parameters does the DH convention use per joint?",
            (
                opt("Two"),
                opt("Four", correct=True),
                opt("Six"),
                opt("Eight"),
            ),
            "Four: a, alpha, d, theta.",
        ),
        q(
            "Forward kinematics is computed as:",
            (
                opt("A product of per-joint transforms", correct=True),
                opt("The inverse of the Jacobian"),
                opt("A sum of torques"),
                opt("The SVD of M"),
            ),
            "FK multiplies the per-joint transforms from base to tool.",
        ),
        q(
            "Which statement about inverse kinematics is true?",
            (
                opt("It always has a unique solution"),
                opt("It can have multiple, no, or infinitely many solutions", correct=True),
                opt("It needs no joint-limit checks"),
                opt("It maps angles to pose"),
            ),
            "IK solutions are multiple, none, or infinite depending on geometry and reach.",
        ),
        q(
            "The relation tau = J^T F expresses:",
            (
                opt("Force-torque duality", correct=True),
                opt("Conservation of energy"),
                opt("The mass matrix"),
                opt("Gimbal lock"),
            ),
            "The transpose Jacobian maps an end-effector wrench to joint torques.",
        ),
        q(
            "Manipulability w = sqrt(det(J J^T)) goes to zero at:",
            (
                opt("A singularity", correct=True),
                opt("Maximum dexterity"),
                opt("The home position always"),
                opt("Zero payload"),
            ),
            "Manipulability collapses to zero exactly at singular configurations.",
        ),
        q(
            "The damping factor lambda in damped least-squares trades:",
            (
                opt("Exact tracking for bounded joint speeds near singularities", correct=True),
                opt("Speed for color accuracy"),
                opt("DoF for payload"),
                opt("Encoder lines for torque"),
            ),
            "Larger lambda keeps joint speeds safe near singularities at the cost of small error.",
        ),
    ),
)
