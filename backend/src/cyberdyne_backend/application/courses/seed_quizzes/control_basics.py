from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is control? A short history": (
            q(
                "In one sentence, what is the core loop of control engineering?",
                (
                    opt("Command an input and never look at the result"),
                    opt("Measure, compare to a goal, correct, repeat", correct=True),
                    opt("Solve the plant model once and run it open loop forever"),
                    opt("Add as much gain as possible until it is fast"),
                ),
                "Control means measuring what a system does and adjusting the input: measure, compare to a goal, correct, repeat.",
            ),
            q(
                "James Watt's 1788 flyball governor is remembered as what?",
                (
                    opt("The first frequency-domain stability tool"),
                    opt("The first state-space model"),
                    opt("The first widely-used automatic feedback controller", correct=True),
                    opt("The first model predictive controller"),
                ),
                "Watt's spinning-ball governor held a steam engine's speed steady and is the first widely-used automatic feedback controller.",
            ),
            q(
                "Rudolf Kalman's 1960 contribution split the field by introducing which framework?",
                (
                    opt("State-space and modern control", correct=True),
                    opt("The root-locus method"),
                    opt("Proportional-integral-derivative action"),
                    opt("Active Disturbance Rejection Control"),
                ),
                "Kalman recast control in state-space and gave the Kalman filter, splitting the field into classic (frequency-domain) and modern (state-space).",
            ),
        ),
        "Open loop vs. closed loop": (
            q(
                "How is the error e defined in a closed-loop system?",
                (
                    opt("e = y - u, output minus control"),
                    opt("e = r - y, setpoint minus measurement", correct=True),
                    opt("e = r + y, setpoint plus measurement"),
                    opt("e = u - r, control minus setpoint"),
                ),
                "The controller drives the error e = r - y, the setpoint minus the measured output, toward zero.",
            ),
            q(
                "Which benefit does feedback provide that open loop never can?",
                (
                    opt("Zero sensor cost"),
                    opt("Guaranteed stability with any gain"),
                    opt("Disturbance rejection", correct=True),
                    opt("Immunity to measurement noise"),
                ),
                "Feedback rejects disturbances: when a gust or load pushes the output off, the error grows and the controller pushes back.",
            ),
            q(
                "What is a cost or risk that feedback introduces?",
                (
                    opt("It removes the need for any model"),
                    opt("The risk of instability if you push back too hard", correct=True),
                    opt("It makes the system slower in every case"),
                    opt("It eliminates the ability to track a setpoint"),
                ),
                "Feedback needs a sensor and risks instability and sensitivity to measurement noise; managing those trade-offs is control design.",
            ),
        ),
        "System response: first & second order": (
            q(
                "For a first-order system with time constant tau, the output reaches what fraction of its final value in tau seconds?",
                (
                    opt("about 37 percent"),
                    opt("about 50 percent"),
                    opt("about 63 percent", correct=True),
                    opt("about 98 percent"),
                ),
                "A first-order response reaches about 63 percent of its final value in one time constant tau, and about 98 percent in 4 tau.",
            ),
            q(
                "In a second-order system, which parameter controls how oscillatory the response is?",
                (
                    opt("the damping ratio zeta", correct=True),
                    opt("the natural frequency omega_n"),
                    opt("the steady-state gain K"),
                    opt("the time constant tau"),
                ),
                "The damping ratio zeta sets how oscillatory the response is, while the natural frequency omega_n sets how fast.",
            ),
            q(
                "Which damping condition gives the fastest response with no overshoot?",
                (
                    opt("underdamped, zeta < 1"),
                    opt("critically damped, zeta = 1", correct=True),
                    opt("overdamped, zeta > 1"),
                    opt("undamped, zeta = 0"),
                ),
                "Critically damped (zeta = 1) is the sweet spot: the fastest response with no overshoot; underdamped overshoots and overdamped is sluggish.",
            ),
        ),
        "Meet the PID controller": (
            q(
                "Which PID term erases the steady-state offset that proportional control alone leaves?",
                (
                    opt("the proportional term P"),
                    opt("the integral term I", correct=True),
                    opt("the derivative term D"),
                    opt("the feedforward term"),
                ),
                "P alone leaves a steady-state error; the integral term I accumulates past error until the offset is gone.",
            ),
            q(
                "What undesirable side effect does the derivative term D have?",
                (
                    opt("It removes steady-state error"),
                    opt("It amplifies measurement noise", correct=True),
                    opt("It causes integral windup"),
                    opt("It always destabilises the loop"),
                ),
                "D reacts to the rate of change and adds damping, but it amplifies noise, so it is almost always filtered.",
            ),
            q(
                "Under proportional control of a first-order plant, the step response settles at what value?",
                (
                    opt("exactly 1, the setpoint"),
                    opt("Kp / (1 + Kp), just below 1", correct=True),
                    opt("1 + Kp, above the setpoint"),
                    opt("zero"),
                ),
                "The closed-loop response settles at Kp/(1+Kp), always below 1; that residual gap is the steady-state error the integral term exists to erase.",
            ),
        ),
        "Lab: simulate a PI controller": (
            q(
                "In the lab, what happens to the steady-state error when you set Ki = 0 (pure P control)?",
                (
                    opt("a steady-state offset appears", correct=True),
                    opt("the error is driven exactly to zero"),
                    opt("the output diverges to infinity"),
                    opt("the controller stops producing any output"),
                ),
                "With Ki = 0 the loop is pure proportional, so a steady-state offset appears; adding integral action removes it.",
            ),
            q(
                "In the discrete PI loop, how is the integral term updated each step?",
                (
                    opt("integral = e / dt"),
                    opt("integral += e * dt", correct=True),
                    opt("integral = Kp * e"),
                    opt("integral -= Kd * e"),
                ),
                "The integral accumulates the error over time: integral += e*dt each step, and the control law is uk = Kp*e + Ki*integral.",
            ),
            q(
                "Raising Ki to a large value (e.g. 6) in the lab tends to do what?",
                (
                    opt("remove the offset faster but grow the overshoot", correct=True),
                    opt("eliminate overshoot entirely"),
                    opt("introduce a permanent steady-state error"),
                    opt("have no effect on the response"),
                ),
                "Raising Ki removes the offset faster but the overshoot grows, illustrating the integral term's lag and windup tendency.",
            ),
        ),
    },
    final=(
        q(
            "What single idea unifies every controller from Watt's governor to PID?",
            (
                opt("run the input open loop and trust the model"),
                opt("measure, compare to a goal, correct", correct=True),
                opt("maximise the proportional gain"),
                opt("avoid using any sensor"),
            ),
            "Every feedback loop follows the same idea: measure the output, compare to the goal, and correct.",
        ),
        q(
            "A microwave that runs for 30 seconds regardless of food temperature is an example of what?",
            (
                opt("closed-loop control"),
                opt("open-loop control", correct=True),
                opt("PID control"),
                opt("disturbance rejection"),
            ),
            "Running a fixed time with no measurement and no correction is open-loop control: cheap and simple but helpless against surprises.",
        ),
        q(
            "Which damping ratio is a common practical target giving about 5 percent overshoot and quick settling?",
            (
                opt("zeta = 0.1"),
                opt("zeta = 0.7", correct=True),
                opt("zeta = 1.5"),
                opt("zeta = 0.0"),
            ),
            "A damping ratio of about 0.7 is a common target: roughly 5 percent overshoot with quick settling.",
        ),
        q(
            "Match each PID term to its primary effect.",
            (
                opt("I adds damping; D removes offset; P amplifies noise"),
                opt("P speeds response; I removes offset; D adds damping", correct=True),
                opt("P removes offset; I adds damping; D speeds response"),
                opt("D removes offset; P adds damping; I amplifies noise"),
            ),
            "P pushes proportional to error (faster, stiffer), I removes steady-state offset, and D adds damping to tame overshoot.",
        ),
        q(
            "What is the recommended practical order for tuning a PID loop?",
            (
                opt("set D first, then I, then P"),
                opt("set all three gains as high as possible at once"),
                opt(
                    "get a reasonable P, add I to remove offset, add a little filtered D",
                    correct=True,
                ),
                opt("use only I and never P or D"),
            ),
            "Get a reasonable P for speed, add I to remove offset, add a little filtered D to tame overshoot, then stop: simpler loops are more robust.",
        ),
    ),
)
