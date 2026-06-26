"""Biological Databases & Data Management track: Basics -> Intermediate -> Advanced.

A three-level bioinformatics track on storing, querying and sharing biological
data. It moves from the major sequence and structure repositories (NCBI,
UniProt, PDB) and their file formats, through relational querying with SQL and
the data models behind genome browsers, to Ensembl, programmatic REST/GraphQL
access and FAIR data stewardship. Lessons are `text` with LaTeX, interactive
```plot blocks (growth, query cost, similarity) and ```mermaid diagrams of
schemas, identifier mappings and retrieval pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Biological Databases — Basics ────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="bio-databases-basics",
    title="Biological Databases & Data Management — Basics",
    description=(
        "A first map of the public biological data landscape: why we keep "
        "sequences and structures in centralised repositories, the three "
        "pillars NCBI, UniProt and the PDB, the accessions and cross-references "
        "that tie records together, and the FASTA/GenBank file formats you will "
        "read every day. Interactive growth plots and schema diagrams "
        "throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why biological databases exist",
            "10 min",
            r"""
# Why biological databases exist

Sequencing a genome or solving a protein structure is only useful if others can
find, reuse and build on the result. Since the 1980s the community has pooled
this output into **public databases** so that a sequence deposited in Tokyo can
be queried minutes later in São Paulo. The growth is staggering: the
**International Nucleotide Sequence Database Collaboration** (INSDC) — GenBank
(NCBI, USA), the ENA (EMBL-EBI, Europe) and the DDBJ (Japan) — mirrors the same
records daily, and the volume has grown roughly **exponentially** for decades,
doubling every ~18 months in the high-throughput era.

Databases fall into two broad types. **Primary (archival)** databases store
author-submitted experimental data as-is (GenBank, the PDB). **Secondary
(curated)** databases add expert annotation, non-redundancy and cross-links
(UniProt/Swiss-Prot, RefSeq, Pfam). Most discovery work touches both.

```mermaid
flowchart LR
  LAB["Sequencing / structure lab"] --> SUB["Submit record"]
  SUB --> INSDC["INSDC: GenBank / ENA / DDBJ"]
  INSDC --> CUR["Curated: UniProt, RefSeq, Pfam"]
  CUR --> USER["Researcher queries & reuses"]
```

The exponential accumulation of records is what forces us to treat data
*management* — not just storage — as a discipline:

```plot
{"title": "Growth of public sequence records", "xLabel": "years since 1990", "yLabel": "records (relative)", "xRange": [0, 20], "yRange": [0, 30], "grid": true, "functions": [{"expr": "exp(0.18*x)", "label": "exponential growth", "color": "#2563eb"}]}
```

**Next:** the three pillars — NCBI, UniProt and the PDB.
""",
        ),
        _t(
            "The three pillars: NCBI, UniProt, PDB",
            "12 min",
            r"""
# The three pillars: NCBI, UniProt, PDB

Three institutions anchor everyday bioinformatics. **NCBI** (National Center for
Biotechnology Information) hosts GenBank (nucleotide sequences), RefSeq
(curated reference sequences), PubMed (literature), Gene, and the BLAST search
service — all browsable through the **Entrez** cross-database system. **UniProt**
(a EMBL-EBI / SIB / PIR consortium) is the reference for protein sequence and
function, split into the manually reviewed **Swiss-Prot** and the automatically
annotated **TrEMBL**. The **Protein Data Bank** (PDB), run by the wwPDB, is the
single global archive of experimentally determined 3D macromolecular structures
from X-ray crystallography, cryo-EM and NMR.

Each pillar owns a layer of the central dogma: NCBI the gene/transcript, UniProt
the protein's sequence and annotation, the PDB its folded structure.

```mermaid
flowchart LR
  NCBI["NCBI: GenBank / RefSeq / Gene"] -->|encodes| UP["UniProt: protein sequence + function"]
  UP -->|folds into| PDB["PDB: 3D structure"]
  NCBI -. cross-refs .- UP
  UP -. cross-refs .- PDB
```

They are deeply cross-linked: a UniProt entry lists the GenBank/RefSeq
nucleotides that encode it and the PDB structures that contain it, so you can
walk from a gene to a structure without leaving the web. Coverage is uneven,
though — far more sequences are known than structures, a gap that drives
structure prediction (covered in the Advanced course).

