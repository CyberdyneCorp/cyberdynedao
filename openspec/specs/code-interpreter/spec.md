# code-interpreter Specification

## Purpose

Run a code lesson's source on the matching engine (MATLAB or Python) as the
signed-in learner, returning output, artifacts, and (for Python) a variable
namespace + inline rich outputs. (src: adapters/inbound/api/code/router.py,
application/code)

## Requirements

### Requirement: Authenticated, engine-routed code run

The system SHALL expose `POST /api/v1/lessons/{lesson_id}/code/run` to a user
principal only (else `403`); empty source or an unknown language SHALL return
`422`. `language="python"` SHALL route to the Python interpreter; otherwise
(default) to MATLAB. MATLAB SHALL use a deterministic per-`(lesson, user)`
session (stateful across runs within a lesson); Python SHALL use a
server-issued session per run under the restricted sandbox. The bearer SHALL
be forwarded so artifacts land in the learner's workspace.

#### Scenario: MATLAB per-(lesson,user) session

- GIVEN user U1 runs code in lesson L1
- WHEN the run executes
- THEN it uses session id `lesson-L1-U1`

#### Scenario: Two users are isolated

- GIVEN U1 and U2 run code in the same lesson
- WHEN both run
- THEN each gets a distinct session and variables do not leak between them

#### Scenario: Unauthenticated rejected

- GIVEN no user token
- WHEN a code run is requested
- THEN the system SHALL respond `403`

### Requirement: Unified run response with variables + rich outputs

The system SHALL return `{ok, stdout, stderr, artifacts, sessionId, timedOut,
variables, richOutputs}`. For Python, `variables` (name/type/repr/sizeBytes)
and `richOutputs` (mimeType/artifact/text) SHALL be populated when the backend
reports them, and an interpreter error SHALL be folded into `stderr`. For
MATLAB, `variables` and `richOutputs` SHALL be empty (figures surface via
`artifacts`).

#### Scenario: Python surfaces variables and plots

- GIVEN a Python run that defines a variable and emits a figure
- WHEN it completes
- THEN `variables` and `richOutputs` are populated

#### Scenario: MATLAB leaves the new fields empty

- GIVEN a MATLAB run
- WHEN it completes
- THEN `variables` and `richOutputs` are empty
