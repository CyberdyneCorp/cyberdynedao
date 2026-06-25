"""Curated Academy course content — the source of truth for the built-in
MATLAB and Python courses.

Until now the academy's lesson content lived only in the database (created
ad-hoc through the admin UI), so it couldn't be reviewed or re-provisioned.
This module version-controls a rich curriculum and applies it idempotently.

Titles are kept in sync with the live courses so reconciliation updates the
existing lessons in place. Reconciliation is non-destructive and matched by
title:
  * a lesson whose title (case-insensitive) already exists and has the same
    type is updated in place — its id is kept, so learner progress and any
    attached quiz survive;
  * a curated lesson with no match is appended;
  * existing lessons the seed doesn't mention (e.g. a hand-authored quiz) are
    left untouched, never deleted or overwritten.

Run it with ``python -m cyberdyne_backend.cli.seed_academy`` (see that module).
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from cyberdyne_backend.application.courses.seed_adaptive_dsp import ADAPTIVE_DSP_COURSES
from cyberdyne_backend.application.courses.seed_advanced_control import ADVANCED_CONTROL_COURSES
from cyberdyne_backend.application.courses.seed_aerial import AERIAL_COURSES
from cyberdyne_backend.application.courses.seed_algorithms import ALGORITHMS_COURSES
from cyberdyne_backend.application.courses.seed_analog_comms import ANALOG_COMMS_COURSES
from cyberdyne_backend.application.courses.seed_analog_ic import ANALOG_IC_COURSES
from cyberdyne_backend.application.courses.seed_antennas import ANTENNAS_COURSES
from cyberdyne_backend.application.courses.seed_audio_processing import AUDIO_PROCESSING_COURSES
from cyberdyne_backend.application.courses.seed_battery import BATTERY_COURSES
from cyberdyne_backend.application.courses.seed_circuit_analysis import CIRCUIT_ANALYSIS_COURSES
from cyberdyne_backend.application.courses.seed_coding_theory import CODING_THEORY_COURSES
from cyberdyne_backend.application.courses.seed_comparch import COMPARCH_COURSES
from cyberdyne_backend.application.courses.seed_computational_thinking import (
    COMPUTATIONAL_THINKING_COURSES,
)
from cyberdyne_backend.application.courses.seed_computing_foundations import (
    COMPUTING_FOUNDATIONS_COURSES,
)
from cyberdyne_backend.application.courses.seed_concurrency import CONCURRENCY_COURSES
from cyberdyne_backend.application.courses.seed_control import CONTROL_COURSES
from cyberdyne_backend.application.courses.seed_csharp import CSHARP_COURSES
from cyberdyne_backend.application.courses.seed_data_converters import DATA_CONVERTERS_COURSES
from cyberdyne_backend.application.courses.seed_databases import DATABASE_COURSES
from cyberdyne_backend.application.courses.seed_dataeng import DATAENG_COURSES
from cyberdyne_backend.application.courses.seed_devops import DEVOPS_COURSES
from cyberdyne_backend.application.courses.seed_digital_comms import DIGITAL_COMMS_COURSES
from cyberdyne_backend.application.courses.seed_digital_logic import DIGITAL_LOGIC_COURSES
from cyberdyne_backend.application.courses.seed_distributed import DISTRIBUTED_COURSES
from cyberdyne_backend.application.courses.seed_django import DJANGO_COURSES
from cyberdyne_backend.application.courses.seed_dsp import DSP_COURSES
from cyberdyne_backend.application.courses.seed_electric_drives import ELECTRIC_DRIVES_COURSES
from cyberdyne_backend.application.courses.seed_electromagnetics import ELECTROMAGNETICS_COURSES
from cyberdyne_backend.application.courses.seed_electronics import ELECTRONICS_COURSES
from cyberdyne_backend.application.courses.seed_embedded import EMBEDDED_COURSES
from cyberdyne_backend.application.courses.seed_emc import EMC_COURSES
from cyberdyne_backend.application.courses.seed_english_brazil import ENGLISH_BRAZIL_COURSES
from cyberdyne_backend.application.courses.seed_estimation import ESTIMATION_COURSES
from cyberdyne_backend.application.courses.seed_fiber_optics import FIBER_OPTICS_COURSES
from cyberdyne_backend.application.courses.seed_filter_design import FILTER_DESIGN_COURSES
from cyberdyne_backend.application.courses.seed_fpga import FPGA_COURSES
from cyberdyne_backend.application.courses.seed_git import GIT_COURSES
from cyberdyne_backend.application.courses.seed_high_voltage import HIGH_VOLTAGE_COURSES
from cyberdyne_backend.application.courses.seed_hwverification import HW_VERIFICATION_COURSES
from cyberdyne_backend.application.courses.seed_iac import IAC_COURSES
from cyberdyne_backend.application.courses.seed_image_processing import IMAGE_PROCESSING_COURSES
from cyberdyne_backend.application.courses.seed_languages import LANGUAGE_COURSES
from cyberdyne_backend.application.courses.seed_linux import LINUX_COURSES
from cyberdyne_backend.application.courses.seed_machines import MACHINES_COURSES
from cyberdyne_backend.application.courses.seed_math import MATH_COURSES
from cyberdyne_backend.application.courses.seed_microwave import MICROWAVE_COURSES
from cyberdyne_backend.application.courses.seed_ml import ML_COURSES
from cyberdyne_backend.application.courses.seed_mobilerobotics import MOBILE_ROBOTICS_COURSES
from cyberdyne_backend.application.courses.seed_networking import NETWORKING_COURSES
from cyberdyne_backend.application.courses.seed_os import OS_COURSES
from cyberdyne_backend.application.courses.seed_pcb import PCB_COURSES
from cyberdyne_backend.application.courses.seed_photonics import PHOTONICS_COURSES
from cyberdyne_backend.application.courses.seed_physics import PHYSICS_COURSES
from cyberdyne_backend.application.courses.seed_power_electronics import POWER_ELECTRONICS_COURSES
from cyberdyne_backend.application.courses.seed_power_protection import POWER_PROTECTION_COURSES
from cyberdyne_backend.application.courses.seed_power_systems import POWER_SYSTEMS_COURSES
from cyberdyne_backend.application.courses.seed_prob_stats_python import (
    PROB_STATS_PYTHON_COURSES,
)
from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
from cyberdyne_backend.application.courses.seed_radar import RADAR_COURSES
from cyberdyne_backend.application.courses.seed_rails import RAILS_COURSES
from cyberdyne_backend.application.courses.seed_renewable_ev import RENEWABLE_EV_COURSES
from cyberdyne_backend.application.courses.seed_rf_comms import RF_COMMS_COURSES
from cyberdyne_backend.application.courses.seed_rfic import RFIC_COURSES
from cyberdyne_backend.application.courses.seed_robotics import ROBOTICS_COURSES
from cyberdyne_backend.application.courses.seed_security import SECURITY_COURSES
from cyberdyne_backend.application.courses.seed_semiconductors import SEMICONDUCTOR_COURSES
from cyberdyne_backend.application.courses.seed_sensors import SENSORS_COURSES
from cyberdyne_backend.application.courses.seed_signal_integrity import SIGNAL_INTEGRITY_COURSES
from cyberdyne_backend.application.courses.seed_signals import SIGNALS_COURSES
from cyberdyne_backend.application.courses.seed_smart_grid import SMART_GRID_COURSES
from cyberdyne_backend.application.courses.seed_software_architecture import (
    SOFTWARE_ARCHITECTURE_COURSES,
)
from cyberdyne_backend.application.courses.seed_software_quality import SOFTWARE_QUALITY_COURSES
from cyberdyne_backend.application.courses.seed_statistics import STATISTICS_COURSES
from cyberdyne_backend.application.courses.seed_stochastic_processes import (
    STOCHASTIC_PROCESSES_COURSES,
)
from cyberdyne_backend.application.courses.seed_systemdesign import SYSTEM_DESIGN_COURSES
from cyberdyne_backend.application.courses.seed_sysverilog import SYSVERILOG_COURSES
from cyberdyne_backend.application.courses.seed_technical_english import (
    TECHNICAL_ENGLISH_COURSES,
)
from cyberdyne_backend.application.courses.seed_test_measurement import TEST_MEASUREMENT_COURSES
from cyberdyne_backend.application.courses.seed_testing import TESTING_COURSES
from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    apply_quiz_spec,
)
from cyberdyne_backend.application.courses.seed_vectorcalc import VECTORCALC_COURSES
from cyberdyne_backend.application.courses.seed_vlsi import VLSI_COURSES
from cyberdyne_backend.application.courses.seed_webdev import WEBDEV_COURSES
from cyberdyne_backend.application.courses.seed_wireless_comms import WIRELESS_COMMS_COURSES
from cyberdyne_backend.application.quizzes.use_cases import (
    OptionInput,
    QuestionInput,
    UpsertQuiz,
    UpsertQuizCommand,
)
from cyberdyne_backend.domain.courses import (
    Course,
    CourseNotFoundError,
    CourseRepository,
    Lesson,
    new_course,
    new_lesson,
)

# ── Content ──────────────────────────────────────────────────────────────

_MATLAB = SeedCourse(
    slug="matlab-basics",
    title="Matlab Basics",
    description=(
        "Go from zero to writing and running your own MATLAB scripts: the "
        "workspace, variables and matrices, element-wise vs. matrix math, and "
        "how a script executes — with code you run live in the browser."
    ),
    level="Beginner",
    lessons=(
        SeedLesson(
            title="Welcome to MATLAB",
            lesson_type="text",
            duration="6 min",
            text_body="""\
