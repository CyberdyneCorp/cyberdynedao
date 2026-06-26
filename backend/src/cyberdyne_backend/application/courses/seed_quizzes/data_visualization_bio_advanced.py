"""Quiz questions for the Scientific Data Visualization - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Dimensionality reduction maps": (
            q(
                "Compared with PCA, t-SNE and UMAP are designed to preserve:",
                (
                    opt("Local neighbourhood structure", correct=True),
                    opt("Global distances exactly"),
                    opt("Linear axes of variance"),
                    opt("The raw gene counts"),
                ),
                "PCA is linear and global; t-SNE/UMAP prioritise local neighbours.",
            ),
            q(
                "In a UMAP or t-SNE plot, which is NOT reliably meaningful?",
                (
                    opt("The distance and size of gaps between clusters", correct=True),
                    opt("Which points are neighbours"),
                    opt("Membership within a cluster"),
                    opt("Local groupings of cells"),
                ),
                "Only neighbour membership is faithful; inter-cluster distance and cluster size are not.",
            ),
            q(
                "t-SNE's perplexity and UMAP's n_neighbors control:",
                (
                    opt("The balance between local and global structure", correct=True),
                    opt("The colour scale"),
                    opt("The number of genes"),
                    opt("The output file format"),
                ),
                "These parameters trade off how much local versus global detail is preserved.",
            ),
        ),
        "Network & graph visualisation": (
            q(
                "Force-directed layouts position nodes by treating edges as:",
                (
                    opt("Springs, with nodes as mutually repelling charges", correct=True),
                    opt("Fixed grid cells"),
                    opt("Random coordinates"),
                    opt("Alphabetical lists"),
                ),
                "Fruchterman-Reingold and ForceAtlas2 minimise a spring-charge energy.",
            ),
            q(
                "The 'hairball' problem in dense networks is best mitigated by:",
                (
                    opt("Filtering edges or switching to a matrix (adjacency) view", correct=True),
                    opt("Adding more edges"),
                    opt("Using a rainbow palette"),
                    opt("Removing all node labels only"),
                ),
                "Matrix views and edge filtering scale to dense graphs where layouts tangle.",
            ),
            q(
                "Mapping node size to degree is an example of:",
                (
                    opt("Encoding a graph property on a visual channel", correct=True),
                    opt("Changing the layout algorithm"),
                    opt("Computing centrality"),
                    opt("Filtering the graph"),
                ),
                "Size, colour and edge width carry degree, module and confidence.",
            ),
        ),
        "Genomic tracks & heatmaps": (
            q(
                "Genome-browser tracks are aligned so that:",
                (
                    opt("Features at the same genomic coordinate line up vertically", correct=True),
                    opt("Colours match across tracks"),
                    opt("Every track uses the same height"),
                    opt("Tracks are sorted alphabetically"),
                ),
                "A shared horizontal coordinate axis lets the eye correlate features by position.",
            ),
            q(
                "A Manhattan plot displays:",
                (
                    opt("Genomic position on x and -log10(p) on y", correct=True),
                    opt("Time on x and temperature on y"),
                    opt("Two principal components"),
                    opt("A protein surface"),
                ),
                "Strong GWAS associations rise above the significance threshold line.",
            ),
            q(
                "For a row-scaled (z-score) expression heatmap, the right colour scale is:",
                (
                    opt("Diverging and zero-centred", correct=True),
                    opt("Sequential single-hue"),
                    opt("Qualitative"),
                    opt("Rainbow / jet"),
                ),
                "Z-scores have a meaningful zero, so over- and under-expression should read symmetrically.",
            ),
        ),
        "Molecular & structural figures": (
            q(
                "To show a protein's secondary structure and overall fold, use a:",
                (
                    opt("Cartoon / ribbon representation", correct=True),
                    opt("Solvent surface"),
                    opt("Ball-and-stick of every atom"),
                    opt("A bar chart"),
                ),
                "Cartoons abstract the backbone into helices and sheets.",
            ),
            q(
                "When presenting an AlphaFold model you should always show:",
                (
                    opt("pLDDT confidence colouring and the PAE plot", correct=True),
                    opt("Only a single ribbon with no confidence"),
                    opt("The raw FASTA sequence"),
                    opt("A pie chart of residues"),
                ),
                "Confidence metrics prevent presenting low-confidence regions as determined structure.",
            ),
            q(
                "Colouring a molecular surface red-to-blue typically encodes:",
                (
                    opt("Electrostatic potential (negative to positive)", correct=True),
                    opt("Residue number"),
                    opt("Atom mass"),
                    opt("The chain identifier only"),
                ),
                "Red negative, blue positive is the conventional electrostatic mapping.",
            ),
        ),
        "Interactive & AI-assisted visualisation": (
            q(
                "Shneiderman's visual-information mantra is:",
                (
                    opt("Overview first, zoom and filter, then details on demand", correct=True),
                    opt("Details first, never zoom"),
                    opt("Always show everything at once"),
                    opt("Random exploration only"),
                ),
                "This sequence structures effective interactive exploration.",
            ),
            q(
                "A key caution for AI-generated charts is that they:",
                (
                    opt(
                        "Must be checked for misleading axes, wrong scales and fabricated trends",
                        correct=True,
                    ),
                    opt("Are always correct by construction"),
                    opt("Never need colour-blind-safe palettes"),
                    opt("Cannot be edited"),
                ),
                "AI tools inherit model blind spots and require verification.",
            ),
            q(
                "Where does AI enter the modern visualisation pipeline?",
                (
                    opt(
                        "Chart generation, embedding/layout, and captioning/accessibility",
                        correct=True,
                    ),
                    opt("Only in printing"),
                    opt("Only in choosing fonts"),
                    opt("Nowhere"),
                ),
                "NL-to-chart, neural UMAP/parametric t-SNE, and alt-text generation are all AI-assisted.",
            ),
        ),
    },
    final=(
        q(
            "Why must DR-map parameters always be reported?",
            (
                opt("Different settings yield qualitatively different maps", correct=True),
                opt("They change the file size"),
                opt("They are required by law"),
                opt("They set the colour palette only"),
            ),
            "t-SNE/UMAP are stochastic and parameter-sensitive, so settings affect interpretation.",
        ),
        q(
            "A scale-free network's degree distribution roughly follows:",
            (
                opt("A power law, P(k) ~ k^(-gamma)", correct=True),
                opt("A uniform distribution"),
                opt("A bell curve centred on the mean"),
                opt("A straight horizontal line"),
            ),
            "A few hubs and many low-degree nodes produce a heavy-tailed power law.",
        ),
        q(
            "A clustered heatmap reorders rows and columns using:",
            (
                opt("Dendrograms from hierarchical clustering", correct=True),
                opt("Alphabetical sorting"),
                opt("Random shuffling"),
                opt("The file timestamp"),
            ),
            "Hierarchical clustering reorders so co-regulated blocks become visible.",
        ),
        q(
            "The surface representation of a structure is most useful for:",
            (
                opt("Showing pockets and shape complementarity", correct=True),
                opt("Reading the exact sequence"),
                opt("Counting hydrogen bonds at the active site"),
                opt("Displaying secondary structure"),
            ),
            "The solvent-accessible envelope highlights cavities and binding surfaces.",
        ),
        q(
            "Linked (brushing) views in an interactive tool let a user:",
            (
                opt("Select in one view and see the selection highlighted in others", correct=True),
                opt("Disable all interactivity"),
                opt("Export to PDF only"),
                opt("Change the model's weights"),
            ),
            "Coordinated views connect selections across panels for exploration.",
        ),
        q(
            "Accessibility in visualisation requires:",
            (
                opt("Colour-blind-safe palettes, alt-text and direct labels", correct=True),
                opt("Hue-only encoding"),
                opt("Removing all labels"),
                opt("Rainbow colormaps"),
            ),
            "Accessibility is a requirement, not a finishing touch, in modern figures.",
        ),
    ),
)
