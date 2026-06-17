# analytics Specification

## Purpose

Read-only reporting: a learner's own dashboard and a platform-wide admin
overview, aggregated across the learning, courses, and quizzes tables. (src:
adapters/inbound/api/analytics/router.py, domain/analytics, persistence/analytics)

## Requirements

### Requirement: Learner dashboard

The system SHALL expose `GET /api/v1/analytics/me` for the authenticated
learner, returning counts derived from their data: enrolled/completed/active
paths, completed/in-progress modules, average module percent, quizzes
attempted/passed, quiz pass rate, average best quiz score, total quiz
attempts, certificates, and completed/in-progress courses. Rates and averages
SHALL be `0.0` when there is no data (zero denominator).

#### Scenario: Fresh learner reads zeros

- GIVEN a learner with no activity
- WHEN they GET `/api/v1/analytics/me`
- THEN all counts are 0 and all rates are 0.0

#### Scenario: Mixed activity aggregates correctly

- GIVEN a learner with one 100% module and one 50% module
- WHEN they read the dashboard
- THEN `avg_module_percent` is 75.0 and `completed_modules` is 1

### Requirement: Admin overview

The system SHALL expose `GET /api/v1/admin/analytics/overview` to an `editor`,
returning platform KPIs: total learners, total/completed enrollments +
completion rate, published/draft courses, total modules/paths/certificates,
total quiz attempts, quiz pass rate, and average quiz score.

#### Scenario: Platform KPIs

- GIVEN 2 enrollments (1 completed) across the platform
- WHEN an editor GETs the overview
- THEN `enrollment_completion_rate` is 50.0