# Welcome to MATLAB

MATLAB (*Matrix Laboratory*) is a numerical computing language built around
one idea: **everything is a matrix**. A single number is just a 1x1 matrix and
a row vector is 1xN, so the same operators work whether you're adding two
numbers or two thousand.

## Where you type things

- **Command Window** — type an expression, press Enter, see the result now.
- **Editor** — write reusable `.m` script files (you'll do this shortly).
- **Workspace** — every variable you create lives here until you `clear` it.

## Your first expressions

```matlab
2 + 2          % 4
x = 5;         % the ; suppresses output — x is stored silently
y = x .^ 2     % 25  (no semicolon, so MATLAB prints it)
```

A `%` starts a comment. A trailing `;` hides the result but still runs the
line — use it to keep the Command Window tidy.

## Getting help

`help sin` prints quick docs for any function; `doc sin` opens the full page.

**Next:** how MATLAB stores data — variables, vectors, and matrices.
""",
        ),
        SeedLesson(
            title="Variables & Matrices",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Variables & Matrices

You never declare a type in MATLAB — assign a value and the variable exists.

```matlab
name = "Ada";      % a string
n    = 42;         % a number
v    = [1 2 3 4];  % a row vector
```

## Building matrices

Spaces (or commas) separate columns; semicolons separate rows:

```matlab
A = [1 2 3;
     4 5 6];       % a 2x3 matrix
size(A)            % [2 3]
```

Handy generators: `zeros(2,3)`, `ones(3)`, `eye(3)` (identity), and the
**colon operator** for ranges:

```matlab
t = 0:0.5:2        % [0 0.5 1 1.5 2]  — start:step:stop
```

## Indexing (1-based!)

MATLAB indices start at **1**, not 0.

```matlab
v(1)        % first element
A(2, 3)     % row 2, column 3  -> 6
A(:, 2)     % every row of column 2  -> [2; 5]
v(end)      % last element
```

## Element-wise vs. matrix math

This trips up everyone: `*` is **matrix** multiplication, `.*` is
**element-wise**. The same goes for `./` and `.^`, and `'` transposes.

```matlab
[1 2 3] .* [4 5 6]   % [4 10 18]  element-wise
[1 2 3] *  [4;5;6]   % 32         row x column (dot product)
```

**Next:** turning these expressions into a script that runs top to bottom.
""",
        ),
        SeedLesson(
            title="How a MATLAB script runs",
            lesson_type="text",
            duration="7 min",
            text_body="""\
# How a MATLAB script runs

A **script** is a `.m` file of statements that execute **top to bottom**,
sharing the same workspace as the Command Window. There's no `main()` — the
first line runs first, and each line updates the workspace as the interpreter
walks the file:

```mermaid
flowchart TD
  A[Read next line] --> B{Statement type?}
  B -->|Assignment| C[Store variable in workspace]
  B -->|Expression| D[Evaluate and display]
  C --> E[More lines?]
  D --> E
  E -->|Yes| A
  E -->|No| F([Done])
```

## Printing results

- `disp(value)` — print one value, no name.
- `fprintf("mean = %.2f\\n", mean(y))` — formatted, C-style printing.
- Drop the `;` to let MATLAB echo a value with its variable name.

## A small script

```matlab
total = 0;
for k = 1:5
    total = total + k^2;   % 1 + 4 + 9 + 16 + 25
end
fprintf('sum of squares = %d\\n', total)   % 55
```

## Scripts vs. functions

A script shares your workspace; a **function** gets its own and takes inputs:

```matlab
function r = rms(v)
    r = sqrt(mean(v .^ 2));
end
```

> Tip: open the **code** lesson next and run a script yourself.
""",
        ),
        SeedLesson(
            title="Control flow: if, for & while",
            lesson_type="text",
            duration="11 min",
            text_body="""\
# Control flow: if, for & while

Real programs make **decisions** and **repeat** work. MATLAB groups every
block with the keyword `end` (indenting is style, not syntax). Conditions use
`==`, `~=` (not equal), `&&` (and), `||` (or).

## if / elseif / else

Branches are tested top to bottom; the first true one runs.

```matlab
score = 82;
if score >= 90
    grade = 'A';
elseif score >= 80
    grade = 'B';
else
    grade = 'C';
end
disp(grade)   % B
```

```mermaid
flowchart TD
  A{score at least 90} -->|yes| B[grade A]
  A -->|no| C{score at least 80}
  C -->|yes| D[grade B]
  C -->|no| E[grade C]
```

## for — repeat a known number of times

A `for` walks the columns of whatever you give it; `1:5` is just a row vector.

```matlab
total = 0;
for k = 1:5
    total = total + k;     % 1+2+3+4+5
end
fprintf('total = %d\\n', total)   % 15
```

## while — repeat until the condition is false

```matlab
n = 1;
while n < 100
    n = n * 2;   % 1, 2, 4, ... 128 -> stops
end
```

```mermaid
flowchart TD
  S([start]) --> C{condition true}
  C -->|yes| B[run loop body]
  B --> C
  C -->|no| E([exit loop])
```

## break and continue

Inside any loop:

- **`break`** leaves the loop immediately.
- **`continue`** skips the rest of this pass and jumps to the next one.

```matlab
for n = 1:7
    if n == 5
        break;        % stop entirely at 5
    end
    if mod(n, 2) == 0
        continue;     % skip even numbers
    end
    disp(n)           % prints 1, 3
end
```

```mermaid
flowchart TD
  N[next item] --> Q{break?}
  Q -->|yes| X([leave loop])
  Q -->|no| S{continue?}
  S -->|yes| N
  S -->|no| B[run body]
  B --> N
```

> Every `if` / `for` / `while` must be closed with its own `end`.
""",
        ),
        SeedLesson(
            title="Run your first script",
            lesson_type="code",
            duration="10 min",
            text_body="""\
% Your first MATLAB script — edit it and press Run.
% Build a matrix, transpose it, and combine the two.

A = [1 2; 3 4];
B = A';            % transpose
C = A * B;         % matrix multiply

disp('A * A^T =')
disp(C)
fprintf('trace = %d\\n', trace(C))   % sum of the diagonal

% Try it yourself:
%   1. Change A to a 3x3 matrix and re-run.
%   2. Compare C = A * B (matrix) with A .* B (element-wise) — why the error?
""",
        ),
    ),
)

