"""Quiz questions for the Cheminformatics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is cheminformatics and why it exists": (
            q(
                "Cheminformatics is best described as the science of what?",
                (
                    opt(
                        "Representing, storing, searching and analysing chemical information with computers",
                        correct=True,
                    ),
                    opt("Synthesising new reagents in a wet lab"),
                    opt("Designing laboratory glassware"),
                    opt("Manufacturing pharmaceutical tablets"),
                ),
                "It applies computation and statistics to chemical structures and data.",
            ),
            q(
                "Which databases are major public sources of chemical structures?",
                (
                    opt("PubChem and ChEMBL", correct=True),
                    opt("GenBank and UniProt"),
                    opt("IMDb and Wikipedia"),
                    opt("PDB and only PDB"),
                ),
                "PubChem and ChEMBL hold tens of millions of compounds with measured data.",
            ),
            q(
                "Why is computational triage essential in chemistry?",
                (
                    opt(
                        "Drug-like chemical space is far larger than what can be synthesised and tested",
                        correct=True,
                    ),
                    opt("Computers can perform chemical reactions directly"),
                    opt("Lab instruments stopped working"),
                    opt("There are too few known molecules to study"),
                ),
                "Estimated drug-like space is ~10^60 molecules, so we must choose computationally.",
            ),
        ),
        "Molecules as graphs: atoms, bonds and valence": (
            q(
                "In the molecular-graph abstraction, what are atoms and bonds?",
                (
                    opt("Atoms are vertices (nodes) and bonds are edges", correct=True),
                    opt("Atoms are edges and bonds are vertices"),
                    opt("Both are edges"),
                    opt("Both are 3D coordinates only"),
                ),
                "A molecule is modelled as a graph: atoms = nodes, bonds = edges.",
            ),
            q(
                "How many bonds does a neutral carbon atom typically form?",
                (
                    opt("Four", correct=True),
                    opt("One"),
                    opt("Two"),
                    opt("Six"),
                ),
                "Neutral carbon has a valence of four.",
            ),
            q(
                "Substructure search is an instance of which graph problem?",
                (
                    opt("Subgraph isomorphism", correct=True),
                    opt("Shortest path"),
                    opt("Minimum spanning tree"),
                    opt("Topological sort"),
                ),
                "Finding a pattern inside a molecule is subgraph isomorphism.",
            ),
        ),
        "SMILES: writing molecules as text": (
            q(
                "What does SMILES encode?",
                (
                    opt("A molecular graph as a compact ASCII string", correct=True),
                    opt("A 3D protein fold"),
                    opt("A reaction rate constant"),
                    opt("A spectroscopy trace"),
                ),
                "SMILES walks the graph and writes atoms and bonds as text.",
            ),
            q(
                "In SMILES, how is a benzene ring commonly written?",
                (
                    opt("c1ccccc1", correct=True),
                    opt("C-C-C-C-C-C"),
                    opt("[Bz]"),
                    opt("O=C=O"),
                ),
                "Lowercase letters denote aromatic atoms; matching ring digits close the ring.",
            ),
            q(
                "A key limitation of raw SMILES strings is that they are:",
                (
                    opt("Non-unique: one molecule has many valid strings", correct=True),
                    opt("Always exactly one per molecule"),
                    opt("Unable to represent rings"),
                    opt("Binary, not text"),
                ),
                "Ethanol is both CCO and OCC, so canonicalisation is needed to compare.",
            ),
        ),
        "Canonicalisation and structure validation": (
            q(
                "What problem does canonicalisation solve?",
                (
                    opt(
                        "It produces one deterministic SMILES per molecule for comparison",
                        correct=True,
                    ),
                    opt("It computes binding energies"),
                    opt("It draws 3D structures"),
                    opt("It measures reaction yields"),
                ),
                "Canonical ordering yields a single canonical SMILES so duplicates can be found.",
            ),
            q(
                "Which classic algorithm underlies canonical atom ranking?",
                (
                    opt("The Morgan algorithm", correct=True),
                    opt("Dijkstra's algorithm"),
                    opt("Newton-Raphson"),
                    opt("Gaussian elimination"),
                ),
                "Morgan-style iterative refinement of atom invariants gives a canonical order.",
            ),
            q(
                "What is an InChIKey used for?",
                (
                    opt("A fixed-length hash for exact-structure lookup", correct=True),
                    opt("Measuring lipophilicity"),
                    opt("Encoding 3D coordinates"),
                    opt("Storing reaction mechanisms"),
                ),
                "The InChIKey is a hashed, searchable key for exact-match retrieval.",
            ),
        ),
        "Chemical file formats and databases": (
            q(
                "What does an SDF file typically contain?",
                (
                    opt("Many molecules plus tagged property fields", correct=True),
                    opt("Only a single protein sequence"),
                    opt("Raw spectrometer voltages"),
                    opt("Compiled program code"),
                ),
                "SDF concatenates Molfiles with associated data, ideal for screening libraries.",
            ),
            q(
                "Which is a recommended ingest practice for chemical databases?",
                (
                    opt(
                        "Convert structures to a canonical form and store the InChIKey",
                        correct=True,
                    ),
                    opt("Keep every random SMILES string as-is"),
                    opt("Discard all identifiers"),
                    opt("Store only the molecular weight"),
                ),
                "Canonicalising on ingest enables deduplication and exact lookup.",
            ),
            q(
                "ChEMBL is best known for holding what?",
                (
                    opt("Bioactive molecules with measured potencies", correct=True),
                    opt("Only protein crystal structures"),
                    opt("Genome sequences"),
                    opt("Weather records"),
                ),
                "ChEMBL curates bioactive compounds and their activity data.",
            ),
        ),
    },
    final=(
        q(
            "The dominant abstraction for a molecule in cheminformatics is:",
            (
                opt("A graph of atoms (nodes) and bonds (edges)", correct=True),
                opt("A single floating-point number"),
                opt("A bitmap image"),
                opt("A sound waveform"),
            ),
            "Molecules are modelled as graphs.",
        ),
        q(
            "Which SMILES string represents acetic acid?",
            (
                opt("CC(=O)O", correct=True),
                opt("CCO"),
                opt("O=C=O"),
                opt("c1ccccc1"),
            ),
            "CC(=O)O is acetic acid; CCO is ethanol.",
        ),
        q(
            "Why must SMILES be canonicalised before string comparison?",
            (
                opt(
                    "Because one molecule can be written as many different valid SMILES",
                    correct=True,
                ),
                opt("Because SMILES cannot store rings"),
                opt("Because SMILES is a binary format"),
                opt("Because canonical SMILES is shorter to type"),
            ),
            "Non-uniqueness means raw strings cannot be compared directly.",
        ),
        q(
            "Sanitisation of a structure includes perceiving aromaticity using which rule?",
            (
                opt("Huckel's 4n+2 rule", correct=True),
                opt("The octet rule only"),
                opt("Hund's rule"),
                opt("The Pauli exclusion principle"),
            ),
            "Aromaticity perception checks Huckel's 4n+2 condition.",
        ),
        q(
            "Which format is best for shipping a screening library with per-molecule data?",
            (
                opt("SDF", correct=True),
                opt("Plain CSV of names only"),
                opt("A single PDB file"),
                opt("A JPEG image"),
            ),
            "SDF carries many structures plus tagged property fields.",
        ),
        q(
            "Searching a database for a substructure corresponds to which problem?",
            (
                opt("Subgraph isomorphism", correct=True),
                opt("Sorting"),
                opt("Linear regression"),
                opt("Fourier transform"),
            ),
            "Substructure search is subgraph isomorphism on molecular graphs.",
        ),
    ),
)
