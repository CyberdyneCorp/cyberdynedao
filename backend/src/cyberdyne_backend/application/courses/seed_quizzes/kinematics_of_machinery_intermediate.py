"""Quiz questions for the Kinematics & Dynamics of Machinery - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Vector-loop position analysis": (
            q(
                "The vector-loop (loop-closure) equation expresses that:",
                (
                    opt("the link vectors sum to zero around the closed chain", correct=True),
                    opt("the link masses are equal"),
                    opt("the angular velocities cancel"),
                    opt("friction is neglected"),
                ),
                "Closure means the position vectors form a closed polygon, summing to zero.",
            ),
            q(
                "Splitting the complex four-bar loop into real and imaginary parts gives:",
                (
                    opt("two scalar equations in two unknown angles", correct=True),
                    opt("one linear equation"),
                    opt("four independent unknowns"),
                    opt("no usable equations"),
                ),
                "Real and imaginary parts yield two nonlinear scalar equations for theta3 and theta4.",
            ),
            q(
                "These position equations are typically solved numerically with:",
                (
                    opt("Newton-Raphson iteration", correct=True),
                    opt("simple matrix inversion of a linear system"),
                    opt("the quadratic formula only"),
                    opt("a Fourier transform"),
                ),
                "The position equations are nonlinear (sines/cosines), so Newton-Raphson is standard.",
            ),
        ),
        "Velocity analysis and instant centers": (
            q(
                "Differentiating the position loop once with respect to time gives equations that are:",
                (
                    opt("linear in the unknown angular velocities", correct=True),
                    opt("still nonlinear in the velocities"),
                    opt("independent of position"),
                    opt("quadratic in the velocities"),
                ),
                "Once positions are known, the velocity loop is a linear system in w3 and w4.",
            ),
            q(
                "The number of instant centers of an n-link mechanism is:",
                (
                    opt("n(n-1)/2", correct=True),
                    opt("n(n+1)/2"),
                    opt("2n"),
                    opt("n squared"),
                ),
                "Each pair of links has one instant center, giving N = n(n-1)/2.",
            ),
            q(
                "The Kennedy-Aronhold theorem states that for any three bodies, their three instant centers are:",
                (
                    opt("collinear (lie on one straight line)", correct=True),
                    opt("always coincident"),
                    opt("perpendicular"),
                    opt("at infinity"),
                ),
                "Kennedy's theorem: the three ICs shared by any three bodies are collinear.",
            ),
        ),
        "Acceleration analysis and the Coriolis term": (
            q(
                "The normal (centripetal) acceleration of a point on a rotating link has magnitude:",
                (
                    opt("omega squared times r", correct=True),
                    opt("alpha times r"),
                    opt("omega times r"),
                    opt("2 omega r"),
                ),
                "Normal acceleration is omega^2 * r, directed toward the center of rotation.",
            ),
            q(
                "Coriolis acceleration appears whenever a point:",
                (
                    opt("slides along a link that is also rotating", correct=True),
                    opt("moves in a straight line at constant speed"),
                    opt("is fixed to a rigid link"),
                    opt("is at the center of rotation"),
                ),
                "The 2*omega*v_rel Coriolis term arises with relative sliding on a rotating member.",
            ),
            q(
                "The magnitude of the Coriolis acceleration is:",
                (
                    opt("2 omega v_rel", correct=True),
                    opt("omega squared r"),
                    opt("alpha r"),
                    opt("omega v_rel / 2"),
                ),
                "a_cor = 2 * omega x v_rel, magnitude 2*omega*v_rel.",
            ),
        ),
        "Cam profiles and follower motion": (
            q(
                "The fundamental law of cam design requires that the follower's:",
                (
                    opt("displacement, velocity and acceleration all be continuous", correct=True),
                    opt("velocity be constant"),
                    opt("acceleration be infinite at dwells"),
                    opt("displacement be discontinuous"),
                ),
                "Continuity of s, v and a (finite jerk) avoids shock and vibration.",
            ),
            q(
                "Which standard rise motion has acceleration that starts and ends at zero?",
                (
                    opt("cycloidal", correct=True),
                    opt("constant velocity"),
                    opt("simple harmonic"),
                    opt("constant acceleration with sudden reversal"),
                ),
                "Cycloidal motion has zero acceleration at both boundaries, ideal for high speed.",
            ),
            q(
                "For a translating follower, the pressure angle should generally be kept below about:",
                (
                    opt("30 degrees", correct=True),
                    opt("80 degrees"),
                    opt("60 degrees"),
                    opt("0 degrees exactly"),
                ),
                "Keeping the pressure angle under ~30 deg limits side thrust; enlarge the base circle if exceeded.",
            ),
        ),
        "Gear trains and the train value": (
            q(
                "For a single external mesh, the speed ratio omega3/omega2 equals:",
                (
                    opt("minus N2/N3", correct=True),
                    opt("plus N3/N2"),
                    opt("N2 times N3"),
                    opt("N2 plus N3"),
                ),
                "Ratio is inverse to tooth counts; the minus sign reflects reversed rotation for external gears.",
            ),
            q(
                "In a simple gear train, idler gears between input and output:",
                (
                    opt("do not change the overall ratio (only the sense)", correct=True),
                    opt("multiply the ratio by their tooth count"),
                    opt("double the output torque"),
                    opt("set the train value alone"),
                ),
                "Idlers cancel in a simple train; only the first and last gears set the magnitude.",
            ),
            q(
                "Epicyclic (planetary) trains are most easily solved with the:",
                (
                    opt("formula method using motion relative to the carrier", correct=True),
                    opt("simple-train idler cancellation rule"),
                    opt("Freudenstein equation"),
                    opt("Kennedy theorem"),
                ),
                "The relative-to-carrier formula (w_last - w_c)/(w_first - w_c) = e handles planetaries.",
            ),
        ),
    },
    final=(
        q(
            "Loop-closure position equations for a four-bar are:",
            (
                opt("nonlinear and solved iteratively", correct=True),
                opt("linear and solved by inversion"),
                opt("trivially zero"),
                opt("independent of crank angle"),
            ),
            "Sines and cosines make them nonlinear; Newton-Raphson or Freudenstein solves them.",
        ),
        q(
            "After positions are known, the velocity equations are:",
            (
                opt("linear in the angular velocities", correct=True),
                opt("nonlinear in the velocities"),
                opt("undefined"),
                opt("quadratic"),
            ),
            "Differentiating once yields a linear system for the unknown angular velocities.",
        ),
        q(
            "The Coriolis term 2*omega*v_rel must be included when there is:",
            (
                opt("sliding along a rotating link", correct=True),
                opt("pure rotation of a rigid link"),
                opt("a stationary mechanism"),
                opt("constant straight-line motion"),
            ),
            "Relative sliding on a rotating member produces the Coriolis acceleration.",
        ),
        q(
            "The preferred high-speed cam rise motion is:",
            (
                opt("cycloidal", correct=True),
                opt("constant velocity"),
                opt("instantaneous step"),
                opt("simple harmonic for shock loads"),
            ),
            "Cycloidal motion has continuous, zero-at-ends acceleration, minimizing vibration.",
        ),
        q(
            "The train value e of a compound gear train is:",
            (
                opt("product of driver teeth over product of driven teeth", correct=True),
                opt("sum of all tooth counts"),
                opt("set only by the idler gears"),
                opt("the first gear's tooth count"),
            ),
            "e = (product of drivers)/(product of driven), multiplying across each mesh.",
        ),
        q(
            "The number of instant centers in a four-bar (n = 4) is:",
            (
                opt("6", correct=True),
                opt("4"),
                opt("3"),
                opt("12"),
            ),
            "N = n(n-1)/2 = 4*3/2 = 6.",
        ),
    ),
)
