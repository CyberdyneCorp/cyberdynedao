"""Curated quiz questions for the Kubernetes - Intermediate course
(per-lesson checkpoints plus a final comprehensive quiz). Keys are the EXACT
content-lesson titles so the seed can interleave a checkpoint quiz after each."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Config & Secrets": (
            q(
                "What kind of values are ConfigMaps meant to hold?",
                (
                    opt("Sensitive values like database passwords"),
                    opt("Non-sensitive configuration", correct=True),
                    opt("Container images for the registry"),
                    opt("Persistent storage volumes"),
                ),
                "ConfigMaps hold non-sensitive config while Secrets hold sensitive values.",
            ),
            q(
                "How are Secret values stored according to the lesson?",
                (
                    opt("base64-encoded, and can be encrypted at rest", correct=True),
                    opt("Encrypted with the cluster TLS certificate only"),
                    opt("As plain text inside the container image"),
                    opt("Compressed and stored in the ConfigMap"),
                ),
                "Secrets hold sensitive values that are base64-encoded and can be encrypted at rest.",
            ),
            q(
                "What benefit does injecting config via ConfigMaps and Secrets provide?",
                (
                    opt("It encrypts all network traffic between Pods"),
                    opt("It automatically scales the Pod under load"),
                    opt(
                        "The same image runs in dev/staging/prod with different config, no rebuild",
                        correct=True,
                    ),
                    opt("It removes the need for a container registry"),
                ),
                "Keeping config out of the image lets the same image run across environments with different config and no rebuild.",
            ),
        ),
        "Storage: volumes & PersistentVolumes": (
            q(
                "What is a PersistentVolumeClaim (PVC)?",
                (
                    opt("A Pod's request for storage", correct=True),
                    opt("A piece of storage in the cluster"),
                    opt("A controller that reconciles custom resources"),
                    opt("An HTTP entry point that routes by host"),
                ),
                "A PVC is a Pod's request for storage, while a PV is the actual piece of storage in the cluster.",
            ),
            q(
                "What does a StorageClass do?",
                (
                    opt("It restricts which Pods can talk to which"),
                    opt("It provisions PVs automatically via dynamic provisioning", correct=True),
                    opt("It caps the CPU and memory a Pod can use"),
                    opt("It mounts a ConfigMap as a file"),
                ),
                "A StorageClass provisions PVs automatically, which is dynamic provisioning.",
            ),
            q(
                "For stateful apps with stable identity such as databases, what should you use?",
                (
                    opt("A plain Deployment with a shared volume"),
                    opt("A LoadBalancer Service per Pod"),
                    opt("A StatefulSet with per-Pod PVCs", correct=True),
                    opt("A DaemonSet across every node"),
                ),
                "Stateful apps with stable identity should use a StatefulSet with per-Pod PVCs rather than a plain Deployment.",
            ),
        ),
        "Ingress & autoscaling": (
            q(
                "Why use an Ingress instead of a LoadBalancer Service per app?",
                (
                    opt(
                        "One HTTP entry point routes by host/path to many Services",
                        correct=True,
                    ),
                    opt("It encrypts data at rest on persistent volumes"),
                    opt("It provisions PVs automatically for each Service"),
                    opt("It restarts containers when a health check fails"),
                ),
                "An Ingress is one HTTP entry point that routes by host/path to many Services, avoiding a costly LoadBalancer per app.",
            ),
            q(
                "What does the Horizontal Pod Autoscaler (HPA) require to work?",
                (
                    opt("A StatefulSet instead of a Deployment"),
                    opt("Resource requests set on the Pods", correct=True),
                    opt("A NetworkPolicy allowing all traffic"),
                    opt("An encrypted Secret store"),
                ),
                "The HPA adds and removes Pod replicas based on load and needs resource requests set.",
            ),
            q(
                "With the example autoscale command, what happens when CPU goes above 70%?",
                (
                    opt("The Deployment rolls back to the previous version"),
                    opt("Traffic is blocked until CPU drops"),
                    opt("The HPA scales out by adding replicas", correct=True),
                    opt("The Pod is restarted by the liveness probe"),
                ),
                "CPU above 70% triggers scale out, and when load drops the HPA scales back in.",
            ),
        ),
    },
    final=(
        q(
            "Which object holds non-sensitive configuration injected into a Pod?",
            (
                opt("Secret"),
                opt("ConfigMap", correct=True),
                opt("PersistentVolume"),
                opt("Ingress"),
            ),
            "ConfigMaps hold non-sensitive config while Secrets hold sensitive values.",
        ),
        q(
            "In the PV/PVC model, which separates the request from the supply of storage?",
            (
                opt("A PV is the request and a PVC is the supply"),
                opt(
                    "A PVC is the Pod's request and a PV is the storage in the cluster",
                    correct=True,
                ),
                opt("A StorageClass is the request and a PVC is the supply"),
                opt("A StatefulSet is the request and a Deployment is the supply"),
            ),
            "A PVC is the Pod's request for storage and a PV is the piece of storage in the cluster.",
        ),
        q(
            "What is the purpose of an Ingress?",
            (
                opt(
                    "To provide one HTTP entry point routing by host/path to many Services",
                    correct=True,
                ),
                opt("To provision persistent volumes dynamically"),
                opt("To give each Pod a stable network identity"),
                opt("To cap a Pod's CPU and memory usage"),
            ),
            "An Ingress is a single HTTP entry point that routes by host and path to many Services via an ingress controller.",
        ),
        q(
            "What does the HPA do and what does it need?",
            (
                opt("It encrypts secrets at rest and needs a StorageClass"),
                opt(
                    "It adds/removes Pod replicas based on load and needs resource requests set",
                    correct=True,
                ),
                opt("It routes HTTP traffic and needs an ingress controller"),
                opt("It provisions PVs and needs a PersistentVolumeClaim"),
            ),
            "The HPA adds and removes Pod replicas based on load and requires resource requests to be set.",
        ),
        q(
            "What are namespaces used for within one cluster?",
            (
                opt("To provision storage automatically"),
                opt("To isolate teams/environments within one cluster", correct=True),
                opt("To route HTTP traffic to Services"),
                opt("To encode Secret values in base64"),
            ),
            "Namespaces are used to isolate teams and environments within a single cluster.",
        ),
    ),
)
