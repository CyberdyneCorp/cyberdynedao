"""Quiz questions for the Analytical & Instrumental Chemistry - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Mass spectrometry: ionisation & the mass spectrum": (
            q(
                "A mass spectrometer separates ions according to their:",
                (
                    opt("mass-to-charge ratio m/z", correct=True),
                    opt("boiling point"),
                    opt("absorbance"),
                    opt("pH"),
                ),
                "Ions are separated by m/z; intensity vs m/z gives the spectrum.",
            ),
            q(
                "Electrospray (ESI) and MALDI are examples of:",
                (
                    opt("soft ionisation that preserves intact biomolecules", correct=True),
                    opt("hard ionisation that always fragments analytes"),
                    opt("chromatographic detectors"),
                    opt("reference electrodes"),
                ),
                "Soft methods transfer intact molecules; EI is the hard, fragmenting method.",
            ),
            q(
                "Resolving power R = m/delta_m determines whether the instrument can:",
                (
                    opt("distinguish two near-isobaric ions", correct=True),
                    opt("change the pH"),
                    opt("set the scan rate"),
                    opt("increase the path length"),
                ),
                "High R (Orbitrap, TOF) resolves close masses and enables formula assignment.",
            ),
        ),
        "Tandem MS & hyphenated LC-MS/MS": (
            q(
                "In tandem MS (MS/MS), the sequence is:",
                (
                    opt("select a precursor, fragment it, then scan product ions", correct=True),
                    opt("scan products, then select a precursor"),
                    opt("measure absorbance, then current"),
                    opt("dilute, then weigh"),
                ),
                "MS/MS isolates a precursor, fragments it (CID), and analyses the products.",
            ),
            q(
                "Multiple reaction monitoring (MRM) on a triple quadrupole gives:",
                (
                    opt(
                        "very low detection limits by recording a specific transition", correct=True
                    ),
                    opt("a full untargeted survey of all ions"),
                    opt("the NMR chemical shift"),
                    opt("the pH of the eluent"),
                ),
                "MRM records a chosen precursor->product transition, suppressing background.",
            ),
            q(
                "A stable-isotope-labelled internal standard improves quantitation because it:",
                (
                    opt(
                        "co-elutes and ionises identically, correcting matrix effects", correct=True
                    ),
                    opt("has a completely different retention time"),
                    opt("changes the column chemistry"),
                    opt("eliminates the need for the mass analyzer"),
                ),
                "A 13C/15N analogue behaves identically, correcting ion suppression.",
            ),
        ),
        "Nuclear magnetic resonance spectroscopy": (
            q(
                "The Larmor frequency of an NMR-active nucleus is proportional to:",
                (
                    opt("the static magnetic field B0", correct=True),
                    opt("the sample concentration"),
                    opt("the pH"),
                    opt("the column length"),
                ),
                "nu = (gamma/2pi) B0; resonance frequency scales with field strength.",
            ),
            q(
                "The NMR spectrum is obtained from the free induction decay by:",
                (
                    opt("a Fourier transform", correct=True),
                    opt("a calibration curve"),
                    opt("a titration"),
                    opt("a dilution"),
                ),
                "The time-domain FID is Fourier-transformed into the frequency spectrum.",
            ),
            q(
                "Chemical shift is reported in ppm so that it is:",
                (
                    opt("independent of the spectrometer field strength", correct=True),
                    opt("equal to the molar mass"),
                    opt("proportional to concentration"),
                    opt("the same as the coupling constant J"),
                ),
                "Normalising by spectrometer frequency makes delta field-independent.",
            ),
        ),
        "Generating omics data: metabolomics & proteomics": (
            q(
                "Shotgun proteomics typically digests proteins into peptides using:",
                (
                    opt("trypsin", correct=True),
                    opt("hydrochloric acid only"),
                    opt("acetonitrile"),
                    opt("a glass electrode"),
                ),
                "Trypsin cleaves proteins into peptides for nano-LC-MS/MS analysis.",
            ),
            q(
                "Omics feature matrices are described as 'large p, small n' meaning:",
                (
                    opt("many more features than samples", correct=True),
                    opt("many more samples than features"),
                    opt("equal features and samples"),
                    opt("no features at all"),
                ),
                "Thousands of features but few samples is the hallmark omics regime.",
            ),
            q(
                "With thousands of features tested at once, the main statistical danger is:",
                (
                    opt("false positives from multiple testing", correct=True),
                    opt("too few significant figures"),
                    opt("excessive path length"),
                    opt("low pH"),
                ),
                "Multiple testing inflates false positives; FDR control (e.g. BH) is needed.",
            ),
        ),
        "Chemometrics & machine learning for analytical data": (
            q(
                "Principal component analysis (PCA) finds directions that maximise:",
                (
                    opt("variance in the data", correct=True),
                    opt("covariance with the response"),
                    opt("the molar mass"),
                    opt("the retention time"),
                ),
                "PCA is unsupervised, maximising variance; PLS maximises covariance with y.",
            ),
            q(
                "Partial least squares (PLS) differs from PCA because it:",
                (
                    opt(
                        "finds components that maximise covariance with the response", correct=True
                    ),
                    opt("ignores the response variable"),
                    opt("requires a mass spectrometer"),
                    opt("only works on a single variable"),
                ),
                "PLS is supervised, building latent variables relevant to prediction.",
            ),
            q(
                "The cardinal rule for modelling 'large p, small n' data is:",
                (
                    opt(
                        "honest validation (nested CV, held-out test, permutation tests)",
                        correct=True,
                    ),
                    opt("use as many components as features"),
                    opt("never split the data"),
                    opt("report only the training accuracy"),
                ),
                "Flexible models overfit; rigorous validation prevents confident nonsense.",
            ),
        ),
        "Validation, QA/QC & reproducibility": (
            q(
                "Which is NOT a standard method-validation figure of merit?",
                (
                    opt("brand of the manufacturer", correct=True),
                    opt("accuracy"),
                    opt("precision"),
                    opt("limit of detection"),
                ),
                "Validation covers accuracy, precision, linearity, LOD/LOQ, selectivity, robustness.",
            ),
            q(
                "On a control chart, a check standard beyond +/- 3 sigma usually means:",
                (
                    opt("the method is out of control and should be investigated", correct=True),
                    opt("the result is perfectly fine"),
                    opt("the molar mass changed"),
                    opt("a new wavelength is needed"),
                ),
                "The +/- 3 sigma action limit flags loss of control requiring action.",
            ),
            q(
                "Reproducibility of omics/ML results is best supported by:",
                (
                    opt(
                        "sharing raw data and code with independent-cohort validation", correct=True
                    ),
                    opt("reporting only the best-performing fold"),
                    opt("hiding the preprocessing steps"),
                    opt("using a single sample"),
                ),
                "Open data/code, batch correction and external validation underpin reproducibility.",
            ),
        ),
    },
    final=(
        q(
            "High-resolution accurate-mass measurement (a few ppm) is valuable because it:",
            (
                opt("helps assign molecular formulae", correct=True),
                opt("removes the need for chromatography"),
                opt("sets the pH"),
                opt("increases the scan rate only"),
            ),
            "Accurate mass narrows candidate formulae for identification.",
        ),
        q(
            "Untargeted (full-scan DDA/DIA) acquisition is used primarily for:",
            (
                opt("discovery of unknown features", correct=True),
                opt("the lowest-possible targeted detection limits"),
                opt("measuring pH"),
                opt("calibrating a glass electrode"),
            ),
            "Untargeted scans catalogue many features; MRM is for targeted quantitation.",
        ),
        q(
            "In an NMR spectrum, the peak integral is proportional to:",
            (
                opt("the number of equivalent nuclei", correct=True),
                opt("the spectrometer field strength"),
                opt("the column length"),
                opt("the pH"),
            ),
            "Integrals count equivalent nuclei, making NMR inherently quantitative.",
        ),
        q(
            "Benjamini-Hochberg correction is applied in omics to control the:",
            (
                opt("false discovery rate across many tests", correct=True),
                opt("retention factor"),
                opt("molar absorptivity"),
                opt("Larmor frequency"),
            ),
            "BH limits the expected proportion of false positives among discoveries.",
        ),
        q(
            "Deep learning is increasingly used in analytical chemistry to:",
            (
                opt(
                    "predict spectra and learn features from raw chromatograms/spectra",
                    correct=True,
                ),
                opt("replace the need for any sample"),
                opt("eliminate calibration entirely"),
                opt("set the oven temperature only"),
            ),
            "CNNs/transformers learn from raw data and predict fragmentation, RT and shifts.",
        ),
        q(
            "What separates a publishable analytical signal from an irreproducible artefact?",
            (
                opt(
                    "disciplined QA/QC, reported uncertainty and independent validation",
                    correct=True,
                ),
                opt("using the most expensive instrument"),
                opt("reporting more significant figures"),
                opt("avoiding any blanks or controls"),
            ),
            "Rigorous QA/QC and external validation are what make results trustworthy.",
        ),
    ),
)
