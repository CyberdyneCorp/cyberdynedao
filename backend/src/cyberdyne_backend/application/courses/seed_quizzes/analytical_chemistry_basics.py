"""Quiz questions for the Analytical & Instrumental Chemistry - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The analytical process & significant figures": (
            q(
                "How many significant figures does the value 0.0042 have?",
                (
                    opt("two", correct=True),
                    opt("four"),
                    opt("five"),
                    opt("one"),
                ),
                "Leading zeros are placeholders and not significant; only the 4 and 2 count.",
            ),
            q(
                "In a multiplication, how many significant figures should the result keep?",
                (
                    opt("the fewest significant figures of any factor", correct=True),
                    opt("the most significant figures of any factor"),
                    opt("the fewest decimal places of any factor"),
                    opt("always three"),
                ),
                "Multiplication/division keep the fewest significant figures of the inputs.",
            ),
            q(
                "Which step is NOT part of the analytical process pipeline?",
                (
                    opt("Marketing the instrument", correct=True),
                    opt("Sampling"),
                    opt("Sample preparation"),
                    opt("Calibration and statistics"),
                ),
                "The pipeline is sampling, prep, measurement, calibration/statistics, then result.",
            ),
        ),
        "Error, precision & uncertainty": (
            q(
                "A miscalibrated pipette that shifts every reading the same way introduces:",
                (
                    opt("systematic error (bias)", correct=True),
                    opt("random error"),
                    opt("improved precision"),
                    opt("no error"),
                ),
                "A consistent offset is systematic error; it harms accuracy, not precision.",
            ),
            q(
                "For a product y = a*b, how do relative uncertainties combine?",
                (
                    opt("in quadrature: (uy/y)^2 = (ua/a)^2 + (ub/b)^2", correct=True),
                    opt("they simply add: uy = ua + ub"),
                    opt("the larger one is used alone"),
                    opt("they cancel out"),
                ),
                "For products, relative uncertainties add in quadrature.",
            ),
            q(
                "Random error primarily limits which quality of a measurement?",
                (
                    opt("precision", correct=True),
                    opt("accuracy"),
                    opt("the number of significant figures allowed"),
                    opt("the molar mass"),
                ),
                "Random scatter limits precision; bias limits accuracy.",
            ),
        ),
        "Calibration & the standard curve": (
            q(
                "In the calibration line y = m*c + b, what does the slope m represent?",
                (
                    opt("the sensitivity (signal per unit concentration)", correct=True),
                    opt("the blank signal"),
                    opt("the detection limit"),
                    opt("the correlation coefficient"),
                ),
                "Slope is sensitivity; the intercept b is the blank/offset.",
            ),
            q(
                "Standard addition is most useful when:",
                (
                    opt("the sample matrix changes the slope (matrix effects)", correct=True),
                    opt("the blank is exactly zero"),
                    opt("only one standard is available"),
                    opt("the analyte is volatile"),
                ),
                "Spiking into the sample corrects for matrix effects on sensitivity.",
            ),
            q(
                "The limit of detection is conventionally defined as:",
                (
                    opt("3 sigma of the blank divided by the slope", correct=True),
                    opt("the highest standard concentration"),
                    opt("the slope times the intercept"),
                    opt("10 times the mean signal"),
                ),
                "LOD = 3*sigma_blank/m; LOQ uses a factor of 10.",
            ),
        ),
        "Moles, concentration & solutions": (
            q(
                "The dilution relation c1*V1 = c2*V2 expresses conservation of:",
                (
                    opt("moles of solute", correct=True),
                    opt("mass of solvent"),
                    opt("temperature"),
                    opt("absorbance"),
                ),
                "Diluting adds solvent but does not change the number of moles of solute.",
            ),
            q(
                "Molarity is defined as:",
                (
                    opt("moles of solute per litre of solution", correct=True),
                    opt("grams of solute per litre of solvent"),
                    opt("moles per kilogram of solvent"),
                    opt("mass divided by molar mass"),
                ),
                "Molarity c = n/V in mol/L; molality uses kg of solvent.",
            ),
            q(
                "Given mass m and molar mass M, the number of moles is:",
                (
                    opt("n = m / M", correct=True),
                    opt("n = m * M"),
                    opt("n = M / m"),
                    opt("n = m / Na"),
                ),
                "Amount of substance n equals mass divided by molar mass.",
            ),
        ),
        "Acid-base equilibria & buffers": (
            q(
                "The Henderson-Hasselbalch equation gives buffer pH as:",
                (
                    opt("pH = pKa + log([A-]/[HA])", correct=True),
                    opt("pH = pKa - log([HA]/[A-]) only at pH 7"),
                    opt("pH = Ka * [A-]/[HA]"),
                    opt("pH = -log(Kw)"),
                ),
                "pH = pKa + log([base]/[acid]); buffering peaks when [A-] = [HA].",
            ),
            q(
                "A buffer resists pH change most effectively when:",
                (
                    opt("pH is near the pKa of the weak acid", correct=True),
                    opt("the acid is fully dissociated"),
                    opt("only strong acid is present"),
                    opt("the concentration is extremely low"),
                ),
                "Maximum buffer capacity occurs at pH = pKa.",
            ),
            q(
                "At 25 C the ion product of water Kw equals:",
                (
                    opt("1.0e-14", correct=True),
                    opt("1.0e-7"),
                    opt("7.0"),
                    opt("6.022e23"),
                ),
                "Kw = [H+][OH-] = 1.0e-14 at 25 C, so neutral pH is 7.",
            ),
        ),
        "Separations & the partition principle": (
            q(
                "The partition (distribution) coefficient K_D is the ratio of analyte in:",
                (
                    opt("the stationary phase to the mobile phase", correct=True),
                    opt("the solid to the gas at the detector"),
                    opt("the blank to the standard"),
                    opt("the product to the precursor ion"),
                ),
                "K_D = [A]_stationary / [A]_mobile drives every chromatographic separation.",
            ),
            q(
                "Two species are separated by chromatography because they have different:",
                (
                    opt("partition coefficients K_D", correct=True),
                    opt("molar masses only"),
                    opt("colours"),
                    opt("boiling points only"),
                ),
                "Differing K_D makes species travel at different effective speeds.",
            ),
            q(
                "For a fixed total solvent volume, liquid-liquid extraction is most efficient when done as:",
                (
                    opt("several small portions rather than one large portion", correct=True),
                    opt("a single large portion"),
                    opt("one extraction at high temperature"),
                    opt("no extraction at all"),
                ),
                "Multiple small extractions remove more analyte than one large one.",
            ),
        ),
    },
    final=(
        q(
            "A result reported with more significant figures than the method supports is:",
            (
                opt("overstating the precision actually achieved", correct=True),
                opt("always more accurate"),
                opt("required by SI units"),
                opt("a way to reduce systematic error"),
            ),
            "Significant figures are a claim about precision; do not exceed what the method gives.",
        ),
        q(
            "The relative standard deviation (RSD) is used to:",
            (
                opt("compare precision across methods or measurements", correct=True),
                opt("measure systematic bias"),
                opt("determine molar mass"),
                opt("set the pH of a buffer"),
            ),
            "RSD = s/x-bar lets you compare scatter regardless of magnitude.",
        ),
        q(
            "A correlation coefficient r above about 0.995 on a calibration line indicates:",
            (
                opt("a good linear fit to the standards", correct=True),
                opt("a high detection limit"),
                opt("a large systematic error"),
                opt("the analyte is volatile"),
            ),
            "High |r| signals a good linear fit, though residuals are a stronger check.",
        ),
        q(
            "To dilute a stock 10-fold you would:",
            (
                opt("take 1 part stock and add solvent to 10 parts total", correct=True),
                opt("add 10 parts stock to 1 part solvent"),
                opt("evaporate to one tenth the volume"),
                opt("double the concentration"),
            ),
            "c1*V1 = c2*V2: 1 volume of stock made up to 10 gives a 10-fold dilution.",
        ),
        q(
            "An internal standard improves quantitation by:",
            (
                opt("ratioing the analyte signal to a fixed added reference", correct=True),
                opt("removing the need for any calibration"),
                opt("increasing the molar mass"),
                opt("lowering the pH"),
            ),
            "Ratioing to an added reference cancels run-to-run variation.",
        ),
        q(
            "Repeating partition continuously along a packed column is the basis of:",
            (
                opt("chromatography", correct=True),
                opt("potentiometry"),
                opt("the Beer-Lambert law"),
                opt("Avogadro's number"),
            ),
            "A column turns one partition equilibrium into thousands of stages.",
        ),
    ),
)
