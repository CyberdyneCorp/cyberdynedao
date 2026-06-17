# quizzes Specification

## Purpose

Lesson-attached assessments: editor authoring, a learner player that never
leaks answers, server-side grading + attempt tracking, AI contextual
feedback, and a cross-lesson browse catalogue. (src:
adapters/inbound/api/quizzes/router.py, domain/quizzes, application/quizzes)

## Requirements

### Requirement: Editor authoring with structural invariants

The system SHALL allow an `editor` to upsert and delete a lesson's quiz
(`PUT`/`GET`/`DELETE /api/v1/admin/lessons/{lesson_id}/quiz`). A quiz SHALL
have 1–15 questions, each with 2–6 options and exactly one correct option, and
a passing score in 1..100 (default 70); violating any invariant SHALL return
`422`. A quiz is 1:1 with its lesson; a missing quiz SHALL return `404`.

#### Scenario: Invalid structure rejected

- GIVEN an upsert with a question having two correct options
- WHEN an editor submits it
- THEN the system SHALL respond `422` and store nothing

### Requirement: Answer-safe learner player

The system SHALL serve the quiz to a learner (`GET
/api/v1/lessons/{lesson_id}/quiz`) without `is_correct` flags or
explanations. Submitting an attempt (`POST …/quiz/attempts`) SHALL grade
server-side: `score = round(correct/total*100)`, `passed = score >=
passing_score`, unanswered counted wrong; an answer referencing an unknown
question/option SHALL return `422`. Each attempt SHALL get a monotonically
increasing `attempt_number`; a passing attempt SHALL auto-complete the lesson.

#### Scenario: Player view hides answers

- GIVEN a quiz exists
- WHEN a learner GETs the quiz
- THEN options carry no `is_correct` and questions carry no explanation

#### Scenario: Passing auto-completes the lesson

- GIVEN a quiz-type lesson with passing score 70
- WHEN a learner submits answers scoring 100
- THEN the attempt is `passed` and the lesson is marked 100% complete

#### Scenario: Attempt numbering increments

- GIVEN a learner who has submitted one attempt
- WHEN they submit a second
- THEN it has `attempt_number = 2` and both appear in attempt history (oldest first)

### Requirement: AI contextual feedback (read-only)

The system SHALL provide `POST /api/v1/lessons/{lesson_id}/quiz/feedback` that
grades the submitted answers WITHOUT recording an attempt and returns, per
question, the static explanation plus an LLM `ai_explanation` for incorrect
answers (`null` for correct ones).

#### Scenario: Feedback records no attempt

- GIVEN a learner with no prior attempts
- WHEN they request feedback on some answers
- THEN AI explanations are returned for wrong answers and the attempt history stays empty

### Requirement: Browse catalogue

The system SHALL expose `GET /api/v1/quizzes` listing quizzes from published
courses with lesson/course/category metadata, question count, and the
learner's most-recent attempt — filterable by `courseSlug` and `domain`
(category) and keyset-paged (`limit` 1..100 default 20, opaque `cursor`).

#### Scenario: Filtered, paged browse

- GIVEN published courses with quizzes
- WHEN a learner GETs `/api/v1/quizzes?courseSlug=python&limit=10`
- THEN only that course's quizzes are returned with a `nextCursor` when more remain
