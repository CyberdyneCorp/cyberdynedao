"""Create the three "Life Sciences" learning paths + their modules via the
admin API.

Companion to ``create_computer_engineering_path`` — an operational, run-once
helper, NOT app seed data. The 150 Biology→AI-Drug-Design courses are seeded by
the academy seed; this curates them into three guided, enrollable paths that
mirror the degree arc:

  * life-sciences-foundations   — Bacharelado foundations (20 tracks)
  * bioinformatics-omics        — molecular sciences & bioinformatics (13 tracks)
  * drug-design-ai              — computational & AI drug design (17 tracks)

Each module bundles one track's three courses ({slug}-basics/-intermediate/
-advanced) via ``courseSlugs``. Idempotent: existing modules/paths (409) are
skipped, so it is safe to re-run.

    python -m cyberdyne_backend.cli.create_life_sciences_paths

Configuration via environment variables (same scheme as the Computer
Engineering helper):
  ACADEMY_API_BASE   default https://dao.backend.coolify.cyberdynecorp.ai
  ACADEMY_AUTH_BASE  default https://auth.backend.coolify.cyberdynecorp.ai
  ACADEMY_TOKEN      a bearer token (skips login), OR
  ACADEMY_EMAIL / ACADEMY_PASSWORD   to log in
  ACADEMY_INSECURE_TLS=1   disable TLS verification (self-signed hosts)
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_API_BASE = "https://dao.backend.coolify.cyberdynecorp.ai"
DEFAULT_AUTH_BASE = "https://auth.backend.coolify.cyberdynecorp.ai"

# Each tuple is one track -> one module: (slug, title, category, level, icon,
# description). The module bundles the track's three courses. Tracks are grouped
# into the three paths below in the same order learners should take them.
_Track = tuple[str, str, str, str, str, str]

_FOUNDATIONS: tuple[_Track, ...] = (
    (
        "math-life-sciences",
        "Mathematics for Life Sciences",
        "Quantitative",
        "Beginner",
        "📐",
        "Calculus, linear algebra and differential equations for biological models.",
    ),
    (
        "biostatistics",
        "Statistics & Biostatistics",
        "Quantitative",
        "Beginner",
        "📊",
        "Distributions, hypothesis testing, regression and experimental design.",
    ),
    (
        "physics-life-sciences",
        "Physics for Life Sciences",
        "Quantitative",
        "Beginner",
        "⚛️",
        "Mechanics, thermodynamics, diffusion and the biophysics of macromolecules.",
    ),
    (
        "scientific-computing",
        "Scientific Computing & Linux",
        "Quantitative",
        "Beginner",
        "💻",
        "The shell, environments and reproducible pipelines for bioinformatics.",
    ),
    (
        "general-chemistry",
        "General & Inorganic Chemistry",
        "Chemistry",
        "Beginner",
        "🧪",
        "Atoms, bonding, equilibria and kinetics; metals in biology.",
    ),
    (
        "organic-chemistry",
        "Organic Chemistry",
        "Chemistry",
        "Intermediate",
        "⚗️",
        "Functional groups, mechanisms, stereochemistry and biomolecule chemistry.",
    ),
    (
        "physical-chemistry",
        "Physical Chemistry & Thermodynamics",
        "Chemistry",
        "Intermediate",
        "🌡️",
        "Energetics, kinetics, quantum chemistry and spectroscopy.",
    ),
    (
        "analytical-chemistry",
        "Analytical & Instrumental Chemistry",
        "Chemistry",
        "Intermediate",
        "🔭",
        "Separations, chromatography, mass spectrometry and NMR.",
    ),
    (
        "cell-biology",
        "Cell Biology",
        "Core Biology",
        "Beginner",
        "🧫",
        "Membranes, organelles, the cytoskeleton, signalling and the cell cycle.",
    ),
    (
        "biochemistry",
        "Biochemistry",
        "Core Biology",
        "Intermediate",
        "🧬",
        "Biomolecules, enzymes, metabolism and bioenergetics.",
    ),
    (
        "molecular-biology",
        "Molecular Biology",
        "Core Biology",
        "Intermediate",
        "🧬",
        "The central dogma, gene regulation, epigenetics and CRISPR.",
    ),
    (
        "genetics",
        "Genetics",
        "Core Biology",
        "Intermediate",
        "🧬",
        "Inheritance, mutation, population and medical genetics.",
    ),
    (
        "microbiology",
        "Microbiology",
        "Core Biology",
        "Intermediate",
        "🦠",
        "Microbial diversity, growth, pathogenesis and the microbiome.",
    ),
    (
        "physiology",
        "Human Physiology",
        "Core Biology",
        "Intermediate",
        "🫀",
        "Homeostasis and the organ systems behind drug targets.",
    ),
    (
        "immunology",
        "Immunology",
        "Core Biology",
        "Intermediate",
        "🛡️",
        "Innate and adaptive immunity, antibodies and immunotherapeutics.",
    ),
    (
        "evolution-ecology",
        "Evolution & Ecology",
        "Core Biology",
        "Beginner",
        "🌳",
        "Selection, phylogeny, molecular evolution and ecological context.",
    ),
    (
        "programming-biology-python",
        "Python Programming for Biologists",
        "Programming & Data",
        "Intermediate",
        "🐍",
        "Python through Biopython, NumPy and pandas for biological data.",
    ),
    (
        "r-data-analysis",
        "R & Data Analysis",
        "Programming & Data",
        "Intermediate",
        "📈",
        "R, the tidyverse and Bioconductor for omics data analysis.",
    ),
    (
        "bio-databases",
        "Biological Databases & Data Management",
        "Programming & Data",
        "Intermediate",
        "🗄️",
        "NCBI, UniProt, PDB, Ensembl; formats, SQL and FAIR data.",
    ),
    (
        "data-visualization-bio",
        "Scientific Data Visualization",
        "Programming & Data",
        "Intermediate",
        "📊",
        "Charts, networks, genomic tracks and molecular figures.",
    ),
)

_BIOINFORMATICS: tuple[_Track, ...] = (
    (
        "structural-biology",
        "Structural Biology",
        "Molecular & Structural",
        "Intermediate",
        "🧊",
        "Protein/nucleic-acid structure, X-ray, cryo-EM and structure-based design.",
    ),
    (
        "protein-science",
        "Protein Science & Enzymology",
        "Molecular & Structural",
        "Intermediate",
        "🧬",
        "Folding, stability, enzyme kinetics, mechanism and inhibitor design.",
    ),
    (
        "genomics",
        "Genomics",
        "Molecular & Structural",
        "Intermediate",
        "🧬",
        "Genome assembly, annotation, variation and comparative genomics.",
    ),
    (
        "pharmacology",
        "Pharmacology",
        "Molecular & Structural",
        "Intermediate",
        "💊",
        "Receptors, dose-response, pharmacodynamics, pharmacokinetics and ADME.",
    ),
    (
        "medicinal-chemistry",
        "Medicinal Chemistry",
        "Molecular & Structural",
        "Advanced",
        "⚗️",
        "Drug-likeness, SAR, lead optimization and modern modalities.",
    ),
    (
        "bioinformatics",
        "Introduction to Bioinformatics",
        "Bioinformatics Core",
        "Intermediate",
        "🧬",
        "Algorithms, databases, tools and reproducible pipelines.",
    ),
    (
        "sequence-analysis",
        "Sequence Analysis & Alignment",
        "Bioinformatics Core",
        "Intermediate",
        "🔡",
        "Pairwise/multiple alignment, BLAST, profile HMMs and motifs.",
    ),
    (
        "phylogenetics",
        "Phylogenetics & Molecular Evolution",
        "Bioinformatics Core",
        "Advanced",
        "🌳",
        "Tree building, substitution models, Bayesian inference and phylogenomics.",
    ),
    (
        "ngs-analysis",
        "Next-Generation Sequencing Analysis",
        "Bioinformatics Core",
        "Advanced",
        "🧬",
        "Read QC, alignment, variant calling and NGS pipelines.",
    ),
    (
        "transcriptomics",
        "Transcriptomics (RNA-Seq)",
        "Bioinformatics Core",
        "Advanced",
        "🧬",
        "Quantification, differential expression, pathways and isoforms.",
    ),
    (
        "proteomics-metabolomics",
        "Proteomics & Metabolomics",
        "Bioinformatics Core",
        "Advanced",
        "🧪",
        "Mass-spec identification/quantification, PTMs and multi-omics.",
    ),
    (
        "systems-biology",
        "Systems & Network Biology",
        "Bioinformatics Core",
        "Advanced",
        "🕸️",
        "Pathways, networks, dynamical and constraint-based models.",
    ),
    (
        "single-cell-omics",
        "Single-Cell & Spatial Omics",
        "Bioinformatics Core",
        "Advanced",
        "🔬",
        "scRNA-seq, clustering, trajectories and spatial transcriptomics.",
    ),
)

_DRUG_DESIGN: tuple[_Track, ...] = (
    (
        "molecular-modeling",
        "Molecular Modeling & Visualization",
        "Computational",
        "Intermediate",
        "🧬",
        "Force fields, minimization, conformers and system preparation.",
    ),
    (
        "molecular-dynamics",
        "Molecular Dynamics Simulations",
        "Computational",
        "Advanced",
        "🌀",
        "Integrators, ensembles, solvation, free energy and trajectory analysis.",
    ),
    (
        "protein-structure-prediction",
        "Protein Structure Prediction",
        "Computational",
        "Advanced",
        "🧬",
        "Homology modeling, coevolution and AlphaFold/RoseTTAFold.",
    ),
    (
        "cheminformatics",
        "Cheminformatics",
        "Computational",
        "Intermediate",
        "⚗️",
        "SMILES, descriptors, fingerprints, similarity and RDKit.",
    ),
    (
        "computer-aided-drug-design",
        "Computer-Aided Drug Design (CADD)",
        "Computational",
        "Advanced",
        "💊",
        "Structure- and ligand-based design, fragment-based and de novo.",
    ),
    (
        "docking-virtual-screening",
        "Molecular Docking & Virtual Screening",
        "Computational",
        "Advanced",
        "🎯",
        "Poses, scoring functions and high-throughput screening.",
    ),
    (
        "qsar-modeling",
        "QSAR & Pharmacophore Modeling",
        "Computational",
        "Advanced",
        "📐",
        "Linear/nonlinear QSAR, 3D-QSAR, pharmacophores and validation.",
    ),
    (
        "ml-life-sciences",
        "Machine Learning for Life Sciences",
        "AI / ML",
        "Intermediate",
        "🤖",
        "Features, models, cross-validation, metrics and pitfalls in biology.",
    ),
    (
        "deep-learning-biology",
        "Deep Learning for Biology",
        "AI / ML",
        "Advanced",
        "🧠",
        "CNNs, RNNs, transformers, GNNs and protein/sequence language models.",
    ),
    (
        "ai-drug-discovery",
        "AI-Driven Drug Discovery",
        "AI / ML",
        "Advanced",
        "💊",
        "Property/activity prediction, foundation models and active learning.",
    ),
    (
        "generative-molecular-design",
        "Generative Models for Molecular Design",
        "AI / ML",
        "Advanced",
        "✨",
        "VAEs, GANs, RL and diffusion for de novo molecule design.",
    ),
    (
        "target-identification",
        "Computational Target Identification",
        "AI / ML",
        "Advanced",
        "🎯",
        "Omics, network and genetics evidence; druggability and validation.",
    ),
    (
        "admet-prediction",
        "ADMET & Toxicity Prediction",
        "AI / ML",
        "Advanced",
        "🧪",
        "Solubility, permeability, metabolism and toxicity models.",
    ),
    (
        "protein-ligand-binding",
        "Protein-Ligand Binding & Free-Energy Methods",
        "AI / ML",
        "Advanced",
        "🔗",
        "Binding thermodynamics, MM/PBSA, FEP and affinity prediction.",
    ),
    (
        "drug-development-regulatory",
        "Drug Development, Clinical Trials & Regulatory",
        "Translational",
        "Advanced",
        "📋",
        "Preclinical, trial phases, GxP, regulatory pathways and IP.",
    ),
    (
        "reproducible-research",
        "Reproducible Research & Scientific Software",
        "Translational",
        "Intermediate",
        "♻️",
        "Version control, workflows (Nextflow/Snakemake), containers and FAIR.",
    ),
    (
        "capstone-ai-drug-design",
        "Capstone: End-to-End AI Drug Design Project",
        "Translational",
        "Advanced",
        "🏆",
        "Target → screen → model → generate → validate, end to end.",
    ),
)

# (path slug, title, icon, estimated_time, description, tracks)
_PATHS: tuple[tuple[str, str, str, str, str, tuple[_Track, ...]], ...] = (
    (
        "life-sciences-foundations",
        "Biology Foundations",
        "🧫",
        "20-30 weeks",
        "The Bacharelado base: the quantitative, chemical and biological "
        "fundamentals — plus programming and data skills — that everything else "
        "builds on. No prior chemistry or programming assumed.",
        _FOUNDATIONS,
    ),
    (
        "bioinformatics-omics",
        "Bioinformatics & Omics",
        "🧪",
        "12-18 weeks",
        "Where biology meets computation: molecular and structural sciences, "
        "sequence and phylogenetic analysis, NGS, and the omics (transcriptomics, "
        "proteomics, metabolomics, single-cell).",
        _BIOINFORMATICS,
    ),
    (
        "drug-design-ai",
        "Drug Design & AI",
        "💊",
        "16-24 weeks",
        "The Mestrado core: molecular modeling and simulation, cheminformatics "
        "and CADD, then machine learning, generative design and an end-to-end "
        "AI drug-design capstone.",
        _DRUG_DESIGN,
    ),
)

_LEVELS = ("basics", "intermediate", "advanced")


def build_payloads() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (module payloads, path payloads). Pure — unit-tested. Each module
    bundles a track's three courses; each path references only modules built
    here. Module slugs are namespaced ``ls-`` to avoid clashing with existing
    learning modules (e.g. the Computer Engineering ``databases`` module)."""
    modules: list[dict[str, Any]] = []
    paths: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path_slug, title, icon, est, desc, tracks in _PATHS:
        module_slugs: list[str] = []
        for track_slug, m_title, category, level, m_icon, m_desc in tracks:
            mod_slug = f"ls-{track_slug}"
            if mod_slug in seen:  # pragma: no cover - guards editing mistakes
                raise ValueError(f"duplicate module slug: {mod_slug}")
            seen.add(mod_slug)
            modules.append(
                {
                    "slug": mod_slug,
                    "title": m_title,
                    "category": category,
                    "level": level,
                    "duration": "4-6 hr",
                    "icon": m_icon,
                    "description": m_desc,
                    "topics": ["Basics", "Intermediate", "Advanced"],
                    "courseSlugs": [f"{track_slug}-{lv}" for lv in _LEVELS],
                }
            )
            module_slugs.append(mod_slug)
        paths.append(
            {
                "slug": path_slug,
                "title": title,
                "description": desc,
                "moduleSlugs": module_slugs,
                "estimatedTime": est,
                "icon": icon,
            }
        )
    return modules, paths


