# agent-chat Specification

## Purpose

Global Agent Chat: a top-level assistant a signed-in learner can ask anything
with no course open. Unlike the lesson-anchored Socratic tutor it answers
directly, is aware of the learner's own history (learner-context tools), accepts
images, points each answer at the covering course/lesson (catalog match), and
logs out-of-catalog topics to the demand registry. Reuses the chat session
store. (src: adapters/inbound/api/agent_chat/router.py, application/agent_chat)

## Requirements

### Requirement: History-aware direct-answer turn

The system SHALL run an answer turn (`POST /api/v1/agent/sessions/{id}/messages`)
for a signed-in learner that answers directly (a distinct answer-mode persona,
not Socratic) and MAY call learner-context tools — the learner's own course
progress, active tracks/paths, and recommendations — to ground answers about
their learning, scoped to the authenticated user only. Text turns SHALL count
toward the AI-message quota (#230). Attached upload ids (incl. a photographed
question) SHALL be ingested (text/vision) and grounded. An unknown session
SHALL return `404`; an unauthenticated caller SHALL be refused (`401`/`403`).

#### Scenario: Reflects real progress

- GIVEN a learner who has completed some courses
- WHEN they ask "what have I finished / what next?"
- THEN the answer reflects their real progress and active track via the learner-context tools

### Requirement: Course routing with each answer

With each answer the system SHALL return the covering course/lesson via the
catalog semantic match (the #231 matcher) as ranked, deep-linkable `courseRefs`
(`{courseSlug, lessonId?, score, matchReason}`).

#### Scenario: Photographed question answered with a covering course

- GIVEN a learner attaches a photographed question
- WHEN the agent answers
- THEN the reply includes ranked `courseRefs` pointing at the covering course/lesson

### Requirement: Unavailable-topic capture

When no course clears the relevance threshold, the system SHALL still answer
best-effort AND record the topic to the demand registry (#232) as an
agent-sourced request, echoing an `unmatchedTopic` (topic + subject) in the
response.

#### Scenario: Out-of-catalog topic is recorded

- GIVEN the learner asks about a topic no course covers
- WHEN the agent answers
- THEN `unmatchedTopic` is returned and a course request is recorded for authors
