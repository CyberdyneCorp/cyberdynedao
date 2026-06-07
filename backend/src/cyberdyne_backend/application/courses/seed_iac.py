"""Curated Infrastructure-as-Code courses: Terraform and Ansible, each at
basic, intermediate, and advanced levels.

Grounded in the user's Obsidian `Infrastructure` vault. Lessons are `text` with
code fences (hcl / yaml / bash) — no live cloud to apply against in the
Academy, so config is illustrative. Each course ends with a quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="3 min")


# ── Terraform ────────────────────────────────────────────────────────────────

_TF_BASICS = SeedCourse(
    slug="terraform-basics",
    title="Terraform — Basics",
    description=(
        "Provision cloud infrastructure as code: what IaC and Terraform are, "
        "writing resources in HCL with variables and outputs, and the "
        "init/plan/apply workflow."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is Infrastructure as Code?",
            "8 min",
            """\
# What is Infrastructure as Code?

Instead of clicking around a cloud console, **Infrastructure as Code (IaC)**
describes your servers, networks and databases in text files you version in
git. **Terraform** is the most popular IaC tool — declarative and cloud-
agnostic.

You declare the **desired state**; Terraform figures out the API calls to make
reality match.

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app" {
  ami           = "ami-0abc123"
  instance_type = "t3.micro"
  tags = { Name = "app-server" }
}
```

- A **provider** (aws, gcp, azure, kubernetes…) knows how to talk to a platform.
- A **resource** is one piece of infrastructure.
- Terraform tracks what it created in **state** (next lessons).

**Next:** resources, variables, and outputs.
""",
        ),
        _t(
            "Resources, variables & outputs",
            "9 min",
            """\
# Resources, variables & outputs

Terraform's language is **HCL** (HashiCorp Configuration Language).

## Variables — parameterise your config

```hcl
variable "instance_type" {
  type    = string
  default = "t3.micro"
}

resource "aws_instance" "app" {
  ami           = "ami-0abc123"
  instance_type = var.instance_type     # reference with var.
}
```

Set them via `-var`, a `terraform.tfvars` file, or environment
(`TF_VAR_instance_type`).

## Outputs — surface useful values

```hcl
output "public_ip" {
  value = aws_instance.app.public_ip
}
```

## References build a dependency graph

Referencing one resource from another (`aws_instance.app.id`) tells Terraform
the order to create things — it builds a graph and parallelises the rest. All
`.tf` files in a directory are loaded together.

**Next:** the everyday workflow.
""",
        ),
        _t(
            "The Terraform workflow",
            "9 min",
            """\
# The Terraform workflow

Four commands cover day-to-day use:

```bash
terraform init      # download providers, set up the working dir
terraform plan      # preview: what will be created/changed/destroyed
terraform apply     # make it real (asks for confirmation)
terraform destroy   # tear it all down
```

## Plan before apply

`plan` shows a diff — `+` create, `~` update, `-` destroy — *before* anything
changes. Reviewing the plan is the safety habit that prevents accidents.

## State

Terraform records what it manages in a **state file** (`terraform.tfstate`).
On the next `apply` it compares desired config against state to compute the
minimal change. **Never edit state by hand**, and for teams keep it in a shared
**remote backend** (next course) rather than on your laptop.

```bash
terraform fmt        # format files
terraform validate   # check syntax
```

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_TF_INTERMEDIATE = SeedCourse(
    slug="terraform-intermediate",
    title="Terraform — Intermediate",
    description=(
        "Scale beyond a single file: remote state and locking, reusable modules, "
        "and dynamic config with expressions, count/for_each and data sources."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "State, backends & workspaces",
            "9 min",
            """\
# State, backends & workspaces

A local `terraform.tfstate` doesn't work for teams — two people applying at once
corrupts it. A **remote backend** stores state centrally and **locks** it so
only one apply runs at a time.

```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/app.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"   # state locking
  }
}
```

- State is the source of truth Terraform diffs against — protect it (versioning,
  encryption).
- **Workspaces** let one config manage multiple instances (e.g. dev/staging)
  with separate state:

```bash
terraform workspace new staging
terraform workspace select prod
```

For real environment separation, many teams prefer separate state files/dirs
over workspaces.

**Next:** packaging config into modules.
""",
        ),
        _t(
            "Modules",
            "9 min",
            """\
# Modules

A **module** is a reusable bundle of resources with inputs and outputs — the
unit of DRY in Terraform. Any directory of `.tf` files is a module; you call it
from another.

```hcl
# modules/web/variables.tf
variable "name" { type = string }