**Next:** accessions, versions and the IDs that name every record.
""",
        ),
        _t(
            "Accessions, versions and identifiers",
            "11 min",
            r"""
# Accessions, versions and identifiers

Every record carries a stable **accession** — a database-issued identifier that
must never be reused for a different entity. Their shapes encode their source:
a GenBank nucleotide looks like `M10051`, a RefSeq transcript like `NM_000518`,
a RefSeq protein like `NP_000509`, a UniProt accession like `P68871`, and a PDB
entry is a short code such as `4HHB`. Learning to read these prefixes tells you
instantly which database and molecule type you are dealing with.

Records change as knowledge improves, so accessions carry a **version** suffix:
`NM_000518.5` is the fifth revision of that transcript. Cite the versioned form
for reproducibility — the bare accession always resolves to the latest version,
which may differ from what your analysis used.

```mermaid
flowchart TB
  ACC["Accession NM_000518"] --> V1["NM_000518.4 (older)"]
  ACC --> V2["NM_000518.5 (current)"]
  V2 --> CITE["Cite versioned ID for reproducibility"]
```

Distinct from accessions are internal **GI numbers** (legacy NCBI integers) and
**secondary accessions** left behind when records merge. A single biological
molecule — say human haemoglobin beta — therefore appears under many IDs across
databases (Gene `3043`, RefSeq `NM_000518`, UniProt `P68871`, PDB `4HHB`).
Reconciling these is the **identifier mapping** problem, central to data
integration.

**Next:** how FASTA and GenBank flat files actually store sequences.
""",
        ),
        _t(
            "FASTA and GenBank file formats",
            "12 min",
            r"""
# FASTA and GenBank file formats

The **FASTA** format is the lingua franca of sequence data: a single header line
beginning with `>` (the identifier and free-text description) followed by the
sequence on subsequent lines, in one-letter IUPAC codes (`ACGT`/`U` for nucleic
acids, 20 letters for amino acids, plus ambiguity codes like `N`). It is plain
text, trivially parsable, and carries no annotation — just the residues.

```
>sp|P68871|HBB_HUMAN Hemoglobin subunit beta
MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKV
```

The **GenBank flat file** is far richer: a structured record with a `LOCUS`
line (length, molecule type, date), `DEFINITION`, `ACCESSION`, `VERSION`, the
`SOURCE`/organism, a **FEATURES** table annotating genes, CDS, exons and their
coordinates, and the `ORIGIN` sequence block. Coordinates and qualifiers in the
features table are what let a browser draw a gene model.

```mermaid
flowchart TB
  GB["GenBank flat file"] --> H["LOCUS / DEFINITION / VERSION"]
  GB --> F["FEATURES: gene, CDS, exon coords"]
  GB --> O["ORIGIN: the sequence"]
  GB -->|strip annotation| FASTA["FASTA: header + residues"]
```

Other formats specialise: **FASTQ** adds per-base Phred quality scores for raw
reads, **GFF/GTF** describe genome annotation as tab-delimited features, and
**PDB/mmCIF** hold atomic coordinates. Choosing the right format — and parsing
it robustly — is a daily bioinformatics skill.

**Next:** searching and retrieving records from the web.
""",
        ),
        _t(
            "Searching and retrieving records",
            "11 min",
            r"""
# Searching and retrieving records

Two retrieval modes dominate. **Text/field search** finds records by metadata:
NCBI's **Entrez** lets you combine terms with Boolean operators and field tags,
e.g. `hemoglobin[Title] AND Homo sapiens[Organism] AND refseq[Filter]`. UniProt
and the PDB offer analogous structured query builders. The skill is narrowing a
huge hit list with the right fields rather than free-text alone.

**Sequence-similarity search** finds records by content. **BLAST** (Basic Local
Alignment Search Tool) takes a query sequence and ranks database hits by local
alignment score, reporting an **E-value** — the number of hits this good
expected by chance. Smaller E-values mean more significant matches; the E-value
falls roughly exponentially as alignment score rises.

```plot
{"title": "BLAST significance vs alignment score", "xLabel": "bit score", "yLabel": "E-value", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "E-value decays with score", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  Q["Query"] --> T{"Know an ID or keyword?"}
  T -->|yes| ENT["Entrez / field search"]
  T -->|no, have a sequence| BL["BLAST similarity search"]
  ENT --> R["Records"]
  BL --> R
```

