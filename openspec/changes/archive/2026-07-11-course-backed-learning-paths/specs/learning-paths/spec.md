## ADDED Requirements

### Requirement: Course-backed modules (stages)

A learning module SHALL optionally bundle one or more courses via `courseSlugs`. A module with `courseSlugs` represents a **stage** in a path whose substance is those courses; its title/level/duration/icon/topics remain the stage's display metadata. The public module and path read endpoints SHALL include each module's `courseSlugs` plus a lightweight expansion (`slug`, `title`, `level`) of the linked courses for rendering. A module MAY have zero linked courses (a legacy descriptive milestone).

#### Scenario: Module exposes its linked courses

- **GIVEN** a module `foundations` with `courseSlugs: ["python-course", "computational-thinking-basics"]`
- **WHEN** the public catalogue is read
- **THEN** the module reports those `courseSlugs` and an expansion carrying each course's slug/title/level

### Requirement: Derived module completion from linked courses

For a module with one or more `courseSlugs`, the system SHALL derive the user's module completion from course progress: the module is complete (100%) **iff every linked course is complete** for that user, and its percent is derived from the linked courses' completion. A module with no `courseSlugs` SHALL retain the legacy self-reported percent (`PATCH /learning/modules/{slug}/progress`). Path gating, eligibility, and certificate eligibility SHALL use this derived completion.

#### Scenario: Stage completes when all its courses are done

- **GIVEN** a module linking courses `c1` and `c2`, with `c1` complete and `c2` at 40%
- **WHEN** the user's path state is computed
- **THEN** the module is not complete
- **AND** when `c2` reaches 100% the module becomes complete

#### Scenario: Course-less module still self-reports

- **GIVEN** a seeded module with no linked courses
- **WHEN** the user PATCHes its progress to 100
- **THEN** it is complete, exactly as before this change

### Requirement: Admin assigns courses to a module

An editor SHALL set a module's linked courses by supplying `courseSlugs` on create/update of a module. Every slug SHALL reference an existing course; an unknown course slug SHALL be rejected with `422` and SHALL NOT persist.

#### Scenario: Assigning a real course to a stage

- **GIVEN** course `python-course` exists
- **WHEN** an editor sets module `foundations` `courseSlugs` to `["python-course"]`
- **THEN** the module stores that linkage and the public catalogue reflects it

#### Scenario: Unknown course rejected

- **WHEN** an editor sets a module's `courseSlugs` to include a slug with no matching course
- **THEN** the system SHALL respond `422` and the module is unchanged

### Requirement: Learner can browse and progress a path of courses

The learner UI SHALL provide a Learning Paths view: list paths, enroll, and for an enrolled path show each stage (module) with its linked courses, the per-stage lock/unlock state (existing gating), the next course to take, and the path certificate once every stage is complete. Opening a course from a stage SHALL navigate to the existing course player; stage completion updates as the user completes those courses.

#### Scenario: Path view reflects course progress

- **GIVEN** a user enrolled in a path whose first stage links one course
- **WHEN** the user completes that course
- **THEN** the path view shows the first stage complete and unlocks the next stage per gating
