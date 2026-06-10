"""Curated quiz questions for the Physics - Basics course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each lesson."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Motion: position, velocity, acceleration": (
            q(
                "How is velocity defined in terms of position?",
                (
                    opt("The second time derivative of position"),
                    opt("The time derivative of position, dx/dt", correct=True),
                    opt("Position multiplied by time"),
                    opt("The integral of acceleration over distance"),
                ),
                "Velocity is the rate of change of position, v = dx/dt, the slope of x versus t.",
            ),
            q(
                "For constant acceleration, which equation gives position over time?",
                (
                    opt("x(t) = v0 + a t"),
                    opt("x(t) = x0 + v0 t + (1/2) a t^2", correct=True),
                    opt("x(t) = x0 + a t^2"),
                    opt("x(t) = (1/2) a t"),
                ),
                "Integrating constant acceleration twice gives x(t) = x0 + v0 t + (1/2) a t^2.",
            ),
            q(
                "Why is a car turning at constant speed still accelerating?",
                (
                    opt("Because its speed is secretly increasing"),
                    opt("Because the direction of its velocity vector changes", correct=True),
                    opt("Because friction always adds acceleration"),
                    opt("Because position is a scalar, not a vector"),
                ),
                "Acceleration is the change of the velocity vector, and turning changes its direction even at constant speed.",
            ),
        ),
        "Forces & Newton's laws": (
            q(
                "What does Newton's second law state?",
                (
                    opt("Every force has an equal and opposite partner"),
                    opt("Net force equals mass times acceleration, F = m a", correct=True),
                    opt("With no net force, velocity stays constant"),
                    opt("Force equals mass times velocity"),
                ),
                "Newton's second law is F = m a, the central equation of dynamics.",
            ),
            q(
                "For a drone of mass m to hover, what must the rotor thrust T equal?",
                (
                    opt("Zero"),
                    opt("mg, the weight", correct=True),
                    opt("Twice the weight, 2mg"),
                    opt("The friction force"),
                ),
                "Hovering means a = 0, so T - mg = 0 and thrust equals the weight mg.",
            ),
            q(
                "On a slope, a block starts to slide when which condition is met?",
                (
                    opt("tan(alpha) > mu", correct=True),
                    opt("tan(alpha) < mu"),
                    opt("sin(alpha) > cos(alpha)"),
                    opt("mu > 1 regardless of angle"),
                ),
                "It slides when the gravity component along the slope beats max friction, i.e. tan(alpha) > mu.",
            ),
        ),
        "Energy & momentum": (
            q(
                "What is the formula for kinetic energy?",
                (
                    opt("K = m g h"),
                    opt("K = (1/2) m v^2", correct=True),
                    opt("K = m v"),
                    opt("K = F times d"),
                ),
                "Kinetic energy is K = (1/2) m v^2.",
            ),
            q(
                "Dropping an object from height h with no friction, what is its speed on arrival?",
                (
                    opt("v = g h"),
                    opt("v = sqrt(2 g h)", correct=True),
                    opt("v = 2 g h"),
                    opt("v = sqrt(g h)"),
                ),
                "All potential energy mgh converts to kinetic energy (1/2)mv^2, giving v = sqrt(2 g h).",
            ),
            q(
                "How is momentum defined in the lesson?",
                (
                    opt("p = (1/2) m v^2"),
                    opt("p = m v", correct=True),
                    opt("p = m g h"),
                    opt("p = F times d"),
                ),
                "Momentum is p = m v, and Newton's second law is really F = dp/dt.",
            ),
        ),
    },
    final=(
        q(
            "Which quantity describes how fast velocity changes?",
            (
                opt("Position"),
                opt("Acceleration", correct=True),
                opt("Momentum"),
                opt("Work"),
            ),
            "Acceleration a = dv/dt is the rate of change of velocity.",
        ),
        q(
            "Which statement matches Newton's first law (inertia)?",
            (
                opt("Net force equals mass times acceleration"),
                opt("With no net force, velocity stays constant", correct=True),
                opt("Every force has an equal and opposite partner"),
                opt("Force equals the rate of change of momentum"),
            ),
            "Newton's first law says that with no net force an object keeps constant velocity, and rest stays at rest.",
        ),
        q(
            "With no friction, what quantity is conserved as an object moves?",
            (
                opt("Kinetic energy alone"),
                opt("The total mechanical energy E = K + U", correct=True),
                opt("Potential energy alone"),
                opt("The force on the object"),
            ),
            "Without friction the total mechanical energy E = K + U stays constant.",
        ),
        q(
            "A thrown projectile combines which two kinds of motion?",
            (
                opt("Constant velocity sideways and constant acceleration downward", correct=True),
                opt("Constant acceleration in every direction"),
                opt("Constant velocity in every direction"),
                opt("Zero velocity and zero acceleration"),
            ),
            "A projectile moves at constant velocity horizontally while accelerating downward at -g.",
        ),
        q(
            "What is the rotational cousin of momentum mentioned at the end of the course?",
            (
                opt("Torque"),
                opt("Angular momentum", correct=True),
                opt("Kinetic energy"),
                opt("Moment of inertia"),
            ),
            "Angular momentum is the rotational counterpart of linear momentum and drives the next course.",
        ),
    ),
)
