"""Curated quiz questions for the Circuit Analysis - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Frequency response & resonance": (
            q(
                "The resonant frequency of a series RLC circuit is:",
                (
                    opt("$\\omega_0 = 1/\\sqrt{LC}$", correct=True),
                    opt("$\\omega_0 = R/L$"),
                    opt("$\\omega_0 = \\sqrt{LC}$"),
                    opt("$\\omega_0 = 1/(RC)$"),
                ),
                "At $\\omega_0 = 1/\\sqrt{LC}$ the inductive and capacitive reactances cancel.",
            ),
            q(
                "At resonance in a series RLC circuit, the impedance is:",
                (
                    opt("maximum and purely reactive"),
                    opt("minimum and purely resistive", correct=True),
                    opt("zero"),
                    opt("infinite"),
                ),
                "The reactances cancel, leaving a minimum, purely resistive impedance, so current peaks.",
            ),
            q(
                "A higher quality factor $Q$ produces a resonance peak that is:",
                (
                    opt("taller and narrower (smaller bandwidth)", correct=True),
                    opt("shorter and wider"),
                    opt("shifted to a lower frequency"),
                    opt("independent of bandwidth"),
                ),
                "$\\text{BW} = \\omega_0/Q$, so high $Q$ gives a narrow, selective peak.",
            ),
        ),
        "The Laplace transform for circuits": (
            q(
                "In the Laplace domain, the s-domain impedance of an inductor is:",
                (
                    opt("$1/(sL)$"),
                    opt("$sL$", correct=True),
                    opt("$L$"),
                    opt("$sC$"),
                ),
                "s-domain impedances: $Z_R=R$, $Z_L=sL$, $Z_C=1/(sC)$.",
            ),
            q(
                "The Laplace transform turns differentiation in time into:",
                (
                    opt("integration"),
                    opt("multiplication by $s$ (with the initial condition)", correct=True),
                    opt("division by $\\omega$"),
                    opt("a phase shift of 90 degrees"),
                ),
                "$\\mathcal{L}\\{df/dt\\} = sF(s) - f(0^-)$, converting ODEs into algebra in $s$.",
            ),
            q(
                "Setting $s = j\\omega$ in the Laplace analysis recovers:",
                (
                    opt("the DC resistive solution"),
                    opt("the phasor / AC steady-state result", correct=True),
                    opt("an unstable response"),
                    opt("the initial conditions only"),
                ),
                "Laplace contains AC ($s=j\\omega$) and DC ($s=0$) as special cases.",
            ),
        ),
        "Transfer functions, poles & zeros": (
            q(
                "A transfer function $H(s)$ is defined (with zero initial conditions) as:",
                (
                    opt("input over output, $X(s)/Y(s)$"),
                    opt("output over input, $Y(s)/X(s)$", correct=True),
                    opt("the product of input and output"),
                    opt("the derivative of the output"),
                ),
                "$H(s) = Y(s)/X(s)$, a ratio of polynomials $N(s)/D(s)$.",
            ),
            q(
                "The poles of $H(s)$ are:",
                (
                    opt("the roots of the numerator $N(s)$"),
                    opt("the roots of the denominator $D(s)$", correct=True),
                    opt("the frequencies where the output is nulled"),
                    opt("always located at the origin"),
                ),
                "Poles are roots of $D(s)$ (natural frequencies); zeros are roots of $N(s)$ (output nulls).",
            ),
            q(
                "A circuit is stable when all of its poles lie:",
                (
                    opt("in the right half of the s-plane"),
                    opt("in the left half of the s-plane ($\\sigma < 0$)", correct=True),
                    opt("exactly on the imaginary axis"),
                    opt("at the origin"),
                ),
                "Left-half-plane poles ($\\sigma<0$) decay → stable; right-half-plane poles grow → unstable.",
            ),
        ),
        "Two-port networks": (
            q(
                "Which parameter set relates port voltages to port currents as $\\mathbf{V} = \\mathbf{z}\\mathbf{I}$?",
                (
                    opt("z-parameters (impedance)", correct=True),
                    opt("y-parameters (admittance)"),
                    opt("h-parameters (hybrid)"),
                    opt("ABCD parameters"),
                ),
                "z-parameters give $\\mathbf{V} = \\mathbf{z}\\,\\mathbf{I}$ from open-circuit tests.",
            ),
            q(
                "Cascading two two-ports (output into input) is computed by:",
                (
                    opt("adding their z-matrices"),
                    opt("multiplying their ABCD (transmission) matrices", correct=True),
                    opt("inverting their y-matrices"),
                    opt("averaging their h-parameters"),
                ),
                "The ABCD form makes a cascade equal to the matrix product of the individual ABCD matrices.",
            ),
            q(
                "Hybrid (h) parameters are especially associated with:",
                (
                    opt("transmission-line cascades"),
                    opt("transistor small-signal models (e.g. $h_{fe}=\\beta$)", correct=True),
                    opt("purely resistive networks"),
                    opt("ideal voltage sources"),
                ),
                "h-parameters mix voltage and current and are the classic transistor model parameters.",
            ),
        ),
        "Coupled inductors & transformers": (
            q(
                "The coupling coefficient between two inductors is:",
                (
                    opt("$k = M/\\sqrt{L_1 L_2}$, with $0 \\le k \\le 1$", correct=True),
                    opt("$k = \\sqrt{L_1 L_2}/M$"),
                    opt("$k = M L_1 L_2$"),
                    opt("$k = L_1/L_2$"),
                ),
                "$k = M/\\sqrt{L_1 L_2}$ measures shared flux, between 0 and 1.",
            ),
            q(
                "For an ideal transformer with turns ratio $n = N_1/N_2$:",
                (
                    opt("$V_1/V_2 = n$ and $I_1/I_2 = 1/n$", correct=True),
                    opt("$V_1/V_2 = 1/n$ and $I_1/I_2 = n$"),
                    opt("$V_1/V_2 = n^2$"),
                    opt("voltage and current both scale by $n$"),
                ),
                "Voltage scales by $n$, current by $1/n$, so power in equals power out.",
            ),
            q(
                "A load $Z_L$ on the secondary reflects to the primary as:",
                (
                    opt("$Z_L/n$"),
                    opt("$n\\,Z_L$"),
                    opt("$n^2 Z_L$", correct=True),
                    opt("$Z_L/n^2$"),
                ),
                "Impedance reflects by the square of the turns ratio: $Z_{in} = n^2 Z_L$.",
            ),
        ),
        "Applied circuit analysis": (
            q(
                "To find the DC operating point of a circuit with reactive elements, you:",
                (
                    opt("open the inductors and short the capacitors"),
                    opt(
                        "short the inductors and open the capacitors, then use nodal/mesh + Thevenin",
                        correct=True,
                    ),
                    opt("solve the full Laplace transform"),
                    opt("ignore all the resistors"),
                ),
                "At DC, inductors are shorts and capacitors are opens; then apply resistive-circuit methods.",
            ),
            q(
                "Which analysis is the right tool for predicting transient stability?",
                (
                    opt("DC nodal analysis"),
                    opt("examining the poles of $H(s)$ in the Laplace domain", correct=True),
                    opt("the maximum power transfer theorem"),
                    opt("a single voltage-divider calculation"),
                ),
                "Pole locations of $H(s)$ reveal the damping and stability of the transient response.",
            ),
            q(
                "The unifying theme of the track is that DC, AC and transient analysis are the same circuit at:",
                (
                    opt(
                        "$s = 0$ (DC), $s = j\\omega$ (AC), and general $s$ (transient)",
                        correct=True,
                    ),
                    opt("three unrelated sets of physical laws"),
                    opt("only resistive operating points"),
                    opt("frequencies above resonance only"),
                ),
                "DC is $s=0$, AC is $s=j\\omega$, and the full transient is general $s$ — one linear circuit.",
            ),
        ),
    },
    final=(
        q(
            "At series resonance, what happens to impedance and current?",
            (
                opt("impedance is minimum and resistive; current peaks", correct=True),
                opt("impedance is maximum; current is zero"),
                opt("impedance is purely reactive; current is unchanged"),
                opt("both impedance and current are infinite"),
            ),
            "Cancelling reactances leave a minimum resistive impedance, so the current is maximum.",
        ),
        q(
            "Which set of s-domain impedances is correct?",
            (
                opt("$Z_R = R$, $Z_L = sL$, $Z_C = 1/(sC)$", correct=True),
                opt("$Z_R = sR$, $Z_L = L$, $Z_C = sC$"),
                opt("$Z_R = R$, $Z_L = 1/(sL)$, $Z_C = sC$"),
                opt("$Z_R = R/s$, $Z_L = sL$, $Z_C = C$"),
            ),
            "In the s-domain: $Z_R=R$, $Z_L=sL$, $Z_C=1/(sC)$.",
        ),
        q(
            "Poles in the right half of the s-plane indicate a response that is:",
            (
                opt("decaying and stable"),
                opt("growing and unstable", correct=True),
                opt("a sustained constant oscillation"),
                opt("purely resistive"),
            ),
            "Right-half-plane poles ($\\sigma>0$) grow exponentially — an unstable circuit.",
        ),
        q(
            "Why are ABCD parameters convenient for chained stages?",
            (
                opt("they are always real numbers"),
                opt("cascading equals multiplying the ABCD matrices", correct=True),
                opt("they ignore the load impedance"),
                opt("they only apply at DC"),
            ),
            "A cascade of two-ports is the matrix product of their ABCD matrices.",
        ),
        q(
            "An ideal transformer with $n = 3$ presents an $8\\,\\Omega$ secondary load to the primary as:",
            (
                opt("$8/3 \\approx 2.7\\,\\Omega$"),
                opt("$24\\,\\Omega$"),
                opt("$72\\,\\Omega$", correct=True),
                opt("$8\\,\\Omega$"),
            ),
            "$Z_{in} = n^2 Z_L = 9 \\times 8 = 72\\,\\Omega$.",
        ),
        q(
            "The phasor/AC analysis is recovered from the Laplace transfer function by setting:",
            (
                opt("$s = 0$"),
                opt("$s = j\\omega$", correct=True),
                opt("$s = \\infty$"),
                opt("$s = R$"),
            ),
            "Evaluating $H(s)$ at $s=j\\omega$ gives the sinusoidal steady-state (frequency) response.",
        ),
    ),
)
