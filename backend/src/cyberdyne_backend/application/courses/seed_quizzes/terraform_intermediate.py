"""Curated quiz questions for the Terraform - Intermediate course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each lesson."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "State, backends & workspaces": (
            q(
                "Why does a local terraform.tfstate file not work well for teams?",
                (
                    opt("It cannot store more than one resource at a time"),
                    opt("Two people applying at once can corrupt it", correct=True),
                    opt("It is encrypted and unreadable by other users"),
                    opt("It only works on the machine that ran terraform init"),
                ),
                "A local state file breaks for teams because two people applying at once corrupts it.",
            ),
            q(
                "In the example S3 backend, what is the dynamodb_table used for?",
                (
                    opt("State locking", correct=True),
                    opt("Storing the state file contents"),
                    opt("Encrypting the bucket"),
                    opt("Selecting the AWS region"),
                ),
                "The dynamodb_table provides state locking so only one apply runs at a time.",
            ),
            q(
                "What do Terraform workspaces let you do?",
                (
                    opt("Run multiple applies on the same state simultaneously"),
                    opt(
                        "Use one config to manage multiple instances with separate state",
                        correct=True,
                    ),
                    opt("Replace the need for a remote backend entirely"),
                    opt("Encrypt the state file at rest automatically"),
                ),
                "Workspaces let one config manage multiple instances such as dev and staging with separate state.",
            ),
        ),
        "Modules": (
            q(
                "What is a module in Terraform?",
                (
                    opt("A reusable bundle of resources with inputs and outputs", correct=True),
                    opt("A single resource block defined inline"),
                    opt("A remote backend used for storing state"),
                    opt("A workspace that isolates state per environment"),
                ),
                "A module is a reusable bundle of resources with inputs and outputs, the unit of DRY in Terraform.",
            ),
            q(
                "What can a module source point at besides a local path?",
                (
                    opt("Only other local directories"),
                    opt("The Terraform Registry or a git repo", correct=True),
                    opt("A DynamoDB lock table"),
                    opt("An S3 backend bucket"),
                ),
                "source can point at a local path, the Terraform Registry, or a git repo.",
            ),
            q(
                "How would you reference the id output of a module named web?",
                (
                    opt("aws_instance.web.id"),
                    opt("output.web.id"),
                    opt("module.web.id", correct=True),
                    opt("var.web.id"),
                ),
                "A module output is referenced as module.web.id.",
            ),
        ),
        "Expressions, loops & data sources": (
            q(
                "Why is for_each usually safer than count?",
                (
                    opt("It runs the apply faster than count"),
                    opt("Adding or removing an item does not reindex the others", correct=True),
                    opt("It does not require a provider to be configured"),
                    opt("It works without referencing any variables"),
                ),
                "for_each is safer because adding or removing an item does not reindex the others, unlike count.",
            ),
            q(
                "What does a data source let you do?",
                (
                    opt("Read existing infrastructure", correct=True),
                    opt("Create many copies of a resource"),
                    opt("Lock the remote state file"),
                    opt("Define reusable input variables"),
                ),
                "A data source reads existing infrastructure so you can reference it in your config.",
            ),
            q(
                "Where are values like project and env defined in the lesson example?",
                (
                    opt("In a data source"),
                    opt("In a locals block", correct=True),
                    opt("In a backend block"),
                    opt("In an output block"),
                ),
                "The common_tags map with project and env is defined inside a locals block.",
            ),
        ),
    },
    final=(
        q(
            "What two things does a remote backend provide that a local state file does not?",
            (
                opt("Central storage and locking so only one apply runs at a time", correct=True),
                opt("Automatic module versioning and a registry"),
                opt("Built-in functions and data sources"),
                opt("count and for_each looping support"),
            ),
            "A remote backend stores state centrally and locks it so only one apply runs at a time.",
        ),
        q(
            "Which Terraform feature is the unit of DRY for packaging reusable resources?",
            (
                opt("Workspaces"),
                opt("Modules", correct=True),
                opt("Data sources"),
                opt("Locals"),
            ),
            "A module is the reusable bundle of resources with inputs and outputs, the unit of DRY in Terraform.",
        ),
        q(
            "When creating many resources, why might you choose for_each over count?",
            (
                opt("for_each is the only one that supports tags"),
                opt("Removing an item with for_each does not reindex the rest", correct=True),
                opt("count cannot create more than one resource"),
                opt("for_each does not require a provider"),
            ),
            "for_each keys resources by name, so adding or removing an item does not reindex the others.",
        ),
        q(
            "How do you read an existing AMI rather than create one?",
            (
                opt("With a module call"),
                opt("With a data source such as data aws_ami", correct=True),
                opt("With a workspace"),
                opt("With a locals block"),
            ),
            "Data sources like data aws_ami read existing infrastructure for reference in config.",
        ),
        q(
            "What does the dynamodb_table in the S3 backend example handle?",
            (
                opt("State locking", correct=True),
                opt("Storing the state file"),
                opt("Selecting the region"),
                opt("Versioning the bucket"),
            ),
            "The dynamodb_table provides state locking in the S3 backend configuration.",
        ),
    ),
)
