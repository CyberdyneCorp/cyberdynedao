"""Academy seed content — the Git & Version Control track (Beginner → Advanced).

* ``git-basics``        — the model, commits/branches/merge, remotes
* ``git-intermediate``  — merge vs rebase, conflicts, history surgery, workflows
* ``git-advanced``      — internals (content-addressing), recovery, scale, review

Real ``git``/`sha1` can't run in the sandbox, so those appear as read-only
```bash / ```python blocks; runnable ``code`` lessons model git's ideas (commit
DAG, diff, content-addressed store) in pure Python builtins.
"""
# Lesson content uses arrows/symbols (→, ←, ↑) in diagrams and strings.

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# git-basics
# ──────────────────────────────────────────────────────────────────────

_GIT_BASICS = SeedCourse(
    slug="git-basics",
    title="Git & Version Control — Basics",
    description=(
        "Version control from first principles: why it exists, Git's "
        "three areas, commits as snapshots, branching and merging, and working "
        "with remotes. With a runnable model of the commit graph."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why version control?",
            "8 min",
            r"""# Why version control?

Before version control: `report_final.doc`, `report_final_v2.doc`,
`report_final_REALLY_final.doc`. Multiply that by a team and a codebase and you
have chaos.

A **Version Control System (VCS)** records the full history of a project so you
can:

- **Track every change** — who changed what, when, and *why* (the commit
  message).
- **Travel in time** — return to any past state; recover deleted code.
- **Work in parallel** — many people on the same codebase without overwriting
  each other.
- **Experiment safely** — try ideas on a branch; throw it away or merge it.

**Git** is the de-facto standard. It's **distributed**: every clone is a full
copy of the entire history, so you can commit, branch, and view history offline,
and there's no single point of failure. (Older systems like SVN were
*centralised* — one server held history and you needed it online to commit.)

The mental model to hold onto: **Git stores snapshots, not diffs.** Each commit
captures what *all* your tracked files looked like at that moment (sharing
unchanged files efficiently under the hood). Everything else builds on that.
""",
        ),
        _t(
            "The three areas & your first commits",
            "10 min",
            r"""# The three areas

Git has three places your work lives, and `add`/`commit` move it between them:

```
  working directory   →  staging area (index)  →  repository
      (edit files)         (git add)               (git commit)
```

- **Working directory** — your actual files, where you edit.
- **Staging area** — a *draft* of your next commit. You choose exactly what goes
  in with `git add`, so a commit can be a focused, logical change rather than
  "everything I touched".
- **Repository** — the committed history (the `.git` folder).

A typical first session:

```bash
git init                      # create a repo in this folder
git status                    # see what's changed / staged
git add app.py                # stage one file
git add .                     # or stage everything changed
git commit -m "Add greeting"  # snapshot the staged changes
git log --oneline             # view history
```

**Good commits** are small, focused, and have a clear message in the imperative
mood ("Add login validation", not "fixed stuff"). The first line is a ≤50-char
summary; add a blank line then detail if needed. Future-you reading `git log`
will be grateful.
""",
        ),
        _t(
            "Commits as snapshots: the graph",
            "9 min",
            r"""# Commits as a graph

Each commit points to its **parent**, forming a chain — actually a **directed
acyclic graph (DAG)**. A commit records: a snapshot of the files, the
parent(s), author, timestamp, message, and a unique **hash id** derived from all
of that.

A linear history:

```
A ← B ← C   (each arrow = "child points to parent")
        ↑
       main  (a branch is just a movable pointer to a commit)
        ↑
       HEAD  (where you are now)
```

Two key ideas:

- A **branch** is nothing but a lightweight, movable **pointer** to a commit —
  that's why branching in Git is instant and cheap.
- **HEAD** is a pointer to your current branch (hence the current commit).

When you commit, Git creates a new node, sets its parent to the current commit,
and moves the branch pointer (and HEAD) forward to it. When you branch, it just
writes a new pointer at the same commit. Understanding "pointers to nodes in a
DAG" makes branching, merging, and even rebasing feel obvious — you'll build
this graph in code next.
""",
        ),
        _code(
            "Model the commit graph",
            "12 min",
            r"""# A tiny model of Git's commit DAG — commits point to parents; branches and
# HEAD are just pointers. Press Run, then add a commit and re-run.

# Each commit: id -> (parent_id_or_None, message)
commits = {
    "a1": (None, "Initial commit"),
    "b2": ("a1", "Add greeting"),
    "c3": ("b2", "Add tests"),
}
branches = {"main": "c3"}     # a branch is a pointer to a commit
head = "main"                  # HEAD points to a branch

# (dicts are passed in, so these helpers stay self-contained)
def commit(commits, branches, head, message):
    parent = branches[head]
    new_id = "x" + str(len(commits))      # toy id
    commits[new_id] = (parent, message)
    branches[head] = new_id               # move the branch pointer forward
    return new_id

def history(commits, branches, branch):
    chain = []
    node = branches[branch]
    while node is not None:
        parent, msg = commits[node]
        chain.append((node, msg))
        node = parent
    return chain

print("commit:", commit(commits, branches, head, "Add logging"))
print("\\nhistory of main (newest first):")
for node, msg in history(commits, branches, "main"):
    print(" ", node, "-", msg)
print("\\nmain now points to:", branches["main"], "| HEAD ->", head)
""",
        ),
        _t(
            "Branches & HEAD",
            "9 min",
            r"""# Branches & HEAD

Because a branch is just a pointer, you create one and switch to it instantly:

```bash
git branch feature-login        # create a branch at the current commit
git switch feature-login        # move HEAD onto it (older: git checkout)
git switch -c feature-login     # create + switch in one step
```

Now commits you make move `feature-login` forward while `main` stays put:

```
A ← B ← C            (main)
         \
          D ← E      (feature-login, HEAD)
```

This is the heart of Git's workflow: **isolate work on a branch**, keep `main`
stable and releasable, and integrate when ready. Branches are cheap and
disposable — make one per feature, fix, or experiment.

`git switch main` moves HEAD back; your files change to match that commit. Your
feature work isn't lost — it's safe on its branch until you merge or delete it.

A common beginner fear is "losing work" when switching — Git won't let you
switch with uncommitted changes that would be overwritten; commit or `git stash`
them first (stash is covered in the next course).
""",
        ),
        _t(
            "Merging branches",
            "9 min",
            r"""# Merging branches

When a branch is ready, you **merge** it back. Two scenarios:

**Fast-forward** — if `main` hasn't moved since you branched, Git just slides
`main`'s pointer forward to your branch tip. No new commit, perfectly linear:

```
before:  A ← B ← C (main)  ⋯  C ← D ← E (feature)
after :  A ← B ← C ← D ← E (main)        # pointer moved up
```

**Merge commit** — if *both* branches advanced, Git creates a new commit with
**two parents** that ties the histories together:

```
A ← B ← C ← F (main)
     \        \
      D ← E ← M (merge commit, parents = F and E)
```

```bash
git switch main
git merge feature-login        # ff if possible, else a merge commit
```

If the same lines changed on both sides, you get a **merge conflict** — Git
marks the clashing regions and asks you to choose; you resolve, `git add`, and
commit. (Conflict resolution and the merge-vs-rebase debate are the start of the
Intermediate course.) Delete the branch after merging: `git branch -d
feature-login`.
""",
        ),
        _t(
            "Working with remotes",
            "9 min",
            r"""# Working with remotes

So far everything is local. A **remote** is a shared copy of the repo (on
GitHub, GitLab, a server) that a team syncs through.

```bash
git clone https://github.com/org/repo.git   # copy a remote locally
git remote -v                                 # list remotes (origin = default)
git fetch                                     # download remote changes (no merge)
git pull                                       # fetch + merge into current branch
git push                                       # upload your commits
git push -u origin feature-login              # first push of a new branch
```

The mental model: `origin/main` is your local snapshot of where the remote's
`main` was at your last fetch. `fetch` updates that snapshot; `merge`/`pull`
integrates it; `push` sends your commits up.

Because Git is distributed, you commit locally as much as you like and push when
ready — no constant server round-trips. The typical team loop:

1. `git pull` to get the latest.
2. Branch, commit your work.
3. `git push` your branch.
4. Open a **pull request** for review, then merge.

If `push` is rejected ("non-fast-forward"), someone pushed before you — `pull`
(integrating their work), resolve any conflicts, then push again.
""",
        ),
        _t(
            ".gitignore & undoing things",
            "8 min",
            r"""# .gitignore & undoing things

**Don't commit everything.** Build output, dependencies, secrets, and local
config shouldn't be in the repo. A **`.gitignore`** file lists patterns Git will
skip:

```
node_modules/
__pycache__/
*.log
.env            # NEVER commit secrets
build/
```

(Already-tracked files aren't ignored retroactively — `git rm --cached` them
first.)

**Undoing**, from safest to most destructive:

```bash
git restore app.py             # discard unstaged changes to a file
git restore --staged app.py    # unstage (keep the edits)
git commit --amend             # fix the LAST commit (message or contents)
git revert <commit>            # make a NEW commit that undoes an old one (safe, shareable)
git reset --hard <commit>      # move the branch back, DISCARDING changes (dangerous)
```

The golden rule: **`revert` for public history, `reset` for local-only.** Once
you've pushed, prefer `revert` — rewriting shared history (with `reset` or
rebase) breaks everyone else's clones. And almost nothing is truly lost in
Git: the **reflog** remembers where HEAD has been, so even a bad `reset` is
usually recoverable (covered in Advanced).
""",
        ),
        quiz_lesson(
            "Quiz: Git Basics",
            (
                q(
                    "What does Git store at each commit?",
                    (
                        opt(
                            "A snapshot of all tracked files (sharing unchanged ones), plus parent, author, message",
                            correct=True,
                        ),
                        opt("Only the diff (lines added/removed) from the previous commit"),
                        opt("Just the message and timestamp"),
                        opt("A compressed copy of the remote server"),
                    ),
                    "Git is snapshot-based; unchanged files are shared internally for efficiency.",
                ),
                q(
                    "What is a Git branch, technically?",
                    (
                        opt("A lightweight, movable pointer to a commit", correct=True),
                        opt("A full copy of the repository"),
                        opt("A folder containing duplicated files"),
                        opt("A remote server"),
                    ),
                    "Branches are just pointers — which is why creating/switching them is instant.",
                ),
                q(
                    "What is the staging area for?",
                    (
                        opt("Choosing exactly which changes go into the next commit", correct=True),
                        opt("Storing the remote's history"),
                        opt("Backing up deleted files"),
                        opt("Running the test suite"),
                    ),
                    "`git add` stages a curated set of changes so commits are focused and logical.",
                ),
                q(
                    "When does a merge fast-forward instead of creating a merge commit?",
                    (
                        opt(
                            "When the target branch hasn't advanced since you branched — the pointer just slides forward",
                            correct=True,
                        ),
                        opt("When both branches changed the same lines"),
                        opt("Whenever you push to a remote"),
                        opt("Only on the main branch"),
                    ),
                    "With no divergence, Git moves the pointer forward; divergence needs a 2-parent merge commit.",
                ),
                q(
                    "Why prefer `git revert` over `git reset --hard` for already-pushed commits?",
                    (
                        opt(
                            "revert adds a new commit that undoes changes without rewriting shared history",
                            correct=True,
                        ),
                        opt("reset is slower"),
                        opt("revert deletes the remote"),
                        opt("reset only works offline"),
                    ),
                    "Rewriting public history breaks others' clones; revert is safe because it only adds history.",
                ),
                q(
                    "What belongs in .gitignore?",
                    (
                        opt(
                            "Build output, dependencies, logs, and secrets like .env", correct=True
                        ),
                        opt("Your source code"),
                        opt("The commit messages"),
                        opt("Branch pointers"),
                    ),
                    "Ignore generated/dependency files and never commit secrets.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# git-intermediate
# ──────────────────────────────────────────────────────────────────────

_GIT_INTERMEDIATE = SeedCourse(
    slug="git-intermediate",
    title="Git & Version Control — Intermediate",
    description=(
        "Day-to-day fluency: merge vs rebase, resolving conflicts, history "
        "surgery (interactive rebase, stash, cherry-pick, reflog), tags & "
        "semver, and the team branching strategies that keep big repos sane."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Merge vs rebase",
            "10 min",
            r"""# Merge vs rebase

Two ways to integrate a branch — the most argued-about topic in Git.

**Merge** keeps history exactly as it happened, adding a merge commit:

```
A ← B ← C ← M (main)
     \      /
      D ← E       (feature)
```

Truthful, non-destructive, but the graph gets tangled with many merge commits.

**Rebase** *replays* your branch's commits on top of the latest target, as if
you'd started from there — giving a clean, linear history:

```
before:  A ← B ← C (main)        after rebase onto main:
              \                    A ← B ← C ← D' ← E'
               D ← E (feature)            (feature, replayed)
```

```bash
git switch feature
git rebase main         # replay feature's commits on top of main
```

Note `D'`/`E'` are **new commits** (new hashes) — rebase **rewrites history**.

**The golden rule of rebase:** never rebase commits you've already pushed and
others may have based work on — you'd diverge from their copies. Rebase **local,
unpushed** work to tidy it; **merge** to integrate shared branches. Many teams:
rebase your feature onto main to keep it current, then merge it in.
""",
        ),
        _t(
            "Resolving conflicts",
            "9 min",
            r"""# Resolving conflicts

A conflict happens when two branches change **the same lines** (or one edits a
file the other deleted). Git can't guess your intent, so it pauses and marks the
clash:

```
<<<<<<< HEAD
greeting = "Hello"
=======
greeting = "Hi there"
>>>>>>> feature-login
```

- Everything between `<<<<<<<` and `=======` is **your** side (current branch).
- Between `=======` and `>>>>>>>` is the **incoming** side.

To resolve: **edit the file** to the version you want (keep one, the other, or a
combination), delete the conflict markers, then:

```bash
git add app.py        # mark this file resolved
git status            # see remaining conflicts
git commit            # (merge) or: git rebase --continue
```

Tips that prevent pain:
- **Pull/rebase often** — small, frequent integrations conflict less than one
  giant merge.
- Use a **merge tool** (`git mergetool`, or your IDE's 3-way view) for messy
  conflicts.
- `git merge --abort` / `git rebase --abort` backs out cleanly if you want to
  start over.

Conflicts feel scary at first but are routine — they're just Git asking a
question only you can answer.
""",
        ),
        _code(
            "How diff works: longest common subsequence",
            "13 min",
            r"""# Git's diff finds what changed by computing the LONGEST COMMON SUBSEQUENCE
# (LCS) of the two versions' lines — the unchanged backbone. Everything not on
# it is an add or a delete. Here it is in pure Python (no libraries).

old = ["import os", "def greet():", "    print('hi')", "greet()"]
new = ["import os", "import sys", "def greet():", "    print('hello')", "greet()"]

def lcs_table(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    return dp

dp = lcs_table(old, new)
i, j = 0, 0
print("diff (old -> new):")
while i < len(old) and j < len(new):
    if old[i] == new[j]:
        print("  ", old[i])          # unchanged (on the LCS)
        i += 1; j += 1
    elif dp[i + 1][j] >= dp[i][j + 1]:
        print("- ", old[i]); i += 1   # removed
    else:
        print("+ ", new[j]); j += 1   # added
while i < len(old):
    print("- ", old[i]); i += 1
while j < len(new):
    print("+ ", new[j]); j += 1
""",
        ),
        _t(
            "History surgery: rebase -i, amend, squash",
            "10 min",
            r"""# History surgery

Before sharing work, you can **clean up** local commits into a tidy story.

**Amend** the last commit (fix the message or add a forgotten file):

```bash
git add forgotten.py
git commit --amend -m "Add login validation"
```

**Interactive rebase** rewrites a *range* of commits — reorder, edit, drop, or
**squash** several into one:

```bash
git rebase -i HEAD~4        # edit the last 4 commits
```

You get an editor listing the commits with actions:

```
pick   a1c  Add login form
squash b2d  fix typo            # fold into the commit above
squash c3e  fix another typo
reword d4f  Add validation      # change this message
```

Result: three messy commits become one clean "Add login form" plus a reworded
"Add validation" — a reviewable history instead of a trail of "fix typo".

Same golden rule as rebase: **only rewrite commits you haven't pushed.** The
goal isn't a fake history — it's a *readable* one: each commit a coherent,
self-contained change that compiles and passes tests. Reviewers (and `git
bisect`, in the next course) reward you for it.
""",
        ),
        _t(
            "Stash, cherry-pick & the reflog",
            "9 min",
            r"""# Stash, cherry-pick & the reflog

Three power tools for everyday flow:

**Stash** — shelve uncommitted work to switch context, then bring it back:

```bash
git stash               # set work aside (working dir goes clean)
git switch main         # do an urgent fix
git switch feature
git stash pop           # reapply your shelved work
```

**Cherry-pick** — copy a single commit from one branch onto another (e.g.
backport a fix to a release branch):

```bash
git cherry-pick a1c2d3e   # apply just that commit here (as a new commit)
```

**Reflog** — Git's safety net. It logs every move of HEAD (commits, switches,
resets, rebases) for ~90 days, so you can recover "lost" commits:

```bash
git reflog                       # list recent HEAD positions
git reset --hard HEAD@{2}        # jump back to where you were 2 moves ago
```

Did a `reset --hard` and panic? The old commit isn't gone — `git reflog` will
show its hash, and `git checkout <hash>` (or branch from it) brings it back.
Internalising the reflog removes the fear of experimenting: in Git, **mistakes
are almost always reversible.**
""",
        ),
        _t(
            "Tags, releases & semantic versioning",
            "8 min",
            r"""# Tags, releases & semantic versioning

A **tag** marks a specific commit permanently — typically a release. Unlike a
branch, it doesn't move.

```bash
git tag -a v1.2.0 -m "Release 1.2.0"   # annotated tag (recommended)
git push origin v1.2.0                  # tags aren't pushed by default
git tag                                  # list tags
git checkout v1.2.0                      # inspect that exact release
```

**Semantic Versioning (SemVer)** gives those tags meaning: `MAJOR.MINOR.PATCH`.

- **MAJOR** — incompatible/breaking API changes (1.x → 2.0.0).
- **MINOR** — new features, backward-compatible (1.2 → 1.3.0).
- **PATCH** — backward-compatible bug fixes (1.2.0 → 1.2.1).

So `2.0.0` warns consumers "this may break you"; `1.3.0` says "safe new
features"; `1.2.1` says "just fixes". Pre-releases append a label: `2.0.0-rc.1`.

This convention lets dependency managers (npm, pip, cargo) resolve safe upgrades
automatically (e.g. "accept any `1.x` ≥ 1.2"). Pair tags with **release notes**
/ a changelog so humans know what changed, and many teams automate version
bumps and changelogs from commit messages (Conventional Commits).
""",
        ),
        _t(
            "Branching strategies for teams",
            "9 min",
            r"""# Branching strategies for teams

How a team uses branches shapes how smoothly it ships. The main approaches:

**GitHub Flow** (simple, most common) — `main` is always deployable. Branch per
change → PR → review → merge → deploy. Short-lived branches, continuous
delivery. Great default for web apps and small/medium teams.

**Trunk-Based Development** — everyone integrates to `main` (trunk) very
frequently (at least daily), often behind **feature flags** for unfinished work.
Minimises long-lived branches and merge hell; pairs with strong CI. Favoured by
high-velocity orgs.

**Git Flow** — structured branches: `main` (releases), `develop` (integration),
plus `feature/*`, `release/*`, `hotfix/*`. Powerful for scheduled releases and
multiple supported versions, but heavyweight — often overkill for continuous web
deployment.

The trends that matter regardless of model:

- **Short-lived branches** — the longer a branch lives, the worse the merge.
- **Small, frequent PRs** — easier to review, faster to ship.
- **Protected `main`** — require PR review + green CI before merge.
- **Keep `main` releasable** — never leave it broken.

Pick the lightest model that fits your release cadence; complexity should serve
the team, not the other way around.
""",
        ),
        quiz_lesson(
            "Quiz: Git in Daily Practice",
            (
                q(
                    "What does `git rebase` do that `git merge` doesn't?",
                    (
                        opt(
                            "Replays commits onto a new base, rewriting them into a linear history",
                            correct=True,
                        ),
                        opt("Uploads commits to the remote"),
                        opt("Deletes the feature branch"),
                        opt("Creates a tag"),
                    ),
                    "Rebase creates new commits on top of the target; merge preserves history with a merge commit.",
                ),
                q(
                    "What is the golden rule of rebasing?",
                    (
                        opt(
                            "Never rebase commits that have been pushed and others may depend on",
                            correct=True,
                        ),
                        opt("Always rebase before every commit"),
                        opt("Only rebase the main branch"),
                        opt("Rebase deletes conflicts automatically"),
                    ),
                    "Rebasing rewrites history; doing it to shared commits diverges everyone's clones.",
                ),
                q(
                    "Between `=======` and `>>>>>>>` in a conflict, whose changes are shown?",
                    (
                        opt("The incoming branch's changes", correct=True),
                        opt("Your current branch's changes"),
                        opt("The remote server's configuration"),
                        opt("The previous commit"),
                    ),
                    "Top (HEAD…=======) is your side; bottom (=======…>>>>>>>) is the incoming branch.",
                ),
                q(
                    "What does the reflog let you do?",
                    (
                        opt(
                            "Recover commits/positions HEAD has visited, even after a bad reset",
                            correct=True,
                        ),
                        opt("Push tags to the remote"),
                        opt("Ignore files"),
                        opt("Merge two repositories"),
                    ),
                    "The reflog records HEAD's recent moves, so 'lost' commits are usually recoverable.",
                ),
                q(
                    "In SemVer, which part bumps for a backward-incompatible change?",
                    (
                        opt("MAJOR (e.g. 1.4.2 → 2.0.0)", correct=True),
                        opt("MINOR"),
                        opt("PATCH"),
                        opt("None — versions never change for breaking changes"),
                    ),
                    "MAJOR signals breaking changes; MINOR adds compatible features; PATCH fixes bugs.",
                ),
                q(
                    "What does cherry-pick do?",
                    (
                        opt(
                            "Applies a single specific commit onto the current branch", correct=True
                        ),
                        opt("Merges two whole branches"),
                        opt("Deletes a commit from history"),
                        opt("Creates a new remote"),
                    ),
                    "Cherry-pick copies one commit (e.g. to backport a fix) as a new commit on your branch.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# git-advanced
# ──────────────────────────────────────────────────────────────────────

_GIT_ADVANCED = SeedCourse(
    slug="git-advanced",
    title="Git & Version Control — Advanced",
    description=(
        "Under the hood and at scale: Git's content-addressed object model, "
        "recovery with reflog and bisect, submodules and monorepos, hooks and "
        "CI, big-repo performance, and collaboration via reviews and protected "
        "branches."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Git internals: the object model",
            "11 min",
            r"""# Git internals: the object model

Under `.git`, Git is a simple **content-addressed key-value store**. Four object
types, each named by the **hash of its content**:

- **blob** — the contents of a file (no name, just bytes).
- **tree** — a directory listing: names → blob/tree hashes (this is where
  filenames live).
- **commit** — points to one **tree** (the snapshot), parent commit(s), author,
  and message.
- **tag** — an annotated pointer to a commit.

```
commit ──tree──▶ tree ──▶ blob (app.py)
   │                 └──▶ blob (README)
   └─parent─▶ commit ...
```

The crucial property: a Git object's id **is** the hash of its content
(historically SHA-1, moving to SHA-256). So:

- **Identical content → identical hash → stored once.** Deduplication is free.
- **Any change → different hash all the way up** to the commit, so history is
  **tamper-evident**: you can't alter a past file without changing every
  descendant commit's id.

```bash
git cat-file -p HEAD        # see the commit object (tree, parent, author)
git cat-file -p <tree>      # see a directory listing
```

This is why two branches with the same file share storage, and why a commit hash
uniquely pins an *entire* project state. You'll model content-addressing next.
""",
        ),
        _code(
            "A content-addressed object store",
            "13 min",
            r"""# Model Git's core idea: store objects BY A HASH OF THEIR CONTENT.
# (Git uses SHA-1/256; that lib isn't in the sandbox, so we use a simple toy
#  hash — the PRINCIPLE is identical: same content => same id => stored once.)

store = {}                      # the object database: id -> content

def put(store, content):
    # A small polynomial rolling hash -> hex id (illustrative; git uses SHA).
    h = 0
    for ch in content:
        h = (h * 31 + ord(ch)) % (2 ** 32)
    oid = format(h, "08x")
    store[oid] = content        # writing the same content twice is a no-op
    return oid

# Two files with identical content...
id1 = put(store, "print('hello')\n")
id2 = put(store, "print('hello')\n")
id3 = put(store, "print('world')\n")

print("file1 id:", id1)
print("file2 id:", id2, "(same content -> SAME id)")
print("file3 id:", id3, "(different content -> different id)")
print("dedup works:", id1 == id2)
print("objects actually stored:", len(store))   # 2, not 3
# A commit just stores the id of a 'tree' that maps names -> these blob ids.
print("retrieve id1:", store[id1].strip())
""",
        ),
        _t(
            "Recovery & debugging: reflog, bisect, fsck",
            "10 min",
            r"""# Recovery & debugging

**Nothing is really lost.** Commits stay in the object store (unreferenced) until
garbage collection, ~90 days later. To recover:

```bash
git reflog                     # every HEAD move; find the lost commit's hash
git branch rescue <hash>       # re-attach it to a branch
git fsck --lost-found          # find dangling commits the reflog missed
```

**Find the commit that introduced a bug** with `git bisect` — a binary search
over history:

```bash
git bisect start
git bisect bad                 # current commit is broken
git bisect good v1.2.0         # this old release worked
# Git checks out the midpoint; you test and mark each:
git bisect good   # or  git bisect bad
# ...repeat; Git halves the range each time...
git bisect reset               # when it names the culprit
```

Across 1,000 commits, bisect finds the offender in ~10 steps instead of 1,000.
You can even automate it: `git bisect run ./test.sh` lets a test script answer
good/bad for you, pinpointing the regression hands-free.

These tools turn "we broke something, somewhere, sometime" into a fast,
mechanical search — and remove the fear of aggressive history editing, because
the reflog has your back.
""",
        ),
        _t(
            "Submodules & monorepos",
            "9 min",
            r"""# Submodules & monorepos

Two answers to "how do we manage many projects?"

**Submodules** — embed one repo inside another, pinned to a specific commit:

```bash
git submodule add https://github.com/org/lib.git vendor/lib
git submodule update --init --recursive   # after cloning the parent
```

The parent records *which commit* of the sub-repo it uses, so builds are
reproducible. The cost: submodules are fiddly — you must update and commit the
pointer deliberately, and contributors forget to `--init`. Good for vendoring a
dependency you occasionally bump.

**Monorepo** — one big repo holding many projects/services, sharing tooling and
atomic cross-project commits. Used at huge scale (Google, Meta). Benefits:
unified history, easy refactors across boundaries, one CI. Costs: the repo grows
huge and needs tooling (build systems like Bazel, sparse/partial checkouts) to
stay fast.

**Polyrepo** (one repo per project) is the opposite trade-off: independence and
small repos, but cross-cutting changes span many PRs and versioning gets
complex.

There's no universal winner — choose by team size, how coupled the projects
are, and your tolerance for tooling investment. Many orgs run a pragmatic mix.
""",
        ),
        _t(
            "Hooks & automation",
            "9 min",
            r"""# Hooks & automation

**Git hooks** are scripts Git runs automatically at lifecycle events — your
chance to enforce quality before bad code spreads.

**Client-side** (in `.git/hooks/`, or managed by tools like *pre-commit* /
*husky*):

- `pre-commit` — run linters, formatters, secret scanners; **block the commit**
  if they fail.
- `commit-msg` — enforce a message format (e.g. Conventional Commits).
- `pre-push` — run the test suite before code leaves your machine.

```bash
# .git/hooks/pre-commit (made executable)
#!/bin/sh
npm run lint && npm test || { echo "checks failed"; exit 1; }
```

**Server-side** (`pre-receive`, `update`) run on the remote to enforce policy no
client can bypass — reject force-pushes to `main`, require signed commits, etc.

In practice most teams run the real gates in **CI** (GitHub Actions, GitLab CI):
on every push/PR, a pipeline checks out the code, runs lint + type-check + tests
+ security scans, and **branch protection** blocks merging until they pass. Local
hooks give fast feedback; CI is the authoritative gate because it can't be
skipped. Together they keep `main` green.
""",
        ),
        _t(
            "Performance, scale & collaboration",
            "10 min",
            r"""# Performance, scale & collaboration

**Big repositories** strain Git (it was built for source code, not gigabytes of
assets). Tools that help:

- **Git LFS (Large File Storage)** — keep large binaries (videos, datasets,
  models) out of history; the repo stores small pointers, the blobs live
  elsewhere.
- **Shallow clone** (`--depth 1`) — grab only recent history for CI, where you
  don't need the full past.
- **Partial / sparse checkout** — fetch only the files/paths you need from a
  huge monorepo.
- **`git gc` / commit-graph** — repack and index to keep operations fast.

**Collaboration at scale** is mostly process, enforced by the platform:

- **Pull/Merge Requests** — the unit of review. Keep them **small and focused**
  (under a few hundred lines) so reviews are fast and thorough.
- **Code review** — at least one approval; review for correctness, design,
  security, and tests — not just style (let linters handle style).
- **Protected branches** — require green CI + approvals; forbid force-push to
  `main`; optionally require signed commits and linear history.
- **CODEOWNERS** — auto-request the right reviewers for each path.

The throughline of this whole track: Git's simple model (snapshots, pointers,
content-addressed objects) scales from a solo script to thousands of engineers —
*if* you pair it with small changes, fast CI, and disciplined review.
""",
        ),
        quiz_lesson(
            "Quiz: Git Internals & Scale",
            (
                q(
                    "How is a Git object's id determined?",
                    (
                        opt(
                            "It's a hash of the object's content, so identical content gets the same id",
                            correct=True,
                        ),
                        opt("It's a random UUID assigned at commit time"),
                        opt("It's the file's path"),
                        opt("It's an auto-incrementing number"),
                    ),
                    "Content-addressing means dedup is free and history is tamper-evident.",
                ),
                q(
                    "Which object type stores filenames?",
                    (
                        opt(
                            "tree (a directory listing mapping names to blob/tree ids)",
                            correct=True,
                        ),
                        opt("blob"),
                        opt("commit"),
                        opt("tag"),
                    ),
                    "Blobs hold file *contents* (nameless); trees map names to blobs/trees.",
                ),
                q(
                    "Why can't you alter a past file without it being detectable?",
                    (
                        opt(
                            "Changing content changes its hash, which changes every descendant commit's id",
                            correct=True,
                        ),
                        opt("Git encrypts the whole repo"),
                        opt("The remote server locks old commits"),
                        opt("Past commits are read-only files"),
                    ),
                    "Hashes chain upward, so any tampering ripples through all later commit ids.",
                ),
                q(
                    "What problem does `git bisect` solve, and how fast?",
                    (
                        opt(
                            "Finds the commit that introduced a bug via binary search (~log₂ N steps)",
                            correct=True,
                        ),
                        opt("Merges two branches automatically"),
                        opt("Compresses the repository"),
                        opt("Lists all contributors"),
                    ),
                    "Bisect halves the suspect range each step — ~10 tests across 1,000 commits.",
                ),
                q(
                    "What is Git LFS for?",
                    (
                        opt(
                            "Keeping large binary files out of history, storing small pointers instead",
                            correct=True,
                        ),
                        opt("Encrypting commits"),
                        opt("Running tests faster"),
                        opt("Merging submodules"),
                    ),
                    "LFS replaces big blobs with pointers so the repo stays small and fast.",
                ),
                q(
                    "Why do most teams enforce quality gates in CI rather than only local hooks?",
                    (
                        opt(
                            "CI can't be skipped/bypassed, so it's the authoritative gate before merge",
                            correct=True,
                        ),
                        opt("Local hooks are always faster"),
                        opt("CI doesn't need tests"),
                        opt("Hooks run on the remote server"),
                    ),
                    "Local hooks give fast feedback but can be bypassed; CI + branch protection is enforceable.",
                ),
            ),
        ),
    ),
)


GIT_COURSES = (_GIT_BASICS, _GIT_INTERMEDIATE, _GIT_ADVANCED)
