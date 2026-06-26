"""Quiz questions for the Manufacturing Processes - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Process simulation: casting and forming FEM": (
            q(
                "The latent-heat source term in the solidification heat equation accounts for:",
                (
                    opt("energy released as liquid metal freezes", correct=True),
                    opt("friction at the cutting tool"),
                    opt("the cost of tooling"),
                    opt("springback in forming"),
                ),
                "Phase change releases latent heat over the freezing range.",
            ),
            q(
                "An explicit finite-difference heat solver is stable only if:",
                (
                    opt("alpha dt / dx^2 <= 0.5", correct=True),
                    opt("alpha dt / dx^2 >= 2"),
                    opt("dt is arbitrarily large"),
                    opt("dx equals zero"),
                ),
                "The explicit scheme requires the Fourier number r = alpha dt/dx^2 <= 0.5 in 1-D.",
            ),
            q(
                "Forming FEM commonly predicts which defect or effect?",
                (
                    opt("springback and fold/lap defects", correct=True),
                    opt("Taylor tool wear constant"),
                    opt("assembly efficiency"),
                    opt("weld arc voltage"),
                ),
                "Large-deformation elastoplastic FEM predicts forces, folds and springback.",
            ),
        ),
        "Additive manufacturing physics": (
            q(
                "Volumetric energy density in powder-bed fusion is:",
                (
                    opt("E_v = P / (v h t)", correct=True),
                    opt("E_v = v h t / P"),
                    opt("E_v = P v h t"),
                    opt("E_v = P / v only"),
                ),
                "E_v = laser power over scan speed times hatch spacing times layer thickness.",
            ),
            q(
                "Too low an energy density typically produces:",
                (
                    opt("lack-of-fusion voids", correct=True),
                    opt("keyhole porosity"),
                    opt("a fully dense part guaranteed"),
                    opt("excessive melting"),
                ),
                "Insufficient energy leaves un-melted, lack-of-fusion porosity.",
            ),
            q(
                "Steep thermal gradients in AM most directly cause:",
                (
                    opt("residual stress and part distortion", correct=True),
                    opt("lower material cost"),
                    opt("zero need for supports"),
                    opt("faster assembly"),
                ),
                "Rapid, uneven cooling builds residual stress that warps parts.",
            ),
        ),
        "Machining parameter and cost optimization": (
            q(
                "Cost per part as a function of cutting speed is:",
                (
                    opt("convex, with a clear minimum-cost speed", correct=True),
                    opt("strictly decreasing forever"),
                    opt("constant for all speeds"),
                    opt("strictly increasing forever"),
                ),
                "Machining time falls but tool cost rises, giving a convex cost curve.",
            ),
            q(
                "The minimum-cost speed and maximum-production speed together:",
                (
                    opt("bracket a sensible operating window", correct=True),
                    opt("are always identical"),
                    opt("require zero tool changes"),
                    opt("ignore tool life entirely"),
                ),
                "The economic operating range lies between these two speeds.",
            ),
            q(
                "Tool-change time and tooling cost per edge enter the cost model because:",
                (
                    opt(
                        "faster cutting shortens tool life, adding change and tool cost",
                        correct=True,
                    ),
                    opt("they reduce machining time"),
                    opt("they have no effect on cost"),
                    opt("they only matter for casting"),
                ),
                "Higher speed means more frequent, costly tool changes.",
            ),
        ),
        "Design of experiments and ML process models": (
            q(
                "Fractional factorial and response-surface designs aim to:",
                (
                    opt("extract maximum information from few experimental runs", correct=True),
                    opt("test every possible combination exhaustively"),
                    opt("avoid any data collection"),
                    opt("eliminate the need for a model"),
                ),
                "DOE structures runs to learn efficiently from limited experiments.",
            ),
            q(
                "A second-order response surface model includes:",
                (
                    opt("linear, quadratic and interaction terms", correct=True),
                    opt("only a constant term"),
                    opt("only linear terms"),
                    opt("no factors at all"),
                ),
                "It fits beta_0 plus linear, square and cross (interaction) terms.",
            ),
            q(
                "Bayesian optimization with an ML surrogate is used to:",
                (
                    opt(
                        "choose the next experiment that best improves the model/objective",
                        correct=True,
                    ),
                    opt("randomly pick experiments"),
                    opt("avoid building any model"),
                    opt("fix the cutting speed permanently"),
                ),
                "It uses the surrogate's uncertainty to pick informative next runs.",
            ),
        ),
        "Design for manufacturing and assembly": (
            q(
                "DFMA is impactful because most product cost is:",
                (
                    opt("locked in during design", correct=True),
                    opt("decided only at final inspection"),
                    opt("set by the shipping method"),
                    opt("independent of part count"),
                ),
                "70-80% of cost is committed at the design stage.",
            ),
            q(
                "In the Boothroyd-Dewhurst method, a part can be combined if it:",
                (
                    opt(
                        "need not move, be a different material, or be separable for assembly",
                        correct=True,
                    ),
                    opt("is the most expensive part"),
                    opt("is the heaviest part"),
                    opt("has the tightest tolerance"),
                ),
                "If none of the three criteria apply, the part is a candidate to merge.",
            ),
            q(
                "GD&T (ASME Y14.5 / ISO 1101) is used to:",
                (
                    opt(
                        "communicate functional tolerances and enable stack-up analysis",
                        correct=True,
                    ),
                    opt("specify the cutting speed"),
                    opt("define the weld current"),
                    opt("set the pouring temperature"),
                ),
                "GD&T conveys functional tolerance requirements for analysis and inspection.",
            ),
        ),
    },
    final=(
        q(
            "An explicit transient heat-conduction solver is stable when:",
            (
                opt("alpha dt / dx^2 <= 0.5", correct=True),
                opt("alpha dt / dx^2 = 10"),
                opt("dt is infinite"),
                opt("dx is infinite"),
            ),
            "The Fourier-number stability limit in 1-D is 0.5.",
        ),
        q(
            "Keyhole porosity in powder-bed fusion arises from:",
            (
                opt("too high a volumetric energy density", correct=True),
                opt("too low an energy density"),
                opt("perfect process settings"),
                opt("the absence of a laser"),
            ),
            "Excess energy causes keyholing and trapped gas porosity.",
        ),
        q(
            "The economically optimal cutting speed minimizes:",
            (
                opt("cost per part (a convex function of speed)", correct=True),
                opt("only the tool life"),
                opt("only the machining time"),
                opt("the rake angle"),
            ),
            "Cost per part is convex, so a minimum-cost speed exists.",
        ),
        q(
            "Design of experiments is valuable because it:",
            (
                opt("learns process behavior from few, well-chosen runs", correct=True),
                opt("requires testing all combinations"),
                opt("needs no measurements"),
                opt("only works for casting"),
            ),
            "Structured designs maximize information per experiment.",
        ),
        q(
            "A low Boothroyd-Dewhurst assembly efficiency suggests you should:",
            (
                opt("combine or eliminate parts", correct=True),
                opt("add more fasteners"),
                opt("increase the part count"),
                opt("tighten every tolerance"),
            ),
            "Low efficiency flags parts that can be merged to simplify assembly.",
        ),
        q(
            "Residual stress in additive manufacturing is primarily driven by:",
            (
                opt("steep thermal gradients during rapid solidification", correct=True),
                opt("the price of the powder"),
                opt("the choice of fastener"),
                opt("the assembly sequence"),
            ),
            "Uneven, rapid cooling builds in residual stress and distortion.",
        ),
    ),
)