Both modes return accessions you can then fetch in FASTA, GenBank or other
formats — the bridge from *finding* data to *using* it.

**Next:** turning ad-hoc retrieval into reproducible workflows.
""",
        ),
        _t(
            "From clicks to reproducible workflows",
            "10 min",
            r"""
# From clicks to reproducible workflows

Pointing and clicking through a web portal does not scale and is not
reproducible: nobody can rerun your mouse. The first step toward data
*management* is replacing manual downloads with **scripted, recorded**
retrieval. NCBI exposes **E-utilities** (`esearch`, `efetch`, `elink`) as URL
endpoints; UniProt, the PDB and Ensembl offer REST APIs; and libraries like
**Biopython** wrap them so a few lines fetch exactly the records your analysis
declares.

```mermaid
flowchart LR
  SCRIPT["Versioned script"] --> API["E-utilities / REST API"]
  API --> RAW["Raw records (FASTA/GenBank)"]
  RAW --> PROC["Parse & analyse"]
  PROC --> OUT["Results + provenance log"]
```

Reproducibility rests on a few habits: pin **versioned accessions**, record the
**database release** you queried, save the **exact query string**, and store the
raw downloads alongside results so the pipeline can be rerun. As datasets grow,
the cost of a naive linear scan over flat files grows with them — which is why
the next course moves data into indexed, queryable databases.

```plot
{"title": "Cost of scanning flat files vs dataset size", "xLabel": "records (millions)", "yLabel": "scan time (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "linear scan O(n)", "color": "#2563eb"}]}
```

**Next:** test your grasp of the data landscape.
""",
        ),
        _quiz(),
    ),
)


# ── Biological Databases — Intermediate ──────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="bio-databases-intermediate",
    title="Biological Databases & Data Management — Intermediate",
    description=(
        "The relational core of biological data management: the relational "
        "model and entity-relationship design for genomic data, querying with "
        "SQL (joins, aggregation, indexing), normalisation versus pragmatic "
        "denormalisation, and the structure databases (PDB/mmCIF) and ontologies "
        "(Gene Ontology) that give records shared meaning. Interactive cost "
        "plots and schema diagrams throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The relational model for biological data",
            "12 min",
            r"""
# The relational model for biological data

A **relational database** stores data as **tables** (relations) of rows
(tuples) and typed columns (attributes). Each table has a **primary key** that
uniquely identifies a row, and **foreign keys** that reference keys in other
tables, encoding relationships. For biological data this maps naturally: a
`gene` table, a `transcript` table referencing its gene, a `protein` table
referencing its transcript — the central dogma rendered as keys.

```mermaid
flowchart LR
  GENE["gene (gene_id PK)"] -->|gene_id FK| TX["transcript (tx_id PK, gene_id FK)"]
  TX -->|tx_id FK| PROT["protein (prot_id PK, tx_id FK)"]
  PROT -->|prot_id FK| XREF["xref (prot_id FK, db, accession)"]
```

We design schemas with **entity-relationship (ER) modelling**: identify
entities (gene, transcript, protein), their attributes, and the cardinality of
relationships — one gene has *many* transcripts (1:N), a protein may map to
*many* external databases (N:M, resolved by a junction table). Capturing these
cardinalities correctly prevents both data loss and duplication.

The payoff over flat files is **declarative querying**: you state *what* you
want, not how to fetch it, and the engine plans the execution. The relational
model, formalised by Codd in 1970, underlies the genome-browser back ends, LIMS
and warehouses you will query for the rest of this course.

**Next:** writing SQL to ask questions of the data.
""",
        ),
        _t(
            "Querying with SQL: SELECT and JOIN",
            "13 min",
            r"""
# Querying with SQL: SELECT and JOIN

**SQL** (Structured Query Language) is how we interrogate relational data. The
workhorse is `SELECT … FROM … WHERE`, choosing columns, a source table and a
row filter. To combine related tables you **JOIN** on matching keys:

```sql
SELECT g.symbol, t.tx_id, p.accession
FROM gene g
JOIN transcript t ON t.gene_id = g.gene_id
JOIN protein   p ON p.tx_id    = t.tx_id
WHERE g.organism = 'Homo sapiens';
```

An **INNER JOIN** keeps only rows with matches on both sides; a **LEFT JOIN**
keeps every left-hand row even when no match exists (yielding `NULL`s) — vital
when, say, listing all genes including those with no annotated protein. Getting
join type and condition right is the most common source of subtle errors in
biological queries.

