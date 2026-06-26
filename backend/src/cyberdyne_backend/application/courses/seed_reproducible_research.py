"""Reproducible Research & Scientific Software track: Basics -> Intermediate -> Advanced.

Teaches the practice of computational reproducibility — from Git and project
structure, through environments, testing and workflow managers (Snakemake,
Nextflow), to containers, FAIR data and open science. Lessons embed interactive
```plot blocks for quantitative ideas and ```mermaid diagrams for pipelines and
processes.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


_BASICS = SeedCourse(
    slug="reproducible-research-basics",
    title="Reproducible Research & Scientific Software — Basics",
    description=(
        "Why computational results so often fail to reproduce, and the foundational "
        "habits that fix it: version control with Git, a clean project structure, "
        "literate notebooks, recording dependencies, and managing data and licences."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The reproducibility crisis",
            "10 min",
            r"""
# The reproducibility crisis

A result is **reproducible** if someone else (or future you) can re-run your
code on your data and obtain the *same* numbers. Surveys — including the 2016
*Nature* poll of 1,576 researchers — found that over 70% had failed to
reproduce another scientist's experiments, and more than half could not
reproduce their own. In computation the leading causes are mundane: lost
scripts, undocumented manual steps, uncontrolled software versions, and data
that drifts.

A useful ladder of goals:

```mermaid
flowchart LR
  A[Reproducible: same data + same code -> same result] --> B[Replicable: new data + same method -> consistent result]
  B --> C[Reusable: others can adapt your code and data]
```

The payoff compounds: as the share of analysis steps you automate rises, the
fraction you can faithfully re-run climbs toward 1.

```plot
{"title": "Reproducibility vs. automation", "xLabel": "Steps automated (fraction)", "yLabel": "Reproducible result probability", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+0.15)", "label": "P(reproduce)", "color": "#2563eb"}]}
```

Reproducibility is not perfectionism — it is the minimum standard that lets
science self-correct.

**Next:** version control with Git.
""",
        ),
        _t(
            "Version control with Git",
            "11 min",
            r"""
# Version control with Git

**Git** records snapshots (commits) of your project, so every result is tied to
an exact state of the code. No more `analysis_final_v3_REALLY_final.R`.

```bash
git init
git add analysis.py data/clean.csv
git commit -m "Add cleaning + first regression"
git log --oneline          # the history of snapshots
git diff HEAD~1            # what changed since the last commit
```

Each commit has a unique **SHA-1 hash** (e.g. `a1b9f2c`) you can cite in a
paper — `git checkout a1b9f2c` restores exactly the code that produced a figure.

```mermaid
flowchart LR
  W[Working directory] -->|git add| S[Staging area]
  S -->|git commit| R[Local repository]
  R -->|git push| H[Remote: GitHub/GitLab]
```

Commit **early and often**, with messages that explain *why*. Commit source
code, scripts and small text data; do **not** commit large binaries, secrets,
or generated outputs — those go in `.gitignore`.

```
# .gitignore
__pycache__/
*.RData
results/figures/
.env
```

A clean history is itself documentation: `git log` becomes a lab notebook of
your analysis.

**Next:** structuring a project so others (and tools) can find their way.
""",
        ),
        _t(
            "Project structure",
            "10 min",
            r"""
# Project structure

A predictable layout lets a newcomer — or an automated pipeline — locate code,
data and outputs without guessing. The widely used *Noble (2009)* and
*Cookiecutter Data Science* conventions converge on a few directories:

```mermaid
flowchart TB
  P[project/] --> D[data/raw -> read-only]
  P --> Dp[data/processed -> generated]
  P --> S[src/ -> reusable code]
  P --> N[notebooks/ -> exploration]
  P --> R[results/ -> figures, tables]
  P --> E[environment.yml / requirements.txt]
  P --> Rd[README.md + LICENSE]
```

Three rules carry most of the value:

- **Raw data is sacred and read-only.** Never edit `data/raw/`; every
  transformation writes to `data/processed/` via a script, so the path from raw
  to result is fully traceable.
