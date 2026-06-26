"""Scientific Computing & Linux track: Basics -> Intermediate -> Advanced.

From the shell, files and SSH, through environments, scripting and version
control, up to reproducible Snakemake/Nextflow pipelines, Slurm HPC clusters
and containers for bioinformatics. Lessons embed interactive ```plot blocks for
quantitative ideas (scaling, speedup, growth/decay) and ```mermaid diagrams for
filesystems, pipelines and scheduler workflows.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


_BASICS = SeedCourse(
    slug="scientific-computing-basics",
    title="Scientific Computing & Linux — Basics",
    description=(
        "Get productive on the command line: the Unix filesystem, navigating and "
        "manipulating files, the permissions model, text-processing pipes, and "
        "logging into remote servers over SSH. The foundation every "
        "bioinformatician and computational scientist stands on."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why Linux and the shell for science",
            "9 min",
            r"""# Why Linux and the shell for science

Almost all serious scientific computing runs on **Linux**: HPC clusters,
cloud instances, sequencing-core servers, and the tools of bioinformatics
(`bwa`, `samtools`, `GATK`, `bcftools`) are built for it. The **shell** — most
commonly **Bash** — is a text interface where you type commands and the kernel
runs them. Unlike clicking through a GUI, every shell action is a line of text:
it can be saved, shared, version-controlled, and re-run identically. That is the
seed of **reproducibility**.

The Unix philosophy is *small programs that do one thing well, joined together*.
You rarely use one giant tool; you compose `grep`, `sort`, `cut`, and `awk` into
a pipeline that solves your exact problem.

A command has three parts: the program, its options (flags), and arguments:

```bash
ls -l -h /data/genomes
# program: ls   flags: -l (long) -h (human-readable)   argument: a path
```

Use `man ls` to read any command's manual, or `ls --help` for a quick summary.

```mermaid
flowchart LR
    U[You type a command] --> S[Bash shell parses it]
    S --> K[Linux kernel executes]
    K --> O[Output to terminal]
    O --> U
```

**Next:** navigating the filesystem tree.
""",
        ),
        _t(
            "The filesystem and navigation",
            "10 min",
            r"""# The filesystem and navigation

Linux organises everything under a single **root** `/` — there are no drive
letters. Paths are either **absolute** (start at `/`, e.g. `/home/ana/data`) or
**relative** to your current directory. Key shortcuts: `.` is here, `..` is the
parent, `~` is your home directory.

The core navigation commands:

```bash
pwd                 # print working directory (where am I?)
ls -lah             # list, long + all + human sizes
cd /data/project    # change directory (absolute)
cd ../results       # relative: up one, into results
cd                  # with no argument, go home (~)
```

A typical scientific layout keeps data, code and results separate:

```mermaid
flowchart TB
    root["/"] --> home["/home/ana"]
    home --> proj["project/"]
    proj --> data["data/  (raw reads)"]
    proj --> scripts["scripts/  (code)"]
    proj --> results["results/  (outputs)"]
```

**Everything is a file** in Unix — even directories and devices. That uniformity
is what lets the same handful of commands manipulate genomes, configs, and
hardware. Tab-completion (press Tab) finishes file names and saves typing and
typos; the up-arrow recalls previous commands.

**Next:** creating, copying and removing files safely.
""",
        ),
        _t(
            "Files: create, copy, move, remove",
            "9 min",
            r"""# Files: create, copy, move, remove

You will constantly reshape your working tree. The essential verbs:

```bash
mkdir -p results/qc      # make directories, -p creates parents as needed
touch notes.txt          # create an empty file / update its timestamp
cp reads.fq backup.fq    # copy; cp -r for whole directories
mv old.txt new.txt       # move OR rename (same operation)
rm temp.txt              # remove a file
rm -r scratch/           # remove a directory and its contents
```

