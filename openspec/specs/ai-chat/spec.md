# ai-chat Specification

## Purpose

The AI Tutor: chat sessions (anonymous or authenticated), a tool-using agent
turn (non-streaming JSON and an SSE streaming twin), and history. (src:
adapters/inbound/api/ai_chat/router.py, application/ai_chat, docs/chat-streaming.md)

## Requirements

### Requirement: Sessions and history

The system SHALL create a chat session (`POST /api/v1/chat/sessions`) for an
anonymous (`user_id = null`) or authenticated caller, and return its messages
in order (`GET /api/v1/chat/sessions/{id}`). An unknown session SHALL return
`404`. Sessions SHALL be isolated; no cross-session history is exposed.

#### Scenario: Anonymous session

- GIVEN no auth token
- WHEN a client POSTs `/api/v1/chat/sessions`
- THEN a session is created with a null user and `201` is returned

#### Scenario: Unknown session history

- GIVEN a non-existent session id
- WHEN history is requested
- THEN the system SHALL respond `404`

### Requirement: Tool-using message turn

The system SHALL run a message turn (`POST /api/v1/chat/sessions/{id}/messages`,
content 1..4000 chars) that loops the LLM with the Cyberdyne tool set up to a
bounded number of tool rounds (4), persisting user/assistant/tool messages,
and returns the final assistant message. The tool set includes external source
tools — `web_search` (open-web search), `youtube_transcript`, and
`youtube_playlist` — so the agent can ground answers in the public web and
YouTube; each returns a bounded, JSON-stringified payload, and reports an
error result (never failing the turn) when its upstream is unavailable. An upstream LLM failure SHALL return
`502`; an unknown session SHALL return `404`. An optional
`interpreterSessionId` + `attachments` SHALL thread into tool dispatch; the
caller's bearer SHALL be forwarded to tools.

An `attachments` entry that is an upload id (`POST /api/v1/uploads`, issue
#220) SHALL be resolved and the turn grounded in its contents — text extracted
for PDF/DOCX/CSV/XLSX, a vision description for images — while an entry that is
an interpreter-workspace filename SHALL keep the existing read-in-workspace
behavior. The resolved attachments (id, filename, contentType) SHALL be echoed
on the message in history so the client can render attachment chips.

#### Scenario: Tool round then final answer

- GIVEN the LLM requests a tool then answers
- WHEN a turn runs
- THEN the tool is dispatched, results persisted, and the final assistant message returned

#### Scenario: Attachment grounds the reply

- GIVEN a learner uploads a PDF and sends a message with its `uploadId` in `attachments`
- WHEN the turn runs
- THEN the extracted text is inlined into the prompt and the message in history echoes the attachment metadata

#### Scenario: Tool-round cap

- GIVEN an LLM that always requests another tool
- WHEN a turn runs
- THEN the loop stops at the 4-round cap and returns the last assistant message

### Requirement: SSE streaming twin

The system SHALL provide `POST /api/v1/chat/sessions/{id}/messages/stream`
returning `text/event-stream`. Each event SHALL be one `data: <json>\n\n`
line whose `type` is `status` (tool round starting), `delta` (answer-text
chunk), `done` (terminal; carries the full persisted assistant message), or
`error` (in-band; HTTP stays 200). There SHALL be no `[DONE]` sentinel; the
terminal event SHALL be `done` or `error`, after zero+ `status` then zero+
`delta` events.

#### Scenario: Stream ordering

- GIVEN a turn that runs a tool then answers
- WHEN the stream is consumed
- THEN a `status` event precedes the `delta` events, ending with a single `done` event

#### Scenario: Error delivered in-band

- GIVEN the provider fails after the stream has opened
- WHEN streaming
- THEN an `error` event is emitted and the HTTP status remains 200

### Requirement: Per-IP rate limit on message turns

The system SHALL rate-limit the chat message endpoints
(`POST .../messages` and `.../messages/stream`) per client IP — a coarse
guard against a single client burning LLM tokens in a loop. Exceeding the
limit SHALL return `429`. The limit is in-memory and per-replica; a request
with no resolvable client IP SHALL be allowed through.

#### Scenario: Too many messages

- GIVEN a client has reached the per-IP message limit within the window
- WHEN it posts another chat message
- THEN the system SHALL respond `429`