```mermaid
flowchart LR
  G["gene"] -->|INNER JOIN on gene_id| T["transcript"]
  T -->|LEFT JOIN on tx_id| P["protein (may be NULL)"]
```

Filter predicates in `WHERE`, pattern-match with `LIKE`, restrict to sets with
`IN`, and bound numeric ranges (e.g. `WHERE length BETWEEN 100 AND 500`). A
well-formed `WHERE` clause is also what lets an **index** prune the search,
turning a full-table scan into a targeted lookup — the topic two lessons ahead.

**Next:** summarising data with aggregation and grouping.
""",
        ),
        _t(
            "Aggregation, grouping and set operations",
            "12 min",
            r"""
# Aggregation, grouping and set operations

Beyond fetching rows, SQL **summarises** them. Aggregate functions —
`COUNT`, `SUM`, `AVG`, `MIN`, `MAX` — collapse many rows into one statistic.
`GROUP BY` partitions rows first, computing one aggregate per group, and
`HAVING` filters those groups (unlike `WHERE`, which filters rows before
grouping):

```sql
SELECT organism, COUNT(*) AS n_proteins, AVG(length) AS mean_len
FROM protein
GROUP BY organism
HAVING COUNT(*) > 1000
ORDER BY n_proteins DESC;
```

This single query answers "which organisms have over 1000 proteins, and how
long are they on average?" — the kind of cross-cutting question flat files
cannot answer cheaply.

```mermaid
flowchart LR
  ROWS["rows"] --> W["WHERE: filter rows"]
  W --> GB["GROUP BY: partition"]
  GB --> AGG["aggregate per group"]
  AGG --> H["HAVING: filter groups"]
  H --> ORD["ORDER BY / LIMIT"]
```

**Set operations** combine query results: `UNION` (distinct rows from either),
`INTERSECT` (in both — e.g. genes hit by two screens), and `EXCEPT` (in one but
not the other). Together with **subqueries** and **common table expressions
(CTEs)** they let you compose complex analytical questions from simple parts,
keeping queries readable as they grow.

**Next:** making those queries fast with indexes.
""",
        ),
        _t(
            "Indexing and query performance",
            "12 min",
            r"""
# Indexing and query performance

Without help, the engine answers a `WHERE accession = 'P68871'` by reading
every row — a **full table scan**, cost $O(n)$ in the table size. An **index**,
typically a balanced **B-tree**, stores keys in sorted order so a lookup costs
$O(\log n)$: on a 10-million-row table that is the difference between millions
of reads and a couple of dozen. The contrast is dramatic as data grows:

```plot
{"title": "Lookup cost: full scan vs B-tree index", "xLabel": "rows (millions)", "yLabel": "reads (relative)", "xRange": [1, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "full scan O(n)", "color": "#dc2626"}, {"expr": "log(x)+1", "label": "index O(log n)", "color": "#16a34a"}]}
```

Indexes are not free: each one costs storage and slows inserts/updates, since
the index must be maintained. So you index the columns that appear in `WHERE`,
`JOIN` and `ORDER BY` clauses — primary keys (indexed automatically), foreign
keys, and high-selectivity lookup columns like accessions.

```mermaid
flowchart LR
  Q["Query with WHERE/JOIN"] --> PLAN["Planner: EXPLAIN"]
  PLAN -->|index available| IDX["Index scan O(log n)"]
  PLAN -->|none / low selectivity| SCAN["Sequential scan O(n)"]
```

Use `EXPLAIN`/`EXPLAIN ANALYZE` to see the planner's chosen path and confirm an
index is actually used. Reading query plans — not guessing — is the core skill
of database performance tuning.

**Next:** organising the schema with normalisation.
""",
        ),
        _t(
            "Normalisation and schema design",
            "11 min",
            r"""
# Normalisation and schema design

**Normalisation** is the discipline of structuring tables to eliminate
redundancy and the **update anomalies** it causes. If an organism's taxonomy is
copied into every protein row, fixing a renamed species means editing millions
of rows — and any miss leaves inconsistent data. The normal forms remove this:
**1NF** demands atomic values (no comma-lists of cross-references in a cell),
**2NF** removes partial dependencies on part of a composite key, and **3NF**
removes transitive dependencies (taxonomy belongs in an `organism` table the
protein merely references).