**`rm` is permanent** — there is no recycle bin. A misplaced space, like
`rm -r /  home` instead of `/home`, is catastrophic. Defensive habits: run
`ls` on a glob before `rm` it, and use `rm -i` for interactive confirmation.

Wildcards (globs) let one command act on many files. `*` matches any string,
`?` one character, `[12]` a set:

```bash
ls *.fastq.gz            # all gzipped FASTQ files
cp sample_?.txt backup/  # sample_1.txt, sample_2.txt, ...
```

View files without an editor: `cat` dumps the whole file, `less` pages through
it (`q` to quit), `head -n 20` and `tail -n 20` show the first/last lines —
indispensable for peeking at huge sequencing files.

```mermaid
flowchart LR
    mk[mkdir] --> to[touch / edit]
    to --> cp[cp / mv]
    cp --> rm[rm]
```

**Next:** who can read and run what — permissions.
""",
        ),
        _t(
            "Permissions and ownership",
            "10 min",
            r"""# Permissions and ownership

Linux is multi-user, so every file carries an **owner**, a **group**, and a set
of permissions. `ls -l` shows them:

```
-rwxr-xr--  1 ana lab  4096 run.sh
 │└┬┘└┬┘└┬┘    │   │
 │ u  g  o    owner group
 type
```

Three permission classes — **u**ser (owner), **g**roup, **o**thers — each with
**r**ead, **w**rite, **x**ecute bits. For a *file*, `x` means runnable; for a
*directory*, `x` means you may enter it. Each bit is a value — r=4, w=2, x=1 —
so a class digit is their sum: `7 = rwx`, `5 = r-x`, `0 = ---`.

```bash
chmod 755 run.sh    # rwx for owner, r-x for group and others
chmod +x script.sh  # add execute for everyone
chmod u+w,o-r data  # symbolic: owner gains write, others lose read
chown ana:lab file  # change owner and group (often needs sudo)
```

To run your own script: `chmod +x analysis.sh` then `./analysis.sh`. Sensitive
files (an SSH private key) demand `chmod 600` — owner read/write only — or the
SSH client will refuse to use them.

```mermaid
flowchart LR
    F[File] --> U["user (owner): rwx"]
    F --> G["group: r-x"]
    F --> O["others: r--"]
```

**Next:** pipes that build powerful one-liners.
""",
        ),
        _t(
            "Pipes, redirection and text tools",
            "11 min",
            r"""# Pipes, redirection and text tools

The shell's superpower is **composition**. Every program reads from *standard
input* (stdin) and writes to *standard output* (stdout) and *standard error*
(stderr). A **pipe** `|` feeds one program's stdout into the next's stdin;
**redirection** sends streams to files.

```bash
command > out.txt     # stdout to a file (overwrite)
command >> out.txt    # stdout appended
command 2> err.log    # stderr to a file
command < in.txt      # read stdin from a file
```

The classic text toolkit:

- `grep PATTERN file` — keep lines matching a (regex) pattern.
- `cut -f2 -d','` — extract column 2 of a comma-separated file.
- `sort` / `uniq -c` — order lines / count unique occurrences.
- `wc -l` — count lines.
- `awk '{print $1, $3}'` — field-aware mini-language.

A real bioinformatics one-liner: count how many reads map to each chromosome:

```bash
samtools view aln.bam | cut -f3 | sort | uniq -c | sort -rn
```

Each stage is simple; the **pipeline** is expressive. Pipes also matter for
performance: data streams through memory rather than writing huge intermediate
files. The data flows left to right:

```mermaid
flowchart LR
    A[samtools view] -->|stdout| B[cut -f3]
    B -->|stdout| C[sort]
    C -->|stdout| D[uniq -c]
    D --> E[sort -rn]
```

**Next:** reaching remote servers over SSH.
""",
        ),
        _t(
            "Remote servers with SSH and scp",
            "10 min",
            r"""# Remote servers with SSH and scp

Your data and compute usually live on a **remote server** — a cluster login node
or a cloud VM. **SSH** (Secure Shell) gives you an encrypted terminal on that
machine:

```bash
ssh ana@cluster.uni.edu        # log in, prompts for a password
ssh -p 2222 ana@host           # non-default port
```

Typing a password every time is slow and weak. Use **key-based auth**: generate
a keypair, keep the **private** key secret on your laptop, and copy the
**public** key to the server.

```bash
ssh-keygen -t ed25519          # creates ~/.ssh/id_ed25519(.pub)
ssh-copy-id ana@cluster.uni.edu  # installs your public key there
```

Now SSH logs you in with no password, and tools like `git` and `rsync` work
seamlessly. Move files with `scp` (copy) or `rsync` (efficient, resumable sync):

```bash
scp results.csv ana@host:/data/   # local -> remote
rsync -avP big_dir/ ana@host:/data/big_dir/   # mirror, show progress
```

Run long jobs that survive a disconnect with `tmux` or `screen`, or submit them
to the cluster's scheduler (covered later).

```mermaid
flowchart LR
    L[Laptop: private key] -->|encrypted SSH| S[Server: public key]
    L -.scp / rsync.-> S
```

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


_INTERMEDIATE = SeedCourse(
    slug="scientific-computing-intermediate",
    title="Scientific Computing & Linux — Intermediate",
    description=(
        "Turn ad-hoc commands into reliable software: Bash scripting, reproducible "
        "Python environments with conda and virtualenv, Git version control, "
        "process and resource management, and the package/build tooling that makes "
        "an analysis re-runnable by anyone."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Bash scripting fundamentals",
            "11 min",
            r"""# Bash scripting fundamentals

A **script** is a file of shell commands run as a unit — the bridge from typing
commands to automating them. Start every script with a **shebang** naming the
interpreter, and make it executable:

```bash
#!/usr/bin/env bash
set -euo pipefail        # fail fast: error, undefined var, pipe error
echo "Processing $1"     # $1 is the first argument
```

`set -euo pipefail` is the single most important habit: without it a script
keeps running after a failed command and can silently corrupt results.

Variables, conditionals and loops:

```bash
SAMPLES="A B C"
for s in $SAMPLES; do
    if [[ -f "reads_$s.fq" ]]; then
        echo "Aligning $s"
        bwa mem ref.fa "reads_$s.fq" > "aln_$s.sam"
    fi
done
```

Always **quote** variables (`"$s"`) so spaces in filenames don't split into
multiple arguments — a notorious source of bugs. Each command sets an **exit
status**: `0` means success, non-zero means failure, available as `$?` and used
by `if` and `&&`/`||`.

```mermaid
flowchart TB
    A["#!/usr/bin/env bash"] --> B["set -euo pipefail"]
    B --> C[read inputs / args]
    C --> D{loop over samples}
    D --> E[run tool]
    E --> F[write outputs]
```

**Next:** isolating dependencies with environments.
""",
        ),
        _t(
            "Reproducible environments: conda and venv",
            "11 min",
            r"""# Reproducible environments: conda and venv

"It works on my machine" is the enemy of science. Different versions of Python,
NumPy, or `samtools` give different numbers. **Environments** isolate a project's
exact dependencies so it runs identically elsewhere.

Python's built-in **virtualenv** handles pure-Python packages:

```bash
python -m venv .venv
source .venv/bin/activate
pip install numpy==1.26 pandas==2.2
pip freeze > requirements.txt   # pin exact versions
```

For bioinformatics, **conda** (via the fast `mamba`, with the **bioconda**
channel) is dominant because it installs non-Python tools and their C libraries
too:

```bash
conda create -n align -c bioconda -c conda-forge bwa samtools=1.20
conda activate align
conda env export > environment.yml   # full, reproducible spec
```

Sharing `environment.yml` or `requirements.txt` lets a collaborator recreate
your exact stack. The growth of dependency conflicts as a project ages is real —
pinning versions tames it. As a project accumulates packages, the chance of a
clash without pinning rises sharply.

```plot
{"title": "Risk of version conflicts vs unpinned dependencies", "xLabel": "number of unpinned packages", "yLabel": "conflict probability", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "P(conflict)", "color": "#dc2626"}]}
```

**Next:** versioning your code with Git.
""",
        ),
        _t(
            "Version control with Git",
            "11 min",
            r"""# Version control with Git

Scripts and analyses evolve; **Git** records every version so you can see what
changed, when, and why — and recover anything. A Git repository tracks
**snapshots** (commits), each pointing to its parent, forming a history graph.

The core daily loop:

```bash
git init                      # start tracking this folder
git add analysis.py           # stage a change for the next snapshot
git commit -m "Add QC step"   # record it with a message
git log --oneline             # browse history
```

**Branches** let you develop a feature or try an idea without disturbing the
working version; **merging** brings it back:

```bash
git switch -c feature/trim    # create and move to a branch
# ... edit, commit ...
git switch main
git merge feature/trim        # integrate the work
```

Collaborate through a **remote** (GitHub, GitLab): `git push` uploads commits,
`git pull` fetches and integrates others' work. A good `.gitignore` keeps large
data and generated outputs out of the repo — version the **code**, not the
gigabytes.

```mermaid
flowchart LR
    A[main] --> B[commit]
    B --> C[commit]
    C -->|switch -c| D[feature]
    D --> E[commit]
    E -->|merge| C
```

**Next:** managing running processes.
""",
        ),
        _t(
            "Processes, jobs and resource monitoring",
            "10 min",
            r"""# Processes, jobs and resource monitoring

Every running program is a **process** with a numeric PID. Long analyses must be
launched, watched, and sometimes stopped — without monitoring you cannot tell if
a job is working or thrashing.

```bash
ps aux | grep bwa     # find a process and its PID
top      # or htop     live view of CPU/memory per process
kill 1234             # ask process 1234 to stop (SIGTERM)
kill -9 1234          # force it (SIGKILL) as a last resort
```

Control jobs from the shell itself:

```bash
long_job.sh &         # run in the background
jobs                  # list background jobs
fg %1                 # bring job 1 to the foreground
nohup long_job.sh &   # keep running after you log out
```

Watch resources so you size jobs correctly: `free -h` (memory), `df -h` (disk),
`du -sh dir/` (a directory's size). Memory matters most in bioinformatics — a
genome assembler can need hundreds of GB; exceeding RAM triggers the kernel's
**OOM killer**. Runtime usually grows with input size, often super-linearly for
alignment and assembly:

```plot
{"title": "Job runtime vs input size", "xLabel": "input size (GB)", "yLabel": "runtime (hours)", "xRange": [0, 10], "yRange": [0, 8], "grid": true, "functions": [{"expr": "0.05*x^2", "label": "O(n^2) alignment", "color": "#2563eb"}, {"expr": "0.3*x", "label": "O(n) streaming", "color": "#16a34a"}]}
```

**Next:** scheduling and automating work.
""",
        ),
        _t(
            "Scheduling and automation with cron",
            "9 min",
            r"""# Scheduling and automation with cron

Routine tasks — nightly backups, weekly database refreshes, periodic QC — should
run themselves. **cron** is the Unix time-based scheduler. You edit your
schedule with `crontab -e`; each line is five time fields plus a command:

```
┌ minute (0-59)
│ ┌ hour (0-23)
│ │ ┌ day of month (1-31)
│ │ │ ┌ month (1-12)
│ │ │ │ ┌ day of week (0-6, Sun=0)
│ │ │ │ │
0 2 * * *  /home/ana/backup.sh    # every day at 02:00
0 3 * * 1  /home/ana/weekly_qc.sh # 03:00 every Monday
*/15 * * * * /home/ana/poll.sh    # every 15 minutes
```

Cron jobs run with a **minimal environment** — no `conda activate`, a bare
`PATH`. Scripts must therefore use absolute paths and activate their own
environment explicitly, and should redirect output to a log so failures are
visible:

```bash
0 2 * * * /home/ana/backup.sh >> /home/ana/logs/backup.log 2>&1
```

For one-off "run this at 3pm" use `at`; for system services, `systemd` timers.
The big idea: encode the *when* alongside the *what*, so the pipeline keeps
running with no human in the loop.

```mermaid
flowchart LR
    C[cron daemon] -->|checks every minute| T{time matches?}
    T -->|yes| R[run command]
    R --> L[append to log]
    T -->|no| W[wait]
```

**Next:** packaging tools so they install cleanly.
""",
        ),
        _t(
            "Package and build tooling",
            "10 min",
            r"""# Package and build tooling

Reproducibility extends to **how software is built and installed**. Linux
distributions ship system package managers (`apt` on Debian/Ubuntu, `dnf` on
Fedora) that resolve dependencies and install precompiled binaries:

```bash
sudo apt update && sudo apt install build-essential samtools
```

Many scientific tools are distributed as **source** and built with the classic
trio. `make` reads a `Makefile` of *targets*, *prerequisites*, and *recipes*,
rebuilding only what changed — the same dependency-graph idea behind every
modern pipeline:

```bash
./configure --prefix=$HOME/.local   # detect the system, set install path
make -j4                            # compile, 4 parallel jobs
make install                        # place binaries on PATH
```

Modern Python projects declare their build in `pyproject.toml` and install with
`pip install .` or `uv`. The unifying principle is a **declarative spec**: state
*what* you depend on and *what* outputs you need, and let the tool figure out the
order and skip unchanged work.

```mermaid
flowchart LR
    src[source code] --> conf[./configure]
    conf --> mk[make: build only changed targets]
    mk --> inst[make install -> PATH]
    pyproj[pyproject.toml] --> pip[pip install .]
```

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


_ADVANCED = SeedCourse(
    slug="scientific-computing-advanced",
    title="Scientific Computing & Linux — Advanced",
    description=(
        "Scale up and lock down reproducibility: workflow managers (Snakemake, "
        "Nextflow), Slurm on HPC clusters, parallel and distributed computing, "
        "containers (Docker, Singularity/Apptainer) for bioinformatics, and "
        "AI/GPU-accelerated computational methods. The state of the art for "
        "reproducible, large-scale science."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Reproducible pipelines: Snakemake and Nextflow",
            "12 min",
            r"""# Reproducible pipelines: Snakemake and Nextflow

A real analysis is a chain of steps — QC, trim, align, call variants, annotate.
Wiring them with a hand-written Bash script breaks the moment one step fails
halfway. **Workflow managers** model the analysis as a **directed acyclic graph
(DAG)** of rules: each rule declares its inputs, outputs and command, and the
engine computes the order, runs independent steps in parallel, resumes after
failure, and re-runs only what is out of date.

**Snakemake** is Python-flavoured and rule-based:

```python
rule align:
    input:  reads="reads/{sample}.fq", ref="ref.fa"
    output: "aln/{sample}.bam"
    threads: 8
    shell:  "bwa mem -t {threads} {input.ref} {input.reads} | samtools sort -o {output}"
```

The `{sample}` **wildcard** lets one rule fan out over every sample. **Nextflow**
takes a dataflow approach with *channels* and *processes* and excels at running
the same pipeline across laptops, clusters and clouds; **nf-core** curates
community-vetted pipelines.

```mermaid
flowchart LR
    QC[fastqc] --> TRIM[trim]
    TRIM --> ALIGN[bwa mem]
    ALIGN --> SORT[samtools sort]
    SORT --> CALL[variant calling]
    CALL --> ANN[annotate]
```

Because the DAG plus pinned environments fully specify the computation, anyone
can reproduce your results from raw data with one command.

**Next:** submitting work to an HPC scheduler.
""",
        ),
        _t(
            "HPC clusters and the Slurm scheduler",
            "12 min",
            r"""# HPC clusters and the Slurm scheduler

A **High-Performance Computing (HPC)** cluster is hundreds of compute nodes
behind a shared filesystem. You never run heavy work on the **login node**;
instead you submit **batch jobs** to a **scheduler** that queues them and assigns
resources fairly. **Slurm** is the most common scheduler.

A job is a script with `#SBATCH` directives requesting resources:

```bash
#!/bin/bash
#SBATCH --job-name=align
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --array=1-100        # 100 independent tasks (one per sample)

module load samtools
bwa mem -t 8 ref.fa reads_${SLURM_ARRAY_TASK_ID}.fq > out.sam
```

Submit and monitor:

```bash
sbatch job.sh        # queue the job
squeue -u $USER      # see your queued/running jobs
sacct -j 12345       # accounting: CPU/memory actually used
scancel 12345        # cancel a job
```

**Job arrays** are the killer feature for genomics — one submission spawns one
task per sample, all running in parallel. Request honestly: ask for too little
memory and the job is killed; too much and it waits longer in the queue and
wastes the allocation. Throughput scales with the nodes you can grab, up to the
serial fraction (Amdahl's law, next lesson).

```mermaid
flowchart LR
    U[sbatch job.sh] --> Q[Slurm queue]
    Q --> S{scheduler assigns}
    S --> N1[node 1]
    S --> N2[node 2]
    S --> N3[node N]
```

**Next:** how much faster can parallelism actually go?
""",
        ),
        _t(
            "Parallel and distributed computing",
            "12 min",
            r"""# Parallel and distributed computing

Speed comes from doing work **at the same time**. Three levels: **multithreading**
(`-t 8` shares one node's cores and memory), **multiprocessing** (independent
processes, e.g. GNU `parallel` or a job array), and **distributed** computing
(MPI or frameworks like Dask/Spark spanning many nodes).

But speedup is bounded. If a fraction $p$ of the work is parallelisable and
$1-p$ is inherently serial, **Amdahl's law** caps the speedup on $N$ processors:

$$S(N) = \frac{1}{(1-p) + \frac{p}{N}}$$

As $N \to \infty$, $S \to \frac{1}{1-p}$. With 90% parallel work the ceiling is
just 10x, no matter how many cores you throw at it — the serial part dominates.

```plot
{"title": "Amdahl's law: speedup vs processors (p = 0.9)", "xLabel": "processors N", "yLabel": "speedup S(N)", "xRange": [1, 64], "yRange": [0, 11], "grid": true, "functions": [{"expr": "1/(0.1 + 0.9/x)", "label": "S(N), p=0.9", "color": "#2563eb"}, {"expr": "10", "label": "ceiling 1/(1-p)", "color": "#dc2626"}]}
```

Embarrassingly parallel problems (independent per-sample tasks) approach linear
scaling; tightly coupled problems suffer communication overhead. The practical
lesson: profile first, parallelise the bottleneck, and watch for the serial
fraction and I/O — often the true limit on a shared cluster filesystem.

**Next:** packaging the whole environment with containers.
""",
        ),
        _t(
            "Containers for bioinformatics",
            "12 min",
            r"""# Containers for bioinformatics

Conda pins packages, but the OS underneath can still differ. **Containers** go
further: they bundle the application *plus* its entire userspace — libraries,
tools, config — into one image that runs identically anywhere. Unlike a virtual
machine, a container shares the host kernel, so it is lightweight and starts in
seconds.

**Docker** is the standard for building images from a `Dockerfile`:

```dockerfile
FROM mambaorg/micromamba:1.5
RUN micromamba install -y -n base -c bioconda -c conda-forge \
    bwa=0.7.18 samtools=1.20
COPY pipeline.smk /work/
```

On HPC, plain Docker is usually forbidden (it needs root), so clusters use
**Singularity/Apptainer**, which runs as an unprivileged user and reads Docker
images directly:

```bash
apptainer pull docker://quay.io/biocontainers/samtools:1.20
apptainer exec samtools_1.20.sif samtools --version
```

Combine containers with Snakemake/Nextflow and you get the gold standard: each
rule runs in a pinned container, so the pipeline is byte-for-byte reproducible
years later. **BioContainers** publishes a ready image for nearly every
bioinformatics tool.

```mermaid
flowchart LR
    DF[Dockerfile] --> IMG[image: app + libs + OS userspace]
    IMG --> R1[run on laptop]
    IMG --> R2[run on HPC via Apptainer]
    IMG --> R3[run on cloud]
```

**Next:** AI- and GPU-accelerated scientific computing.
""",
        ),
        _t(
            "GPU and AI-accelerated computing",
            "12 min",
            r"""# GPU and AI-accelerated computing

Modern computational science is increasingly **GPU-accelerated** and
**AI-driven**. A GPU runs thousands of simple cores in parallel, ideal for the
dense linear algebra behind deep learning and molecular simulation. On a cluster
you request one explicitly:

```bash
#SBATCH --gres=gpu:1
module load cuda
nvidia-smi          # check the allocated GPU and its memory
```

The landmark example is **AlphaFold2**: a deep neural network that predicts a
protein's 3D structure from its amino-acid sequence to near-experimental
accuracy — a decades-old grand challenge solved with GPUs and learned
representations. Related tools (ESMFold, RoseTTAFold, the AlphaFold3 family)
extend this to complexes and interactions. Across genomics, AI now powers basecalling
(Oxford Nanopore), variant calling (Google's **DeepVariant**, which reframes
calling as image classification), and expression prediction.

Performance follows a learning/scaling pattern: accuracy rises steeply with
model and data scale, then saturates — diminishing returns set in:

```plot
{"title": "Model accuracy vs training scale", "xLabel": "relative compute / data", "yLabel": "accuracy", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "8*x/(2+x)/9", "label": "saturating gains", "color": "#16a34a"}]}
```

Practical workflow: containerise the model, pin GPU/CUDA versions, request the
GPU through Slurm, and wrap it as a workflow rule so an AI step is just another
reproducible node in the pipeline.

```mermaid
flowchart LR
    SEQ[protein sequence] --> NN[deep network, GPU]
    NN --> STR[predicted 3D structure]
    STR --> DOWN[docking / function analysis]
```

**Next:** check your knowledge.
""",
        ),
        _t(
            "Reproducibility and FAIR data",
            "11 min",
            r"""# Reproducibility and FAIR data

The point of every preceding tool is **reproducibility**: another scientist
(including future-you) should be able to regenerate your results exactly. This
demands more than code — it requires capturing *code + environment + data +
provenance* together.

A robust reproducible project bundles:

- **Code** under Git, tagged at the published version.
- **Environment** pinned (`environment.yml` and/or a container image digest).
- **Workflow** as a Snakemake/Nextflow DAG that runs end to end.
- **Data** archived with stable identifiers (DOIs via Zenodo, accessions in
  SRA/ENA, GEO).

The community standard for data is **FAIR**: **F**indable, **A**ccessible,
**I**nteroperable, **R**eusable — persistent IDs, open protocols, standard
formats (FASTQ, BAM, VCF), and rich metadata. Workflow managers also emit
**provenance**: which inputs, parameters and software versions produced each
output, so any result is traceable.

```mermaid
flowchart LR
    DATA[FAIR data + DOI] --> WF[versioned workflow]
    ENV[pinned container] --> WF
    CODE[Git-tagged code] --> WF
    WF --> RES[results + provenance]
    RES --> PUB[publication + archive]
```

Reproducibility is not bureaucracy; it is what makes a computational result
*science* rather than an anecdote, and it lets the field build cumulatively.

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


SCIENTIFIC_COMPUTING_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["SCIENTIFIC_COMPUTING_COURSES"]
