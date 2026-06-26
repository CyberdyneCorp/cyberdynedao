"""Quiz questions for the Phylogenetics & Molecular Evolution - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What a phylogenetic tree means": (
            q(
                "What does an internal node of a phylogenetic tree represent?",
                (
                    opt("An inferred common ancestor", correct=True),
                    opt("A currently living species"),
                    opt("A measurement error"),
                    opt("A geographic location"),
                ),
                "Tips are observed taxa; internal nodes are inferred ancestors.",
            ),
            q(
                "A clade (monophyletic group) consists of:",
                (
                    opt("An ancestor plus all of its descendants", correct=True),
                    opt("An ancestor plus some of its descendants"),
                    opt("Several unrelated lineages grouped by similarity"),
                    opt("Only the tip taxa drawn next to each other"),
                ),
                "Only a complete ancestor-plus-all-descendants group reflects real history.",
            ),
            q(
                "Why does rotating the two children of a node not change the tree?",
                (
                    opt(
                        "Trees encode shared ancestry, not the left-right order of tips",
                        correct=True,
                    ),
                    opt("Rotation deletes a branch"),
                    opt("Rotation changes the root"),
                    opt("Tip order is the only thing that matters"),
                ),
                "Topology is defined by branching pattern; tip order is arbitrary.",
            ),
        ),
        "Rooting, polarity and the outgroup": (
            q(
                "What does rooting a tree provide that an unrooted tree lacks?",
                (
                    opt(
                        "Polarity: the direction of time and ancestral vs derived states",
                        correct=True,
                    ),
                    opt("The number of taxa"),
                    opt("The alignment columns"),
                    opt("The substitution rate"),
                ),
                "Only a rooted tree distinguishes ancestor from descendant.",
            ),
            q(
                "The standard way to root a tree is to use:",
                (
                    opt("An outgroup known to lie outside the ingroup", correct=True),
                    opt("The taxon with the longest name"),
                    opt("The first taxon in the file"),
                    opt("A randomly chosen tip"),
                ),
                "The root is placed on the branch joining outgroup to ingroup.",
            ),
            q(
                "Midpoint rooting can mislead when:",
                (
                    opt("Substitution rates vary strongly across lineages", correct=True),
                    opt("All lineages evolve at the same rate"),
                    opt("The alignment is gap-free"),
                    opt("There are exactly three taxa"),
                ),
                "Midpoint rooting assumes a roughly clock-like (constant-rate) tree.",
            ),
        ),
        "Homology, orthology and paralogy": (
            q(
                "Orthologs and paralogs differ in that:",
                (
                    opt(
                        "Orthologs arise by speciation, paralogs by gene duplication", correct=True
                    ),
                    opt("Orthologs arise by duplication, paralogs by speciation"),
                    opt("Both arise only by horizontal transfer"),
                    opt("They are synonyms"),
                ),
                "Speciation produces orthologs; duplication produces paralogs.",
            ),
            q(
                "Similarity produced by convergence rather than common ancestry is called:",
                (
                    opt("Homoplasy", correct=True),
                    opt("Orthology"),
                    opt("Synteny"),
                    opt("Recombination"),
                ),
                "Homoplasy is similarity not inherited from a common ancestor.",
            ),
            q(
                "Why is mixing paralogs into a species-tree dataset a problem?",
                (
                    opt(
                        "It recovers the gene history rather than the species history", correct=True
                    ),
                    opt("Paralogs cannot be aligned at all"),
                    opt("Paralogs have no mutations"),
                    opt("It always improves accuracy"),
                ),
                "Sampling different paralogs across taxa traces duplication, not speciation.",
            ),
        ),
        "Multiple sequence alignment": (
            q(
                "In a multiple sequence alignment, a column ideally contains:",
                (
                    opt(
                        "Residues that are positionally homologous (descend from one ancestral site)",
                        correct=True,
                    ),
                    opt("Residues chosen at random"),
                    opt("Only the most common base"),
                    opt("Gaps only"),
                ),
                "Each column is a hypothesis of positional homology.",
            ),
            q(
                "Why do practical tools use progressive alignment along a guide tree?",
                (
                    opt("Exact multiple alignment is computationally intractable", correct=True),
                    opt("Progressive alignment is always optimal"),
                    opt("Guide trees remove the need for sequences"),
                    opt("It avoids using any scoring scheme"),
                ),
                "Optimal MSA is NP-hard, so heuristics like progressive alignment are used.",
            ),
            q(
                "Trimming tools such as trimAl or Gblocks are used to:",
                (
                    opt(
                        "Remove ambiguously aligned, gap-rich regions before tree building",
                        correct=True,
                    ),
                    opt("Add new sequences"),
                    opt("Root the final tree"),
                    opt("Increase the number of taxa"),
                ),
                "Masking unreliable columns avoids spurious homology signal.",
            ),
        ),
        "Genetic distances and saturation": (
            q(
                "The p-distance between two aligned sequences is:",
                (
                    opt("The proportion of sites that differ", correct=True),
                    opt("The number of taxa"),
                    opt("The transition/transversion ratio"),
                    opt("The branch length in time"),
                ),
                "p-distance is the fraction of differing aligned positions.",
            ),
            q(
                "Why does p-distance underestimate true divergence over long times?",
                (
                    opt("Multiple substitutions hit the same site (saturation)", correct=True),
                    opt("Sequences get shorter"),
                    opt("Mutations stop occurring"),
                    opt("Gaps are counted twice"),
                ),
                "Hidden multiple hits make observed differences plateau.",
            ),
            q(
                "The Jukes-Cantor correction blows up as the p-distance approaches:",
                (
                    opt("0.75", correct=True),
                    opt("0.10"),
                    opt("0.50"),
                    opt("1.00"),
                ),
                "At p = 3/4 the JC69 logarithm diverges: the signal is saturated.",
            ),
        ),
        "Distance-based tree building: UPGMA and Neighbor-Joining": (
            q(
                "UPGMA assumes which of the following?",
                (
                    opt("A strict molecular clock (equal rates in all lineages)", correct=True),
                    opt("Unequal rates among lineages"),
                    opt("No mutations occur"),
                    opt("All branches have zero length"),
                ),
                "UPGMA is correct only under a constant-rate clock.",
            ),
            q(
                "What advantage does Neighbor-Joining have over UPGMA?",
                (
                    opt(
                        "It does not assume a molecular clock and handles unequal rates",
                        correct=True,
                    ),
                    opt("It always produces a rooted ultrametric tree"),
                    opt("It uses no distance matrix"),
                    opt("It examines every possible topology exhaustively"),
                ),
                "NJ minimizes total branch length and tolerates rate variation.",
            ),
            q(
                "A general limitation of distance methods compared with likelihood is that they:",
                (
                    opt(
                        "Summarize sequences into distances, discarding per-site information",
                        correct=True,
                    ),
                    opt("Cannot run on more than four taxa"),
                    opt("Require a Bayesian prior"),
                    opt("Always take longer to compute"),
                ),
                "Distances lose the site-by-site signal that character-based methods use.",
            ),
        ),
    },
    final=(
        q(
            "Which group reflects true evolutionary history?",
            (
                opt("A monophyletic clade", correct=True),
                opt("A paraphyletic group"),
                opt("A polyphyletic group"),
                opt("Any group of similar-looking taxa"),
            ),
            "Only a clade (ancestor plus all descendants) is a natural group.",
        ),
        q(
            "An outgroup is used primarily to:",
            (
                opt("Root the tree and establish character polarity", correct=True),
                opt("Increase the alignment length"),
                opt("Remove homoplasy"),
                opt("Speed up the computation"),
            ),
            "Outgroup rooting gives the direction of evolutionary change.",
        ),
        q(
            "Genes that arose by duplication within a genome are:",
            (
                opt("Paralogs", correct=True),
                opt("Orthologs"),
                opt("Outgroups"),
                opt("Synonymous sites"),
            ),
            "Duplication yields paralogs; speciation yields orthologs.",
        ),
        q(
            "Each column of a good MSA represents:",
            (
                opt("A hypothesis of positional homology", correct=True),
                opt("A single species"),
                opt("A guide tree node"),
                opt("A bootstrap replicate"),
            ),
            "Columns align residues inferred to share one ancestral position.",
        ),
        q(
            "Distance corrections such as Jukes-Cantor are needed because:",
            (
                opt("Observed differences saturate due to multiple hits", correct=True),
                opt("Sequences cannot be aligned"),
                opt("Mutations are always beneficial"),
                opt("Trees must be ultrametric"),
            ),
            "Corrections recover true substitutions per site from observed differences.",
        ),
        q(
            "Compared with UPGMA, Neighbor-Joining is preferred because it:",
            (
                opt("Does not assume a molecular clock", correct=True),
                opt("Is the only method that needs an alignment"),
                opt("Produces no branch lengths"),
                opt("Requires fewer than three taxa"),
            ),
            "NJ is consistent for additive distances under varying rates.",
        ),
    ),
)
