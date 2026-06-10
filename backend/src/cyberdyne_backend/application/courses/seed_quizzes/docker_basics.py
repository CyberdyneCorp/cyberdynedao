"""Curated quiz questions for the Docker - Basics course (per-lesson checkpoints
plus a final comprehensive quiz). Keys are the EXACT content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Containers vs. virtual machines": (
            q(
                "How does a container differ from a virtual machine?",
                (
                    opt("It virtualises the hardware and ships a whole guest OS"),
                    opt(
                        "It shares the host kernel and isolates just the process",
                        correct=True,
                    ),
                    opt("It requires a hypervisor to boot each application"),
                    opt("It always weighs several gigabytes and boots slowly"),
                ),
                "A container shares the host kernel and isolates only the process, making it light and fast to start.",
            ),
            q(
                "In Docker terms, what is an image?",
                (
                    opt("A running instance of a container"),
                    opt("A read-only template of your app plus its dependencies", correct=True),
                    opt("The registry where containers are stored"),
                    opt("The hypervisor that runs the guest OS"),
                ),
                "An image is a read-only template containing your app and its dependencies.",
            ),
            q(
                "What is a registry such as Docker Hub used for?",
                (
                    opt("Running detached containers in the background"),
                    opt("Storing and sharing images", correct=True),
                    opt("Virtualising hardware for guest operating systems"),
                    opt("Mapping host ports to container ports"),
                ),
                "A registry like Docker Hub is where images are stored and shared.",
            ),
        ),
        "Images & containers": (
            q(
                "What does the -d flag do in docker run?",
                (
                    opt("Deletes the container after it stops"),
                    opt("Detaches the container so it runs in the background", correct=True),
                    opt("Downloads the image from the registry"),
                    opt("Gives you an interactive terminal"),
                ),
                "The -d flag detaches the container so it runs in the background.",
            ),
            q(
                "In docker run -d -p 8080:80 nginx, what does -p 8080:80 do?",
                (
                    opt("Exposes the container port 80 on the host port 8080", correct=True),
                    opt("Exposes the container port 8080 on the host port 80"),
                    opt("Runs the container with 80 percent of available memory"),
                    opt("Pulls 8080 layers from the nginx image"),
                ),
                "It maps the host's 8080 to the container's port 80, in host:container order.",
            ),
            q(
                "Why are containers described as ephemeral?",
                (
                    opt("They can only run for a few seconds before stopping"),
                    opt(
                        "When one is removed, changes inside it are gone unless a volume is used",
                        correct=True,
                    ),
                    opt("They cannot be restarted once stopped"),
                    opt("They share their filesystem with every other container"),
                ),
                "Containers are ephemeral because removing one loses any changes made inside, unless a volume persists them.",
            ),
        ),
        "Your first Dockerfile": (
            q(
                "What is a Dockerfile?",
                (
                    opt("A running instance of an image"),
                    opt("A recipe that builds an image layer by layer", correct=True),
                    opt("The registry that stores built images"),
                    opt("The interactive shell inside a container"),
                ),
                "A Dockerfile is a recipe that builds an image, layer by layer.",
            ),
            q(
                "Why is package*.json copied before the rest of the source?",
                (
                    opt("Because COPY can only run once per Dockerfile"),
                    opt(
                        "So npm install only re-runs when dependencies change, reusing cached layers",
                        correct=True,
                    ),
                    opt("Because the source files would otherwise overwrite it"),
                    opt("Because EXPOSE requires the manifest to be present first"),
                ),
                "Copying the manifests first lets Docker reuse the cached npm install layer until dependencies change.",
            ),
            q(
                "What is the difference between RUN and CMD in a Dockerfile?",
                (
                    opt("RUN sets the working directory; CMD copies files"),
                    opt(
                        "RUN executes at build time; CMD is the default command run on start",
                        correct=True,
                    ),
                    opt("RUN exposes a port; CMD installs dependencies"),
                    opt("RUN is the default start command; CMD runs during the build"),
                ),
                "RUN executes at build time while CMD defines the default command run when the container starts.",
            ),
        ),
    },
    final=(
        q(
            "What core advantage do containers have over virtual machines?",
            (
                opt("They run a full guest OS for stronger isolation"),
                opt(
                    "They share the host kernel, so they are light and start in milliseconds",
                    correct=True,
                ),
                opt("They require a hypervisor to schedule each process"),
                opt("They store all data permanently by default"),
            ),
            "Containers share the host kernel and isolate just the process, so they are far lighter and faster than VMs.",
        ),
        q(
            "Which command both pulls (if needed), creates, and starts a container in one step?",
            (
                opt("docker images"),
                opt("docker run", correct=True),
                opt("docker build"),
                opt("docker ps -a"),
            ),
            "docker run combines pull (if needed), create, and start in a single command.",
        ),
        q(
            "How do you build an image named myapp:1.0 from the current directory?",
            (
                opt("docker run -t myapp:1.0 ."),
                opt("docker build -t myapp:1.0 .", correct=True),
                opt("docker pull myapp:1.0 ."),
                opt("docker exec -t myapp:1.0 ."),
            ),
            "docker build -t myapp:1.0 . builds and tags the image from the current directory.",
        ),
        q(
            "What does the -it flag combination give you when running a container?",
            (
                opt("An interactive terminal", correct=True),
                opt("A detached background process"),
                opt("An immutable image tag"),
                opt("A persistent volume mount"),
            ),
            "The -it flags give you an interactive terminal in the container.",
        ),
        q(
            "Which three core ideas does the course define for Docker?",
            (
                opt("Hypervisor, guest OS, and host OS"),
                opt("Image, container, and registry", correct=True),
                opt("Layer, volume, and network"),
                opt("Build, run, and push"),
            ),
            "The three core ideas are the image (template), the container (running instance), and the registry (where images live).",
        ),
    ),
)