- **Separate code from outputs.** Anything in `results/` should be *re-creatable*
  by running the code — so it can be safely git-ignored and regenerated.
- **One command to rebuild.** A `Makefile` or `run_all.sh` that turns raw data
  into every figure is the single best reproducibility investment.

A good `README.md` states what the project does, how to install dependencies,
and the one command that reproduces the results.

**Next:** notebooks and literate programming.
""",
        ),
        _t(
            "Literate programming & notebooks",
            "10 min",
            r"""
# Literate programming & notebooks

Donald Knuth's **literate programming** interleaves prose, code and output so a
human can read the *argument* and a machine can run it. Modern tools — Jupyter,
R Markdown, Quarto — embody this: narrative, the code that produced a figure,
and the figure itself live in one document.

```mermaid
flowchart LR
  T[Text: explanation] --> C[Code cell]
  C --> O[Output: figure / table]
  O --> T2[Text: interpretation]
```

The danger is **hidden state**: cells run out of order leave variables that
won't exist on a fresh start. The fix is simple and non-negotiable —
*Restart kernel & Run All* before you trust a notebook, and before you commit:

```bash
jupyter nbconvert --to notebook --execute analysis.ipynb
# or, for Quarto:
quarto render report.qmd
```

Because `.ipynb` files store outputs as JSON, they create noisy Git diffs. Strip
outputs before committing (e.g. with `nbstripout`) or keep the heavy analysis in
plain `.py`/`.R` scripts and reserve notebooks for the readable report.

The guiding rule: a notebook should run **top to bottom on a clean kernel** and
give identical results every time.

**Next:** capturing the software environment your code needs.
""",
        ),
        _t(
            "Tracking dependencies",
            "10 min",
            r"""
# Tracking dependencies

Code that "worked last year" usually fails because a dependency changed. Pin the
*exact* versions so the same software stack rebuilds anywhere.

In Python, an environment file or lock file records names **and** versions:

```text
# requirements.txt (pinned)
numpy==1.26.4
pandas==2.2.2
scikit-learn==1.5.0
```

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt      # snapshot the resolved versions
```

The hazard is **silent version drift** — an unpinned `numpy` resolves to
whatever is newest, and the probability that *all* dependencies still match
falls fast as the number of loose packages grows.

```plot
{"title": "Drift risk vs. number of unpinned packages", "xLabel": "Unpinned packages", "yLabel": "P(environment still matches)", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "P(match)", "color": "#dc2626"}]}
```

Conda's `environment.yml`, R's **renv**, and language-native lock files
(`poetry.lock`, `uv.lock`) all serve the same goal. Commit the lock file so the
environment is part of the version-controlled record.

**Next:** data management and licences.
""",
        ),
        _t(
            "Data management & licensing",
            "9 min",
            r"""
# Data management & licensing

Code is only half of a result — the **data** must be findable, intact and
legally reusable. Three habits matter.

**Integrity by checksum.** A cryptographic hash detects silent corruption: if
even one byte changes, the digest changes completely.

```bash
sha256sum data/raw/measurements.csv > data/raw/measurements.csv.sha256
sha256sum -c data/raw/measurements.csv.sha256   # verify later
```

**A persistent identifier.** Deposit datasets in an archive (Zenodo, Dryad,
Figshare) that mints a **DOI** — a stable citation that won't rot like a URL.

```mermaid
flowchart LR
  C[Collect data] --> V[Validate + checksum]
  V --> A[Archive: Zenodo/Dryad]
  A --> DOI[Mint DOI]
  DOI --> Cite[Cite in paper]
