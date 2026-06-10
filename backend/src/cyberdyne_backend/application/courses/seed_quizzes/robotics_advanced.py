"""Curated quiz for the Robotics - Advanced course (slug robotics-advanced):
a checkpoint quiz after each content lesson plus a final comprehensive quiz.
Keys are the EXACT content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "DH parameters & 3D forward kinematics": (
            q(
                "How many numbers does the Denavit-Hartenberg convention use to describe the step from one link frame to the next?",
                (
                    opt("Two"),
                    opt("Three"),
                    opt("Four", correct=True),
                    opt("Six"),
                ),
                "DH describes each link-to-link step with four numbers: joint angle, link offset, link length, and link twist.",
            ),
            q(
                "Which four quantities make up a Denavit-Hartenberg parameter set for a link?",
                (
                    opt("joint angle, link offset, link length, link twist", correct=True),
                    opt("mass, inertia, length, twist"),
                    opt("position, velocity, acceleration, jerk"),
                    opt("Kp, Ki, Kd, and the setpoint"),
                ),
                "The DH parameters are theta (joint angle), d (link offset), a (link length), and alpha (link twist).",
            ),
            q(
                "How is the full forward kinematics of an n-joint arm built from the per-link DH transforms?",
                (
                    opt("By adding the transforms together"),
                    opt("By multiplying them in order, T = T1 T2 ... Tn", correct=True),
                    opt("By inverting each transform and summing them"),
                    opt("By taking the determinant of each transform"),
                ),
                "Each DH step becomes a homogeneous transform Ti, and the full FK is their product T1 T2 ... Tn.",
            ),
        ),
        "Manipulator dynamics": (
            q(
                "In the equation of motion M(q) qddot + C(q,qdot) qdot + g(q) = tau, what does the matrix M represent?",
                (
                    opt("the configuration-dependent inertia matrix", correct=True),
                    opt("the Coriolis and centrifugal effects"),
                    opt("the gravity vector"),
                    opt("the joint torques"),
                ),
                "M is the configuration-dependent inertia matrix; C captures Coriolis and centrifugal effects and g is gravity.",
            ),
            q(
                "What torque does a single link held out horizontally require against gravity?",
                (
                    opt("zero, because gravity does no work horizontally"),
                    opt("m g ell cos(theta)", correct=True),
                    opt("Kp times the position error"),
                    opt("the determinant of the Jacobian"),
                ),
                "A link held out horizontally needs torque tau = m g ell cos(theta), and it swings like a pendulum if released.",
            ),
            q(
                "Why is dynamics needed in addition to kinematics?",
                (
                    opt(
                        "to size motors, simulate the robot, and build model-based controllers",
                        correct=True,
                    ),
                    opt("to compute the reachable workspace annulus"),
                    opt("to count the number of inverse-kinematics solutions"),
                    opt("to attach a coordinate frame to each link"),
                ),
                "Kinematics ignores mass, so dynamics is what you need to size motors, simulate the robot, and build model-based controllers.",
            ),
        ),
        "Trajectory generation": (
            q(
                "Why can you not simply command a target joint angle directly?",
                (
                    opt("because it would demand infinite acceleration", correct=True),
                    opt("because the Jacobian would become singular"),
                    opt("because gravity would cancel the motion"),
                    opt("because the inertia matrix is not invertible"),
                ),
                "Commanding a target angle directly demands infinite acceleration, so a smooth time profile is used instead.",
            ),
            q(
                "What is the normalised cubic (smoothstep) trajectory that meets zero-velocity boundary conditions?",
                (
                    opt("q(s) = q0 + (qf - q0)(3s^2 - 2s^3)", correct=True),
                    opt("q(s) = q0 + (qf - q0) s"),
                    opt("q(s) = q0 cos(s) + qf sin(s)"),
                    opt("q(s) = q0 + (qf - q0) exp(-s)"),
                ),
                "The cubic smoothstep q(s) = q0 + (qf - q0)(3s^2 - 2s^3) meets zero-velocity boundary conditions over 0 <= s <= 1.",
            ),
            q(
                "Which profile is common for long moves at a speed limit?",
                (
                    opt("a constant-jerk profile"),
                    opt(
                        "a trapezoidal velocity profile: accelerate, cruise, decelerate",
                        correct=True,
                    ),
                    opt("a step input straight to the target"),
                    opt("a sinusoidal torque profile"),
                ),
                "For long moves at a speed limit a trapezoidal velocity profile that accelerates, cruises, then decelerates is common.",
            ),
        ),
        "Control: PID & computed torque": (
            q(
                "In the PID law tau = Kp e + Ki integral(e) + Kd edot, what does the Kd (derivative) term do?",
                (
                    opt("pulls the joint toward the target"),
                    opt("damps oscillation", correct=True),
                    opt("erases steady-state error"),
                    opt("cancels the gravity torque"),
                ),
                "The derivative term Kd damps oscillation, while Kp pulls toward the target and Ki erases steady-state error.",
            ),
            q(
                "Which PID term erases steady-state error?",
                (
                    opt("the proportional term Kp"),
                    opt("the derivative term Kd"),
                    opt("the integral term Ki", correct=True),
                    opt("the feed-forward gravity term"),
                ),
                "The integral term Ki erases steady-state error by accumulating the error over time.",
            ),
            q(
                "What does computed-torque control use to achieve high performance?",
                (
                    opt("only a very large proportional gain"),
                    opt(
                        "the dynamics M, C, g to cancel nonlinearities and feed-forward the needed torque",
                        correct=True,
                    ),
                    opt("the Denavit-Hartenberg table of the arm"),
                    opt("a trapezoidal velocity profile alone"),
                ),
                "Computed-torque control uses the dynamics M, C, g to cancel nonlinearities and feed-forward the torque the trajectory needs, leaving PID a small error to clean up.",
            ),
        ),
        "Lab: trajectory + Jacobian velocity": (
            q(
                "In the lab, how is the cubic trajectory value q computed for a normalised time s?",
                (
                    opt("q0 + (qf - q0) * (3*s**2 - 2*s**3)", correct=True),
                    opt("q0 + (qf - q0) * s"),
                    opt("q0 * np.cos(s)"),
                    opt("np.linalg.pinv(s)"),
                ),
                "The lab samples the smoothstep q = q0 + (qf - q0) * (3*s**2 - 2*s**3).",
            ),
            q(
                "What does the lab report when det(J) goes to 0?",
                (
                    opt("that the arm is at a singularity having lost a DOF", correct=True),
                    opt("that the trajectory has finished"),
                    opt("that the inertia matrix is identity"),
                    opt("that the PID gains are tuned"),
                ),
                "Setting t2 = 0 makes the arm straight so det(J) goes to 0, a singularity where the arm loses a degree of freedom.",
            ),
            q(
                "How does the lab compute the manipulability w?",
                (
                    opt("sqrt(det(J @ J.T))", correct=True),
                    opt("det(J) squared"),
                    opt("the trace of J"),
                    opt("the norm of qdot"),
                ),
                "The lab prints manipulability w = sqrt(det(J @ J.T)), where a bigger value means more dexterous.",
            ),
        ),
    },
    final=(
        q(
            "How many numbers per link does the Denavit-Hartenberg convention use, and what is the full forward kinematics?",
            (
                opt("four numbers, with FK the product of per-link transforms", correct=True),
                opt("three numbers, with FK the sum of per-link transforms"),
                opt("six numbers, with FK the inverse of the first transform"),
                opt("two numbers, with FK the determinant of the chain"),
            ),
            "DH uses four numbers per link and the full FK is the product T1 T2 ... Tn of the per-link homogeneous transforms.",
        ),
        q(
            "In the manipulator equation M qddot + C qdot + g = tau, which term captures gravity?",
            (
                opt("M, the inertia matrix"),
                opt("C, the Coriolis and centrifugal term"),
                opt("g, the gravity vector", correct=True),
                opt("tau, the joint torques"),
            ),
            "g(q) is the gravity term; M is inertia, C is Coriolis and centrifugal, and tau are the joint torques.",
        ),
        q(
            "Why is a cubic (smoothstep) trajectory preferred over commanding the target angle directly?",
            (
                opt("it gives finite acceleration and zero velocity at the ends", correct=True),
                opt("it reaches the target faster than any other profile"),
                opt("it makes the Jacobian invertible"),
                opt("it removes the need for any control loop"),
            ),
            "Commanding the angle directly demands infinite acceleration; the cubic eases position in and out with finite acceleration and zero end velocities.",
        ),
        q(
            "In a PID controller, which gains damp oscillation and erase steady-state error respectively?",
            (
                opt("Kp damps, Ki erases"),
                opt("Kd damps, Ki erases", correct=True),
                opt("Ki damps, Kd erases"),
                opt("Kp damps, Kd erases"),
            ),
            "Kd (derivative) damps oscillation and Ki (integral) erases steady-state error, while Kp pulls toward the target.",
        ),
        q(
            "What characterises a singularity of the 2-link arm, as exercised in the lab?",
            (
                opt("det(J) goes to 0 and the arm loses a degree of freedom", correct=True),
                opt("the inertia matrix M becomes singular"),
                opt("the integral gain Ki goes to infinity"),
                opt("the DH table gains an extra row"),
            ),
            "At a singularity (for example t2 = 0, arm straight) det(J) goes to 0 and the arm loses a degree of freedom.",
        ),
    ),
)
