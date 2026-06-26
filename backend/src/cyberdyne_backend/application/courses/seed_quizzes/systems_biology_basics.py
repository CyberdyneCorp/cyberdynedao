"""Quiz questions for the Systems & Network Biology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is systems biology?": (
            q(
                "How does systems biology differ from classical molecular biology?",
                (
                    opt(
                        "It studies components as an interacting network, not in isolation",
                        correct=True,
                    ),
                    opt("It only studies single genes one at a time"),
                    opt("It avoids using mathematical models"),
                    opt("It ignores experimental data entirely"),
                ),
                "Systems biology is integrative: behaviour emerges from interactions among many parts.",
            ),
            q(
                "What is an emergent property?",
                (
                    opt(
                        "A behaviour of the system that no single component has alone", correct=True
                    ),
                    opt("A property of one isolated enzyme"),
                    opt("The molecular weight of a protein"),
                    opt("A purely random measurement error"),
                ),
                "Bistability of a toggle switch is emergent: neither gene has it alone.",
            ),
            q(
                "Which best describes the systems-biology workflow?",
                (
                    opt("Measure, model, simulate, predict, then test and refine", correct=True),
                    opt("Sequence a gene once and stop"),
                    opt("Only run experiments, never model"),
                    opt("Only build models, never measure"),
                ),
                "It is an iterative loop between data and computational models.",
            ),
        ),
        "Biological networks and graphs": (
            q(
                "In a biological network graph, what do nodes and edges represent?",
                (
                    opt("Nodes are molecules; edges are interactions", correct=True),
                    opt("Nodes are interactions; edges are molecules"),
                    opt("Nodes are time points; edges are samples"),
                    opt("Both are always undirected reactions"),
                ),
                "Molecules are nodes, their interactions are edges.",
            ),
            q(
                "What is a hub in a network?",
                (
                    opt("A high-degree node with many connections, often essential", correct=True),
                    opt("A node with exactly one edge"),
                    opt("An edge between two metabolites"),
                    opt("A node with no edges"),
                ),
                "Hubs have unusually many edges and tend to be biologically important.",
            ),
            q(
                "A scale-free network has a degree distribution that follows what form?",
                (
                    opt("A power law: most nodes few links, a few hubs many", correct=True),
                    opt("A uniform distribution"),
                    opt("Every node has identical degree"),
                    opt("A perfectly bell-shaped normal curve"),
                ),
                "P(k) ~ k^-gamma is the scale-free signature.",
            ),
        ),
        "Pathways: metabolism, signalling and regulation": (
            q(
                "What does a signalling pathway like the MAPK cascade primarily do?",
                (
                    opt("Transmit and amplify a signal from receptor to nucleus", correct=True),
                    opt("Replicate the genome"),
                    opt("Store energy as fat"),
                    opt("Translate every mRNA in the cell"),
                ),
                "Successive phosphorylations relay and amplify the signal.",
            ),
            q(
                "Which resources curate biological pathways in machine-readable form?",
                (
                    opt("KEGG, Reactome and WikiPathways", correct=True),
                    opt("GenBank reads only"),
                    opt("Raw microscope images"),
                    opt("Spreadsheets of lab notes only"),
                ),
                "These databases encode pathways for analysis and modelling.",
            ),
            q(
                "Why does a multi-step cascade often give a switch-like response?",
                (
                    opt(
                        "Successive steps sharpen the dose response into a steep sigmoid",
                        correct=True,
                    ),
                    opt("It makes the response perfectly linear"),
                    opt("It removes all nonlinearity"),
                    opt("It eliminates the signal completely"),
                ),
                "Chaining steps steepens the input-output relation.",
            ),
        ),
        "Network motifs": (
            q(
                "What is a network motif?",
                (
                    opt(
                        "A small sub-circuit appearing far more often than in random networks",
                        correct=True,
                    ),
                    opt("A single isolated gene"),
                    opt("The largest hub in the network"),
                    opt("A random edge with no function"),
                ),
                "Motifs are over-represented sub-circuits with identifiable functions.",
            ),
            q(
                "What can a coherent type-1 feed-forward loop with an AND gate do?",
                (
                    opt("Filter out brief input pulses via a sign-sensitive delay", correct=True),
                    opt("Permanently shut off all genes"),
                    opt("Replace the need for any promoter"),
                    opt("Make the response instantaneous to any noise"),
                ),
                "It responds only to persistent input, filtering transient noise.",
            ),
            q(
                "What is one effect of negative autoregulation?",
                (
                    opt("It speeds the response time and reduces noise", correct=True),
                    opt("It slows the response and adds noise"),
                    opt("It makes a gene unable to ever turn on"),
                    opt("It doubles the genome size"),
                ),
                "A self-repressing gene reaches steady state faster.",
            ),
        ),
        "Enzyme kinetics and dose response": (
            q(
                "In the Michaelis-Menten equation, what does Km represent?",
                (
                    opt("The substrate concentration giving half-maximal rate", correct=True),
                    opt("The maximum possible reaction rate"),
                    opt("The total enzyme concentration"),
                    opt("The product concentration at equilibrium"),
                ),
                "Km is the [S] at which v equals Vmax/2; it reflects affinity.",
            ),
            q(
                "What does a Hill coefficient greater than 1 indicate?",
                (
                    opt("Cooperative binding and a steeper, switch-like response", correct=True),
                    opt("No binding at all"),
                    opt("A perfectly linear response"),
                    opt("That Km is negative"),
                ),
                "n>1 sharpens the dose response, enabling switches.",
            ),
            q(
                "At very high substrate concentration, the Michaelis-Menten rate approaches what?",
                (
                    opt("Vmax (saturation)", correct=True),
                    opt("Zero"),
                    opt("Infinity"),
                    opt("Km"),
                ),
                "The rate plateaus at the maximum velocity Vmax.",
            ),
        ),
        "Feedback, robustness and homeostasis": (
            q(
                "What does negative feedback typically produce in a network?",
                (
                    opt("Stability and homeostasis", correct=True),
                    opt("Runaway amplification"),
                    opt("Permanent bistability"),
                    opt("Complete loss of regulation"),
                ),
                "Negative feedback suppresses deviations, stabilising the output.",
            ),
            q(
                "Bacterial chemotaxis is a classic example of what behaviour?",
                (
                    opt(
                        "Exact adaptation: return to baseline regardless of stimulus level",
                        correct=True,
                    ),
                    opt("Irreversible commitment"),
                    opt("Sustained oscillation forever"),
                    opt("No response to stimuli"),
                ),
                "Chemotaxis adapts to absolute level, sensing only changes.",
            ),
            q(
                "Robustness in systems biology is best described as what?",
                (
                    opt(
                        "A system-level insensitivity to parameter or environmental variation",
                        correct=True,
                    ),
                    opt("A property of a single molecule"),
                    opt("The speed of DNA replication"),
                    opt("The molecular weight of an enzyme"),
                ),
                "Robustness arises from network structure, not any one part.",
            ),
        ),
    },
    final=(
        q(
            "Which phrase best captures the core idea of systems biology?",
            (
                opt("The whole is more than the sum of its parts", correct=True),
                opt("Only one gene matters at a time"),
                opt("Models should never be tested against data"),
                opt("Networks are irrelevant to cell function"),
            ),
            "Emergent behaviour arises from interactions among many components.",
        ),
        q(
            "Which network type uses directed activate/repress edges from regulators to targets?",
            (
                opt("Gene regulatory network", correct=True),
                opt("Undirected PPI network"),
                opt("A pie chart"),
                opt("A random unweighted graph"),
            ),
            "GRNs are directed: transcription factors act on target genes.",
        ),
        q(
            "What is the defining feature of a scale-free network?",
            (
                opt("A power-law degree distribution with rare high-degree hubs", correct=True),
                opt("Every node has the same degree"),
                opt("No node has more than two edges"),
                opt("All edges are directed cycles"),
            ),
            "Most nodes have few links; a few hubs dominate connectivity.",
        ),
        q(
            "What kind of response do cooperative (Hill, n>1) interactions create?",
            (
                opt("A steep, switch-like dose response", correct=True),
                opt("A flat, constant response"),
                opt("A strictly linear response"),
                opt("No response at all"),
            ),
            "Cooperativity steepens the input-output curve.",
        ),
        q(
            "Which feedback type underlies bistability and cellular memory?",
            (
                opt("Positive feedback", correct=True),
                opt("Negative feedback only"),
                opt("No feedback"),
                opt("Random diffusion only"),
            ),
            "Positive feedback amplifies and can create two stable states.",
        ),
        q(
            "A feed-forward loop is an example of what?",
            (
                opt("A recurring network motif with a computational function", correct=True),
                opt("A single isolated metabolite"),
                opt("A sequencing error"),
                opt("A type of chromosome"),
            ),
            "The FFL is the most studied network motif.",
        ),
    ),
)
