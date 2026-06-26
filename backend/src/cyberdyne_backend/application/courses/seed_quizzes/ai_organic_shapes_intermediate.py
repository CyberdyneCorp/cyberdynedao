"""Quiz questions for the AI-Driven Organic & Biomimetic Shapes - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Signed distance fields and implicit modelling": (
            q(
                "Two SDFs are combined into a union by taking the:",
                (
                    opt("minimum of the two fields", correct=True),
                    opt("maximum of the two fields"),
                    opt("sum of the two fields"),
                    opt("product of the two fields"),
                ),
                "Union is min(f1, f2); intersection is max; subtraction is max(f1, -f2).",
            ),
            q(
                "A true signed distance field satisfies the eikonal equation, meaning:",
                (
                    opt("the gradient magnitude equals 1 everywhere", correct=True),
                    opt("the field is always zero"),
                    opt("the field has no gradient"),
                    opt("the field equals the colour"),
                ),
                "||grad f|| = 1 for a true SDF, so the gradient gives the exact surface normal.",
            ),
            q(
                "Increasing the smooth-union parameter k produces:",
                (
                    opt("a larger fillet, adding material at the junction", correct=True),
                    opt("a sharper seam"),
                    opt("no change to the junction"),
                    opt("a hole in the part"),
                ),
                "Larger k swells a more generous, organic fillet (more mass); small k keeps a sharp seam.",
            ),
        ),
        "TPMS and lattice mathematics": (
            q(
                "The implicit equation sin(x)cos(y) + sin(y)cos(z) + sin(z)cos(x) = c defines a:",
                (
                    opt("gyroid", correct=True),
                    opt("sphere"),
                    opt("cube"),
                    opt("cylinder"),
                ),
                "That is the standard gyroid approximation; Schwarz-P uses cos(x)+cos(y)+cos(z).",
            ),
            q(
                "To make a TPMS lattice denser in high-stress regions you can:",
                (
                    opt("grade the cell size or thickness offset with position", correct=True),
                    opt("change only the colour"),
                    opt("rotate the whole part 90 degrees"),
                    opt("lower the print temperature"),
                ),
                "Spatially varying a (cell size) or t (thickness) grades density, mimicking bone.",
            ),
            q(
                "A gyroid lattice's stiffness scales with relative density approximately as:",
                (
                    opt("rho squared (bending-dominated)", correct=True),
                    opt("rho cubed"),
                    opt("independent of density"),
                    opt("inversely with density"),
                ),
                "Gyroids behave close to bending-dominated, E*/Es ~ rho^2.",
            ),
        ),
        "Procedural growth: L-systems and reaction-diffusion": (
            q(
                "An L-system generates plant-like geometry by:",
                (
                    opt(
                        "rewriting a string of symbols with production rules, then interpreting it",
                        correct=True,
                    ),
                    opt("solving a finite-element problem"),
                    opt("denoising random noise"),
                    opt("subtracting two SDFs"),
                ),
                "L-systems are grammar rewriting systems interpreted as turtle graphics / branches.",
            ),
            q(
                "Gray-Scott reaction-diffusion produces:",
                (
                    opt("Turing patterns such as spots and stripes", correct=True),
                    opt("perfectly straight lines only"),
                    opt("a uniform field"),
                    opt("topology-optimised brackets"),
                ),
                "Two reacting, diffusing species form Turing spot/stripe patterns seen in animal coats and coral.",
            ),
            q(
                "Murray's law for a symmetric bifurcation states that:",
                (
                    opt(
                        "the parent radius cubed equals the sum of daughter radii cubed",
                        correct=True,
                    ),
                    opt("all radii are equal"),
                    opt("radius grows with each generation"),
                    opt("radius is unrelated to branching"),
                ),
                "r0^3 = r1^3 + r2^3 minimises pumping cost; symmetric daughters shrink by 2^(-1/3).",
            ),
        ),
        "Marching cubes and mesh extraction": (
            q(
                "Marching cubes converts a scalar field into a mesh by:",
                (
                    opt(
                        "classifying each cube's 8 corners and looking up triangle patterns",
                        correct=True,
                    ),
                    opt("ray-tracing the field for colour"),
                    opt("solving the heat equation"),
                    opt("sorting the voxels by value"),
                ),
                "Each cube's inside/outside corner pattern indexes an edge/triangle lookup table.",
            ),
            q(
                "Where on a crossed cube edge is the vertex placed?",
                (
                    opt(
                        "by linear interpolation to where the field equals the isolevel",
                        correct=True,
                    ),
                    opt("always at the edge midpoint"),
                    opt("at a random point"),
                    opt("at the cube centre"),
                ),
                "t = (c - f_a)/(f_b - f_a) interpolates the crossing point along the edge.",
            ),
            q(
                "Halving the voxel spacing roughly multiplies the triangle count by:",
                (
                    opt("4 (triangles ~ area / h^2)", correct=True),
                    opt("2"),
                    opt("no change"),
                    opt("8"),
                ),
                "Triangle count tracks surface area divided by h^2, so halving h quadruples triangles.",
            ),
        ),
        "Learned shape representations": (
            q(
                "A neural implicit field (e.g. DeepSDF) represents a shape as:",
                (
                    opt("an MLP that outputs SDF or occupancy at any query point", correct=True),
                    opt("a fixed list of triangles"),
                    opt("a 2D photograph"),
                    opt("a G-code program"),
                ),
                "DeepSDF is an MLP f_theta(p, z) predicting signed distance, queryable at any point.",
            ),
            q(
                "Interpolating between two DeepSDF latent codes produces:",
                (
                    opt("a smooth morph between the two shapes", correct=True),
                    opt("two disconnected shapes"),
                    opt("random noise"),
                    opt("a flat plane"),
                ),
                "A continuous latent space lets you interpolate codes to morph smoothly between shapes.",
            ),
            q(
                "A key advantage of neural implicit representations is that they are:",
                (
                    opt("resolution-free (query any point) and compact", correct=True),
                    opt("limited to a single fixed grid size"),
                    opt("unable to be meshed"),
                    opt("always larger than voxel grids"),
                ),
                "They can be sampled at arbitrary resolution and stored compactly as network weights.",
            ),
        ),
    },
    final=(
        q(
            "In SDF modelling, an offset that thickens a shell is implemented by:",
            (
                opt("subtracting a constant from the field, f -> f - t", correct=True),
                opt("multiplying the field by t"),
                opt("taking the maximum with t"),
                opt("squaring the field"),
            ),
            "Offsetting the level set by t uniformly grows or shrinks the surface.",
        ),
        q(
            "Which equation approximates a Schwarz-P minimal surface?",
            (
                opt("cos(x) + cos(y) + cos(z) = c", correct=True),
                opt("x^2 + y^2 + z^2 = r^2"),
                opt("sin(x)*cos(y) + sin(y)*cos(z) + sin(z)*cos(x) = c"),
                opt("x + y + z = c"),
            ),
            "Schwarz-P uses the cosine sum; the sin-cos cyclic sum is the gyroid.",
        ),
        q(
            "Space-colonisation growth is especially suited to generating:",
            (
                opt("branching networks like leaf veins or lungs", correct=True),
                opt("perfectly smooth spheres"),
                opt("flat plates"),
                opt("regular cubes"),
            ),
            "Branches grow toward attractor points, producing organic venation-like networks.",
        ),
        q(
            "Marching cubes outputs a mesh that is, by construction:",
            (
                opt("watertight, suitable for printing", correct=True),
                opt("a point cloud only"),
                opt("a 2D image"),
                opt("a NURBS solid"),
            ),
            "Marching cubes extracts a closed (watertight) triangle isosurface.",
        ),
        q(
            "The DeepSDF training loss is typically a clamped L1 between predicted and true:",
            (
                opt("signed distance samples", correct=True),
                opt("RGB colours"),
                opt("triangle counts"),
                opt("print temperatures"),
            ),
            "It minimises a clamped L1 over sampled SDF values, learning the shape and its latent code.",
        ),
        q(
            "Why are TPMS lattices attractive for additive manufacturing?",
            (
                opt(
                    "they are smooth, self-supporting, and have near-zero mean curvature",
                    correct=True,
                ),
                opt("they have many sharp stress-concentrating corners"),
                opt("they cannot be parameterised"),
                opt("they require solid infill only"),
            ),
            "Near-zero mean curvature means no stress raisers, and they print without internal supports.",
        ),
    ),
)
