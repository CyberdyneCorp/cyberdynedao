"""Curated quiz questions for the Terraform - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Dependencies, lifecycle & dynamic blocks": (
            q(
                "When two resources have no reference between them but order still matters, how do you force the dependency?",
                (
                    opt("Add a count meta-argument to both resources"),
                    opt("Use the depends_on meta-argument", correct=True),
                    opt("Wrap them in a dynamic block"),
                    opt("Set ignore_changes on the first resource"),
                ),
                "depends_on forces an explicit ordering when Terraform cannot infer it from references.",
            ),
            q(
                "Which lifecycle setting creates the replacement resource before destroying the old one to avoid downtime?",
                (
                    opt("prevent_destroy = true"),
                    opt("ignore_changes = [tags]"),
                    opt("create_before_destroy = true", correct=True),
                    opt("depends_on = []"),
                ),
                "create_before_destroy builds the new resource first so replacement happens without downtime.",
            ),
            q(
                "What is the purpose of a dynamic block such as a dynamic ingress block?",
                (
                    opt("To generate repeated nested blocks from a collection", correct=True),
                    opt("To prevent a critical resource from being destroyed"),
                    opt("To run Terraform commands inside a CI pipeline"),
                    opt("To import existing resources under management"),
                ),
                "A dynamic block generates nested blocks by iterating over a collection with for_each.",
            ),
        ),
        "CI/CD, policy & drift": (
            q(
                "Why is the plan saved with terraform plan -out=tfplan before applying in CI?",
                (
                    opt("So apply runs exactly the reviewed plan", correct=True),
                    opt("Because apply cannot run without an internet connection"),
                    opt("To skip the init step on later runs"),
                    opt("To automatically approve the merge request"),
                ),
                "Saving the plan as an artifact lets apply execute exactly what was reviewed.",
            ),
            q(
                "Which tools are named for enforcing policy as code before apply?",
                (
                    opt("Terratest and tflint"),
                    opt("Sentinel and OPA/conftest", correct=True),
                    opt("import and validate"),
                    opt("VPC and S3 modules"),
                ),
                "Policy as code is enforced with Sentinel or OPA/conftest, for example to block public S3 buckets.",
            ),
            q(
                "What does terraform plan -detailed-exitcode return when drift exists?",
                (
                    opt("Exit code 0"),
                    opt("Exit code 1"),
                    opt("Exit code 2", correct=True),
                    opt("Exit code 5"),
                ),
                "With -detailed-exitcode an exit code of 2 signals that drift exists.",
            ),
        ),
        "Production practices": (
            q(
                "Why should you pin module and provider versions?",
                (
                    opt("For reproducible builds", correct=True),
                    opt("To enable drift detection"),
                    opt("To hide outputs from CLI output"),
                    opt("To force create_before_destroy behaviour"),
                ),
                "Pinning module and provider versions gives reproducible builds.",
            ),
            q(
                "How should secrets be handled according to the lesson?",
                (
                    opt("Hard-code them directly in the resource block"),
                    opt("Commit them in a *.tfvars file in the repo"),
                    opt(
                        "Pull them from a secrets manager and mark outputs sensitive", correct=True
                    ),
                    opt("Store them as module version pins"),
                ),
                "Never hard-code or commit secrets; pull from a secrets manager and mark outputs sensitive = true.",
            ),
            q(
                "What does terraform import do?",
                (
                    opt("Brings existing resources under Terraform management", correct=True),
                    opt("Validates module syntax in CI"),
                    opt("Detects drift between state and config"),
                    opt("Generates nested blocks from a collection"),
                ),
                "terraform import brings existing resources under Terraform management.",
            ),
        ),
    },
    final=(
        q(
            "Which lifecycle setting guards a critical resource from being destroyed?",
            (
                opt("create_before_destroy"),
                opt("prevent_destroy", correct=True),
                opt("ignore_changes"),
                opt("depends_on"),
            ),
            "prevent_destroy guards critical resources from being destroyed.",
        ),
        q(
            "In a CI pipeline, what is the recommended control around the apply step?",
            (
                opt("Run apply automatically on every commit without review"),
                opt("Gate apply behind a merge or approval", correct=True),
                opt("Skip the plan step entirely"),
                opt("Run apply only from a developer laptop"),
            ),
            "apply should be gated behind a merge or approval so changes are reviewed like code.",
        ),
        q(
            "What is drift in the Terraform sense?",
            (
                opt(
                    "When real infrastructure diverges from the config after out-of-band changes",
                    correct=True,
                ),
                opt("When a module version is upgraded automatically"),
                opt("When a secret is committed to the repository"),
                opt("When a dynamic block fails to render"),
            ),
            "Drift is when real state diverges from config because infra was changed by hand.",
        ),
        q(
            "Which tool is named for integration-testing Terraform modules in CI?",
            (
                opt("Terratest", correct=True),
                opt("Sentinel"),
                opt("Atlantis"),
                opt("conftest"),
            ),
            "Terratest is used for integration tests of modules in CI alongside validate and tflint.",
        ),
        q(
            "Why separate state per environment and per blast-radius?",
            (
                opt("To enable dynamic blocks"),
                opt("So a bad apply cannot take everything down", correct=True),
                opt("To avoid having to pin versions"),
                opt("To make secrets visible in CLI output"),
            ),
            "Separating state per environment and blast-radius limits the damage of a bad apply.",
        ),
    ),
)
