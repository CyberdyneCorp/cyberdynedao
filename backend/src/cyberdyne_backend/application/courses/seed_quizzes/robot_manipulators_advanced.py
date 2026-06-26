"""Quiz questions for the Robot Manipulators & Industrial Robotics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Manipulator dynamics: the equation of motion": (
            q(
                "In M(q)*qddot + C(q,qdot)*qdot + g(q) = tau, what is M(q)?",
                (
                    opt("The mass / inertia matrix", correct=True),
                    opt("The Coriolis term"),
                    opt("The gravity vector"),
                    opt("The Jacobian"),
                ),
                "M(q) is the symmetric positive-definite inertia matrix.",
            ),
            q(
                "The term C(q,qdot)*qdot captures:",
                (
                    opt("Coriolis and centrifugal effects", correct=True),
                    opt("Gravity only"),
                    opt("Pure inertia"),
                    opt("Encoder noise"),
                ),
                "C contains the velocity-coupled Coriolis and centrifugal torques.",
            ),
            q(
                "Which algorithm computes inverse dynamics in O(n) time?",
                (
                    opt("Recursive Newton-Euler (RNEA)", correct=True),
                    opt("Gaussian elimination"),
                    opt("The fast Fourier transform"),
                    opt("Dijkstra's algorithm"),
                ),
                "RNEA is the O(n) outward-inward sweep used for real-time inverse dynamics.",
            ),
        ),
        "Computed-torque control": (
            q(
                "What is the goal of computed-torque control?",
                (
                    opt(
                        "Cancel the nonlinear dynamics to leave a linear error system", correct=True
                    ),
                    opt("Ignore the dynamic model"),
                    opt("Maximize torque ripple"),
                    opt("Run fully open-loop"),
                ),
                "It uses M, C, g to feedback-linearize, yielding a decoupled linear error system.",
            ),
            q(
                "After feedback linearization the closed-loop error obeys:",
                (
                    opt("eddot + Kd*edot + Kp*e = 0", correct=True),
                    opt("e = constant"),
                    opt("A random walk"),
                    opt("eddot = tau"),
                ),
                "The model cancellation leaves a decoupled second-order error system you can place.",
            ),
            q(
                "What is the main weakness of computed-torque control?",
                (
                    opt("It depends on accurate knowledge of M, C, g", correct=True),
                    opt("It needs no sensors"),
                    opt("It cannot place poles"),
                    opt("It only works at zero speed"),
                ),
                "Model errors (payload, friction) degrade the cancellation; adaptive variants help.",
            ),
        ),
        "Operational-space and impedance control": (
            q(
                "Operational-space control writes the dynamics in:",
                (
                    opt("Task (Cartesian) coordinates via the Jacobian", correct=True),
                    opt("Frequency domain only"),
                    opt("Joint coordinates only"),
                    opt("Pixel coordinates"),
                ),
                "Khatib's formulation expresses dynamics in task space; tau = J^T F.",
            ),
            q(
                "Impedance control regulates:",
                (
                    opt("The relationship between motion and force", correct=True),
                    opt("Only the motor temperature"),
                    opt("Only position, ignoring force"),
                    opt("Only force, ignoring motion"),
                ),
                "Impedance shapes a virtual mass-spring-damper between motion and contact force.",
            ),
            q(
                "How is redundancy exploited in the operational-space framework?",
                (
                    opt("Extra DoF act in the null space of J for secondary goals", correct=True),
                    opt("By removing joints"),
                    opt("By increasing the payload"),
                    opt("By disabling feedback"),
                ),
                "Null-space torques handle posture or joint-limit goals without disturbing the task.",
            ),
        ),
        "Optimization-based trajectory planning": (
            q(
                "Trajectory optimization minimizes an objective subject to:",
                (
                    opt(
                        "Dynamics and constraints like joint, torque, and collision limits",
                        correct=True,
                    ),
                    opt("No constraints at all"),
                    opt("Only the color of the robot"),
                    opt("The DH table size"),
                ),
                "It is an optimal control problem with dynamics and physical constraints.",
            ),
            q(
                "Which method discretizes states and controls and hands them to an NLP solver?",
                (
                    opt("Direct collocation", correct=True),
                    opt("The law of cosines"),
                    opt("Quaternion slerp"),
                    opt("Gimbal lock"),
                ),
                "Direct collocation discretizes the trajectory and solves it as a nonlinear program.",
            ),
            q(
                "Which planners fold a collision-cost gradient into trajectory optimization?",
                (
                    opt("CHOMP, STOMP, TrajOpt", correct=True),
                    opt("PID, LQR, MPC"),
                    opt("FFT, DFT, DCT"),
                    opt("TCP, UDP, IP"),
                ),
                "CHOMP/STOMP/TrajOpt deform an initial path out of collision while keeping it smooth.",
            ),
        ),
        "Learning-based manipulator control": (
            q(
                "In reinforcement learning, the policy pi_theta maps:",
                (
                    opt("States to actions to maximize expected reward", correct=True),
                    opt("Torques to encoder lines"),
                    opt("Pixels to DH parameters"),
                    opt("Mass to gravity"),
                ),
                "An RL policy chooses actions from states to maximize cumulative reward.",
            ),
            q(
                "What does sim-to-real with domain randomization address?",
                (
                    opt(
                        "Transferring a simulation-trained policy to real hardware robustly",
                        correct=True,
                    ),
                    opt("Removing the need for a reward"),
                    opt("Eliminating all sensors"),
                    opt("Making the robot heavier"),
                ),
                "Randomizing sim parameters makes the learned policy robust to the reality gap.",
            ),
            q(
                "Why are hybrid model-based plus learned controllers the pragmatic state of the art?",
                (
                    opt(
                        "The model gives stability/safety while learning handles unmodeled effects",
                        correct=True,
                    ),
                    opt("Because models are never useful"),
                    opt("Because learning is always unsafe alone and models never help"),
                    opt("Because they avoid all feedback"),
                ),
                "A nominal model-based term ensures safety; the learned part captures what the model misses.",
            ),
        ),
        "Case study: a 6-DoF pick-and-place cell": (
            q(
                "In the pick-and-place pipeline, what immediately follows vision-based pose detection?",
                (
                    opt("Dynamics identification"),
                    opt("Inverse kinematics to find joint angles", correct=True),
                    opt("Shipping the part"),
                    opt("Powering off the arm"),
                ),
                "After the camera gives the object pose, IK finds the joint angles to reach it.",
            ),
            q(
                "When multiple IK solutions exist, a good selection rule is to pick the one that is:",
                (
                    opt(
                        "Within joint limits and closest to the current configuration", correct=True
                    ),
                    opt("Farthest from the current pose"),
                    opt("The first in the list regardless of limits"),
                    opt("The one with the largest joint angles"),
                ),
                "Choosing a feasible solution nearest the current joints keeps motion smooth and short.",
            ),
            q(
                "Why switch to impedance / force control during the grasp approach?",
                (
                    opt("So a misaligned part is guided in rather than jammed", correct=True),
                    opt("To increase cycle time on purpose"),
                    opt("To disable the camera"),
                    opt("To remove gravity compensation"),
                ),
                "Compliance on contact lets the part seat instead of jamming under stiff position control.",
            ),
        ),
    },
    final=(
        q(
            "The gravity term g(q) in the equation of motion represents:",
            (
                opt("Configuration-dependent gravity torques", correct=True),
                opt("Coriolis effects"),
                opt("The inertia matrix"),
                opt("Encoder resolution"),
            ),
            "g(q) is the joint torque needed to hold the arm against gravity.",
        ),
        q(
            "Computed-torque control turns the closed loop into:",
            (
                opt("A decoupled linear second-order error system", correct=True),
                opt("A nonlinear chaotic system"),
                opt("An open-loop integrator"),
                opt("A pure delay"),
            ),
            "Feedback linearization leaves eddot + Kd*edot + Kp*e = 0.",
        ),
        q(
            "Impedance control is most useful for:",
            (
                opt("Contact-rich tasks like assembly and human interaction", correct=True),
                opt("Free-space high-speed slewing only"),
                opt("Replacing the encoder"),
                opt("Eliminating dynamics"),
            ),
            "Regulating the motion-force relationship makes contact tasks safe and robust.",
        ),
        q(
            "Direct collocation solves trajectory optimization by:",
            (
                opt("Discretizing the trajectory and solving a nonlinear program", correct=True),
                opt("Ignoring the dynamics"),
                opt("Random sampling with no objective"),
                opt("Inverting the Jacobian once"),
            ),
            "It turns the optimal-control problem into an NLP over discretized states/controls.",
        ),
        q(
            "Domain randomization in sim-to-real is used to:",
            (
                opt("Make a learned policy robust to the reality gap", correct=True),
                opt("Speed up the encoder"),
                opt("Remove the reward function"),
                opt("Increase the payload"),
            ),
            "Randomizing simulation parameters helps the policy transfer to real hardware.",
        ),
        q(
            "A reliable pick-and-place cell achieves robustness mainly through:",
            (
                opt(
                    "Co-designed perception, kinematics, planning, and control handing off well",
                    correct=True,
                ),
                opt("One single clever algorithm"),
                opt("Maximizing peak torque"),
                opt("Disabling feedback to save time"),
            ),
            "Reliability is a system property: the stages must hand off cleanly to each other.",
        ),
    ),
)