```mermaid
flowchart LR
  FLAT["Wide flat table (redundant)"] --> NF1["1NF: atomic cells"]
  NF1 --> NF2["2NF: no partial deps"]
  NF2 --> NF3["3NF: no transitive deps"]
  NF3 --> REF["Reference tables + FKs"]
```

Normalisation trades write-side cleanliness for read-side joins. In
analytical/warehouse settings — and in genome browsers serving heavy read
traffic — engineers often **denormalise** deliberately, precomputing joined
"wide" tables or materialised views to cut query latency, accepting controlled
redundancy. The right point on this spectrum depends on the read/write mix.

A sound schema also enforces **integrity constraints**: `NOT NULL`, `UNIQUE`,
foreign-key constraints and `CHECK` rules so the database itself rejects
impossible data (a negative sequence length, an orphaned transcript). Letting
the engine guard invariants beats trusting every client to behave.

**Next:** structure data and the ontologies that give records meaning.
""",
        ),
        _t(
            "Structure data, mmCIF and ontologies",
            "12 min",
            r"""
# Structure data, mmCIF and ontologies

Structural data has its own data model. The legacy **PDB format** packed atomic
coordinates into fixed-width columns, which broke for very large complexes.
Modern archives use **mmCIF/PDBx** (macromolecular Crystallographic Information
File), a self-describing key–value format organised into named categories
(`_atom_site`, `_entity`, `_struct_conn`) that maps cleanly onto relational
tables — each category is essentially a relation, each tag a column.

```mermaid
flowchart LR
  PDB["Legacy PDB (fixed columns)"] -->|superseded by| CIF["mmCIF / PDBx categories"]
  CIF --> AS["_atom_site (x,y,z,occupancy,B)"]
  CIF --> EN["_entity / _struct_conn"]
  AS --> REL["Loads into relational tables"]
```

Querying structures means asking content questions: which entries contain a
given ligand, fall below a resolution cutoff, or share a fold. Resolution
matters because lower (better) values mean more reliable coordinates.

Just as important is **controlled vocabulary**. The **Gene Ontology (GO)**
provides three structured, machine-readable hierarchies — molecular function,
biological process, cellular component — as a directed acyclic graph where a
term's annotations propagate to its ancestors. Ontologies turn free-text
guesses into queryable, comparable annotations, enabling enrichment analysis
and cross-database integration that plain keywords cannot support.

**Next:** check your relational and structural data skills.
""",
        ),
        _quiz(),
    ),
)


# ── Biological Databases — Advanced ──────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="bio-databases-advanced",
    title="Biological Databases & Data Management — Advanced",
    description=(
        "State-of-the-art biological data access and stewardship: the Ensembl "
        "genome resource and coordinate systems, programmatic REST and GraphQL "
        "APIs with robust pagination and rate handling, the FAIR principles and "
        "persistent identifiers, scalable storage for petabyte sequencing "
        "archives, and AI-era resources such as AlphaFold DB and learned "
        "embedding search. Interactive scaling plots and pipeline diagrams "
        "throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Ensembl, genome browsers and coordinates",
            "12 min",
            r"""
# Ensembl, genome browsers and coordinates

**Ensembl** (EMBL-EBI) is an integrative genome resource: for each species it
ties a **genome assembly** to gene/transcript **annotation**, comparative
genomics (orthologues, gene trees), variation and regulation, all over a shared
coordinate system. The unit of location is `assembly:chromosome:start-end:strand`
(e.g. `GRCh38:11:5225464-5229395:-1`), and every analysis must declare which
**assembly** it uses — coordinates are meaningless without it.

```mermaid
flowchart LR
  ASM["Assembly (GRCh38)"] --> ANN["Gene / transcript annotation"]
  ANN --> COMP["Comparative: orthologues, trees"]
  ANN --> VAR["Variation"]
  ANN --> REG["Regulation"]
  ASM --> LIFT["Liftover between assemblies"]
```

Because assemblies are revised (GRCh37 → GRCh38), the **same biological locus
has different coordinates** across releases, and a coordinate without its
assembly is a common, silent source of error. Tools like **liftOver/CrossMap**
remap features between assemblies, but not every region maps cleanly.

Genome browsers (Ensembl, the UCSC Genome Browser, JBrowse) render these tracks
visually, but their real power for analysis is the **export and API** layer
behind them, and **BioMart**, which lets you pull custom tabular slices (e.g.
all human kinase transcripts with their UniProt IDs) without writing SQL.