```

**A licence.** Without one, code and data are "all rights reserved" and nobody
may legally reuse them. Use a recognised licence: **MIT/BSD/Apache-2.0** for
code, **CC0 or CC BY** for data. A `LICENSE` file in the repo makes the terms
machine-readable and unambiguous.

Together, version control + pinned environment + archived, licensed data form
the reproducible package that a reader needs.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_INTERMEDIATE = SeedCourse(
    slug="reproducible-research-intermediate",
    title="Reproducible Research & Scientific Software — Intermediate",
    description=(
        "Engineering practices that make scientific software trustworthy: Git "
        "branching and collaboration, automated testing, build automation with Make "
        "and Snakemake, continuous integration, and random-seed determinism."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Branching & collaboration",
            "11 min",
            r"""
# Branching & collaboration

A **branch** is a movable pointer that lets you develop a feature without
disturbing the working `main`. Merging brings the work back together with a full
record of who changed what.

```mermaid
flowchart LR
  M1[main] --> M2[main]
  M1 --> F1[feature: new model]
  F1 --> F2[feature: tests]
  F2 --> PR[Pull request review]
  PR --> M3[merge into main]
  M2 --> M3
```

```bash
git switch -c feature/bootstrap-ci
# ...edit, commit...
git push -u origin feature/bootstrap-ci
# open a Pull Request; a reviewer comments and approves
```

A **Pull/Merge Request** is the unit of peer review for code: a colleague reads
the diff, runs the tests, and approves before it reaches `main`. Keep branches
small and short-lived to avoid painful merge conflicts.

When two people edit the same lines, Git reports a **conflict** and marks both
versions (`<<<<<<<`, `=======`, `>>>>>>>`); you resolve by choosing or combining
them, then committing. Use **tags** (`git tag v1.0.0`) to mark the exact commit
behind a published result, so reviewers can fetch precisely that state.

**Next:** automated testing for scientific code.
""",
        ),
        _t(
            "Automated testing",
            "11 min",
            r"""
# Automated testing

Scientific bugs are quiet — a wrong sign or off-by-one still produces plausible
numbers. **Automated tests** encode expected behaviour so regressions are caught
the moment they appear.

```python
# test_stats.py  (pytest)
import numpy as np
from mystats import zscore

def test_zscore_mean_is_zero():
    x = np.array([2.0, 4.0, 4.0, 4.0, 6.0])
    assert np.isclose(zscore(x).mean(), 0.0)

def test_zscore_unit_std():
    x = np.random.default_rng(0).normal(size=1000)
    assert np.isclose(zscore(x).std(), 1.0, atol=1e-2)
```

```bash
pytest -q            # discovers and runs every test_*.py
```

Useful test types for research code:

- **Unit tests** check one function against known inputs/outputs.
- **Property tests** assert invariants ("a normalised vector has norm 1") over
  many random inputs (Hypothesis).
- **Regression tests** lock in a previously correct numeric result.

Test value rises sharply with even modest coverage, then sees diminishing
returns near 100% — aim for the parts where a bug would corrupt a result.

```plot
{"title": "Bugs caught vs. test coverage", "xLabel": "Coverage (fraction)", "yLabel": "Bugs caught (fraction)", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(0.3/x)^2)", "label": "caught", "color": "#16a34a"}]}
```

**Next:** turning many steps into one reproducible build.
""",
        ),
        _t(
            "Build automation with Make",
            "10 min",
            r"""
# Build automation with Make

Manual, remembered steps are the enemy of reproducibility. **GNU Make** encodes
the dependency graph between files: a *target* is rebuilt only when a *
prerequisite* is newer, so `make` always produces an up-to-date result from the
minimum work.

```makefile
results/figure1.png: src/plot.py data/processed/clean.csv
	python src/plot.py

data/processed/clean.csv: src/clean.py data/raw/measurements.csv
	python src/clean.py

all: results/figure1.png
```

```bash
make all      # builds clean.csv (if stale) then figure1.png
```

Make reads this as a graph and rebuilds in the correct order:

```mermaid
flowchart LR
  R[data/raw/measurements.csv] --> C[src/clean.py]
  C --> P[data/processed/clean.csv]
  P --> Pl[src/plot.py]
  Pl --> F[results/figure1.png]
