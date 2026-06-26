"""Quiz questions for the Engineering Graphics, GD&T & CAD - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Parametric feature-based solid modelling": (
            q(
                "In a parametric CAD model, changing a driving dimension causes the model to:",
                (
                    opt("regenerate from its feature history", correct=True),
                    opt("be deleted and redrawn by hand"),
                    opt("lose all constraints"),
                    opt("convert to a 2D drawing"),
                ),
                "Parameters drive features; editing one regenerates the model, preserving design intent.",
            ),
            q(
                "A 2D sketch is fully defined when its degrees of freedom equal:",
                (
                    opt("zero", correct=True),
                    opt("the number of points"),
                    opt("twice the number of constraints"),
                    opt("six"),
                ),
                "DOF = 2*points - constraints; a fully defined sketch has zero DOF.",
            ),
            q(
                "An under-constrained sketch will:",
                (
                    opt("allow geometry to drag unpredictably", correct=True),
                    opt("throw an over-constrained conflict"),
                    opt("be impossible to extrude"),
                    opt("automatically add a fillet"),
                ),
                "Under-constrained sketches have free DOF and move unpredictably; over-constrained ones conflict.",
            ),
        ),
        "Assemblies, mates and degrees of freedom": (
            q(
                "Each rigid component placed in an assembly begins with how many degrees of freedom?",
                (
                    opt("six", correct=True),
                    opt("three"),
                    opt("one"),
                    opt("zero"),
                ),
                "A free rigid body has 6 DOF; mates remove them until fully constrained (0 DOF).",
            ),
            q(
                "The Kutzbach/Gruebler mobility of a four-bar linkage (n=4, j1=4) is:",
                (
                    opt("1", correct=True),
                    opt("0"),
                    opt("2"),
                    opt("3"),
                ),
                "M = 3(n-1) - 2*j1 = 3*3 - 8 = 1, one input drives the mechanism.",
            ),
            q(
                "A planar assembly computed to have mobility M = 0 is:",
                (
                    opt("a rigid structure with no motion", correct=True),
                    opt("a single-DOF mechanism"),
                    opt("an over-constrained error always"),
                    opt("a two-DOF mechanism"),
                ),
                "M = 0 means fully constrained / rigid (e.g. a triangle of links).",
            ),
        ),
        "The geometric kernel: B-rep and NURBS": (
            q(
                "A boundary representation (B-rep) stores a solid as:",
                (
                    opt("topology (vertices, edges, faces) bound to geometry", correct=True),
                    opt("only a triangle mesh"),
                    opt("a set of 2D drawings"),
                    opt("a list of dimensions"),
                ),
                "B-rep is a topology graph (V/E/F/shells) linked to geometric points, curves and surfaces.",
            ),
            q(
                "Euler's formula for a simple closed polyhedron states:",
                (
                    opt("V - E + F = 2", correct=True),
                    opt("V + E + F = 0"),
                    opt("V * E * F = 1"),
                    opt("V - E - F = 2"),
                ),
                "V - E + F = 2 for genus 0; generally V - E + F = 2(1 - g).",
            ),
            q(
                "What capability makes NURBS the CAD standard for free-form geometry?",
                (
                    opt("weights let them represent conics like circles exactly", correct=True),
                    opt("they require no control points"),
                    opt("they are always linear"),
                    opt("they cannot be trimmed"),
                ),
                "Rational weights allow exact conics, which plain polynomial splines cannot represent.",
            ),
        ),
        "Model-based definition and PMI": (
            q(
                "In Model-Based Definition (MBD), the authoritative source of design data is the:",
                (
                    opt("3D model with semantic PMI", correct=True),
                    opt("paper drawing"),
                    opt("title block alone"),
                    opt("CMM report"),
                ),
                "MBD makes the annotated 3D model the single source of truth; the 2D drawing is optional.",
            ),
            q(
                "Which neutral exchange format carries semantic (machine-readable) PMI?",
                (
                    opt("STEP AP242", correct=True),
                    opt("plain DXF"),
                    opt("JPEG"),
                    opt("CSV"),
                ),
                "STEP AP242 carries semantic PMI; QIF handles quality data, 3D PDF is for presentation.",
            ),
            q(
                "Semantic (representation) PMI differs from presentation PMI because it is:",
                (
                    opt("machine-interpretable and linked to the faces it controls", correct=True),
                    opt("only human-readable annotation"),
                    opt("printed on paper only"),
                    opt("ignored by downstream tools"),
                ),
                "Semantic PMI is linked to geometry and machine-readable, unlocking automated CAM and inspection.",
            ),
        ),
        "CAD automation and generative design": (
            q(
                "Topology optimization by the SIMP method minimizes which objective?",
                (
                    opt(
                        "compliance (it maximizes stiffness) under a volume constraint",
                        correct=True,
                    ),
                    opt("the number of features"),
                    opt("the drawing scale"),
                    opt("the surface roughness"),
                ),
                "SIMP minimizes compliance U^T K U subject to a volume fraction, maximizing stiffness.",
            ),
            q(
                "In SIMP, the penalization exponent p (around 3) on element density serves to:",
                (
                    opt("push densities toward solid (1) or void (0)", correct=True),
                    opt("increase the part volume"),
                    opt("disable the volume constraint"),
                    opt("convert NURBS to meshes"),
                ),
                "Penalizing E_e = rho^p * E_0 makes intermediate densities inefficient, driving a black-and-white design.",
            ),
            q(
                "Generative design inverts the traditional workflow by:",
                (
                    opt(
                        "computing optimal geometry from loads, supports and targets", correct=True
                    ),
                    opt("drawing geometry first and never analyzing it"),
                    opt("removing all constraints"),
                    opt("requiring manual sketching of every option"),
                ),
                "You specify loads, supports and goals; the algorithm generates and evaluates candidate geometries.",
            ),
        ),
    },
    final=(
        q(
            "The defining property of parametric, feature-based CAD is that:",
            (
                opt("a history of features is driven by editable parameters", correct=True),
                opt("geometry is fixed and cannot be changed"),
                opt("only 2D sketches are stored"),
                opt("there are no constraints"),
            ),
            "Editable parameters drive the feature tree and regenerate the model.",
        ),
        q(
            "Mates in an assembly are used to:",
            (
                opt("remove degrees of freedom between components", correct=True),
                opt("add material to a part"),
                opt("change the drawing scale"),
                opt("delete features"),
            ),
            "Each mate removes DOF; a fully constrained part reaches 0 DOF.",
        ),
        q(
            "A solid stored as a topology graph linked to geometric surfaces is a:",
            (
                opt("boundary representation (B-rep)", correct=True),
                opt("point cloud"),
                opt("raster image"),
                opt("dimension table"),
            ),
            "B-rep binds topology (V/E/F) to geometry and underlies modern kernels.",
        ),
        q(
            "NURBS are preferred for free-form CAD geometry because their weights allow:",
            (
                opt("exact representation of conics such as circles", correct=True),
                opt("only straight lines"),
                opt("removal of all control points"),
                opt("automatic dimensioning"),
            ),
            "Rational weights make conics exact, unlike plain polynomial splines.",
        ),
        q(
            "Model-Based Definition reduces rework primarily by:",
            (
                opt("providing a single authoritative source consumed downstream", correct=True),
                opt("printing more drawings"),
                opt("removing all tolerances"),
                opt("using only presentation PMI"),
            ),
            "A single annotated 3D model removes drawing/model mismatch and feeds CAM/CMM directly.",
        ),
        q(
            "In SIMP topology optimization, the compliance over iterations typically:",
            (
                opt("decreases and converges as material is redistributed", correct=True),
                opt("increases without bound"),
                opt("stays exactly constant"),
                opt("oscillates forever and never converges"),
            ),
            "Iterative FE plus sensitivity-driven density updates drive compliance down to a converged optimum.",
        ),
    ),
)
