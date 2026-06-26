"""Quiz questions for the Materials Science & Engineering - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Metals & alloy design": (
            q(
                "Stainless steels resist corrosion mainly because of:",
                (
                    opt("at least 10.5 percent Cr forming a passive Cr2O3 film", correct=True),
                    opt("a high carbon content"),
                    opt("being pure iron"),
                    opt("an aluminium coating only"),
                ),
                "Chromium >= 10.5% forms a self-healing passive oxide layer.",
            ),
            q(
                "The figure of merit for lightweighting a tension member is:",
                (
                    opt("specific strength, sigma_y / rho", correct=True),
                    opt("density alone"),
                    opt("melting point"),
                    opt("electrical conductivity"),
                ),
                "Specific strength (strength-to-weight) ranks materials for light, strong parts.",
            ),
            q(
                "Nickel-based superalloys are used in turbine blades because they:",
                (
                    opt(
                        "resist creep at high temperature (gamma-prime strengthened)", correct=True
                    ),
                    opt("are the cheapest available metal"),
                    opt("are the lightest metals"),
                    opt("are perfect electrical insulators"),
                ),
                "Ni superalloys keep strength and resist creep at the high temperatures of turbines.",
            ),
        ),
        "Ceramics & glasses": (
            q(
                "Ceramics are brittle primarily because:",
                (
                    opt(
                        "their bonds give almost no dislocation glide to relieve crack tips",
                        correct=True,
                    ),
                    opt("they have too many free electrons"),
                    opt("they always contain water"),
                    opt("their Young's modulus is very low"),
                ),
                "Without easy slip, ceramics cannot blunt cracks by plastic flow, so they fracture.",
            ),
            q(
                "The Weibull modulus m describes:",
                (
                    opt(
                        "the scatter/reliability of strength (higher m = less scatter)",
                        correct=True,
                    ),
                    opt("the melting temperature"),
                    opt("the diffusion coefficient"),
                    opt("the elastic modulus"),
                ),
                "A higher Weibull modulus means tighter strength distribution and more reliability.",
            ),
            q(
                "A glass is distinguished from a crystalline ceramic by:",
                (
                    opt("its amorphous (no long-range order) structure", correct=True),
                    opt("having metallic bonding"),
                    opt("being ductile at room temperature"),
                    opt("containing dislocations that glide easily"),
                ),
                "Glasses are amorphous and become rigid below the glass transition T_g.",
            ),
        ),
        "Polymers & viscoelasticity": (
            q(
                "A thermoset differs from a thermoplastic in that it:",
                (
                    opt("is cross-linked and cannot be remelted", correct=True),
                    opt("softens and flows on each reheating"),
                    opt("contains no covalent bonds"),
                    opt("is always a metal"),
                ),
                "Thermosets form permanent cross-linked networks; thermoplastics remelt.",
            ),
            q(
                "Viscoelastic stress relaxation in the Maxwell model follows:",
                (
                    opt("sigma(t) = sigma_0 exp(-t/tau)", correct=True),
                    opt("sigma(t) = sigma_0 * t"),
                    opt("sigma(t) constant forever"),
                    opt("sigma(t) increasing exponentially"),
                ),
                "Maxwell (spring + dashpot in series) gives exponential relaxation with tau = eta/E.",
            ),
            q(
                "Below its glass transition temperature T_g, a thermoplastic is:",
                (
                    opt("glassy and stiff", correct=True),
                    opt("rubbery and compliant"),
                    opt("molten"),
                    opt("gaseous"),
                ),
                "Below T_g the polymer is glassy/stiff; above T_g it becomes rubbery.",
            ),
        ),
        "Composites & micromechanics": (
            q(
                "The rule of mixtures for longitudinal stiffness gives:",
                (
                    opt("E_parallel = Vf*Ef + (1-Vf)*Em (iso-strain upper bound)", correct=True),
                    opt("E_parallel = Vf*Em + (1-Vf)*Ef"),
                    opt("1/E = Vf/Ef + (1-Vf)/Em"),
                    opt("E_parallel independent of fibre fraction"),
                ),
                "Aligned fibres in iso-strain give the Voigt upper bound E = Vf*Ef + (1-Vf)*Em.",
            ),
            q(
                "Transverse to aligned fibres, the composite stiffness is:",
                (
                    opt("dominated by the matrix (Reuss lower bound)", correct=True),
                    opt("equal to the fibre modulus"),
                    opt("the same as longitudinal"),
                    opt("always zero"),
                ),
                "Transverse loading is iso-stress, giving the matrix-dominated Reuss lower bound.",
            ),
            q(
                "Plies are stacked at several angles in a laminate to:",
                (
                    opt("manage the strong anisotropy of aligned fibres", correct=True),
                    opt("increase the density"),
                    opt("remove all the fibres"),
                    opt("lower the fibre modulus"),
                ),
                "Multi-angle stacking gives more balanced in-plane properties despite fibre anisotropy.",
            ),
        ),
        "Materials selection & Ashby charts": (
            q(
                "A materials performance index is:",
                (
                    opt(
                        "a group of properties that, when maximised, optimises a design objective",
                        correct=True,
                    ),
                    opt("the price per kilogram only"),
                    opt("the melting temperature"),
                    opt("a single arbitrary number with no derivation"),
                ),
                "An index like E/rho is derived from objective + constraint and ranks candidates.",
            ),
            q(
                "For a light, stiff beam in bending, the index to maximise is:",
                (
                    opt("E^(1/2) / rho", correct=True),
                    opt("E / rho"),
                    opt("rho / E"),
                    opt("E * rho"),
                ),
                "Bending stiffness at minimum mass maximises E^(1/2)/rho (slope-2 guideline).",
            ),
            q(
                "On a log-log Ashby chart, a selection guideline of fixed slope represents:",
                (
                    opt("a constant value of the performance index", correct=True),
                    opt("a constant price"),
                    opt("a single material"),
                    opt("the melting point"),
                ),
                "Sliding a constant-index line toward the optimum corner selects the best materials.",
            ),
        ),
        "Computational & ML materials discovery": (
            q(
                "Density functional theory (DFT) computes properties from:",
                (
                    opt("quantum electronic structure (ab initio)", correct=True),
                    opt("only macroscopic tensile tests"),
                    opt("empirical Ashby charts"),
                    opt("the lever rule"),
                ),
                "DFT predicts properties from first-principles electronic structure.",
            ),
            q(
                "CALPHAD is used to model:",
                (
                    opt("thermodynamic phase equilibria of multicomponent alloys", correct=True),
                    opt("turbulent fluid flow"),
                    opt("electrical circuits"),
                    opt("fatigue crack images"),
                ),
                "CALPHAD computes phase diagrams/thermodynamics for complex alloy systems.",
            ),
            q(
                "An ML surrogate plus Bayesian optimisation (active learning) helps by:",
                (
                    opt("reaching a good design with few costly evaluations", correct=True),
                    opt("removing the need for any data"),
                    opt("guaranteeing zero error instantly"),
                    opt("replacing thermodynamics with guesswork"),
                ),
                "The surrogate screens fast and active learning picks the most informative next experiment.",
            ),
        ),
    },
    final=(
        q(
            "Which property best ranks materials for a light, strong tie-rod?",
            (
                opt("specific strength, sigma_y / rho", correct=True),
                opt("absolute density"),
                opt("electrical conductivity"),
                opt("colour"),
            ),
            "A light, strong tension member maximises sigma_y/rho.",
        ),
        q(
            "Ceramic strength is treated statistically (Weibull) because:",
            (
                opt("failure is controlled by the largest pre-existing flaw", correct=True),
                opt("ceramics have no measurable strength"),
                opt("they yield like ductile metals"),
                opt("strength does not vary between samples"),
            ),
            "Flaw-controlled brittle fracture makes ceramic strength scatter, modelled by Weibull statistics.",
        ),
        q(
            "Viscoelastic creep and stress relaxation in polymers arise because they are:",
            (
                opt("part elastic and part viscous (time-dependent)", correct=True),
                opt("purely elastic"),
                opt("purely brittle"),
                opt("perfectly rigid"),
            ),
            "Combined spring + dashpot behaviour makes polymer response time- and temperature-dependent.",
        ),
        q(
            "The longitudinal stiffness of an aligned-fibre composite increases with fibre fraction as:",
            (
                opt("a linear rule of mixtures, E = Vf*Ef + (1-Vf)*Em", correct=True),
                opt("an exponential law"),
                opt("the inverse of Vf"),
                opt("independent of Vf"),
            ),
            "The Voigt rule of mixtures is linear in fibre volume fraction.",
        ),
        q(
            "The Ashby method selects materials by:",
            (
                opt(
                    "plotting property charts and applying performance indices under constraints",
                    correct=True,
                ),
                opt("always choosing the cheapest material"),
                opt("ignoring the design objective"),
                opt("picking the densest option"),
            ),
            "Ashby selection couples property charts with derived performance indices and constraints.",
        ),
        q(
            "The ICME / computational-discovery vision links scales by:",
            (
                opt(
                    "feeding DFT/MD to CALPHAD to phase-field to FEM, often with ML surrogates",
                    correct=True,
                ),
                opt("using only hand calculations"),
                opt("testing every candidate physically first"),
                opt("relying on a single length scale"),
            ),
            "Integrated Computational Materials Engineering chains multiscale models, accelerated by ML.",
        ),
    ),
)