def _ctx() -> ssl.SSLContext | None:
    if os.environ.get("ACADEMY_INSECURE_TLS") == "1":
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None


def _call(method: str, url: str, token: str, body: dict[str, Any] | None = None) -> tuple[int, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, context=_ctx()) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw


def _token() -> str:
    token = os.environ.get("ACADEMY_TOKEN")
    if token:
        return token
    auth = os.environ.get("ACADEMY_AUTH_BASE", DEFAULT_AUTH_BASE)
    email = os.environ.get("ACADEMY_EMAIL")
    password = os.environ.get("ACADEMY_PASSWORD")
    if not (email and password):
        raise SystemExit("set ACADEMY_TOKEN, or ACADEMY_EMAIL + ACADEMY_PASSWORD")
    req = urllib.request.Request(
        f"{auth}/api/v1/auth/login",
        data=json.dumps({"email": email, "password": password}).encode(),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=_ctx()) as r:
        access_token: str = json.loads(r.read().decode())["access_token"]
    return access_token


def main() -> int:
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    token = _token()
    modules, paths = build_payloads()

    for module in modules:
        st, _ = _call("POST", f"{api}/api/v1/admin/learning/modules", token, module)
        verb = "created" if st in (200, 201) else ("exists" if st == 409 else f"FAILED {st}")
        print(f"  module {module['slug']}: {verb}")

    failed = 0
    for path in paths:
        st, body = _call("POST", f"{api}/api/v1/admin/learning/paths", token, path)
        if st in (200, 201):
            print(f"  path {path['slug']}: created")
        elif st == 409:
            print(f"  path {path['slug']}: exists")
        else:
            print(f"  path {path['slug']}: FAILED {st} {body}")
            failed += 1
    if failed:
        return 1
    print("Done — the three Life Sciences paths are live and enrollable.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
