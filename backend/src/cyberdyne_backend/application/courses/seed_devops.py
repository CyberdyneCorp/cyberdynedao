"""Curated DevOps courses: Docker and Kubernetes, each at basic, intermediate,
and advanced levels.

Grounded in the user's Obsidian `Infrastructure/Docker and Kubernetes` vault.
Lessons are `text` with syntax-highlighted code fences (bash / dockerfile /
yaml) — there's no Docker/K8s runtime in the Academy, so commands are
illustrative. Each course ends with a knowledge-check quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="3 min")


# ── Docker ───────────────────────────────────────────────────────────────────

_DOCKER_BASICS = SeedCourse(
    slug="docker-basics",
    title="Docker — Basics",
    description=(
        "Containers from zero: what Docker is and how it differs from VMs, working "
        "with images and containers, and writing your first Dockerfile."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Containers vs. virtual machines",
            "8 min",
            """\
# Containers vs. virtual machines

Docker packages an app **and its dependencies** into a **container** — a
lightweight, isolated process that runs the same on any machine. "Works on my
machine" disappears.

```mermaid
flowchart TB
  subgraph VM[Virtual machines]
    H1[Hardware] --> HV[Hypervisor] --> G1[Guest OS + App] & G2[Guest OS + App]
  end
  subgraph C[Containers]
    H2[Hardware] --> OS[Host OS] --> D[Docker Engine] --> A1[App] & A2[App]
  end
```

- A **VM** virtualises hardware and ships a whole guest OS — heavy (GBs, slow
  to boot).
- A **container** shares the host kernel and isolates just the process — light
  (MBs, starts in milliseconds).

Three core ideas:

- **Image** — a read-only template (your app + dependencies).
- **Container** — a running instance of an image.
- **Registry** — where images are stored and shared (e.g. Docker Hub).

**Next:** running images and managing containers.
""",
        ),
        _t(
            "Images & containers",
            "9 min",
            """\
# Images & containers

```bash
docker pull nginx              # fetch an image from a registry
docker images                  # list local images

docker run -d -p 8080:80 nginx # run detached, map host:container port
docker ps                      # list running containers
docker ps -a                   # include stopped ones

docker logs <id>               # view output
docker exec -it <id> sh        # shell into a running container
docker stop <id> && docker rm <id>
```

- `-d` detaches (runs in the background); `-p 8080:80` exposes the container's
  port 80 on the host's 8080.
- `-it` gives you an interactive terminal.
- Containers are **ephemeral** — when one is removed, changes inside it are
  gone (unless you use a volume — intermediate course).

`docker run` = pull (if needed) + create + start, in one command.

**Next:** building your own image with a Dockerfile.
""",
        ),
        _t(
            "Your first Dockerfile",
            "10 min",
            """\
# Your first Dockerfile

A **Dockerfile** is a recipe that builds an image, layer by layer.

```dockerfile
FROM node:20-slim          # base image
WORKDIR /app               # working directory inside the image
COPY package*.json ./      # copy dependency manifests first (caching!)
RUN npm install            # install deps as a layer
COPY . .                   # then copy the rest of the source
EXPOSE 3000
CMD ["node", "server.js"]  # the process to run on start
```

Build and run it:

```bash
docker build -t myapp:1.0 .
docker run -p 3000:3000 myapp:1.0
```

- Each instruction creates a cached **layer**; Docker reuses unchanged layers,
  so copying `package.json` before the source means `npm install` only re-runs
  when dependencies change.
