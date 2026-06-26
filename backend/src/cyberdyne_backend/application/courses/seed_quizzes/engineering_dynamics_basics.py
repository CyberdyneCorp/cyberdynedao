"""Quiz questions for the Engineering Dynamics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What dynamics studies": (
            q(
                "What distinguishes kinematics from kinetics?",
                (
                    opt(
                        "Kinematics describes motion; kinetics links forces to motion", correct=True
                    ),
                    opt("Kinematics deals with forces; kinetics ignores them"),
                    opt("They are two names for the same thing"),
                    opt("Kinematics applies only to rigid bodies"),
                ),
                "Kinematics is the geometry of motion (x, v, a); kinetics connects forces to that motion via Newton's laws.",
            ),
            q(
                "When is the particle model appropriate?",
                (
                    opt("When the body's rotation and size can be ignored", correct=True),
                    opt("Only when the body is literally a single atom"),
                    opt("Whenever the body is spinning quickly"),
                    opt("Only for bodies in static equilibrium"),
                ),
                "A particle has all mass at a point; it is valid when orientation/rotation does not matter.",
            ),
            q(
                "For constant acceleration, which equation is correct?",
                (
                    opt("x = x0 + v0 t + (1/2) a t^2", correct=True),
                    opt("x = x0 + (1/2) v0 t^2"),
                    opt("v = v0 + (1/2) a t^2"),
                    opt("x = v0 + a t"),
                ),
                "Integrating constant acceleration twice gives x = x0 + v0 t + (1/2) a t^2.",
            ),
        ),
        "Rectilinear motion: position, velocity, acceleration": (
            q(
                "On a velocity-time graph, what does the area under the curve represent?",
                (
                    opt("Displacement", correct=True),
                    opt("Acceleration"),
                    opt("Jerk"),
                    opt("Force"),
                ),
                "Area under v(t) is the integral of velocity, which is displacement; the slope is acceleration.",
            ),
            q(
                "A car brakes from 25 m/s at -6 m/s^2. Its approximate stopping distance is?",
                (
                    opt("About 52 m", correct=True),
                    opt("About 25 m"),
                    opt("About 150 m"),
                    opt("About 4 m"),
                ),
                "d = v0^2/(2|a|) = 625/12 ~= 52 m.",
            ),
            q(
                "The identity a dx = v dv is most useful when?",
                (
                    opt("Acceleration is known as a function of position", correct=True),
                    opt("Acceleration is always zero"),
                    opt("Time is the only known variable"),
                    opt("The motion is two-dimensional"),
                ),
                "It eliminates time, giving v^2 = v0^2 + 2 integral(a dx) when a depends on x.",
            ),
        ),
        "Curvilinear motion and projectiles": (
            q(
                "During projectile flight (no drag), the horizontal velocity is?",
                (
                    opt("Constant, because there is no horizontal force", correct=True),
                    opt("Increasing due to gravity"),
                    opt("Zero throughout"),
                    opt("Equal to the vertical velocity"),
                ),
                "Gravity acts only vertically, so the horizontal component stays constant.",
            ),
            q(
                "On flat ground, range is maximized at which launch angle?",
                (
                    opt("45 degrees", correct=True),
                    opt("30 degrees"),
                    opt("60 degrees"),
                    opt("90 degrees"),
                ),
                "R = v0^2 sin(2 theta)/g is largest when sin(2 theta) = 1, i.e. theta = 45 degrees.",
            ),
            q(
                "Why do the x and y motions of a projectile decouple?",
                (
                    opt(
                        "Because the acceleration (gravity) is constant and purely vertical",
                        correct=True,
                    ),
                    opt("Because air resistance couples them"),
                    opt("Because horizontal velocity is zero"),
                    opt("Because the path is a straight line"),
                ),
                "With constant acceleration only in y, each component integrates independently.",
            ),
        ),
        "Normal and tangential acceleration": (
            q(
                "Which acceleration component changes the direction of motion?",
                (
                    opt("Normal acceleration a_n = v^2/rho", correct=True),
                    opt("Tangential acceleration a_t = dv/dt"),
                    opt("Gravitational acceleration only"),
                    opt("None of them"),
                ),
                "The normal component points toward the center of curvature and turns the velocity vector.",
            ),
            q(
                "A body moving at constant speed around a curve has?",
                (
                    opt("Zero tangential but nonzero normal acceleration", correct=True),
                    opt("Zero total acceleration"),
                    opt("Nonzero tangential acceleration"),
                    opt("Zero normal acceleration"),
                ),
                "Constant speed means a_t = 0, but turning means a_n = v^2/rho is not zero.",
            ),
            q(
                "At v = 20 m/s on a curve of radius 50 m, the normal acceleration is?",
                (
                    opt("8 m/s^2", correct=True),
                    opt("0.4 m/s^2"),
                    opt("400 m/s^2"),
                    opt("2.5 m/s^2"),
                ),
                "a_n = v^2/rho = 400/50 = 8 m/s^2.",
            ),
        ),
        "Relative motion of particles": (
            q(
                "For non-rotating translating frames, how do velocities combine?",
                (
                    opt("v_B = v_A + v_B/A (vector addition)", correct=True),
                    opt("v_B = v_A - v_B/A only along x"),
                    opt("v_B = v_A * v_B/A"),
                    opt("Velocities cannot be related between frames"),
                ),
                "Relative motion adds vectorially: v_B equals v_A plus the velocity of B relative to A.",
            ),
            q(
                "A boat does 3 m/s relative to water against a 1.5 m/s current. To cross straight, aim?",
                (
                    opt("30 degrees upstream", correct=True),
                    opt("Straight across (0 degrees)"),
                    opt("60 degrees upstream"),
                    opt("Straight downstream"),
                ),
                "sin(alpha) = 1.5/3 = 0.5, so alpha = 30 degrees upstream cancels the drift.",
            ),
            q(
                "The term v_B/A means?",
                (
                    opt("The velocity of B as seen from A", correct=True),
                    opt("The velocity of A as seen from B"),
                    opt("The sum of both speeds"),
                    opt("The acceleration of B"),
                ),
                "v_B/A is the velocity of B measured in A's (translating) frame.",
            ),
        ),
        "Newton's second law: a first look": (
            q(
                "Newton's second law in vector form states?",
                (
                    opt("Sum of forces = m a", correct=True),
                    opt("Sum of forces = m v"),
                    opt("Sum of forces = 0 always"),
                    opt("Sum of forces = m / a"),
                ),
                "The net force equals mass times acceleration, component by component.",
            ),
            q(
                "On a frictionless incline of angle theta, a block's acceleration is?",
                (
                    opt("g sin(theta), independent of mass", correct=True),
                    opt("g cos(theta), proportional to mass"),
                    opt("g, regardless of angle"),
                    opt("Zero"),
                ),
                "Only the weight component m g sin(theta) acts along the slope, so a = g sin(theta), mass cancels.",
            ),
            q(
                "Why draw a free-body diagram first?",
                (
                    opt(
                        "To isolate the body and show every external force before writing equations",
                        correct=True,
                    ),
                    opt("To compute energy directly"),
                    opt("Because it replaces Newton's law"),
                    opt("To find the natural frequency"),
                ),
                "An FBD isolates the body and exposes all external forces so the equations of motion can be written correctly.",
            ),
        ),
    },
    final=(
        q(
            "Which pair correctly defines velocity and acceleration?",
            (
                opt("v = dx/dt and a = dv/dt", correct=True),
                opt("v = dv/dt and a = dx/dt"),
                opt("v = integral of a and a = integral of v"),
                opt("v = a t^2 and a = v t"),
            ),
            "Velocity is the time derivative of position; acceleration is the time derivative of velocity.",
        ),
        q(
            "A projectile launched at 20 m/s and 45 degrees has a range of about?",
            (
                opt("About 41 m", correct=True),
                opt("About 20 m"),
                opt("About 80 m"),
                opt("About 4 m"),
            ),
            "R = v0^2 sin(2 theta)/g = 400 * 1 / 9.81 ~= 41 m.",
        ),
        q(
            "Centripetal (normal) acceleration depends on?",
            (
                opt("Speed squared divided by radius of curvature", correct=True),
                opt("Speed divided by radius"),
                opt("Radius divided by speed"),
                opt("Only the tangential force"),
            ),
            "a_n = v^2/rho points toward the center of curvature.",
        ),
        q(
            "Which statement about relative velocity is correct?",
            (
                opt("v_B = v_A + v_B/A for translating frames", correct=True),
                opt("Relative velocity is always zero"),
                opt("v_B/A equals v_A/B"),
                opt("Velocities multiply between frames"),
            ),
            "Velocities add vectorially; v_B/A is the negative of v_A/B.",
        ),
        q(
            "Weight and mass differ how?",
            (
                opt(
                    "Mass is inertia (kg); weight is the gravitational force m g (N)", correct=True
                ),
                opt("They are identical quantities"),
                opt("Weight is measured in kilograms"),
                opt("Mass changes with location, weight does not"),
            ),
            "Mass is constant inertia; weight W = m g is a force that varies with g.",
        ),
        q(
            "A block on a frictionless 30 degree incline accelerates at about?",
            (
                opt("About 4.9 m/s^2", correct=True),
                opt("About 9.8 m/s^2"),
                opt("About 8.5 m/s^2"),
                opt("Zero"),
            ),
            "a = g sin(30) = 9.81 * 0.5 ~= 4.9 m/s^2, independent of mass.",
        ),
    ),
)
