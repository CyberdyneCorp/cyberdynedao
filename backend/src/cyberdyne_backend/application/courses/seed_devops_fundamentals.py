"""Academy seed content - DevOps Fundamentals.

The conceptual overview that ties the DevOps stage together: what DevOps
is (culture and the lifecycle loop), continuous integration, continuous
delivery/deployment, infrastructure as code, containers and orchestration
at a high level, observability (logs/metrics/traces), and how teams
measure themselves (DORA metrics, SRE, blameless postmortems). It sits in
front of the tool-specific courses (Docker, Kubernetes, Terraform,
Ansible) as the "why and how it fits together" introduction. Every lesson
is a direct explanation with concrete config/pipeline examples and a
mermaid diagram, followed by a checkpoint quiz; the course closes with a
comprehensive final quiz.
"""

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


_DEVOPS_FUNDAMENTALS = SeedCourse(
    slug="devops-fundamentals",
    title="DevOps Fundamentals",
    description=(
        "The DevOps big picture, before the tools: culture and the lifecycle "
        "loop, continuous integration and delivery, infrastructure as code, "
        "containers and orchestration, observability, and how teams measure "
        "themselves (DORA, SRE) - with real pipeline, Dockerfile and "
        "Terraform examples and a diagram in every lesson."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# DevOps Fundamentals

DevOps is not a tool you install - it is a way of building and running
software so that changes reach users quickly, safely, and often. The
tools (Docker, Kubernetes, Terraform, CI systems) are how; the culture
and the feedback loops are why. This course gives you the whole picture
before you go deep on any single tool.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short real example (a pipeline file, a
Dockerfile, a Terraform snippet), and draws the idea as a diagram. After
each lesson there is a short quiz; at the end, a final quiz covers the
whole course.

What you will build understanding for, in order:

1. **What DevOps is** - culture, the wall of confusion, the lifecycle loop
2. **Continuous Integration** - build and test on every change
3. **Continuous Delivery/Deployment** - release safely and often
4. **Infrastructure as Code** - servers defined in version-controlled files
5. **Containers and orchestration** - Docker and Kubernetes, at a glance
6. **Observability** - logs, metrics, and traces
7. **Reliability and DORA metrics** - measuring speed and stability
8. **Putting it together** - the end-to-end path from commit to production

This is the map. The tool-specific courses in this track (Docker,
Kubernetes, Terraform, Ansible) are the deep dives; knowing where each
fits makes them far easier to learn.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is DevOps, fundamentally?",
                    (
                        opt("A single tool you install on a server"),
                        opt("A job title for the person who runs the servers"),
                        opt(
                            "A culture and set of practices for delivering software "
                            "quickly, safely and often - the tools are how, not what",
                            correct=True,
                        ),
                        opt("A programming language for automation"),
                    ),
                    "DevOps is culture + practices + tooling; the goal is fast, safe, "
                    "frequent delivery, not any one product.",
                ),
                q(
                    "How does this course relate to the Docker/Kubernetes/Terraform "
                    "courses in the track?",
                    (
                        opt("It replaces them"),
                        opt(
                            "It is the big-picture overview that shows where each tool "
                            "fits, before the tool-specific deep dives",
                            correct=True,
                        ),
                        opt("It only covers cloud billing"),
                        opt("It is unrelated to the other DevOps courses"),
                    ),
                    "Learn the map first (this course), then the tools (the deep-dive "
                    "courses) make sense in context.",
                ),
            ),
        ),
        # -- 1. What is DevOps -----------------------------------------
        _t(
            "What is DevOps? Culture and the loop",
            "9 min",
            """# What is DevOps? Culture and the loop

Historically, **Development** wrote code and threw it over a wall to
**Operations**, who had to run it. Dev was rewarded for change; Ops for
stability. Those incentives conflict - the "wall of confusion" - and the
result was slow, risky, finger-pointing releases.

**DevOps** removes the wall: the same team (or tightly-collaborating
teams) **builds and runs** the software, sharing responsibility for both
shipping features and keeping them healthy. "You build it, you run it."

A common way to remember the culture is **CALMS**:

- **Culture** - shared ownership, blameless learning from failure.
- **Automation** - if a step is manual and repeated, automate it.
- **Lean** - small batches; ship small changes continuously.
- **Measurement** - decide with data (see the DORA lesson).
- **Sharing** - visible information, knowledge, and tooling across teams.

The work is usually drawn as an **infinite loop** - because software is
never "done", it cycles continuously:

```mermaid
graph LR
    PLAN["Plan"] --> CODE["Code"]
    CODE --> BUILD["Build"]
    BUILD --> TEST["Test"]
    TEST --> RELEASE["Release"]
    RELEASE --> DEPLOY["Deploy"]
    DEPLOY --> OPERATE["Operate"]
    OPERATE --> MONITOR["Monitor"]
    MONITOR --> PLAN
```

The two halves matter: the left (plan/code/build/test) is where CI lives;
the right (release/deploy/operate/monitor) is where CD and observability
live. Feedback from **monitor** flows back into **plan** - that closing
loop is the whole point.

The one thing to remember: DevOps is about **flow and feedback** - move
changes smoothly from idea to production, then learn from production to
improve the next change.
""",
        ),
        quiz_lesson(
            "Quiz: What is DevOps? Culture and the loop",
            (
                q(
                    "What was the 'wall of confusion' DevOps set out to remove?",
                    (
                        opt("A firewall between the office and the internet"),
                        opt(
                            "The divide between Development (rewarded for change) and "
                            "Operations (rewarded for stability), whose conflicting "
                            "incentives made releases slow and risky",
                            correct=True,
                        ),
                        opt("The gap between frontend and backend code"),
                        opt("The barrier between staging and the database"),
                    ),
                    "Dev wanted change, Ops wanted stability; DevOps aligns them with "
                    "shared ownership - 'you build it, you run it.'",
                ),
                q(
                    "What does the M in CALMS stand for?",
                    (
                        opt("Microservices"),
                        opt("Monitoring tools"),
                        opt("Measurement - deciding with data", correct=True),
                        opt("Migration"),
                    ),
                    "CALMS = Culture, Automation, Lean, Measurement, Sharing.",
                ),
                q(
                    "Why is the DevOps lifecycle drawn as an infinite loop?",
                    (
                        opt("Because the tools run in an infinite loop"),
                        opt(
                            "Software is never 'done' - feedback from monitoring in "
                            "production flows back into planning the next change",
                            correct=True,
                        ),
                        opt("Because deployments must repeat exactly every hour"),
                        opt("It is just a logo, with no meaning"),
                    ),
                    "Plan-code-build-test-release-deploy-operate-monitor, then back to "
                    "plan: continuous flow and feedback.",
                ),
            ),
        ),
        # -- 2. CI -----------------------------------------------------
        _t(
            "Continuous Integration",
            "10 min",
            """# Continuous Integration

**Continuous Integration (CI)** means every change a developer pushes is
automatically **built and tested** - many times a day, on a shared main
branch. The goal is to catch integration problems within minutes of
introducing them, while the change is small and the author still has it
in mind.

The mechanics: a developer pushes to the repository; a **CI server**
(GitHub Actions, GitLab CI, Jenkins...) checks out the code and runs a
**pipeline** - a sequence of automated steps. If any step fails, the
change is blocked and the author is told immediately.

A minimal GitHub Actions pipeline:

```yaml
# .github/workflows/ci.yml - runs on every push
name: CI
on: [push]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4          # get the code
      - uses: actions/setup-node@v4        # set up the toolchain
        with: { node-version: 20 }
      - run: npm ci                        # install deps
      - run: npm run lint                  # static checks
      - run: npm test                      # the test suite
```

What makes CI *continuous* rather than just "we have tests":

- **Integrate to main frequently** - at least daily, ideally per change.
  Long-lived branches defeat the purpose (they hide integration problems
  until a painful merge).
- **Every push runs the pipeline** - automatically, no human deciding to
  run it.
- **A red build stops the line** - a failing pipeline is the team's top
  priority to fix; you do not build on a broken main.
- **Fast and reliable** - a slow or flaky pipeline gets ignored. Keep it
  quick (parallelize, cache) and deterministic.

CI is the foundation everything else builds on: you cannot deliver
continuously if you are not integrating continuously.

```mermaid
graph LR
    PUSH["Developer pushes"] --> TRIG["CI server triggers pipeline"]
    TRIG --> BUILD["Build"]
    BUILD --> LINT["Lint and static checks"]
    LINT --> TEST["Automated tests"]
    TEST --> PASS["Green merge allowed"]
    TEST --> FAIL["Red block and alert author"]
```

Remember: CI turns "did my change break anything?" from a worry into an
automatic answer within minutes.
""",
        ),
        quiz_lesson(
            "Quiz: Continuous Integration",
            (
                q(
                    "What does Continuous Integration automate?",
                    (
                        opt("Deploying to production servers"),
                        opt(
                            "Building and testing every pushed change automatically, so "
                            "integration problems are caught within minutes",
                            correct=True,
                        ),
                        opt("Provisioning cloud infrastructure"),
                        opt("Writing the code itself"),
                    ),
                    "CI = build + test on every push to a shared branch; fast feedback "
                    "on small changes.",
                ),
                q(
                    "Why are long-lived feature branches discouraged in CI?",
                    (
                        opt("They use too much disk space"),
                        opt(
                            "They hide integration problems until a large, painful merge "
                            "- defeating the point of integrating continuously",
                            correct=True,
                        ),
                        opt("Git cannot handle more than one branch"),
                        opt("They make the pipeline run faster"),
                    ),
                    "Integrate to main frequently (ideally per change) so conflicts "
                    "surface small and early.",
                ),
                q(
                    "In CI, what should happen when the pipeline goes red (a build fails)?",
                    (
                        opt("Ignore it and keep merging"),
                        opt("Deploy anyway to save time"),
                        opt(
                            "Fixing it becomes the team's top priority - you do not "
                            "build on a broken main",
                            correct=True,
                        ),
                        opt("Delete the failing test"),
                    ),
                    "A red build stops the line; a healthy main is a shared responsibility.",
                ),
            ),
        ),
        # -- 3. CD -----------------------------------------------------
        _t(
            "Continuous Delivery and Deployment",
            "10 min",
            """# Continuous Delivery and Deployment

Once CI produces a tested build (an **artifact**), the next question is
getting it to users. Two related terms:

- **Continuous Delivery** - every change that passes CI is *automatically
  prepared* for release and could be deployed at the push of a button. A
  human makes the final go/no-go call.
- **Continuous Deployment** - one step further: every change that passes
  the pipeline is *automatically deployed to production*, no human gate.

Both extend the pipeline past testing into **environments** - typically a
promotion path where a build proves itself before reaching users:

```yaml
# extending the pipeline: build -> deploy to staging -> deploy to prod
deploy-staging:
  needs: build-and-test          # only if CI passed
  run: ./deploy.sh staging
deploy-production:
  needs: deploy-staging          # promote the SAME artifact
  environment: production        # may require an approval
  run: ./deploy.sh production
```

The rule: **build the artifact once, promote the same artifact** through
staging to production. Rebuilding per environment risks shipping
something you never tested.

Because deploying often still carries risk, safe **release strategies**
limit the blast radius:

- **Blue-green** - run two identical environments; deploy to the idle one
  ("green"), then switch traffic over. Instant rollback: switch back.
- **Canary** - route a small percentage of traffic to the new version;
  watch the metrics; ramp up only if it stays healthy.
- **Rolling** - replace instances a few at a time so the service stays up.
- **Feature flags** - deploy code dark, then turn a feature on for a
  subset of users independently of the deploy.

```mermaid
graph LR
    ART["Tested artifact"] --> STG["Deploy to staging"]
    STG --> CHK["Automated checks and approval"]
    CHK --> CAN["Canary small traffic slice"]
    CAN --> HEALTHY["Metrics healthy"]
    HEALTHY --> FULL["Roll out to all users"]
    CAN --> ROLL["Unhealthy roll back"]
```

Remember: delivery makes every good build *releasable*; deployment makes
it *released*; release strategies make releasing *safe*.
""",
        ),
        quiz_lesson(
            "Quiz: Continuous Delivery and Deployment",
            (
                q(
                    "What is the difference between Continuous Delivery and Continuous Deployment?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "Delivery keeps every passing change ready to release behind "
                            "a human go/no-go; Deployment releases every passing change "
                            "to production automatically",
                            correct=True,
                        ),
                        opt("Delivery is for hardware, Deployment for software"),
                        opt("Deployment requires no testing"),
                    ),
                    "Both automate up to production; the difference is whether a human "
                    "presses the final button.",
                ),
                q(
                    "Why 'build once, promote the same artifact' through environments?",
                    (
                        opt("To use less CI compute"),
                        opt(
                            "Rebuilding per environment risks shipping something "
                            "different from what you tested",
                            correct=True,
                        ),
                        opt("Because artifacts expire after one deploy"),
                        opt("It is required by YAML syntax"),
                    ),
                    "The thing you tested in staging must be the exact thing that "
                    "reaches production.",
                ),
                q(
                    "A canary release does what?",
                    (
                        opt("Deploys to all users at once"),
                        opt("Runs the tests a second time"),
                        opt(
                            "Routes a small slice of traffic to the new version and "
                            "watches metrics before ramping up",
                            correct=True,
                        ),
                        opt("Keeps two full environments and switches between them"),
                    ),
                    "Canary limits blast radius: prove health on a few percent of "
                    "traffic first. (Two-environment switching is blue-green.)",
                ),
            ),
        ),
        # -- 4. IaC ----------------------------------------------------
        _t(
            "Infrastructure as Code",
            "10 min",
            """# Infrastructure as Code

**Infrastructure as Code (IaC)** means defining your servers, networks,
databases and other resources in **version-controlled files** instead of
clicking through a console. The files are the source of truth; a tool
makes the real infrastructure match them.

Why it matters:

- **Reproducible** - stand up an identical environment from the same code,
  every time. No "works on the one server someone configured by hand."
- **Versioned and reviewed** - infrastructure changes go through the same
  pull-request review and history as application code.
- **Auditable and recoverable** - the files document exactly what exists;
  rebuild after a disaster by re-applying them.

A **declarative** example in Terraform - you describe the *desired state*,
the tool figures out the steps:

```hcl
# main.tf - desired state: one web server on AWS
resource "aws_instance" "web" {
  ami           = "ami-0abcd1234"
  instance_type = "t3.micro"
  tags = { Name = "web-server" }
}
```

Run `terraform plan` and it shows the diff between the world and your
files; `terraform apply` makes reality match. Two ideas make this safe:

- **Declarative over imperative** - you state *what* you want, not the
  step-by-step *how*. The tool computes the changes needed.
- **Idempotent** - applying the same config repeatedly converges to the
  same state. Already-correct resources are left alone; only drift is
  fixed. (Ansible, Terraform, and friends are built around this.)

IaC covers two overlapping jobs: **provisioning** (creating the servers
and networks - Terraform, CloudFormation) and **configuration
management** (setting up what runs on them - Ansible, Chef, Puppet).

```mermaid
graph LR
    CODE["Infra defined in files"] --> VCS["Version control and review"]
    VCS --> PLAN["Plan shows the diff"]
    PLAN --> APPLY["Apply makes reality match"]
    APPLY --> STATE["Desired state reached"]
    STATE --> IDEM["Idempotent re-apply is safe"]
```

Remember: if you configured it by hand, you cannot reliably reproduce it.
Put the infrastructure in code and let the diff drive the change.
""",
        ),
        quiz_lesson(
            "Quiz: Infrastructure as Code",
            (
                q(
                    "What does Infrastructure as Code mean?",
                    (
                        opt("Writing application code that needs no servers"),
                        opt(
                            "Defining infrastructure (servers, networks, databases) in "
                            "version-controlled files that a tool applies",
                            correct=True,
                        ),
                        opt("Storing passwords in the codebase"),
                        opt("Coding directly on the production server"),
                    ),
                    "The files are the source of truth; the tool makes real "
                    "infrastructure match them - reproducible and reviewable.",
                ),
                q(
                    "What does 'idempotent' mean for an IaC tool?",
                    (
                        opt("It can only run once"),
                        opt("It deletes everything and rebuilds each run"),
                        opt(
                            "Applying the same config repeatedly converges to the same "
                            "state - already-correct resources are left untouched",
                            correct=True,
                        ),
                        opt("It runs faster the second time"),
                    ),
                    "Idempotence lets you re-apply safely: only drift is corrected, so "
                    "the outcome is predictable.",
                ),
                q(
                    "In a declarative IaC file, what do you specify?",
                    (
                        opt("The exact shell commands to run in order"),
                        opt(
                            "The desired end state - the tool computes the steps to reach it",
                            correct=True,
                        ),
                        opt("Only the deletion steps"),
                        opt("The CPU instructions for the server"),
                    ),
                    "Declarative = describe what you want; the tool figures out how "
                    "(imperative would be the step-by-step how).",
                ),
            ),
        ),
        # -- 5. Containers & orchestration -----------------------------
        _t(
            "Containers and orchestration",
            "10 min",
            """# Containers and orchestration

A **container** packages an application together with everything it needs
to run - runtime, libraries, config - into one portable, isolated unit.
It runs the same on a laptop, a CI runner, and a production server,
solving "works on my machine." Containers are lighter than virtual
machines: they share the host kernel instead of each carrying a full OS.

You define a container image with a **Dockerfile**:

```dockerfile
# Dockerfile - a reproducible image for a Node app
FROM node:20-alpine        # base image
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev      # install only production deps
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]  # what runs when the container starts
```

`docker build` turns this into an **image** (a versioned artifact you can
push to a registry); `docker run` starts a **container** (a running
instance of the image).

One container is easy. Running *hundreds* across a fleet of machines -
restarting crashed ones, scaling with load, rolling out new versions
without downtime, connecting them - is **orchestration**, and the
standard is **Kubernetes**. You give Kubernetes a **declarative** desired
state and it continuously works to maintain it:

```yaml
# deployment.yaml - "keep 3 replicas of this image running"
apiVersion: apps/v1
kind: Deployment
metadata: { name: web }
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: web
          image: myregistry/web:1.4.0
```

If a container dies, Kubernetes starts a new one; if a node fails, it
reschedules the work elsewhere; ask for more replicas and it spreads them
across the cluster. It is IaC's idempotent, desired-state idea applied to
running workloads.

```mermaid
graph TD
    DF["Dockerfile"] --> IMG["Build image"]
    IMG --> REG["Push to registry"]
    REG --> K8S["Kubernetes desired state"]
    K8S --> P1["Pod replica"]
    K8S --> P2["Pod replica"]
    K8S --> HEAL["Self heal and scale"]
```

Remember: containers make one app portable and reproducible; orchestration
keeps many of them running the way you declared, automatically.
""",
        ),
        quiz_lesson(
            "Quiz: Containers and orchestration",
            (
                q(
                    "What problem does a container solve?",
                    (
                        opt("It makes code run without any server"),
                        opt(
                            "It packages an app with its runtime, libraries and config "
                            "into one portable unit that runs the same everywhere",
                            correct=True,
                        ),
                        opt("It encrypts the source code"),
                        opt("It replaces the need for testing"),
                    ),
                    "Containers end 'works on my machine' by shipping the environment "
                    "with the app - lighter than a VM (shared kernel).",
                ),
                q(
                    "What is the difference between a Docker image and a container?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "An image is the built, versioned artifact; a container is a "
                            "running instance of an image",
                            correct=True,
                        ),
                        opt("An image runs; a container is just a file"),
                        opt("A container is bigger than its image"),
                    ),
                    "docker build -> image (artifact in a registry); docker run -> "
                    "container (a live instance).",
                ),
                q(
                    "What does an orchestrator like Kubernetes do?",
                    (
                        opt("Compiles the application source code"),
                        opt("Writes the Dockerfile for you"),
                        opt(
                            "Maintains a declared desired state across a cluster - "
                            "restarting, rescheduling and scaling containers "
                            "automatically",
                            correct=True,
                        ),
                        opt("Runs only a single container on one machine"),
                    ),
                    "You declare the desired state (e.g. 3 replicas); Kubernetes "
                    "continuously reconciles reality to it.",
                ),
            ),
        ),
        # -- 6. Observability ------------------------------------------
        _t(
            "Observability - logs, metrics, traces",
            "10 min",
            """# Observability - logs, metrics, traces

Once software is running, you need to know **what it is doing and why**.
**Monitoring** asks known questions ("is CPU high? is the site up?");
**observability** is the broader ability to ask *new* questions about a
system from the outside - to debug problems you did not anticipate. It
rests on **three pillars**:

- **Logs** - timestamped records of discrete events ("order 123 failed:
  payment declined"). Great for the detail of *what happened*. Structure
  them (JSON) so they are searchable, not just human prose.
- **Metrics** - numeric measurements over time, aggregated ("requests per
  second", "p99 latency", "error rate"). Cheap to store, ideal for
  dashboards and alerts - the *health at a glance*.
- **Traces** - the path of a single request across services, with timing
  at each hop. In a distributed system, traces show *where* the time (or
  the failure) went.

Metrics tell you **something is wrong**; traces tell you **where**; logs
tell you **what** exactly. You use them together.

On top of the pillars sits **alerting**: rules on metrics that page a
human when something crosses a threshold - but alert on **symptoms users
feel** (error rate, latency), not every internal blip, or people learn to
ignore the pager ("alert fatigue"). A common toolchain: Prometheus
(metrics) + Grafana (dashboards) + a log store + a tracing system like
Jaeger or OpenTelemetry.

```mermaid
graph TD
    APP["Running services"] --> LOGS["Logs what happened"]
    APP --> METRICS["Metrics health over time"]
    APP --> TRACES["Traces where time went"]
    METRICS --> ALERT["Alert on user facing symptoms"]
    ALERT --> ONCALL["Page a human"]
    LOGS --> DEBUG["Debug the details"]
    TRACES --> DEBUG
```

Remember: you cannot operate what you cannot see. Metrics for health and
alerts, traces to localize, logs for the detail - the closing half of the
DevOps loop that feeds the next change.
""",
        ),
        quiz_lesson(
            "Quiz: Observability - logs, metrics, traces",
            (
                q(
                    "What are the three pillars of observability?",
                    (
                        opt("Build, test, deploy"),
                        opt("Logs, metrics, and traces", correct=True),
                        opt("Dev, staging, production"),
                        opt("CPU, memory, disk"),
                    ),
                    "Logs (events), metrics (numbers over time), traces (a request's "
                    "path across services).",
                ),
                q(
                    "Which pillar is best for a health dashboard and alerting?",
                    (
                        opt("Logs"),
                        opt("Traces"),
                        opt(
                            "Metrics - cheap numeric time series, ideal for dashboards and thresholds",
                            correct=True,
                        ),
                        opt("None - use screenshots"),
                    ),
                    "Metrics give health at a glance; traces localize a problem, logs "
                    "give the detail.",
                ),
                q(
                    "What is 'alert fatigue' and how do you avoid it?",
                    (
                        opt("Servers overheating - add fans"),
                        opt(
                            "People ignoring the pager because there are too many "
                            "alerts; avoid it by alerting on user-facing symptoms, not "
                            "every internal blip",
                            correct=True,
                        ),
                        opt("The pipeline running too slowly"),
                        opt("Logs filling the disk"),
                    ),
                    "Noisy alerts get ignored; page on symptoms users actually feel "
                    "(error rate, latency).",
                ),
            ),
        ),
        # -- 7. DORA / reliability -------------------------------------
        _t(
            "Reliability and DORA metrics",
            "10 min",
            """# Reliability and DORA metrics

How do you know your DevOps is actually working? The **DORA** metrics
(from the DevOps Research and Assessment program) are the industry
standard, and research shows the best teams are better at **both** speed
and stability - the old idea that you trade one for the other is false.

The **four key metrics**:

- **Deployment Frequency** - how often you release to production. Elite
  teams deploy on demand, many times a day. (Speed)
- **Lead Time for Changes** - how long from a commit to it running in
  production. Shorter is better. (Speed)
- **Change Failure Rate** - what fraction of deployments cause a problem
  needing remediation. Lower is better. (Stability)
- **Time to Restore Service** - how quickly you recover when something
  does break. Shorter is better. (Stability)

Speed metrics improve with CI/CD and small batches; stability metrics
improve with testing, good release strategies, and fast rollback - the
practices from the earlier lessons.

Reliability is also a **culture**, drawn largely from **Site Reliability
Engineering (SRE)**:

- **Error budgets** - 100% reliability is the wrong target; you set an
  objective (say 99.9%) and the allowed unreliability is a *budget* you
  can spend on shipping features. Fast enough and reliable enough, not
  perfect.
- **Blameless postmortems** - after an incident, analyze the *system and
  process* that let it happen, not the individual. People are honest only
  when they are not punished, and honesty is how you actually fix causes.
- **Automate toil** - repetitive manual operational work is "toil";
  automating it is how Ops scales without just adding people.

```mermaid
graph TD
    SPEED["Speed"] --> DF["Deployment frequency"]
    SPEED --> LT["Lead time for changes"]
    STAB["Stability"] --> CFR["Change failure rate"]
    STAB --> TTR["Time to restore service"]
    STAB --> EB["Error budgets"]
    STAB --> PM["Blameless postmortems"]
```

Remember: measure both speed and stability, spend an error budget rather
than chase perfection, and learn from failure without blame.
""",
        ),
        quiz_lesson(
            "Quiz: Reliability and DORA metrics",
            (
                q(
                    "Which set correctly lists the four DORA metrics?",
                    (
                        opt("CPU, memory, disk, network"),
                        opt(
                            "Deployment frequency, lead time for changes, change failure "
                            "rate, time to restore service",
                            correct=True,
                        ),
                        opt("Uptime, latency, cost, headcount"),
                        opt("Commits, branches, merges, tags"),
                    ),
                    "Two speed (frequency, lead time) and two stability (change failure "
                    "rate, time to restore) metrics.",
                ),
                q(
                    "What does DORA research say about speed vs stability?",
                    (
                        opt("You must trade one for the other"),
                        opt(
                            "The best teams excel at both - speed and stability go "
                            "together, they are not a trade-off",
                            correct=True,
                        ),
                        opt("Stability does not matter"),
                        opt("Only speed can be measured"),
                    ),
                    "Elite performers score high on both; the practices that speed you "
                    "up also make you more stable.",
                ),
                q(
                    "What is the point of an SRE 'error budget'?",
                    (
                        opt("To bill customers for downtime"),
                        opt("To fire whoever caused an outage"),
                        opt(
                            "100% reliability is the wrong target; you set an objective "
                            "and treat the allowed unreliability as a budget to spend on "
                            "shipping features",
                            correct=True,
                        ),
                        opt("To prevent any deployment ever"),
                    ),
                    "Reliable enough, not perfect - the budget balances new features "
                    "against stability. Blameless postmortems keep the learning honest.",
                ),
            ),
        ),
        # -- 8. Putting it together ------------------------------------
        _t(
            "Putting it together - commit to production",
            "9 min",
            """# Putting it together - commit to production

Every piece connects into one path: a change flows from a developer's
commit all the way to running, observed software - automatically, safely,
and with feedback that improves the next change.

Follow one change end to end:

1. **Commit** - a developer pushes a small change to version control.
2. **CI** - the pipeline builds the code and runs the tests; a red build
   blocks the change immediately.
3. **Artifact** - a passing build produces a versioned artifact (often a
   container image pushed to a registry) - built once.
4. **Delivery** - the same artifact is promoted to staging and verified.
5. **Deployment** - it is released to production with a safe strategy
   (canary or blue-green), on a fleet an orchestrator keeps healthy.
6. **Observe** - logs, metrics and traces show how it behaves for real
   users; alerts fire on symptoms; DORA metrics track speed and stability.
7. **Feedback** - what you learn in production feeds the next plan -
   closing the loop.

Underneath it all, **infrastructure as code** defines the environments
this runs on, so every stage is reproducible and reviewed.

```mermaid
graph LR
    COMMIT["Commit"] --> CI["CI build and test"]
    CI --> ART["Versioned artifact"]
    ART --> STG["Deliver to staging"]
    STG --> PROD["Safe deploy to production"]
    PROD --> OBS["Observe logs metrics traces"]
    OBS --> FEEDBACK["Feedback to next change"]
    FEEDBACK --> COMMIT
```

None of this requires mastering every tool at once. Start with CI on one
project, add automated deployment, put your infrastructure in code, and
add observability. Each step shortens the loop between an idea and
knowing whether it worked - which is the whole purpose of DevOps. The
tool courses in this track (Docker, Kubernetes, Terraform, Ansible) are
where you go deep on each piece from here.
""",
        ),
        quiz_lesson(
            "Quiz: Putting it together - commit to production",
            (
                q(
                    "In the end-to-end flow, what produces the artifact that gets deployed?",
                    (
                        opt("The developer builds it by hand on production"),
                        opt(
                            "A passing CI pipeline builds a versioned artifact once "
                            "(often a container image), which is then promoted",
                            correct=True,
                        ),
                        opt("Each environment builds its own from scratch"),
                        opt("The monitoring system generates it"),
                    ),
                    "Build once in CI, promote the same artifact through staging to production.",
                ),
                q(
                    "What closes the DevOps loop in the end-to-end path?",
                    (
                        opt("Deleting the old servers"),
                        opt(
                            "Feedback from observing production flows back into planning "
                            "the next change",
                            correct=True,
                        ),
                        opt("Rebuilding the artifact nightly"),
                        opt("Turning off alerts once deployed"),
                    ),
                    "Observe in production, learn, feed it into the next commit - flow "
                    "and feedback.",
                ),
                q(
                    "What is a sensible way to adopt DevOps on a project?",
                    (
                        opt("Adopt every tool at once on day one"),
                        opt(
                            "Start with CI, then automated deployment, then "
                            "infrastructure as code, then observability - each step "
                            "shortens the feedback loop",
                            correct=True,
                        ),
                        opt("Never change anything already working"),
                        opt("Only measure, never automate"),
                    ),
                    "Incremental adoption: each practice shortens the idea-to-feedback "
                    "loop, which is the point.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is DevOps?",
                    (
                        opt("A single automation tool"),
                        opt(
                            "A culture and set of practices for delivering software "
                            "quickly, safely and often, built on flow and feedback",
                            correct=True,
                        ),
                        opt("The team that only runs servers"),
                        opt("A cloud provider"),
                    ),
                    "Flow (idea to production) and feedback (production to next change) "
                    "- tools serve that goal.",
                ),
                q(
                    "What does Continuous Integration guarantee?",
                    (
                        opt("Automatic production deploys"),
                        opt(
                            "Every pushed change is built and tested automatically, "
                            "catching integration issues within minutes",
                            correct=True,
                        ),
                        opt("Zero bugs ever reach any branch"),
                        opt("Servers defined in code"),
                    ),
                    "CI is build+test on every push to a shared branch; it is the "
                    "foundation continuous delivery builds on.",
                ),
                q(
                    "Continuous Deployment differs from Continuous Delivery because it…",
                    (
                        opt("skips testing entirely"),
                        opt("only works for mobile apps"),
                        opt(
                            "releases every change that passes the pipeline to "
                            "production automatically, with no human gate",
                            correct=True,
                        ),
                        opt("requires manual builds"),
                    ),
                    "Delivery keeps builds releasable behind a button; deployment "
                    "presses the button automatically.",
                ),
                q(
                    "Why 'build once, promote the same artifact'?",
                    (
                        opt("To save disk space"),
                        opt(
                            "So production runs exactly what was tested in staging - "
                            "rebuilding per environment risks divergence",
                            correct=True,
                        ),
                        opt("Because artifacts cannot be copied"),
                        opt("It is a Kubernetes requirement"),
                    ),
                    "The tested artifact and the released artifact must be identical.",
                ),
                q(
                    "What makes an Infrastructure-as-Code tool 'idempotent'?",
                    (
                        opt("It runs exactly once"),
                        opt(
                            "Re-applying the same config converges to the same state; "
                            "already-correct resources are untouched",
                            correct=True,
                        ),
                        opt("It rebuilds everything each run"),
                        opt("It only creates, never updates"),
                    ),
                    "Idempotence makes re-applying safe: only drift is corrected.",
                ),
                q(
                    "What is the difference between a container image and a container?",
                    (
                        opt("Nothing"),
                        opt(
                            "The image is the built, versioned artifact; the container "
                            "is a running instance of it",
                            correct=True,
                        ),
                        opt("The container is stored in a registry, the image runs"),
                        opt("Images are only for Windows"),
                    ),
                    "docker build -> image; docker run -> container.",
                ),
                q(
                    "What does a container orchestrator like Kubernetes provide?",
                    (
                        opt("A code editor"),
                        opt(
                            "Maintaining a declared desired state across a cluster - "
                            "self-healing, scaling, and rescheduling containers",
                            correct=True,
                        ),
                        opt("A single container on one laptop"),
                        opt("A replacement for version control"),
                    ),
                    "Declare desired state (e.g. 3 replicas); Kubernetes reconciles "
                    "reality to it continuously.",
                ),
                q(
                    "Metrics tell you something is wrong, traces tell you where - what "
                    "do logs give you?",
                    (
                        opt("The exact detail of what happened for a specific event", correct=True),
                        opt("The CPU temperature"),
                        opt("The deployment frequency"),
                        opt("The Dockerfile"),
                    ),
                    "Logs are the detailed events; metrics are health, traces localize "
                    "across services - used together.",
                ),
                q(
                    "Which are the four DORA metrics?",
                    (
                        opt("Uptime, cost, headcount, latency"),
                        opt(
                            "Deployment frequency, lead time for changes, change failure "
                            "rate, time to restore service",
                            correct=True,
                        ),
                        opt("Commits, PRs, merges, releases"),
                        opt("CPU, memory, disk, network"),
                    ),
                    "Two speed, two stability - and elite teams excel at both.",
                ),
                q(
                    "What is the purpose of a blameless postmortem?",
                    (
                        opt("To identify who to fire"),
                        opt("To avoid ever writing about incidents"),
                        opt(
                            "To analyze the system and process that allowed an incident, "
                            "without blaming individuals, so causes get honestly fixed",
                            correct=True,
                        ),
                        opt("To increase the alert count"),
                    ),
                    "People are honest only when not punished; honesty is how you fix "
                    "the real, systemic causes.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

DEVOPS_FUNDAMENTALS_COURSES: tuple[SeedCourse, ...] = (_DEVOPS_FUNDAMENTALS,)
