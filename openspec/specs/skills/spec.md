# skills Specification

## Purpose

The Profile Skill Map: per-domain skill mastery + weak areas, derived
server-side from lesson completion blended with quiz performance. (src:
adapters/inbound/api/skills/router.py, domain/skills)

## Requirements

### Requirement: Skill mastery and weak areas

The system SHALL expose `GET /api/v1/skills/me` returning, per skill (a course
category; its `domain` is the parent category or itself when top-level), a
`mastery` (0..100), `courseCount`, and `weak` flag, plus `weakAreas` and
next-step `suggestions`. Mastery SHALL be `round(100·(0.6·lessonCompletion +
0.4·bestQuizAvg))` over published courses, dropping the quiz term when no quiz
was attempted. A skill the learner has engaged with (`courseCount > 0`)
scoring below 40 SHALL be `weak`. Suggestions SHALL be drawn from the weakest
skills first, capped at 5. Skills SHALL be ordered by domain then name.

#### Scenario: Blended mastery

- GIVEN a skill with full lesson completion and a best quiz score of 80
- WHEN the Skill Map is read
- THEN its mastery is 92

#### Scenario: Weak skill surfaced with a suggestion

- GIVEN a skill at 25% the learner has engaged with
- WHEN the Skill Map is read
- THEN the skill is flagged `weak`, listed in `weakAreas`, and contributes a next-step course suggestion