**Next:** driving these resources programmatically through APIs.
""",
        ),
        _t(
            "REST and GraphQL APIs for data access",
            "13 min",
            r"""
# REST and GraphQL APIs for data access

Modern resources expose **web APIs** for programmatic access. A **REST** API
maps resources to URLs and uses HTTP verbs and status codes: `GET
/lookup/id/ENSG00000139618` returns a gene as JSON. You select representations
with the `Accept` header (JSON, XML, FASTA) and read status codes —
`200` OK, `404` not found, `429` too many requests — to handle outcomes
programmatically rather than scraping HTML.

```mermaid
flowchart LR
  CLIENT["Client script"] -->|GET /endpoint| API["REST endpoint"]
  API -->|200 + JSON page| CLIENT
  API -->|429 Too Many Requests| BACKOFF["Wait & retry (backoff)"]
  BACKOFF --> CLIENT
```

Two practical realities dominate. **Pagination**: large result sets arrive in
pages (`limit`/`offset` or cursor tokens), and you must loop until exhausted.
**Rate limiting**: servers cap requests and return `429`; a robust client uses
**exponential backoff**, where the wait between retries grows exponentially to
relieve the server.

```plot
{"title": "Exponential backoff between retries", "xLabel": "retry attempt", "yLabel": "wait (relative units)", "xRange": [0, 8], "yRange": [0, 30], "grid": true, "functions": [{"expr": "exp(0.45*x)", "label": "wait = base * 2^attempt", "color": "#dc2626"}]}
```

**GraphQL** APIs (used by UniProt, RNAcentral and others) let the client ask for
exactly the fields it needs in one typed query, avoiding the over-/under-fetching
of fixed REST endpoints. Both styles share the same disciplines: authenticate
where required, cache responses, and respect the provider's usage policy.

**Next:** making the data itself findable and reusable — the FAIR principles.
""",
        ),
        _t(
            "FAIR principles and persistent identifiers",
            "12 min",
            r"""
# FAIR principles and persistent identifiers

The **FAIR** principles define good data stewardship: data should be
**Findable** (rich metadata, a globally unique persistent ID, indexed),
**Accessible** (retrievable by that ID over an open protocol, with metadata
outliving the data), **Interoperable** (using shared vocabularies and formats,
e.g. GO and ontologies), and **Reusable** (clear provenance and a usage
licence). Crucially, FAIR targets **machines** as much as humans — automated
pipelines must be able to find and combine datasets without manual help.

```mermaid
flowchart LR
  F["Findable: PID + metadata"] --> A["Accessible: open protocol"]
  A --> I["Interoperable: shared vocabularies"]
  I --> R["Reusable: provenance + licence"]
```

The keystone is the **persistent identifier (PID)**: a **DOI**, **accession**,
or **ORCID** (for people) that resolves to the resource even when URLs change.
Compact, resolvable IDs via **identifiers.org**/MIRIAM (`uniprot:P68871`)
support cross-resource linking; data deposited in **INSDC**, the PDB or
**Zenodo** acquires a citable PID by design.

FAIR is explicitly **not** the same as "open" — sensitive human genomic data can
be FAIR yet **controlled-access** (e.g. via dbGaP/EGA), where authorisation
gates retrieval but findability and standards still apply. Funders and journals
now mandate FAIR **data-management plans**, making this stewardship a routine
part of the scientific workflow rather than an afterthought.

**Next:** the storage and infrastructure that hold petabyte-scale archives.
""",
        ),
        _t(
            "Scaling storage for petabyte archives",
            "12 min",
            r"""
# Scaling storage for petabyte archives

Raw sequencing output grows faster than per-disk capacity, so archives like the
**Sequence Read Archive (SRA)** and ENA hold petabytes. Three strategies tame
this. **Compression**: domain-specific codecs such as **CRAM** store aligned
reads as differences against a reference plus quality bins, shrinking BAM files
by large factors. **Object storage** in the cloud (S3-style) gives effectively
unbounded, durable capacity addressed by key.

```plot
{"title": "Raw vs reference-compressed archive size", "xLabel": "samples (thousands)", "yLabel": "storage (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "raw / BAM", "color": "#dc2626"}, {"expr": "0.3*x", "label": "CRAM (ref-compressed)", "color": "#16a34a"}]}
```

