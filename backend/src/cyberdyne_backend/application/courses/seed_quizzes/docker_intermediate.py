"""Curated quiz questions for the Docker - Intermediate course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each one."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Volumes & persistent data": (
            q(
                "Why do you need volumes for container data?",
                (
                    opt("Containers cannot write to their own filesystem at all"),
                    opt(
                        "Containers are ephemeral, so filesystem changes vanish when one is deleted",
                        correct=True,
                    ),
                    opt("Volumes make containers start faster"),
                    opt("Volumes are required before a container can be built"),
                ),
                "Volumes store data outside the container's lifecycle, so it survives deletion.",
            ),
            q(
                "Which volume type does the lesson recommend as best for databases?",
                (
                    opt("A bind mount"),
                    opt("A tmpfs mount"),
                    opt("A named volume managed by Docker", correct=True),
                    opt("A read-only mount"),
                ),
                "A named volume is managed by Docker and is described as best for databases.",
            ),
            q(
                "What is a bind mount good for according to the lesson?",
                (
                    opt("Live-reloading source in development", correct=True),
                    opt("Encrypting data at rest"),
                    opt("Sharing data between unrelated registries"),
                    opt("Replacing the container's base image"),
                ),
                "A bind mount maps a host folder into the container, great for live-reloading source in development.",
            ),
        ),
        "Networking": (
            q(
                "On a user-defined network, how do containers find each other?",
                (
                    opt("By their published host port number"),
                    opt("By their container name used as a hostname", correct=True),
                    opt("By a fixed IP address you must assign"),
                    opt("By the image name they were built from"),
                ),
                "On a user-defined network, containers resolve each other by container name as a hostname.",
            ),
            q(
                "What does the flag -p 8080:80 do?",
                (
                    opt("Connects two containers on the same network"),
                    opt("Creates a new named volume"),
                    opt(
                        "Publishes a container port to the host so the outside world can reach it",
                        correct=True,
                    ),
                    opt("Limits the container to 80 MB of memory"),
                ),
                "-p 8080:80 publishes a port to the host, exposing it to the outside world.",
            ),
            q(
                "What simple security default does the lesson recommend?",
                (
                    opt(
                        "Keep internal services off published ports and expose only the gateway",
                        correct=True,
                    ),
                    opt("Publish every container port so monitoring is easier"),
                    opt("Assign each container a static public IP"),
                    opt("Disable all container networking"),
                ),
                "Keeping internal services off published ports, with only the gateway exposed, is a strong security default.",
            ),
        ),
        "Docker Compose": (
            q(
                "What does Docker Compose declare in one YAML file?",
                (
                    opt("A single container's build instructions only"),
                    opt("Multiple containers that run together as one app", correct=True),
                    opt("The host kernel modules to load"),
                    opt("The registry credentials for pushing images"),
                ),
                "Compose declares several containers, such as web plus db plus cache, in one YAML file and runs them together.",
            ),
            q(
                "Which command builds and starts everything in the background?",
                (
                    opt("docker compose logs -f"),
                    opt("docker compose down"),
                    opt("docker compose up -d", correct=True),
                    opt("docker compose build"),
                ),
                "docker compose up -d builds and starts everything detached.",
            ),
            q(
                "How can the api service reach the db service in Compose?",
                (
                    opt("By the db container's fixed IP address"),
                    opt(
                        "By name, because Compose creates a shared network automatically",
                        correct=True,
                    ),
                    opt("Only after publishing the db port to the host"),
                    opt("By exporting an environment file on the host"),
                ),
                "Compose creates a shared network automatically, so api reaches db by name.",
            ),
        ),
    },
    final=(
        q(
            "What is the main purpose of a Docker volume?",
            (
                opt("To make images smaller"),
                opt("To persist data beyond a container's lifecycle", correct=True),
                opt("To publish ports to the host"),
                opt("To define multi-container apps"),
            ),
            "Volumes store data outside the container, so it survives restarts and removals.",
        ),
        q(
            "How do containers on the same user-defined network communicate?",
            (
                opt("By container name resolved as a hostname", correct=True),
                opt("By manually assigned static IPs"),
                opt("Only through published host ports"),
                opt("Through a shared bind mount"),
            ),
            "On a user-defined network, containers resolve each other by container name, no IPs needed.",
        ),
        q(
            "What does docker compose down do?",
            (
                opt("Builds and starts all services"),
                opt("Streams the logs of all services"),
                opt("Stops and removes the containers, with -v to drop volumes", correct=True),
                opt("Publishes all container ports to the host"),
            ),
            "docker compose down stops and removes containers; add -v to also drop volumes.",
        ),
        q(
            "Which mount type is best suited for live-reloading source code in development?",
            (
                opt("A named volume"),
                opt("A bind mount", correct=True),
                opt("A read-only registry layer"),
                opt("A published port"),
            ),
            "A bind mount maps a host folder into the container, ideal for live-reloading source in development.",
        ),
        q(
            "Why is keeping internal services off published ports a good security default?",
            (
                opt("It speeds up image builds"),
                opt(
                    "Containers on the same network can still reach each other without exposing those services to the outside world",
                    correct=True,
                ),
                opt("It is required for volumes to work"),
                opt("It forces Compose to use a shared network"),
            ),
            "Containers on the same network reach each other without publishing ports, so only the gateway needs exposing.",
        ),
    ),
)