- `CMD` is the default command; `RUN` executes at build time.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_DOCKER_INTERMEDIATE = SeedCourse(
    slug="docker-intermediate",
    title="Docker — Intermediate",
    description=(
        "Make containers production-ready: persisting data with volumes, container "
        "networking, and orchestrating multi-container apps with Docker Compose."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Volumes & persistent data",
            "9 min",
            """\
# Volumes & persistent data

Containers are ephemeral — delete one and its filesystem changes vanish.
**Volumes** store data outside the container's lifecycle.

```bash
docker volume create pgdata
docker run -d -v pgdata:/var/lib/postgresql/data postgres   # named volume

docker run -v $(pwd)/site:/usr/share/nginx/html nginx       # bind mount
```

- A **named volume** is managed by Docker — best for databases.
- A **bind mount** maps a host folder into the container — great for live-
  reloading source in development.

The same `-v host:container` syntax works for both; data survives container
restarts and removals.

**Next:** how containers talk to each other.
""",
        ),
        _t(
            "Networking",
            "9 min",
            """\
# Networking

Each container gets its own network namespace. Docker **networks** let
containers find and talk to each other by name.

```bash
docker network create appnet
docker run -d --name db --network appnet postgres
docker run -d --name api --network appnet myapi
```

On a user-defined network, containers resolve each other by **container name**
as a hostname — the `api` container reaches the database at `db:5432`, no IPs
needed.

- `-p 8080:80` publishes a port to the **host** (outside world).
- Containers on the same network reach each other **without** publishing ports.

Keeping internal services off published ports (only the gateway is exposed) is
a simple, strong security default.

**Next:** wiring it all together with Compose.
""",
        ),
        _t(
            "Docker Compose",
            "10 min",
            """\
# Docker Compose

Real apps are several containers (web + db + cache). **Compose** declares them
in one YAML file and runs them together.

```yaml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://app:secret@db:5432/app
    depends_on:
      - db
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker compose up -d     # build + start everything
docker compose logs -f
docker compose down      # stop + remove (add -v to drop volumes)
```

Compose creates a shared network automatically, so `api` reaches `db` by name.
One file, one command — reproducible local stacks.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_DOCKER_ADVANCED = SeedCourse(
    slug="docker-advanced",
    title="Docker — Advanced",
    description=(
        "Ship lean, secure images: multi-stage builds, image-size and security "
        "hardening, and registries/BuildKit on the path to orchestration."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Multi-stage builds & tiny images",
            "10 min",
            """\
# Multi-stage builds & tiny images

A build needs compilers and dev tools; the final image shouldn't ship them. A
**multi-stage build** compiles in one stage and copies only the artifact into a
minimal runtime stage.

```dockerfile
# stage 1: build
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app ./cmd/server

# stage 2: runtime (tiny, no toolchain)
FROM gcr.io/distroless/static
COPY --from=build /app /app
ENTRYPOINT ["/app"]
```

- `COPY --from=build` pulls just the binary from the earlier stage.
- A **distroless** or `alpine`/`slim` base drops the shell and package
  manager — images go from ~800MB to a few MB.
- Smaller images pull faster, start faster, and have a smaller attack surface.

Add a `.dockerignore` so build context stays small and secrets don't leak in.

**Next:** security hardening.
""",
        ),
        _t(
            "Security & hardening",
            "9 min",
            """\
# Security & hardening

Containers share the host kernel, so a careless image is a real risk.

```dockerfile
FROM node:20-slim
RUN useradd -m app
USER app                       # don't run as root
```

Best practices:

- **Run as a non-root user** (`USER`) — root in the container is dangerous if
  it escapes.
- **Pin versions** (`node:20.11-slim`, not `latest`) for reproducible builds.
- **Don't bake secrets** into images or `ENV`; inject them at runtime
  (`--env-file`, Docker/K8s secrets, or BuildKit `--secret`).
- **Scan images** for known CVEs:

```bash
docker scout cves myapp:1.0
trivy image myapp:1.0
```

- Prefer **read-only** filesystems and drop Linux capabilities
  (`--read-only`, `--cap-drop ALL`) where you can.

A minimal base image (previous lesson) is itself a security win — fewer
packages, fewer vulnerabilities.

**Next:** registries, BuildKit, and the handoff to orchestration.
""",
        ),
        _t(
            "Registries, BuildKit & orchestration",
            "9 min",
            """\
# Registries, BuildKit & orchestration

## Registries

Images are shared through registries (Docker Hub, GHCR, ECR):

```bash
docker tag myapp:1.0 ghcr.io/acme/myapp:1.0
docker push ghcr.io/acme/myapp:1.0
docker pull ghcr.io/acme/myapp:1.0
```

Tag immutably (a git SHA or version), not just `latest`, so deploys are
reproducible.

## BuildKit & multi-arch

Modern builds use **BuildKit** (`buildx`) for caching, secrets, and building
for multiple CPU architectures:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/acme/myapp:1.0 --push .
```

## Beyond a single host

`docker compose` runs containers on **one** machine. To run across many
machines with self-healing, scaling, and rolling updates, you hand off to an
**orchestrator** — Kubernetes.

**Next:** test what you've learned. Then start the Kubernetes track.
""",
        ),
        _quiz(),
    ),
)

# ── Kubernetes ───────────────────────────────────────────────────────────────

_K8S_BASICS = SeedCourse(
    slug="kubernetes-basics",
    title="Kubernetes — Basics",
    description=(
        "Container orchestration from the ground up: what a cluster is, the core "
        "objects (Pods, Deployments), exposing apps with Services, and driving it "
        "all with kubectl."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why Kubernetes?",
            "8 min",
            """\
# Why Kubernetes?

Docker runs containers on one machine. **Kubernetes (K8s)** runs them across a
fleet — and keeps them running: it restarts crashed containers, reschedules
them when a machine dies, scales them up and down, and rolls out new versions
without downtime.

```mermaid
flowchart TB
  CP[Control plane: API server, scheduler, etcd] --> N1[Node 1]
  CP --> N2[Node 2]
  N1 --> P1[Pod] & P2[Pod]
  N2 --> P3[Pod]
```

- A **cluster** is a set of **nodes** (machines) plus a **control plane** that
  decides what runs where.
- You describe the **desired state** in YAML ("3 replicas of this image"); K8s
  continuously reconciles reality to match it.

That declarative, self-healing model is the whole point.

**Next:** the smallest unit you deploy — Pods, via Deployments.
""",
        ),
        _t(
            "Pods, Deployments & ReplicaSets",
            "10 min",
            """\
# Pods, Deployments & ReplicaSets

- A **Pod** is the smallest deployable unit — one (or a few tightly-coupled)
  containers sharing a network and storage. Pods are disposable.
- A **Deployment** manages Pods for you: it creates a **ReplicaSet** that keeps
  N identical Pods running and handles rolling updates.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
        - name: web
          image: nginx:1.27
          ports:
            - containerPort: 80
```

```bash
kubectl apply -f web.yaml
kubectl get pods            # three web-... pods
kubectl scale deployment/web --replicas=5
```

Delete a Pod and the Deployment immediately recreates it — that's self-healing.

**Next:** giving Pods a stable address with Services.
""",
        ),
        _t(
            "Services & kubectl",
            "9 min",
            """\
# Services & kubectl

Pods are ephemeral and get new IPs when recreated. A **Service** gives a stable
name and address, load-balancing across the matching Pods.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector: { app: web }      # targets pods with this label
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP             # internal; LoadBalancer for external
```

- **ClusterIP** — reachable only inside the cluster (the default).
- **NodePort / LoadBalancer** — expose externally.

## Everyday kubectl

```bash
kubectl get pods,svc,deploy        # list resources
kubectl describe pod <name>        # detail + events
kubectl logs <pod> -f              # stream logs
kubectl exec -it <pod> -- sh       # shell in
kubectl apply -f manifest.yaml     # create/update from YAML
```

`kubectl apply` is declarative — re-applying converges to the file's state.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_K8S_INTERMEDIATE = SeedCourse(
    slug="kubernetes-intermediate",
    title="Kubernetes — Intermediate",
    description=(
        "Configure and operate real workloads: ConfigMaps and Secrets, persistent "
        "storage, and exposing + autoscaling apps with Ingress and the HPA."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Config & Secrets",
            "9 min",
            """\
# Config & Secrets

Keep configuration out of your image. **ConfigMaps** hold non-sensitive config;
**Secrets** hold sensitive values (base64-encoded, and can be encrypted at
rest).

```yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: app-config }
data:
  LOG_LEVEL: "info"
---
apiVersion: v1
kind: Secret
metadata: { name: app-secret }
type: Opaque
stringData:
  DATABASE_PASSWORD: "s3cret"
```

Inject them into a Pod as environment variables (or mounted files):

```yaml
envFrom:
  - configMapRef: { name: app-config }
  - secretRef:    { name: app-secret }
```

Now the same image runs in dev/staging/prod with different config — no rebuild.

**Next:** persistent storage.
""",
        ),
        _t(
            "Storage: volumes & PersistentVolumes",
            "9 min",
            """\
# Storage: volumes & PersistentVolumes

A Pod's filesystem dies with it. For data that must survive, Kubernetes
separates the **request** from the **supply**:

- a **PersistentVolume (PV)** is a piece of storage in the cluster;
- a **PersistentVolumeClaim (PVC)** is a Pod's request for storage;
- a **StorageClass** provisions PVs automatically (dynamic provisioning).

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: data }
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests: { storage: 5Gi }
```

Mount the claim in a Pod:

```yaml
volumes:
  - name: data
    persistentVolumeClaim: { claimName: data }
```

For stateful apps with stable identity (databases), use a **StatefulSet** with
per-Pod PVCs rather than a plain Deployment.

**Next:** exposing and scaling apps.
""",
        ),
        _t(
            "Ingress & autoscaling",
            "9 min",
            """\
# Ingress & autoscaling

## Ingress

A `LoadBalancer` Service per app is expensive. An **Ingress** is one HTTP entry
point that routes by host/path to many Services (handled by an ingress
controller like NGINX or Traefik):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: { name: site }
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service: { name: web, port: { number: 80 } }
```

## Horizontal Pod Autoscaler

The **HPA** adds/removes Pod replicas based on load (needs resource requests
set):

```bash
kubectl autoscale deployment web --cpu-percent=70 --min=2 --max=10
```

CPU above 70% → scale out; load drops → scale back in. Use **namespaces** to
isolate teams/environments within one cluster.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_K8S_ADVANCED = SeedCourse(
    slug="kubernetes-advanced",
    title="Kubernetes — Advanced",
    description=(
        "Operate Kubernetes in production: packaging with Helm and extending the "
        "API with operators/CRDs, locking it down with RBAC, and running reliably "
        "with probes, limits and rollouts."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Helm & extending the API",
            "10 min",
            """\
# Helm & extending the API

## Helm — the package manager

Real apps are many manifests. **Helm** packages them into a templated, version-
ed **chart** you install with one command:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install mydb bitnami/postgresql --set auth.password=secret
helm upgrade mydb bitnami/postgresql --set primary.persistence.size=20Gi
helm rollback mydb 1
```

Values (`values.yaml` / `--set`) parameterise the same chart across
environments.

## Operators & CRDs

You can teach Kubernetes new object types with **Custom Resource Definitions
(CRDs)**, and an **operator** is a controller that reconciles them — encoding
operational know-how (e.g. "a `PostgresCluster` resource that manages backups
and failover"). It's the same desired-state pattern, extended to your own
domain.

**Next:** access control with RBAC.
""",
        ),
        _t(
            "RBAC & security",
            "9 min",
            """\
# RBAC & security

**Role-Based Access Control** governs who (and which Pods) can do what.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { namespace: app, name: pod-reader }
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata: { namespace: app, name: read-pods }
subjects:
  - kind: ServiceAccount
    name: my-app
roleBinding: {}        # binds the Role to the ServiceAccount
```

- A **ServiceAccount** is a Pod's identity; grant it the **least privilege** it
  needs.
- **NetworkPolicies** restrict which Pods can talk to which — default-deny, then
  allow only what's required.
- Add **Pod Security Standards** (non-root, no privilege escalation) and keep
  secrets in a real secret store.

**Next:** running reliably in production.
""",
        ),
        _t(
            "Production: probes, limits & rollouts",
            "10 min",
            """\
# Production: probes, limits & rollouts

## Health probes

Kubernetes needs to know if your app is alive and ready:

```yaml
livenessProbe:                 # restart the container if this fails
  httpGet: { path: /healthz, port: 8080 }
readinessProbe:                # only send traffic when this passes
  httpGet: { path: /ready, port: 8080 }
```

## Resource requests & limits

```yaml
resources:
  requests: { cpu: "100m", memory: "128Mi" }   # scheduler reserves this
  limits:   { cpu: "500m", memory: "256Mi" }   # capped here
```

Requests drive scheduling and the HPA; limits prevent a noisy neighbour from
starving the node.

## Rollouts

Deployments roll out new versions gradually and can roll back instantly:

```bash
kubectl rollout status deployment/web
kubectl rollout undo deployment/web
```

Pair this with GitOps (Argo CD / Flux) so the cluster's state always matches a
git repo — auditable, reproducible operations.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


DEVOPS_COURSES: tuple[SeedCourse, ...] = (
    _DOCKER_BASICS,
    _DOCKER_INTERMEDIATE,
    _DOCKER_ADVANCED,
    _K8S_BASICS,
    _K8S_INTERMEDIATE,
    _K8S_ADVANCED,
)

__all__ = ["DEVOPS_COURSES"]
