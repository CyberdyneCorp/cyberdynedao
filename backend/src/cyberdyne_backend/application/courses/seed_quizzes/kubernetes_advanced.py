"""Curated quiz questions for the Kubernetes - Advanced course (per-lesson
checkpoints + a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Helm & extending the API": (
            q(
                "What is Helm described as in this lesson?",
                (
                    opt("A controller that reconciles custom resources"),
                    opt(
                        "The package manager that bundles many manifests into a templated chart",
                        correct=True,
                    ),
                    opt("A network policy engine that restricts Pod traffic"),
                    opt("A built-in Kubernetes object type for databases"),
                ),
                "Helm is the package manager that packages many manifests into a templated, versioned chart you install with one command.",
            ),
            q(
                "How does the lesson say a single Helm chart is parameterised across environments?",
                (
                    opt("By editing the chart source for each environment"),
                    opt("Through values supplied via values.yaml or --set", correct=True),
                    opt("By installing a separate operator per environment"),
                    opt("By defining a new CRD for every environment"),
                ),
                "Values supplied through values.yaml or --set parameterise the same chart across environments.",
            ),
            q(
                "According to the lesson, what is an operator?",
                (
                    opt(
                        "A controller that reconciles custom resources, encoding operational know-how",
                        correct=True,
                    ),
                    opt("A command that rolls back a Helm release to a prior revision"),
                    opt("A ServiceAccount that grants Pods least privilege"),
                    opt("A chart repository hosted by a vendor"),
                ),
                "An operator is a controller that reconciles CRDs, encoding operational know-how using the same desired-state pattern.",
            ),
        ),
        "RBAC & security": (
            q(
                "What does Role-Based Access Control govern in the lesson?",
                (
                    opt("How charts are versioned and rolled back"),
                    opt("Who and which Pods can do what", correct=True),
                    opt("How the scheduler reserves CPU and memory"),
                    opt("Which container image registries are trusted"),
                ),
                "RBAC governs who (and which Pods) can do what.",
            ),
            q(
                "What is a ServiceAccount according to the lesson?",
                (
                    opt("A Pod's identity, which should be granted least privilege", correct=True),
                    opt("A rule that lists allowed verbs on a resource"),
                    opt("A default-deny rule for Pod-to-Pod traffic"),
                    opt("A templated chart installed with one command"),
                ),
                "A ServiceAccount is a Pod's identity, and you grant it the least privilege it needs.",
            ),
            q(
                "How does the lesson say NetworkPolicies should be applied?",
                (
                    opt("Allow all traffic, then block known-bad sources"),
                    opt("Default-deny, then allow only what is required", correct=True),
                    opt("Only between Pods that share a ServiceAccount"),
                    opt("Only on Pods that run as non-root"),
                ),
                "NetworkPolicies should be default-deny, then allow only what is required.",
            ),
        ),
        "Production: probes, limits & rollouts": (
            q(
                "What does a livenessProbe do when it fails?",
                (
                    opt("Stops sending traffic to the container"),
                    opt("Restarts the container", correct=True),
                    opt("Rolls back the Deployment to the previous version"),
                    opt("Caps the container's CPU and memory"),
                ),
                "A livenessProbe restarts the container if it fails.",
            ),
            q(
                "According to the lesson, what role do resource requests play?",
                (
                    opt("They cap the maximum CPU and memory a container can use"),
                    opt("They drive scheduling and the HPA by reserving capacity", correct=True),
                    opt("They restart the container when health checks fail"),
                    opt("They define which Pods may talk to which"),
                ),
                "Requests drive scheduling and the HPA; the scheduler reserves the requested capacity.",
            ),
            q(
                "Which command instantly reverts a Deployment to its previous version?",
                (
                    opt("kubectl rollout status deployment/web"),
                    opt("kubectl rollout undo deployment/web", correct=True),
                    opt("helm rollback web 1"),
                    opt("kubectl rollout restart deployment/web"),
                ),
                "kubectl rollout undo deployment/web rolls back a Deployment to its previous version instantly.",
            ),
        ),
    },
    final=(
        q(
            "Which tool packages many manifests into a templated, versioned chart?",
            (
                opt("An operator"),
                opt("Helm", correct=True),
                opt("A NetworkPolicy"),
                opt("Argo CD"),
            ),
            "Helm is the package manager that bundles manifests into a templated, versioned chart.",
        ),
        q(
            "What lets you teach Kubernetes new object types?",
            (
                opt("Custom Resource Definitions (CRDs)", correct=True),
                opt("Resource requests and limits"),
                opt("Readiness probes"),
                opt("RoleBindings"),
            ),
            "CRDs let you add new object types, and an operator reconciles them.",
        ),
        q(
            "Under RBAC, what should you grant a ServiceAccount?",
            (
                opt("Cluster-admin so Pods never hit permission errors"),
                opt("The least privilege it needs", correct=True),
                opt("Access only during business hours"),
                opt("The same role as every other Pod"),
            ),
            "A ServiceAccount is a Pod's identity and should be granted the least privilege it needs.",
        ),
        q(
            "Which probe controls whether a Pod receives traffic?",
            (
                opt("livenessProbe"),
                opt("readinessProbe", correct=True),
                opt("startupProbe"),
                opt("healthProbe"),
            ),
            "The readinessProbe only sends traffic to the Pod when it passes.",
        ),
        q(
            "What does pairing rollouts with GitOps tools like Argo CD or Flux achieve?",
            (
                opt(
                    "It keeps the cluster's state matching a git repo for auditable, reproducible operations",
                    correct=True,
                ),
                opt("It removes the need for resource requests and limits"),
                opt("It replaces RBAC with network policies"),
                opt("It packages manifests into Helm charts automatically"),
            ),
            "GitOps keeps the cluster's state matching a git repo, making operations auditable and reproducible.",
        ),
    ),
)
