"""Curated quiz questions for the Physics - Intermediate course (per-lesson
checkpoints keyed by EXACT content-lesson title, plus a final comprehensive
quiz). Every question is answerable from the lesson body."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Rotational motion & torque": (
            q(
                "What is the rotational analogue of Newton's law F = ma?",
                (
                    opt("tau = I omega"),
                    opt("tau = I alpha", correct=True),
                    opt("L = I alpha"),
                    opt("F = I omega"),
                ),
                "The lesson maps F = ma to its rotational twin tau = I alpha, with torque, moment of inertia, and angular acceleration.",
            ),
            q(
                "According to the lesson, why does a longer wrench turn a tighter bolt with the same hand force?",
                (
                    opt("A longer lever arm increases the torque tau = r F sin phi", correct=True),
                    opt("A longer wrench reduces the moment of inertia"),
                    opt("A longer wrench increases the angular momentum L"),
                    opt("A longer wrench changes the force into a torque directly"),
                ),
                "Torque grows with the lever arm r, so lengthening the wrench produces more turning effect for the same force.",
            ),
            q(
                "What does the lesson say happens to angular momentum L when there is no torque?",
                (
                    opt("It decays exponentially to zero"),
                    opt(
                        "It is conserved, giving a spinning rotor gyroscopic stiffness",
                        correct=True,
                    ),
                    opt("It grows linearly with time"),
                    opt("It equals the moment of inertia times the torque"),
                ),
                "With no torque L is conserved, which is why a spinning rotor resists tilting (gyroscopic stiffness).",
            ),
        ),
        "Oscillations & the calculus you need": (
            q(
                "For a mass on a spring with restoring force F = -k x, what is the angular frequency omega?",
                (
                    opt("omega = k/m"),
                    opt("omega = sqrt(k/m)", correct=True),
                    opt("omega = sqrt(m/k)"),
                    opt("omega = k m"),
                ),
                "Newton's law gives x'' + omega^2 x = 0 with omega = sqrt(k/m).",
            ),
            q(
                "What does the lesson use as its real-world example of damping?",
                (
                    opt("A pendulum clock"),
                    opt("A car's suspension", correct=True),
                    opt("A guitar string"),
                    opt("A spinning rotor"),
                ),
                "The damped oscillation section frames damping as a car's suspension, tuned near critical so a pothole gives a single smooth dip.",
            ),
            q(
                "What does the lesson call the direction of steepest increase, often related to force by F = -grad U?",
                (
                    opt("The partial derivative"),
                    opt("The gradient", correct=True),
                    opt("The Lagrangian"),
                    opt("The angular velocity"),
                ),
                "The gradient grad f is the direction of steepest increase, and a force is often F = -grad U.",
            ),
        ),
        "Rigid bodies in 3D: frames & rotations": (
            q(
                "In the lesson, which frame is the inertial frame fixed to the ground where position lives?",
                (
                    opt("The body frame"),
                    opt("The world frame", correct=True),
                    opt("The rotor frame"),
                    opt("The gyroscope frame"),
                ),
                "The world frame is inertial and fixed to the ground; position lives there, while thrust and inertia live in the body frame.",
            ),
            q(
                "What property does the rotation matrix R have according to the lesson?",
                (
                    opt("It is orthogonal, so its inverse equals its transpose", correct=True),
                    opt("It is diagonal with the moments of inertia"),
                    opt("It is symmetric and equal to its own square"),
                    opt("It always equals the identity matrix"),
                ),
                "R is orthogonal, meaning R inverse equals R transpose.",
            ),
            q(
                "The two Newton-Euler equations in the lesson describe which pair of motions?",
                (
                    opt("Translation (Newton) and rotation (Euler)", correct=True),
                    opt("Damping and oscillation"),
                    opt("Gravity and thrust only"),
                    opt("Roll and pitch only"),
                ),
                "The Newton-Euler equations are two vector equations: translation (Newton) and rotation (Euler), written in the body frame.",
            ),
        ),
    },
    final=(
        q(
            "Across the course, which quantity plays the role of rotational mass?",
            (
                opt("Angular velocity omega"),
                opt("Moment of inertia I", correct=True),
                opt("Torque tau"),
                opt("Angular momentum L"),
            ),
            "Moment of inertia I is the rotational mass: how hard it is to spin something, depending on how mass is distributed.",
        ),
        q(
            "What kind of equation does Newton's law produce for a mass on a spring?",
            (
                opt("A differential equation relating a function to its derivatives", correct=True),
                opt("A rotation matrix"),
                opt("A cross product of two vectors"),
                opt("A potential energy gradient"),
            ),
            "The spring gives a differential equation x'' + omega^2 x = 0 whose solution oscillates.",
        ),
        q(
            "Which calculus tool does the lesson say the Lagrangian method is built from?",
            (
                opt("The cross product"),
                opt("The partial derivative", correct=True),
                opt("The rotation matrix"),
                opt("Angular momentum"),
            ),
            "The partial derivative measures the rate of change in one variable holding others fixed, and the Lagrangian method is built from these.",
        ),
        q(
            "What effect appears when taking the rate of change of a vector in a rotating frame?",
            (
                opt("A damping term proportional to zeta"),
                opt("An extra omega cross (dot) term", correct=True),
                opt("A gradient of the potential energy"),
                opt("A restoring force -k x"),
            ),
            "In a rotating frame, the rate of change of any vector picks up an omega cross (dot) term.",
        ),
        q(
            "Which expression gives the size of a torque in the lesson?",
            (
                opt("tau = r F sin phi", correct=True),
                opt("tau = I omega"),
                opt("tau = m g z"),
                opt("tau = sqrt(k/m)"),
            ),
            "The size of a torque is tau = r F sin phi, growing with the lever arm and with how perpendicular the push is.",
        ),
    ),
)
