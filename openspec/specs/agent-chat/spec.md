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
progress, active tracks/paths, recommendations, and lesson notes (optionally
filtered to one course) — to ground answers about their learning, scoped to the
authenticated user only (the `user_id` is never a tool argument). The turn MAY
also call external source tools (`web_search`, `youtube_transcript`,
`youtube_playlist`) to ground answers in the public web and YouTube, each
returning a bounded payload and an error result (never failing the turn) when
its upstream is unavailable. Text turns SHALL count
toward the AI-message quota (#230). Attached upload ids (incl. a photographed
question) SHALL be ingested (text/vision) and grounded. An unknown session
SHALL return `404`; an unauthenticated caller SHALL be refused (`401`/`403`).

#### Scenario: Reflects real progress

- GIVEN a learner who has completed some courses
- WHEN they ask "what have I finished / what next?"
- THEN the answer reflects their real progress and active track via the learner-context tools

### Requirement: Proposed Notebook actions (client-committed)

The turn SHALL include a structured `notebookAction` when (and only when) the
learner asks to save or synthesize something into their Notebook (e.g. "make a
mindmap of my Algorithms notes and save it") — `{op: create|append, title?,
type?, targetNoteId?, body}` (mindmaps as a fenced `mermaid` block in `body`). The
backend SHALL only PROPOSE: it performs NO notebook write/append/delete; the
client commits via the notebook endpoints after the learner confirms. Ordinary
Q&A turns SHALL omit `notebookAction`. An `append` proposal SHALL carry a
`targetNoteId`.

#### Scenario: Save-to-Notebook request yields a proposed action

- GIVEN a learner asks to make a mindmap of a course's notes and save it
- WHEN the agent answers (after reading their notes via `get_my_notes`)
- THEN the response includes `notebookAction{op:"create", body:<mermaid mindmap>}` and no server-side write occurs

#### Scenario: Ordinary question has no action

- GIVEN an ordinary question
- WHEN the agent answers
- THEN `notebookAction` is omitted

### Requirement: Course routing with each answer

With each answer the system SHALL return the covering course/lesson via the
catalog semantic match (the #231 matcher) as ranked, deep-linkable `courseRefs`
(`{courseSlug, lessonId?, score, matchReason}`).

#### Scenario: Photographed question answered with a covering course

- GIVEN a learner attaches a photographed question
- WHEN the agent answers
- THEN the reply includes ranked `courseRefs` pointing at the covering course/lesson

### Requirement: Session history read

The system SHALL expose `GET /api/v1/agent/sessions/{id}` returning the
session's messages oldest-first. It SHALL accept an optional `limit` (1..200)
that returns the most-recent `limit` messages (still chronological) plus a
`nextCursor`, and an optional `before` cursor (the prior `nextCursor`) to page
backwards into older history. Omitting `limit` SHALL return the full history
unchanged, and `nextCursor` SHALL be additive (`null` when unpaged or when the
oldest message is included) so existing clients are unaffected. The same
contract applies to the tutor history read (`GET /api/v1/chat/sessions/{id}`).

#### Scenario: Recent page with backward cursor

- GIVEN a session with several turns of history
- WHEN a client GETs the session with `limit=2`
- THEN the two most-recent messages are returned with a `nextCursor`, and
  passing it back as `before` returns the preceding (older) page

### Requirement: Unavailable-topic capture

When no course clears the relevance threshold, the system SHALL still answer
best-effort AND record the topic to the demand registry (#232) as an
agent-sourced request, echoing an `unmatchedTopic` (topic + subject) in the
response.

#### Scenario: Out-of-catalog topic is recorded

- GIVEN the learner asks about a topic no course covers
- WHEN the agent answers
- THEN `unmatchedTopic` is returned and a course request is recorded for authors
