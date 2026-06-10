from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is Infrastructure as Code?": (
            q(
                "How does Infrastructure as Code describe servers, networks and databases?",
                (
                    opt("By clicking around a cloud console and saving screenshots"),
                    opt("In text files you version in git", correct=True),
                    opt("In a binary database only the cloud provider can read"),
                    opt("By emailing change requests to the platform team"),
                ),
                "IaC describes infrastructure in text files that you version in git rather than clicking around a console.",
            ),
            q(
                "In Terraform, what is the job of a provider such as aws, gcp or azure?",
                (
                    opt("It knows how to talk to a particular platform", correct=True),
                    opt("It stores the encrypted state file remotely"),
                    opt("It defines a single piece of infrastructure"),
                    opt("It formats your HCL files automatically"),
                ),
                "A provider (aws, gcp, azure, kubernetes) knows how to talk to a platform.",
            ),
            q(
                "What does Terraform do when you declare the desired state?",
                (
                    opt("It runs the imperative commands you typed in order"),
                    opt("It figures out the API calls to make reality match", correct=True),
                    opt("It only validates syntax and never changes anything"),
                    opt("It deletes all existing infrastructure first"),
                ),
                "You declare the desired state and Terraform figures out the API calls to make reality match it.",
            ),
        ),
        "Resources, variables & outputs": (
            q(
                "What is the name of Terraform's configuration language?",
                (
                    opt("YAML"),
                    opt("HCL, the HashiCorp Configuration Language", correct=True),
                    opt("JSON Schema"),
                    opt("TOML"),
                ),
                "Terraform's language is HCL, the HashiCorp Configuration Language.",
            ),
            q(
                "Which of these is a valid way to set a Terraform variable?",
                (
                    opt("A terraform.tfvars file", correct=True),
                    opt("A terraform.state binary file"),
                    opt("The provider block region argument"),
                    opt("An output block value"),
                ),
                "Variables can be set via -var, a terraform.tfvars file, or the TF_VAR_ environment prefix.",
            ),
            q(
                "Why does referencing one resource from another matter in Terraform?",
                (
                    opt("It hides the resource from the state file"),
                    opt(
                        "It tells Terraform the order to create things by building a graph",
                        correct=True,
                    ),
                    opt("It encrypts the referenced value automatically"),
                    opt("It prevents the resource from ever being destroyed"),
                ),
                "References build a dependency graph that tells Terraform the order to create things, then it parallelises the rest.",
            ),
        ),
        "The Terraform workflow": (
            q(
                "Which command downloads providers and sets up the working directory?",
                (
                    opt("terraform plan"),
                    opt("terraform init", correct=True),
                    opt("terraform apply"),
                    opt("terraform destroy"),
                ),
                "terraform init downloads providers and sets up the working directory.",
            ),
            q(
                "In a terraform plan diff, what does the + symbol mean?",
                (
                    opt("Create", correct=True),
                    opt("Update"),
                    opt("Destroy"),
                    opt("Ignore"),
                ),
                "In a plan diff + means create, ~ means update, and - means destroy.",
            ),
            q(
                "What is the advice the lesson gives about the Terraform state file?",
                (
                    opt("Edit it by hand to fix drift quickly"),
                    opt(
                        "Never edit state by hand, and use a shared remote backend for teams",
                        correct=True,
                    ),
                    opt("Commit it as plaintext to every git branch"),
                    opt("Delete it after each apply to save space"),
                ),
                "The lesson says never edit state by hand and for teams keep it in a shared remote backend.",
            ),
        ),
    },
    final=(
        q(
            "What does the term declarative mean for Terraform as described in this course?",
            (
                opt(
                    "You declare the desired state and Terraform makes reality match", correct=True
                ),
                opt("You write step-by-step shell commands to provision each resource"),
                opt("You manually click through the cloud console"),
                opt("You only describe what to delete, never what to create"),
            ),
            "Terraform is declarative: you declare the desired state and it figures out the API calls to match it.",
        ),
        q(
            "Which four commands cover day-to-day Terraform use?",
            (
                opt("init, plan, apply, destroy", correct=True),
                opt("build, test, deploy, rollback"),
                opt("clone, commit, push, merge"),
                opt("create, read, update, delete"),
            ),
            "The everyday workflow is terraform init, plan, apply, and destroy.",
        ),
        q(
            "How do you reference a variable named instance_type inside HCL?",
            (
                opt("var.instance_type", correct=True),
                opt("output.instance_type"),
                opt("data.instance_type"),
                opt("provider.instance_type"),
            ),
            "Variables are referenced with the var. prefix, for example var.instance_type.",
        ),
        q(
            "Why is reviewing the plan before apply called the safety habit?",
            (
                opt(
                    "It shows a diff of what will be created, changed or destroyed before anything changes",
                    correct=True,
                ),
                opt("It automatically rolls back any failed apply"),
                opt("It encrypts the state file before sending it"),
                opt("It downloads the providers needed for the run"),
            ),
            "plan shows a diff before anything changes, so reviewing it prevents accidents.",
        ),
        q(
            "What is an output block used for in Terraform?",
            (
                opt("To surface useful values such as a resource public IP", correct=True),
                opt("To download and configure a provider"),
                opt("To store the encrypted state remotely"),
                opt("To define a reusable input parameter"),
            ),
            "Outputs surface useful values, for example exposing aws_instance.app.public_ip.",
        ),
    ),
)
