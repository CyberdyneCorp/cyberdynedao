"""Curated quiz questions for the robotics-intermediate course (Inverse
Kinematics & the Jacobian). Keys in ``per_lesson`` are the EXACT content-lesson
titles; the seed interleaves a checkpoint quiz after each, plus the final
comprehensive quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Inverse kinematics: find the joint angles": (
            q(
                "What problem does inverse kinematics (IK) solve for the 2-link arm?",
                (
                    opt("Given the joint angles, it computes the hand position"),
                    opt(
                        "Given a desired hand position (x, y), it finds the joint angles that get there",
                        correct=True,
                    ),
                    opt("It computes the mass and inertia of each link"),
                    opt("It plots the workspace boundary of the arm"),
                ),
                "IK is the direction that finds the joint angles producing a desired hand position (x, y).",
            ),
            q(
                "Which mathematical relation gives the closed-form IK solution for the 2-link arm?",
                (
                    opt("The law of cosines", correct=True),
                    opt("Newton's second law"),
                    opt("The Pythagorean theorem alone"),
                    opt("The chain rule"),
                ),
                "The lesson derives the closed-form IK for the 2-link arm from the law of cosines.",
            ),
            q(
                "In the closed-form solution, how is theta_2 obtained from its cosine?",
                (
                    opt("Using arccos (acos) of c2", correct=True),
                    opt("Using atan2 of x and y"),
                    opt("Using the natural logarithm of c2"),
                    opt("Using the square root of c2"),
                ),
                "The code computes c2 then takes acos(c2) to get theta_2 for the elbow-down pose.",
            ),
        ),
        "Multiple solutions, reach & singularities": (
            q(
                "Why does IK for the 2-link arm typically have two solutions?",
                (
                    opt("Because atan2 always returns two angles"),
                    opt(
                        "Because theta_2 from arccos can be plus or minus, giving elbow-up vs elbow-down",
                        correct=True,
                    ),
                    opt("Because the arm has two links of different lengths"),
                    opt("Because the target can be specified in two coordinate systems"),
                ),
                "The plus or minus sign on theta_2 from arccos produces the elbow-up and elbow-down poses reaching the same point.",
            ),
            q(
                "How many IK solutions does a typical 6-DOF arm have?",
                (
                    opt("Exactly 1"),
                    opt("Exactly 2"),
                    opt("Up to 8", correct=True),
                    opt("Infinitely many always"),
                ),
                "The lesson states a 6-DOF arm typically has up to 8 IK solutions, from which the controller picks one.",
            ),
            q(
                "What condition signals that a target point is unreachable?",
                (
                    opt("theta_1 equals theta_2"),
                    opt(
                        "The absolute value of cos(theta_2) exceeds 1, so arccos is undefined",
                        correct=True,
                    ),
                    opt("The determinant of the Jacobian is positive"),
                    opt("The target lies exactly on the x-axis"),
                ),
                "If the target is outside the workspace annulus, |cos(theta_2)| > 1 and arccos is undefined, so the point is unreachable.",
            ),
        ),
        "Velocity kinematics & the Jacobian": (
            q(
                "What does the Jacobian J(q) map?",
                (
                    opt("Joint angles to end-effector position"),
                    opt("Joint velocities to end-effector velocity", correct=True),
                    opt("End-effector position to joint torques"),
                    opt("Link masses to joint accelerations"),
                ),
                "The Jacobian maps joint velocities to end-effector velocity via x-dot = J(q) q-dot.",
            ),
            q(
                "What does each column of the Jacobian represent?",
                (
                    opt("How the tip moves when one joint turns", correct=True),
                    opt("The mass of one link"),
                    opt("The length of one link"),
                    opt("The angle limit of one joint"),
                ),
                "Each column of J is how the tip moves when one joint turns.",
            ),
            q(
                "How does the Jacobian transpose relate end-effector forces to joints?",
                (
                    opt(
                        "It maps end-effector forces to joint torques via tau = J^T F", correct=True
                    ),
                    opt("It maps joint torques to link lengths"),
                    opt("It maps Cartesian position to joint angles"),
                    opt("It maps joint accelerations to forces"),
                ),
                "The transpose maps end-effector forces to joint torques: tau = J^T F.",
            ),
        ),
        "Singularities & manipulability": (
            q(
                "Mathematically, what defines a singularity?",
                (
                    opt("A configuration where the Jacobian loses rank, det J = 0", correct=True),
                    opt("A configuration where all joint angles are zero"),
                    opt("A configuration where the arm has maximum reach and full rank"),
                    opt("A configuration where the manipulability is maximized"),
                ),
                "A singularity is where the Jacobian loses rank and det J = 0.",
            ),
            q(
                "For the 2-link arm, at which values of theta_2 does a singularity occur?",
                (
                    opt("theta_2 = 0 or pi (arm straight or fully folded)", correct=True),
                    opt("theta_2 = pi/2 only"),
                    opt("theta_2 = pi/4 or 3pi/4"),
                    opt("Any nonzero theta_2"),
                ),
                "For the 2-link arm the singularity happens when theta_2 = 0 or pi, the arm straight or fully folded.",
            ),
            q(
                "How is the manipulability measure w defined?",
                (
                    opt(
                        "w = sqrt(det(J J^T)), the area of the manipulability ellipse", correct=True
                    ),
                    opt("w = det J only"),
                    opt("w = the sum of the link lengths"),
                    opt("w = the trace of the Jacobian"),
                ),
                "Manipulability is w = sqrt(det(J J^T)), which is the area of the manipulability ellipse.",
            ),
        ),
        "Lab: analytic & numerical inverse kinematics": (
            q(
                "In the lab, how does the analytic IK produce both elbow solutions?",
                (
                    opt(
                        "By multiplying arccos(c2) by a sign of +1 (elbow-down) or -1 (elbow-up)",
                        correct=True,
                    ),
                    opt("By running the loop twice with different link lengths"),
                    opt("By swapping x and y in the target"),
                    opt("By increasing the number of iterations"),
                ),
                "The lab loops over sign +1 (elbow-down) and -1 (elbow-up) applied to arccos(c2) to get both solutions.",
            ),
            q(
                "What technique does the numerical IK in the lab use to update the guess?",
                (
                    opt("The Jacobian pseudo-inverse applied to the position error", correct=True),
                    opt("The law of cosines on each iteration"),
                    opt("Random sampling of joint angles"),
                    opt("Gradient of the link masses"),
                ),
                "Numerical IK updates q by adding pinv(J) times the (target - p) position error each iteration.",
            ),
            q(
                "According to the lab, what happens if you move the target outside the reach, such as [3, 0]?",
                (
                    opt("arccos fails because the point is unreachable", correct=True),
                    opt("The arm reaches it with elbow-up only"),
                    opt("The Jacobian becomes the identity matrix"),
                    opt("Manipulability becomes infinite"),
                ),
                "Moving the target outside the reach makes arccos fail, signalling the point is unreachable.",
            ),
        ),
    },
    final=(
        q(
            "What is the core distinction between forward kinematics and inverse kinematics?",
            (
                opt("FK finds angles from a position; IK finds a position from angles"),
                opt(
                    "IK finds joint angles for a desired hand position; FK finds the position from angles",
                    correct=True,
                ),
                opt("Both compute the same thing in different units"),
                opt("FK uses the Jacobian; IK never does"),
            ),
            "IK finds the joint angles for a desired hand position, the reverse of FK which gives position from angles.",
        ),
        q(
            "Which equation correctly relates joint and end-effector velocities?",
            (
                opt("x-dot = J(q) q-dot", correct=True),
                opt("q-dot = J(q) x-dot"),
                opt("tau = J x"),
                opt("x = J^T q"),
            ),
            "The velocity Jacobian gives x-dot = J(q) q-dot, mapping joint velocities to end-effector velocity.",
        ),
        q(
            "Why do control schemes try to keep the arm away from singularities?",
            (
                opt(
                    "Because det J = 0 there, the arm loses a degree of freedom and commanded joint speeds explode",
                    correct=True,
                ),
                opt("Because the links physically detach at singularities"),
                opt("Because the workspace doubles in size there"),
                opt("Because the Jacobian becomes the identity there"),
            ),
            "At a singularity det J = 0, the arm loses a Cartesian direction and J^-1 blows up, demanding huge joint speeds.",
        ),
        q(
            "What does a flat, collapsed manipulability ellipse indicate?",
            (
                opt("The arm is dexterous in every direction"),
                opt("The arm is near a singularity", correct=True),
                opt("The arm is at the center of its workspace"),
                opt("The Jacobian has full rank and maximal area"),
            ),
            "A flat, collapsed ellipse means the arm is near a singularity; a fat round ellipse means it is dexterous.",
        ),
        q(
            "Which method works as a numerical IK solver for any arm, not just the 2-link closed form?",
            (
                opt(
                    "Iterating with the Jacobian pseudo-inverse on the position error", correct=True
                ),
                opt("The law of cosines"),
                opt("Taking atan2 of the link lengths"),
                opt("Computing det(J J^T) once"),
            ),
            "Numerical IK via the Jacobian pseudo-inverse generalizes to any arm, unlike the closed-form law of cosines.",
        ),
    ),
)
