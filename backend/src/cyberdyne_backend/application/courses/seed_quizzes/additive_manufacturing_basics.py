"""Quiz questions for the Additive Manufacturing - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is additive manufacturing?": (
            q(
                "How does additive manufacturing build a part?",
                (
                    opt("By adding material layer upon layer from a 3D model", correct=True),
                    opt("By removing material from a solid billet"),
                    opt("By pouring molten metal into a mould"),
                    opt("By forging a heated blank between dies"),
                ),
                "AM is additive - material is added layer by layer, unlike subtractive or formative methods.",
            ),
            q(
                "A key economic advantage of AM is that cost is largely decoupled from:",
                (
                    opt("geometric complexity", correct=True),
                    opt("material density"),
                    opt("the operator's wage"),
                    opt("electricity price"),
                ),
                "An internal channel or lattice costs little more than a solid block, so complexity is nearly free.",
            ),
            q(
                "For a fixed part height, halving the layer thickness will:",
                (
                    opt("double the number of layers", correct=True),
                    opt("halve the number of layers"),
                    opt("leave the layer count unchanged"),
                    opt("eliminate the need for supports"),
                ),
                "Number of layers N = H/t, so halving t doubles N (and roughly doubles build time).",
            ),
        ),
        "The seven AM process families": (
            q(
                "Which standard defines AM terminology and the process families?",
                (
                    opt("ISO/ASTM 52900", correct=True),
                    opt("ISO 9001"),
                    opt("ASME Y14.5"),
                    opt("IEC 61131"),
                ),
                "ISO/ASTM 52900 is the foundational AM terminology standard.",
            ),
            q(
                "Which family uses a laser or projector to cure liquid resin?",
                (
                    opt("Vat photopolymerization", correct=True),
                    opt("Material extrusion"),
                    opt("Binder jetting"),
                    opt("Sheet lamination"),
                ),
                "Vat photopolymerization (SLA/DLP) cures liquid photopolymer with light.",
            ),
            q(
                "Powder bed fusion fuses material using:",
                (
                    opt("a focused laser or electron beam on a powder bed", correct=True),
                    opt("a heated nozzle extruding filament"),
                    opt("jetted droplets of photopolymer"),
                    opt("bonded and cut sheets of material"),
                ),
                "PBF (SLS/SLM/DMLS/EBM) sinters or melts a powder bed with a laser or electron beam.",
            ),
        ),
        "Fused filament fabrication (FFF/FDM)": (
            q(
                "In FFF, the volumetric flow rate needed is approximately:",
                (
                    opt("line width x layer height x print speed", correct=True),
                    opt("nozzle diameter divided by speed"),
                    opt("layer height divided by speed"),
                    opt("filament diameter times bed temperature"),
                ),
                "Vdot = w * h * v; the hot end's melt rate caps achievable speed.",
            ),
            q(
                "FFF parts are mechanically anisotropic mainly because:",
                (
                    opt("inter-layer (Z) bonds are weaker than beads within a layer", correct=True),
                    opt("the filament is stronger when heated"),
                    opt("infill is always 100 percent"),
                    opt("the bed temperature varies randomly"),
                ),
                "Layer-to-layer adhesion in Z is weaker than the continuous material in the XY plane.",
            ),
            q(
                "A typical FFF nozzle diameter is about:",
                (
                    opt("0.4 mm", correct=True),
                    opt("4 mm"),
                    opt("0.01 mm"),
                    opt("2 mm"),
                ),
                "0.4 mm is the common default nozzle size for FFF printers.",
            ),
        ),
        "Stereolithography (SLA/DLP)": (
            q(
                "The Jacobs working curve relates cure depth to exposure as:",
                (
                    opt("Cd = Dp * ln(E/Ec)", correct=True),
                    opt("Cd = Dp * E / Ec"),
                    opt("Cd = E / (Dp * Ec)"),
                    opt("Cd = Ec * ln(E * Dp)"),
                ),
                "Cure depth grows logarithmically with exposure above the critical energy Ec.",
            ),
            q(
                "Compared with FFF, SLA typically offers:",
                (
                    opt("finer resolution and smoother surfaces", correct=True),
                    opt("stronger inter-layer bonds always"),
                    opt("no post-processing"),
                    opt("cheaper feedstock per kilogram"),
                ),
                "Tiny laser spot or LCD pixel gives 25-100 um layers and sharp detail.",
            ),
            q(
                "After printing, an SLA part is typically washed and then:",
                (
                    opt("UV post-cured to reach full mechanical properties", correct=True),
                    opt("quenched in water to harden it"),
                    opt("sintered in a furnace"),
                    opt("electroplated"),
                ),
                "Wash in IPA, remove supports, then UV post-cure to fully crosslink the resin.",
            ),
        ),
        "The digital workflow: CAD to G-code": (
            q(
                "An STL file represents a part as:",
                (
                    opt("a triangle mesh of its surface", correct=True),
                    opt("a parametric B-rep solid"),
                    opt("a stack of bitmap images"),
                    opt("a list of G-code commands"),
                ),
                "STL stores the surface as tessellated triangles; 3MF adds units, color and materials.",
            ),
            q(
                "What does the slicer produce as its final output?",
                (
                    opt("G-code with motion and extrusion commands", correct=True),
                    opt("a CAD assembly"),
                    opt("an STL mesh"),
                    opt("a CMM inspection report"),
                ),
                "The slicer intersects the mesh into layers and emits machine G-code.",
            ),
            q(
                "Exporting an STL with too coarse a tessellation causes:",
                (
                    opt("visible facets / chord error on curved surfaces", correct=True),
                    opt("a perfectly smooth surface"),
                    opt("loss of all infill"),
                    opt("automatic support generation"),
                ),
                "Chord error delta = R(1 - cos(theta/2)) grows with facet angle, showing facets.",
            ),
        ),
    },
    final=(
        q(
            "Additive manufacturing is best described as:",
            (
                opt("building a part layer by layer from a 3D model", correct=True),
                opt("machining a part from a billet"),
                opt("casting a part in a mould"),
                opt("stamping sheet metal"),
            ),
            "AM adds material layer by layer, the defining characteristic.",
        ),
        q(
            "Which process family is fused filament fabrication part of?",
            (
                opt("Material extrusion", correct=True),
                opt("Vat photopolymerization"),
                opt("Powder bed fusion"),
                opt("Binder jetting"),
            ),
            "FFF/FDM is a material-extrusion process.",
        ),
        q(
            "Stereolithography belongs to which family?",
            (
                opt("Vat photopolymerization", correct=True),
                opt("Material extrusion"),
                opt("Directed energy deposition"),
                opt("Sheet lamination"),
            ),
            "SLA/DLP cure liquid resin and are vat photopolymerization.",
        ),
        q(
            "In FFF, doubling layer height at fixed volumetric flow will:",
            (
                opt("roughly halve the maximum print speed", correct=True),
                opt("double the maximum print speed"),
                opt("leave print speed unchanged"),
                opt("require a smaller nozzle"),
            ),
            "Vdot = w*h*v, so larger h means lower achievable v for fixed flow.",
        ),
        q(
            "Which file format adds units, color and material data beyond STL?",
            (
                opt("3MF", correct=True),
                opt("CSV"),
                opt("DXF"),
                opt("PDF"),
            ),
            "3MF is a richer AM format carrying units, color and materials.",
        ),
        q(
            "A major advantage of AM relative to machining is:",
            (
                opt("complex internal geometry adds little cost", correct=True),
                opt("it always produces stronger parts"),
                opt("it needs no digital model"),
                opt("it never requires post-processing"),
            ),
            "AM cost is largely decoupled from geometric complexity.",
        ),
    ),
)