```

Because the recipe is the *single source of truth* for "how to rebuild
everything", `make all` on a fresh clone regenerates every output deterministi-
cally. This one file converts a pile of scripts into a pipeline.

**Next:** scaling pipelines with Snakemake.
""",
        ),
        _t(
            "Workflow management with Snakemake",
            "11 min",
            r"""
# Workflow management with Snakemake

Make struggles with many similar files and clusters. **Snakemake** (Python-
based, *Köster & Rahmann, 2012*) generalises it: rules use **wildcards** to
process many samples and can run on a cluster or cloud.

```python
SAMPLES = ["s1", "s2", "s3"]

rule all:
    input: expand("results/{s}.txt", s=SAMPLES)

rule analyse:
    input:  "data/{s}.fastq"
    output: "results/{s}.txt"
    threads: 4
    shell:  "analyse --in {input} --out {output} -t {threads}"
```

Snakemake builds a **directed acyclic graph (DAG)** of jobs, runs independent
branches in parallel, and re-executes only what is out of date:

```mermaid
flowchart LR
  D1[data/s1.fastq] --> A1[analyse s1] --> R1[results/s1.txt]
  D2[data/s2.fastq] --> A2[analyse s2] --> R2[results/s2.txt]
  R1 --> Agg[rule all]
  R2 --> Agg
```

```bash
snakemake -n              # dry run: show the plan
snakemake --cores 8       # execute, 8 cores
```

Each rule can declare its own **conda environment** or **container**, so the
whole multi-step analysis is portable and reproducible. **Nextflow** offers a
similar dataflow model favoured in genomics (nf-core).

**Next:** continuous integration.
""",
        ),
        _t(
            "Continuous integration",
            "10 min",
            r"""
# Continuous integration

**Continuous Integration (CI)** runs your tests automatically on every push, in
a clean environment, so "it works on my machine" never reaches collaborators.

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: pytest --cov=src
```

The loop is short and unforgiving — a broken commit fails within minutes, before
it can spread:

```mermaid
flowchart LR
  Push[git push] --> Trig[CI triggered]
  Trig --> Env[Fresh environment]
  Env --> Inst[Install pinned deps]
  Inst --> Test[Run tests + lint]
  Test -->|pass| Green[Merge allowed]
  Test -->|fail| Red[Block + notify]
```

CI also **re-installs your pinned dependencies from scratch every time**, so it
silently verifies that your environment file is complete and reproducible — a
free check on the work from the Basics course. Add linting (`ruff`), type
checks, and even a full pipeline run on a small sample for stronger guarantees.

**Next:** randomness, seeds and determinism.
""",
        ),
        _t(
            "Random seeds & determinism",
            "10 min",
            r"""
# Random seeds & determinism

Any method using randomness — bootstrapping, cross-validation splits, stochastic
gradient descent, MCMC — gives different numbers on each run unless you fix the
**seed** of the pseudo-random number generator (PRNG). A PRNG is deterministic:
the same seed yields the same stream.

```python
import numpy as np
rng = np.random.default_rng(42)   # explicit, reproducible generator
sample = rng.normal(size=1000)
```

Prefer an **explicit generator object** over the global `np.random.seed` — the
global state leaks between modules and is hard to reason about. For full
determinism set every relevant seed (Python `random`, NumPy, and the framework,
e.g. `torch.manual_seed`).

A subtler trap is **parallelism**: results that depend on the order threads
finish are non-deterministic even with a fixed seed. The mismatch between runs
grows with the number of uncontrolled stochastic sources.

```plot
{"title": "Run-to-run variance vs. uncontrolled seeds", "xLabel": "Uncontrolled random sources", "yLabel": "Relative variance between runs", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "variance", "color": "#dc2626"}]}
```

