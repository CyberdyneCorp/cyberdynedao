"""Curated quiz questions for the Circuit Analysis - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Capacitors & inductors": (
            q(
                "The i–v law for a capacitor is:",
                (
                    opt("$i_C = C\\,dv/dt$", correct=True),
                    opt("$v_C = C\\,di/dt$"),
                    opt("$i_C = v/C$"),
                    opt("$i_C = C\\,v$"),
                ),
                "A capacitor obeys $i_C = C\\,dv/dt$; an inductor obeys $v_L = L\\,di/dt$.",
            ),
            q(
                "At DC steady state (nothing changing), a capacitor and an inductor look like:",
                (
                    opt("capacitor → short, inductor → open"),
                    opt("capacitor → open, inductor → short", correct=True),
                    opt("both → open circuits"),
                    opt("both → short circuits"),
                ),
                "At DC, $i_C=0$ (open) and $v_L=0$ (short).",
            ),
            q(
                "The energy stored in a capacitor is:",
                (
                    opt("$\\tfrac12 C v^2$", correct=True),
                    opt("$C v$"),
                    opt("$\\tfrac12 C v$"),
                    opt("$C v^2$"),
                ),
                "Capacitor energy is $\\tfrac12 C v^2$; inductor energy is $\\tfrac12 L i^2$.",
            ),
        ),
        "First-order RC/RL transients": (
            q(
                "The time constant of an RC circuit is:",
                (
                    opt("$R/C$"),
                    opt("$RC$", correct=True),
                    opt("$L/R$"),
                    opt("$1/(RC)$"),
                ),
                "An RC circuit has $\\tau = RC$; an RL circuit has $\\tau = L/R$.",
            ),
            q(
                "After one time constant, a charging RC step response reaches about:",
                (
                    opt("37% of its final value"),
                    opt("50% of its final value"),
                    opt("63% of its final value", correct=True),
                    opt("99% of its final value"),
                ),
                "$v_C(\\tau)=V_s(1-e^{-1})\\approx 0.63\\,V_s$, i.e. about 63%.",
            ),
            q(
                "The general first-order response can be written as:",
                (
                    opt("$x(t) = x(\\infty) + (x(0) - x(\\infty))e^{-t/\\tau}$", correct=True),
                    opt("$x(t) = x(0)e^{t/\\tau}$"),
                    opt("$x(t) = x(\\infty)\\,t/\\tau$"),
                    opt("$x(t) = x(0) + x(\\infty)t$"),
                ),
                "Final value plus the decaying difference from the initial value: a single exponential.",
            ),
        ),
        "Second-order RLC transients": (
            q(
                "An RLC circuit with damping ratio $\\zeta < 1$ is:",
                (
                    opt("overdamped, with no oscillation"),
                    opt("underdamped, oscillating (ringing) while it decays", correct=True),
                    opt("critically damped"),
                    opt("unstable and growing"),
                ),
                "$\\zeta<1$ is underdamped: complex roots produce a decaying ringing response.",
            ),
            q(
                "Critical damping ($\\zeta = 1$) gives:",
                (
                    opt("the fastest response with no overshoot", correct=True),
                    opt("the slowest possible response"),
                    opt("sustained oscillation forever"),
                    opt("maximum overshoot"),
                ),
                "Critically damped is the fastest approach to the final value without overshoot.",
            ),
            q(
                "The undamped natural frequency of an RLC circuit is:",
                (
                    opt("$\\omega_0 = 1/\\sqrt{LC}$", correct=True),
                    opt("$\\omega_0 = \\sqrt{LC}$"),
                    opt("$\\omega_0 = R/L$"),
                    opt("$\\omega_0 = 1/(RC)$"),
                ),
                "The natural frequency is $\\omega_0 = 1/\\sqrt{LC}$.",
            ),
        ),
        "AC steady-state & phasors": (
            q(
                "In AC steady state, a linear circuit's response to a sinusoid is a sinusoid:",
                (
                    opt("at a different frequency, same amplitude"),
                    opt("at the same frequency, with changed amplitude and phase", correct=True),
                    opt("that is no longer sinusoidal"),
                    opt("only if the circuit is purely resistive"),
                ),
                "Linear circuits preserve frequency; only amplitude and phase change.",
            ),
            q(
                "A phasor represents a sinusoid $V_m\\cos(\\omega t+\\phi)$ by:",
                (
                    opt("its instantaneous value at $t=0$"),
                    opt(
                        "the complex number $V_m\\,e^{j\\phi}$ (amplitude and phase)", correct=True
                    ),
                    opt("its average value over one period"),
                    opt("its frequency alone"),
                ),
                "The phasor $V_m e^{j\\phi}=V_m\\angle\\phi$ keeps amplitude and phase, dropping $\\cos\\omega t$.",
            ),
            q(
                "Using phasors, the time-derivative operator $d/dt$ becomes:",
                (
                    opt("division by $\\omega$"),
                    opt("multiplication by $j\\omega$", correct=True),
                    opt("multiplication by $\\omega^2$"),
                    opt("a constant offset"),
                ),
                "In the phasor domain $d/dt \\to j\\omega$, turning calculus into algebra.",
            ),
        ),
        "Impedance & admittance": (
            q(
                "The impedance of an inductor is:",
                (
                    opt("$1/(j\\omega L)$"),
                    opt("$j\\omega L$", correct=True),
                    opt("$\\omega L$ (real)"),
                    opt("$L/(j\\omega)$"),
                ),
                "$Z_L = j\\omega L$; the capacitor is $Z_C = 1/(j\\omega C)$.",
            ),
            q(
                "Writing $Z = R + jX$, a positive reactance $X$ corresponds to:",
                (
                    opt("a capacitor, with voltage lagging current"),
                    opt("an inductor, with voltage leading current", correct=True),
                    opt("a pure resistor"),
                    opt("a short circuit"),
                ),
                "Inductive reactance is positive (voltage leads); capacitive is negative (voltage lags).",
            ),
            q(
                "Admittance $Y$ is defined as:",
                (
                    opt("$1/Z$", correct=True),
                    opt("$Z^2$"),
                    opt("$jZ$"),
                    opt("the real part of $Z$"),
                ),
                "Admittance is the reciprocal of impedance, $Y = 1/Z$.",
            ),
        ),
        "AC power & power factor": (
            q(
                "Real (average) power delivered to an AC load is:",
                (
                    opt("$V_{rms} I_{rms}\\sin\\theta$"),
                    opt("$V_{rms} I_{rms}\\cos\\theta$", correct=True),
                    opt("$V_{rms} I_{rms}$"),
                    opt("$V_{rms} I_{rms}\\tan\\theta$"),
                ),
                "Real power is $P = V_{rms}I_{rms}\\cos\\theta$ (watts).",
            ),
            q(
                "The power factor of a load is:",
                (
                    opt("$\\sin\\theta = Q/S$"),
                    opt("$\\cos\\theta = P/S$", correct=True),
                    opt("$\\tan\\theta = Q/P$"),
                    opt("$S/P$"),
                ),
                "Power factor is $\\cos\\theta = P/S$; it is 1 for a purely resistive load.",
            ),
            q(
                "Apparent ($S$), real ($P$) and reactive ($Q$) power are related by:",
                (
                    opt("$S = P + Q$"),
                    opt("$S^2 = P^2 + Q^2$", correct=True),
                    opt("$S = P - Q$"),
                    opt("$P^2 = S^2 + Q^2$"),
                ),
                "They form a right triangle: $S^2 = P^2 + Q^2$.",
            ),
        ),
    },
    final=(
        q(
            "Which two element laws are correct?",
            (
                opt("$i_C = C\\,dv/dt$ and $v_L = L\\,di/dt$", correct=True),
                opt("$v_C = C\\,di/dt$ and $i_L = L\\,dv/dt$"),
                opt("$i_C = v/C$ and $v_L = i/L$"),
                opt("$i_C = C\\,v$ and $v_L = L\\,i$"),
            ),
            "Capacitor: $i_C = C\\,dv/dt$. Inductor: $v_L = L\\,di/dt$.",
        ),
        q(
            "A first-order circuit settles to within about 1% of its final value after roughly:",
            (
                opt("$1\\tau$"),
                opt("$2\\tau$"),
                opt("$5\\tau$", correct=True),
                opt("$0.5\\tau$"),
            ),
            "After about $5\\tau$ the exponential has decayed to under 1% remaining.",
        ),
        q(
            "Matching damping regime to behaviour, which is correct?",
            (
                opt("Underdamped → no oscillation; overdamped → rings"),
                opt(
                    "Underdamped → rings; critically damped → fastest without overshoot",
                    correct=True,
                ),
                opt("Critically damped → maximum overshoot"),
                opt("Overdamped → unstable"),
            ),
            "Underdamped rings; critically damped is fastest with no overshoot; overdamped crawls in slowly.",
        ),
        q(
            "Which statement about phasor-domain impedances is correct?",
            (
                opt(
                    "$Z_L = j\\omega L$ and $Z_C = 1/(j\\omega C)$, and they combine like resistors",
                    correct=True,
                ),
                opt("$Z_L = 1/(j\\omega L)$ and $Z_C = j\\omega C$"),
                opt("impedances cannot be combined in series or parallel"),
                opt("all impedances are purely real"),
            ),
            "$Z_L=j\\omega L$, $Z_C=1/(j\\omega C)$, and series/parallel rules carry over from resistors.",
        ),
        q(
            "An inductor's reactance magnitude as frequency increases:",
            (
                opt("increases, since $|Z_L| = \\omega L$", correct=True),
                opt("decreases, since $|Z_L| = 1/(\\omega L)$"),
                opt("stays constant"),
                opt("becomes negative"),
            ),
            "$|Z_L| = \\omega L$ grows with frequency, so an inductor blocks high frequencies.",
        ),
        q(
            "Why do plants install power-factor-correction capacitors?",
            (
                opt("to increase reactive power $Q$"),
                opt(
                    "to cancel inductive reactive power and raise the power factor toward 1",
                    correct=True,
                ),
                opt("to lower the source voltage"),
                opt("to convert real power into reactive power"),
            ),
            "Capacitors supply leading reactive power that cancels inductive $Q$, pushing pf toward 1.",
        ),
    ),
)
