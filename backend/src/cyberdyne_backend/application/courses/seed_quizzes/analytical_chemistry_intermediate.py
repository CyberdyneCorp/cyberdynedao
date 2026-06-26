"""Quiz questions for the Analytical & Instrumental Chemistry - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Spectrophotometry & the Beer-Lambert law": (
            q(
                "The Beer-Lambert law states that absorbance A equals:",
                (
                    opt("epsilon * b * c", correct=True),
                    opt("epsilon / (b * c)"),
                    opt("c / (epsilon * b)"),
                    opt("b * c / epsilon"),
                ),
                "A = epsilon*b*c, linear in path length and concentration.",
            ),
            q(
                "Absorbance is related to transmittance T by:",
                (
                    opt("A = -log10(T)", correct=True),
                    opt("A = T"),
                    opt("A = 10^T"),
                    opt("A = 1/T"),
                ),
                "A = -log10(I/I0) = -log10(T).",
            ),
            q(
                "Beer-Lambert linearity typically breaks down when:",
                (
                    opt("absorbance is high (roughly above 1)", correct=True),
                    opt("the path length is exactly 1 cm"),
                    opt("the wavelength equals lambda_max"),
                    opt("the blank is subtracted"),
                ),
                "At high A, stray light and analyte association bend the curve downward.",
            ),
        ),
        "Chromatographic theory: retention & resolution": (
            q(
                "The retention factor k is defined as:",
                (
                    opt("(tR - tM) / tM", correct=True),
                    opt("tR / tM only at the dead time"),
                    opt("tM / tR"),
                    opt("tR * tM"),
                ),
                "k = (tR - tM)/tM measures retention relative to the dead time.",
            ),
            q(
                "Baseline resolution of two peaks corresponds to Rs of about:",
                (
                    opt("1.5", correct=True),
                    opt("0.1"),
                    opt("16"),
                    opt("100"),
                ),
                "Rs near 1.5 gives baseline separation.",
            ),
            q(
                "In the master resolution equation, the most powerful lever is usually:",
                (
                    opt("selectivity alpha (the chemistry of the phases)", correct=True),
                    opt("the detector wavelength"),
                    opt("the injector temperature"),
                    opt("the sample volume only"),
                ),
                "Changing selectivity moves peaks apart more efficiently than raising N.",
            ),
        ),
        "Band broadening & the van Deemter equation": (
            q(
                "The van Deemter equation is:",
                (
                    opt("H = A + B/u + C*u", correct=True),
                    opt("H = A*u + B + C/u^2"),
                    opt("H = (A + B + C)/u"),
                    opt("H = A*B*C*u"),
                ),
                "H = A + B/u + C*u, the sum of three broadening contributions.",
            ),
            q(
                "The B/u term (longitudinal diffusion) dominates at:",
                (
                    opt("low linear velocity", correct=True),
                    opt("high linear velocity"),
                    opt("zero concentration"),
                    opt("high absorbance"),
                ),
                "B/u grows as velocity drops because analyte sits longer and diffuses.",
            ),
            q(
                "Sub-2-micron (UHPLC) particles mainly improve efficiency by:",
                (
                    opt(
                        "flattening the C term so columns stay efficient at high speed",
                        correct=True,
                    ),
                    opt("eliminating the need for a pump"),
                    opt("removing the B term entirely"),
                    opt("lowering the backpressure"),
                ),
                "Smaller particles reduce mass-transfer (C) resistance, at the cost of pressure.",
            ),
        ),
        "HPLC & GC in practice": (
            q(
                "Reversed-phase HPLC uses:",
                (
                    opt(
                        "a nonpolar stationary phase (C18) with a polar mobile phase", correct=True
                    ),
                    opt("a polar stationary phase with a nonpolar mobile phase"),
                    opt("a gas mobile phase"),
                    opt("no stationary phase"),
                ),
                "Reversed phase: nonpolar C18 stationary phase, polar aqueous/organic mobile phase.",
            ),
            q(
                "In GC, the role played by gradient elution in HPLC is filled by:",
                (
                    opt("temperature programming of the oven", correct=True),
                    opt("changing the detector"),
                    opt("increasing the path length"),
                    opt("adding a buffer"),
                ),
                "GC ramps oven temperature; HPLC ramps mobile-phase strength.",
            ),
            q(
                "For quantitation, the integrated peak area is proportional to:",
                (
                    opt("the amount of analyte (over the linear range)", correct=True),
                    opt("the retention time"),
                    opt("the column length"),
                    opt("the dead time"),
                ),
                "Peak area scales with injected amount within the linear dynamic range.",
            ),
        ),
        "Potentiometry & ion-selective electrodes": (
            q(
                "The Nernst equation makes electrode potential linear in:",
                (
                    opt("the logarithm of activity/concentration", correct=True),
                    opt("the square of concentration"),
                    opt("the concentration directly"),
                    opt("the absorbance"),
                ),
                "E = E0 - (0.0592/n) log Q, so E is linear in log(activity).",
            ),
            q(
                "A glass pH electrode changes potential by approximately:",
                (
                    opt("-59 mV per pH unit", correct=True),
                    opt("-1 V per pH unit"),
                    opt("+59 V per pH unit"),
                    opt("0 mV per pH unit"),
                ),
                "Near-Nernstian response is about -59 mV/pH at 25 C for n = 1.",
            ),
            q(
                "An ionic-strength buffer such as TISAB is added so that potentiometry:",
                (
                    opt(
                        "keeps activity coefficients constant so readings track concentration",
                        correct=True,
                    ),
                    opt("changes the analyte molar mass"),
                    opt("eliminates the reference electrode"),
                    opt("converts current to voltage"),
                ),
                "Potentiometry senses activity; a fixed ionic strength makes it track concentration.",
            ),
        ),
        "Voltammetry & cyclic voltammetry": (
            q(
                "In voltammetry the applied variable and the measured variable are:",
                (
                    opt("applied potential, measured current", correct=True),
                    opt("applied current, measured mass"),
                    opt("applied pH, measured absorbance"),
                    opt("applied temperature, measured volume"),
                ),
                "Voltammetry applies a potential and reads the resulting current.",
            ),
            q(
                "The Randles-Sevcik equation says peak current scales with:",
                (
                    opt("the square root of the scan rate", correct=True),
                    opt("the square of the scan rate"),
                    opt("the inverse of concentration"),
                    opt("the logarithm of potential"),
                ),
                "For diffusion control, i_p is proportional to v^(1/2) and to concentration.",
            ),
            q(
                "Stripping voltammetry achieves very low detection limits by:",
                (
                    opt(
                        "pre-concentrating the analyte onto the electrode before scanning",
                        correct=True,
                    ),
                    opt("using a longer path length"),
                    opt("raising the pH"),
                    opt("removing the reference electrode"),
                ),
                "Pre-concentration before the sweep pushes detection into the ppt range.",
            ),
        ),
    },
    final=(
        q(
            "To maximise spectrophotometric sensitivity you measure at:",
            (
                opt("the wavelength of maximum absorption, lambda_max", correct=True),
                opt("the shortest available wavelength"),
                opt("a wavelength where absorbance is zero"),
                opt("any random wavelength"),
            ),
            "lambda_max gives the largest, most stable absorbance signal.",
        ),
        q(
            "The plate number N is a measure of:",
            (
                opt("column efficiency (peak sharpness)", correct=True),
                opt("the partition coefficient"),
                opt("the detector wavelength"),
                opt("the buffer capacity"),
            ),
            "N = 16(tR/w)^2; larger N means narrower, more efficient peaks.",
        ),
        q(
            "The optimum linear velocity in the van Deemter curve corresponds to:",
            (
                opt("the minimum plate height H", correct=True),
                opt("the maximum backpressure"),
                opt("zero retention"),
                opt("the highest detector signal"),
            ),
            "The B/u and C*u terms trade off to give a minimum H at u_opt.",
        ),
        q(
            "LC-MS and GC-MS are powerful because mass spectrometry adds:",
            (
                opt("identification on top of the chromatographic separation", correct=True),
                opt("a longer path length"),
                opt("a higher pH"),
                opt("a lower scan rate"),
            ),
            "Coupling MS to a separation gives both resolution and structural ID.",
        ),
        q(
            "Potentiometry is performed at essentially:",
            (
                opt("zero current, measuring a potential", correct=True),
                opt("high current, measuring mass"),
                opt("fixed potential, measuring absorbance"),
                opt("high temperature, measuring volume"),
            ),
            "Potentiometry reads equilibrium potential at negligible current.",
        ),
        q(
            "A reversible redox couple in cyclic voltammetry shows peak separation of about:",
            (
                opt("59/n mV between forward and reverse peaks", correct=True),
                opt("exactly 1 V regardless of n"),
                opt("no separation at all"),
                opt("several volts"),
            ),
            "A reversible couple has peaks separated by roughly 59/n mV with equal heights.",
        ),
    ),
)