_PYTHON = SeedCourse(
    slug="python-course",
    title="Python Course",
    description=(
        "A hands-on introduction to Python: values and types, how the "
        "interpreter runs your code, and writing your first runnable script — "
        "executed live in a sandboxed interpreter."
    ),
    level="Beginner",
    lessons=(
        SeedLesson(
            title="Welcome to Python",
            lesson_type="text",
            duration="6 min",
            text_body="""\
# Welcome to Python

Python is a readable, batteries-included language used for scripting, data,
the web, and AI. Its defining trait: **indentation defines structure** — there
are no curly braces.

## What this course covers

- values, variables and the core types
- how the interpreter turns your file into output
- writing and running your own script
- a quick knowledge check

## Your first lines

```python
print("hello, cyberdyne")
name = "Ada"
print(f"welcome, {name}")     # f-strings drop expressions in { }
```

`print()` shows a value and `type(x)` tells you its type. There's no compile
step you manage by hand — you run the file and see the result.

**Next:** the values and types you'll use everywhere.
""",
        ),
        SeedLesson(
            title="Variables & Types",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Variables & Types

Python is **dynamically typed** — assign a value and the variable exists, no
declaration needed.

```python
name = "Ada"        # str
age = 36            # int
pi = 3.14159        # float
ready = True        # bool
```

Inspect a type with `type(x)`; format text with f-strings:

```python
print(f"{name} is {age}")        # Ada is 36
print(f"pi to 2dp = {pi:.2f}")   # pi to 2dp = 3.14
```

## The everyday collections

```python
nums = [1, 2, 3]            # list — ordered, mutable
nums.append(4)             # [1, 2, 3, 4]
nums[0], nums[-1]          # 1, 4   (0-based; -1 is the last)

user = {"name": "Ada", "role": "admin"}   # dict — key -> value
user["role"]               # "admin"
user.get("email", "—")    # default if the key is missing
```

Rule of thumb: a **list** for an ordered collection, a **dict** when you look
things up by name.

**Next:** how Python actually runs the file you wrote.
""",
        ),
        SeedLesson(
            title="How Python runs your code",
            lesson_type="text",
            duration="6 min",
            text_body="""\
# How Python runs your code

When you run a `.py` file, Python compiles it to **bytecode** and a virtual
machine executes that, line by line, producing your output:

```mermaid
flowchart LR
  S([source.py]) --> C[Compile to bytecode]
  C --> V[Python VM executes]
  V --> O([Output])
```

Statements run top to bottom. Indentation (4 spaces) groups a block:

```python
for n in [1, 2, 3]:
    print(n * n)        # 1, 4, 9

total = 0
for k in range(1, 6):
    total += k          # 1+2+3+4+5
print("total =", total) # total = 15
```

A **comprehension** builds a list in one expressive line:

```python
squares = [k * k for k in range(1, 6)]
print("sum of squares =", sum(squares))   # 55
```

> Tip: open the **code** lesson next and run a script yourself.
""",
        ),
        SeedLesson(
            title="Control flow: if, for & while",
            lesson_type="text",
            duration="11 min",
            text_body="""\
# Control flow: if, for & while

Real programs make **decisions** and **repeat** work. Python uses
**indentation** (4 spaces) to mark a block and a colon `:` to open it.

## if / elif / else

Branches are tested top to bottom; the first true one runs.

```python
score = 82
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
print(grade)   # B
```

```mermaid
flowchart TD
  A{score at least 90} -->|yes| B[grade A]
  A -->|no| C{score at least 80}
  C -->|yes| D[grade B]
  C -->|no| E[grade C]
```

## for — repeat over a sequence

```python
for n in [1, 2, 3]:
    print(n * n)        # 1, 4, 9

for i in range(3):       # 0, 1, 2
    print(i)
```

## while — repeat until the condition is false

```python
total = 0
while total < 10:
    total += 3           # 3, 6, 9, 12 -> stops
```

```mermaid
flowchart TD
  S([start]) --> C{condition true}
  C -->|yes| B[run loop body]
  B --> C
  C -->|no| E([exit loop])
```

## break and continue

Inside any loop:

- **`break`** leaves the loop immediately.
- **`continue`** skips the rest of this pass and jumps to the next one.

```python
for n in range(1, 8):
    if n == 5:
        break            # stop entirely at 5
    if n % 2 == 0:
        continue         # skip even numbers
    print(n)             # prints 1, 3
```

```mermaid
flowchart TD
  N[next item] --> Q{break?}
  Q -->|yes| X([leave loop])
  Q -->|no| S{continue?}
  S -->|yes| N
  S -->|no| B[run body]
  B --> N
```

> Reach for **for** when you know what you're iterating over, **while** when
> you loop until something changes.
""",
        ),
        SeedLesson(
            title="Run your first Python script",
            lesson_type="code",
            duration="10 min",
            text_body="""\
# Your first Python script — edit it and press Run.
# Goal: summarise a small dataset of scores.

scores = [88, 72, 95, 64, 80, 91]

print(f"count:   {len(scores)}")
print(f"highest: {max(scores)}")
print(f"lowest:  {min(scores)}")
print(f"average: {sum(scores) / len(scores):.1f}")

# A comprehension to find who passed (>= 70):
passed = [s for s in scores if s >= 70]
print(f"passed:  {len(passed)} of {len(scores)}")

# Try it yourself:
#   1. Add a score of 100 and re-run — watch the average move.
#   2. Print the scores sorted high-to-low: sorted(scores, reverse=True)
""",
        ),
    ),
)

_BLOCKCHAIN = SeedCourse(
    slug="blockchain-basics",
    title="Blockchain Basics",
    description=(
        "Understand blockchains from first principles: the distributed-ledger "
        "idea, hashing and how blocks chain together, Proof-of-Work consensus "
        "(with a miner you run yourself), and how Bitcoin ties it all into "
        "peer-to-peer digital money."
    ),
    level="Beginner",
    lessons=(
        SeedLesson(
            title="What is a blockchain?",
            lesson_type="text",
            duration="8 min",
            text_body="""\
# What is a blockchain?

A blockchain is a **distributed ledger** — a database that many computers keep
a copy of, where everyone agrees on the same history without trusting a central
authority. A useful mental model is a very particular database:

- **fast to read**, but **slow to write** — every write needs the network to
  reach *consensus* first;
- **append-only** — you add new records, you don't edit old ones;
- **every write costs money** (a "gas" fee), so you store small things
  (amounts, hashes, short strings), not files.

## The problem it solves: double-spending

Digital money is just data — and data can be copied. What stops Alice paying
the same coin to two people?

```mermaid
flowchart TD
  A[Alice has 1 coin] --> B[pays Bob]
  A --> C[copies it]
  C --> D[pays Carol the same coin]
  B --> G[Double spend!]
  D --> G
  G --> H[Bank: a trusted middleman decides]
  G --> I[Blockchain: shared ledger + consensus]
```

A bank solves this by being a trusted middleman. A blockchain solves it by
making **everyone** hold the ledger and agree, via math, on which transaction
came first — no middleman required.

## A chain of blocks

Transactions are grouped into **blocks**, and each block points back to the one
before it, forming a chain:

```mermaid
flowchart LR
  G([Genesis]) --> B1[Block 1] --> B2[Block 2] --> B3[Block N...]
```

**Next:** the cryptographic glue that makes this chain tamper-evident — hashing.
""",
        ),
        SeedLesson(
            title="Hashing & blocks",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Hashing & blocks

A **hash function** (Bitcoin uses SHA-256) turns any input into a fixed-size
fingerprint. Three properties make it the backbone of a blockchain:

- **deterministic** — same input always gives the same hash;
- **one-way** — you can't reverse the hash back into the input;
- **avalanche** — change one character and the hash looks completely different.

```python
import hashlib
hashlib.sha256(b"hello").hexdigest()   # 2cf24dba5fb0a30e26e83b2ac5b9e29e...
hashlib.sha256(b"hellp").hexdigest()   # 7f1a... totally different
```

## What's in a block

| Field | Purpose |
|-------|---------|
| **Previous hash** | links to the block before it |
| **Transactions** | the data being recorded (a Merkle root, really) |
| **Timestamp** | when it was made |
| **Nonce** | a number miners search for (next lesson) |

Because each block includes the **previous block's hash**, the blocks are
chained — and that makes tampering obvious:

```mermaid
flowchart LR
  B1["Block 1\\nhash: 00a1"] --> B2["Block 2\\nprev: 00a1\\nhash: 00b2"]
  B2 --> B3["Block 3\\nprev: 00b2\\nhash: 00c3"]
```

If someone edits Block 1, its hash changes, so Block 2's "previous hash" no
longer matches — and every block after it breaks. To rewrite history you'd have
to redo **all** the following blocks, which (next lesson) is made deliberately
expensive.

**Next:** how the network agrees on new blocks — Proof of Work.
""",
        ),
        SeedLesson(
            title="Consensus & Proof of Work",
            lesson_type="text",
            duration="10 min",
            text_body="""\
# Consensus & Proof of Work

Only one block can be added at a time, and thousands of nodes must agree on
which. The rule they follow is the **consensus mechanism**. The original one,
used by Bitcoin, is **Proof of Work (PoW)**.

## The mining puzzle

Miners race to find a **nonce** that makes the block's hash fall below a
target — in practice, "start with N zeros". Hashing is unpredictable, so the
only way to find it is to try nonces one by one:

```mermaid
flowchart TD
  T[Take block data + nonce] --> H[Hash it]
  H --> Q{Hash starts with N zeros?}
  Q -->|no| I[nonce = nonce + 1] --> T
  Q -->|yes| B[Broadcast block, claim reward]
```

Finding the nonce is **hard** (lots of guessing), but checking it is **instant**
(one hash). That asymmetry is what secures the chain.

## Why it's secure: the 51% attack

To rewrite history an attacker must out-mine the rest of the network combined —
controlling **>50% of the hash power**. For Bitcoin that's billions in hardware
and energy. Even then they could only double-spend their own coins or censor
transactions; they **cannot** steal others' coins or mint new ones.

## Proof of Work vs Proof of Stake

| | Proof of Work | Proof of Stake |
|---|---|---|
| **Who writes** | first to solve the hash puzzle | a validator chosen by stake |
| **Cost to attack** | 51% of hash power | 51% of staked tokens |
| **Energy** | very high | low |
| **Examples** | Bitcoin, Litecoin | Ethereum, Cardano |

**Next:** run a tiny miner yourself.
""",
        ),
        SeedLesson(
            title="Mine a block (toy example)",
            lesson_type="code",
            duration="10 min",
            text_body="""\
# A toy Proof-of-Work miner. Edit and press Run.
# It searches for a nonce so the block "hash" starts with N zeros —
# exactly what Bitcoin miners do, just with a tiny stand-in hash.

def toy_hash(s):
    # A tiny teaching hash (NOT secure!). Real Bitcoin uses SHA-256.
    h = 2166136261
    for ch in s:
        h = ((h ^ ord(ch)) * 16777619) % (2 ** 32)
    return format(h, "08x")

block = "Alice -> Bob: 1 coin | prev: 0000abc"
zeros = 4                      # the difficulty: more zeros = more work
target = "0" * zeros

nonce = 0
digest = toy_hash(f"{block}{nonce}")
while not digest.startswith(target):
    nonce += 1
    digest = toy_hash(f"{block}{nonce}")

print(f"difficulty: {zeros} leading zeros")
print(f"nonce found: {nonce}")
print(f"block hash:  {digest}")

# Try it yourself:
#   1. Raise zeros to 5 and re-run — notice how much longer it takes.
#   2. Change one character of `block` and watch the nonce change completely.
""",
        ),
        SeedLesson(
            title="Bitcoin",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Bitcoin

Bitcoin (BTC) is the first cryptocurrency, launched in 2009 by the pseudonymous
**Satoshi Nakamoto** as "a peer-to-peer electronic cash system". It was the
first design to solve double-spending without a trusted middleman, by combining
a distributed ledger with Proof of Work.

| Property | Value |
|----------|-------|
| Created | January 2009 |
| Max supply | 21 million (fixed) |
| Block time | ~10 minutes |
| Consensus | Proof of Work (SHA-256) |
| Smallest unit | 1 satoshi = 0.00000001 BTC |

## Why it matters

- **Trust math, not institutions** — rules are enforced by code, not a bank.
- **Fixed supply** — 21M cap creates digital scarcity (no money printing).
- **Permissionless & borderless** — anyone can transact, 24/7, censorship-resistant.

## The UTXO model

Bitcoin doesn't store account balances. Instead your wallet owns **Unspent
Transaction Outputs (UTXOs)** — like physical coins. To spend, you consume
whole UTXOs as inputs and create new ones as outputs (the leftover is your
change; the gap is the miner's fee):

```mermaid
flowchart LR
  UA[UTXO 0.5 BTC] --> TX[Transaction]
  UB[UTXO 0.3 BTC] --> TX
  TX --> O1[0.6 BTC to Dave]
  TX --> O2[0.199 BTC change to Alice]
  TX --> FEE[0.001 BTC fee to miner]
```

## Halving

Every ~4 years (210,000 blocks) the block reward halves — 50 → 25 → ... →
3.125 BTC (2024). This steadily slows new supply until the last bitcoin is
mined around 2140.

> Bitcoin is intentionally simple and conservative. Programmable money — smart
> contracts, DeFi — is where chains like Ethereum and Solana go next.
""",
        ),
        SeedLesson(
            title="Check your knowledge",
            lesson_type="quiz",
            duration="3 min",
        ),
    ),
)

_BLOCKCHAIN_ADVANCED = SeedCourse(
    slug="blockchain-beyond-basics",
    title="Blockchain: Beyond the Basics",
    description=(
        "Go deeper into how chains actually work: Bitcoin Script (with a stack "
        "machine you run yourself), the main consensus families, self-custody "
        "with cold wallets, and Ethereum + Solidity for programmable money."
    ),
    level="Intermediate",
    lessons=(
        SeedLesson(
            title="Bitcoin Script",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Bitcoin Script

Bitcoin doesn't have "balances" — it has coins (UTXOs) locked by a tiny
program. To spend one you must supply inputs that make that program succeed.
That program is written in **Bitcoin Script**: a simple, **stack-based**
language that is deliberately **not Turing-complete** (no loops, no
recursion) — so validation always terminates and can't hang the network.

## Locking and unlocking

Every coin carries a **locking script** (`scriptPubKey`) — the puzzle. To
spend it you provide an **unlocking script** (`scriptSig`) — the solution. A
node concatenates them and runs the stack machine; the spend is valid if the
script finishes with a truthy value on top of the stack.

## P2PKH — "pay to public-key hash"

The classic locking script proves you own the private key behind an address:

```text
scriptPubKey:  OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
scriptSig:     <signature> <publicKey>
```

```mermaid
flowchart TD
  P[push sig + pubKey] --> D[OP_DUP duplicates pubKey]
  D --> H[OP_HASH160 hashes it]
  H --> E[OP_EQUALVERIFY: hash == pubKeyHash?]
  E --> C[OP_CHECKSIG: signature valid?]
  C --> R{stack top truthy?}
  R -->|yes| OK([spend allowed])
  R -->|no| NO([rejected])
```

Opcodes push data or pop operands and push results. Because the language is
intentionally limited, richer logic lives off-chain or on programmable chains
like Ethereum.

**Next:** run a tiny stack machine yourself.
""",
        ),
        SeedLesson(
            title="Run a Bitcoin Script (toy)",
            lesson_type="code",
            duration="10 min",
            text_body="""\
# A toy Bitcoin Script evaluator. Edit and press Run.
# Bitcoin Script is a STACK machine: numbers are pushed; opcodes pop
# operands and push results. A script "succeeds" if it ends with a single
# truthy value on the stack.

script = ["2", "3", "OP_ADD", "5", "OP_EQUALVERIFY", "1"]

stack = []
for token in script:
    if token == "OP_ADD":
        b = stack.pop(); a = stack.pop(); stack.append(a + b)
    elif token == "OP_DUP":
        stack.append(stack[-1])
    elif token == "OP_EQUALVERIFY":
        b = stack.pop(); a = stack.pop()
        if a != b:
            raise ValueError("EQUALVERIFY failed - script invalid")
    else:
        stack.append(int(token))     # a number literal: push it
    print(f"after {token:14} -> {stack}")

ok = len(stack) == 1 and stack[-1] != 0
print("script valid:", ok)

# Try it yourself:
#   1. Change the final "1" to "0" — the script ends "false" (invalid).
#   2. Make EQUALVERIFY fail (e.g. "2 3 OP_ADD 6 OP_EQUALVERIFY 1") and watch
#      the error — that's how an invalid spend is rejected.
""",
        ),
        SeedLesson(
            title="Consensus & its types",
            lesson_type="text",
            duration="10 min",
            text_body="""\
# Consensus & its types

Consensus is the rule that lets thousands of nodes agree on the next block
without a central authority. Different chains make different trade-offs between
**decentralization, security, speed, and energy**.

```mermaid
mindmap
  root((CONSENSUS))
    Proof of Work
      Mining
      Energy heavy
      Bitcoin
    Proof of Stake
      Validators stake
      Energy light
      Ethereum
    Variants
      DPoS
      PoA
      PoH
      BFT
```

| Mechanism | Who may add a block | Notes |
|-----------|---------------------|-------|
| **PoW** (Proof of Work) | first to solve a hash puzzle | secure, energy-heavy — Bitcoin |
| **PoS** (Proof of Stake) | a validator chosen by stake | energy-light — Ethereum, Cardano |
| **DPoS** (Delegated PoS) | a few delegates token-holders vote in | fast, more centralized — EOS, Tron |
| **PoA** (Proof of Authority) | a known, approved set of validators | private/consortium chains |
| **PoH** (Proof of History) | a verifiable clock ordering events | pairs with PoS — Solana |
| **BFT** (Byzantine Fault Tolerant) | validators vote in rounds | fast **finality** — Tendermint/Cosmos |

## Finality

- **Probabilistic** (PoW): a block gets *exponentially* safer as more blocks
  pile on top — Bitcoin users wait ~6 confirmations.
- **Deterministic** (BFT-style): once validators vote, the block is final and
  can't be reverted.

## Attacking consensus

PoW needs **51% of hash power**; PoS needs **51% of stake**. PoS adds
**slashing** — misbehaving validators lose part of their stake, making attacks
costly without burning energy.

**Next:** holding the keys to your coins safely.
""",
        ),
        SeedLesson(
            title="Cold wallets & self-custody",
            lesson_type="text",
            duration="8 min",
            text_body="""\
# Cold wallets & self-custody

Your coins live on-chain; what you actually hold is the **private key** that
authorizes spending them. "Not your keys, not your coins."

| | Hot wallet | Cold wallet |
|--|------------|-------------|
| **Connected** | online (app, exchange, browser) | offline hardware device |
| **Convenience** | high | lower |
| **Attack surface** | large (malware, phishing, exchange hacks) | tiny — keys never leave the device |
| **Use for** | small, day-to-day amounts | long-term savings |

## How a hardware wallet works

A device like a Ledger or Trezor stores the private key in a secure chip. When
you send funds, the transaction is sent **to** the device, you confirm on its
screen, and only the **signature** comes back — the key never touches your
(possibly compromised) computer.

```mermaid
flowchart LR
  PC[Laptop builds tx] --> D[Hardware wallet signs offline]
  D --> PC2[Signed tx returns]
  PC2 --> N[Broadcast to network]
```

## The seed phrase (BIP-39)

Your key is backed up as **12 or 24 words**. Anyone with those words controls
the funds, so:

- write them on paper or steel — **never** a photo, cloud note, or password
  manager;
- store copies in separate secure places;
- nobody legitimate will ever ask for them.

> Self-custody means you are the bank: total control, total responsibility.

**Next:** programmable money on Ethereum.
""",
        ),
        SeedLesson(
            title="Ethereum",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Ethereum

If Bitcoin is digital gold, **Ethereum is a world computer**. Launched in 2015
by Vitalik Buterin, it lets anyone deploy **smart contracts** — programs that
run exactly as written on every node.

| Property | Value |
|----------|-------|
| Created | 2015 |
| Consensus | Proof of Stake (since 2022) |
| Block time | ~12 seconds |
| Languages | Solidity, Vyper |
| Supply | no hard cap (fee-burning can make it deflationary) |

## Accounts, not UTXOs

Bitcoin tracks unspent outputs; Ethereum keeps running **balances** in
accounts — closer to a bank ledger, and simpler for contracts to reason about.

| | Bitcoin | Ethereum |
|--|---------|----------|
| **Model** | UTXO | Account balances |
| **Question** | "What if money couldn't be printed?" | "What if contracts couldn't be broken?" |

Two account kinds: **EOAs** (controlled by a private key — people) and
**contract accounts** (controlled by their code).

## The EVM and gas

The **Ethereum Virtual Machine** runs contract bytecode on every node. Each
operation costs **gas**, paid in ETH — this both compensates validators and
stops infinite loops (run out of gas → the transaction reverts).

## Composability

Contracts can call other contracts, so protocols snap together like
money-legos — the foundation of DeFi, NFTs, and DAOs.

**Next:** write a contract in Solidity.
""",
        ),
        SeedLesson(
            title="Solidity",
            lesson_type="text",
            duration="10 min",
            text_body="""\
# Solidity

**Solidity** is the statically-typed language for Ethereum smart contracts. A
`contract` is much like a class: it has persistent **state** (stored on-chain,
so writing costs gas) and **functions** that read or change it.

## Core types

| Type | Use |
|------|-----|
| `uint` / `int` | numbers (`uint` = `uint256`) — counters, balances |
| `address` / `address payable` | account addresses; payable can receive ETH |
| `bool`, `string`, `bytes32` | flags, text, fixed hashes |
| `mapping(key => value)` | on-chain hashmap (e.g. balances) |
| `struct`, `enum`, arrays | grouped / custom data |

## A first contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleStorage {
    uint storedData;                 // state — lives on-chain

    function set(uint x) public {    // changes state -> costs gas
        storedData = x;
    }

    function get() public view returns (uint) {  // read-only -> free
        return storedData;
    }
}
```

Functions marked `payable` may receive ETH; `view` functions only read and
cost no gas when called externally.

## Security matters most

A deployed contract is public and immutable, and it holds real money — bugs are
exploits. The classic one is **reentrancy**: a contract calls out to another
*before* updating its own state, letting the callee re-enter and drain funds.

> Follow **checks-effects-interactions**: validate inputs, update your state,
> *then* make external calls. Audit before you deploy.

**Next:** check your knowledge.
""",
        ),
        SeedLesson(
            title="Check your knowledge",
            lesson_type="quiz",
            duration="4 min",
        ),
    ),
)

_RAW_COURSES: tuple[SeedCourse, ...] = (
    _MATLAB,
    _PYTHON,
    _BLOCKCHAIN,
    _BLOCKCHAIN_ADVANCED,
    *LANGUAGE_COURSES,
    *DATABASE_COURSES,
    *DEVOPS_COURSES,
    *IAC_COURSES,
    *LINUX_COURSES,
    *PHYSICS_COURSES,
    *MATH_COURSES,
    *VECTORCALC_COURSES,
    *STATISTICS_COURSES,
    *ROBOTICS_COURSES,
    *ALGORITHMS_COURSES,
    *CSHARP_COURSES,
    *SIGNALS_COURSES,
    *CONTROL_COURSES,
    *DIGITAL_LOGIC_COURSES,
    *ELECTRONICS_COURSES,
    *POWER_ELECTRONICS_COURSES,
    *EMBEDDED_COURSES,
    *ELECTROMAGNETICS_COURSES,
    *RF_COMMS_COURSES,
    *SENSORS_COURSES,
    *PCB_COURSES,
    *SEMICONDUCTOR_COURSES,
    *VLSI_COURSES,
    *DSP_COURSES,
    *MACHINES_COURSES,
    *COMPARCH_COURSES,
    *SYSVERILOG_COURSES,
    *ANALOG_IC_COURSES,
    *PHOTONICS_COURSES,
    *BATTERY_COURSES,
    *DIGITAL_COMMS_COURSES,
    *MICROWAVE_COURSES,
    *ML_COURSES,
    *SECURITY_COURSES,
    *GIT_COURSES,
    *OS_COURSES,
    *TESTING_COURSES,
    *NETWORKING_COURSES,
    *SYSTEM_DESIGN_COURSES,
    *DISTRIBUTED_COURSES,
    *WEBDEV_COURSES,
    *DATAENG_COURSES,
    *CONCURRENCY_COURSES,
    *SIGNAL_INTEGRITY_COURSES,
    *EMC_COURSES,
    *TEST_MEASUREMENT_COURSES,
    *HW_VERIFICATION_COURSES,
    *ANTENNAS_COURSES,
    *AERIAL_COURSES,
    *MOBILE_ROBOTICS_COURSES,
    *ESTIMATION_COURSES,
    *FPGA_COURSES,
    *POWER_SYSTEMS_COURSES,
    *PROB_STATS_PYTHON_COURSES,
    *CIRCUIT_ANALYSIS_COURSES,
    *FILTER_DESIGN_COURSES,
    *DATA_CONVERTERS_COURSES,
    *RFIC_COURSES,
    *STOCHASTIC_PROCESSES_COURSES,
    *CODING_THEORY_COURSES,
    *ANALOG_COMMS_COURSES,
    *WIRELESS_COMMS_COURSES,
    *FIBER_OPTICS_COURSES,
    *RADAR_COURSES,
    *IMAGE_PROCESSING_COURSES,
    *AUDIO_PROCESSING_COURSES,
    *ADAPTIVE_DSP_COURSES,
    *ADVANCED_CONTROL_COURSES,
    *ELECTRIC_DRIVES_COURSES,
    *HIGH_VOLTAGE_COURSES,
    *POWER_PROTECTION_COURSES,
    *SMART_GRID_COURSES,
    *RENEWABLE_EV_COURSES,
    *SOFTWARE_ARCHITECTURE_COURSES,
    *SOFTWARE_QUALITY_COURSES,
    *COMPUTATIONAL_THINKING_COURSES,
    *COMPUTING_FOUNDATIONS_COURSES,
    *TECHNICAL_ENGLISH_COURSES,
    *ENGLISH_BRAZIL_COURSES,
    *DJANGO_COURSES,
    *RAILS_COURSES,
)


def _with_registry_quizzes(courses: tuple[SeedCourse, ...]) -> tuple[SeedCourse, ...]:
    """Attach checkpoint + final quizzes from ``QUIZ_REGISTRY`` to each course
    that has a spec. Courses already carrying interleaved quizzes inline (the
    Linux track) aren't in the registry, so they pass through untouched."""
    return tuple(
        apply_quiz_spec(course, QUIZ_REGISTRY[course.slug])
        if course.slug in QUIZ_REGISTRY
        else course
        for course in courses
    )


ACADEMY_COURSES: tuple[SeedCourse, ...] = _with_registry_quizzes(_RAW_COURSES)


# ── Apply ────────────────────────────────────────────────────────────────


async def seed_courses(
    repo: CourseRepository,
    *,
    courses: tuple[SeedCourse, ...] = ACADEMY_COURSES,
    now: datetime | None = None,
    quiz_author: UpsertQuiz | None = None,
) -> list[str]:
    """Upsert each curated course and return a human-readable summary per
    course. Idempotent: a second run produces no further changes.

    When ``quiz_author`` is supplied, curated quiz lessons that carry questions
    (``SeedLesson.quiz``) are authored after the course is saved (lesson ids are
    stable by then). Without it, lesson structure is reconciled but quizzes are
    left alone — so the in-memory unit tests don't need a quiz repo."""
    summary: list[str] = []
    for spec in courses:
        course, created = await _get_or_create(repo, spec, now=now)
        _apply_metadata(course, spec)
        added, updated = _reconcile_lessons(course, spec, now=now)
        course.publish(now=now)
        await repo.save(course)
        authored = 0
        if quiz_author is not None:
            authored = await _author_quizzes(quiz_author, course, spec)
        verb = "created" if created else "updated"
        summary.append(
            f"{spec.slug}: {verb} (+{added} lessons, {updated} updated, "
            f"{len(course.lessons)} total, {authored} quizzes)"
        )
    return summary


async def _author_quizzes(quiz_author: UpsertQuiz, course: Course, spec: SeedCourse) -> int:
    """Author each curated quiz lesson's questions against the saved lesson id.
    Idempotent: ``UpsertQuiz`` fully replaces the lesson's quiz each run."""
    wanted = {
        sl.title.casefold(): sl for sl in spec.lessons if sl.lesson_type == "quiz" and sl.quiz
    }
    authored = 0
    for lesson in course.lessons:
        if lesson.lesson_type.value != "quiz":
            continue
        sl = wanted.get(lesson.title.casefold())
        if sl is None:
            continue
        cmd = UpsertQuizCommand(
            passing_score=sl.passing_score,
            questions=[
                QuestionInput(
                    prompt=question.prompt,
                    explanation=question.explanation,
                    options=[
                        OptionInput(text=o.text, is_correct=o.is_correct) for o in question.options
                    ],
                )
                for question in sl.quiz
            ],
        )
        await quiz_author.execute(lesson.id, cmd)
        authored += 1
    return authored


async def _get_or_create(
    repo: CourseRepository, spec: SeedCourse, *, now: datetime | None
) -> tuple[Course, bool]:
    try:
        return await repo.get_by_slug(spec.slug, include_drafts=True), False
    except CourseNotFoundError:
        course = new_course(
            title=spec.title,
            description=spec.description,
            level=spec.level,
            slug=spec.slug,
            now=now,
        )
        return course, True


def _apply_metadata(course: Course, spec: SeedCourse) -> None:
    course.description = spec.description
    # The slug (the stable key) is left alone so existing links and progress
    # keep resolving.


def _reconcile_lessons(
    course: Course, spec: SeedCourse, *, now: datetime | None
) -> tuple[int, int]:
    by_title = {lesson.title.casefold(): lesson for lesson in course.lessons}
    added = updated = 0
    ordered: list[Lesson] = []
    seen: set[UUID] = set()
    for sl in spec.lessons:
        existing = by_title.get(sl.title.casefold())
        if existing is not None and existing.lesson_type.value == sl.lesson_type:
            # Quiz lessons carry no body; only refresh text/code content.
            if sl.lesson_type in ("text", "code"):
                existing.set_content(text_body=sl.text_body, duration=sl.duration, now=now)
            updated += 1
            ordered.append(existing)
            seen.add(existing.id)
        elif existing is None:
            lesson = new_lesson(
                course_id=course.id,
                title=sl.title,
                lesson_type=sl.lesson_type,
                text_body=sl.text_body,
                duration=sl.duration,
                sort_order=len(ordered),
                now=now,
            )
            ordered.append(lesson)
            added += 1
        else:
            # A lesson with this title but a different type exists — leave it
            # untouched rather than clobber hand-authored content, but keep it.
            ordered.append(existing)
            seen.add(existing.id)
    # Preserve any existing lessons the seed doesn't mention (e.g. a
    # hand-authored quiz), appended after the curated sequence.
    for lesson in course.lessons:
        if lesson.id not in seen and lesson not in ordered:
            ordered.append(lesson)
    # Honour the curated order so interleaved quiz lessons land in position —
    # ids are preserved, so learner progress survives the reorder.
    for index, lesson in enumerate(ordered):
        lesson.sort_order = index
    course.lessons[:] = ordered
    return added, updated


__all__ = ["ACADEMY_COURSES", "SeedCourse", "SeedLesson", "seed_courses"]
