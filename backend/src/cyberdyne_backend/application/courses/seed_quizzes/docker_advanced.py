"""Curated quiz questions for the docker-advanced course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT
content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Multi-stage builds & tiny images": (
            q(
                "What is the point of a multi-stage build?",
                (
                    opt("To run the compiler again every time the container starts"),
                    opt(
                        "To compile in one stage and copy only the artifact into a minimal runtime stage",
                        correct=True,
                    ),
                    opt("To split one image across several registries"),
                    opt("To skip the build step entirely and ship source code"),
                ),
                "A multi-stage build compiles in one stage and copies only the artifact into a minimal runtime stage, so the final image ships no toolchain.",
            ),
            q(
                "What does the instruction COPY --from=build /app /app do?",
                (
                    opt("Pulls just the binary from the earlier build stage", correct=True),
                    opt("Copies the entire build stage including the compiler"),
                    opt("Downloads the app from a remote registry"),
                    opt("Copies files from the host build directory into the image"),
                ),
                "COPY --from=build pulls just the binary produced by the earlier stage, leaving the toolchain behind.",
            ),
            q(
                "Why use a distroless or alpine/slim base image for the runtime stage?",
                (
                    opt("It adds extra debugging shells to the image"),
                    opt("It is required to run multi-arch builds"),
                    opt(
                        "It drops the shell and package manager so images shrink and have a smaller attack surface",
                        correct=True,
                    ),
                    opt("It automatically scans the image for CVEs"),
                ),
                "A distroless or slim base drops the shell and package manager, shrinking images from hundreds of MB to a few MB and reducing the attack surface.",
            ),
        ),
        "Security & hardening": (
            q(
                "Why should a container not run as root?",
                (
                    opt("Root cannot read mounted volumes"),
                    opt("Root in the container is dangerous if it escapes", correct=True),
                    opt("Running as root makes images larger"),
                    opt("Docker refuses to start containers owned by root"),
                ),
                "Containers share the host kernel, so root in the container is dangerous if it escapes; use a non-root USER instead.",
            ),
            q(
                "How should secrets be provided to a container?",
                (
                    opt("Baked into the image so they are always available"),
                    opt("Hardcoded in an ENV instruction in the Dockerfile"),
                    opt(
                        "Injected at runtime via --env-file, Docker/K8s secrets, or BuildKit --secret",
                        correct=True,
                    ),
                    opt("Committed to the git repository alongside the source"),
                ),
                "Do not bake secrets into images or ENV; inject them at runtime with --env-file, Docker/K8s secrets, or BuildKit --secret.",
            ),
            q(
                "Which tools are used to scan an image for known CVEs?",
                (
                    opt("docker tag and docker push"),
                    opt("docker scout cves and trivy image", correct=True),
                    opt("docker compose and docker buildx"),
                    opt("kubectl describe and kubectl logs"),
                ),
                "The lesson shows docker scout cves and trivy image as the tools for scanning an image for known CVEs.",
            ),
        ),
        "Registries, BuildKit & orchestration": (
            q(
                "How should images be tagged so deploys are reproducible?",
                (
                    opt("Always with the latest tag"),
                    opt("Immutably, with a git SHA or version", correct=True),
                    opt("With a random string per build"),
                    opt("Without any tag at all"),
                ),
                "Tag immutably with a git SHA or version, not just latest, so deploys are reproducible.",
            ),
            q(
                "What does BuildKit (buildx) provide for modern builds?",
                (
                    opt("It replaces the need for a registry"),
                    opt("It only works on a single CPU architecture"),
                    opt(
                        "Caching, secrets, and building for multiple CPU architectures",
                        correct=True,
                    ),
                    opt("It automatically deploys images to Kubernetes"),
                ),
                "BuildKit (buildx) provides caching, secrets, and building for multiple CPU architectures such as linux/amd64 and linux/arm64.",
            ),
            q(
                "What do you hand off to when you need to run containers across many machines with self-healing and scaling?",
                (
                    opt("docker compose"),
                    opt("A second Docker Hub account"),
                    opt("An orchestrator such as Kubernetes", correct=True),
                    opt("A larger single host"),
                ),
                "docker compose runs containers on one machine; to run across many machines with self-healing, scaling, and rolling updates you hand off to an orchestrator, Kubernetes.",
            ),
        ),
    },
    final=(
        q(
            "In a multi-stage build, what gets shipped in the final image?",
            (
                opt("The compiler and all dev tools"),
                opt("Only the artifact copied into a minimal runtime stage", correct=True),
                opt("The full build context including secrets"),
                opt("The source code and the binary together"),
            ),
            "A multi-stage build copies only the artifact into a minimal runtime stage, so the final image ships no compilers or dev tools.",
        ),
        q(
            "Which practice improves both image size and security?",
            (
                opt("Using a minimal base image such as distroless or slim", correct=True),
                opt("Running every process as root"),
                opt("Baking secrets into the image"),
                opt("Tagging everything as latest"),
            ),
            "A minimal base image has fewer packages and therefore fewer vulnerabilities, so it shrinks the image and is itself a security win.",
        ),
        q(
            "What is the recommended way to set a container user for security?",
            (
                opt("Leave it as the default root user"),
                opt("Create and switch to a non-root user with USER", correct=True),
                opt("Disable the USER instruction entirely"),
                opt("Use the latest tag to pick the user automatically"),
            ),
            "Create a non-root user and switch to it with the USER instruction, since root in the container is dangerous if it escapes.",
        ),
        q(
            "Which command builds an image for multiple architectures and pushes it?",
            (
                opt("docker scout cves -t ghcr.io/acme/myapp:1.0"),
                opt("docker compose up --platform linux/amd64,linux/arm64"),
                opt(
                    "docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/acme/myapp:1.0 --push .",
                    correct=True,
                ),
                opt("docker pull ghcr.io/acme/myapp:1.0 --multi-arch"),
            ),
            "docker buildx build with --platform linux/amd64,linux/arm64 and --push builds for multiple architectures and pushes the result.",
        ),
        q(
            "Why is docker compose not enough to run containers across many machines?",
            (
                opt("It cannot pull images from a registry"),
                opt("It runs containers on only one machine", correct=True),
                opt("It does not support multi-stage builds"),
                opt("It requires images to be tagged as latest"),
            ),
            "docker compose runs containers on a single machine; running across many machines with self-healing and scaling requires an orchestrator like Kubernetes.",
        ),
    ),
)
