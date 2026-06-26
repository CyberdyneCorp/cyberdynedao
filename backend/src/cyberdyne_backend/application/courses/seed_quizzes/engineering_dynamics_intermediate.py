"""Quiz questions for the Engineering Dynamics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Equations of motion with friction": (
            q(
                "How do static and kinetic Coulomb friction compare?",
                (
                    opt("Static can be larger; mu_k is less than mu_s", correct=True),
                    opt("Kinetic is always larger than static"),
                    opt("They are always exactly equal"),
                    opt("Static friction does not exist"),
                ),
                "Static friction holds up to mu_s N; once sliding, kinetic friction mu_k N applies with mu_k < mu_s.",
            ),
            q(
                "Pulling a block with an upward-angled force does what to the normal force?",
                (
                    opt("Reduces it, which reduces friction", correct=True),
                    opt("Increases it, which increases friction"),
                    opt("Leaves it unchanged"),
                    opt("Makes it negative immediately"),
                ),
                "The upward component lowers N = m g - P sin(phi), so kinetic friction mu_k N drops.",
            ),
            q(
                "Kinetic friction force always acts in which direction?",
                (
                    opt("Opposite to the direction of sliding", correct=True),
                    opt("In the direction of motion"),
                    opt("Perpendicular to the surface"),
                    opt("Toward the center of curvature"),
                ),
                "Kinetic friction opposes relative sliding motion.",
            ),
        ),
        "Work and the work-energy theorem": (
            q(
                "The work-energy theorem states that net work equals?",
                (
                    opt("The change in kinetic energy", correct=True),
                    opt("The change in momentum"),
                    opt("The total force"),
                    opt("The impulse applied"),
                ),
                "U(1->2) = T2 - T1, the change in kinetic energy.",
            ),
            q(
                "Why does the normal force usually do no work?",
                (
                    opt("It is perpendicular to the displacement", correct=True),
                    opt("It is always zero"),
                    opt("It is a conservative force"),
                    opt("It acts only at the start"),
                ),
                "Work is force dotted with displacement; a perpendicular force contributes nothing.",
            ),
            q(
                "An ideal spring compressed by x stores how much energy?",
                (
                    opt("(1/2) k x^2", correct=True),
                    opt("k x"),
                    opt("(1/2) k x"),
                    opt("k x^2"),
                ),
                "Spring potential energy is (1/2) k x^2.",
            ),
        ),
        "Conservative forces and energy conservation": (
            q(
                "Which force is conservative?",
                (
                    opt("Gravity", correct=True),
                    opt("Kinetic friction"),
                    opt("Air drag"),
                    opt("A time-varying applied force"),
                ),
                "Gravity (and ideal springs) are conservative; friction and drag dissipate energy.",
            ),
            q(
                "A pendulum of length L released from rest at angle theta0 reaches what speed at the bottom?",
                (
                    opt("sqrt(2 g L (1 - cos theta0))", correct=True),
                    opt("sqrt(2 g L cos theta0)"),
                    opt("g L theta0"),
                    opt("sqrt(g / L)"),
                ),
                "Energy conservation: (1/2) m v^2 = m g L (1 - cos theta0).",
            ),
            q(
                "When non-conservative forces act, energy bookkeeping becomes?",
                (
                    opt("T1 + V1 + U_nc = T2 + V2", correct=True),
                    opt("T1 + V1 = T2 + V2 still holds exactly"),
                    opt("Energy can be ignored entirely"),
                    opt("Momentum replaces energy"),
                ),
                "Add the non-conservative work term U_nc (negative for friction/drag).",
            ),
        ),
        "Linear impulse and momentum": (
            q(
                "The impulse-momentum principle equates impulse to?",
                (
                    opt("The change in linear momentum", correct=True),
                    opt("The change in kinetic energy"),
                    opt("The change in potential energy"),
                    opt("The change in position"),
                ),
                "Integral of net force over time equals m v2 - m v1.",
            ),
            q(
                "When is linear momentum conserved?",
                (
                    opt("When the net external impulse is zero", correct=True),
                    opt("Whenever kinetic energy is conserved"),
                    opt("Only in elastic collisions"),
                    opt("Always, without exception"),
                ),
                "Zero net external impulse means momentum is unchanged.",
            ),
            q(
                "A 0.15 kg ball hits a wall at 20 m/s and rebounds at 15 m/s. The impulse magnitude is?",
                (
                    opt("About 5.25 N s", correct=True),
                    opt("About 0.75 N s"),
                    opt("About 3.0 N s"),
                    opt("About 35 N s"),
                ),
                "J = m (v2 - v1) = 0.15 * (15 - (-20)) = 5.25 N s.",
            ),
        ),
        "Angular momentum and impact": (
            q(
                "Angular momentum of a particle about O is defined as?",
                (
                    opt("r cross m v", correct=True),
                    opt("m v only"),
                    opt("I alpha"),
                    opt("(1/2) m v^2"),
                ),
                "H_O = r x m v; its rate of change equals the net moment about O.",
            ),
            q(
                "The coefficient of restitution e = 1 corresponds to?",
                (
                    opt("A perfectly elastic impact (kinetic energy conserved)", correct=True),
                    opt("A perfectly plastic impact (bodies stick)"),
                    opt("Zero relative velocity before impact"),
                    opt("Infinite contact force"),
                ),
                "e = 1 is fully elastic; e = 0 is fully plastic where bodies move together.",
            ),
            q(
                "Why does a skater spin faster when pulling in their arms?",
                (
                    opt(
                        "Angular momentum is conserved while moment of inertia decreases",
                        correct=True,
                    ),
                    opt("Their kinetic energy is conserved"),
                    opt("Their linear momentum increases"),
                    opt("An external torque speeds them up"),
                ),
                "With no external moment H = I omega is constant; lowering I raises omega.",
            ),
        ),
        "Numerical integration of the equations of motion": (
            q(
                "To integrate m x'' = F, you first recast it as?",
                (
                    opt("A first-order state system in [x, v]", correct=True),
                    opt("A single algebraic equation"),
                    opt("A purely static balance"),
                    opt("A frequency-domain transfer function"),
                ),
                "Define y = [x, v] so y' = [v, F/m], a first-order system for solve_ivp.",
            ),
            q(
                "Which SciPy method suits a stiff system with widely separated time constants?",
                (
                    opt("Radau or BDF", correct=True),
                    opt("RK45 always"),
                    opt("Forward Euler with a huge step"),
                    opt("A frequency sweep"),
                ),
                "Implicit methods like Radau/BDF handle stiffness; RK45 is the default for non-stiff problems.",
            ),
            q(
                "Why does quadratic drag prevent a closed-form projectile solution?",
                (
                    opt(
                        "Drag depends on the speed |v|, coupling the x and y motions nonlinearly",
                        correct=True,
                    ),
                    opt("Drag removes gravity"),
                    opt("Drag is perpendicular to velocity"),
                    opt("Drag makes the path a perfect parabola"),
                ),
                "Quadratic drag couples the components through |v|, so the equations are nonlinear and need numerics.",
            ),
        ),
    },
    final=(
        q(
            "For a block pushed at angle phi, the kinetic-friction normal force is?",
            (
                opt("N = m g - P sin(phi) for an upward-angled push", correct=True),
                opt("N = m g + P always"),
                opt("N = P cos(phi)"),
                opt("N = mu_k m g regardless of P"),
            ),
            "An upward force component reduces N to m g - P sin(phi).",
        ),
        q(
            "Which method most directly gives a speed as a function of position?",
            (
                opt("Work-energy theorem", correct=True),
                opt("Impulse-momentum"),
                opt("Coefficient of restitution"),
                opt("Free-body diagram alone"),
            ),
            "Work integrates force over distance, relating speed to position via T2 - T1.",
        ),
        q(
            "Mechanical energy is conserved when?",
            (
                opt("Only conservative forces do work", correct=True),
                opt("Friction is present"),
                opt("An external impulse acts"),
                opt("The body is at rest"),
            ),
            "T + V is constant when no non-conservative force does work.",
        ),
        q(
            "Two particles collide with no external force. What is conserved?",
            (
                opt("Total linear momentum", correct=True),
                opt("Total kinetic energy in all cases"),
                opt("Each particle's individual velocity"),
                opt("The coefficient of restitution only"),
            ),
            "Momentum is always conserved in an isolated collision; kinetic energy only when e = 1.",
        ),
        q(
            "The coefficient of restitution relates which speeds?",
            (
                opt("Separation speed to approach speed along the line of impact", correct=True),
                opt("Total momentum to total energy"),
                opt("Angular to linear momentum"),
                opt("Static to kinetic friction"),
            ),
            "e = (separation speed)/(approach speed), between 0 and 1.",
        ),
        q(
            "When numerically integrating dynamics, an event function is used to?",
            (
                opt("Stop integration at a condition such as ground impact", correct=True),
                opt("Increase the order of the method"),
                opt("Convert the problem to static equilibrium"),
                opt("Remove gravity from the model"),
            ),
            "An event with terminal=True halts solve_ivp when a condition (e.g. height = 0) is met.",
        ),
    ),
)