# modules/web/main.tf
resource "aws_instance" "this" {
  ami           = "ami-0abc123"
  instance_type = "t3.micro"
  tags = { Name = var.name }
}

# modules/web/outputs.tf
output "id" { value = aws_instance.this.id }
```

Call it:

```hcl
module "web" {
  source = "./modules/web"
  name   = "frontend"
}

# use its output:
# module.web.id
```

`source` can also point at the **Terraform Registry** or a git repo
(`source = "terraform-aws-modules/vpc/aws"`). Compose small modules into
environments.

**Next:** dynamic expressions and data sources.
""",
        ),
        _t(
            "Expressions, loops & data sources",
            "9 min",
            """\
# Expressions, loops & data sources

## locals and expressions

```hcl
locals {
  common_tags = { project = "cyberdyne", env = terraform.workspace }
}
```

## count and for_each — create many

```hcl
resource "aws_instance" "node" {
  count         = 3                      # node[0], node[1], node[2]
  ami           = "ami-0abc123"
  instance_type = "t3.micro"
}

resource "aws_iam_user" "u" {
  for_each = toset(["ada", "bob"])       # keyed by name
  name     = each.key
}
```

`for_each` is usually safer than `count` — adding/removing an item doesn't
reindex the others.

## Data sources — read existing infra

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter { name = "name"  values = ["ubuntu/images/*-22.04-*"] }
}
# reference: data.aws_ami.ubuntu.id
```

