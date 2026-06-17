# recommendations Specification

## Purpose

Recommend next courses to a learner via a deterministic ranking plus an LLM
narrative intro. (src: adapters/inbound/api/recommendations/router.py,
application/recommendations)

## Requirements

### Requirement: Deterministic ranking with LLM narrative

The system SHALL expose `GET /api/v1/recommendations/me` for the authenticated
learner. It SHALL infer a target level (Beginner with no progress;
Intermediate with module/quiz progress; Advanced after a completed path or
certificate), rank published courses by `(mandatory first, distance to target
level, lower level, sort_order)`, cap the shortlist (default 3), attach a
per-course reason, and add an LLM-written motivational summary. When the
published catalogue is empty, the shortlist SHALL be empty and a fixed
"no published courses yet" summary returned WITHOUT calling the LLM.

#### Scenario: Beginner gets easiest first

- GIVEN a fresh learner and a mixed-level catalogue
- WHEN they GET `/api/v1/recommendations/me`
- THEN the shortlist is ordered Beginner→Advanced with a non-empty summary

#### Scenario: Mandatory ranks first

- GIVEN a mandatory Advanced course and an optional Beginner course
- WHEN a fresh learner reads recommendations
- THEN the mandatory course is first with reason "Required course"

#### Scenario: Empty catalogue skips the LLM

- GIVEN no published courses
- WHEN a learner reads recommendations
- THEN courses is empty and the fixed "no published courses yet" summary is returned with no LLM call
