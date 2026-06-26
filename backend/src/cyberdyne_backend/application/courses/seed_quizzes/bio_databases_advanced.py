"""Quiz questions for the Biological Databases & Data Management - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Ensembl, genome browsers and coordinates": (
            q(
                "Why is a genomic coordinate meaningless without its assembly?",
                (
                    opt("The same locus has different coordinates across assemblies", correct=True),
                    opt("Coordinates are encrypted per user"),
                    opt("Assemblies have no coordinate system"),
                    opt("Coordinates are random integers"),
                ),
                "Assembly revisions (GRCh37 to GRCh38) shift coordinates, so the assembly must be declared.",
            ),
            q(
                "What does a tool like liftOver/CrossMap do?",
                (
                    opt("Remap features between genome assemblies", correct=True),
                    opt("Compress FASTQ reads"),
                    opt("Predict 3D structures"),
                    opt("Issue DOIs"),
                ),
                "Liftover remaps coordinates from one assembly to another, though not all regions map.",
            ),
            q(
                "BioMart is most useful for:",
                (
                    opt("pulling custom tabular slices without writing SQL", correct=True),
                    opt("aligning raw reads"),
                    opt("rate limiting an API"),
                    opt("storing atomic coordinates"),
                ),
                "BioMart lets users export filtered, joined tables from Ensembl-style resources.",
            ),
        ),
        "REST and GraphQL APIs for data access": (
            q(
                "An HTTP 429 status code from an API means:",
                (
                    opt("too many requests; the client should back off", correct=True),
                    opt("the resource was found successfully"),
                    opt("the record does not exist"),
                    opt("the request was unauthorised"),
                ),
                "429 signals rate limiting; a robust client retries with backoff.",
            ),
            q(
                "Exponential backoff means the wait between retries:",
                (
                    opt("grows exponentially with the attempt number", correct=True),
                    opt("is a fixed constant"),
                    opt("shrinks toward zero"),
                    opt("is chosen by the server header only"),
                ),
                "Backoff multiplies the delay each attempt to relieve an overloaded server.",
            ),
            q(
                "A key advantage of GraphQL over fixed REST endpoints is:",
                (
                    opt(
                        "the client requests exactly the fields it needs in one query", correct=True
                    ),
                    opt("it cannot be rate limited"),
                    opt("it returns only HTML"),
                    opt("it needs no schema"),
                ),
                "GraphQL avoids over- and under-fetching by letting clients shape the response.",
            ),
        ),
        "FAIR principles and persistent identifiers": (
            q(
                "What does the 'F' in FAIR stand for?",
                (
                    opt("Findable", correct=True),
                    opt("Free"),
                    opt("Fast"),
                    opt("Federated"),
                ),
                "FAIR is Findable, Accessible, Interoperable, Reusable.",
            ),
            q(
                "Why is a persistent identifier (PID) central to FAIR data?",
                (
                    opt("It resolves to the resource even when URLs change", correct=True),
                    opt("It compresses the data"),
                    opt("It makes the data open by default"),
                    opt("It deletes old versions"),
                ),
                "PIDs (DOIs, accessions, ORCIDs) give stable, resolvable references.",
            ),
            q(
                "Can data be FAIR yet not open?",
                (
                    opt("Yes; controlled-access human data can still be FAIR", correct=True),
                    opt("No; FAIR means fully public"),
                    opt("Only if it has no metadata"),
                    opt("Only for protein structures"),
                ),
                "FAIR is about good stewardship; access can still be authorised/controlled.",
            ),
        ),
        "Scaling storage for petabyte archives": (
            q(
                "How does CRAM achieve strong compression of aligned reads?",
                (
                    opt(
                        "By storing differences against a reference plus binned qualities",
                        correct=True,
                    ),
                    opt("By deleting all the reads"),
                    opt("By converting reads to protein"),
                    opt("By encrypting the file"),
                ),
                "CRAM is reference-based, encoding only deviations from the reference.",
            ),
            q(
                "The principle 'move compute to data' means:",
                (
                    opt(
                        "run analyses in the cloud next to the archive instead of downloading it",
                        correct=True,
                    ),
                    opt("download everything to a laptop first"),
                    opt("store data only on tape"),
                    opt("disable all indexes"),
                ),
                "Data gravity makes it cheaper to bring computation to petabyte archives.",
            ),
            q(
                "Which columnar format is common for distributed analytical queries?",
                (
                    opt("Parquet", correct=True),
                    opt("FASTA"),
                    opt("mmCIF"),
                    opt("GenBank flat file"),
                ),
                "Parquet is a columnar format scanned efficiently by Spark/BigQuery-style engines.",
            ),
        ),
        "AI-era resources: AlphaFold DB and embeddings": (
            q(
                "What does the pLDDT score in AlphaFold DB report?",
                (
                    opt("Per-residue confidence in the predicted structure", correct=True),
                    opt("The experimental X-ray resolution"),
                    opt("The number of database records"),
                    opt("The sequence length"),
                ),
                "pLDDT is a per-residue confidence; low-confidence regions are unreliable.",
            ),
            q(
                "Embedding-based search retrieves homologues by:",
                (
                    opt(
                        "nearest neighbours of dense vectors from a protein language model",
                        correct=True,
                    ),
                    opt("exact string matching of accessions"),
                    opt("comparing file sizes"),
                    opt("reading PubMed abstracts"),
                ),
                "Models like ESM map sequences to vectors; ANN indexes find close ones.",
            ),
            q(
                "An approximate-nearest-neighbour index (e.g. HNSW) makes vector search:",
                (
                    opt("scale roughly sub-linearly in collection size", correct=True),
                    opt("require comparing against every entry"),
                    opt("impossible above a million records"),
                    opt("identical in cost to BLAST"),
                ),
                "ANN indexes avoid an exhaustive O(n) scan, retrieving in roughly logarithmic time.",
            ),
        ),
        "Integrating data and provenance pipelines": (
            q(
                "The recurring obstacle when joining Ensembl, UniProt and AlphaFold is:",
                (
                    opt("identifier mapping between different accessions", correct=True),
                    opt("lack of any data"),
                    opt("incompatible electricity standards"),
                    opt("missing FASTA headers"),
                ),
                "Each resource uses its own IDs, so mapping/xrefs are needed to integrate.",
            ),
            q(
                "Why run integration in a workflow manager like Nextflow or Snakemake?",
                (
                    opt(
                        "To declare inputs/outputs and capture reproducible provenance",
                        correct=True,
                    ),
                    opt("To avoid using any databases"),
                    opt("To remove version numbers"),
                    opt("To prevent parallel execution"),
                ),
                "Workflow managers record steps, tool versions and provenance for rerunnability.",
            ),
            q(
                "A knowledge graph queried with SPARQL is an example of:",
                (
                    opt("materialising an integrated view of many sources once", correct=True),
                    opt("a raw FASTQ archive"),
                    opt("a rate-limiting policy"),
                    opt("an image compression codec"),
                ),
                "RDF triple stores/knowledge graphs precompute the integrated, queryable view.",
            ),
        ),
    },
    final=(
        q(
            "Why must every coordinate-based analysis declare its genome assembly?",
            (
                opt("The same locus maps to different coordinates across assemblies", correct=True),
                opt("Assemblies change the DNA alphabet"),
                opt("Coordinates are otherwise encrypted"),
                opt("It selects the file format"),
            ),
            "Assembly revisions shift coordinates, so the assembly is part of any locus.",
        ),
        q(
            "A robust API client handling HTTP 429 should:",
            (
                opt("retry with exponential backoff", correct=True),
                opt("retry instantly forever"),
                opt("treat it as success"),
                opt("delete its local cache"),
            ),
            "429 means rate limited; backoff relieves the server and recovers gracefully.",
        ),
        q(
            "Which is NOT one of the FAIR principles?",
            (
                opt("Free", correct=True),
                opt("Findable"),
                opt("Interoperable"),
                opt("Reusable"),
            ),
            "FAIR is Findable, Accessible, Interoperable, Reusable; 'open' is separate.",
        ),
        q(
            "CRAM reduces sequencing archive size mainly by:",
            (
                opt("reference-based compression of aligned reads", correct=True),
                opt("discarding all metadata"),
                opt("storing only protein sequences"),
                opt("converting to FASTA"),
            ),
            "CRAM encodes differences from a reference plus binned qualities.",
        ),
        q(
            "AlphaFold DB differs from the experimental PDB because it stores:",
            (
                opt("predicted structures with per-residue confidence", correct=True),
                opt("only crystallography data"),
                opt("raw sequencing reads"),
                opt("relational schemas"),
            ),
            "AlphaFold DB holds 200M+ predicted models annotated with pLDDT and PAE.",
        ),
        q(
            "The throughline of modern biological data management is that data is valuable when it is:",
            (
                opt("findable, queryable, versioned and reproducibly combined", correct=True),
                opt("stored on a single laptop"),
                opt("never given an identifier"),
                opt("kept in fixed-width text only"),
            ),
            "FAIR identifiers, versioning, indexing and reproducible integration make data useful.",
        ),
    ),
)
