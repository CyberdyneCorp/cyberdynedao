"""Quiz questions for the Parametric & Simulation-Driven Design - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Design tables and part families": (
            q(
                "In a design table, each row typically represents:",
                (
                    opt("one configuration (a member of the part family)", correct=True),
                    opt("one finite element"),
                    opt("one drawing sheet"),
                    opt("one material property only"),
                ),
                "Rows are configurations and columns are parameters or suppression states.",
            ),
            q(
                "A design table lets one model represent a whole catalogue by:",
                (
                    opt("reading parameter values (and suppression) per row", correct=True),
                    opt("storing a separate mesh per part"),
                    opt("freezing the geometry"),
                    opt("removing all parameters"),
                ),
                "One parametric model plus a table of rows generates a family of variants.",
            ),
            q(
                "Besides changing dimensions, design-table rows can also:",
                (
                    opt("suppress features, varying the topology per configuration", correct=True),
                    opt("change the unit system of the computer"),
                    opt("delete the solver"),
                    opt("rename the operating system"),
                ),
                "Suppressing a feature per row drops a hole or boss, varying topology not just size.",
            ),
        ),
        "Configurations and variation management": (
            q(
                "A configuration is best described as:",
                (
                    opt(
                        "a saved state of dimensions, suppression and properties in one document",
                        correct=True,
                    ),
                    opt("a separate CAD application"),
                    opt("a type of mesh element"),
                    opt("a printer driver"),
                ),
                "Configurations store intentional variation inside a single document.",
            ),
            q(
                "Cramming too many configurations into one document tends to:",
                (
                    opt("increase maintenance cost (file bloat)", correct=True),
                    opt("eliminate all maintenance cost"),
                    opt("improve solver accuracy"),
                    opt("reduce the part count to zero"),
                ),
                "There is a sweet spot: too few wastes reuse, too many bloats and complicates the file.",
            ),
            q(
                "A common use of a simplified configuration is to:",
                (
                    opt("provide a lightweight representation for large assemblies", correct=True),
                    opt("increase the polygon count"),
                    opt("add more fasteners"),
                    opt("delete the feature tree"),
                ),
                "Simplified reps speed up large assemblies by hiding non-essential detail.",
            ),
        ),
        "Top-down assembly and skeletons": (
            q(
                "In top-down assembly, a skeleton holds:",
                (
                    opt("the controlling dimensions that individual parts reference", correct=True),
                    opt("only the final rendered image"),
                    opt("the solver settings"),
                    opt("the bill of materials only"),
                ),
                "Parts reference the skeleton, so editing it updates all of them.",
            ),
            q(
                "To change a shared interface across n parts, a skeleton-driven approach needs:",
                (
                    opt("essentially one edit (in the skeleton)", correct=True),
                    opt("n separate edits, one per part"),
                    opt("no model at all"),
                    opt("a new file per part"),
                ),
                "Editing the skeleton once propagates to every part that references it.",
            ),
            q(
                "Bottom-up assembly differs from top-down because it:",
                (
                    opt("models parts independently then mates them together", correct=True),
                    opt("starts from a controlling skeleton"),
                    opt("never uses mates"),
                    opt("requires a digital twin"),
                ),
                "Bottom-up builds parts first; top-down drives parts from an assembly-level skeleton.",
            ),
        ),
        "Associativity and external references": (
            q(
                "Associativity means that:",
                (
                    opt(
                        "a drawing or assembly updates when its referenced part changes",
                        correct=True,
                    ),
                    opt("documents never affect each other"),
                    opt("geometry must be re-entered by hand"),
                    opt("meshes are generated automatically"),
                ),
                "Associative links keep related documents in sync without manual re-syncing.",
            ),
            q(
                "A circular external reference (A drives B drives A):",
                (
                    opt("breaks regeneration and should be avoided", correct=True),
                    opt("speeds up rebuilds"),
                    opt("is required for associativity"),
                    opt("improves mesh quality"),
                ),
                "Circular dependencies cannot resolve and break the rebuild; keep references one-directional.",
            ),
            q(
                "As the reference-chain depth grows, rebuild time tends to:",
                (
                    opt("increase, roughly linearly with chain length", correct=True),
                    opt("stay exactly constant"),
                    opt("drop to zero"),
                    opt("become negative"),
                ),
                "More layers to propagate through means longer rebuilds; keep references shallow.",
            ),
        ),
        "Equation-driven and in-context geometry": (
            q(
                "An equation-driven curve is defined by:",
                (
                    opt("an explicit y=f(x) or a parametric pair x(t), y(t)", correct=True),
                    opt("a tessellated mesh"),
                    opt("a screenshot of a sketch"),
                    opt("the title block"),
                ),
                "Equation-driven curves model cams, involutes and spirals precisely from math.",
            ),
            q(
                "The involute curve is the standard profile for a:",
                (
                    opt("gear-tooth flank", correct=True),
                    opt("title block border"),
                    opt("bolt thread callout"),
                    opt("dimension line"),
                ),
                "The involute, traced by unwinding a string from a base circle, is the gear-tooth flank.",
            ),
            q(
                "In-context geometry sketched against a neighbouring part:",
                (
                    opt("guarantees fit but creates an external reference", correct=True),
                    opt("never creates any dependency"),
                    opt("converts the part to a mesh"),
                    opt("removes all parameters"),
                ),
                "In-context features track the neighbour but add a reference; break the link once frozen.",
            ),
        ),
        "Meshing and the first CAD-CAE handoff": (
            q(
                "A mesh-convergence study checks that:",
                (
                    opt("the result approaches a limit as the mesh is refined", correct=True),
                    opt("the file size stays the same"),
                    opt("the color of the part is correct"),
                    opt("no parameters are used"),
                ),
                "Refining the mesh should drive the computed result toward a mesh-independent value.",
            ),
            q(
                "Defeaturing before meshing means:",
                (
                    opt(
                        "removing tiny details (fillets, logos) that do not affect the physics",
                        correct=True,
                    ),
                    opt("adding more fasteners"),
                    opt("doubling the element size"),
                    opt("deleting the loads"),
                ),
                "Defeaturing avoids sliver elements and cuts element count without changing the answer.",
            ),
            q(
                "Discretization error in a well-formed mesh typically scales as:",
                (
                    opt("a power of element size h (error ~ C h^p)", correct=True),
                    opt("independent of element size"),
                    opt("proportional to the file name length"),
                    opt("inversely to the material density"),
                ),
                "Error decreases as a power of element size; smaller h gives a more accurate solution.",
            ),
        ),
    },
    final=(
        q(
            "A design table generates a part family by:",
            (
                opt(
                    "driving parameters and suppression states from spreadsheet rows", correct=True
                ),
                opt("storing one mesh per part"),
                opt("freezing all geometry"),
                opt("deleting the feature tree"),
            ),
            "Each row is a configuration; one model serves a whole catalogue.",
        ),
        q(
            "Managing many variants inside one document is the job of:",
            (
                opt("configurations", correct=True),
                opt("the title block"),
                opt("the mesh"),
                opt("the solver"),
            ),
            "Configurations store intentional variation; too many bloats the file.",
        ),
        q(
            "Top-down (skeleton-driven) assembly is preferred when you want to:",
            (
                opt("control a shared interface from one place", correct=True),
                opt("model every part in complete isolation"),
                opt("avoid all references"),
                opt("eliminate the assembly"),
            ),
            "A skeleton is the single source of truth for shared dimensions.",
        ),
        q(
            "Which dependency pattern breaks regeneration?",
            (
                opt("a circular external reference", correct=True),
                opt("a shallow one-directional reference"),
                opt("a skeleton driving parts"),
                opt("an associative drawing link"),
            ),
            "Circular references cannot resolve; keep references shallow and one-directional.",
        ),
        q(
            "An equation-driven curve is the right tool to model a:",
            (
                opt("cam or involute gear-tooth profile precisely", correct=True),
                opt("title block"),
                opt("default tolerance note"),
                opt("printer setting"),
            ),
            "Math-defined curves capture cams, involutes and spirals exactly.",
        ),
        q(
            "Trustworthy FEA results require a:",
            (
                opt("mesh-convergence study toward a mesh-independent value", correct=True),
                opt("single coarse mesh, never refined"),
                opt("larger file size"),
                opt("removal of all boundary conditions"),
            ),
            "Refining the mesh until the result stabilizes confirms the answer is mesh-independent.",
        ),
    ),
)