Beyond a single machine, queries go **distributed**: columnar formats
(**Parquet**), data lakes and engines (Spark, BigQuery) scan terabytes in
parallel, and specialised systems index variants (e.g. tile/zarr stores,
Hail) for population-scale genomics.

```mermaid
flowchart LR
  READS["Raw reads (FASTQ)"] --> ALN["Align to reference"]
  ALN --> CRAM["CRAM: reference compression"]
  CRAM --> OBJ["Cloud object storage"]
  OBJ --> ENGINE["Distributed query (Spark / BigQuery)"]
```

A second principle is **move compute to data**: rather than download a petabyte,
researchers run analyses in the cloud beside the archive (the model behind the
NIH STRIDES / cloud platforms and federated networks like GA4GH). The economics
of data gravity, not just algorithms, now shape how large-scale biology is done.

**Next:** AI-era resources — predicted structures and embedding search.
""",
        ),
        _t(
            "AI-era resources: AlphaFold DB and embeddings",
            "13 min",
            r"""
# AI-era resources: AlphaFold DB and embeddings

Machine learning has created entirely new database categories. **AlphaFold DB**
(DeepMind / EMBL-EBI) holds **predicted** 3D structures for over 200 million
UniProt proteins — orders of magnitude beyond the ~200k experimental PDB
entries — closing the sequence/structure gap. Predicted models are not
ground truth, so each carries per-residue confidence (**pLDDT**) and a
**Predicted Aligned Error (PAE)** matrix; treating low-confidence regions as
reliable coordinates is a classic misuse.

```mermaid
flowchart LR
  SEQ["UniProt sequence"] --> AF["AlphaFold prediction"]
  AF --> MODEL["3D model + pLDDT + PAE"]
  MODEL --> AFDB["AlphaFold DB (200M+ models)"]
  AFDB -. complements .- PDB["Experimental PDB"]
```

The second shift is **embedding-based search**. Protein language models
(ESM, ProtT5) map a sequence to a dense vector so that similar proteins lie
close in vector space; **vector databases** with approximate-nearest-neighbour
indexes (HNSW, IVF) then retrieve homologues that classical BLAST misses,
sub-linearly in the collection size.

```plot
{"title": "Search cost: exact scan vs ANN vector index", "xLabel": "database size (millions)", "yLabel": "comparisons (relative)", "xRange": [1, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "exact / BLAST O(n)", "color": "#dc2626"}, {"expr": "log(x)+1", "label": "ANN index ~O(log n)", "color": "#16a34a"}]}
```

Structure-aware tools (**Foldseek**) and predicted-interaction resources extend
this further. The lasting lesson: AI does not replace databases — it produces
vast new data that still needs FAIR identifiers, confidence metadata and
scalable, queryable storage.

**Next:** test your mastery of modern biological data management.
""",
        ),
        _t(
            "Integrating data and provenance pipelines",
            "11 min",
            r"""
# Integrating data and provenance pipelines

Real projects pull from many sources — Ensembl annotation, UniProt function,
AlphaFold structures, variant archives — and must **integrate** them on shared
keys. The recurring obstacle is **identifier mapping**: the same molecule wears
different accessions in each resource, so services like the **UniProt ID
mapping** tool and **bioDBnet** exist purely to translate IDs, and a mismatch
silently drops or duplicates records.

```mermaid
flowchart LR
  ENS["Ensembl gene IDs"] --> MAP["ID mapping / xrefs"]
  UP["UniProt accessions"] --> MAP
  AF["AlphaFold (by UniProt)"] --> MAP
  MAP --> JOIN["Integrated dataset"]
  JOIN --> PROV["Provenance: sources, versions, queries"]
```

Integration must be **reproducible**, so production work runs in **workflow
managers** — Nextflow, Snakemake, CWL — that declare each step's inputs,
outputs and tool versions, and capture **provenance**: which database release,
which query, which container image produced each result. This metadata is what
makes a published analysis rerunnable years later.

The cost of repeatedly re-fetching and re-joining grows with the number of
sources, which is why teams build local **data warehouses / knowledge graphs**
(e.g. RDF triple stores queried with SPARQL) that materialise the integrated
view once. The throughline of this whole track: data is only valuable when it
is **findable, queryable, versioned and reproducibly combined**.

**Next:** test your mastery of modern biological data management.
""",
        ),
        _quiz(),
    ),
)


BIO_DATABASES_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["BIO_DATABASES_COURSES"]