Report the seed(s) alongside results, and confirm a fresh clone with the same
seed reproduces your numbers exactly.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_ADVANCED = SeedCourse(
    slug="reproducible-research-advanced",
    title="Reproducible Research & Scientific Software — Advanced",
    description=(
        "State-of-the-art reproducibility: containers and Docker, fully captured "
        "environments with Nix and lock files, the FAIR principles, computational "
        "provenance, reproducibility for machine learning, and open-science "
        "publishing."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Containers for reproducibility",
            "11 min",
            r"""
# Containers for reproducibility

Pinned packages still sit on *your* operating system, with *your* system
libraries. A **container** packages the application together with its entire
user-space environment, so it runs identically on a laptop, an HPC node, or the
cloud.

```dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /work/src/
WORKDIR /work
ENTRYPOINT ["python", "src/run.py"]
```

```bash
docker build -t myanalysis:1.0 .
docker run --rm -v "$PWD/data:/work/data" myanalysis:1.0
```

```mermaid
flowchart TB
  Host[Host OS + kernel] --> Eng[Container runtime]
  Eng --> Img[Image: OS libs + Python + deps + code]
  Img --> Run[Identical container anywhere]
```

For shared HPC clusters where users lack root, **Apptainer/Singularity** runs
the *same* image without a privileged daemon and can convert Docker images
directly. Pin the base image by **digest** (`python:3.12-slim@sha256:...`), not a
moving tag, and archive the image (or its `Dockerfile` + lock file) so the
environment is itself reproducible years later.

**Next:** fully reproducible environments with Nix and lock files.
""",
        ),
        _t(
            "Reproducible environments with Nix",
            "10 min",
            r"""
# Reproducible environments with Nix

A `Dockerfile` that runs `apt-get install` is only as reproducible as the
upstream repositories on build day. **Nix** goes further: it builds every
dependency from a pinned set of sources, identified by content hash, into an
isolated store — so the *same* inputs always yield a **bit-for-bit identical**
environment.

```nix
# flake.nix (excerpt)
{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  outputs = { nixpkgs, ... }: {
    devShells.default = nixpkgs.legacyPackages.x86_64-linux.mkShell {
      packages = [ python312 python312Packages.numpy python312Packages.pandas ];
    };
  };
}
```

The committed `flake.lock` pins the exact revision of *all* sources, the key to
reproducibility:

```mermaid
flowchart LR
  Lock[flake.lock pins inputs] --> Build[Build from content-hashed sources]
  Build --> Store[/nix/store/hash-pkg/]
  Store --> Same[Identical env on any machine]
```

The broader idea is **lock files everywhere**: `uv.lock`, `poetry.lock`,
`renv.lock`, `conda-lock` and `flake.lock` all record a fully *resolved*
dependency graph, not just top-level requests. A lock file plus a container or
Nix flake is today's gold standard for a portable scientific environment.

**Next:** FAIR data principles.
""",
        ),
        _t(
            "FAIR principles & open science",
            "11 min",
            r"""
# FAIR principles & open science

The **FAIR** principles (*Wilkinson et al., 2016*, *Scientific Data*) define
what makes data and software genuinely reusable — by machines as well as people:

```mermaid
flowchart TB
  F[Findable: persistent ID + rich metadata] --> A[Accessible: open protocol, metadata persists]
  A --> I[Interoperable: shared vocabularies, standard formats]
  I --> R[Reusable: clear licence + provenance]
```

- **Findable** — a DOI and indexed metadata so the object can be located.
- **Accessible** — retrievable by a standard, open protocol (HTTP, with
  authentication where needed); metadata stays available even if the data is
  restricted.
- **Interoperable** — uses community standards and controlled vocabularies/
  ontologies, so different datasets combine.
- **Reusable** — a clear licence, detailed provenance, and domain-relevant
  metadata.

FAIR is **not** the same as "open": sensitive data can be FAIR while access is
controlled. The principles also apply to **software** (FAIR4RS): cite code with
a DOI (Zenodo's GitHub integration mints one per release), include a
`CITATION.cff` file, and version it semantically. Funders and journals
increasingly *require* FAIR data and software, making these skills directly
career-relevant.

**Next:** capturing computational provenance.
""",
        ),
        _t(
            "Computational provenance",
            "10 min",
            r"""
# Computational provenance

**Provenance** is the recorded lineage of a result: which inputs, which code
version, which parameters and environment produced *this* figure. Reproducibility
asks "can I get the same answer again?"; provenance answers "how exactly was this
answer made?".

```mermaid
flowchart LR
  In[Input data + hash] --> Run[Run: code SHA + params + env]
  Run --> Out[Output + metadata]
  Out --> Prov[Provenance record: who, what, when, how]
```

Levels of capture, from light to complete:

- **Manual** — log the Git commit, seed and parameters in the output's metadata
  or filename.
- **Workflow-native** — Snakemake/Nextflow write reports and a DAG; tools like
  **MLflow** or **Weights & Biases** log every run's params, metrics and
  artifacts automatically.
- **System-level** — frameworks such as **ReproZip** or **CWL** capture the
  exact files and commands a run touched, packing them into a re-runnable
  bundle.

The W3C **PROV** model gives a standard vocabulary (Entity, Activity, Agent) for
expressing this lineage so it is machine-readable and queryable. Good provenance
turns a static result into one you can interrogate, audit and trust.

**Next:** reproducibility for machine learning.
""",
        ),
        _t(
            "Reproducible machine learning",
            "11 min",
            r"""
# Reproducible machine learning

ML adds reproducibility hazards beyond ordinary code: large evolving datasets,
stochastic training, GPU non-determinism, and dozens of hyperparameters. A
reproducible ML project versions **all four** of code, data, environment and
the trained model.

```mermaid
flowchart LR
  Code[Code: Git] --> Exp[Experiment run]
  Data[Data: DVC + hash] --> Exp
  Cfg[Config: params.yaml + seed] --> Exp
  Env[Env: container/lock] --> Exp
  Exp --> Track[Track: MLflow run + metrics]
  Track --> Model[Versioned model + provenance]
```

Key tools and habits:

- **DVC (Data Version Control)** stores large data/models in remote storage
  while Git tracks lightweight pointers — so `git checkout` restores the matching
  data *and* model.
- **Experiment tracking** (MLflow, W&B) logs params, metrics, the Git SHA and
  artifacts for every run, making results comparable and auditable.
- **Determinism**: fix all seeds and enable deterministic kernels
  (`torch.use_deterministic_algorithms(True)`), accepting some speed cost.

Even with care, run-to-run accuracy varies; its spread shrinks roughly as
$1/\sqrt{n}$ as you average over $n$ seeds, which is why papers should report
mean ± std over several runs, not a single best number.

```plot
{"title": "Reported accuracy spread vs. number of seeds", "xLabel": "Number of seeds averaged", "yLabel": "Std of mean accuracy", "xRange": [1, 25], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "std of mean", "color": "#2563eb"}]}
```

**Next:** publishing reproducible, open research.
""",
        ),
        _t(
            "Publishing reproducible research",
            "10 min",
            r"""
# Publishing reproducible research

The final step is packaging everything so a reader can rebuild your results from
scratch. A modern **reproducibility bundle** ties the threads of this track
together.

```mermaid
flowchart TB
  Repo[Git repo: code + workflow] --> DOI[Archived release: Zenodo DOI]
  Env[Container / Nix / lock file] --> DOI
  DataDOI[Archived data: DOI] --> DOI
  DOI --> Paper[Paper: cites all DOIs + commit]
  Paper --> Reader[Reader rebuilds with one command]
```

Practical components:

- **A one-command rebuild** — Make/Snakemake/Nextflow that regenerates every
  figure and table, run inside the archived container.
- **Persistent identifiers** for code (Zenodo release DOI), data (repository
  DOI) and the paper, cross-linked so each points to the others.
- **Executable artifacts** — Binder, CodeOcean "compute capsules", or Quarto
  manuscripts let reviewers re-run the analysis in the browser without local
  setup.
- **Open licences and preprints** — deposit a preprint (bioRxiv/arXiv) and pick
  an OSI/Creative-Commons licence so others may legally build on the work.

Reproducibility is not an afterthought you add at submission; it is the way you
work throughout — version control, environments, tests, workflows and
provenance — so that publishing it is the easy last step.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

REPRODUCIBLE_RESEARCH_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["REPRODUCIBLE_RESEARCH_COURSES"]
