"""Quiz questions for the Materials Science & Engineering - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Crystal defects & dislocations": (
            q(
                "Plastic deformation in crystals is carried mainly by:",
                (
                    opt("the glide of dislocations (1-D line defects)", correct=True),
                    opt("vacancies hopping at random"),
                    opt("breaking all bonds across a plane at once"),
                    opt("grain boundaries melting"),
                ),
                "Dislocation glide lets crystals yield far below their theoretical strength.",
            ),
            q(
                "Real yield strengths are far below the theoretical bond-breaking strength because:",
                (
                    opt("dislocations let slip occur one line at a time", correct=True),
                    opt("atoms are heavier than predicted"),
                    opt("Young's modulus is overestimated"),
                    opt("grains are too large"),
                ),
                "Moving one dislocation needs far less stress than shearing a whole plane at once.",
            ),
            q(
                "A vacancy is best classified as a:",
                (
                    opt("0-D (point) defect", correct=True),
                    opt("1-D (line) defect"),
                    opt("2-D (planar) defect"),
                    opt("3-D (volume) defect"),
                ),
                "Vacancies are point (0-D) defects; dislocations are line defects.",
            ),
        ),
        "Strengthening mechanisms": (
            q(
                "The Hall-Petch relation says yield strength increases as:",
                (
                    opt("grain size decreases (sigma_y rises with 1/sqrt(d))", correct=True),
                    opt("grain size increases"),
                    opt("temperature increases"),
                    opt("density decreases"),
                ),
                "Hall-Petch: sigma_y = sigma_0 + k_y / sqrt(d); finer grains are stronger.",
            ),
            q(
                "Work (strain) hardening strengthens a metal by:",
                (
                    opt("multiplying and tangling dislocations", correct=True),
                    opt("dissolving the grain boundaries"),
                    opt("reducing the dislocation density to zero"),
                    opt("lowering the melting point"),
                ),
                "Cold work raises dislocation density (flow stress ~ sqrt(rho)), impeding further slip.",
            ),
            q(
                "A common trade-off of nearly all strengthening mechanisms is:",
                (
                    opt("reduced ductility / formability", correct=True),
                    opt("higher density"),
                    opt("lower Young's modulus"),
                    opt("increased electrical resistance only"),
                ),
                "Stronger usually means less ductile, the central tension in alloy design.",
            ),
        ),
        "Diffusion & Fick's laws": (
            q(
                "Fick's first law states that diffusion flux is proportional to:",
                (
                    opt("the concentration gradient, J = -D dC/dx", correct=True),
                    opt("the square of temperature"),
                    opt("the applied stress"),
                    opt("the grain size"),
                ),
                "Fick's first law: J = -D dC/dx for steady-state diffusion.",
            ),
            q(
                "The diffusion coefficient depends on temperature as:",
                (
                    opt("D = D0 exp(-Q/RT) (Arrhenius)", correct=True),
                    opt("D proportional to T"),
                    opt("D independent of temperature"),
                    opt("D proportional to 1/T squared"),
                ),
                "D follows an Arrhenius law; ln D vs 1/T is a straight line of slope -Q/R.",
            ),
            q(
                "In carburising, the case depth scales roughly as:",
                (
                    opt("the square root of (D times time)", correct=True),
                    opt("linearly with time"),
                    opt("the square of time"),
                    opt("independent of time"),
                ),
                "The erf solution gives depth ~ sqrt(Dt), so 4x time only doubles depth.",
            ),
        ),
        "Phase diagrams & the lever rule": (
            q(
                "The lever rule is used to find:",
                (
                    opt("the relative amounts (fractions) of each phase present", correct=True),
                    opt("the diffusion coefficient"),
                    opt("the Young's modulus"),
                    opt("the cooling rate"),
                ),
                "The lever rule gives phase fractions from the tie-line in a two-phase field.",
            ),
            q(
                "At a eutectic point, on cooling a single liquid transforms into:",
                (
                    opt("two solid phases simultaneously (L -> alpha + beta)", correct=True),
                    opt("a single solid phase only"),
                    opt("a gas"),
                    opt("austenite only"),
                ),
                "The eutectic reaction L -> alpha + beta occurs at the lowest melting point.",
            ),
            q(
                "The two phase fractions computed by the lever rule must:",
                (
                    opt("sum to one", correct=True),
                    opt("each equal one"),
                    opt("sum to the temperature"),
                    opt("be negative"),
                ),
                "W_L + W_alpha = 1; the lever rule conserves total mass.",
            ),
        ),
        "Iron-carbon & heat treatment": (
            q(
                "Quenching steel rapidly from austenite produces:",
                (
                    opt("hard, brittle martensite", correct=True),
                    opt("soft pearlite"),
                    opt("pure ferrite"),
                    opt("liquid iron"),
                ),
                "Fast cooling traps carbon into martensite by a diffusionless transformation.",
            ),
            q(
                "The eutectoid reaction in steel (0.76 wt% C, 727 C) forms:",
                (
                    opt("pearlite (alpha + Fe3C lamellae)", correct=True),
                    opt("austenite"),
                    opt("a single liquid"),
                    opt("graphite"),
                ),
                "gamma -> alpha + Fe3C gives the lamellar pearlite microstructure.",
            ),
            q(
                "Tempering quenched martensite is done to:",
                (
                    opt("restore toughness (reduce brittleness)", correct=True),
                    opt("make it fully austenitic"),
                    opt("increase brittleness further"),
                    opt("dissolve all carbon"),
                ),
                "Tempering reheats martensite to trade some hardness for much-needed toughness.",
            ),
        ),
        "Fracture, fatigue & creep": (
            q(
                "A crack grows catastrophically when the stress intensity K reaches:",
                (
                    opt("the fracture toughness K_IC", correct=True),
                    opt("the Young's modulus"),
                    opt("the Poisson's ratio"),
                    opt("the melting point"),
                ),
                "LEFM: failure when K = Y*sigma*sqrt(pi*a) reaches K_IC.",
            ),
            q(
                "An endurance limit on an S-N curve means:",
                (
                    opt("below a stress amplitude, life is effectively infinite", correct=True),
                    opt("the material fails on the first cycle"),
                    opt("toughness is zero"),
                    opt("creep dominates"),
                ),
                "Steels show a stress amplitude below which fatigue life is essentially unlimited.",
            ),
            q(
                "Creep becomes important mainly when:",
                (
                    opt("temperature exceeds about 0.4 of the melting temperature", correct=True),
                    opt("the load is purely elastic and cold"),
                    opt("the material is a brittle ceramic at room temperature"),
                    opt("the stress is zero"),
                ),
                "Creep (time-dependent deformation) matters at high homologous temperature, T > 0.4 Tm.",
            ),
        ),
    },
    final=(
        q(
            "Dislocations are which dimensionality of defect?",
            (
                opt("1-D (line) defects", correct=True),
                opt("0-D (point) defects"),
                opt("2-D (planar) defects"),
                opt("3-D (volume) defects"),
            ),
            "Dislocations are line (1-D) defects that carry plastic flow.",
        ),
        q(
            "Which strengthening mechanism uses fine second-phase particles to obstruct slip?",
            (
                opt("precipitation / dispersion strengthening", correct=True),
                opt("grain coarsening"),
                opt("annealing"),
                opt("recovery"),
            ),
            "Precipitates force dislocations to bow (Orowan) or cut through them.",
        ),
        q(
            "Fick's second law governs:",
            (
                opt("how concentration evolves in time (transient diffusion)", correct=True),
                opt("steady-state flux only"),
                opt("elastic stress"),
                opt("the lever rule"),
            ),
            "Fick's second law dC/dt = D d2C/dx2 describes transient diffusion.",
        ),
        q(
            "On a binary phase diagram, the tie line is used together with the lever rule to find:",
            (
                opt("the compositions and amounts of the coexisting phases", correct=True),
                opt("the activation energy for diffusion"),
                opt("the fatigue limit"),
                opt("the Burgers vector"),
            ),
            "Tie-line ends give phase compositions; the lever rule gives their fractions.",
        ),
        q(
            "In the iron-carbon system, austenite is:",
            (
                opt("the FCC high-temperature phase with high carbon solubility", correct=True),
                opt("the hard brittle iron carbide"),
                opt("the BCC low-carbon phase"),
                opt("a polymer phase"),
            ),
            "Austenite (gamma) is FCC, stable above ~727 C, dissolving much more carbon than ferrite.",
        ),
        q(
            "Fatigue failure is characterised by:",
            (
                opt("crack growth under cyclic loading below the yield strength", correct=True),
                opt("instantaneous overload fracture"),
                opt("slow deformation at high temperature under constant load"),
                opt("chemical corrosion only"),
            ),
            "Fatigue grows cracks over many cycles at stresses well below static yield.",
        ),
    ),
)