Built-in functions (`merge`, `lookup`, `length`, `cidrsubnet`…) shape values.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_TF_ADVANCED = SeedCourse(
    slug="terraform-advanced",
    title="Terraform — Advanced",
    description=(
        "Run Terraform like a platform team: dependencies and lifecycle control, "
        "CI/CD with policy and drift detection, and production module/secret "
        "practices."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Dependencies, lifecycle & dynamic blocks",
            "10 min",
            """\
# Dependencies, lifecycle & dynamic blocks

## Explicit dependencies

Terraform infers order from references; when there's no reference but order
still matters, force it:

```hcl
resource "aws_instance" "app" {
  # ...
  depends_on = [aws_iam_role_policy.app]
}
```

## lifecycle — control replace/destroy

```hcl
resource "aws_instance" "app" {
  lifecycle {
    create_before_destroy = true   # avoid downtime on replacement
    prevent_destroy       = true   # guard critical resources
    ignore_changes        = [tags] # don't fight external edits
  }
}
```

## dynamic blocks — generate nested blocks

```hcl
dynamic "ingress" {
  for_each = var.ports
  content {
    from_port = ingress.value
    to_port   = ingress.value
    protocol  = "tcp"
  }
}
```

These give you fine control over how the dependency graph is built and how
resources are replaced.

**Next:** running Terraform in CI/CD.
""",
        ),
        _t(
            "CI/CD, policy & drift",
            "9 min",
            """\
# CI/CD, policy & drift

## Automated pipelines

Run Terraform in CI so changes are reviewed like code:

```bash
terraform init -input=false
terraform plan -out=tfplan        # plan as an artifact
terraform apply -input=false tfplan   # apply the exact reviewed plan
```

Gate `apply` behind a merge/approval; save the plan so apply does exactly what
was reviewed.

## Policy as code

Enforce rules before apply with **Sentinel** or **OPA/conftest** — e.g. "no
public S3 buckets", "only approved instance types". Tools like Terraform Cloud,
Atlantis, and Spacelift wrap this workflow.

## Drift detection

If someone changes infra by hand, real state **drifts** from config. Detect it:

```bash
terraform plan -detailed-exitcode   # exit 2 = drift exists
```

Run this on a schedule to catch out-of-band changes and re-converge.

**Next:** production practices.
""",
        ),
        _t(
            "Production practices",
            "9 min",
            """\
# Production practices

## Compose, don't repeat

Build a library of small modules (network, db, service) and assemble them per
environment. Pin module and provider **versions** for reproducible builds:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.1"
}
```

## Secrets

Never hard-code secrets or commit `*.tfvars` with them. Pull from a secrets
manager at plan/apply time and mark outputs `sensitive = true`:

```hcl
output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true        # hidden from CLI output
}
```

## Importing & testing

- `terraform import` brings existing resources under management.
- Validate modules with `terraform validate`, `tflint`, and integration tests
  (**Terratest**) in CI.
- Separate state per environment and per blast-radius so a bad apply can't take
  everything down.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Ansible ──────────────────────────────────────────────────────────────────

_ANSIBLE_BASICS = SeedCourse(
    slug="ansible-basics",
    title="Ansible — Basics",
    description=(
        "Agentless configuration management: how Ansible works over SSH, writing "
        "idempotent playbooks with modules, and inventories plus ad-hoc commands."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is Ansible?",
            "8 min",
            """\
# What is Ansible?

**Ansible** automates configuration — installing packages, editing files,
starting services — across many machines at once. Its big selling point:
**agentless**. It connects over plain **SSH** (WinRM on Windows), so there's
nothing to install on the managed hosts.

```mermaid
flowchart LR
  CN[Control node: ansible] -->|SSH| H1[web1]
  CN -->|SSH| H2[web2]
  CN -->|SSH| H3[db1]
```

- A **control node** (your laptop / CI) pushes changes out.
- **Managed nodes** just need SSH + Python.
- Configuration is described in **YAML** — readable, version-controlled.

Crucially, Ansible aims to be **idempotent**: running a playbook twice leaves
the system in the same state — it only changes what isn't already correct.

**Next:** playbooks and modules.
""",
        ),
        _t(
            "Playbooks & modules",
            "10 min",
            """\
# Playbooks & modules

A **playbook** is a YAML file of **plays**, each running a list of **tasks** on
a set of hosts. Each task calls a **module** (the unit of work).

```yaml
- name: Set up web servers
  hosts: web
  become: true                # run with sudo
  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present

    - name: Ensure nginx is running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
```

```bash
ansible-playbook -i inventory.ini site.yml
```

- Modules (`apt`, `copy`, `template`, `service`, `user`…) are **declarative**:
  you state the desired result, not the commands.
- `state: present` / `started` is idempotent — already installed/running tasks
  report **ok**, not **changed**.

**Next:** inventory and ad-hoc commands.
""",
        ),
        _t(
            "Inventory & ad-hoc commands",
            "8 min",
            """\
# Inventory & ad-hoc commands

The **inventory** lists the hosts you manage, organised into groups:

```ini
[web]
web1.example.com
web2.example.com

[db]
db1.example.com

[prod:children]
web
db
```

Playbooks target a group via `hosts: web`.

## Ad-hoc commands

For one-off actions you don't need a playbook — run a module directly:

```bash
ansible all -i inventory.ini -m ping             # connectivity check
ansible web -m apt -a "name=curl state=present" --become
ansible all -m shell -a "uptime"
```

`-m` picks the module, `-a` passes arguments. Use ad-hoc for quick checks;
write playbooks for anything you'll repeat.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_ANSIBLE_INTERMEDIATE = SeedCourse(
    slug="ansible-intermediate",
    title="Ansible — Intermediate",
    description=(
        "Build maintainable automation: variables, facts and Jinja2 templates; "
        "packaging with roles; and control flow with conditionals, loops and "
        "handlers."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Variables, facts & templates",
            "9 min",
            """\
# Variables, facts & templates

## Variables

Define them in the play, in `group_vars/`, `host_vars/`, or pass with `-e`:

```yaml
vars:
  app_port: 8080
tasks:
  - debug:
      msg: "listening on {{ app_port }}"   # {{ }} is Jinja2
```

## Facts

Ansible auto-gathers **facts** about each host (OS, IP, CPU…) — use them in
conditionals and templates: `ansible_facts['os_family']`,
`ansible_default_ipv4.address`.

## Jinja2 templates

The `template` module renders a `.j2` file with variables and copies it to the
host:

```jinja
# nginx.conf.j2
server {
    listen {{ app_port }};
    server_name {{ inventory_hostname }};
}
```

```yaml
- name: Deploy nginx config
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx          # triggers a handler
```

**Next:** packaging it all into roles.
""",
        ),
        _t(
            "Roles",
            "9 min",
            """\
# Roles

A **role** packages tasks, variables, templates, files and handlers into a
reusable, standard directory layout — the unit of sharing in Ansible.

```text
roles/
  nginx/
    tasks/main.yml
    handlers/main.yml
    templates/nginx.conf.j2
    defaults/main.yml      # default variables
    vars/main.yml
```

Use a role from a play:

```yaml
- hosts: web
  become: true
  roles:
    - nginx
    - { role: app, app_port: 9000 }   # with variables
```

- `defaults/` holds overridable defaults; `tasks/main.yml` is the entry point.
- Share and reuse community roles via **Ansible Galaxy**:

```bash
ansible-galaxy role install geerlingguy.nginx
```

Roles keep playbooks short and make automation composable across projects.

**Next:** conditionals, loops, and error handling.
""",
        ),
        _t(
            "Conditionals, loops & handlers",
            "9 min",
            """\
# Conditionals, loops & handlers

## when — run tasks conditionally

```yaml
- name: Install apache (Debian only)
  ansible.builtin.apt: { name: apache2, state: present }
  when: ansible_facts['os_family'] == "Debian"
```

## loop — repeat a task

```yaml
- name: Create users
  ansible.builtin.user: { name: "{{ item }}" }
  loop: [ada, bob, cara]
```

## Handlers — run once, at the end, only if notified

```yaml
tasks:
  - template: { src: nginx.conf.j2, dest: /etc/nginx/nginx.conf }
    notify: restart nginx
handlers:
  - name: restart nginx
    ansible.builtin.service: { name: nginx, state: restarted }
```

## block / rescue — error handling

```yaml
- block:
    - command: /opt/risky.sh
  rescue:
    - debug: { msg: "it failed, rolling back" }
```

Use **tags** (`--tags deploy`) to run only part of a playbook.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_ANSIBLE_ADVANCED = SeedCourse(
    slug="ansible-advanced",
    title="Ansible — Advanced",
    description=(
        "Operate Ansible at scale: encrypting secrets with Vault, dynamic "
        "inventory and execution strategies, and testing/CI with Molecule and "
        "collections."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Ansible Vault & secrets",
            "9 min",
            """\
# Ansible Vault & secrets

Playbooks often need passwords, API keys, certificates — which must **not** sit
in plaintext in git. **Ansible Vault** encrypts them.

```bash
ansible-vault create secrets.yml         # create encrypted file
ansible-vault edit secrets.yml           # edit in place
ansible-vault encrypt group_vars/prod/vault.yml
```

Encrypted vars are used transparently when you supply the key at run time:

```bash
ansible-playbook site.yml --ask-vault-pass
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

You can even encrypt a **single value** inline:

```yaml
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  6536...
```

Convention: keep public vars in `vars.yml` and secret ones in an encrypted
`vault.yml`, referenced from the same group.

**Next:** dynamic inventory and scaling.
""",
        ),
        _t(
            "Dynamic inventory & scaling",
            "9 min",
            """\
# Dynamic inventory & scaling

A static inventory file doesn't fit the cloud, where hosts come and go.
**Dynamic inventory** queries the source of truth (AWS, GCP, Azure, k8s) at run
time via an inventory plugin:

```yaml
# aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions: [us-east-1]
keyed_groups:
  - key: tags.Role        # group hosts by their Role tag
```

```bash
ansible-inventory -i aws_ec2.yml --graph
```

## Scaling execution

- **Strategies**: `free` lets hosts run independently (vs the default `linear`
  lockstep); `forks` controls parallelism.
- **`serial`** does rolling updates — N hosts at a time — so a bad change
  doesn't hit the whole fleet:

```yaml
- hosts: web
  serial: 2          # two at a time
```

- **`delegate_to`** runs a task on a different host (e.g. update a load
  balancer); **`async`** runs long tasks without blocking.

**Next:** testing and CI.
""",
        ),
        _t(
            "Testing, CI & collections",
            "9 min",
            """\
# Testing, CI & collections

## Lint and dry-run

```bash
ansible-lint site.yml                 # best-practice linting
ansible-playbook site.yml --check     # dry run: report changes, make none
ansible-playbook site.yml --check --diff
```

`--check` plus an **idempotence test** (run twice; the second run must report
zero `changed`) is the core quality gate for automation.

## Molecule — test roles

**Molecule** spins up a container/VM, applies a role, and asserts the result —
so roles are tested like software:

```bash
molecule test    # create -> converge -> idempotence -> verify -> destroy
```

Wire `ansible-lint` + `molecule` into CI so every change to a role is verified.

## Collections

Modules now ship in **collections** (`ansible.builtin`, `community.general`,
`amazon.aws`), versioned and installed via Galaxy:

```bash
ansible-galaxy collection install community.general
```

For teams, **AWX / Ansible Automation Platform** adds a UI, scheduling, RBAC and
audit on top.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


IAC_COURSES: tuple[SeedCourse, ...] = (
    _TF_BASICS,
    _TF_INTERMEDIATE,
    _TF_ADVANCED,
    _ANSIBLE_BASICS,
    _ANSIBLE_INTERMEDIATE,
    _ANSIBLE_ADVANCED,
)

__all__ = ["IAC_COURSES"]
