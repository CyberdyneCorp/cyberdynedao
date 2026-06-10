"""Curated quiz questions for the Kubernetes - Basics course (per-lesson
checkpoints keyed by the EXACT content-lesson title, plus a final comprehensive
quiz). Grounded entirely in the lesson bodies in ``seed_devops``."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why Kubernetes?": (
            q(
                "How does Kubernetes differ from plain Docker according to the lesson?",
                (
                    opt("It runs containers on a single machine only"),
                    opt(
                        "It runs containers across a fleet of machines and keeps them running",
                        correct=True,
                    ),
                    opt("It replaces containers with virtual machines"),
                    opt("It builds container images faster than Docker"),
                ),
                "Docker runs containers on one machine while Kubernetes runs them across a fleet and keeps them running.",
            ),
            q(
                "What two parts make up a Kubernetes cluster as described?",
                (
                    opt("A registry and a build server"),
                    opt("A hypervisor and guest operating systems"),
                    opt(
                        "A set of nodes (machines) plus a control plane that decides what runs where",
                        correct=True,
                    ),
                    opt("A load balancer and a single Pod"),
                ),
                "A cluster is a set of nodes plus a control plane that decides what runs where.",
            ),
            q(
                "How do you tell Kubernetes what you want running?",
                (
                    opt(
                        "You describe the desired state in YAML and K8s reconciles reality to match it",
                        correct=True,
                    ),
                    opt("You manually start each container on every node by hand"),
                    opt("You edit the kernel configuration directly"),
                    opt("You write imperative shell scripts that run on a timer"),
                ),
                "You describe the desired state in YAML and Kubernetes continuously reconciles reality to match it.",
            ),
        ),
        "Pods, Deployments & ReplicaSets": (
            q(
                "What is the smallest deployable unit in Kubernetes?",
                (
                    opt("A ReplicaSet"),
                    opt("A Deployment"),
                    opt(
                        "A Pod - one or a few tightly-coupled containers sharing network and storage",
                        correct=True,
                    ),
                    opt("A Service"),
                ),
                "A Pod is the smallest deployable unit, holding one or a few tightly-coupled containers that share a network and storage.",
            ),
            q(
                "What does a Deployment create to keep N identical Pods running?",
                (
                    opt("A Service"),
                    opt("A ReplicaSet", correct=True),
                    opt("A ConfigMap"),
                    opt("A namespace"),
                ),
                "A Deployment manages Pods by creating a ReplicaSet that keeps N identical Pods running and handles rolling updates.",
            ),
            q(
                "What happens when you delete a Pod managed by a Deployment?",
                (
                    opt("The Deployment is also deleted"),
                    opt("Nothing replaces it until you re-apply the YAML"),
                    opt(
                        "The Deployment immediately recreates it, demonstrating self-healing",
                        correct=True,
                    ),
                    opt("The whole cluster restarts"),
                ),
                "Deleting a Pod triggers the Deployment to immediately recreate it, which is self-healing.",
            ),
        ),
        "Services & kubectl": (
            q(
                "Why do Pods need a Service in front of them?",
                (
                    opt("Pods cannot run more than one container without a Service"),
                    opt(
                        "Pods are ephemeral and get new IPs when recreated, so a Service gives a stable name and address",
                        correct=True,
                    ),
                    opt("A Service is required to build the container image"),
                    opt("Without a Service a Pod cannot read its logs"),
                ),
                "Pods are ephemeral and get new IPs when recreated, so a Service gives a stable name and address and load-balances across them.",
            ),
            q(
                "Which Service type is reachable only inside the cluster and is the default?",
                (
                    opt("ClusterIP", correct=True),
                    opt("NodePort"),
                    opt("LoadBalancer"),
                    opt("Ingress"),
                ),
                "ClusterIP is the default Service type and is reachable only inside the cluster.",
            ),
            q(
                "What does the kubectl logs command with -f do?",
                (
                    opt("It deletes the Pod's logs"),
                    opt("It streams a Pod's logs", correct=True),
                    opt("It creates resources from a YAML file"),
                    opt("It opens an interactive shell in the Pod"),
                ),
                "kubectl logs <pod> -f streams the Pod's logs.",
            ),
        ),
    },
    final=(
        q(
            "What core model makes Kubernetes restart crashed containers and reschedule them when a machine dies?",
            (
                opt("Imperative scripting run on each node"),
                opt(
                    "A declarative, self-healing model that reconciles reality to the desired state",
                    correct=True,
                ),
                opt("Manual operator intervention for every failure"),
                opt("Virtual machine snapshots taken on a schedule"),
            ),
            "Kubernetes uses a declarative, self-healing model that continuously reconciles reality to match the desired state.",
        ),
        q(
            "Which object manages Pods by creating a ReplicaSet and handling rolling updates?",
            (
                opt("A Service"),
                opt("A Deployment", correct=True),
                opt("A ClusterIP"),
                opt("A node"),
            ),
            "A Deployment manages Pods by creating a ReplicaSet and handling rolling updates.",
        ),
        q(
            "How do you scale a Deployment named web to five replicas?",
            (
                opt("kubectl scale deployment/web --replicas=5", correct=True),
                opt("kubectl logs deployment/web --replicas=5"),
                opt("kubectl describe deployment/web --replicas=5"),
                opt("docker run -d --replicas=5 web"),
            ),
            "kubectl scale deployment/web --replicas=5 sets the Deployment to five Pods.",
        ),
        q(
            "What does a Service do for the set of Pods it targets?",
            (
                opt("It builds their container images"),
                opt(
                    "It gives a stable name and address and load-balances across the matching Pods",
                    correct=True,
                ),
                opt("It stores their persistent data"),
                opt("It runs them on a single dedicated node"),
            ),
            "A Service gives a stable name and address and load-balances across the Pods matching its selector.",
        ),
        q(
            "Why is kubectl apply described as declarative?",
            (
                opt("It only works the first time and errors on re-runs"),
                opt(
                    "Re-applying converges the cluster to the file's desired state",
                    correct=True,
                ),
                opt("It deletes all resources before creating new ones"),
                opt("It requires manual confirmation for every change"),
            ),
            "kubectl apply is declarative because re-applying converges the cluster to the manifest file's state.",
        ),
    ),
)
