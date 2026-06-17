# activity Specification

## Purpose

Record lightweight per-user learning activity events and derive the
Profile/Today metric tiles: study streak plus activity counts. (src:
adapters/inbound/api/activity/router.py, domain/activity)

## Requirements

### Requirement: Record activity events

The system SHALL accept `POST /api/v1/me/activity` from an authenticated user
with a `kind` (`lesson_viewed`/`code_run`/`simulation_run`/`concept_mastered`)
and optional `ref`. An unknown `kind` SHALL return `422`. Events SHALL be
immutable and user-scoped.

#### Scenario: Invalid kind

- GIVEN an authenticated user
- WHEN they POST an activity with `kind="bogus"`
- THEN the system SHALL respond `422`

### Requirement: Derived streak and counts

The system SHALL expose `GET /api/v1/me/stats` returning `currentStreakDays`,
`longestStreakDays`, `lastActiveOn`, `codeRunsCount`, `simulationsRun`, and
`conceptsMastered`. The current streak SHALL count consecutive calendar days
with at least one event, keeping a one-day grace (a streak holds if there was
activity yesterday but not yet today). Days SHALL bucket in UTC unless
`tzOffsetMinutes` is supplied (clamped to UTC-12..UTC+14). `conceptsMastered`
SHALL count distinct `concept_mastered` refs.

#### Scenario: Counts and same-day streak

- GIVEN a user records two `code_run`, one `simulation_run`, and `concept_mastered` for the same ref twice, all today
- WHEN they GET `/api/v1/me/stats`
- THEN `codeRunsCount=2`, `simulationsRun=1`, `conceptsMastered=1`, `currentStreakDays=1`

#### Scenario: Grace day

- GIVEN activity on the two days before today and none today
- WHEN stats are read
- THEN `currentStreakDays` still counts those two days

#### Scenario: Empty stats

- GIVEN a user with no activity
- WHEN they GET `/api/v1/me/stats`
- THEN all counts and streaks are 0 and `lastActiveOn` is null
