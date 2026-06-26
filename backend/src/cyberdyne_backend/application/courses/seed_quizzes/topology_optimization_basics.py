"""Quiz questions for the Topology Optimization - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is topology optimization?": (
            q(
                "Topology optimization decides primarily:",
                (
                    opt("where material should be placed in the design domain", correct=True),
                    opt("only the colour of the part"),
                    opt("only a single bar thickness"),
                    opt("the loading that will be applied"),
                ),
                "It finds the best material layout given loads, supports and a material budget.",
            ),
            q(
                "The classic objective in basic topology optimization is to:",
                (
                    opt("minimise compliance (maximise stiffness)", correct=True),
                    opt("maximise compliance"),
                    opt("maximise total mass"),
                    opt("minimise the number of nodes"),
                ),
                "Minimising compliance c = uT K u makes the structure as stiff as possible.",
            ),
            q(
                "Why do optimized layouts often look organic, like bone?",
                (
                    opt("nature solves the same stiffness-per-mass problem", correct=True),
                    opt("the solver adds random noise"),
                    opt("organic shapes are required by the standard"),
                    opt("it is purely cosmetic post-processing"),
                ),
                "Efficient load paths under a material budget tend toward branching, bone-like forms.",
            ),
        ),
        "Sizing, shape and topology optimization": (
            q(
                "Sizing optimization changes:",
                (
                    opt("dimensions like thickness, with fixed geometry", correct=True),
                    opt("the number of holes"),
                    opt("the overall connectivity"),
                    opt("nothing at all"),
                ),
                "Sizing tunes parameters but cannot move material or change topology.",
            ),
            q(
                "Compared with shape optimization, topology optimization can additionally:",
                (
                    opt("change the number of holes and connectivity", correct=True),
                    opt("only move existing boundaries"),
                    opt("only scale the whole part uniformly"),
                    opt("only pick a material colour"),
                ),
                "Topology decides connectivity; shape only moves boundaries of a fixed topology.",
            ),
            q(
                "Roughly how many design variables does a density-based topology problem have?",
                (
                    opt("about one per element, often 10^5 to 10^7", correct=True),
                    opt("exactly three"),
                    opt("one per load case"),
                    opt("zero, it is parameter-free"),
                ),
                "Each element carries a density, so the dimension equals the element count.",
            ),
        ),
        "The density approach and SIMP": (
            q(
                "The density approach relaxes the 0/1 choice by:",
                (
                    opt("letting each element density vary continuously in [0,1]", correct=True),
                    opt("removing all constraints"),
                    opt("solving a pure integer program directly"),
                    opt("using only two elements"),
                ),
                "Continuous densities make the problem differentiable and tractable.",
            ),
            q(
                "In SIMP, the element modulus is interpolated as:",
                (
                    opt("E = Emin + rho^p (E0 - Emin) with p >= 3", correct=True),
                    opt("E = E0 / rho"),
                    opt("E = rho + E0"),
                    opt("E = E0 regardless of density"),
                ),
                "SIMP penalises intermediate densities with the exponent p.",
            ),
            q(
                "Why use a penalisation exponent p >= 3?",
                (
                    opt(
                        "to make grey (intermediate) densities inefficient, pushing toward 0/1",
                        correct=True,
                    ),
                    opt("to make grey densities cheaper than solid"),
                    opt("to keep the design fully grey"),
                    opt("to remove the volume constraint"),
                ),
                "A half-dense element gives only 0.5^3 of the stiffness for half the volume.",
            ),
        ),
        "Compliance minimisation with a volume constraint": (
            q(
                "Compliance c = uT K u physically represents:",
                (
                    opt("the work done by the external load (inverse stiffness)", correct=True),
                    opt("the total mass"),
                    opt("the number of elements"),
                    opt("the yield stress"),
                ),
                "Lower compliance means a stiffer structure.",
            ),
            q(
                "Without a volume constraint, the minimum-compliance optimum is:",
                (
                    opt("trivially the fully solid domain", correct=True),
                    opt("an empty domain"),
                    opt("a checkerboard"),
                    opt("undefined"),
                ),
                "The volume budget is what forces real material choices.",
            ),
            q(
                "The equilibrium constraint that must hold each iteration is:",
                (
                    opt("K u = F", correct=True),
                    opt("rho = 1 everywhere"),
                    opt("c = 0"),
                    opt("u = F"),
                ),
                "Displacements come from solving the FE equilibrium K u = F.",
            ),
        ),
        "Checkerboards, mesh dependence and filtering": (
            q(
                "Checkerboarding is best described as:",
                (
                    opt(
                        "a numerical artefact of alternating solid/void overestimated in stiffness",
                        correct=True,
                    ),
                    opt("a physically optimal microstructure"),
                    opt("a meshing error that crashes the solver"),
                    opt("the correct converged answer"),
                ),
                "Low-order elements over-estimate the stiffness of the checkerboard pattern.",
            ),
            q(
                "Mesh dependence means a finer mesh tends to give:",
                (
                    opt("more, thinner members instead of a converged design", correct=True),
                    opt("exactly the same design every time"),
                    opt("fewer members"),
                    opt("a solid block"),
                ),
                "Without a length scale, refinement keeps adding finer features.",
            ),
            q(
                "A density filter imposes a minimum length scale by:",
                (
                    opt("averaging each density over neighbours within radius rmin", correct=True),
                    opt("deleting every other element"),
                    opt("doubling the load"),
                    opt("increasing the penalisation to p=10"),
                ),
                "The neighbourhood average couples elements and removes checkerboards.",
            ),
        ),
    },
    final=(
        q(
            "The defining freedom of topology optimization versus shape/sizing is:",
            (
                opt("changing connectivity, including the number of holes", correct=True),
                opt("only tuning a thickness"),
                opt("only moving boundaries"),
                opt("only choosing a material"),
            ),
            "Topology optimization can create and remove holes and branches.",
        ),
        q(
            "The standard basic objective and constraint pair is:",
            (
                opt("minimise compliance subject to a volume fraction", correct=True),
                opt("maximise compliance subject to a stress limit"),
                opt("minimise mass with no constraints"),
                opt("maximise volume subject to stiffness"),
            ),
            "Minimum compliance at a fixed material budget is the canonical problem.",
        ),
        q(
            "SIMP stands for and does:",
            (
                opt(
                    "Solid Isotropic Material with Penalisation; penalises grey densities",
                    correct=True,
                ),
                opt("Simple Integer Material Programming; solves exactly"),
                opt("Stiffness Independent Material Property; ignores density"),
                opt("Smoothed Inverse Mesh Procedure; refines the mesh"),
            ),
            "SIMP interpolates modulus as rho^p to discourage intermediate densities.",
        ),
        q(
            "A small Emin term in SIMP is kept mainly to:",
            (
                opt("keep the global stiffness matrix non-singular", correct=True),
                opt("increase the part mass"),
                opt("make void elements stiffer than solid"),
                opt("remove the volume constraint"),
            ),
            "A tiny residual stiffness in void avoids a singular K.",
        ),
        q(
            "Filtering with radius rmin primarily prevents:",
            (
                opt("checkerboarding and mesh dependence", correct=True),
                opt("convergence of the solver"),
                opt("the volume constraint from being applied"),
                opt("the load from being transmitted"),
            ),
            "The filter sets a minimum feature size and removes artefacts.",
        ),
        q(
            "A practical workflow uses topology optimization to:",
            (
                opt("generate a concept layout, then refine with shape and sizing", correct=True),
                opt("replace all manufacturing steps"),
                opt("avoid any finite-element analysis"),
                opt("fix the topology before starting"),
            ),
            "Topology gives the concept; shape and sizing clean it for manufacture.",
        ),
    ),
)
