# achievements Specification

## Purpose

Badges with deterministic award rules: earned + in-progress achievements with
progress toward unearned ones, awarded on read. (src:
adapters/inbound/api/achievements/router.py, domain/achievements)

## Requirements

### Requirement: Deterministic, metric-bound achievements

The system SHALL expose `GET /api/v1/achievements/me` returning every
achievement with `progress {current, target}` and an `earnedAt` (null while
in-progress). Each achievement SHALL bind a single metric (courses completed,
quizzes passed, perfect quizzes, certificates earned, modules completed) to a
target, and be earned when the metric value reaches the target; `current`
SHALL be capped at `target`. Metrics SHALL be aggregated read-only across the
courses/quizzes/learning tables.

#### Scenario: Fresh learner sees all in progress

- GIVEN a learner with no activity
- WHEN they GET `/api/v1/achievements/me`
- THEN every achievement has `earnedAt = null` and `current = 0`

#### Scenario: Threshold crossing earns the badge

- GIVEN a learner who has completed one course
- WHEN they read achievements
- THEN "First Steps" has a non-null `earnedAt` and higher-tier course badges remain in progress

### Requirement: Award-on-read idempotency

The system SHALL persist a newly-earned achievement with the current
timestamp the first time it is observed earned, so `earnedAt` is stable; a
subsequent read SHALL NOT re-award it or shift its timestamp.

#### Scenario: Stable earnedAt

- GIVEN an achievement earned on a prior read
- WHEN the learner reads achievements again
- THEN its `earnedAt` is unchanged and nothing is re-awarded
