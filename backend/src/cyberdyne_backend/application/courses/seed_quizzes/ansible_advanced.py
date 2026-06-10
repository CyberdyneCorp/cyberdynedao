from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Ansible Vault & secrets": (
            q(
                "What is the purpose of Ansible Vault?",
                (
                    opt("To store inventory hosts for cloud providers"),
                    opt(
                        "To encrypt secrets such as passwords, API keys, and certificates",
                        correct=True,
                    ),
                    opt("To run long tasks without blocking the playbook"),
                    opt("To lint playbooks for best practices"),
                ),
                "Ansible Vault encrypts secrets like passwords, API keys, and certificates so they are not stored in plaintext in git.",
            ),
            q(
                "Which command supplies the vault key from a file at run time?",
                (
                    opt("ansible-playbook site.yml --ask-vault-pass"),
                    opt("ansible-vault edit secrets.yml"),
                    opt(
                        "ansible-playbook site.yml --vault-password-file ~/.vault_pass",
                        correct=True,
                    ),
                    opt("ansible-vault encrypt group_vars/prod/vault.yml"),
                ),
                "The --vault-password-file flag reads the vault key from a file rather than prompting for it.",
            ),
            q(
                "What convention does the lesson recommend for organizing variables?",
                (
                    opt(
                        "Keep public vars in vars.yml and secret ones in an encrypted vault.yml",
                        correct=True,
                    ),
                    opt("Store all variables, public and secret, in a single encrypted file"),
                    opt("Encrypt every variable file regardless of sensitivity"),
                    opt("Never use group_vars for secrets"),
                ),
                "The convention keeps public vars in vars.yml and secret ones in an encrypted vault.yml referenced from the same group.",
            ),
        ),
        "Dynamic inventory & scaling": (
            q(
                "Why is dynamic inventory used instead of a static inventory file in the cloud?",
                (
                    opt("Because static files cannot store group variables"),
                    opt(
                        "Because cloud hosts come and go, so it queries the source of truth at run time",
                        correct=True,
                    ),
                    opt("Because dynamic inventory encrypts host names automatically"),
                    opt("Because static inventory is incompatible with roles"),
                ),
                "Dynamic inventory queries the source of truth (AWS, GCP, Azure, k8s) at run time because cloud hosts come and go.",
            ),
            q(
                "What does the serial keyword accomplish in a play?",
                (
                    opt("It runs hosts independently rather than in lockstep"),
                    opt("It controls the number of parallel forks"),
                    opt("It performs rolling updates, N hosts at a time", correct=True),
                    opt("It delegates a task to a different host"),
                ),
                "serial does rolling updates, applying changes to N hosts at a time so a bad change does not hit the whole fleet.",
            ),
            q(
                "What does the free strategy do compared to the default linear strategy?",
                (
                    opt("It lets hosts run independently instead of in lockstep", correct=True),
                    opt("It runs all hosts in strict lockstep order"),
                    opt("It limits parallelism to a single fork"),
                    opt("It runs a task on a delegated host"),
                ),
                "The free strategy lets hosts run independently, whereas the default linear strategy runs them in lockstep.",
            ),
        ),
        "Testing, CI & collections": (
            q(
                "What does ansible-playbook site.yml --check do?",
                (
                    opt("It encrypts the playbook with Vault"),
                    opt("It performs a dry run that reports changes but makes none", correct=True),
                    opt("It installs collections from Galaxy"),
                    opt("It spins up a container to test a role"),
                ),
                "The --check flag performs a dry run that reports what would change while making no changes.",
            ),
            q(
                "What sequence does molecule test run?",
                (
                    opt("lint -> encrypt -> deploy -> audit"),
                    opt("create -> converge -> idempotence -> verify -> destroy", correct=True),
                    opt("install -> graph -> serial -> destroy"),
                    opt("check -> diff -> converge -> publish"),
                ),
                "molecule test runs create, converge, idempotence, verify, then destroy.",
            ),
            q(
                "How are Ansible modules now packaged and installed?",
                (
                    opt("As collections versioned and installed via Galaxy", correct=True),
                    opt("As encrypted vault files"),
                    opt("As inventory plugins loaded at run time"),
                    opt("As standalone binaries from each cloud provider"),
                ),
                "Modules ship in collections such as ansible.builtin and community.general, installed via ansible-galaxy.",
            ),
        ),
    },
    final=(
        q(
            "Which tool encrypts secrets so they are not stored in plaintext in git?",
            (
                opt("Molecule"),
                opt("ansible-lint"),
                opt("Ansible Vault", correct=True),
                opt("ansible-galaxy"),
            ),
            "Ansible Vault encrypts secrets such as passwords and API keys.",
        ),
        q(
            "What is the core quality gate for automation described in the course?",
            (
                opt(
                    "Running --check plus an idempotence test where the second run reports zero changed",
                    correct=True,
                ),
                opt("Encrypting every variable with Vault"),
                opt("Using the free strategy on all plays"),
                opt("Installing the latest collections before each run"),
            ),
            "The core quality gate is --check plus an idempotence test: a second run must report zero changed.",
        ),
        q(
            "Which keyword runs a task on a different host, for example to update a load balancer?",
            (
                opt("serial"),
                opt("delegate_to", correct=True),
                opt("forks"),
                opt("async"),
            ),
            "delegate_to runs a task on a different host, such as updating a load balancer.",
        ),
        q(
            "Why does dynamic inventory suit cloud environments?",
            (
                opt("It encrypts host data at rest"),
                opt(
                    "It queries the source of truth at run time as hosts come and go", correct=True
                ),
                opt("It removes the need for inventory plugins"),
                opt("It guarantees idempotent playbook runs"),
            ),
            "Dynamic inventory queries the cloud source of truth at run time, fitting environments where hosts come and go.",
        ),
        q(
            "For teams, what does AWX / Ansible Automation Platform add on top of Ansible?",
            (
                opt("A UI, scheduling, RBAC, and audit", correct=True),
                opt("Automatic encryption of all playbooks"),
                opt("A replacement for collections"),
                opt("A dynamic inventory plugin for AWS only"),
            ),
            "AWX / Ansible Automation Platform adds a UI, scheduling, RBAC, and audit on top of Ansible.",
        ),
    ),
)
